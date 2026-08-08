from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()

CHECKPOINT_5176_DOCUMENT = (
    POST / "5176-Y5-R2FR-predeclared-paired-high-mode-seed-ensemble.md"
)
CHECKPOINT_5176_RUNNER = (
    POST
    / "scripts"
    / "Y5_R2FR_5176_predeclared_paired_high_mode_seed_ensemble.py"
)
CHECKPOINT_5176_VERIFIER = (
    POST / "scripts" / "Y5_R2FR_5176_runner_freeze_verifier.py"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"
CHECKPOINT_5176_PROTOCOL = CHECKPOINT_5176_ROOT / "ensemble_protocol.json"
CHECKPOINT_5176_SCHEDULE = (
    CHECKPOINT_5176_ROOT / "predeclared_seed_schedule.csv"
)
CHECKPOINT_5176_RESULT = (
    CHECKPOINT_5176_ROOT / "paired_ensemble_results.json"
)
CHECKPOINT_5176_SCORE = CHECKPOINT_5176_ROOT / "paired_seed_scores.csv"
CHECKPOINT_5176_FREEZE = CHECKPOINT_5176_ROOT / "runner_freeze.json"
CHECKPOINT_5176_VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5176_VALIDATION.csv"
)

CHECKPOINT_5170_DOCUMENT = (
    POST
    / "5170-Y5-R2FR-collective-stress-residual-single-coupling-no-go-and-conserved-kernel-target.md"
)
CHECKPOINT_5170_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5170"
    / "collective_stress_residual_results.json"
)
CHECKPOINT_4960_DOCUMENT = (
    POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)
CHECKPOINT_4960_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "integrated_H_universal_source_results.json"
)
CHECKPOINT_4960_CALIBRATIONS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "local_limit_chain_and_calibrations.csv"
)
SCORE_DEFINITION_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5164_mass_conserving_two_component_initial_value_gate.py"
)
Q_DEFINITION_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5163_parent_wave_and_visible_source_response_gate.py"
)

OUT = POST / "source-intake" / "functional_rg" / "5177"
SEED_DIAGNOSTICS_CSV = OUT / "paired_seed_metric_split_diagnostics.csv"
NORMALIZATION_CSV = OUT / "constant_normalization_no_go.csv"
RADIAL_PROFILE_CSV = OUT / "reconstructed_radial_profiles.csv"
RADIAL_CONTRIBUTION_CSV = OUT / "paired_radial_MSE_contributions.csv"
DESCRIPTIVE_STATISTICS_CSV = OUT / "post_hoc_descriptive_statistics.csv"
SUMMARY_CSV = OUT / "metric_split_summary.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
DECISION_CSV = OUT / "route_decision.csv"
RESULT_JSON = OUT / "locked_metric_split_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5177_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-theorem.md"
)

MARKER = "MTS_5177_LOCKED_ENSEMBLE_METRIC_SPLIT_NO_RETUNING_THEOREM"
CHECKED_DATE = "2026-07-23"
PROTOCOL_SHA256 = (
    "64529978cc452b302a5f09f52fff4be7af2ae8ef5cd64f29a8352005925fb7e7"
)
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
BOOTSTRAP_REPLICATES = 20_000
BOOTSTRAP_SEED = 517700777
ALPHA = 0.05

MODEL_FAMILIES = (
    ("MTS", "MTS_1E_MINUS20_ISOTROPIC_96", "MTS_1e_minus20_eV"),
    ("CDM", "CDM_ISOTROPIC_96", "CDM"),
)

ROUTE_DECISION = (
    "THE_LOCKED_MTS_Q_ADVANTAGE_IS_A_LOCAL_TRANSITION_SLOPE_EFFECT_WHILE_"
    "GLOBAL_AMPLITUDE_AND_CENTERED_SHAPE_REMAIN_UNRESOLVED_AND_NO_CONSTANT_"
    "SOURCE_NORMALIZATION_CAN_MATCH_TRANSITION_AND_EDGE_OR_REPLACE_THE_"
    "CALIBRATED_GN_RETURN_TO_A_PARENT_DERIVED_NONMULTIPLICATIVE_CONSERVED_"
    "STATE_STRESS_BEFORE_A_NEW_PREREGISTERED_GATE"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
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


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(file_digest(path).encode("ascii"))
    return digest.hexdigest()


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5177_script": SCRIPT,
        "checkpoint_5176_document": CHECKPOINT_5176_DOCUMENT,
        "checkpoint_5176_runner": CHECKPOINT_5176_RUNNER,
        "checkpoint_5176_verifier": CHECKPOINT_5176_VERIFIER,
        "checkpoint_5176_protocol": CHECKPOINT_5176_PROTOCOL,
        "checkpoint_5176_schedule": CHECKPOINT_5176_SCHEDULE,
        "checkpoint_5176_result": CHECKPOINT_5176_RESULT,
        "checkpoint_5176_score": CHECKPOINT_5176_SCORE,
        "checkpoint_5176_freeze": CHECKPOINT_5176_FREEZE,
        "checkpoint_5176_validation": CHECKPOINT_5176_VALIDATION,
        "checkpoint_5170_document": CHECKPOINT_5170_DOCUMENT,
        "checkpoint_5170_result": CHECKPOINT_5170_RESULT,
        "checkpoint_4960_document": CHECKPOINT_4960_DOCUMENT,
        "checkpoint_4960_result": CHECKPOINT_4960_RESULT,
        "checkpoint_4960_calibrations": CHECKPOINT_4960_CALIBRATIONS,
        "score_definition_script": SCORE_DEFINITION_SCRIPT,
        "q_definition_script": Q_DEFINITION_SCRIPT,
    }


def load_runner() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5176_for_5177", CHECKPOINT_5176_RUNNER
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load module: {CHECKPOINT_5176_RUNNER}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def bootstrap_interval(
    values: np.ndarray, stream_offset: int
) -> tuple[float, float]:
    generator = np.random.default_rng(BOOTSTRAP_SEED + stream_offset)
    indices = generator.integers(
        0, values.size, size=(BOOTSTRAP_REPLICATES, values.size)
    )
    means = np.mean(values[indices], axis=1)
    lower, upper = np.quantile(means, [ALPHA / 2.0, 1.0 - ALPHA / 2.0])
    return float(lower), float(upper)


def exact_sign_flip_p(values: np.ndarray) -> float:
    observed = abs(float(np.mean(values)))
    extreme = 0
    total = 2 ** int(values.size)
    for signs in itertools.product((-1.0, 1.0), repeat=int(values.size)):
        trial = abs(
            float(np.mean(values * np.asarray(signs, dtype=float)))
        )
        if trial >= observed - 1.0e-15:
            extreme += 1
    return extreme / total


def descriptive_row(
    metric_id: str,
    definition: str,
    values: list[float],
    stream_offset: int,
    units: str,
    sign_convention: str,
) -> dict[str, Any]:
    array = np.asarray(values, dtype=float)
    lower, upper = bootstrap_interval(array, stream_offset)
    return {
        "metric_id": metric_id,
        "definition": definition,
        "sample_count": int(array.size),
        "mean": float(np.mean(array)),
        "median": float(np.median(array)),
        "sample_standard_deviation": float(np.std(array, ddof=1)),
        "bootstrap_95_lower": lower,
        "bootstrap_95_upper": upper,
        "exact_two_sided_sign_flip_p": exact_sign_flip_p(array),
        "units": units,
        "sign_convention": sign_convention,
        "inferential_status": (
            "POST_HOC_DESCRIPTIVE_ONLY_NOT_PART_OF_5176_CONFIRMATORY_RULE"
        ),
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True, allow_nan=False),
        }
    )


def load_counts(path: Path) -> np.ndarray:
    with np.load(path, allow_pickle=False) as archive:
        return np.asarray(archive["averaged_counts"], dtype=float)


def reconstruct_model(
    runner: Any,
    base: dict[str, Any],
    seed_dir: Path,
    seed_index: int,
    high_mode_seed: int,
    short_model: str,
    family_id: str,
    recorded_model: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    radii = np.asarray(base["radii"], dtype=float)
    target_velocity_squared = np.asarray(base["target_velocity"], dtype=float)
    score_mask = np.asarray(base["score_mask"], dtype=bool)
    transition_radius = float(base["transition_radius"])
    edge_radius = float(base["edge_radius"])
    target_edge_mass = float(base["target_edge_mass"])
    run_dir = seed_dir / "runs" / family_id
    phase_masses: list[np.ndarray] = []

    for phase_sign, phase_name, cache_name in (
        (-1, "minus", "MINUS1"),
        (1, "plus", "PLUS1"),
    ):
        snapshot_path = (
            run_dir / f"phase_{phase_name}_isolated_initial_state.npz"
        )
        with np.load(snapshot_path, allow_pickle=False) as archive:
            positions = np.asarray(archive["positions_kpc"], dtype=float)
            particle_mass = float(archive["particle_mass_Msun"][0])
        _, initial_mass = runner.resolution.DYNAMICS.snapshot_profile(
            positions, radii, particle_mass
        )
        source_counts = load_counts(
            run_dir
            / "evolution-cache"
            / f"SOURCE_PHASE_{cache_name}.npz"
        )
        control_counts = load_counts(
            run_dir
            / "evolution-cache"
            / f"CONTROL_PHASE_{cache_name}.npz"
        )
        background_mass = (
            4.0
            * math.pi
            * runner.resolution.PM.RHO_M_MSUN_MPC3
            * (radii / 1000.0) ** 3
            / 3.0
        )
        source_mass = runner.resolution.PM.MOTION_FRACTION * np.maximum(
            source_counts * particle_mass - background_mass, 0.0
        )
        control_mass = runner.resolution.PM.MOTION_FRACTION * np.maximum(
            control_counts * particle_mass - background_mass, 0.0
        )
        ratio = np.ones_like(radii)
        positive_control = control_mass > 0.0
        ratio[positive_control] = (
            source_mass[positive_control] / control_mass[positive_control]
        )
        phase_masses.append(initial_mass * ratio)

    corrected_mass = 0.5 * (phase_masses[0] + phase_masses[1])
    gravitational_constant = (
        runner.resolution.DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
    )
    velocity_squared = (
        gravitational_constant
        * corrected_mass
        / np.maximum(radii, np.finfo(float).tiny)
    )
    score = runner.resolution.DYNAMICS.score_profile(
        radii,
        corrected_mass,
        target_velocity_squared,
        score_mask,
        transition_radius,
        edge_radius,
        target_edge_mass,
    )
    score_valid = (
        score_mask & np.isfinite(velocity_squared) & (velocity_squared > 0.0)
    )
    if np.any(target_velocity_squared[score_valid] <= 0.0):
        raise RuntimeError("nonpositive target inside score mask")
    log_residual = np.full(radii.shape, np.nan, dtype=float)
    log_residual[score_valid] = np.log10(
        velocity_squared[score_valid]
        / target_velocity_squared[score_valid]
    )
    scored_residual = log_residual[score_valid]
    mean_log_residual = float(np.mean(scored_residual))
    centered_variance = float(
        np.mean((scored_residual - mean_log_residual) ** 2)
    )
    best_amplitude = 10.0 ** (-mean_log_residual)
    local_q_valid = (
        (radii > 0.0)
        & (velocity_squared > 0.0)
        & np.isfinite(velocity_squared)
    )
    local_q_indices = np.flatnonzero(local_q_valid)
    transition_index = int(
        np.searchsorted(radii[local_q_indices], transition_radius)
    )
    lower = max(0, transition_index - 2)
    upper = min(len(local_q_indices), transition_index + 3)
    q_stencil = local_q_indices[lower:upper]
    q_invariance_error = max(
        abs(
            float(
                runner.resolution.DYNAMICS.PREVIOUS.local_logarithmic_q(
                    radii, amplitude * velocity_squared, transition_radius
                )
            )
            - float(score["q"])
        )
        for amplitude in (0.25, best_amplitude, 4.0)
    )
    transition_ratio = float(
        score["transition_velocity_squared_ratio_to_target"]
    )
    edge_ratio = float(score["edge_mass_ratio_to_target"])
    transition_amplitude = 1.0 / transition_ratio
    edge_amplitude = 1.0 / edge_ratio
    two_anchor_amplitude = 1.0 / math.sqrt(
        transition_ratio * edge_ratio
    )
    two_anchor_mismatch_factor = math.sqrt(edge_ratio / transition_ratio)

    diagnostics = {
        "seed_index": seed_index,
        "high_mode_seed": high_mode_seed,
        "model": short_model,
        "recorded_model": recorded_model,
        "q": float(score["q"]),
        "RMSE_dex": float(score["velocity_squared_log10_RMSE"]),
        "mean_log10_residual_dex": mean_log_residual,
        "centered_shape_variance_dex2": centered_variance,
        "centered_shape_RMSE_dex": math.sqrt(centered_variance),
        "best_post_hoc_amplitude": best_amplitude,
        "best_post_hoc_implied_delta_G_over_G": best_amplitude - 1.0,
        "transition_velocity_squared_ratio_to_target": transition_ratio,
        "edge_mass_ratio_to_target": edge_ratio,
        "amplitude_required_at_transition": transition_amplitude,
        "amplitude_required_at_edge": edge_amplitude,
        "two_anchor_log_minimax_amplitude": two_anchor_amplitude,
        "two_anchor_unavoidable_mismatch_factor": (
            two_anchor_mismatch_factor
        ),
        "q_stencil_min_radius_kpc": float(radii[q_stencil[0]]),
        "q_stencil_max_radius_kpc": float(radii[q_stencil[-1]]),
        "q_stencil_count": int(q_stencil.size),
        "score_count": int(np.count_nonzero(score_valid)),
        "constant_amplitude_q_maximum_error": q_invariance_error,
        "target_used_only_for_post_evolution_scoring": True,
        "target_used_to_define_evolution": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
        "_mass": corrected_mass,
        "_velocity_squared": velocity_squared,
        "_score_valid": score_valid,
        "_log_residual": log_residual,
        "_q_stencil": q_stencil,
    }

    profile_rows: list[dict[str, Any]] = []
    q_lower_index = int(q_stencil[0])
    q_upper_index = int(q_stencil[-1])
    for radius_index, radius in enumerate(radii):
        if radius_index < q_lower_index:
            zone = "INNER_OF_Q_STENCIL"
        elif radius_index <= q_upper_index:
            zone = "Q_STENCIL"
        else:
            zone = "OUTER_OF_Q_STENCIL"
        residual = log_residual[radius_index]
        profile_rows.append(
            {
                "seed_index": seed_index,
                "high_mode_seed": high_mode_seed,
                "model": short_model,
                "radius_index": radius_index,
                "radius_kpc": float(radius),
                "radius_over_transition": float(radius / transition_radius),
                "zone": zone,
                "in_score_mask": bool(score_valid[radius_index]),
                "in_q_stencil": bool(radius_index in q_stencil),
                "corrected_motion_mass_Msun": float(
                    corrected_mass[radius_index]
                ),
                "predicted_velocity_squared_km2_s2": float(
                    velocity_squared[radius_index]
                ),
                "target_velocity_squared_km2_s2": float(
                    target_velocity_squared[radius_index]
                ),
                "log10_velocity_squared_ratio_dex": (
                    float(residual) if math.isfinite(residual) else ""
                ),
                "squared_log_residual_dex2": (
                    float(residual**2) if math.isfinite(residual) else ""
                ),
                "target_used_only_for_post_evolution_scoring": True,
                "target_used_to_define_evolution": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return diagnostics, profile_rows


def public_diagnostics(
    diagnostics: dict[str, Any]
) -> dict[str, Any]:
    return {
        key: value
        for key, value in diagnostics.items()
        if not key.startswith("_")
    }


def summary_row(
    metric_id: str,
    value: Any,
    units: str,
    interpretation: str,
) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "value": value,
        "units": units,
        "interpretation": interpretation,
        "inferential_status": (
            "EXACT_RECONSTRUCTION_OR_POST_HOC_DIAGNOSTIC_AS_LABELLED"
        ),
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def document_text(result: dict[str, Any]) -> str:
    summary = result["summary"]
    confirmatory = result["checkpoint_5176_confirmatory_result"]
    return f"""# 5177 - Locked ensemble metric split and no-retuning theorem

Marker: `{MARKER}`.

Date: {CHECKED_DATE}.

## Question and discipline

Checkpoint 5176 completed its frozen twelve-seed comparison with a significant
MTS-directed q-band-distance component but no RMSE or joint-win preference.
This checkpoint does not retune either model and does not run another
trajectory. It reconstructs all 24 scored profiles from the frozen phase and
evolution caches, reproduces every recorded q and RMSE, and asks what the split
means mathematically.

All diagnostics below are post hoc unless they quote checkpoint 5176's locked
confirmatory result. They cannot be used to promote the 5176 outcome.

## Two different estimands

The q statistic is a five-point local logarithmic slope around
`R_tr={summary['transition_radius_kpc']} kpc`:

```text
q[V^2] = 2 d ln(V^2) / d ln R.
```

Its exact stencil is
`[{summary['q_stencil_min_radius_kpc']},
{summary['q_stencil_max_radius_kpc']}] kpc`.
The RMSE instead uses {summary['score_count']} scored radii:

```text
e_i = log10(V_i^2/V_target,i^2),
RMSE^2 = mean_i(e_i^2).
```

Checkpoint 5176's immutable result remains:

```text
mean D_q = {confirmatory['q_statistics']['mean']};
bootstrap95 D_q =
  [{confirmatory['q_statistics']['bootstrap_95_lower']},
   {confirmatory['q_statistics']['bootstrap_95_upper']}];
exact sign-flip p(D_q) =
  {confirmatory['q_statistics']['exact_two_sided_sign_flip_p']};

mean D_RMSE = {confirmatory['RMSE_statistics']['mean']} dex;
bootstrap95 D_RMSE =
  [{confirmatory['RMSE_statistics']['bootstrap_95_lower']},
   {confirmatory['RMSE_statistics']['bootstrap_95_upper']}] dex;
exact sign-flip p(D_RMSE) =
  {confirmatory['RMSE_statistics']['exact_two_sided_sign_flip_p']};

MTS joint wins = {confirmatory['MTS_joint_wins']};
CDM joint wins = {confirmatory['CDM_joint_wins']};
joint sign p = {confirmatory['joint_exact_two_sided_sign_p']}.
```

The frozen verdict is therefore
`{confirmatory['verdict']}`.

## Exact amplitude-shape decomposition

For a positive constant normalization `A`,

```text
e_i(A) = e_i + log10(A),
q[A V^2] = q[V^2],
A_best = 10^(-mean e),
min_A RMSE^2 = Var(e).
```

Thus a constant source or gravity normalization cannot alter q. The
reconstruction verifies this for all 24 profiles with maximum numerical error
`{summary['constant_amplitude_q_maximum_error']}`.

Across the twelve paired seeds,

```text
mean MTS log residual = {summary['mean_MTS_log_residual_dex']} dex;
mean CDM log residual = {summary['mean_CDM_log_residual_dex']} dex;

mean MTS centered-shape RMSE =
  {summary['mean_MTS_centered_shape_RMSE_dex']} dex;
mean CDM centered-shape RMSE =
  {summary['mean_CDM_centered_shape_RMSE_dex']} dex;

mean Delta MSE(MTS-CDM) = {summary['mean_delta_MSE_dex2']} dex^2
  = Delta bias^2 {summary['mean_delta_bias_squared_dex2']}
  + Delta centered variance {summary['mean_delta_centered_variance_dex2']}.
```

The bias-squared contribution is
`{summary['bias_fraction_of_mean_delta_MSE']}` of the mean MSE difference and
the centered-shape contribution is
`{summary['shape_fraction_of_mean_delta_MSE']}`. Even after granting each
profile its own post-hoc best normalization, MTS has no mean centered-shape
advantage. This diagnostic normalization is not a permitted fit.

The radial identity is also exact:

```text
inner-of-stencil contribution =
  {summary['mean_inner_delta_MSE_contribution_dex2']};
q-stencil contribution =
  {summary['mean_q_stencil_delta_MSE_contribution_dex2']};
outer-of-stencil contribution =
  {summary['mean_outer_delta_MSE_contribution_dex2']};
sum = {summary['mean_delta_MSE_dex2']}.
```

The q advantage is therefore a local slope result, not evidence that the
global profile amplitude or centered shape is already solved.

## Constant-coupling no-go survives the ensemble

Let `T` be the transition velocity-squared ratio and `E` the edge mass ratio.
A constant normalization that matches the transition requires `A_tr=1/T`;
one that matches the edge requires `A_edge=1/E`. Across all 24 profiles,

```text
A_tr range =
  [{summary['minimum_transition_amplitude']},
   {summary['maximum_transition_amplitude']}];
A_edge range =
  [{summary['minimum_edge_amplitude']},
   {summary['maximum_edge_amplitude']}].
```

These ranges are disjoint. For every profile the best log-minimax compromise

```text
A_2anchor = 1/sqrt(T E)
```

still leaves an unavoidable multiplicative mismatch
`sqrt(E/T)` in
`[{summary['minimum_two_anchor_mismatch_factor']},
  {summary['maximum_two_anchor_mismatch_factor']}]`.

Checkpoint 4960 independently fixes the same `G_N=1/(8 pi M_R^2)` in the
Einstein, Poisson, Newton, lensing and matter-source residues and forbids
arena retuning. Checkpoint 5170 already rejected a constant source multiplier
for the earlier formation state. The completed stochastic ensemble strengthens
that result: changing a universal coupling cannot explain the q signal, and a
galaxy-only amplitude fit would both conflict with local calibration and fail
the transition/edge shape test.

## Consequence

The result does not identify a new free coupling. It excludes that shortcut.
The surviving mechanism must be nonmultiplicative and parent-derived: a
conserved, compensated, scale-dependent occupied-state or motion-sector stress
that changes radial structure while remaining silent on the checkpoint-4960
local GR/Newton/Maxwell branch. The classical Vlasov density response rejected
at checkpoint 5171 may not be added again.

Route decision:
`{ROUTE_DECISION}`.

The next theory calculation must return to the parent motion-sector
Hessian/current and derive such an operator, or prove that the current
occupied-state branch cannot supply one. Only after that derivation may a new
cross-galaxy discrimination gate be preregistered. No parameter may be fitted
to this UGC09133 residual.

## Audit

All `{result['validation_count']}/{result['validation_count']}` validations
pass. The 5176 tree is unchanged at
`{result['checkpoint_5176_tree_sha256']}`. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. Every new row remains
`valid_for_claim=false`, and no GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()

    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(json.dumps(missing, indent=2))
    source_hashes_before = {
        key: file_digest(path) for key, path in paths.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_tree_before = tree_digest(CHECKPOINT_5176_ROOT)
    runner = load_runner()
    common = runner.common_context()
    base = common["base_context"]
    radii = np.asarray(base["radii"], dtype=float)
    target_velocity_squared = np.asarray(base["target_velocity"], dtype=float)
    transition_radius = float(base["transition_radius"])

    protocol = json.loads(
        CHECKPOINT_5176_PROTOCOL.read_text(encoding="utf-8")
    )
    aggregate = json.loads(
        CHECKPOINT_5176_RESULT.read_text(encoding="utf-8")
    )
    freeze = json.loads(
        CHECKPOINT_5176_FREEZE.read_text(encoding="utf-8")
    )
    checkpoint_5170 = json.loads(
        CHECKPOINT_5170_RESULT.read_text(encoding="utf-8")
    )
    schedule = read_csv(CHECKPOINT_5176_SCHEDULE)
    previous_validations = read_csv(CHECKPOINT_5176_VALIDATION)
    calibration_rows = read_csv(CHECKPOINT_4960_CALIBRATIONS)
    gn_calibration = next(
        row
        for row in calibration_rows
        if row.get("source_row_id") == "CAL4947_00_GN"
    )

    seed_rows: list[dict[str, Any]] = []
    normalization_rows: list[dict[str, Any]] = []
    radial_profile_rows: list[dict[str, Any]] = []
    radial_contribution_rows: list[dict[str, Any]] = []
    score_q_errors: list[float] = []
    score_rmse_errors: list[float] = []
    result_hash_checks: list[bool] = []
    decomposition_errors: list[float] = []
    radial_errors: list[float] = []
    q_invariance_errors: list[float] = []

    for schedule_row in schedule:
        seed_index = int(schedule_row["seed_index"])
        high_mode_seed = int(schedule_row["high_mode_seed"])
        seed_dir = (
            CHECKPOINT_5176_ROOT
            / "seeds"
            / f"seed_{seed_index:02d}_{high_mode_seed}"
        )
        seed_result_path = seed_dir / "seed_result.json"
        seed_status_path = seed_dir / "status.json"
        complete_marker_path = seed_dir / "COMPLETE.marker"
        seed_result = json.loads(seed_result_path.read_text(encoding="utf-8"))
        seed_status = json.loads(seed_status_path.read_text(encoding="utf-8"))
        result_hash_checks.append(
            seed_status["state"] == "COMPLETE"
            and file_digest(seed_result_path) == seed_status["result_sha256"]
            and f"result_sha256={seed_status['result_sha256']}"
            in complete_marker_path.read_text(encoding="utf-8")
        )
        recorded_scores = {
            row["model"]: row for row in read_csv(seed_dir / "forward_scores.csv")
        }
        by_model: dict[str, dict[str, Any]] = {}
        for short_model, family_id, recorded_model in MODEL_FAMILIES:
            diagnostics, profile_rows = reconstruct_model(
                runner,
                base,
                seed_dir,
                seed_index,
                high_mode_seed,
                short_model,
                family_id,
                recorded_model,
            )
            recorded = recorded_scores[recorded_model]
            score_q_errors.append(
                abs(float(diagnostics["q"]) - float(recorded["forward_q"]))
            )
            score_rmse_errors.append(
                abs(
                    float(diagnostics["RMSE_dex"])
                    - float(recorded["forward_RMSE_dex"])
                )
            )
            q_invariance_errors.append(
                float(diagnostics["constant_amplitude_q_maximum_error"])
            )
            by_model[short_model] = diagnostics
            normalization_rows.append(public_diagnostics(diagnostics))
            radial_profile_rows.extend(profile_rows)

        mts = by_model["MTS"]
        cdm = by_model["CDM"]
        if not np.array_equal(mts["_score_valid"], cdm["_score_valid"]):
            raise RuntimeError(f"score masks differ at seed {seed_index}")
        if not np.array_equal(mts["_q_stencil"], cdm["_q_stencil"]):
            raise RuntimeError(f"q stencils differ at seed {seed_index}")
        score_indices = np.flatnonzero(mts["_score_valid"])
        q_stencil = mts["_q_stencil"]
        q_lower_index = int(q_stencil[0])
        q_upper_index = int(q_stencil[-1])
        paired_delta_mse = (
            float(mts["RMSE_dex"]) ** 2 - float(cdm["RMSE_dex"]) ** 2
        )
        delta_bias_squared = (
            float(mts["mean_log10_residual_dex"]) ** 2
            - float(cdm["mean_log10_residual_dex"]) ** 2
        )
        delta_centered_variance = (
            float(mts["centered_shape_variance_dex2"])
            - float(cdm["centered_shape_variance_dex2"])
        )
        decomposition_error = abs(
            paired_delta_mse
            - delta_bias_squared
            - delta_centered_variance
        )
        decomposition_errors.append(decomposition_error)
        zone_contributions = {
            "INNER_OF_Q_STENCIL": 0.0,
            "Q_STENCIL": 0.0,
            "OUTER_OF_Q_STENCIL": 0.0,
        }
        for radius_index in score_indices:
            if radius_index < q_lower_index:
                zone = "INNER_OF_Q_STENCIL"
            elif radius_index <= q_upper_index:
                zone = "Q_STENCIL"
            else:
                zone = "OUTER_OF_Q_STENCIL"
            mts_residual = float(mts["_log_residual"][radius_index])
            cdm_residual = float(cdm["_log_residual"][radius_index])
            paired_squared_difference = (
                mts_residual**2 - cdm_residual**2
            )
            contribution = paired_squared_difference / len(score_indices)
            zone_contributions[zone] += contribution
            radial_contribution_rows.append(
                {
                    "seed_index": seed_index,
                    "high_mode_seed": high_mode_seed,
                    "radius_index": int(radius_index),
                    "radius_kpc": float(radii[radius_index]),
                    "radius_over_transition": float(
                        radii[radius_index] / transition_radius
                    ),
                    "zone": zone,
                    "MTS_log_residual_dex": mts_residual,
                    "CDM_log_residual_dex": cdm_residual,
                    "paired_squared_residual_difference_dex2": (
                        paired_squared_difference
                    ),
                    "contribution_to_global_paired_delta_MSE_dex2": (
                        contribution
                    ),
                    "target_used_only_for_post_evolution_scoring": True,
                    "target_used_to_define_evolution": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        radial_error = abs(
            paired_delta_mse - sum(zone_contributions.values())
        )
        radial_errors.append(radial_error)
        seed_rows.append(
            {
                "seed_index": seed_index,
                "high_mode_seed": high_mode_seed,
                "D_q_band_distance_MTS_minus_CDM": float(
                    seed_result["D_q_MTS_minus_CDM_band_distance"]
                ),
                "D_RMSE_MTS_minus_CDM_dex": (
                    float(mts["RMSE_dex"]) - float(cdm["RMSE_dex"])
                ),
                "D_MSE_MTS_minus_CDM_dex2": paired_delta_mse,
                "D_bias_squared_MTS_minus_CDM_dex2": delta_bias_squared,
                "D_centered_variance_MTS_minus_CDM_dex2": (
                    delta_centered_variance
                ),
                "D_centered_shape_RMSE_MTS_minus_CDM_dex": (
                    float(mts["centered_shape_RMSE_dex"])
                    - float(cdm["centered_shape_RMSE_dex"])
                ),
                "D_mean_log_residual_MTS_minus_CDM_dex": (
                    float(mts["mean_log10_residual_dex"])
                    - float(cdm["mean_log10_residual_dex"])
                ),
                "D_transition_ratio_MTS_minus_CDM": (
                    float(mts["transition_velocity_squared_ratio_to_target"])
                    - float(cdm["transition_velocity_squared_ratio_to_target"])
                ),
                "D_edge_ratio_MTS_minus_CDM": (
                    float(mts["edge_mass_ratio_to_target"])
                    - float(cdm["edge_mass_ratio_to_target"])
                ),
                "inner_delta_MSE_contribution_dex2": zone_contributions[
                    "INNER_OF_Q_STENCIL"
                ],
                "q_stencil_delta_MSE_contribution_dex2": (
                    zone_contributions["Q_STENCIL"]
                ),
                "outer_delta_MSE_contribution_dex2": zone_contributions[
                    "OUTER_OF_Q_STENCIL"
                ],
                "MTS_RMSE_dex": float(mts["RMSE_dex"]),
                "CDM_RMSE_dex": float(cdm["RMSE_dex"]),
                "MTS_mean_log_residual_dex": float(
                    mts["mean_log10_residual_dex"]
                ),
                "CDM_mean_log_residual_dex": float(
                    cdm["mean_log10_residual_dex"]
                ),
                "MTS_centered_shape_RMSE_dex": float(
                    mts["centered_shape_RMSE_dex"]
                ),
                "CDM_centered_shape_RMSE_dex": float(
                    cdm["centered_shape_RMSE_dex"]
                ),
                "MTS_transition_ratio": float(
                    mts["transition_velocity_squared_ratio_to_target"]
                ),
                "CDM_transition_ratio": float(
                    cdm["transition_velocity_squared_ratio_to_target"]
                ),
                "MTS_edge_ratio": float(mts["edge_mass_ratio_to_target"]),
                "CDM_edge_ratio": float(cdm["edge_mass_ratio_to_target"]),
                "decomposition_identity_error": decomposition_error,
                "radial_partition_identity_error": radial_error,
                "target_used_only_for_post_evolution_scoring": True,
                "target_used_to_define_evolution": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    descriptive_specs = (
        (
            "D_MSE_MTS_minus_CDM",
            "RMSE_MTS^2-RMSE_CDM^2",
            "D_MSE_MTS_minus_CDM_dex2",
            "dex^2",
            "negative favors MTS",
        ),
        (
            "D_bias_squared_MTS_minus_CDM",
            "mean(e_MTS)^2-mean(e_CDM)^2",
            "D_bias_squared_MTS_minus_CDM_dex2",
            "dex^2",
            "negative favors MTS",
        ),
        (
            "D_centered_variance_MTS_minus_CDM",
            "Var(e_MTS)-Var(e_CDM)",
            "D_centered_variance_MTS_minus_CDM_dex2",
            "dex^2",
            "negative favors MTS",
        ),
        (
            "D_centered_shape_RMSE_MTS_minus_CDM",
            "sqrt(Var(e_MTS))-sqrt(Var(e_CDM))",
            "D_centered_shape_RMSE_MTS_minus_CDM_dex",
            "dex",
            "negative favors MTS",
        ),
        (
            "D_mean_log_residual_MTS_minus_CDM",
            "mean(e_MTS)-mean(e_CDM)",
            "D_mean_log_residual_MTS_minus_CDM_dex",
            "dex",
            "zero means equal multiplicative bias",
        ),
        (
            "D_transition_ratio_MTS_minus_CDM",
            "T_MTS-T_CDM",
            "D_transition_ratio_MTS_minus_CDM",
            "dimensionless",
            "positive is closer to unity for this underpredicted ensemble",
        ),
        (
            "D_edge_ratio_MTS_minus_CDM",
            "E_MTS-E_CDM",
            "D_edge_ratio_MTS_minus_CDM",
            "dimensionless",
            "negative is closer to unity for this overpredicted ensemble",
        ),
        (
            "inner_delta_MSE_contribution",
            "inner radial contribution to paired global Delta MSE",
            "inner_delta_MSE_contribution_dex2",
            "dex^2",
            "negative favors MTS",
        ),
        (
            "q_stencil_delta_MSE_contribution",
            "q-stencil radial contribution to paired global Delta MSE",
            "q_stencil_delta_MSE_contribution_dex2",
            "dex^2",
            "negative favors MTS",
        ),
        (
            "outer_delta_MSE_contribution",
            "outer radial contribution to paired global Delta MSE",
            "outer_delta_MSE_contribution_dex2",
            "dex^2",
            "negative favors MTS",
        ),
    )
    descriptive_rows = [
        descriptive_row(
            metric_id,
            definition,
            [float(row[field]) for row in seed_rows],
            offset,
            units,
            sign_convention,
        )
        for offset, (
            metric_id,
            definition,
            field,
            units,
            sign_convention,
        ) in enumerate(descriptive_specs, start=1)
    ]

    def seed_mean(field: str) -> float:
        return float(np.mean([float(row[field]) for row in seed_rows]))

    mts_normalizations = [
        row for row in normalization_rows if row["model"] == "MTS"
    ]
    cdm_normalizations = [
        row for row in normalization_rows if row["model"] == "CDM"
    ]
    transition_amplitudes = [
        float(row["amplitude_required_at_transition"])
        for row in normalization_rows
    ]
    edge_amplitudes = [
        float(row["amplitude_required_at_edge"])
        for row in normalization_rows
    ]
    mismatch_factors = [
        float(row["two_anchor_unavoidable_mismatch_factor"])
        for row in normalization_rows
    ]
    mean_delta_mse = seed_mean("D_MSE_MTS_minus_CDM_dex2")
    mean_delta_bias_squared = seed_mean(
        "D_bias_squared_MTS_minus_CDM_dex2"
    )
    mean_delta_centered_variance = seed_mean(
        "D_centered_variance_MTS_minus_CDM_dex2"
    )
    summary = {
        "transition_radius_kpc": transition_radius,
        "q_stencil_min_radius_kpc": float(
            normalization_rows[0]["q_stencil_min_radius_kpc"]
        ),
        "q_stencil_max_radius_kpc": float(
            normalization_rows[0]["q_stencil_max_radius_kpc"]
        ),
        "q_stencil_count": int(normalization_rows[0]["q_stencil_count"]),
        "score_count": int(normalization_rows[0]["score_count"]),
        "mean_MTS_RMSE_dex": seed_mean("MTS_RMSE_dex"),
        "mean_CDM_RMSE_dex": seed_mean("CDM_RMSE_dex"),
        "mean_D_RMSE_MTS_minus_CDM_dex": seed_mean(
            "D_RMSE_MTS_minus_CDM_dex"
        ),
        "MTS_RMSE_wins": sum(
            float(row["D_RMSE_MTS_minus_CDM_dex"]) < 0.0
            for row in seed_rows
        ),
        "CDM_RMSE_wins": sum(
            float(row["D_RMSE_MTS_minus_CDM_dex"]) > 0.0
            for row in seed_rows
        ),
        "mean_MTS_log_residual_dex": seed_mean(
            "MTS_mean_log_residual_dex"
        ),
        "mean_CDM_log_residual_dex": seed_mean(
            "CDM_mean_log_residual_dex"
        ),
        "ensemble_best_MTS_post_hoc_amplitude": 10.0
        ** (-seed_mean("MTS_mean_log_residual_dex")),
        "ensemble_best_CDM_post_hoc_amplitude": 10.0
        ** (-seed_mean("CDM_mean_log_residual_dex")),
        "mean_MTS_centered_shape_RMSE_dex": seed_mean(
            "MTS_centered_shape_RMSE_dex"
        ),
        "mean_CDM_centered_shape_RMSE_dex": seed_mean(
            "CDM_centered_shape_RMSE_dex"
        ),
        "mean_D_centered_shape_RMSE_MTS_minus_CDM_dex": seed_mean(
            "D_centered_shape_RMSE_MTS_minus_CDM_dex"
        ),
        "mean_delta_MSE_dex2": mean_delta_mse,
        "mean_delta_bias_squared_dex2": mean_delta_bias_squared,
        "mean_delta_centered_variance_dex2": (
            mean_delta_centered_variance
        ),
        "bias_fraction_of_mean_delta_MSE": (
            mean_delta_bias_squared / mean_delta_mse
        ),
        "shape_fraction_of_mean_delta_MSE": (
            mean_delta_centered_variance / mean_delta_mse
        ),
        "mean_inner_delta_MSE_contribution_dex2": seed_mean(
            "inner_delta_MSE_contribution_dex2"
        ),
        "mean_q_stencil_delta_MSE_contribution_dex2": seed_mean(
            "q_stencil_delta_MSE_contribution_dex2"
        ),
        "mean_outer_delta_MSE_contribution_dex2": seed_mean(
            "outer_delta_MSE_contribution_dex2"
        ),
        "minimum_transition_amplitude": min(transition_amplitudes),
        "maximum_transition_amplitude": max(transition_amplitudes),
        "minimum_edge_amplitude": min(edge_amplitudes),
        "maximum_edge_amplitude": max(edge_amplitudes),
        "normalization_anchor_ranges_disjoint": (
            max(edge_amplitudes) < min(transition_amplitudes)
        ),
        "minimum_two_anchor_mismatch_factor": min(mismatch_factors),
        "maximum_two_anchor_mismatch_factor": max(mismatch_factors),
        "mean_two_anchor_mismatch_factor": float(
            np.mean(mismatch_factors)
        ),
        "mean_MTS_transition_ratio": float(
            np.mean(
                [
                    float(
                        row[
                            "transition_velocity_squared_ratio_to_target"
                        ]
                    )
                    for row in mts_normalizations
                ]
            )
        ),
        "mean_CDM_transition_ratio": float(
            np.mean(
                [
                    float(
                        row[
                            "transition_velocity_squared_ratio_to_target"
                        ]
                    )
                    for row in cdm_normalizations
                ]
            )
        ),
        "mean_MTS_edge_ratio": float(
            np.mean(
                [
                    float(row["edge_mass_ratio_to_target"])
                    for row in mts_normalizations
                ]
            )
        ),
        "mean_CDM_edge_ratio": float(
            np.mean(
                [
                    float(row["edge_mass_ratio_to_target"])
                    for row in cdm_normalizations
                ]
            )
        ),
        "constant_amplitude_q_maximum_error": max(q_invariance_errors),
        "maximum_score_q_reconstruction_error": max(score_q_errors),
        "maximum_score_RMSE_reconstruction_error": max(
            score_rmse_errors
        ),
        "maximum_MSE_decomposition_error": max(decomposition_errors),
        "maximum_radial_partition_error": max(radial_errors),
        "route_decision": ROUTE_DECISION,
        "valid_for_claim": False,
    }
    summary_rows = [
        summary_row(
            "transition_radius",
            summary["transition_radius_kpc"],
            "kpc",
            "fixed parent transition radius",
        ),
        summary_row(
            "q_stencil_radius_range",
            (
                f"[{summary['q_stencil_min_radius_kpc']},"
                f"{summary['q_stencil_max_radius_kpc']}]"
            ),
            "kpc",
            "five-point local slope stencil",
        ),
        summary_row(
            "mean_D_RMSE",
            summary["mean_D_RMSE_MTS_minus_CDM_dex"],
            "dex",
            "locked paired mean; positive favors CDM",
        ),
        summary_row(
            "mean_D_MSE",
            summary["mean_delta_MSE_dex2"],
            "dex^2",
            "exact amplitude-shape decomposition target",
        ),
        summary_row(
            "mean_D_bias_squared",
            summary["mean_delta_bias_squared_dex2"],
            "dex^2",
            "multiplicative-amplitude contribution",
        ),
        summary_row(
            "mean_D_centered_variance",
            summary["mean_delta_centered_variance_dex2"],
            "dex^2",
            "amplitude-free centered-shape contribution",
        ),
        summary_row(
            "transition_amplitude_range",
            (
                f"[{summary['minimum_transition_amplitude']},"
                f"{summary['maximum_transition_amplitude']}]"
            ),
            "dimensionless",
            "constant A required to match transition",
        ),
        summary_row(
            "edge_amplitude_range",
            (
                f"[{summary['minimum_edge_amplitude']},"
                f"{summary['maximum_edge_amplitude']}]"
            ),
            "dimensionless",
            "constant A required to match edge",
        ),
        summary_row(
            "anchor_ranges_disjoint",
            summary["normalization_anchor_ranges_disjoint"],
            "boolean",
            "no constant A can match both transition and edge",
        ),
        summary_row(
            "route_decision",
            ROUTE_DECISION,
            "token",
            "return to parent-derived nonmultiplicative stress",
        ),
    ]
    decision_rows = [
        {
            "route_decision": ROUTE_DECISION,
            "checkpoint_5176_verdict_preserved": aggregate["verdict"],
            "constant_source_normalization_rejected": True,
            "calibrated_GN_retained": True,
            "parent_nonmultiplicative_state_stress_derived": False,
            "next_target": (
                "derive_or_reject_parent_motion_Hessian_current_occupied_state_"
                "stress_with_conservation_compensation_and_local_vacuum_silence"
            ),
            "new_cross_galaxy_gate_allowed_now": False,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance_rows = [
        {
            "source_id": key,
            "local_path": str(path),
            "path_type": "file",
            "sha256": source_hashes_before[key],
            "role": "read_only_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    provenance_rows.append(
        {
            "source_id": "checkpoint_5176_complete_output_tree",
            "local_path": str(CHECKPOINT_5176_ROOT),
            "path_type": "directory_tree",
            "sha256": checkpoint_5176_tree_before,
            "role": "read_only_frozen_cache_and_result_source",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )

    source_hashes_after = {
        key: file_digest(path) for key, path in paths.items()
    }
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_tree_after = tree_digest(CHECKPOINT_5176_ROOT)
    freeze_checks = {
        "runner_script_sha256": file_digest(CHECKPOINT_5176_RUNNER)
        == freeze["runner_script_sha256"],
        "protocol_file_sha256": file_digest(CHECKPOINT_5176_PROTOCOL)
        == freeze["protocol_file_sha256"],
        "schedule_file_sha256": file_digest(CHECKPOINT_5176_SCHEDULE)
        == freeze["schedule_file_sha256"],
        "source_provenance_sha256": file_digest(
            CHECKPOINT_5176_ROOT / "source_provenance.csv"
        )
        == freeze["source_provenance_sha256"],
        "first_seed_result_sha256": file_digest(
            CHECKPOINT_5176_ROOT
            / "seeds"
            / "seed_01_3240854344"
            / "seed_result.json"
        )
        == freeze["first_seed_result_sha256"],
    }

    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    add_validation(
        validation,
        "source_hashes_unchanged",
        source_hashes_before == source_hashes_after,
        source_hashes_after,
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_before == formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "checkpoint_5176_tree_read_only",
        checkpoint_5176_tree_before == checkpoint_5176_tree_after,
        checkpoint_5176_tree_after,
    )
    add_validation(
        validation,
        "checkpoint_5176_protocol_hash_preserved",
        protocol["protocol_sha256"] == PROTOCOL_SHA256
        and aggregate["protocol_sha256"] == PROTOCOL_SHA256,
        PROTOCOL_SHA256,
    )
    add_validation(
        validation,
        "checkpoint_5176_final_verdict_preserved",
        aggregate["completed_confirmatory_seeds"] == 12
        and aggregate["verdict"]
        == "STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE",
        aggregate["verdict"],
    )
    add_validation(
        validation,
        "schedule_complete_unique_and_ordered",
        [int(row["seed_index"]) for row in schedule] == list(range(1, 13))
        and len(
            {int(row["high_mode_seed"]) for row in schedule}
        )
        == 12,
        [
            (int(row["seed_index"]), int(row["high_mode_seed"]))
            for row in schedule
        ],
    )
    add_validation(
        validation,
        "all_seed_result_hashes_and_markers_match",
        all(result_hash_checks),
        result_hash_checks,
    )
    add_validation(
        validation,
        "checkpoint_5176_validation_still_passes",
        len(previous_validations) == 12
        and all(row["passed"].lower() == "true" for row in previous_validations),
        len(previous_validations),
    )
    add_validation(
        validation,
        "all_five_freeze_hashes_reproduce",
        all(freeze_checks.values()),
        freeze_checks,
    )
    add_validation(
        validation,
        "all_24_q_scores_reconstructed",
        len(score_q_errors) == 24 and max(score_q_errors) < 1.0e-12,
        max(score_q_errors),
    )
    add_validation(
        validation,
        "all_24_RMSE_scores_reconstructed",
        len(score_rmse_errors) == 24
        and max(score_rmse_errors) < 1.0e-12,
        max(score_rmse_errors),
    )
    add_validation(
        validation,
        "constant_amplitude_q_invariance",
        max(q_invariance_errors) < 1.0e-12,
        max(q_invariance_errors),
    )
    add_validation(
        validation,
        "MSE_bias_variance_identity",
        max(decomposition_errors) < 1.0e-14,
        max(decomposition_errors),
    )
    add_validation(
        validation,
        "radial_MSE_partition_identity",
        max(radial_errors) < 1.0e-14,
        max(radial_errors),
    )
    add_validation(
        validation,
        "fixed_five_point_q_stencil",
        all(int(row["q_stencil_count"]) == 5 for row in normalization_rows),
        {
            "minimum_kpc": summary["q_stencil_min_radius_kpc"],
            "maximum_kpc": summary["q_stencil_max_radius_kpc"],
        },
    )
    add_validation(
        validation,
        "positive_target_inside_score_mask",
        bool(
            np.all(
                target_velocity_squared[
                    np.asarray(base["score_mask"], dtype=bool)
                ]
                > 0.0
            )
        ),
        summary["score_count"],
    )
    add_validation(
        validation,
        "transition_and_edge_normalizations_disjoint",
        summary["normalization_anchor_ranges_disjoint"],
        {
            "transition": [
                summary["minimum_transition_amplitude"],
                summary["maximum_transition_amplitude"],
            ],
            "edge": [
                summary["minimum_edge_amplitude"],
                summary["maximum_edge_amplitude"],
            ],
        },
    )
    add_validation(
        validation,
        "checkpoint_4960_GN_is_single_and_not_arena_retunable",
        gn_calibration["status"] == "MEASURED_ONCE_NOT_PREDICTED"
        and gn_calibration["arena_retuning_allowed"].lower() == "false",
        gn_calibration,
    )
    add_validation(
        validation,
        "checkpoint_5170_constant_coupling_no_go_inherited",
        checkpoint_5170["constant_source_coupling_rejected_as_shape_repair"]
        is True,
        checkpoint_5170["route_decision"],
    )
    generated_rows = (
        seed_rows
        + normalization_rows
        + radial_profile_rows
        + radial_contribution_rows
        + descriptive_rows
        + summary_rows
        + provenance_rows
        + decision_rows
    )
    add_validation(
        validation,
        "all_generated_rows_nonclaim",
        all(row.get("valid_for_claim") is False for row in generated_rows),
        len(generated_rows),
    )
    add_validation(
        validation,
        "target_not_used_to_define_evolution",
        all(
            row.get("target_used_to_define_evolution") is False
            for row in (
                seed_rows
                + normalization_rows
                + radial_profile_rows
                + radial_contribution_rows
                + decision_rows
            )
        ),
        "target enters only inherited post-evolution score",
    )
    failures = [row for row in validation if not row["passed"]]
    result = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "checkpoint_5176_confirmatory_result": aggregate,
        "summary": summary,
        "route_decision": ROUTE_DECISION,
        "constant_source_normalization_rejected": True,
        "calibrated_GN_retained": True,
        "parent_nonmultiplicative_state_stress_derived": False,
        "checkpoint_5176_tree_sha256": checkpoint_5176_tree_after,
        "formalization_workbench_tree_sha256": formal_after,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "validation_count": len(validation),
        "validation_failures": failures,
        "valid_for_claim": False,
    }

    if arguments.dry_run:
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
        if failures:
            raise RuntimeError(json.dumps(failures, indent=2))
        return

    write_csv(SEED_DIAGNOSTICS_CSV, seed_rows)
    write_csv(NORMALIZATION_CSV, normalization_rows)
    write_csv(RADIAL_PROFILE_CSV, radial_profile_rows)
    write_csv(RADIAL_CONTRIBUTION_CSV, radial_contribution_rows)
    write_csv(DESCRIPTIVE_STATISTICS_CSV, descriptive_rows)
    write_csv(SUMMARY_CSV, summary_rows)
    write_csv(PROVENANCE_CSV, provenance_rows)
    write_csv(DECISION_CSV, decision_rows)
    write_csv(VALIDATION_CSV, validation)
    write_json(RESULT_JSON, result)
    DOCUMENT.write_text(document_text(result), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if failures:
        raise RuntimeError(json.dumps(failures, indent=2))


if __name__ == "__main__":
    main()
