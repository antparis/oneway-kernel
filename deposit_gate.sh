#!/usr/bin/env bash
# deposit_gate.sh -- 2026-07-18
# Mechanical deposit gate for the one-way kernel paper (v11 seal).
# Fail-closed: ANY missing or mismatched pinned piece => exit 1, no deposit.
# Run from the repo root: bash deposit_gate.sh
#
# What it guards (the paper's own promise, Data availability section):
#   "The symbolic certification harness, the simulation scripts, and the
#    findings files underlying every certified claim in this paper are
#    archived alongside this deposit."

cd "$(dirname "$0")" || exit 1
FAIL=0
WARN=0

ok()   { printf '  [OK]   %s\n' "$1"; }
bad()  { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL+1)); }
warn() { printf '  [WARN] %s\n' "$1"; WARN=$((WARN+1)); }

# file exists, nonzero size
need() {
  if [ -s "$1" ]; then ok "$1"; else bad "MISSING or empty: $1"; fi
}

# file exists AND sha256 matches full pin
pin() {
  if [ ! -s "$1" ]; then bad "MISSING: $1"; return; fi
  h=$(sha256sum "$1" | cut -d' ' -f1)
  if [ "$h" = "$2" ]; then ok "$1  sha256 pinned"; else bad "sha256 MISMATCH: $1 ($h != $2)"; fi
}

# file exists AND sha256 starts with prefix (when only the prefix is graved)
pinp() {
  if [ ! -s "$1" ]; then bad "MISSING: $1"; return; fi
  h=$(sha256sum "$1" | cut -d' ' -f1)
  case "$h" in
    "$2"*) ok "$1  sha256 prefix pinned" ;;
    *)     bad "sha256 prefix MISMATCH: $1 ($h !~ $2*)" ;;
  esac
}

echo "== 1. SEAL v11 (the canonical objects, Anthony's machine) =="
need paper/SEAL_v11.txt
pin  paper/oneway_kernel_paper_v11.pdf f510cf18a2c79b07bbfdb131c2be168a328bf329b58f9eb9f2415a4615d6e85a
pin  paper/oneway_kernel_paper_v11.tex a801936d3aeb791530fb68ae2485394f069adcedac26f4212d67c145aa2c92ee

echo "== 2. Patcher chain (reproducibility from the sealed v3) =="
need paper/build_v5.py
need paper/build_v6.py
need paper/build_v7.py
pin  paper/oneway_kernel_paper_v7.tex 6570569fd88405eb06ed75c59ec64c773fdd2365131b55ce56d0d750eeba30ea
pin  paper/build_v8.py  68306b07c73ea21b5e671eb7d032ced2572d54abb7bdbb26aaa216aa9b7f9b95
pin  paper/build_v9.py  fcd4af373a8f573ebd6ab484ce11c0de78deaf0a16d7df3cfb9a93ab727b5472
pin  paper/build_v10.py 24548a88a1e70c367f9ebf10cd9ae80080ee937b33893afa9f28c17302d77951
pin  paper/build_v11.py d05cfe82f2d370376bef885b407c4756b0b7a3e1c2afeafdcf858ad59874f055

echo "== 3. Certification harnesses promised to the public (code/) =="
need code/kernel_heterodyne_test.py
need code/judge_heterodyne_052.py
pinp code/judge_repair_058_v2.py cffac21a
pin  code/calendar_weights_test.py  bb9371cd19ff2dfe2631ab8f16dfb52d90af6fce134f80665663c25a8226099e
pin  code/amplitude_calendar_test.py 1130c24dd71bfcac7c734afd7b95efbd3db4896dfff5ec364b2bf2329466af87

echo "== 4. FINDINGS promised to the public (docs/) =="
need docs/FINDINGS_20260711_heterodyne_052.md
need docs/FINDINGS_20260711_oriented_bell_054.md
need docs/FINDINGS_20260713_reciprocity_dichotomy_055.md
need docs/FINDINGS_20260714_comparative_witness_057.md
need docs/FINDINGS_20260714_corrigendum_core_058.md
need docs/FINDINGS_20260714_errata_055_supersession.md
need docs/FINDINGS_20260714_judge_v2_projection_trap_059.md
pin  docs/FINDINGS_20260717_calendar_weights_060.md 72ffd9814c85c6f4fdeed456966afd436eaf15eaf10e58124e55cb65ff95d50f
pin  docs/FINDINGS_20260717_amplitude_calendar_061.md f9bcb05ab5bdd0427195a220b68a4ecd81cd6d852af1023694c2dc085217f15a

echo "== 5. Stray files (warnings only -- we commit by explicit name) =="
for s in paper/0 paper/v7_bundle.tar.gz code/__pycache__; do
  [ -e "$s" ] && warn "stray present, do NOT commit: $s"
done
ls paper/*.bak-s* >/dev/null 2>&1 && warn "old .bak-s* files present in paper/ (leave uncommitted)"

echo "=================================================================="
if [ "$FAIL" -eq 0 ]; then
  echo "DEPOSIT GATE: PASS ($WARN warning(s)) -- the paper's promises are on disk."
  echo "Next allowed step: explicit named git add + commit (push only on order)."
  exit 0
else
  echo "DEPOSIT GATE: FAIL -- $FAIL blocking issue(s), $WARN warning(s). NO DEPOSIT."
  exit 1
fi
