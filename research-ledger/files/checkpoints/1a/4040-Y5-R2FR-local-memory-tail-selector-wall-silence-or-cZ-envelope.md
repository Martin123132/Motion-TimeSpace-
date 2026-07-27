# 4040 - Local Memory Tail Selector Wall Silence Or cZ Envelope

- Timestamp: `2026-07-01T23:32:04+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `8/8`.

## What Actually Moved

4040 tries the exact zero route for the last `c_Z` pieces and refuses to smuggle it.

The zero theorem would need:

- `P_loc K_mem=0` or disjoint support on the compact stationary collar;
- or a real gap/range bound `||J_Z^tail||_1 <= C_mem exp(-L_collar/ell_mem)||H||_1`;
- a fixed/exact/topological selector with no wall motion or shell mismatch.

The current corpus does not prove those inputs.

## Result

So the full `c_Z=0` claim is not made. Instead the remaining hidden-current effect is an absolute envelope:

`A_Z_remaining <= A_tail + A_wall`.

with

- `A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1`;
- `A_wall <= C_G(D_Z,M_Z,L_collar)*|c_Z|*(||jump(D_Z n.grad Z)||_Sigma + ||delta S_wall/delta Z||_Sigma)`.

No cancellation credit is allowed.

## Guardrail

Local memory silence is not global memory silence. The FLRW/cosmology memory branch remains alive.

## Current Verdict

- Current evaluator result: `TAIL_WALL_SILENCE_NOT_PROVED_CZ_ENVELOPE_ACTIVE`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4040`.
- Remaining live local residuals: `Delta_cZ_envelope`, `c_norm`, `c_nonEH`.

## Next Target

- `4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md`
- `scripts/Y5_R2FR_4041_cnorm_common_mode_into_kappa_obs_or_Gdot_bound.py`
