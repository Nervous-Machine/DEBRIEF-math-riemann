import Main
open Lean in
-- R6: every constant whose name ends in RiemannHypothesis, with its module of origin
#eval show CoreM Unit from do
  let env ← getEnv
  let mut hits : Array (Name × Option Name) := #[]
  for (n, _) in env.constants.toList do
    if n.toString.endsWith "RiemannHypothesis" then
      hits := hits.push (n, env.getModuleFor? n)
  IO.println s!"constants ending in RiemannHypothesis: {hits.size}"
  for (n, m) in hits.qsort (fun a b => a.1.toString < b.1.toString) do
    IO.println s!"  {n} : module {m}"
  IO.println s!"modules imported: {env.header.moduleNames.size}; constants: {env.constants.size}"
#print RiemannHypothesis
#check @riemannHypothesis
#check @riemannZeta_eq_zero_re
#check @LFunction_ne_zero_of_half_lt_re
#check @LFunction_eq_zero_re
#check @LFunction_eq_zero_re_of_isPrimitive
-- R5
#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive
