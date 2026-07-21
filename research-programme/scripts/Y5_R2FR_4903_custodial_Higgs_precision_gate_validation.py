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

import Y5_R2FR_4903_custodial_Higgs_precision_gate as research  # noqa: E402


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
        ("SRC4903_09_checkpoint", POST / "4903-Y5-R2FR-custodial-Higgs-coset-completion-and-electroweak-precision-or-linear-Higgs-freeze.md", "MTS_CUSTODIAL_HIGGS_COMPLETION_PRECISION_GATE_4903"),
        ("SRC4903_10_formal", FORMAL / "919-PPC4161-custodial-Higgs-completion-and-freeze.md", "PPC4161_CUSTODIAL_HIGGS_COMPLETION_FREEZE_4903"),
        ("SRC4903_11_claim", FORMAL / "02-claims-register.csv", "L-745"),
        ("SRC4903_12_variables", FORMAL / "04-variable-audit.csv", "HiggsStatus4903_MTS"),
        ("SRC4903_13_equations", FORMAL / "05-equation-register.md", "1.196 Custodial Higgs"),
        ("SRC4903_14_redteam", FORMAL / "06-consistency-red-team.md", "147. A custodial completion can be viable"),
        ("SRC4903_15_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4903"),
        ("SRC4903_16_resume", POST / "CURRENT_LOCAL_RESUME.md", "PPC4161_CUSTODIAL_HIGGS_COMPLETION_FREEZE_4903"),
        ("SRC4903_17_research", SCRIPTS / "Y5_R2FR_4903_custodial_Higgs_precision_gate.py", "def Higgs_coupling_map"),
        ("SRC4903_18_gate", SCRIPTS / "Y5_R2FR_4903_custodial_Higgs_precision_gate_validation.py", "VAL4903_OVERALL"),
    ]
    for source_id, path, marker in outputs:
        exists = path.exists()
        content = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        rows.append({"source_id": source_id, "source_type": "generated_local_text_or_code", "source_path_or_url": str(path), "local_path_required": True, "source_exists": exists, "marker": marker, "marker_found": marker in content, "source_checked_date": "2026-07-11"})
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    groups: dict[str, list[dict[str, Any]]] = {}
    mapping = (("COSET", "coset"), ("MASS_GATE", "mass"), ("COUPLING_MAP", "couplings"), ("PRIMARY_BOUND", "bound"), ("COMPARATOR", "comparator"), ("OWNERSHIP_GATE", "ownership"))
    for output_name, section_name in mapping:
        section = sections[section_name]
        groups[output_name] = tagged(section["rows"])
        groups[f"{output_name}_SUMMARY"] = tagged([scalar_summary(section, {"rows"})])
    arbitration = sections["arbitration"]
    groups["ARBITRATION"] = tagged([arbitration])
    groups["DECISION"] = tagged([{"overall_decision": calculation["decision"], "custodial_construction_status": arbitration["custodial_construction_status"], "precision_status": arbitration["precision_status"], "CP2_Higgs_status": arbitration["CP2_Higgs_status"], "next_target": arbitration["next_target"], "all_checks_pass": calculation["all_checks_pass"]}])
    return groups


def validation_rows(calculation: dict[str, Any], sources: list[dict[str, Any]], groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    sections = calculation["sections"]
    coset, mass, couplings, bound = sections["coset"], sections["mass"], sections["couplings"], sections["bound"]
    comparator, ownership, arbitration = sections["comparator"], sections["ownership"], sections["arbitration"]
    previous = read_csv(OUTPUT / "P8_Y5_BRR545_4902_VALIDATION.csv")
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-745"]
    symbols = ("CustodialCoset4903_MTS", "Sigma4903_MTS", "CustodialRho4903_MTS", "Xi4903_MTS", "KappaV4903_MTS", "Kappa2V4903_MTS", "HHBound4903_MTS", "CompletionCompare4903_MTS", "ParentOwnership4903_MTS", "CustodialGate4903_MTS", "UnifiedRedirect4903_MTS", "HiggsStatus4903_MTS")
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected = [row for row in variables if row["symbol"] in symbols]
    counts = {symbol: sum(row["symbol"] == symbol for row in variables) for symbol in symbols}
    variable_sources_exist = all((ROOT / path).exists() for row in selected for path in row["source_files"].split(";"))
    checkpoint = (POST / "4903-Y5-R2FR-custodial-Higgs-coset-completion-and-electroweak-precision-or-linear-Higgs-freeze.md").read_text(encoding="utf-8")
    formal_note = (FORMAL / "919-PPC4161-custodial-Higgs-completion-and-freeze.md").read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [OUTPUT / "P8_Y5_R2FR_4903_SOURCE_REGISTER.csv", *[OUTPUT / f"P8_Y5_R2FR_4903_{name}.csv" for name in groups]]
    rows = [
        check("VAL4903_00_prior", bool(previous) and previous[-1]["check_id"] == "VAL4902_OVERALL" and previous[-1]["status"] == "PASS", "4902 validation inherited"),
        check("VAL4903_01_sources", sections["sources"]["passed"] and all(row["source_exists"] and row["marker_found"] for row in sources), "all source markers exist"),
        check("VAL4903_02_coset", coset["passed"] and coset["Goldstone_count"] == 4 and coset["complex_Higgs_doublets"] == 1, "minimal field-count coset constructed"),
        check("VAL4903_03_custodial_group", coset["custodial_SU2R_present"] and not coset["nonconstant_invariant_potential"], "custodial group and potential limit explicit"),
        check("VAL4903_04_not_unique", coset["minimal_in_pNGB_field_count"] and not coset["unique_group_theoretic_completion"] and not coset["selected_by_MTS_parent"], "minimality not overclaimed"),
        check("VAL4903_05_mass", mass["passed"] and mass["rho"] == "1" and mass["rho_minus_one"] == "0" and mass["photon_mass_squared"] == "0", "custodial mass theorem passes"),
        check("VAL4903_06_couplings", couplings["passed"] and couplings["kappa_V"] == "sqrt(1 - xi)" and couplings["kappa_2V"] == "1 - 2*xi", "Higgs coupling modifiers derived"),
        check("VAL4903_07_correlation", couplings["coupling_relation_residual"] == "0" and not couplings["fermion_modifier_unique"], "gauge correlation closes without overclaiming flavor"),
        check("VAL4903_08_bound_source", bound["passed"] and bound["observed_kappa2V_lower"] == 0.73 and bound["observed_kappa2V_upper"] == 1.3, "primary interval recorded"),
        check("VAL4903_09_bound_translation", bound["xi_max_fraction"] == "27/200" and abs(bound["f_over_v_min"] - 2.721655269759087) < 1e-12, "conditional xi and f/v bounds reproduce"),
        check("VAL4903_10_bound_scope", bound["valid_as_conditional_smoke_bound"] and not bound["full_experimental_likelihood_reproduced"], "interval smoke not mislabeled likelihood"),
        check("VAL4903_11_compare", comparator["passed"] and comparator["same_minimal_scalar_count"] and comparator["CP2_custodial_failure_repaired"], "three routes compared consistently"),
        check("VAL4903_12_no_primitive_gain", not comparator["MTS_primitive_improvement"], "new group does not fake primitive ownership"),
        check("VAL4903_13_ownership", ownership["passed"] and ownership["total_clauses"] == 12 and not ownership["primitive_custodial_Higgs_reentry"] and ownership["linear_Higgs_fallback_closed"], "parent gate blocks promotion"),
        check("VAL4903_14_arbitration", arbitration["passed"] and arbitration["active_Higgs_status"] == "LINEAR_STANDARD_MODEL_HIGGS_CORRESPONDENCE_REMAINS_ACTIVE" and not arbitration["primitive_Higgs_claim_allowed"] and not arbitration["public_precision_claim_allowed"], "route arbitration passes"),
        check("VAL4903_15_claim", len(claims) == 1 and claims[0]["status"] == "custodial_SO5_over_SO4_completion_derived_precision_smoke_passes_conditionally_parent_selection_absent_CP2_Higgs_frozen_linear_Higgs_active_private_nonclaim", "L-745 unique private status"),
        check("VAL4903_16_variables", len(selected) == 12 and all(counts[symbol] == 1 for symbol in symbols), "twelve variables unique"),
        check("VAL4903_17_variable_sources", variable_sources_exist, "all variable source paths exist"),
        check("VAL4903_18_documents", "MTS_CUSTODIAL_HIGGS_COMPLETION_PRECISION_GATE_4903" in checkpoint and "PPC4161_CUSTODIAL_HIGGS_COMPLETION_FREEZE_4903" in formal_note, "checkpoint and formal markers exist"),
        check("VAL4903_19_registers", "1.196 Custodial Higgs" in equations and "147. A custodial completion can be viable" in redteam and "PPC4161 checkpoint 4903" in spine, "formal registers updated"),
        check("VAL4903_20_resume", "PPC4161_CUSTODIAL_HIGGS_COMPLETION_FREEZE_4903" in resume and NEXT_TARGET in resume, "resume and 4904 handoff updated"),
        check("VAL4903_21_placeholders", not any("MISSING_" in str(value) for row in all_rows for value in row.values()), "no placeholders"),
        check("VAL4903_22_nonclaim", all(not row["valid_for_claim"] for row in all_rows), "all evidence private nonclaim"),
        check("VAL4903_23_csv", all(path.exists() and read_csv(path) for path in output_paths), f"{len(output_paths)} evidence CSVs parse"),
        check("VAL4903_24_scripts", compile_source(SCRIPTS / "Y5_R2FR_4903_custodial_Higgs_precision_gate.py") and compile_source(SCRIPTS / "Y5_R2FR_4903_custodial_Higgs_precision_gate_validation.py"), "scripts compile"),
        check("VAL4903_25_pycache", not (SCRIPTS / "__pycache__").exists(), "no pycache"),
        check("VAL4903_26_next", NEXT_TARGET in checkpoint and arbitration["next_target"] == NEXT_TARGET, "unified-action target selected"),
        check("VAL4903_27_internal", calculation["all_checks_pass"], "calculation internally passes"),
    ]
    rows.append(check("VAL4903_OVERALL", all(row["status"] == "PASS" for row in rows), "MTS_CUSTODIAL_HIGGS_COMPLETION_PRECISION_GATE_4903_VALIDATED"))
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4903_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4903_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4903_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4903_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4903_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
