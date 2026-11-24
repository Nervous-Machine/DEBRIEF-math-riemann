#!/usr/bin/env python3 -I
"""Crossing trace (layer two of the prior): what Mathlib directories do the wings of each joint reach, how different
are the wings, and how rare in Mathlib are the directory pairs a joint brings together. Same for the largest joints
of the 100 large Mathlib proofs of the prior trace, so the archive's joints can be placed. Also exports dominator
trees (constants at 0.1% or more) for the eight largest Mathlib proofs, for drawing.
Usage: python3 -I crossing.py ARCHIVE_DIR MATHLIB_DIR PRIOR_DIR OUT_DIR
ARCHIVE_DIR: nodes.tsv, edges.tsv of the archive walk; MATHLIB_DIR: nodes.tsv, edges.tsv of the Mathlib walk;
PRIOR_DIR: shapes.tsv (roots) and crossings.tsv (pair table). Env: ROOT (riemannHypothesis), TOPJ (20), TOPC (6)."""
import sys, os, re, collections, time, json, statistics as st
sys.setrecursionlimit(10000)
A, M, PR, out = sys.argv[1:5]; os.makedirs(out, exist_ok=True)
ROOT_N = os.environ.get("ROOT", "riemannHypothesis"); TOPJ = int(os.environ.get("TOPJ", "20")); TOPC = int(os.environ.get("TOPC", "6"))
t0 = time.time()
def log(s): print(f"[{time.time()-t0:7.0f}s] {s}", flush=True)
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|^_private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def|\._abel_|\._simp_|\._nlinarith|\._linarith|\.«)")
RET = re.compile(r"((_alt\d*)+|'+|_(bis|ter|quater)|_(new|old|v\d+|fix|fixed|final|redo|retry|again|rev|revised|corrected|patched))$")
def dir2(m):
    c = m.split("."); return "/".join(c[:2]) if len(c) > 1 else c[0]
# ---------- pair table ----------
ratio = {}; cnt = {}
with open(f"{PR}/crossings.tsv") as f:
    next(f)
    for line in f:
        a, b, c, da, db, r, ex = line.rstrip("\n").split("\t")
        ratio[(a, b)] = ratio[(b, a)] = float(r); cnt[(a, b)] = cnt[(b, a)] = int(c)
DIRS = sorted({a for a, b in ratio}); DI = {d: i for i, d in enumerate(DIRS)}
log(f"pair table {len(ratio)//2} pairs over {len(DIRS)} directories")

class G:
    def __init__(self, d, archive_only_expand):
        self.names = []; self.ids = {}; self.kind = []; self.module = []; self.arch = []; self.L1 = []; self.L2 = []
        with open(f"{d}/nodes.tsv") as f:
            next(f)
            for line in f:
                p = line.rstrip("\n").split("\t")
                if len(p) < 6 or p[0] in self.ids: continue
                self.ids[p[0]] = len(self.names); self.names.append(p[0]); self.kind.append(p[1]); self.module.append(p[2]); self.arch.append(p[3] == "1"); self.L1.append(int(p[4])); self.L2.append(int(p[5]))
        N = self.N = len(self.names); self.succ = [[] for _ in range(N)]
        with open(f"{d}/edges.tsv") as f:
            for line in f:
                a, _, b = line.rstrip("\n").partition("\t"); ia = self.ids.get(a); ib = self.ids.get(b)
                if ia is None or ib is None or ia == ib: continue
                self.succ[ia].append(ib)
        for i in range(N):
            if len(self.succ[i]) > 1: self.succ[i] = list(set(self.succ[i]))
        # footprint bit per node: Mathlib directory of the node itself (library nodes in the archive walk; every node in the Mathlib walk)
        self.bit = [0] * N
        for i in range(N):
            m = self.module[i]
            if m.startswith("Mathlib.") and not (archive_only_expand and self.arch[i]):
                dd = dir2(m)
                if dd in DI: self.bit[i] = 1 << DI[dd]
        self.expand = (lambda v: self.arch[v]) if archive_only_expand else (lambda v: True)
        log(f"graph {d}: {N} nodes, {sum(len(s) for s in self.succ)} edges")
    def rng(self, v): return self.L2[v] - self.L1[v] + 1 if self.L1[v] else 0
    def tree(self, root):
        """dominator tree over the expanded cone; returns rpo, order, idom, children, dom, own, fp (footprint masks over the full cone incl. library leaves)"""
        names, succ, ex = self.names, self.succ, self.expand
        order = []; seen = bytearray(self.N)
        stack = [(root, iter(sorted((y for y in succ[root] if ex(y)), key=lambda j: names[j])))]; seen[root] = 1
        while stack:
            v, it = stack[-1]; nxt = next(it, None)
            if nxt is None: order.append(v); stack.pop(); continue
            if seen[nxt]: continue
            seen[nxt] = 1; stack.append((nxt, iter(sorted((y for y in succ[nxt] if ex(y)), key=lambda j: names[j]))))
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
            if self.L1[v] > 0:
                key = (self.module[v], self.L1[v], self.L2[v]); n = names[v]
                if key not in holder or (len(n), n) < (len(names[holder[key]]), names[holder[key]]): holder[key] = v
        own = collections.Counter({v: k[2] - k[1] + 1 for k, v in holder.items()})
        dom = {}
        for v in order: dom[v] = own[v] + sum(dom[c] for c in children[v])
        for v in rpo: children[v].sort(key=lambda c: (-dom[c], names[c]))
        # footprints: postorder over the expanded cone; unexpanded successors (library leaves) contribute their own bit
        fp = {}
        bit = self.bit
        for v in order:
            m = bit[v]
            for w in succ[v]:
                if w in idx: m |= fp[w]
                else: m |= bit[w]
            fp[v] = m
        return rpo, order, idom, children, dom, own, fp

def bits(m): return [DIRS[i] for i in range(len(DIRS)) if m >> i & 1]
def jaccard_dist(a, b):
    u = bin(a | b).count("1"); return 1 - bin(a & b).count("1") / u if u else 0.0
def joint_measures(g, v, children, dom, fp, tot):
    ch = children[v][:TOPC]
    if len(ch) < 2: return None
    masks = [fp[c] for c in ch]
    excl = []
    for i, mk in enumerate(masks):
        others = 0
        for j, mo in enumerate(masks):
            if j != i: others |= mo
        excl.append(mk & ~others)
    pairs = []
    for i in range(len(ch)):
        for j in range(i + 1, len(ch)):
            for a in bits(excl[i]):
                for b in bits(excl[j]):
                    pairs.append((ratio.get((a, b), 0.0), cnt.get((a, b), 0), a, b, g.names[ch[i]], g.names[ch[j]]))
    pairs.sort()
    return dict(name=g.names[v], share=dom[v] / tot, joined=(dom[v] - dom[children[v][0]]) / tot, children=len(children[v]), own=g.rng(v),
                footprint=bin(fp[v]).count("1"), jd12=jaccard_dist(masks[0], masks[1]), jd_mean=(st.mean(jaccard_dist(masks[i], masks[j]) for i in range(len(masks)) for j in range(i + 1, len(masks)))),
                excl_dirs=sum(bin(e).count("1") for e in excl), n_pairs=len(pairs), rarest=(pairs[0] if pairs else None))

rep = []
def P(s=""): rep.append(s); print(s, flush=True)
def pc(x): return f"{100*x:.1f}%"
P("# Crossing trace: what the wings reach, and how rare the joins are\n")
P("Footprint of a constant = the set of Mathlib second-level directories its cone reaches (through the library boundary, for the archive). For a joint, the wings are its largest dominated children (up to six); a directory is exclusive to a wing when no other wing reaches it; the joint's crossings are the pairs of exclusive directories from different wings, each scored by how often Mathlib theorems depend on that pair together, as a ratio to what independence would give (crossings.tsv of the prior trace: 1 = as often as chance, below 1 = rarer, 0 = never seen together).\n")

# ---------- archive ----------
ga = G(A, archive_only_expand=True)
root = ga.ids[ROOT_N]
rpo, order, idom, children, dom, own, fp = ga.tree(root); tot = dom[root]
log(f"archive tree {len(rpo)}")
P("## X1. The archive\n")
P(f"The cone of `{ROOT_N}` reaches {bin(fp[root]).count('1')} of {len(DIRS)} Mathlib directories: " + ", ".join(bits(fp[root])) + ".\n")
missing = [d for d in DIRS if not (fp[root] >> DI[d]) & 1]
P(f"Not reached: {', '.join(missing) if missing else 'none'}.\n")
def joined(v): return dom[v] - (dom[children[v][0]] if children[v] else 0)
joints = sorted((v for v in rpo if dom[v] >= 0.005 * tot and len(children[v]) >= 2), key=lambda v: -joined(v))[:TOPJ]
arows = []
P(f"### The {len(joints)} largest joints: wings, footprints, rarest crossing\n")
P("| joint | joins | wings (of) | footprint | Jaccard distance of the two largest wings | exclusive dirs | rarest pair the wings bring together | ratio to chance | Mathlib theorems with that pair |\n|---|---|---|---|---|---|---|---|---|")
for v in joints:
    jm = joint_measures(ga, v, children, dom, fp, tot)
    if not jm: continue
    arows.append(jm); r = jm["rarest"]
    P(f"| `{jm['name'].split('.')[-1]}` | {pc(jm['joined'])} | {min(TOPC, jm['children'])} ({jm['children']}) | {jm['footprint']} | {jm['jd12']:.2f} | {jm['excl_dirs']} | {(r[2]+' + '+r[3]) if r else '(wings reach the same directories)'} | {f'{r[0]:.2f}' if r else ''} | {f'{r[1]:,}' if r else ''} |")
P()
# wings of the three largest joints in detail
P("### The wings of the three largest joints\n")
for jm_v in joints[:3]:
    P(f"`{ga.names[jm_v]}`:\n")
    ch = children[jm_v][:TOPC]; masks = [fp[c] for c in ch]
    for i, c in enumerate(ch):
        others = 0
        for j, mo in enumerate(masks):
            if j != i: others |= mo
        ex = bits(masks[i] & ~others)
        P(f"- `{ga.names[c].split('.')[-1]}` {pc(dom[c]/tot)}: reaches {bin(masks[i]).count('1')} directories" + (f"; only this wing reaches {', '.join(ex)}" if ex else "; nothing only this wing reaches"))
    P()
with open(f"{out}/archive_joints.tsv", "w") as f:
    f.write("joint\tshare\tjoined\tchildren\town_lines\tfootprint\tjd12\tjd_mean\texclusive_dirs\tpairs\trarest_ratio\trarest_count\trarest_a\trarest_b\twing_a\twing_b\n")
    for jm in arows:
        r = jm["rarest"] or (None, None, "", "", "", "")
        f.write(f"{jm['name']}\t{jm['share']:.5f}\t{jm['joined']:.5f}\t{jm['children']}\t{jm['own']}\t{jm['footprint']}\t{jm['jd12']:.4f}\t{jm['jd_mean']:.4f}\t{jm['excl_dirs']}\t{jm['n_pairs']}\t{'' if r[0] is None else f'{r[0]:.4f}'}\t{'' if r[1] is None else r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}\n")
# export the archive tree at 0.1% for drawing (same as hinges.tsv but with footprint size)
log("archive joints done")
del ga, rpo, order, idom, children, dom, own, fp
# ---------- Mathlib ----------
gm = G(M, archive_only_expand=False)
roots = [l.split("\t")[0] for l in open(f"{PR}/shapes.tsv")][1:]
mrows = []; trees = {}
for k, rn in enumerate(roots):
    r = gm.ids.get(rn)
    if r is None: continue
    rpo, order, idom, children, dom, own, fp = gm.tree(r); tot = dom[r] or 1
    def jn(v): return dom[v] - (dom[children[v][0]] if children[v] else 0)
    cand = [v for v in rpo if dom[v] >= 0.005 * tot and len(children[v]) >= 2]
    best = max(cand, key=jn) if cand else None
    row = dict(root=rn, cone=len(rpo), footprint=bin(fp[r]).count("1"))
    jm = joint_measures(gm, best, children, dom, fp, tot) if best is not None else None
    row["joint"] = jm
    mrows.append(row)
    if k < 8:
        sel = [v for v in rpo if dom[v] >= 0.001 * tot]; si = {v: i for i, v in enumerate(sel)}
        depth = {r: 0}
        for v in rpo:
            if v != r: depth[v] = depth[idom[v]] + 1
        trees[rn] = [[gm.names[v], si.get(idom[v], -1) if v != r else -1, dom[v], gm.rng(v), dir2(gm.module[v]), 1 if RET.search(gm.names[v].rsplit('.', 1)[-1]) else 0, len(children[v]), depth[v]] for v in sel]
    if k % 20 == 0: log(f"mathlib {k}")
json.dump(trees, open(f"{out}/mathlib_trees.json", "w"), separators=(",", ":"))
with open(f"{out}/mathlib_joints.tsv", "w") as f:
    f.write("root\tcone\tfootprint\tjoint\tjoined\tchildren\tjoint_footprint\tjd12\tjd_mean\texclusive_dirs\tpairs\trarest_ratio\trarest_count\trarest_a\trarest_b\n")
    for row in mrows:
        jm = row["joint"]
        if jm:
            r = jm["rarest"] or (None, None, "", "", "", "")
            f.write(f"{row['root']}\t{row['cone']}\t{row['footprint']}\t{jm['name']}\t{jm['joined']:.5f}\t{jm['children']}\t{jm['footprint']}\t{jm['jd12']:.4f}\t{jm['jd_mean']:.4f}\t{jm['excl_dirs']}\t{jm['n_pairs']}\t{'' if r[0] is None else f'{r[0]:.4f}'}\t{'' if r[1] is None else r[1]}\t{r[2]}\t{r[3]}\n")
        else: f.write(f"{row['root']}\t{row['cone']}\t{row['footprint']}\t\t\t\t\t\t\t\t\t\t\t\t\n")
P("## X2. The same measures for the largest joint of each of the 100 large Mathlib proofs\n")
fps = [row["footprint"] for row in mrows]; jms = [row["joint"] for row in mrows if row["joint"]]
def quart(xs):
    xs = list(xs)
    if len(xs) < 2: return (xs[0], xs[0], xs[0]) if xs else (0, 0, 0)
    q = st.quantiles(xs, n=4); return q[0], st.median(xs), q[2]
P(f"Mathlib directories reached by the cone: Q1/median/Q3 {quart(fps)[0]:.0f} / {quart(fps)[1]:.0f} / {quart(fps)[2]:.0f} of {len(DIRS)}; the archive reaches {arows[0]['footprint'] if arows else '?'} (measured at its largest joint, which carries the whole cone).\n")
jd = [j["jd12"] for j in jms]; ex = [j["excl_dirs"] for j in jms]
withpairs = [j for j in jms if j["rarest"]]
rr = [j["rarest"][0] for j in withpairs]
P("| measure | Mathlib Q1 | median | Q3 | archive, largest joint | archive, median of its top joints |\n|---|---|---|---|---|---|")
P(f"| Jaccard distance of the two largest wings | {quart(jd)[0]:.2f} | {quart(jd)[1]:.2f} | {quart(jd)[2]:.2f} | {arows[0]['jd12']:.2f} | {st.median(a['jd12'] for a in arows):.2f} |")
P(f"| directories exclusive to one wing | {quart(ex)[0]:.0f} | {quart(ex)[1]:.0f} | {quart(ex)[2]:.0f} | {arows[0]['excl_dirs']} | {st.median(a['excl_dirs'] for a in arows):.0f} |")
if rr:
    ar = [a['rarest'][0] for a in arows if a['rarest']]
    a0r = f"{arows[0]['rarest'][0]:.2f}" if arows and arows[0]['rarest'] else 'none'
    P(f"| rarest crossing, ratio to chance (joints with any exclusive pair: Mathlib {len(withpairs)} of {len(jms)}, archive {len(ar)} of {len(arows)}) | {quart(rr)[0]:.2f} | {quart(rr)[1]:.2f} | {quart(rr)[2]:.2f} | {a0r} | {f'{st.median(ar):.2f}' if ar else 'none'} |")
P()
P("Rarest crossings realised by Mathlib's largest joints (ten lowest ratios):\n\n| root | joint | pair | ratio | theorems |\n|---|---|---|---|---|")
for row in sorted((r for r in mrows if r["joint"] and r["joint"]["rarest"]), key=lambda r: r["joint"]["rarest"][0])[:10]:
    j = row["joint"]; r = j["rarest"]; P(f"| `{row['root']}` | `{j['name'].split('.')[-1]}` | {r[2]} + {r[3]} | {r[0]:.2f} | {r[1]:,} |")
P(); log("mathlib done")
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n"); log(f"written {out}")
