#!/usr/bin/env python3 -I
"""Structure analysis of the dependency walk (nodes.tsv, edges.tsv) written by DepCone.lean. Integer-indexed version
of analyze.py (same measures, same outputs) for the full archive (1.27 M constants, 149 M edges).
Usage: python3 -I analyze2.py DATA_DIR OUT_DIR
DATA_DIR holds nodes.tsv, edges.tsv, files_wc.txt (wc -l per .lean file, paths src/...), lines_per_dir.txt."""
import sys, os, re, collections, time
sys.setrecursionlimit(10000)
data, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ROOT_N = os.environ.get("ROOT", "riemannHypothesis")
FORK_HARD_N = os.environ.get("FORK_HARD", "UpperTheory.FinalTheorems.everyCharacter")
FORK_SHORT_N = os.environ.get("FORK_SHORT", "Formalism.VW.rh_of_every")
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def)")
t0 = time.time()
def log(s): print(f"[{time.time()-t0:7.0f}s] {s}", flush=True)

# ---------- load nodes ----------
names = []; ids = {}; kind = []; module = []; arch = []; L1 = []; L2 = []
with open(f"{data}/nodes.tsv") as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 6: continue
        ids[p[0]] = len(names); names.append(p[0]); kind.append(p[1]); module.append(p[2]); arch.append(p[3] == "1")
        L1.append(int(p[4])); L2.append(int(p[5]))
N = len(names)
log(f"nodes {N}")
# ---------- load edges ----------
succ = [[] for _ in range(N)]
ne = 0; unknown = 0
with open(f"{data}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        ia = ids.get(a); ib = ids.get(b)
        if ia is None or ib is None: unknown += 1; continue
        if ia != ib: succ[ia].append(ib); ne += 1
for i in range(N):
    if len(succ[i]) > 1: succ[i] = list(set(succ[i]))
ne_d = sum(len(s) for s in succ)
log(f"edges read {ne} (unknown endpoints {unknown}), distinct {ne_d}")
is_arch = arch
n_arch = sum(arch); n_lib = sum(1 for i in range(N) if not arch[i] and kind[i] != "missing"); n_missing = sum(1 for k in kind if k == "missing")
print(f"nodes {N} archive {n_arch} library {n_lib} missing {n_missing} edges {ne_d}")

# ---------- source totals ----------
def mod_path(m): return "src/" + m.replace(".", "/") + ".lean"
wc = {}
with open(f"{data}/files_wc.txt") as f:
    for line in f:
        p = line.split()
        if len(p) == 2: wc[p[1]] = int(p[0])
dir_lines_total = {}
with open(f"{data}/lines_per_dir.txt") as f:
    for line in f:
        p = line.split()
        if len(p) == 2 and p[0].endswith("/"): dir_lines_total[p[0][:-1]] = int(p[1])
dir_files_total = collections.Counter(p.split("/")[1] for p in wc)
total_lines = sum(wc.values())
def top(m): return m.split(".")[0]
def top2(m):
    c = m.split("."); return "/".join(c[:2]) if len(c) > 1 else c[0]

def decl_lines(S):
    per_mod = collections.defaultdict(list)
    for i in S:
        if L1[i] > 0: per_mod[module[i]].append((L1[i], L2[i]))
    total = 0
    for m, rs in per_mod.items():
        rs.sort(); cs, ce = rs[0]
        for s, e in rs[1:]:
            if s <= ce + 1: ce = max(ce, e)
            else: total += ce - cs + 1; cs, ce = s, e
        total += ce - cs + 1
    return total
def module_lines(S):
    mods = {module[i] for i in S}
    return sum(wc.get(mod_path(m), 0) for m in mods), len(mods)
def cone(start):
    """archive constants reachable from start (start included if archive)"""
    seen = bytearray(N); st = [start]; res = []
    while st:
        x = st.pop()
        if seen[x]: continue
        seen[x] = 1
        if arch[x]:
            res.append(x)
            for y in succ[x]:
                if not seen[y] and arch[y]: st.append(y)
    return res

rep = []
def P(s=""): rep.append(s); print(s, flush=True)
ROOT = ids[ROOT_N]
C = cone(ROOT); Cset = set(C)
log(f"cone of root: {len(C)}")
P(f"# Structure trace of the archive below `{ROOT_N}`\n")
P("## R2. The archive cone (constants the kernel uses for the main theorem)\n")
kinds = collections.Counter(kind[i] for i in C)
aux = sum(1 for i in C if AUX.search(names[i]))
dl = decl_lines(C); ml, nm = module_lines(C)
P("| measure | value |\n|---|---|")
P(f"| archive constants in the cone | {len(C):,} |")
P(f"| of which auxiliary (generated names) | {aux:,} |")
P(f"| by kind | {', '.join(f'{k} {v:,}' for k, v in kinds.most_common())} |")
P(f"| constants without a declaration range | {sum(1 for i in C if L1[i] == 0):,} |")
P(f"| declaration lines (union of ranges) | {dl:,} |")
P(f"| modules touched | {nm:,} of {len(wc):,} |")
P(f"| lines of the modules touched | {ml:,} of {total_lines:,} ({100*ml/total_lines:.1f}%) |")
P(f"| library (Mathlib/Lean) constants named directly by archive constants | {n_lib:,} |")
P(f"| archive constants walked from all five entry theorems (not only the root) | {n_arch:,} |")
P()
P("### Per top-level directory\n")
P("| directory | files total | modules touched | lines total | lines of touched modules | share touched | declaration lines used | constants used |")
P("|---|---|---|---|---|---|---|---|")
by_top = collections.defaultdict(list)
for i in C: by_top[top(module[i])].append(i)
rows = []
for d in sorted(set(dir_lines_total) | set(by_top)):
    ns = by_top.get(d, []); ml_d, nm_d = module_lines(ns); lt = dir_lines_total.get(d, wc.get(f"src/{d}.lean", 0))
    rows.append((d, dir_files_total.get(d, 1 if f"src/{d}.lean" in wc else 0), nm_d, lt, ml_d, (100*ml_d/lt if lt else 0), decl_lines(ns), len(ns)))
for r in rows: P(f"| {r[0]} | {r[1]:,} | {r[2]:,} | {r[3]:,} | {r[4]:,} | {r[5]:.1f}% | {r[6]:,} | {r[7]:,} |")
with open(f"{out}/per_directory.tsv", "w") as f:
    f.write("directory\tfiles_total\tmodules_touched\tlines_total\tlines_touched_modules\tshare_pct\tdecl_lines\tconstants\n")
    for r in rows: f.write("\t".join(str(x) for x in r) + "\n")
P()
P("### Second-level directories\n")
P("| directory | files total | modules touched | lines total | lines of touched modules | share | constants used |")
P("|---|---|---|---|---|---|---|")
by_top2 = collections.defaultdict(list)
for i in C: by_top2[top2(module[i])].append(i)
files2 = collections.Counter("/".join(p.split("/")[1:3]) for p in wc if p.count("/") >= 3)
lines2 = collections.Counter()
for p, l in wc.items():
    if p.count("/") >= 3: lines2["/".join(p.split("/")[1:3])] += l
rows2 = []
for d in sorted(set(files2) | {k for k in by_top2 if "/" in k}):
    ns = by_top2.get(d, []); ml_d, nm_d = module_lines(ns)
    rows2.append((d, files2.get(d, 0), nm_d, lines2.get(d, 0), ml_d, (100*ml_d/lines2[d] if lines2.get(d) else 0), len(ns)))
for r in rows2: P(f"| {r[0]} | {r[1]:,} | {r[2]:,} | {r[3]:,} | {r[4]:,} | {r[5]:.1f}% | {r[6]:,} |")
with open(f"{out}/per_directory2.tsv", "w") as f:
    for r in rows2: f.write("\t".join(str(x) for x in r) + "\n")
P()
P("### Library boundary, by top-level module\n")
libtop = collections.Counter(top(module[i]) for i in range(N) if not arch[i] and kind[i] != "missing")
P("| library | distinct constants named directly by the archive |\n|---|---|")
for k, v in libtop.most_common(): P(f"| {k} | {v:,} |")
P()
log("R2 done")

# ---------- R3 ----------
P(f"## R3. The fork: `{FORK_HARD_N}` versus `{FORK_SHORT_N}`\n")
H = set(cone(ids[FORK_HARD_N])) if FORK_HARD_N in ids else set()
Sh = set(cone(ids[FORK_SHORT_N])) if FORK_SHORT_N in ids else set()
def row(label, S):
    P(f"| {label} | {len(S):,} | {100*len(S)/len(C):.2f}% | {decl_lines(S):,} | {100*decl_lines(S)/dl:.2f}% | {module_lines(S)[1]:,} |")
P("| set | archive constants | share of cone | declaration lines | share of cone lines | modules |")
P("|---|---|---|---|---|---|")
row(f"cone({ROOT_N})", Cset); row(f"cone({FORK_HARD_N})", H); row(f"cone({FORK_SHORT_N})", Sh)
row("intersection", H & Sh); row(f"cone({FORK_SHORT_N}) minus cone({FORK_HARD_N})", Sh - H); row(f"cone({ROOT_N}) minus both", Cset - H - Sh)
P()
rest = sorted(names[i] for i in (Cset - H - Sh))
P(f"Constants in cone({ROOT_N}) outside both fork cones ({len(rest)}): " + ", ".join(rest[:60]) + (" …" if len(rest) > 60 else ""))
d2 = sorted(names[i] for i in (Sh - H))
P(f"\nConstants in cone({FORK_SHORT_N}) not in cone({FORK_HARD_N}) ({len(d2)}): " + ", ".join(d2[:80]) + (" …" if len(d2) > 80 else ""))
with open(f"{out}/short_minus_hard.txt", "w") as f: f.write("\n".join(d2) + "\n")
P()
log("R3 done")

# ---------- R4 dominators ----------
P("## R4. Dominators below the root (what exists only to serve one lemma)\n")
# RPO over the archive subgraph reachable from ROOT (iterative DFS, children in name order for determinism)
order = []; seen = bytearray(N)
succ_a = {}
st = [(ROOT, iter(sorted((y for y in succ[ROOT] if arch[y]), key=lambda j: names[j])))]; seen[ROOT] = 1
while st:
    v, it = st[-1]
    nxt = next(it, None)
    if nxt is None: order.append(v); st.pop(); continue
    if seen[nxt]: continue
    seen[nxt] = 1; st.append((nxt, iter(sorted((y for y in succ[nxt] if arch[y]), key=lambda j: names[j]))))
rpo = order[::-1]; idx = [-1] * N
for k, v in enumerate(rpo): idx[v] = k
preds = collections.defaultdict(list)
for v in rpo:
    for w in succ[v]:
        if idx[w] >= 0: preds[w].append(v)
log(f"rpo {len(rpo)}")
idom = [-1] * N; idom[ROOT] = ROOT
def intersect(a, b):
    while a != b:
        while idx[a] > idx[b]: a = idom[a]
        while idx[b] > idx[a]: b = idom[b]
    return a
changed = True; passes = 0
while changed:
    changed = False; passes += 1
    for v in rpo[1:]:
        new = -1
        for p in preds[v]:
            if idom[p] != -1: new = p if new == -1 else intersect(p, new)
        if idom[v] != new: idom[v] = new; changed = True
    log(f"dominator pass {passes}")
children = collections.defaultdict(list)
for v in rpo:
    if v != ROOT: children[idom[v]].append(v)
holder = {}
for v in rpo:
    if L1[v] > 0:
        key = (module[v], L1[v], L2[v]); n = names[v]
        if key not in holder or (len(n), n) < (len(names[holder[key]]), names[holder[key]]): holder[key] = v
own = collections.Counter()
for key, v in holder.items(): own[v] = key[2] - key[1] + 1
dom_lines = {}; dom_count = {}
for v in order:
    dom_lines[v] = own[v] + sum(dom_lines[c] for c in children[v]); dom_count[v] = 1 + sum(dom_count[c] for c in children[v])
tot = dom_lines[ROOT]
P(f"Dominator iteration converged in {passes} passes. Dominated lines of the root: {tot:,} (distinct declaration ranges in the cone, each counted once); constants {dom_count[ROOT]:,}.\n")
P("### Top 40 constants by dominated declaration lines\n")
P("| constant | module | kind | dominated lines | share | dominated constants | own lines |")
P("|---|---|---|---|---|---|---|")
ranked = sorted(rpo, key=lambda v: (-dom_lines[v], names[v]))
for v in ranked[:40]:
    P(f"| `{names[v]}` | {module[v]} | {kind[v]} | {dom_lines[v]:,} | {100*dom_lines[v]/tot:.1f}% | {dom_count[v]:,} | {L2[v]-L1[v]+1 if L1[v] else 0} |")
with open(f"{out}/dominators.tsv", "w") as f:
    f.write("constant\tmodule\tkind\tidom\tdominated_lines\tdominated_constants\n")
    for v in ranked[:5000]: f.write(f"{names[v]}\t{module[v]}\t{kind[v]}\t{names[idom[v]]}\t{dom_lines[v]}\t{dom_count[v]}\n")
P()
P("### The spine: from the root, always the child dominating the most lines\n")
P("| step | constant | module | dominated lines | share of root | lines leaving the spine here |")
P("|---|---|---|---|---|---|")
v = ROOT; step = 0; spine = []
while True:
    ch = children[v]
    if not ch: spine.append(v); break
    ch.sort(key=lambda c: (-dom_lines[c], names[c]))
    nxt = ch[0]; leaving = dom_lines[v] - dom_lines[nxt]
    P(f"| {step} | `{names[v]}` | {module[v]} | {dom_lines[v]:,} | {100*dom_lines[v]/tot:.1f}% | {leaving:,} |")
    spine.append(v)
    if dom_lines[nxt] < 0.02 * tot: break
    v = nxt; step += 1
P()
P("### Children of each spine constant (where the lines go when they leave the spine)\n")
for v in spine:
    ch = sorted(children[v], key=lambda c: (-dom_lines[c], names[c]))[:8]
    if len(children[v]) > 1:
        P(f"- `{names[v]}` ({len(children[v])} dominated children): " + "; ".join(f"`{names[c]}` {dom_lines[c]:,} ({100*dom_lines[c]/tot:.1f}%)" for c in ch))
P()
with open(f"{out}/spine.txt", "w") as f: f.write("\n".join(names[v] for v in spine) + "\n")
with open(f"{out}/top_dominators.txt", "w") as f: f.write("\n".join(names[v] for v in ranked[:40]) + "\n")
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n")
log(f"written {out}")
