# 5328 - D2 midpoint regulator-zero normal-form gate

## Local derivation

The three events previously labelled `BRANCH_DEATH` are not admitted as
unexplained fold singularities. Across all seven regulators, each pole reaches
the fixed upper energy support with a nonzero one-sided margin slope before
the scan branch disappears. The parent root finder also rejects zero channel
derivative roots. Together with the validated simple-pole fits, the
implicit-function theorem gives a smooth regulated pole trajectory.

Writing `m(x)=E_upper-E_p(x,0)=kappa(x0-x)+...`, `kappa != 0`, the energy
primitive has local form `A log(m+i a epsilon)+regular`. Its outer integral
obeys `integral_0^L log(kappa y+i a epsilon)dy = [(kappa y+i a epsilon)
(log(kappa y+i a epsilon)-1)]_0^L/kappa`. The lower endpoint is therefore
proportional to `epsilon log epsilon`; the upper endpoint is analytic. The
complete local integral has `epsilon log epsilon`, `epsilon`, and quadratic-logarithmic
remainders. A `sqrt(epsilon)` fold term is not part of the derived family; it
is nevertheless fitted as an adversarial sensitivity diagnostic.

## Result

- reference zero intercept: `36.4288701854` `+4.08427928405 i`;
- leading-family relative bound: `0.00511710630388`;
- complete-remainder relative bound: `0.00744703818449`;
- excluded half-power diagnostic relative shift: `0.00030157397139`;
- event topology gate: `True`;
- decision: **D2_MIDPOINT_REGULATOR_ZERO_ACCEPTED__BUILD_DECAY_ANGLE_QUADRATURE**;
- validation: **PASS**.

## Claim boundary

Acceptance applies only to the fixed `D2_MID` decay-angle node. It does not
establish the decay-angle integral, full phase space, UV coefficient, local
GR, or the full MTS framework.
