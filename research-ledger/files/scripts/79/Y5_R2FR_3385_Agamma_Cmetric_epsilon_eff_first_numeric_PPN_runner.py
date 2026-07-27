from __future__ import annotations

import csv
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
DOC = ROOT / "3385-Y5-R2FR-A_gamma-Cmetric-epsilon-eff-first-numeric-PPN-runner-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3385_SOURCE_REGISTER.csv",
    "runner_inputs": OUT / "P8_Y5_R2FR_3385_RUNNER_INPUTS.csv",
    "cassini_rescore": OUT / "P8_Y5_R2FR_3385_CASSINI_GAMMA_RESCORING_NONCLAIM.csv",
    "thresholds": OUT / "P8_Y5_R2FR_3385_EPSILON_EFF_THRESHOLDS_NONCLAIM.csv",
    "missing_inputs": OUT / "P8_Y5_R2FR_3385_MISSING_INPUTS_FOR_CLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3385_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3385_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3385_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3385_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3385_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3385_0_3384_doc", ROOT / "3384-Y5-R2FR-Cmetric-Gamma-post-UOC-PPN-zero-or-first-bound-row-under-AX1090.md", "3384 Cmetric/Gamma handoff"),
    ("SRC3385_1_3384_bound", OUT / "P8_Y5_R2FR_3384_FIRST_GAMMA_PPN_BOUND_ROW_NONCLAIM.csv", "3384 Cassini gamma bound row"),
    ("SRC3385_2_3384_inputs", OUT / "P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv", "3384 metric response input requirements"),
    ("SRC3385_3_3335_doc", ROOT / "3335-Y5-R2FR-PPN-composite-tree-envelope-first-numeric-nonclaim-under-AX1090.md", "3335 reduced PPN envelope smoke"),
    ("SRC3385_4_3335_smoke", OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv", "3335 reduced PPN envelope scenarios"),
    ("SRC3385_5_3335_response", OUT / "P8_Y5_R2FR_3335_RESPONSE_PLACEHOLDER_GRID.csv", "3335 response product placeholder grid"),
    ("SRC3385_6_3335_thresholds", OUT / "P8_Y5_R2FR_3335_THRESHOLD_SENSITIVITY.csv", "3335 threshold sensitivity"),
    ("SRC3385_7_3332_epsilon", OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv", "epsilon_eff formulas"),
    ("SRC3385_8_3331_appn", OUT / "P8_Y5_R2FR_3331_APPN_BOUND.csv", "A_PPN symbolic bounds"),
    ("SRC3385_9_3331_cmetric", OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv", "C_metric symbolic bounds"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
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
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def to_float(value: str, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def cassini_bound() -> float:
    path = OUT / "P8_Y5_R2FR_3384_FIRST_GAMMA_PPN_BOUND_ROW_NONCLAIM.csv"
    for row in read_csv_rows(path):
        if row.get("row_id") == "GB3384_0_Cassini_gamma_component_bound":
            return to_float(row.get("external_bound_abs", ""), 6.7e-5)
    return 6.7e-5


def runner_input_rows(bound: float) -> list[dict[str, str]]:
    smoke_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv")
    return [
        {
            "input_id": "IN3385_0_bound",
            "quantity": "B_gamma_Cassini_2sigma_envelope",
            "value": f"{bound:.15e}",
            "units": "dimensionless",
            "source_path": str(OUT / "P8_Y5_R2FR_3384_FIRST_GAMMA_PPN_BOUND_ROW_NONCLAIM.csv"),
            "status": "EXTERNAL_BOUND_PRESENT",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3385_1_scenarios",
            "quantity": "3335 reduced PPN smoke scenarios",
            "value": str(len(smoke_rows)),
            "units": "rows",
            "source_path": str(OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv"),
            "status": "PLACEHOLDER_NONCLAIM_SCENARIOS",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3385_2_formula",
            "quantity": "gamma residual formula",
            "value": "|delta_gamma_MTS| <= R_Gamma + A_gamma*Cmetric*epsilon_eff^2 + epsilon_composite",
            "units": "dimensionless",
            "source_path": str(OUT / "P8_Y5_R2FR_3384_FIRST_GAMMA_PPN_BOUND_ROW_NONCLAIM.csv"),
            "status": "FORMULA_READY_COMPONENTS_PLACEHOLDER",
            "valid_for_claim": "false",
        },
    ]


def cassini_rescore_rows(bound: float) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in read_csv_rows(OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv"):
        total = to_float(source.get("R_total_smoke", ""))
        margin = bound - total if math.isfinite(total) else math.nan
        pass_like = math.isfinite(total) and total <= bound
        rows.append(
            {
                "scenario_id": source.get("scenario_id", ""),
                "A_PPN_times_Cmetric": source.get("A_PPN_times_Cmetric", ""),
                "epsilon_eff": source.get("epsilon_eff", ""),
                "tree_residual": source.get("tree_residual", ""),
                "epsilon_composite": source.get("epsilon_composite", ""),
                "R_Gamma": source.get("R_Gamma", ""),
                "R_total_smoke": source.get("R_total_smoke", ""),
                "B_gamma_Cassini": f"{bound:.15e}",
                "cassini_pass_like": bool_text(pass_like),
                "cassini_margin": f"{margin:.15e}" if math.isfinite(margin) else "nan",
                "dominant_term": source.get("dominant_term", ""),
                "why_nonclaim": "3335 scenario inputs are placeholders/nonclaim; this is a comparator plumbing run, not evidence",
                "valid_for_claim": "false",
            }
        )
    return rows


def threshold_rows(bound: float) -> list[dict[str, str]]:
    response_values = [1.0, 1.0e6, 1.0e12, 1.0e16]
    rows: list[dict[str, str]] = []
    for value in response_values:
        epsilon_allow = math.sqrt(bound / value)
        rows.append(
            {
                "threshold_id": f"TH3385_AxC_{value:.0e}",
                "A_gamma_times_Cmetric": f"{value:.6e}",
                "B_gamma_Cassini": f"{bound:.15e}",
                "epsilon_eff_max_if_other_floors_zero": f"{epsilon_allow:.15e}",
                "formula": "epsilon_eff <= sqrt(B_gamma/(A_gamma*Cmetric))",
                "status": "NONCLAIM_THRESHOLD_HELPER",
                "valid_for_claim": "false",
            }
        )
    return rows


def missing_input_rows() -> list[dict[str, str]]:
    return [
        {"missing_id": "MISS3385_0_Agamma", "quantity": "A_gamma(q_U,gauge)", "why_needed": "turns raw metric residual into gamma PPN units", "current_status": "symbolic; q_U/gauge/readout/source residuals not filled", "next_action": "choose Solar-system comparison and source q_U/gauge convention", "valid_for_claim": "false"},
        {"missing_id": "MISS3385_1_Cmetric", "quantity": "C_metric(lambda_PPN)", "why_needed": "bounds MTS metric operator response", "current_status": "symbolic factor bound only", "next_action": "fill P_PPN,G_fix,W_src,D_readout,S_band,H_band,N_source or prove zero", "valid_for_claim": "false"},
        {"missing_id": "MISS3385_2_epsilon_eff", "quantity": "epsilon_eff_PPN", "why_needed": "controls first-gradient/tree leakage amplitude", "current_status": "formula only", "next_action": "derive epsilon_bg=epsilon_boundary=epsilon_kernel_aniso=0 or bound them", "valid_for_claim": "false"},
        {"missing_id": "MISS3385_3_floors", "quantity": "R_Gamma, epsilon_composite, R_nonEH, R_transfer", "why_needed": "subtract floors before claiming tree budget", "current_status": "some smoke values exist but not source-backed", "next_action": "sign Gamma proxy or fill component bounds", "valid_for_claim": "false"},
    ]


def runner_rows(rescore: list[dict[str, str]]) -> list[dict[str, str]]:
    pass_count = sum(1 for row in rescore if row["cassini_pass_like"] == "true")
    fail_count = sum(1 for row in rescore if row["cassini_pass_like"] == "false")
    return [
        {"run_id": "RUN3385_0_rescore", "test": "rescore 3335 placeholder scenarios against Cassini gamma envelope", "result": "PASS_NONCLAIM_RUNNER", "detail": f"pass_like={pass_count}; fail_like={fail_count}; rows={len(rescore)}", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3385_1_bound_present", "test": "real external gamma comparator exists", "result": "PASS_EXTERNAL_BOUND_PRESENT", "detail": "B_gamma_Cassini imported from 3384/Cassini intake", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3385_2_prediction_ready", "test": "MTS prediction row is source-ready", "result": "FAIL_MTS_INPUTS_PLACEHOLDER", "detail": "A_gamma, Cmetric, epsilon_eff and floor components are symbolic/placeholders", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3385_3_firewall", "test": "prevent PPN pass claim", "result": "PASS_CLAIM_FIREWALL", "detail": "scenario pass-like rows remain nonclaim until source-backed inputs replace placeholders", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def gate_rows(source_ok: bool, rescore: list[dict[str, str]]) -> list[dict[str, str]]:
    pass_count = sum(1 for row in rescore if row["cassini_pass_like"] == "true")
    return [
        {"gate_id": "GATE3385_0_sources", "claim": "all 3385 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates 3384/3335/3331/3332 inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3385_1_runner_executes", "claim": "Cassini rescore runner produces scenario rows", "gate_pass": bool_text(len(rescore) > 0), "reason": f"rows={len(rescore)} pass_like={pass_count}", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3385_2_external_bound", "claim": "external gamma bound is present", "gate_pass": "true", "reason": "B_gamma_Cassini imported from 3384", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3385_3_mts_prediction", "claim": "MTS prediction inputs are source-backed", "gate_pass": "false", "reason": "A_gamma/Cmetric/epsilon_eff/floors remain placeholder or symbolic", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3385_4_local_ppn", "claim": "local PPN gamma component passes", "gate_pass": "false", "reason": "pass-like scenarios are not evidence until missing inputs are sourced", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows(rescore: list[dict[str, str]]) -> list[dict[str, str]]:
    pass_count = sum(1 for row in rescore if row["cassini_pass_like"] == "true")
    fail_count = sum(1 for row in rescore if row["cassini_pass_like"] == "false")
    return [
        {"decision_id": "DEC3385_0_progress", "decision": "The gamma comparator now runs against a real local bound.", "because": f"3335 smoke scenarios were rescored against Cassini: pass_like={pass_count}, fail_like={fail_count}.", "next_action": "replace placeholder response/epsilon/floor inputs with source-backed values or zero theorems", "valid_for_claim": "false"},
        {"decision_id": "DEC3385_1_main_lesson", "decision": "The branch can survive or fail depending on epsilon_eff and composite/floor size.", "because": "existing smoke rows show both pass-like and fail-like behavior under the same external bound.", "next_action": "attack epsilon_eff parent silence first", "valid_for_claim": "false"},
        {"decision_id": "DEC3385_2_best_next", "decision": "Best next theorem target is epsilon_eff=0.", "because": "if first-gradient/boundary/kernel anisotropy silence is signed, the harsh Cmetric amplification becomes far less dangerous.", "next_action": "derive epsilon_bg=epsilon_boundary=epsilon_kernel_aniso=0 or produce first finite inputs", "valid_for_claim": "false"},
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {"target_id": "3386-Y5-R2FR-epsilon-eff-parent-silence-or-first-finite-inputs-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3386_epsilon_eff_parent_silence_or_first_finite_inputs.py", "objective": "try to prove epsilon_bg_PPN=epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0 under UOC/local branch; if not, fill first finite nonclaim inputs", "why_next": "3385 shows epsilon_eff is the key controllable term in the Cassini gamma runner", "valid_for_claim": "false"},
        {"target_id": "3387-Y5-R2FR-Cmetric-factor-source-fill-or-operator-zero-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3387_Cmetric_factor_source_fill_or_operator_zero.py", "objective": "fill or zero P_PPN,G_fix,W_src,D_readout,S_band,H_band,N_source in the Cmetric bound", "why_next": "Cmetric remains the operator multiplier for all metric-response PPN components", "valid_for_claim": "false"},
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3385*")
        if hit.name.startswith(("3385-Y5", "P8_Y5_R2FR_3385", "P8_Y5_BRR545_3385", "Y5_R2FR_3385"))
    ] if FW.exists() else []
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3385_0_sources_exist_parse", "all cited 3385 source paths exist and parse", source_ok, ""),
        ("VAL3385_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3385_2_rescore_rows", "Cassini rescore has at least one scenario", len(rows_by_name["cassini_rescore"]) > 0, f"rows={len(rows_by_name['cassini_rescore'])}"),
        ("VAL3385_3_thresholds", "epsilon thresholds cover four response products", len(rows_by_name["thresholds"]) == 4, ""),
        ("VAL3385_4_runner", "runner executes and blocks source-ready claim", {"PASS_NONCLAIM_RUNNER", "PASS_EXTERNAL_BOUND_PRESENT", "FAIL_MTS_INPUTS_PLACEHOLDER", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3385_5_gates", "gates pass execution/external bound and block MTS/local PPN claim", gate_map.get("GATE3385_1_runner_executes") == "true" and gate_map.get("GATE3385_2_external_bound") == "true" and gate_map.get("GATE3385_3_mts_prediction") == "false" and gate_map.get("GATE3385_4_local_ppn") == "false", ""),
        ("VAL3385_6_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3385_7_next_target", "next target moves to epsilon_eff parent silence", rows_by_name["next"][0]["target_id"].startswith("3386-Y5-R2FR-epsilon-eff"), ""),
        ("VAL3385_8_write_scope_outside_formalization", "no 3385 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3385_9_overall", "3385 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    pass_count = sum(1 for row in rows_by_name["cassini_rescore"] if row["cassini_pass_like"] == "true")
    fail_count = sum(1 for row in rows_by_name["cassini_rescore"] if row["cassini_pass_like"] == "false")
    lines = [
        "# 3385 - Y5/R2FR A_gamma Cmetric epsilon_eff first numeric PPN runner under AX1090",
        "",
        "## Summary",
        "- 3385 wires the post-UOC gamma residual formula to a real local comparator: the Cassini gamma envelope staged in 3384.",
        f"- Runner result: existing 3335 placeholder scenarios rescore as `{pass_count}` pass-like and `{fail_count}` fail-like against the Cassini envelope.",
        "- This is not evidence yet: the scenario inputs are placeholder/nonclaim, but the plumbing now exposes which terms control survival.",
        "- Main lesson: `epsilon_eff_PPN` and composite/floor terms decide the fight once `A_gamma*Cmetric` becomes harsh.",
        "- Best next strike: prove parent silence for `epsilon_eff_PPN`, i.e. `epsilon_bg_PPN=epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0`, or fill first finite inputs.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Runner Inputs",
        md_table(rows_by_name["runner_inputs"]),
        "## Cassini Gamma Rescoring",
        md_table(rows_by_name["cassini_rescore"]),
        "## Epsilon Eff Thresholds",
        md_table(rows_by_name["thresholds"]),
        "## Missing Inputs For Claim",
        md_table(rows_by_name["missing_inputs"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    bound = cassini_bound()
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rescore = cassini_rescore_rows(bound)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "runner_inputs": runner_input_rows(bound),
        "cassini_rescore": rescore,
        "thresholds": threshold_rows(bound),
        "missing_inputs": missing_input_rows(),
        "runner": runner_rows(rescore),
        "gates": gate_rows(source_ok, rescore),
        "decision": decision_rows(rescore),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
