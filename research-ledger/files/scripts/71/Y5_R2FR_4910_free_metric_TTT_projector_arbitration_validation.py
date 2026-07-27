from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4910_free_metric_TTT_projector_arbitration as research


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": research.MARKER,
            "valid_for_claim": False,
            "source_checked_date": research.CHECKED_DATE,
        }
        for row in rows
    ]


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def finite_float(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f"nonfinite {key}: {row[key]}")
    return value


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    generated = [
        (
            "SRC4910_06_checkpoint",
            POST
            / "4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md",
            research.MARKER,
        ),
        (
            "SRC4910_07_formal_note",
            FORMAL / "926-PPC4161-free-TTT-projector-arbitration.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4910_08_provenance",
            POST
            / "source-intake"
            / "microscopic_vertex"
            / "4910"
            / "PROVENANCE.md",
            "MTS_FREE_TTT_PROJECTOR_PROVENANCE_4910",
        ),
        (
            "SRC4910_09_research_script",
            SCRIPTS / "Y5_R2FR_4910_free_metric_TTT_projector_arbitration.py",
            "def full_basis_projector_contract_rows",
        ),
        (
            "SRC4910_10_validation_script",
            SCRIPTS
            / "Y5_R2FR_4910_free_metric_TTT_projector_arbitration_validation.py",
            "VAL4910_OVERALL",
        ),
        (
            "SRC4910_11_claim_register",
            FORMAL / "02-claims-register.csv",
            "L-752",
        ),
        (
            "SRC4910_12_variable_register",
            FORMAL / "04-variable-audit.csv",
            "ProjectorFailure4910_MTS",
        ),
        (
            "SRC4910_13_equation_register",
            FORMAL / "05-equation-register.md",
            "1.203 Free TTT projector arbitration",
        ),
        (
            "SRC4910_14_redteam",
            FORMAL / "06-consistency-red-team.md",
            "154. Momentum order does not identify an operator",
        ),
        (
            "SRC4910_15_spine",
            FORMAL / "07-unification-spine.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4910_16_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
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
                "sha256": research.sha256(path) if exists else "",
            }
        )
    return tagged(rows)


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4909_VALIDATION.csv")
    dense = read_csv(OUTPUT / "P8_Y5_R2FR_4910_DENSE_MOMENTUM_VALIDATION.csv")
    grid = read_csv(OUTPUT / "P8_Y5_R2FR_4910_FREE_TTT_GRID.csv")
    fits = read_csv(OUTPUT / "P8_Y5_R2FR_4910_NAIVE_C3_FITS.csv")
    failure = read_csv(OUTPUT / "P8_Y5_R2FR_4910_PROJECTOR_FAILURE.csv")[0]
    no_go = read_csv(OUTPUT / "P8_Y5_R2FR_4910_EUCLIDEAN_RICCI_FLAT_NO_GO.csv")
    contaminants = read_csv(OUTPUT / "P8_Y5_R2FR_4910_A6_CONTAMINANTS.csv")
    options = read_csv(OUTPUT / "P8_Y5_R2FR_4910_PROJECTOR_OPTIONS.csv")
    contract = read_csv(OUTPUT / "P8_Y5_R2FR_4910_FULL_BASIS_PROJECTOR_CONTRACT.csv")
    gate = read_csv(OUTPUT / "P8_Y5_R2FR_4910_INTERACTING_RUN_GATE.csv")
    local = read_csv(OUTPUT / "P8_Y5_R2FR_4910_LOCAL_LIMIT_GATE.csv")
    decision = read_csv(OUTPUT / "P8_Y5_R2FR_4910_DECISION.csv")[0]
    gate_status = {row["gate"]: row["status"] for row in gate}
    option_status = {row["route"]: row["status"] for row in options}
    local_status = {row["arena"]: row["status"] for row in local}

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-752"
    ]
    claim_status = (
        "exact_free_metric_TTT_dense_validated_single_real_Euclidean_TT_"
        "Weyl_division_rejected_full_off_shell_a6_template_inverse_"
        "selected_interacting_run_withheld_active_residual_zero_private_"
        "nonclaim"
    )
    symbols = (
        "SymmetricMetricStencil4910_MTS",
        "LatticeMetricVertex4910_MTS",
        "FreeTTT4910_MTS",
        "DenseMomentumResidual4910_MTS",
        "NaiveQ6Fit4910_MTS",
        "ExpectedScalarZeta4910_MTS",
        "ProjectorFailure4910_MTS",
        "EuclideanRicciFlatNoGo4910_MTS",
        "A6Contamination4910_MTS",
        "TemplateMatrix4910_MTS",
        "CorrelatedInverse4910_MTS",
        "ContinuumGate4910_MTS",
        "InteractingRunGate4910_MTS",
        "ResidualStatus4910_MTS",
    )
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected = [row for row in variables if row.get("symbol") in symbols]
    counts = {
        symbol: sum(row.get("symbol") == symbol for row in variables)
        for symbol in symbols
    }
    variable_sources_exist = all(
        (ROOT / relative).exists()
        for row in selected
        for relative in row["source_files"].split(";")
    )

    checkpoint_path = (
        POST
        / "4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md"
    )
    formal_path = FORMAL / "926-PPC4161-free-TTT-projector-arbitration.md"
    provenance_path = (
        POST / "source-intake" / "microscopic_vertex" / "4910" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    output_paths = sorted(OUTPUT.glob("P8_Y5_R2FR_4910_*.csv"))
    all_rows: list[dict[str, Any]] = sources.copy()
    for path in output_paths:
        all_rows.extend(read_csv(path))
    scripts = [
        SCRIPTS / "Y5_R2FR_4910_free_metric_TTT_projector_arbitration.py",
        SCRIPTS
        / "Y5_R2FR_4910_free_metric_TTT_projector_arbitration_validation.py",
    ]

    rows = [
        check(
            "VAL4910_00_prior",
            bool(prior)
            and prior[-1]["check_id"] == "VAL4909_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4909 validation inherited",
        ),
        check(
            "VAL4910_01_sources",
            research.source_contract()["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all local and generated source markers exist",
        ),
        check(
            "VAL4910_02_dense_count",
            len(dense) == 2 and {int(row["size"]) for row in dense} == {3, 4},
            "independent dense checks exist on two complete lattices",
        ),
        check(
            "VAL4910_03_dense_residual",
            all(row["passed"] == "True" for row in dense)
            and max(finite_float(row, "absolute_residual") for row in dense) < 1e-13,
            "dense and momentum TTT implementations agree",
        ),
        check(
            "VAL4910_04_grid",
            len(grid) == 14
            and {int(row["size"]) for row in grid} == {24, 32}
            and {int(row["momentum_scale"]) for row in grid} == set(range(7)),
            "fourteen exact free TTT response rows exist",
        ),
        check(
            "VAL4910_05_grid_real",
            max(abs(finite_float(row, "W123_density_imag")) for row in grid) < 1e-12,
            "momentum-conserving free response is real",
        ),
        check(
            "VAL4910_06_fit_count",
            len(fits) == 6
            and {int(row["maximum_scale"]) for row in fits} == {4, 5, 6},
            "six independent lattice and fit-window extractions exist",
        ),
        check(
            "VAL4910_07_fit_failure",
            all(row["same_sign_as_expected"] == "False" for row in fits)
            and all(row["within_factor_two"] == "False" for row in fits)
            and min(abs(finite_float(row, "naive_over_expected")) for row in fits) > 130,
            "every naive extraction fails sign and magnitude",
        ),
        check(
            "VAL4910_08_expected",
            all(
                math.isclose(
                    finite_float(row, "expected_continuum_scalar_zeta"),
                    1.0 / (30240.0 * (4.0 * math.pi) ** 2),
                    rel_tol=1e-14,
                )
                for row in fits
            ),
            "known scalar coefficient is used consistently",
        ),
        check(
            "VAL4910_09_failure_aggregate",
            int(failure["fit_count"]) == 6
            and 134 < finite_float(failure, "minimum_absolute_naive_over_expected") < 136
            and finite_float(failure, "maximum_absolute_naive_over_expected") > 164
            and failure["naive_projector_pass"] == "False",
            "projector-failure aggregate reproduces",
        ),
        check(
            "VAL4910_10_no_go",
            len(no_go) == 5
            and no_go[-1]["step"] == "theorem"
            and "does not exist" in no_go[-1]["equation"],
            "real periodic Euclidean Ricci-flat Weyl no-go is recorded",
        ),
        check(
            "VAL4910_11_contaminants",
            len(contaminants) == 11
            and all(row["survives_off_shell_TT"] == "True" for row in contaminants)
            and {row["class"] for row in contaminants} == {"derivative", "cubic"},
            "raw derivative and cubic a6 contaminant classes are retained",
        ),
        check(
            "VAL4910_12_options",
            option_status["single_real_Euclidean_TT_triplet"] == "REJECTED"
            and option_status["full_off_shell_a6_template_matrix"] == "SELECTED"
            and option_status["complex_null_on_shell_amplitude"] == "ANALYTIC_CROSSCHECK",
            "corrected projector route is selected explicitly",
        ),
        check(
            "VAL4910_13_contract",
            len(contract) == 8
            and any(row["equation"] == "rank(M)=number of retained independent O_A^(6)" for row in contract)
            and any("zeta_C3=v_A c_A" in row["equation"] for row in contract),
            "full-rank correlated basis-inverse contract is complete",
        ),
        check(
            "VAL4910_14_interacting_gate",
            gate_status["free_triangle_and_seagulls"] == "PASS"
            and gate_status["free_known_C3_recovery"] == "FAIL"
            and gate_status["real_Euclidean_on_shell_projection"] == "THEOREM_BLOCKED"
            and gate_status["interacting_TTT_long_run"] == "DO_NOT_RUN",
            "interacting execution is withheld for the derived reason",
        ),
        check(
            "VAL4910_15_local_limits",
            local_status["massless_spin2_pole"] == "UNCHANGED"
            and local_status["Newton_and_PPN"] == "UNCHANGED"
            and local_status["Maxwell_and_Poynting"] == "UNCHANGED"
            and local_status["Gamma_MTS_res"] == "ZERO",
            "local GR Newton and Maxwell baselines remain unchanged",
        ),
        check(
            "VAL4910_16_decision",
            decision["c6_promoted"] == "False"
            and decision["Gamma_MTS_res"] == "0"
            and decision["all_checks_pass"] == "True"
            and decision["next_target"] == NEXT_TARGET,
            "no failed coefficient enters the active action",
        ),
        check(
            "VAL4910_17_claim",
            len(claims) == 1 and claims[0]["status"] == claim_status,
            "L-752 is unique and scoped",
        ),
        check(
            "VAL4910_18_variables",
            len(selected) == len(symbols)
            and all(counts[symbol] == 1 for symbol in symbols),
            "fourteen checkpoint variables are unique",
        ),
        check(
            "VAL4910_19_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4910_20_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_FREE_TTT_PROJECTOR_PROVENANCE_4910" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4910_21_registers",
            "1.203 Free TTT projector arbitration" in equations
            and "154. Momentum order does not identify an operator" in redteam
            and "PPC4161 checkpoint 4910" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4910_22_resume",
            "Last checkpoint: `4910-" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume handoff points to 4910 and 4911",
        ),
        check(
            "VAL4910_23_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no placeholder markers",
        ),
        check(
            "VAL4910_24_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no nonfinite numeric cells",
        ),
        check(
            "VAL4910_25_nonclaim",
            all(str(row.get("valid_for_claim")) == "False" for row in all_rows),
            "all generated rows remain private nonclaim",
        ),
        check(
            "VAL4910_26_csv",
            len(output_paths) == 12
            and all(path.exists() and read_csv(path) for path in output_paths),
            "twelve evidence CSVs parse",
        ),
        check(
            "VAL4910_27_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4910_28_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4910_29_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4911 is selected but not pre-created",
        ),
    ]
    rows.append(
        check(
            "VAL4910_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4910_SOURCE_REGISTER.csv", sources)
    validation = validation_rows(sources)
    write_csv(OUTPUT / "P8_Y5_BRR545_4910_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4910_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4910_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
