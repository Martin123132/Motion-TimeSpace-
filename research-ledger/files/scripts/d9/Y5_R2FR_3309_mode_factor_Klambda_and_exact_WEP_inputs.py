from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3309-Y5-R2FR-mode-factor-Klambda-and-exact-WEP-inputs-under-AX1090.md"

SRC_3308_DOC = ROOT / "3308-Y5-R2FR-source-coefficient-sik-gate-or-WEP-linear-bound-runner-under-AX1090.md"
SRC_3308_MATRIX = OUT / "P8_Y5_R2FR_3308_WEP_LINEAR_CONSTRAINT_MATRIX.csv"
SRC_3308_PROXY = OUT / "P8_Y5_R2FR_3308_UNIT_MODE_FACTOR_SENSITIVITY_PROXY.csv"
SRC_3308_DECISION = OUT / "P8_Y5_R2FR_3308_DECISION_LEDGER.csv"
SRC_3308_NEXT = OUT / "P8_Y5_R2FR_3308_NEXT_TARGET.csv"
SRC_3308_VALIDATION = OUT / "P8_Y5_BRR545_3308_VALIDATION.csv"

MICROSCOPE_ARXIV = "https://arxiv.org/abs/2209.15487"
MICROSCOPE_DOI = "10.1103/PhysRevLett.129.121102"
MICROSCOPE_ESA = "https://www.esa.int/Science_Exploration/Space_Science/Microscope"
EOTWASH_ARXIV = "https://arxiv.org/abs/0712.0607"
EOTWASH_DOI = "10.1103/PhysRevLett.100.041101"

EARTH_MEAN_RADIUS_M = 6_371_000.0
MICROSCOPE_ALTITUDE_M = 710_000.0
MICROSCOPE_R_PROXY_M = EARTH_MEAN_RADIUS_M + MICROSCOPE_ALTITUDE_M
EOTWASH_EARTH_R_PROXY_M = EARTH_MEAN_RADIUS_M

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3309_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_R2FR_3309_KLAMBDA_DERIVATION.csv",
    "exact_inputs": OUT / "P8_Y5_R2FR_3309_EXACT_WEP_INPUT_LEDGER.csv",
    "constraint_update": OUT / "P8_Y5_R2FR_3309_KLAMBDA_CONSTRAINT_UPDATE.csv",
    "claim_blockers": OUT / "P8_Y5_R2FR_3309_WEP_CLAIM_BLOCKERS.csv",
    "runner": OUT / "P8_Y5_R2FR_3309_KLAMBDA_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3309_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3309_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3309_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3309_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 820) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 420)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    local_sources = [
        (SRC_3308_DOC, "3308 linear bound runner handoff", ["K_i(lambda_i)", "s_i dot Delta_q_AB"]),
        (SRC_3308_MATRIX, "3308 linear constraint matrix", ["LC3308_scalar", "K_0(lambda_0)"]),
        (SRC_3308_PROXY, "3308 unit mode proxy rows", ["unit_mode_factor_proxy_bound"]),
        (SRC_3308_DECISION, "3308 decision", ["K_i(lambda)", "s_ik"]),
        (SRC_3308_NEXT, "3308 next target", ["mode-factor-Klambda", "exact WEP inputs"]),
        (SRC_3308_VALIDATION, "3308 validation", ["VAL3308_11_overall", "true"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(local_sources):
        rows.append(
            {
                "source_id": f"SRC3309_{index}",
                "source_type": "local_path",
                "path_or_url": str(path),
                "exists_or_url_present": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    rows.extend(
        [
            {
                "source_id": "SRC3309_6",
                "source_type": "external_primary",
                "path_or_url": MICROSCOPE_ARXIV,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "MICROSCOPE final WEP result; eta Ti/Pt and uncertainties",
                "evidence_hits": "source-backed external row; eta(Ti,Pt)=(-1.5 +/- 2.3_stat +/- 1.5_syst)*10^-15; DOI 10.1103/PhysRevLett.129.121102",
                "valid_for_claim": "false",
            },
            {
                "source_id": "SRC3309_7",
                "source_type": "external_primary",
                "path_or_url": MICROSCOPE_ESA,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "ESA MICROSCOPE mission overview; orbit about 710 km and Pt-Rh/Ti-Al-V alloy category",
                "evidence_hits": "source-backed mission context; not a material assay table",
                "valid_for_claim": "false",
            },
            {
                "source_id": "SRC3309_8",
                "source_type": "external_primary",
                "path_or_url": EOTWASH_ARXIV,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "Eot-Wash Be/Ti WEP anchor; eta and differential acceleration",
                "evidence_hits": "source-backed external row; eta_Earth(Be-Ti)=(0.3 +/- 1.8)*10^-13 and Delta a_N=(-0.2 +/- 2.8)*10^-15 m/s^2, Delta a_W=(0.6 +/- 3.1)*10^-15 m/s^2",
                "valid_for_claim": "false",
            },
        ]
    )
    return rows


def klambda_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "KDER3309_0_potential",
            "statement": "For one finite mode, Phi_i(r) = -G_cal M_E/r * alpha_i_star Xi_i[E] Xi_i[A] exp(-r/lambda_i).",
            "result": "finite-mode potential contribution relative to Newtonian source E",
            "valid_for_claim": "false",
        },
        {
            "step_id": "KDER3309_1_acceleration",
            "statement": "a_i/a_N = alpha_i_star Xi_i[E] Xi_i[A] (1+r/lambda_i) exp(-r/lambda_i).",
            "result": "Yukawa acceleration has the derivative factor (1+r/lambda_i) exp(-r/lambda_i)",
            "valid_for_claim": "false",
        },
        {
            "step_id": "KDER3309_2_Eotvos_difference",
            "statement": "eta_AB,E^(i) ~= alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i).",
            "result": "finite-mode WEP signal is K_i(lambda_i,r,E) Delta_Xi_i[A,B]",
            "valid_for_claim": "false",
        },
        {
            "step_id": "KDER3309_3_mode_factor",
            "statement": "K_i(lambda_i,r,E) = alpha_i_star Xi_i[E] (1+r/lambda_i) exp(-r/lambda_i).",
            "result": "mode factor isolated from material contrast s_i dot Delta_q_AB",
            "valid_for_claim": "false",
        },
        {
            "step_id": "KDER3309_4_limits",
            "statement": "For lambda_i >> r, K_i -> alpha_i_star Xi_i[E]; for lambda_i << r, K_i is exponentially suppressed.",
            "result": "long-range WEP tests constrain source coefficients only when the finite-mode range is comparable to or larger than source separation",
            "valid_for_claim": "false",
        },
    ]


def exact_wep_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "EXWEP3309_0_MICROSCOPE_eta",
            "anchor_id": "WEP3306_0_MICROSCOPE_Ti_Pt",
            "source_url": MICROSCOPE_ARXIV,
            "doi": MICROSCOPE_DOI,
            "quantity": "eta_Ti_Pt",
            "value": "-1.5e-15",
            "stat_uncertainty": "2.3e-15",
            "syst_uncertainty": "1.5e-15",
            "confidence_status": "reported stat/syst uncertainties; no confidence-level conversion applied",
            "upgrade_status": "UPGRADED_SOURCE_BACKED",
            "valid_for_claim": "false",
        },
        {
            "input_id": "EXWEP3309_1_MICROSCOPE_materials",
            "anchor_id": "WEP3306_0_MICROSCOPE_Ti_Pt",
            "source_url": MICROSCOPE_ESA,
            "doi": "MISSING_MATERIAL_ASSAY_DOI",
            "quantity": "test_body_material_categories",
            "value": "platinum-rhodium alloy vs titanium-aluminium-vanadium alloy",
            "stat_uncertainty": "not_applicable",
            "syst_uncertainty": "not_applicable",
            "confidence_status": "exact alloy fractions/isotopic assay still missing",
            "upgrade_status": "PARTIAL_SOURCE_BACKED_CATEGORY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "EXWEP3309_2_MICROSCOPE_range",
            "anchor_id": "WEP3306_0_MICROSCOPE_Ti_Pt",
            "source_url": MICROSCOPE_ESA,
            "doi": "not_applicable",
            "quantity": "Earth_source_separation_proxy",
            "value": f"{MICROSCOPE_R_PROXY_M:.12g}",
            "stat_uncertainty": "not_applicable",
            "syst_uncertainty": "uses Earth mean radius plus 710 km orbit altitude; not orbit ephemeris",
            "confidence_status": "range proxy only",
            "upgrade_status": "PARTIAL_SOURCE_BACKED_RANGE_PROXY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "EXWEP3309_3_EOTWASH_eta",
            "anchor_id": "WEP3306_1_EOTWASH_Be_Ti",
            "source_url": EOTWASH_ARXIV,
            "doi": EOTWASH_DOI,
            "quantity": "eta_Earth_Be_Ti",
            "value": "0.3e-13",
            "stat_uncertainty": "1.8e-13",
            "syst_uncertainty": "MISSING_SEPARATE_SYSTEMATIC",
            "confidence_status": "reported uncertainty in abstract; no full covariance/systematic conversion applied",
            "upgrade_status": "UPGRADED_SOURCE_BACKED",
            "valid_for_claim": "false",
        },
        {
            "input_id": "EXWEP3309_4_EOTWASH_differential_acceleration",
            "anchor_id": "WEP3306_1_EOTWASH_Be_Ti",
            "source_url": EOTWASH_ARXIV,
            "doi": EOTWASH_DOI,
            "quantity": "Delta_a_N_and_Delta_a_W",
            "value": "Delta_a_N=(-0.2 +/- 2.8)e-15 m/s^2; Delta_a_W=(0.6 +/- 3.1)e-15 m/s^2",
            "stat_uncertainty": "see_value",
            "syst_uncertainty": "MISSING_SEPARATE_SYSTEMATIC",
            "confidence_status": "source-backed anchor; not converted into eta(lambda) table",
            "upgrade_status": "UPGRADED_SOURCE_BACKED",
            "valid_for_claim": "false",
        },
        {
            "input_id": "EXWEP3309_5_EOTWASH_range",
            "anchor_id": "WEP3306_1_EOTWASH_Be_Ti",
            "source_url": EOTWASH_ARXIV,
            "doi": EOTWASH_DOI,
            "quantity": "Earth_source_separation_proxy",
            "value": f"{EOTWASH_EARTH_R_PROXY_M:.12g}",
            "stat_uncertainty": "not_applicable",
            "syst_uncertainty": "uses Earth mean radius; lab/source geometry not fully modeled",
            "confidence_status": "range proxy only",
            "upgrade_status": "PARTIAL_SOURCE_BACKED_RANGE_PROXY",
            "valid_for_claim": "false",
        },
    ]


def range_symbol_for_anchor(anchor_id: str) -> tuple[str, float, str]:
    if "MICROSCOPE" in anchor_id:
        return "r_MICROSCOPE_Earth_proxy", MICROSCOPE_R_PROXY_M, "Earth mean radius plus 710 km orbit altitude"
    return "r_EOTWASH_Earth_proxy", EOTWASH_EARTH_R_PROXY_M, "Earth mean radius proxy"


def constraint_update_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SRC_3308_MATRIX):
        mode_index = "0" if row["mode"] == "scalar" else "2"
        range_symbol, range_value, range_status = range_symbol_for_anchor(row["anchor_id"])
        rows.append(
            {
                "constraint_id": row["constraint_id"],
                "mode": row["mode"],
                "anchor_id": row["anchor_id"],
                "range_symbol": range_symbol,
                "range_value_m_proxy": f"{range_value:.12g}",
                "range_status": range_status,
                "K_symbolic": f"K_{mode_index}(lambda_{mode_index},{range_symbol})",
                "K_formula": f"alpha{mode_index}_star * Xi_{mode_index}[Earth] * (1+{range_symbol}/lambda_{mode_index}) * exp(-{range_symbol}/lambda_{mode_index})",
                "updated_constraint": f"|K_{mode_index}(lambda_{mode_index},{range_symbol}) * ({row['linear_form']})| <= eta_bound_ABE",
                "claim_blocker": "alpha_star, lambda_i, Xi_i[Earth], exact material charges, and confidence convention still missing",
                "valid_for_claim": "false",
            }
        )
    return rows


def claim_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK3309_0_alpha_star",
            "missing_object": "alpha0_star, alpha2_star",
            "why_needed": "sets finite-mode force amplitude before WEP bounds can constrain s_i",
            "route_to_fix": "derive Z_i and U_i or prove pure metric limit for mode residues/readout",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "BLK3309_1_lambda",
            "missing_object": "lambda_0, lambda_2",
            "why_needed": "sets range suppression in K_i(lambda)",
            "route_to_fix": "derive parent quadratic coefficients or bound lambda_i as scan parameter",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "BLK3309_2_source_charge",
            "missing_object": "Xi_0[Earth], Xi_2[Earth]",
            "why_needed": "Earth/source composition enters K_i(lambda)",
            "route_to_fix": "derive source universality or build Earth source-charge model",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "BLK3309_3_exact_materials",
            "missing_object": "exact alloy/isotope composition and binding/EM accounting",
            "why_needed": "proxy Delta_q rows are not exact experimental material charges",
            "route_to_fix": "extract material composition tables from experiment papers or official mission docs",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "BLK3309_4_confidence",
            "missing_object": "single confidence convention/covariance treatment",
            "why_needed": "eta central/stat/syst rows cannot be converted into claim bounds inconsistently",
            "route_to_fix": "choose one-sided/two-sided CL convention and use full paper uncertainties",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    exact_inputs = exact_wep_input_rows()
    updates = constraint_update_rows()
    blockers = claim_blocker_rows()
    upgraded_eta = [
        row
        for row in exact_inputs
        if row["upgrade_status"] == "UPGRADED_SOURCE_BACKED"
        and "eta" in row["quantity"]
    ]
    return [
        {
            "runner_id": "RUN3309_0_K_derivation",
            "test": "K(lambda) acceleration factor derived",
            "result": "PASS_NONCLAIM",
            "detail": "K_i=lambda factor includes (1+r/lambda_i) exp(-r/lambda_i)",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3309_1_exact_eta_inputs",
            "test": "source-backed eta inputs upgraded for MICROSCOPE and Eot-Wash",
            "result": "PASS_NONCLAIM" if len(upgraded_eta) >= 2 else "FAIL",
            "detail": ";".join(row["input_id"] for row in upgraded_eta),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3309_2_constraint_updates",
            "test": "all 3308 constraints receive K(lambda,r) update",
            "result": "PASS_NONCLAIM" if len(updates) == len(read_csv(SRC_3308_MATRIX)) else "FAIL",
            "detail": ";".join(row["constraint_id"] for row in updates),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3309_3_claim_permission",
            "test": "WEP constraints claim-ready",
            "result": "REFUSE_CLAIM_BLOCKERS_ACTIVE",
            "detail": ";".join(row["missing_object"] for row in blockers),
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3309_0_K_numeric",
            "claim": "K_i(lambda_i) is numeric for WEP scoring",
            "requirements": "alpha_i_star, lambda_i, Xi_i[Earth], and range geometry numeric/sourced",
            "current_evidence": "K_i derived symbolically and range proxy staged",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3309_1_exact_WEP_inputs",
            "claim": "WEP input rows are exact enough for claim bounds",
            "requirements": "exact materials, source body, confidence convention, covariance/systematics, and range handling",
            "current_evidence": "eta rows upgraded but material/range/confidence remain partial",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3309_2_WEP_bound_runner",
            "claim": "linear WEP runner can bound s_ik combinations for local-GR claim",
            "requirements": "GATE3309_0 and GATE3309_1 true",
            "current_evidence": "symbolic nonclaim runner only",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3309_0",
            "question": "Did 3309 derive the missing K(lambda) mode factor?",
            "answer": "yes, symbolically",
            "reason": "differentiating the Yukawa potential gives K_i=lambda factor alpha_i_star Xi_i[E](1+r/lambda_i)exp(-r/lambda_i)",
            "next_action": "derive or scan alpha_i_star, lambda_i, and Xi_i[Earth]",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3309_1",
            "question": "Did 3309 make the WEP inputs claim-ready?",
            "answer": "no",
            "reason": "eta anchors are source-backed, but exact material composition, source charge, confidence conversion, and mode ranges are not filled",
            "next_action": "build Earth/source charge and lambda-scan runner or return to parent coefficient derivation",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3309_0_3310",
            "target_doc": "3310-Y5-R2FR-lambda-scan-WEP-envelope-or-parent-range-derivation-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3310_lambda_scan_WEP_envelope_or_parent_range_derivation.py",
            "objective": "derive lambda_0/lambda_2 from parent coefficients if possible; otherwise build a nonclaim lambda-scan envelope for K_i(lambda) showing where MICROSCOPE/Eot-Wash can constrain s_ik combinations",
            "guardrails": "do not treat source-backed eta anchors as final bounds until exact materials/source charges/confidence are fixed; keep scalar and spin2 modes separate",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    local_source_paths = [Path(row["path_or_url"]) for row in source_rows if row["source_type"] == "local_path"]
    external_sources = [row for row in source_rows if row["source_type"] == "external_primary"]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    derivation = klambda_derivation_rows()
    exact_inputs = exact_wep_input_rows()
    updates = constraint_update_rows()
    blockers = claim_blocker_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3309_0_sources_exist",
            "all local sources exist and external URLs are present",
            all(path.exists() for path in local_source_paths)
            and all(row["path_or_url"].startswith("https://") for row in external_sources),
            "",
        ),
        (
            "VAL3309_1_sources_parse",
            "all local cited source paths parse",
            all(parse_ok(path) for path in local_source_paths),
            "",
        ),
        (
            "VAL3309_2_outputs_parse",
            "all 3309 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3309_3_K_derivation_complete",
            "K derivation includes potential, acceleration, Eotvos difference, and limits",
            all(
                any(token in row["step_id"] for row in derivation)
                for token in ["potential", "acceleration", "Eotvos", "mode_factor", "limits"]
            ),
            "",
        ),
        (
            "VAL3309_4_exact_eta_inputs_upgraded",
            "source-backed eta inputs exist for MICROSCOPE and Eot-Wash",
            any(row["input_id"] == "EXWEP3309_0_MICROSCOPE_eta" and row["upgrade_status"] == "UPGRADED_SOURCE_BACKED" for row in exact_inputs)
            and any(row["input_id"] == "EXWEP3309_3_EOTWASH_eta" and row["upgrade_status"] == "UPGRADED_SOURCE_BACKED" for row in exact_inputs),
            "",
        ),
        (
            "VAL3309_5_partial_inputs_marked_nonclaim",
            "partial material/range/confidence rows remain nonclaim",
            all(row["valid_for_claim"] == "false" for row in exact_inputs)
            and any("PARTIAL" in row["upgrade_status"] for row in exact_inputs),
            "",
        ),
        (
            "VAL3309_6_all_constraints_updated",
            "all 3308 constraints receive K(lambda,r) updates",
            len(updates) == len(read_csv(SRC_3308_MATRIX))
            and all("K_" in row["K_symbolic"] and "exp" in row["K_formula"] for row in updates),
            "",
        ),
        (
            "VAL3309_7_claim_blockers_complete",
            "claim blockers include alpha, lambda, source charge, exact materials, and confidence",
            all(
                any(token in row["missing_object"] for row in blockers)
                for token in ["alpha", "lambda", "Xi_", "alloy", "confidence"]
            ),
            "",
        ),
        (
            "VAL3309_8_runner_refuses_claim",
            "runner refuses claim with blockers active",
            any(row["result"] == "REFUSE_CLAIM_BLOCKERS_ACTIVE" for row in runners),
            "",
        ),
        (
            "VAL3309_9_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3309_10_next_target_lambda_scan",
            "next target is lambda scan or parent range derivation",
            "lambda-scan" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3309_11_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3309_12_overall",
            "3309 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_str(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def render_doc() -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}` ({row['source_type']}): `{row['path_or_url']}` — role={row['role']}"
        for row in source_register_rows()
    )
    derivation_table = "\n".join(
        f"- `{row['step_id']}`: {row['statement']} Result: {row['result']}."
        for row in klambda_derivation_rows()
    )
    input_table = "\n".join(
        f"- `{row['input_id']}` `{row['quantity']}`: value={row['value']}; status={row['upgrade_status']}; source={row['source_url']}"
        for row in exact_wep_input_rows()
    )
    update_table = "\n".join(
        f"- `{row['constraint_id']}`: `{row['updated_constraint']}` with {row['range_symbol']}={row['range_value_m_proxy']} m."
        for row in constraint_update_rows()
    )
    blocker_table = "\n".join(
        f"- `{row['blocker_id']}` `{row['missing_object']}`: {row['route_to_fix']}."
        for row in claim_blocker_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3309 - Mode factor K(lambda) and exact WEP inputs under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The WEP mode factor is now derived.

For a Yukawa finite mode,

`eta_AB,E^(i) ~= alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i)`.

So the isolated mode factor is

`K_i(lambda_i,r,E) = alpha_i_star Xi_i[E] (1+r/lambda_i) exp(-r/lambda_i)`.

This turns each WEP row into

`|K_i(lambda_i,r,E) (s_i dot Delta_q_AB)| <= eta_bound_ABE`.

MICROSCOPE and Eot-Wash eta anchors are upgraded to source-backed nonclaim inputs. They are still not final claim bounds because exact material composition, source charge, finite-mode ranges, amplitude factors, and confidence conversion remain unresolved.

## Source Register

{source_table}

## K(lambda) Derivation

{derivation_table}

## Exact/Upgraded WEP Input Ledger

{input_table}

## Constraint Updates

{update_table}

## Claim Blockers

{blocker_table}

## Runner

{runner_table}

## Promotion Gates

{gate_table}

## Decision

{decision_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["derivation"], klambda_derivation_rows())
    write_csv(OUTPUTS["exact_inputs"], exact_wep_input_rows())
    write_csv(OUTPUTS["constraint_update"], constraint_update_rows())
    write_csv(OUTPUTS["claim_blockers"], claim_blocker_rows())
    write_csv(OUTPUTS["runner"], runner_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
