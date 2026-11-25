import Main
open Lean
-- Write the dependency graph of every constant in the environment reachable from the archive's Main module (the
-- archive itself and the libraries it imports), module by module from the module table, with declaration ranges
-- taken from each module's range table. Same method and format as trace-prior/MathlibGraph.lean; the `archive`
-- column is 1 for a module that is not from a dependency package (Mathlib, Lean, Init, Std, Batteries, Aesop, Qq,
-- ProofWidgets, Plausible, ImportGraph, LeanSearchClient, Cli, Lake) and 0 otherwise.
-- nodes.tsv: id name kind module archive line_start line_end (id = line order); edges.tsv: user_id used_id as integers, so
-- that the table fits the disk (amendment A1: the first run wrote names and filled the disk at 34,000 modules).
-- Progress to a file every 1000 modules.
def outDir : String := "/home/heidibennett.guest/untrusted/alpoge-rh/edit/graph"
def depRoots : List String := ["Mathlib", "Lean", "Init", "Std", "Batteries", "Aesop", "Qq", "ProofWidgets", "Plausible", "ImportGraph", "LeanSearchClient", "Cli", "Lake"]
def isArchive (m : Name) : Bool := match m.getRoot with
  | .str _ s => !(depRoots.contains s)
  | _ => true
def kindOf : ConstantInfo → String
  | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"
def usedConsts (ci : ConstantInfo) : Array Name :=
  let a := ci.type.getUsedConstants
  match ci.value? (allowOpaque := true) with
  | some v => a ++ v.getUsedConstants
  | none => match ci with
    | .inductInfo val => a ++ val.ctors.toArray
    | .ctorInfo val => a.push val.induct
    | .recInfo val => a ++ val.all.toArray
    | _ => a
#eval show CoreM Unit from do
  let env ← getEnv
  let mods := env.header.moduleNames
  let datas := env.header.moduleData
  -- pass 1: ids, in module order then declaration order
  let mut ids : Std.HashMap Name Nat := {}
  let mut n := 0
  for i in [0:mods.size] do
    for c in datas[i]!.constants do
      ids := ids.insert c.name n
      n := n + 1
  let hn ← IO.FS.Handle.mk (outDir ++ "/nodes.tsv") .write
  let he ← IO.FS.Handle.mk (outDir ++ "/edges.tsv") .write
  let prog ← IO.FS.Handle.mk (outDir ++ "/progress.txt") .write
  hn.putStrLn "id\tname\tkind\tmodule\tarchive\tline_start\tline_end"
  let mut k := 0
  let mut ne := 0
  let mut missing := 0
  let mut na := 0
  for i in [0:mods.size] do
    let m := mods[i]!
    let d := datas[i]!
    let arch := if isArchive m then "1" else "0"
    if arch == "1" then na := na + 1
    let ranges := declRangeExt.getModuleEntries env i
    let mut nb := ""
    let mut eb := ""
    for c in d.constants do
      let (l1, l2) := match ranges.binSearch (c.name, default) (fun a b => Name.quickLt a.1 b.1) with
        | some (_, r) => (r.range.pos.line, r.range.endPos.line)
        | none => (0, 0)
      nb := nb ++ s!"{k}\t{c.name}\t{kindOf c}\t{m}\t{arch}\t{l1}\t{l2}\n"
      for u in usedConsts c do
        match ids.get? u with
        | some j => eb := eb ++ s!"{k}\t{j}\n"; ne := ne + 1
        | none => missing := missing + 1
      k := k + 1
    hn.putStr nb
    he.putStr eb
    if i % 1000 == 0 then
      prog.putStrLn s!"{i} modules {k} constants {ne} edges"
      prog.flush
  hn.flush; he.flush
  prog.putStrLn s!"done {mods.size} modules ({na} archive) {k} constants {ne} edges {missing} used names not in any module"; prog.flush
  IO.println s!"modules {mods.size} archive_modules {na} constants {k} edges {ne} missing_targets {missing}"
