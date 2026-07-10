#!/usr/bin/env python3
"""patch_v3_date.py -- single-line patcher for the v3 paper title date.

Change \\date{July 4, 2026} -> \\date{July 10, 2026} in
oneway_kernel_paper_v3.tex, with a dated backup and asserted anchors.

Discipline (project rules):
  - single-line anchor, asserted to occur EXACTLY once;
  - dated backup written BEFORE any modification;
  - brace balance of the whole file asserted unchanged after splice;
  - no other line touched (asserted: exactly one line differs);
  - idempotence guard: refuses to run if the target is already patched.

Run from anywhere:  python3 patch_v3_date.py
Target path is fixed to the repository copy on Anthony's machine.
"""
import datetime
import pathlib
import shutil
import sys

TARGET = pathlib.Path.home() / "Desktop/oneway-kernel/paper/oneway_kernel_paper_v3.tex"
OLD = r"\date{July 4, 2026}"
NEW = r"\date{July 10, 2026}"


def fail(msg):
    print(f"PATCH ABORTED: {msg}")
    sys.exit(1)


def main():
    if not TARGET.is_file():
        fail(f"target not found: {TARGET}")
    text = TARGET.read_text(encoding="utf-8")

    if NEW in text:
        fail("target already contains the new date -- nothing to do (idempotence guard)")
    n = text.count(OLD)
    if n != 1:
        fail(f"anchor {OLD!r} found {n} times, expected exactly 1")

    stamp = datetime.date.today().strftime("%Y%m%d")
    backup = TARGET.with_name(TARGET.name + f".bak_{stamp}")
    if backup.exists():
        fail(f"backup already exists, refusing to overwrite: {backup}")
    shutil.copy2(TARGET, backup)
    print(f"backup written: {backup}")

    patched = text.replace(OLD, NEW, 1)

    # assertions before writing
    if patched.count(NEW) != 1 or OLD in patched:
        fail("post-splice anchor assertion failed")
    for ch in "{}":
        if patched.count(ch) != text.count(ch):
            fail(f"brace balance changed for {ch!r}")
    old_lines, new_lines = text.splitlines(), patched.splitlines()
    if len(old_lines) != len(new_lines):
        fail("line count changed")
    diff = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
    if len(diff) != 1:
        fail(f"expected exactly 1 changed line, got {len(diff)}")

    TARGET.write_text(patched, encoding="utf-8")
    print(f"patched line {diff[0] + 1}: {old_lines[diff[0]].strip()!r} -> {new_lines[diff[0]].strip()!r}")
    print("PATCH OK -- recompile (2x pdflatex) and re-seal the PDF md5 next")


if __name__ == "__main__":
    main()
