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

import Y5_R2FR_4901_nonabelian_chiral_SM_gate as research  # noqa: E402


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
            "SRC4901_13_checkpoint",
            POST
            / "4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md",
            "MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901",
        ),
        (
            "SRC4901_14_formal",
            FORMAL / "917-PPC4161-nonabelian-chiral-SM-correspondence.md",
            "PPC4161_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_4901",
        ),
        (
            "SRC4901_15_claim",
            FORMAL / "02-claims-register.csv",
            "L-743",
        ),
        (
            "SRC4901_16_variables",
            FORMAL / "04-variable-audit.csv",
            "SMStatus4901_MTS",
        ),
        (
            "SRC4901_17_equations",
            FORMAL / "05-equation-register.md",
            "1.194 Non-Abelian chiral",
        ),
        (
            "SRC4901_18_redteam",
            FORMAL / "06-consistency-red-team.md",
            "145. Anomaly cancellation checks",
        ),
        (
            "SRC4901_19_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4901",
        ),
        (
            "SRC4901_20_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_4901",
        ),
        (
            "SRC4901_21_research",
            SCRIPTS / "Y5_R2FR_4901_nonabelian_chiral_SM_gate.py",
            "def hypercharge_rank_theorem",
        ),
        (
            "SRC4901_22_gate",
            SCRIPTS / "Y5_R2FR_4901_nonabelian_chiral_SM_gate_validation.py",
            "VAL4901_OVERALL",
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
    legacy = sections["legacy_YM"]
    cp2 = sections["CP2"]
    reps = sections["representations"]
    anomalies = sections["anomalies"]
    hypercharge = sections["hypercharge"]
    correspondence = sections["correspondence"]
    primitive = sections["primitive_gate"]
    arbitration = sections["arbitration"]
    return {
        "CORPUS_AUDIT": tagged(corpus["rows"]),
        "CORPUS_SUMMARY": tagged([scalar_summary(corpus, {"rows"})]),
        "LEGACY_YM_AUDIT": tagged(legacy["rows"]),
        "LEGACY_YM_SUMMARY": tagged([scalar_summary(legacy, {"rows"})]),
        "CP2_ROUTE": tagged(cp2["rows"]),
        "CP2_SUMMARY": tagged([scalar_summary(cp2, {"rows"})]),
        "SM_REPRESENTATIONS": tagged(reps["rows"]),
        "SM_REPRESENTATION_SUMMARY": tagged([scalar_summary(reps, {"rows"})]),
        "ANOMALY_LEDGER": tagged(anomalies["rows"]),
        "ANOMALY_SUMMARY": tagged([scalar_summary(anomalies, {"rows"})]),
        "HYPERCHARGE_CONSTRAINTS": tagged(hypercharge["rows"]),
        "HYPERCHARGE_SOLUTION": tagged(hypercharge["solution_rows"]),
        "ELECTRIC_CHARGES": tagged(hypercharge["electric_rows"]),
        "HYPERCHARGE_SUMMARY": tagged(
            [
                scalar_summary(
                    hypercharge,
                    {"rows", "solution_rows", "electric_rows"},
                )
            ]
        ),
        "SM_ACTION": tagged(correspondence["rows"]),
        "ELECTROWEAK_RELATIONS": tagged(correspondence["relation_rows"]),
        "SM_CORRESPONDENCE_SUMMARY": tagged(
            [scalar_summary(correspondence, {"rows", "relation_rows"})]
        ),
        "PRIMITIVE_GATE": tagged(primitive["rows"]),
        "PRIMITIVE_GATE_SUMMARY": tagged(
            [scalar_summary(primitive, {"rows"})]
        ),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "primitive_nonabelian_status": arbitration[
                        "primitive_nonabelian_status"
                    ],
                    "legacy_YM_status": arbitration["legacy_YM_status"],
                    "hypercharge_status": arbitration["hypercharge_status"],
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
    legacy = sections["legacy_YM"]
    cp2 = sections["CP2"]
    reps = sections["representations"]
    anomalies = sections["anomalies"]
    hypercharge = sections["hypercharge"]
    correspondence = sections["correspondence"]
    primitive = sections["primitive_gate"]
    arbitration = sections["arbitration"]
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4900_VALIDATION.csv"
    )
    claims_register = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-743"
    ]
    variable_symbols = (
        "NonAbelianAudit4901_MTS",
        "LegacyYMAudit4901_MTS",
        "CP2GaugeRoute4901_MTS",
        "GSM4901_MTS",
        "SMRep4901_MTS",
        "Anomaly4901_MTS",
        "Witten4901_MTS",
        "HyperchargeRank4901_MTS",
        "Qem4901_MTS",
        "SMAction4901_MTS",
        "SMGate4901_MTS",
        "SMStatus4901_MTS",
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
        / "4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "917-PPC4161-nonabelian-chiral-SM-correspondence.md"
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
        OUTPUT / "P8_Y5_R2FR_4901_SOURCE_REGISTER.csv",
        *[OUTPUT / f"P8_Y5_R2FR_4901_{name}.csv" for name in groups],
    ]
    rows = [
        check(
            "VAL4901_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4900_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4900 validation inherited",
        ),
        check(
            "VAL4901_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"] for row in sources
            ),
            "all local and primary source markers exist",
        ),
        check(
            "VAL4901_02_corpus",
            corpus["passed"] and corpus["files_scanned"] == 26,
            "all core and particle Markdown sources scanned",
        ),
        check(
            "VAL4901_03_legacy_only",
            corpus["only_legacy_YM_owns_nonabelian_labels"]
            and corpus["SU2_files"] == 1
            and corpus["SU3_files"] == 1,
            "only the legacy Yang-Mills file owns non-Abelian labels",
        ),
        check(
            "VAL4901_04_parent_absent",
            not corpus["complete_chiral_nonabelian_parent_present"],
            "no complete chiral non-Abelian parent is present",
        ),
        check(
            "VAL4901_05_legacy_audit",
            legacy["passed"]
            and legacy["audited_clauses"] == 8
            and legacy["valid_clauses"] == 0,
            "legacy Yang-Mills operator chain audited",
        ),
        check(
            "VAL4901_06_legacy_gap",
            not legacy["legacy_mass_gap_claim_valid"]
            and "QUARANTINED" in legacy["legacy_status"],
            "legacy mass-gap claim remains quarantined",
        ),
        check(
            "VAL4901_07_CP2",
            cp2["passed"]
            and cp2["closed_clues"] == 1
            and not cp2["nonabelian_parent_derived"],
            "CP2 retained as a U2 clue rather than promoted",
        ),
        check(
            "VAL4901_08_representations",
            reps["passed"]
            and reps["fermion_multiplets_per_generation"] == 5
            and reps["Higgs_doublets"] == 1,
            "explicit one-generation representation table generated",
        ),
        check(
            "VAL4901_09_families",
            reps["family_count"] == 3
            and reps["family_count_origin"] == "ADOPTED_NOT_MTS_DERIVED",
            "three families are not mislabeled as derived",
        ),
        check(
            "VAL4901_10_anomalies",
            anomalies["passed"]
            and anomalies["local_anomalies_cancel"]
            and len(anomalies["rows"]) == 7,
            "all local anomaly sums vanish exactly",
        ),
        check(
            "VAL4901_11_Witten",
            anomalies["SU2_doublets_per_generation"] == 4
            and anomalies["Witten_global_anomaly_cancelled"],
            "Witten SU2 global anomaly cancels",
        ),
        check(
            "VAL4901_12_anomaly_not_selector",
            not anomalies["anomaly_cancellation_selects_representations"],
            "consistency is not promoted to primitive selection",
        ),
        check(
            "VAL4901_13_hypercharge_rank",
            hypercharge["passed"]
            and hypercharge["rank"] == 5
            and hypercharge["nullity"] == 1,
            "hypercharge matrix has exact rank five and nullity one",
        ),
        check(
            "VAL4901_14_hypercharge_solution",
            hypercharge["normalized_solution"]
            == "1/6;-2/3;1/3;-1/2;1;1/2"
            and all(row["matches_SM"] for row in hypercharge["solution_rows"]),
            "YH normalization reproduces all SM hypercharge ratios",
        ),
        check(
            "VAL4901_15_cubic",
            hypercharge["U1_cubic_after_solution"] == "0",
            "cubic U1 anomaly vanishes on the exact solution",
        ),
        check(
            "VAL4901_16_neutrino_branch",
            hypercharge["right_neutrino_nullity_without_Majorana"] == 2
            and hypercharge["right_neutrino_nullity_with_Ync_zero_Majorana"]
            == 1,
            "right-neutrino ambiguity is explicit",
        ),
        check(
            "VAL4901_17_conditional",
            hypercharge["conditional_hypercharge_ratios_derived"]
            and not hypercharge["primitive_MTS_hypercharge_selector_derived"],
            "conditional theorem is separated from primitive origin",
        ),
        check(
            "VAL4901_18_correspondence",
            correspondence["passed"]
            and correspondence["correspondence_gate_passed"]
            and not correspondence["primitive_nonabelian_origin_derived"],
            "SM known limit closes by explicit correspondence",
        ),
        check(
            "VAL4901_19_parameters",
            "imported_or_calibrated" in correspondence["parameter_status"],
            "gauge Higgs and Yukawa parameters remain explicit inputs",
        ),
        check(
            "VAL4901_20_primitive_gate",
            primitive["passed"]
            and primitive["total_clauses"] == 12
            and not primitive["primitive_nonabelian_reentry_allowed"]
            and primitive["correspondence_fallback_closed"],
            "primitive gate blocked while correspondence fallback closes",
        ),
        check(
            "VAL4901_21_arbitration",
            arbitration["passed"]
            and arbitration["SM_correspondence_status"]
            == "EXPLICIT_ANOMALY_FREE_STANDARD_MODEL_CORRESPONDENCE_MODULE_ADOPTED"
            and not arbitration["public_claim_allowed"],
            "private nonclaim arbitration passes",
        ),
        check(
            "VAL4901_22_claim",
            len(claims_register) == 1
            and claims_register[0]["status"]
            == "primitive_nonabelian_chiral_parent_not_derived_explicit_anomaly_free_SM_correspondence_adopted_hypercharge_ratios_conditional_parameters_imported_private_nonclaim",
            "L-743 unique private nonclaim status",
        ),
        check(
            "VAL4901_23_variables",
            len(new_variables) == 12
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "twelve checkpoint variables are unique",
        ),
        check(
            "VAL4901_24_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4901_25_documents",
            "MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901"
            in checkpoint
            and "PPC4161_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_4901"
            in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4901_26_registers",
            "1.194 Non-Abelian chiral" in equations
            and "145. Anomaly cancellation checks" in redteam
            and "PPC4161 checkpoint 4901" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4901_27_resume",
            "PPC4161_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_4901" in resume
            and NEXT_TARGET in resume,
            "resume and 4902 handoff updated",
        ),
        check(
            "VAL4901_28_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4901_29_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4901_30_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4901_31_scripts",
            compile_source(SCRIPTS / "Y5_R2FR_4901_nonabelian_chiral_SM_gate.py")
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4901_nonabelian_chiral_SM_gate_validation.py"
            ),
            "research and validation scripts compile",
        ),
        check(
            "VAL4901_32_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4901_33_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4902 Higgs Yukawa ownership target selected",
        ),
        check(
            "VAL4901_34_internal",
            calculation["all_checks_pass"],
            "4901 calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4901_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4901_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4901_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4901_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4901_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4901_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
