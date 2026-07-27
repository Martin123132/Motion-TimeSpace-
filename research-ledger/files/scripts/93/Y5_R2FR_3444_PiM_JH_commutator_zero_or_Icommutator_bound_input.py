from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3444-Y5-R2FR-PiM-JH-commutator-zero-or-Icommutator-bound-input-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3443": ROOT / "3443-Y5-R2FR-source-normalization-Csrc-zero-or-measured-GM-bound-input-under-AX1090.md",
    "next_3443": OUT / "P8_Y5_R2FR_3443_NEXT_TARGET.csv",
    "csrc_decomposition_3443": OUT / "P8_Y5_R2FR_3443_CSRC_DECOMPOSITION.csv",
    "flux_link_3443": OUT / "P8_Y5_R2FR_3443_FLUX_OBSTRUCTION_LINK.csv",
    "doc_1013": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "obstruction_1013": OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "flux_attempt_1013": OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv",
    "doc_1014": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "commutator_1014": OUT / "P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "coefficient_1014": OUT / "P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv",
    "claim_gate_1014": OUT / "P8_Y5_R10_1014_CLAIM_GATE.csv",
    "doc_1152": ROOT / "1152-Y5-R10-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
    "audit_1152": OUT / "P8_Y5_R10_1152_COMMUTATOR_ZERO_THEOREM_AUDIT.csv",
    "acquisition_1152": OUT / "P8_Y5_R10_1152_R_EQ_I_COMMUTATOR_SOURCE_ACQUISITION_ROWS.csv",
    "guards_1152": OUT / "P8_Y5_R10_1152_PROJECTOR_ROUTE_GUARDS.csv",
    "doc_2585": ROOT / "2585-Y5-R2FR-PiM-chainmap-commutator-zero-or-Icommutator-bound-fill.md",
    "audit_2585": OUT / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv",
    "bound_rows_2585": OUT / "P8_Y5_PIM_CHAINMAP_2585_ICOMMUTATOR_BOUND_ROWS.csv",
    "doc_3373": ROOT / "3373-Y5-R2FR-PiM-commutator-chainmap-zero-or-Icommutator-bound-under-AX1090.md",
    "theorem_3373": OUT / "P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "route_3373": OUT / "P8_Y5_R2FR_3373_PIM_ROUTE_SPLIT.csv",
    "doc_3426": ROOT / "3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md",
    "chain_map_3426": OUT / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
    "branch_split_3426": OUT / "P8_Y5_R2FR_3426_PIM_BRANCH_SPLIT.csv",
    "topological_demoter_3426": OUT / "P8_Y5_R2FR_3426_TOPOLOGICAL_PIM_DEMOTER.csv",
    "projector_stress_contract": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "projector_algebra_contract": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "bound_fill_template": OUT / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
    "radial_bound_input": OUT / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
    "input_fill_template": OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3444_SOURCE_REGISTER.csv",
    "commutator_zero_theorem_attempt": OUT / "P8_Y5_R2FR_3444_COMMUTATOR_ZERO_THEOREM_ATTEMPT.csv",
    "branch_selection_gate": OUT / "P8_Y5_R2FR_3444_PIM_BRANCH_SELECTION_GATE.csv",
    "chain_map_signature_audit": OUT / "P8_Y5_R2FR_3444_CHAIN_MAP_SIGNATURE_AUDIT.csv",
    "icommutator_bound_input": OUT / "P8_Y5_R2FR_3444_ICOMMUTATOR_BOUND_INPUT.csv",
    "projector_stress_interface": OUT / "P8_Y5_R2FR_3444_PROJECTOR_STRESS_INTERFACE.csv",
    "csrc_flux_update": OUT / "P8_Y5_R2FR_3444_CSRC_FLUX_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3444_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3444_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3444_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3444_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3444_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    lines.extend("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows)
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3443": "immediate C_src handoff selecting [d,Pi_M]J_H",
        "next_3443": "machine-readable 3444 target",
        "csrc_decomposition_3443": "C_src flux-tail context",
        "flux_link_3443": "direct link from C_src to PiM commutator",
        "doc_1013": "measured-GM obstruction checkpoint",
        "obstruction_1013": "older exact obstruction vector",
        "flux_attempt_1013": "older PiM/J_H flux theorem attempt",
        "doc_1014": "prior commutator/projector variation gate",
        "commutator_1014": "prior theorem attempt rows",
        "coefficient_1014": "prior R_eq/I_commutator/projector bound rows",
        "claim_gate_1014": "prior claim gates blocking commutator promotion",
        "doc_1152": "later direct commutator zero audit",
        "audit_1152": "direct zero theorem audit",
        "acquisition_1152": "R_eq/I_commutator acquisition rows",
        "guards_1152": "no-shortcut route guards",
        "doc_2585": "R2FR chainmap checkpoint",
        "audit_2585": "chainmap antecedent audit",
        "bound_rows_2585": "I_commutator retained bound rows",
        "doc_3373": "R2FR commutator chainmap theorem checkpoint",
        "theorem_3373": "exact conditional chainmap theorem rows",
        "route_3373": "route split including old topological risk",
        "doc_3426": "Hilbert-identity PiM improvement checkpoint",
        "chain_map_3426": "identity/inclusion branch theorem rows",
        "branch_split_3426": "branch split selecting Hilbert identity as preferred",
        "topological_demoter_3426": "old topological PiM demotion rows",
        "projector_stress_contract": "projector variation stress contract",
        "projector_algebra_contract": "projector algebra not enough for flux closure",
        "bound_fill_template": "commutator/projector fallback fill row",
        "radial_bound_input": "radial/source-normalization interface",
        "input_fill_template": "source-backed input requirements",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCES.items()
    ]


def commutator_zero_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "COMZ3444_0_product_rule",
            "claim_piece": "projected-current commutator identity",
            "statement": "[d,Pi_M]J_H := d(Pi_M J_H)-Pi_M(dJ_H)",
            "derivation": "This is the exact obstruction in the product rule d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H. It cannot be deleted by projector algebra or by measured-GM calibration.",
            "result": "EXACT_OBSTRUCTION_IDENTITY_ACTIVE",
            "missing_to_promote": "zero theorem or source-backed I_commutator bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "COMZ3444_1_Hilbert_identity_zero",
            "claim_piece": "Hilbert-identity branch commutator zero",
            "statement": "If Pi_M^H is the identity/inclusion on the parent public Hilbert mass-current subcomplex C_H^M(A_ext), then [d,Pi_M^H]J_H^M=0.",
            "derivation": "On C_H^M(A_ext), Pi_M^H J=J and Pi_M^H dJ=dJ. Therefore d(Pi_M^H J)-Pi_M^H(dJ)=dJ-dJ=0. If the exterior is source-free, dJ_H^M=0 also gives both terms zero separately.",
            "result": "EXACT_CONDITIONAL_THEOREM_IDENTITY_BRANCH",
            "missing_to_promote": "parent must adopt Pi_M^H before readout; J_H^M must be the same source current used by clocks, rods, orbitals and local field equations",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "COMZ3444_2_extra_current_separation",
            "claim_piece": "why identity branch is not cheating",
            "statement": "J_H=J_H^M+J_extra; [d,Pi_M^H]J_H^M=0 but -Pi_M^H dJ_extra remains in Omega_GM unless extra-current projection is zero/bounded.",
            "derivation": "The identity branch kills only the operator commutator on the mass-current subcomplex. It does not absorb non-Hilbert, memory, boundary, species, frame, coupling or domain exchange into measured GM.",
            "result": "COMMUTATOR_REMOVED_ONLY_FROM_MASS_BRANCH",
            "missing_to_promote": "Pi_M dJ_extra, A_parent, R_eq/B_zero if old topological labels survive, coupling baseline and calibration tails",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "COMZ3444_3_fixed_scalar_charge_route",
            "claim_piece": "fixed Hilbert charge representative branch",
            "statement": "Pi_M^H J := ell_H[J;tau,S] omega_H gives [d,Pi_M^H]J=0 if d omega_H=0, ell_H is surface-invariant/chain-compatible, and J lies in the same Hilbert source complex.",
            "derivation": "The scalar-charge branch is also viable, but it has more clauses than the identity branch: omega_H must be parent-fixed and closed, ell_H must be H_tau-derived rather than fitted, and its radial/domain variation must vanish or be bounded.",
            "result": "EXACT_IF_DELLH_ZERO_DOMEGA_ZERO_AND_CHAIN_COMPATIBLE",
            "missing_to_promote": "ell_H owner, omega_H owner, surface invariance and no metric/domain stress",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "COMZ3444_4_old_topological_demoted",
            "claim_piece": "old independent topological Pi_M route",
            "statement": "Pi_M^top may be closed, but it is not automatically the observed Hilbert source charge: Pi_M^top J_H - Pi_M^H J_H = dB_zero + R_eq.",
            "derivation": "A conserved wrong object cannot prove Newton/source normalization. Unless R_eq=0 and compact boundary flux vanishes, old topological Pi_M remains a closure or bound-input route, not a local-GR derivation.",
            "result": "OLD_TOPOLOGICAL_ROUTE_DEMOTED_TO_BOUND_OR_SAME_OBJECT_GATE",
            "missing_to_promote": "Hilbert-topological equality, boundary-zero theorem and common M_H_ref denominator",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "COMZ3444_5_verdict",
            "claim_piece": "current commutator status",
            "statement": "The commutator has an exact low-scrutiny zero mechanism in the Hilbert-identity branch, but current MTS has not yet parent-adopted that branch as the source-current definition.",
            "derivation": "3444 therefore advances the route: do not keep hunting arbitrary Pi_M zeros; adopt/prove Pi_M^H from the parent Hilbert source branch or keep I_commutator rows active for any non-identity/topological/Hodge implementation.",
            "result": "FORWARD_ROUTE_FOUND_NOT_PUBLIC_CLAIM",
            "missing_to_promote": "parent adoption of Pi_M^H, source-free exterior/domain lock, extra-current projection and calibration/coupling tails",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def branch_selection_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "PBG3444_0_Hilbert_identity",
            "branch": "Pi_M^H is identity/inclusion on the parent public Hilbert mass-current subcomplex",
            "commutator_status": "THEOREM_ZERO_IF_PARENT_ADOPTED",
            "projector_stress_status": "NO_INDEPENDENT_PROJECTOR_STRESS",
            "residuals_retained": "-Pi_M dJ_extra;A_parent;coupling_baseline;calibration_tail",
            "decision": "PREFERRED_LOW_SCRUTINY_ROUTE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBG3444_1_fixed_Hilbert_charge",
            "branch": "Pi_M^H maps Hilbert current to ell_H omega_H with closed parent-fixed omega_H",
            "commutator_status": "ZERO_IF_ELLH_SURFACE_INVARIANT_AND_CHAIN_COMPATIBLE",
            "projector_stress_status": "ZERO_ONLY_IF_ELLH_OMEGAH_METRIC_DOMAIN_SILENT",
            "residuals_retained": "dell_H;domega_H;domain_motion;M_H_ref_lock",
            "decision": "BACKUP_ROUTE_MORE_ASSUMPTIONS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBG3444_2_old_topological",
            "branch": "independent topological Pi_M/J_M_top",
            "commutator_status": "NOT_USED_FOR_CLAIM_UNLESS_SAME_OBJECT_SIGNED",
            "projector_stress_status": "RETAIN_OR_BOUND",
            "residuals_retained": "R_eq_integral;B_zero_flux;I_commutator;conserved_wrong_object",
            "decision": "DEMOTE_TO_CLOSURE_OR_BOUND_INPUT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBG3444_3_Hodge_DeWitt_domain",
            "branch": "metric/Hodge/orthogonal/domain projector",
            "commutator_status": "NOT_ZERO_BY_DEFAULT",
            "projector_stress_status": "T_PiM_MUST_BE_RETAINED_AND_MAPPED",
            "residuals_retained": "epsilon_projector_stress;PPN_beta_gamma_alpha_xi;domain_preferred_frame",
            "decision": "REJECT_AS_SILENT_LOCAL_GR_ROUTE_UNLESS_STRESS_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def chain_map_signature_audit() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "CMS3444_0_parent_adopts_PiMH",
            "required_signature": "parent action/local branch defines Pi_M^H as identity or inclusion on Hilbert mass-current subcomplex before readout",
            "current_status": "NOT_YET_PARENT_ADOPTED_IN_THIS_CHECKPOINT",
            "if_signed": "I_commutator^H=0 by exact chain-map identity",
            "if_unsigned": "I_commutator remains live for arbitrary Pi_M",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "CMS3444_1_current_domain",
            "required_signature": "J_H^M belongs to the same source-current complex acted on by Pi_M^H",
            "current_status": "CONDITIONAL_ON_PUBLIC_HILBERT_SOURCE_BRANCH",
            "if_signed": "commutator theorem targets the observed source current rather than a surrogate",
            "if_unsigned": "closed-current theorem may be applied to the wrong object",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "CMS3444_2_exterior_on_shell",
            "required_signature": "compact exterior is source-free/on-shell for J_H^M and fixed before orbital scoring",
            "current_status": "CONDITIONAL_FIXED_DOMAIN_NEEDED",
            "if_signed": "dJ_H^M=0 and no domain-motion commutator is generated",
            "if_unsigned": "D_domain Pi_M and source leakage remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "CMS3444_3_no_post_readout_mask",
            "required_signature": "Pi_M^H is not chosen after measured-GM/orbital fitting",
            "current_status": "POLICY_ACTIVE_PARENT_PROOF_NEEDED",
            "if_signed": "source projection is a theorem object, not a fit mask",
            "if_unsigned": "measured-GM absorption shortcut invalidates the branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "CMS3444_4_no_hodge_projector",
            "required_signature": "identity/inclusion branch forbids independent Hodge, Green, DeWitt or metric-domain projector in the parent variation",
            "current_status": "ROUTE_SELECTION_CLAUSE_WRITTEN",
            "if_signed": "delta_g Pi_M^H=0 as an independent stress source",
            "if_unsigned": "projector stress interface must be used",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "CMS3444_5_topological_label_removed_or_equated",
            "required_signature": "old topological mass label is either removed or proved equal to the Hilbert source charge",
            "current_status": "OLD_TOPOLOGICAL_PIM_DEMOTED_NOT_REPAIRED",
            "if_signed": "R_eq/B_zero guard can close",
            "if_unsigned": "old topological branch remains closure-only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "CMS3444_6_verdict",
            "required_signature": "CMS3444_0 through CMS3444_5 signed together",
            "current_status": "NOT_ALL_SIGNED_ROUTE_READY",
            "if_signed": "OBS3444_1 commutator obstruction can be removed from the mass branch",
            "if_unsigned": "use nonclaim I_commutator/projector-stress bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def icommutator_bound_input() -> list[dict[str, Any]]:
    return [
        {
            "bound_input_id": "ICB3444_0_identity_branch_theorem_zero",
            "quantity": "I_commutator^H",
            "definition": "M_H_ref^-1 abs(int_A_ext [d,Pi_M^H]J_H^M)",
            "value_or_theorem": "0_IF_CMS3444_0_TO_CMS3444_4_PARENT_SIGNED",
            "units": "dimensionless_after_M_H_ref_normalization",
            "source_requirement": "parent proof file adopting Pi_M^H and Hilbert mass-current complex",
            "observable_link": "Newton;PPN;R10;R11;orbital",
            "status": "THEOREM_ZERO_CONDITIONAL_NOT_CLAIM_READY",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "ICB3444_1_old_topological_Icommutator",
            "quantity": "I_commutator^top",
            "definition": "M_H_ref^-1 abs(int_A_ext [d,Pi_M^top]J_H)",
            "value_or_theorem": "MISSING_I_COMMUTATOR_OR_SAME_OBJECT_THEOREM",
            "units": "dimensionless_after_M_H_ref_normalization_or_GM_flux_before_normalization",
            "source_requirement": "source-backed finite-shell calculation or R_eq=0 plus fixed chain-map theorem",
            "observable_link": "R10;PPN;Gdot;source_normalization;local_GR",
            "status": "RETAINED_NONCLAIM_FOR_NON_IDENTITY_BRANCHES",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "ICB3444_2_domain_motion",
            "quantity": "D_domain Pi_M",
            "definition": "operator/domain/worldtube/linking-surface derivative contribution to [d,Pi_M]J_H",
            "value_or_theorem": "MISSING_FIXED_DOMAIN_THEOREM_OR_OPERATOR_BOUND",
            "units": "operator_norm_or_dimensionless_flux",
            "source_requirement": "fixed compact exterior/source worldtube theorem or sourced domain-motion coefficient",
            "observable_link": "preferred_frame;preferred_location;R10;orbital;Gdot",
            "status": "RETAINED_UNLESS_IDENTITY_BRANCH_DOMAIN_LOCK_SIGNED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "ICB3444_3_total_no_cancellation",
            "quantity": "epsilon_PiM_comm_abs",
            "definition": "abs(I_commutator^top)+abs(D_domain Pi_M)+abs(epsilon_projector_stress)+abs(R_eq_integral)+abs(B_zero_flux)",
            "value_or_theorem": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_after_common_M_H_ref_normalization",
            "source_requirement": "each component separately theorem-zero or source-backed; no cancellation credit",
            "observable_link": "Newton;PPN;R10;R11;clock;orbital;local_GR",
            "status": "ABSOLUTE_ENVELOPE_DEFINED_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def projector_stress_interface() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "PSI3444_0_identity_no_independent_stress",
            "quantity": "delta_g Pi_M^H",
            "definition": "identity/inclusion map on Hilbert mass-current subcomplex has no independent projector variation",
            "result": "ZERO_IF_PARENT_ADOPTS_IDENTITY_BRANCH",
            "maps_to": "projector_stress_beta_equiv removed only for identity branch",
            "status": "CONDITIONAL_NOT_PUBLIC_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "PSI3444_1_hodge_domain_stress",
            "quantity": "T_PiM_munu",
            "definition": "stress generated by metric/Hodge/Green/domain dependence of Pi_M",
            "result": "RETAIN_AND_MAP_TO_PPN_R11_IF_USED",
            "maps_to": "gamma-1;beta-1;alpha_i;xi;R10;R11;source_normalization",
            "status": "RETAINED_FOR_NON_IDENTITY_PROJECTORS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "PSI3444_2_boundary_exact_guard",
            "quantity": "B_zero_flux and R_eq",
            "definition": "exact/boundary or topological-Hilbert difference surviving old topological PiM",
            "result": "NOT_TOUCHED_BY_IDENTITY_COMMUTATOR_PROOF_IF_OLD_LABEL_SURVIVES",
            "maps_to": "Newton source normalization;radial Meff hair;orbital calibration",
            "status": "RETAINED_UNTIL_OLD_TOPOLOGICAL_LABEL_REMOVED_OR_EQUATED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def csrc_flux_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "CFU3444_0_commutator_component",
            "prior_component": "FOL3443_2_projector_commutator;OBS1013_1_PiM_commutator",
            "before": "[d,Pi_M]J_H was retained as a live C_src flux-tail obstruction",
            "after": "in Hilbert-identity branch, [d,Pi_M^H]J_H^M=0 exactly; in old topological/Hodge/domain branches, I_commutator remains retained",
            "effect_on_Csrc": "C_src improves only if parent adopts Pi_M^H and no extra-current/source-calibration tail is hidden",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "CFU3444_1_total_obstruction",
            "prior_component": "Omega_GM",
            "before": "Omega_GM := -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent + R_eq + B_zero_flux + Delta_cal + Delta_PPN",
            "after": "Omega_GM^H := -Pi_M^H dJ_extra + A_parent + Delta_coupling + Delta_cal + Delta_PPN, with R_eq/B_zero absent only if old topological label is removed",
            "effect_on_Csrc": "commutator can be removed from preferred branch, but source-normalization/local-GR still needs extra-current, boundary/anomaly, coupling and calibration closures",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "CFU3444_2_no_cancellation_policy",
            "prior_component": "CSD3443_6_flux_tail",
            "before": "flux tail had multiple symbolic missing components",
            "after": "identity branch may set I_commutator^H=0, but every remaining term is scored separately under absolute no-cancellation envelope",
            "effect_on_Csrc": "one obstruction gets a plausible derivation route without allowing fitted cancellation or measured-GM laundering",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3444_0_sources",
            "claim": "all 3444 cited sources exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3444_1_exact_identity_proof",
            "claim": "there is an exact commutator-zero proof for Pi_M^H",
            "gate_pass": True,
            "reason": "Pi_M^H=identity/inclusion gives dPi-Pid=0 on the Hilbert mass-current subcomplex",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3444_2_parent_adoption",
            "claim": "MTS currently parent-signs Pi_M^H as the source-current projector",
            "gate_pass": False,
            "reason": "3444 writes the contract; it does not yet locate/adopt the parent action clause",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3444_3_old_topological_claim",
            "claim": "old topological Pi_M can support measured-GM/Newton claim",
            "gate_pass": False,
            "reason": "old topological PiM is demoted unless same-object equality and boundary-zero flux are proved",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3444_4_projector_stress",
            "claim": "projector stress is absent for every Pi_M implementation",
            "gate_pass": False,
            "reason": "stress silence is exact only for identity branch; Hodge/domain/topological implementations retain stress/bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3444_5_local_GR_Newton",
            "claim": "local GR/Newton reduction is now promoted",
            "gate_pass": False,
            "reason": "commutator branch improved, but C_src still needs parent adoption, extra-current zero, coupling/calibration closure and PPN residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3444_0_stop_chasing_arbitrary_PiM",
            "decision": "Do not keep trying to zero a generic projector commutator.",
            "because": "generic Pi_M can be a Hodge/domain/readout operator and then must carry stress; projector algebra alone never proves source closure",
            "next_action": "restrict the preferred branch to Pi_M^H identity/inclusion on the Hilbert mass current",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3444_1_preferred_branch",
            "decision": "Use the Hilbert-identity Pi_M^H branch as the less-scrutiny local source route.",
            "because": "the commutator zero is then an exact chain-map identity, not a fitted cancellation or topological guess",
            "next_action": "parent-adopt Pi_M^H and verify J_H^M is the same public source current used by clocks, rods, orbitals and field equations",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3444_2_old_topological_status",
            "decision": "Demote old independent topological Pi_M to closure-only or bound-input.",
            "because": "a closed topological current can still be the wrong conserved object for measured GM",
            "next_action": "only revive it through R_eq=0 plus boundary-zero proof, otherwise keep I_commutator/R_eq rows nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption-or-Htau-source-current-lock-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3445_Hilbert_identity_PiM_parent_adoption_or_Htau_source_current_lock.py",
            "objective": "turn the 3444 conditional commutator-zero mechanism into a parent-owned local branch by adopting Pi_M^H as identity/inclusion on the public Hilbert mass current, locking H_tau/source-current/domain ownership, and explicitly retaining extra-current/coupling/calibration tails",
            "success_condition": "Pi_M^H is parent-owned before readout on the same J_H^M used by clocks/orbits/field equations, or the branch is demoted back to nonclaim I_commutator/source-bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3444_0_preferred_branch",
            "branch": "Pi_M^H_identity",
            "theorem_zero_available": True,
            "parent_adopted": False,
            "score_ready": False,
            "result": "THEOREM_ROUTE_READY_NOT_CLAIM_READY",
            "why": "exact identity proof exists but parent branch adoption and source-current lock are not yet written",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN3444_1_non_identity_branches",
            "branch": "old_topological_or_Hodge_domain",
            "theorem_zero_available": False,
            "parent_adopted": False,
            "score_ready": False,
            "result": "RETAIN_ICOMMUTATOR_AND_PROJECTOR_STRESS_ROWS",
            "why": "non-identity implementations do not inherit dPi-Pid=0 and may generate stress/wrong-current residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    generated_csv_rows_parse = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        if path.exists():
            try:
                read_csv(path)
            except csv.Error:
                generated_csv_rows_parse = False

    validations = [
        {
            "check_id": "VAL3444_0_sources_exist",
            "condition": "all cited 3444 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3444_1_identity_zero_proof",
            "condition": "Hilbert-identity exact zero theorem is written",
            "passed": any(
                row["theorem_id"] == "COMZ3444_1_Hilbert_identity_zero"
                and row["result"] == "EXACT_CONDITIONAL_THEOREM_IDENTITY_BRANCH"
                for row in rows_by_name["commutator_zero_theorem_attempt"]
            ),
            "detail": "Pi_M^H identity/inclusion chain-map proof present",
        },
        {
            "check_id": "VAL3444_2_old_topological_demoted",
            "condition": "old topological PiM is not used as measured-GM proof",
            "passed": any(
                row["branch_id"] == "PBG3444_2_old_topological"
                and row["decision"] == "DEMOTE_TO_CLOSURE_OR_BOUND_INPUT"
                for row in rows_by_name["branch_selection_gate"]
            ),
            "detail": "conserved-wrong-object guard active",
        },
        {
            "check_id": "VAL3444_3_bound_rows_nonclaim",
            "condition": "I_commutator bound rows remain nonclaim unless parent adoption closes them",
            "passed": any(
                row["bound_input_id"] == "ICB3444_1_old_topological_Icommutator"
                and row["value_or_theorem"] == "MISSING_I_COMMUTATOR_OR_SAME_OBJECT_THEOREM"
                for row in rows_by_name["icommutator_bound_input"]
            ),
            "detail": "non-identity branches retain missing I_commutator",
        },
        {
            "check_id": "VAL3444_4_projector_stress_interface",
            "condition": "identity branch and Hodge/domain branch stress rules are separated",
            "passed": any(row["interface_id"] == "PSI3444_0_identity_no_independent_stress" for row in rows_by_name["projector_stress_interface"])
            and any(row["interface_id"] == "PSI3444_1_hodge_domain_stress" for row in rows_by_name["projector_stress_interface"]),
            "detail": "no silent stress deletion",
        },
        {
            "check_id": "VAL3444_5_csrc_update",
            "condition": "C_src update removes commutator only conditionally and retains remaining Omega_GM terms",
            "passed": any(
                row["update_id"] == "CFU3444_1_total_obstruction" and "Delta_coupling" in row["after"]
                for row in rows_by_name["csrc_flux_update"]
            ),
            "detail": "C_src flux update keeps remaining tails",
        },
        {
            "check_id": "VAL3444_6_next_target",
            "condition": "next target parent-adopts Hilbert identity PiM",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3444_7_no_cancellation",
            "condition": "total commutator envelope uses absolute components and no cancellation credit",
            "passed": any(
                row["bound_input_id"] == "ICB3444_3_total_no_cancellation" and "no cancellation" in row["source_requirement"].lower()
                for row in rows_by_name["icommutator_bound_input"]
            ),
            "detail": "absolute envelope row present",
        },
        {
            "check_id": "VAL3444_8_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": generated_csv_rows_parse,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3444_9_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3444_10_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3444_11_overall",
            "condition": "3444 commutator checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3444 - PiM/JH Commutator Zero or Icommutator Bound Input

## Summary
- This checkpoint attacks the exact C_src obstruction `[d,Pi_M]J_H`.
- The useful move is not another generic projector hunt: define the preferred local branch as `Pi_M^H`, the identity/inclusion on the public Hilbert mass-current subcomplex.
- In that branch, the commutator proof is exact: `d(Pi_M^H J_H^M)-Pi_M^H(dJ_H^M)=dJ_H^M-dJ_H^M=0`.
- This is progress, but not yet a public claim: the parent action still has to adopt `Pi_M^H` before readout and prove that `J_H^M` is the same source current used by clocks, rods, orbitals and field equations.
- Old independent topological `Pi_M` is demoted to closure-only or source-bound rows unless it is proved equal to the Hilbert source current.

## Source Register
{md_table(rows_by_name["source_register"])}

## Commutator Zero Theorem Attempt
{md_table(rows_by_name["commutator_zero_theorem_attempt"])}

## PiM Branch Selection Gate
{md_table(rows_by_name["branch_selection_gate"])}

## Chain-Map Signature Audit
{md_table(rows_by_name["chain_map_signature_audit"])}

## Icommutator Bound Input
{md_table(rows_by_name["icommutator_bound_input"])}

## Projector Stress Interface
{md_table(rows_by_name["projector_stress_interface"])}

## Csrc Flux Update
{md_table(rows_by_name["csrc_flux_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is a real forward step: the commutator can be killed cleanly if MTS chooses the Hilbert-identity source branch instead of an independent topological projector. The next work is to parent-own that choice, not to circle the generic `[d,Pi_M]` gap again. If that parent-adoption fails, the non-identity branches stay honestly demoted to `I_commutator`, `R_eq`, `B_zero_flux`, and projector-stress bound rows.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "commutator_zero_theorem_attempt": commutator_zero_theorem_attempt(),
        "branch_selection_gate": branch_selection_gate(),
        "chain_map_signature_audit": chain_map_signature_audit(),
        "icommutator_bound_input": icommutator_bound_input(),
        "projector_stress_interface": projector_stress_interface(),
        "csrc_flux_update": csrc_flux_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3444 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
