# 5268 - Soft-energy endpoint completion

## Question

Checkpoint 5267 accepted the topology-aware fixed-angle energy integral only on
`1.0e-04 <= x <= 0.9999`. This checkpoint tests and restores
the omitted `x -> 0` and `x -> 1` tails without changing the angular variables.

## Topology bridge

The endpoint branch is not re-solved by an unstable winding calculation at
`x=0`. Instead, each of the six components in both regulators is anchored to
the accepted checkpoint-5267 winding state at `x=1.0e-04` or
`x=0.9999`. The relevant analytic surfaces are scanned down to
endpoint distance `1.0e-06`. The remaining approach to the
endpoint uses the exact soft-endpoint and finite pole-coalescence results in
checkpoints 5019 and 5029.

This is a boundary-anchored numerical continuation. It is not an interval proof
of every winding state below the numerical floor.

## Invariant endpoint law

Checkpoint 5010 defines

`H(x) = [g(x)-g(0)]/x`.

For differentiable `g`,

`H(x) = g'(0) + g''(0)x/2 + O(x^2)`.

The separately labelled residue components become ill-conditioned when
reciprocal pole pairs coalesce, while their physical sum remains finite.
Therefore only the invariant regulator combination `2 E020 - E040`, with the
inherited kernel and A00 factor, is extrapolated below the numerical floor.

## Numerical result

The checkpoint-5267 interior value was

`I_interior = -36.8618887518162 -12.5530499811092 i`.

The completed two-tail correction is

`Delta I_endpoint = -0.246572365134427 -0.976820669832234 i`,

giving

`I_completed = -37.1084611169506 -13.5298706509414 i`.

The correction is `0.0255065924146` of the completed magnitude.
Across numerical floors `1.0e-07, 3.0e-07, 1.0e-06`,
the order-512 result changes by relative fraction
`4.45322322607e-07`. The corrected order-32 and
order-128 relative errors are `0.00213465878764`
and `3.3044856168e-06`.

## Unresolved sub-floor cap

Endpoint finiteness is derived, but the finite-resolution magnitude cap is
conditional rather than an interval proof. The recorded cap assumes no
sub-floor spike exceeds `10` times the largest
measured or fitted endpoint scale. Under that explicit assumption,

`|Delta I_unresolved| <= 0.012703089006`,

or `0.000321613135928` of the completed
fixed-angle magnitude.

## Decision

`ACCEPT_FIXED_ANGLE_SOFT_ENERGY_ENDPOINT_COMPLETION__PROCEED_TO_ANGULAR_TOPOLOGY`

Validation passed: `true`.

This accepts a conditional, numerically stable fixed-angle energy rule with both
endpoint tails restored. It does not accept the two angular integrations, the
full phase-space coefficient, a numeric UV fixed point, local GR, or full MTS.

## Next derivation

Restore the two angular integrations while preserving the component topology,
the energy-pole subtraction, and this endpoint rule. The angular Jacobian is
`1/4`; angular chamber transitions and angular endpoint caps must be resolved
before interpreting any coefficient.

## Artifacts

- Runner: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5268_soft_energy_endpoint_completion.py`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5268\soft_energy_endpoint_completion_result.json`
- Convergence: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5268\soft_energy_endpoint_completion_convergence.csv`
- Physical endpoint samples: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5268\soft_energy_endpoint_physical_samples.csv`
- E040 worker: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5268\workers\E040\endpoint_worker_result.json`
- E020 worker: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5268\workers\E020\endpoint_worker_result.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5268\soft_energy_endpoint_completion_validation.csv`
