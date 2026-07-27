from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point as research


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


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    generated = [
        (
            "SRC4909_06_checkpoint",
            POST
            / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md",
            research.MARKER,
        ),
        (
            "SRC4909_07_formal_note",
            FORMAL / "925-PPC4161-motion-scalar-gap-and-TTT-matching.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4909_08_provenance",
            POST
            / "source-intake"
            / "microscopic_vertex"
            / "4909"
            / "PROVENANCE.md",
            "MTS_MOTION_SCALAR_LATTICE_TTT_PROVENANCE_4909",
        ),
        (
            "SRC4909_09_research_script",
            SCRIPTS
            / "Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point.py",
            "def Weyl_cubic_template",
        ),
        (
            "SRC4909_10_validation_script",
            SCRIPTS
            / "Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point_validation.py",
            "VAL4909_OVERALL",
        ),
        (
            "SRC4909_11_claim_register",
            FORMAL / "02-claims-register.csv",
            "L-751",
        ),
        (
            "SRC4909_12_variable_register",
            FORMAL / "04-variable-audit.csv",
            "MassGap4909_MTS",
        ),
        (
            "SRC4909_13_equation_register",
            FORMAL / "05-equation-register.md",
            "1.202 Motion-scalar lattice gap",
        ),
        (
            "SRC4909_14_redteam",
            FORMAL / "06-consistency-red-team.md",
            "153. A stable coarse-lattice mass",
        ),
        (
            "SRC4909_15_spine",
            FORMAL / "07-unification-spine.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4909_16_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4909_17_manifest",
            OUTPUT / "P8_Y5_R2FR_4909_RUN_MANIFEST.json",
            '"profile": "checkpoint"',
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
                "source_type": "generated_local_text_code_or_data",
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": research.sha256(path) if exists else "",
            }
        )
    return tagged(rows)


def finite_float(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f"nonfinite {key}: {row[key]}")
    return value


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4908_VALIDATION.csv")
    scaling = read_csv(OUTPUT / "P8_Y5_R2FR_4909_LATTICE_SCALING.csv")
    local = read_csv(OUTPUT / "P8_Y5_R2FR_4909_LOCAL_DELTA_VALIDATION.csv")[0]
    gaussian = read_csv(OUTPUT / "P8_Y5_R2FR_4909_GAUSSIAN_THIRD_RESPONSE.csv")[0]
    distinct = read_csv(OUTPUT / "P8_Y5_R2FR_4909_GAUSSIAN_DISTINCT_TTT.csv")[0]
    mass_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4909_MASS_GAP_RUNS.csv")
    aggregates = read_csv(OUTPUT / "P8_Y5_R2FR_4909_CUTOFF_AGGREGATES.csv")
    extrapolation = read_csv(OUTPUT / "P8_Y5_R2FR_4909_EXTRAPOLATION.csv")[0]
    volume = read_csv(OUTPUT / "P8_Y5_R2FR_4909_FINITE_VOLUME.csv")[0]
    replicate = read_csv(OUTPUT / "P8_Y5_R2FR_4909_REPLICATE_CONSISTENCY.csv")[0]
    seagulls = read_csv(OUTPUT / "P8_Y5_R2FR_4909_DENSITIZED_SEAGULLS.csv")[0]
    Weyl = read_csv(OUTPUT / "P8_Y5_R2FR_4909_WEYL_CUBIC_TEMPLATE.csv")
    stress = read_csv(OUTPUT / "P8_Y5_R2FR_4909_STRESS_THREE_POINT_GATE.csv")
    decision = read_csv(OUTPUT / "P8_Y5_R2FR_4909_DECISION.csv")[0]
    correlations = read_csv(OUTPUT / "P8_Y5_R2FR_4909_CORRELATIONS.csv")
    manifest = json.loads(
        (OUTPUT / "P8_Y5_R2FR_4909_RUN_MANIFEST.json").read_text(
            encoding="utf-8"
        )
    )

    free = [row for row in mass_rows if row["branch"] == "free_validation"]
    interacting = [row for row in mass_rows if row["branch"] == "literal_MTS"]
    cutoffs = {float(row["mu_hat"]) for row in interacting}
    stress_status = {row["stage"]: row["current_status"] for row in stress}

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-751"
    ]
    claim_status = (
        "finite_lattice_measure_sampler_and_connected_TTT_validated_"
        "mass_gap_pilot_near_mu_promising_not_promoted_nonzero_Weyl_"
        "template_derived_interacting_c6_unmeasured_active_residual_"
        "zero_private_nonclaim"
    )
    symbols = (
        "LatticeField4909_MTS",
        "LatticeCoupling4909_MTS",
        "LiteralTrajectory4909_MTS",
        "MassCorrelator4909_MTS",
        "MassGap4909_MTS",
        "ContinuumFit4909_MTS",
        "FiniteVolume4909_MTS",
        "ReplicaGate4909_MTS",
        "ConnectedTTT4909_MTS",
        "DensitizedSeagull4909_MTS",
        "TTTriplet4909_MTS",
        "WeylTemplate4909_MTS",
        "C6Diagnostic4909_MTS",
        "CountertermGate4909_MTS",
        "ResidualStatus4909_MTS",
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
        / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md"
    )
    formal_path = FORMAL / "925-PPC4161-motion-scalar-gap-and-TTT-matching.md"
    provenance_path = (
        POST / "source-intake" / "microscopic_vertex" / "4909" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    output_paths = sorted(OUTPUT.glob("P8_Y5_R2FR_4909_*.csv"))
    all_rows: list[dict[str, Any]] = sources.copy()
    for path in output_paths:
        all_rows.extend(read_csv(path))
    scripts = [
        SCRIPTS / "Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point.py",
        SCRIPTS
        / "Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point_validation.py",
    ]

    rows = [
        check(
            "VAL4909_00_prior",
            bool(prior)
            and prior[-1]["check_id"] == "VAL4908_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4908 validation inherited",
        ),
        check(
            "VAL4909_01_sources",
            research.source_contract()["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all local and generated source markers exist",
        ),
        check(
            "VAL4909_02_scaling",
            len(scaling) == 7
            and any(row["equation"] == "g_a=(a mu)^(8/3)=mu_hat^(8/3); r_a=0" for row in scaling)
            and any(row["equation"] == "mu_hat=a mu -> 0" for row in scaling),
            "finite lattice and continuum scaling contracts exist",
        ),
        check(
            "VAL4909_03_local_delta",
            local["passed"] == "True"
            and int(local["trials"]) == 64
            and finite_float(local, "max_absolute_delta_action_residual") < 5e-12,
            "local update agrees with full action",
        ),
        check(
            "VAL4909_04_manifest",
            manifest["marker"] == research.MARKER
            and manifest["profile"] == "checkpoint"
            and len(manifest["configs"]) == 7,
            "checkpoint run manifest freezes seven configurations",
        ),
        check(
            "VAL4909_05_free_count",
            len(free) == 1 and len(interacting) == 6 and len(cutoffs) == 4,
            "one free and six interacting rows at four cutoffs exist",
        ),
        check(
            "VAL4909_06_free_mass",
            finite_float(free[0], "free_relative_error") < 0.01
            and math.isclose(
                finite_float(free[0], "expected_free_lattice_mass"),
                2.0 * math.asinh(0.7 / 2.0),
                rel_tol=1e-14,
            ),
            "free lattice mass calibration is below one percent",
        ),
        check(
            "VAL4909_07_interacting_finite",
            all(finite_float(row, "mass_gap_lattice") > 0 for row in interacting)
            and all(0.45 < finite_float(row, "metropolis_acceptance") < 0.55 for row in interacting)
            and all(finite_float(row, "c_m_lattice") > 0 for row in interacting),
            "all interacting runs have finite positive masses and healthy acceptance",
        ),
        check(
            "VAL4909_08_aggregates",
            len(aggregates) == 4
            and math.isclose(min(finite_float(row, "c_m") for row in aggregates), 0.9875948044747319, rel_tol=1e-12)
            and math.isclose(max(finite_float(row, "c_m") for row in aggregates), 1.0974329090247295, rel_tol=1e-12),
            "four largest-volume cutoff aggregates reproduce",
        ),
        check(
            "VAL4909_09_constant_fit",
            math.isclose(finite_float(extrapolation, "constant_c_m"), 1.0212886943350583, rel_tol=1e-12)
            and math.isclose(finite_float(extrapolation, "constant_c_m_standard_error"), 0.024081276678541118, rel_tol=1e-12)
            and finite_float(extrapolation, "constant_chi_squared_per_dof") < 1.0,
            "constant mass-ratio pilot fit reproduces",
        ),
        check(
            "VAL4909_10_model_scope",
            finite_float(extrapolation, "two_sigma_model_union_minimum") < 0.73
            and finite_float(extrapolation, "two_sigma_model_union_maximum") > 1.18
            and extrapolation["literal_trajectory_drift_resolved"] == "False"
            and extrapolation["promotion_ready"] == "False",
            "broad model union and nonpromotion are retained",
        ),
        check(
            "VAL4909_11_finite_volume",
            abs(finite_float(volume, "difference_pull")) < 1.0
            and volume["finite_volume_resolved"] == "False",
            "single finite-volume comparison has no resolved shift",
        ),
        check(
            "VAL4909_12_replicate",
            1.9 < abs(finite_float(replicate, "difference_pull")) < 2.1
            and replicate["three_sigma_consistent"] == "True",
            "replicate two-sigma spread is exposed and three-sigma consistent",
        ),
        check(
            "VAL4909_13_correlation_rows",
            len(correlations) == sum(int(row["size"]) // 2 + 1 for row in mass_rows),
            "all periodic mean correlators are recorded",
        ),
        check(
            "VAL4909_14_gaussian_one_source",
            gaussian["passed"] == "True"
            and abs(finite_float(gaussian, "third_pull")) < 1.0
            and finite_float(gaussian, "third_relative_error") < 0.06,
            "one-source connected third response matches exact determinant",
        ),
        check(
            "VAL4909_15_gaussian_distinct",
            distinct["passed"] == "True"
            and abs(finite_float(distinct, "pull")) < 1.0
            and finite_float(distinct, "relative_error") < 0.03,
            "distinct-source triangle-plus-seagull response matches exact determinant",
        ),
        check(
            "VAL4909_16_seagulls",
            seagulls["passed"] == "True"
            and seagulls["first_volume_derivative"] == "0"
            and seagulls["mixed_second_volume_derivative"] == "-3"
            and seagulls["mixed_third_volume_derivative"] == "18",
            "densitized volume seagulls close symbolically",
        ),
        check(
            "VAL4909_17_Weyl_count",
            len(Weyl) == 4
            and [int(row["integer_momentum_scale"]) for row in Weyl] == [1, 2, 3, 4],
            "four Weyl-cubic momentum scales exist",
        ),
        check(
            "VAL4909_18_Weyl_template",
            math.isclose(finite_float(Weyl[0], "symmetrized_Weyl_cubic_template"), 0.11385470182761107, rel_tol=1e-13)
            and max(finite_float(row, "scale_six_residual") for row in Weyl) < 1e-9
            and [finite_float(row, "ratio_to_scale_one") for row in Weyl] == [1.0, 64.0, 729.0000000000008, 4096.0],
            "nonzero TT template has exact sixth-power scaling",
        ),
        check(
            "VAL4909_19_stress_contract",
            stress_status["metric_source_family"] == "NONZERO_TT_WEYL_CUBIC_TRIPLET_CONSTRUCTED"
            and stress_status["action_derivatives"] == "EXACT_DENSITIZED_VOLUME_SEAGULLS_DERIVED"
            and stress_status["connected_third_response"] == "EXACT_IDENTITY_GAUSSIAN_VALIDATED"
            and stress_status["Weyl_cubic_projection"] == "NOT_NUMERICALLY_EXECUTED",
            "TTT progress and remaining interacting projection are explicit",
        ),
        check(
            "VAL4909_20_c6_diagnostic",
            finite_float(extrapolation, "single_free_pole_c6_diagnostic") > 1e-7
            and extrapolation["single_free_pole_c6_is_result"] == "False",
            "free-pole c6 remains an explicit nonresult",
        ),
        check(
            "VAL4909_21_decision",
            decision["profile"] == "checkpoint"
            and decision["mass_gap_promoted"] == "False"
            and decision["c6_promoted"] == "False"
            and decision["Gamma_MTS_res"] == "0"
            and decision["Weyl_template_pass"] == "True",
            "mass and c6 remain unpromoted with active residual zero",
        ),
        check(
            "VAL4909_22_claim",
            len(claims) == 1 and claims[0]["status"] == claim_status,
            "L-751 is unique and scoped",
        ),
        check(
            "VAL4909_23_variables",
            len(selected) == len(symbols)
            and all(counts[symbol] == 1 for symbol in symbols),
            "fifteen checkpoint variables are unique",
        ),
        check(
            "VAL4909_24_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4909_25_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_MOTION_SCALAR_LATTICE_TTT_PROVENANCE_4909" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4909_26_registers",
            "1.202 Motion-scalar lattice gap" in equations
            and "153. A stable coarse-lattice mass" in redteam
            and "PPC4161 checkpoint 4909" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4909_27_resume",
            "Last checkpoint: `4909-" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume handoff points to 4909 and 4910",
        ),
        check(
            "VAL4909_28_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no placeholder markers",
        ),
        check(
            "VAL4909_29_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no nonfinite numeric cells",
        ),
        check(
            "VAL4909_30_nonclaim",
            all(str(row.get("valid_for_claim")) == "False" for row in all_rows),
            "all generated rows remain private nonclaim",
        ),
        check(
            "VAL4909_31_csv",
            len(output_paths) == 15
            and all(path.exists() and read_csv(path) for path in output_paths),
            "fifteen evidence CSVs parse",
        ),
        check(
            "VAL4909_32_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4909_33_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4909_34_next",
            NEXT_TARGET in checkpoint
            and decision["next_target"] == NEXT_TARGET
            and not (POST / NEXT_TARGET).exists(),
            "4910 is selected but not pre-created",
        ),
    ]
    rows.append(
        check(
            "VAL4909_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4909_SOURCE_REGISTER.csv", sources)
    validation = validation_rows(sources)
    write_csv(OUTPUT / "P8_Y5_BRR545_4909_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4909_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4909_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
