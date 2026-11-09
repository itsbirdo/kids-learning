#!/usr/bin/env python3
"""Create the planned GitHub issues from docs/issues/*.md using the GitHub CLI.

Usage:
    python3 docs/issues/create_issues.py --repo OWNER/REPO [--ref main] [--dry-run] [--no-type]

Requires `gh` authenticated with write access to the repository. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

LABELS = {
    "epic": ("5319e7", "Tracking issue for the whole build"),
    "decision": ("0e8a16", "Architecture or product decision record"),
    "spike": ("fbca04", "Time-boxed investigation"),
    "phase-0-foundations": ("c5def5", "Phase 0: decisions, scaffolding, spike"),
    "phase-1-content": ("c5def5", "Phase 1: curriculum, content tooling, audio, images"),
    "phase-2-core-app": ("c5def5", "Phase 2: offline core app"),
    "phase-3-speaking": ("c5def5", "Phase 3: speaking checks and scoring"),
    "phase-4-dynamic-voice": ("c5def5", "Phase 4: dynamic speech and custom words"),
    "phase-5-conversation": ("c5def5", "Phase 5: optional scripted conversation practice"),
    "phase-6-ship": ("c5def5", "Phase 6: release and platforms"),
    "phase-7-german": ("c5def5", "Phase 7: German course (second language pack)"),
    "cross-cutting": ("bfdadc", "Applies across phases"),
    "area: app": ("1d76db", "Flutter app"),
    "area: speech": ("1d76db", "Speech in/out, scoring"),
    "area: content": ("1d76db", "Lessons, audio, images"),
    "area: infra": ("1d76db", "Tooling, CI, gateway, release"),
    "area: safety": ("b60205", "Privacy, terms, child safety"),
    "android": ("3ddc84", "Android-specific"),
    "ios": ("aaaaaa", "iOS/iPadOS-specific"),
}

REF_RE = re.compile(r"(?<![\w/&])#(\d+)\b")


def parse_spec(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path.name}: missing front matter")
    meta: dict = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("["):
            items = [v.strip().strip('"').strip("'") for v in value.strip("[]").split(",")]
            meta[key.strip()] = [i for i in items if i]
        elif value in ("null", ""):
            meta[key.strip()] = None
        else:
            meta[key.strip()] = value.strip('"')
    meta["planned_number"] = int(meta["planned_number"])
    meta["parent"] = int(meta["parent"]) if meta.get("parent") else None
    meta["body"] = m.group(2).lstrip("\n")
    meta["file"] = path.name
    return meta


def absolutize_links(body: str, repo: str, ref: str) -> str:
    base = f"https://github.com/{repo}/blob/{ref}/docs/"
    tree = f"https://github.com/{repo}/tree/{ref}/docs/"

    def repl(m: re.Match) -> str:
        target = m.group(2)
        if target.startswith(("http://", "https://", "#")):
            return m.group(0)
        if target.startswith("../"):
            rel = target[3:]
        else:
            rel = "issues/" + target
        url = (tree if rel.endswith("/") else base) + rel
        return f"[{m.group(1)}]({url})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, body)


def remap_refs(body: str, mapping: dict[int, int]) -> str:
    return REF_RE.sub(lambda m: f"#{mapping.get(int(m.group(1)), int(m.group(1)))}", body)


def gh_api(args: list[str], dry: bool) -> dict:
    cmd = ["gh", "api", *args]
    if dry:
        print("DRY:", " ".join(a if len(a) < 80 else a[:77] + "..." for a in cmd))
        return {}
    out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else {}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", default="main", help="git ref used for links to docs")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-type", action="store_true", help="skip GitHub issue types")
    a = ap.parse_args()

    specs = sorted((parse_spec(p) for p in HERE.glob("[0-9][0-9]-*.md")), key=lambda s: s["planned_number"])
    print(f"{len(specs)} specs found")

    for name, (color, desc) in LABELS.items():
        cmd = ["gh", "label", "create", name, "--repo", a.repo, "--color", color, "--description", desc, "--force"]
        if a.dry_run:
            print("DRY:", " ".join(cmd))
        else:
            subprocess.run(cmd, check=True, capture_output=True, text=True)

    created: dict[int, dict] = {}
    for s in specs:
        body = absolutize_links(s["body"], a.repo, a.ref)
        args = [f"repos/{a.repo}/issues", "-X", "POST", "-f", f"title={s['title']}", "-f", f"body={body}"]
        for label in s.get("labels") or []:
            args += ["-f", f"labels[]={label}"]
        if s.get("type") and not a.no_type:
            args += ["-f", f"type={s['type']}"]
        res = gh_api(args, a.dry_run)
        number = res.get("number", s["planned_number"])
        created[s["planned_number"]] = {"number": number, "id": res.get("id"), "body": body, "spec": s}
        print(f"#{number}  {s['title']}" + ("" if number == s["planned_number"] else f"  (planned #{s['planned_number']})"))

    mapping = {k: v["number"] for k, v in created.items()}
    if any(k != v for k, v in mapping.items()):
        print("Numbers differ from plan; rewriting cross-references…")
        for info in created.values():
            new_body = remap_refs(info["body"], mapping)
            if new_body != info["body"]:
                gh_api([f"repos/{a.repo}/issues/{info['number']}", "-X", "PATCH", "-f", f"body={new_body}"], a.dry_run)

    for info in created.values():
        parent = info["spec"]["parent"]
        if parent and not a.dry_run:
            gh_api([f"repos/{a.repo}/issues/{mapping[parent]}/sub_issues", "-X", "POST",
                    "-F", f"sub_issue_id={info['id']}"], a.dry_run)
        elif parent:
            print(f"DRY: link #{info['number']} as sub-issue of #{mapping[parent]}")
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr or str(e))
        raise SystemExit(1)
