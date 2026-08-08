# 5319 - Regulator-zero asymptotic normal-form gate

## Derivation

Checkpoint 5315 established a transverse support crossing with `kappa != 0`
and outer primitive `A log|x-x_event| + regular`.  With the regulator,
the local complex normal form is `log(kappa y + i epsilon)`.  Its one-sided
integral admits `epsilon log epsilon`, `epsilon`, and quadratic-logarithmic
remainders.  It does not admit a `sqrt(epsilon)` term: the squared coordinate
used in 5315 regularizes a logarithm and is not a half-power physical branch.

The five complex finite-regulator values are fitted with the full enumerated
normal-form family.  Input uncertainties are conservative complex disks, not
statistical standard deviations.  The intercept error uses the exact linear
influence map `sum_i |h_i| delta_i`, plus family, leave-one-out, small-window,
weighting-choice, and pairwise Richardson stability envelopes.

## Result

- reference zero intercept: `104.555917237` `-19.9020855474 i`;
- leading-family relative bound: `0.00402129182323`;
- complete-remainder relative bound: `0.010649390821`;
- acceptance limit: `0.01`;
- fixed-decay zero limit accepted: `False`;
- decision: **LEADING_ZERO_LIMIT_STABLE__ADD_E00125_TO_CLOSE_REMAINDER_ENVELOPE**;
- validation: **PASS**.

## Claim boundary

This checkpoint cannot establish decay-angle integration, the full phase-space
coefficient, a UV prediction, local GR, or the full MTS theory.  If the complete
remainder envelope misses the inherited one-percent gate, the next action is an
actual smaller-regulator computation, not deletion of the remainder family.
