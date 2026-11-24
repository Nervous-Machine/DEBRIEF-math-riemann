import Lean
open Lean
-- Compare two compiled modules (.olean) of the same source: the one the community's cache supplied and the one
-- recompiled here from the pinned source. Prints the constant counts, the names present in only one of them, and the
-- number of constants whose set of used constants differs. usage: lake env lean --run SpotCheck.lean A.olean B.olean
def usedConsts (ci : ConstantInfo) : Array Name :=
  let a := ci.type.getUsedConstants
  match ci.value? (allowOpaque := true) with
  | some v => a ++ v.getUsedConstants
  | none => match ci with
    | .inductInfo val => a ++ val.ctors.toArray
    | .ctorInfo val => a.push val.induct
    | .recInfo val => a ++ val.all.toArray
    | _ => a
def sortedNames (a : Array Name) : Array Name := (a.qsort (fun x y => Name.quickLt x y)).toList.eraseDups.toArray
def main (args : List String) : IO Unit := do
  let (da, _) ← readModuleData ⟨args[0]!⟩
  let (db, _) ← readModuleData ⟨args[1]!⟩
  let mut mb : Std.HashMap Name ConstantInfo := {}
  for c in db.constants do mb := mb.insert c.name c
  let mut ma : Std.HashMap Name ConstantInfo := {}
  for c in da.constants do ma := ma.insert c.name c
  let mut onlyA := 0; let mut onlyB := 0; let mut edgeDiff := 0
  for c in da.constants do
    match mb.get? c.name with
    | none => onlyA := onlyA + 1
    | some c' => if sortedNames (usedConsts c) != sortedNames (usedConsts c') then edgeDiff := edgeDiff + 1
  for c in db.constants do
    if !(ma.contains c.name) then onlyB := onlyB + 1
  IO.println s!"constants_a {da.constants.size} constants_b {db.constants.size} only_a {onlyA} only_b {onlyB} edge_diff {edgeDiff}"
