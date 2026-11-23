import Main
open Lean
-- Dump every constant in the environment: name, kind, module. Archive flag by module prefix as in DepCone.lean.
def archivePrefixes : List String := ["BuildAid","CompanionTheory","Development","Formalism","GroundTheory","Lemmata","PositivityTheory","ReciprocityTheory","Supplements","Statements","Main"]
def isArchiveModule (m : Name) : Bool := match m.components with | c :: _ => archivePrefixes.contains c.toString | [] => false
def kindOf : ConstantInfo → String
  | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"
def outPath : String := "/home/heidibennett.guest/untrusted/alpoge-rh/trace-structure/suffix/names_all.tsv"
#eval show CoreM Unit from do
  let env ← getEnv
  let arr : Array (Name × String) := env.constants.fold (fun acc nm ci => acc.push (nm, kindOf ci)) #[]
  let h ← IO.FS.Handle.mk outPath .write
  h.putStrLn "name\tkind\tmodule\tarchive"
  let mut na := 0; let mut nl := 0
  for (nm, k) in arr do
    let m := match env.getModuleFor? nm with | some m => m | none => Name.anonymous
    let a := isArchiveModule m
    if a then na := na + 1 else nl := nl + 1
    h.putStrLn s!"{nm}\t{k}\t{m}\t{if a then "1" else "0"}"
  h.flush
  IO.println s!"constants {arr.size} archive {na} library {nl}"
