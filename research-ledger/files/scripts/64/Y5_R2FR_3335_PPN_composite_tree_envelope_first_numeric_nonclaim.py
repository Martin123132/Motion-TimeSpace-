from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3335-Y5-R2FR-PPN-composite-tree-envelope-first-numeric-nonclaim-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3335_0_3334_doc",
        "path": ROOT / "3334-Y5-R2FR-Gamma-constant-curvature-or-Ksolar-proxy-map-under-AX1090.md",
        "role": "Gamma fork and next target",
    },
    {
        "source_id": "SRC3335_1_3334_budget",
        "path": OUT / "P8_Y5_R2FR_3334_UPDATED_REDUCED_PPN_BUDGET.csv",
        "role": "reduced PPN budget with Gamma fork",
    },
    {
        "source_id": "SRC3335_2_3334_gamma",
        "path": OUT / "P8_Y5_R2FR_3334_GAMMA_BRANCH_MAP.csv",
        "role": "Gamma fork definitions",
    },
    {
        "source_id": "SRC3335_3_3334_constant",
        "path": OUT / "P8_Y5_R2FR_3334_CONSTANT_CURVATURE_BOUND.csv",
        "role": "Lambda-like Gamma scale rows",
    },
    {
        "source_id": "SRC3335_4_3332_epsilon",
        "path": OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv",
        "role": "epsilon_eff and T_grad formulas",
    },
    {
        "source_id": "SRC3335_5_3332_composite",
        "path": OUT / "P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv",
        "role": "PPN composite CLT/contact formulas",
    },
    {
        "source_id": "SRC3335_6_3331_appn",
        "path": OUT / "P8_Y5_R2FR_3331_APPN_BOUND.csv",
        "role": "A_PPN weak-potential response formulas",
    },
    {
        "source_id": "SRC3335_7_3331_cmetric",
        "path": OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv",
        "role": "C_metric operator response formulas",
    },
    {
        "source_id": "SRC3335_8_3329_priors",
        "path": OUT / "P8_Y5_R2FR_3329_SMOKE_PRIORS.csv",
        "role": "placeholder B_PPN smoke ceiling and response-sweep convention",
    },
    {
        "source_id": "SRC3335_9_3329_smoke",
        "path": OUT / "P8_Y5_R2FR_3329_PPN_NUMERIC_SMOKE.csv",
        "role": "earlier broad PPN smoke comparison",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3335_SOURCE_REGISTER.csv",
    "response": OUT / "P8_Y5_R2FR_3335_RESPONSE_PLACEHOLDER_GRID.csv",
    "tree": OUT / "P8_Y5_R2FR_3335_TREE_EPSILON_SCENARIOS.csv",
    "composite": OUT / "P8_Y5_R2FR_3335_COMPOSITE_SCENARIOS.csv",
    "gamma": OUT / "P8_Y5_R2FR_3335_GAMMA_FORK_SCENARIOS.csv",
    "envelope": OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv",
    "thresholds": OUT / "P8_Y5_R2FR_3335_THRESHOLD_SENSITIVITY.csv",
    "inputs": OUT / "P8_Y5_R2FR_3335_REQUIRED_SOURCE_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3335_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3335_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3335_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3335_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
B_PPN_SMOKE = 1.0e-5
K_SOLAR_PROXY = 1.0e-122
LAMBDA_1AU_GAMMA = 1.281458091885e-30
LAMBDA_100AU_GAMMA = 1.281458091885e-26


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
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


def response_rows() -> list[dict[str, Any]]:
    return [
        {
            "response_id": "RESP3335_0_gentle",
            "A_PPN_times_Cmetric": f"{1.0e0:.6e}",
            "interpretation": "gentle response product placeholder; not sourced",
            "source_status": "PLACEHOLDER_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "response_id": "RESP3335_1_large",
            "A_PPN_times_Cmetric": f"{1.0e6:.6e}",
            "interpretation": "large response product comparable to earlier smoke sensitivity",
            "source_status": "PLACEHOLDER_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "response_id": "RESP3335_2_harsh",
            "A_PPN_times_Cmetric": f"{1.0e12:.6e}",
            "interpretation": "harsh weak-potential/operator amplification placeholder",
            "source_status": "PLACEHOLDER_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "response_id": "RESP3335_3_extreme",
            "A_PPN_times_Cmetric": f"{1.0e16:.6e}",
            "interpretation": "extreme stress-test response product; useful only as a failure-mode probe",
            "source_status": "PLACEHOLDER_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def t_grad(ell_over_lambda: float) -> float:
    return ell_over_lambda * math.exp(-0.5 * ell_over_lambda * ell_over_lambda)


def tree_scenario_specs() -> list[dict[str, Any]]:
    raw = [
        {
            "tree_id": "TREE3335_0_exact_silence",
            "label": "exact first-gradient silence",
            "ell_over_lambda": 0.0,
            "epsilon_bg": 0.0,
            "epsilon_boundary": 0.0,
            "epsilon_kernel_aniso": 0.0,
        },
        {
            "tree_id": "TREE3335_1_short_mode_smoothed",
            "label": "short mode under smoothing",
            "ell_over_lambda": 10.0,
            "epsilon_bg": 1.0e-3,
            "epsilon_boundary": 1.0e-18,
            "epsilon_kernel_aniso": 1.0e-18,
        },
        {
            "tree_id": "TREE3335_2_long_clean",
            "label": "long mode clean boundary",
            "ell_over_lambda": 1.0e-6,
            "epsilon_bg": 1.0e-3,
            "epsilon_boundary": 1.0e-12,
            "epsilon_kernel_aniso": 1.0e-12,
        },
        {
            "tree_id": "TREE3335_3_equal_smoothing_risky",
            "label": "lambda around smoothing scale",
            "ell_over_lambda": 1.0,
            "epsilon_bg": 1.0e-6,
            "epsilon_boundary": 1.0e-12,
            "epsilon_kernel_aniso": 1.0e-12,
        },
        {
            "tree_id": "TREE3335_4_boundary_dominated",
            "label": "boundary/aniso dominated",
            "ell_over_lambda": 1.0e-6,
            "epsilon_bg": 1.0e-9,
            "epsilon_boundary": 1.0e-6,
            "epsilon_kernel_aniso": 1.0e-8,
        },
    ]
    for item in raw:
        transfer = 0.0 if item["ell_over_lambda"] == 0.0 else t_grad(item["ell_over_lambda"])
        epsilon_eff = item["epsilon_bg"] * transfer + item["epsilon_boundary"] + item["epsilon_kernel_aniso"]
        item["T_grad"] = transfer
        item["epsilon_eff"] = epsilon_eff
        item["tree_formula"] = "epsilon_eff=epsilon_bg*T_grad+epsilon_boundary+epsilon_kernel_aniso"
        item["valid_for_claim"] = "false"
    return raw


def tree_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in tree_scenario_specs():
        row = dict(item)
        for response in response_rows():
            response_value = float(response["A_PPN_times_Cmetric"])
            row[f"tree_residual_{response['response_id']}"] = f"{response_value * item['epsilon_eff'] ** 2:.6e}"
        rows.append(row)
    return rows


def composite_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "comp_id": "COMP3335_0_ultra_clean",
            "label": "commuting centered high-N low-sigma",
            "N_eff": 1.0e18,
            "delta_comm": 0.0,
            "sigma_Dpi": 1.0e-6,
            "C3": 1.0,
            "delta_bias": 0.0,
            "rho_P1": 0.0,
            "Q2_norm": 0.0,
            "epsilon_2p": 1.0e-24,
            "epsilon_contact": 1.0e-20,
            "epsilon_boundary": 1.0e-18,
            "epsilon_kernel_aniso": 1.0e-18,
        },
        {
            "comp_id": "COMP3335_1_clean_CLT",
            "label": "centered CLT but finite skew",
            "N_eff": 1.0e12,
            "delta_comm": 0.0,
            "sigma_Dpi": 1.0e-3,
            "C3": 1.0,
            "delta_bias": 0.0,
            "rho_P1": 0.0,
            "Q2_norm": 0.0,
            "epsilon_2p": 1.0e-20,
            "epsilon_contact": 1.0e-18,
            "epsilon_boundary": 1.0e-18,
            "epsilon_kernel_aniso": 1.0e-18,
        },
        {
            "comp_id": "COMP3335_2_contact_limited",
            "label": "contact floor dominates",
            "N_eff": 1.0e12,
            "delta_comm": 0.0,
            "sigma_Dpi": 1.0e-3,
            "C3": 1.0,
            "delta_bias": 0.0,
            "rho_P1": 0.0,
            "Q2_norm": 0.0,
            "epsilon_2p": 1.0e-20,
            "epsilon_contact": 1.0e-8,
            "epsilon_boundary": 1.0e-12,
            "epsilon_kernel_aniso": 1.0e-12,
        },
        {
            "comp_id": "COMP3335_3_commutator_warning",
            "label": "PPN projection/smoothing commutator leakage",
            "N_eff": 1.0e12,
            "delta_comm": 1.0e-4,
            "sigma_Dpi": 1.0e-3,
            "C3": 1.0,
            "delta_bias": 0.0,
            "rho_P1": 0.0,
            "Q2_norm": 0.0,
            "epsilon_2p": 1.0e-12,
            "epsilon_contact": 1.0e-12,
            "epsilon_boundary": 1.0e-12,
            "epsilon_kernel_aniso": 1.0e-12,
        },
        {
            "comp_id": "COMP3335_4_contact_fail",
            "label": "large unrenormalized contact floor",
            "N_eff": 1.0e12,
            "delta_comm": 0.0,
            "sigma_Dpi": 1.0e-3,
            "C3": 1.0,
            "delta_bias": 0.0,
            "rho_P1": 0.0,
            "Q2_norm": 0.0,
            "epsilon_2p": 1.0e-12,
            "epsilon_contact": 1.0e-4,
            "epsilon_boundary": 1.0e-12,
            "epsilon_kernel_aniso": 1.0e-12,
        },
    ]
    rows: list[dict[str, Any]] = []
    for item in specs:
        one_particle = (
            item["delta_comm"] * item["sigma_Dpi"]
            + (item["C3"] / math.sqrt(item["N_eff"]) + item["delta_bias"]) * item["sigma_Dpi"] ** 2
            + item["rho_P1"] * item["Q2_norm"]
        )
        total = one_particle + item["epsilon_2p"] + item["epsilon_contact"] + item["epsilon_boundary"] + item["epsilon_kernel_aniso"]
        row = dict(item)
        row["epsilon_1p"] = f"{one_particle:.6e}"
        row["epsilon_composite"] = f"{total:.6e}"
        row["formula"] = "epsilon_composite=epsilon_1p+epsilon_2p+epsilon_contact+epsilon_boundary+epsilon_kernel_aniso"
        row["source_status"] = "NUMERIC_PLACEHOLDER_NONCLAIM"
        row["valid_for_claim"] = "false"
        rows.append(row)
    return rows


def gamma_rows() -> list[dict[str, Any]]:
    return [
        {
            "gamma_id": "GAMMA3335_0_pole_zero_only",
            "label": "finite pole zero; total floor set zero for sensitivity only",
            "R_Gamma": f"{0.0:.6e}",
            "status": "BRANCH_SENSITIVITY_ONLY",
            "valid_for_claim": "false",
        },
        {
            "gamma_id": "GAMMA3335_1_Lambda_1AU_A1",
            "label": "Lambda-like 1 AU A_Gamma=1 sanity check",
            "R_Gamma": f"{LAMBDA_1AU_GAMMA:.6e}",
            "status": "ORDER_OF_MAGNITUDE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "gamma_id": "GAMMA3335_2_Lambda_100AU_A1",
            "label": "Lambda-like 100 AU A_Gamma=1 sanity check",
            "R_Gamma": f"{LAMBDA_100AU_GAMMA:.6e}",
            "status": "ORDER_OF_MAGNITUDE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "gamma_id": "GAMMA3335_3_Ksolar_A1",
            "label": "K_solar proxy A_K=1 if parent map signed",
            "R_Gamma": f"{K_SOLAR_PROXY:.6e}",
            "status": "PROXY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "gamma_id": "GAMMA3335_4_open_warning",
            "label": "open local Gamma warning floor",
            "R_Gamma": f"{1.0e-4:.6e}",
            "status": "PLACEHOLDER_FAIL_MODE",
            "valid_for_claim": "false",
        },
    ]


def lookup(rows: list[dict[str, Any]], key: str, value: str) -> dict[str, Any]:
    for row in rows:
        if row[key] == value:
            return row
    raise KeyError(value)


def envelope_rows() -> list[dict[str, Any]]:
    trees = tree_scenario_specs()
    comps = composite_rows()
    gammas = gamma_rows()
    cases = [
        ("ENV3335_0_clean_lambda", "RESP3335_1_large", "TREE3335_1_short_mode_smoothed", "COMP3335_1_clean_CLT", "GAMMA3335_1_Lambda_1AU_A1"),
        ("ENV3335_1_long_mode_harsh_survives", "RESP3335_2_harsh", "TREE3335_2_long_clean", "COMP3335_1_clean_CLT", "GAMMA3335_1_Lambda_1AU_A1"),
        ("ENV3335_2_equal_smoothing_tree_fail", "RESP3335_2_harsh", "TREE3335_3_equal_smoothing_risky", "COMP3335_1_clean_CLT", "GAMMA3335_1_Lambda_1AU_A1"),
        ("ENV3335_3_contact_composite_fail", "RESP3335_1_large", "TREE3335_1_short_mode_smoothed", "COMP3335_4_contact_fail", "GAMMA3335_1_Lambda_1AU_A1"),
        ("ENV3335_4_open_Gamma_fail", "RESP3335_1_large", "TREE3335_2_long_clean", "COMP3335_1_clean_CLT", "GAMMA3335_4_open_warning"),
        ("ENV3335_5_Ksolar_clean", "RESP3335_1_large", "TREE3335_2_long_clean", "COMP3335_0_ultra_clean", "GAMMA3335_3_Ksolar_A1"),
        ("ENV3335_6_boundary_large_response", "RESP3335_1_large", "TREE3335_4_boundary_dominated", "COMP3335_2_contact_limited", "GAMMA3335_1_Lambda_1AU_A1"),
        ("ENV3335_7_boundary_harsh_fail", "RESP3335_2_harsh", "TREE3335_4_boundary_dominated", "COMP3335_2_contact_limited", "GAMMA3335_1_Lambda_1AU_A1"),
        ("ENV3335_8_commutator_warning", "RESP3335_1_large", "TREE3335_2_long_clean", "COMP3335_3_commutator_warning", "GAMMA3335_2_Lambda_100AU_A1"),
    ]
    rows: list[dict[str, Any]] = []
    for case_id, response_id, tree_id, comp_id, gamma_id in cases:
        response = lookup(response_rows(), "response_id", response_id)
        tree = lookup(trees, "tree_id", tree_id)
        comp = lookup(comps, "comp_id", comp_id)
        gamma = lookup(gammas, "gamma_id", gamma_id)
        response_value = float(response["A_PPN_times_Cmetric"])
        epsilon_eff = float(tree["epsilon_eff"])
        tree_residual = response_value * epsilon_eff * epsilon_eff
        composite_residual = float(comp["epsilon_composite"])
        gamma_residual = float(gamma["R_Gamma"])
        total = tree_residual + composite_residual + gamma_residual
        terms = {
            "tree_residual": tree_residual,
            "epsilon_composite": composite_residual,
            "R_Gamma": gamma_residual,
        }
        dominant = max(terms, key=terms.get)
        rows.append(
            {
                "scenario_id": case_id,
                "response_id": response_id,
                "tree_id": tree_id,
                "comp_id": comp_id,
                "gamma_id": gamma_id,
                "A_PPN_times_Cmetric": f"{response_value:.6e}",
                "epsilon_eff": f"{epsilon_eff:.6e}",
                "tree_residual": f"{tree_residual:.6e}",
                "epsilon_composite": f"{composite_residual:.6e}",
                "R_Gamma": f"{gamma_residual:.6e}",
                "R_total_smoke": f"{total:.6e}",
                "B_PPN_smoke": f"{B_PPN_SMOKE:.6e}",
                "smoke_pass_like": bool_str(total <= B_PPN_SMOKE),
                "dominant_term": dominant,
                "interpretation": "nonclaim pass-like/fail-like reduced PPN envelope",
                "valid_for_claim": "false",
            }
        )
    return rows


def threshold_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for response in response_rows():
        response_value = float(response["A_PPN_times_Cmetric"])
        eps_allowed = math.sqrt(B_PPN_SMOKE / response_value)
        rows.append(
            {
                "threshold_id": f"THR3335_eps_{response['response_id']}",
                "quantity": "epsilon_eff_allowed_if_tree_only",
                "A_PPN_times_Cmetric": f"{response_value:.6e}",
                "formula": "epsilon_eff <= sqrt(B_PPN_smoke/(A_PPN*C_metric))",
                "value": f"{eps_allowed:.6e}",
                "source_status": "PLACEHOLDER_NONCLAIM",
                "valid_for_claim": "false",
            }
        )
    rows.extend(
        [
            {
                "threshold_id": "THR3335_comp_floor",
                "quantity": "composite_floor_rule",
                "formula": "epsilon_composite_PPN < B_PPN_smoke is necessary before tree/Gamma details matter",
                "value": f"{B_PPN_SMOKE:.6e}",
                "source_status": "PLACEHOLDER_NONCLAIM",
                "valid_for_claim": "false",
            },
            {
                "threshold_id": "THR3335_gamma_open",
                "quantity": "Gamma_open_floor_rule",
                "formula": "R_Gamma_open < B_PPN_smoke is necessary unless Gamma is Lambda-like or K_solar mapped",
                "value": f"{B_PPN_SMOKE:.6e}",
                "source_status": "PLACEHOLDER_NONCLAIM",
                "valid_for_claim": "false",
            },
        ]
    )
    return rows


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3335_0_real_B_PPN",
            "quantity": "real PPN threshold vector",
            "needed_for": "replace B_PPN_smoke",
            "current_status": "MISSING_REAL_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3335_1_A_PPN_Cmetric",
            "quantity": "A_PPN*C_metric source-bounded product",
            "needed_for": "claim-grade tree residual",
            "current_status": "PLACEHOLDER_GRID_ONLY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3335_2_epsilon_eff",
            "quantity": "epsilon_bg_PPN, ell_s/lambda_PPN, boundary, anisotropy",
            "needed_for": "tree leakage amplitude",
            "current_status": "SCENARIO_GRID_ONLY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3335_3_composite",
            "quantity": "N_eff, delta_comm, spectral gap, contact scaling, projection leakage",
            "needed_for": "epsilon_composite_PPN",
            "current_status": "SCENARIO_GRID_ONLY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3335_4_Gamma",
            "quantity": "Gamma_local/Lambda-like bound or Gamma->K_solar map",
            "needed_for": "Gamma fork promotion",
            "current_status": "FORK_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3335_0_envelope_built",
            "claim": "first reduced PPN numeric nonclaim envelope exists",
            "passed": "true",
            "reason": "tree, composite, Gamma, response-product, and threshold sensitivity rows are generated",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3335_1_pass_fail_sensitivity",
            "claim": "envelope contains both pass-like and fail-like scenarios",
            "passed": "true",
            "reason": "dominant failure modes separate tree, composite, and open Gamma floors",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3335_2_no_claim",
            "claim": "no PPN/local-GR pass is claimed",
            "passed": "true",
            "reason": "all numeric values are placeholders or nonclaim sanity checks",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3335_3_claim_ready",
            "claim": "PPN/local-GR branch is claim-ready",
            "passed": "false",
            "reason": "real B_PPN, A_PPN*C_metric, epsilon_eff, composite, and Gamma source inputs are still missing",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    envelope = envelope_rows()
    fail_modes = sorted({row["dominant_term"] for row in envelope if row["smoke_pass_like"] == "false"})
    pass_modes = len([row for row in envelope if row["smoke_pass_like"] == "true"])
    fail_count = len(envelope) - pass_modes
    return [
        {
            "decision_id": "DEC3335_0",
            "question": "What did the first reduced numeric envelope show?",
            "answer": f"{pass_modes} pass-like and {fail_count} fail-like nonclaim scenarios under B_PPN_smoke",
            "reason": "the branch is sensitive mainly to tree leakage under harsh response, composite contact/commutator floors, and open Gamma",
            "next_action": "source or derive the dominant floors rather than widening the theory again",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3335_1",
            "question": "Which terms kill the branch in smoke?",
            "answer": ", ".join(fail_modes),
            "reason": "dominant_term tracking separates tree, composite, and Gamma failure modes",
            "next_action": "attack composite/contact and tree epsilon_eff before more Gamma work unless Gamma_local becomes source-owned",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3335_2",
            "question": "Can this be used publicly?",
            "answer": "no",
            "reason": "the numbers are scaffold/sensitivity only; they organize derivation work but do not prove a PPN pass",
            "next_action": "turn placeholders into source-bound rows or keep as private steering",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3336-Y5-R2FR-PPN-dominant-floor-source-acquisition-or-derivation-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3336_PPN_dominant_floor_source_acquisition_or_derivation.py",
            "objective": "replace the dominant 3335 placeholder floors with source-owned or derived bounds, prioritizing composite contact/commutator and tree epsilon_eff before Gamma unless Gamma_local is sourced",
            "must_include": "real PPN threshold candidate; A_PPN*C_metric acquisition contract; composite contact/commutator derivation attempt; epsilon_eff boundary/aniso derivation attempt; no PPN pass claim",
            "fallback_if_failed": "produce a minimal source-acquisition table for the exact missing numerical inputs and stop adding new symbolic branches",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    response = response_rows()
    tree = tree_rows()
    comp = composite_rows()
    gamma = gamma_rows()
    envelope = envelope_rows()
    thresholds = threshold_rows()
    inputs = required_input_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3335_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3335_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3335_2_outputs_parse",
            "check": "all 3335 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3335_3_response_grid",
            "check": "response grid includes placeholder A_PPN*C_metric products",
            "passed": len(response) >= 4 and all(row["source_status"] == "PLACEHOLDER_NONCLAIM" for row in response),
            "detail": "",
        },
        {
            "check_id": "VAL3335_4_tree_scenarios",
            "check": "tree scenarios include T_grad, epsilon_eff, and response-product residual columns",
            "passed": any(float(row["T_grad"]) > 0 for row in tree)
            and any("tree_residual_RESP3335_2_harsh" in row for row in tree)
            and any(float(row["epsilon_eff"]) == 0.0 for row in tree),
            "detail": "",
        },
        {
            "check_id": "VAL3335_5_composite_scenarios",
            "check": "composite scenarios include CLT, commutator, contact, and fail-mode floors",
            "passed": any(float(row["delta_comm"]) > 0 for row in comp)
            and any(float(row["epsilon_contact"]) >= 1.0e-4 for row in comp)
            and any(float(row["N_eff"]) >= 1.0e18 for row in comp),
            "detail": "",
        },
        {
            "check_id": "VAL3335_6_gamma_forks",
            "check": "Gamma fork scenarios include finite-pole zero, Lambda-like, K_solar, and open warning",
            "passed": {"GAMMA3335_0_pole_zero_only", "GAMMA3335_1_Lambda_1AU_A1", "GAMMA3335_3_Ksolar_A1", "GAMMA3335_4_open_warning"}.issubset(
                {row["gamma_id"] for row in gamma}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3335_7_envelope_sensitivity",
            "check": "envelope has pass-like and fail-like scenarios with distinct dominant terms",
            "passed": any(row["smoke_pass_like"] == "true" for row in envelope)
            and any(row["smoke_pass_like"] == "false" for row in envelope)
            and {"tree_residual", "epsilon_composite", "R_Gamma"}.issubset({row["dominant_term"] for row in envelope}),
            "detail": "",
        },
        {
            "check_id": "VAL3335_8_thresholds",
            "check": "threshold sensitivity includes epsilon_eff and composite/Gamma floor rules",
            "passed": any("epsilon_eff" in row["quantity"] for row in thresholds)
            and any(row["quantity"] == "composite_floor_rule" for row in thresholds)
            and any(row["quantity"] == "Gamma_open_floor_rule" for row in thresholds),
            "detail": "",
        },
        {
            "check_id": "VAL3335_9_inputs",
            "check": "required source inputs include B_PPN, response product, epsilon_eff, composite, and Gamma",
            "passed": {"REQ3335_0_real_B_PPN", "REQ3335_1_A_PPN_Cmetric", "REQ3335_2_epsilon_eff", "REQ3335_3_composite", "REQ3335_4_Gamma"}.issubset(
                {row["input_id"] for row in inputs}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3335_10_no_claim",
            "check": "nonclaim gates pass while claim-ready gate remains false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3335_0_envelope_built", "GATE3335_1_pass_fail_sensitivity", "GATE3335_2_no_claim"}
            )
            and any(row["gate_id"] == "GATE3335_3_claim_ready" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3335_11_next_3336",
            "check": "next target prioritizes dominant floor acquisition/derivation",
            "passed": any("dominant" in row["objective"] and "composite" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3335_12_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3335_13_overall",
            "check": "3335 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    pass_count = len([row for row in envelope_rows() if row["smoke_pass_like"] == "true"])
    fail_count = len(envelope_rows()) - pass_count
    lines: list[str] = [
        "# 3335 - PPN composite/tree envelope first numeric nonclaim under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3335 builds the first reduced local-PPN numeric envelope after the branch cleanup.",
        "",
        "The working reduced budget is",
        "",
        "`R_PPN <= R_Gamma_fork + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN`.",
        "",
        f"Using the earlier placeholder `B_PPN_smoke={B_PPN_SMOKE:.1e}`, the reduced smoke grid gives `{pass_count}` pass-like and `{fail_count}` fail-like nonclaim scenarios.",
        "",
        "The useful result is not a pass. The useful result is ranking the monsters:",
        "",
        "- harsh `A_PPN C_metric` plus imperfect smoothing can make the tree channel dominate;",
        "- unrenormalized contact or PPN projector/smoothing commutator leakage can make the composite floor dominate;",
        "- an open local Gamma floor still kills the branch, but Lambda-like and `K_solar` Gamma forks are tiny in the nonclaim sanity rows.",
        "",
        "The tree threshold rule is",
        "",
        "`epsilon_eff_PPN <= sqrt(B_PPN_smoke/(A_PPN C_metric))`.",
        "",
        "For the harsh placeholder `A_PPN C_metric=1e12`, this means `epsilon_eff_PPN` has to be around `3.16e-9` or smaller before composite/Gamma floors are counted.",
        "",
        "So the next best work is not another broad theory branch. It is source-owning or deriving the dominant floor inputs: `A_PPN C_metric`, `epsilon_eff`, contact/commutator composite terms, and real `B_PPN`.",
        "",
        "No PPN/local-GR pass is claimed.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Response Placeholder Grid", response_rows(), "response_id"),
        ("Tree Epsilon Scenarios", tree_rows(), "tree_id"),
        ("Composite Scenarios", composite_rows(), "comp_id"),
        ("Gamma Fork Scenarios", gamma_rows(), "gamma_id"),
        ("Reduced PPN Envelope Smoke", envelope_rows(), "scenario_id"),
        ("Threshold Sensitivity", threshold_rows(), "threshold_id"),
        ("Required Source Inputs", required_input_rows(), "input_id"),
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
            "- Numeric response products, composite inputs, and `B_PPN_smoke` are placeholders for sensitivity only.",
            "- Lambda-like and `K_solar` Gamma rows remain nonclaim sanity checks.",
            "- The checkpoint is useful only as a steering map for what to derive/source next.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["response"], response_rows())
    write_csv(OUTPUTS["tree"], tree_rows())
    write_csv(OUTPUTS["composite"], composite_rows())
    write_csv(OUTPUTS["gamma"], gamma_rows())
    write_csv(OUTPUTS["envelope"], envelope_rows())
    write_csv(OUTPUTS["thresholds"], threshold_rows())
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
