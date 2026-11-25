import Lean
open Lean
def usedConsts (ci : ConstantInfo) : Array Name :=
  let a := ci.type.getUsedConstants
  match ci.value? (allowOpaque := true) with
  | some v => a ++ v.getUsedConstants
  | none => a
def main (args : List String) : IO Unit := do
  let (da, _) ← readModuleData ⟨args[0]!⟩
  let (db, _) ← readModuleData ⟨args[1]!⟩
  let na := da.constants.map (·.name); let nb := db.constants.map (·.name)
  for c in da.constants do if !(nb.contains c.name) then IO.println s!"only_cached {c.name}"
  for c in db.constants do if !(na.contains c.name) then IO.println s!"only_recompiled {c.name}"
  for c in da.constants do
    match db.constants.find? (·.name == c.name) with
    | some c' => if (usedConsts c).qsort Name.quickLt != (usedConsts c').qsort Name.quickLt then IO.println s!"edge_diff {c.name}"
    | none => pure ()
