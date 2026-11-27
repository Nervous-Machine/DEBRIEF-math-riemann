#!/bin/sh
# Cycle 3: rerun of the compact edition of the 25 November rewriting (lsernau/grh-lean, commit 72fead10, folder
# grh-compact) in the VM. usage: sh rh_cycle3.sh   (run inside the VM). Every step logs to $O; a failed step is
# recorded and the script goes on to the next step that does not depend on it.
set -u
W=~/untrusted/sernau-grh; O=$W/out; A=~/untrusted/alpoge-rh/src/lean; mkdir -p "$O"
export PATH=$HOME/.elan/bin:$PATH
T() { date -u +%Y-%m-%dT%H:%M:%SZ; }
step() { echo "$1 $(T)" >> "$O/steps.txt"; }
df -B1 --output=avail ~ | tail -1 > "$O/disk_start.txt"
# C1 source
step "C1 clone start"
[ -d "$W/repo" ] || git clone -q https://github.com/lsernau/grh-lean.git "$W/repo" > "$O/clone.log" 2>&1
cd "$W/repo" && git checkout -q 72fead102f663d5c7a407964a13dc0cf9d977207 && git rev-parse HEAD > "$O/head.txt" && git rev-list --count HEAD > "$O/commit_count.txt"
cd "$W/repo/grh-compact" || { echo "no grh-compact" > "$O/FAILED"; exit 1; }
cat lean-toolchain > "$O/toolchain.txt"; grep -A3 'name = "mathlib"' lakefile.toml > "$O/mathlib_pin.txt"
find src -name '*.lean' | sort > "$O/files.txt"; wc -l < "$O/files.txt" > "$O/file_count.txt"
find src -name '*.lean' -print0 | xargs -0 cat | wc -l > "$O/lines_total.txt"
find src -name '*.lean' -print0 | xargs -0 cat | python3 -I -c "
import sys,re
t=sys.stdin.read(); t=re.sub(r'/-.*?-/','',t,flags=re.S)
print(sum(1 for l in t.split(chr(10)) if l.strip() and not l.strip().startswith('--')))" > "$O/lines_code.txt"
step "C1 end"
# C2 static scan of the project source (word matches, comments included; every hit listed)
grep -rnwE 'sorry|admit|native_decide|axiom|implemented_by|extern|unsafe|opaque|macro|syntax|elab|notation|macro_rules|elab_rules|run_cmd|run_tac' src scripts Challenge.lean > "$O/C2_scan.txt" 2>&1; echo "exit $?" >> "$O/C2_scan.txt"
step "C2 end"
# C3 Mathlib cache and build
step "C3 cache start"
ulimit -n "$(ulimit -Hn)" 2>/dev/null
lake exe cache get > "$O/cache.log" 2>&1; echo "cache exit $?" >> "$O/cache.log"
step "C3 build start"
/usr/bin/time -v lake build > "$O/build.log" 2> "$O/build_time.txt"; echo "build exit $?" >> "$O/build.log"
grep -c "error" "$O/build.log" > "$O/build_error_lines.txt"
step "C3 end"
df -B1 --output=avail ~ | tail -1 > "$O/disk_after_build.txt"
# C4 axioms (the repository's script) and types
lake env lean scripts/PrintAxioms.lean > "$O/C4_axioms.txt" 2>&1; echo "exit $?" >> "$O/C4_axioms.txt"
cat > "$O/C4_types.lean" <<'L'
import Main
#check @riemannHypothesis
#check @riemannZeta_eq_zero_re
#check @LFunction_ne_zero_of_half_lt_re
#check @LFunction_eq_zero_re
#check @LFunction_eq_zero_re_of_isPrimitive
#print RiemannHypothesis
#eval show Lean.MetaM Unit from do
  let env ← Lean.getEnv
  for n in [`RiemannHypothesis, `RiemannZetaZerosOnLine, `DirichletLNonvanishingRightOfHalf, `DirichletLZerosOnLine, `PrimitiveDirichletLZerosOnLine] do
    IO.println s!"{n} : {(env.getModuleIdxFor? n).map (fun i => env.header.moduleNames[i.toNat]!)}"
L
lake env lean "$O/C4_types.lean" > "$O/C4_types.txt" 2>&1; echo "exit $?" >> "$O/C4_types.txt"
step "C4 end"
# C5 statements against the archive's own statement file (blank lines ignored), and the rewrite's Challenge.lean
diff -B "$A/src/Statements.lean" src/Statements.lean > "$O/C5_statements_vs_archive.diff" 2>&1; echo "exit $?" >> "$O/C5_statements_vs_archive.diff"
sha256sum "$A/src/Statements.lean" src/Statements.lean Challenge.lean > "$O/C5_hashes.txt"
step "C5 end"
# C6 kernel replay of every project module (leanchecker), 16 at a time
sed 's#^src/##; s#\.lean$##; s#/#.#g' "$O/files.txt" > "$O/modules.txt"
step "C6 start"
xargs -P 16 -I{} sh -c 'out=$(timeout 3600 lake env leanchecker {} 2>&1); e=$?; r=$(printf "%s" "$out" | tail -3 | tr "\n" " "); printf "%s\texit %s\t%s\n" "{}" "$e" "$r"' < "$O/modules.txt" > "$O/C6_replay.tsv" 2>&1
step "C6 end"
# C7 export of the five theorems and the external kernels
lake env leanexport Main -- riemannHypothesis riemannZeta_eq_zero_re LFunction_ne_zero_of_half_lt_re LFunction_eq_zero_re LFunction_eq_zero_re_of_isPrimitive > "$W/export.ndjson" 2> "$O/C7_export_err.txt"; echo "export exit $?" > "$O/C7_export.txt"
ls -l "$W/export.ndjson" >> "$O/C7_export.txt"; sha256sum "$W/export.ndjson" >> "$O/C7_export.txt"
B=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0/bin
printf '{"export_file_path":"%s","permitted_axioms":["propext","Classical.choice","Quot.sound","Lean.trustCompiler"],"unpermitted_axiom_hard_error":false,"num_threads":16,"print_success_message":true}\n' "$W/export.ndjson" > "$O/nanoda.json"
step "C7 nanoda start"; /usr/bin/time -v "$B/nanoda_bin" "$O/nanoda.json" > "$O/C7_nanoda.txt" 2> "$O/C7_nanoda_time.txt"; echo "exit $?" >> "$O/C7_nanoda.txt"
step "C7 con-leche start"; /usr/bin/time -v "$B/con-leche" --verified --jobs=16 "$W/export.ndjson" > "$O/C7_conleche.txt" 2> "$O/C7_conleche_time.txt"; echo "exit $?" >> "$O/C7_conleche.txt"
step "C7 con-ron start"; /usr/bin/time -v "$B/con-ron" --verified --jobs=16 "$W/export.ndjson" > "$O/C7_conron.txt" 2> "$O/C7_conron_time.txt"; echo "exit $?" >> "$O/C7_conron.txt"
step "C7 lean4lean start"; ( ulimit -v 88000000; /usr/bin/time -v timeout 14400 lake env lean4lean Main > "$O/C7_lean4lean.txt" 2> "$O/C7_lean4lean_time.txt"; echo "exit $?" >> "$O/C7_lean4lean.txt" )
step "C7 end"
df -B1 --output=avail ~ | tail -1 > "$O/disk_end.txt"
cd "$O" && sha256sum *.txt *.tsv *.diff > "$O/outputs.sha256" 2>/dev/null
echo DONE > "$O/DONE"
