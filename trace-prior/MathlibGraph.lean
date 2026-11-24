import Mathlib
open Lean
-- Write the dependency graph of every constant in the environment (Mathlib and the Lean libraries it imports), module
-- by module from the module table, with declaration ranges taken from each module's range table in one call.
-- nodes.tsv: name kind module archive(0) line_start line_end; edges.tsv: user used. Progress to a file every 1000 modules.
def outDir : String := "/home/heidibennett.guest/untrusted/alpoge-rh/trace-structure/prior"
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
  let hn ← IO.FS.Handle.mk (outDir ++ "/nodes.tsv") .write
  let he ← IO.FS.Handle.mk (outDir ++ "/edges.tsv") .write
  let prog ← IO.FS.Handle.mk (outDir ++ "/progress.txt") .write
  hn.putStrLn "name\tkind\tmodule\tarchive\tline_start\tline_end"
  let mods := env.header.moduleNames
  let datas := env.header.moduleData
  let mut n := 0
  let mut ne := 0
  for i in [0:mods.size] do
    let m := mods[i]!
    let d := datas[i]!
    let ranges := declRangeExt.getModuleEntries env i
    let mut nb := ""
    let mut eb := ""
    for c in d.constants do
      let (l1, l2) := match ranges.binSearch (c.name, default) (fun a b => Name.quickLt a.1 b.1) with
        | some (_, r) => (r.range.pos.line, r.range.endPos.line)
        | none => (0, 0)
      nb := nb ++ s!"{c.name}\t{kindOf c}\t{m}\t0\t{l1}\t{l2}\n"
      for u in usedConsts c do
        eb := eb ++ s!"{c.name}\t{u}\n"
        ne := ne + 1
      n := n + 1
    hn.putStr nb
    he.putStr eb
    if i % 1000 == 0 then
      prog.putStrLn s!"{i} modules {n} constants {ne} edges"
      prog.flush
  hn.flush; he.flush
  prog.putStrLn s!"done {mods.size} modules {n} constants {ne} edges"; prog.flush
  IO.println s!"modules {mods.size} constants {n} edges {ne}"
