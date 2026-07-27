from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1864"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_SOURCE_REGISTER.csv",
    "local_gr_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_LOCAL_GR_REDUCTION_THEOREM.csv",
    "rlocal_to_sr_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_RLOCAL_TO_SR_MAP.csv",
    "priority_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_PROOF_ROUTE_PRIORITY_MATRIX.csv",
    "first_attack_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_FIRST_PROOF_ATTACK_CONTRACT.csv",
    "empirical_backstop": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_EMPIRICAL_BACKSTOP_MAP.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1864_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def path_has_needle(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC1864_0_1863_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1863-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md",
            "required_needle": "NEXT1863_0_primary",
            "use_in_1864": "selects the local-GR reduction contract and residual-vector prioritizer.",
        },
        {
            "source_id": "SRC1864_1_1863_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1863_VALIDATION.csv",
            "required_needle": "VAL1863_OVERALL",
            "use_in_1864": "confirms 1863 passed before the local-GR reduction contract is built.",
        },
        {
            "source_id": "SRC1864_2_1863_contract",
            "source_kind": "parent_current_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_PARENT_CURRENT_CONTRACT.csv",
            "required_needle": "PCC1863_7_parent_Euler_bridge",
            "use_in_1864": "imports the parent Euler bridge as the local GR/Newton reduced-branch requirement.",
        },
        {
            "source_id": "SRC1864_3_1863_residual_vector",
            "source_kind": "residual_vector",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_IX_JX_DEMOTION_LEDGER.csv",
            "required_needle": "IJX1863_7_total_vector",
            "use_in_1864": "imports R_local^MTS as the residual vector that must enter S_R rather than being hidden.",
        },
        {
            "source_id": "SRC1864_4_1863_requirements",
            "source_kind": "finite_residual_requirements",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_FINITE_RESIDUAL_REQUIREMENTS.csv",
            "required_needle": "FRR1863_4_parent_Euler_bridge",
            "use_in_1864": "imports the requirement to derive local reciprocity from the parent Euler difference.",
        },
        {
            "source_id": "SRC1864_5_1276_doc",
            "source_kind": "parent_Euler_contract_precedent",
            "source_path": ROOT / "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            "required_needle": "ESC1276_9_verdict",
            "use_in_1864": "provides the earlier executable but non-derivative parent Euler/source contract.",
        },
        {
            "source_id": "SRC1864_6_1276_contract_csv",
            "source_kind": "parent_Euler_contract_csv",
            "source_path": RESIDUALS / "P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
            "required_needle": "ESC1276_9_verdict",
            "use_in_1864": "lists E_time, E_radial, D_R, S_R, operator and boundary certificates.",
        },
        {
            "source_id": "SRC1864_7_1275_missing_csv",
            "source_kind": "missing_parent_Euler_inputs",
            "source_path": RESIDUALS / "P8_Y5_R10_1275_MISSING_PARENT_EULER_SOURCE_MAP.csv",
            "required_needle": "MPE1275_1_Euler_pair",
            "use_in_1864": "records the absent Euler pair/source map/boundary no-charge inputs.",
        },
        {
            "source_id": "SRC1864_8_1859_doc",
            "source_kind": "no_GR_import_route_selection",
            "source_path": ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            "required_needle": "BEST_NONCIRCULAR_ROUTE",
            "use_in_1864": "selects the MTS-owned E_time/E_radial equation difference over phase-volume closure.",
        },
        {
            "source_id": "SRC1864_9_1859_routes",
            "source_kind": "route_selection_csv",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_FIELD_EQUATION_ROUTE_SELECTION.csv",
            "required_needle": "FRS1859_2_parent_Euler_difference",
            "use_in_1864": "identifies the parent Euler difference as primary and EH inheritance as a held bridge.",
        },
        {
            "source_id": "SRC1864_10_1860_doc",
            "source_kind": "q_loc_EH_blocker",
            "source_path": ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
            "required_needle": "epsilon_GK_q_loc",
            "use_in_1864": "keeps q_loc as a live extra-sector residual that must enter S_R.",
        },
        {
            "source_id": "SRC1864_11_1860_activation",
            "source_kind": "q_loc_activation_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_ACTIVATION_CONTRACT.csv",
            "required_needle": "ACTC1860_6_verdict",
            "use_in_1864": "shows the q_loc formal normal form is not activated as a physical local-GR theorem.",
        },
        {
            "source_id": "SRC1864_12_1860_eh_bridge",
            "source_kind": "local_EH_bridge_impact",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_LOCAL_EH_BRIDGE_IMPACT.csv",
            "required_needle": "EHB1860_3_verdict",
            "use_in_1864": "states local EH/GR inheritance is not reopened while q_loc/readout locks remain open.",
        },
        {
            "source_id": "SRC1864_13_1860_epsilon",
            "source_kind": "q_loc_residual_row",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_EPSILON_GK_QLOC_RETENTION.csv",
            "required_needle": "RET1860_0_epsilon_GK_q_loc",
            "use_in_1864": "gives epsilon_GK_q_loc and its test links.",
        },
        {
            "source_id": "SRC1864_14_1862_source_measure",
            "source_kind": "source_measure_residual",
            "source_path": ROOT / "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
            "required_needle": "DHS1862_0_Delta_Hsrc",
            "use_in_1864": "imports Delta_Hsrc and I_X as source-normalization components.",
        },
        {
            "source_id": "SRC1864_15_1849_qbarXT",
            "source_kind": "qbarXT_component_envelope",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv",
            "required_needle": "QBC1849_5_total_abs_guard",
            "use_in_1864": "imports ordinary-matter X charge leakage components.",
        },
        {
            "source_id": "SRC1864_16_1804_constants",
            "source_kind": "constant_sector_debt",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_CONSTANT_SUPERSELECTION_GATE.csv",
            "required_needle": "CSG1804_5_verdict",
            "use_in_1864": "imports alpha/mass/clock constant-sector residuals.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in sources:
        path = source["source_path"]
        needle = source["required_needle"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_kind": source["source_kind"],
                "source_path": str(path),
                "path_exists": as_bool_text(path.exists()),
                "required_needle": needle,
                "needle_found": as_bool_text(path_has_needle(path, needle)),
                "use_in_1864": source["use_in_1864"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def local_gr_theorem() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_0_variables",
            "piece": "local reciprocal variables",
            "statement": "Define J_q:=T sqrt(S) and C_R:=ln(T^2 S)=2 ln(J_q).",
            "proof_status": "EXACT_DEFINITION",
            "missing_for_claim": "none_as_definition",
            "result_if_closed": "C_R=0 is equivalent to T^2 S=1 and the reciprocal local branch.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_1_parent_Euler_pair",
            "piece": "parent E_time and E_radial",
            "statement": "Derive E_time:=delta S_parent/delta ln(T) and E_radial:=delta S_parent/delta ln(sqrt(S)) or their coframe equivalents from the MTS parent action.",
            "proof_status": "MISSING_EULER_PAIR",
            "missing_for_claim": "MISSING_L_PARENT;MISSING_E_TIME;MISSING_E_RADIAL;MISSING_NO_EH_IMPORT_CERTIFICATE",
            "result_if_closed": "creates the legal objects whose difference can select the local reciprocal branch.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_2_DR_normal_form",
            "piece": "radial equation-difference normal form",
            "statement": "Show D_R[MTS]:=E_time-E_radial = partial_r C_R - S_R[R_local^MTS,source,boundary,readout] = 0, or the second-order no-hair form partial_r(W partial_r C_R)=J_R with W>0.",
            "proof_status": "CONTRACT_ONLY_PRIMARY_TARGET",
            "missing_for_claim": "MISSING_ALGEBRAIC_DERIVATION_OF_D_R;MISSING_SOURCE_MAP;MISSING_OPERATOR_SIGN",
            "result_if_closed": "turns local GR reduction into source/boundary/residual silence rather than an imposed plateau.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_3_source_silence",
            "piece": "S_R=0 or bounded",
            "statement": "Prove every component of S_R vanishes on the local vacuum/source-balanced branch, or keep absolute finite bounds with common units and arena projections.",
            "proof_status": "RESIDUAL_VECTOR_RETAINED",
            "missing_for_claim": "MISSING_DELTA_HSRC_ZERO;MISSING_IX_JX_ZERO_OR_BOUNDS;MISSING_QLOC_ZERO_OR_BOUND;MISSING_CONSTANT_SOURCE_SILENCE",
            "result_if_closed": "makes C_R constant in the first-order form, or source-free in the second-order form.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_4_boundary_no_charge",
            "piece": "Q_R=0 and normalization",
            "statement": "Prove boundary/reference class sets Q_R=0 and C_R(infinity)=0 or an equivalent regular matching condition.",
            "proof_status": "BOUNDARY_NO_CHARGE_UNSIGNED",
            "missing_for_claim": "MISSING_BOUNDARY_CLASS;MISSING_EDGE_CHARGE_ZERO;MISSING_REFERENCE_SUBTRACTION_OWNER",
            "result_if_closed": "integrates the source-free D_R equation to C_R=0 rather than C_R=constant or hair.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_5_reciprocal_consequence",
            "piece": "local reciprocal/GR branch",
            "statement": "If LGT1864_1 through LGT1864_4 close, C_R=0 follows; with T^2=1-L and S=(1-L)^(-p), C_R=0 gives p=1 and the GR-style reciprocal local metric branch.",
            "proof_status": "EXACT_CONDITIONAL_NOT_ACTIVATED",
            "missing_for_claim": "UPSTREAM_LGT1864_1_TO_LGT1864_4_NOT_CLOSED",
            "result_if_closed": "opens the route to source-normalized Newton/PPN only after metric/readout/source gates are also signed.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "LGT1864_6_verdict",
            "piece": "local GR/Newton derivation status",
            "statement": "The theorem contract is exact and useful, but current MTS has not derived the Euler pair, D_R normal form, S_R silence, or boundary no-charge conditions.",
            "proof_status": "LOCAL_GR_REDUCTION_CONTRACT_READY_NOT_DERIVED",
            "missing_for_claim": "MISSING_FIRST_PROOF_ATTACK_D_R_NORMAL_FORM",
            "result_if_closed": "the project would have a defensible derivation route rather than a closure axiom.",
            "closes_local_GR": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def rlocal_to_sr_map() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_0_Delta_Hsrc",
            "residual": "Delta_Hsrc",
            "enters_SR_as": "source-normalization/source-measure mismatch",
            "source_status": "CENTRAL_Y5_RESIDUAL_RETAINED",
            "zero_or_bound_needed": "Delta_Hsrc=0 or finite source-bound in the same M_H_ref convention",
            "test_links": "orbital;Gauss;PPN;source_normalized_Newton",
            "priority_class": "high_coupling",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_1_I_X",
            "residual": "I_X",
            "enters_SR_as": "first non-EH curl/source component in delta_H_tau",
            "source_status": "NOT_THEOREM_ZERO",
            "zero_or_bound_needed": "parent-current owner plus X source silence or finite I_X bound",
            "test_links": "orbital;PPN;local_GR;source_normalization",
            "priority_class": "high_coupling",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_2_J_X_qbarXT",
            "residual": "J_X/qbar_XT",
            "enters_SR_as": "ordinary/hidden matter source current in the dangerous local direction",
            "source_status": "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            "zero_or_bound_needed": "matter functor descent, no-marker/constants, hidden-tail silence, or finite qbar components",
            "test_links": "R10;WEP;clock;PPN;orbital",
            "priority_class": "high_coupling",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_3_constants",
            "residual": "b_alpha/b_mu/b_mA/b_nuc/b_clock_i",
            "enters_SR_as": "dimensionless constant and composition leakage into matter/source/readout",
            "source_status": "ALPHA_MASS_CLOCK_CHANNELS_RETAINED",
            "zero_or_bound_needed": "no-extra-F2/no-mass/no-binding/no-clock-shadow theorem or finite coefficient matrix",
            "test_links": "fine_structure;WEP;clock;R10",
            "priority_class": "high_coupling",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_4_boundary_history",
            "residual": "boundary/history/non-Hilbert tails",
            "enters_SR_as": "edge charge, support, domain, reference and memory tails",
            "source_status": "TAILS_NOT_ZERO_NOT_BOUNDED",
            "zero_or_bound_needed": "zero-flux/exact primitive or absolute finite boundary/history rows",
            "test_links": "orbital;source_normalization;R10;local_GR",
            "priority_class": "boundary_hair",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_5_epsilon_GK_q_loc",
            "residual": "epsilon_GK_q_loc",
            "enters_SR_as": "extra-sector local force/source residual contaminating the EH/Euler bridge",
            "source_status": "RETAIN_NONCLAIM",
            "zero_or_bound_needed": "Gamma_eff/K_hat live action pair, metric response, coupling lock, projector/boundary and observable lock",
            "test_links": "local_GR;PPN;clock;orbital;WEP;R10",
            "priority_class": "extra_sector",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_6_qR_SR",
            "residual": "q_R/S_R reciprocal hair",
            "enters_SR_as": "integration charge or source imbalance in the radial reciprocal equation",
            "source_status": "BOUNDARY_NO_CHARGE_UNSIGNED",
            "zero_or_bound_needed": "Q_R=0 theorem, source-balance theorem, boundary normalization",
            "test_links": "PPN_gamma;orbital;lightcone;local_GR",
            "priority_class": "direct_GR_shape",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "RSM1864_7_readout_projection",
            "residual": "readout/projection leakage",
            "enters_SR_as": "observed metric/source/readout map reentry after field equations",
            "source_status": "PURE_POSTPROCESSING_SAFE_NOT_GENERAL",
            "zero_or_bound_needed": "arena-by-arena pure readout typing or finite projection/reentry coefficients",
            "test_links": "Pantheon;BAO;SPARC;R10;WEP;clock;PPN",
            "priority_class": "readout_lock",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def priority_matrix() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "PR1864_0_DR_normal_form",
            "candidate_target": "derive D_R[MTS]=E_time-E_radial normal form and S_R decomposition",
            "direct_GR_leverage": 5,
            "derivation_readiness": 4,
            "dependency_risk": 3,
            "empirical_backstop_value": 5,
            "why_ranked_here": "it creates the equation where all residuals live; without it, zeroing individual channels does not prove the reciprocal GR branch.",
            "decision": "SELECT_FIRST",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PR1864_1_Gamma_Khat_q_loc",
            "candidate_target": "activate Gamma_eff/K_hat/q_loc as a live action/metric-response pair",
            "direct_GR_leverage": 5,
            "derivation_readiness": 3,
            "dependency_risk": 4,
            "empirical_backstop_value": 4,
            "why_ranked_here": "q_loc blocks EH inheritance, but it still needs the D_R/S_R ledger to say how q_loc contaminates reciprocity.",
            "decision": "SECOND_AFTER_DR_LEDGER",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PR1864_2_no_extra_matter_vertices",
            "candidate_target": "forbid extra F2/mass/binding/source-weight vertices",
            "direct_GR_leverage": 4,
            "derivation_readiness": 3,
            "dependency_risk": 5,
            "empirical_backstop_value": 5,
            "why_ranked_here": "this is the coupling gut-punch, but it is broad; better to know first which S_R slot these coefficients must silence.",
            "decision": "HELD_PARALLEL_HIGH_VALUE",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PR1864_3_boundary_no_charge",
            "candidate_target": "prove Q_R=0 and boundary/reference normalization",
            "direct_GR_leverage": 4,
            "derivation_readiness": 3,
            "dependency_risk": 3,
            "empirical_backstop_value": 3,
            "why_ranked_here": "necessary for C_R=0 after source silence, but premature before D_R operator form is chosen.",
            "decision": "THIRD_OR_PARALLEL_AFTER_OPERATOR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PR1864_4_common_units_arena_maps",
            "candidate_target": "declare common units and arena projections for R_local^MTS",
            "direct_GR_leverage": 3,
            "derivation_readiness": 5,
            "dependency_risk": 2,
            "empirical_backstop_value": 5,
            "why_ranked_here": "fast and test-useful, but it is a fallback/test scaffold rather than a derivation of GR.",
            "decision": "BACKSTOP_WORK_AFTER_DR_DEFINITION",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PR1864_5_full_parent_action",
            "candidate_target": "derive the full parent action grammar in one step",
            "direct_GR_leverage": 5,
            "derivation_readiness": 1,
            "dependency_risk": 5,
            "empirical_backstop_value": 2,
            "why_ranked_here": "ultimate target, but too broad for the next move; use the D_R normal form as the action grammar stress test.",
            "decision": "NOT_FIRST_TOO_BROAD",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def first_attack_contract() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_0_field_variables",
            "needed_piece": "minimal local variables",
            "contract": "Declare local static/spherical or weak-field variables T,S or equivalent coframe components plus all residual slots before varying.",
            "success_condition": "variables are parent-owned and not copied from a GR ansatz after the fact.",
            "current_status": "PARTIAL_SYMBOL_MAP_ONLY",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_1_parent_action_slice",
            "needed_piece": "local parent action slice",
            "contract": "Write S_parent^local = integral dr L_MTS[T,S,Phi_extra,Psi,boundary] with source/readout slots declared.",
            "success_condition": "E_time and E_radial can be varied from L_MTS without importing Einstein equations.",
            "current_status": "MISSING_L_MTS_CORE",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_2_Euler_pair",
            "needed_piece": "E_time and E_radial",
            "contract": "Compute E_time:=delta S_parent/delta ln(T) and E_radial:=delta S_parent/delta ln(sqrt(S)) including residual/source/boundary terms.",
            "success_condition": "both equations are explicit and MTS-owned.",
            "current_status": "MISSING_EULER_PAIR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_3_difference_algebra",
            "needed_piece": "D_R algebra",
            "contract": "Form E_time-E_radial and collect terms into partial_r C_R - S_R or partial_r(W partial_r C_R)-J_R.",
            "success_condition": "C_R derivative appears with declared operator and all non-GR pieces are listed in S_R/J_R.",
            "current_status": "PRIMARY_1865_TARGET",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_4_SR_decomposition",
            "needed_piece": "S_R residual source map",
            "contract": "Map Delta_Hsrc, I_X/J_X, qbar_XT, constants, boundary/history, epsilon_GK_q_loc, q_R and readout leakage into S_R slots.",
            "success_condition": "no residual is silently dropped or hidden inside fitted GM.",
            "current_status": "SKELETON_READY_VALUES_MISSING",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_5_no_import_guard",
            "needed_piece": "no-GR-import certificate",
            "contract": "Any use of GR equations is labelled benchmark-only unless local EH fixed point has already been derived from MTS.",
            "success_condition": "the proof does not use G^t_t-G^r_r=0, Schwarzschild AB=1, or fitted PPN success as a premise.",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attack_id": "FAC1864_6_verdict",
            "needed_piece": "first proof attack readiness",
            "contract": "1865 should attempt FAC1864_0 through FAC1864_5 and either derive D_R or demote it to an explicit S_R residual-decomposition closure.",
            "success_condition": "D_R normal form is derived, or every failed clause becomes a named missing input/source row.",
            "current_status": "SELECTED_FOR_1865",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def empirical_backstop() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "backstop_id": "EBS1864_0_R10_WEP",
            "arena": "R10/WEP",
            "uses_residuals": "J_X;qbar_XT;b_alpha;b_mA;epsilon_GK_q_loc",
            "needed_before_scoring": "common normalization, lambda/range, source/test charge split, source-backed bounds",
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "backstop_id": "EBS1864_1_PPN",
            "arena": "PPN/lightcone",
            "uses_residuals": "C_R;q_R/S_R;epsilon_GK_q_loc;readout_projection",
            "needed_before_scoring": "D_R normal form, metric readout map, gamma/beta projection, boundary normalization",
            "current_status": "NOT_SCORE_READY",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "backstop_id": "EBS1864_2_clock_fine_structure",
            "arena": "clock/fine-structure",
            "uses_residuals": "b_alpha;b_mu;b_nuc;b_clock_i;readout_projection",
            "needed_before_scoring": "constant-sector coefficient values or theorem-zero plus tau_clock/local dXhat map",
            "current_status": "SOURCE_SENSITIVITIES_EXIST_MTS_COEFFICIENTS_MISSING",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "backstop_id": "EBS1864_3_orbital_Newton",
            "arena": "orbital/source-normalized Newton",
            "uses_residuals": "Delta_Hsrc;I_X;boundary_history;q_R/S_R",
            "needed_before_scoring": "do not use fitted GM as source proof; derive/source-bound Delta_Hsrc and boundary/no-charge terms",
            "current_status": "GUARDRAIL_ACTIVE_NOT_SCORE_READY",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1864_0_local_GR_reduction",
            "claim": "MTS derives the local GR/Newton branch",
            "status": "BLOCKED",
            "reason": "LGT1864_1 through LGT1864_4 are not closed.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1864_1_DR_normal_form",
            "claim": "D_R[MTS]=partial_r C_R-S_R is derived",
            "status": "BLOCKED",
            "reason": "E_time, E_radial, the source map and the operator sign/order remain missing.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1864_2_SR_zero",
            "claim": "S_R=0 on the local vacuum/source-balanced branch",
            "status": "BLOCKED",
            "reason": "R_local^MTS components remain nonclaim residuals with missing zero theorems or bounds.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1864_3_empirical_pass",
            "claim": "R10/WEP/PPN/clock/orbital arenas pass from the local branch",
            "status": "BLOCKED",
            "reason": "common units, arena projections and source-backed coefficient values are absent.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1864_0_theorem_contract",
            "decision": "LOCAL_GR_REDUCTION_THEOREM_CONTRACT_EXACT_CONDITIONAL",
            "reason": "C_R=0 follows cleanly from a parent-derived D_R equation, source silence and no-charge boundary normalization.",
            "next_action": "do not promote; use as a proof checklist.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1864_1_residual_map",
            "decision": "RLOCAL_MUST_ENTER_SR_EXPLICITLY",
            "reason": "Delta_Hsrc, I_X/J_X, constants, boundary/history, q_loc and readout leakage are exactly the terms that would spoil C_R=0.",
            "next_action": "no residual can be hidden in fitted GM or dropped from the local equation.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1864_2_first_target",
            "decision": "DR_NORMAL_FORM_AND_SR_DECOMPOSITION_SELECTED_FIRST",
            "reason": "it is the shortest noncircular move toward GR/Newton: derive the equation before trying to kill every source term.",
            "next_action": "build 1865 to attempt E_time/E_radial/D_R normal form or demote the missing pieces.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1864_3_not_claim",
            "decision": "LOCAL_GR_NEWTON_REMAINS_BLOCKED",
            "reason": "the reduction contract is ready, but the parent Euler pair, S_R silence and boundary no-charge proof are not derived.",
            "next_action": "keep all local claims private/nonclaim until the proof chain closes or finite residual rows score honestly.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1864_0_primary",
            "next_target": "1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md",
            "script": "scripts/Y5_R2FR_parent_Euler_difference_normal_form_or_SR_residual_decomposition_1865.py",
            "objective": "attempt to derive E_time, E_radial and D_R[MTS]=partial_r C_R-S_R from an MTS local parent action slice; if this fails, emit a precise S_R residual decomposition and missing-input ledger without claiming local GR.",
            "selection_status": "selected",
            "success_condition": "D_R normal form is derived without GR import, or every missing parent/action/source/operator/boundary clause becomes an explicit nonclaim residual row.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1864_1_parallel",
            "next_target": "1865b-Y5-R2FR-Gamma-Khat-q-loc-live-action-pair-or-SR-source-row.md",
            "script": "scripts/Y5_R2FR_Gamma_Khat_qloc_live_action_pair_or_SR_source_row_1865b.py",
            "objective": "try to turn Gamma_eff/K_hat into a live metric-response pair or map epsilon_GK_q_loc into an S_R source row with units and arena projections.",
            "selection_status": "held_parallel",
            "success_condition": "q_loc is either parent-zero in the D_R source map or retained as a quantified S_R component.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1864_2_parallel_coupling",
            "next_target": "1865c-Y5-R2FR-no-extra-F2-mass-binding-source-vertex-or-SR-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_no_extra_F2_mass_binding_source_vertex_or_SR_coefficient_pack_1865c.py",
            "objective": "attack the matter/constant/source coupling channel by proving no extra vertices or producing finite S_R coefficient rows.",
            "selection_status": "held_parallel",
            "success_condition": "alpha/mass/binding/source-weight terms are theorem-zero or become source-backed finite S_R coefficients.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_fields = {"valid_for_claim", "claim_allowed", "gate_pass", "closes_local_GR"}
    for rows in rows_by_name.values():
        for row in rows:
            for field in guarded_fields:
                if str(row.get(field, "")).strip().lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                    return False
                if str(row.get("claim_allowed", "")).strip().lower() == "true":
                    return False
    return True


def csvs_parse(paths: list[Path]) -> bool:
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
    return True


def copy_branch_outputs(paths: list[Path]) -> None:
    for folder in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
        folder.mkdir(parents=True, exist_ok=True)
    for path in paths:
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1864_{path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        targets = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1864_{path.name}",
        ]
        if not all(target.exists() for target in targets):
            return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1864*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    theorem = rows_by_name["local_gr_theorem"]
    sr_map = rows_by_name["rlocal_to_sr_map"]
    priorities = rows_by_name["priority_matrix"]
    attacks = rows_by_name["first_attack_contract"]
    claims = rows_by_name["claim_gate"]
    decisions = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1864_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in sources) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1864_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in sources) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1864_2_theorem_contract_not_promoted",
            "status": "PASS" if any(row["proof_status"] == "LOCAL_GR_REDUCTION_CONTRACT_READY_NOT_DERIVED" for row in theorem) else "FAIL",
            "detail": "local-GR theorem contract is ready but not derived",
        },
        {
            "validation_id": "VAL1864_3_all_local_GR_flags_false",
            "status": "PASS" if all(row["closes_local_GR"] == "False" for row in theorem) else "FAIL",
            "detail": "no local-GR theorem row closes the claim",
        },
        {
            "validation_id": "VAL1864_4_residual_map_covers_Rlocal",
            "status": "PASS" if len(sr_map) >= 8 else "FAIL",
            "detail": "R_local^MTS components are mapped into S_R slots",
        },
        {
            "validation_id": "VAL1864_5_priority_selects_DR",
            "status": "PASS" if any(row["route_id"] == "PR1864_0_DR_normal_form" and row["decision"] == "SELECT_FIRST" for row in priorities) else "FAIL",
            "detail": "D_R normal form and S_R decomposition selected as first proof attack",
        },
        {
            "validation_id": "VAL1864_6_first_attack_contract_ready",
            "status": "PASS" if any(row["attack_id"] == "FAC1864_6_verdict" and row["current_status"] == "SELECTED_FOR_1865" for row in attacks) else "FAIL",
            "detail": "first proof attack contract is ready for 1865",
        },
        {
            "validation_id": "VAL1864_7_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claims) else "FAIL",
            "detail": "all local/reduction/test claim gates remain blocked",
        },
        {
            "validation_id": "VAL1864_8_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim, local-GR or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1864_9_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked claim-ready",
        },
        {
            "validation_id": "VAL1864_10_decision_next",
            "status": "PASS" if any(row["decision"] == "DR_NORMAL_FORM_AND_SR_DECOMPOSITION_SELECTED_FIRST" for row in decisions) else "FAIL",
            "detail": "decision ledger selects D_R normal form first",
        },
        {
            "validation_id": "VAL1864_11_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1864_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1864_12_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1864_13_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1864_14_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1864_15_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1864 outputs found under formalization-workbench",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1864_OVERALL",
            "status": overall,
            "detail": "1864 local-GR reduction contract and residual-vector prioritizer checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1864 - Y5/R2FR Local-GR Reduction Contract And Residual-Vector Prioritizer",
        "",
        "## Verdict",
        "",
        "1864 turns the local-GR problem into a concrete theorem contract. The target is no longer 'assume a local plateau' or 'hope tests are quiet'. The target is: derive the parent Euler pair, form `D_R[MTS]=E_time-E_radial`, show it becomes `partial_r C_R-S_R=0` or a positive second-order no-hair equation, then prove `S_R=0` and `Q_R=0` without importing GR.",
        "",
        "The exact conditional prize is strong: `C_R=ln(T^2 S)=0`, hence `T^2 S=1`; with `T^2=1-L` and `S=(1-L)^(-p)`, this gives `p=1`, the reciprocal GR-style local metric branch. But the current corpus has not derived the parent Euler pair, the `D_R` normal form, source silence, or boundary no-charge theorem.",
        "",
        "Therefore the best next attack is not to chase every coupling at once. It is to derive the `D_R` normal form and explicit `S_R[R_local^MTS]` decomposition first. That gives every later coupling/q_loc/boundary proof a legal slot in the local-GR derivation.",
        "",
        "**Claim ceiling:** no local-GR/Newton reduction claim, no `D_R` derivation claim, no `S_R=0` claim, no R10/WEP/PPN/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1864.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1864", "valid_for_claim"],
        ),
        "",
        "## Local GR Reduction Theorem",
        "",
        markdown_table(
            rows_by_name["local_gr_theorem"],
            ["theorem_id", "piece", "statement", "proof_status", "missing_for_claim", "result_if_closed", "closes_local_GR", "valid_for_claim"],
        ),
        "",
        "## R_local To S_R Map",
        "",
        markdown_table(
            rows_by_name["rlocal_to_sr_map"],
            ["map_id", "residual", "enters_SR_as", "source_status", "zero_or_bound_needed", "test_links", "priority_class", "valid_for_claim"],
        ),
        "",
        "## Proof Route Priority Matrix",
        "",
        markdown_table(
            rows_by_name["priority_matrix"],
            ["route_id", "candidate_target", "direct_GR_leverage", "derivation_readiness", "dependency_risk", "empirical_backstop_value", "why_ranked_here", "decision", "valid_for_claim"],
        ),
        "",
        "## First Proof Attack Contract",
        "",
        markdown_table(
            rows_by_name["first_attack_contract"],
            ["attack_id", "needed_piece", "contract", "success_condition", "current_status", "valid_for_claim"],
        ),
        "",
        "## Empirical Backstop Map",
        "",
        markdown_table(
            rows_by_name["empirical_backstop"],
            ["backstop_id", "arena", "uses_residuals", "needed_before_scoring", "current_status", "valid_for_claim"],
        ),
        "",
        "## Claim Gates",
        "",
        markdown_table(
            rows_by_name["claim_gate"],
            ["claim_id", "claim", "status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Decision Ledger",
        "",
        markdown_table(
            rows_by_name["decision_ledger"],
            ["decision_id", "decision", "reason", "next_action", "valid_for_claim"],
        ),
        "",
        "## Next Target",
        "",
        markdown_table(
            rows_by_name["next_target"],
            ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "status", "detail", "valid_for_claim"],
        ),
        "",
        "## Interpretation",
        "",
        "This is the cleanest route of attack. We are not claiming the knockout; we are building the round-by-round scoring system for the local theorem. If 1865 can derive the `D_R` normal form, the GR/Newton reduction problem becomes a finite list of source terms to kill or bound. If it cannot, we will know exactly which action/current/source-map object is missing rather than just saying 'coupling' in the dark.",
    ]
    DOC_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "local_gr_theorem": local_gr_theorem(),
        "rlocal_to_sr_map": rlocal_to_sr_map(),
        "priority_matrix": priority_matrix(),
        "first_attack_contract": first_attack_contract(),
        "empirical_backstop": empirical_backstop(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }

    non_validation_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, rows_by_name[key])

    copy_branch_outputs(non_validation_paths)
    remove_pycache()

    rows_by_name["validation"] = validation_rows(rows_by_name, non_validation_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    copy_branch_outputs([OUTPUTS["validation"]])
    remove_pycache()

    if any(row["status"] == "FAIL" for row in rows_by_name["validation"]):
        raise SystemExit("1864 validation failed")

    print(f"Wrote {DOC_PATH}")
    for path in OUTPUTS.values():
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
