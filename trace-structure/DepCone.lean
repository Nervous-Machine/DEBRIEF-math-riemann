import Main
open Lean

/-- Top-level module components that belong to the archive (lakefile.toml defaultTargets plus Statements). -/
def archivePrefixes : List String :=
  ["BuildAid", "CompanionTheory", "Development", "Formalism", "GroundTheory", "Lemmata",
   "PositivityTheory", "ReciprocityTheory", "Supplements", "Statements", "Main"]
def outDir : String := "/home/heidibennett.guest/untrusted/alpoge-rh/trace-structure"
/-- The five entry theorems of Main.lean. -/
def roots : Array Name :=
  #[`riemannHypothesis, `riemannZeta_eq_zero_re, `LFunction_ne_zero_of_half_lt_re,
    `LFunction_eq_zero_re, `LFunction_eq_zero_re_of_isPrimitive]

def isArchiveModule (m : Name) : Bool :=
  match m.components with
  | c :: _ => archivePrefixes.contains c.toString
  | [] => false

def kindOf : ConstantInfo → String
  | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "thm" | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quot" | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"

/-- Every constant named in the type or the value (proof term) of a constant. -/
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
  let hN ← IO.FS.Handle.mk (outDir ++ "/nodes.tsv") .write
  let hE ← IO.FS.Handle.mk (outDir ++ "/edges.tsv") .write
  hN.putStrLn "name\tkind\tmodule\tarchive\tline_start\tline_end"
  let mut visited : NameSet := {}
  let mut stack : Array Name := roots
  let mut nArch := 0
  let mut nLib := 0
  let mut nEdges := 0
  let mut nMissing := 0
  while stack.size > 0 do
    let n := stack.back!
    stack := stack.pop
    if visited.contains n then continue
    visited := visited.insert n
    match env.find? n with
    | none =>
      nMissing := nMissing + 1
      hN.putStrLn s!"{n}\tmissing\t\t0\t0\t0"
    | some ci =>
      let modName := env.getModuleFor? n
      let isArch := (modName.map isArchiveModule).getD false
      let rng ← findDeclarationRanges? n
      let (l1, l2) := match rng with
        | some r => (r.range.pos.line, r.range.endPos.line)
        | none => (0, 0)
      hN.putStrLn s!"{n}\t{kindOf ci}\t{modName.getD Name.anonymous}\t{if isArch then 1 else 0}\t{l1}\t{l2}"
      if isArch then
        nArch := nArch + 1
        for d in usedConsts ci do
          hE.putStrLn s!"{n}\t{d}"
          nEdges := nEdges + 1
          if !visited.contains d then
            stack := stack.push d
      else
        nLib := nLib + 1
    if (nArch + nLib) % 20000 == 0 then
      IO.eprintln s!"progress: archive {nArch} library {nLib} edges {nEdges}"
  hN.flush
  hE.flush
  IO.println s!"archive constants {nArch}; library boundary constants {nLib}; edges written {nEdges}; missing {nMissing}; modules in environment {env.header.moduleNames.size}"
