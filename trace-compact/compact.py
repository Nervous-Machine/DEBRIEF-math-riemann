#!/usr/bin/env python3 -I
"""Shape of the compact edition: the measures of trace-prior/prior.py (its shape() copied unchanged) on the archive
part of a graph written by ArchiveGraph.lean, for the five entry theorems, with the archive's own earlier row and the
Mathlib quartiles beside the main one.
Usage: python3 -I edit.py GRAPH_DIR OUT_DIR [MATHLIB_SHAPES_TSV]"""
import sys, os, re, collections, time, statistics as st
data, out = sys.argv[1], sys.argv[2]; mshapes = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(out, exist_ok=True)
ROOTS = os.environ.get("ROOTS", "riemannHypothesis,riemannZeta_eq_zero_re,LFunction_ne_zero_of_half_lt_re,LFunction_eq_zero_re,LFunction_eq_zero_re_of_isPrimitive").split(",")  # ROOTS env only for the synthetic test
MAIN = ROOTS[0]
t0 = time.time()
def log(s): print(f"[{time.time()-t0:7.0f}s] {s}", flush=True)
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|^_private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def|\._abel_|\._simp_|\._nlinarith|\._linarith|\._omega|\._lemma|\.noConfusion|\.rec$|\.recOn$|\.casesOn$|\.below$|\.brecOn$|\.ibelow$|\.binductionOn$|\.mk\.inj|\.sizeOf_spec|\.inj$|\.injEq$|\.ctorIdx|\.toCtorIdx|\.ofNat$|\.noConfusionType)")
RET = re.compile(r"((_alt\d*)+|_(bis|ter|quater)|_(new|old|v\d+|fix|fixed|final|redo|retry|again|rev|revised|corrected|patched))$")
PRIME = re.compile(r"'+$")
names = []; ids = {}; kind = []; module = []; arch = []; L1 = []; L2 = []
byid = []   # amendment A1: nodes.tsv may carry an id column and edges.tsv integer ids; both formats are read
with open(f"{data}/nodes.tsv") as f:
    hdr = next(f).rstrip("\n").split("\t"); intfmt = hdr[0] == "id"
    for line in f:
        p = line.rstrip("\n").split("\t")
        if intfmt:
            if len(p) < 7: continue
            byid.append(ids.get(p[1], len(names))); p = p[1:]
        if len(p) < 6 or p[0] in ids: continue
        ids[p[0]] = len(names); names.append(p[0]); kind.append(p[1]); module.append(p[2]); arch.append(p[3] == "1"); L1.append(int(p[4])); L2.append(int(p[5]))
N = len(names); NA = sum(arch); log(f"nodes {N} archive {NA} ({'integer' if intfmt else 'name'} edges)")
succ = [[] for _ in range(N)]; ne = 0
with open(f"{data}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        if intfmt:
            try: ia = byid[int(a)]; ib = byid[int(b)]
            except (ValueError, IndexError): continue
        else:
            ia = ids.get(a); ib = ids.get(b)
        if ia is None or ib is None or ia == ib: continue
        ne += 1
        if arch[ia] and arch[ib]: succ[ia].append(ib)   # the archive's own graph, as the structure trace measured it
for i in range(N):
    if len(succ[i]) > 1: succ[i] = list(set(succ[i]))
log(f"edges {ne} inside the archive {sum(len(s) for s in succ)}")
def dir2(m):
    c = m.split("."); return "/".join(c[:2]) if len(c) > 1 else c[0]
def rng(v): return L2[v] - L1[v] + 1 if L1[v] else 0
def cone(root):
    seen = bytearray(N); st_ = [root]; res = []
    while st_:
        x = st_.pop()
        if seen[x]: continue
        seen[x] = 1; res.append(x); st_.extend(y for y in succ[x] if not seen[y])
    return res
def shape(root):
    """dominator tree of cone(root); returns dict of shape measures (copied from trace-prior/prior.py)"""
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
    changed = True; passes = 0
    while changed:
        changed = False; passes += 1
        for v in rpo[1:]:
            new = None
            for p in preds[v]:
                if p in idom: new = p if new is None else inter(p, new)
            if idom.get(v) != new: idom[v] = new; changed = True
        log(f"  dominator pass {passes}")
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
    dl = collections.Counter(); best = {}
    for v in rpo:
        d = dir2(module[v]); dl[d] += own[v]
        if d not in best or dom[v] > dom[best[d]]: best[d] = v
    bigd, bigl = dl.most_common(1)[0] if dl else ("", 0)
    named = [v for v in rpo if not AUX.search(names[v])]
    res = dict(root=names[root], module=module[root], constants=len(rpo), named=len(named), lines=tot,
                sp1=at(1), sp2=at(2), sp3=at(3), sp5=at(5), sp8=at(8), spine_len=len(spine), leaves_dir_at=(leave if leave is not None else -1),
                leave_share=(sp[leave] if leave is not None else 0.0),
                hinges=len(hinges), hinge_own_median=(st.median(hown) if hown else 0), hinge_own_max=(max(hown) if hown else 0),
                hinge_retry=sum(1 for v in hinges if RET.search(names[v].rsplit(".", 1)[-1])), hinge_prime=sum(1 for v in hinges if PRIME.search(names[v].rsplit(".", 1)[-1])),
                joint1=(js[0] if js else 0), joint3=sum(js[:3]), top_dir=bigd, top_dir_share=bigl / tot, top_dir_maxdom=(dom[best[bigd]] / tot if bigd else 0),
                dirs=len(dl), retry_rate=(1000 * sum(1 for v in named if RET.search(names[v].rsplit(".", 1)[-1])) / max(len(named), 1)))
    # the spine and the hinges, for the record
    with open(f"{out}/spine_{names[root]}.tsv", "w") as f:
        f.write("step\tname\tmodule\tshare\n")
        for k, v in enumerate(spine): f.write(f"{k}\t{names[v]}\t{module[v]}\t{dom[v]/tot:.5f}\n")
    with open(f"{out}/hinges_{names[root]}.tsv", "w") as f:
        f.write("name\tmodule\tdominated_share\town_lines\tjoined_share\n")
        for v in sorted(hinges, key=lambda v: -dom[v]): f.write(f"{names[v]}\t{module[v]}\t{dom[v]/tot:.5f}\t{rng(v)}\t{joined(v)/tot:.5f}\n")
    return res
# ---------- the archive before (trace-2026-11-23-structure/-closet/-suffix, via trace-prior/prior.py) ----------
ARCH = dict(root="riemannHypothesis", constants=1265256, lines=10660526, sp1=1.0, sp2=1.0, sp3=1.0, sp5=0.6682, sp8=0.1134, spine_len=27, leaves_dir_at=13, leave_share=0.0172,
            hinges=81, hinge_own_median=4, hinge_own_max=88, hinge_retry=32, hinge_prime=1, joint1=0.2723, joint3=0.7176, top_dir="Development/AbelianVarietyTheory", top_dir_share=4675299/10660526, top_dir_maxdom=0.0172,
            dirs=0, retry_rate=15.4)
rep = []
def P(s=""): rep.append(s); print(s, flush=True)
def pct(x): return f"{100*x:.1f}%"
P("# Shape of the compact edition\n")
anamed = [i for i in range(N) if arch[i] and not AUX.search(names[i])]
amods = len({module[i] for i in range(N) if arch[i]})
P(f"Graph: {N:,} constants in all, {NA:,} in the archive ({amods:,} archive modules), {len(anamed):,} of them named; {ne:,} edges, {sum(len(s) for s in succ):,} inside the archive. Retry marks (no primes) per 1,000 named archive constants: {1000*sum(1 for i in anamed if RET.search(names[i].rsplit('.',1)[-1]))/max(len(anamed),1):.1f} (before: 15.4 by the suffix trace's regexes over the whole archive).\n")
rows = {}
used = bytearray(N)
for r in ROOTS:
    if r not in ids: P(f"root `{r}` not in the graph"); continue
    log(f"shape {r}")
    rows[r] = shape(ids[r])
    for v in cone(ids[r]): used[v] = 1
P(f"Archive constants reached from any of the five entry theorems: {sum(used[i] for i in range(N) if arch[i]):,} of {NA:,} ({pct(sum(used[i] for i in range(N) if arch[i])/max(NA,1))}); before: 66% of the archive's constants by the suffix trace.\n")
if not rows: sys.exit("no root found in the graph")
with open(f"{out}/shapes_compact.tsv", "w") as f:
    keys = list(next(iter(rows.values())).keys()); f.write("\t".join(keys) + "\n")
    for r in rows.values(): f.write("\t".join(str(r[k]) for k in keys) + "\n")
M = None
if mshapes and os.path.exists(mshapes):
    import csv
    M = list(csv.DictReader(open(mshapes), delimiter="\t"))
    def mq(k, p): return st.quantiles([float(r[k]) for r in M], n=4)[p]
main = rows.get(MAIN)
if main:
    P(f"## `{MAIN}`: the archive before, the compact edition, and Mathlib's hundred\n")
    P("| measure | archive before | compact edition | Mathlib Q1 | median | Q3 |\n|---|---|---|---|---|---|")
    for key, label, f in [("constants", "cone constants", lambda x: f"{int(x):,}"), ("lines", "dominated lines", lambda x: f"{int(x):,}"),
                          ("sp1", "spine share, step 1", pct), ("sp2", "step 2", pct), ("sp3", "step 3", pct), ("sp5", "step 5", pct), ("sp8", "step 8", pct),
                          ("spine_len", "spine length", lambda x: f"{x:.0f}"), ("leaves_dir_at", "step at which the spine leaves the root's directory", lambda x: f"{x:.0f}"),
                          ("hinges", "hinges at 1%", lambda x: f"{x:.0f}"), ("hinge_own_median", "median own lines of hinges", lambda x: f"{x:.0f}"), ("hinge_own_max", "longest hinge, lines", lambda x: f"{x:.0f}"),
                          ("hinge_retry", "hinges with a retry mark", lambda x: f"{x:.0f}"), ("hinge_prime", "hinges with a prime", lambda x: f"{x:.0f}"),
                          ("joint1", "largest joint, share joined", pct), ("joint3", "three largest joints", pct),
                          ("top_dir_share", "largest directory's share of cone lines", pct), ("top_dir_maxdom", "largest share any constant in it dominates", pct),
                          ("retry_rate", "retry marks per 1,000 named constants", lambda x: f"{x:.1f}")]:
        mcols = f" {f(mq(key,0))} | {f(st.median(float(r[key]) for r in M))} | {f(mq(key,2))} |" if M else " | | |"
        P(f"| {label} | {f(ARCH[key])} | {f(main[key])} |{mcols}")
    P(f"\nLargest directory before: {ARCH['top_dir']}; now: {main['top_dir']} ({main['dirs']} directories in the cone).\n")
P("## The five entry theorems\n")
P("| root | cone | lines | spine at 3 | at 5 | hinges | median own | largest joint |\n|---|---|---|---|---|---|---|---|")
for r in rows.values(): P(f"| `{r['root']}` | {r['constants']:,} | {r['lines']:,} | {pct(r['sp3'])} | {pct(r['sp5'])} | {r['hinges']} | {r['hinge_own_median']:.0f} | {pct(r['joint1'])} |")
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n"); log(f"written {out}")
