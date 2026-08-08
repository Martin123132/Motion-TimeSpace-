from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3010"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3010-Y5-R2FR-first-Gamma-Khat-response-operator-row-or-q_loc-coupling-bound-interface-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3010_SOURCE_REGISTER.csv",
    "operator_attempt": RESIDUALS / "P8_Y5_R2FR_3010_RESPONSE_OPERATOR_ROW_ATTEMPT.csv",
    "live_gate": RESIDUALS / "P8_Y5_R2FR_3010_LIVE_RESPONSE_COMPONENT_GATE.csv",
    "bound_interface": RESIDUALS / "P8_Y5_R2FR_3010_QLOC_COUPLING_BOUND_INTERFACE.csv",
    "arena_acquisition": RESIDUALS / "P8_Y5_R2FR_3010_LOCAL_ARENA_ACQUISITION_MATRIX.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3010_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3010_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3010_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3010_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3010_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "operator_attempt_copy": PARENT_ACTION / "first_Gamma_Khat_response_operator_row_3010_NOT_LIVE.csv",
    "live_gate_copy": PARENT_ACTION / "live_response_component_gate_3010_FAIL_CLOSED.csv",
    "bound_interface_copy": LOCAL_BOUNDS / "q_loc_coupling_bound_interface_3010_NONCLAIM.csv",
    "arena_acquisition_copy": LOCAL_BOUNDS / "local_arena_acquisition_matrix_3010_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3010_LOCAL_BOUND_ACQUISITION_MATRIX_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    ("SRC3010_00_3009_next", RESIDUALS / "P8_Y5_R2FR_3009_NEXT_TARGET.csv", ["NEXT3009_0_3010", "first_Gamma_Khat_response_operator_row"], "3009 selects response-operator row or bound interface."),
    ("SRC3010_01_3009_doc", ROOT / "3009-Y5-R2FR-Gamma-Khat-metric-response-symbol-match-and-coupling-descent-guard-under-AX1090.md", ["Delta_K", "NEXT3009_0_3010"], "3009 names Delta_K and points to 3010."),
    ("SRC3010_02_3009_symbol", RESIDUALS / "P8_Y5_R2FR_3009_REAL_SYMBOL_MATCH_AUDIT.csv", ["SYM3009_1_formal_variation", "SYM3009_6_symbol_match_verdict"], "3009 symbol audit: formal variation only passes."),
    ("SRC3010_03_3009_deltaK", RESIDUALS / "P8_Y5_R2FR_3009_DELTA_K_OBSTRUCTION_DECOMPOSITION.csv", ["DK3009_0_identity", "DK3009_8_no_cancellation"], "3009 Delta_K obstruction decomposition."),
    ("SRC3010_04_3009_coupling", RESIDUALS / "P8_Y5_R2FR_3009_COUPLING_DESCENT_GUARD_AUDIT.csv", ["CDG3009_0_q_map", "CDG3009_7_guard_verdict"], "3009 coupling descent guard audit."),
    ("SRC3010_05_3009_interface", RESIDUALS / "P8_Y5_R2FR_3009_SOURCE_READY_RESIDUAL_INTERFACE.csv", ["RI3009_0_Delta_K", "RI3009_3_total"], "3009 residual interface."),
    ("SRC3010_06_ROR1836", RESIDUALS / "P8_Y5_PARENT_QLOC_1836_RESPONSE_OPERATOR_REQUIREMENTS.csv", ["ROR1836_0_common_vector", "ROR1836_5_no_cancellation"], "response-operator requirements across WEP/clock/lightcone/projective sectors."),
    ("SRC3010_07_ROP2207", RESIDUALS / "P8_Y5_PARENT_QLOC_2207_FIRST_RESPONSE_OPERATOR_ROW.csv", ["ROP2207_0_PPN_q_loc_linear_response_schema", "ROP2207_1_R10_q_loc_range_response_held"], "first nonclaim PPN/R10 response schema rows."),
    ("SRC3010_08_ROP2409", RESIDUALS / "P8_Y5_PARENT_QLOC_2409_QLOC_RESPONSE_OPERATOR_STATUS.csv", ["ROP2409_0_PPN_q_loc_linear_response_schema", "ROP2409_2_R10_yukawa_kernel_scaffold"], "2409 response operator status."),
    ("SRC3010_09_QOP2700", RESIDUALS / "P8_Y5_R2FR_2700_FIRST_QLOC_RESPONSE_OPERATOR_ROW_NONCLAIM.csv", ["QOP2700_0_PPN_GK_q_loc_response_operator", "R_PPN_GK"], "2700 first q_loc response operator row remains nonclaim."),
    ("SRC3010_10_QB2733", RESIDUALS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", ["QB2733_0_vector_envelope", "QB2733_3_verdict"], "2733 q_loc residual bound interface."),
    ("SRC3010_11_DER2809", RESIDUALS / "P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv", ["DER2809_0_time", "DER2809_5_total"], "2809 Delta_K derivative interface."),
    ("SRC3010_12_QB2811", RESIDUALS / "P8_Y5_R2FR_2811_QDELTAK_BOUND_INTERFACE.csv", ["QB2811_0_CPloc", "QB2811_5_score_gate"], "2811 q_DeltaK bound interface."),
    ("SRC3010_13_AM2611", RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv", ["AM2611_0_zero_condition", "AM2611_10_R_matter_arena"], "matter/source coupling bound interface."),
    ("SRC3010_14_CV2660", RESIDUALS / "P8_Y5_COUPLING_VECTOR_2660_COUPLING_RESIDUAL_VECTOR_SCHEMA.csv", ["CV2660_0_c_g", "CV2660_7_total_policy"], "coupling residual vector schema."),
]

source_rows = [
    base(
        {
            "source_id": source_id,
            "source_path": str(path),
            "path_exists": path.exists(),
            "required_anchors": "; ".join(required),
            "anchors_found": anchors(path, required),
            "missing_anchors": missing_anchors(path, required),
            "role": role,
        }
    )
    for source_id, path, required, role in SOURCE_SPECS
]


operator_rows = [
    base(
        {
            "operator_id": "ROP3010_0_PPN_GK_lowered_operator",
            "arena": "PPN",
            "input_residual": "q_loc_residual_vector_abs or q_DeltaK_abs + Ward/coupling terms",
            "operator_form": "Delta_PPN_GK^a = int_D K_PPN^a{}_nu(x,xprime;g_obs,source_frame,boundary) q_loc^nu(xprime) dVprime",
            "derived_status": "SCHEMA_READY_NOT_LIVE",
            "what_was_lowered": "formal Green/operator shape and required inputs are explicit",
            "blocking_missing_inputs": "MISSING_K_PPN_KERNEL;MISSING_QLOC_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_BOUNDARY_SUPPORT;MISSING_PPN_GAUGE",
            "units": "q_loc force_density_or_arena_normalized -> dimensionless PPN coefficients",
            "source_anchors": "ROP2207_0_PPN_q_loc_linear_response_schema;QOP2700_0_PPN_GK_q_loc_response_operator",
        }
    ),
    base(
        {
            "operator_id": "ROP3010_1_R10_Yukawa_lane",
            "arena": "R10_short_range",
            "input_residual": "q_loc(lambda) or effective Yukawa source coefficient",
            "operator_form": "alpha_R10_q(lambda)=int W_R10(lambda,x) q_loc(x)dV after range/source normalization",
            "derived_status": "SCAFFOLD_READY_NOT_LIVE",
            "what_was_lowered": "Yukawa kernel lane selected as near-term empirical route",
            "blocking_missing_inputs": "MISSING_QLOC_TO_YUKAWA_SOURCE_MAP;MISSING_LAMBDA_X;MISSING_CHARGE_NORMALIZATION;MISSING_REAL_BOUND_CURVE",
            "units": "q_loc range-normalized -> dimensionless alpha(lambda)",
            "source_anchors": "ROP2409_2_R10_yukawa_kernel_scaffold;ROP2207_1_R10_q_loc_range_response_held",
        }
    ),
    base(
        {
            "operator_id": "ROP3010_2_DeltaK_to_q_bound",
            "arena": "local_force_preprojection",
            "input_residual": "Delta_K component vector",
            "operator_form": "||q_DeltaK|| <= C_Ploc D_Delta + C_comm ||Delta_K||",
            "derived_status": "DERIVED_BOUND_INTERFACE_NONNUMERIC",
            "what_was_lowered": "Delta_K has a clean nonnumeric differential/projection envelope",
            "blocking_missing_inputs": "MISSING_DELTAK_COMPONENT_VALUES;MISSING_C_PLOC;MISSING_C_COMM;MISSING_DERIVATIVE_SCALES",
            "units": "stress_response_derivative -> force_density",
            "source_anchors": "DER2809_5_total;QB2811_4_total",
        }
    ),
    base(
        {
            "operator_id": "ROP3010_3_matter_coupling_bound",
            "arena": "source_coupling_preprojection",
            "input_residual": "A_matter and coupling vector components",
            "operator_form": "R_matter,arena <= U_B ||P_arena L_X^{-1}|| A_matter plus visible coupling vector terms",
            "derived_status": "BOUND_INTERFACE_NONNUMERIC",
            "what_was_lowered": "matter/source coupling leaks have named components and arena projection needs",
            "blocking_missing_inputs": "MISSING_A_MATTER_VALUES;MISSING_ESTAR_UNITS;MISSING_OPERATOR_INVERSE;MISSING_ARENA_PROJECTIONS",
            "units": "E_star/source current norm -> arena residual",
            "source_anchors": "AM2611_8_A_matter;AM2611_10_R_matter_arena;CV2660_7_total_policy",
        }
    ),
    base(
        {
            "operator_id": "ROP3010_4_live_component_verdict",
            "arena": "all",
            "input_residual": "first live Gamma/Khat response component",
            "operator_form": "requires parent-owned Gamma density, live Khat component, metric response, units, projection",
            "derived_status": "NO_LIVE_COMPONENT_PARENT_OWNED",
            "what_was_lowered": "no live row, but bound interfaces are now coherent",
            "blocking_missing_inputs": "MISSING_PARENT_OWNED_RESPONSE_COMPONENT",
            "units": "not score-ready",
            "source_anchors": "SYM3009_6_symbol_match_verdict;ROR1836_5_no_cancellation",
        }
    ),
]


live_gate_rows = [
    base(
        {
            "gate_id": "LRG3010_0_parent_density",
            "needed_for_live_row": "explicit parent-owned Gamma_eff density",
            "current_status": "MISSING",
            "pass_now": False,
            "if_fail": "operator row remains response schema only",
            "source_anchors": "SYM3009_0_Gamma_density",
        }
    ),
    base(
        {
            "gate_id": "LRG3010_1_live_Khat_component",
            "needed_for_live_row": "one live K_hat component matched to K_metric component",
            "current_status": "MISSING_COMPONENT_BY_COMPONENT_CERTIFICATE",
            "pass_now": False,
            "if_fail": "Delta_K component retained",
            "source_anchors": "SYM3009_2_Khat_identity;DK3009_8_no_cancellation",
        }
    ),
    base(
        {
            "gate_id": "LRG3010_2_units",
            "needed_for_live_row": "units map from stress/force density to arena observable",
            "current_status": "MISSING_UNITS_RESPONSE_MAP",
            "pass_now": False,
            "if_fail": "not score-ready",
            "source_anchors": "SYM3009_5_units_readout;ROP3010_0_PPN_GK_lowered_operator",
        }
    ),
    base(
        {
            "gate_id": "LRG3010_3_source_normalization",
            "needed_for_live_row": "source normalization independent of orbital GM",
            "current_status": "MISSING_SOURCE_NORMALIZATION",
            "pass_now": False,
            "if_fail": "no PPN/R10 comparison",
            "source_anchors": "ROP2207_0_PPN_q_loc_linear_response_schema;QB2733_2_observable_projection",
        }
    ),
    base(
        {
            "gate_id": "LRG3010_4_coupling_guard",
            "needed_for_live_row": "q-only matter/source descent or explicit coupling bounds",
            "current_status": "COUPLING_DESCENT_NOT_CLOSED",
            "pass_now": False,
            "if_fail": "even a GK row cannot prove local GR",
            "source_anchors": "CDG3009_7_guard_verdict;AM2611_0_zero_condition",
        }
    ),
    base(
        {
            "gate_id": "LRG3010_5_verdict",
            "needed_for_live_row": "all LRG3010_0..4 pass",
            "current_status": "LIVE_RESPONSE_ROW_FAILS_CLOSED",
            "pass_now": False,
            "if_fail": "use bound-interface fallback",
            "source_anchors": "ROP3010_4_live_component_verdict",
        }
    ),
]


bound_interface_rows = [
    base(
        {
            "bound_id": "BI3010_0_q_DeltaK",
            "family": "Delta_K metric-response mismatch",
            "bound_form": "||q_DeltaK|| <= C_Ploc D_Delta + C_comm ||Delta_K||",
            "required_inputs": "Delta_K components; derivative scales; P_loc norm; commutator norm; source/frame convention",
            "status": "SOURCE_READY_NONNUMERIC",
            "arena_use": "feeds PPN/R10/clock/orbital force residual after projection",
            "source_anchors": "QB2811_4_total;DER2809_5_total",
        }
    ),
    base(
        {
            "bound_id": "BI3010_1_Ward_Euler_boundary",
            "family": "Ward/Euler/boundary terms",
            "bound_form": "||q_Ward|| <= ||P_loc||(sum_A ||E_A nabla Phi^A|| + ||boundary/improvement flux||)",
            "required_inputs": "E_A list; local source-free clause; boundary/no-flux or boundary bound",
            "status": "SOURCE_READY_SCHEMA",
            "arena_use": "prevents q_loc=Ward residual from being set zero by words",
            "source_anchors": "RI3009_1_Ward_Euler;QRES3008_4_boundary_flux",
        }
    ),
    base(
        {
            "bound_id": "BI3010_2_matter_source",
            "family": "matter/source descent leakage",
            "bound_form": "A_matter <= A_geom + A_theta + A_lift + A_direct + A_worldtube + A_boundary + A_nonHilbert",
            "required_inputs": "component values or theorem-zero clauses in one E_star norm",
            "status": "SOURCE_READY_NONNUMERIC",
            "arena_use": "feeds WEP/clock/source-normalization/local GR guard",
            "source_anchors": "AM2611_8_A_matter",
        }
    ),
    base(
        {
            "bound_id": "BI3010_3_coupling_vector",
            "family": "visible hidden-coupling vector",
            "bound_form": "Residual_bound(arena) <= sum_i abs(projection_i(arena)*coefficient_i)+retained_tail_abs",
            "required_inputs": "c_g,b_dis,dln_alpha,dln_m,P_WEP,q_nonH,tau projection pack",
            "status": "SOURCE_READY_NONNUMERIC",
            "arena_use": "feeds R10/PPN/clock/WEP/orbital/EM",
            "source_anchors": "CV2660_0_c_g;CV2660_7_total_policy",
        }
    ),
    base(
        {
            "bound_id": "BI3010_4_total_no_cancellation",
            "family": "q_loc plus coupling total",
            "bound_form": "epsilon_local_total_abs <= abs(q_DeltaK)+abs(q_Ward)+abs(A_matter/coupling vector)+abs(projection tails)",
            "required_inputs": "all component families theorem-zero or source-backed numeric; no cancellation",
            "status": "NOT_SCORE_READY_COMPONENTS_MISSING",
            "arena_use": "global local-GR/PPN/R10 gate",
            "source_anchors": "RI3009_3_total;ROR1836_5_no_cancellation",
        }
    ),
]


arena_rows = [
    base(
        {
            "arena_id": "ARENA3010_0_R10",
            "arena": "R10 short-range",
            "observable": "alpha(lambda)",
            "needed_projection": "q_loc/Delta_K/coupling coefficient -> Yukawa source normalization",
            "needed_data": "real alpha_bound(lambda) curve; lambda_X; charge normalization",
            "current_status": "ACQUIRE_OR_BOUND",
            "first_input_row": "BI3010_0_q_DeltaK + BI3010_3_coupling_vector",
        }
    ),
    base(
        {
            "arena_id": "ARENA3010_1_PPN",
            "arena": "PPN",
            "observable": "gamma-1,beta-1,alpha_i,zeta_i,xi",
            "needed_projection": "K_PPN kernel and weak-field gauge/source frame",
            "needed_data": "PPN thresholds and q_loc radial/profile source normalization",
            "current_status": "ACQUIRE_OR_BOUND",
            "first_input_row": "ROP3010_0_PPN_GK_lowered_operator",
        }
    ),
    base(
        {
            "arena_id": "ARENA3010_2_clocks_EM",
            "arena": "clocks/EM",
            "observable": "redshift, clock drift, alpha_EM variation",
            "needed_projection": "P_clock and dln_alpha_EM/dX map",
            "needed_data": "clock sensitivity coefficients and tau_clock projection",
            "current_status": "ACQUIRE_OR_BOUND",
            "first_input_row": "BI3010_3_coupling_vector",
        }
    ),
    base(
        {
            "arena_id": "ARENA3010_3_WEP",
            "arena": "WEP/composition",
            "observable": "eta_AB or source/test composition residual",
            "needed_projection": "P_WEP_eta_AB and material fractions",
            "needed_data": "MICROSCOPE or equivalent official bound/readout",
            "current_status": "ACQUIRE_OR_BOUND",
            "first_input_row": "BI3010_2_matter_source + BI3010_3_coupling_vector",
        }
    ),
    base(
        {
            "arena_id": "ARENA3010_4_orbital",
            "arena": "orbital/source mass",
            "observable": "extra acceleration/source-mass drift",
            "needed_projection": "q_loc acceleration map without importing orbital GM as denominator",
            "needed_data": "source normalization and orbit residual threshold",
            "current_status": "ACQUIRE_OR_BOUND",
            "first_input_row": "BI3010_0_q_DeltaK + BI3010_4_total_no_cancellation",
        }
    ),
    base(
        {
            "arena_id": "ARENA3010_5_total",
            "arena": "all local arenas",
            "observable": "local-GR/Newton gate",
            "needed_projection": "all arena projections and no-cancellation envelope",
            "needed_data": "theorem-zero rows or real numeric bounds for every retained residual",
            "current_status": "NOT_SCORE_READY",
            "first_input_row": "BI3010_4_total_no_cancellation",
        }
    ),
]


gate_rows = [
    base({"gate_id": "GATE3010_0_sources", "gate": "all 3010 source anchors exist", "gate_status": "PASS" if all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows) else "FAIL", "condition_passed": all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows), "promotion_allowed_now": False, "reason": "sources support response/bound staging only"}),
    base({"gate_id": "GATE3010_1_operator_attempt", "gate": "response operator row attempted", "gate_status": "PASS_SCHEMA_ONLY", "condition_passed": True, "promotion_allowed_now": False, "reason": "operator rows are schema/bound interfaces, not live parent-owned components"}),
    base({"gate_id": "GATE3010_2_live_component", "gate": "one live response component parent-owned and united", "gate_status": "FAIL_CLOSED", "condition_passed": False, "promotion_allowed_now": False, "reason": "parent density, live Khat component, units, source normalization and coupling guard all fail"}),
    base({"gate_id": "GATE3010_3_bound_interface", "gate": "failed components source-ready as nonclaim bound inputs", "gate_status": "PASS_NONCLAIM", "condition_passed": True, "promotion_allowed_now": False, "reason": "Delta_K, Ward/boundary, matter source and coupling vector interfaces are staged"}),
    base({"gate_id": "GATE3010_4_local_claims", "gate": "local GR/Newton/PPN/WEP/R10 claim allowed", "gate_status": "FAIL_CLOSED", "condition_passed": False, "promotion_allowed_now": False, "reason": "no live response row and no numeric/source-backed bound pass"}),
]


decision_rows = [
    base({"decision_id": "DEC3010_0_no_live_row", "decision": "Do not call any response operator live.", "rationale": "The operator rows lower the form, but no parent-owned Gamma/Khat component with units and source normalization exists.", "next_effect": "keep q_loc/local GR nonclaim."}),
    base({"decision_id": "DEC3010_1_bound_interface_wins", "decision": "Use the bound-interface fallback.", "rationale": "Delta_K and coupling families are now named enough to acquire data or theorem-zero rows without hiding residuals.", "next_effect": "local testing can start as nonclaim acquisition."}),
    base({"decision_id": "DEC3010_2_R10_PPN_priority", "decision": "Prioritize R10 and PPN projections first.", "rationale": "R10 has a clean alpha(lambda) structure, while PPN directly protects the GR/Newton reduction; clocks/WEP/EM follow as coupling guards.", "next_effect": "3011 should build the acquisition matrix and dry-run schemas."}),
]


next_rows = [
    base(
        {
            "next_id": "NEXT3010_0_3011",
            "priority": "selected_primary",
            "target_doc": "3011-Y5-R2FR-local-bound-acquisition-matrix-for-q_loc-DeltaK-and-coupling-vector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_local_bound_acquisition_matrix_for_q_loc_DeltaK_and_coupling_vector_under_AX1090_3011.py",
            "mission": "Build the local-bound acquisition matrix for R10, PPN, clocks/EM, WEP and orbital arenas using the 3010 q_loc/Delta_K/coupling interfaces, without claiming a pass.",
            "success_condition": "each arena has required source files, projection quantities, units, status and first acquisition row; missing items are blockers not fabricated numbers.",
            "fallback_if_fail": "select only one arena, preferably R10, and acquire real source-backed bound rows first.",
            "guardrails": "no numeric claim without source-backed projection and bound data; no cancellation; no hidden coupling; no EH-only import; no orbital-GM denominator; no local-GR/Newton/PPN/WEP/R10 pass claim; no GitHub; no formalization-workbench edits",
        }
    )
]


write_csv(OUTPUTS["sources"], source_rows)
write_csv(OUTPUTS["operator_attempt"], operator_rows)
write_csv(OUTPUTS["live_gate"], live_gate_rows)
write_csv(OUTPUTS["bound_interface"], bound_interface_rows)
write_csv(OUTPUTS["arena_acquisition"], arena_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

shutil.copyfile(OUTPUTS["operator_attempt"], BRANCH_OUTPUTS["operator_attempt_copy"])
shutil.copyfile(OUTPUTS["live_gate"], BRANCH_OUTPUTS["live_gate_copy"])
shutil.copyfile(OUTPUTS["bound_interface"], BRANCH_OUTPUTS["bound_interface_copy"])
shutil.copyfile(OUTPUTS["arena_acquisition"], BRANCH_OUTPUTS["arena_acquisition_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = []
for copy_id, path in BRANCH_OUTPUTS.items():
    copy_rows = rows(path)
    claim_flags_present = any(
        boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("score_ready")) or boolish(row.get("valid_prediction_row"))
        for row in copy_rows
    )
    branch_rows.append(base({"copy_id": copy_id, "path": str(path), "path_exists": path.exists(), "row_count": len(copy_rows), "csv_parse_ok": csv_ok(path), "claim_flags_present": claim_flags_present}))
write_csv(OUTPUTS["branches"], branch_rows)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv" or not path.exists():
            continue
        for row in rows(path):
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if boolish(row.get(key)):
                    return False
    return True


validation_rows = [
    base({"validation_id": "VAL3010_00_sources_exist", "passed": all(boolish(row["path_exists"]) for row in source_rows), "detail": "every cited source path exists", "required": True}),
    base({"validation_id": "VAL3010_01_source_anchors", "passed": all(boolish(row["anchors_found"]) for row in source_rows), "detail": "every source contains required anchors", "required": True}),
    base({"validation_id": "VAL3010_02_operator_attempt_written", "passed": len(operator_rows) >= 5 and any(row["operator_id"] == "ROP3010_4_live_component_verdict" for row in operator_rows), "detail": "operator attempt rows and verdict exist", "required": True}),
    base({"validation_id": "VAL3010_03_live_gate_fails_closed", "passed": any(row["gate_id"] == "LRG3010_5_verdict" and not boolish(row["pass_now"]) for row in live_gate_rows), "detail": "live response row is explicitly failed closed", "required": True}),
    base({"validation_id": "VAL3010_04_bound_interface_written", "passed": len(bound_interface_rows) >= 5 and any(row["bound_id"] == "BI3010_4_total_no_cancellation" for row in bound_interface_rows), "detail": "q_loc/coupling bound interface and total no-cancellation row are staged", "required": True}),
    base({"validation_id": "VAL3010_05_arena_matrix_written", "passed": len(arena_rows) >= 6 and any(row["arena_id"] == "ARENA3010_5_total" for row in arena_rows), "detail": "local arena acquisition matrix is staged", "required": True}),
    base({"validation_id": "VAL3010_06_local_claims_blocked", "passed": any(row["gate_id"] == "GATE3010_4_local_claims" and not boolish(row["promotion_allowed_now"]) for row in gate_rows), "detail": "no local GR/Newton/PPN/WEP/R10 claim is allowed", "required": True}),
    base({"validation_id": "VAL3010_07_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3011-Y5-R2FR-local-bound-acquisition-matrix"), "detail": "3011 selects local-bound acquisition matrix", "required": True}),
    base({"validation_id": "VAL3010_08_branch_copies", "passed": all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) and not boolish(row["claim_flags_present"]) for row in branch_rows), "detail": "branch copies exist, parse, and carry no claim flags", "required": True}),
    base({"validation_id": "VAL3010_09_csv_parse", "passed": all(csv_ok(path) for path in list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())), "detail": "all 3010 CSV outputs parse cleanly", "required": True}),
    base({"validation_id": "VAL3010_10_paths_under_post_checkpoint", "passed": all(under(path, ROOT) for path in generated_paths), "detail": "all generated outputs are under post-checkpoint-work", "required": True}),
    base({"validation_id": "VAL3010_11_formalization_untouched", "passed": not any(FORMALIZATION.rglob("*3010*")) if FORMALIZATION.exists() else True, "detail": "no targeted 3010 files exist under formalization-workbench", "required": True}),
    base({"validation_id": "VAL3010_12_no_claim_flags", "passed": no_claim_flags(list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())), "detail": "all generated rows remain valid_for_claim=false and claim_allowed=false", "required": True}),
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(base({"validation_id": "VAL3010_OVERALL", "passed": overall_pass, "detail": "3010 attempts a first Gamma/Khat response operator row, fails live ownership closed, stages q_loc/Delta_K/coupling bound interfaces and local arena acquisition rows without promoting local GR/Newton", "required": True}))
write_csv(OUTPUTS["validation"], validation_rows)


doc = f"""# 3010 - Y5/R2FR First Gamma-Khat Response Operator Row Or q_loc Coupling Bound Interface Under AX1090

Status: `Y5_R2FR_3010_no_live_response_operator_bound_interface_and_local_acquisition_matrix_staged_3011_next`

Generated: `{RUN_UTC}`

## Current Verdict

3010 tries to lower the obstruction into an actual response-operator row. The answer is: not live yet. We have useful operator schemas, especially PPN and R10, and we have a real nonnumeric bound interface for `Delta_K -> q_loc`, but no parent-owned `Gamma_eff/K_metric/K_hat` component with units, source normalization and coupling guard all closed.

The most concrete surviving bound form is:

`||q_DeltaK|| <= C_Ploc D_Delta + C_comm ||Delta_K||`.

That is not a score and not a local-GR proof, but it is a usable acquisition interface. It tells us exactly what must be sourced or proved zero: `Delta_K` components, derivative scales, projector norm, projector commutator, source/frame convention, plus matter/coupling residuals.

So 3010 does not move us to a claim. It moves us to test plumbing: R10, PPN, clocks/EM, WEP and orbital arenas now have an acquisition matrix tied to the same no-cancellation residual stack.

## Source Register

{md_table(source_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Response Operator Row Attempt

{md_table(operator_rows, ["operator_id", "arena", "operator_form", "derived_status", "blocking_missing_inputs", "units"])}

## Live Response Component Gate

{md_table(live_gate_rows, ["gate_id", "needed_for_live_row", "current_status", "pass_now", "if_fail"])}

## q_loc Coupling Bound Interface

{md_table(bound_interface_rows, ["bound_id", "family", "bound_form", "required_inputs", "status", "arena_use"])}

## Local Arena Acquisition Matrix

{md_table(arena_rows, ["arena_id", "arena", "observable", "needed_projection", "needed_data", "current_status", "first_input_row"])}

## Promotion Gates

{md_table(gate_rows, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is where we stop trying to squeeze a proof out of a schema. The operator road is still promising, but it is not live. The useful win is that `Delta_K`, Ward/boundary leakage and hidden coupling now have a shared bound-interface language. That means the next move can finally lean toward testing without pretending the derivation is finished.

The best next bite is R10 plus PPN: R10 because the `alpha(lambda)` lane is clean, PPN because it guards the actual GR/Newton reduction.

## Forbidden Claims From 3010

- A live `Gamma/Khat` response operator is parent-owned.
- `Delta_K` is zero or numerically bounded.
- `q_loc` is below any local arena threshold.
- Hidden coupling residuals are bounded or zero.
- Local GR/Newton/PPN/WEP/R10 pass.
"""

DOC.write_text(doc, encoding="utf-8")

if not overall_pass:
    failed = [row["validation_id"] for row in validation_rows if not boolish(row["passed"])]
    raise SystemExit(f"3010 validation failed: {failed}")

print(f"wrote {DOC}")
for key, path in OUTPUTS.items():
    print(f"{key}: {path}")
for key, path in BRANCH_OUTPUTS.items():
    print(f"{key}: {path}")
