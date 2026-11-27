import Main
#check @riemannHypothesis
#check @riemannZeta_eq_zero_re
#check @LFunction_ne_zero_of_half_lt_re
#check @LFunction_eq_zero_re
#check @LFunction_eq_zero_re_of_isPrimitive
#print RiemannHypothesis
#eval show Lean.MetaM Unit from do
  let env ← Lean.getEnv
  for n in [`RiemannHypothesis, `RiemannZetaZerosOnLine, `DirichletLNonvanishingRightOfHalf, `DirichletLZerosOnLine, `PrimitiveDirichletLZerosOnLine] do
    IO.println s!"{n} : {(env.getModuleIdxFor? n).map (fun i => env.header.moduleNames[i.toNat]!)}"
