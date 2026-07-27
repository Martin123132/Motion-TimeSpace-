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

import Y5_R2FR_4900_charged_matter_QED_gate as research  # noqa: E402


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
            "SRC4900_15_checkpoint",
            POST
            / "4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md",
            "MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900",
        ),
        (
            "SRC4900_16_formal",
            FORMAL
            / "916-PPC4161-charged-matter-audit-and-Dirac-QED-correspondence.md",
            "PPC4161_CHARGED_MATTER_AND_DIRAC_QED_4900",
        ),
        (
            "SRC4900_17_claim",
            FORMAL / "02-claims-register.csv",
            "L-742",
        ),
        (
            "SRC4900_18_variables",
            FORMAL / "04-variable-audit.csv",
            "ParticleStatus4900_MTS",
        ),
        (
            "SRC4900_19_equations",
            FORMAL / "05-equation-register.md",
            "1.193 Charged-matter representation",
        ),
        (
            "SRC4900_20_redteam",
            FORMAL / "06-consistency-red-team.md",
            "144. A winding label is not a fermion representation",
        ),
        (
            "SRC4900_21_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4900",
        ),
        (
            "SRC4900_22_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_CHARGED_MATTER_AND_DIRAC_QED_4900",
        ),
        (
            "SRC4900_23_research",
            SCRIPTS / "Y5_R2FR_4900_charged_matter_QED_gate.py",
            "def corpus_field_content_audit",
        ),
        (
            "SRC4900_24_gate",
            SCRIPTS / "Y5_R2FR_4900_charged_matter_QED_gate_validation.py",
            "VAL4900_OVERALL",
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
    corpus = sections["corpus"]
    representation = sections["representation"]
    claims = sections["claims"]
    solver = sections["solver"]
    correspondence = sections["correspondence"]
    beta = sections["beta"]
    primitive = sections["primitive_gate"]
    arbitration = sections["arbitration"]
    return {
        "CORPUS_FIELD_CONTENT": tagged(corpus["rows"]),
        "CORPUS_FIELD_SUMMARY": tagged(
            [scalar_summary(corpus, {"rows", "all_paths"})]
        ),
        "REPRESENTATION_NO_GO": tagged(representation["rows"]),
        "REPRESENTATION_SUMMARY": tagged(
            [scalar_summary(representation, {"rows"})]
        ),
        "PARTICLE_CLAIM_AUDIT": tagged(claims["rows"]),
        "PARTICLE_CLAIM_SUMMARY": tagged(
            [scalar_summary(claims, {"rows"})]
        ),
        "LEPTON_SOLVER": tagged(solver["rows"]),
        "LEPTON_RATIOS": tagged(solver["ratio_rows"]),
        "LEPTON_SOLVER_SUMMARY": tagged(
            [scalar_summary(solver, {"rows", "ratio_rows"})]
        ),
        "DIRAC_QED_CORRESPONDENCE": tagged(correspondence["rows"]),
        "DIRAC_QED_SUMMARY": tagged(
            [scalar_summary(correspondence, {"rows"})]
        ),
        "QED_BETA_SPECTRA": tagged(beta["rows"]),
        "QED_BETA_SUMMARY": tagged([scalar_summary(beta, {"rows"})]),
        "PRIMITIVE_PARTICLE_GATE": tagged(primitive["rows"]),
        "PRIMITIVE_PARTICLE_GATE_SUMMARY": tagged(
            [scalar_summary(primitive, {"rows"})]
        ),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "primitive_particle_status": arbitration[
                        "primitive_particle_status"
                    ],
                    "QED_beta_status": arbitration["QED_beta_status"],
                    "classical_only_freeze_status": arbitration[
                        "classical_only_freeze_status"
                    ],
                    "next_target": arbitration["next_target"],
                    "all_checks_pass": calculation["all_checks_pass"],
                }
            ]
        ),
    }


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
    corpus = sections["corpus"]
    representation = sections["representation"]
    claims = sections["claims"]
    solver = sections["solver"]
    correspondence = sections["correspondence"]
    beta = sections["beta"]
    primitive = sections["primitive_gate"]
    arbitration = sections["arbitration"]
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4899_VALIDATION.csv"
    )
    claims_register = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-742"
    ]
    variable_symbols = (
        "ParticleFieldAudit4900_MTS",
        "FermionNoGo4900_MTS",
        "Winding4900_MTS",
        "LeptonSolver4900_MTS",
        "DiracQED4900_MTS",
        "ChargeRep4900_MTS",
        "Bqed4900_MTS",
        "AlphaRun4900_MTS",
        "ParticleGate4900_MTS",
        "ParticleStatus4900_MTS",
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
        / "4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "916-PPC4161-charged-matter-audit-and-Dirac-QED-correspondence.md"
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
        OUTPUT / "P8_Y5_R2FR_4900_SOURCE_REGISTER.csv",
        *[OUTPUT / f"P8_Y5_R2FR_4900_{name}.csv" for name in groups],
    ]
    rows = [
        check(
            "VAL4900_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4899_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4899 validation inherited",
        ),
        check(
            "VAL4900_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"] for row in sources
            ),
            "all parent particle and primary source markers exist",
        ),
        check(
            "VAL4900_02_corpus_files",
            corpus["passed"] and corpus["files_scanned"] == 12,
            "all twelve particle files scanned",
        ),
        check(
            "VAL4900_03_missing_field_content",
            corpus["critical_objects_present"] == 0
            and not corpus["primitive_Dirac_QED_field_content_present"]
            and all(not row["present"] for row in corpus["rows"]),
            "no Grassmann Dirac Clifford spinor U1 or spin-statistics owner found",
        ),
        check(
            "VAL4900_04_representation_no_go",
            representation["passed"]
            and not representation["primitive_charged_fermion_derived"]
            and not representation["winding_charge_map_derived"],
            "scalar winding route does not derive charged fermions",
        ),
        check(
            "VAL4900_05_three_family",
            not representation["exact_three_family_theorem"]
            and not representation["topological_fermion_route_present"],
            "exactly-three and topological-fermion theorems remain absent",
        ),
        check(
            "VAL4900_06_claim_audit",
            claims["passed"]
            and claims["audited_claims"] == 6
            and claims["current_particle_claims"] == 0,
            "six particle claims quarantined with assets retained",
        ),
        check(
            "VAL4900_07_claim_paths",
            claims["all_source_paths_exist"],
            "all audited particle source paths exist",
        ),
        check(
            "VAL4900_08_solver_rows",
            solver["passed"]
            and len(solver["rows"]) == 12
            and len(solver["ratio_rows"]) == 4,
            "lepton code reproduced on four radial cutoffs",
        ),
        check(
            "VAL4900_09_solver_reproduction",
            solver["published_R40_reproduction_error"] < 1.0e-10,
            "published R=40 ratios reproduce",
        ),
        check(
            "VAL4900_10_solver_nonlocalized",
            solver["all_R80_boundary_values_nonzero"]
            and solver["all_mass_growth_exponents_near_three"]
            and not solver["finite_energy_soliton_established"],
            "profiles do not decay and mass integral grows approximately R cubed",
        ),
        check(
            "VAL4900_11_solver_inputs",
            solver["amplitude_inputs"] == 3
            and solver["target_mass_ratios"] == 2
            and "FITTED" in solver["mass_prediction_status"],
            "three selected amplitudes are not parameter-free eigenvalues",
        ),
        check(
            "VAL4900_12_QED_correspondence",
            correspondence["passed"]
            and correspondence["correspondence_gate_passed"]
            and correspondence["correspondence_module_status"]
            == "EXPLICIT_STANDARD_DIRAC_QED_CORRESPONDENCE_ADOPTED",
            "standard Dirac QED known-limit module closes by explicit adoption",
        ),
        check(
            "VAL4900_13_QED_not_primitive",
            not correspondence["primitive_MTS_fermion_derivation"],
            "correspondence module is not mislabeled scalar emergence",
        ),
        check(
            "VAL4900_14_anomalies",
            correspondence["gauge_anomaly_per_Dirac"] == "q^3+(-q)^3=0"
            and correspondence["mixed_gravity_anomaly_per_Dirac"]
            == "q+(-q)=0",
            "vectorlike Dirac anomaly cancellation is explicit",
        ),
        check(
            "VAL4900_15_beta",
            beta["passed"]
            and beta["spectrum_rows"] == 5
            and "2 alpha^2" in beta["beta_alpha_general"],
            "one-loop QED beta law and five spectrum rows generated",
        ),
        check(
            "VAL4900_16_beta_nonuniqueness",
            beta["inverse_running_spread_at_ratio"] > 10.0
            and not beta["current_parent_B_effective_derived"],
            "unfixed spectrum gives materially different running",
        ),
        check(
            "VAL4900_17_beta_scalar",
            sum(row["primitive_scalar_compatible"] for row in beta["rows"])
            == 1
            and next(
                row for row in beta["rows"] if row["primitive_scalar_compatible"]
            )["B_effective_Dirac_units"]
            == 0.25,
            "complex scalar and Dirac vacuum polarization are distinguished",
        ),
        check(
            "VAL4900_18_primitive_gate",
            primitive["passed"]
            and primitive["total_clauses"] == 10
            and primitive["passed_clauses"] == 1
            and not primitive["primitive_particle_reentry_allowed"],
            "primitive particle derivation gate remains closed",
        ),
        check(
            "VAL4900_19_arbitration",
            arbitration["passed"]
            and arbitration["QED_correspondence_status"]
            == "EXPLICIT_STANDARD_DIRAC_QED_CORRESPONDENCE_ADOPTED",
            "QED correspondence arbitration passes",
        ),
        check(
            "VAL4900_20_freeze",
            arbitration["classical_only_freeze_status"]
            == "AVOIDED_BY_EXPLICIT_STANDARD_DIRAC_QED_CORRESPONDENCE_MODULE"
            and arbitration["current_particle_claim_count"] == 0,
            "classical-only freeze avoided without reviving primitive claims",
        ),
        check(
            "VAL4900_21_claim",
            len(claims_register) == 1
            and claims_register[0]["status"]
            == "primitive_scalar_particle_claims_quarantined_explicit_Dirac_QED_correspondence_adopted_beta_function_conditional_spectrum_not_derived_private_nonclaim",
            "L-742 unique private nonclaim status",
        ),
        check(
            "VAL4900_22_variables",
            len(new_variables) == 10
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4900_23_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4900_24_documents",
            "MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900"
            in checkpoint
            and "PPC4161_CHARGED_MATTER_AND_DIRAC_QED_4900" in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4900_25_registers",
            "1.193 Charged-matter representation" in equations
            and "144. A winding label is not a fermion representation"
            in redteam
            and "PPC4161 checkpoint 4900" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4900_26_resume",
            "PPC4161_CHARGED_MATTER_AND_DIRAC_QED_4900" in resume
            and NEXT_TARGET in resume,
            "resume and 4901 handoff updated",
        ),
        check(
            "VAL4900_27_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4900_28_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4900_29_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4900_30_scripts",
            compile_source(SCRIPTS / "Y5_R2FR_4900_charged_matter_QED_gate.py")
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4900_charged_matter_QED_gate_validation.py"
            ),
            "research and validation scripts compile",
        ),
        check(
            "VAL4900_31_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4900_32_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4901 nonabelian chiral gauge target selected",
        ),
        check(
            "VAL4900_33_internal",
            calculation["all_checks_pass"],
            "4900 calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4900_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4900_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4900_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4900_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4900_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4900_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
