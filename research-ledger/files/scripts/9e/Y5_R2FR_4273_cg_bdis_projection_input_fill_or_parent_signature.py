from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4273"
CLAIM_ID = "L-114"
BRANCH = "MTS_R2FR_Y5_CG_BDIS_PROJECTION_INPUT_FILL_OR_PARENT_SIGNATURE_4273"
DECISION = "CG_BDIS_PROJECTION_CONTRACT_BUILT_UNIT_GAMMA_RANGE_FILLED_NX_CG_TAILS_STILL_BLOCK_NONCLAIM"
MARKER = "PPC4161_CG_BDIS_PROJECTION_INPUT_FILL_OR_PARENT_SIGNATURE_4273"
PACKET_MARKER = "PPC4161_PACKET_CG_BDIS_PROJECTION_INPUT_FILL_OR_PARENT_SIGNATURE_4273"
NEXT_TARGET = "4274-Y5-R2FR-parent-NX-cg-product-or-no-extra-frame-action-domain-proof.md"

FORMAL_PATH = FORMAL / "289-PPC4161-cg-bdis-projection-input-fill-or-parent-no-extra-frame-action-signature.md"
DOC_PATH = POST / "4273-Y5-R2FR-cg-bdis-projection-input-fill-or-parent-no-extra-frame-action-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4273_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4273_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_BOUND_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4273_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"

ALPHA_EFF_BOUND = 0.00578792
UNIT_Y_GAMMA = 1.0
UNIT_RANGE_RESPONSE = 1.0
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)

SOURCES = {
    "SRC4273_00_4272_formal": (
        FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md",
        "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS",
        "4272 handoff: Dq_geom wants scoreable c_g/b_dis frame-vector inputs.",
    ),
    "SRC4273_01_4272_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4272_VALIDATION.csv",
        "VAL4272_6_control_smoke_computes",
        "4272 runner proved the arithmetic path computes controls but refuses live rows.",
    ),
    "SRC4273_02_2104_ppn_projection": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv",
        "alpha_eff<=0.00578792",
        "Existing PPN projection template with unit canonical scalar coefficient.",
    ),
    "SRC4273_03_944_bound_pack": (
        SOURCE_DIR / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
        "FLB944_0_cg_weyl",
        "Frame-leak schema naming c_g and b_dis local arenas.",
    ),
    "SRC4273_04_945_first_rows": (
        SOURCE_DIR / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
        "BND945_4_disformal_value",
        "First c_g/b_dis rows are still placeholder nonclaim rows.",
    ),
    "SRC4273_05_live_4254": (
        LIVE_COMPONENT_CANDIDATE_PATH,
        "Dq_geom",
        "Live local-GR tomography candidate receiving the sharpened geometry blocker.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_number(value: str) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def parent_signature_retry_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PSR4273_0_exact_parent_clause",
            "S_ord=sum_A S_A[Psi_A,e_obs(q),omega[e_obs],theta_A] with no A_g(X), B_dis(X), h_s^perp, source-only frame, post-readout frame, or hidden Hodge frame slot.",
            "would imply c_g=b_dis=h_s^perp=0 by absence of independent representative-frame variables",
            "NOT_SIGNED_BY_CURRENT_PARENT_CORPUS",
            "MISSING_PUBLIC_PARENT_ACTION_DOMAIN_SIGNATURE",
        ),
        (
            "PSR4273_1_private_same_frame_clause",
            "Existing same-frame/private-selector rows support a closure branch.",
            "useful private route",
            "NOT_PUBLIC_THEOREM",
            "PRIVATE_SELECTOR_NOT_PARENT_ACTION",
        ),
        (
            "PSR4273_2_result",
            "The zero route stays live as a target but cannot be used for claim credit in 4273.",
            "fall back to projection contract",
            "ZERO_ROUTE_REJECTED_FOR_PUBLIC_CLAIM",
            "RUN_FINITE_CG_BDIS_CONTRACT",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "attempted_clause": clause,
            "would_give": would_give,
            "status": status,
            "blocker": blocker,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, clause, would_give, status, blocker in raw
    ]


def projection_derivation_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DER4273_0_scalar_template",
            "universal conformal scalar readout",
            "gamma-1=-2 alpha_eff^2 Y_gamma R_gamma/(1+alpha_eff^2 Y_gamma R_gamma)+tails",
            "PRJ2104_1_common_conformal_branch",
            "DERIVED_CONDITIONAL_TEMPLATE",
            "not yet MTS parent-owned",
        ),
        (
            "DER4273_1_unit_gamma",
            "canonical scalar normalization",
            "Y_gamma=1 in the 2104 canonical scalar template",
            "PRJ2104_4_Cassini_projection_bound",
            "FILLED_PROJECTION_INPUT",
            "conditional on using the canonical scalar branch, not raw c_g",
        ),
        (
            "DER4273_2_unit_range_worst_case",
            "long-range/local PPN worst case",
            "R_gamma=1 gives the conservative unsuppressed local response; a massive/screened branch would replace it by 0<R_gamma<=1",
            "PRJ2104_4_Cassini_projection_bound",
            "FILLED_PROJECTION_INPUT",
            "unit response is a worst-case contract, not an MTS range derivation",
        ),
        (
            "DER4273_3_bound_conversion",
            "Cassini/PPN diagnostic conversion",
            "|N_X c_g| sqrt(Y_gamma R_gamma) <= alpha_eff_bound, so with Y_gamma=R_gamma=1: |N_X c_g| <= 0.00578792",
            "PRJ2104_4_Cassini_projection_bound",
            "DERIVED_CONTRACT",
            "requires parent value for N_X c_g and theorem-zero/absolute-summed tails",
        ),
        (
            "DER4273_4_bdis_separation",
            "disformal branch",
            "b_dis is not scoreable from the Cassini alpha_eff row alone; it must be routed to preferred-frame, clock, orbital, or explicit disformal PPN projection rows.",
            "BND945_4_disformal_value",
            "SEPARATED_NOT_SCORED_AS_CG",
            "prevents hiding disformal residue in the c_g bound",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": derivation_id,
            "target": target,
            "formula_or_statement": formula,
            "source_anchor": source_anchor,
            "status": status,
            "remaining_caveat": caveat,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for derivation_id, target, formula, source_anchor, status, caveat in raw
    ]


def first_contract_rows() -> List[Dict[str, str]]:
    bound_on_abs_nxcg = ALPHA_EFF_BOUND / math.sqrt(UNIT_Y_GAMMA * UNIT_RANGE_RESPONSE)
    return [
        {
            **common(),
            "contract_id": "CON4273_0_unit_ppn_cg_contract",
            "quantity": "abs(N_X*c_g)",
            "formula": "abs(N_X*c_g) <= alpha_eff_bound/sqrt(Y_gamma*R_gamma)",
            "Y_gamma": f"{UNIT_Y_GAMMA:.1f}",
            "range_response": f"{UNIT_RANGE_RESPONSE:.1f}",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "derived_bound_value": f"{bound_on_abs_nxcg:.8f}",
            "units": "dimensionless",
            "filled_inputs": "Y_gamma=1; range_response=1; alpha_eff_bound=0.00578792",
            "missing_inputs": "parent N_X*c_g product; c_g source path; tail theorem-zero or absolute-sum guard",
            "status": "PROJECTION_CONTRACT_DERIVED_NOT_MTS_SCORED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "contract_id": "CON4273_1_bdis_route_contract",
            "quantity": "b_dis",
            "formula": "score b_dis only through explicit disformal/preferred-frame/clock/orbital projection matrix",
            "Y_gamma": "not_applicable",
            "range_response": "not_applicable",
            "alpha_eff_bound": "not_applicable",
            "derived_bound_value": "MISSING_BDIS_PROJECTION_MATRIX",
            "units": "model_dependent",
            "filled_inputs": "route separated from c_g alpha_eff contract",
            "missing_inputs": "Pi_dis; preferred-frame/clock/orbital bound source; parent b_dis value or zero theorem",
            "status": "BDIS_NOT_SCOREABLE_FROM_CASSINI_ALPHA_ROW",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def frame_vector_input_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "FVI4273_0_parent_zero",
            "parent_no_extra_frame_signature",
            "MISSING_PUBLIC_PARENT_ACTION_DOMAIN_SIGNATURE",
            "If filled, set c_g=b_dis=h_s^perp=0.",
        ),
        (
            "FVI4273_1_unit_gamma_range",
            "Y_gamma;range_response",
            "FILLED_CONDITIONAL_UNIT_PPN_CONTRACT",
            "Y_gamma=1 and R_gamma=1 for the conservative canonical scalar PPN contract.",
        ),
        (
            "FVI4273_2_parent_product",
            "N_X*c_g",
            "MISSING_PARENT_NUMERIC_PRODUCT_OR_ZERO_THEOREM",
            "This is now the first real c_g-side object to derive or bound.",
        ),
        (
            "FVI4273_3_disformal_vector",
            "b_dis;Pi_dis",
            "MISSING_BDIS_PROJECTION_MATRIX",
            "Route separately; do not compare raw b_dis to the alpha_eff row.",
        ),
        (
            "FVI4273_4_tail_guard",
            "nonH;readout;gauge;source;boundary;EM tails",
            "MISSING_TAIL_THEOREM_ZERO_OR_ABSOLUTE_SUM",
            "No cancellation against c_g is allowed.",
        ),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "input_quantity": quantity,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, status, meaning in raw
    ]


def runner_input_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "row_id": "RUN4273_0_live_contract_no_parent_product",
            "row_type": "nxcg_contract",
            "N_X_c_g": "MISSING_PARENT_NX_CG_PRODUCT",
            "alpha_eff": "",
            "Y_gamma": f"{UNIT_Y_GAMMA:.1f}",
            "range_response": f"{UNIT_RANGE_RESPONSE:.1f}",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "MISSING_TAIL_THEOREM_ZERO_OR_ABSOLUTE_SUM",
            "source_path": str(FORMAL_PATH),
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "RUN4273_1_live_bdis_no_projection",
            "row_type": "bdis_projection",
            "N_X_c_g": "not_applicable",
            "alpha_eff": "",
            "Y_gamma": "not_applicable",
            "range_response": "not_applicable",
            "alpha_eff_bound": "not_applicable",
            "tail_guard_status": "MISSING_BDIS_PROJECTION_MATRIX",
            "source_path": str(FORMAL_PATH),
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4273_0_nxcg_toy_pass",
            "row_type": "nxcg_contract",
            "N_X_c_g": "0.001",
            "alpha_eff": "",
            "Y_gamma": f"{UNIT_Y_GAMMA:.1f}",
            "range_response": f"{UNIT_RANGE_RESPONSE:.1f}",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4273_1_nxcg_toy_fail",
            "row_type": "nxcg_contract",
            "N_X_c_g": "0.01",
            "alpha_eff": "",
            "Y_gamma": f"{UNIT_Y_GAMMA:.1f}",
            "range_response": f"{UNIT_RANGE_RESPONSE:.1f}",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def score_row(row: Dict[str, str]) -> Dict[str, str]:
    out = dict(row)
    out["computed_alpha_eff"] = ""
    out["derived_bound_on_abs_NX_cg"] = ""
    out["passed_bound"] = "False"
    out["score_ready"] = "False"
    out["failure_modes"] = ""
    out["verdict"] = "REFUSED"

    if row["row_type"] != "nxcg_contract":
        out["failure_modes"] = "BDIS_REQUIRES_EXPLICIT_PROJECTION_MATRIX"
        return out

    y_gamma = row.get("Y_gamma", "")
    response = row.get("range_response", "")
    bound = row.get("alpha_eff_bound", "")
    if not (is_number(y_gamma) and is_number(response) and is_number(bound)):
        out["failure_modes"] = "MISSING_NUMERIC_Y_GAMMA_RANGE_OR_BOUND"
        return out

    y_value = float(y_gamma)
    response_value = float(response)
    bound_value = float(bound)
    if y_value <= 0.0 or response_value <= 0.0 or bound_value <= 0.0:
        out["failure_modes"] = "NONPOSITIVE_PROJECTION_INPUT"
        return out

    nxcg_bound = bound_value / math.sqrt(y_value * response_value)
    out["derived_bound_on_abs_NX_cg"] = f"{nxcg_bound:.8f}"

    nxcg = row.get("N_X_c_g", "")
    if not is_number(nxcg):
        out["failure_modes"] = "MISSING_PARENT_NX_CG_PRODUCT;MISSING_TAIL_GUARD"
        out["verdict"] = "CONTRACT_DERIVED_LIVE_ROW_BLOCKED"
        return out

    alpha_eff = abs(float(nxcg)) * math.sqrt(y_value * response_value)
    out["computed_alpha_eff"] = f"{alpha_eff:.8g}"
    out["passed_bound"] = str(alpha_eff <= bound_value)

    if row.get("control_only") == "True":
        out["verdict"] = "CONTROL_PASS_NONCLAIM" if alpha_eff <= bound_value else "CONTROL_FAIL_NONCLAIM"
        out["failure_modes"] = "CONTROL_ONLY"
        return out

    if row.get("tail_guard_status") != "THEOREM_ZERO" or row.get("valid_for_claim") != "True":
        out["failure_modes"] = "TAIL_GUARD_NOT_CLOSED_OR_VALID_FOR_CLAIM_FALSE"
        out["verdict"] = "NUMERIC_BUT_NONCLAIM" if alpha_eff <= bound_value else "NUMERIC_FAIL_NONCLAIM"
        return out

    out["score_ready"] = "True"
    out["verdict"] = "PASS_CLAIM_READY" if alpha_eff <= bound_value else "FAIL_CLAIM_READY"
    return out


def runner_rows() -> List[Dict[str, str]]:
    return [score_row(row) for row in runner_input_rows()]


def bound_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_CG_BDIS_PROJECTION_CONTRACT_4273",
            "target_component": "Dq_geom",
            "norm_or_bound": "abs(N_X*c_g) <= 0.00578792 under Y_gamma=R_gamma=1 plus zero/absolute tail guard",
            "numeric_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "units": "dimensionless",
            "filled_inputs": "Y_gamma;range_response;alpha_eff_bound",
            "missing": "N_X*c_g;tail_guard;b_dis_projection_or_zero;parent no-extra-frame signature",
            "source_path": str(FORMAL_PATH),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def later_geom_override() -> Dict[str, str]:
    candidates = [
        (
            SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "0.0",
        ),
        (
            SOURCE_DIR / "P8_Y5_R2FR_4276_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW",
        ),
        (
            SOURCE_DIR / "P8_Y5_R2FR_4275_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        ),
        (
            SOURCE_DIR / "P8_Y5_R2FR_4274_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE",
        ),
    ]
    for path, expected in candidates:
        for row in csv_rows(path):
            if row.get("probe_id") == "Dq_geom" and row.get("epsilon") == expected:
                return row
    return {}


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    later_geom = later_geom_override()
    rows: List[Dict[str, str]] = []
    seen = set()
    for row in previous:
        probe = row.get("probe_id", "")
        if not probe:
            continue
        updated = dict(row)
        updated.update(common())
        if probe == "Dq_geom":
            if later_geom:
                updated["epsilon"] = later_geom["epsilon"]
                updated["epsilon_C1"] = later_geom["epsilon_C1"]
                updated["source_path"] = later_geom["source_path"]
            else:
                updated["epsilon"] = "MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR"
                updated["epsilon_C1"] = "MISSING_C1_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR"
                updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        rows.append(updated)
        seen.add(probe)
    for probe in PROBE_ORDER:
        if probe in seen:
            continue
        rows.append(
            {
                **common(),
                "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": later_geom["epsilon"]
                if probe == "Dq_geom" and later_geom
                else "MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR"
                if probe == "Dq_geom"
                else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": later_geom["epsilon_C1"]
                if probe == "Dq_geom" and later_geom
                else "MISSING_C1_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR"
                if probe == "Dq_geom"
                else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": later_geom["source_path"] if probe == "Dq_geom" and later_geom else str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4273_0_parent_signature",
            "No-extra-frame remains the clean theorem route but is still not parent-signed.",
            "Do not claim c_g=b_dis=0 from private same-frame closure rows.",
            NEXT_TARGET,
        ),
        (
            "DEC4273_1_projection_fill",
            "PPN c_g projection side is now compressed to a concrete product contract.",
            "Under Y_gamma=R_gamma=1, the live bound is |N_X*c_g|<=0.00578792 before tails.",
            "derive or source N_X*c_g",
        ),
        (
            "DEC4273_2_bdis_guard",
            "b_dis is deliberately excluded from the c_g alpha_eff score.",
            "It needs its own disformal/preferred-frame/clock/orbital projection matrix or a zero theorem.",
            "derive Pi_dis or prove no disformal slot",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4273_0_no_parent_zero_claim", "c_g=b_dis=0 cannot be claimed until the public parent action signs no-extra-frame."),
        ("FW4273_1_no_raw_cg_claim", "raw c_g is never compared directly to Cassini/R10/clock rows."),
        ("FW4273_2_no_bdis_smuggling", "b_dis cannot be hidden inside the c_g alpha_eff contract."),
        ("FW4273_3_no_tail_cancellation", "tails must be theorem-zero or absolute-summed; cancellation credit is forbidden."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4273",
            "current_status": "projection side sharpened; parent product and tails still missing",
            "local_gr_claim": "False",
            "ppn_claim": "False",
            "newton_claim": "False",
            "em_claim": "False",
            "next_best_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4273 filled the conservative PPN projection coefficient/range contract; the remaining c_g-side problem is the parent-owned N_X*c_g product or a no-extra-frame theorem.",
            "success_condition": "derive N_X*c_g=0, source a numeric N_X*c_g product, or parent-sign the no-extra-frame action domain; also close/absolute-sum tails.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4273 attempts the parent no-extra-frame route again and keeps it unsigned, then derives the first concrete c_g-side PPN projection contract: in the canonical "
            "unit scalar-response branch, |N_X*c_g|<=0.00578792 before tails. This fills Y_gamma=1 and range_response=1 as a conservative contract, but it does not supply "
            "the MTS parent product N_X*c_g, b_dis projection matrix, or theorem-zero/absolute-sum tail guards."
        ),
        "current_evidence": (
            "4273 source register, parent signature retry, projection derivation rows, first scoreable projection contract, frame-vector inputs, runner results, updated Dq_geom candidate, decision and firewall."
        ),
        "status": "private_projection_contract_built_parent_product_and_tails_missing_nonclaim",
        "next_test": "Derive or source N_X*c_g, prove the public no-extra-frame action-domain signature, or build the explicit b_dis/preferred-frame projection matrix.",
        "key_risk": "Treating the unit PPN projection contract as an MTS c_g prediction, or ignoring b_dis/tail no-cancellation guards.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_unique_block(path: Path, marker: str, title: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n"
    path.write_text(text.rstrip() + block, encoding="utf-8")


def formal_doc() -> str:
    return f"""
# 289 - PPC4161 c_g/b_dis projection input fill or parent no-extra-frame action signature

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4273 does **not** claim local GR, PPN, R10, WEP, clock, orbital, Newtonian, or EM closure.

It does move the live blocker:

```text
old 4272 blocker: MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS
new 4273 blocker: MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR
```

## Parent zero route

The exact no-extra-frame clause remains:

```text
S_ord=sum_A S_A[Psi_A,e_obs(q),omega[e_obs],theta_A]
```

with no independent:

```text
A_g(X), B_dis(X), h_s^perp, source-only frame, post-readout frame, hidden Hodge frame slot.
```

If signed by the public parent action, that clause gives:

```text
c_g=b_dis=h_s^perp=0.
```

Current evidence still does not sign it. Private same-frame selectors are useful but not public parent-action derivations.

## Projection contract

The 2104 conformal scalar PPN template gives:

```text
gamma-1 = -2 alpha_eff^2 Y_gamma R_gamma/(1+alpha_eff^2 Y_gamma R_gamma) + tails.
```

In the canonical unit-response contract:

```text
Y_gamma=1,
R_gamma=1,
alpha_eff = |N_X c_g|.
```

The diagnostic Cassini/PPN bound therefore becomes:

```text
|N_X c_g| <= 0.00578792
```

before tails, and only after non-c_g tails are theorem-zero or absolute-summed.

## b_dis separation

`b_dis` is not scoreable from the canonical `alpha_eff` row. It needs an explicit disformal/preferred-frame/clock/orbital projection matrix, or a parent theorem removing the disformal slot.

## Live feed

The live `Dq_geom` row now points to the first concrete object to derive:

```text
N_X c_g
```

plus the no-cancellation tail guard and the `b_dis` projection/zero route.

## Next target

`{NEXT_TARGET}` should derive/source the parent-owned `N_X c_g` product or prove the parent action has no extra frame slot.
"""


def checkpoint_doc() -> str:
    return f"""
# 4273 - c_g/b_dis projection input fill or parent no-extra-frame action signature

Marker: `{MARKER}`

Decision: `{DECISION}`

4273 tries the no-extra-frame theorem route first. It remains unsigned, so the finite route is sharpened instead.

The concrete progress is:

```text
Y_gamma=1,
R_gamma=1,
|N_X c_g| <= 0.00578792
```

as a nonclaim PPN projection contract.

The remaining live obstruction is no longer the whole projection map. It is:

```text
N_X c_g,
b_dis projection or zero theorem,
tail theorem-zero or absolute-sum guard.
```

All rows remain `valid_for_claim=false`.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    derivations = csv_rows(paths["projection_derivation"])
    contracts = csv_rows(paths["first_contract"])
    frame_inputs = csv_rows(paths["frame_inputs"])
    runners = csv_rows(paths["runner"])
    components = csv_rows(paths["local_candidate"])
    acceptable_geom_epsilons = {
        "MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR",
        "MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW",
        "0.0",
    }
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + csv_rows(paths["parent_retry"])
        + derivations
        + contracts
        + frame_inputs
        + csv_rows(paths["runner_inputs"])
        + runners
        + csv_rows(paths["core_bound"])
        + components
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4273_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4273_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4273_2_unit_projection_filled",
            any(row["derivation_id"] == "DER4273_1_unit_gamma" and row["status"] == "FILLED_PROJECTION_INPUT" for row in derivations)
            and any(row["derivation_id"] == "DER4273_2_unit_range_worst_case" for row in derivations),
            "unit Y_gamma/range projection rows emitted",
        ),
        (
            "VAL4273_3_nxcg_contract_numeric",
            any(row["contract_id"] == "CON4273_0_unit_ppn_cg_contract" and row["derived_bound_value"] == f"{ALPHA_EFF_BOUND:.8f}" for row in contracts),
            "unit contract derives the N_X*c_g bound value",
        ),
        (
            "VAL4273_4_live_runner_blocked",
            any(row["row_id"] == "RUN4273_0_live_contract_no_parent_product" and row["verdict"] == "CONTRACT_DERIVED_LIVE_ROW_BLOCKED" for row in runners),
            "live row blocked by missing parent product and tails",
        ),
        (
            "VAL4273_5_controls_compute",
            any(row["row_id"] == "CTRL4273_0_nxcg_toy_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runners)
            and any(row["row_id"] == "CTRL4273_1_nxcg_toy_fail" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in runners),
            "toy controls prove pass/fail arithmetic",
        ),
        (
            "VAL4273_6_bdis_separated",
            any(row["input_id"] == "FVI4273_3_disformal_vector" and row["status"] == "MISSING_BDIS_PROJECTION_MATRIX" for row in frame_inputs),
            "b_dis is not smuggled into c_g score",
        ),
        (
            "VAL4273_7_live_4254_updated",
            any(row.get("probe_id") == "Dq_geom" and row.get("epsilon") in acceptable_geom_epsilons for row in components),
            "live Dq_geom candidate sharpened or later-refined",
        ),
        ("VAL4273_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4273_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4273_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4273_11_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4273_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4273_SOURCE_REGISTER.csv",
        "parent_retry": SOURCE_DIR / "P8_Y5_R2FR_4273_PARENT_SIGNATURE_RETRY.csv",
        "projection_derivation": SOURCE_DIR / "P8_Y5_R2FR_4273_PROJECTION_DERIVATION.csv",
        "first_contract": SOURCE_DIR / "P8_Y5_R2FR_4273_FIRST_SCOREABLE_PROJECTION_CONTRACT.csv",
        "frame_inputs": SOURCE_DIR / "P8_Y5_R2FR_4273_FRAME_VECTOR_INPUT_ROWS.csv",
        "runner_inputs": SOURCE_DIR / "P8_Y5_R2FR_4273_BOUND_RUNNER_INPUTS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4273_BOUND_RUNNER_RESULTS.csv",
        "core_bound": CORE_BOUND_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4273_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4273_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4273_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4273_NEXT_TARGET.csv",
    }

    write_csv(paths["sources"], source_rows())
    write_csv(paths["parent_retry"], parent_signature_retry_rows())
    write_csv(paths["projection_derivation"], projection_derivation_rows())
    write_csv(paths["first_contract"], first_contract_rows())
    write_csv(paths["frame_inputs"], frame_vector_input_rows())
    write_csv(paths["runner_inputs"], runner_input_rows())
    write_csv(paths["runner"], runner_rows())
    write_csv(paths["core_bound"], bound_candidate_rows())
    component_candidate = component_candidate_rows()
    write_csv(paths["local_candidate"], component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4273 c_g/b_dis projection contract",
        "4273 keeps the parent no-extra-frame zero route unsigned but sharpens the finite route: the canonical PPN projection side is now the product contract `|N_X c_g| <= 0.00578792` under unit scalar response before tails. The live missing object is the parent-owned `N_X c_g` product plus tail guards and a separate `b_dis` projection/zero route.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4273 packet projection contract",
        "Packet update: `Dq_geom` is no longer blocked by an unspecified projection map. It is blocked by `N_X c_g`, `b_dis/Pi_dis`, and no-cancellation tail guards.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
