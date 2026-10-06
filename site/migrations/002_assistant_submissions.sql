-- Migration 002: Pre-print Assistant service (pay-per-use, credit-based)
-- Users submit titles (case series / SR-MA); 1 credit per submission;
-- backend worker processes 1-2 at a time; deliverables go to Supabase Storage
-- bucket 'assistant-deliveries', private per user (path prefix = user_id).
-- NOTE (product pivot 2026-10): assistant deliverables are DRAFT manuscripts +
-- verification dossiers delivered privately to the requester, framed as
-- AI-assisted with human verification per journal policy. Public preprint
-- publication rules (migration 001) remain unchanged.

-- 1. CREDITS: one balance row per user. Admin grants credits; RPC spends them.
create table if not exists public.assistant_credits (
  user_id uuid primary key references public.profiles(id) on delete cascade,
  balance integer not null default 0 check (balance >= 0),
  updated_at timestamptz not null default now()
);

-- 2. SUBMISSIONS: private to the owner. Users never insert/update directly;
-- the RPC (security definer) is the only user-facing write path.
create table if not exists public.assistant_submissions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  paper_type text not null check (paper_type in ('case-series','sr-ma')),
  title text not null check (length(trim(title)) between 10 and 400),
  status text not null default 'queued'
    check (status in ('queued','processing','review','complete','failed','no-go','cancelled')),
  status_note text,
  topic_report jsonb,
  deliverable_paths jsonb,   -- [{path, name}] in storage bucket
  dossier_paths jsonb,       -- human-review documents: checklist, audit trail, references
  created_at timestamptz not null default now(),
  started_at timestamptz,
  completed_at timestamptz
);

create index if not exists idx_submissions_user on public.assistant_submissions(user_id);
create index if not exists idx_submissions_status on public.assistant_submissions(status);

-- 3. SUBMISSION RPC: atomic credit spend + insert. Refunds happen only via
-- admin/worker on 'failed' or 'no-go' (see refund RPC below).
create or replace function public.submit_assistant_request(p_paper_type text, p_title text)
returns uuid language plpgsql security definer set search_path = public as $$
declare
  uid uuid := auth.uid();
  sid uuid;
begin
  if uid is null then
    raise exception 'Not signed in';
  end if;
  if not exists (select 1 from public.profiles where id = uid and approved) then
    raise exception 'Account is not approved yet. Assistant submissions require vetting.';
  end if;
  if p_paper_type not in ('case-series','sr-ma') then
    raise exception 'Invalid paper type';
  end if;
  -- spend credit atomically
  update public.assistant_credits
     set balance = balance - 1, updated_at = now()
   where user_id = uid and balance > 0;
  if not found then
    raise exception 'No credits available. Each submission costs 1 credit ($99.99).';
  end if;
  insert into public.assistant_submissions(user_id, paper_type, title)
  values (uid, p_paper_type, trim(p_title))
  returning id into sid;
  return sid;
end $$;

-- 4. REFUND RPC (service-role/admin): failed or no-go submissions return the credit.
create or replace function public.refund_assistant_credit(p_submission uuid)
returns void language plpgsql security definer set search_path = public as $$
declare
  r record;
begin
  select * into r from public.assistant_submissions where id = p_submission;
  if r.id is null then raise exception 'Submission not found'; end if;
  if r.status not in ('failed','no-go') then
    raise exception 'Only failed/no-go submissions are refundable';
  end if;
  if r.status_note like '%refunded%' then
    raise exception 'Already refunded';
  end if;
  insert into public.assistant_credits(user_id, balance)
  values (r.user_id, 1)
  on conflict (user_id) do update set balance = assistant_credits.balance + 1, updated_at = now();
  update public.assistant_submissions
     set status_note = coalesce(status_note,'') || ' [credit refunded]'
   where id = p_submission;
end $$;

-- 5. ADMIN GRANT RPC: add credits to a user (admin-only via authenticated check;
-- the worker uses the service-role key which bypasses RLS anyway).
create or replace function public.admin_grant_assistant_credits(p_user uuid, p_amount int)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from public.profiles where id = auth.uid() and is_admin) then
    raise exception 'Admin only';
  end if;
  if p_amount is null or p_amount < 1 or p_amount > 50 then
    raise exception 'Amount must be 1-50';
  end if;
  insert into public.assistant_credits(user_id, balance) values (p_user, p_amount)
  on conflict (user_id) do update set balance = assistant_credits.balance + p_amount, updated_at = now();
end $$;

-- 6. RLS
alter table public.assistant_credits enable row level security;
alter table public.assistant_submissions enable row level security;

drop policy if exists assistant_credits_self_read on public.assistant_credits;
create policy assistant_credits_self_read on public.assistant_credits for select to authenticated
  using (auth.uid() = user_id);

drop policy if exists assistant_submissions_owner_read on public.assistant_submissions;
create policy assistant_submissions_owner_read on public.assistant_submissions for select to authenticated
  using (auth.uid() = user_id
         or exists (select 1 from public.profiles p where p.id = auth.uid() and p.is_admin));

-- No user insert/update policies: writes go through the security-definer RPCs
-- and the worker's service-role key only.

-- 7. STORAGE: private bucket; owner reads/writes only own prefix.
insert into storage.buckets (id, name, public)
values ('assistant-deliveries', 'assistant-deliveries', false)
on conflict (id) do nothing;

drop policy if exists "assistant owner read" on storage.objects;
create policy "assistant owner read" on storage.objects for select to authenticated
  using (bucket_id = 'assistant-deliveries' and auth.uid()::text = (storage.foldername(name))[1]);

drop policy if exists "assistant owner write" on storage.objects;
create policy "assistant owner write" on storage.objects for insert to authenticated
  with check (bucket_id = 'assistant-deliveries' and auth.uid()::text = (storage.foldername(name))[1]);
