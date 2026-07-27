# 2373 - Noether Source Charge Identity Or NonHilbert Residual Row

## Result

The Noether/source-charge route gives a real theorem, but not the whole prize.

The usable theorem is conditional:

`if a single observed matter action is fixed, T_H := delta S_m/delta e_obs is the active ordinary-matter source before readout, and Ward/Noether identities conserve it on shell`.

That kills post-variation source-current rescaling.  It does **not** prove that no independent gravitational source charge exists, because pre-action species weights remain conserved if they are legal, and non-Hilbert channels can still enter through spin/torsion, boundary/worldtube flux, readout reentry, or improvement/superpotential flux.

So the live source-side envelope is:

`||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement`.

The best next structural attack is no-hypermomentum / Levi-Civita source connection.  If ordinary matter/source/readout do not vary an independent connection, the spin/torsion head can collapse.  If not, the honest route is a P4 residual row.

## Noether Source-Charge Identity Attempt

| row_id | identity_piece | status | proof_or_obstruction |
| --- | --- | --- | --- |
| NSCI2373_0_target | Noether source charge identity | TARGET_SHARPENED | would derive Minimal Universal Matter Coupling rather than using it as private restriction |
| NSCI2373_1_hilbert_owner | Hilbert source owner | EXACT_CONDITIONAL_THEOREM | kills post-variation source-current rescaling only after the action/signature is fixed |
| NSCI2373_2_ward_noether | Ward/Noether conservation | EXACT_CONDITIONAL_CONSERVATION | conservation of a chosen source does not prove source uniqueness or universal normalization |
| NSCI2373_3_canonical_improvement | canonical-to-Hilbert improvement | CONDITIONAL_IMPROVEMENT_BOUND_REQUIRED | safe only if compact exterior boundary/improvement flux is zero, projected silent, or bounded |
| NSCI2373_4_pre_action_weight | pre-action species weights | COUNTERMODEL_SURVIVES_WITHOUT_MUMC | Noether conservation preserves the weighted current; it does not forbid the weight |
| NSCI2373_5_nonhilbert_channels | non-Hilbert source-current channels | OPEN_RETAIN_RESIDUAL_ROW | Hilbert/Noether identity for ordinary matter does not automatically silence all source channels |
| NSCI2373_6_projected_mass_charge | projected measured-GM charge | PROJECTED_MASS_CHARGE_NOT_CLOSED | Pi_M commutator, exchange current, boundary flux, and orbital calibration exceed unprojected Ward conservation |
| NSCI2373_7_verdict | derive no independent gravitational source charge now | NOT_DERIVED_RETAIN_NONHILBERT_ROW | conditional owner is real, but pre-action weights, non-Hilbert channels, and projected mass-charge closure remain open |

## NonHilbert Residual Row

| row_id | quantity | bound_form | status | next_input |
| --- | --- | --- | --- | --- |
| NHR2373_0_total | P_source_J_NH_abs | \|\|P_source[J_NH]\|\| <= E_spin + E_boundary + E_readout + E_improvement | CONTRACT_READY_VALUES_MISSING | zero theorem or envelope for every component in common units |
| NHR2373_1_spin_torsion | E_spin | E_spin >= \|\|P_source[J_spin/torsion/nonmetricity/hypermomentum]\|\| | MISSING_ZERO_OR_ENVELOPE | Levi-Civita/no-hypermomentum theorem or source-backed spin-current envelope |
| NHR2373_2_boundary_worldtube | E_boundary | E_boundary >= \|\|P_source[J_boundary/worldtube]\|\| | MISSING_ZERO_OR_ENVELOPE | boundary/falloff/orientation theorem or source-backed flux bound |
| NHR2373_3_readout_reentry | E_readout | E_readout >= \|\|P_source[J_readout_reentry]\|\| | MISSING_ZERO_OR_ENVELOPE | downstream/no-source-codomain proof per arena or finite residual |
| NHR2373_4_improvement_flux | E_improvement | E_improvement >= \|\|P_source[J_improvement_flux]\|\| | MISSING_ZERO_OR_ENVELOPE | improvement flux zero theorem or compact-flux envelope |
| NHR2373_5_projected_mass | Delta_M_projected | Delta_M_projected = [d,Pi_M]J_H + Pi_M J_exchange + boundary/anomaly flux | PROJECTOR_CLOSURE_MISSING | projected mass-charge closure checkpoint |

## NonHilbert Trident Update

| row_id | trident_head | status | fallback_or_effect |
| --- | --- | --- | --- |
| TRI2373_0_total | total non-Hilbert source current | NOT_ZERO_RETAIN_COMPONENTS | absolute residual envelope, no cancellation |
| TRI2373_1_spin_torsion | spin/torsion/nonmetricity/hypermomentum | SELECTED_NEXT_PRIMARY_GATE | closest GR-like structural route; retain P4 residual if not proved |
| TRI2373_2_boundary_improvement | boundary/worldtube/improvement flux | PARALLEL_GATE_OPEN | cannot silently drop exact terms if improper/edge charge survives |
| TRI2373_3_readout_reentry | readout/domain/frame reentry | PARALLEL_GATE_OPEN | requires no-source-codomain/commutator proof per arena |

## Source Charge Gate Impact

| row_id | gate | claim_status | still_missing |
| --- | --- | --- | --- |
| SCI2373_0_MUMC_branch | Minimal Universal Matter Coupling private branch | private_condition_only | Noether/source-charge derivation of the restriction |
| SCI2373_1_no_species_charge | no independent gravitational source charge | not_derived | proof that no pre-action species source coefficient is admissible |
| SCI2373_2_nonhilbert_gate | non-Hilbert/boundary/readout source currents | retained_residual | spin/torsion, boundary flux, readout reentry, improvement flux inputs |
| SCI2373_3_GM_source_charge | measured-GM projected source charge | not_closed | closed Pi_M J_H, exchange silence, boundary flux zero, Kepler calibration |
| SCI2373_4_local_GR_Newton | full local GR/Newton recovery | blocked | left-hand EH/Newton limit, PPN/readout residuals, projector/domain closure |

## Claim Gates

| row_id | gate | gate_status | claim_effect |
| --- | --- | --- | --- |
| CG2373_0_sources | source paths and needles valid | PASS | audit reproducible |
| CG2373_1_hilbert_noether_owner | Hilbert/Noether source owner exact conditionally | PASS | conditional theorem retained |
| CG2373_2_no_independent_charge | no independent gravitational source charge derived now | FAIL | pre-action weights remain countermodel outside MUMC |
| CG2373_3_nonhilbert_silence | non-Hilbert source current is zero | FAIL | trident residual gates remain |
| CG2373_4_projected_GM_charge | measured-GM charge derived from closed Hilbert projection | FAIL | projected mass charge not closed |
| CG2373_5_local_GR_Newton | local GR/Newton recovery derived | FAIL | not enough yet |
| CG2373_6_github_public_update | safe to push as public evidence | FAIL | private derivation/residual checkpoint only |

## Next Target

| row_id | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- |
| NEXT2373_0_selected | 2374-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md | prove ordinary matter/source/readout do not vary an independent connection, or that the independent connection is Palatini/EH projectively silent for the source channel | if not proved, emit first P4 torsion/nonmetricity/hypermomentum residual row as nonclaim |
| NEXT2373_1_parallel | 2374b-Y5-R2FR-boundary-improvement-flux-zero-or-envelope.md | prove compact boundary/improvement flux is zero/projected silent under the Hamiltonian reference | otherwise retain E_boundary and E_improvement finite envelopes |
| NEXT2373_2_parallel | 2374c-Y5-R2FR-readout-no-reentry-commutator-or-envelope.md | prove readout/domain/frame maps have no source-current codomain and no reentry commutator per arena | otherwise retain E_readout finite envelope |
| NEXT2373_3_parallel | 2374d-Y5-R2FR-Hilbert-Noether-mass-projector-closure.md | close d(Pi_M J_H)=0 and GM calibration rather than relying on unprojected Ward conservation | otherwise retain Delta_M_projected residual |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NONHILBERT_RESIDUAL_ROW.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NONHILBERT_TRIDENT_UPDATE.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_SOURCE_CHARGE_GATE_IMPACT.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2373_VALIDATION.csv`

## Practical Status

This is a controlled failure in the good sense.  We did not prove the source-charge identity strongly enough to derive Minimal Universal Matter Coupling, but we did stop the leak from being vague.  The source side now has a named residual envelope and a first structural gate: no-hypermomentum / Levi-Civita source connection.
