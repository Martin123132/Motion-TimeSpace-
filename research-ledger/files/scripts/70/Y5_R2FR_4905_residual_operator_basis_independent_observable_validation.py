from __future__ import annotations

import csv
import json
import math
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

import Y5_R2FR_4905_residual_operator_basis_independent_observable as research  # noqa: E402


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


def scalar_summary(section: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in section.items()
        if key != "rows"
    }


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    generated = [
        (
            "SRC4905_12_checkpoint",
            POST
            / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md",
            research.MARKER,
        ),
        (
            "SRC4905_13_formal",
            FORMAL / "921-PPC4161-first-residual-operator-and-independent-test.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4905_14_claim",
            FORMAL / "02-claims-register.csv",
            "L-747",
        ),
        (
            "SRC4905_15_variables",
            FORMAL / "04-variable-audit.csv",
            "IndependentGate4905_MTS",
        ),
        (
            "SRC4905_16_equations",
            FORMAL / "05-equation-register.md",
            "1.198 First residual basis",
        ),
        (
            "SRC4905_17_redteam",
            FORMAL / "06-consistency-red-team.md",
            "149. An operator candidate is not active",
        ),
        (
            "SRC4905_18_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4905",
        ),
        (
            "SRC4905_19_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4905_20_research",
            SCRIPTS
            / "Y5_R2FR_4905_residual_operator_basis_independent_observable.py",
            "def nonlocal_response_basis",
        ),
        (
            "SRC4905_21_validation",
            SCRIPTS
            / "Y5_R2FR_4905_residual_operator_basis_independent_observable_validation.py",
            "VAL4905_OVERALL",
        ),
    ]
    for source_id, path, marker in generated:
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
    mapping = (
        ("FIELDS", "fields"),
        ("FACTORIZATION", "factorization"),
        ("REDUCTION", "reduction"),
        ("DIMENSION_SIX_BASIS", "basis"),
        ("CUBIC_MATCHING", "matching"),
        ("HEAVY_VISIBILITY", "visibility"),
        ("NONLOCAL_RESPONSE", "response"),
        ("NO_SLIP_SAMPLES", "samples"),
        ("WARD_REENTRY", "Ward"),
        ("INDEPENDENT_GATE", "gate"),
        ("ARBITRATION", "arbitration"),
    )
    groups: dict[str, list[dict[str, Any]]] = {}
    for output_name, section_name in mapping:
        section = sections[section_name]
        groups[output_name] = tagged(section["rows"])
        groups[f"{output_name}_SUMMARY"] = tagged([scalar_summary(section)])
    groups["DECISION"] = tagged(
        [
            {
                "overall_decision": calculation["decision"],
                "direct_MTS_SM_threshold_status": sections["arbitration"][
                    "direct_MTS_SM_threshold_status"
                ],
                "first_local_operator": sections["arbitration"][
                    "first_local_operator"
                ],
                "first_competitive_candidate": sections["arbitration"][
                    "first_competitive_candidate"
                ],
                "active_novel_MTS_numeric_predictions": sections[
                    "arbitration"
                ]["active_novel_MTS_numeric_predictions"],
                "next_target": calculation["next_target"],
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
    fields = sections["fields"]
    factorization = sections["factorization"]
    reduction = sections["reduction"]
    basis = sections["basis"]
    matching = sections["matching"]
    visibility = sections["visibility"]
    response = sections["response"]
    samples = sections["samples"]
    ward = sections["Ward"]
    gate = sections["gate"]
    arbitration = sections["arbitration"]

    previous = read_csv(OUTPUT / "P8_Y5_BRR545_4904_VALIDATION.csv")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-747"
    ]
    symbols = (
        "ResidualBasis4905_MTS",
        "Factorization4905_MTS",
        "DirectPortal4905_MTS",
        "GRSMEFTBasis4905_MTS",
        "WeylCubic4905_MTS",
        "CubicCoefficient4905_MTS",
        "HeavyLoopVisibility4905_MTS",
        "FormFactorR4905_MTS",
        "FormFactorC4905_MTS",
        "ResponseA04905_MTS",
        "ResponseA24905_MTS",
        "MuDyn4905_MTS",
        "MuLens4905_MTS",
        "NoSlip4905_MTS",
        "IndependentGate4905_MTS",
    )
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected = [row for row in variables if row["symbol"] in symbols]
    counts = {
        symbol: sum(row["symbol"] == symbol for row in variables)
        for symbol in symbols
    }
    variable_sources_exist = all(
        (ROOT / path).exists()
        for row in selected
        for path in row["source_files"].split(";")
    )

    checkpoint = (
        POST
        / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "921-PPC4161-first-residual-operator-and-independent-test.md"
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
        OUTPUT / "P8_Y5_R2FR_4905_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4905_{name}.csv"
            for name in groups
        ],
    ]
    visibility_rows = visibility["rows"]
    ten_solar = visibility_rows[0]
    source_urls = {
        row["source_path_or_url"]
        for row in sources
        if not row["local_path_required"]
    }

    rows = [
        check(
            "VAL4905_00_prior",
            bool(previous)
            and previous[-1]["check_id"] == "VAL4904_OVERALL"
            and previous[-1]["status"] == "PASS",
            "4904 validation inherited",
        ),
        check(
            "VAL4905_01_sources",
            sections["sources"]["passed"]
            and all(row["source_exists"] and row["marker_found"] for row in sources),
            "all local and recorded primary source markers exist",
        ),
        check(
            "VAL4905_02_primary_urls",
            {research.GRSMEFT_URL, research.HEAVY_FIELDS_URL, research.HEAT_KERNEL_URL}
            .issubset(source_urls),
            "three primary web sources recorded",
        ),
        check(
            "VAL4905_03_fields",
            fields["passed"]
            and fields["infrared_extra_MTS_fields"] == 0
            and fields["active_mixed_MTS_SM_vertices"] == 0,
            "active infrared field content frozen",
        ),
        check(
            "VAL4905_04_factorization",
            factorization["passed"]
            and factorization["factorized_determinant"] == "K_MTS*K_SM",
            "fixed-metric determinant factorization reproduces",
        ),
        check(
            "VAL4905_05_direct_portal_zero",
            factorization["direct_MTS_SM_threshold_coefficients"] == 0
            and basis["direct_mixed_MTS_coefficients_nonzero"] == 0,
            "direct mixed MTS threshold portal is zero in stated domain",
        ),
        check(
            "VAL4905_06_reduction",
            reduction["passed"]
            and reduction["first_local_on_shell_dimension"] == 6,
            "lower local operators reduced consistently",
        ),
        check(
            "VAL4905_07_basis",
            basis["passed"]
            and basis["operator_count"] == 10
            and basis["pure_gravity_operators"] == 2
            and basis["mixed_bosonic_operators"] == 8,
            "complete dimension-six gravity basis reproduced",
        ),
        check(
            "VAL4905_08_dimension_seven",
            basis["dimension_seven_new_gravity_operators"] == 0,
            "no new dimension-seven gravity operators",
        ),
        check(
            "VAL4905_09_matching_signs",
            matching["passed"]
            and matching["rows"][0]["sign"] == "positive"
            and matching["rows"][1]["sign"] == "negative"
            and matching["rows"][2]["sign"] == "positive",
            "heavy scalar Dirac vector weights reproduce",
        ),
        check(
            "VAL4905_10_spectral_cancellation",
            matching["equal_mass_one_of_each_signed_weight"] == "0",
            "equal-mass scalar Dirac vector c1 weights cancel",
        ),
        check(
            "VAL4905_11_matching_scope",
            not matching["bare_matching_declared"]
            and not matching["complete_gapped_MTS_spectrum_declared"]
            and not matching["numeric_MTS_coefficient_promoted"],
            "total numeric Weyl-cubic coefficient withheld",
        ),
        check(
            "VAL4905_12_visibility_ratio",
            visibility["passed"]
            and math.isclose(
                visibility["computed_temperature_to_horizon_ratio"],
                -2.0 / 113.0,
                rel_tol=1e-12,
            ),
            "independent Schwarzschild response ratio reproduces",
        ),
        check(
            "VAL4905_13_visibility_size",
            abs(ten_solar["fractional_horizon_shift_one_real_scalar"]) < 1e-80
            and not visibility["local_heavy_loop_selected_as_competitive_route"],
            "local heavy loop rejected as macroscopic route",
        ),
        check(
            "VAL4905_14_response_basis",
            response["passed"]
            and response["mu_lensing"] == "1/A_2",
            "general scalar and spin-two response basis reproduces",
        ),
        check(
            "VAL4905_15_no_slip",
            response["no_slip_dynamic"] == response["no_slip_lensing"]
            and response["no_slip_eta"] == "1"
            and response["form_factor_condition"] == "F_C(q^2)=-3 F_R(q^2)",
            "no-slip theorem closes",
        ),
        check(
            "VAL4905_16_spin_two_relation",
            response["spin_two_relation_residual"] == "0"
            and response["spin_two_lensing_from_dynamic"]
            == "mu_lens=(3 mu_dyn+1)/4",
            "spin-two-only comparator relation closes",
        ),
        check(
            "VAL4905_17_inverse_samples",
            samples["passed"]
            and samples["samples"] == 5
            and all(row["pole_guard_A_positive"] for row in samples["rows"]),
            "inverse no-slip response samples reproduce",
        ),
        check(
            "VAL4905_18_Ward_scope",
            ward["passed"]
            and ward["candidate_Ward_compatible"]
            and not ward["candidate_activation_allowed"],
            "Ward compatibility separated from activation",
        ),
        check(
            "VAL4905_19_independent_split",
            gate["passed"]
            and gate["calibration_observable"] == "galaxy_kinematics_only"
            and gate["independent_target_observable"] == "galaxy_lensing_and_slip"
            and gate["prediction_vector"]
            == "(mu_lens-mu_dyn,eta-1)=(0,0)",
            "independent observable split pre-registered",
        ),
        check(
            "VAL4905_20_activation",
            not gate["promotion_allowed"]
            and gate["closed_clauses"] == 4
            and gate["total_clauses"] == 10,
            "candidate remains inactive with six gates open",
        ),
        check(
            "VAL4905_21_arbitration",
            arbitration["passed"]
            and arbitration["first_local_operator"] == "O_C3"
            and arbitration["active_novel_MTS_numeric_predictions"] == 0
            and not arbitration["public_claim_allowed"],
            "private arbitration is internally consistent",
        ),
        check(
            "VAL4905_22_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "direct_MTS_SM_thresholds_factorized_zero_first_local_Weyl_cubic_nonlocal_no_slip_candidate_selected_independent_lensing_gate_open_private_nonclaim",
            "L-747 unique and scoped",
        ),
        check(
            "VAL4905_23_variables",
            len(selected) == 15
            and all(counts[symbol] == 1 for symbol in symbols),
            "fifteen variables unique",
        ),
        check(
            "VAL4905_24_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4905_25_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note,
            "checkpoint and formal note markers exist",
        ),
        check(
            "VAL4905_26_registers",
            "1.198 First residual basis" in equations
            and "149. An operator candidate is not active" in redteam
            and "PPC4161 checkpoint 4905" in spine,
            "formal registers updated",
        ),
        check(
            "VAL4905_27_resume",
            research.FORMAL_MARKER in resume and NEXT_TARGET in resume,
            "resume handoff updated",
        ),
        check(
            "VAL4905_28_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder markers",
        ),
        check(
            "VAL4905_29_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4905_30_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4905_31_scripts",
            compile_source(
                SCRIPTS
                / "Y5_R2FR_4905_residual_operator_basis_independent_observable.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4905_residual_operator_basis_independent_observable_validation.py"
            ),
            "scripts compile",
        ),
        check(
            "VAL4905_32_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4905_33_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET
            and not (POST / NEXT_TARGET).exists(),
            "4906 handoff selected but not pre-created",
        ),
        check(
            "VAL4905_34_internal",
            calculation["all_checks_pass"],
            "calculation internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4905_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4905_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4905_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4905_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4905_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4905_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
