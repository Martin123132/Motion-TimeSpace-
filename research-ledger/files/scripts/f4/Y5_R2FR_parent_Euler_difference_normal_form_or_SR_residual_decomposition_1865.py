from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1865"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_SOURCE_REGISTER.csv",
    "variable_orientation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_VARIABLE_ORIENTATION_AUDIT.csv",
    "dr_derivation_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_DR_DERIVATION_ATTEMPT.csv",
    "sr_residual_decomposition": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_SR_RESIDUAL_DECOMPOSITION.csv",
    "missing_input_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_MISSING_INPUT_LEDGER.csv",
    "no_gr_import_guard": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_NO_GR_IMPORT_GUARD.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1865_VALIDATION.csv",
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
            "source_id": "SRC1865_0_1864_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md",
            "required_needle": "NEXT1864_0_primary",
            "use_in_1865": "selects the parent Euler difference normal-form attempt.",
        },
        {
            "source_id": "SRC1865_1_1864_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1864_VALIDATION.csv",
            "required_needle": "VAL1864_OVERALL",
            "use_in_1865": "confirms 1864 passed before 1865 starts.",
        },
        {
            "source_id": "SRC1865_2_1864_theorem",
            "source_kind": "local_GR_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_LOCAL_GR_REDUCTION_THEOREM.csv",
            "required_needle": "LGT1864_2_DR_normal_form",
            "use_in_1865": "imports the D_R normal-form theorem target.",
        },
        {
            "source_id": "SRC1865_3_1864_SR_map",
            "source_kind": "S_R_map",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_RLOCAL_TO_SR_MAP.csv",
            "required_needle": "RSM1864_7_readout_projection",
            "use_in_1865": "imports all R_local^MTS residual slots that must enter S_R.",
        },
        {
            "source_id": "SRC1865_4_1864_attack_contract",
            "source_kind": "first_attack_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1864_FIRST_PROOF_ATTACK_CONTRACT.csv",
            "required_needle": "FAC1864_6_verdict",
            "use_in_1865": "imports the required 1865 proof-attack steps.",
        },
        {
            "source_id": "SRC1865_5_1276_contract",
            "source_kind": "parent_Euler_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
            "required_needle": "ESC1276_9_verdict",
            "use_in_1865": "states the earlier executable contract and its missing Euler/source map inputs.",
        },
        {
            "source_id": "SRC1865_6_1275_missing",
            "source_kind": "missing_Euler_inputs",
            "source_path": RESIDUALS / "P8_Y5_R10_1275_MISSING_PARENT_EULER_SOURCE_MAP.csv",
            "required_needle": "MPE1275_0_Lcore",
            "use_in_1865": "records that L_core, Euler pair, source map, W and boundary no-charge are missing.",
        },
        {
            "source_id": "SRC1865_7_1272_variational",
            "source_kind": "radial_cell_variational_attempt",
            "source_path": RESIDUALS / "P8_Y5_R10_1272_RADIAL_CELL_VARIATIONAL_DERIVATION_ATTEMPT.csv",
            "required_needle": "RCD1272_7_verdict",
            "use_in_1865": "shows the radial-cell action route is conditional but not parent-derived.",
        },
        {
            "source_id": "SRC1865_8_1272_matrix",
            "source_kind": "cell_principle_test_matrix",
            "source_path": RESIDUALS / "P8_Y5_R10_1272_CELL_PRINCIPLE_TEST_MATRIX.csv",
            "required_needle": "CPT1272_5_constrained_action",
            "use_in_1865": "compares Liouville, configuration-cell, current, gauge and constrained-action routes.",
        },
        {
            "source_id": "SRC1865_9_1273_variables",
            "source_kind": "u_v_variable_change",
            "source_path": RESIDUALS / "P8_Y5_R10_1273_UV_RADIAL_CELL_VARIABLE_CHANGE.csv",
            "required_needle": "UV1273_0_u_cell_volume",
            "use_in_1865": "supplies the clean u/v split for C_R and cone-ratio variables.",
        },
        {
            "source_id": "SRC1865_10_1274_unimodular",
            "source_kind": "unimodular_cell_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1274_UNIMODULAR_CELL_ORIGIN_AUDIT.csv",
            "required_needle": "URO1274_6_less_scrutiny_rule",
            "use_in_1865": "selects field-equation difference over imposed cell unimodularity.",
        },
        {
            "source_id": "SRC1865_11_1577_current",
            "source_kind": "cell_current_no_charge_attempt",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1577_RADIAL_CELL_CURRENT_ATTEMPT.csv",
            "required_needle": "RCC1577_4_verdict",
            "use_in_1865": "shows conserved radial-cell current leaves Q_R hair unless no-charge is derived.",
        },
        {
            "source_id": "SRC1865_12_1253_Hcore",
            "source_kind": "Hcore_source_equation_attempt",
            "source_path": RESIDUALS / "P8_Y5_R10_1253_RECIPROCAL_HCORE_SOURCE_EQUATION_ATTEMPT.csv",
            "required_needle": "HCE1253_0_reciprocal_euler_source",
            "use_in_1865": "shows the reciprocal source equation needs explicit H_core/L_MTS_core.",
        },
        {
            "source_id": "SRC1865_13_10_observer_contract",
            "source_kind": "observer_map_contract",
            "source_path": ROOT / "10-observer-map-symplectic-contract.md",
            "required_needle": "observer_map_contract_written_not_satisfied",
            "use_in_1865": "states the parent action contract for deriving R_AB=0 and no reciprocal hair.",
        },
        {
            "source_id": "SRC1865_14_11_cell_current",
            "source_kind": "cell_current_origin_attempt",
            "source_path": ROOT / "11-cell-current-origin-attempt.md",
            "required_needle": "ordinary cell-current conservation does not close",
            "use_in_1865": "documents that conservation permits Q_R hair.",
        },
        {
            "source_id": "SRC1865_15_1859_route",
            "source_kind": "no_GR_import_route",
            "source_path": ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            "required_needle": "BEST_NONCIRCULAR_ROUTE",
            "use_in_1865": "keeps the MTS-owned field-equation difference as the least circular route.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source_entry in sources:
        source_path = source_entry["source_path"]
        needle = source_entry["required_needle"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_entry["source_id"],
                "source_kind": source_entry["source_kind"],
                "source_path": str(source_path),
                "path_exists": as_bool_text(source_path.exists()),
                "required_needle": needle,
                "needle_found": as_bool_text(path_has_needle(source_path, needle)),
                "use_in_1865": source_entry["use_in_1865"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def variable_orientation_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VOA1865_0_definitions",
            "object": "local logarithmic variables",
            "calculation": "x:=ln T, y:=ln sqrt(S), C_R:=ln(T^2 S)=2(x+y), v_cone:=ln(T/sqrt(S))=x-y.",
            "result": "DEFINITION_EXACT",
            "obstruction": "none_as_definition",
            "consequence": "C_R=0 exactly gives T sqrt(S)=1 and the reciprocal branch.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VOA1865_1_generic_Euler_difference",
            "object": "generic parent action slice",
            "calculation": "For S=int dr L(x,y,x',y',Phi), E_x-E_y=(partial_x-partial_y)L - d/dr[(partial_xprime-partial_yprime)L].",
            "result": "GENERIC_DIFFERENCE_NOT_DERIVED",
            "obstruction": "no generic identity makes this equal partial_r C_R - S_R",
            "consequence": "the D_R normal form requires a parent-signed reciprocity-selector kernel, not just any local action.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VOA1865_2_C_only_warning",
            "object": "C_R-only toy sector",
            "calculation": "A toy L(C_R,C_R') varies naturally with the C_R direction; depending on sign convention this may correspond to an Euler sum or a rotated constraint, not automatically to named E_time-E_radial.",
            "result": "ORIENTATION_CERTIFICATE_REQUIRED",
            "obstruction": "MISSING_EULER_ORIENTATION_AND_SIGN_CONVENTION",
            "consequence": "one must prove which parent variation combination actually selects C_R.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VOA1865_3_GR_import_guard",
            "object": "GR-style identity",
            "calculation": "In GR, a radial equation difference can yield a derivative of ln(T^2 S), but using that identity before deriving the local EH fixed point imports the result.",
            "result": "REFERENCE_ONLY_UNTIL_EH_FIXED_POINT_DERIVED",
            "obstruction": "MISSING_LOCAL_EH_PARENT_DERIVATION",
            "consequence": "D_R must be derived from MTS action/current variables or explicitly labelled a GR benchmark.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VOA1865_4_verdict",
            "object": "variable orientation route",
            "calculation": "The u/v split is clean, but the live parent action has not supplied the orientation that makes E_time-E_radial the C_R Euler/constraint equation.",
            "result": "VARIABLE_SPLIT_READY_OPERATOR_IDENTITY_MISSING",
            "obstruction": "MISSING_RECIPROCITY_SELECTOR_OR_PARENT_EULER_ORIENTATION",
            "consequence": "do not claim D_R normal form; build selector/operator proof or demote to source rows.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def dr_derivation_attempt() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_0_target",
            "target": "D_R[MTS] normal form",
            "equation_attempted": "D_R[MTS]:=E_time-E_radial = partial_r C_R - S_R[R_local^MTS,source,boundary,readout] = 0",
            "derivation_status": "TARGET_RESTATED",
            "missing_or_blocker": "needs explicit L_MTS_core and parent variation definitions",
            "outcome": "not a claim",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_1_parent_action_slice",
            "target": "S_parent^local",
            "equation_attempted": "S_parent^local=int dr L_MTS[x,y,Phi_extra,Psi,boundary]",
            "derivation_status": "NOT_AVAILABLE_IN_CURRENT_CORPUS",
            "missing_or_blocker": "MISSING_EXPLICIT_L_MTS_CORE_OR_H_CORE",
            "outcome": "cannot compute actual E_time/E_radial from first principles",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_2_generic_variation",
            "target": "generic Euler difference",
            "equation_attempted": "E_x-E_y=(partial_x-partial_y)L - d/dr[(partial_xprime-partial_yprime)L]",
            "derivation_status": "DERIVED_GENERIC_IDENTITY",
            "missing_or_blocker": "identity is too weak; it does not force partial_r C_R",
            "outcome": "GENERIC_EULER_DIFFERENCE_NO_GO_GUARD",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_3_first_order_selector",
            "target": "first-order reciprocal constraint/source law",
            "equation_attempted": "L_selector=lambda_R(partial_r C_R - S_R) or lambda_R C_R as a nonpropagating constraint",
            "derivation_status": "EXACT_IF_INSERTED",
            "missing_or_blocker": "MISSING_PARENT_ORIGIN_OF_lambda_R_AND_CONSTRAINT_CLASS",
            "outcome": "works as closure/auxiliary ansatz, not current derivation",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_4_second_order_current",
            "target": "current/no-hair reciprocal field",
            "equation_attempted": "partial_r(W_R partial_r C_R)=J_R, with W_R>0",
            "derivation_status": "CONDITIONAL_SOURCE_EQUATION",
            "missing_or_blocker": "MISSING_W_R_PARENT_DERIVATION;MISSING_J_R_SOURCE_MAP;MISSING_Q_R_ZERO_THEOREM",
            "outcome": "conservation alone leaves Q_R hair",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_5_SR_decomposition",
            "target": "S_R residual source side",
            "equation_attempted": "S_R := Sigma_i c_i R_i with R_i in R_local^MTS",
            "derivation_status": "SYMBOLIC_DECOMPOSITION_READY",
            "missing_or_blocker": "MISSING_COEFFICIENTS_UNITS_AND_PARENT_SOURCE_MAP",
            "outcome": "useful nonclaim decomposition, not a zero theorem",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DRA1865_6_verdict",
            "target": "D_R derivation",
            "equation_attempted": "derive D_R from MTS local parent action without EH import",
            "derivation_status": "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS",
            "missing_or_blocker": "MISSING_RECIPROCITY_SELECTOR_PARENT_KERNEL_OR_EXPLICIT_L_MTS_CORE",
            "outcome": "demote to S_R residual decomposition and target the selector/operator next",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def sr_residual_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_0_Delta_Hsrc",
            "sr_slot": "S_R_source_measure",
            "residual_symbol": "Delta_Hsrc",
            "symbolic_entry": "c_H Delta_Hsrc/M_H_ref",
            "meaning": "source-normalization mismatch between parent Hamiltonian charge and observed mass/source readout",
            "current_status": "CENTRAL_Y5_RESIDUAL_RETAINED",
            "missing_to_score": "MISSING_c_H;MISSING_COMMON_UNITS;MISSING_DELTA_HSRC_ZERO_OR_BOUND",
            "arena_links": "orbital;Gauss;PPN;Newton",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_1_I_X",
            "sr_slot": "S_R_current_curl",
            "residual_symbol": "I_X",
            "symbolic_entry": "c_I I_X/M_H_ref",
            "meaning": "first non-EH curl/source component in the parent current/integrability chain",
            "current_status": "NOT_THEOREM_ZERO",
            "missing_to_score": "MISSING_c_I;MISSING_PARENT_CURRENT_OWNER;MISSING_IX_BOUND",
            "arena_links": "orbital;PPN;source_normalization;local_GR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_2_J_X_qbarXT",
            "sr_slot": "S_R_matter_source",
            "residual_symbol": "J_X/qbar_XT",
            "symbolic_entry": "c_J J_X + c_q qbar_XT",
            "meaning": "ordinary and hidden matter source charge in the dangerous local residual direction",
            "current_status": "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            "missing_to_score": "MISSING_c_J;c_q;MISSING_QBAR_COMPONENT_VALUES;MISSING_MATTER_DESCENT",
            "arena_links": "R10;WEP;clock;PPN;orbital",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_3_constants",
            "sr_slot": "S_R_constant_composition",
            "residual_symbol": "b_alpha,b_mu,b_mA,b_nuc,b_clock_i",
            "symbolic_entry": "c_alpha b_alpha + c_mu b_mu + c_A b_mA + c_nuc b_nuc + Sigma_i c_clock_i b_clock_i",
            "meaning": "dimensionless EM/mass/nuclear/clock leakage into local source and readout",
            "current_status": "ALPHA_MASS_CLOCK_CHANNELS_RETAINED",
            "missing_to_score": "MISSING_COEFFICIENT_MATRIX;MISSING_NO_EXTRA_F2;MISSING_NO_MASS_VERTEX",
            "arena_links": "fine_structure;WEP;clock;R10",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_4_boundary_history",
            "sr_slot": "S_R_boundary_history",
            "residual_symbol": "J_boundary,J_history,qbar_nonH",
            "symbolic_entry": "c_B B_R + c_hist H_R + c_nonH qbar_nonH",
            "meaning": "edge charge, reference, support, domain, non-Hilbert and memory/history source tails",
            "current_status": "TAILS_NOT_ZERO_NOT_BOUNDED",
            "missing_to_score": "MISSING_BOUNDARY_CLASS;MISSING_HISTORY_KERNEL_BOUND;MISSING_NONHILBERT_BOUND",
            "arena_links": "orbital;source_normalization;R10;local_GR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_5_q_loc",
            "sr_slot": "S_R_extra_sector",
            "residual_symbol": "epsilon_GK_q_loc",
            "symbolic_entry": "c_GK epsilon_GK_q_loc",
            "meaning": "Gamma/Khat/q_loc extra-sector local force/source residual",
            "current_status": "RETAIN_NONCLAIM",
            "missing_to_score": "MISSING_c_GK;MISSING_GAMMA_KHAT_ACTION_PAIR;MISSING_OBSERVABLE_LOCK",
            "arena_links": "local_GR;PPN;clock;orbital;WEP;R10",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_6_reciprocal_hair",
            "sr_slot": "S_R_QR_hair",
            "residual_symbol": "Q_R,J_R",
            "symbolic_entry": "Q_R or int J_R dr after operator integration",
            "meaning": "integration charge/source imbalance in the reciprocal radial-cell equation",
            "current_status": "NO_CHARGE_THEOREM_NOT_DERIVED",
            "missing_to_score": "MISSING_QR_ZERO;MISSING_JR_SOURCE_MAP;MISSING_BOUNDARY_NO_CHARGE",
            "arena_links": "PPN_gamma;orbital;lightcone;local_GR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_7_readout",
            "sr_slot": "S_R_readout_projection",
            "residual_symbol": "C_R[A],projection/readout leakage",
            "symbolic_entry": "c_readout C_readout + c_proj Delta_Pi",
            "meaning": "post-variation readout/projection/calibration reentry into metric or source observables",
            "current_status": "PURE_POSTPROCESSING_SAFE_NOT_GENERAL",
            "missing_to_score": "MISSING_ARENA_DOMAIN_TYPING;MISSING_PROJECTION_COEFFICIENTS",
            "arena_links": "Pantheon;BAO;SPARC;R10;WEP;clock;PPN",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SRD1865_8_total",
            "sr_slot": "S_R_total_abs",
            "residual_symbol": "S_R[R_local^MTS]",
            "symbolic_entry": "|S_R| <= sum absolute values of SRD1865_0 through SRD1865_7",
            "meaning": "no-cancellation local reciprocal source envelope",
            "current_status": "SYMBOLIC_READY_VALUES_MISSING",
            "missing_to_score": "MISSING_ALL_COEFFICIENTS_COMMON_UNITS_ARENA_PROJECTIONS",
            "arena_links": "local_GR;PPN;orbital;R10;WEP;clock",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def missing_input_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "missing_id": "MIL1865_0_Lcore",
            "needed_input": "explicit local MTS parent action/Hamiltonian core",
            "why_needed": "without L_MTS_core or H_core, E_time and E_radial cannot be varied.",
            "current_status": "MISSING_EXPLICIT_L_MTS_CORE",
            "if_not_filled": "D_R normal form remains closure/contract only.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "missing_id": "MIL1865_1_orientation",
            "needed_input": "Euler orientation/sign certificate",
            "why_needed": "the parent variation combination that selects C_R must be proven, not guessed from GR.",
            "current_status": "MISSING_RECIPROCITY_SELECTOR_ORIENTATION",
            "if_not_filled": "E_time-E_radial could select the wrong variable combination.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "missing_id": "MIL1865_2_operator_kernel",
            "needed_input": "reciprocity-selector operator or W_R kernel",
            "why_needed": "D_R must contain partial_r C_R or partial_r(W_R partial_r C_R) with a parent-owned sign/order.",
            "current_status": "MISSING_OPERATOR_SIGN_AND_KERNEL",
            "if_not_filled": "no no-hair/local reciprocal theorem can be run.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "missing_id": "MIL1865_3_source_map",
            "needed_input": "S_R source/residual coefficient map",
            "why_needed": "all residuals must enter S_R with common units and no fitted-GM hiding.",
            "current_status": "MISSING_SR_COEFFICIENTS",
            "if_not_filled": "empirical comparison remains symbolic and nonclaim.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "missing_id": "MIL1865_4_no_charge",
            "needed_input": "Q_R=0 boundary/source neutrality theorem",
            "why_needed": "current conservation gives Q_R constant, not zero.",
            "current_status": "MISSING_QR_ZERO_THEOREM",
            "if_not_filled": "reciprocal hair remains an explicit local residual.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "missing_id": "MIL1865_5_constraint_origin",
            "needed_input": "parent origin of lambda_R C_R or equivalent auxiliary constraint",
            "why_needed": "a multiplier constraint gives C_R=0 exactly only if the multiplier is parent-forced and compatible with matter/boundary/readout.",
            "current_status": "MISSING_MULTIPLIER_ORIGIN_AND_DIRAC_CHAIN",
            "if_not_filled": "constraint route remains closure-only.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def no_gr_import_guard() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1865_0_forbidden_GR_difference",
            "forbidden_move": "use GR G^t_t-G^r_r=0 to derive partial_r ln(T^2 S)=0",
            "why_forbidden": "this imports the exact local theorem MTS is trying to earn.",
            "allowed_replacement": "derive E_time and E_radial from L_MTS_core or label GR identity as benchmark only.",
            "guard_pass": as_bool_text(True),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1865_1_forbidden_metric_ansatz",
            "forbidden_move": "impose T^2 S=1, AB=1, p=1, or C_R=0 as a plateau/coordinate choice",
            "why_forbidden": "it smuggles local GR into the branch before the parent action proves it.",
            "allowed_replacement": "use C_R=0 only as conditional consequence or nonclaim closure baseline.",
            "guard_pass": as_bool_text(True),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1865_2_forbidden_current_shortcut",
            "forbidden_move": "claim cell-current conservation proves Q_R=0",
            "why_forbidden": "conservation gives Q_R constant and permits reciprocal hair.",
            "allowed_replacement": "derive a no-charge theorem or keep Q_R/J_R as residuals.",
            "guard_pass": as_bool_text(True),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1865_3_forbidden_test_shortcut",
            "forbidden_move": "use PPN/orbital success or fitted GM to define the source-normalized local theorem",
            "why_forbidden": "tests compare the branch; they do not derive the parent source map.",
            "allowed_replacement": "source-bound residuals only after coefficients and arena projections exist.",
            "guard_pass": as_bool_text(True),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1865_0_DR_derived",
            "claim": "D_R[MTS]=partial_r C_R-S_R is derived",
            "status": "BLOCKED",
            "reason": "explicit L_MTS_core, Euler pair, orientation certificate and operator kernel are missing.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1865_1_SR_zero",
            "claim": "S_R=0 on the local branch",
            "status": "BLOCKED",
            "reason": "S_R is decomposed symbolically, but every live component lacks zero theorem or numeric coefficient rows.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1865_2_QR_zero",
            "claim": "reciprocal charge Q_R vanishes",
            "status": "BLOCKED",
            "reason": "cell-current conservation permits Q_R hair and no-charge theorem is not derived.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1865_3_local_GR_Newton",
            "claim": "MTS derives local GR/Newton",
            "status": "BLOCKED",
            "reason": "D_R normal form, S_R silence and Q_R boundary/no-charge remain missing.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1865_0_real_derivation_attempt",
            "decision": "GENERIC_EULER_DIFFERENCE_NO_GO_GUARD_ADDED",
            "reason": "a generic action variation gives E_x-E_y, but not automatically partial_r C_R; the reciprocity-selector operator must be parent-derived.",
            "next_action": "target the missing selector/orientation/kernel rather than claiming D_R.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1865_1_DR_status",
            "decision": "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "L_MTS_core/H_core, E_time/E_radial, source map, operator sign and no-charge conditions remain absent.",
            "next_action": "retain D_R as exact contract plus symbolic S_R decomposition.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1865_2_SR_status",
            "decision": "SR_RESIDUAL_DECOMPOSITION_READY_NONCLAIM",
            "reason": "all known local residuals have a slot in S_R, so future coupling/q_loc/boundary work cannot hide outside the local equation.",
            "next_action": "fill coefficients/units only after the selector/operator exists.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1865_3_next",
            "decision": "RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION_NEXT",
            "reason": "this is now the smallest missing object between the exact C_R theorem and a derivable local-GR branch.",
            "next_action": "build 1866 to derive the selector kernel from H_core/L_MTS_core or demote it to closure-only.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1865_0_primary",
            "next_target": "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
            "script": "scripts/Y5_R2FR_reciprocity_selector_operator_or_Hcore_source_equation_1866.py",
            "objective": "try to derive the parent reciprocity-selector orientation/kernel that makes the time/radial Euler combination select C_R; if unavailable, demote D_R to a closure-only benchmark and emit source-ready Z_R/J_R/S_R coefficient requirements.",
            "selection_status": "selected",
            "success_condition": "parent-owned L_MTS_core/H_core yields the C_R operator without GR import, or all missing selector/source/operator inputs become explicit nonclaim rows.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1865_1_parallel_current",
            "next_target": "1866b-Y5-R2FR-reciprocal-no-charge-boundary-theorem-or-QR-source-row.md",
            "script": "scripts/Y5_R2FR_reciprocal_no_charge_boundary_theorem_or_QR_source_row_1866b.py",
            "objective": "attempt Q_R=0 from boundary/source neutrality; if not, create finite Q_R/J_R source rows for PPN/orbital/lightcone comparison.",
            "selection_status": "held_parallel",
            "success_condition": "Q_R no-charge theorem or finite sourced reciprocal-hair residual rows.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1865_2_parallel_q_loc",
            "next_target": "1866c-Y5-R2FR-epsilon-GK-q-loc-to-SR-coefficient-map.md",
            "script": "scripts/Y5_R2FR_epsilon_GK_qloc_to_SR_coefficient_map_1866c.py",
            "objective": "map epsilon_GK_q_loc into S_R with a declared coefficient/unit convention or prove the q_loc source slot vanishes.",
            "selection_status": "held_parallel",
            "success_condition": "q_loc term is parent-zero or source-ready as an S_R component.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_fields = {"valid_for_claim", "claim_allowed", "gate_pass", "guard_pass"}
    for table_rows in rows_by_name.values():
        for table_row in table_rows:
            for field_name in guarded_fields:
                if field_name == "guard_pass":
                    continue
                if str(table_row.get(field_name, "")).strip().lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for table_rows in rows_by_name.values():
        for table_row in table_rows:
            row_text = " ".join(str(value) for value in table_row.values())
            if "MISSING_" in row_text:
                if str(table_row.get("valid_for_claim", "")).strip().lower() == "true":
                    return False
                if str(table_row.get("claim_allowed", "")).strip().lower() == "true":
                    return False
    return True


def csvs_parse(paths: list[Path]) -> bool:
    for csv_path in paths:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
    return True


def copy_branch_outputs(paths: list[Path]) -> None:
    for branch_folder in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
        branch_folder.mkdir(parents=True, exist_ok=True)
    for output_path in paths:
        shutil.copy2(output_path, MICROSCOPE_RESIDUALS / output_path.name)
        shutil.copy2(output_path, QUARANTINE / output_path.name)
        shutil.copy2(output_path, RAB_QUEUE / f"JR1865_{output_path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for output_path in paths:
        expected_paths = [
            MICROSCOPE_RESIDUALS / output_path.name,
            QUARANTINE / output_path.name,
            RAB_QUEUE / f"JR1865_{output_path.name}",
        ]
        if not all(expected_path.exists() for expected_path in expected_paths):
            return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1865*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    variable_rows = rows_by_name["variable_orientation_audit"]
    derivation_rows = rows_by_name["dr_derivation_attempt"]
    sr_rows = rows_by_name["sr_residual_decomposition"]
    missing_rows = rows_by_name["missing_input_ledger"]
    guard_rows = rows_by_name["no_gr_import_guard"]
    claim_rows = rows_by_name["claim_gate"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1865_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1865_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1865_2_variable_obstruction_recorded",
            "status": "PASS" if any(row["result"] == "GENERIC_DIFFERENCE_NOT_DERIVED" for row in variable_rows) else "FAIL",
            "detail": "generic Euler-difference no-go guard is recorded",
        },
        {
            "validation_id": "VAL1865_3_DR_not_promoted",
            "status": "PASS" if any(row["derivation_status"] == "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS" for row in derivation_rows) else "FAIL",
            "detail": "D_R normal form is not promoted as derived",
        },
        {
            "validation_id": "VAL1865_4_SR_decomposition_complete",
            "status": "PASS" if len(sr_rows) >= 9 and any(row["slot_id"] == "SRD1865_8_total" for row in sr_rows) else "FAIL",
            "detail": "S_R residual decomposition includes all current residual slots and total envelope",
        },
        {
            "validation_id": "VAL1865_5_missing_inputs_named",
            "status": "PASS" if any(row["current_status"] == "MISSING_EXPLICIT_L_MTS_CORE" for row in missing_rows) else "FAIL",
            "detail": "explicit local parent action/Hcore missing input is named",
        },
        {
            "validation_id": "VAL1865_6_no_GR_import_guard_active",
            "status": "PASS" if all(row["guard_pass"] == "True" for row in guard_rows) else "FAIL",
            "detail": "no-GR-import guard rows are active",
        },
        {
            "validation_id": "VAL1865_7_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_rows) else "FAIL",
            "detail": "all local-GR/D_R/S_R/Q_R claim gates remain blocked",
        },
        {
            "validation_id": "VAL1865_8_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1865_9_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked claim-ready",
        },
        {
            "validation_id": "VAL1865_10_decision_next",
            "status": "PASS" if any(row["decision"] == "RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION_NEXT" for row in decision_rows) else "FAIL",
            "detail": "decision ledger selects reciprocity selector/Hcore source equation next",
        },
        {
            "validation_id": "VAL1865_11_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1865_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1865_12_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1865_13_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1865_14_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1865_15_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1865 outputs found under formalization-workbench",
        },
    ]
    overall_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1865_OVERALL",
            "status": overall_status,
            "detail": "1865 parent Euler difference normal form or S_R residual decomposition checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1865 - Y5/R2FR Parent Euler Difference Normal Form Or S_R Residual Decomposition",
        "",
        "## Verdict",
        "",
        "1865 makes the first real attempt at the `D_R` derivation and finds the important obstruction. A generic parent action does not automatically make `E_time-E_radial` equal `partial_r C_R-S_R`. With `x=ln T`, `y=ln sqrt(S)`, and `C_R=2(x+y)`, the raw generic identity is `E_x-E_y=(partial_x-partial_y)L-d/dr[(partial_xprime-partial_yprime)L]`; that is not the desired `C_R` operator unless the parent action supplies a reciprocity-selector orientation/kernel.",
        "",
        "So the current branch has not derived local GR/Newton. But the result is not empty: it tells us exactly what is missing. We need either a parent-owned first-order constraint/selector, a second-order positive reciprocal operator with a no-charge theorem, or an explicit `L_MTS_core/H_core` whose Euler pair really produces the `C_R` normal form. Until then, `D_R` is an exact contract and `S_R[R_local^MTS]` is a nonclaim residual decomposition.",
        "",
        "**Claim ceiling:** no `D_R` derivation claim, no `S_R=0` claim, no `Q_R=0` claim, no local-GR/Newton reduction claim, no R10/WEP/PPN/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1865.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1865", "valid_for_claim"],
        ),
        "",
        "## Variable Orientation Audit",
        "",
        markdown_table(
            rows_by_name["variable_orientation_audit"],
            ["audit_id", "object", "calculation", "result", "obstruction", "consequence", "valid_for_claim"],
        ),
        "",
        "## D_R Derivation Attempt",
        "",
        markdown_table(
            rows_by_name["dr_derivation_attempt"],
            ["attempt_id", "target", "equation_attempted", "derivation_status", "missing_or_blocker", "outcome", "valid_for_claim"],
        ),
        "",
        "## S_R Residual Decomposition",
        "",
        markdown_table(
            rows_by_name["sr_residual_decomposition"],
            ["slot_id", "sr_slot", "residual_symbol", "symbolic_entry", "meaning", "current_status", "missing_to_score", "arena_links", "valid_for_claim"],
        ),
        "",
        "## Missing Input Ledger",
        "",
        markdown_table(
            rows_by_name["missing_input_ledger"],
            ["missing_id", "needed_input", "why_needed", "current_status", "if_not_filled", "valid_for_claim"],
        ),
        "",
        "## No-GR-Import Guard",
        "",
        markdown_table(
            rows_by_name["no_gr_import_guard"],
            ["guard_id", "forbidden_move", "why_forbidden", "allowed_replacement", "guard_pass", "valid_for_claim"],
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
        "This is good hard progress. We tried the derivation and found the exact missing gear: not 'coupling' in the fog, but the reciprocity-selector operator or parent `H_core/L_MTS_core` that makes the radial/time Euler combination select `C_R`. If 1866 can derive that selector, the route to GR/Newton gets much more serious. If it cannot, the local branch is not dead, but it becomes an explicit closure/residual branch that must fight the data with sourced coefficients.",
    ]
    DOC_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "variable_orientation_audit": variable_orientation_audit(),
        "dr_derivation_attempt": dr_derivation_attempt(),
        "sr_residual_decomposition": sr_residual_decomposition(),
        "missing_input_ledger": missing_input_ledger(),
        "no_gr_import_guard": no_gr_import_guard(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }

    non_validation_paths = [output_path for output_name, output_path in OUTPUTS.items() if output_name != "validation"]
    for output_name, output_path in OUTPUTS.items():
        if output_name != "validation":
            write_csv(output_path, rows_by_name[output_name])

    copy_branch_outputs(non_validation_paths)
    remove_pycache()

    rows_by_name["validation"] = validation_rows(rows_by_name, non_validation_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    copy_branch_outputs([OUTPUTS["validation"]])
    remove_pycache()

    if any(row["status"] == "FAIL" for row in rows_by_name["validation"]):
        raise SystemExit("1865 validation failed")

    print(f"Wrote {DOC_PATH}")
    for output_path in OUTPUTS.values():
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
