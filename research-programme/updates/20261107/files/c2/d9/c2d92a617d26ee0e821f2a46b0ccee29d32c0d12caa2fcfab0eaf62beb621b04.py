from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import traceback

import mpmath as mp
import numpy as np
import psutil
from scipy.linalg import eigvals

from regulated_operator import TensorRegulatedCandidate, assemble
from ward_core import WardCandidate
from operator_core import Candidate
from operator_explicit_mesh import assemble_explicit


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/regulated-operator"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite evidence.")
    OUTPUT.mkdir(parents=True)
    parent = ROOT.parent / "collective-operator-20261003/results/stage-integrity.json"
    mp.mp.dps = 70
    projection_checks = []
    model = TensorRegulatedCandidate(4., 48)
    mass = mp.mpf(10) / 9
    for frequency, first, second in [(mp.mpf(".01"), mp.mpf(".7"), mp.mpf(".701")),
                                    (mp.mpf(".2"), mp.mpf(".7"), mp.mpf(".7")),
                                    (mp.mpf(3), mp.mpf(".1"), mp.mpf(8))]:
        actual = model.exchange_l2(np.array([float(frequency)]), np.array([float(first)]), np.array([float(second)]))[0]
        for row in range(2):
            for column in range(2):
                def function(angle):
                    squared = frequency**2 + first**2 + second**2 - 2 * first * second * angle
                    shifted = squared + squared**3 / 4**4
                    determinant = shifted * (shifted + mass) + 4 * frequency**2
                    numerator = [[shifted, 2 * frequency], [-2 * frequency, shifted + mass]][row][column]
                    return (3 * angle**2 - 1) * numerator / (4 * determinant)
                expected = mp.quad(function, [-1, 0, mp.mpf(".9"), mp.mpf(".99"), mp.mpf(".999"), 1])
                relative = abs(actual[row, column] - expected) / abs(expected)
                assert relative < mp.mpf("2e-7"), (frequency, first, second, row, column, relative)
                projection_checks.append({"frequency": str(frequency), "first": str(first), "second": str(second),
                                          "row": row, "column": column, "relative_error": str(relative), "passed": True})
    edges = 2 * np.linspace(0, 1, 4)**1.5
    baseline, _ = assemble_explicit(Candidate(), edges, order=4)
    replay, _ = assemble(TensorRegulatedCandidate(None), edges, order=4)
    bare_replay_error = float(np.max(np.abs(baseline - replay)))
    assert bare_replay_error < 1e-16
    print(json.dumps({"stage": "projection_and_bare_replay_complete", "projection_checks": len(projection_checks)}), flush=True)
    configurations = [(None, 8, 16., 4, 32), (4., 8, 16., 4, 32), (4., 8, 16., 6, 48),
                      (4., 12, 16., 6, 48), (4., 8, 32., 4, 32)]
    rows = []
    for scale, inner, extent, order, angular in configurations:
        edges = np.concatenate([2 * np.linspace(0, 1, inner + 1)**1.5, [3., 4., 6., 8., 12., 16.]])
        if extent > 16:
            edges = np.concatenate([edges, [24., 32.]])
        label = f"reg{scale}-inner{inner}-box{int(extent)}-q{order}-ang{angular}"
        directory = OUTPUT / label
        directory.mkdir()
        started = time.monotonic()
        matrix, centers = assemble(TensorRegulatedCandidate(scale, angular), edges, order)
        assert np.all(np.isfinite(matrix))
        eigenvalues = eigvals(matrix)
        frequency, momentum = np.meshgrid(centers, centers, indexing="ij")
        soft_squared = momentum**2 + frequency**2 / (5 / 23)
        weights = np.stack([1 + 1 / soft_squared, np.ones_like(soft_squared),
                            1 + 1 / np.sqrt(soft_squared), 1 + 1 / np.sqrt(soft_squared)], axis=-1).ravel()
        bound = float(np.max((np.abs(matrix) @ weights) / weights))
        assert np.max(np.abs(eigenvalues)) <= bound * (1 + 1e-10)
        assert bound < 1
        source = np.tile([1., 1., 0., 0.], len(matrix) // 4)
        first_rung = matrix @ source
        largest_real_index = int(np.argmax(eigenvalues.real))
        assert abs(eigenvalues[largest_real_index].imag) < 1e-10
        coefficient = (1 / 9)**2 * math.sqrt(5 / 23) / (32 * math.pi**2)
        prediction = coefficient / float(soft_squared[0, 0])
        row = {"name": label, "regulator_scale": scale, "inner_cells": inner, "numerical_box": extent,
               "cell_order": order, "angular_order": angular, "matrix_dimension": len(matrix),
               "first_center": float(centers[0]), "spectral_radius": float(np.max(np.abs(eigenvalues))),
               "largest_positive_eigenvalue": float(eigenvalues[largest_real_index].real),
               "analytic_soft_weight_matrix_bound": bound,
               "first_rung_at_lowest_node": first_rung[:4].tolist(),
               "parameter_free_radial_soft_prediction": prediction,
               "radial_soft_ratio": float(first_rung[0] / prediction),
               "elapsed_seconds": time.monotonic() - started}
        np.save(directory / "operator.npy", matrix)
        np.savez(directory / "diagnostics.npz", eigenvalues=eigenvalues, centers=centers, edges=edges,
                 soft_weights=weights, first_rung=first_rung, source=source)
        (directory / "status.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "projection_checks": projection_checks, "bare_replay_error": bare_replay_error,
              "rows": rows, "parent_sha256": hashlib.sha256(parent.read_bytes()).hexdigest(),
              "operator_sha256": hashlib.sha256((ROOT / "regulated_operator.py").read_bytes()).hexdigest(),
              "ward_core_sha256": hashlib.sha256((ROOT / "ward_core.py").read_bytes()).hexdigest(),
              "source": "F=p^2 Z(s) h Y2m, Z=1+3s^2/Lambda^4; h_source=identity",
              "operator_scope": "Regulator-completed source and quadratic propagators, bare cubic-exchange ladder. Not fully dressed.",
              "full_continuum_spectral_bound_proved": False,
              "new_regulator_is_physical_operator": False}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "matrices": len(rows)}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        if OUTPUT.exists():
            (OUTPUT / "FAILED.json").write_text(json.dumps({"state": "failed", "error": repr(error), "traceback": traceback.format_exc()}, indent=2), encoding="utf-8")
        raise
