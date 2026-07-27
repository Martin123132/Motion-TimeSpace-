from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4911_full_offshell_a6_template_projector as research


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
            "SRC4911_06_checkpoint",
            POST
            / "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md",
            research.MARKER,
        ),
        (
            "SRC4911_07_formal_note",
            FORMAL / "927-PPC4161-full-offshell-a6-template-projector.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4911_08_provenance",
            POST
            / "source-intake"
            / "microscopic_vertex"
            / "4911"
            / "PROVENANCE.md",
            "MTS_FULL_OFFSHELL_A6_PROJECTOR_PROVENANCE_4911",
        ),
        (
            "SRC4911_09_research_script",
            SCRIPTS / "Y5_R2FR_4911_full_offshell_a6_template_projector.py",
            "def dependency_relations",
        ),
        (
            "SRC4911_10_validation_script",
            SCRIPTS
            / "Y5_R2FR_4911_full_offshell_a6_template_projector_validation.py",
            "VAL4911_OVERALL",
        ),
        (
            "SRC4911_11_claim_register",
            FORMAL / "02-claims-register.csv",
            "L-753",
        ),
        (
            "SRC4911_12_variable_register",
            FORMAL / "04-variable-audit.csv",
            "RicciFlatMap4911_MTS",
        ),
        (
            "SRC4911_13_equation_register",
            FORMAL / "05-equation-register.md",
            "1.204 Full off-shell `a6` template quotient",
        ),
        (
            "SRC4911_14_redteam",
            FORMAL / "06-consistency-red-team.md",
            "155. Source-vector recovery is not determinant recovery",
        ),
        (
            "SRC4911_15_spine",
            FORMAL / "07-unification-spine.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4911_16_resume",
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

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4910_VALIDATION.csv")
    basis = read_csv(OUTPUT / "P8_Y5_R2FR_4911_INTEGRATED_A6_BASIS.csv")
    ensemble = read_csv(OUTPUT / "P8_Y5_R2FR_4911_SOURCE_ENSEMBLE.csv")
    template_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4911_TEMPLATE_MATRIX.csv")
    diagnostics = read_csv(
        OUTPUT / "P8_Y5_R2FR_4911_GEOMETRY_DIAGNOSTICS.csv"
    )
    crosschecks = read_csv(OUTPUT / "P8_Y5_R2FR_4911_GRID_CROSSCHECK.csv")
    spectrum = read_csv(OUTPUT / "P8_Y5_R2FR_4911_SINGULAR_SPECTRUM.csv")
    pivots = read_csv(OUTPUT / "P8_Y5_R2FR_4911_PIVOT_BASIS.csv")
    dependencies = read_csv(
        OUTPUT / "P8_Y5_R2FR_4911_DEPENDENCY_RELATIONS.csv"
    )
    nullspace = read_csv(OUTPUT / "P8_Y5_R2FR_4911_NULLSPACE.csv")
    recovery = read_csv(
        OUTPUT / "P8_Y5_R2FR_4911_FREE_COEFFICIENT_RECOVERY.csv"
    )
    leave_one = read_csv(OUTPUT / "P8_Y5_R2FR_4911_LEAVE_ONE_GEOMETRY.csv")
    ricci_flat = read_csv(OUTPUT / "P8_Y5_R2FR_4911_RICCI_FLAT_MAP.csv")
    projector = read_csv(OUTPUT / "P8_Y5_R2FR_4911_PROJECTOR_GATE.csv")
    interacting = read_csv(
        OUTPUT / "P8_Y5_R2FR_4911_INTERACTING_RUN_GATE.csv"
    )
    local = read_csv(OUTPUT / "P8_Y5_R2FR_4911_LOCAL_LIMIT_GATE.csv")
    decision = read_csv(OUTPUT / "P8_Y5_R2FR_4911_DECISION.csv")[0]

    geometry_ids = sorted(row["geometry_id"] for row in ensemble)
    operator_names = list(research.OPERATOR_NAMES)
    matrix = np.zeros((len(geometry_ids), len(operator_names)), dtype=float)
    geometry_lookup = {name: index for index, name in enumerate(geometry_ids)}
    operator_lookup = {name: index for index, name in enumerate(operator_names)}
    for row in template_rows:
        matrix[
            geometry_lookup[row["geometry_id"]],
            operator_lookup[row["operator"]],
        ] = finite_float(row, "mixed_third_template")
    column_norms = np.linalg.norm(matrix, axis=0)
    normalized = matrix / column_norms
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    independent_rank = int(np.sum(singular_values > singular_values[0] * 1e-10))

    projector_status = {row["gate"]: row["status"] for row in projector}
    interacting_status = {
        row["gate"]: row["status"] for row in interacting
    }
    local_status = {row["arena"]: row["status"] for row in local}

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-753"
    ]
    claim_status = (
        "sourced_integrated_a6_basis_exact_nilpotent_geometric_templates_"
        "rank_eight_quotient_Ricci_flat_map_known_scalar_source_vector_"
        "recovered_free_lattice_multigeometry_required_interacting_"
        "withheld_active_residual_zero_private_nonclaim"
    )
    symbols = (
        "IntegratedA6Basis4911_MTS",
        "NilpotentMetricJet4911_MTS",
        "GeometricTemplate4911_MTS",
        "TemplateRank4911_MTS",
        "QuotientBasis4911_MTS",
        "DependencyIdentity4911_MTS",
        "RicciFlatMap4911_MTS",
        "ConventionMap4911_MTS",
        "FreeSourceRecovery4911_MTS",
        "GridCrosscheck4911_MTS",
        "LeaveOneGeometry4911_MTS",
        "FreeLatticeGate4911_MTS",
        "InteractingRunGate4911_MTS",
        "ResidualStatus4911_MTS",
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
        / "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md"
    )
    formal_path = FORMAL / "927-PPC4161-full-offshell-a6-template-projector.md"
    provenance_path = (
        POST / "source-intake" / "microscopic_vertex" / "4911" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    output_paths = sorted(OUTPUT.glob("P8_Y5_R2FR_4911_*.csv"))
    all_rows: list[dict[str, Any]] = sources.copy()
    for path in output_paths:
        all_rows.extend(read_csv(path))
    scripts = [
        SCRIPTS / "Y5_R2FR_4911_full_offshell_a6_template_projector.py",
        SCRIPTS
        / "Y5_R2FR_4911_full_offshell_a6_template_projector_validation.py",
    ]

    source_numerators = np.array(
        [finite_float(row, "source_integrated_numerator") for row in basis]
    )
    engine_numerators = np.array(
        [finite_float(row, "engine_integrated_numerator") for row in basis]
    )
    source_expected = research.A6_SOURCE_INTEGRATED_NUMERATORS
    engine_expected = research.A6_ENGINE_INTEGRATED_NUMERATORS
    retained_pivots = [
        row["operator"] for row in pivots if row["retained"] == "True"
    ]

    rows = [
        check(
            "VAL4911_00_prior",
            bool(prior)
            and prior[-1]["check_id"] == "VAL4910_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4910 validation inherited",
        ),
        check(
            "VAL4911_01_sources",
            research.source_contract()["passed"]
            and len(sources) == 17
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all primary local and generated source markers exist",
        ),
        check(
            "VAL4911_02_basis_count",
            len(basis) == 12
            and [int(row["operator_index"]) for row in basis] == list(range(12))
            and [row["operator"] for row in basis] == operator_names,
            "all twelve integrated a6 columns are ordered and named",
        ),
        check(
            "VAL4911_03_basis_coefficients",
            np.max(np.abs(source_numerators - source_expected)) < 1e-14
            and np.max(np.abs(engine_numerators - engine_expected)) < 1e-14
            and np.max(
                np.abs(
                    np.array(
                        [finite_float(row, "engine_a6_coefficient") for row in basis]
                    )
                    - engine_expected / math.factorial(7)
                )
            )
            < 1e-16,
            "source integration and H-to-g cubic sign conversion reproduce",
        ),
        check(
            "VAL4911_04_ensemble",
            len(ensemble) == 12
            and geometry_ids == [f"G{index:02d}" for index in range(12)]
            and all(
                finite_float(row, "momentum_closure_residual") < 1e-14
                for row in ensemble
            ),
            "twelve momentum-conserving source geometries exist",
        ),
        check(
            "VAL4911_05_template_matrix",
            len(template_rows) == 144
            and set(row["geometry_id"] for row in template_rows)
            == set(geometry_ids)
            and set(row["operator"] for row in template_rows)
            == set(operator_names)
            and np.all(np.isfinite(matrix))
            and np.all(column_norms > 1e-12),
            "complete finite nonzero twelve-by-twelve template matrix exists",
        ),
        check(
            "VAL4911_06_geometry_identities",
            len(diagnostics) == 12
            and max(
                finite_float(row, key)
                for row in diagnostics
                for key in (
                    "metric_inverse_residual",
                    "riemann_first_pair_residual",
                    "riemann_last_pair_residual",
                    "riemann_pair_exchange_residual",
                    "ricci_symmetry_residual",
                    "flat_curvature_residual",
                    "imaginary_residual",
                )
            )
            < 2e-12,
            "metric curvature symmetry and reality residuals close",
        ),
        check(
            "VAL4911_07_grid_crosscheck",
            len(crosschecks) == 2
            and {int(row["baseline_size"]) for row in crosschecks} == {6}
            and {int(row["crosscheck_size"]) for row in crosschecks} == {8}
            and max(
                finite_float(row, "relative_template_residual")
                for row in crosschecks
            )
            < 3e-15,
            "independent 6^4 and 8^4 geometric templates agree",
        ),
        check(
            "VAL4911_08_independent_rank",
            independent_rank == 8
            and singular_values[7] > 0.05
            and singular_values[8] < 2e-15,
            "independent SVD reproduces the rank-eight quotient and four-null gap",
        ),
        check(
            "VAL4911_09_spectrum",
            len(spectrum) == 12
            and sum(row["retained"] == "True" for row in spectrum) == 8
            and all(int(row["rank"]) == 8 for row in spectrum)
            and 51 < finite_float(spectrum[0], "condition_number_retained") < 52,
            "recorded singular spectrum and retained condition reproduce",
        ),
        check(
            "VAL4911_10_pivot_basis",
            retained_pivots
            == [
                "D1_grad_R_squared",
                "D4_grad_Riemann_squared",
                "C7_I1_Riemann_cubed",
                "C4_Ricci_cubed",
                "C8_I2_Riemann_cubed",
                "C1_R_cubed",
                "C3_R_Riemann_squared",
                "C5_Ricci_Ricci_Riemann",
            ],
            "pivoted QR quotient basis reproduces",
        ),
        check(
            "VAL4911_11_dependencies",
            len(dependencies) == 32
            and {
                row["dependent_operator"] for row in dependencies
            }
            == {
                "C6_Ricci_Riemann_Riemann",
                "D3_crossed_grad_Ricci",
                "D2_grad_Ricci_squared",
                "C2_R_Ricci_squared",
            }
            and max(
                finite_float(row, "relative_relation_residual")
                for row in dependencies
            )
            < 9e-16
            and max(
                finite_float(row, "rational_approximation_residual")
                for row in dependencies
            )
            < 5e-15,
            "four dependencies reduce to stable rational identities",
        ),
        check(
            "VAL4911_12_nullspace",
            len(nullspace) == 48
            and {int(row["null_vector"]) for row in nullspace} == set(range(4))
            and max(
                abs(finite_float(row, "Ricci_flat_map_residual"))
                for row in nullspace
            )
            < 1e-14,
            "Ricci-flat functional annihilates all four null directions",
        ),
        check(
            "VAL4911_13_recovery_rows",
            len(recovery) == 12
            and [row["operator"] for row in recovery] == operator_names
            and all(
                finite_float(row, "quotient_response_recovery_residual") < 6e-16
                for row in recovery
            ),
            "source and recovered quotient representatives are recorded",
        ),
        check(
            "VAL4911_14_ricci_flat_map",
            len(ricci_flat) == 4
            and any("I2=I1/2" in row["equation"] for row in ricci_flat)
            and any("-1/15120" in row["equation"] for row in ricci_flat),
            "four-dimensional Ricci-flat and proper-time map is explicit",
        ),
        check(
            "VAL4911_15_zeta",
            math.isclose(
                finite_float(decision, "recovered_free_scalar_zeta"),
                1.0 / (30240.0 * (4.0 * math.pi) ** 2),
                rel_tol=2e-13,
                abs_tol=3e-20,
            )
            and abs(
                finite_float(decision, "recovered_free_scalar_zeta")
                - finite_float(decision, "expected_free_scalar_zeta")
            )
            < 3e-20,
            "known massive-scalar Weyl-cubic coefficient is recovered",
        ),
        check(
            "VAL4911_16_leave_one",
            len(leave_one) == 12
            and all(int(row["rank"]) == 8 for row in leave_one)
            and max(
                finite_float(row, "absolute_zeta_residual")
                for row in leave_one
            )
            < 4e-19
            and max(
                finite_float(row, "condition_number_retained")
                for row in leave_one
            )
            < 168,
            "every leave-one-geometry inverse preserves rank and zeta",
        ),
        check(
            "VAL4911_17_projector_gate",
            len(projector_status) == 5
            and set(projector_status.values()) == {"PASS"},
            "all geometric projector gates pass",
        ),
        check(
            "VAL4911_18_interacting_gate",
            interacting_status["geometric_projector"] == "PASS"
            and interacting_status["exact_free_lattice_multigeometry_response"]
            == "REQUIRED"
            and interacting_status["cutoff_and_volume_sequence"] == "REQUIRED"
            and interacting_status["interacting_TTT_long_run"]
            == "DO_NOT_RUN_YET"
            and interacting_status["active_residual"] == "ZERO_PRESERVED",
            "interacting execution is withheld at the independent free-lattice gate",
        ),
        check(
            "VAL4911_19_local_limits",
            local_status["GR_Newton_PPN"] == "UNCHANGED"
            and local_status["Maxwell_Poynting"] == "UNCHANGED"
            and local_status["strong_gravity_C3"] == "CALIBRATION_ONLY"
            and local_status["Gamma_MTS_res"] == "ZERO",
            "local GR Newton PPN Maxwell and active residual remain unchanged",
        ),
        check(
            "VAL4911_20_decision",
            decision["template_rank"] == "8"
            and decision["interacting_run_launched"] == "False"
            and decision["Gamma_MTS_res"] == "0"
            and decision["all_checks_pass"] == "True"
            and decision["next_target"] == NEXT_TARGET,
            "decision preserves nonclaim and selects independent lattice recovery",
        ),
        check(
            "VAL4911_21_claim",
            len(claims) == 1 and claims[0]["status"] == claim_status,
            "L-753 is unique and accurately scoped",
        ),
        check(
            "VAL4911_22_variables",
            len(selected_variables) == len(symbols)
            and all(variable_counts[symbol] == 1 for symbol in symbols),
            "fourteen checkpoint variables are unique",
        ),
        check(
            "VAL4911_23_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4911_24_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_FULL_OFFSHELL_A6_PROJECTOR_PROVENANCE_4911"
            in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4911_25_registers",
            "1.204 Full off-shell `a6` template quotient" in equations
            and "155. Source-vector recovery is not determinant recovery"
            in redteam
            and "PPC4161 checkpoint 4911" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4911_26_resume",
            "Last checkpoint: `4911-" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume handoff points to 4911 and 4912",
        ),
        check(
            "VAL4911_27_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no placeholder markers",
        ),
        check(
            "VAL4911_28_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no nonfinite numeric cells",
        ),
        check(
            "VAL4911_29_nonclaim",
            all(str(row.get("valid_for_claim")) == "False" for row in all_rows),
            "all generated rows remain private nonclaim",
        ),
        check(
            "VAL4911_30_csv",
            len(output_paths) == 17
            and all(path.exists() and read_csv(path) for path in output_paths),
            "seventeen evidence CSVs parse",
        ),
        check(
            "VAL4911_31_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4911_32_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4911_33_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4912 is selected but not pre-created",
        ),
    ]
    rows.append(
        check(
            "VAL4911_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4911_SOURCE_REGISTER.csv", sources)
    validation = validation_rows(sources)
    write_csv(OUTPUT / "P8_Y5_BRR545_4911_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4911_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4911_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
