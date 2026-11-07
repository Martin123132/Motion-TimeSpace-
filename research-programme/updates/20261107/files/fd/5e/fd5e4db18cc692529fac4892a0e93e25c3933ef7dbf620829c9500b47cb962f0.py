from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "collective-operator-20261003"
OUTPUT = ROOT / "results/soft-response"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite executed evidence.")
    OUTPUT.mkdir(parents=True)
    mass, chemical, frequency, momentum_squared = sym.symbols("mass chemical frequency momentum_squared", positive=True)
    alpha = 2 * chemical / mass
    phase = 1 / (momentum_squared + (1 + 4 * chemical**2 / mass) * frequency**2)
    soft = sym.Matrix([[1 / mass - alpha**2 * frequency**2 * phase, alpha * frequency * phase],
                       [-alpha * frequency * phase, phase]])
    column = sym.Matrix([1, alpha * frequency])
    row = sym.Matrix([[1, -alpha * frequency]])
    matrix = column * row
    checks = []

    def check(name, value):
        assert sym.simplify(value) == 0, (name, value)
        checks.append({"name": name, "passed": True})

    for index in range(2):
        check(f"soft_left_projection_{index}", (soft * column)[index] - (1 / mass if index == 0 else 0))
        check(f"soft_right_projection_{index}", (row * soft)[index] - (1 / mass if index == 0 else 0))
    for first in range(2):
        for second in range(2):
            check(f"soft_sandwich_{first}_{second}", (soft * matrix * soft)[first, second] - (1 / mass**2 if first == 0 and second == 0 else 0))

    shifted = sym.symbols("shifted", positive=True)
    inverse = sym.Matrix([[shifted + mass, -2 * chemical * frequency],
                          [2 * chemical * frequency, shifted]])
    exact = inverse.inv()
    amplitude_axis = sym.Matrix([1, 0])
    completed_column = inverse * amplitude_axis / mass
    completed_row = amplitude_axis.T * inverse / mass
    for first in range(2):
        for second in range(2):
            check(f"exact_algebraic_completion_not_full_vertex_claim_{first}_{second}",
                  (exact * completed_column * completed_row * exact)[first, second]
                  - (1 / mass**2 if first == 0 and second == 0 else 0))
    sound = math.sqrt(5 / 23)
    coefficient = (1 / 9)**2 * sound / (32 * math.pi**2)
    rows = []
    report_path = PREVIOUS / "results/fixed-infrared-refinement/status.json"
    parent_report = json.loads(report_path.read_text(encoding="utf-8"))
    for old in parent_report["rows"]:
        folder = PREVIOUS / "results/fixed-infrared-refinement" / old["name"]
        operator = np.load(folder / "operator.npy", allow_pickle=False)
        data = np.load(folder / "diagnostics.npz", allow_pickle=False)
        centers = data["centers"]
        frequency_grid, momentum_grid = np.meshgrid(centers, centers, indexing="ij")
        soft_squared = momentum_grid**2 + frequency_grid**2 / sound**2
        weights = np.stack([1 + 1 / soft_squared, np.ones_like(soft_squared),
                            1 + 1 / np.sqrt(soft_squared), 1 + 1 / np.sqrt(soft_squared)], axis=-1).ravel()
        bound = float(np.max((np.abs(operator) @ weights) / weights))
        assert old["spectral_radius"] < bound < 1
        first_rung = operator @ np.tile([1., 1., 0., 0.], len(operator) // 4)
        radial_prediction = coefficient / float(soft_squared[0, 0])
        mixed_prediction = -math.sqrt(2) * (2 / (10 / 9)) * centers[0] * radial_prediction
        rows.append({"name": old["name"], "lowest_frequency_and_momentum": float(centers[0]),
                     "radial_first_rung": float(first_rung[0]), "radial_prediction_no_fit": radial_prediction,
                     "radial_ratio": float(first_rung[0] / radial_prediction),
                     "antisymmetric_first_rung": float(first_rung[3]), "antisymmetric_prediction_no_fit": float(mixed_prediction),
                     "antisymmetric_ratio": float(first_rung[3] / mixed_prediction),
                     "analytic_weight_matrix_bound": bound, "parent_matrix_sha256": hashlib.sha256((folder / "operator.npy").read_bytes()).hexdigest()})
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "exact_checks": checks, "exact_check_count": len(checks),
              "infrared_coefficient": coefficient, "mass_squared": 10 / 9,
              "leading_nonanalytic_radial_propagator_response_bound_for_unit_shear": coefficient / (10 / 9)**2,
              "parent_rows": rows, "parent_report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
              "sandwich_scope": "The leading soft nonanalytic tensor-source contribution. This is not a bound on the entire stress response or on all pair fluctuations.",
              "exact_completion_scope": "An algebraic identity using inverse-propagator-dressed radial vectors; the actual full vertex has not been proved equal to that completion.",
              "continuum_operator_norm_bound_proved": False,
              "physical_soft_weights_chosen_before_replaying_matrix": True}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(checks), "coefficient": coefficient,
                      "finest_parent_radial_ratio": rows[-1]["radial_ratio"],
                      "finest_parent_mixed_ratio": rows[-1]["antisymmetric_ratio"],
                      "leading_propagated_contribution_bound": report["leading_nonanalytic_radial_propagator_response_bound_for_unit_shear"]}))


if __name__ == "__main__":
    main()
