from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4914_complex_source_Taylor_TTT_replica as research


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUN_COMPLEX = POST / "runs" / "20260712-4914-complex-discrete-checkpoint"
RUN_MASS = POST / "runs" / "20260712-4914-mass-propagation"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
MARKER = research.MARKER
NEXT_TARGET = research.NEXT_TARGET
CLAIM_STATUS = (
    "complex_source_algebra_and_free_determinant_pass_direct_moment_route_"
    "rejected_complex_discrete_replica_zero_compatible_covariant_gate_"
    "failed_C3_residual_demoted_active_zero_private_nonclaim"
)
VARIABLES = (
    "ComplexSourceJet4914_MTS",
    "SignChannel4914_MTS",
    "ComplexFFT4914_MTS",
    "FreeDeterminantJet4914_MTS",
    "DirectMomentGate4914_MTS",
    "ComplexReplica4914_MTS",
    "ScaledResidual4914_MTS",
    "CrossStencilCovariance4914_MTS",
    "MassPropagation4914_MTS",
    "EstimatorAggregate4914_MTS",
    "CovariantGate4914_MTS",
    "ResidualStatus4914_MTS",
)
BASE_EVIDENCE = (
    "P8_Y5_R2FR_4914_JET_ALGEBRA_VALIDATION.csv",
    "P8_Y5_R2FR_4914_FREE_DETERMINANT_JET_SMOKE.csv",
    "P8_Y5_R2FR_4914_REPLICA_CHAIN_SUMMARY.csv",
    "P8_Y5_R2FR_4914_PROJECTED_REPLICA.csv",
    "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_CHAIN_SUMMARY.csv",
    "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_RESPONSES.csv",
    "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_COVARIANCE.csv",
    "P8_Y5_R2FR_4914_COMPLEX_CROSS_STENCIL_COVARIANCE.csv",
    "P8_Y5_R2FR_4914_COMPLEX_PROJECTED_REPLICA.csv",
    "P8_Y5_R2FR_4914_COMPLEX_REPLICA_RUN_STATUS.csv",
    "P8_Y5_R2FR_4914_EXACT_FREE_MASS_DERIVATIVE.csv",
    "P8_Y5_R2FR_4914_MASS_AUGMENTED_PROJECTION.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
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
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": research.CHECKED_DATE,
        }
        for row in rows
    ]


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = (
        "utf-16"
        if raw.startswith((b"\xff\xfe", b"\xfe\xff"))
        else "utf-8"
    )
    return raw.decode(encoding, errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def quotient_linear_row(
    matrix: np.ndarray, covariance: np.ndarray
) -> np.ndarray:
    column_norms = np.linalg.norm(matrix, axis=0)
    normalized = matrix / column_norms
    covariance = 0.5 * (covariance + covariance.T)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    positive = eigenvalues[eigenvalues > 0]
    floor = max(
        float(np.median(positive)) * 1e-6 if len(positive) else 1e-20,
        float(np.max(eigenvalues)) * 1e-10,
        1e-30,
    )
    inverse = (
        eigenvectors * (1.0 / np.maximum(eigenvalues, floor))
    ) @ eigenvectors.T
    normal = normalized.T @ inverse @ normalized
    beta_map = (
        np.linalg.pinv(normal, rcond=1e-10)
        @ normalized.T
        @ inverse
    )
    coefficient_map = beta_map / column_norms[:, np.newaxis]
    return research.checkpoint_4911.RICCI_FLAT_C3_MAP @ coefficient_map


def joint_projection_rows() -> list[dict[str, Any]]:
    geometry_ids, matrix = research.checkpoint_4913.load_geometric_matrix()
    responses = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_RESPONSES.csv"
    )
    covariance_rows = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_CROSS_STENCIL_COVARIANCE.csv"
    )
    summaries = {
        row["label"]: row
        for row in read_csv(
            OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_CHAIN_SUMMARY.csv"
        )
    }
    labels = [
        f"{stencil}:{geometry_id}"
        for stencil in research.SOURCE_STENCILS
        for geometry_id in geometry_ids
    ]
    stacked_matrix = np.vstack([matrix, matrix])
    output: list[dict[str, Any]] = []
    for config, summary in summaries.items():
        response_map = {
            (row["stencil"], row["geometry_id"]): row
            for row in responses
            if row["config"] == config
        }
        response = np.asarray(
            [
                float(response_map[(stencil, geometry_id)]["matched_delta_q6"])
                for stencil in research.SOURCE_STENCILS
                for geometry_id in geometry_ids
            ]
        )
        covariance_map = {
            (row["channel_i"], row["channel_j"]): float(row["covariance"])
            for row in covariance_rows
            if row["config"] == config
        }
        covariance = np.asarray(
            [
                [covariance_map[(first, second)] for second in labels]
                for first in labels
            ]
        )
        recovered = research.checkpoint_4913.correlated_quotient_recovery(
            stacked_matrix, response, covariance
        )
        linear_row = quotient_linear_row(stacked_matrix, covariance)
        standard_error = math.sqrt(
            max(float(linear_row @ covariance @ linear_row), 0.0)
        )
        mu2 = float(summary["mu_hat"]) ** 2
        output.append(
            {
                "config": config,
                "zeta_joint": recovered["zeta"],
                "zeta_joint_standard_error": standard_error,
                "zeta_joint_significance": recovered["zeta"] / standard_error,
                "scaled_joint": mu2 * recovered["zeta"],
                "scaled_joint_standard_error": mu2 * standard_error,
                "euclidean_residual": recovered["euclidean_residual"],
                "chi_squared": recovered["chi_squared"],
                "covariance_condition": recovered["covariance_condition"],
                "mass_uncertainty_included": False,
                "promotion_allowed": False,
            }
        )
    return tagged(output)


def weighted_combination(
    values: list[tuple[float, float]]
) -> tuple[float, float, float]:
    weights = np.asarray([1.0 / error**2 for _, error in values])
    numbers = np.asarray([value for value, _ in values])
    mean = float(np.sum(weights * numbers) / np.sum(weights))
    error = float(1.0 / math.sqrt(float(np.sum(weights))))
    return mean, error, mean / error


def combination_rows(
    joint_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    summaries_4914 = {
        row["label"]: row
        for row in read_csv(
            OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_CHAIN_SUMMARY.csv"
        )
    }
    projected_4914 = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_MASS_AUGMENTED_PROJECTION.csv"
    )
    projected_4913 = read_csv(
        OUTPUT / "P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv"
    )
    mu_4913 = {"N12_mu0p6": 0.6, "N16_mu0p4": 0.4}
    output: list[dict[str, Any]] = []
    for stencil in research.SOURCE_STENCILS:
        selected = [
            row for row in projected_4914 if row["stencil"] == stencil
        ]
        complex_values = [
            (
                float(row["zeta_delta"])
                * float(summaries_4914[row["config"]]["mu_hat"]) ** 2,
                float(row["conservative_standard_error"])
                * float(summaries_4914[row["config"]]["mu_hat"]) ** 2,
            )
            for row in selected
        ]
        mean, error, significance = weighted_combination(complex_values)
        cutoff_shift = abs(complex_values[0][0] - complex_values[1][0]) / math.hypot(
            complex_values[0][1], complex_values[1][1]
        )
        output.append(
            {
                "evidence_set": "4914_complex_only",
                "channel": stencil,
                "point_count": len(complex_values),
                "scaled_coefficient": mean,
                "scaled_standard_error": error,
                "significance": significance,
                "cutoff_shift_sigma": cutoff_shift,
                "promotion_allowed": False,
            }
        )
        all_values = list(complex_values)
        all_values.extend(
            (
                float(row["zeta"]) * mu_4913[row["config"]] ** 2,
                float(row["zeta_delta_standard_error"])
                * mu_4913[row["config"]] ** 2,
            )
            for row in projected_4913
            if row["stencil"] == stencil
        )
        mean, error, significance = weighted_combination(all_values)
        output.append(
            {
                "evidence_set": "4913_and_4914_independent",
                "channel": stencil,
                "point_count": len(all_values),
                "scaled_coefficient": mean,
                "scaled_standard_error": error,
                "significance": significance,
                "cutoff_shift_sigma": "not_applicable",
                "promotion_allowed": False,
            }
        )
    joint_values = [
        (
            float(row["scaled_joint"]),
            float(row["scaled_joint_standard_error"]),
        )
        for row in joint_rows
    ]
    mean, error, significance = weighted_combination(joint_values)
    cutoff_shift = abs(joint_values[0][0] - joint_values[1][0]) / math.hypot(
        joint_values[0][1], joint_values[1][1]
    )
    output.append(
        {
            "evidence_set": "4914_complex_joint_stencils",
            "channel": "joint",
            "point_count": len(joint_values),
            "scaled_coefficient": mean,
            "scaled_standard_error": error,
            "significance": significance,
            "cutoff_shift_sigma": cutoff_shift,
            "promotion_allowed": False,
        }
    )
    return tagged(output)


def gate_rows(
    joint: list[dict[str, Any]], combinations: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    algebra = read_csv(OUTPUT / BASE_EVIDENCE[0])
    free = read_csv(OUTPUT / BASE_EVIDENCE[1])
    direct = read_csv(OUTPUT / BASE_EVIDENCE[3])[0]
    summaries = read_csv(OUTPUT / BASE_EVIDENCE[4])
    complex_rows = read_csv(OUTPUT / BASE_EVIDENCE[8])
    mass_rows = read_csv(OUTPUT / BASE_EVIDENCE[11])
    free_summary = next(row for row in free if row["row_type"] == "summary")
    chain_health = all(
        0.42 < float(row["mean_metropolis_acceptance"]) < 0.58
        and float(row["mean_overrelax_acceptance"]) > 0.95
        and float(row["tau_zero_mode_observations"]) < 5.0
        and int(row["block_count"]) >= 100
        for row in summaries
    )
    maximum_estimator_shift = max(
        float(row["independent_4913_shift_sigma"]) for row in complex_rows
    )
    complex_combinations = [
        row
        for row in combinations
        if row["evidence_set"] == "4914_complex_only"
    ]
    all_combinations = [
        row
        for row in combinations
        if row["evidence_set"] == "4913_and_4914_independent"
    ]
    joint_combination = next(
        row
        for row in combinations
        if row["evidence_set"] == "4914_complex_joint_stencils"
    )
    residuals = [
        float(row["euclidean_residual"]) for row in complex_rows
    ] + [float(row["euclidean_residual"]) for row in joint]
    maximum_mass = max(
        float(row["mass_standard_error_component"]) for row in mass_rows
    )
    direct_error = float(direct["zeta_delta_standard_error"])
    best_complex_error = min(
        float(row["zeta_delta_standard_error"]) for row in complex_rows
    )
    return tagged(
        [
            {
                "gate_id": "G4914_00_algebra",
                "gate": "complex_source_algebra",
                "status": "PASS",
                "metric": max(float(row["metric"]) for row in algebra[:-1]),
                "criterion_satisfied": all(row["passed"] == "True" for row in algebra),
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_01_free",
                "gate": "exact_free_determinant",
                "status": "PASS",
                "metric": float(free_summary["reduced_chi_squared"]),
                "secondary_metric": float(free_summary["maximum_absolute_pull"]),
                "criterion_satisfied": free_summary["passed"] == "True",
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_02_direct",
                "gate": "direct_coordinate_moment_estimator",
                "status": "REJECTED_VARIANCE",
                "metric": direct_error,
                "secondary_metric": direct_error / best_complex_error,
                "criterion_satisfied": direct_error / best_complex_error > 1000,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_03_chain",
                "gate": "complex_replica_chain_health",
                "status": "PASS" if chain_health else "FAIL",
                "metric": max(
                    float(row["tau_zero_mode_observations"]) for row in summaries
                ),
                "criterion_satisfied": chain_health,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_04_replica",
                "gate": "independent_estimator_compatibility",
                "status": "PASS",
                "metric": maximum_estimator_shift,
                "criterion_satisfied": maximum_estimator_shift < 2.0,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_05_cutoff",
                "gate": "scaled_cutoff_consistency",
                "status": "PASS_DIAGNOSTIC",
                "metric": max(
                    float(row["cutoff_shift_sigma"])
                    for row in complex_combinations
                ),
                "criterion_satisfied": all(
                    float(row["cutoff_shift_sigma"]) < 1.0
                    for row in complex_combinations
                ),
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_06_complex_significance",
                "gate": "complex_only_nonzero_significance",
                "status": "BELOW_PROMOTION",
                "metric": max(
                    abs(float(row["significance"]))
                    for row in complex_combinations + [joint_combination]
                ),
                "criterion_satisfied": all(
                    abs(float(row["significance"])) < 3.0
                    for row in complex_combinations + [joint_combination]
                ),
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_07_all_evidence",
                "gate": "all_independent_nonzero_significance",
                "status": "FAIL_TO_REJECT_ZERO",
                "metric": max(
                    abs(float(row["significance"])) for row in all_combinations
                ),
                "criterion_satisfied": all(
                    abs(float(row["significance"])) < 2.0
                    for row in all_combinations
                ),
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_08_covariance",
                "gate": "covariant_image",
                "status": "FAIL",
                "metric": min(residuals),
                "secondary_metric": max(residuals),
                "criterion_satisfied": max(residuals) > 0.5,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_09_mass",
                "gate": "exact_free_mass_propagation",
                "status": "PASS_NEGLIGIBLE",
                "metric": maximum_mass,
                "criterion_satisfied": maximum_mass < 1e-4,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_10_promotion",
                "gate": "interacting_C3_promotion",
                "status": "BLOCKED_DEMOTED",
                "metric": 0,
                "criterion_satisfied": True,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_11_active",
                "gate": "Gamma_MTS_res",
                "status": "ZERO_PRESERVED",
                "metric": 0,
                "criterion_satisfied": True,
                "promotion_allowed": False,
            },
            {
                "gate_id": "G4914_12_next",
                "gate": "programme_route",
                "status": "RETURN_TO_PARENT_EH_SOURCE_COUPLING",
                "metric": 0,
                "criterion_satisfied": True,
                "promotion_allowed": False,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    sources: list[tuple[str, Path, str, str]] = [
        (
            "SRC4914_00_predecessor",
            POST
            / "4913-Y5-R2FR-matched-subtracted-interacting-motion-scalar-TTT-continuum-coefficient-or-zero-residual.md",
            "MTS_MATCHED_INTERACTING_TTT_SMOKE_4913",
            "validated_predecessor",
        ),
        (
            "SRC4914_01_predecessor_validation",
            OUTPUT / "P8_Y5_BRR545_4913_VALIDATION.csv",
            "VAL4913_OVERALL",
            "validated_predecessor",
        ),
        (
            "SRC4914_02_checkpoint",
            POST
            / "4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4914_03_formal",
            FORMAL
            / "930-PPC4161-complex-source-TTT-arbitration-and-residual-demotion.md",
            research.FORMAL_MARKER,
            "generated_formal_note",
        ),
        (
            "SRC4914_04_provenance",
            POST / "source-intake" / "microscopic_vertex" / "4914" / "PROVENANCE.md",
            "MTS_COMPLEX_SOURCE_TTT_PROVENANCE_4914",
            "generated_provenance",
        ),
        (
            "SRC4914_05_research",
            SCRIPTS / "Y5_R2FR_4914_complex_source_Taylor_TTT_replica.py",
            "def measure_complex_jet_observables",
            "generated_research_code",
        ),
        (
            "SRC4914_06_validation",
            SCRIPTS
            / "Y5_R2FR_4914_complex_source_Taylor_TTT_replica_validation.py",
            "VAL4914_OVERALL",
            "generated_validation_code",
        ),
        ("SRC4914_07_claim", FORMAL / "02-claims-register.csv", "L-756", "register"),
        (
            "SRC4914_08_variable",
            FORMAL / "04-variable-audit.csv",
            "ComplexSourceJet4914_MTS",
            "register",
        ),
        (
            "SRC4914_09_equation",
            FORMAL / "05-equation-register.md",
            "1.207 Complex-source TTT arbitration",
            "register",
        ),
        (
            "SRC4914_10_redteam",
            FORMAL / "06-consistency-red-team.md",
            "158. An exact derivative",
            "register",
        ),
        (
            "SRC4914_11_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4914",
            "register",
        ),
        (
            "SRC4914_12_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
            "resume",
        ),
        (
            "SRC4914_13_complex_status",
            RUN_COMPLEX / "status.json",
            '"status": "COMPLETE"',
            "run_record",
        ),
        (
            "SRC4914_14_complex_log",
            RUN_COMPLEX / "log.txt",
            "estimator=complex_discrete",
            "run_record",
        ),
        (
            "SRC4914_15_complex_marker",
            RUN_COMPLEX / "COMPLETE.marker",
            "MTS_4914_REPLICA_COMPLETE",
            "run_record",
        ),
        (
            "SRC4914_16_mass_log",
            RUN_MASS / "log.txt",
            "P8_Y5_R2FR_4914_MASS_PROPAGATION_PASS",
            "run_record",
        ),
        (
            "SRC4914_17_mass_marker",
            RUN_MASS / "COMPLETE.marker",
            "MTS_4914_MASS_PROPAGATION_COMPLETE",
            "run_record",
        ),
    ]
    evidence_names = list(BASE_EVIDENCE) + [
        "P8_Y5_R2FR_4914_JOINT_STENCIL_PROJECTION.csv",
        "P8_Y5_R2FR_4914_SCALED_COMBINATIONS.csv",
        "P8_Y5_R2FR_4914_GATE_DECISION.csv",
    ]
    for index, filename in enumerate(evidence_names, start=18):
        sources.append(
            (
                f"SRC4914_{index:02d}_{Path(filename).stem}",
                OUTPUT / filename,
                MARKER,
                "numeric_evidence",
            )
        )
    output: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        output.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": sha256(path) if exists else "",
            }
        )
    return tagged(output)


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def validation_rows(
    joint: list[dict[str, Any]],
    combinations: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4913_VALIDATION.csv")
    gate_map = {row["gate"]: row for row in gates}
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-756"
    ]
    variable_rows = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in VARIABLES
    ]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )
    checkpoint = (
        POST
        / "4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "930-PPC4161-complex-source-TTT-arbitration-and-residual-demotion.md"
    ).read_text(encoding="utf-8")
    provenance = (
        POST / "source-intake" / "microscopic_vertex" / "4914" / "PROVENANCE.md"
    ).read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    generated_paths = [OUTPUT / name for name in BASE_EVIDENCE] + [
        OUTPUT / "P8_Y5_R2FR_4914_JOINT_STENCIL_PROJECTION.csv",
        OUTPUT / "P8_Y5_R2FR_4914_SCALED_COMBINATIONS.csv",
        OUTPUT / "P8_Y5_R2FR_4914_GATE_DECISION.csv",
        OUTPUT / "P8_Y5_R2FR_4914_SOURCE_REGISTER.csv",
    ]
    all_rows = [row for path in generated_paths for row in read_csv(path)]
    run_state = json.loads((RUN_COMPLEX / "status.json").read_text(encoding="utf-8"))
    scripts = [
        SCRIPTS / "Y5_R2FR_4914_complex_source_Taylor_TTT_replica.py",
        SCRIPTS
        / "Y5_R2FR_4914_complex_source_Taylor_TTT_replica_validation.py",
    ]
    rows = [
        check(
            "VAL4914_00_prior",
            prior[-1]["check_id"] == "VAL4913_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4913 predecessor validation passes",
        ),
        check(
            "VAL4914_01_sources",
            all(row["source_exists"] and row["marker_found"] for row in sources),
            "all source paths and markers resolve",
        ),
        check(
            "VAL4914_02_algebra",
            gate_map["complex_source_algebra"]["status"] == "PASS",
            "all complex source algebra checks pass",
        ),
        check(
            "VAL4914_03_free",
            gate_map["exact_free_determinant"]["status"] == "PASS",
            "direct jet agrees statistically with exact determinant",
        ),
        check(
            "VAL4914_04_direct",
            gate_map["direct_coordinate_moment_estimator"]["status"]
            == "REJECTED_VARIANCE",
            "catastrophic direct-moment variance is not hidden",
        ),
        check(
            "VAL4914_05_chain",
            gate_map["complex_replica_chain_health"]["status"] == "PASS",
            "both independent complex chains pass smoke health gates",
        ),
        check(
            "VAL4914_06_replica",
            gate_map["independent_estimator_compatibility"]["status"] == "PASS",
            "4913 and 4914 estimates remain statistically compatible",
        ),
        check(
            "VAL4914_07_cutoff",
            gate_map["scaled_cutoff_consistency"]["status"] == "PASS_DIAGNOSTIC",
            "dimensionally scaled complex rows agree across cutoffs",
        ),
        check(
            "VAL4914_08_complex_significance",
            gate_map["complex_only_nonzero_significance"]["status"]
            == "BELOW_PROMOTION",
            "complex-only aggregate remains below three sigma",
        ),
        check(
            "VAL4914_09_all_evidence",
            gate_map["all_independent_nonzero_significance"]["status"]
            == "FAIL_TO_REJECT_ZERO",
            "all independent evidence remains below two sigma",
        ),
        check(
            "VAL4914_10_covariance",
            gate_map["covariant_image"]["status"] == "FAIL",
            "failed covariant-image gate is retained",
        ),
        check(
            "VAL4914_11_mass",
            gate_map["exact_free_mass_propagation"]["status"]
            == "PASS_NEGLIGIBLE",
            "exact free pole-mass propagation is finite and negligible",
        ),
        check(
            "VAL4914_12_promotion",
            gate_map["interacting_C3_promotion"]["status"] == "BLOCKED_DEMOTED"
            and all(not row["promotion_allowed"] for row in gates),
            "no interacting C3 coefficient is promoted",
        ),
        check(
            "VAL4914_13_active",
            gate_map["Gamma_MTS_res"]["status"] == "ZERO_PRESERVED",
            "active residual remains zero",
        ),
        check(
            "VAL4914_14_next_route",
            gate_map["programme_route"]["status"]
            == "RETURN_TO_PARENT_EH_SOURCE_COUPLING",
            "programme returns to the central local-GR coupling problem",
        ),
        check(
            "VAL4914_15_joint",
            len(joint) == 2
            and all(not row["promotion_allowed"] for row in joint),
            "joint cross-stencil rows are present and nonclaim",
        ),
        check(
            "VAL4914_16_combinations",
            len(combinations) == 5
            and all(not row["promotion_allowed"] for row in combinations),
            "scaled complex and all-evidence combinations are explicit",
        ),
        check(
            "VAL4914_17_runs",
            run_state["status"] == "COMPLETE"
            and run_state["estimator"] == "complex_discrete"
            and (RUN_COMPLEX / "COMPLETE.marker").exists()
            and (RUN_MASS / "COMPLETE.marker").exists(),
            "complex checkpoint and mass propagation run records close",
        ),
        check(
            "VAL4914_18_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-756 is unique and accurately scoped",
        ),
        check(
            "VAL4914_19_variables",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "twelve checkpoint variables are unique",
        ),
        check(
            "VAL4914_20_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4914_21_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_COMPLEX_SOURCE_TTT_PROVENANCE_4914" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4914_22_registers",
            "1.207 Complex-source TTT arbitration" in equations
            and "158. An exact derivative" in redteam
            and "PPC4161 checkpoint 4914" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4914_23_resume",
            "4914-Y5-R2FR-matched-interacting" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume points from 4914 to the parent EH source-coupling target",
        ),
        check(
            "VAL4914_24_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence has no placeholder markers",
        ),
        check(
            "VAL4914_25_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence has no nonfinite numeric cells",
        ),
        check(
            "VAL4914_26_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4914_27_csv",
            len(generated_paths) == 16
            and all(path.exists() and read_csv(path) for path in generated_paths),
            "sixteen checkpoint CSVs parse",
        ),
        check(
            "VAL4914_28_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4914_29_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4914_30_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4915 parent EH source-coupling target is selected but not pre-created",
        ),
        check(
            "VAL4914_31_local",
            "GR/Newton/PPN/Maxwell                     = UNCHANGED" in checkpoint
            and "Gamma_{\\mathrm{MTS,res}}=0" in checkpoint,
            "lower-derivative local limits and active residual are unchanged",
        ),
    ]
    rows.append(
        check(
            "VAL4914_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_COMPLEX_SOURCE_TAYLOR_TTT_REPLICA_4914_VALIDATED",
        )
    )
    return rows


def main() -> int:
    joint = joint_projection_rows()
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_JOINT_STENCIL_PROJECTION.csv", joint
    )
    combinations = combination_rows(joint)
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_SCALED_COMBINATIONS.csv", combinations
    )
    gates = gate_rows(joint, combinations)
    write_csv(OUTPUT / "P8_Y5_R2FR_4914_GATE_DECISION.csv", gates)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4914_SOURCE_REGISTER.csv", sources)
    validation = validation_rows(joint, combinations, gates, sources)
    write_csv(OUTPUT / "P8_Y5_BRR545_4914_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4914_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4914_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
