#!/usr/bin/env python3 -I
"""Suffix trace: retry fossils in constant names. Inputs: DATA_DIR (nodes.tsv, edges.tsv from DepCone.lean),
NAMES (names_all.tsv from Names.lean: every constant in the environment), OUT_DIR.
Usage: python3 -I suffix.py DATA_DIR NAMES OUT_DIR   Env: ROOT (default riemannHypothesis)."""
import sys, os, re, collections, time
sys.setrecursionlimit(10000)
data, namesf, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
ROOT_N = os.environ.get("ROOT", "riemannHypothesis")
t0 = time.time()
def log(s): print(f"[{time.time()-t0:7.0f}s] {s}", flush=True)
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|^_private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def|\._abel_|\._simp_|\._nlinarith|\._linarith|\.«)")
# registered suffix classes, applied to the last name component
CLASSES = [
  ("alt",      re.compile(r"(_alt\d*)+$")),
  ("prime",    re.compile(r"'+$")),
  ("bis_ter",  re.compile(r"_(bis|ter|quater)$")),
  ("fixword",  re.compile(r"_(new|old|v\d+|fix|fixed|final|redo|retry|again|rev|revised|corrected|patched)$")),
  ("numbered", re.compile(r"[a-z](\d+)$")),   # noisy: GL3, GSp4 and friends are excluded by requiring a lowercase letter before the digits, but 'Slim2' and 'n5' both match
]
STRIP = re.compile(r"((_alt\d*)+|'+|_(bis|ter|quater)|_(new|old|v\d+|fix|fixed|final|redo|retry|again|rev|revised|corrected|patched))+$")
def last(n): return n.rsplit(".", 1)[-1]
def classes_of(n):
    l = last(n); return [c for c, r in CLASSES if r.search(l)]
def alt_depth(n): return len(re.findall(r"_alt\d*", last(n))) if CLASSES[0][1].search(last(n)) else 0
def base_of(n):
    ns, _, l = n.rpartition("."); b = STRIP.sub("", l)
    return (ns + "." + b) if ns else b

# ---------- all names ----------
allk = {}; allmod = {}; arch_all = set(); lib_all = set()
with open(namesf) as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 4: continue
        allk[p[0]] = p[1]; allmod[p[0]] = p[2]
        (arch_all if p[3] == "1" else lib_all).add(p[0])
log(f"environment constants {len(allk)} archive {len(arch_all)} library {len(lib_all)}")

# ---------- walk tables, cone, dominators (as closet.py) ----------
names = []; ids = {}; kind = []; module = []; arch = []; L1 = []; L2 = []
with open(f"{data}/nodes.tsv") as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 6: continue
        ids[p[0]] = len(names); names.append(p[0]); kind.append(p[1]); module.append(p[2]); arch.append(p[3] == "1")
        L1.append(int(p[4])); L2.append(int(p[5]))
N = len(names)
succ = [[] for _ in range(N)]
with open(f"{data}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        ia = ids.get(a); ib = ids.get(b)
        if ia is None or ib is None: continue
        if ia != ib: succ[ia].append(ib)
for i in range(N):
    if len(succ[i]) > 1: succ[i] = list(set(succ[i]))
ROOT = ids[ROOT_N]
order = []; seen = bytearray(N)
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
idom = [-1] * N; idom[ROOT] = ROOT
def intersect(a, b):
    while a != b:
        while idx[a] > idx[b]: a = idom[a]
        while idx[b] > idx[a]: b = idom[b]
    return a
changed = True
while changed:
    changed = False
    for v in rpo[1:]:
        new = -1
        for p in preds[v]:
            if idom[p] != -1: new = p if new == -1 else intersect(p, new)
        if idom[v] != new: idom[v] = new; changed = True
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
dom_lines = {}
for v in order: dom_lines[v] = own[v] + sum(dom_lines[c] for c in children[v])
tot = dom_lines[ROOT]
cone = {names[v] for v in rpo}
log(f"cone {len(cone)} root lines {tot}")

rep = []
def P(s=""): rep.append(s); print(s, flush=True)
def pc(a, b): return f"{100*a/b:.2f}%" if b else "n/a"
P(f"# Suffix trace: retry fossils in the names below `{ROOT_N}`\n")

# ---------- S0 reach at the constant level ----------
P("## S0. The environment, and how much of the archive's constants the proof uses\n")
arch_named = {n for n in arch_all if not AUX.search(n)}
cone_named = {n for n in cone if not AUX.search(n)}
P("| set | constants | of which machine-named (aux) |\n|---|---|---|")
P(f"| environment | {len(allk):,} | {sum(1 for n in allk if AUX.search(n)):,} |")
P(f"| archive (all modules) | {len(arch_all):,} | {len(arch_all)-len(arch_named):,} |")
P(f"| library (Mathlib, Lean, Init, …) | {len(lib_all):,} | {sum(1 for n in lib_all if AUX.search(n)):,} |")
P(f"| cone of the root | {len(cone):,} | {len(cone)-len(cone_named):,} |")
P(f"| cone, as share of archive | {pc(len(cone), len(arch_all))} | named only: {pc(len(cone_named), len(arch_named))} |")
P()
def top(m): return m.split(".")[0]
def top2(m): c = m.split("."); return "/".join(c[:2]) if len(c) > 1 else c[0]
P("### Archive constants per top-level directory: written vs used\n")
P("| directory | constants | in the cone | share | named constants | named in cone | share |\n|---|---|---|---|---|---|---|")
wa = collections.Counter(top(allmod[n]) for n in arch_all); ua = collections.Counter(top(allmod[n]) for n in cone if n in allmod)
wn = collections.Counter(top(allmod[n]) for n in arch_named); un = collections.Counter(top(allmod[n]) for n in cone_named if n in allmod)
for d, c in wa.most_common(): P(f"| {d} | {c:,} | {ua[d]:,} | {pc(ua[d], c)} | {wn[d]:,} | {un[d]:,} | {pc(un[d], wn[d])} |")
P()
wa2 = collections.Counter(top2(allmod[n]) for n in arch_named); ua2 = collections.Counter(top2(allmod[n]) for n in cone_named if n in allmod)
with open(f"{out}/reach_dir2.tsv", "w") as f:
    f.write("directory\tnamed_constants\tnamed_in_cone\tshare\n")
    for d, c in wa2.most_common(): f.write(f"{d}\t{c}\t{ua2[d]}\t{ua2[d]/c:.4f}\n")
P("Second-level directories with the lowest named-constant usage (at least 1,000 named constants):\n")
P("| directory | named constants | in cone | share |\n|---|---|---|---|")
for d, c in sorted(((d, c) for d, c in wa2.items() if c >= 1000), key=lambda t: ua2[t[0]]/t[1])[:15]: P(f"| {d} | {c:,} | {ua2[d]:,} | {pc(ua2[d], c)} |")
P(); log("S0 done")

# ---------- S1 suffix classes ----------
P("## S1. Suffix classes, archive against library (named constants only)\n")
P("| class | archive, all | per 1,000 | archive, in cone | per 1,000 | library | per 1,000 |\n|---|---|---|---|---|---|---|")
lib_named = {n for n in lib_all if not AUX.search(n)}
cls_arch = collections.Counter(); cls_cone = collections.Counter(); cls_lib = collections.Counter()
for n in arch_named:
    for c in classes_of(n): cls_arch[c] += 1
for n in cone_named:
    for c in classes_of(n): cls_cone[c] += 1
for n in lib_named:
    for c in classes_of(n): cls_lib[c] += 1
for c, _ in CLASSES:
    P(f"| {c} | {cls_arch[c]:,} | {1000*cls_arch[c]/len(arch_named):.1f} | {cls_cone[c]:,} | {1000*cls_cone[c]/len(cone_named):.1f} | {cls_lib[c]:,} | {1000*cls_lib[c]/len(lib_named):.1f} |")
anyr = lambda n: any(c != "numbered" for c in classes_of(n))
ra, rc, rl = sum(1 for n in arch_named if anyr(n)), sum(1 for n in cone_named if anyr(n)), sum(1 for n in lib_named if anyr(n))
P(f"| any retry class (alt, prime, bis_ter, fixword) | {ra:,} | {1000*ra/len(arch_named):.1f} | {rc:,} | {1000*rc/len(cone_named):.1f} | {rl:,} | {1000*rl/len(lib_named):.1f} |")
P()
fw = collections.Counter(); 
for n in arch_named:
    m = CLASSES[3][1].search(last(n))
    if m: fw[m.group(1)] += 1
P("Fix-words in the archive: " + (", ".join(f"{w} {c:,}" for w, c in fw.most_common()) or "none"))
P(); log("S1 done")

# ---------- S2 alt depth ----------
P("## S2. How many times `_alt` is stacked\n")
P("| depth | archive, all | archive, in cone | examples (in cone) |\n|---|---|---|---|")
da = collections.Counter(alt_depth(n) for n in arch_named if alt_depth(n)); dc = collections.Counter(alt_depth(n) for n in cone_named if alt_depth(n))
ex = collections.defaultdict(list)
for n in sorted(cone_named):
    d = alt_depth(n)
    if d and len(ex[d]) < 3: ex[d].append(n)
for d in sorted(da): P(f"| {d} | {da[d]:,} | {dc[d]:,} | {', '.join('`'+e+'`' for e in ex[d])} |")
P(f"\nDeepest stack in the archive: {max(da) if da else 0}; in the cone: {max(dc) if dc else 0}.")
P(); log("S2 done")

# ---------- S3 families ----------
P("## S3. Families: a base name and its retry variants\n")
P("A family is the set of archive constants (named, same namespace) that strip to the same base name under the registered suffix rules. Only families with at least two members are counted.\n")
fam = collections.defaultdict(set)
for n in arch_named: fam[base_of(n)].add(n)
fams = {b: ms for b, ms in fam.items() if len(ms) >= 2}
sizes = collections.Counter(len(ms) for ms in fams.values())
P(f"Families with at least two members: {len(fams):,}, covering {sum(len(ms) for ms in fams.values()):,} constants. Size distribution: " + ", ".join(f"{s}: {c:,}" for s, c in sorted(sizes.items())))
# how many members in the cone
inc = collections.Counter(); only_latest = 0; several = 0; none_used = 0; base_used_with_variant = 0
def rank(n):   # later retry = higher rank: alt depth, then primes, then bis/ter/fixword, then base
    l = last(n); return (alt_depth(n), len(re.search(r"'*$", l).group(0)), 1 if CLASSES[2][1].search(l) or CLASSES[3][1].search(l) else 0)
rows = []
for b, ms in fams.items():
    used = [m for m in ms if m in cone]
    inc[len(used)] += 1
    if not used: none_used += 1
    elif len(used) >= 2: several += 1
    else:
        latest = max(ms, key=rank)
        if used[0] == latest: only_latest += 1
    if b in ms and b in cone and any(m != b and m in cone for m in ms): base_used_with_variant += 1
    rows.append((len(ms), len(used), b))
P(f"\n| members in the cone | families |\n|---|---|")
for k in sorted(inc): P(f"| {k} | {inc[k]:,} |")
P(f"\nFamilies with no member in the cone: {none_used:,} ({pc(none_used, len(fams))}). Exactly one member used and it is the latest variant: {only_latest:,}. Two or more members used (earlier versions still load-bearing): {several:,} ({pc(several, len(fams))}). Base name used alongside a variant: {base_used_with_variant:,}.")
P("\nLargest families:\n\n| members | in cone | base |\n|---|---|---|")
for s, u, b in sorted(rows, reverse=True)[:25]: P(f"| {s} | {u} | `{b}` |")
with open(f"{out}/families.tsv", "w") as f:
    f.write("base\tmembers\tin_cone\tnames\n")
    for b, ms in sorted(fams.items(), key=lambda t: -len(t[1])): f.write(f"{b}\t{len(ms)}\t{sum(1 for m in ms if m in cone)}\t{' '.join(sorted(ms))}\n")
P(); log("S3 done")

# ---------- S4 where the suffixed constants sit ----------
P("## S4. Retry suffixes on the hinges and along the spine\n")
hinges = [v for v in rpo if dom_lines[v] >= 0.01 * tot]
hs = [v for v in hinges if anyr(names[v])]
P(f"Hinges (at least 1% of the root's lines): {len(hinges)}; with a retry suffix: {len(hs)} ({pc(len(hs), len(hinges))}).")
P("| hinge with retry suffix | dominates | classes |\n|---|---|---|")
for v in sorted(hs, key=lambda v: -dom_lines[v]): P(f"| `{names[v]}` | {pc(dom_lines[v], tot)} | {', '.join(c for c in classes_of(names[v]) if c != 'numbered')} |")
v = ROOT; spine = []
while True:
    spine.append(v)
    if not children[v]: break
    v = max(children[v], key=lambda c: (dom_lines[c], names[c]))
ss = [v for v in spine if anyr(names[v])]
P(f"\nSpine constants: {len(spine)}; with a retry suffix: {len(ss)}: " + ", ".join(f"`{names[v]}`" for v in ss))
# dominated lines under suffixed constants whose idom is not suffixed (top-most suffixed), as a share
topmost = [v for v in rpo if anyr(names[v]) and (v == ROOT or not anyr(names[idom[v]]))]
P(f"\nLines dominated by the top-most retry-suffixed constants (no suffixed dominator above them): {sum(dom_lines[v] for v in topmost):,} of {tot:,} ({pc(sum(dom_lines[v] for v in topmost), tot)}).")
P("\nPer top-level directory, retry-suffixed share of the named constants in the cone:\n\n| directory | named in cone | with retry suffix | share |\n|---|---|---|---|")
cd = collections.Counter(top(allmod.get(n, module[ids[n]])) for n in cone_named); cs = collections.Counter(top(allmod.get(n, module[ids[n]])) for n in cone_named if anyr(n))
for d, c in cd.most_common(): P(f"| {d} | {c:,} | {cs[d]:,} | {pc(cs[d], c)} |")
P(); log("S4 done")
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n")
log(f"written {out}")
