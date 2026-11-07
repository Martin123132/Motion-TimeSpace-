from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import psutil


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/curved-validation"


def derivative(values, axis):
    frequencies = np.fft.fftfreq(values.shape[axis], 1 / values.shape[axis])
    shape = [1] * values.ndim
    shape[axis] = len(frequencies)
    transformed = np.fft.fft(values, axis=axis)
    return np.fft.ifft(1j * frequencies.reshape(shape) * transformed, axis=axis).real


def action(inverse_metric, phase_gradient):
    volume = 1 / np.sqrt(-np.linalg.det(inverse_metric))
    kinetic = -.5 * np.einsum("...ab,...a,...b->...", inverse_metric, phase_gradient, phase_gradient)
    gradient = np.zeros(kinetic.shape + (4,))
    for axis in range(2):
        gradient[..., axis] = derivative(kinetic, axis)
    norm = np.einsum("...ab,...a,...b->...", inverse_metric, gradient, gradient)
    pressure = kinetic + .2 * kinetic**2 + .03 * kinetic**3
    coefficient = .07 + .02 * kinetic
    lagrangian = pressure - coefficient * norm
    return float(np.mean(volume * lagrangian) * (2 * math.pi)**2)


def fields(inverse_metric, phase_gradient, omit_response=False):
    metric = np.linalg.inv(inverse_metric)
    volume = 1 / np.sqrt(-np.linalg.det(inverse_metric))
    kinetic = -.5 * np.einsum("...ab,...a,...b->...", inverse_metric, phase_gradient, phase_gradient)
    gradient = np.zeros(kinetic.shape + (4,))
    for axis in range(2):
        gradient[..., axis] = derivative(kinetic, axis)
    raised_gradient = np.einsum("...ab,...b->...a", inverse_metric, gradient)
    gradient_norm = np.einsum("...a,...a->...", gradient, raised_gradient)
    box = sum(derivative(volume * raised_gradient[..., axis], axis) for axis in range(2)) / volume
    pressure = kinetic + .2 * kinetic**2 + .03 * kinetic**3
    pressure_x = 1 + .4 * kinetic + .09 * kinetic**2
    coefficient = .07 + .02 * kinetic
    response = pressure_x if omit_response else pressure_x + .02 * gradient_norm + 2 * coefficient * box
    lagrangian = pressure - coefficient * gradient_norm
    current = response[..., None] * np.einsum("...ab,...b->...a", inverse_metric, phase_gradient)
    phase_euler = sum(derivative(volume * current[..., axis], axis) for axis in range(2)) / volume
    stress = (response[..., None, None] * np.einsum("...a,...b->...ab", phase_gradient, phase_gradient)
              + 2 * coefficient[..., None, None] * np.einsum("...a,...b->...ab", gradient, gradient)
              + metric * lagrangian[..., None, None])
    mixed = inverse_metric @ stress
    upper = mixed @ inverse_metric
    divergence = np.zeros_like(phase_gradient)
    for component in range(4):
        divergence[..., component] = sum(derivative(volume * mixed[..., axis, component], axis) for axis in range(2)) / volume
        if component < 2:
            divergence[..., component] -= .5 * np.einsum("...ab,...ab->...", derivative(metric, component), upper)
    target = phase_euler[..., None] * phase_gradient
    trace = np.einsum("...ab,...ab->...", inverse_metric, stress)
    reversed_stress = stress - metric * trace[..., None, None] / 2
    return {"volume": volume, "metric": metric, "kinetic": kinetic, "gradient": gradient,
            "response": response, "pressure": pressure, "coefficient": coefficient, "stress": stress,
            "reversed_stress": reversed_stress, "phase_euler": phase_euler,
            "divergence": divergence, "target": target}


def fixtures(cells):
    values = 2 * math.pi * np.arange(cells) / cells
    time, space = np.meshgrid(values, values, indexing="ij")
    periodic = .1 * np.sin(time) * np.cos(space) + .04 * np.cos(2 * time) * np.sin(space)
    phase_gradient = np.zeros((cells, cells, 4))
    phase_gradient[..., 0] = 1 + derivative(periodic, 0)
    phase_gradient[..., 1] = derivative(periodic, 1)
    inverse_metric = np.broadcast_to(np.diag([-1., 1., 1., 1.]), (cells, cells, 4, 4)).copy()
    for first in range(4):
        for second in range(first, 4):
            profile = .015 * np.sin((first % 2 + 1) * time + (second % 2 + 1) * space + .3 * (first + second))
            inverse_metric[..., first, second] += profile
            if first != second:
                inverse_metric[..., second, first] += profile
    assert np.all(np.linalg.eigvalsh(inverse_metric)[..., 0] < 0)
    assert np.all(np.linalg.eigvalsh(inverse_metric)[..., 1:] > 0)
    return time, space, phase_gradient, inverse_metric


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite executed evidence.")
    OUTPUT.mkdir(parents=True)
    noether = []
    for cells in [32, 64]:
        time, space, phase_gradient, inverse_metric = fixtures(cells)
        data = fields(inverse_metric, phase_gradient)
        residual = data["divergence"] - data["target"]
        scale = max(float(np.max(np.abs(data["target"]))), 1.)
        error = float(np.max(np.abs(residual)))
        assert error < 1e-8 * scale, (cells, error, scale)
        wrong = fields(inverse_metric, phase_gradient, omit_response=True)
        wrong_error = float(np.max(np.abs(wrong["divergence"] - wrong["target"])))
        assert wrong_error > max(1e-5, 1000 * error)
        source_expected = (data["response"][..., None, None] * np.einsum("...a,...b->...ab", phase_gradient, phase_gradient)
                           + 2 * data["coefficient"][..., None, None] * np.einsum("...a,...b->...ab", data["gradient"], data["gradient"])
                           + data["metric"] * (data["kinetic"] * data["response"] - data["pressure"])[..., None, None])
        assert np.max(np.abs(source_expected - data["reversed_stress"])) < 1e-12
        noether.append({"cells": cells, "absolute_error": error, "relative_error": error / scale,
                        "omitted_Q_terms_negative_control_error": wrong_error, "passed": True})

    def integral(values):
        return float(np.mean(values) * (2 * math.pi)**2)

    rows = []
    for first, second in itertools.combinations_with_replacement(range(4), 2):
        direction = np.zeros_like(inverse_metric)
        profile = .7 * np.sin(time + space) + .4 * np.cos(2 * time - space) + .2
        direction[..., first, second] = profile
        if first != second:
            direction[..., second, first] = profile
        predicted = -.5 * integral(data["volume"] * np.einsum("...ab,...ab->...", data["stress"], direction))
        estimates = []
        for step in [1e-4, 5e-5]:
            measured = (action(inverse_metric + step * direction, phase_gradient)
                        - action(inverse_metric - step * direction, phase_gradient)) / (2 * step)
            estimates.append(measured)
        error = abs(estimates[-1] - predicted)
        assert error < 2e-8 + 2e-7 * abs(predicted), (first, second, estimates, predicted)
        rows.append({"kind": "inverse_metric", "component": [first, second], "predicted": predicted,
                     "measured": estimates, "absolute_error": error, "passed": True})

    variation = .07 * np.sin(2 * time + 3 * space) + .03 * np.cos(time - space)
    gradient_variation = np.zeros_like(phase_gradient)
    for axis in range(2):
        gradient_variation[..., axis] = derivative(variation, axis)
    predicted = integral(data["volume"] * data["phase_euler"] * variation)
    estimates = []
    for step in [1e-4, 5e-5]:
        estimates.append((action(inverse_metric, phase_gradient + step * gradient_variation)
                          - action(inverse_metric, phase_gradient - step * gradient_variation)) / (2 * step))
    error = abs(estimates[-1] - predicted)
    assert error < 2e-8 + 2e-7 * abs(predicted)
    rows.append({"kind": "phase", "predicted": predicted, "measured": estimates, "absolute_error": error, "passed": True})

    density_metric = data["volume"][..., None, None] * inverse_metric
    for fixture in range(3):
        direction = np.zeros_like(inverse_metric)
        for first, second in itertools.combinations_with_replacement(range(4), 2):
            profile = .1 * np.sin((fixture + 1) * time + space + first + .4 * second) + .02
            direction[..., first, second] = profile
            direction[..., second, first] = profile
        predicted = -.5 * integral(np.einsum("...ab,...ab->...", data["reversed_stress"], direction))
        estimates = []
        for step in [1e-4, 5e-5]:
            positive = density_metric + step * direction
            negative = density_metric - step * direction
            metric_positive = positive / np.sqrt(-np.linalg.det(positive))[..., None, None]
            metric_negative = negative / np.sqrt(-np.linalg.det(negative))[..., None, None]
            estimates.append((action(metric_positive, phase_gradient) - action(metric_negative, phase_gradient)) / (2 * step))
        error = abs(estimates[-1] - predicted)
        assert error < 2e-8 + 2e-7 * abs(predicted)
        rows.append({"kind": "parent_density_metric", "fixture": fixture, "predicted": predicted,
                     "measured": estimates, "absolute_error": error, "passed": True})
    report = {
        "state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
        "curved_off_shell_Noether_fixtures": noether, "finite_action_variations": rows,
        "finite_action_variation_count": len(rows),
        "profile_scope": "Four-dimensional Lorentzian metric with t,x dependence, periodic integration test profiles and unit spectator volume; not a cosmological solution.",
        "test_functions": "P=X+0.2X^2+0.03X^3; A=0.07+0.02X, generic identity fixtures rather than a fitted physical model.",
        "parent_density_chain_tested": True,
        "derivation_sha256": hashlib.sha256((ROOT / "results/derivation/status.json").read_bytes()).hexdigest(),
    }
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "noether": noether, "finite_variations": len(rows),
                      "maximum_variation_absolute_error": max(row["absolute_error"] for row in rows)}))


if __name__ == "__main__":
    main()

