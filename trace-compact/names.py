#!/usr/bin/env python3 -I
"""Names and Mathlib footprint: the compact edition against the original archive.
Usage: python3 -I names.py COMPACT_GRAPH_DIR ARCHIVE_NAMES_ALL_TSV ARCHIVE_CONE_NODES_TSV OUT_DIR
COMPACT_GRAPH_DIR: nodes.tsv (id name kind module archive line_start line_end) and edges.tsv (integer ids) written by
CompactGraph.lean. ARCHIVE_NAMES_ALL_TSV: every constant of the archive's environment (trace-suffix, name kind module
archive). ARCHIVE_CONE_NODES_TSV: the constants reachable from the archive's five entry theorems, with the library
constants they use directly (trace-structure, name kind module archive line_start line_end).
Named = not matched by the AUX regex of trace-edit/edit.py (machine-generated names). Cone = project constants
reachable from the five entry theorems over project-internal edges, as edit.py computes it. Footprint = Mathlib
constants (module root Mathlib) used directly by a cone constant, as the archive's cone table records them."""
import sys, os, re, json
g, archnames, archcone, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
AUX = re.compile(r"(\._proof_\d+|\.proof_\d+|\._eq_\d+|\.eq_\d+|\.match_\d+|\._private\.|^_private\.|\._aux|_unexpander|\._sunfold|\._cstage|\.inst[A-Z]|\.eq_def|\._abel_|\._simp_|\._nlinarith|\._linarith|\._omega|\._lemma|\.noConfusion|\.rec$|\.recOn$|\.casesOn$|\.below$|\.brecOn$|\.ibelow$|\.binductionOn$|\.mk\.inj|\.sizeOf_spec|\.inj$|\.injEq$|\.ctorIdx|\.toCtorIdx|\.ofNat$|\.noConfusionType)")
ROOTS = ["riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re", "LFunction_eq_zero_re", "LFunction_eq_zero_re_of_isPrimitive"]
names, arch, module = [], [], []
with open(f"{g}/nodes.tsv") as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 7: continue
        names.append(p[1]); module.append(p[3]); arch.append(p[4] == "1")
N = len(names); idx = {n: i for i, n in enumerate(names)}
succ = [[] for _ in range(N)]; libuse = [[] for _ in range(N)]
with open(f"{g}/edges.tsv") as f:
    for line in f:
        a, _, b = line.rstrip("\n").partition("\t")
        try: ia = int(a); ib = int(b)
        except ValueError: continue
        if ia >= N or ib >= N or ia == ib or not arch[ia]: continue
        (succ if arch[ib] else libuse)[ia].append(ib)
seen = bytearray(N); stack = [idx[r] for r in ROOTS if r in idx]
while stack:
    x = stack.pop()
    if seen[x]: continue
    seen[x] = 1; stack.extend(y for y in succ[x] if not seen[y])
proj = [i for i in range(N) if arch[i]]
proj_named = {names[i] for i in proj if not AUX.search(names[i])}
cone_named = {names[i] for i in proj if seen[i] and not AUX.search(names[i])}
root = lambda m: m.split(".")[0]
fc = {names[j] for i in proj if seen[i] for j in libuse[i] if root(module[j]) == "Mathlib"}
compact_mathlib_all = {names[i] for i in range(N) if not arch[i] and root(module[i]) == "Mathlib"}
a_all = set()
with open(archnames) as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4 and p[3] == "1" and not AUX.search(p[0]): a_all.add(p[0])
a_cone, fa = set(), set()
with open(archcone) as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 4: continue
        if p[3] == "1":
            if not AUX.search(p[0]): a_cone.add(p[0])
        elif root(p[2]) == "Mathlib":
            fa.add(p[0])
last = lambda s: {n.rsplit(".", 1)[-1] for n in s}
r = {
    "compact_project_constants": len(proj), "compact_project_named": len(proj_named), "compact_cone_named": len(cone_named),
    "archive_named_all": len(a_all), "archive_cone_named": len(a_cone),
    "N1_compact_named_with_exact_archive_name": len(proj_named & a_all),
    "N1_share": round(len(proj_named & a_all) / max(len(proj_named), 1), 4),
    "N1b_compact_named_with_archive_last_component": sum(1 for n in proj_named if n.rsplit(".", 1)[-1] in last(a_all)),
    "N2_compact_cone_named_in_archive_cone": len(cone_named & a_cone),
    "N3_archive_cone_named_kept_by_exact_name": len(a_cone & proj_named),
    "N3_share": round(len(a_cone & proj_named) / max(len(a_cone), 1), 5),
    "F_compact_mathlib_direct": len(fc), "F_archive_mathlib_direct": len(fa),
    "F_intersection": len(fc & fa), "F_containment_compact_in_archive": round(len(fc & fa) / max(len(fc), 1), 4),
    "F_jaccard": round(len(fc & fa) / max(len(fc | fa), 1), 4),
    "F_archive_names_absent_from_compact_mathlib": len(fa - compact_mathlib_all),
}
json.dump(r, open(f"{out}/names.json", "w"), indent=1)
with open(f"{out}/kept_names.txt", "w") as f:
    f.write("\n".join(sorted(proj_named & a_all)) + "\n")
for k, v in r.items(): print(f"{k}\t{v}")
