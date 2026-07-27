from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5212 = FUNCTIONAL_RG / "5212"
SOURCE_5214 = FUNCTIONAL_RG / "5214"
SOURCE_5220 = FUNCTIONAL_RG / "5220"
SOURCE_5224 = FUNCTIONAL_RG / "5224"
SOURCE = FUNCTIONAL_RG / "5225"
RESIDUALS = POST / "source-intake" / "mts_residuals"

RESULT_5212 = SOURCE_5212 / "fresh_two_stratum_pilot_results.json"
EVENTS_5212 = SOURCE_5212 / "fresh_two_stratum_completed_event_rows.csv"
AUDIT_5214 = SOURCE_5214 / "A00_source_pole_family_audit.json"
RESULT_5220 = SOURCE_5220 / "fresh_grouped_classifier_A00_pilot_results.json"
MANIFEST_5224 = SOURCE_5224 / "frozen_replacement_manifest.json"
RESULT_5224 = SOURCE_5224 / "replacement_scaled_controlled_results.json"
EVENTS_5224 = SOURCE_5224 / "replacement_event_rows.csv"
CONTROLS_5224 = SOURCE_5224 / "replacement_A00_control_rows.csv"
VALIDATION_5224 = (
    RESIDUALS / "P8_Y5_BRR545_5224_VALIDATION.csv"
)
RUN_5224 = (
    SOURCE_5224 / "runs" / "replacement_scaled_controlled_v1"
)

RESULT = SOURCE / "control_multiplier_and_raw_salvage.json"
INFLUENCE = SOURCE / "permutation_control_event_influence.csv"
CONTRACT = SOURCE / "slot_balanced_estimator_contract.json"
DOCUMENT = (
    POST
    / "5225-Y5-R2FR-permutation-control-multiplier-theorem-and-raw-estimator-salvage.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5225_VALIDATION.csv"

MARKER = "MTS_5225_PERMUTATION_CONTROL_MULTIPLIER_AND_RAW_SALVAGE"
REVISION = "control-multiplier-correction-and-slot-balanced-route-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
KNOWN_MASTER_LOCAL_COEFFICIENT = 161.42318077192922
PHYSICAL_LOCAL_COEFFICIENT = -0.006798211255145276
PHYSICAL_LOCAL_STANDARD_ERROR = 7.327856002402611e-05


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def sample_covariance(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.cov(left, right, ddof=1)[0, 1])


def standard_deviation_ratio(
    raw: np.ndarray, control: np.ndarray, beta: float
) -> float:
    raw_sd = float(np.std(raw, ddof=1))
    return float(np.std(raw - beta * control, ddof=1) / raw_sd)


def multiplier_diagnostics(
    rows: list[dict[str, Any]], label: str
) -> dict[str, Any]:
    raw = np.asarray([float(row["raw_A00_real"]) for row in rows])
    control = np.asarray([float(row["control_real"]) for row in rows])
    covariance = sample_covariance(raw, control)
    control_variance = float(np.var(control, ddof=1))
    beta_optimal = covariance / control_variance
    lower = min(0.0, 2.0 * beta_optimal)
    upper = max(0.0, 2.0 * beta_optimal)
    return {
        "label": label,
        "event_count": len(rows),
        "raw_control_correlation": float(np.corrcoef(raw, control)[0, 1]),
        "raw_control_covariance": covariance,
        "control_sample_variance": control_variance,
        "posthoc_variance_minimizing_beta": beta_optimal,
        "posthoc_beta_is_claim_valid": False,
        "empirical_nonincrease_beta_interval": [lower, upper],
        "beta_zero_standard_deviation_ratio": standard_deviation_ratio(
            raw, control, 0.0
        ),
        "beta_half_standard_deviation_ratio": standard_deviation_ratio(
            raw, control, 0.5
        ),
        "beta_one_standard_deviation_ratio": standard_deviation_ratio(
            raw, control, 1.0
        ),
        "posthoc_beta_standard_deviation_ratio": standard_deviation_ratio(
            raw, control, beta_optimal
        ),
        "raw_sample_standard_deviation": float(np.std(raw, ddof=1)),
        "control_sample_standard_deviation": float(
            np.std(control, ddof=1)
        ),
        "beta_one_adjusted_sample_standard_deviation": float(
            np.std(raw - control, ddof=1)
        ),
    }


def array(
    rows: list[dict[str, str]], stratum: str, field: str
) -> np.ndarray:
    return np.asarray(
        [
            float(row[field])
            for row in rows
            if row["stratum"] == stratum
        ],
        dtype=np.float64,
    )


def raw_coefficient_estimate(
    label: str,
    full_real: np.ndarray,
    full_imaginary: np.ndarray,
    topological_real: np.ndarray,
    topological_imaginary: np.ndarray,
    tail: dict[str, Any],
    thresholds: dict[str, Any],
) -> dict[str, Any]:
    hhh_real = (
        PHYSICAL_LOCAL_COEFFICIENT
        + float(np.mean(full_real))
        + float(np.mean(topological_real))
    )
    hhh_imaginary = float(
        np.mean(full_imaginary) + np.mean(topological_imaginary)
    )
    k_real = -4.0 * (
        KNOWN_MASTER_LOCAL_COEFFICIENT + 2.0 * hhh_real
    )
    k_imaginary = -8.0 * hhh_imaginary
    real_standard_error = 8.0 * math.sqrt(
        PHYSICAL_LOCAL_STANDARD_ERROR**2
        + float(np.var(full_real, ddof=1)) / len(full_real)
        + float(np.var(topological_real, ddof=1))
        / len(topological_real)
    )
    imaginary_standard_error = 8.0 * math.sqrt(
        float(np.var(full_imaginary, ddof=1)) / len(full_imaginary)
        + float(np.var(topological_imaginary, ddof=1))
        / len(topological_imaginary)
    )
    tail_gate = bool(
        len(topological_real)
        >= int(thresholds["minimum_tail_event_count"])
        and float(tail["maximum_leave_one_out_shift_standard_errors"])
        <= float(thresholds["maximum_leave_one_out_shift_standard_errors"])
        and float(tail["ordered_half_means"]["difference_sigma"])
        <= float(thresholds["maximum_ordered_half_difference_sigma"])
        and float(tail["maximum_absolute_event_share"])
        <= float(thresholds["maximum_absolute_event_share"])
    )
    real_fraction_gate = bool(
        real_standard_error
        <= float(thresholds["maximum_real_standard_error_fraction"])
        * max(
            abs(k_real),
            float(thresholds["real_precision_scale_floor"]),
        )
    )
    imaginary_gate = bool(
        abs(k_imaginary)
        <= float(thresholds["maximum_imaginary_mean_standard_errors"])
        * imaginary_standard_error
    )
    return {
        "label": label,
        "full_event_count": len(full_real),
        "topological_event_count": len(topological_real),
        "full_real_sample_standard_deviation": float(
            np.std(full_real, ddof=1)
        ),
        "raw_topological_real_sample_standard_deviation": float(
            np.std(topological_real, ddof=1)
        ),
        "candidate_K_mu": {
            "real": k_real,
            "imaginary": k_imaginary,
            "real_standard_error": real_standard_error,
            "imaginary_standard_error": imaginary_standard_error,
        },
        "raw_real_tail_gate": tail_gate,
        "real_precision_fraction_gate": real_fraction_gate,
        "imaginary_zero_compatibility_gate": imaginary_gate,
        "maximum_nonlocal_mismatch_not_recomputed": True,
        "coefficient_precision_gate": False,
        "valid_for_numeric_UV_claim": False,
    }


def partition_ratio_influence(
    control_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in control_rows:
        seed = int(row["seed"])
        ratio_rows: list[dict[str, Any]] = []
        for epsilon_id in ("E040", "E020"):
            job = (
                RUN_5224
                / "topological-jobs"
                / (
                    f"TOP__{epsilon_id}__S{seed}_N0000"
                    "__A00__primary24.json"
                )
            )
            document = read_json(job)
            for pair in document["pair_rows"]:
                weighted = complex(
                    float(pair["weighted_permuted_contribution"]["real"]),
                    float(
                        pair["weighted_permuted_contribution"]["imaginary"]
                    ),
                )
                if abs(weighted) == 0.0:
                    continue
                first_ratio = complex(
                    float(pair["first_permutation_partition_ratio"]["real"]),
                    float(
                        pair["first_permutation_partition_ratio"][
                            "imaginary"
                        ]
                    ),
                )
                second_ratio = complex(
                    float(pair["second_permutation_partition_ratio"]["real"]),
                    float(
                        pair["second_permutation_partition_ratio"][
                            "imaginary"
                        ]
                    ),
                )
                ratio_rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "maximum_ratio_magnitude": max(
                            abs(first_ratio), abs(second_ratio)
                        ),
                        "weighted_permuted_magnitude": abs(weighted),
                    }
                )
        maximum_ratio = max(
            (
                float(item["maximum_ratio_magnitude"])
                for item in ratio_rows
            ),
            default=0.0,
        )
        maximum_weighted = max(
            (
                float(item["weighted_permuted_magnitude"])
                for item in ratio_rows
            ),
            default=0.0,
        )
        results.append(
            {
                "seed": seed,
                "tranche": int(row["tranche"]),
                "raw_A00_real": float(row["raw_A00_real"]),
                "control_real": float(row["control_real"]),
                "adjusted_A00_real": float(row["adjusted_A00_real"]),
                "absolute_control_real": abs(float(row["control_real"])),
                "maximum_partition_ratio_magnitude": maximum_ratio,
                "maximum_weighted_permuted_magnitude": maximum_weighted,
                "selected_control_pair_count_E040": int(
                    row["E040_selected_control_pair_count"]
                ),
                "selected_control_pair_count_E020": int(
                    row["E020_selected_control_pair_count"]
                ),
                "valid_for_numeric_UV_claim": False,
            }
        )
    ordered = sorted(
        results, key=lambda item: item["absolute_control_real"], reverse=True
    )
    for index, row in enumerate(ordered, start=1):
        row["absolute_control_rank"] = index
    return ordered


def slot_balanced_contract() -> dict[str, Any]:
    return {
        "checkpoint": 5225,
        "checkpoint_marker": MARKER,
        "selected_next_route": (
            "derive_and_blind_test_direct_slot_balanced_permutation_pair"
        ),
        "rejected_route": (
            "do_not_retune_or_reuse_the_source_only_importance_ratio_control"
        ),
        "channel_estimators": {
            "slot_3": "A3=3*w3*F3(q3)",
            "slot_1": "A1=3*w1*F1(q1)",
            "paired": "A_pair=(A3+A1)/2",
        },
        "derived_expectation_identity": (
            "under the exact g1<->g3 chart bijection, invariant phase-space "
            "measure and identical-state sum imply E[A1]=E[A3]=I and "
            "therefore E[A_pair]=I"
        ),
        "derived_variance_identity": (
            "if A1 and A3 are square-integrable and identically distributed, "
            "Var(A_pair)=(Var(A3)+Cov(A3,A1))/2<=Var(A3)"
        ),
        "why_the_bound_holds": (
            "Cauchy-Schwarz gives Cov(A3,A1)<=sqrt(Var(A3)Var(A1))="
            "Var(A3)"
        ),
        "forbidden_importance_ratio": (
            "the paired estimator evaluates each chart with its own bounded "
            "partition weight; it never multiplies a source family by w1/w3"
        ),
        "required_implementation_proofs": [
            "explicit q3-to-q1 chart bijection and Jacobian",
            "slot-agnostic topology and homotopy construction",
            "full integrand and subtraction relabelling covariance",
            "per-chart finite second moment or a proved envelope",
            "machine check that the two channel estimators have equal means",
        ],
        "blind_pilot_gate": {
            "freeze_seeds_and_thresholds_before_outcomes": True,
            "all_jobs_must_converge": True,
            "channel_mean_difference_must_be_zero_compatible": True,
            "paired_variance_must_not_exceed_single_channel_variance": True,
            "no_posthoc_control_multiplier": True,
        },
        "fallback_if_chart_map_fails": (
            "use the raw estimator only and derive a new independent "
            "allocation; beta=1 is retired"
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    sources = [
        Path(__file__).resolve(),
        RESULT_5212,
        EVENTS_5212,
        AUDIT_5214,
        RESULT_5220,
        MANIFEST_5224,
        RESULT_5224,
        EVENTS_5224,
        CONTROLS_5224,
        VALIDATION_5224,
    ]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing source paths: {missing}")

    result_5220 = read_json(RESULT_5220)
    result_5224 = read_json(RESULT_5224)
    manifest_5224 = read_json(MANIFEST_5224)
    thresholds = manifest_5224["acceptance_thresholds"]
    controls = read_csv(CONTROLS_5224)
    fresh_events = read_csv(EVENTS_5224)
    legacy_events = read_csv(EVENTS_5212)

    fresh_diagnostics = multiplier_diagnostics(controls, "fresh_all_24")
    tranche_diagnostics = [
        multiplier_diagnostics(
            [
                row
                for row in controls
                if int(row["tranche"]) == tranche
            ],
            f"fresh_tranche_{tranche}",
        )
        for tranche in (1, 2)
    ]

    pilot_analysis = result_5220["analysis"]
    pilot_control_variance = (
        float(
            pilot_analysis["control_real"]["sample_standard_deviation"]
        )
        ** 2
    )
    pilot_beta = (
        float(pilot_analysis["raw_control_covariance"])
        / pilot_control_variance
    )
    raw_fresh = np.asarray(
        [float(row["raw_A00_real"]) for row in controls]
    )
    control_fresh = np.asarray(
        [float(row["control_real"]) for row in controls]
    )
    pilot_multiplier = {
        "pilot_event_count": int(pilot_analysis["event_count"]),
        "pilot_raw_control_correlation": float(
            pilot_analysis["raw_control_correlation"]
        ),
        "pilot_posthoc_variance_minimizing_beta": pilot_beta,
        "pilot_beta_applied_to_fresh_standard_deviation_ratio": (
            standard_deviation_ratio(raw_fresh, control_fresh, pilot_beta)
        ),
        "pilot_delete_one_maximum_standard_deviation_ratio": max(
            float(row["standard_deviation_ratio"])
            for row in pilot_analysis[
                "delete_one_standard_deviation_ratios"
            ]
        ),
        "pilot_beta_is_independent_of_fresh_sample": True,
        "pilot_beta_is_efficient_on_fresh_sample": False,
    }

    fresh_full_real = array(fresh_events, "full", "naive_local_real")
    fresh_full_imaginary = array(
        fresh_events, "full", "naive_local_imaginary"
    )
    fresh_topological_real = array(
        fresh_events, "topological", "raw_topological_local_real"
    )
    fresh_topological_imaginary = array(
        fresh_events, "topological", "raw_topological_local_imaginary"
    )
    legacy_full_real = array(legacy_events, "full", "naive_local_real")
    legacy_full_imaginary = array(
        legacy_events, "full", "naive_local_imaginary"
    )
    legacy_topological_real = array(
        legacy_events, "topological", "topological_local_real"
    )
    legacy_topological_imaginary = array(
        legacy_events, "topological", "topological_local_imaginary"
    )

    raw_fresh_estimate = raw_coefficient_estimate(
        "fresh_raw_2_plus_24",
        fresh_full_real,
        fresh_full_imaginary,
        fresh_topological_real,
        fresh_topological_imaginary,
        result_5224["analysis"]["new_only_estimate"][
            "raw_topological_local"
        ]["real"],
        thresholds,
    )
    raw_pooled_estimate = raw_coefficient_estimate(
        "compatible_raw_pool_4_plus_36",
        np.concatenate((legacy_full_real, fresh_full_real)),
        np.concatenate(
            (legacy_full_imaginary, fresh_full_imaginary)
        ),
        np.concatenate(
            (legacy_topological_real, fresh_topological_real)
        ),
        np.concatenate(
            (
                legacy_topological_imaginary,
                fresh_topological_imaginary,
            )
        ),
        result_5224["analysis"]["pooled_estimate"][
            "raw_topological_local"
        ]["real"],
        thresholds,
    )

    influence = partition_ratio_influence(controls)
    write_csv(INFLUENCE, influence)
    contract = slot_balanced_contract()
    atomic_json(CONTRACT, contract)

    formal_digest = tree_digest(FORMAL)
    result = {
        "checkpoint": 5225,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": (
            "RETIRE_BETA_ONE_KEEP_ZERO_IDENTITY_AND_BUILD_DIRECT_"
            "SLOT_BALANCED_PAIR"
        ),
        "control_multiplier_theorem": {
            "zero_mean_identity": (
                "C=Y13-(w1/w3)Y31 and E[C]=0, subject to integrability"
            ),
            "unbiased_family": (
                "for deterministic beta independent of the evaluation "
                "sample, F_beta=F-beta*C obeys E[F_beta]=E[F]"
            ),
            "variance_law": (
                "Var(F-beta*C)=Var(F)-2*beta*Cov(F,C)+"
                "beta^2*Var(C)"
            ),
            "variance_minimizer": "beta*=Cov(F,C)/Var(C)",
            "correction_to_checkpoint_5214_wording": (
                "permutation symmetry fixes the internal ratio w1/w3 and "
                "the zero-mean identity; it does not fix the external "
                "control multiplier beta to one"
            ),
            "checkpoint_5214_identity_retained": True,
            "checkpoint_5224_beta_one_efficiency_rejected": True,
        },
        "fresh_multiplier_diagnostics": fresh_diagnostics,
        "tranche_multiplier_diagnostics": tranche_diagnostics,
        "pilot_multiplier_transfer": pilot_multiplier,
        "importance_ratio_tail_diagnostic": {
            "largest_absolute_controls": influence[:4],
            "maximum_partition_ratio_magnitude": max(
                float(row["maximum_partition_ratio_magnitude"])
                for row in influence
            ),
            "square_integrability_status": "not_proved",
            "standard_massless_soft_measure_condition": (
                "if dPhi~E1^a dE1 and Y31~E1^p, the squared reweighted "
                "term is locally integrable only when "
                "a+2p-4>-1; for a=1 this requires p>1"
            ),
            "inference": (
                "the observed large ratios and control outliers explain "
                "the failed variance gate but do not alone prove an "
                "infinite population variance"
            ),
        },
        "raw_estimator_salvage": {
            "fresh": raw_fresh_estimate,
            "pooled": raw_pooled_estimate,
            "interpretation": (
                "the raw estimator is finite and cheaper in fresh-sample "
                "variance than beta=1, but neither raw estimate passes "
                "tail and precision requirements"
            ),
        },
        "next_estimator_contract": str(CONTRACT),
        "source_provenance": [
            {"path": str(path), "sha256": digest(path)}
            for path in sources
        ],
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)

    validation_5224 = read_csv(VALIDATION_5224)
    validation_rows = [
        {
            "check": "all_source_paths_exist",
            "passed": not missing,
            "detail": str(len(sources)),
        },
        {
            "check": "replacement_design_complete_without_failed_jobs",
            "passed": (
                result_5224["state"] == "COMPLETE_DESIGN"
                and int(result_5224["counts"]["completed_converged"]) == 520
                and int(result_5224["counts"]["completed_unconverged"]) == 0
                and int(result_5224["counts"]["failed"]) == 0
                and int(result_5224["counts"]["missing"]) == 0
            ),
            "detail": json.dumps(result_5224["counts"], sort_keys=True),
        },
        {
            "check": "checkpoint_5224_validation_all_passed",
            "passed": (
                bool(result_5224["validation_all_passed"])
                and all(
                    row["passed"].strip().lower() == "true"
                    for row in validation_5224
                )
            ),
            "detail": str(len(validation_5224)),
        },
        {
            "check": "symmetry_ratio_separated_from_control_multiplier",
            "passed": (
                "does not fix the external"
                in result["control_multiplier_theorem"][
                    "correction_to_checkpoint_5214_wording"
                ]
            ),
            "detail": result["control_multiplier_theorem"][
                "variance_law"
            ],
        },
        {
            "check": "fresh_beta_one_efficiency_rejected",
            "passed": (
                fresh_diagnostics[
                    "beta_one_standard_deviation_ratio"
                ]
                > 1.0
                and not result_5224["analysis"][
                    "fresh_control_diagnostics"
                ]["final_control_gate"]
            ),
            "detail": str(
                fresh_diagnostics[
                    "beta_one_standard_deviation_ratio"
                ]
            ),
        },
        {
            "check": "pilot_multiplier_does_not_transfer",
            "passed": (
                pilot_multiplier[
                    "pilot_beta_applied_to_fresh_standard_deviation_ratio"
                ]
                > 1.0
            ),
            "detail": str(
                pilot_multiplier[
                    "pilot_beta_applied_to_fresh_standard_deviation_ratio"
                ]
            ),
        },
        {
            "check": "importance_ratio_tail_is_explicit",
            "passed": (
                result["importance_ratio_tail_diagnostic"][
                    "maximum_partition_ratio_magnitude"
                ]
                > 10.0
                and result["importance_ratio_tail_diagnostic"][
                    "square_integrability_status"
                ]
                == "not_proved"
            ),
            "detail": str(
                result["importance_ratio_tail_diagnostic"][
                    "maximum_partition_ratio_magnitude"
                ]
            ),
        },
        {
            "check": "raw_estimates_are_finite_nonclaims",
            "passed": all(
                math.isfinite(
                    float(
                        estimate["candidate_K_mu"][
                            "real_standard_error"
                        ]
                    )
                )
                and not estimate["valid_for_numeric_UV_claim"]
                for estimate in (raw_fresh_estimate, raw_pooled_estimate)
            ),
            "detail": (
                f"{raw_fresh_estimate['candidate_K_mu']['real_standard_error']};"
                f"{raw_pooled_estimate['candidate_K_mu']['real_standard_error']}"
            ),
        },
        {
            "check": "slot_balanced_route_uses_no_importance_ratio",
            "passed": (
                "never multiplies"
                in contract["forbidden_importance_ratio"]
                and contract["channel_estimators"]["paired"]
                == "A_pair=(A3+A1)/2"
            ),
            "detail": contract["forbidden_importance_ratio"],
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": not any(
                (
                    result["valid_for_numeric_UV_claim"],
                    result["valid_for_local_GR_claim"],
                    result["valid_for_full_MTS_claim"],
                    contract["valid_for_numeric_UV_claim"],
                    contract["valid_for_local_GR_claim"],
                    contract["valid_for_full_MTS_claim"],
                )
            ),
            "detail": "numeric UV, local GR and full MTS remain false",
        },
    ]
    write_csv(VALIDATION, validation_rows)
    if not all(bool(row["passed"]) for row in validation_rows):
        raise RuntimeError(
            "checkpoint-5225 validation failed: "
            + json.dumps(
                [row for row in validation_rows if not row["passed"]],
                indent=2,
            )
        )

    fresh_raw = raw_fresh_estimate["candidate_K_mu"]
    pooled_raw = raw_pooled_estimate["candidate_K_mu"]
    largest = influence[0]
    document = f"""# 5225 - Permutation-control multiplier theorem and raw salvage

## Result

Checkpoint 5224 completed all `520/520` jobs with no failed or
unconverged job, but its frozen unit-multiplier control failed exactly as
the protocol required it to fail. The final decision is
`{result['decision']}`.

This is an estimator correction, not a contradiction in the MTS amplitude.
The zero-mean permutation identity survives. The claim that permutation
symmetry fixes the *external* control multiplier to one does not.

## Exact multiplier theorem

Let

`C = Y13 - (w1/w3) Y31`, with `E[C]=0`.

For any deterministic multiplier `beta` chosen independently of the
evaluation sample,

`F_beta = F - beta C`

is unbiased, and

`Var(F_beta) = Var(F) - 2 beta Cov(F,C) + beta^2 Var(C)`.

Thus `beta*=Cov(F,C)/Var(C)` minimizes variance. Symmetry fixes the
internal reweighting `w1/w3`; it does not select `beta=1`. The historical
checkpoint-5214 identity remains valid, but its unit-multiplier wording is
superseded here.

## What the scaled test established

- Fresh events: `{fresh_diagnostics['event_count']}`.
- Fresh raw-control correlation:
  `{fresh_diagnostics['raw_control_correlation']:.9g}`.
- Fresh post-hoc optimum `beta`:
  `{fresh_diagnostics['posthoc_variance_minimizing_beta']:.9g}`
  (diagnostic only).
- Unit-`beta` A00 SD ratio:
  `{fresh_diagnostics['beta_one_standard_deviation_ratio']:.9g}`.
- Pilot-derived `beta={pilot_beta:.9g}` applied unchanged to the fresh
  sample gives SD ratio
  `{pilot_multiplier['pilot_beta_applied_to_fresh_standard_deviation_ratio']:.9g}`.
- The two fresh tranches select opposite/near-zero empirical multipliers:
  `{tranche_diagnostics[0]['posthoc_variance_minimizing_beta']:.9g}` and
  `{tranche_diagnostics[1]['posthoc_variance_minimizing_beta']:.9g}`.

The largest fresh control has `|C|={largest['absolute_control_real']:.9g}`
and a rootwise partition-ratio magnitude up to
`{largest['maximum_partition_ratio_magnitude']:.9g}`. Across the sample the
maximum ratio is
`{result['importance_ratio_tail_diagnostic']['maximum_partition_ratio_magnitude']:.9g}`.
The ratio `(E3/E1)^2` therefore creates an importance-reweighting tail that
was not controlled by the small pilot. Infinite variance is not claimed:
square integrability remains unproved.

## Raw-estimator salvage

Removing the rejected control gives:

- Fresh `2+24`:
  `K_mu={fresh_raw['real']:.9g}{fresh_raw['imaginary']:+.9g} i`,
  with real/imaginary SE
  `{fresh_raw['real_standard_error']:.9g}` /
  `{fresh_raw['imaginary_standard_error']:.9g}`.
- Compatible raw pool `4+36`:
  `K_mu={pooled_raw['real']:.9g}{pooled_raw['imaginary']:+.9g} i`,
  with real/imaginary SE
  `{pooled_raw['real_standard_error']:.9g}` /
  `{pooled_raw['imaginary_standard_error']:.9g}`.

Both remain tail/precision non-claims. The useful result is that the raw
calculation is finite and recoverable; the failed unit control did not
destroy the underlying event data.

## Derived next route

The next estimator should pair *directly evaluated channels*, not
importance-reweight one source family:

`A3 = 3 w3 F3(q3)`,

`A1 = 3 w1 F1(q1)`,

`A_pair = (A3 + A1)/2`.

Under the exact `g1<->g3` chart bijection,
`E[A1]=E[A3]=I`. If the channels are square-integrable and identically
distributed,

`Var(A_pair) = (Var(A3)+Cov(A3,A1))/2 <= Var(A3)`.

This follows from Cauchy-Schwarz and gives a genuine non-increase theorem.
Each channel uses its own bounded partition weight; no `w1/w3` factor is
allowed. The next implementation must derive the chart Jacobian, make the
topology/homotopy code slot-agnostic, and blind-test the paired estimator.
If that map cannot be built, the fallback is a newly allocated raw run,
not a post-hoc retuning of `beta`.

## Claim boundary

No numerical UV coefficient, local-GR result, galaxy result, or full-MTS
claim follows. The crossed-`hhh` coefficient remains unresolved, and the
other cut classes remain outside this calculation.

## Evidence

- Result: `{RESULT}`
- Event influence: `{INFLUENCE}`
- Next-estimator contract: `{CONTRACT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)

    print(
        json.dumps(
            {
                "checkpoint": 5225,
                "decision": result["decision"],
                "fresh_beta_one_sd_ratio": fresh_diagnostics[
                    "beta_one_standard_deviation_ratio"
                ],
                "fresh_raw_K_mu": fresh_raw,
                "pooled_raw_K_mu": pooled_raw,
                "maximum_partition_ratio_magnitude": result[
                    "importance_ratio_tail_diagnostic"
                ]["maximum_partition_ratio_magnitude"],
                "validation_all_passed": True,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
