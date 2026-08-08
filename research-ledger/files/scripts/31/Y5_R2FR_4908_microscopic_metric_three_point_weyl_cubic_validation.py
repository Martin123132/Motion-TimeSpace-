from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4908_microscopic_metric_three_point_weyl_cubic as research


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
            "SRC4908_13_checkpoint",
            POST
            / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
            research.MARKER,
        ),
        (
            "SRC4908_14_formal_note",
            FORMAL / "924-PPC4161-microscopic-metric-three-point-Weyl-cubic.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4908_15_provenance",
            POST
            / "source-intake"
            / "microscopic_vertex"
            / "4908"
            / "PROVENANCE.md",
            "MTS_MICROSCOPIC_VERTEX_PRIMARY_SOURCE_PROVENANCE_4908",
        ),
        (
            "SRC4908_16_research_script",
            SCRIPTS
            / "Y5_R2FR_4908_microscopic_metric_three_point_weyl_cubic.py",
            "def determinant_three_point",
        ),
        (
            "SRC4908_17_validation_script",
            SCRIPTS
            / "Y5_R2FR_4908_microscopic_metric_three_point_weyl_cubic_validation.py",
            "VAL4908_OVERALL",
        ),
        (
            "SRC4908_18_claim_register",
            FORMAL / "02-claims-register.csv",
            "L-750",
        ),
        (
            "SRC4908_19_equation_register",
            FORMAL / "05-equation-register.md",
            "1.201 Microscopic metric three-point",
        ),
        (
            "SRC4908_20_redteam",
            FORMAL / "06-consistency-red-team.md",
            "152. A formal Hessian zero",
        ),
        (
            "SRC4908_21_spine",
            FORMAL / "07-unification-spine.md",
            research.FORMAL_MARKER,
        ),
        (
            "SRC4908_22_resume",
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
    hessian = sections["hessian"]
    vertex = sections["vertex"]
    determinant = sections["determinant"]
    loop = sections["loop"]
    scaling = sections["scaling"]
    owners = sections["owners"]
    local = sections["local"]

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4907_VALIDATION.csv")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-750"
    ]
    claim_status = (
        "metric_vertex_and_Ward_derived_source_regularized_one_loop_"
        "Weyl_cubic_zero_limit_but_Gaussian_vacuum_uncontrolled_"
        "nonperturbative_c6_scaling_derived_total_coefficient_unowned_"
        "active_residual_zero_private_nonclaim"
    )
    symbols = (
        "CoreCuspPotential4908_MTS",
        "SourceBackground4908_MTS",
        "SourceHessian4908_MTS",
        "MetricVertex4908_MTS",
        "MetricWard4908_MTS",
        "DeterminantThreePoint4908_MTS",
        "WeylCubicHessian4908_MTS",
        "GaussianControl4908_MTS",
        "MotionScale4908_MTS",
        "NonperturbativeC64908_MTS",
        "SKDiagonal4908_MTS",
        "LocalCubicGate4908_MTS",
        "ResidualStatus4908_MTS",
    )
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    selected = [row for row in variables if row.get("symbol") in symbols]
    counts = {
        symbol: sum(row.get("symbol") == symbol for row in variables)
        for symbol in symbols
    }
    variable_sources_exist = all(
        (ROOT / relative_path).exists()
        for row in selected
        for relative_path in row["source_files"].split(";")
    )

    checkpoint_path = (
        POST
        / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md"
    )
    formal_path = FORMAL / "924-PPC4161-microscopic-metric-three-point-Weyl-cubic.md"
    provenance_path = (
        POST
        / "source-intake"
        / "microscopic_vertex"
        / "4908"
        / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(
        encoding="utf-8"
    )
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(
        encoding="utf-8"
    )
    spine = (FORMAL / "07-unification-spine.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(
        encoding="utf-8"
    )

    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / "P8_Y5_R2FR_4908_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4908_{name}.csv"
            for name in groups
        ],
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4908_microscopic_metric_three_point_weyl_cubic.py",
        SCRIPTS
        / "Y5_R2FR_4908_microscopic_metric_three_point_weyl_cubic_validation.py",
    ]
    sweep = loop["rows"]
    j_one = next(row for row in sweep if row["j_abs"] == 1.0)
    j_half = next(row for row in sweep if row["j_abs"] == 0.5)
    gates = {row["gate"]: row["status"] for row in calculation["rows"]}

    rows = [
        check(
            "VAL4908_00_prior",
            bool(prior)
            and prior[-1]["check_id"] == "VAL4907_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4907 validation inherited",
        ),
        check(
            "VAL4908_01_sources",
            calculation["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all local and generated source markers exist",
        ),
        check(
            "VAL4908_02_hessian",
            hessian["passed"]
            and hessian["stationarity_residual"] == "0"
            and hessian["mass_squared"] == "lambda**3/(3*J**2)"
            and not hessian["vacuum_hessian_finite"],
            "source-selected cusp Hessian derives exactly",
        ),
        check(
            "VAL4908_03_cubic_quartic",
            hessian["cubic"] == "-2*lambda**6/(9*J**5)"
            and hessian["quartic"] == "10*lambda**9/(27*J**8)",
            "source-selected scalar interactions derive exactly",
        ),
        check(
            "VAL4908_04_metric_vertex",
            vertex["passed"] and vertex["Ward_identity_exact"],
            "scalar metric vertex obeys exact Ward identity",
        ),
        check(
            "VAL4908_05_Ward_components",
            vertex["Ward_residual"] == ["0", "0", "0", "0"],
            "all four Ward residual components vanish",
        ),
        check(
            "VAL4908_06_determinant",
            determinant["passed"]
            and determinant["commuting_third_variation"]
            == determinant["expected"]
            and "D123" in determinant["exact_operator_formula"],
            "complete determinant third variation closes",
        ),
        check(
            "VAL4908_07_scalar_weight",
            loop["passed"]
            and math.isclose(
                loop["scalar_weight_numeric"],
                1.0 / (30240.0 * (4.0 * math.pi) ** 2),
                rel_tol=1e-15,
            ),
            "massive real-scalar Weyl-cubic weight reproduces",
        ),
        check(
            "VAL4908_08_formal_limits",
            loop["formal_one_loop_vacuum_coefficient_zero"]
            and loop["vacuum_limit"] == "0"
            and loop["cutoff_removed_vacuum_limit"] == "0",
            "both formal source-to-zero orders give zero",
        ),
        check(
            "VAL4908_09_control_anchor",
            j_one["Gaussian_control_below_one"]
            and math.isclose(
                j_one["abs_g3_over_m_J"],
                2.0 * math.sqrt(3.0) / 9.0,
                rel_tol=1e-15,
            )
            and math.isclose(j_one["abs_g4"], 10.0 / 27.0, rel_tol=1e-15),
            "finite-source perturbative anchor reproduces",
        ),
        check(
            "VAL4908_10_control_failure",
            not loop["Gaussian_control_near_vacuum"]
            and not j_half["Gaussian_control_below_one"]
            and j_half["abs_g3_over_m_J"] > 6.0
            and j_half["abs_g4"] > 94.0
            and all(
                not row["Gaussian_control_below_one"]
                for row in sweep
                if row["j_abs"] <= 0.5
            ),
            "Gaussian control fails before the vacuum limit",
        ),
        check(
            "VAL4908_11_scaling",
            scaling["passed"]
            and str(scaling["mu_power"]) == "3/8"
            and str(scaling["zeta_lambda_power"]) == "-3/4"
            and scaling["unknown_dimensionless_constants"] == ["c_m", "c_6"],
            "nonperturbative problem reduces to dimensionless constants",
        ),
        check(
            "VAL4908_12_SK_owner",
            owners["passed"]
            and owners["SK_diagonal_action_value"] == 0
            and owners["r_a_physical_species_count"] == 1,
            "diagonal action normalization holds and response variables are not double-counted",
        ),
        check(
            "VAL4908_13_total_owner",
            not owners["real_complex_primitive_count_fixed"]
            and not owners["closed_completion_fixed"]
            and not owners["total_parity_even_numeric_coefficient_owned"]
            and owners["parity_odd_scalar_threshold"] == 0,
            "parity-even total remains unowned while scalar parity-odd threshold is zero",
        ),
        check(
            "VAL4908_14_flat_order",
            local["passed"]
            and local["C3_first_variation_at_flat"] == "0"
            and local["C3_second_variation_at_flat"] == "0"
            and local["C3_third_variation_at_flat"] == "6*C1**3",
            "Weyl-cubic operator begins at cubic metric order",
        ),
        check(
            "VAL4908_15_local_GR",
            not local["propagator_modified"]
            and not local["Newton_linear_modified"]
            and local["relative_scaling"] == "epsilon_3~|zeta| q^4/M_R^2",
            "flat graviton pole and linear Newton exchange remain unchanged",
        ),
        check(
            "VAL4908_16_Maxwell",
            local["Maxwell_direct_mixed_MTS_threshold"] == 0,
            "fixed-metric MTS slice creates no direct mixed Maxwell threshold",
        ),
        check(
            "VAL4908_17_gate_scope",
            gates["finite_stationary_Gaussian_Hessian"] == "FAIL"
            and gates["formal_one_loop_vacuum_C3"] == "ZERO_LIMIT_ONLY"
            and gates["Gaussian_control_at_vacuum"] == "FAIL"
            and gates["nonperturbative_scaling"] == "PASS"
            and gates["total_parity_even_owner"] == "FAIL",
            "failure and surviving derivation scopes are explicit",
        ),
        check(
            "VAL4908_18_decision",
            calculation["all_checks_pass"]
            and calculation["formal_Hessian_sector_C3_vacuum_limit"] == 0
            and not calculation["all_order_interacting_scalar_C3_proved_zero"]
            and calculation["total_parent_C3_numeric"] == "not_promoted"
            and calculation["Gamma_MTS_res"] == 0,
            "active residual remains zero without claiming physical total zero",
        ),
        check(
            "VAL4908_19_claim",
            len(claims) == 1 and claims[0]["status"] == claim_status,
            "L-750 is unique and scoped",
        ),
        check(
            "VAL4908_20_variables",
            len(selected) == len(symbols)
            and all(counts[symbol] == 1 for symbol in symbols),
            "thirteen checkpoint variables are unique",
        ),
        check(
            "VAL4908_21_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4908_22_documents",
            research.MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_MICROSCOPIC_VERTEX_PRIMARY_SOURCE_PROVENANCE_4908"
            in provenance,
            "checkpoint, formal note and provenance markers exist",
        ),
        check(
            "VAL4908_23_registers",
            "1.201 Microscopic metric three-point" in equations
            and "152. A formal Hessian zero" in redteam
            and "PPC4161 checkpoint 4908" in spine,
            "formal equation, red-team and spine registers updated",
        ),
        check(
            "VAL4908_24_resume",
            research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume
            and "Last checkpoint: `4908-" in resume,
            "resume handoff points to 4908 and 4909",
        ),
        check(
            "VAL4908_25_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder markers in generated evidence",
        ),
        check(
            "VAL4908_26_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence has no nonfinite numeric cells",
        ),
        check(
            "VAL4908_27_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated rows remain private nonclaim",
        ),
        check(
            "VAL4908_28_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4908_29_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4908_30_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4908_31_next",
            NEXT_TARGET in checkpoint
            and calculation["next_target"] == NEXT_TARGET
            and not (POST / NEXT_TARGET).exists(),
            "4909 is selected but not pre-created",
        ),
        check(
            "VAL4908_32_internal",
            calculation["all_checks_pass"],
            "all calculation-level checks pass",
        ),
    ]
    rows.append(
        check(
            "VAL4908_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    groups = research.output_groups(calculation)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4908_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4908_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4908_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4908_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4908_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
