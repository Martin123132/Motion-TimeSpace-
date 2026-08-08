from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_GK_QLOC_HELMHOLTZ_CURRENT_SPINE_4114"
CHECKPOINT_ID = "4114"
DECISION = "GK_QLOC_STRESS_IDENTITY_AND_CONDITIONAL_SGK_ROUTE_IMPORTED_SCALAR_DENSITY_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4114_00_4113_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4113_NEXT_TARGET.csv",
        "4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md",
        "4113 selected Gamma/Khat response-action Helmholtz as next target.",
    ),
    "SRC4114_01_4113_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4113_STATUS.csv",
        "BIANCHI_CONDITIONAL_LAW_AND_RESIDUAL_OWNER_INVENTORY_IMPORTED_GK_ORPHAN_NEXT",
        "Current-chain Bianchi/residual inventory handoff.",
    ),
    "SRC4114_02_3627_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_STATUS.csv",
        "SGK_HELMHOLTZ_ROUTE_CONDITIONAL_BOUND_BRANCH_STAGED_NO_CLAIM",
        "3627 conditional S_GK route and nonclaim bound branch.",
    ),
    "SRC4114_03_3627_action_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_SGK_HELMHOLTZ_ACTION_GATE.csv",
        "HAG3627_6_verdict",
        "S_GK action-existence/Helmholtz gate.",
    ),
    "SRC4114_04_3627_metric_response": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv",
        "MRD3627_3_Helmholtz_obstruction",
        "Gamma_eff scalar-density metric-response candidate.",
    ),
    "SRC4114_05_3627_double_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_EULER_DOUBLE_ZERO_BOUNDARY_GATE.csv",
        "DZ3627_4_boundary",
        "Euler/double-zero/boundary gates for q_loc silence.",
    ),
    "SRC4114_06_3627_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_QLOC_TGK_BOUND_ROWS.csv",
        "QTB3627_5_boundary_flux",
        "q_loc/T_GK nonclaim component-bound rows.",
    ),
    "SRC4114_07_3627_decisions": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_DECISION_GATES.csv",
        "DEC3627_4_next_target",
        "3627 decision selecting explicit scalar-density construction.",
    ),
    "SRC4114_08_3627_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3627_NEXT_TARGET.csv",
        "3628-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md",
        "3627 next target: explicit Gamma_eff scalar-density construction.",
    ),
    "SRC4114_09_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4114_Gamma_Khat_response_action_Helmholtz_or_qloc_TGK_bound.py",
        "Reproducible generator for this 4114 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needle": needle,
                "needle_found": bool_string(path.exists() and needle in text),
                "role": role,
                "claim_allowed": bool_string(False),
                "valid_for_claim": bool_string(False),
            }
        )
    return rows


def stress_identity_rows() -> List[dict]:
    rows = [
        (
            "ID4114_0_TGK",
            "T_GK^{mn}",
            "T_GK^{mn}:=Gamma_eff g^{mn}-K_hat^{mn}",
            "algebraic stress rewrite available",
            "PASS_IDENTITY_NOT_ACTION_PROOF",
        ),
        (
            "ID4114_1_qloc",
            "q_loc^n",
            "q_loc^n:=P_loc nabla_m T_GK^{mn}",
            "q_loc is the projected divergence of the retained GK stress",
            "PASS_IDENTITY_NOT_ZERO_PROOF",
        ),
        (
            "ID4114_2_ward",
            "Ward residual route",
            "if T_GK=-(2/sqrt(-g))delta S_GK/delta g then nabla_m T_GK^{mn}=sum_A E_A nabla^n Phi^A + boundary",
            "local q_loc silence is derived only if Euler and boundary terms vanish",
            "EXACT_CONDITIONAL_NOT_SIGNED",
        ),
        (
            "ID4114_3_claim_guard",
            "closure guard",
            "q_loc=0 cannot be asserted from the stress rewrite alone",
            "requires S_GK action, Helmholtz, double-zero and no-flux gates",
            "NO_SMUGGLING_GUARD",
        ),
    ]
    return [
        {
            **row_base(),
            "identity_id": identity_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_id": "SRC4114_03_3627_action_gate",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for identity_id, obj, formula, meaning, status in rows
    ]


def helmholtz_gate_rows() -> List[dict]:
    rows = [
        ("HAG4114_0_action_existence", "local scalar action exists", "there exists S_GK[g,Phi] with T_GK^{mn}=-(2/sqrt(-g))delta S_GK/delta g_mn", "NOT_SUPPLIED_CURRENT_CORPUS"),
        ("HAG4114_1_Helmholtz", "variational Helmholtz symmetry", "delta(sqrt(-g)T_GK^{mn})/delta g_ab is symmetric as second variation up to boundary terms", "NOT_CHECKED_CURRENT_MTS"),
        ("HAG4114_2_metric_response", "Gamma scalar-density response", "Gamma_eff is covariant scalar density and K_hat equals its metric response under one fixed convention", "BEST_CANDIDATE_NOT_MATCHED_TO_EXISTING_MTS"),
        ("HAG4114_3_positive_auxiliary", "positive auxiliary/no-hair action", "positive source-free operator matches Gamma/Khat pieces and suppresses local hair", "CONDITIONAL_CANDIDATE_NEEDS_SYMBOL_MATCH"),
        ("HAG4114_4_topological", "exact/topological sector", "S_GK=int dB_GK or topological density gives zero bulk stress and fixed/no-flux boundary charge", "BOUNDARY_FLUX_RISK_OPEN"),
        ("HAG4114_5_verdict", "current S_GK proof status", "action-existence, Helmholtz, metric-response, Euler, double-zero, projector and boundary gates all pass", "SGK_NOT_CLAIMED_BOUND_BRANCH_REQUIRED"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "test": test,
            "requirement": requirement,
            "current_status": status,
            "source_id": "SRC4114_03_3627_action_gate",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for gate_id, test, requirement, status in rows
    ]


def metric_response_rows() -> List[dict]:
    rows = [
        (
            "MR4114_0_candidate_action",
            "S_GK=-int d^4x sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "Gamma_eff must be covariant, local, unit-declared and fixed before readout",
            "FORMULA_WRITTEN_NOT_PARENT_MATCHED",
        ),
        (
            "MR4114_1_response_tensor",
            "K_metric^{mn}:=-2 delta Gamma_eff/delta g_mn - convention_terms",
            "one fixed sign/volume convention and derivative/boundary terms must be included",
            "MATCH_MISSING_CURRENT_CORPUS",
        ),
        (
            "MR4114_2_comparison",
            "DeltaK^{mn}:=K_hat^{mn}-K_metric^{mn}",
            "DeltaK must be zero, pure boundary/topological, or retained as coefficient row",
            "NEXT_COMPUTATION_TARGET",
        ),
        (
            "MR4114_3_obstruction",
            "delta(sqrt(-g)(Gamma g-Khat)^{mn})/delta g_ab != symmetric second variation => no S_GK",
            "if Helmholtz fails, demote q_loc/T_GK to finite bound rows",
            "OBSTRUCTION_NOT_RESOLVED",
        ),
    ]
    return [
        {
            **row_base(),
            "response_id": response_id,
            "formula": formula,
            "condition_or_use": condition,
            "current_status": status,
            "source_id": "SRC4114_04_3627_metric_response",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for response_id, formula, condition, status in rows
    ]


def double_zero_boundary_rows() -> List[dict]:
    rows = [
        ("DZ4114_0_background", "Gamma_eff(Phi0) constant and absorbed into Lambda_eff/background subtraction", "no local force from fixed-point value", "CONDITIONAL_STANDARD_NOT_PARENT_MATCHED"),
        ("DZ4114_1_stress_value", "T_GK^{mn}(Phi0)=0 or pure background", "no zeroth-order local metric/source residual", "NOT_MATCHED_CURRENT_CORPUS"),
        ("DZ4114_2_first_variation", "partial_A T_GK^{mn}(Phi0)=0", "linear PPN/fifth-force/source-normalization leakage absent", "F1_NOT_PROVED"),
        ("DZ4114_3_positive_operator", "extra-field operator has positive Hessian/gap and no source term", "compact local exterior gives zero/exponentially bounded hair", "POSITIVE_OPERATOR_NOT_DERIVED"),
        ("DZ4114_4_boundary", "S_GK boundary/symplectic terms have zero or fixed topological flux", "bulk q_loc zero cannot leak through source mass or radial force", "BOUNDARY_OPEN"),
    ]
    return [
        {
            **row_base(),
            "zero_id": zero_id,
            "required_condition": condition,
            "effect": effect,
            "current_status": status,
            "source_id": "SRC4114_05_3627_double_zero",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for zero_id, condition, effect, status in rows
    ]


def bound_branch_rows() -> List[dict]:
    rows = [
        ("QTB4114_0_compact_proxy", "max |P_loc d_rel J_rel| or q_loc leakage proxy", "7.432631961576971e-06", "dimensionless_proxy", "RETAINED_ANCHOR_PROXY_NONCLAIM"),
        ("QTB4114_1_alpha3", "q_loc preferred-frame alpha3 channel", "MISSING_QLOC_TO_ALPHA3_COEFFICIENT", "dimensionless", "MAPPING_MISSING_BLOCKED"),
        ("QTB4114_2_PPN_metric_tail", "T_GK/q_loc contribution to gamma,beta,xi", "MISSING_WEAK_FIELD_METRIC_SOLUTION", "dimensionless_vector", "PPN_MAPPING_MISSING_BLOCKED"),
        ("QTB4114_3_Newton_source", "T_GK/q_loc contribution to delta_Newton_MTS", "MISSING_PI00_DELTAE_OR_SOURCE_PROFILE", "dimensionless_or_acceleration_profile", "SOURCE_MASS_CLOSURE_MISSING"),
        ("QTB4114_4_TGK_stress_norm", "||T_GK|| local exterior stress norm", "MISSING_TGK_STRESS_NORM_OR_ZERO_THEOREM", "stress_or_metric_response_units", "STRESS_NORM_MISSING_BLOCKED"),
        ("QTB4114_5_boundary_flux", "S_GK boundary/symplectic flux", "MISSING_BOUNDARY_FLUX_OR_NO_FLUX_THEOREM", "flux_over_MH_or_declared_boundary_units", "BOUNDARY_NO_FLUX_MISSING"),
    ]
    return [
        {
            **row_base(),
            "bound_id": bound_id,
            "quantity": quantity,
            "candidate_value": candidate_value,
            "units": units,
            "status": status,
            "source_id": "SRC4114_06_3627_bounds",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for bound_id, quantity, candidate_value, units, status in rows
    ]


def decision_rows() -> List[dict]:
    rows = [
        ("DEC4114_0_identity", "q_loc is exactly the projected divergence of T_GK once T_GK=Gamma_eff g-K_hat is defined.", "ALGEBRAIC_PROGRESS_IMPORTED", "use this as residual definition whether or not S_GK exists"),
        ("DEC4114_1_action_route", "Least-scrutiny derivation route is Gamma_eff as covariant scalar density and K_hat as its metric response.", "BEST_ROUTE_SELECTED_NOT_CLOSED", "construct explicit Gamma_eff scalar density and compute K_metric"),
        ("DEC4114_2_claim_guard", "Current corpus does not prove S_GK action-existence, Helmholtz symmetry, metric-response match, double-zero, or boundary no-flux.", "SGK_NOT_CLAIMED", "do not claim local q_loc/T_GK silence"),
        ("DEC4114_3_bound_branch", "q_loc/T_GK component-bound rows are staged and remain nonclaim.", "BOUND_BRANCH_STAGED_NOT_SCORED", "fill weak-field projection, stress norm and source-backed bounds if action route fails"),
        ("DEC4114_4_next", "Next current-chain target is explicit Gamma_eff scalar-density construction or bound runner.", "NEXT_TARGET_SELECTED", "4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md"),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "next_action": next_action,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for decision_id, decision, status, next_action in rows
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4114_0",
            "target_doc": "4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_4115_SGK_explicit_scalar_density_construction_or_bound_runner.py",
            "objective": "attempt an explicit Gamma_eff scalar-density construction, compute the corresponding K_metric response, compare it to K_hat, and either sign the metric-response owner or demote q_loc/T_GK to the nonclaim bound runner",
            "success_gate": "Gamma_eff has declared fields, units and covariance; K_metric is computed with boundary terms; K_hat-K_metric is zero or retained as coefficient row; F1/double-zero and boundary gates are evaluated",
            "reason": "4114 shows the route is mathematically clean but unsigned; the next real leap is an explicit scalar-density object, not another generic gate.",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4114_0",
            "decision": DECISION,
            "strongest_result": "4114 imports the exact GK/q_loc stress identity and the conditional variational S_GK route into the active spine. q_loc can be a Ward residual if Gamma_eff is an owned scalar-density action and K_hat is its metric response, but the action/Helmholtz/double-zero/boundary gates are not signed.",
            "what_changed": "The hard orphan is no longer vague: either construct Gamma_eff as an explicit covariant scalar density and compute K_metric, or demote q_loc/T_GK to component-bound rows.",
            "still_missing": "explicit Gamma_eff fields/units/covariance, K_metric computation, K_hat-K_metric comparison, Helmholtz symmetry, F1/double-zero, positive operator, boundary no-flux, and PPN/Newton projection coefficients",
            "claim_state": "no SGK_q_loc_TGK_local_GR_PPN_Newton_R10_R11 claim",
            "next_target": "4115 SGK explicit scalar-density construction or bound runner",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4114_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4114_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4114_GK_QLOC_STRESS_IDENTITY": SOURCE_DIR / "P8_Y5_R2FR_4114_GK_QLOC_STRESS_IDENTITY.csv",
        "P8_Y5_R2FR_4114_SGK_HELMHOLTZ_GATE": SOURCE_DIR / "P8_Y5_R2FR_4114_SGK_HELMHOLTZ_GATE.csv",
        "P8_Y5_R2FR_4114_METRIC_RESPONSE_ROUTE": SOURCE_DIR / "P8_Y5_R2FR_4114_METRIC_RESPONSE_ROUTE.csv",
        "P8_Y5_R2FR_4114_DOUBLE_ZERO_BOUNDARY_GATE": SOURCE_DIR / "P8_Y5_R2FR_4114_DOUBLE_ZERO_BOUNDARY_GATE.csv",
        "P8_Y5_R2FR_4114_QLOC_TGK_BOUND_BRANCH": SOURCE_DIR / "P8_Y5_R2FR_4114_QLOC_TGK_BOUND_BRANCH.csv",
        "P8_Y5_R2FR_4114_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4114_DECISION_GATE.csv",
        "P8_Y5_R2FR_4114_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4114_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4114_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4114_STATUS.csv",
    }


def markdown_table(rows: List[dict], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    status = status_rows()[0]
    lines = [
        "# 4114 - Gamma/Khat response action Helmholtz or q_loc/T_GK bound",
        "",
        "## Verdict",
        "4114 imports the `3627` GK/q_loc action-existence work into the active `411x` spine. The route is mathematically clean but not yet signed: `q_loc` is a Ward residual only if `Gamma_eff` is an owned scalar-density action and `K_hat` is its metric response.",
        "",
        "No `S_GK`, `q_loc=0`, `T_GK=0`, PPN, Newton, R10/R11, source-normalization, or local-GR claim follows.",
        "",
        "## Strongest Current Result",
        f"- `{status['decision']}`",
        f"- {status['strongest_result']}",
        f"- {status['what_changed']}",
        "",
        "## GK / q_loc Stress Identity",
        markdown_table(stress_identity_rows(), ["identity_id", "object", "formula", "meaning", "status"]),
        "",
        "## Helmholtz / Action Gate",
        markdown_table(helmholtz_gate_rows(), ["gate_id", "test", "requirement", "current_status"]),
        "",
        "## Metric-Response Route",
        markdown_table(metric_response_rows(), ["response_id", "formula", "condition_or_use", "current_status"]),
        "",
        "## Double-Zero / Boundary Gate",
        markdown_table(double_zero_boundary_rows(), ["zero_id", "required_condition", "effect", "current_status"]),
        "",
        "## q_loc / T_GK Bound Branch",
        markdown_table(bound_branch_rows(), ["bound_id", "quantity", "candidate_value", "units", "status"]),
        "",
        "## Decisions",
        markdown_table(decision_rows(), ["decision_id", "decision", "status", "next_action"]),
        "",
        "## Next Target",
        markdown_table(next_target_rows(), ["target_doc", "target_script", "objective", "success_gate"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4114_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_GK_QLOC_STRESS_IDENTITY"], stress_identity_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_SGK_HELMHOLTZ_GATE"], helmholtz_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_METRIC_RESPONSE_ROUTE"], metric_response_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_DOUBLE_ZERO_BOUNDARY_GATE"], double_zero_boundary_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_QLOC_TGK_BOUND_BRANCH"], bound_branch_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4114_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({**row_base(), "check_id": check_id, "check": check, "passed": bool_string(passed), "detail": detail, "claim_allowed": bool_string(False)})

    missing_sources = [source_id for source_id, (path, _, _) in LOCAL_SOURCES.items() if not path.exists()]
    missing_needles = []
    for source_id, (path, needle, _) in LOCAL_SOURCES.items():
        if path.exists() and needle not in read_text(path):
            missing_needles.append(f"{source_id}:{needle}")
    add("VAL4114_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4114_1_sources_contain_needles", "every local source contains expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_ok = True
    parse_counts = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4114_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    identity_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4114_GK_QLOC_STRESS_IDENTITY"]))
    identity_ok = all(token in identity_text for token in ["T_GK", "q_loc", "Ward", "NO_SMUGGLING_GUARD"])
    add("VAL4114_3_identity", "GK/q_loc stress identity present", identity_ok, "identity tokens checked")

    helmholtz_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4114_SGK_HELMHOLTZ_GATE"]))
    helmholtz_ok = all(token in helmholtz_text for token in ["Helmholtz", "metric-response", "SGK_NOT_CLAIMED", "BOUNDARY"])
    add("VAL4114_4_helmholtz", "S_GK Helmholtz/action gate blocks claim", helmholtz_ok, "Helmholtz tokens checked")

    response_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4114_METRIC_RESPONSE_ROUTE"]))
    response_ok = all(token in response_text for token in ["Gamma_eff", "K_metric", "DeltaK", "OBSTRUCTION"])
    add("VAL4114_5_metric_response", "metric-response route names explicit next computation", response_ok, "response tokens checked")

    zero_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4114_DOUBLE_ZERO_BOUNDARY_GATE"]))
    zero_ok = all(token in zero_text for token in ["partial_A", "positive Hessian", "boundary", "F1_NOT_PROVED"])
    add("VAL4114_6_double_zero", "double-zero and boundary gates retained", zero_ok, "double-zero tokens checked")

    bound_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4114_QLOC_TGK_BOUND_BRANCH"]))
    bound_ok = all(token in bound_text for token in ["7.432631961576971e-06", "alpha3", "gamma,beta,xi", "BOUNDARY_NO_FLUX_MISSING"])
    add("VAL4114_7_bound_branch", "q_loc/T_GK bound branch staged nonclaim", bound_ok, "bound tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4114_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md"
    add("VAL4114_8_next_target", "next target is 4115 explicit scalar-density construction", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4114_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("decision") == DECISION and "no SGK" in status_rows_local[0].get("claim_state", "")
    add("VAL4114_9_status", "status records GK/q_loc route and no-claim state", status_ok, "status row checked")

    all_rows = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") for row in all_rows)
    add("VAL4114_10_no_claim_flags", "all generated rows remain no-claim", no_claim, f"row_count={len(all_rows)}")

    output_paths = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4114*")) or any(FORMALIZATION.rglob("4114-Y5-R2FR*"))
    add("VAL4114_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4114_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4114_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
