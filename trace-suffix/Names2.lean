import Main
open Lean
-- Dump every constant in the environment, module by module (ModuleData.constants), with kind and module. Replaces
-- Names.lean, which looked each constant's module up one at a time and ran at about 90 constants a second.
def archivePrefixes : List String := ["BuildAid","CompanionTheory","Development","Formalism","GroundTheory","Lemmata","PositivityTheory","ReciprocityTheory","Supplements","Statements","Main"]
def isArchiveModule (m : Name) : Bool := match m.components with | c :: _ => archivePrefixes.contains c.toString | [] => false
def kindOf : ConstantInfo → String
  | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"
def outPath : String := "/home/heidibennett.guest/untrusted/alpoge-rh/trace-structure/suffix/names_all.tsv"
def progPath : String := "/home/heidibennett.guest/untrusted/alpoge-rh/trace-structure/suffix/dump_progress.txt"
#eval show CoreM Unit from do
  let env ← getEnv
  let h ← IO.FS.Handle.mk outPath .write
  let prog ← IO.FS.Handle.mk progPath .write
  h.putStrLn "name\tkind\tmodule\tarchive"
  let mods := env.header.moduleNames
  let datas := env.header.moduleData
  let mut n := 0
  let mut na := 0
  for i in [0:mods.size] do
    let m := mods[i]!
    let d := datas[i]!
    let a := isArchiveModule m
    let flag := if a then "1" else "0"
    let mut buf := ""
    for c in d.constants do
      buf := buf ++ s!"{c.name}\t{kindOf c}\t{m}\t{flag}\n"
    h.putStr buf
    n := n + d.constants.size
    if a then na := na + d.constants.size
    if i % 2000 == 0 then
      prog.putStrLn s!"{i} modules {n} constants"
      prog.flush
  h.flush
  prog.putStrLn s!"done {mods.size} modules {n} constants"
  prog.flush
  IO.println s!"modules {mods.size} constants {n} archive {na} library {n - na}"
