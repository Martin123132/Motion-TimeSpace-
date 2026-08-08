# 4157 - Constraint Green Kernel Zero Or Homogeneous Mass Residual

Timestamp UTC: `2026-07-02T11:31:58+00:00`  
Branch: `MTS_R2FR_Y5_CONSTRAINT_GREEN_KERNEL_ZERO_4157`  
Decision: `CONSTRAINT_GREEN_KERNEL_ZERO_THEOREM_DERIVED_CONDITIONALLY_HOMOGENEOUS_MASS_RESIDUAL_RETAINED`

## Purpose
4156 narrowed the source-normalization problem to one sharp question:

Can the parent exterior constraint Green map contain a homogeneous unsourced `1/r` mass mode independent of `J_H_total`?

If no, the Newton source-glue branch moves forward. If yes or unsigned, the mode must be retained as `R_kernel`; it cannot be hidden inside fitted `GM`.

## Actual Derivation
Let `u_ext` denote the exterior Newton/EH weak-field charge/readout variable controlled by the parent constraint map. For fixed parent operator, gauge, frame, units, source domain and source current,

`L_ext u_ext = S[J_H_total]`.

If two candidate exterior solutions have the same `J_H_total`, their difference `h` obeys:

`L_ext h = 0`.

So the exact Green split is:

`u_ext = G_ext S[J_H_total] + h`.

In the stationary local weak-field exterior, the source-free scalar part has the harmonic form:

`h=C_0+a_hom/r+sum_{l>=1,m} C_lm r^{-(l+1)}Y_lm(theta,phi)`.

`C_0` is a reference/gauge constant. The higher multipoles are shape hair. The dangerous Newton-source term is:

`h_0=a_hom/r`.

The Gauss-flux amplitude law is:

`M_kernel = -(1/G_ref) a_hom = (1/(4*pi*G_ref)) int_S grad h . dS`,

so

`epsilon_kernel=|R_kernel|/M_H_ref=|a_hom|/(G_ref M_H_ref)`.

That is the precise residual, not a vague missing coupling.

## Conditional Zero Theorem
`R_kernel=0` follows if the parent supplies either of the following before orbital readout:

1. **Strong Dirichlet/energy route:** `L_ext h=0` on the fixed exterior annulus with `h|S_in=0` and `h|S_out=0`, giving `h=0` by uniqueness/maximum principle/energy identity.
2. **Charge-flux route:** `delta H_tau[h]=0` for every source-free homogeneous branch, with no hidden boundary/range/domain/EM/symplectic charge, giving `a_hom=0` by Gauss flux.

The guardrail is important:

`h -> 0` as `r -> infinity` does **not** prove `a_hom=0`, because `a_hom/r -> 0`.

So plain asymptotic flatness is not enough. The theory needs a fixed boundary/reference/charge package that kills the monopole.

## Current Verdict
The derivation succeeds conditionally, but not as a live MTS claim yet.

| Item | Status | Meaning |
|---|---|---|
| Green split `u=G_ext S+h` | DERIVED CONDITIONAL | requires fixed parent operator/domain |
| homogeneous `1/r` mode | IDENTIFIED | exact source-normalization obstruction |
| amplitude law | DERIVED CONDITIONAL | `epsilon_kernel=|a_hom|/(G_ref M_H_ref)` |
| asymptotic-flatness shortcut | BLOCKED | decay alone still allows `a_hom/r` |
| parent boundary/reference zero | UNSIGNED | next target |
| Newton/local GR claim | NOT CLAIMED | `R_kernel` retained |

## Residual Law
Until the boundary/reference lock is parent-signed, retain:

`epsilon_kernel <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_source_charge_mismatch + epsilon_hidden_boundary_charge + epsilon_surface_flux + epsilon_domain_gauge`.

No cancellation credit is allowed unless a parent identity proves the cancellation.

## What This Moves
This does move the framework forward: the kernel problem is no longer "something missing in the coupling." It is the exact question of whether the parent action fixes or forbids the source-free monopole coefficient `a_hom` before readout.

If `a_hom=0`, the same Hilbert/Hamiltonian source can control the Newtonian `1/r` term. If `a_hom` is nonzero or unbounded, local GR remains blocked at first order.

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_GREEN_UNIQUENESS_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_NEWTON_IMPACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4157_NEXT_TARGET.csv`

## Next Target
- `4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md`
- Prove the fixed parent boundary/reference data force `a_hom=0`, or produce the first strict `epsilon_kernel` bound row.
