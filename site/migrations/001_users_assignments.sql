-- Migration 001: single-role 'User' model, assignments, structured reviews
-- All review artifacts public; capability comes from per-paper assignment, not account type.

-- 1. PROFILES: linked to Supabase auth.users. One account type; vetting = approved flag.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  full_name text not null,
  credentials text,
  registration_no text,
  organisation text,
  specialty text,
  position text,
  country text,
  orcid text,
  bio text,
  approved boolean not null default false,        -- vetted by admins; gates assignment
  is_admin boolean not null default false,
  email text not null
);

-- 2. ASSIGNMENTS: per-paper capability, fully public (open auditing).
create table if not exists public.assignments (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  paper_id uuid not null references public.papers(id) on delete cascade,
  user_id uuid not null references public.profiles(id) on delete cascade,
  capacity text not null check (capacity in ('claimant','reviewer')),
  status text not null default 'assigned' check (status in ('assigned','in_progress','submitted','withdrawn')),
  assigned_at timestamptz not null default now(),
  unique (paper_id, user_id, capacity)
);

-- 3. REVIEWS: link to auth user + assignment; add structured substantive content.
alter table public.reviews
  add column if not exists user_id uuid references public.profiles(id),
  add column if not exists assignment_id uuid references public.assignments(id),
  add column if not exists structured jsonb,
  add column if not exists coi_statement text;

-- 4. COMPLETENESS: a submitted review must carry the structured payload.
alter table public.reviews
  add constraint reviews_structured_present check (structured is not null or reviewer_id is not null);

-- 5. STATUS AUTOMATION: assignment opens review; last required review completes paper.
create or replace function public.on_assignment_status()
returns trigger language plpgsql as $$
begin
  if new.status = 'in_progress' then
    update public.papers set status = 'in_review' where id = new.paper_id and status = 'awaiting_review';
  end if;
  return new;
end $$;

drop trigger if exists trg_assignment_status on public.assignments;
create trigger trg_assignment_status after update of status on public.assignments
for each row execute function public.on_assignment_status();

-- 6. HELPER: can paper be marked peer_reviewed? (all active reviewer assignments have submitted)
create or replace function public.paper_review_complete(pid uuid)
returns boolean language sql stable as $$
  select not exists (
    select 1 from public.assignments a
    where a.paper_id = pid and a.capacity = 'reviewer' and a.status in ('assigned','in_progress')
  ) and exists (
    select 1 from public.assignments a
    where a.paper_id = pid and a.capacity = 'reviewer' and a.status = 'submitted'
  );
$$;

-- 7. AUTO-FLIP: when a review is inserted and every reviewer assignment is submitted, mark paper peer_reviewed.
create or replace function public.on_review_insert()
returns trigger language plpgsql as $$
begin
  update public.assignments set status = 'submitted'
  where id = new.assignment_id and status in ('assigned','in_progress');
  update public.papers set status = 'peer_reviewed', published_at = coalesce(published_at, now())
  where id = new.paper_id and public.paper_review_complete(new.paper_id) and status != 'peer_reviewed';
  return new;
end $$;

drop trigger if exists trg_review_insert on public.reviews;
create trigger trg_review_insert after insert on public.reviews
for each row execute function public.on_review_insert();

-- 8. RLS: the open-audit premise — everything readable by anon; writes gated.
alter table public.profiles enable row level security;
alter table public.assignments enable row level security;

drop policy if exists profiles_public_read on public.profiles;
create policy profiles_public_read on public.profiles for select using (true);

drop policy if exists profiles_self_insert on public.profiles;
create policy profiles_self_insert on public.profiles for insert to authenticated
  with check (auth.uid() = id);

drop policy if exists profiles_self_update on public.profiles;
create policy profiles_self_update on public.profiles for update to authenticated
  using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists assignments_public_read on public.assignments;
create policy assignments_public_read on public.assignments for select using (true);

-- only admins (is_admin) create assignments; users update own assignment status
drop policy if exists assignments_admin_write on public.assignments;
create policy assignments_admin_write on public.assignments for insert to authenticated
  with check (exists (select 1 from public.profiles p where p.id = auth.uid() and p.is_admin));

drop policy if exists assignments_self_update on public.assignments;
create policy assignments_self_update on public.assignments for update to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- reviews already have anon insert (legacy form); keep public write but require approved profile for structured ones
drop policy if exists reviews_public_read on public.reviews;
create policy reviews_public_read on public.reviews for select using (true);

drop policy if exists reviews_authored_insert on public.reviews;
create policy reviews_authored_insert on public.reviews for insert to authenticated
  with check (auth.uid() = user_id and exists (
    select 1 from public.profiles p where p.id = auth.uid() and p.approved
  ));

-- 9. INDEXES
create index if not exists idx_assignments_paper on public.assignments(paper_id);
create index if not exists idx_assignments_user on public.assignments(user_id);
create index if not exists idx_reviews_paper on public.reviews(paper_id);
create index if not exists idx_profiles_email on public.profiles(email);
