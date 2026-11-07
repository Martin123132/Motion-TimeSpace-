from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import traceback

import numpy as np
import psutil

from ward_core import WardCandidate, ward_slice, tadpole_integrals


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/ward-validation"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite evidence.")
    OUTPUT.mkdir(parents=True)
    checks = []

    def close(name, actual, expected, relative=2e-7, absolute=1e-13):
        error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
        scale = float(max(np.max(np.abs(actual)), np.max(np.abs(expected))))
        budget = absolute + relative * scale
        assert error <= budget, (name, error, budget)
        checks.append({"name": name, "error": error, "budget": budget, "passed": True})

    fixtures = [(1.1, .25, .8, 2.), (1.1, .65, .3, 4.), (.4, -.7, 1.2, 3.)]
    hard_rows = []
    for regulator_scale in [None, 2., 4.]:
        model = WardCandidate(regulator_scale)
        for fixture in fixtures:
            coarse = ward_slice(model, *fixture, 48)
            fine = ward_slice(model, *fixture, 96)
            replay = ward_slice(model, *fixture, 128)
            tag = f"reg{regulator_scale}-fixture{fixture}"
            close(tag + "-Ward", replay["completed_vertex"], replay["direct_spatial_derivative"])
            close(tag + "-refinement", fine["direct_spatial_derivative"], replay["direct_spatial_derivative"])
            close(tag + "-routing-plus-surface",
                  replay["direct_spatial_derivative"] - replay["collapsed_parent_vertex"],
                  replay["routing_correction"] + replay["boundary"])
            omitted_surface_error = float(np.max(np.abs(replay["first_leg_half"] + replay["second_leg_half"]
                                                        - replay["direct_spatial_derivative"])))
            actual_error = float(np.max(np.abs(replay["completed_vertex"] - replay["direct_spatial_derivative"])))
            assert omitted_surface_error > 100 * actual_error + 1e-14
            hard_rows.append({"regulator_scale": regulator_scale, "fixture": fixture,
                              **{key: value.tolist() for key, value in replay.items()},
                              "omitted_surface_error": omitted_surface_error,
                              "completed_Ward_error": actual_error,
                              "coarse_to_fine_derivative_difference": float(np.max(np.abs(coarse["direct_spatial_derivative"] - fine["direct_spatial_derivative"])))})
    print(json.dumps({"stage": "hard_boundaries_complete", "fixtures": len(hard_rows)}), flush=True)

    infinite_rows = []
    for regulator_scale in [2., 4.]:
        model = WardCandidate(regulator_scale)
        for external, internal, momentum in [(1.1, .25, .8), (.7, .2, .3)]:
            first = ward_slice(model, external, internal, momentum, math.inf, 128)
            reflected = ward_slice(model, external, external - internal, momentum, math.inf, 128)
            coarse = ward_slice(model, external, internal, momentum, math.inf, 96)
            tag = f"infinite-reg{regulator_scale}-{external}-{internal}-{momentum}"
            close(tag + "-Ward", first["completed_vertex"], first["direct_spatial_derivative"], relative=2e-6)
            close(tag + "-refinement", first["direct_spatial_derivative"], coarse["direct_spatial_derivative"], relative=2e-6)
            close(tag + "-routing", first["first_leg_half"], reflected["second_leg_half"], relative=2e-6)
            close(tag + "-paired-collapse",
                  2 * (first["first_leg_half"] + reflected["first_leg_half"]),
                  first["direct_spatial_derivative"] + reflected["direct_spatial_derivative"], relative=2e-6)
            infinite_rows.append({"scale": regulator_scale, "external_frequency": external,
                                  "internal_frequency": internal, "momentum": momentum,
                                  "completed": first["completed_vertex"].tolist(),
                                  "direct": first["direct_spatial_derivative"].tolist(),
                                  "paired_collapse_error": float(np.max(np.abs(
                                      2 * (first["first_leg_half"] + reflected["first_leg_half"])
                                      - first["direct_spatial_derivative"] - reflected["direct_spatial_derivative"])))})
    print(json.dumps({"stage": "infinite_spatial_Ward_complete", "paired_fixtures": len(infinite_rows)}), flush=True)

    finite_variation_rows = []
    for regulator_scale in [2., 4.]:
        model = WardCandidate(regulator_scale)
        for frequency, momentum_squared, shear in [(.3, .7, .25), (2., 3., 1.2)]:
            propagator = model.propagator(frequency, momentum_squared)
            squared = frequency**2 + momentum_squared
            predicted = -shear * model.derivative_factor(squared) * (propagator @ propagator)
            displacement = 1e-5
            measured = (model.propagator(frequency, momentum_squared + displacement * shear)
                        - model.propagator(frequency, momentum_squared - displacement * shear)) / (2 * displacement)
            close(f"finite-metric-reg{regulator_scale}-{frequency}", measured, predicted, relative=1e-8)
            wrong = -shear * (propagator @ propagator)
            missing_source_error = float(np.max(np.abs(wrong - measured)))
            assert missing_source_error > 1e-7
            finite_variation_rows.append({"scale": regulator_scale, "frequency": frequency,
                                         "missing_regulator_source_error": missing_source_error})

    tadpole_rows = []
    for regulator_scale in [2., 4., 8.]:
        model = WardCandidate(regulator_scale)
        estimates = {order: tadpole_integrals(model, order) for order in [32, 64, 96]}
        fine = estimates[96]
        close(f"tadpole-reg{regulator_scale}-refinement", estimates[64]["tadpole"], fine["tadpole"], relative=2e-6)
        close(f"tadpole-reg{regulator_scale}-phase-identity", fine["phase_self_energy"], fine["tadpole_over_amplitude"], relative=1e-12)
        close(f"tadpole-reg{regulator_scale}-zero-phase-after-shift", fine["phase_mass_after_background_shift"], 0., relative=0., absolute=2e-14)
        assert abs(fine["relative_background_shift"]) < .1
        tadpole_rows.append({"scale": regulator_scale, "orders": estimates})
        print(json.dumps({"stage": "Goldstone_background", "scale": regulator_scale, **fine}), flush=True)
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "checks": checks, "checks_passed": len(checks), "hard_boundary_fixtures": hard_rows,
              "infinite_spatial_paired_fixtures": infinite_rows, "metric_variations": finite_variation_rows,
              "tadpole_rows": tadpole_rows,
              "core_sha256": hashlib.sha256((ROOT / "ward_core.py").read_bytes()).hexdigest(),
              "algebra_sha256": hashlib.sha256((ROOT / "results/algebra/status.json").read_bytes()).hexdigest(),
              "physical_renormalized_background_shift_claimed": False,
              "complete_regulated_collective_operator_recomputed": False,
              "scope": "One-loop metric and phase Ward checks, including surface/routing corrections. Infinity-mapped spatial slices and full tadpole integrals; not a full dressed dynamics calculation."}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "checks": len(checks)}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        if OUTPUT.exists():
            (OUTPUT / "FAILED.json").write_text(json.dumps({"state": "failed", "error": repr(error), "traceback": traceback.format_exc()}, indent=2), encoding="utf-8")
        raise
