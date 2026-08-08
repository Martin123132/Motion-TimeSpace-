# 3564 - Non-Hilbert source bypass improvement zero or bound

## Verdict
3564 closes only the clean subpiece: exact `dmu` improvements are conditionally silent in the Hamiltonian surface one-form when `tau`, the surface and corner class are fixed. But total non-Hilbert source bypass is not zeroed.

So `nonHilbert_source_bypass` is now an official nonclaim fallback vector: spin/torsion, boundary/worldtube, readout reentry, shadow/projector/support and decoupled blocks are absolute-summed until individually zeroed or bounded.

## Exact improvement lemma
`L' = L + dmu` gives `theta' = theta + delta mu` and `Q_tau' = Q_tau + i_tau mu`; therefore `k_tau' = delta Q_tau' - i_tau theta' = k_tau` when `[delta,i_tau]=0` and no corner/topological/readout residue exists.

This is useful but narrow. It does not silence spin/torsion, boundary/worldtube charges, readout reentry or projector/support tails.

## What moved
- Exact improvements are separated from unclassified boundary/current flux.
- Total `J_NH` is decomposed into named component gates.
- The non-Hilbert bypass vector is promoted to official nonclaim fallback.
- Next target is the closest GR-like structural gate: spin/torsion/hypermomentum silence.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_SOURCE_REGISTER.csv`
- `bypass_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv`
- `component_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_COMPONENT_GATES.csv`
- `official_fallback`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_OFFICIAL_NONHILBERT_FALLBACK_ROWS.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3564_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_nonHilbert_bypass_official_fallback_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3564_VALIDATION.csv`

## Theorem rows
- `NHB3564_0_decomposition`: After the Hilbert source is extracted, write J_active = J_H + J_NH with J_NH = J_spin/torsion + J_boundary/worldtube + J_readout + J_improvement + J_shadow/projector + J_decoupled.
- `NHB3564_1_exact_improvement_cancellation`: If a non-Hilbert contribution is a genuine exact improvement L' = L + dmu on the same field bundle, with fixed tau, fixed surface embedding, no corner/topological remainder and no readout dependence, then its Hamiltonian surface one-form contribution cancels: delta(i_tau mu)-i_tau(delta mu)=0.
- `NHB3564_2_total_zero_conditions`: P_source[J_NH]=0 follows only if spin/torsion is absent/projected-silent, boundary/worldtube/improvement flux has zero compact local projection, readout/domain/frame reentry is forbidden, shadow/projector/support tails are zero, and decoupled conserved blocks are excluded or bounded.
- `NHB3564_3_live_failure`: Current MTS does not sign total non-Hilbert silence: spin/torsion/nonmetricity, boundary/worldtube flux, readout reentry, shadow/projector support and nonminimal/decoupled blocks remain open or unsigned.
- `NHB3564_4_official_fallback`: Because total P_source[J_NH]=0 is not signed, epsilon_current_owner_NH_abs is now the official nonclaim fallback for the density/source-current branch, using absolute component envelopes and no cancellation.
- `NHB3564_5_next_gate`: The best next derivation target is spin/torsion/nonmetricity/hypermomentum silence, because it is the closest GR-like structural route: metric-only Levi-Civita source geometry or Palatini EH plus no hypermomentum.

## Component gates
- `NHC3564_0_spin_torsion` `E_spin`: LIVE_UNSIGNED (spin/torsion/nonmetricity/hypermomentum source projection)
- `NHC3564_1_boundary_worldtube` `E_boundary`: LIVE_UNSIGNED (boundary/worldtube/source-current projection)
- `NHC3564_2_improvement_flux` `E_improvement`: PARTIAL_EXACT_ZERO_FOR_CLASSIFIED_DMU_ONLY (canonical/Hilbert improvement or superpotential flux)
- `NHC3564_3_readout_reentry` `E_readout`: LIVE_UNSIGNED (post-variation readout/domain/frame current reentry)
- `NHC3564_4_shadow_projector` `E_shadow_projector`: LIVE_UNSIGNED (shadow connection/projector/domain/support tail)
- `NHC3564_5_decoupled_block` `E_decoupled`: LIVE_INVENTORY (separately conserved non-Hilbert source block)
- `NHC3564_6_total` `epsilon_current_owner_NH_abs`: OFFICIAL_NONCLAIM_FALLBACK (absolute non-Hilbert source-current owner envelope)

## Official fallback rows
- `FNH3564_0_total` `epsilon_current_owner_NH_abs`: OFFICIAL_NONCLAIM_TOTAL_ENVELOPE
- `FNH3564_1_spin` `E_spin`: MISSING_NO_GAMMA_CERTIFICATE_OR_P4_VALUE
- `FNH3564_2_boundary` `E_boundary`: MISSING_B_ZERO_FLUX_OR_SOURCE_BOUND
- `FNH3564_3_improvement` `E_improvement`: PARTIAL_EXACT_DMU_ZERO_ELSE_BOUND_REQUIRED
- `FNH3564_4_readout` `E_readout`: MISSING_READOUT_REENTRY_ZERO_OR_LEAKAGE_VALUE
- `FNH3564_5_shadow_projector` `E_shadow_projector`: MISSING_SHADOW_PROJECTOR_SUPPORT_VALUE
- `FNH3564_6_decoupled` `E_decoupled`: MISSING_ARENA_EXCLUSION_OR_BOUND
- `FNH3564_7_no_cancellation` `sum_abs_components`: ACTIVE_GUARD

## Decision ledger
- `DEC3564_0`: Exact improvement cancellation is a partial theorem. Classified exact dmu improvements cancel from the Hamiltonian surface one-form under fixed tau/surface/no-corner clauses.
- `DEC3564_1`: Total non-Hilbert bypass is not zeroed. Spin/torsion, boundary/worldtube, readout reentry, shadow/projector and decoupled blocks remain live.
- `DEC3564_2`: Official non-Hilbert fallback selected. Future local-GR source-current work uses the absolute non-Hilbert envelope unless a component theorem closes.
- `DEC3564_3`: Next target is spin/torsion silence. The closest GR-like route is proving the local source branch is metric-only Levi-Civita or Palatini EH with no hypermomentum.

## Next target
- `3565-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md`
- Objective: try to prove the local source branch is metric-only Levi-Civita, or Palatini EH with no matter/source/readout hypermomentum and projective silence; if not, promote E_spin/P4 torsion-nonmetricity bound rows
