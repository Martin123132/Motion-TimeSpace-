from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4904_unified_action_Ward_parameter_ledger as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    if hasattr(value, "item"):
        return value.item()
    return value


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        normalized = {key: serializable(value) for key, value in row.items()}
        normalized["valid_for_claim"] = False
        normalized["timestamp_utc"] = TIMESTAMP
        output.append(normalized)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return False
    return True


def scalar_summary(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    outputs = [
        ("SRC4904_13_checkpoint", POST / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md", "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904"),
        ("SRC4904_14_formal", FORMAL / "920-PPC4161-current-unified-action-and-parameter-ledger.md", "PPC4161_CURRENT_UNIFIED_ACTION_PARAMETER_LEDGER_4904"),
        ("SRC4904_15_claim", FORMAL / "02-claims-register.csv", "L-746"),
        ("SRC4904_16_variables", FORMAL / "04-variable-audit.csv", "UnifiedStatus4904_MTS"),
        ("SRC4904_17_equations", FORMAL / "05-equation-register.md", "1.197 Current unified action"),
        ("SRC4904_18_redteam", FORMAL / "06-consistency-red-team.md", "148. A unified action is not yet a predictive unification"),
        ("SRC4904_19_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4904"),
        ("SRC4904_20_resume", POST / "CURRENT_LOCAL_RESUME.md", "PPC4161_CURRENT_UNIFIED_ACTION_PARAMETER_LEDGER_4904"),
        ("SRC4904_21_research", SCRIPTS / "Y5_R2FR_4904_unified_action_Ward_parameter_ledger.py", "def Ward_interface_ledger"),
        ("SRC4904_22_gate", SCRIPTS / "Y5_R2FR_4904_unified_action_Ward_parameter_ledger_validation.py", "VAL4904_OVERALL"),
    ]
    for source_id, path, marker in outputs:
        exists = path.exists()
        content = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        rows.append({"source_id": source_id, "source_type": "generated_local_text_or_code", "source_path_or_url": str(path), "local_path_required": True, "source_exists": exists, "marker": marker, "marker_found": marker in content, "source_checked_date": "2026-07-11"})
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    groups: dict[str, list[dict[str, Any]]] = {}
    mapping = (("SECTORS", "sectors"), ("ACTION", "action"), ("EW_ROTATION", "EW_rotation"), ("NO_DOUBLE_COUNTING", "double_counting"), ("WARD", "Ward"), ("BOUNDARY", "boundary"), ("PARAMETERS", "parameters"), ("LIMITS", "limits"), ("PREDICTIONS", "predictions"), ("ASSEMBLY_GATE", "assembly"))
    for output_name, section_name in mapping:
        section = sections[section_name]
        groups[output_name] = tagged(section["rows"])
        excluded = {"rows", "extension_rows"}
        groups[f"{output_name}_SUMMARY"] = tagged([scalar_summary(section, excluded)])
        if section_name == "parameters":
            groups["PARAMETER_EXTENSIONS"] = tagged(section["extension_rows"])
    arbitration = sections["arbitration"]
    groups["ARBITRATION"] = tagged([arbitration])
    groups["DECISION"] = tagged([{"overall_decision": calculation["decision"], "MTS_low_energy_status": arbitration["MTS_low_energy_status"], "Ward_status": arbitration["Ward_status"], "parameter_status": arbitration["parameter_status"], "prediction_status": arbitration["prediction_status"], "next_target": arbitration["next_target"], "all_checks_pass": calculation["all_checks_pass"]}])
    return groups


def validation_rows(calculation: dict[str, Any], sources: list[dict[str, Any]], groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    s = calculation["sections"]
    sectors, action, rotation, double = s["sectors"], s["action"], s["EW_rotation"], s["double_counting"]
    Ward, boundary, parameters, limits = s["Ward"], s["boundary"], s["parameters"], s["limits"]
    predictions, assembly, arbitration = s["predictions"], s["assembly"], s["arbitration"]
    previous = read_csv(OUTPUT / "P8_Y5_BRR545_4903_VALIDATION.csv")
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-746"]
    symbols = ("UnifiedAction4904_MTS", "ActiveSector4904_MTS", "MTSResidual4904_MTS", "EWRotation4904_MTS", "NoDoubleCount4904_MTS", "Ward4904_MTS", "ExchangeMatrix4904_MTS", "Boundary4904_MTS", "ParameterCount4904_MTS", "LimitMap4904_MTS", "PredictionGap4904_MTS", "UnifiedStatus4904_MTS")
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected = [row for row in variables if row["symbol"] in symbols]
    counts = {symbol: sum(row["symbol"] == symbol for row in variables) for symbol in symbols}
    variable_sources_exist = all((ROOT / path).exists() for row in selected for path in row["source_files"].split(";"))
    checkpoint = (POST / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md").read_text(encoding="utf-8")
    formal_note = (FORMAL / "920-PPC4161-current-unified-action-and-parameter-ledger.md").read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [OUTPUT / "P8_Y5_R2FR_4904_SOURCE_REGISTER.csv", *[OUTPUT / f"P8_Y5_R2FR_4904_{name}.csv" for name in groups]]
    rows = [
        check("VAL4904_00_prior", bool(previous) and previous[-1]["check_id"] == "VAL4903_OVERALL" and previous[-1]["status"] == "PASS", "4903 validation inherited"),
        check("VAL4904_01_sources", s["sources"]["passed"] and all(row["source_exists"] and row["marker_found"] for row in sources), "all source markers exist"),
        check("VAL4904_02_sectors", sectors["passed"] and sectors["sectors"] == 10 and sectors["active_extra_MTS_source_terms"] == 0, "active frozen and retired sectors separated"),
        check("VAL4904_03_action", action["passed"] and action["active_baseline_condition"] == "Gamma_MTS,res=0" and action["active_terms"] == 9, "current action assembled"),
        check("VAL4904_04_rotation", rotation["passed"] and rotation["rotation_rank"] == 2 and rotation["UV_gauge_bosons"] == rotation["IR_gauge_bosons"] == 12, "electroweak IR rotation preserves field count"),
        check("VAL4904_05_no_extra_photon", not rotation["independent_extra_QED_photon"] and double["extra_photon_count"] == 0, "QED is not duplicated"),
        check("VAL4904_06_double_count", double["passed"] and double["clauses"] == double["closed_clauses"] == 10, "all no-double-counting clauses close"),
        check("VAL4904_07_Ward", Ward["passed"] and Ward["total_source_conserved"] and Ward["all_internal_exchange_columns_sum_zero"], "Ward exchange closes"),
        check("VAL4904_08_exchange_rank", Ward["rank"] == 2 and Ward["connected_components"] == 2 and Ward["column_sums"] == "0;0;0", "exchange incidence matrix reproduces"),
        check("VAL4904_09_boundary", boundary["passed"] and boundary["two_derivative_variational_problem_closed"] and not boundary["higher_derivative_nonperturbative_problem_closed"], "boundary scope explicit"),
        check("VAL4904_10_parameters", parameters["passed"] and parameters["SM_baseline_parameters"] == 19 and parameters["active_GR_plus_SM_baseline_parameters"] == 21, "parameter count reproduces"),
        check("VAL4904_11_parameter_basis", parameters["basis_double_count_free"] and parameters["active_novel_MTS_parameters"] == 0, "parameter basis is independent"),
        check("VAL4904_12_neutrino_counts", parameters["Dirac_neutrino_total"] == 28 and parameters["Majorana_neutrino_total"] == 30, "neutrino extension counts explicit"),
        check("VAL4904_13_limits", limits["passed"] and limits["known_limits_closed"] == 6 and not limits["novel_MTS_extension_closed"], "known-limit ladder closes honestly"),
        check("VAL4904_14_predictions", predictions["passed"] and predictions["active_novel_MTS_numeric_predictions"] == 0 and predictions["competitive_prediction_gap_open"], "prediction gap explicit"),
        check("VAL4904_15_assembly", assembly["passed"] and assembly["assembly_passed"] and assembly["closed_clauses"] == 12, "assembly gate closes"),
        check("VAL4904_16_arbitration", arbitration["passed"] and arbitration["current_action_status"] == "ONE_DIFF_COVARIANT_RENORMALIZED_GR_PLUS_SM_EFT_ASSEMBLED_WITHOUT_DOUBLE_COUNTING" and not arbitration["public_unified_theory_claim_allowed"], "private arbitration passes"),
        check("VAL4904_17_claim", len(claims) == 1 and claims[0]["status"] == "current_diff_covariant_GR_plus_SM_EFT_assembled_no_double_counting_Ward_interfaces_closed_twenty_one_baseline_inputs_active_novel_MTS_prediction_gap_explicit_private_nonclaim", "L-746 unique private status"),
        check("VAL4904_18_variables", len(selected) == 12 and all(counts[symbol] == 1 for symbol in symbols), "twelve variables unique"),
        check("VAL4904_19_variable_sources", variable_sources_exist, "all variable sources exist"),
        check("VAL4904_20_documents", "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904" in checkpoint and "PPC4161_CURRENT_UNIFIED_ACTION_PARAMETER_LEDGER_4904" in formal_note, "checkpoint and formal markers exist"),
        check("VAL4904_21_registers", "1.197 Current unified action" in equations and "148. A unified action is not yet a predictive unification" in redteam and "PPC4161 checkpoint 4904" in spine, "formal registers updated"),
        check("VAL4904_22_resume", "PPC4161_CURRENT_UNIFIED_ACTION_PARAMETER_LEDGER_4904" in resume and NEXT_TARGET in resume, "resume and 4905 handoff updated"),
        check("VAL4904_23_placeholders", not any("MISSING_" in str(value) for row in all_rows for value in row.values()), "no placeholders"),
        check("VAL4904_24_nonclaim", all(not row["valid_for_claim"] for row in all_rows), "all evidence private nonclaim"),
        check("VAL4904_25_csv", all(path.exists() and read_csv(path) for path in output_paths), f"{len(output_paths)} evidence CSVs parse"),
        check("VAL4904_26_scripts", compile_source(SCRIPTS / "Y5_R2FR_4904_unified_action_Ward_parameter_ledger.py") and compile_source(SCRIPTS / "Y5_R2FR_4904_unified_action_Ward_parameter_ledger_validation.py"), "scripts compile"),
        check("VAL4904_27_pycache", not (SCRIPTS / "__pycache__").exists(), "no pycache"),
        check("VAL4904_28_next", NEXT_TARGET in checkpoint and arbitration["next_target"] == NEXT_TARGET, "first nontrivial operator target selected"),
        check("VAL4904_29_internal", calculation["all_checks_pass"], "calculation internally passes"),
    ]
    rows.append(check("VAL4904_OVERALL", all(row["status"] == "PASS" for row in rows), "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904_VALIDATED"))
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4904_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4904_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4904_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4904_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4904_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
