#!/usr/bin/env python3 -I
"""Closet trace: on the dominator tree of the walk (nodes.tsv, edges.tsv from DepCone.lean), look for small
constants in small places that carry a large share of the proof. Same loading and dominator computation as
analyze2.py (integer-indexed Cooper-Harvey-Kennedy); new measures K1-K5 and a Lean file for K6.
Usage: python3 -I closet.py DATA_DIR OUT_DIR [ALREADY_PRINTED_FILE]
Env: ROOT (default riemannHypothesis), HINGE (share for K1, default 0.01), SMALLDIR (share for K2, default 0.02),
JOINT (share floor for K3, default 0.005), SHORT (own-line ceiling for a 'short joint', default 50)."""
import sys, os, re, collections, time
sys.setrecursionlimit(10000)
data, out = sys.argv[1], sys.argv[2]
already = set()
if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
    already = {l.strip() for l in open(sys.argv[3]) if l.strip()}
os.makedirs(out, exist_ok=True)
ROOT_N = os.environ.get("ROOT", "riemannHypothesis")
HINGE = float(os.environ.get("HINGE", "0.01"))
SMALLDIR = float(os.environ.get("SMALLDIR", "0.02"))
JOINT = float(os.environ.get("JOINT", "0.005"))
SHORT = int(os.environ.get("SHORT", "50"))
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
with open(f"{data}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        ia = ids.get(a); ib = ids.get(b)
        if ia is None or ib is None: continue
        if ia != ib: succ[ia].append(ib)
for i in range(N):
    if len(succ[i]) > 1: succ[i] = list(set(succ[i]))
log(f"edges {sum(len(s) for s in succ)}")

# ---------- source totals per directory ----------
def mod_path(m): return "src/" + m.replace(".", "/") + ".lean"
wc = {}
with open(f"{data}/files_wc.txt") as f:
    for line in f:
        p = line.split()
        if len(p) == 2: wc[p[1]] = int(p[0])
total_lines = sum(wc.values())
def dir2_of_path(p):           # src/A/B/C/.../X.lean -> A/B  (A alone when the file sits in A/)
    c = p.split("/")[1:-1]
    return "/".join(c[:2]) if c else "(root)"
def dir2_of_module(m):
    c = m.split(".")[:-1]
    return "/".join(c[:2]) if c else "(root)"
def dir_of_module(m): return "/".join(m.split(".")[:-1]) or "(root)"
dir2_lines = collections.Counter()
for p, n in wc.items(): dir2_lines[dir2_of_path(p)] += n
dir_lines = collections.Counter()
for p, n in wc.items(): dir_lines["/".join(p.split("/")[1:-1]) or "(root)"] += n

# ---------- cone, RPO, dominators (as analyze2.py) ----------
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
log(f"cone {len(rpo)}")
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
depth = {ROOT: 0}
for v in rpo:
    if v != ROOT: depth[v] = depth[idom[v]] + 1
for v in rpo: children[v].sort(key=lambda c: (-dom_lines[c], names[c]))
def biggest_child(v): return dom_lines[children[v][0]] if children[v] else 0
def joined(v): return dom_lines[v] - biggest_child(v)   # own lines plus every child but the largest: mass that meets at v and nowhere below
def rng(v): return L2[v] - L1[v] + 1 if L1[v] else 0
def pct(x): return f"{100*x/tot:.2f}%"
log(f"dominators done, root {tot}")

rep = []
def P(s=""): rep.append(s); print(s, flush=True)
P(f"# Closet trace below `{ROOT_N}`\n")
P(f"Dominator iteration converged in {passes} passes; root dominates {tot:,} declaration lines over {dom_count[ROOT]:,} constants. Archive source: {total_lines:,} lines.\n")

# ---------- K1 hinges ----------
P(f"## K1. Hinges: every constant dominating at least {100*HINGE:g}% of the root's lines\n")
hinges = sorted((v for v in rpo if dom_lines[v] >= HINGE * tot), key=lambda v: (-dom_lines[v], names[v]))
P(f"{len(hinges)} constants.\n")
P("| # | constant | directory | kind | own lines | dominates | share | constants | direct children | depth |")
P("|---|---|---|---|---|---|---|---|---|---|")
for k, v in enumerate(hinges, 1):
    P(f"| {k} | `{names[v]}` | {dir_of_module(module[v])} | {kind[v]} | {rng(v)} | {dom_lines[v]:,} | {pct(dom_lines[v])} | {dom_count[v]:,} | {len(children[v])} | {depth[v]} |")
with open(f"{out}/hinges.tsv", "w") as f:
    f.write("constant\tmodule\tkind\town_lines\tdominated_lines\tshare\tdominated_constants\tchildren\tdepth\tidom\tjoined_lines\n")
    for v in sorted((v for v in rpo if dom_lines[v] >= 0.001 * tot), key=lambda v: (-dom_lines[v], names[v])):
        f.write(f"{names[v]}\t{module[v]}\t{kind[v]}\t{rng(v)}\t{dom_lines[v]}\t{dom_lines[v]/tot:.5f}\t{dom_count[v]}\t{len(children[v])}\t{depth[v]}\t{names[idom[v]]}\t{joined(v)}\n")
P()
hd = collections.Counter(dir2_of_module(module[v]) for v in hinges)
P("Hinges per second-level directory: " + "; ".join(f"{d} {n}" for d, n in hd.most_common()))
P(); log("K1 done")

# ---------- K2 directories ----------
P(f"## K2. Second-level directories: size against the largest share any of their constants dominates\n")
P(f"A 'big theory' here is a second-level directory holding at least {100*SMALLDIR:g}% of the archive's lines. A closet by location is a constant dominating at least {100*HINGE:g}% of the root's lines whose module lies in a directory below that size.\n")
WRAPPER_DIRS = {"(root)", "Main", "Supplements/Kernels"}   # Main.lean and Supplements/Kernels/MainTheorems.lean: the 16-line wrapper file observed before registration; they hold the root and its two renamings, not a closet
best = {}
for v in rpo:
    d = dir2_of_module(module[v])
    if d not in best or dom_lines[v] > dom_lines[best[d]]: best[d] = v
used_lines = collections.Counter()
for v in rpo: used_lines[dir2_of_module(module[v])] += own[v]
rows = sorted(set(dir2_lines) | set(best), key=lambda d: -dir2_lines.get(d, 0))
P("| directory | lines | share of archive | dominated lines of its constants (own) | largest dominator in it | dominates | big theory? |")
P("|---|---|---|---|---|---|---|")
closets = []
with open(f"{out}/directories2.tsv", "w") as f:
    f.write("directory\tlines\tshare_of_archive\town_lines_used\tlargest_dominator\tits_dominated_lines\tits_share\n")
    for d in rows:
        tl = dir2_lines.get(d, 0); sh = tl / total_lines if total_lines else 0
        b = best.get(d)
        bn = names[b] if b is not None else ""; bl = dom_lines[b] if b is not None else 0
        big = sh >= SMALLDIR
        if b is not None and not big and bl >= HINGE * tot and d not in WRAPPER_DIRS: closets.append(b)
        if b is not None or tl > 0:
            P(f"| {d} | {tl:,} | {100*sh:.2f}% | {used_lines[d]:,} | {'`'+bn+'`' if bn else ''} | {pct(bl) if b is not None else ''} | {'yes' if big else ''} |")
        f.write(f"{d}\t{tl}\t{sh:.5f}\t{used_lines[d]}\t{bn}\t{bl}\t{bl/tot:.5f}\n")
P()
P(f"Big theories: {sum(1 for d in rows if dir2_lines.get(d,0)/total_lines >= SMALLDIR) if total_lines else 0} directories. Closets by location: {len(closets)}.")
for v in closets: P(f"- `{names[v]}` in {dir_of_module(module[v])} ({dir2_lines[dir2_of_module(module[v])]:,} lines, {100*dir2_lines[dir2_of_module(module[v])]/total_lines:.2f}% of the archive) dominates {dom_lines[v]:,} lines ({pct(dom_lines[v])}), own lines {rng(v)}")
with open(f"{out}/closets.txt", "w") as f: f.write("\n".join(names[v] for v in closets) + ("\n" if closets else ""))
P(); log("K2 done")

# ---------- K3 joints ----------
P(f"## K3. Joints: where dominated mass meets (constants dominating at least {100*JOINT:g}%, ranked by lines that meet at them and nowhere below)\n")
P("joined lines = own lines + dominated lines of every dominated child except the largest. A pure wrapper joins almost nothing; a constant that combines several large inputs joins a lot. A short joint has at most "
  f"{SHORT} own lines.\n")
cand = [v for v in rpo if dom_lines[v] >= JOINT * tot]
jr = sorted(cand, key=lambda v: (-joined(v), names[v]))
P("| # | constant | directory | own lines | joined lines | share | dominates | direct children | largest child |")
P("|---|---|---|---|---|---|---|---|---|")
for k, v in enumerate(jr[:20], 1):
    lc = children[v][0] if children[v] else None
    P(f"| {k} | `{names[v]}` | {dir_of_module(module[v])} | {rng(v)} | {joined(v):,} | {pct(joined(v))} | {pct(dom_lines[v])} | {len(children[v])} | {'`'+names[lc]+'` '+pct(dom_lines[lc]) if lc is not None else ''} |")
P()
short = [v for v in jr if rng(v) <= SHORT][:10]
P(f"Short joints (own lines at most {SHORT}), top ten by joined lines:\n")
P("| # | constant | directory | own lines | joined lines | share | direct children |")
P("|---|---|---|---|---|---|---|")
for k, v in enumerate(short, 1):
    P(f"| {k} | `{names[v]}` | {dir_of_module(module[v])} | {rng(v)} | {joined(v):,} | {pct(joined(v))} | {len(children[v])} |")
with open(f"{out}/joints.tsv", "w") as f:
    f.write("constant\tmodule\town_lines\tjoined_lines\tjoined_share\tdominated_lines\tchildren\n")
    for v in jr: f.write(f"{names[v]}\t{module[v]}\t{rng(v)}\t{joined(v)}\t{joined(v)/tot:.5f}\t{dom_lines[v]}\t{len(children[v])}\n")
P(); log("K3 done")

# ---------- K4 full spine ----------
P("## K4. The spine to its end: from the root, always the child dominating the most lines, until a constant with no dominated child\n")
P("| step | constant | directory | own lines | dominates | share | direct children |")
P("|---|---|---|---|---|---|---|")
v = ROOT; step = 0; spine = []; changes = []
while True:
    spine.append(v)
    P(f"| {step} | `{names[v]}` | {dir_of_module(module[v])} | {rng(v)} | {dom_lines[v]:,} | {pct(dom_lines[v])} | {len(children[v])} |")
    if step > 0 and dir2_of_module(module[v]) != dir2_of_module(module[spine[-2]]):
        changes.append((step, dir2_of_module(module[spine[-2]]), dir2_of_module(module[v]), dom_lines[v]))
    if not children[v]: break
    v = children[v][0]; step += 1
P()
P(f"Spine length {len(spine)} steps. Second-level directory changes along it: " + ("; ".join(f"step {s}: {a} → {b} at {pct(l)}" for s, a, b, l in changes) if changes else "none"))
with open(f"{out}/spine_full.txt", "w") as f: f.write("\n".join(names[v] for v in spine) + "\n")
P(); log("K4 done")

# ---------- K5 small-text, large-mass ----------
P(f"## K5. Leverage: constants dominating at least {100*JOINT:g}% with the fewest own lines per dominated line, wrappers excluded (at least 2 direct children)\n")
lev = sorted((v for v in cand if len(children[v]) >= 2 and rng(v) > 0), key=lambda v: (rng(v) / dom_lines[v], names[v]))[:20]
P("| # | constant | directory | own lines | dominates | share | direct children | joined share |")
P("|---|---|---|---|---|---|---|---|")
for k, v in enumerate(lev, 1):
    P(f"| {k} | `{names[v]}` | {dir_of_module(module[v])} | {rng(v)} | {dom_lines[v]:,} | {pct(dom_lines[v])} | {len(children[v])} | {pct(joined(v))} |")
P(); log("K5 done")

# ---------- K6 statements to print ----------
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.eq_def)")
want = []
for v in closets + jr[:10] + short + spine[-5:] + lev[:5]:
    n = names[v]
    if n not in already and n not in want and not AUX.search(n) and not n.startswith("_private."): want.append(n)
IDENT = re.compile(r"^[A-Za-z_α-ωΑ-Ω][A-Za-z0-9_'!?α-ωΑ-Ω₀-₉ᵢ-ᵪ]*$")
def lean_name(n): return ".".join(c if IDENT.match(c) else f"«{c}»" for c in n.split("."))
with open(f"{out}/K6_statements.lean", "w") as f:
    f.write("import Main\nset_option pp.proofs false\nset_option pp.maxSteps 100000\n-- K6: statements of the closets (if any), the ten largest joints, the short joints, the last five spine constants and the five highest-leverage constants, those not already printed in R5\n")
    for n in want: f.write(f"#check @{lean_name(n)}\n")
P(f"## K6. {len(want)} statements to print (K6_statements.lean): " + ", ".join(f"`{n}`" for n in want))
open(f"{out}/report.md", "w").write("\n".join(rep) + "\n")
log(f"written {out}")
