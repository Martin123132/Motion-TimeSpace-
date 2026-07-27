# 4020 - Local GR Conditional Rollup Or First Executable PPN Score

- Timestamp: `2026-07-01T21:45:12+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The local-GR branch has now moved from scattered gates into one clean adoption-or-score fork:

1. **Adoption route:** if the parent action explicitly adopts the 4017 `K_G` packet, the 4019 EH-only/R11 no-extra local action, the 4012/4015 source-charge map, the 4013/4014 EM once-only owner, and the q_loc PPN-projector kernel, then the local branch conditionally gives the GR PPN vector:

`gamma=1`, `beta=1`, `alpha_i=xi=zeta_i=0`, and `Gdot/G=0`.

2. **Score route:** if any adoption clause fails, the branch falls into the absolute PPN residual score:

`Delta_PPN_abs_4020 = |delta_gamma_R11|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|alpha_i|+|xi|+|zeta_i|+|Gdot/G|`.

No cancellation credit is allowed.

## Current State

- Current evaluator result: `CURRENT_STATE_NOT_SCOREABLE_NONCLAIM`.
- PPN result: `local-GR branch is coherent as a conditional route, but no public PPN pass exists`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4020`.
- Source needles found: `20/20`.

## What This Actually Means

This is progress, not victory. The chain is no longer "maybe local closure saves us"; it is now:

`parent adoption witness OR executable PPN residual score`.

The best next move is the derivation-first route: try to write the parent-owned local action witness that makes the EH-only/R11/no-extra and source-current clauses real. If that witness cannot be written without cheating, fill the first PPN coefficient rows instead.

## Missing Before Any Public Claim

- Final parent action must adopt `K_G` as a global branch sector.
- Final parent action must adopt EH-only plus matter/EM/exact/topological local operators through 2PN.
- `Pi_M/H_tau` source equality must be parent-owned before orbital readout.
- `B_source=A_source^2` must be derived or scored.
- `q_loc/Khat` must be killed by PPN projectors or bounded numerically.
- Preferred-frame/conservation terms must be theorem-zero or score-backed.

## Next Target

- `4021-Y5-R2FR-parent-adoption-witness-or-first-PPN-score-input-fill.md`
- `scripts/Y5_R2FR_4021_parent_adoption_witness_or_first_PPN_score_input_fill.py`
