# 4045 - cZ Kernel/Wall Zero Theorem Or First Bound Values

- Timestamp: `2026-07-02T00:01:07+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `12/12`.

## What Actually Moved

4045 uses the 4043 projector/domain result to reduce the 4040 `c_Z` envelope.

Before: `A_Z_remaining <= A_tail + A_wall`.

After, in the selected private branch: `A_wall_projector=0`, so `Delta_cZ_selected = A_tail`.

This is not full `c_Z=0`. It is a real narrowing: the selected branch no longer carries the projector/domain selector-wall term; the remaining live piece is the memory/history kernel tail.

## Remaining Tail Formula

`A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1`.

To finish this route we need either `P_loc K_mem=0` / disjoint support on the compact collar, or real values/bounds for `C_G`, `c_Z`, `C_mem`, `ell_mem`, `L_collar`, and `||H||_1`.

## Current Verdict

- Current evaluator result: `CZ_REDUCED_TO_TAIL_ONLY_NOT_ZERO`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4045`.
- Remaining live local residuals: `Delta_cZ_tail`, `Delta_cnorm_envelope`, `Parent_packet_adoption`.

## Next Target

- `4046-Y5-R2FR-memory-tail-support-gap-zero-theorem-or-tail-bound-inputs.md`
- `scripts/Y5_R2FR_4046_memory_tail_support_gap_zero_theorem_or_tail_bound_inputs.py`
