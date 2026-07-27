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

import Y5_R2FR_4902_Higgs_Yukawa_mass_gate as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), default=str
        )
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
        (
            "SRC4902_15_checkpoint",
            POST
            / "4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md",
            "MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902",
        ),
        (
            "SRC4902_16_formal",
            FORMAL / "918-PPC4161-Higgs-Yukawa-mass-ownership.md",
            "PPC4161_HIGGS_YUKAWA_MASS_OWNERSHIP_4902",
        ),
        (
            "SRC4902_17_claim",
            FORMAL / "02-claims-register.csv",
            "L-744",
        ),
        (
            "SRC4902_18_variables",
            FORMAL / "04-variable-audit.csv",
            "HiggsStatus4902_MTS",
        ),
        (
            "SRC4902_19_equations",
            FORMAL / "05-equation-register.md",
            "1.195 Higgs ownership",
        ),
        (
            "SRC4902_20_redteam",
            FORMAL / "06-consistency-red-team.md",
            "146. CP2 has the right dimension",
        ),
        (
            "SRC4902_21_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4902",
        ),
        (
            "SRC4902_22_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_HIGGS_YUKAWA_MASS_OWNERSHIP_4902",
        ),
        (
            "SRC4902_23_research",
            SCRIPTS / "Y5_R2FR_4902_Higgs_Yukawa_mass_gate.py",
            "def CP2_custodial_gate",
        ),
        (
            "SRC4902_24_gate",
            SCRIPTS / "Y5_R2FR_4902_Higgs_Yukawa_mass_gate_validation.py",
            "VAL4902_OVERALL",
        ),
    ]
    for source_id, path, marker in outputs:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "generated_local_text_or_code",
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "source_checked_date": "2026-07-11",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    groups: dict[str, list[dict[str, Any]]] = {}
    mapping = (
        ("HIGGS_OWNER", "owner"),
        ("CP2_GEOMETRY", "CP2_geometry"),
        ("CP2_CUSTODIAL", "CP2_custodial"),
        ("LINEAR_HIGGS", "linear_Higgs"),
        ("EW_IDENTIFIABILITY", "EW_identifiability"),
        ("YUKAWA_RANK", "Yukawa"),
        ("LEGACY_MASS_AUDIT", "legacy_mass"),
        ("NEUTRINO_BRANCH", "neutrino"),
        ("PROMOTION_GATE", "promotion"),
    )
    for output_name, section_name in mapping:
        section = sections[section_name]
        groups[output_name] = tagged(section["rows"])
        groups[f"{output_name}_SUMMARY"] = tagged(
            [scalar_summary(section, {"rows"})]
        )
    arbitration = sections["arbitration"]
    groups["ARBITRATION"] = tagged([arbitration])
    groups["DECISION"] = tagged(
        [
            {
                "overall_decision": calculation["decision"],
                "primitive_Higgs_status": arbitration["primitive_Higgs_status"],
                "CP2_precision_status": arbitration["CP2_precision_status"],
                "Yukawa_status": arbitration["Yukawa_status"],
                "next_target": arbitration["next_target"],
                "all_checks_pass": calculation["all_checks_pass"],
            }
        ]
    )
    return groups


def validation_rows(
    calculation: dict[str, Any],
    sources: list[dict[str, Any]],
    groups: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    sections = calculation["sections"]
    owner = sections["owner"]
    geometry = sections["CP2_geometry"]
    custodial = sections["CP2_custodial"]
    linear = sections["linear_Higgs"]
    identifiability = sections["EW_identifiability"]
    Yukawa = sections["Yukawa"]
    legacy = sections["legacy_mass"]
    neutrino = sections["neutrino"]
    promotion = sections["promotion"]
    arbitration = sections["arbitration"]
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4901_VALIDATION.csv"
    )
    claims_register = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-744"
    ]
    variable_symbols = (
        "HiggsOwner4902_MTS",
        "CP2Higgs4902_MTS",
        "FSMetric4902_MTS",
        "CP2Rho4902_MTS",
        "LinearHiggs4902_MTS",
        "EWJacobian4902_MTS",
        "YukawaRank4902_MTS",
        "LegacyMass4902_MTS",
        "NuMass4902_MTS",
        "HiggsGate4902_MTS",
        "CustodialTarget4902_MTS",
        "HiggsStatus4902_MTS",
    )
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    new_variables = [
        row for row in variable_rows if row["symbol"] in variable_symbols
    ]
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in variable_symbols
    }
    variable_sources_exist = True
    for row in new_variables:
        for source_path in row["source_files"].split(";"):
            variable_sources_exist = (
                variable_sources_exist and (ROOT / source_path).exists()
            )
    checkpoint = (
        POST
        / "4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "918-PPC4161-Higgs-Yukawa-mass-ownership.md"
    ).read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(
        encoding="utf-8"
    )
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(
        encoding="utf-8"
    )
    spine = (FORMAL / "07-unification-spine.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / "P8_Y5_R2FR_4902_SOURCE_REGISTER.csv",
        *[OUTPUT / f"P8_Y5_R2FR_4902_{name}.csv" for name in groups],
    ]
    rows = [
        check("VAL4902_00_prior", bool(previous_validation) and previous_validation[-1]["check_id"] == "VAL4901_OVERALL" and previous_validation[-1]["status"] == "PASS", "4901 validation inherited"),
        check("VAL4902_01_sources", sections["sources"]["passed"] and all(row["source_exists"] and row["marker_found"] for row in sources), "all local and primary source markers exist"),
        check("VAL4902_02_owner", owner["passed"] and not owner["primitive_real_scalar_is_Higgs"] and owner["CP2_conditional_representation_owner"], "real scalar rejected and CP2 representation clue retained"),
        check("VAL4902_03_owner_limit", not owner["CP2_potential_and_vacuum_owner"] and owner["linear_Higgs_correspondence_required"], "CP2 potential and vacuum remain open"),
        check("VAL4902_04_CP2_dimension", geometry["passed"] and geometry["real_dimension"] == 4 and geometry["complex_doublets"] == 1, "CP2 contains exactly one complex tangent doublet"),
        check("VAL4902_05_FS_metric", geometry["metric_positive"] and geometry["metric_determinant"] == "f**4/(r2 + 1)**3", "Fubini-Study metric is positive"),
        check("VAL4902_06_potential_no_go", not geometry["nonconstant_SU3_invariant_potential_exists"] and geometry["explicit_breaking_required"], "transitivity forbids a nonconstant invariant potential"),
        check("VAL4902_07_CP2_rho", custodial["passed"] and custodial["rho"] == "t**2 + 1" and custodial["rho_minus_one"] == "t**2", "raw CP2 custodial relation derived"),
        check("VAL4902_08_CP2_blocked", not custodial["rho_exactly_one_at_nonzero_tangent"] and not custodial["CP2_Higgs_branch_precision_ready"], "CP2 branch blocked pending custodial completion"),
        check("VAL4902_09_linear", linear["passed"] and linear["neutral_determinant"] == "0" and linear["rho"] == "1", "linear Higgs known limit closes"),
        check("VAL4902_10_linear_inputs", not linear["Higgs_potential_parameters_derived_from_MTS"] and not linear["vacuum_scale_derived_from_MTS"], "linear Higgs parameters remain inputs"),
        check("VAL4902_11_EW_rank", identifiability["passed"] and identifiability["jacobian_rank"] == 4 and identifiability["generic_full_rank"], "electroweak calibration map is full rank"),
        check("VAL4902_12_EW_prediction", not identifiability["independent_MTS_relation_in_four_observable_block"], "no extra relation claimed in the four-observable block"),
        check("VAL4902_13_Yukawa", Yukawa["passed"] and Yukawa["charged_flavor_parameters"] == 13 and Yukawa["charged_mass_and_CKM_observables"] == 13, "charged flavor parameter and observable ranks match"),
        check("VAL4902_14_mass_not_predicted", not Yukawa["Yukawa_matrices_derived_from_MTS"] and not Yukawa["charged_mass_spectrum_predicted"], "Yukawa inverse map is not mislabeled prediction"),
        check("VAL4902_15_legacy", legacy["passed"] and legacy["audited_claims"] == 4 and legacy["promoted_claims"] == 0 and legacy["all_assets_retained"], "legacy mass claims remain quarantined with assets retained"),
        check("VAL4902_16_neutrino", neutrino["passed"] and not neutrino["baseline_massive_neutrinos_closed"] and not neutrino["MTS_neutrino_mass_matrix_derived"], "massive-neutrino ownership remains open"),
        check("VAL4902_17_neutrino_options", neutrino["Weinberg_operator_available_as_correspondence"] and neutrino["seesaw_available_as_correspondence"], "honest neutrino correspondence options recorded"),
        check("VAL4902_18_promotion", promotion["passed"] and promotion["total_clauses"] == 12 and not promotion["primitive_Higgs_mass_reentry_allowed"] and promotion["linear_correspondence_closed"], "primitive gate blocked while linear known limit closes"),
        check("VAL4902_19_arbitration", arbitration["passed"] and arbitration["linear_Higgs_status"] == "EXPLICIT_LINEAR_HIGGS_CORRESPONDENCE_RETAINED_AS_ACTIVE_KNOWN_LIMIT" and not arbitration["public_claim_allowed"], "private nonclaim arbitration passes"),
        check("VAL4902_20_claim", len(claims_register) == 1 and claims_register[0]["status"] == "primitive_Higgs_Yukawa_mass_origin_not_derived_CP2_doublet_kinetic_conditional_custodial_gate_failed_linear_Higgs_correspondence_active_parameters_imported_private_nonclaim", "L-744 unique private nonclaim status"),
        check("VAL4902_21_variables", len(new_variables) == 12 and all(variable_counts[symbol] == 1 for symbol in variable_symbols), "twelve checkpoint variables are unique"),
        check("VAL4902_22_variable_sources", variable_sources_exist, "all checkpoint variable source paths exist"),
        check("VAL4902_23_documents", "MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902" in checkpoint and "PPC4161_HIGGS_YUKAWA_MASS_OWNERSHIP_4902" in formal_note, "checkpoint and formal markers exist"),
        check("VAL4902_24_registers", "1.195 Higgs ownership" in equations and "146. CP2 has the right dimension" in redteam and "PPC4161 checkpoint 4902" in spine, "equation red-team and spine registers updated"),
        check("VAL4902_25_resume", "PPC4161_HIGGS_YUKAWA_MASS_OWNERSHIP_4902" in resume and NEXT_TARGET in resume, "resume and 4903 handoff updated"),
        check("VAL4902_26_placeholders", not any("MISSING_" in str(value) for row in all_rows for value in row.values()), "no placeholder evidence rows"),
        check("VAL4902_27_nonclaim", all(not row["valid_for_claim"] for row in all_rows), "all generated evidence remains private nonclaim"),
        check("VAL4902_28_csv", all(path.exists() and read_csv(path) for path in output_paths), f"{len(output_paths)} evidence CSVs parse"),
        check("VAL4902_29_scripts", compile_source(SCRIPTS / "Y5_R2FR_4902_Higgs_Yukawa_mass_gate.py") and compile_source(SCRIPTS / "Y5_R2FR_4902_Higgs_Yukawa_mass_gate_validation.py"), "research and validation scripts compile"),
        check("VAL4902_30_pycache", not (SCRIPTS / "__pycache__").exists(), "no post-checkpoint script pycache"),
        check("VAL4902_31_next", NEXT_TARGET in checkpoint and arbitration["next_target"] == NEXT_TARGET, "4903 custodial completion target selected"),
        check("VAL4902_32_internal", calculation["all_checks_pass"], "4902 calculation internally passes"),
    ]
    rows.append(check("VAL4902_OVERALL", all(row["status"] == "PASS" for row in rows), "MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902_VALIDATED"))
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4902_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4902_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4902_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4902_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4902_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
