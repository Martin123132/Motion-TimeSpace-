# 4035 - Source Only Vertex Exclusion Or cT cEM Fill

- Timestamp: `2026-07-01T23:09:13+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4035 attacks the first two source-leak coefficients:

`c_T` from `Z*T_H` or `gamma*T_H`, and `c_EM` from `Z*F_EM^2` or `gamma*F_EM^2`.

The clean theorem route is a typed parent normal form:

`S_total=S_EH[g_obs]+I_Gamma[g_obs,Z,R_even,D]+S_matter[psi,Qvis,theta]+S_EM[A,Qvis,J]+S_binding+dB`.

If matter and EM are functors only of `Qvis`, and if there is no parent morphism from hidden/source slots into matter or EM action scalars, then source-only vertices are forbidden.

## Guardrail

Exchange parity alone is not enough. Ordinary matter trace can be exchange-even. The proof needs typed-domain/source-slot exclusion, not just "odd things vanish".

## If The Theorem Fails

The first coefficient rows are:

- `Q_phi_T=(2/3)c_T int_W T_H dV`;
- `Q_phi_EM=(2/3)c_EM int_W F_EM^2 dV`.

Those feed `alpha_phi(lambda)` and source-WEP rows before any R10/local-GR claim.

## Current Verdict

- Current evaluator result: `VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4035`.
- Source needles found: `8/8`.

## Next Target

- `4036-Y5-R2FR-no-Hom-source-slot-theorem-or-cT-cEM-units.md`
- `scripts/Y5_R2FR_4036_no_Hom_source_slot_theorem_or_cT_cEM_units.py`
