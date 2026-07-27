# 4034 - No Linear Source Leak Proof Or Qphi Coefficient Fill

- Timestamp: `2026-07-01T23:01:53+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4034 decomposes the leak term:

`F_source_leak=c_T*T_H + c_EM*F_EM^2 + c_Poynting*divS_EM + c_B*B_boundary + c_Z*J_Z + c_norm*Delta_source_norm + c_nonEH*O_nonEH`.

The proof route is now explicit:

1. ordinary matter and EM enter only `S_matter+S_EM+S_binding`;
2. `Gamma_eff-Gamma_0` is exchange-even/quadratic in local residuals;
3. source-only vertices such as `Z*T_H` and `Z*F_EM^2` are forbidden by the parent object language;
4. ordinary EM stress is counted once in the total Hilbert source;
5. radiative/background Poynting flux and boundary odd charge are either zero or scored.

If all clauses are signed, `F_source_leak=0`.

## Current Obstruction

The dangerous terms are now concrete:

`c_T`, `c_EM`, `c_Poynting`, `c_B`, `c_Z`, and `c_norm`.

The largest immediate proof target is source-only vertex exclusion. Matter trace can be exchange-even, so exchange parity alone is not enough.

## Current Verdict

- Current evaluator result: `NO_LINEAR_SOURCE_LEAK_CONDITIONAL_QPHI_COEFFICIENTS_RETAINED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4034`.
- Source needles found: `8/8`.

## Next Target

- `4035-Y5-R2FR-source-only-vertex-exclusion-or-cT-cEM-fill.md`
- `scripts/Y5_R2FR_4035_source_only_vertex_exclusion_or_cT_cEM_fill.py`
