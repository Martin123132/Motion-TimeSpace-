from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as research


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUN = POST / "runs" / "20260712-4912-checkpoint"
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


def source_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "SRC4912_00_predecessor",
            POST
            / "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md",
            "MTS_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911",
            "validated_predecessor",
        ),
        (
            "SRC4912_01_predecessor_validation",
            OUTPUT / "P8_Y5_BRR545_4911_VALIDATION.csv",
            "VAL4911_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4912_02_TT_determinant",
            POST
            / "4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md",
            "MTS_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910",
            "dense_validated_TT_response",
        ),
        (
            "SRC4912_03_geometric_matrix",
            OUTPUT / "P8_Y5_R2FR_4911_TEMPLATE_MATRIX.csv",
            "G00,0,D1_grad_R_squared",
            "rank_eight_geometric_templates",
        ),
        (
            "SRC4912_04_checkpoint",
            POST
            / "4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md",
            research.MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4912_05_formal_note",
            FORMAL
            / "928-PPC4161-independent-continuum-TTT-and-matched-subtraction.md",
            research.FORMAL_MARKER,
            "generated_formal_note",
        ),
        (
            "SRC4912_06_provenance",
            POST
            / "source-intake"
            / "microscopic_vertex"
            / "4912"
            / "PROVENANCE.md",
            "MTS_INDEPENDENT_CONTINUUM_TTT_PROVENANCE_4912",
            "generated_provenance",
        ),
        (
            "SRC4912_07_research_script",
            SCRIPTS
            / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector.py",
            "def matched_subtraction_contract_rows",
            "generated_research_code",
        ),
        (
            "SRC4912_08_validation_script",
            SCRIPTS
            / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector_validation.py",
            "VAL4912_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4912_09_claim_register",
            FORMAL / "02-claims-register.csv",
            "L-754",
            "generated_register",
        ),
        (
            "SRC4912_10_variable_register",
            FORMAL / "04-variable-audit.csv",
            "MatchedDifference4912_MTS",
            "generated_register",
        ),
        (
            "SRC4912_11_equation_register",
            FORMAL / "05-equation-register.md",
            "1.205 Independent determinant recovery and matched subtraction",
            "generated_register",
        ),
        (
            "SRC4912_12_redteam",
            FORMAL / "06-consistency-red-team.md",
            "156. A correct continuum projector does not rescue a contaminated absolute lattice coefficient",
            "generated_register",
        ),
        (
            "SRC4912_13_spine",
            FORMAL / "07-unification-spine.md",
            research.FORMAL_MARKER,
            "generated_register",
        ),
        (
            "SRC4912_14_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
            "generated_resume",
        ),
        (
            "SRC4912_15_run_status",
            RUN / "status.json",
            '"status": "COMPLETE"',
            "long_run_record",
        ),
        (
            "SRC4912_16_run_log",
            RUN / "log.txt",
            "continuum_residual=9.376e-16",
            "long_run_record",
        ),
        (
            "SRC4912_17_completion_marker",
            RUN / "COMPLETE.marker",
            "MTS_4912_COMPLETE",
            "long_run_record",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = ""
        if exists:
            raw = path.read_bytes()
            content = raw.decode(
                "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8",
                errors="replace",
            )
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": research.checkpoint_4911.sha256(path)
                if exists
                else "",
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

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4911_VALIDATION.csv")
    taylor = read_csv(OUTPUT / "P8_Y5_R2FR_4912_TAYLOR_VALIDATION.csv")
    contacts = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_VOLUME_CONTACT_DERIVATIVES.csv"
    )
    continuum_response = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_Q6_RESPONSES.csv"
    )
    continuum = read_csv(OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_RECOVERY.csv")
    continuum_leave = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_LEAVE_ONE.csv"
    )
    lattice_response = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_FREE_Q6_RESPONSES.csv"
    )
    coefficients = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_QUOTIENT_COEFFICIENTS.csv"
    )
    lattice = read_csv(OUTPUT / "P8_Y5_R2FR_4912_QUOTIENT_RECOVERY.csv")
    lattice_leave = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_LEAVE_ONE_GEOMETRY.csv"
    )
    cutoff = read_csv(OUTPUT / "P8_Y5_R2FR_4912_CUTOFF_FITS.csv")
    subtraction = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_MATCHED_SUBTRACTION_CONTRACT.csv"
    )
    arbitration = read_csv(OUTPUT / "P8_Y5_R2FR_4912_ARBITRATION.csv")
    interacting = read_csv(
        OUTPUT / "P8_Y5_R2FR_4912_INTERACTING_RUN_GATE.csv"
    )
    local = read_csv(OUTPUT / "P8_Y5_R2FR_4912_LOCAL_LIMIT_GATE.csv")
    decision = read_csv(OUTPUT / "P8_Y5_R2FR_4912_DECISION.csv")[0]
    run_status = read_csv(OUTPUT / "P8_Y5_R2FR_4912_RUN_STATUS.csv")[0]

    arbitration_status = {row["route"]: row["status"] for row in arbitration}
    interacting_status = {
        row["gate"]: row["status"] for row in interacting
    }
    local_status = {row["arena"]: row["status"] for row in local}

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-754"
    ]
    claim_status = (
        "traceful_determinant_contacts_exact_direct_continuum_"
        "multigeometry_free_C3_recovered_two_mass_scaling_pass_absolute_"
        "coarse_lattice_rejected_matched_subtraction_selected_paired_"
        "interacting_smoke_next_active_residual_zero_private_nonclaim"
    )
    symbols = (
        "TracefulVolumeContact4912_MTS",
        "MomentumTaylorJet4912_MTS",
        "DirectContinuumTTT4912_MTS",
        "ContinuumQuadrature4912_MTS",
        "ContinuumRecovery4912_MTS",
        "MassScaling4912_MTS",
        "LatticeNearest4912_MTS",
        "LatticeImproved4912_MTS",
        "HypercubicResidual4912_MTS",
        "AbsoluteLatticeGate4912_MTS",
        "UVSoftness4912_MTS",
        "MatchedDifference4912_MTS",
        "InteractingGate4912_MTS",
        "ResidualStatus4912_MTS",
    )
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected_variables = [
        row for row in variables if row.get("symbol") in symbols
    ]
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variables)
        for symbol in symbols
    }
    variable_sources_exist = all(
        (ROOT / relative).exists()
        for row in selected_variables
        for relative in row["source_files"].split(";")
    )

    checkpoint_path = (
        POST
        / "4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md"
    )
    formal_path = (
        FORMAL
        / "928-PPC4161-independent-continuum-TTT-and-matched-subtraction.md"
    )
    provenance_path = (
        POST / "source-intake" / "microscopic_vertex" / "4912" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    output_paths = sorted(OUTPUT.glob("P8_Y5_R2FR_4912_*.csv"))
    all_rows: list[dict[str, Any]] = sources.copy()
    for path in output_paths:
        all_rows.extend(read_csv(path))
    scripts = [
        SCRIPTS
        / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector.py",
        SCRIPTS
        / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector_validation.py",
    ]

    rows = [
        check(
            "VAL4912_00_prior",
            bool(prior)
            and prior[-1]["check_id"] == "VAL4911_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4911 validation inherited",
        ),
        check(
            "VAL4912_01_sources",
            len(sources) == 18
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all parent generated register and run sources exist",
        ),
        check(
            "VAL4912_02_Taylor_count",
            len(taylor) == 6 and all(row["passed"] == "True" for row in taylor),
            "direct Taylor propagator and traceful contact tests all pass",
        ),
        check(
            "VAL4912_03_TT_direct",
            finite_float(taylor[0], "absolute_residual") < 2e-18,
            "arbitrary direct response reproduces dense-validated 4910 TT result",
        ),
        check(
            "VAL4912_04_Taylor_six",
            finite_float(taylor[1], "absolute_residual") < 2e-18
            and finite_float(taylor[2], "absolute_residual") < 3e-16,
            "sixth-order Taylor response and inverse recurrence reproduce",
        ),
        check(
            "VAL4912_05_traceful_contacts",
            max(finite_float(row, "absolute_residual") for row in taylor[3:])
            < 1e-16
            and len(contacts) == 3
            and {row["contact"] for row in contacts}
            == {"first", "pair", "triple"},
            "first pair and triple traceful volume contacts are exact",
        ),
        check(
            "VAL4912_06_continuum_response_count",
            len(continuum_response) == 24
            and {row["config"] for row in continuum_response}
            == {"C64_A8_m1", "C64_A8_m2"}
            and {row["geometry_id"] for row in continuum_response}
            == {f"G{index:02d}" for index in range(12)}
            and max(
                abs(finite_float(row, "complex_q6_imag"))
                for row in continuum_response
            )
            < 1e-14,
            "two complete real twelve-geometry continuum responses exist",
        ),
        check(
            "VAL4912_07_continuum_recovery",
            len(continuum) == 2
            and all(finite_float(row, "response_residual") < 1e-14 for row in continuum)
            and all(
                abs(finite_float(row, "zeta_m2_over_target") - 1.0) < 5e-12
                for row in continuum
            ),
            "independent continuum determinant recovers exact quotient",
        ),
        check(
            "VAL4912_08_mass_scaling",
            {finite_float(row, "mass") for row in continuum} == {1.0, 2.0}
            and abs(
                finite_float(continuum[0], "zeta_m2")
                - finite_float(continuum[1], "zeta_m2")
            )
            < 1e-20,
            "inverse-mass-squared scaling is exact at two masses",
        ),
        check(
            "VAL4912_09_continuum_leave_one",
            len(continuum_leave) == 24
            and min(
                finite_float(row, "zeta_m2_over_target")
                for row in continuum_leave
            )
            > 0.99999999999
            and max(
                finite_float(row, "zeta_m2_over_target")
                for row in continuum_leave
            )
            < 1.00000000001,
            "every continuum leave-one projection recovers the target",
        ),
        check(
            "VAL4912_10_lattice_response_count",
            len(lattice_response) == 48
            and len({row["config"] for row in lattice_response}) == 4
            and max(
                abs(finite_float(row, "complex_q6_imag"))
                for row in lattice_response
            )
            < 1e-14,
            "four complete real lattice-control response matrices exist",
        ),
        check(
            "VAL4912_11_lattice_coefficients",
            len(coefficients) == 48
            and len({row["config"] for row in coefficients}) == 4,
            "all four quotient representatives contain twelve coefficients",
        ),
        check(
            "VAL4912_12_lattice_rejection",
            len(lattice) == 4
            and all(finite_float(row, "response_residual") > 0.15 for row in lattice)
            and all(
                abs(finite_float(row, "zeta_m2_over_target")) > 1000
                for row in lattice
            ),
            "absolute coarse-lattice responses fail covariant image and magnitude gates",
        ),
        check(
            "VAL4912_13_lattice_leave_one",
            len(lattice_leave) == 48
            and min(
                finite_float(row, "zeta_m2_over_target")
                for row in lattice_leave
            )
            < -8000
            and max(
                finite_float(row, "zeta_m2_over_target")
                for row in lattice_leave
            )
            > 4000,
            "coarse absolute source dependence is explicitly unstable",
        ),
        check(
            "VAL4912_14_cutoff_diagnostics",
            len(cutoff) == 2
            and all(row["valid_continuum_fit"] == "False" for row in cutoff)
            and all("coarse" in row["fit_model"] for row in cutoff),
            "two-point coarse lines are explicitly invalidated",
        ),
        check(
            "VAL4912_15_subtraction_contract",
            len(subtraction) == 6
            and any("Delta y_a" in row["equation"] for row in subtraction)
            and any("lambda/p^(8/3)" in row["equation"] for row in subtraction),
            "matched subtraction and UV-softness contracts are complete",
        ),
        check(
            "VAL4912_16_arbitration",
            arbitration_status["independent_continuum_determinant_rank8_projector"]
            == "PASS"
            and arbitration_status["absolute_coarse_lattice_q6_projection"]
            == "REJECTED"
            and arbitration_status["same_regulator_free_subtraction"]
            == "SELECTED"
            and arbitration_status["unsubtracted_interacting_absolute_coefficient"]
            == "PROHIBITED",
            "continuum and matched routes win the explicit arbitration",
        ),
        check(
            "VAL4912_17_interacting_gate",
            interacting_status["traceful_determinant_contacts"] == "PASS"
            and interacting_status["independent_continuum_free_recovery"] == "PASS"
            and interacting_status["absolute_lattice_free_recovery"] == "FAIL"
            and interacting_status["matched_subtraction_contract"]
            == "READY_FOR_PAIRED_SMOKE"
            and interacting_status["interacting_long_run"] == "DO_NOT_RUN_YET"
            and interacting_status["active_residual"] == "ZERO_PRESERVED",
            "only the paired short interacting route is authorized",
        ),
        check(
            "VAL4912_18_local_limits",
            local_status["GR_Newton_PPN"] == "UNCHANGED"
            and local_status["Maxwell_Poynting"] == "UNCHANGED"
            and local_status["Gamma_MTS_res"] == "ZERO",
            "GR Newton PPN Maxwell and active residual remain unchanged",
        ),
        check(
            "VAL4912_19_decision",
            decision["continuum_pass"] == "True"
            and decision["absolute_lattice_pass"] == "False"
            and decision["matched_subtraction_selected"] == "True"
            and decision["interacting_long_run_launched"] == "False"
            and decision["Gamma_MTS_res"] == "0"
            and decision["next_target"] == NEXT_TARGET,
            "decision preserves zero and selects 4913 paired smoke",
        ),
        check(
            "VAL4912_20_run_status",
            run_status["profile"] == "checkpoint"
            and run_status["validation_pass"] == "True"
            and run_status["continuum_pass"] == "True"
            and run_status["all_finite"] == "True"
            and RUN.joinpath("COMPLETE.marker").exists(),
            "checkpoint run log status and completion marker close",
        ),
        check(
            "VAL4912_21_claim",
            len(claims) == 1 and claims[0]["status"] == claim_status,
            "L-754 is unique and accurately scoped",
        ),
        check(
            "VAL4912_22_variables",
            len(selected_variables) == len(symbols)
            and all(variable_counts[symbol] == 1 for symbol in symbols),
            "fourteen checkpoint variables are unique",
        ),
        check(
            "VAL4912_23_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4912_24_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_INDEPENDENT_CONTINUUM_TTT_PROVENANCE_4912"
            in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4912_25_registers",
            "1.205 Independent determinant recovery and matched subtraction"
            in equations
            and "156. A correct continuum projector does not rescue a contaminated absolute lattice coefficient"
            in redteam
            and "PPC4161 checkpoint 4912" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4912_26_resume",
            (
                "Last checkpoint: `4912-" in resume
                or "Last checkpoint: `4913-" in resume
            )
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume preserves the 4912 marker and reaches its 4913 successor",
        ),
        check(
            "VAL4912_27_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no placeholder markers",
        ),
        check(
            "VAL4912_28_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no nonfinite numeric cells",
        ),
        check(
            "VAL4912_29_nonclaim",
            all(str(row.get("valid_for_claim")) == "False" for row in all_rows),
            "all generated rows remain private nonclaim",
        ),
        check(
            "VAL4912_30_csv",
            len(output_paths) == 17
            and all(path.exists() and read_csv(path) for path in output_paths),
            "seventeen evidence CSVs parse",
        ),
        check(
            "VAL4912_31_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4912_32_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4912_33_next",
            NEXT_TARGET in checkpoint
            and (
                not (POST / NEXT_TARGET).exists()
                or "MTS_MATCHED_INTERACTING_TTT_SMOKE_4913"
                in (POST / NEXT_TARGET).read_text(
                    encoding="utf-8", errors="replace"
                )
            ),
            "4913 is selected and is either pending or marker-valid",
        ),
    ]
    rows.append(
        check(
            "VAL4912_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_FREE_LATTICE_MULTIGEOMETRY_CONTINUUM_PROJECTOR_4912_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4912_SOURCE_REGISTER.csv", sources)
    validation = validation_rows(sources)
    write_csv(OUTPUT / "P8_Y5_BRR545_4912_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4912_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4912_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
