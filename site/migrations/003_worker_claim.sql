-- Migration 003: worker RPCs for the Pre-print Assistant queue.
-- All service-role only: revoke from anon/authenticated so only the backend
-- worker (service key) can claim/complete/fail jobs.

create or replace function public.claim_assistant_jobs(p_worker text, p_limit int default 2)
returns setof public.assistant_submissions
language plpgsql security definer set search_path = public as $$
begin
  return query
  update public.assistant_submissions s
     set status = 'processing', started_at = now()
   where s.id in (
     select id from public.assistant_submissions
      where status = 'queued'
      order by created_at
      limit greatest(1, least(p_limit, 5))
      for update skip locked)
   returning s.*;
end $$;

create or replace function public.complete_assistant_job(
  p_id uuid, p_deliverables jsonb, p_dossier jsonb, p_note text default null)
returns void language plpgsql security definer set search_path = public as $$
begin
  update public.assistant_submissions
     set status = 'review',
         deliverable_paths = p_deliverables,
         dossier_paths = p_dossier,
         status_note = coalesce(p_note, status_note),
         completed_at = now()
   where id = p_id and status = 'processing';
  if not found then raise exception 'Job % not in processing state', p_id; end if;
end $$;

create or replace function public.fail_assistant_job(p_id uuid, p_note text, p_refund bool default true)
returns void language plpgsql security definer set search_path = public as $$
declare r record;
begin
  update public.assistant_submissions
     set status = 'failed', status_note = coalesce(p_note, 'production failed'), completed_at = now()
   where id = p_id and status in ('processing','queued');
  if not found then raise exception 'Job % not claimable/failed', p_id; end if;
  if p_refund then perform public.refund_assistant_credit(p_id); end if;
end $$;

create or replace function public.nogo_assistant_job(p_id uuid, p_report jsonb, p_note text)
returns void language plpgsql security definer set search_path = public as $$
begin
  update public.assistant_submissions
     set status = 'no-go', topic_report = p_report,
         status_note = coalesce(p_note, 'feasibility gate: insufficient full-text sources'),
         completed_at = now()
   where id = p_id and status in ('processing','queued');
  if not found then raise exception 'Job % not claimable/no-go-able', p_id; end if;
  perform public.refund_assistant_credit(p_id);
end $$;

-- Lock these down: service_role only.
revoke execute on function public.claim_assistant_jobs(text,int) from public, anon, authenticated;
revoke execute on function public.complete_assistant_job(uuid,jsonb,jsonb,text) from public, anon, authenticated;
revoke execute on function public.fail_assistant_job(uuid,text,bool) from public, anon, authenticated;
revoke execute on function public.nogo_assistant_job(uuid,jsonb,text) from public, anon, authenticated;
revoke execute on function public.refund_assistant_credit(uuid) from public, anon, authenticated;
