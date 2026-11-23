#!/usr/bin/env python3 -I
"""Structure analysis of the dependency walk (nodes.tsv, edges.tsv) written by DepCone.lean.
Usage: python3 -I analyze.py DATA_DIR OUT_DIR
DATA_DIR holds nodes.tsv, edges.tsv, files_wc.txt (wc -l per .lean file, paths src/...), lines_per_dir.txt.
Writes OUT_DIR/report.md and several tsv files. Standard library only."""
import sys, os, re, collections

data, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ROOT = os.environ.get("ROOT", "riemannHypothesis")
FORK_HARD = os.environ.get("FORK_HARD", "UpperTheory.FinalTheorems.everyCharacter")
FORK_SHORT = os.environ.get("FORK_SHORT", "Formalism.VW.rh_of_every")
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def)")

# ---------- load ----------
nodes = {}  # name -> (kind, module, arch, l1, l2)
with open(f"{data}/nodes.tsv") as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 6: continue
        nodes[p[0]] = (p[1], p[2], p[3] == "1", int(p[4]), int(p[5]))
succ = collections.defaultdict(set)
with open(f"{data}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        if a != b: succ[a].add(b)
arch = {n for n, v in nodes.items() if v[2]}
lib = {n for n, v in nodes.items() if not v[2] and v[0] != "missing"}
missing = {n for n, v in nodes.items() if v[0] == "missing"}
print(f"nodes {len(nodes)} archive {len(arch)} library {len(lib)} missing {len(missing)} edges {sum(len(s) for s in succ.values())}")

# module -> file path and wc lines
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

def decl_lines(names):
    """Union of declaration ranges per module (avoids double counting auxiliary declarations)."""
    per_mod = collections.defaultdict(list)
    for n in names:
        k, m, a, l1, l2 = nodes[n]
        if l1 > 0: per_mod[m].append((l1, l2))
    total = 0
    for m, rs in per_mod.items():
        rs.sort(); cur_s, cur_e = rs[0]
        for s, e in rs[1:]:
            if s <= cur_e + 1: cur_e = max(cur_e, e)
            else: total += cur_e - cur_s + 1; cur_s, cur_e = s, e
        total += cur_e - cur_s + 1
    return total

def module_lines(names):
    mods = {nodes[n][1] for n in names}
    return sum(wc.get(mod_path(m), 0) for m in mods), len(mods)

def cone(start, restrict_arch=True):
    seen = set(); st = [start]
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x)
        if x in arch:
            for y in succ[x]:
                if y not in seen and (y in arch or not restrict_arch): st.append(y)
    return seen

rep = []
def P(s=""): rep.append(s); print(s)

# ---------- R2: the archive cone ----------
C = cone(ROOT) & arch
P(f"# Structure trace of the archive below `{ROOT}`\n")
P("## R2. The archive cone (constants the kernel uses for the main theorem)\n")
kinds = collections.Counter(nodes[n][0] for n in C)
aux = sum(1 for n in C if AUX.search(n))
dl = decl_lines(C); ml, nm = module_lines(C)
P(f"| measure | value |\n|---|---|")
P(f"| archive constants in the cone | {len(C):,} |")
P(f"| of which auxiliary (generated names) | {aux:,} |")
P(f"| by kind | {', '.join(f'{k} {v:,}' for k, v in kinds.most_common())} |")
P(f"| constants without a declaration range | {sum(1 for n in C if nodes[n][3] == 0):,} |")
P(f"| declaration lines (union of ranges) | {dl:,} |")
P(f"| modules touched | {nm:,} of {len(wc):,} |")
P(f"| lines of the modules touched | {ml:,} of {total_lines:,} ({100*ml/total_lines:.1f}%) |")
P(f"| library (Mathlib/Lean) constants named directly by archive constants | {len(lib):,} |")
P()
P("### Per top-level directory\n")
P("| directory | files total | modules touched | lines total | lines of touched modules | share touched | declaration lines used | constants used |")
P("|---|---|---|---|---|---|---|---|")
by_top = collections.defaultdict(set)
for n in C: by_top[top(nodes[n][1])].add(n)
rows = []
for d in sorted(set(dir_lines_total) | set(by_top)):
    ns = by_top.get(d, set()); ml_d, nm_d = module_lines(ns); lt = dir_lines_total.get(d, wc.get(f"src/{d}.lean", 0))
    rows.append((d, dir_files_total.get(d, 1 if f"src/{d}.lean" in wc else 0), nm_d, lt, ml_d, (100*ml_d/lt if lt else 0), decl_lines(ns), len(ns)))
for r in rows: P(f"| {r[0]} | {r[1]:,} | {r[2]:,} | {r[3]:,} | {r[4]:,} | {r[5]:.1f}% | {r[6]:,} | {r[7]:,} |")
with open(f"{out}/per_directory.tsv", "w") as f:
    f.write("directory\tfiles_total\tmodules_touched\tlines_total\tlines_touched_modules\tshare_pct\tdecl_lines\tconstants\n")
    for r in rows: f.write("\t".join(str(x) for x in r) + "\n")
P()
P("### Second-level directories (Development/, Formalism/, GroundTheory/, ReciprocityTheory/, CompanionTheory/)\n")
P("| directory | files total | modules touched | lines total | lines of touched modules | share | constants used |")
P("|---|---|---|---|---|---|---|")
by_top2 = collections.defaultdict(set)
for n in C: by_top2[top2(nodes[n][1])].add(n)
files2 = collections.Counter("/".join(p.split("/")[1:3]) for p in wc if p.count("/") >= 3)
lines2 = collections.Counter()
for p, l in wc.items():
    if p.count("/") >= 3: lines2["/".join(p.split("/")[1:3])] += l
rows2 = []
for d in sorted(set(files2) | {k for k in by_top2 if "/" in k}):
    ns = by_top2.get(d, set()); ml_d, nm_d = module_lines(ns)
    rows2.append((d, files2.get(d, 0), nm_d, lines2.get(d, 0), ml_d, (100*ml_d/lines2[d] if lines2.get(d) else 0), len(ns)))
for r in rows2: P(f"| {r[0]} | {r[1]:,} | {r[2]:,} | {r[3]:,} | {r[4]:,} | {r[5]:.1f}% | {r[6]:,} |")
with open(f"{out}/per_directory2.tsv", "w") as f:
    for r in rows2: f.write("\t".join(str(x) for x in r) + "\n")
P()
P("### Library boundary, by top-level module\n")
libtop = collections.Counter(top(nodes[n][1]) for n in lib)
P("| library | distinct constants named directly by the archive |\n|---|---|")
for k, v in libtop.most_common(): P(f"| {k} | {v:,} |")
P()

# ---------- R3: the fork ----------
P("## R3. The fork: `everyCharacter` versus `rh_of_every`\n")
H = cone(FORK_HARD) & arch if FORK_HARD in nodes else set()
Sh = cone(FORK_SHORT) & arch if FORK_SHORT in nodes else set()
def row(label, S):
    P(f"| {label} | {len(S):,} | {100*len(S)/len(C):.2f}% | {decl_lines(S):,} | {100*decl_lines(S)/dl:.2f}% | {module_lines(S)[1]:,} |")
P("| set | archive constants | share of cone | declaration lines | share of cone lines | modules |")
P("|---|---|---|---|---|---|")
row(f"cone({ROOT})", C)
row(f"cone({FORK_HARD})", H)
row(f"cone({FORK_SHORT})", Sh)
row("intersection", H & Sh)
row(f"cone({FORK_SHORT}) minus cone({FORK_HARD})", Sh - H)
row(f"cone({ROOT}) minus both", C - H - Sh)
P()
P(f"Constants in cone({ROOT}) outside both fork cones ({len(C - H - Sh)}): " + ", ".join(sorted(C - H - Sh)[:60]) + (" …" if len(C - H - Sh) > 60 else ""))
P(f"\nConstants in cone({FORK_SHORT}) not in cone({FORK_HARD}) ({len(Sh - H)}): " + ", ".join(sorted(Sh - H)[:80]) + (" …" if len(Sh - H) > 80 else ""))
P()

# ---------- R4: dominators ----------
P("## R4. Dominators below the root (what exists only to serve one lemma)\n")
# restrict to archive subgraph reachable from ROOT; DAG assumed (Lean constants are acyclic)
order = []; seen = set(); st = [(ROOT, iter(sorted(succ[ROOT] & arch)))]; seen.add(ROOT)
while st:
    v, it = st[-1]
    nxt = next(it, None)
    if nxt is None: order.append(v); st.pop(); continue
    if nxt in seen: continue
    seen.add(nxt); st.append((nxt, iter(sorted(succ[nxt] & arch))))
rpo = order[::-1]; idx = {v: i for i, v in enumerate(rpo)}
preds = collections.defaultdict(list)
for v in rpo:
    for w in succ[v]:
        if w in idx: preds[w].append(v)
idom = {ROOT: ROOT}
def intersect(a, b):
    while a != b:
        while idx[a] > idx[b]: a = idom[a]
        while idx[b] > idx[a]: b = idom[b]
    return a
changed = True; passes = 0
while changed:
    changed = False; passes += 1
    for v in rpo[1:]:
        cands = [p for p in preds[v] if p in idom]
        new = cands[0]
        for p in cands[1:]: new = intersect(p, new)
        if idom.get(v) != new: idom[v] = new; changed = True
print(f"dominator passes {passes}")
children = collections.defaultdict(list)
for v, d in idom.items():
    if v != ROOT: children[d].append(v)
# dominated declaration lines: each distinct (module, start, end) range is credited once, to the shortest-named
# constant that carries it (auxiliary declarations share their parent's range); then subtree sums in post-order.
holder = {}
for n in idx:
    k, m, a, l1, l2 = nodes[n]
    if l1 > 0:
        key = (m, l1, l2)
        if key not in holder or (len(n), n) < (len(holder[key]), holder[key]): holder[key] = n
own = collections.Counter()
for key, n in holder.items(): own[n] = key[2] - key[1] + 1
dom_lines = {}; dom_count = {}
for v in order:  # post-order of the DFS: every dominator-tree child is finished before its parent
    dom_lines[v] = own[v] + sum(dom_lines[c] for c in children[v])
    dom_count[v] = 1 + sum(dom_count[c] for c in children[v])
tot = dom_lines[ROOT]
P(f"Dominated lines of the root: {tot:,} (sum of distinct declaration ranges in the cone); constants {dom_count[ROOT]:,}.\n")
P("### Top 40 constants by dominated declaration lines\n")
P("| constant | module | kind | dominated lines | share | dominated constants | own lines |")
P("|---|---|---|---|---|---|---|")
ranked = sorted(idx, key=lambda v: -dom_lines[v])
for v in ranked[:40]:
    k, m, a, l1, l2 = nodes[v]
    P(f"| `{v}` | {m} | {k} | {dom_lines[v]:,} | {100*dom_lines[v]/tot:.1f}% | {dom_count[v]:,} | {l2-l1+1 if l1 else 0} |")
with open(f"{out}/dominators.tsv", "w") as f:
    f.write("constant\tmodule\tkind\tidom\tdominated_lines\tdominated_constants\n")
    for v in ranked: f.write(f"{v}\t{nodes[v][1]}\t{nodes[v][0]}\t{idom[v]}\t{dom_lines[v]}\t{dom_count[v]}\n")
P()
P("### The spine: from the root, always the child dominating the most lines\n")
P("| step | constant | module | dominated lines | share of root | lines leaving the spine here |")
P("|---|---|---|---|---|---|")
v = ROOT; step = 0; spine = []
while True:
    ch = children[v]
    if not ch: break
    ch.sort(key=lambda c: -dom_lines[c])
    nxt = ch[0]
    leaving = dom_lines[v] - dom_lines[nxt]
    k, m, a, l1, l2 = nodes[v]
    P(f"| {step} | `{v}` | {m} | {dom_lines[v]:,} | {100*dom_lines[v]/tot:.1f}% | {leaving:,} |")
    spine.append(v)
    if dom_lines[nxt] < 0.02 * tot: break
    v = nxt; step += 1
P()
P("### Children of each spine constant (where the lines go when they leave the spine)\n")
for v in spine:
    ch = sorted(children[v], key=lambda c: -dom_lines[c])[:8]
    if len(children[v]) > 1:
        P(f"- `{v}` ({len(children[v])} dominated children): " + "; ".join(f"`{c}` {dom_lines[c]:,} ({100*dom_lines[c]/tot:.1f}%)" for c in ch))
P()
with open(f"{out}/spine.txt", "w") as f: f.write("\n".join(spine) + "\n")
with open(f"{out}/top_dominators.txt", "w") as f: f.write("\n".join(ranked[:40]) + "\n")
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n")
print("written", out)
