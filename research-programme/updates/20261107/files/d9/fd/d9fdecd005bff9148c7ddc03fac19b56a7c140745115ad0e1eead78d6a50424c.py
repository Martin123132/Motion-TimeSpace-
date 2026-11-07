import sys
from common import *
sys.path.extend([str(TIMECHAIN), str(PREVIOUS)])
from mean_math import *
from scipy.interpolate import CubicSpline
import numpy as np


def metric_polynomial(background, wave, units):
    count = len(units)
    scale_value = background["scale"]
    amplitude = background["background"]
    source = np.zeros((count, 8))
    source[:, 0] = background["velocity_s"]
    source[:, 2], source[:, 3] = amplitude.imag / (2 * scale_value**2), -amplitude.real / (2 * scale_value**2)
    cosine, sine = np.zeros_like(source), np.zeros_like(source)
    cosine[:, 2], cosine[:, 3] = amplitude.imag / (2 * scale_value**2), amplitude.real / (2 * scale_value**2)
    sine[:, 2], sine[:, 3] = -amplitude.real / (2 * scale_value**2), amplitude.imag / (2 * scale_value**2)
    rows = np.zeros((count, 2, 8))
    rows[:, 0] = -3 * source / (2 * wave)
    rows[:, 0, 5] -= 3 / (wave * scale_value**2)
    rows[:, 0, 7] += 1 / (2 * wave * scale_value**2)
    rows[:, 1, 7] = 1 / (2 * wave * scale_value**2)
    cos_rows, sin_rows = np.zeros_like(rows), np.zeros_like(rows)
    cos_rows[:, 0] = -3 * cosine / (2 * wave)
    sin_rows[:, 0] = -3 * sine / (2 * wave)
    return harmonic_parts(rows * units[:, None], cos_rows * units[:, None], sin_rows * units[:, None])


def calculate(provider, points, wave):
    original, mean, cosine, sine = phase_background(provider, points)
    hessian, exponent, exponent_rate, units = polynomials(mean, cosine, sine, wave)
    order = action_orders(hessian, exponent, exponent_rate)[2]
    metric = product(metric_polynomial(mean, wave, units), order["coordinate_map"])[0].real
    data = transform(original, wave, include_fast=False)
    matrix = data["transform"] * units[:, :, None] / units[:, None, :]
    return dict(hessian=order["hessian"][0].real / (units[:, :, None] * units[:, None, :]),
                source=order["source_map"][0].real * units[:, None, :] / units[:, :, None],
                feedback=metric / units[:, None, :], transform=matrix, units=units)


def main():
    modest()
    check_parent()
    require(read(ROOT / "preflight-v2-result.json")["passed"], "native feedback preflight")
    write(ROOT / "coefficient-inputs.json", dict(sources={str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")},
                                               order=2, algebra=ALGEBRA, numerical=GATE, no_perturbation_history=True))
    provider = Background("heavy")
    wave = dict(read(WAVELENGTH / "inventory-config.json")["waves"])["balanced"]
    pieces = []
    for first in range(0, len(provider.efold), 256):
        guard()
        pieces.append(calculate(provider, provider.efold[first:first + 256], wave))
        if first % 4096 == 0:
            print("Coefficient points", first, "/", len(provider.efold), flush=True)
    tables = {name: np.concatenate([piece[name] for piece in pieces]) for name in pieces[0]}
    del pieces
    np.savez_compressed(ROOT / "heavy-balanced-coefficients.npz", efold=provider.efold, wave=wave, **tables)
    indices = np.unique(np.linspace(0, len(provider.efold) - 2, 97, dtype=int))
    independent = provider.efold[indices] + .43 * (provider.efold[indices + 1] - provider.efold[indices])
    direct = calculate(provider, independent, wave)
    checks = {}
    refined = {}
    for name in ("hessian", "source", "feedback", "transform"):
        fine = CubicSpline(provider.efold, tables[name], axis=0)(independent)
        keep = np.unique(np.r_[np.arange(0, len(provider.efold), 2), len(provider.efold) - 1])
        coarse = CubicSpline(provider.efold[keep], tables[name][keep], axis=0)(independent)
        units = direct["units"]
        if name == "hessian":
            balancing = units[:, :, None] * units[:, None, :]
        elif name in ("source", "transform"):
            balancing = units[:, :, None] / units[:, None, :] if name == "source" else units[:, None, :] / units[:, :, None]
        else:
            balancing = units[:, None, :]
        denominator = norm(direct[name] * balancing)
        checks[name] = sup((fine - direct[name]) * balancing) / denominator
        refined[name] = sup((fine - coarse) * balancing) / denominator
    passed = all(value < GATE for value in list(checks.values()) + list(refined.values()))
    write(ROOT / "coefficient-result.json", dict(passed=passed, wave=wave, points=len(provider.efold), probes=len(independent),
          checks=checks, refinement=refined, sha256=digest(ROOT / "heavy-balanced-coefficients.npz"),
          source="retained dense background only", future_perturbations_used=False))
    print("Coefficient interpolation", checks, refined, passed, flush=True)
    require(passed, "coefficient representation failed; inspect, do not evolve")


if __name__ == "__main__":
    main()
