#!/usr/bin/env python3 -I
"""Proof-shape prior: shape statistics of many Mathlib proofs (same measures as the three archive traces) and a
crossing table of which subject directories are depended on together.
Usage: python3 -I prior.py GRAPH_DIR OUT_DIR   (GRAPH_DIR holds nodes.tsv, edges.tsv written by MathlibGraph.lean)
Env: SAMPLE (default 3000), TOPK (default 100), SEED (default 20261124), MINCONE (default 2000)."""
import sys, os, re, random, collections, time, statistics as st
sys.setrecursionlimit(10000)
data, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
SAMPLE = int(os.environ.get("SAMPLE", "3000")); TOPK = int(os.environ.get("TOPK", "100")); SEED = int(os.environ.get("SEED", "20261124")); MINCONE = int(os.environ.get("MINCONE", "2000"))
t0 = time.time()
def log(s): print(f"[{time.time()-t0:7.0f}s] {s}", flush=True)
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|^_private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def|\._abel_|\._simp_|\._nlinarith|\._linarith|\.«)")
RET = re.compile(r"((_alt\d*)+|_(bis|ter|quater)|_(new|old|v\d+|fix|fixed|final|redo|retry|again|rev|revised|corrected|patched))$")  # primes excluded: Mathlib house style
PRIME = re.compile(r"'+$")
names = []; ids = {}; kind = []; module = []; L1 = []; L2 = []
with open(f"{data}/nodes.tsv") as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 6: continue
        if p[0] in ids: continue
        ids[p[0]] = len(names); names.append(p[0]); kind.append(p[1]); module.append(p[2]); L1.append(int(p[4])); L2.append(int(p[5]))
N = len(names); log(f"nodes {N}")
succ = [[] for _ in range(N)]
with open(f"{data}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        ia = ids.get(a); ib = ids.get(b)
        if ia is None or ib is None or ia == ib: continue
        succ[ia].append(ib)
for i in range(N):
    if len(succ[i]) > 1: succ[i] = list(set(succ[i]))
log(f"edges {sum(len(s) for s in succ)}")
def dir2(m):
    c = m.split("."); return "/".join(c[:2]) if len(c) > 1 else c[0]
def dir_of(m): return "/".join(m.split(".")[:-1]) or m
def rng(v): return L2[v] - L1[v] + 1 if L1[v] else 0

def cone(root):
    seen = bytearray(N); st_ = [root]; res = []
    while st_:
        x = st_.pop()
        if seen[x]: continue
        seen[x] = 1; res.append(x); st_.extend(y for y in succ[x] if not seen[y])
    return res

def shape(root):
    """dominator tree of cone(root); returns dict of shape measures"""
    order = []; seen = bytearray(N)
    stack = [(root, iter(sorted(succ[root], key=lambda j: names[j])))]; seen[root] = 1
    while stack:
        v, it = stack[-1]; nxt = next(it, None)
        if nxt is None: order.append(v); stack.pop(); continue
        if seen[nxt]: continue
        seen[nxt] = 1; stack.append((nxt, iter(sorted(succ[nxt], key=lambda j: names[j]))))
    rpo = order[::-1]; idx = {v: k for k, v in enumerate(rpo)}
    preds = collections.defaultdict(list)
    for v in rpo:
        for w in succ[v]:
            if w in idx: preds[w].append(v)
    idom = {root: root}
    def inter(a, b):
        while a != b:
            while idx[a] > idx[b]: a = idom[a]
            while idx[b] > idx[a]: b = idom[b]
        return a
    changed = True
    while changed:
        changed = False
        for v in rpo[1:]:
            new = None
            for p in preds[v]:
                if p in idom: new = p if new is None else inter(p, new)
            if idom.get(v) != new: idom[v] = new; changed = True
    children = collections.defaultdict(list)
    for v in rpo:
        if v != root: children[idom[v]].append(v)
    holder = {}
    for v in rpo:
        if L1[v] > 0:
            key = (module[v], L1[v], L2[v]); n = names[v]
            if key not in holder or (len(n), n) < (len(names[holder[key]]), names[holder[key]]): holder[key] = v
    own = collections.Counter({v: k[2] - k[1] + 1 for k, v in holder.items()})
    dom = {}
    for v in order: dom[v] = own[v] + sum(dom[c] for c in children[v])
    tot = dom[root] or 1
    for v in rpo: children[v].sort(key=lambda c: (-dom[c], names[c]))
    # spine
    spine = []; v = root
    while True:
        spine.append(v)
        if not children[v]: break
        v = children[v][0]
    sp = [dom[v] / tot for v in spine]
    def at(k): return sp[k] if k < len(sp) else 0.0
    rootdir = dir2(module[root]); leave = next((k for k, v in enumerate(spine) if dir2(module[v]) != rootdir), None)
    hinges = [v for v in rpo if dom[v] >= 0.01 * tot]
    hown = [rng(v) for v in hinges]
    def joined(v): return dom[v] - (dom[children[v][0]] if children[v] else 0)
    js = sorted((joined(v) / tot for v in rpo if dom[v] >= 0.005 * tot), reverse=True)
    # substrate: directory with most own lines in the cone vs max dominator share in it
    dl = collections.Counter(); best = {}
    for v in rpo:
        d = dir2(module[v]); dl[d] += own[v]
        if d not in best or dom[v] > dom[best[d]]: best[d] = v
    bigd, bigl = dl.most_common(1)[0] if dl else ("", 0)
    named = [v for v in rpo if not AUX.search(names[v])]
    return dict(root=names[root], module=module[root], constants=len(rpo), named=len(named), lines=tot,
                sp1=at(1), sp2=at(2), sp3=at(3), sp5=at(5), sp8=at(8), spine_len=len(spine), leaves_dir_at=(leave if leave is not None else -1),
                leave_share=(sp[leave] if leave is not None else 0.0),
                hinges=len(hinges), hinge_own_median=(st.median(hown) if hown else 0), hinge_own_max=(max(hown) if hown else 0),
                hinge_retry=sum(1 for v in hinges if RET.search(names[v].rsplit(".", 1)[-1])), hinge_prime=sum(1 for v in hinges if PRIME.search(names[v].rsplit(".", 1)[-1])),
                joint1=(js[0] if js else 0), joint3=sum(js[:3]), top_dir=bigd, top_dir_share=bigl / tot, top_dir_maxdom=(dom[best[bigd]] / tot if bigd else 0),
                dirs=len(dl), retry_rate=(1000 * sum(1 for v in named if RET.search(names[v].rsplit(".", 1)[-1])) / max(len(named), 1)))

# ---------- sample ----------
cands = [i for i in range(N) if kind[i] == "thm" and module[i].startswith("Mathlib.") and not AUX.search(names[i])]
random.seed(SEED); sample = random.sample(cands, min(SAMPLE, len(cands)))
log(f"candidates {len(cands)} sampled {len(sample)}")
sizes = []
for k, r in enumerate(sample):
    sizes.append((len(cone(r)), r))
    if k % 500 == 0: log(f"cones {k}")
sizes.sort(reverse=True)
rep = []
def P(s=""): rep.append(s); print(s, flush=True)
P("# Proof-shape prior from Mathlib\n")
P(f"Graph: {N:,} constants, {sum(len(s) for s in succ):,} edges (Mathlib and the Lean libraries it imports). Sample: {len(sample):,} named Mathlib theorems drawn uniformly (seed {SEED}) from {len(cands):,}.\n")
P("## Q1. How big are Mathlib proofs? (constants in the cone of a random theorem)\n")
cs = [s for s, _ in sizes]
qs = st.quantiles(cs, n=10)
P("| decile | " + " | ".join(f"{10*(i+1)}%" for i in range(9)) + " | max |\n|---|" + "---|" * 10)
P("| cone constants | " + " | ".join(f"{int(q):,}" for q in qs) + f" | {max(cs):,} |")
P(f"\nMedian {int(st.median(cs)):,}; mean {int(st.mean(cs)):,}; cones of at least {MINCONE:,} constants: {sum(1 for c in cs if c >= MINCONE):,} of {len(cs):,}. The archive's cone is 1,265,256 archive constants plus 67,981 library constants at its boundary.\n")
big = [r for s, r in sizes[:TOPK] if s >= MINCONE]
log(f"shapes for {len(big)}")
rows = []
for k, r in enumerate(big):
    rows.append(shape(r))
    if k % 20 == 0: log(f"shape {k}")
# ---------- archive row (from the three traces of 2026-11-23) ----------
ARCH = dict(root="riemannHypothesis", constants=1265256, lines=10660526, sp1=1.0, sp2=1.0, sp3=1.0, sp5=0.6682, sp8=0.1134, spine_len=27, leaves_dir_at=13, leave_share=0.0172,
            hinges=81, hinge_own_median=4, hinge_own_max=88, hinge_retry=32, hinge_prime=1, joint1=0.2723, joint3=0.7176, top_dir="Development/AbelianVarietyTheory", top_dir_share=4675299/10660526, top_dir_maxdom=0.0172, retry_rate=15.4)
def med(k): return st.median(r[k] for r in rows)
def q(k, p): return st.quantiles([r[k] for r in rows], n=4)[p]
def pct(x): return f"{100*x:.1f}%"
P(f"## Q2. Shape of the {len(rows)} largest sampled Mathlib proofs against the archive\n")
P("Same measures as the three archive traces: spine share at steps 1, 2, 3, 5, 8 below the root; hinges = constants dominating at least 1% of the root's lines; joints = mass meeting at a constant; substrate = the second-level directory with the most lines in the cone and the largest share any constant in it dominates; retry marks exclude primes (Mathlib house style).\n")
P("| measure | Mathlib Q1 | median | Q3 | archive |\n|---|---|---|---|---|")
for key, label, f in [("constants", "cone constants", lambda x: f"{int(x):,}"), ("lines", "dominated lines", lambda x: f"{int(x):,}"),
                      ("sp1", "spine share, step 1", pct), ("sp2", "step 2", pct), ("sp3", "step 3", pct), ("sp5", "step 5", pct), ("sp8", "step 8", pct),
                      ("spine_len", "spine length (steps to a leaf)", lambda x: f"{x:.0f}"), ("leaves_dir_at", "step at which the spine leaves the root's directory", lambda x: f"{x:.0f}"), ("leave_share", "share when it does", pct),
                      ("hinges", "hinges at 1%", lambda x: f"{x:.0f}"), ("hinge_own_median", "median own lines of hinges", lambda x: f"{x:.0f}"), ("hinge_own_max", "longest hinge, lines", lambda x: f"{x:.0f}"),
                      ("hinge_retry", "hinges with a retry mark (no primes)", lambda x: f"{x:.0f}"), ("hinge_prime", "hinges with a prime", lambda x: f"{x:.0f}"),
                      ("joint1", "largest joint, share joined", pct), ("joint3", "three largest joints, share joined", pct),
                      ("top_dir_share", "largest directory's share of cone lines", pct), ("top_dir_maxdom", "largest share any constant in it dominates", pct),
                      ("retry_rate", "retry marks per 1,000 named constants (no primes)", lambda x: f"{x:.1f}")]:
    P(f"| {label} | {f(q(key,0))} | {f(med(key))} | {f(q(key,2))} | {f(ARCH[key])} |")
P()
P("### The ten largest sampled proofs\n")
P("| root | cone | lines | spine at 3 | at 5 | hinges | median own | largest dir | its max dom |\n|---|---|---|---|---|---|---|---|---|")
for r in sorted(rows, key=lambda r: -r["constants"])[:10]:
    P(f"| `{r['root']}` | {r['constants']:,} | {r['lines']:,} | {pct(r['sp3'])} | {pct(r['sp5'])} | {r['hinges']} | {r['hinge_own_median']:.0f} | {r['top_dir']} {pct(r['top_dir_share'])} | {pct(r['top_dir_maxdom'])} |")
P()
with open(f"{out}/shapes.tsv", "w") as f:
    keys = list(rows[0].keys()); f.write("\t".join(keys) + "\n")
    for r in rows: f.write("\t".join(str(r[k]) for k in keys) + "\n")
# where does the archive fall
def rank(key, val, higher_is_more=True):
    vals = [r[key] for r in rows]; below = sum(1 for v in vals if v < val); return below / len(vals)
P("### Where the archive falls in the Mathlib distribution (share of the sampled large proofs below the archive's value)\n")
P("| measure | archive | share of Mathlib proofs below it |\n|---|---|---|")
for key, label in [("sp3", "spine share at step 3"), ("sp5", "spine share at step 5"), ("hinges", "hinges at 1%"), ("hinge_own_median", "median own lines of hinges"), ("joint1", "largest joint"), ("top_dir_share", "largest directory's share"), ("top_dir_maxdom", "largest directory's max dominator"), ("retry_rate", "retry marks per 1,000"), ("spine_len", "spine length")]:
    v = ARCH[key]; P(f"| {label} | {pct(v) if isinstance(v, float) and v <= 1 else v} | {pct(rank(key, v))} |")
P(); log("Q2 done")
# ---------- Q3 crossings ----------
P("## Q3. Crossings: which second-level directories of Mathlib are depended on together\n")
P("For every named Mathlib theorem, the set of second-level directories (Mathlib/Analysis, Mathlib/NumberTheory, …) of its direct named dependencies, excluding its own directory and Lean's core libraries; pairs counted once per theorem.\n")
pair = collections.Counter(); single = collections.Counter(); ex = {}
for i in cands:
    ds = {dir2(module[j]) for j in succ[i] if module[j].startswith("Mathlib.") and not AUX.search(names[j])} - {dir2(module[i])}
    for d in ds: single[d] += 1
    ds = sorted(ds)
    for a in range(len(ds)):
        for b in range(a + 1, len(ds)):
            pair[(ds[a], ds[b])] += 1
            if (ds[a], ds[b]) not in ex: ex[(ds[a], ds[b])] = names[i]
P(f"Theorems {len(cands):,}; directories depended on {len(single)}; directory pairs seen together {len(pair):,}.\n")
P("Most common pairs:\n\n| pair | theorems |\n|---|---|")
for (a, b), c in pair.most_common(12): P(f"| {a} + {b} | {c:,} |")
# rarity: pairs where both directories are common (>= 2000 theorems depend on each) but the pair is rare
common = {d for d, c in single.items() if c >= 2000}
rare = sorted(((c, a, b) for (a, b), c in pair.items() if a in common and b in common), key=lambda t: t[0])[:12]
P("\nRarest pairs among directories that are each depended on by at least 2,000 theorems:\n\n| pair | theorems | one of them |\n|---|---|---|")
for c, a, b in rare: P(f"| {a} + {b} | {c:,} | `{ex[(a,b)]}` |")
expected = {}
with open(f"{out}/crossings.tsv", "w") as f:
    f.write("dir_a\tdir_b\ttheorems\tdepend_on_a\tdepend_on_b\tratio_to_independence\texample\n")
    T = len(cands)
    for (a, b), c in sorted(pair.items(), key=lambda t: -t[1]):
        e = single[a] * single[b] / T
        f.write(f"{a}\t{b}\t{c}\t{single[a]}\t{single[b]}\t{c/e if e else 0:.3f}\t{ex[(a,b)]}\n")
P("\nThe full table, with each pair's count against what independence would give, is in `crossings.tsv`.")
P(); log("Q3 done")
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n"); log(f"written {out}")
