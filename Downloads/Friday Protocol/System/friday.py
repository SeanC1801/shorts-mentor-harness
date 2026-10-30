#!/usr/bin/env python3
"""
Friday — a comprehension gate for AI-assisted code.

The build artifact is your understanding, not the code.
A slice is done when you can explain it without looking.

Zero dependencies. Python 3.8+. Works in any repo, any language.
Full protocol: see PROTOCOL.md
"""

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

VERSION = "0.1.0"
DIR = ".friday"
STATE_FILE = os.path.join(DIR, "state.json")
CONFIG_FILE = os.path.join(DIR, "config.json")

TIERS = ("spine", "organs", "leaves")
STATES = ("dark", "taught", "understood", "stale", "debt")

# States that block a commit. `debt` is deliberately absent: the override
# is never blocked, only recorded.
BLOCKING = ("dark", "stale")

DEFAULT_CONFIG = {
    "fluent_languages": [".py"],
    "gate_tiers": ["spine", "organs"],
    "size_promotion_bytes": 30720,
    "decay_days": {"taught": 3, "understood": 30},
    "tiers": {
        "spine": [
            "**/models.py", "**/schemas.py", "**/schema.*", "**/models/**",
            "**/entities/**", "**/domain/**", "**/migrations/**",
            "**/auth*", "**/*state*", "**/db.*", "**/database.*",
        ],
        "organs": [
            "**/main.*", "**/app.*", "**/server.*", "**/index.js", "**/index.ts",
            "**/routes/**", "**/api/**", "**/services/**", "**/controllers/**",
            "**/handlers/**", "**/*.py", "**/*.js", "**/*.ts", "**/*.go",
            "**/*.rs", "**/*.java", "**/*.rb", "**/*.php",
        ],
        "leaves": [
            "**/*.css", "**/*.scss", "**/*.html", "**/*.md", "**/*.txt",
            "**/*.json", "**/*.yml", "**/*.yaml", "**/*.toml", "**/*.lock",
            "**/*.svg", "**/*.png", "**/*.jpg", "**/*.ico",
            "**/test/**", "**/tests/**", "**/*_test.*", "**/*.test.*",
            "**/static/**", "**/assets/**", "**/templates/**", "**/vendor/**",
        ],
    },
    "ignore": [
        "**/node_modules/**", "**/.git/**", "**/venv/**", "**/.venv/**",
        "**/__pycache__/**", "**/dist/**", "**/build/**", "**/.friday/**",
    ],
}

# Run-command reconciliation: what a stated command implies must exist.
RUNTIME_EVIDENCE = {
    "npm": ["package.json"],
    "yarn": ["package.json"],
    "pnpm": ["package.json"],
    "node": ["package.json"],
    "vite": ["package.json"],
    "uvicorn": ["requirements.txt", "pyproject.toml", "Pipfile"],
    "gunicorn": ["requirements.txt", "pyproject.toml", "Pipfile"],
    "flask": ["requirements.txt", "pyproject.toml", "Pipfile"],
    "django-admin": ["requirements.txt", "pyproject.toml", "manage.py"],
    "cargo": ["Cargo.toml"],
    "go": ["go.mod"],
    "mvn": ["pom.xml"],
    "gradle": ["build.gradle", "build.gradle.kts"],
    "bundle": ["Gemfile"],
    "composer": ["composer.json"],
}


# --------------------------------------------------------------------------
# terminal
# --------------------------------------------------------------------------

def _color_enabled():
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


C = {
    "reset": "\033[0m", "dim": "\033[2m", "bold": "\033[1m",
    "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
    "blue": "\033[34m", "grey": "\033[90m", "cyan": "\033[36m",
}
if not _color_enabled():
    C = {k: "" for k in C}

STATE_STYLE = {
    "dark":       (C["grey"],   "·", "dark"),
    "taught":     (C["yellow"], "◐", "taught"),
    "understood": (C["green"],  "●", "understood"),
    "stale":      (C["blue"],   "◌", "stale"),
    "debt":       (C["red"],    "▲", "DEBT"),
}


def say(msg=""):
    print(msg)


def die(msg, code=1):
    print("%sfriday: %s%s" % (C["red"], msg, C["reset"]), file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------
# repo helpers
# --------------------------------------------------------------------------

def repo_root():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        return os.getcwd()


def git(args):
    try:
        out = subprocess.run(
            ["git"] + args, capture_output=True, text=True, check=True
        )
        return [l for l in out.stdout.splitlines() if l.strip()]
    except Exception:
        return []


def tracked_files(root):
    files = git(["ls-files"])
    if files:
        return files
    # Not a git repo — walk instead.
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "venv", ".venv",
                        "__pycache__", "dist", "build", DIR)]
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            found.append(rel.replace(os.sep, "/"))
    return found


def staged_files():
    return git(["diff", "--cached", "--name-only", "--diff-filter=ACM"])


# --------------------------------------------------------------------------
# state
# --------------------------------------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def blank_state():
    return {"version": VERSION, "files": {}, "concepts": {}, "ledger": []}


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        die("could not read %s (%s)" % (path, e))


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def load_config(root):
    cfg = load_json(os.path.join(root, CONFIG_FILE), None)
    if cfg is None:
        return dict(DEFAULT_CONFIG)
    merged = dict(DEFAULT_CONFIG)
    merged.update(cfg)
    return merged


def load_state(root):
    return load_json(os.path.join(root, STATE_FILE), blank_state())


def save_state(root, state):
    save_json(os.path.join(root, STATE_FILE), state)


def entry(state, path):
    return state["files"].get(path)


def ensure_entry(state, path, tier):
    e = state["files"].get(path)
    if e is None:
        e = {
            "tier": tier,
            "state": "dark",
            "last_verified": None,
            "confidence": None,
            "ladder_depth": None,
            "slice_ids": [],
            "concepts": [],
        }
        state["files"][path] = e
    return e


# --------------------------------------------------------------------------
# decay
# --------------------------------------------------------------------------

def effective_state(e, cfg):
    """Apply decay. `debt` never decays. `dark` cannot decay further."""
    s = e.get("state", "dark")
    if s in ("debt", "dark", "stale"):
        return s
    stamp = e.get("last_verified")
    if not stamp:
        return s
    days = cfg["decay_days"].get(s)
    if not days:
        return s
    try:
        then = datetime.fromisoformat(stamp)
    except ValueError:
        return s
    if then.tzinfo is None:
        then = then.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) - then > timedelta(days=days):
        return "stale"
    return s


# --------------------------------------------------------------------------
# tiering
# --------------------------------------------------------------------------

def matches_any(path, patterns):
    for p in patterns:
        if fnmatch.fnmatch(path, p) or fnmatch.fnmatch("/" + path, p):
            return True
        # allow bare-name globs to match at any depth
        if "/" not in p and fnmatch.fnmatch(os.path.basename(path), p):
            return True
    return False


def ignored(path, cfg):
    return matches_any(path, cfg.get("ignore", []))


def tier_for(path, size, cfg):
    """Deterministic tiering. Paths and size only — never language parsing."""
    reasons = []
    tier = None
    for t in TIERS:
        if matches_any(path, cfg["tiers"].get(t, [])):
            tier = t
            reasons.append("glob:%s" % t)
            break
    if tier is None:
        tier = "leaves"
        reasons.append("default:leaves")

    # Size promotion. Nobody holds 30KB of logic in their head.
    limit = cfg.get("size_promotion_bytes", 30720)
    if size and size > limit and tier == "leaves":
        # Only promote code-shaped leaves, not assets or lockfiles.
        if os.path.splitext(path)[1] in (
            ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs",
            ".java", ".rb", ".php", ".c", ".cpp", ".cs", ".swift", ".kt",
        ):
            tier = "organs"
            reasons.append("size>%dKB" % (limit // 1024))
    elif size and size > limit and tier == "organs":
        reasons.append("size>%dKB (review: may be spine)" % (limit // 1024))

    return tier, reasons


def file_size(root, path):
    try:
        return os.path.getsize(os.path.join(root, path))
    except OSError:
        return 0


# --------------------------------------------------------------------------
# doctor: orphans + run-command reconciliation
# --------------------------------------------------------------------------

def find_orphans(root, files):
    """Files whose basename appears in no other text file. Cheap, no parsing."""
    text_ext = (".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".md", ".json",
                ".toml", ".yml", ".yaml", ".cfg", ".ini", ".txt", ".go",
                ".rs", ".rb", ".php", ".java", ".sh")
    blob = []
    for f in files:
        if os.path.splitext(f)[1] not in text_ext:
            continue
        try:
            with open(os.path.join(root, f), errors="ignore") as fh:
                blob.append((f, fh.read()))
        except OSError:
            continue

    orphans = []
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext not in text_ext:
            continue
        base = os.path.basename(f)
        stem = os.path.splitext(base)[0]
        if stem in ("__init__", "index", "README", "LICENSE"):
            continue
        referenced = False
        for other, content in blob:
            if other == f:
                continue
            if base in content or ("/" + stem) in content or (
                    re.search(r"\b%s\b" % re.escape(stem), content)):
                referenced = True
                break
        if not referenced:
            orphans.append(f)
    return orphans


def reconcile_run_command(root, files, claimed=None):
    """Compare run commands against evidence in the repo.

    Two sources, and the second is the one that matters. Docs are usually
    right; it is the human's *belief* about how the project starts that
    drifts. `claimed` lets you test that belief directly.
    """
    findings = []
    present = set(os.path.basename(f) for f in files)

    def check(source, text):
        for tool, evidence in RUNTIME_EVIDENCE.items():
            if not re.search(r"(?<![\w-])%s(\s|$)" % re.escape(tool), text):
                continue
            if not any(e in present for e in evidence):
                findings.append((source, tool, evidence))

    if claimed:
        check("your claim", claimed)

    for doc in [f for f in files
                if os.path.basename(f).lower().startswith("readme")]:
        try:
            with open(os.path.join(root, doc), errors="ignore") as fh:
                check(doc, fh.read())
        except OSError:
            continue
    return findings


def find_duplicate_names(files):
    """Same filename at different paths. Path tiering cannot tell them apart,
    and usually one of them is dead."""
    seen = {}
    for f in files:
        seen.setdefault(os.path.basename(f), []).append(f)
    return {k: v for k, v in seen.items() if len(v) > 1}


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_init(args):
    root = repo_root()
    fdir = os.path.join(root, DIR)
    os.makedirs(fdir, exist_ok=True)

    cfg_path = os.path.join(root, CONFIG_FILE)
    if not os.path.exists(cfg_path):
        save_json(cfg_path, DEFAULT_CONFIG)
        say("  created %s" % CONFIG_FILE)
    else:
        say("  %s exists, left alone" % CONFIG_FILE)

    st_path = os.path.join(root, STATE_FILE)
    if not os.path.exists(st_path):
        save_json(st_path, blank_state())
        say("  created %s" % STATE_FILE)
    else:
        say("  %s exists, left alone" % STATE_FILE)

    # Copy the engine in so the repo is self-contained.
    dest = os.path.join(fdir, "friday.py")
    src = os.path.abspath(__file__)
    if os.path.abspath(dest) != src:
        with open(src) as a, open(dest, "w") as b:
            b.write(a.read())
        os.chmod(dest, 0o755)
        say("  installed %s/friday.py" % DIR)

    # Git hook.
    hookdir = os.path.join(root, ".git", "hooks")
    if os.path.isdir(hookdir):
        hook = os.path.join(hookdir, "pre-commit")
        if os.path.exists(hook) and "friday" not in open(hook).read():
            say("  %spre-commit hook exists — add this line yourself:%s" %
                (C["yellow"], C["reset"]))
            say("      python3 .friday/friday.py check || exit 1")
        else:
            with open(hook, "w") as f:
                f.write("#!/bin/sh\n"
                        "# Friday comprehension gate\n"
                        "python3 .friday/friday.py check || exit 1\n")
            os.chmod(hook, 0o755)
            say("  installed .git/hooks/pre-commit")
    else:
        say("  %sno .git/hooks — run 'git init' first for the hard stop%s"
            % (C["yellow"], C["reset"]))

    say()
    say("Next:  python3 .friday/friday.py tier")


def cmd_tier(args):
    root = repo_root()
    cfg = load_config(root)
    state = load_state(root)
    files = [f for f in tracked_files(root) if not ignored(f, cfg)]

    proposal = []
    for f in sorted(files):
        size = file_size(root, f)
        tier, reasons = tier_for(f, size, cfg)
        existing = entry(state, f)
        changed = existing is None or existing["tier"] != tier
        proposal.append((f, tier, size, reasons, changed))

    say()
    say("%sCold tiering pass%s  %s(paths and size only — no language parsing)%s"
        % (C["bold"], C["reset"], C["dim"], C["reset"]))
    say()
    for t in TIERS:
        rows = [p for p in proposal if p[1] == t]
        if not rows:
            continue
        say("  %s%s%s" % (C["bold"], t.upper(), C["reset"]))
        for f, _, size, reasons, changed in rows:
            mark = "+" if changed else " "
            say("   %s %-46s %s%6.1fKB  %s%s" %
                (mark, f[:46], C["dim"], size / 1024.0,
                 ",".join(reasons), C["reset"]))
        say()

    if not args.apply:
        say("%sNothing written.%s Correct the globs in %s, then rerun with --apply."
            % (C["dim"], C["reset"], CONFIG_FILE))
        say("Your corrections are the point — path names lie about data ownership.")
        return

    for f, tier, _, _, _ in proposal:
        e = ensure_entry(state, f, tier)
        e["tier"] = tier
    # Drop entries for files that no longer exist.
    for gone in [p for p in list(state["files"]) if p not in files]:
        del state["files"][gone]
    save_state(root, state)
    say("%sWrote %d entries to %s%s" % (C["green"], len(proposal), STATE_FILE, C["reset"]))


def cmd_map(args):
    root = repo_root()
    cfg = load_config(root)
    state = load_state(root)
    if not state["files"]:
        die("no state yet — run: python3 %s/friday.py tier --apply" % DIR)

    counts = {s: 0 for s in STATES}
    say()
    say("%sFRIDAY%s  %s%s%s" %
        (C["bold"], C["reset"], C["dim"], os.path.basename(root), C["reset"]))
    say()

    for t in TIERS:
        rows = [(p, e) for p, e in sorted(state["files"].items())
                if e["tier"] == t]
        if not rows:
            continue
        if t == "leaves" and not args.all:
            counts["dark"] += 0
            say("  %s%s%s  %s%d files, ungated%s" %
                (C["bold"], t.upper(), C["reset"], C["dim"], len(rows), C["reset"]))
            say()
            continue

        say("  %s%s%s" % (C["bold"], t.upper(), C["reset"]))
        for p, e in rows:
            eff = effective_state(e, cfg)
            counts[eff] = counts.get(eff, 0) + 1
            col, glyph, label = STATE_STYLE[eff]
            conf = e.get("confidence") or ""
            rung = e.get("ladder_depth")
            extra = ""
            if conf:
                extra = "%s, rung %s" % (conf, rung if rung is not None else "-")
            say("   %s%s %-44s %-11s%s %s%s%s" %
                (col, glyph, p[:44], label, C["reset"], C["dim"], extra, C["reset"]))
        say()

    total = sum(counts.values())
    if total:
        lit = counts["understood"]
        pct = 100.0 * lit / total
        bar_w = 34
        filled = int(bar_w * lit / total)
        bar = "█" * filled + "░" * (bar_w - filled)
        say("  %s%s%s  %d/%d understood (%.0f%%)" %
            (C["green"], bar, C["reset"], lit, total, pct))
    parts = []
    for s in STATES:
        if counts.get(s):
            col = STATE_STYLE[s][0]
            parts.append("%s%d %s%s" % (col, counts[s], s, C["reset"]))
    if parts:
        say("  " + "   ".join(parts))
    if counts.get("debt", 0) >= 3:
        say()
        say("  %s%d overrides outstanding. Stop and run a comprehension session.%s"
            % (C["red"], counts["debt"], C["reset"]))
    say()


def cmd_check(args):
    """Pre-commit gate. The hard stop."""
    root = repo_root()
    cfg = load_config(root)
    state = load_state(root)
    gate_tiers = cfg.get("gate_tiers", ["spine", "organs"])

    blocked = []
    for f in staged_files():
        if ignored(f, cfg):
            continue
        e = entry(state, f)
        if e is None:
            size = file_size(root, f)
            tier, _ = tier_for(f, size, cfg)
            if tier in gate_tiers:
                blocked.append((f, tier, "untiered"))
            continue
        if e["tier"] not in gate_tiers:
            continue
        eff = effective_state(e, cfg)
        if eff in BLOCKING:
            blocked.append((f, e["tier"], eff))

    if not blocked:
        return

    say()
    say("%sFriday: commit blocked.%s" % (C["red"] + C["bold"], C["reset"]))
    say()
    for f, tier, why in blocked:
        say("  %s▲%s %-44s %s (%s)" % (C["red"], C["reset"], f, tier, why))
    say()
    say("  You are committing code you have not explained.")
    say()
    say("  Explain it:   ask your agent to run the Friday gate on these files")
    say("  Then mark it: python3 %s/friday.py mark <path> understood" % DIR)
    say("  Emergency:    python3 %s/friday.py override <path> \"reason\"" % DIR)
    say()
    sys.exit(1)


def cmd_mark(args):
    root = repo_root()
    cfg = load_config(root)
    state = load_state(root)
    if args.state not in STATES:
        die("state must be one of: %s" % ", ".join(STATES))

    size = file_size(root, args.path)
    tier, _ = tier_for(args.path, size, cfg)
    e = ensure_entry(state, args.path, tier)
    e["state"] = args.state
    e["last_verified"] = now_iso()
    if args.confidence:
        e["confidence"] = args.confidence
    if args.rung is not None:
        e["ladder_depth"] = args.rung
    if args.concept:
        for cid in args.concept:
            if cid not in e["concepts"]:
                e["concepts"].append(cid)
            c = state["concepts"].setdefault(
                cid, {"description": "", "hits": 0, "files": []})
            c["hits"] += 1
            if args.path not in c["files"]:
                c["files"].append(args.path)
            state["ledger"].append({
                "at": now_iso(), "file": args.path,
                "concept": cid, "rung": args.rung,
            })
            if c["hits"] >= 3:
                say("%s  concept '%s' has %d hits — promote it to a project rule%s"
                    % (C["yellow"], cid, c["hits"], C["reset"]))
    save_state(root, state)
    col = STATE_STYLE[args.state][0]
    say("%s%s → %s%s" % (col, args.path, args.state, C["reset"]))


def cmd_override(args):
    root = repo_root()
    cfg = load_config(root)
    state = load_state(root)
    size = file_size(root, args.path)
    tier, _ = tier_for(args.path, size, cfg)
    e = ensure_entry(state, args.path, tier)
    e["state"] = "debt"
    e["last_verified"] = now_iso()
    e["override_reason"] = args.reason
    state["ledger"].append({
        "at": now_iso(), "file": args.path,
        "event": "override", "reason": args.reason,
    })
    save_state(root, state)
    say("%s▲ %s marked DEBT — %s%s" % (C["red"], args.path, args.reason, C["reset"]))
    say("%s  Not blocked. Recorded. It will stay red until you clear it.%s"
        % (C["dim"], C["reset"]))


def cmd_doctor(args):
    root = repo_root()
    cfg = load_config(root)
    files = [f for f in tracked_files(root) if not ignored(f, cfg)]

    say()
    say("%sFriday doctor%s" % (C["bold"], C["reset"]))
    say()

    findings = reconcile_run_command(root, files, args.run)
    if findings:
        say("  %sRun-command mismatch%s" % (C["red"], C["reset"]))
        for source, tool, evidence in findings:
            say("    %s says '%s' — but none of %s exist here."
                % (source, tool, "/".join(evidence)))
        if any(f[0] == "your claim" for f in findings):
            say("    %sYour model of how this project starts is wrong.%s"
                % (C["dim"], C["reset"]))
        say()
    elif args.run:
        say("  %s✓%s your claimed run command reconciles with the repo"
            % (C["green"], C["reset"]))
        say()
    else:
        say("  %s✓%s documented run command reconciles with repo contents"
            % (C["green"], C["reset"]))
        say("    %stest your own belief:  friday doctor --run \"npm run dev\"%s"
            % (C["dim"], C["reset"]))
        say()

    dupes = find_duplicate_names(files)
    if dupes:
        say("  %sDuplicate filenames%s  %s(path tiering cannot tell these apart)%s"
            % (C["yellow"], C["reset"], C["dim"], C["reset"]))
        for name, paths in sorted(dupes.items()):
            say("    %s" % name)
            for p in paths:
                say("      %-44s %s%.1fKB%s"
                    % (p[:44], C["dim"], file_size(root, p) / 1024.0, C["reset"]))
        say("    %sUsually one of these is dead. Which one is live?%s"
            % (C["dim"], C["reset"]))
        say()

    orphans = find_orphans(root, files)
    if orphans:
        total = sum(file_size(root, f) for f in orphans)
        say("  %sOrphans%s  %s(referenced by nothing else)%s"
            % (C["yellow"], C["reset"], C["dim"], C["reset"]))
        for f in orphans:
            say("    %-46s %s%.1fKB%s" %
                (f[:46], C["dim"], file_size(root, f) / 1024.0, C["reset"]))
        say("    %s%.1fKB unreferenced%s" % (C["dim"], total / 1024.0, C["reset"]))
        say()
    else:
        say("  %s✓%s no orphan files" % (C["green"], C["reset"]))
        say()


def cmd_ledger(args):
    root = repo_root()
    state = load_state(root)
    concepts = state.get("concepts", {})
    if not concepts:
        say("No concepts recorded yet.")
        return
    say()
    say("%sConcept registry%s  %s(3 hits = promote to a project rule)%s"
        % (C["bold"], C["reset"], C["dim"], C["reset"]))
    say()
    for cid, c in sorted(concepts.items(), key=lambda kv: -kv[1]["hits"]):
        flag = "%s← promote%s" % (C["yellow"], C["reset"]) if c["hits"] >= 3 else ""
        say("  %s%-26s%s %d hit(s)  %s" % (C["bold"], cid, C["reset"], c["hits"], flag))
        if c.get("description"):
            say("    %s%s%s" % (C["dim"], c["description"], C["reset"]))
        say("    %s%s%s" % (C["dim"], ", ".join(c["files"]), C["reset"]))
    say()


def cmd_status(args):
    root = repo_root()
    cfg = load_config(root)
    state = load_state(root)
    gate_tiers = cfg.get("gate_tiers", ["spine", "organs"])
    pending = []
    for f in staged_files():
        e = entry(state, f)
        if e and e["tier"] in gate_tiers:
            eff = effective_state(e, cfg)
            if eff in BLOCKING:
                pending.append((f, e["tier"], eff))
    if not pending:
        say("%s✓ nothing staged needs a gate%s" % (C["green"], C["reset"]))
        return
    say("%sStaged and ungated:%s" % (C["yellow"], C["reset"]))
    for f, t, s in pending:
        say("  %s  (%s, %s)" % (f, t, s))


# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        prog="friday",
        description="A comprehension gate for AI-assisted code. "
                    "The build artifact is your understanding.",
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init", help="scaffold .friday/ and install the git hook")

    t = sub.add_parser("tier", help="cold tiering pass over the repo")
    t.add_argument("--apply", action="store_true", help="write the result to state")

    m = sub.add_parser("map", help="render the understanding map")
    m.add_argument("--all", action="store_true", help="include leaves")

    sub.add_parser("check", help="pre-commit gate (used by the git hook)")
    d = sub.add_parser("doctor", help="orphan and run-command reconciliation")
    d.add_argument("--run", metavar="CMD",
                   help="test your belief about how this project starts")
    sub.add_parser("ledger", help="show the concept registry")
    sub.add_parser("status", help="what is staged and ungated")

    mk = sub.add_parser("mark", help="record the outcome of a gate")
    mk.add_argument("path")
    mk.add_argument("state", choices=STATES)
    mk.add_argument("--confidence", choices=["sure", "think-so", "guessing"])
    mk.add_argument("--rung", type=int, help="how far down the hint ladder")
    mk.add_argument("--concept", action="append", help="concept id (repeatable)")

    ov = sub.add_parser("override", help="skip a gate; records visible debt")
    ov.add_argument("path")
    ov.add_argument("reason")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return

    {
        "init": cmd_init, "tier": cmd_tier, "map": cmd_map,
        "check": cmd_check, "mark": cmd_mark, "override": cmd_override,
        "doctor": cmd_doctor, "ledger": cmd_ledger, "status": cmd_status,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
