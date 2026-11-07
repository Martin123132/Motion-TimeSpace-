from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import traceback

import numpy as np
import psutil
from scipy.linalg import eig, solve

from operator_core import Candidate, assemble


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results" / "static-operator"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite executed evidence.")
    OUTPUT.mkdir(parents=True)
    authority = json.loads((ROOT / "results/normalization/status.json").read_text(encoding="utf-8"))
    assert authority["state"] == "complete"
    assert authority["core_sha256"] == hashlib.sha256((ROOT / "operator_core.py").read_bytes()).hexdigest()
    configurations = [(4, 4, 4.), (6, 4, 4.), (8, 4, 4.), (8, 6, 4.),
                      (10, 6, 4.), (12, 6, 4.), (12, 8, 4.),
                      (10, 6, 2.), (12, 6, 2.), (10, 6, 8.), (12, 6, 8.)]
    zero, _ = assemble(Candidate(epsilon=0), cells=3, order=4, cutoff=2)
    assert np.max(np.abs(zero)) == 0
    first, _ = assemble(Candidate(epsilon=.01), cells=3, order=4, cutoff=2)
    second, _ = assemble(Candidate(epsilon=.02), cells=3, order=4, cutoff=2)
    scaling_error = float(np.max(np.abs(second - 2 * first)))
    assert scaling_error < 1e-14
    rows = []
    for cells, order, cutoff in configurations:
        started = time.monotonic()
        name = f"n{cells}-q{order}-cut{int(cutoff)}"
        destination = OUTPUT / name
        destination.mkdir()
        matrix, centers = assemble(Candidate(), cells=cells, order=order, cutoff=cutoff)
        assert np.all(np.isfinite(matrix))
        eigenvalues, eigenvectors = eig(matrix, check_finite=True)
        index = int(np.argmax(np.abs(eigenvalues)))
        leading = eigenvalues[index]
        vector = eigenvectors[:, index]
        infinity_norm = float(np.max(np.sum(np.abs(matrix), axis=1)))
        residual = float(np.max(np.abs(matrix @ vector - leading * vector)) / max(np.max(np.abs(vector)), 1e-300))
        assert residual < 1e-10
        assert abs(leading) <= infinity_norm * (1 + 1e-12)
        source = np.tile([1., 1., 0., 0.], cells**2)
        response = solve(np.eye(len(matrix)) - matrix, source)
        response_residual = float(np.max(np.abs(response - source - matrix @ response)))
        assert response_residual < 1e-10
        correction = float(np.max(np.abs(response - source)))
        row = {"name": name, "cells_per_positive_axis": cells, "cell_quadrature_order": order,
               "frequency_and_momentum_cutoff_over_mu": cutoff, "mesh_power": 1.5,
               "matrix_dimension": len(matrix), "spectral_radius": float(abs(leading)),
               "leading_eigenvalue_real": float(leading.real), "leading_eigenvalue_imag": float(leading.imag),
               "maximum_real_eigenvalue": float(np.max(eigenvalues.real)),
               "minimum_distance_to_unit_eigenvalue": float(np.min(np.abs(1 - eigenvalues))),
               "infinity_norm": infinity_norm, "eigenpair_residual": residual,
               "stress_vertex_max_absolute_correction_for_unit_source": correction,
               "stress_vertex_equation_residual": response_residual,
               "finite_matrix_contraction": bool(infinity_norm < 1),
               "finite_matrix_vertex_correction_bound": infinity_norm / (1 - infinity_norm) if infinity_norm < 1 else None,
               "elapsed_seconds": time.monotonic() - started}
        if infinity_norm < 1:
            assert correction <= infinity_norm / (1 - infinity_norm) * (1 + 1e-9)
        np.save(destination / "operator.npy", matrix)
        np.savez(destination / "diagnostics.npz", eigenvalues=eigenvalues, leading_eigenvector=vector,
                 centers=centers, source=source, stress_vertex=response)
        (destination / "status.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "parameters": {"mu": 1, "y": 2, "epsilon": .01, "physical_values_fitted": False},
              "normalization_sha256": hashlib.sha256((ROOT / "results/normalization/status.json").read_bytes()).hexdigest(),
              "core_sha256": authority["core_sha256"], "zero_coupling_matrix_is_zero": True,
              "epsilon_linear_scaling_max_error": scaling_error, "rows": rows,
              "static_total_euclidean_frequency": 0, "total_spatial_momentum": 0,
              "relative_frequencies_retained": True, "cutoff_shape": "box in absolute relative frequency and radial momentum",
              "no_diagonal_epsilon_regulator": True, "analytic_self_cell_log_subtraction": True,
              "renormalized_or_self_consistent_dressed_result": False,
              "continuum_operator_norm_proved": False, "finite_frequency_pole_search": False,
              "scope": "Bare-propagator, action-derived leading cubic-exchange l=2 ladder diagnostic, with no adjustable tensor coupling or counterterm. Finite-cutoff and finite-mesh results are not a full nonperturbative theorem."}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "runs": len(rows)}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        if OUTPUT.exists():
            (OUTPUT / "FAILED.json").write_text(json.dumps({"error": repr(error), "traceback": traceback.format_exc()}, indent=2), encoding="utf-8")
        raise
