# 4158 - Boundary Reference Data Lock Or Kernel Amplitude Bound

Timestamp UTC: `2026-07-02T11:39:11+00:00`  
Branch: `MTS_R2FR_Y5_BOUNDARY_REFERENCE_AHOM_LOCK_4158`  
Decision: `BOUNDARY_REFERENCE_AHOM_LOCK_DERIVED_CONDITIONALLY_PACKET_UNSIGNED_KERNEL_BOUND_ROWS_READY`

## Purpose
4157 identified the exact obstruction:

`h_0=a_hom/r`

with

`epsilon_kernel=|a_hom|/(G_ref M_H_ref)`.

4158 asks whether fixed boundary/reference data kill `a_hom`, or whether the monopole must remain as a strict bound row.

## Annulus Calculation
Work on the compact local exterior annulus:

`Omega_ext={R_in<r<R_out}`.

For the `l=0` source-free difference:

`h_0(r)=A+a_hom/r`.

Two boundary values give:

`a_hom=(h_in-h_out)/(1/R_in-1/R_out)`.

Therefore, if the parent fixes both source-free representative values before readout,

`h_in=0` and `h_out=0 => a_hom=0`.

There is a second, more physical route. The monopole flux is:

`Phi_h(S)=int_S grad h . dS=-4*pi*a_hom`.

So an outer/reference branch plus source-free inner charge matching gives:

`Phi_h(S_in)=0 => a_hom=0`.

Equivalently, in Hamiltonian-charge language:

`delta H_tau[h]=-(1/G_ref)a_hom+B_hidden[h]`.

If `delta H_tau[h]=0` and `B_hidden[h]=0`, then `a_hom=0`.

## What The Existing Corpus Supplies
The earlier boundary rows are useful but not yet sufficient for a live claim:

- 4038/4061 supply a selected source-blind reference branch: `D_source H_ref=D_readout H_ref=0`.
- 4038/4155 supply local stationary Poynting/bound-EM no-extra-flux accounting.
- 4043 supplies a fixed domain/projector selected branch.
- 4054 supplies a no-flux energy-identity template.
- 4056 assembles these as a candidate local parent packet.

But the current corpus has not yet formally adopted that packet as the parent MTS branch, and it has not yet proved the gravitational source-free inner charge condition for `h`.

So 4158 derives the lock contract, but does not claim the lock is live.

## Conditional Lock Theorem
The exact contract is:

`Z_outer_ref * Z_inner_charge * Z_Href * Z_no_hidden * Z_no_incoming * Z_no_backfill => a_hom=0`.

Where:

- `Z_outer_ref`: outer/reference value is fixed before source/readout variation;
- `Z_inner_charge`: `delta Phi_h(S_in)=0` or `delta H_tau[h]=0` for source-free `h`;
- `Z_Href`: reference subtraction is source-blind and q-basic;
- `Z_no_hidden`: no boundary/domain/EM/symplectic hidden mass charge;
- `Z_no_incoming`: no externally supplied free monopole branch;
- `Z_no_backfill`: no orbital `GM` is used to define `M_H_ref`.

## Bound Fallback
If the lock is unsigned, retain route-specific bounds:

`epsilon_kernel <= (|delta h_in|+|delta h_out|)/(G_ref*M_H_ref*|1/R_in-1/R_out|)`,

or

`epsilon_kernel <= |delta Phi_h(S_in)|/(4*pi*G_ref*M_H_ref)`,

or

`epsilon_kernel <= |delta H_tau[h]-delta H_ref[h]|/M_H_ref + epsilon_hidden_boundary`.

The strict total fallback is:

`epsilon_kernel <= route_bound(delta h or delta Phi_h or delta H_tau) + epsilon_hidden_boundary + epsilon_incoming_mass + epsilon_readout_backfill_guard`.

No cancellation credit is allowed.

## Verdict
This is progress: `a_hom` is now controlled by a concrete boundary/charge equation. The problem is no longer "find a coupling." It is:

1. prove the inner source-free Gauss/Hamiltonian charge is zero on the same-source branch; or
2. source a numerical/observational bound for that charge mismatch.

Newton/local GR are still not claimed.

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_AHOM_AMPLITUDE_BOUND_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_NEWTON_IMPACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4158_NEXT_TARGET.csv`

## Next Target
- `4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md`
- Prove `delta Phi_h(S_in)=0` / `delta H_tau[h]=0` for a source-free homogeneous difference under same `J_H_total`, or populate the first source-backed `epsilon_kernel` bound.
