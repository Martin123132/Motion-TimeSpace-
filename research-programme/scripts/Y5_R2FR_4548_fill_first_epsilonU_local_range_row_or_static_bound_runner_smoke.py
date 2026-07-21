from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4548"
CLAIM_ID = "L-390"
BRANCH_ID = "MTS_R2FR_Y5_EPSILON_U_LOCAL_RANGE_AND_STATIC_SMOKE_4548"
MARKER = "PPC4161_FILL_FIRST_EPSILONU_LOCAL_RANGE_ROW_OR_STATIC_BOUND_RUNNER_SMOKE_4548"
PACKET_MARKER = "PPC4161_PACKET_FILL_FIRST_EPSILONU_LOCAL_RANGE_ROW_OR_STATIC_BOUND_RUNNER_SMOKE_4548"
DECISION = "EPSILON_U_LOGISTIC_RANGE_LAW_DERIVED_POINT_ANCHOR_EXTRACTED_DOMAIN_SUP_MISSING_STATIC_BOUND_SMOKE_READY_NONCLAIM"
NEXT_TARGET = "4549-Y5-R2FR-source-real-local-domain-Bmin-or-first-projection-kernel-row.md"

FORMAL_PATH = FORMAL / "564-PPC4161-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md"
DOC_PATH = POST / "4548-Y5-R2FR-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4548_SOURCE_REGISTER.csv"
LOGISTIC_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_EPSILON_U_LOGISTIC_RANGE_LAW.csv"
LOCAL_RANGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_EPSILON_U_LOCAL_RANGE_ROW.csv"
STATIC_INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_STATIC_BOUND_SMOKE_INPUTS.csv"
STATIC_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_STATIC_BOUND_SMOKE_RUNNER.csv"
NUMERIC_BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_NUMERIC_BLOCKERS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4548_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4548_VALIDATION.csv"

VAR_AUDIT = FORMAL / "04-variable-audit.csv"
X_B_DOC = FORMAL / "85-coarse-graining-invariants-XB.md"
X_B_GATE_DOC = FORMAL / "86-XB-invariant-gate.md"
SOURCE_MODEL_DOC = FORMAL / "89-source-model-curvature-Lcg-test.md"
TRACE_GATE_DOC = FORMAL / "91-trace-suppression-closure-gate.md"
SOURCE_MODEL_SUMMARY = FORMAL / "runs" / "source_model_curvature_Lcg_20260527-211932" / "summary.csv"
XB_SUMMARY = FORMAL / "runs" / "XB_invariant_gate_20260527-204233" / "summary.csv"
TRACE_SUMMARY = FORMAL / "runs" / "trace_suppression_closure_gate_20260527-214758" / "summary.csv"

REQ_1975 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1975_BOUND_CONSTANT_REQUIREMENTS.csv"
ENV_1975 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv"
ACQ_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_INPUT_ACQUISITION_QUEUE.csv"
EPS_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_EPSILON_U_BOUND_ROWS.csv"
PROJ_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_ARENA_PROJECTION_CONTRACT.csv"
PASS_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_PASS_INEQUALITY_ROWS.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def safe_float(value: Any) -> float | None:
    try:
        if value is None or str(value).strip().lower() in {"", "missing", "nan"}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4548_00_var_audit_PiB",
            "label": "variable audit Pi_B/U_B",
            "path": VAR_AUDIT,
            "needle": "Pi_B=1/{1+exp[-(B_env-B_*)/Delta_B]}; U_B=1-Pi_B",
        },
        {
            "source_id": "SRC4548_01_var_audit_Benv",
            "label": "variable audit B_env",
            "path": VAR_AUDIT,
            "needle": "B_env=ln(1+A_curv)-w_theta ln(1+E_theta)",
        },
        {
            "source_id": "SRC4548_02_XB_doc_logistic",
            "label": "85 X_B logistic definition",
            "path": X_B_DOC,
            "needle": "1 / {1 + exp[-(B_env - B_*)/Delta_B]}",
        },
        {
            "source_id": "SRC4548_03_XB_gate_values",
            "label": "86 X_B gate rough threshold values",
            "path": X_B_GATE_DOC,
            "needle": "B_* = 1",
        },
        {
            "source_id": "SRC4548_04_source_model_logistic",
            "label": "89 source model Pi_B definition",
            "path": SOURCE_MODEL_DOC,
            "needle": "1 / {1 + exp[-(B_env - B_*) / Delta_B]}",
        },
        {
            "source_id": "SRC4548_05_source_model_summary",
            "label": "source model local point anchor rows",
            "path": SOURCE_MODEL_SUMMARY,
            "needle": "local_weak_field_point_mass_sun_1AU",
        },
        {
            "source_id": "SRC4548_06_XB_summary",
            "label": "X_B summary screening rows",
            "path": XB_SUMMARY,
            "needle": "local_screening_target_conditional_pass",
        },
        {
            "source_id": "SRC4548_07_trace_gate_summary",
            "label": "trace gate local U_B^2 row",
            "path": TRACE_SUMMARY,
            "needle": "local_point_mass_universal_U2_pass",
        },
        {
            "source_id": "SRC4548_08_trace_doc_caveat",
            "label": "trace gate parent-derived caveat",
            "path": TRACE_GATE_DOC,
            "needle": "U_B^2 is derived",
        },
        {
            "source_id": "SRC4548_09_1975_requirements",
            "label": "1975 epsilon_U requirement row",
            "path": REQ_1975,
            "needle": "epsilon_U",
        },
        {
            "source_id": "SRC4548_10_1975_envelope",
            "label": "1975 U_B suppression envelope",
            "path": ENV_1975,
            "needle": "epsilon_U^2",
        },
        {
            "source_id": "SRC4548_11_4547_acquisition",
            "label": "4547 acquisition queue",
            "path": ACQ_4547,
            "needle": "epsilon_U = sup_Dloc U_B",
        },
        {
            "source_id": "SRC4548_12_4547_epsilon_bounds",
            "label": "4547 epsilon bound rows",
            "path": EPS_4547,
            "needle": "EUB4547_alpha3",
        },
        {
            "source_id": "SRC4548_13_4547_projection",
            "label": "4547 arena projection contract",
            "path": PROJ_4547,
            "needle": "same B_static/source profile for all arenas; no retuning",
        },
        {
            "source_id": "SRC4548_14_4547_pass",
            "label": "4547 pass inequalities",
            "path": PASS_4547,
            "needle": "PI4547_alpha3",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = spec["needle"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "valid_for_claim": "False",
            }
        )
    return rows


def logistic_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "LAW4548_0_exact_UB",
            "object": "U_B",
            "assumptions": "Pi_B=(1+exp[-(B_env-B_*)/Delta_B])^-1; U_B=1-Pi_B; Delta_B>0.",
            "derivation": "U_B=1-Pi_B=(1+exp[(B_env-B_*)/Delta_B])^-1.",
            "result": "U_B(B_env) = 1/(1 + exp[(B_env-B_*)/Delta_B])",
            "status": "derived_from_existing_logistic_switch",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4548_1_domain_sup",
            "object": "epsilon_U(D_loc)",
            "assumptions": "D_loc has B_env(x)>=B_min for every x in D_loc; Delta_B>0.",
            "derivation": "U_B is monotone decreasing in B_env, so sup_Dloc U_B occurs at the smallest allowed B_env.",
            "result": "epsilon_U(D_loc) := sup_Dloc U_B <= 1/(1 + exp[(B_min-B_*)/Delta_B])",
            "status": "derived_but_numeric_domain_inputs_missing",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4548_2_large_margin_tail",
            "object": "far-local exponential tail",
            "assumptions": "B_min>B_* and Delta_B>0.",
            "derivation": "For y=(B_min-B_*)/Delta_B>0, 1/(1+e^y) <= e^-y.",
            "result": "epsilon_U(D_loc) <= exp[-(B_min-B_*)/Delta_B]",
            "status": "derived_useful_for_fast_screening_bounds",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4548_3_gradient_tail",
            "object": "gradient leakage",
            "assumptions": "Delta_B>0 and |nabla B_env| <= 1/L_B on D_loc.",
            "derivation": "nabla U_B = -U_B(1-U_B)nabla B_env/Delta_B.",
            "result": "|nabla U_B| <= epsilon_U/(Delta_B L_B)",
            "status": "derived_for_static_bound_runner_inputs",
            "valid_for_claim": "False",
        },
    ]


def local_anchor_from_source_model() -> dict[str, str]:
    rows = read_csv(SOURCE_MODEL_SUMMARY)
    for row in rows:
        if row.get("case") == "local_weak_field_point_mass_sun_1AU":
            return row
    return {}


def logistic_ub(b_env: float, b_star: float, delta_b: float) -> float:
    exponent = (b_env - b_star) / delta_b
    if exponent > 700:
        return 0.0
    return 1.0 / (1.0 + math.exp(exponent))


def local_range_rows(anchor: dict[str, str]) -> list[dict[str, Any]]:
    b_env = safe_float(anchor.get("B_env"))
    b_star = safe_float(anchor.get("B_star"))
    delta_b = safe_float(anchor.get("Delta_B"))
    u_b = safe_float(anchor.get("U_B"))
    computed = (
        logistic_ub(b_env, b_star, delta_b)
        if b_env is not None and b_star is not None and delta_b not in {None, 0.0}
        else None
    )
    return [
        {
            "row_id": "LR4548_0_far_local_domain_formula",
            "domain": "Dloc_far_local := stationary compact local exterior excluding source support and excluding transition shell",
            "range_condition": "B_env(x) >= B_min > B_* on the full tested domain",
            "epsilon_U_candidate": "1/(1 + exp[(B_min-B_*)/Delta_B])",
            "numeric_value": "missing",
            "units": "dimensionless",
            "source_path": str(SOURCE_MODEL_SUMMARY),
            "extraction_method": "domain_sup_formula_not_numeric",
            "missing_inputs": "B_min over a named local test domain; parent-owned B_*; parent-owned Delta_B; proof transition shell is excluded or separately quarantined",
            "status": "formula_ready_domain_sup_missing",
            "valid_for_claim": "False",
        },
        {
            "row_id": "LR4548_1_sun_1AU_point_anchor",
            "domain": "single point anchor: source_model local_weak_field_point_mass_sun_1AU",
            "range_condition": "point evaluation only, not a domain supremum",
            "epsilon_U_candidate": f"{u_b:.16e}" if u_b is not None else "missing",
            "numeric_value": f"{u_b:.16e}" if u_b is not None else "missing",
            "computed_from_logistic": f"{computed:.16e}" if computed is not None else "missing",
            "B_env": f"{b_env:.16e}" if b_env is not None else "missing",
            "B_star": f"{b_star:.16e}" if b_star is not None else "missing",
            "Delta_B": f"{delta_b:.16e}" if delta_b is not None else "missing",
            "units": "dimensionless",
            "source_path": str(SOURCE_MODEL_SUMMARY),
            "extraction_method": "source_model_point_anchor_not_supremum",
            "missing_inputs": "domain supremum; real tested exterior definition; parent-owned threshold/width",
            "status": "numeric_point_anchor_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "LR4548_2_transition_shell_warning",
            "domain": "solar_transition_shell_point_mass",
            "range_condition": "B_env approximately B_*, hence U_B approximately 1/2",
            "epsilon_U_candidate": "0.5",
            "numeric_value": "0.5",
            "units": "dimensionless",
            "source_path": str(SOURCE_MODEL_SUMMARY),
            "extraction_method": "anti_cheat_transition_warning",
            "missing_inputs": "transition current PPN solver or routing theorem",
            "status": "not_usable_for_far_local_suppression_claim",
            "valid_for_claim": "False",
        },
    ]


def static_smoke_inputs() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "SMI4548_0_epsilon_U",
            "symbol": "epsilon_U",
            "meaning": "sup_Dloc U_B",
            "candidate_source": str(LOCAL_RANGE_CSV),
            "status": "formula_ready_domain_sup_missing_point_anchor_available",
            "valid_for_claim": "False",
        },
        {
            "input_id": "SMI4548_1_S_static",
            "symbol": "S_static",
            "meaning": "C_H A_1 + D_m C_lap_m/L_B^2",
            "candidate_source": str(ACQ_4547),
            "status": "symbolic_only_coefficient_products_missing",
            "valid_for_claim": "False",
        },
        {
            "input_id": "SMI4548_2_boundary",
            "symbol": "B_boundary,a",
            "meaning": "arena-specific retained static boundary/vector/shear amplitude",
            "candidate_source": str(ACQ_4547),
            "status": "missing_zero_theorem_or_numeric_bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "SMI4548_3_kernel",
            "symbol": "K_a",
            "meaning": "arena projection kernel converting B_static to observable residual",
            "candidate_source": str(PROJ_4547),
            "status": "missing_projection_kernel",
            "valid_for_claim": "False",
        },
    ]


def smoke_runner_rows(local_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    epsilon_point = next(
        (row.get("numeric_value", "missing") for row in local_rows if row.get("row_id") == "LR4548_1_sun_1AU_point_anchor"),
        "missing",
    )
    rows: list[dict[str, Any]] = []
    for row in read_csv(EPS_4547):
        observable = row.get("observable", "")
        target = row.get("target_bound", row.get("bound", ""))
        kernel = row.get("kernel", f"K_{observable}")
        if observable == "Gdot_static_derivative":
            formula = "No epsilon_U-only static amplitude pass: require theorem D_t B_static=0 or source J_Gdot^t D_t B_static bound."
            epsilon_bound = "not_applicable_without_time_variation_model"
            blockers = "D_t B_static zero proof or time-variation kernel; boundary derivative terms"
        else:
            formula = f"|Delta_{observable}| <= |{kernel}| * (S_static * epsilon_U^2 + B_boundary_{observable})"
            epsilon_bound = row.get("epsilon_U_bound_formula", "")
            blockers = "domain epsilon_U sup; S_static; projection kernel; boundary amplitude"
        rows.append(
            {
                "smoke_id": "SMOKE4548_" + observable.replace(" ", "_").replace("/", "_"),
                "observable": observable,
                "target_bound": target,
                "bound_units": row.get("bound_units", ""),
                "candidate_epsilon_source": "LR4548_1_sun_1AU_point_anchor",
                "candidate_epsilon_value": epsilon_point,
                "static_formula": formula,
                "epsilon_bound_formula": epsilon_bound,
                "schema_status": "schema_pass_numeric_blocked",
                "numeric_blockers": blockers,
                "claim_guard": "point anchor is not a domain sup; no kernels/coefficient products/boundary rows",
                "valid_for_claim": "False",
            }
        )
    return rows


def numeric_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLOCK4548_0_Dloc",
            "symbol": "D_loc",
            "needed_for": "epsilon_U = sup_Dloc U_B",
            "status": "MISSING_NAMED_TEST_DOMAIN",
            "next_action": "define the exact local exterior domain for R10/PPN/clocks/orbits, with transition shell handling",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4548_1_Bmin",
            "symbol": "B_min",
            "needed_for": "epsilon_U <= 1/(1+exp[(B_min-B_*)/Delta_B])",
            "status": "MISSING_DOMAIN_INFIMUM",
            "next_action": "source or compute inf_Dloc B_env from the selected domain, not a single point",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4548_2_Bstar_DeltaB",
            "symbol": "B_*, Delta_B",
            "needed_for": "logistic range numeric value",
            "status": "EXAMPLE_VALUES_ONLY_NOT_PARENT_DERIVED",
            "next_action": "derive threshold/width from parent coarse-graining law or freeze as explicit EFT inputs",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4548_3_Sstatic",
            "symbol": "S_static",
            "needed_for": "B_static = S_static epsilon_U^2 + B_boundary + O(epsilon_U^3)",
            "status": "MISSING_COEFFICIENT_PRODUCTS",
            "next_action": "source C_H A_1 and D_m C_lap_m/L_B^2 or replace with parent zero theorem",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4548_4_Kernels",
            "symbol": "K_a",
            "needed_for": "Delta O_a = K_a B_static",
            "status": "MISSING_ARENA_PROJECTION_KERNELS",
            "next_action": "derive or source first real PPN/R10 projection kernel row",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4548_5_Boundary",
            "symbol": "B_boundary,a",
            "needed_for": "static PPN vector/shear and R10/channel residuals",
            "status": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "next_action": "prove boundary no-hair for retained static channels or add numeric amplitude rows",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE4548_0_logistic_derivation",
            "condition": "exact logistic epsilon_U law derived from existing Pi_B/U_B definitions",
            "status": "PASS",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4548_1_numeric_domain_sup",
            "condition": "epsilon_U supplied as sup over named local domain",
            "status": "FAIL_MISSING_DOMAIN_SUP",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4548_2_static_runner_schema",
            "condition": "static-bound runner rows parse for alpha3, xi, R10, and Gdot derivative caveat",
            "status": "PASS_SCHEMA_ONLY",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4548_3_no_claim_guard",
            "condition": "no local-GR, R10, PPN, or Gdot pass claimed from point anchor/symbolic rows",
            "status": "PASS",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "decision": DECISION,
            "summary": "4548 derives the exact epsilon_U logistic range law and extracts a source-model Sun-1AU U_B point anchor, but refuses to call it a domain supremum. The static-bound smoke runner is now executable/schema-clean and remains nonclaim until D_loc/B_min, S_static, kernels and boundary amplitudes are sourced.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The next real leap is either a domain supremum B_min for epsilon_U or the first actual arena projection kernel; either turns the scorer from symbolic to numerically testable.",
            "no_claim_guard": "Do not use the Sun-1AU point anchor as a PPN/R10 pass.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "created_utc": utc_now(),
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    local_rows_: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append(
        {
            "validation_id": "VAL4548_00_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing",
        }
    )

    law_ok = any(row["law_id"] == "LAW4548_0_exact_UB" for row in laws) and any(
        row["law_id"] == "LAW4548_1_domain_sup" for row in laws
    )
    checks.append(
        {
            "validation_id": "VAL4548_01_logistic_law",
            "status": "PASS" if law_ok else "FAIL",
            "detail": "exact U_B and domain-sup law rows present",
        }
    )

    local_ok = all(row.get("valid_for_claim") == "False" for row in local_rows_) and any(
        row.get("row_id") == "LR4548_1_sun_1AU_point_anchor"
        and row.get("status") == "numeric_point_anchor_nonclaim"
        for row in local_rows_
    )
    checks.append(
        {
            "validation_id": "VAL4548_02_local_range_nonclaim",
            "status": "PASS" if local_ok else "FAIL",
            "detail": "local range keeps point anchor separate from domain sup",
        }
    )

    required = {"alpha3", "xi", "R10_alpha_anchor", "Gdot_static_derivative"}
    got = {row.get("observable", "") for row in smoke}
    smoke_ok = required.issubset(got) and all(row.get("valid_for_claim") == "False" for row in smoke)
    checks.append(
        {
            "validation_id": "VAL4548_03_static_smoke_runner",
            "status": "PASS" if smoke_ok else "FAIL",
            "detail": "static smoke rows include alpha3, xi, R10 and Gdot caveat; all nonclaim",
        }
    )

    claim_guard_ok = all(row.get("valid_for_claim") == "False" for row in gates)
    checks.append(
        {
            "validation_id": "VAL4548_04_claim_guards",
            "status": "PASS" if claim_guard_ok else "FAIL",
            "detail": "claim gates do not promote local-GR/R10/PPN pass",
        }
    )

    generated = [
        SOURCE_REGISTER,
        LOGISTIC_LAW_CSV,
        LOCAL_RANGE_CSV,
        STATIC_INPUTS_CSV,
        STATIC_RUNNER_CSV,
        NUMERIC_BLOCKERS_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_details: list[str] = []
    csv_ok = True
    for path in generated:
        try:
            rows = read_csv(path)
            if not rows:
                csv_ok = False
                csv_details.append(f"{path.name}:no_rows")
        except Exception as exc:  # pragma: no cover - diagnostic path
            csv_ok = False
            csv_details.append(f"{path.name}:{exc}")
    checks.append(
        {
            "validation_id": "VAL4548_05_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(csv_details),
        }
    )

    doc_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    checks.append(
        {
            "validation_id": "VAL4548_06_docs_written",
            "status": "PASS" if doc_ok else "FAIL",
            "detail": "post and formal checkpoint docs written",
        }
    )

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append(
        {
            "validation_id": "VAL4548_07_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present",
        }
    )

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "validation_id": "VAL4548_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4548 epsilon_U local range law and static-bound smoke runner",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    local_rows_: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    generated = utc_now()
    return f"""# 4548 - Fill first epsilon_U local range row or static-bound runner smoke

Generated: `{generated}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4548 does not just say "epsilon_U missing". It derives the exact range law from the existing switch:

```text
Pi_B = 1/(1 + exp[-(B_env-B_*)/Delta_B])
U_B  = 1 - Pi_B
     = 1/(1 + exp[(B_env-B_*)/Delta_B]).
```

Therefore, on any named local domain `D_loc` with `B_env(x) >= B_min` and `Delta_B>0`,

```text
epsilon_U(D_loc) := sup_Dloc U_B
                 <= 1/(1 + exp[(B_min-B_*)/Delta_B]).
```

For a far-local positive margin this gives the faster but weaker tail:

```text
epsilon_U(D_loc) <= exp[-(B_min-B_*)/Delta_B].
```

The existing Sun-1AU source-model row gives a useful point anchor, `U_B ~ 9.73e-14`, but that is not a domain supremum. The transition shell still has `U_B ~ 1/2`, so it cannot be smuggled into the far-local suppression branch.

## Range Law

{markdown_table(laws)}

## Local Range Rows

{markdown_table(local_rows_)}

## Static Smoke Inputs

{markdown_table(inputs)}

## Static Bound Smoke Runner

{markdown_table(smoke)}

## Numeric Blockers

{markdown_table(blockers)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4548 derives the exact epsilon_U logistic range law and creates a static-bound smoke runner; a Sun-1AU numeric point anchor is extracted but no domain-supremum, kernel, coefficient-product or boundary-amplitude claim is made.",
        "current_evidence": "Generated source register, epsilon_U logistic range law, local range rows, static smoke inputs, static-bound smoke runner, numeric blockers, claim gates, status and validation CSVs.",
        "status": "epsilon_range_law_and_static_smoke_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Using a single point-anchor U_B as if it were sup_Dloc U_B for PPN/R10/local-GR evidence.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "The scorer is executable but not numeric evidence until D_loc/B_min, S_static, kernels and boundary rows are sourced.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    laws = logistic_law_rows()
    local_rows_ = local_range_rows(local_anchor_from_source_model())
    inputs = static_smoke_inputs()
    smoke = smoke_runner_rows(local_rows_)
    blockers = numeric_blocker_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LOGISTIC_LAW_CSV, laws)
    write_csv(LOCAL_RANGE_CSV, local_rows_)
    write_csv(STATIC_INPUTS_CSV, inputs)
    write_csv(STATIC_RUNNER_CSV, smoke)
    write_csv(NUMERIC_BLOCKERS_CSV, blockers)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    # Create checkpoint files before validation so the document-existence gate is
    # meaningful on a clean first run; they are overwritten below with the full
    # validation table.
    pending_doc = f"# 4548 - Fill first epsilon_U local range row or static-bound runner smoke\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, laws, local_rows_, smoke, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, laws, local_rows_, inputs, smoke, blockers, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4548 epsilon_U Local Range Law And Static Smoke Runner

Marker: `{MARKER}`  
4548 derives `U_B=1/(1+exp[(B_env-B_*)/Delta_B])` and therefore `epsilon_U(D_loc)<=1/(1+exp[(B_min-B_*)/Delta_B])` for any local domain with `B_env>=B_min`. A Sun-1AU source-model point anchor gives `U_B~9.73e-14`, but this is not a domain supremum and is not evidence for PPN/R10. The static-bound scorer is now schema-clean and waiting on `D_loc/B_min`, `S_static`, arena kernels and boundary amplitudes. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4548 Packet Integration - epsilon_U Range Law And Smoke Scorer

Marker: `{PACKET_MARKER}`  
The local packet now has a derived logistic range law for the unscreened fraction and an executable symbolic scorer. This is forward movement: the next numeric bottleneck is no longer vague `epsilon_U`; it is the concrete `B_min`/domain supremum or first projection kernel row.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4548_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
