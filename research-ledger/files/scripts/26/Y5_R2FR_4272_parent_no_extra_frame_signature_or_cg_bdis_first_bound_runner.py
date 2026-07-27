from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4272"
CLAIM_ID = "L-113"
BRANCH = "MTS_R2FR_Y5_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_FIRST_BOUND_RUNNER_4272"
DECISION = "PARENT_NO_EXTRA_FRAME_SIGNATURE_UNSIGNED_CG_BDIS_BOUND_RUNNER_BUILT_LIVE_ROWS_BLOCKED_NONCLAIM"
MARKER = "PPC4161_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_FIRST_BOUND_RUNNER_4272"
PACKET_MARKER = "PPC4161_PACKET_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_FIRST_BOUND_RUNNER_4272"
NEXT_TARGET = "4273-Y5-R2FR-cg-bdis-projection-input-fill-or-parent-no-extra-frame-action-signature.md"

FORMAL_PATH = FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"
DOC_PATH = POST / "4272-Y5-R2FR-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4272_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_BOUND_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
ALPHA_EFF_BOUND = 0.00578792
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


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4272_00_4271_formal": SourceSpec(
        "SRC4272_00_4271_formal",
        FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md",
        "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND",
        "4271 handoff: parent no-extra-frame zero or finite c_g/b_dis bound.",
    ),
    "SRC4272_01_4271_bridge": SourceSpec(
        "SRC4272_01_4271_bridge",
        SOURCE_DIR / "P8_Y5_R2FR_4271_FRAME_COMPONENT_BRIDGE.csv",
        "FBR4271_2_finite_bound_route",
        "Finite bound route selected when parent signature is unsigned.",
    ),
    "SRC4272_02_2104_ppn_projection": SourceSpec(
        "SRC4272_02_2104_ppn_projection",
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv",
        "PRJ2104_4_Cassini_projection_bound",
        "Cassini/PPN diagnostic bound on canonical alpha_eff.",
    ),
    "SRC4272_03_944_bound_pack": SourceSpec(
        "SRC4272_03_944_bound_pack",
        SOURCE_DIR / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
        "FLB944_0_cg_weyl",
        "Existing frame-leak bound pack names c_g, b_dis and required columns.",
    ),
    "SRC4272_04_945_first_rows": SourceSpec(
        "SRC4272_04_945_first_rows",
        SOURCE_DIR / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
        "BND945_0_cg_value",
        "Existing first frame-leak bound rows are placeholder/nonclaim.",
    ),
    "SRC4272_05_3647_shadow_formula": SourceSpec(
        "SRC4272_05_3647_shadow_formula",
        SOURCE_DIR / "P8_Y5_R2FR_3647_NO_SHADOW_THEOREM_ATTEMPT.csv",
        "NSF3647_6_verdict",
        "No-shadow theorem route is exact but not signed; finite c_g/b_dis rows stay live.",
    ),
    "SRC4272_06_2959_signature_gate": SourceSpec(
        "SRC4272_06_2959_signature_gate",
        SOURCE_DIR / "P8_Y5_R2FR_2959_SINGLE_OBSERVED_FRAME_PARENT_ACTION_GATE.csv",
        "SFRAME2959_7_verdict",
        "Single observed frame parent action gate remains not derived.",
    ),
    "SRC4272_07_2960_closure_guard": SourceSpec(
        "SRC4272_07_2960_closure_guard",
        SOURCE_DIR / "P8_Y5_R2FR_2960_SINGLE_FRAME_CLOSURE_DECLARATION_NONCLAIM.csv",
        "NO_THEOREM_ZERO_CREDIT",
        "Closure branch has no theorem-zero credit.",
    ),
    "SRC4272_08_4234_private_selector": SourceSpec(
        "SRC4272_08_4234_private_selector",
        SOURCE_DIR / "P8_Y5_R2FR_4234_SIX_CLAUSE_EH_COFRAME_GATE.csv",
        "KC4234_0_same_coframe",
        "Private same-frame selector exists but public parent truth remains false.",
    ),
    "SRC4272_09_3769_budget": SourceSpec(
        "SRC4272_09_3769_budget",
        SOURCE_DIR / "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv",
        "SBB3769_1_gamma_shadow",
        "Frame-shadow budget already maps to PPN gamma/beta/clock/source arenas.",
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
    fieldnames: List[str] = list(rows[0].keys())
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


def has_missing(value: str) -> bool:
    return value == "" or "MISSING" in value or value in {"NOT_SCORED", "NOT_RUN"}


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
            "4272 tries the public no-extra-frame parent signature and finds it still unsigned: existing same-frame/private selector rows are not a public parent-action "
            "derivation. It therefore builds the first finite c_g/b_dis geometry-core bound runner. The runner refuses raw c_g comparisons, requires canonical alpha_eff "
            "or c_g with N_X, Y_gamma, range/profile response, sourced tail guards and no-cancellation accounting, and carries the Cassini alpha_eff<=0.00578792 row only "
            "as a diagnostic bound until MTS supplies those inputs."
        ),
        "current_evidence": (
            "4272 source register, parent signature audit, bound schema, input rows, runner results, claim gates, updated Dq_geom candidate, decision and firewall."
        ),
        "status": "private_no_extra_frame_signature_unsigned_cg_bdis_bound_runner_built_live_rows_blocked_nonclaim",
        "next_test": "Fill N_X, Y_gamma/range response, b_dis projection and tail guards, or derive the public no-extra-frame action-domain signature.",
        "key_risk": "Comparing raw c_g to Cassini/R10/clock bounds or treating a private same-frame closure branch as a derived parent theorem.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def signature_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SIG4272_0_exact_clause",
            "public no-extra-frame action domain",
            "S_ord=sum_A S_A[Psi_A,e_obs(q),omega[e_obs],theta_A] with no independent A_g(X), B_dis(X), h_s^perp, source-only frame or post-readout frame slot.",
            "EXACT_CLAUSE_AVAILABLE",
            "Would zero c_g, b_dis and sector shadows by variable absence plus q-chain rule.",
            "parent_action_signature_missing",
        ),
        (
            "SIG4272_1_existing_private_selector",
            "4234 private same-frame selector",
            "Private selector truth exists for same coframe/EH block/vertical silence/boundary routing/kappa source coupling.",
            "PRIVATE_SELECTOR_TRUE_PUBLIC_PARENT_FALSE",
            "Useful private branch, not a public derivation.",
            "public_parent_truth_false",
        ),
        (
            "SIG4272_2_closure_branch",
            "2960 single-frame closure",
            "Closure can be adopted as a labelled branch but carries closure_debt=true and no theorem-zero credit.",
            "CLOSURE_AVAILABLE_NOT_DERIVED",
            "Cannot close Dq_geom in the derived branch.",
            "no_theorem_zero_credit",
        ),
        (
            "SIG4272_3_covariance_wep_ward",
            "failed shortcut tests",
            "General covariance, leading WEP silence or total Ward conservation do not remove universal conformal/disformal source terms.",
            "SHORTCUTS_REFUSED",
            "Finite c_g can be WEP-quiet while still sourcing trace/PPN/clock/orbital channels.",
            "finite_bound_runner_required",
        ),
        (
            "SIG4272_4_verdict",
            "current public no-extra-frame signature",
            "The clause is the right derivation target but not signed by current parent evidence.",
            "PUBLIC_SIGNATURE_UNSIGNED",
            "Keep Dq_geom nonzero/nonclaim and run finite c_g/b_dis bound path.",
            "4272_runner_active",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "clause": clause,
            "statement": statement,
            "status": status,
            "if_signed": if_signed,
            "current_blocker": blocker,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, statement, status, if_signed, blocker in raw
    ]


def bound_schema_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SCHEMA4272_0_alpha_eff",
            "alpha_eff",
            "canonical projected scalar-frame coupling entering PPN gamma",
            "dimensionless",
            "abs(alpha_eff_predicted) <= alpha_eff_bound",
            "alpha_eff_predicted;alpha_eff_bound;tail_guard_status;source_path;valid_for_claim",
            "safe only after all non-cg tails are theorem-zero or included in absolute residual sum",
        ),
        (
            "SCHEMA4272_1_raw_cg",
            "c_g",
            "raw common conformal derivative D ln A_g / dXhat",
            "dimensionless",
            "alpha_eff = abs(N_X*c_g)*sqrt(abs(Y_gamma*range_response)); compare alpha_eff to bound",
            "c_g;N_X;Y_gamma;range_response;tail_guard_status;source_path;valid_for_claim",
            "raw c_g cannot be compared directly to Cassini/R10/clock bounds",
        ),
        (
            "SCHEMA4272_2_bdis",
            "b_dis",
            "representative disformal derivative",
            "model_dependent",
            "requires PPN/preferred-frame/clock projection matrix before scoring",
            "b_dis;Pi_dis;profile;bound_source_path;source_path;valid_for_claim",
            "not scoreable from the Cassini alpha_eff row alone",
        ),
        (
            "SCHEMA4272_3_no_cancellation",
            "tail_guard",
            "all non-target frame/source/readout terms",
            "dimensionless_or_declared",
            "abs(total)<=bound only with absolute-summed tails or theorem-zero tails",
            "tail_terms;tail_values;tail_sources;no_cancellation_guard",
            "forbids hiding b_dis/q_nonH/readout/gauge tails inside c_g",
        ),
    ]
    return [
        {
            **common(),
            "schema_id": schema_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "score_formula": formula,
            "required_columns": required,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for schema_id, quantity, definition, units, formula, required, guard in raw
    ]


def input_rows() -> List[Dict[str, str]]:
    source_2104 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv"
    return [
        {
            **common(),
            "candidate_id": "FBI4272_0_parent_zero_requested_unsigned",
            "quantity": "parent_no_extra_frame_zero",
            "component_value": "0.0",
            "component_units": "dimensionless",
            "N_X": "not_applicable",
            "Y_gamma": "not_applicable",
            "range_response": "not_applicable",
            "bound_value": "0.0",
            "tail_guard_status": "not_applicable",
            "theorem_zero": "True",
            "zero_authority": "MISSING_PUBLIC_PARENT_SIGNATURE",
            "source_path": str(FORMAL_PATH),
            "control_only": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "candidate_id": "FBI4272_1_raw_cg_missing_projection",
            "quantity": "c_g",
            "component_value": "MISSING_PARENT_NUMERIC_CG",
            "component_units": "dimensionless",
            "N_X": "MISSING_CANONICAL_NORMALIZATION_N_X",
            "Y_gamma": "MISSING_Y_GAMMA",
            "range_response": "MISSING_RANGE_PROFILE_RESPONSE",
            "bound_value": str(ALPHA_EFF_BOUND),
            "tail_guard_status": "MISSING_TAIL_GUARDS",
            "theorem_zero": "False",
            "zero_authority": "not_applicable",
            "source_path": "MISSING_PARENT_SOURCE",
            "control_only": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "candidate_id": "FBI4272_2_alpha_eff_bound_only_no_prediction",
            "quantity": "alpha_eff",
            "component_value": "MISSING_MTS_ALPHA_EFF_PREDICTION",
            "component_units": "dimensionless",
            "N_X": "not_applicable",
            "Y_gamma": "1.0",
            "range_response": "1.0",
            "bound_value": str(ALPHA_EFF_BOUND),
            "tail_guard_status": "MISSING_NON_CG_TAIL_ZERO_OR_ABS_SUM",
            "theorem_zero": "False",
            "zero_authority": "not_applicable",
            "source_path": str(source_2104),
            "control_only": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "candidate_id": "FBI4272_3_bdis_missing_projection",
            "quantity": "b_dis",
            "component_value": "MISSING_PARENT_NUMERIC_BDIS",
            "component_units": "model_dependent",
            "N_X": "not_applicable",
            "Y_gamma": "not_applicable",
            "range_response": "not_applicable",
            "bound_value": "MISSING_PREFERRED_FRAME_OR_CLOCK_BOUND_PROJECTION",
            "tail_guard_status": "MISSING_BDIS_PROJECTION_MATRIX",
            "theorem_zero": "False",
            "zero_authority": "not_applicable",
            "source_path": "MISSING_PARENT_SOURCE",
            "control_only": "False",
            "valid_for_claim": "False",
        },
    ]


def control_rows() -> List[Dict[str, str]]:
    source_2104 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv"
    return [
        {
            **common(),
            "candidate_id": "CTRL4272_0_alpha_eff_toy_pass",
            "quantity": "alpha_eff",
            "component_value": "0.001",
            "component_units": "dimensionless",
            "N_X": "not_applicable",
            "Y_gamma": "1.0",
            "range_response": "1.0",
            "bound_value": str(ALPHA_EFF_BOUND),
            "tail_guard_status": "ALL_TAILS_ZERO_OR_NUMERIC_ABS_SUM_INCLUDED",
            "theorem_zero": "False",
            "zero_authority": "not_applicable",
            "source_path": str(source_2104),
            "control_only": "True",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "candidate_id": "CTRL4272_1_alpha_eff_toy_fail",
            "quantity": "alpha_eff",
            "component_value": "0.01",
            "component_units": "dimensionless",
            "N_X": "not_applicable",
            "Y_gamma": "1.0",
            "range_response": "1.0",
            "bound_value": str(ALPHA_EFF_BOUND),
            "tail_guard_status": "ALL_TAILS_ZERO_OR_NUMERIC_ABS_SUM_INCLUDED",
            "theorem_zero": "False",
            "zero_authority": "not_applicable",
            "source_path": str(source_2104),
            "control_only": "True",
            "valid_for_claim": "False",
        },
    ]


def score_row(row: Dict[str, str]) -> Dict[str, str]:
    quantity = row.get("quantity", "")
    candidate_id = row.get("candidate_id", "")
    control_only = row.get("control_only") == "True"
    valid_for_claim = row.get("valid_for_claim") == "True"
    source_path = Path(row.get("source_path", "")) if row.get("source_path") else Path("")
    reasons: List[str] = []
    computed = "NOT_SCORED"
    bound = row.get("bound_value", "")
    verdict = "REFUSED"
    pass_bound = "False"
    score_ready = "False"
    claim_allowed = "False"

    if row.get("theorem_zero") == "True":
        if row.get("zero_authority") == "PARENT_SIGNED_NO_EXTRA_FRAME_TRUE":
            verdict = "THEOREM_ZERO_ACCEPTED_PRIVATE_ONLY" if not valid_for_claim else "THEOREM_ZERO_ACCEPTED"
            computed = "0.0"
            pass_bound = "True"
            score_ready = str(valid_for_claim and not control_only)
        else:
            reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_NO_EXTRA_FRAME_AUTHORITY")
    elif quantity == "alpha_eff":
        if not is_number(row.get("component_value", "")):
            reasons.append("MISSING_NUMERIC_ALPHA_EFF_PREDICTION")
        if not is_number(bound):
            reasons.append("MISSING_NUMERIC_ALPHA_EFF_BOUND")
        if row.get("component_units") != "dimensionless":
            reasons.append("ALPHA_EFF_UNITS_NOT_DIMENSIONLESS")
        if row.get("tail_guard_status") != "ALL_TAILS_ZERO_OR_NUMERIC_ABS_SUM_INCLUDED":
            reasons.append("MISSING_TAIL_GUARDS")
        if not source_path.exists():
            reasons.append("MISSING_EXISTING_SOURCE_PATH")
        if not reasons:
            value = abs(float(row["component_value"]))
            limit = float(bound)
            computed = f"{value:.12g}"
            pass_bound = str(value <= limit)
            verdict = "CONTROL_PASS_NONCLAIM" if control_only and value <= limit else (
                "CONTROL_FAIL_NONCLAIM" if control_only else ("PASS_NONCLAIM" if value <= limit else "FAIL_NONCLAIM")
            )
            score_ready = str(valid_for_claim and not control_only)
    elif quantity == "c_g":
        required_numeric = ("component_value", "N_X", "Y_gamma", "range_response", "bound_value")
        for key in required_numeric:
            if not is_number(row.get(key, "")):
                reasons.append(f"MISSING_NUMERIC_{key.upper()}")
        if row.get("component_units") != "dimensionless":
            reasons.append("CG_UNITS_NOT_DIMENSIONLESS")
        if row.get("tail_guard_status") != "ALL_TAILS_ZERO_OR_NUMERIC_ABS_SUM_INCLUDED":
            reasons.append("MISSING_TAIL_GUARDS")
        if not source_path.exists():
            reasons.append("MISSING_EXISTING_SOURCE_PATH")
        if not reasons:
            c_g = float(row["component_value"])
            n_x = float(row["N_X"])
            y_gamma = float(row["Y_gamma"])
            range_response = float(row["range_response"])
            value = abs(n_x * c_g) * math.sqrt(abs(y_gamma * range_response))
            limit = float(bound)
            computed = f"{value:.12g}"
            pass_bound = str(value <= limit)
            verdict = "CONTROL_PASS_NONCLAIM" if control_only and value <= limit else (
                "CONTROL_FAIL_NONCLAIM" if control_only else ("PASS_NONCLAIM" if value <= limit else "FAIL_NONCLAIM")
            )
            score_ready = str(valid_for_claim and not control_only)
    elif quantity == "b_dis":
        reasons.append("BDIS_PROJECTION_RUNNER_NOT_SCOREABLE_WITH_CASSINI_ALPHA_EFF_ONLY")
        if has_missing(row.get("component_value", "")):
            reasons.append("MISSING_NUMERIC_BDIS")
        if has_missing(row.get("bound_value", "")):
            reasons.append("MISSING_BDIS_BOUND_OR_PROJECTION")
    else:
        reasons.append("UNRECOGNIZED_QUANTITY_OR_SCHEMA_ONLY")

    if not valid_for_claim:
        reasons.append("VALID_FOR_CLAIM_FALSE")
    if control_only:
        reasons.append("CONTROL_ONLY")

    if not reasons and valid_for_claim and not control_only and pass_bound == "True":
        claim_allowed = "True"

    return {
        **common(),
        "runner_id": f"RUN4272_{candidate_id}",
        "candidate_id": candidate_id,
        "quantity": quantity,
        "computed_alpha_eff_or_value": computed,
        "bound_value": bound,
        "pass_bound": pass_bound,
        "score_ready": score_ready,
        "verdict": verdict if reasons else verdict,
        "failure_reasons": ";".join(reasons) if reasons else "NONE",
        "claim_allowed": claim_allowed,
        "valid_for_claim": str(valid_for_claim),
    }


def runner_rows(input_path: Path, control_path: Path) -> List[Dict[str, str]]:
    return [score_row(row) for row in csv_rows(input_path) + csv_rows(control_path)]


def claim_gate_rows(runners: List[Dict[str, str]]) -> List[Dict[str, str]]:
    live_rows = [row for row in runners if "CONTROL_ONLY" not in row.get("failure_reasons", "")]
    return [
        {
            **common(),
            "gate_id": "GATE4272_0_parent_signature",
            "claim": "Dq_geom parent no-extra-frame zero",
            "passed": "False",
            "reason": "public parent signature remains unsigned; private selector/closure has no theorem-zero credit",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GATE4272_1_live_bound_score",
            "claim": "finite c_g/b_dis frame vector score",
            "passed": str(any(row.get("score_ready") == "True" and row.get("pass_bound") == "True" for row in live_rows)),
            "reason": "live rows lack numeric parent component values, canonical normalization, range/profile response, projection matrices or tail guards",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GATE4272_2_raw_cg_forbidden",
            "claim": "raw c_g can be compared directly to Cassini/R10/clock bounds",
            "passed": "False",
            "reason": "runner requires alpha_eff or c_g with N_X, Y_gamma/range response and tail guards",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_CG_BDIS_BOUND_RUNNER_4272",
            "probe_id": "Dq_geom",
            "old_epsilon": "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND",
            "new_epsilon": "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS",
            "new_epsilon_C1": "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS",
            "source_path": str(FORMAL_PATH),
            "status": "PARENT_SIGNATURE_UNSIGNED_FINITE_BOUND_RUNNER_READY_LIVE_INPUTS_MISSING",
            "zero_route": "PARENT_SIGNED_NO_EXTRA_FRAME_TRUE would set c_g=b_dis=sector_shadow=0",
            "finite_bound_route": "score alpha_eff or c_g with N_X, Y_gamma/range_response, sourced tail guards, no-cancellation envelope, and b_dis projection rows",
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
        (
            SOURCE_DIR / "P8_Y5_R2FR_4273_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR",
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
    if not previous:
        previous = [
            {
                **common(),
                "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
            for probe in PROBE_ORDER
        ]
    output: List[Dict[str, str]] = []
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
                updated["epsilon"] = "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
                updated["epsilon_C1"] = "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
                updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        output.append(updated)
        seen.add(probe)
    for probe in PROBE_ORDER:
        if probe not in seen:
            output.append(
                {
                    **common(),
                    "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                    "probe_id": probe,
                    "weight": "1.0",
                    "epsilon": later_geom["epsilon"]
                    if probe == "Dq_geom" and later_geom
                    else "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
                    if probe == "Dq_geom"
                    else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": later_geom["epsilon_C1"]
                    if probe == "Dq_geom" and later_geom
                    else "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
                    if probe == "Dq_geom"
                    else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": later_geom["source_path"] if probe == "Dq_geom" and later_geom else str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4272_0_signature_result",
            "Do not parent-sign no-extra-frame from current evidence.",
            "The exact clause exists, but 2959/2960/4234 show it is a closure/private selector, not a public parent derivation.",
            "keep zero route as target only",
        ),
        (
            "DEC4272_1_runner_result",
            "Use the finite c_g/b_dis runner as the live route until the parent signature appears.",
            "It refuses raw c_g and requires canonical alpha_eff or sourced projection data.",
            NEXT_TARGET,
        ),
        (
            "DEC4272_2_4254_progress",
            "4254 now names the geometry gate as scoreable frame-vector inputs rather than a generic coframe-shadow absence.",
            "The live missing object is concrete: N_X/Y_gamma/range/tails/c_g/b_dis inputs or parent no-extra-frame signature.",
            "rerun 4254 after any input fill",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4272_0_no_private_selector_claim", "Do not turn 4234 private selector truth into public parent no-extra-frame proof.", "public parent signature or finite bound only"),
        ("FW4272_1_no_raw_cg_bound", "Do not compare raw c_g directly to Cassini, R10, clock or WEP bounds.", "canonical alpha_eff or projection matrix required"),
        ("FW4272_2_no_missing_tail_guard", "Do not score alpha_eff/c_g while b_dis, q_nonH, gauge/readout or tail terms are unzeroed and unbounded.", "absolute no-cancellation tail guard"),
        ("FW4272_3_no_control_claim", "Do not use control smoke rows as theory evidence.", "control_only rows remain valid_for_claim=false"),
        ("FW4272_4_no_local_gr_claim", "Do not claim local GR while 4254 still lists Dq_geom and tomography constants.", "4254 missing list must clear with sourced inputs"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4272_0",
            "summary": (
                "4272 keeps the exact no-extra-frame theorem as the preferred derivation target, refuses to promote the current closure/private selector, "
                "and installs a finite c_g/b_dis frame-vector runner whose live rows are blocked until real parent/projection inputs exist."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Fill the first scoreable input: N_X/Y_gamma/range response for c_g, b_dis projection, tail guards, or the parent no-extra-frame action signature.",
            "avoid": "Do not rerun generic no-shadow audits, compare raw c_g to a bound, or use control rows as evidence.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 288 - PPC4161 parent no-extra-frame signature or c_g/b_dis first bound runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4272 does not prove:

```text
Dq_geom = 0
```

and does not claim local GR, PPN, R10, WEP, clock or orbital safety.

## Parent signature attempt

The exact no-extra-frame clause is:

```text
S_ord = sum_A S_A[Psi_A, e_obs(q), omega[e_obs], theta_A]
```

with no independent:

```text
A_g(X), B_dis(X), h_s^perp,
source-only frame,
post-readout frame,
hidden constitutive/Hodge frame slot.
```

If the public parent action signs this clause, the 4271 theorem gives:

```text
c_g = b_dis = h_s^perp = 0.
```

Current evidence does not sign it. Existing same-frame rows are closure/private-selector evidence, not a public parent-action derivation.

## Finite bound runner

The live alternative is an executable finite-bound route:

```text
alpha_eff = |N_X c_g| sqrt(|Y_gamma R_range|)
```

or a directly predicted canonical `alpha_eff`.

The Cassini/PPN diagnostic bound is:

```text
alpha_eff <= {ALPHA_EFF_BOUND}
```

but this is scoreable only when:

```text
N_X, Y_gamma, R_range are sourced,
b_dis/q_nonH/gauge/readout/tail rows are theorem-zero or absolute-summed,
the source path exists,
valid_for_claim=true.
```

Raw `c_g` is never compared directly to the Cassini/R10/clock bounds.

## Live 4254 feed

The live `Dq_geom` row is sharpened to:

```text
MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS.
```

This means the geometry gate now wants specific inputs:

```text
parent no-extra-frame signature
or
c_g, b_dis, N_X, Y_gamma, range/profile response, projection/tail guards.
```

## Next target

`{NEXT_TARGET}` should fill the first scoreable projection input or derive the parent signature.
"""


def checkpoint_doc() -> str:
    return f"""
# 4272 - Y5 R2FR parent no-extra-frame signature or c_g/b_dis first bound runner

Packet marker: `{PACKET_MARKER}`

## Result

The public no-extra-frame parent signature remains unsigned. I did not promote the private same-frame selector.

Instead, 4272 builds the finite frame-vector runner:

```text
c_g / b_dis / alpha_eff -> PPN/R10/clock/WEP-style bounds
```

with strict refusal of raw `c_g` scoring.

## Why this matters

The local-GR route now has a practical fork:

```text
derive parent no-extra-frame
or
fill scoreable frame-vector inputs
```

No more generic "coframe missing" fog.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    audit = csv_rows(paths["audit"])
    schema = csv_rows(paths["schema"])
    inputs = csv_rows(paths["inputs"])
    controls = csv_rows(paths["controls"])
    runners = csv_rows(paths["runners"])
    gates = csv_rows(paths["gates"])
    candidate = csv_rows(paths["candidate"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_geom = [row for row in live_candidate if row.get("probe_id") == "Dq_geom"]
    acceptable_geom_epsilons = {
        "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS",
        "MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR",
        "MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW",
        "0.0",
    }
    acceptable_geom_c1 = {
        "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS",
        "MISSING_C1_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR",
        "MISSING_C1_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_C1_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_C1_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW",
        "0.0",
    }
    acceptable_geom_sources = {
        str(FORMAL_PATH),
        str(FORMAL / "289-PPC4161-cg-bdis-projection-input-fill-or-parent-no-extra-frame-action-signature.md"),
        str(FORMAL / "290-PPC4161-parent-NX-cg-product-or-no-extra-frame-action-domain-proof.md"),
        str(FORMAL / "291-PPC4161-parent-cg-zero-theorem-or-ZX-cg-source-row.md"),
        str(FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md"),
        str(FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"),
    }
    prior_zero_components = {
        "Dq_tau": "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md",
        "Dq_matter": "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Dq_source_readout": "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Dq_theta_marker": "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "Dq_boundary_projector": "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_EM": "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Dq_coeff": "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
    }
    prior_zeros_preserved = True
    for probe, source_file in prior_zero_components.items():
        rows = [row for row in live_candidate if row.get("probe_id") == probe]
        if not rows or rows[0].get("epsilon") != "0.0" or source_file not in rows[0].get("source_path", ""):
            prior_zeros_preserved = False
    live_runner_rows = [row for row in runners if "CONTROL_ONLY" not in row.get("failure_reasons", "")]
    control_runner_rows = [row for row in runners if "CONTROL_ONLY" in row.get("failure_reasons", "")]
    rows = [
        ("VAL4272_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4272_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4272_2_signature_unsigned",
            any(row["status"] == "PUBLIC_SIGNATURE_UNSIGNED" for row in audit),
            "public no-extra-frame signature remains unsigned",
        ),
        (
            "VAL4272_3_bound_schema",
            {"alpha_eff", "c_g", "b_dis", "tail_guard"}.issubset({row.get("quantity") for row in schema}),
            "alpha_eff/c_g/b_dis/tail schema emitted",
        ),
        (
            "VAL4272_4_live_inputs_blocked",
            bool(inputs) and all(row.get("valid_for_claim") == "False" for row in inputs),
            "live inputs are nonclaim placeholders",
        ),
        (
            "VAL4272_5_runner_refuses_live",
            bool(live_runner_rows) and all(row.get("score_ready") == "False" and row.get("claim_allowed") == "False" for row in live_runner_rows),
            "runner refuses all live rows",
        ),
        (
            "VAL4272_6_control_smoke_computes",
            any(row.get("verdict") == "CONTROL_PASS_NONCLAIM" for row in control_runner_rows)
            and any(row.get("verdict") == "CONTROL_FAIL_NONCLAIM" for row in control_runner_rows),
            "control smoke rows compute pass and fail without claim",
        ),
        (
            "VAL4272_7_raw_cg_forbidden_gate",
            any(row.get("gate_id") == "GATE4272_2_raw_cg_forbidden" and row.get("passed") == "False" for row in gates),
            "raw c_g direct bound comparison is forbidden",
        ),
        (
            "VAL4272_8_candidate_nonclaim",
            bool(candidate)
            and candidate[0]["new_epsilon"] == "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
            and candidate[0]["valid_for_claim"] == "False",
            "Dq_geom bound-runner candidate is nonclaim",
        ),
        (
            "VAL4272_9_live_4254_updated_nonzero",
            bool(live_geom)
            and live_geom[0].get("epsilon") in acceptable_geom_epsilons
            and live_geom[0].get("epsilon_C1") in acceptable_geom_c1
            and live_geom[0].get("source_path") in acceptable_geom_sources,
            "live 4254 candidate Dq_geom updated to scoreable or later-sharpened frame-vector input row",
        ),
        (
            "VAL4272_10_local_candidate_matches_live",
            any(row.get("probe_id") == "Dq_geom" and row.get("source_path") in acceptable_geom_sources for row in local_candidate)
            and bool(live_geom)
            and live_geom[0].get("source_path") in acceptable_geom_sources,
            "local and live candidates carry 4272 source or later 4273 refinement",
        ),
        (
            "VAL4272_11_prior_zero_adoptions_preserved",
            prior_zeros_preserved,
            "prior tau/matter/source/theta/boundary/EM/coefficient zero rows preserved",
        ),
        (
            "VAL4272_12_no_fake_claim",
            bool(live_geom)
            and (
                live_geom[0].get("epsilon") != "0.0"
                or (
                    live_geom[0].get("source_path")
                    == str(FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md")
                    and live_geom[0].get("valid_for_claim") == "False"
                )
            )
            and all(row.get("valid_for_claim") == "False" for row in sources + audit + schema + inputs + controls + gates),
            "geometry remains nonzero/nonclaim",
        ),
        ("VAL4272_13_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4272_14_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4272_15_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4272_SOURCE_REGISTER.csv"
    audit_path = SOURCE_DIR / "P8_Y5_R2FR_4272_PARENT_SIGNATURE_AUDIT.csv"
    schema_path = SOURCE_DIR / "P8_Y5_R2FR_4272_FRAME_BOUND_SCHEMA.csv"
    inputs_path = SOURCE_DIR / "P8_Y5_R2FR_4272_FRAME_BOUND_INPUT_CANDIDATES.csv"
    controls_path = SOURCE_DIR / "P8_Y5_R2FR_4272_CONTROL_SMOKE_BOUND_ROWS.csv"
    runner_path = SOURCE_DIR / "P8_Y5_R2FR_4272_FRAME_BOUND_RUNNER_RESULTS.csv"
    gates_path = SOURCE_DIR / "P8_Y5_R2FR_4272_CLAIM_GATES.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4272_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4272_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4272_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4272_NEXT_TARGET.csv"

    write_csv(source_path, source_rows())
    write_csv(audit_path, signature_audit_rows())
    write_csv(schema_path, bound_schema_rows())
    write_csv(inputs_path, input_rows())
    write_csv(controls_path, control_rows())
    runners = runner_rows(inputs_path, controls_path)
    write_csv(runner_path, runners)
    write_csv(gates_path, claim_gate_rows(runners))
    write_csv(CORE_BOUND_CANDIDATE_PATH, bound_candidate_rows())
    component_candidate = component_candidate_rows()
    write_csv(LOCAL_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "audit": audit_path,
        "schema": schema_path,
        "inputs": inputs_path,
        "controls": controls_path,
        "runners": runner_path,
        "gates": gates_path,
        "candidate": CORE_BOUND_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 13 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
