#!/bin/sh
# Edited-archive trace, run inside the VM. Everything under ~/untrusted/alpoge-rh/edit/ is untrusted data.
# usage: sh run_edit.sh COMMIT   (the pinned commit of leanprover-community/riemann-hypothesis, branch main)
set -u
C="${1:?commit}"; B=~/untrusted/alpoge-rh/edit; S=~/nm-scripts; mkdir -p "$B/graph" "$B/out" "$B/spot"
T() { date -u +%Y-%m-%dT%H:%M:%SZ; }
echo "start $(T) commit $C" > "$B/started.txt"; df -B1 --output=avail ~ | tail -1 > "$B/disk_start.txt"
# 1. clone at the pinned commit; the original branch beside it for the identity check
cd "$B" && git clone -q https://github.com/leanprover-community/riemann-hypothesis repo && cd repo && git checkout -q "$C" && git rev-parse HEAD > "$B/head.txt" && git fetch -q origin original && git worktree add -q "$B/original" origin/original && (cd "$B/original" && git rev-parse HEAD) > "$B/original_head.txt"
cat lean-toolchain > "$B/toolchain.txt"; python3 -I -c "import json;[print(p['name'],p['rev']) for p in json.load(open('lake-manifest.json'))['packages']]" > "$B/manifest_revs.txt"
find src -name '*.lean' | wc -l > "$B/lean_files_main.txt"; (cd "$B/original" && find src -name '*.lean' | wc -l) > "$B/lean_files_original.txt"
# 2. identity: original branch against the tarball's extracted source (cycle 2 build directory, sources only)
diff -rq "$B/original/src" ~/untrusted/alpoge-rh/src/lean/src > "$B/P0_diff.txt" 2>&1; echo "diff exit $?" >> "$B/P0_diff.txt"
# 3. toolchain (elan installs the pinned one), Mathlib's cache, then the community's cache of the compiled submission
echo "cache start $(T)" >> "$B/started.txt"
MATHLIB_CACHE_GET_URL=https://cache.mathlib.org/mathlib4 /usr/bin/time -v lake exe mathlib/cache get > "$B/mathlib_cache.log" 2>&1; echo "mathlib cache exit $?" >> "$B/mathlib_cache.log"
/usr/bin/time -v lake exe cache get > "$B/project_cache.log" 2>&1 & CP=$!
while kill -0 $CP 2>/dev/null; do a=$(df -B1 --output=avail ~ | tail -1); if [ "$a" -lt 10000000000 ]; then echo "disk guard: $a bytes free at $(T); fetch killed" >> "$B/project_cache.log"; kill $CP; fi; sleep 60; done
wait $CP; echo "project cache exit $?" >> "$B/project_cache.log"
df -B1 --output=avail ~ | tail -1 > "$B/disk_after_cache.txt"; du -sb .lake/build 2>/dev/null > "$B/build_bytes.txt"
/usr/bin/time -v lake build --no-build > "$B/no_build.log" 2>&1; echo "no-build exit $?" >> "$B/no_build.log"
# 4. the graph, from the module table
echo "walk start $(T)" >> "$B/started.txt"
cp "$S/ArchiveGraph.lean" ./ArchiveGraph.lean && /usr/bin/time -v lake env lean ArchiveGraph.lean > "$B/walk_out.txt" 2> "$B/walk_err.txt"; echo "walk exit $?" >> "$B/walk_out.txt"
echo "walk end $(T)" >> "$B/started.txt"
# 5. spot check: 20 random archive modules recompiled from source, compared with the cached olean
find src -name '*.lean' | sort | python3 -I -c "import sys,random;random.seed(20261125);L=[l.strip() for l in sys.stdin];print('\n'.join(random.sample(L,20)))" > "$B/spot_list.txt"
cp "$S/SpotCheck.lean" ./SpotCheck.lean
while read -r f; do
  m=$(echo "${f#src/}" | sed 's/\.lean$//' | tr '/' '.'); o=".lake/build/lib/lean/${f#src/}"; o="${o%.lean}.olean"; n="$B/spot/$(echo "$m").olean"
  timeout 1800 lake env lean -o "$n" "$f" > "$B/spot/$m.log" 2>&1; e=$?
  if [ -f "$n" ] && [ -f "$o" ]; then r=$(lake env lean --run SpotCheck.lean "$o" "$n" 2>&1 | tail -1); else r="missing olean (cached: $o)"; fi
  echo "$m	compile_exit $e	$r" >> "$B/spot_results.tsv"
done < "$B/spot_list.txt"
# 6. the measures
echo "analysis start $(T)" >> "$B/started.txt"
/usr/bin/time -v python3 -I "$S/edit.py" "$B/graph" "$B/out" "$S/mathlib_shapes.tsv" > "$B/analysis_log.txt" 2> "$B/analysis_err.txt"; echo "analysis exit $?" >> "$B/analysis_log.txt"
echo "end $(T)" >> "$B/started.txt"; df -B1 --output=avail ~ | tail -1 > "$B/disk_end.txt"
cd "$B" && sha256sum head.txt original_head.txt toolchain.txt manifest_revs.txt P0_diff.txt spot_results.tsv graph/nodes.tsv graph/edges.tsv out/*.tsv out/report.md > "$B/outputs.sha256" 2>/dev/null
echo DONE > "$B/DONE"
