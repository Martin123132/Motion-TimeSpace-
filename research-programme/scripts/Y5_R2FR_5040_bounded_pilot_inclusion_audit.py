from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import t


POST = Path(__file__).resolve().parents[1]
RUNNER = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5040"
RUN = SOURCE / "runs" / "nested_sobol_power1_s4_v1"
RESIDUE_DIAGNOSTIC = SOURCE / "cross_source_residue_diagnostic.json"
OUTPUT = SOURCE / "bounded_pilot_inclusion_audit.json"
OUTPUT_CSV = SOURCE / "bounded_pilot_design_comparison.csv"
MARKER = "MTS_5040_BOUNDED_PILOT_INCLUSION_AUDIT"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_bounded_pilot", RUNNER)
M5036 = M5040.M5036


def finite_job(job: dict[str, Any]) -> bool:
    value = job.get("normalized_direct_D_hhh_over_G3")
    return (
        job.get("status") in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
        or (
            job.get("status") == "COMPLETED_UNCONVERGED"
            and job.get("topology_passed")
            and job.get("integral_converged") is False
        )
    ) and isinstance(value, dict) and all(
        math.isfinite(float(value[key])) for key in ("real", "imaginary")
    )


def main() -> None:
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    status = json.loads((RUN / "status.json").read_text(encoding="utf-8"))
    jobs = M5036.load_jobs(RUN)
    residue = json.loads(RESIDUE_DIAGNOSTIC.read_text(encoding="utf-8"))
    if status["unconverged_jobs"] != 8 or residue["candidate_count"] != 8:
        raise RuntimeError("bounded pilot expects the current eight-row obstruction")
    original_numeric_job = M5036.numeric_job
    M5036.numeric_job = finite_job
    try:
        _, lookup = M5036.cyclic_seed_vectors(config, jobs)
    finally:
        M5036.numeric_job = original_numeric_job
    vectors = {
        (int(seed), str(epsilon_id)): np.asarray(vector, dtype=np.complex128)
        for (tier, epsilon_id, seed), vector in lookup.items()
        if tier == "primary24"
    }
    bounded_seeds = [
        int(seed)
        for seed in config["seeds"]
        if all((int(seed), epsilon_id) in vectors for epsilon_id in M5040.EPSILON_IDS)
    ]
    if bounded_seeds != [503401, 503402, 503403]:
        raise RuntimeError(f"unexpected bounded seed set: {bounded_seeds}")
    ladder = M5040.projected_ladder(vectors, bounded_seeds)
    source_result = json.loads(M5040.SOURCE_5037_RESULT.read_text(encoding="utf-8"))
    source_vectors = M5040.complete_vectors(source_result)
    source_ladder = M5040.projected_ladder(source_vectors, list(M5040.SEEDS))
    budgets = M5040.target_budget_rows()
    empirical_kernel_envelope = float(residue["maximum_empirical_cyclic_impact"])
    conservative_vector_envelope = 10.0 * empirical_kernel_envelope
    rows = []
    for component_index, budget in enumerate(budgets):
        source_values = source_ladder["richardson"][:, component_index].real
        bounded_values = ladder["richardson"][:, component_index].real
        source_sd = float(np.std(source_values, ddof=1))
        bounded_sd = float(np.std(bounded_values, ddof=1))
        bounded_halfwidth = float(t.ppf(0.975, 2) * bounded_sd / math.sqrt(3.0))
        independent_halfwidth = float(t.ppf(0.975, 7) * source_sd / math.sqrt(8.0))
        rows.append(
            {
                "component_index": component_index,
                "physical_s_channel_cosine": budget["physical_s_channel_cosine"],
                "target_equivalence_margin": budget["target_equivalence_margin"],
                "sample0_sd": source_sd,
                "bounded_nested_sd_n3": bounded_sd,
                "bounded_nested_to_sample0_sd_ratio": bounded_sd / source_sd,
                "bounded_nested_95_halfwidth_n3": bounded_halfwidth,
                "expected_eight_independent_95_halfwidth": independent_halfwidth,
                "bounded_nested_to_independent_halfwidth_ratio": bounded_halfwidth
                / independent_halfwidth,
                "bounded_richardson_mean": float(np.mean(bounded_values)),
                "fixed_target": budget["fixed_target"],
                "conservative_unresolved_kernel_envelope": conservative_vector_envelope,
                "envelope_to_target_margin_ratio": conservative_vector_envelope
                / budget["target_equivalence_margin"],
                "valid_for_design_pilot": True,
                "valid_for_production_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    output = {
        "checkpoint_marker": MARKER,
        "bounded_nested_seeds": bounded_seeds,
        "unconverged_rows_included": 8,
        "inclusion_scope": "equal-cost variance-design pilot only",
        "maximum_empirical_single_kernel_cyclic_impact": empirical_kernel_envelope,
        "conservative_tenfold_vector_envelope": conservative_vector_envelope,
        "all_envelopes_below_one_part_in_100000_of_target_margin": all(
            row["envelope_to_target_margin_ratio"] < 1.0e-5 for row in rows
        ),
        "components_below_nested_sd_ratio_threshold": [
            row["component_index"]
            for row in rows
            if row["bounded_nested_to_sample0_sd_ratio"]
            < config["equal_cost_design_contract"][
                "nested_sd_ratio_required_to_beat_independent"
            ]
        ],
        "interpretation": (
            "The third nested point may inform the variance-design pilot because a tenfold "
            "inflation of its measured residue impact remains negligible against every source "
            "margin. It is not admitted to the production matrix and cannot close a claim gate."
        ),
        "rows": rows,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(OUTPUT, output)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(
        json.dumps(
            {
                "marker": MARKER,
                "bounded_seeds": bounded_seeds,
                "components_below_sd_threshold": output[
                    "components_below_nested_sd_ratio_threshold"
                ],
                "maximum_envelope_to_margin": max(
                    row["envelope_to_target_margin_ratio"] for row in rows
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
