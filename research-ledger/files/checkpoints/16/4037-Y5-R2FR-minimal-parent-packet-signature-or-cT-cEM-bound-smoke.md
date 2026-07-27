# 4037 - Minimal Parent Packet Signature Or cT cEM Bound Smoke

- Timestamp: `2026-07-01T23:18:59+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `10/10`.

## What Actually Moved

4037 takes the 4036 fork and chooses the clean local branch:

`S_local = S_EH[g_obs] + S_kappa_top + I_Gamma[g_obs,Z,R_even,D] + S_matter[psi,Qvis,theta,A_obs] + S_EM[A,Qvis,J] + S_selector + S_boundary`,

with readouts only after variation.

This is signed as the internal local-branch action-language contract, not as a public full-theory/local-GR claim.

## Direct Coupling Result

Inside this selected packet:

- `c_T_direct=0` for `Z*T_H`, `gamma*T_H`, `q_private*T_A`, and `w_A(Z)S_A`;
- `c_EM_direct=0` for `Z*F_EM^2`, `gamma*F_EM^2`, and `f(Z)F_EM^2`;
- `C_XF2_direct=0` for hidden scalar/response multipliers of `F^2` or `F*F`.

This is no longer a vague missing coupling. It is a branch theorem: if the packet is used, the direct source-only couplings are absent; if the packet is rejected, the finite-bound branch is mandatory.

## Fallback Bound Smoke

If hidden conformal matter or hidden Maxwell multipliers are reintroduced:

`alpha_X=(2/3)*C_alpha_phi*c_X*(I_X/M_H)*(q_test/m_test)`.

So

`|c_X| <= (3/2)*alpha_bound/|C_alpha_phi*(I_X/M_H)*(q_test/m_test)|`.

The fallback is schema/unit-ready but numeric-claim blocked until `alpha_bound`, `C_alpha_phi`, profile integrals, test charge ratios, and EM normalization are real.

## Remaining Local-GR Leak Vector

The next problem is not direct `c_T/c_EM`. The remaining vector is:

- `c_Poynting`: net EM/radiative/background flux through the local collar;
- `c_B`: boundary/corner/reference leakage;
- `c_Z`: hidden/domain/memory current;
- `c_norm`: universal source/action normalization drift;
- `c_nonEH`: non-EH or higher-curvature metric operator leakage.

## Current Verdict

- Current evaluator result: `MINIMAL_SOURCE_CLEAN_LOCAL_PACKET_SIGNED_INTERNALLY`.
- Direct result: `c_T_direct=c_EM_direct=C_XF2_direct=0` inside the selected packet.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4037`.

## Next Target

- `4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md`
- `scripts/Y5_R2FR_4038_Poynting_no_flux_and_boundary_reference_theorem_or_flux_bound.py`
