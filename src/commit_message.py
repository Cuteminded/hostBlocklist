import argparse
from collections import Counter
import os
from pathlib import Path
import subprocess


def previous_content(path):
    return subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def entries(content, rules=False):
    lines = (line.strip() for line in content.splitlines())
    if rules:
        return Counter(line for line in lines if line.startswith("||"))
    return Counter(line for line in lines if line and not line.startswith("#"))


def describe_change(path, label, rules=False):
    before = previous_content(path)
    after = Path(path).read_text(encoding="utf-8")
    if before == after:
        return None
    if path == "README.md":
        return "README updated"

    old_entries = entries(before, rules)
    new_entries = entries(after, rules)
    added = sum((new_entries - old_entries).values())
    removed = sum((old_entries - new_entries).values())
    changes = []
    if added:
        changes.append(f"{added} added")
    if removed:
        changes.append(f"{removed} removed")
    if not changes:
        return f"{label}: formatting, order or metadata updated"
    return f"{label}: {', '.join(changes)}"


def build_message(workflow):
    files = [("src/domains.txt", "domain entries", False)]
    if workflow == "build":
        files = [
            ("adblock.txt", "AdBlock rules", True),
            ("adguard.txt", "AdGuard rules", True),
            *files,
            ("README.md", "README", False),
        ]
    changes = [
        change
        for path, label, rules in files
        if (change := describe_change(path, label, rules))
    ]
    prefix = "Update blocklists" if workflow == "build" else "Clean domains"
    return f"{prefix}: {'; '.join(changes)}" if changes else f"{prefix}: no changes"


def main():
    parser = argparse.ArgumentParser(description="Describe generated changes for a commit.")
    parser.add_argument("workflow", choices=("build", "clean"))
    args = parser.parse_args()
    message = build_message(args.workflow)
    print(message)
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a", encoding="utf-8") as file:
            file.write(f"message={message}\n")


if __name__ == "__main__":
    main()
