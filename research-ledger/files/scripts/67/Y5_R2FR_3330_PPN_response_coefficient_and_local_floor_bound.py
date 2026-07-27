from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md"

SRC_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
SRC_COMPACT = REPO / "core-mts-framework" / "gravity" / "gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md"
SRC_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"

SOURCES = [
    {
        "source_id": "SRC3330_0_3329_doc",
        "path": ROOT / "3329-Y5-R2FR-local-residual-budget-input-prioritizer-and-minimal-numeric-smoke-under-AX1090.md",
        "role": "PPN smoke and next target",
    },
    {
        "source_id": "SRC3330_1_3329_smoke",
        "path": OUT / "P8_Y5_R2FR_3329_PPN_NUMERIC_SMOKE.csv",
        "role": "placeholder PPN smoke scenarios",
    },
    {
        "source_id": "SRC3330_2_3329_priority",
        "path": OUT / "P8_Y5_R2FR_3329_INPUT_PRIORITY.csv",
        "role": "C_PPN / epsilon_eff / composite / Gamma priority order",
    },
    {
        "source_id": "SRC3330_3_3328_budget",
        "path": OUT / "P8_Y5_R2FR_3328_RESIDUAL_BUDGET_FORMULAS.csv",
        "role": "master residual budget formulas",
    },
    {
        "source_id": "SRC3330_4_3322_Ci",
        "path": OUT / "P8_Y5_R2FR_3322_CI_RESPONSE_GATE.csv",
        "role": "C_i projection/propagator/source factor split",
    },
    {
        "source_id": "SRC3330_5_3327_envelope",
        "path": OUT / "P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv",
        "role": "composite envelope formulas",
    },
    {
        "source_id": "SRC3330_6_gravity_PPN",
        "path": SRC_GRAVITY,
        "role": "solar PPN K_solar proxy and weak-field statement",
    },
    {
        "source_id": "SRC3330_7_compact_Newton",
        "path": SRC_COMPACT,
        "role": "compact-system Newtonian recovery",
    },
    {
        "source_id": "SRC3330_8_action",
        "path": SRC_ACTION,
        "role": "Gamma_G field equation and GR recovery condition",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3330_SOURCE_REGISTER.csv",
    "ppn_response": OUT / "P8_Y5_R2FR_3330_PPN_RESPONSE_COEFFICIENT.csv",
    "floors": OUT / "P8_Y5_R2FR_3330_LOCAL_FLOOR_BOUNDS.csv",
    "thresholds": OUT / "P8_Y5_R2FR_3330_PPN_THRESHOLD_FORMULAS.csv",
    "inputs": OUT / "P8_Y5_R2FR_3330_REQUIRED_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3330_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3330_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3330_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3330_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
K_SOLAR_PROXY = 1.0e-61
M_MIN_PROXY = 2.0
GAMMA_PROXY = K_SOLAR_PROXY**M_MIN_PROXY


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1400) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def ppn_response_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CPPN3330_0_metric_normalization",
            "quantity": "q_U",
            "formula": "q_U = |U|/c^2 for the PPN source region",
            "derivation": "PPN parameters compare residual spatial/time metric coefficients to the Newtonian potential scale, so an absolute metric residual is amplified by roughly q_U^-1 in gamma/beta observables",
            "status": "RESPONSE_NORMALIZATION_IDENTIFIED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CPPN3330_1_C_metric",
            "quantity": "C_metric",
            "formula": "C_metric(lambda)=||Pi_metric W_PPN||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| x source_normalization",
            "derivation": "specializes the 3322 C_i operator coefficient to weak-field metric components before PPN normalization",
            "status": "SYMBOLIC_OPERATOR_BOUND",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CPPN3330_2_C_PPN",
            "quantity": "C_PPN",
            "formula": "C_PPN <= A_PPN(q_U,gauge) C_metric, with A_PPN(q_U,gauge) ~ O(q_U^-1) to O(q_U^-2) depending on whether the residual enters linearly or quadratically in the PPN observable",
            "derivation": "PPN response coefficient is not a free number; it is metric projection times weak-potential normalization and gauge/observable map",
            "status": "DERIVED_SYMBOLIC_BOUND",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CPPN3330_3_tree_residual",
            "quantity": "R_tree_PPN",
            "formula": "R_tree_PPN <= C_PPN [epsilon_bg T_grad(lambda_PPN)+epsilon_boundary_PPN+epsilon_kernel_aniso_PPN]^2",
            "derivation": "combines 3321 epsilon_eff with the 3330 C_PPN response coefficient",
            "status": "BOUND_FORMULA_READY",
            "valid_for_claim": "false",
        },
    ]


def local_floor_rows() -> list[dict[str, Any]]:
    return [
        {
            "floor_id": "FLOOR3330_0_Gamma_proxy",
            "floor": "R_Gamma_PPN",
            "formula": f"R_Gamma_PPN_proxy <= K_solar^m <= {GAMMA_PROXY:.3e} for K_solar≈1e-61 and m>=2",
            "status": "ENCOURAGING_PROXY_NOT_FULL_BOUND",
            "reason": "core gravity file states PPN corrections O(K^m), but this only signs the curvature-saturation/Gamma proxy if local Gamma maps to that proxy",
            "valid_for_claim": "false",
        },
        {
            "floor_id": "FLOOR3330_1_Gamma_general",
            "floor": "R_Gamma_PPN",
            "formula": "R_Gamma_PPN <= A_Gamma_PPN |Gamma_local| L_PPN^2",
            "status": "GENERAL_BOUND_FORMULA",
            "reason": "a local cosmological-constant-like term contributes through a dimensionless curvature scale Gamma_local times the squared PPN length scale",
            "valid_for_claim": "false",
        },
        {
            "floor_id": "FLOOR3330_2_epsilon_eff",
            "floor": "epsilon_eff_PPN",
            "formula": "epsilon_eff_PPN = epsilon_bg_PPN T_grad(lambda_PPN)+epsilon_boundary_PPN+epsilon_kernel_aniso_PPN",
            "status": "FORMULA_READY_NOT_NUMERIC",
            "reason": "needs epsilon_bg_PPN, ell_s/lambda_PPN, boundary silence, and kernel isotropy",
            "valid_for_claim": "false",
        },
        {
            "floor_id": "FLOOR3330_3_composite",
            "floor": "epsilon_composite_PPN",
            "formula": "epsilon_composite_PPN <= epsilon_1p_PPN + epsilon_2p_PPN + epsilon_contact_PPN + epsilon_boundary_PPN + epsilon_kernel_aniso_PPN",
            "status": "FORMULA_READY_NOT_NUMERIC",
            "reason": "needs 3327 CLT/spectral/contact inputs specialized to PPN",
            "valid_for_claim": "false",
        },
        {
            "floor_id": "FLOOR3330_4_direct",
            "floor": "epsilon_direct_PPN",
            "formula": "epsilon_direct_PPN=0 only if Delta S_direct[psi,matter,EM]=0 in the local branch",
            "status": "BRANCH_SIGNATURE_ZERO_NOT_MICRO_DERIVED",
            "reason": "3325 excludes direct vertices for clean closure but does not derive microscopic matter descent",
            "valid_for_claim": "false",
        },
    ]


def ppn_threshold_rows() -> list[dict[str, Any]]:
    return [
        {
            "threshold_id": "PTH3330_0_master",
            "formula": "R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff_PPN^2 + epsilon_composite_PPN + epsilon_direct_PPN <= B_PPN",
            "use": "claim-ready PPN comparison only after B_PPN and all terms are sourced",
            "status": "MASTER_THRESHOLD_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "PTH3330_1_epsilon_eff",
            "formula": "epsilon_eff_PPN <= sqrt(max(B_PPN-|R_Gamma_PPN|-epsilon_composite_PPN-epsilon_direct_PPN,0)/C_PPN)",
            "use": "allowable first-gradient leakage after floors are reserved",
            "status": "TREE_CHANNEL_THRESHOLD",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "PTH3330_2_floor_budget",
            "formula": "|R_Gamma_PPN| + epsilon_composite_PPN + epsilon_direct_PPN < B_PPN is required before the tree term has any room",
            "use": "diagnoses floor-dominated failure from 3329 smoke",
            "status": "FLOOR_GATE",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "PTH3330_3_claim_rule",
            "formula": "No row is claim-ready unless B_PPN is real, C_PPN is bounded, epsilon_eff_PPN is bounded, and all floors are bounded below B_PPN",
            "use": "prevents smoke numbers being converted into evidence",
            "status": "NO_CLAIM_RULE",
            "valid_for_claim": "false",
        },
    ]


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3330_0_BPPN",
            "quantity": "B_PPN real threshold",
            "needed_for": "replace smoke threshold with sourced PPN bound",
            "current_status": "MISSING_REAL_SOURCE",
            "priority": "medium",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3330_1_qU",
            "quantity": "q_U=|U|/c^2 and PPN gauge/observable map",
            "needed_for": "A_PPN(q_U,gauge) normalization in C_PPN",
            "current_status": "MISSING_ARENA_NORMALIZATION",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3330_2_Cmetric",
            "quantity": "C_metric operator/projection bound",
            "needed_for": "C_PPN",
            "current_status": "MISSING_OPERATOR_NUMERIC",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3330_3_epsilon_eff",
            "quantity": "epsilon_bg_PPN, ell_s/lambda_PPN, epsilon_boundary_PPN, epsilon_kernel_aniso_PPN",
            "needed_for": "epsilon_eff_PPN",
            "current_status": "MISSING_LOCAL_BOUND",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3330_4_composite",
            "quantity": "PPN-specialized CLT/spectral/contact composite inputs",
            "needed_for": "epsilon_composite_PPN",
            "current_status": "MISSING_LOCAL_BOUND",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3330_5_Gamma",
            "quantity": "Gamma_local or proof that R_Gamma_PPN follows K_solar^m proxy",
            "needed_for": "R_Gamma_PPN",
            "current_status": "PROXY_ONLY",
            "priority": "medium",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3330_0_C_PPN_symbolic",
            "claim": "C_PPN response coefficient has a symbolic/operator bound",
            "passed": "true",
            "reason": "C_PPN is decomposed into weak-potential normalization A_PPN and metric operator coefficient C_metric",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3330_1_Gamma_proxy",
            "claim": "Gamma/saturation PPN floor has a tiny corpus proxy",
            "passed": "true",
            "reason": "K_solar≈1e-61 and m>=2 gives proxy <=1e-122, but only as a proxy",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3330_2_epsilon_eff_formula",
            "claim": "epsilon_eff_PPN formula is ready",
            "passed": "true",
            "reason": "epsilon_eff_PPN is written in terms of T_grad, background, boundary, and anisotropy",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3330_3_composite_formula",
            "claim": "epsilon_composite_PPN formula is ready",
            "passed": "true",
            "reason": "3327 composite envelope is specialized to PPN",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3330_4_C_PPN_numeric",
            "claim": "C_PPN is numerically/source bounded",
            "passed": "false",
            "reason": "q_U/gauge normalization and C_metric operator norm are not numeric",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3330_5_PPN_claim",
            "claim": "PPN/local-GR test is claim-ready",
            "passed": "false",
            "reason": "real B_PPN, numeric C_PPN, epsilon_eff, composite, Gamma, and direct floors are still missing",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3330_0",
            "question": "Did 3330 remove the C_PPN fog?",
            "answer": "partly",
            "reason": "C_PPN is now an operator response multiplied by weak-field PPN normalization, not a free placeholder",
            "next_action": "derive/bound q_U normalization and C_metric operator norm",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3330_1",
            "question": "What is the best encouraging local floor?",
            "answer": "Gamma/saturation proxy",
            "reason": "the corpus solar proxy gives <=1e-122 for K_solar^m, but this must not be applied to psi/composite floors without a mapping proof",
            "next_action": "try to parent-link local Gamma silence to the K_solar proxy or keep R_Gamma_PPN explicit",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3330_2",
            "question": "Can PPN now be claimed?",
            "answer": "no",
            "reason": "3330 improves the formulas but does not supply claim-grade numeric C_PPN or floor bounds",
            "next_action": "attack C_metric/q_U first, then specialize epsilon_eff/composite floors",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3331-Y5-R2FR-PPN-weak-potential-normalization-and-Cmetric-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3331_PPN_weak_potential_normalization_and_Cmetric_bound.py",
            "objective": "derive the PPN weak-potential normalization A_PPN(q_U,gauge) and a conservative C_metric operator bound so C_PPN stops being symbolic",
            "must_include": "weak-field metric ansatz; mapping from residual h_munu to gamma/beta residuals; q_U denominator; gauge caveat; C_metric operator norm; no real PPN claim",
            "fallback_if_failed": "retain C_PPN as symbolic and move to sourcing real PPN/R10 bounds only after operator response is narrowed",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    response = ppn_response_rows()
    floors = local_floor_rows()
    thresholds = ppn_threshold_rows()
    inputs = required_input_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3330_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3330_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3330_2_outputs_parse",
            "check": "all 3330 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3330_3_CPPN_qU",
            "check": "C_PPN response includes q_U normalization and C_metric",
            "passed": any(row["quantity"] == "q_U" for row in response)
            and any(row["quantity"] == "C_metric" for row in response)
            and any(row["quantity"] == "C_PPN" and "q_U" in row["formula"] for row in response),
            "detail": "",
        },
        {
            "check_id": "VAL3330_4_floors",
            "check": "floor rows include Gamma, epsilon_eff, composite, and direct terms",
            "passed": {"R_Gamma_PPN", "epsilon_eff_PPN", "epsilon_composite_PPN", "epsilon_direct_PPN"}.issubset(
                {row["floor"] for row in floors}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3330_5_Ksolar_proxy",
            "check": "Gamma proxy includes 1e-122 scale",
            "passed": any("1.000e-122" in row["formula"] for row in floors),
            "detail": "",
        },
        {
            "check_id": "VAL3330_6_thresholds",
            "check": "threshold formulas include master, epsilon_eff, floor gate, and no-claim rule",
            "passed": {"PTH3330_0_master", "PTH3330_1_epsilon_eff", "PTH3330_2_floor_budget", "PTH3330_3_claim_rule"}.issubset(
                {row["threshold_id"] for row in thresholds}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3330_7_inputs",
            "check": "required inputs include B_PPN, q_U, C_metric, epsilon_eff, composite, Gamma",
            "passed": {"B_PPN real threshold", "q_U=|U|/c^2 and PPN gauge/observable map", "C_metric operator/projection bound", "epsilon_bg_PPN, ell_s/lambda_PPN, epsilon_boundary_PPN, epsilon_kernel_aniso_PPN", "PPN-specialized CLT/spectral/contact composite inputs", "Gamma_local or proof that R_Gamma_PPN follows K_solar^m proxy"}.issubset(
                {row["quantity"] for row in inputs}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3330_8_no_claim",
            "check": "symbolic gates pass while numeric C_PPN and PPN claim remain false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3330_0_C_PPN_symbolic", "GATE3330_1_Gamma_proxy", "GATE3330_2_epsilon_eff_formula", "GATE3330_3_composite_formula"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3330_4_C_PPN_numeric", "GATE3330_5_PPN_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3330_9_next_Cmetric",
            "check": "next target is q_U normalization and C_metric bound",
            "passed": any("q_U" in row["objective"] and "C_metric" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3330_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3330_11_overall",
            "check": "3330 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3330 - PPN response coefficient and local floor bound under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3330 tightens the PPN smoke knobs into symbolic bound objects.",
        "",
        "The important correction is that `C_PPN` is not just the metric response coefficient. PPN observables normalize residual metric terms by the weak Newtonian potential scale",
        "",
        "`q_U = |U|/c^2`.",
        "",
        "So",
        "",
        "`C_PPN <= A_PPN(q_U,gauge) C_metric`,",
        "",
        "with `A_PPN` carrying the weak-field denominator/gauge/observable map and `C_metric` carrying the actual MTS projection-propagator-source norm.",
        "",
        "The PPN residual budget is now",
        "",
        "`R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff_PPN^2 + epsilon_composite_PPN + epsilon_direct_PPN`.",
        "",
        "The encouraging local floor is the corpus solar proxy: `K_solar≈1e-61`, `m>=2`, hence `K_solar^m <= 1e-122`. But this only supports the Gamma/saturation proxy, not the full psi/composite branch.",
        "",
        "No PPN claim follows. The next target is the real bottleneck: derive `A_PPN(q_U,gauge)` and a conservative `C_metric` bound.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("PPN Response Coefficient", ppn_response_rows(), "row_id"),
        ("Local Floor Bounds", local_floor_rows(), "floor_id"),
        ("PPN Threshold Formulas", ppn_threshold_rows(), "threshold_id"),
        ("Required Inputs", required_input_rows(), "input_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It replaces the placeholder `C_PPN` knob with a symbolic PPN response contract.",
            "- It records the `K_solar^m <= 1e-122` Gamma proxy without applying it to unrelated tails.",
            "- It does not use or claim real PPN bounds.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["ppn_response"], ppn_response_rows())
    write_csv(OUTPUTS["floors"], local_floor_rows())
    write_csv(OUTPUTS["thresholds"], ppn_threshold_rows())
    write_csv(OUTPUTS["inputs"], required_input_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
