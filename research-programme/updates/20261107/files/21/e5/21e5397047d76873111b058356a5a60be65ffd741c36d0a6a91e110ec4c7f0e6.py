from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import time
import traceback

import numpy as np
import psutil
from scipy.linalg import eig

from operator_core import Candidate, assemble, rectangle_log_integral, TRANSPOSE_PARITY
from operator_explicit_mesh import assemble_explicit


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results" / "fixed-infrared-refinement"


def cell_integral(model, frequency, momentum, frequency_half, radial_half, order, subtract):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    frequencies, momenta = np.meshgrid(frequency + frequency_half * nodes, momentum + radial_half * nodes, indexing="ij")
    integration_weights = (frequency_half * radial_half * np.outer(weights, weights)).ravel()
    frequencies, momenta = frequencies.ravel(), momenta.ravel()
    exchange = model.exchange_l2(frequency - frequencies, momentum, momenta)
    response = np.einsum("ndf,ndfAB->nAB", exchange, model.coupling_blocks(frequencies, momenta), optimize=True)
    response *= (momenta**4 / momentum**2)[:, None, None]
    singular_source = model.coupling_blocks(np.array([frequency]), np.array([momentum]))[0, 1, 1] / 4
    if subtract:
        distance = ((frequencies - frequency) / model.sound)**2 + (momenta - momentum)**2
        response -= np.log(4 * momentum**2 / distance)[:, None, None] * singular_source
    answer = np.einsum("n,nAB->AB", integration_weights, response, optimize=True)
    if subtract:
        answer += rectangle_log_integral(radial_half, frequency_half, model.sound, momentum) * singular_source
    return answer / (4 * math.pi**3)


def comparison_weight_bound(matrix):
    positive = np.abs(matrix)
    weights = np.ones(len(matrix))
    for iteration in range(200):
        image = positive @ weights
        maximum = float(np.max(image))
        if maximum == 0:
            return 0., weights
        updated = np.maximum(image / maximum, 1e-14)
        weights = 0.5 * weights + 0.5 * updated
    return float(np.max((positive @ weights) / weights)), weights


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to replace an executed refinement.")
    OUTPUT.mkdir(parents=True)
    model = Candidate()
    base, _ = assemble(model, cells=4, order=4, cutoff=4)
    explicit, _ = assemble_explicit(model, 4 * np.linspace(0, 1, 5)**1.5, order=4)
    assert np.max(np.abs(base - explicit)) < 1e-18
    cell_rows = []
    for fixture in [(0.1, 0.2, 0.06, 0.09), (0.8, 1.3, 0.2, 0.15)]:
        reference = cell_integral(model, *fixture, 256, True)
        direct_reference = cell_integral(model, *fixture, 256, False)
        reference_scale = np.max(np.abs(reference))
        independent_error = float(np.max(np.abs(reference - direct_reference)) / reference_scale)
        assert independent_error < 5e-5, independent_error
        records = []
        for order in [4, 8, 16, 32, 64, 128]:
            subtracted = cell_integral(model, *fixture, order, True)
            plain = cell_integral(model, *fixture, order, False)
            records.append({"order": order,
                            "subtracted_relative_error_to_256": float(np.max(np.abs(subtracted - reference)) / reference_scale),
                            "unsubtracted_relative_error_to_256": float(np.max(np.abs(plain - reference)) / reference_scale)})
        assert records[-1]["subtracted_relative_error_to_256"] < 1e-6
        cell_rows.append({"fixture": fixture, "plain_vs_subtracted_256_relative_difference": independent_error,
                          "records": records})
    (OUTPUT / "self-cell-checks.json").write_text(json.dumps(cell_rows, indent=2), encoding="utf-8")

    configurations = [(10, 2., 6), (10, 4., 6), (10, 8., 6), (14, 4., 6), (14, 4., 8)]
    rows = []
    for inner_cells, cutoff, order in configurations:
        edges = 2 * np.linspace(0, 1, inner_cells + 1)**1.5
        if cutoff >= 4:
            edges = np.concatenate([edges, np.array([2.5, 3., 3.5, 4.])])
        if cutoff >= 8:
            edges = np.concatenate([edges, np.array([5., 6., 7., 8.])])
        name = f"inner{inner_cells}-cut{int(cutoff)}-q{order}"
        directory = OUTPUT / name
        directory.mkdir()
        started = time.monotonic()
        matrix, centers = assemble_explicit(model, edges, order=order)
        eigenvalues, vectors = eig(matrix)
        largest = int(np.argmax(np.abs(eigenvalues)))
        largest_eigenvalue = eigenvalues[largest]
        residual = float(np.max(np.abs(matrix @ vectors[:, largest] - largest_eigenvalue * vectors[:, largest])) / np.max(np.abs(vectors[:, largest])))
        assert residual < 1e-10
        bound, weights = comparison_weight_bound(matrix)
        assert abs(largest_eigenvalue) <= bound * (1 + 1e-8)
        cells = len(centers)
        physical_scaling = np.tile(np.repeat(centers**2, 4), cells)
        physical_matrix_norm = float(np.max(np.sum(np.abs(matrix) * physical_scaling[:, None] / physical_scaling[None, :], axis=1)))
        row = {"name": name, "inner_cells": inner_cells, "cutoff_over_mu": cutoff, "cell_order": order,
               "cells_per_positive_axis": cells, "first_center": float(centers[0]),
               "matrix_dimension": len(matrix), "spectral_radius": float(abs(largest_eigenvalue)),
               "largest_positive_eigenvalue": float(np.max(eigenvalues.real)),
               "leading_eigenvalue_real": float(largest_eigenvalue.real),
               "leading_eigenvalue_imaginary": float(largest_eigenvalue.imag),
               "eigenpair_residual": residual,
               "raw_h_infinity_norm": float(np.max(np.sum(np.abs(matrix), axis=1))),
               "grid_physical_vertex_similarity_norm": physical_matrix_norm,
               "positive_weight_comparison_bound": bound,
               "bound_is_for_finite_matrix_only": True, "elapsed_seconds": time.monotonic() - started}
        np.save(directory / "operator.npy", matrix)
        np.savez(directory / "diagnostics.npz", centers=centers, edges=edges, eigenvalues=eigenvalues,
                 positive_norm_weights=weights)
        (directory / "status.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "core_sha256": hashlib.sha256((ROOT / "operator_core.py").read_bytes()).hexdigest(),
              "explicit_mesh_sha256": hashlib.sha256((ROOT / "operator_explicit_mesh.py").read_bytes()).hexdigest(),
              "replayed_original_mesh_exactly": True, "self_cell_checks": cell_rows, "rows": rows,
              "fixed_infrared_for_first_three_cutoffs": True, "continuum_exclusion_proved": False,
              "eigenvalues_not_required_to_equal_between_resolutions": True}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "runs": len(rows)}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        if OUTPUT.exists():
            (OUTPUT / "FAILED.json").write_text(json.dumps({"error": repr(error), "traceback": traceback.format_exc()}, indent=2), encoding="utf-8")
        raise
