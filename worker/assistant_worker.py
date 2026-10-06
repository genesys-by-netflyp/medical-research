#!/usr/bin/env python3
"""Pre-print Assistant backend worker.

Queue mechanics for the assistant service (site/migrations/002, 003).
The pipeline itself is executed by the Hermes research pipeline
(medical-research-pipeline skill) inside the claimed project folder.

Commands:
  queue                     show queued/processing submissions
  claim [--limit 2]         claim up to N queued jobs (atomic, skip locked);
                            scaffolds a project dir under runs/ and prints job JSON
  complete ID --dir DIR     upload files in DIR to private storage under
                            <user_id>/<id>/ and mark the job 'review'
  fail ID --note "..."      mark failed, auto-refund credit
  nogo ID --note "..." [--report path.json]   feasibility-gate rejection, refund

Secrets come from ~/.hermes/secrets/medical-research.env (never print).
"""
import argparse, json, os, sys, urllib.request, urllib.error
from pathlib import Path

SECRETS = {}
for line in open(os.path.expanduser("~/.hermes/secrets/medical-research.env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        SECRETS[k.strip()] = v.strip()

URL = SECRETS["SUPABASE_URL"].rstrip("/")
SRK = SECRETS["SUPABASE_SERVICE_ROLE_KEY"]
RUNS = Path(os.environ.get("ASSISTANT_RUNS", "/opt/data/medical-research/worker/runs"))
BUCKET = "assistant-deliveries"


def rest(method, path, body=None):
    req = urllib.request.Request(
        URL + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": "Bearer " + SRK,
            "apikey": SRK,
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
        method=method,
    )
    try:
        r = urllib.request.urlopen(req, timeout=60)
        raw = r.read().decode()
        return r.status, json.loads(raw) if raw.strip() else None
    except urllib.error.HTTPError as e:
        raise SystemExit(f"REST {method} {path} -> {e.code}: {e.read().decode()[:400]}")


def rpc(name, params):
    return rest("POST", "/rest/v1/rpc/" + name, params)


def storage_upload(bucket, object_path, local_path):
    """Raw upload via the storage REST API (service role)."""
    data = Path(local_path).read_bytes()
    req = urllib.request.Request(
        f"{URL}/storage/v1/object/{bucket}/{object_path}",
        data=data,
        headers={
            "Authorization": "Bearer " + SRK,
            "apikey": SRK,
            "Content-Type": "application/octet-stream",
            "x-upsert": "true",
        },
        method="POST",
    )
    r = urllib.request.urlopen(req, timeout=120)
    return r.status, r.read().decode()[:200]


def scaffold(job):
    d = RUNS / job["id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "job.json").write_text(json.dumps(job, indent=2))
    (d / "deliverables").mkdir(exist_ok=True)
    (d / "dossier").mkdir(exist_ok=True)
    (d / "README.md").write_text(
        f"# Assistant job {job['id']}\n\n"
        f"Title: {job['title']}\nType: {job['paper_type']}\nUser: {job['user_id']}\n\n"
        "Run the medical-research-pipeline in this folder.\n"
        "Put the manuscript (+ any figures) in deliverables/ and the human-review\n"
        "packet (human_reviewer_checklist, audit_trail, references, search_log,\n"
        "extraction sheets) in dossier/. Then:\n"
        f"  assistant_worker.py complete {job['id']} --dir {d}\n"
    )
    return d


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("queue")
    c = sub.add_parser("claim"); c.add_argument("--limit", type=int, default=2)
    m = sub.add_parser("complete"); m.add_argument("id"); m.add_argument("--dir", required=True)
    f = sub.add_parser("fail"); f.add_argument("id"); f.add_argument("--note", required=True)
    n = sub.add_parser("nogo"); n.add_argument("id"); n.add_argument("--note", required=True)
    n.add_argument("--report")
    a = ap.parse_args()

    if a.cmd == "queue":
        _, rows = rest("GET", "/rest/v1/assistant_submissions?select=id,user_id,paper_type,title,status,created_at,started_at&order=created_at")
        for r in rows or []:
            print(f"{r['status']:<10} {r['id']}  [{r['paper_type']}] {r['title'][:80]}")
        if not rows:
            print("(queue empty)")

    elif a.cmd == "claim":
        _, jobs = rpc("claim_assistant_jobs", {"p_worker": "hermes", "p_limit": a.limit})
        for j in jobs or []:
            d = scaffold(j)
            print(f"CLAIMED {j['id']} -> {d}")
        if not jobs:
            print("(nothing queued)")

    elif a.cmd == "complete":
        _, job = rest("GET", "/rest/v1/assistant_submissions?id=eq." + a.id)
        if not job:
            raise SystemExit(f"No submission {a.id}")
        job = job[0]
        deliverables, dossier = [], []
        for group, key in (("deliverables", "deliverable_paths"), ("dossier", "dossier_paths")):
            gdir = Path(a.dir) / group
            for p in sorted(gdir.glob("*")) if gdir.exists() else []:
                opath = f"{job['user_id']}/{a.id}/{p.name}"
                storage_upload(BUCKET, opath, p)
                (deliverables if group == "deliverables" else dossier).append(
                    {"path": opath, "name": p.name})
        rpc("complete_assistant_job", {"p_id": a.id, "p_deliverables": deliverables,
                                       "p_dossier": dossier, "p_note": "uploaded by worker"})
        print(f"COMPLETED {a.id}: {len(deliverables)} deliverable(s), {len(dossier)} dossier file(s)")

    elif a.cmd == "fail":
        rpc("fail_assistant_job", {"p_id": a.id, "p_note": a.note, "p_refund": True})
        print(f"FAILED {a.id} (credit refunded)")

    elif a.cmd == "nogo":
        report = json.load(open(a.report)) if a.report else None
        rpc("nogo_assistant_job", {"p_id": a.id, "p_report": report, "p_note": a.note})
        print(f"NO-GO {a.id} (credit refunded)")


if __name__ == "__main__":
    main()
