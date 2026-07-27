from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
SOURCE_WEIGHT_DOCS = SOURCE_WEIGHT / "docs"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2971"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2971-Y5-R2FR-first-DqZ-JA-leakage-coefficient-acquisition-or-theorem-zero-under-AX1090.md"

SRC_2970_DOC = ROOT / "2970-Y5-R2FR-parent-quotient-map-and-basic-matter-action-signature-or-DqZ-JA-coefficient-row-under-AX1090.md"
SRC_2970_NEXT = RESIDUALS / "P8_Y5_R2FR_2970_NEXT_TARGET.csv"
SRC_2970_COEFF = RESIDUALS / "P8_Y5_R2FR_2970_FIRST_LEAKAGE_COEFFICIENT_ROWS_NONCLAIM.csv"
SRC_2970_SIGNATURE = RESIDUALS / "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv"
SRC_2970_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2970_VALIDATION.csv"

SRC_2884_DQZ_FACTOR = SOURCE_WEIGHT / "RAB_FIRST_DQZ_FACTOR_SOURCE_ROW_2884_NONCLAIM.csv"
SRC_2882_FILL = SOURCE_WEIGHT / "RAB_DQ_LEAK_FILL_ATTEMPT_2882_NONCLAIM.csv"
SRC_2885_BLOCKER = SOURCE_WEIGHT / "RAB_DQZ_ZERO_OR_FACTOR_BLOCKER_LEDGER_2885_NONCLAIM.csv"
SRC_2886_REQUIREMENTS = SOURCE_WEIGHT / "RAB_DQZ_COMPONENT_INPUT_REQUIREMENTS_2886_NONCLAIM.csv"
SRC_2887_COBS = SOURCE_WEIGHT / "RAB_COBS_OPERATOR_NORM_ROW_2887_NONCLAIM.csv"
SRC_2888_CSHADOW = SOURCE_WEIGHT / "RAB_CSHADOW_BOUND_ROW_2888_NONCLAIM.csv"
SRC_2892_NEUTRAL = SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv"
SRC_2893_NO_SOURCE = SOURCE_WEIGHT / "RAB_BETA_SOURCE_NO_SOURCE_SLOT_UPDATE_2893_NONCLAIM.csv"
SRC_2158_JX = SOURCE_WEIGHT_DOCS / "AFRAME_JX_QBARXT_2158_NONCLAIM.csv"
SRC_2911_QMAP = PARENT_ACTION / "Parent_qmap_kernel_attempt_2911_NONCLAIM.csv"
SRC_2913_AUX = PARENT_ACTION / "Parent_auxiliary_constraint_origin_2913_NONCLAIM.csv"
SRC_2914_COBS = PARENT_ACTION / "Cobs_no_shadow_head_audit_2914_NONCLAIM.csv"
SRC_2915_SHADOW = PARENT_ACTION / "Cshadow_zero_theorem_attempt_2915_NONCLAIM.csv"
SRC_2927_TRANSFER = PARENT_ACTION / "AX1090_Cshadow_alpha3_transfer_gate_2927_NONCLAIM.csv"
SRC_2956_DESCENT = PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"
SRC_1671_DQZ_INPUTS = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv"
SRC_1672_ZLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv"
SRC_1674_DQZ_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
SRC_1667_DQ_LEAKS = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"
SRC_1541_DQVM = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv"
SRC_2488_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2572_SHADOW = RESIDUALS / "P8_Y5_NO_SHADOW_2572_COUPLING_SHADOW_AUDIT.csv"
SRC_2721_FINITE = RESIDUALS / "P8_Y5_R2FR_2721_FINITE_ENORM_ESHADOW_ROWS_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2971_SOURCE_REGISTER.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2971_COEFFICIENT_ACQUISITION_AUDIT.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2971_THEOREM_ZERO_ATTEMPT.csv",
    "split": RESIDUALS / "P8_Y5_R2FR_2971_SUBCOEFFICIENT_SPLIT_ROWS_NONCLAIM.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2971_NO_CANCELLATION_ENVELOPE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2971_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2971_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2971_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2971_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2971_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "acquisition_copy": PARENT_ACTION / "first_DqZ_JA_leakage_coefficient_acquisition_2971_NOT_DERIVED.csv",
    "split_copy": LOCAL_BOUNDS / "DqZ_JA_subcoefficient_split_2971_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2971_DqZ_component_matrix_Z_basis_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2971_00_2970_doc", SRC_2970_DOC, "Fallback now exists;NEXT2970_0_2971", "2970 handoff"),
        ("SRC2971_01_2970_next", SRC_2970_NEXT, "NEXT2970_0_2971", "machine-readable 2971 target"),
        ("SRC2971_02_2970_coeff", SRC_2970_COEFF, "COEF2970_0_eps_q_parent;COEF2970_5_J_spurion;COEF2970_9_total", "first coefficient rows"),
        ("SRC2971_03_2970_signature", SRC_2970_SIGNATURE, "SIG2970_8_verdict", "parent signature failure"),
        ("SRC2971_04_2970_validation", SRC_2970_VALIDATION, "VAL2970_OVERALL", "2970 validation"),
        ("SRC2971_05_2884_dqz_factor", SRC_2884_DQZ_FACTOR, "DQZ2884_0_first_factor_row", "first DqZ factor template"),
        ("SRC2971_06_2882_fill", SRC_2882_FILL, "FILL2882_0_Dq_vertical_leak;FILL2882_3_J_vertical_physical", "Dq leak fill attempt"),
        ("SRC2971_07_2885_blocker", SRC_2885_BLOCKER, "DQZF2885_0_Dq_Z_norm;DQZF2885_3_direct_tail_sum", "DqZ blocker ledger"),
        ("SRC2971_08_2886_requirements", SRC_2886_REQUIREMENTS, "REQ2886_2_DqZ;REQ2886_5_direct_tails", "DqZ component input requirements"),
        ("SRC2971_09_2887_cobs", SRC_2887_COBS, "COBS2887_0_operator_norm;COBS2887_2_shadow_frame_guard", "CObs operator row"),
        ("SRC2971_10_2888_cshadow", SRC_2888_CSHADOW, "CSH2888_0_C_shadow_abs;CSH2888_2_d_R_disformal", "Cshadow bound row"),
        ("SRC2971_11_2892_neutral", SRC_2892_NEUTRAL, "PAS2892_1_quotient_action;PAS2892_5_result", "source neutrality schema"),
        ("SRC2971_12_2893_no_source", SRC_2893_NO_SOURCE, "BZ2893_3_no_source_only_slot;BZ2893_6_verdict", "no source-only slot gate"),
        ("SRC2971_13_2158_jx", SRC_2158_JX, "SZI2158_2_zero_theorem;JQD2158_3_source_weight;JQD2158_4_nonHilbert", "J/qbar component split"),
        ("SRC2971_14_2911_qmap", SRC_2911_QMAP, "QMAP2911_6_operator_norm;QMAP2911_7_verdict", "qmap kernel attempt"),
        ("SRC2971_15_2913_aux", SRC_2913_AUX, "PAO2913_1_action_image;PAO2913_6_verdict", "auxiliary constraint origin"),
        ("SRC2971_16_2914_cobs", SRC_2914_COBS, "COBS2914_1_projection_value;COBS2914_5_verdict", "conditional CObs normalization"),
        ("SRC2971_17_2915_shadow", SRC_2915_SHADOW, "ZTH2915_0_exact_conditional;ZTH2915_6_verdict", "Cshadow zero theorem attempt"),
        ("SRC2971_18_2927_transfer", SRC_2927_TRANSFER, "TR2927_2_transfer_map;TR2927_5_verdict", "alpha3-to-shadow transfer blocker"),
        ("SRC2971_19_2956_descent", SRC_2956_DESCENT, "DESC2956_0_chain_rule;DESC2956_7_verdict", "matter descent audit"),
        ("SRC2971_20_2676_owner", SRC_2676_OWNER, "OWN2676_2_hilbert_current_sublemma;OWN2676_4_verdict", "current owner audit"),
        ("SRC2971_21_2677_grammar", SRC_2677_GRAMMAR, "GRM2677_3_species_blind_measure;GRM2677_6_verdict", "species grammar audit"),
        ("SRC2971_22_1671_dqz_inputs", SRC_1671_DQZ_INPUTS, "DQZ1671_0_basis;DQZ1671_2_derivative", "DqZ factor inputs"),
        ("SRC2971_23_1672_zlock", SRC_1672_ZLOCK, "LOCK1672_0_q_loc;LOCK1672_3_PPN", "Z-to-physical lock map"),
        ("SRC2971_24_1674_dqz_matrix", SRC_1674_DQZ_MATRIX, "DQM1674_0_coframe_metric;DQM1674_4_residual_lock", "DqZ derivative matrix"),
        ("SRC2971_25_1667_leaks", SRC_1667_DQ_LEAKS, "DQL1667_0_Dq_Z;DQL1667_4_Dsource_readout", "retained Dq leak rows"),
        ("SRC2971_26_1541_dqvm", SRC_1541_DQVM, "DQC1541_0_C_qm_definition;DQC1541_4_Scg_envelope", "finite coupling row"),
        ("SRC2971_27_2488_zero", SRC_2488_ZERO, "ZTH2488_0_exact_conditional;ZTH2488_2_current_verdict", "no-shadow theorem"),
        ("SRC2971_28_2488_counter", SRC_2488_COUNTER, "CM2488_0_common_weyl;CM2488_3_endpoint_boundary", "no-shadow countermodels"),
        ("SRC2971_29_2572_shadow", SRC_2572_SHADOW, "CS2572_0_kappa_MTS;CS2572_4_no_absorption_guard", "coupling shadow audit"),
        ("SRC2971_30_2721_finite", SRC_2721_FINITE, "FSN2721_0_E_norm_kappa;FSN2721_4_E_norm_absorption", "finite shadow norm rows"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2971_0_eps_q_parent", "eps_q_parent", "NO_SOURCE_BACKED_BOUND", "split into q declaration, parent chart, readout order and q/Z norm subheads", SRC_2911_QMAP),
        ("ACQ2971_1_eps_constraint", "eps_constraint", "NO_SOURCE_BACKED_BOUND", "split into auxiliary sort, action image, compatibility map, variation order and units/rank subheads", SRC_2913_AUX),
        ("ACQ2971_2_eps_factorization", "eps_factorization", "NO_SOURCE_BACKED_BOUND", "split into Q_vis constructor, qbar pullback, no hidden representative label and component matrix subheads", SRC_2911_QMAP),
        ("ACQ2971_3_eps_theta_basic", "eps_theta_basic", "NO_SOURCE_BACKED_BOUND", "split into Obs_e, theta, dmu, connection and endpoint basicness subheads", SRC_2886_REQUIREMENTS),
        ("ACQ2971_4_J_direct", "J_direct", "NO_SOURCE_BACKED_BOUND", "split into direct Z vertex, endpoint Z vertex, source prefactor and matter-domain escape subheads", SRC_2892_NEUTRAL),
        ("ACQ2971_5_J_spurion", "J_spurion", "NO_SOURCE_BACKED_BOUND", "split into species action weight, measure Jacobian, marker/source label return and post-quotient spurion subheads", SRC_2677_GRAMMAR),
        ("ACQ2971_6_J_nonH", "J_nonH", "NO_SOURCE_BACKED_BOUND", "split into non-Hilbert current, torsion/connection current, worldtube support and domain current subheads", SRC_2158_JX),
        ("ACQ2971_7_C_Obs_e", "C_Obs_e", "CONDITIONAL_NORMALIZATION_ONLY", "C_Obs_e=1 exists only if Obs_e is a q-coordinate and norms are parent signed; keep as nonclaim subrow", SRC_2914_COBS),
        ("ACQ2971_8_C_shadow_abs", "C_shadow_abs", "NO_SOURCE_BACKED_BOUND", "split into b_R, d_R, w_R, endpoint, coupling shadow and readout shadow heads", SRC_2888_CSHADOW),
        ("ACQ2971_9_total", "DqZ_JA_first_leakage_total", "NO_TOTAL_BOUND", "absolute envelope only; no cancellation or fitted-baseline absorption", SRC_2970_COEFF),
    ]
    return [
        add_common(
            {
                "acquisition_id": acquisition_id,
                "symbol": symbol,
                "current_status": status,
                "acquisition_result": result,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for acquisition_id, symbol, status, result, path in rows
    ]


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("TZ2971_0_DqZ", "Dq_Z_norm=0", "parent q, Z basis, Dq matrix, source/readout/boundary silence and q/Z norms all close", "NOT_DERIVED", "2884/2885/2911 keep Dq_Z as MISSING_NUMERIC_OR_THEOREM_ZERO", SRC_2885_BLOCKER),
        ("TZ2971_1_J_bulk", "J_direct=J_spurion=J_nonH=0", "ordinary matter descends, no direct source slot, species-blind measure and Hilbert current ownership all close", "NOT_DERIVED", "2158/2676/2677/2892 keep source-current heads open", SRC_2158_JX),
        ("TZ2971_2_CObs", "C_Obs_e fixed", "Obs_e is parent-owned q-coordinate with declared q/e norms", "CONDITIONAL_VALUE_ONLY", "COBS2914_1 gives candidate C_Obs_e=1 but parent ownership/norms are unsigned", SRC_2914_COBS),
        ("TZ2971_3_Cshadow", "C_shadow_abs=0", "terminal public coframe, no shadow slots and support/readout closure all close", "NOT_DERIVED", "2915/2488 keep no-shadow theorem conditional with countermodels", SRC_2915_SHADOW),
        ("TZ2971_4_transfer", "external alpha3 comparator bounds C_shadow_abs", "alpha3-to-geometry transfer map is parent signed and units locked", "TRANSFER_FAILS", "2927 says comparator exists but transfer map/head values are missing", SRC_2927_TRANSFER),
        ("TZ2971_5_verdict", "2971 coefficient theorem-zero package", "all first leakage heads are zero or source-backed finite", "NOT_DERIVED_SPLIT_REQUIRED", "no first coefficient can be promoted in current corpus", SRC_2970_COEFF),
    ]
    return [
        add_common(
            {
                "theorem_attempt_id": attempt_id,
                "target": target,
                "would_need": need,
                "current_status": status,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "accepted_for_scoring": False,
            }
        )
        for attempt_id, target, need, status, blocker, path in rows
    ]


def split_rows() -> list[dict[str, Any]]:
    raw_rows = [
        ("eps_q_parent", "eps_q_declaration", "q projection declared but not parent-owned", "dimensionless", "QMAP2911_0_projection_form", SRC_2911_QMAP),
        ("eps_q_parent", "eps_parent_chart", "Conf_parent chart/action object owner missing", "dimensionless", "SIG2970_0_parent_object", SRC_2970_SIGNATURE),
        ("eps_q_parent", "eps_readout_order", "q/readout order not proven pre-variation", "dimensionless", "AX1090_0_LC_3", SRC_2711_CLOSURE if "SRC_2711_CLOSURE" in globals() else SRC_2970_SIGNATURE),
        ("eps_constraint", "eps_aux_sort", "Z/Lambda auxiliary sort not parent-signed", "dimensionless", "PAO2913_0_parent_sort", SRC_2913_AUX),
        ("eps_constraint", "eps_action_image", "S_Z action image missing", "dimensionless", "PAO2913_1_action_image", SRC_2913_AUX),
        ("eps_constraint", "eps_compatibility_map", "C^A[Q_vis,theta,top] public-basic map missing", "dimensionless", "PAO2913_2_compatibility_map", SRC_2913_AUX),
        ("eps_constraint", "eps_units_rank", "Lambda/Z/C units and rank/null projector missing", "dimensionless", "PAO2913_3_multiplier_units_rank", SRC_2913_AUX),
        ("eps_factorization", "eps_Qvis_constructor", "Q_vis constructor not signed", "dimensionless", "QMAP2911_0_projection_form", SRC_2911_QMAP),
        ("eps_factorization", "eps_qbar_pullback", "q|C_Z=qbar(Q_vis) not certified", "dimensionless", "DQZ1671_3_zero_candidate", SRC_1671_DQZ_INPUTS),
        ("eps_factorization", "eps_component_matrix", "Dq component derivative matrix rows not numeric/theorem-zero", "dimensionless", "DQM1674_4_residual_lock", SRC_1674_DQZ_MATRIX),
        ("eps_theta_basic", "eps_Obs_e", "observed coframe functor missing", "dimensionless", "REQ2886_0_Obs_e", SRC_2886_REQUIREMENTS),
        ("eps_theta_basic", "eps_measure_basic", "measure/volume basicness under v_Z missing", "geometry_norm", "QMAP2911_1_Dq_geometry", SRC_2911_QMAP),
        ("eps_theta_basic", "eps_connection_basic", "connection/covariant derivative basicness missing", "geometry_norm", "COBS2887_0_operator_norm", SRC_2887_COBS),
        ("eps_theta_basic", "eps_endpoint_basic", "endpoint/boundary inherited frame missing", "dimensionless", "CSH2888_0_C_shadow_abs", SRC_2888_CSHADOW),
        ("J_direct", "J_Z_vertex", "direct Z/source vertex in matter action", "source_normalized", "PAS2892_1_quotient_action", SRC_2892_NEUTRAL),
        ("J_direct", "J_source_prefactor", "source-only kappa/w prefactor", "source_normalized", "BZ2893_3_no_source_only_slot", SRC_2893_NO_SOURCE),
        ("J_direct", "J_endpoint_Z", "endpoint/worldtube direct term", "source_normalized", "JQD2158_6_readout", SRC_2158_JX),
        ("J_spurion", "J_species_weight", "w_A or hbar_A action-density weight", "source_normalized", "GRM2677_0_single_action_density_line", SRC_2677_GRAMMAR),
        ("J_spurion", "J_measure_jacobian", "species measure Jacobian", "source_normalized", "GRM2677_3_species_blind_measure", SRC_2677_GRAMMAR),
        ("J_spurion", "J_marker_return", "material/source/preparation label returns after quotienting", "source_normalized", "JQD2158_2_marker", SRC_2158_JX),
        ("J_spurion", "J_source_label_return", "source functor reintroduces species/source labels", "source_normalized", "GRM2677_4_source_label_forgetting", SRC_2677_GRAMMAR),
        ("J_nonH", "J_nonHilbert_current", "non-Hilbert source current", "source_normalized", "JQD2158_4_nonHilbert", SRC_2158_JX),
        ("J_nonH", "J_torsion_connection", "torsion/connection current", "source_normalized", "JQD2158_4_nonHilbert", SRC_2158_JX),
        ("J_nonH", "J_support_worldtube", "support/worldtube shift", "source_normalized", "OWN2676_4_verdict", SRC_2676_OWNER),
        ("J_nonH", "J_domain_current", "domain/current bypass", "source_normalized", "FILL2882_3_J_vertical_physical", SRC_2882_FILL),
        ("C_Obs_e", "C_Obs_operator_norm", "||DObs_e||_{q->e}", "dimensionless", "COBS2887_0_operator_norm", SRC_2887_COBS),
        ("C_Obs_e", "C_Obs_annihilator", "DObs_e restricted to im(Dq[v_Z])", "dimensionless", "COBS2887_1_annihilator", SRC_2887_COBS),
        ("C_Obs_e", "C_Obs_coordinate_norm", "conditional C_Obs_e=1 coordinate normalization", "dimensionless", "COBS2914_1_projection_value", SRC_2914_COBS),
        ("C_shadow_abs", "b_R_common_weyl", "common Weyl shadow coefficient", "dimensionless", "CSH2888_1_b_R_common_weyl", SRC_2888_CSHADOW),
        ("C_shadow_abs", "d_R_disformal", "common disformal/preferred-frame shadow coefficient", "dimensionless", "CSH2888_2_d_R_disformal", SRC_2888_CSHADOW),
        ("C_shadow_abs", "w_R_source_prefactor", "source-prefactor shadow coefficient", "dimensionless", "CM2488_2_source_prefactor", SRC_2488_COUNTER),
        ("C_shadow_abs", "epsilon_endpoint_R", "endpoint/boundary shadow", "dimensionless", "CM2488_3_endpoint_boundary", SRC_2488_COUNTER),
        ("C_shadow_abs", "epsilon_coupling_shadow", "kappa/ellJ/constant/source-mass coupling shadow", "dimensionless", "CS2572_0_kappa_MTS", SRC_2572_SHADOW),
        ("C_shadow_abs", "epsilon_readout_shadow", "readout/calibration shadow", "dimensionless", "FSN2721_4_E_norm_absorption", SRC_2721_FINITE),
    ]
    rows: list[dict[str, Any]] = []
    for parent, symbol, definition, units, source_anchor, path in raw_rows:
        rows.append(
            add_common(
                {
                    "split_id": f"SPL2971_{len(rows):02d}_{symbol}",
                    "parent_coefficient": parent,
                    "subcoefficient": symbol,
                    "definition": definition,
                    "units": units,
                    "candidate_value": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                    "lower_bound": 0,
                    "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                    "source_anchor": source_anchor,
                    "source_path": str(path),
                    "source_path_exists": path.exists(),
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                    "no_cancellation_policy": True,
                }
            )
        )
    return rows


def envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2971_0_DqZ", "Dq_Z_norm", "Dq_Z_norm <= eps_q_parent + eps_constraint + eps_factorization + eps_theta_basic + E_direct_Z", "all subheads source-backed or theorem-zero", SRC_2885_BLOCKER),
        ("ENV2971_1_JA", "J_A_bulk", "|J_A| <= C_matter*Dq_Z_norm + |J_direct| + |J_spurion| + |J_nonH| + boundary/projector tails", "C_matter, Dq_Z_norm and all J subheads source-backed", SRC_2158_JX),
        ("ENV2971_2_readout", "DqZ_readout", "DqZ_readout <= C_Obs_e*Dq_Z_norm*N_Z + C_shadow_abs + endpoint/readout tails", "C_Obs_e, N_Z, C_shadow_abs and endpoint/readout rows source-backed", SRC_2887_COBS),
        ("ENV2971_3_total", "first_leakage_total_abs", "sum of all listed subcoefficients with no cancellation, no fitted-GM absorption and no post-readout deletion", "every head numeric/theorem-zero", SRC_2970_COEFF),
    ]
    return [
        add_common(
            {
                "envelope_id": envelope_id,
                "quantity": quantity,
                "formula": formula,
                "promotion_requirement": requirement,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "numeric_bound_present": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for envelope_id, quantity, formula, requirement, path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2971_0_first_coefficients", "first leakage coefficients sourced or theorem-zero", False, "NO_FIRST_COEFFICIENT_PROMOTED"),
        ("CG2971_1_subcoefficients", "all subcoefficients have source-backed upper bounds", False, "SUBCOEFFICIENT_VALUES_MISSING"),
        ("CG2971_2_DqZ", "Dq_Z_norm score-ready", False, "DqZ_FACTOR_VALUES_MISSING"),
        ("CG2971_3_JA", "J_A source-current score-ready", False, "J_HEAD_VALUES_MISSING"),
        ("CG2971_4_Cshadow", "C_shadow_abs bounded or zero", False, "SHADOW_HEAD_VALUES_MISSING"),
        ("CG2971_5_local_GR", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2971_0_no_promotion", "no first coefficient is promoted", "all candidate values remain missing or conditional only", "keep Dq_Z/J_A nonclaim"),
        ("DEC2971_1_split", "split into source-ready subcoefficients", "the large coefficients are too coarse to fill directly", "use subcoefficient acquisition next"),
        ("DEC2971_2_next", "DqZ component matrix and Z-basis normalization are the best next target", "eps_q_parent/eps_factorization feed the whole Dq_Z stack and have existing 1671/1674 files", "build 2972 around DqZ matrix and N_Z"),
        ("DEC2971_3_claims", "no local-GR, R10, PPN, clock, WEP or orbital claim", "2971 is a ledger refinement only", "private nonclaim checkpoint"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2971_0_2972",
                "priority": "selected_primary",
                "next_doc": "2972-Y5-R2FR-DqZ-component-matrix-and-Z-basis-normalization-or-first-epsq-subrow-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_DqZ_component_matrix_and_Z_basis_normalization_or_first_epsq_subrow_under_AX1090_2972.py",
                "objective": "Try to source the DqZ component derivative matrix, selected Z basis, q/Z norm convention and N_Z normalization from the 1671/1674 rows; if not, emit first eps_q subrows with exact missing inputs.",
                "include": "Z_basis;N_Z;Dq_Z_norm;Dq component matrix;coframe/source/readout/boundary/residual-lock rows;q norm;Z norm;source-backed upper bounds;no-cancellation envelope",
                "exclude": "boundary no-flux proof;CDB closure;M_AB signature proof;arena scoring;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("acquisition_copy", OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"]),
        ("split_copy", OUTPUTS["split"], BRANCH_OUTPUTS["split_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    required_parents = {"eps_q_parent", "eps_constraint", "eps_factorization", "eps_theta_basic", "J_direct", "J_spurion", "J_nonH", "C_Obs_e", "C_shadow_abs"}
    split_parents = {row["parent_coefficient"] for row in all_rows["split"]}
    checks = [
        ("VAL2971_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2971_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2971_2_no_coeff_promoted", all(row["finite_value_present"] is False and row["theorem_zero_adopted"] is False and row["accepted_for_scoring"] is False for row in all_rows["acquisition"]), "no first coefficient promoted", True),
        ("VAL2971_3_theorem_not_adopted", all(row["theorem_zero_adopted"] is False and row["accepted_for_scoring"] is False for row in all_rows["theorem"]), "theorem-zero attempts remain nonclaim", True),
        ("VAL2971_4_split_covers_required", required_parents.issubset(split_parents), "subcoefficient split covers required first coefficients", True),
        ("VAL2971_5_split_nonclaim", all(row["finite_value_present"] is False and row["prediction_source_backed"] is False and row["valid_for_claim"] is False for row in all_rows["split"]), "subcoefficient rows remain nonclaim", True),
        ("VAL2971_6_envelope_nonclaim", all(row["numeric_bound_present"] is False and row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["envelope"]), "envelope rows remain nonclaim", True),
        ("VAL2971_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2971_8_next_target_written", any(row["next_id"] == "NEXT2971_0_2972" for row in all_rows["next"]), "2972 DqZ matrix/Z-basis next target selected", True),
        ("VAL2971_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2971_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2971_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2971_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2971 outputs were written to formalization-workbench", True),
        ("VAL2971_13_doc_written", DOC.exists(), "2971 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2971_OVERALL", "passed": overall, "check": "2971 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2971 - Y5 R2FR: first DqZ/JA leakage coefficient acquisition or theorem-zero under AX1090

Status: `Y5_R2FR_2971_no_first_leakage_coefficient_promoted_subcoefficient_split_written_nonclaim`

Claim ceiling: `no_DqZ_zero_no_JA_zero_no_coefficient_score_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

2971 tried to source or theorem-zero the first leakage coefficient heads from 2970.

- Result: no first coefficient is source-backed or theorem-zero in the current corpus.
- `C_Obs_e=1` exists only as a conditional coordinate normalization; it is not parent-signed and cannot be scored.
- The useful output is the subcoefficient split: each large head is now broken into smaller source-ready targets with no-cancellation policy.
- Next best move is upstream: source the `Dq_Z` component matrix, selected `Z_basis`, q/Z norm convention and `N_Z` normalization from the 1671/1674 rows.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Coefficient Acquisition Audit

{md_table(all_rows["acquisition"], ["acquisition_id", "symbol", "current_status", "acquisition_result", "finite_value_present", "accepted_for_scoring"])}

## Theorem-Zero Attempt

{md_table(all_rows["theorem"], ["theorem_attempt_id", "target", "current_status", "blocking_gap", "theorem_zero_adopted"])}

## Subcoefficient Split Rows

{md_table(all_rows["split"], ["split_id", "parent_coefficient", "subcoefficient", "definition", "candidate_value", "accepted_for_scoring"])}

## No-Cancellation Envelope

{md_table(all_rows["envelope"], ["envelope_id", "quantity", "formula", "promotion_requirement", "numeric_bound_present"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "acquisition": acquisition_rows(),
        "theorem": theorem_rows(),
        "split": split_rows(),
        "envelope": envelope_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2971 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
