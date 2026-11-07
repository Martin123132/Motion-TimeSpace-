from __future__ import annotations

import os
for variable in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[variable] = "1"
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import inspect
import json
import time

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / "collision-temperature-derivative-20261020"
PARENT_SHA = "4cc62d2d664165ab81ed2c0870e0229cdc7212a1bfdc7e9951a0fa387322986f"
sys.path.insert(0, str(PARENT))
import collision_stage185 as old

np, mp, prior, saved, source, linear = old.np, old.mp, old.prior, old.saved, old.source, old.linear
read, write, check = old.read, old.write, old.check
OFFSETS = [.001, -.001, .0005, -.0005, .005, -.005, .01, -.01]
PARTS = ["conductance", "mixed", "basis_second", "basis_tangent_square"]


def relative(actual, expected):
    denominator = np.linalg.norm(expected)
    if not np.isfinite(denominator) or denominator == 0:
        raise ValueError("Undefined relative comparison")
    return float(np.linalg.norm(actual - expected) / denominator)


class Jet:
    __array_priority__ = 10000

    def __init__(self, value, first=0., second=0.):
        self.value = np.asarray(value, dtype=float)
        self.first = np.broadcast_to(np.asarray(first, dtype=float), self.value.shape)
        self.second = np.broadcast_to(np.asarray(second, dtype=float), self.value.shape)

    @staticmethod
    def lift(other):
        return other if isinstance(other, Jet) else Jet(other)

    def __add__(self, other):
        other = self.lift(other)
        return Jet(self.value + other.value, self.first + other.first, self.second + other.second)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.value, -self.first, -self.second)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Jet(self.value * other.value,
                   self.first * other.value + self.value * other.first,
                   self.second * other.value + 2 * self.first * other.first + self.value * other.second)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        return Jet(self.value ** exponent,
                   exponent * self.value ** (exponent - 1) * self.first,
                   exponent * self.value ** (exponent - 1) * self.second
                   + exponent * (exponent - 1) * self.value ** (exponent - 2) * self.first ** 2)

    def __truediv__(self, other):
        return self * self.lift(other) ** -1

    def __rtruediv__(self, other):
        return self.lift(other) / self

    def __getitem__(self, index):
        return Jet(self.value[index], self.first[index], self.second[index])

    def sum(self):
        return Jet(self.value.sum(), self.first.sum(), self.second.sum())

    def expm1(self):
        exponential = np.exp(self.value)
        return Jet(np.expm1(self.value), exponential * self.first,
                   exponential * (self.second + self.first ** 2))


def authenticate():
    seal_path = PARENT / "results/stage-integrity.json"
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal["consumed_and_immediate_rehashed"])
    paths.update({str(PARENT / name): checksum for name, checksum in seal["file_hashes"].items()})
    paths[str(seal_path)] = PARENT_SHA
    for name in ["MTS-COSMOLOGY-LAB-HANDOFF.md", "MTS-HOLDOUT-DATA-EXPOSURE-HANDOFF.md"]:
        path = BRANCH.parent / name
        paths[str(path)] = saved.digest(path)
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def prepare():
    assert not (ROOT / "configuration.json").exists()
    paths = authenticate()
    bank, basis, theta = old.setup()
    parent_config = read(PARENT / "configuration.json")
    assert parent_config["source_prediction_tolerance"] == .01
    assert parent_config["identity_tolerance"] == 1e-10
    with np.load(PARENT / "quadrature.npz") as packet:
        for key in ["nodes", "measure", "values", "mass", "temperature", "chemical", "energy"]:
            assert np.array_equal(getattr(basis, key), packet[key]), key
    config = dict(stage=186, started_utc=datetime.now(timezone.utc).isoformat(),
                  parent_sha256=PARENT_SHA, theta=theta, offsets=OFFSETS,
                  event_order=6, basis_spec=bank.specification,
                  source_prediction_tolerance=.01, identity_tolerance=1e-10,
                  retrospective_saved_target_validation=True,
                  production_derivative="analytic forward second-order product/chain rules, no fitted target coefficient",
                  bookmark_hashes={str(path): saved.digest(path) for path in
                                   [BRANCH / "RESUME-CURRENT.md", BRANCH.parent / "CURRENT_LOCAL_RESUME.md"]})
    write(ROOT / "configuration.json", config)
    write(ROOT / "authenticated-inputs.json", paths)
    write(ROOT / "progress.json", dict(state="prepared"))
    print(json.dumps(dict(state="prepared", authenticated_paths=len(paths), theta=theta)), flush=True)


def event_curvature(theta, order):
    radial, radial_base = old.geometry_module.special.roots_genlaguerre(order, .5)
    scaled = Jet(theta * radial, theta * radial, theta * radial)
    gamma = 1 + scaled
    speed = (scaled * (2 + scaled)) ** .5 / gamma
    raw = gamma * (2 + scaled) ** .5 * radial_base
    radial_weights = raw / raw.sum()
    electron, electron_weights = np.polynomial.legendre.leggauss(order)
    scattering, scattering_weights = np.polynomial.legendre.leggauss(order)
    azimuth = 2 * np.pi * (np.arange(2 * order) + .5) / (2 * order)
    cosine = np.repeat(scattering, len(azimuth))
    transverse_cosine = np.repeat(np.sqrt(1 - scattering ** 2), len(azimuth)) * np.tile(np.cos(azimuth), order)
    angular_weights = np.repeat(scattering_weights / (2 * len(azimuth)), len(azimuth))
    output = {key + suffix: [] for key in ["incident", "outgoing", "weight"] for suffix in ["", "_t", "_tt"]}
    output["cosine"] = []
    for index in range(order):
        beta = speed[index]
        for electron_cosine, electron_weight in zip(electron, electron_weights / 2):
            denominator = 1 - beta * electron_cosine
            incident = gamma[index] * denominator
            parallel = (beta * electron_cosine - beta ** 2) / denominator
            transverse = beta * np.sqrt(1 - electron_cosine ** 2) / incident
            outgoing = gamma[index] * (1 + parallel * cosine + transverse * transverse_cosine)
            weight = radial_weights[index] * denominator * electron_weight * angular_weights
            for key, value in [("incident", incident), ("outgoing", outgoing), ("weight", weight)]:
                for suffix, attribute in [("", "value"), ("_t", "first"), ("_tt", "second")]:
                    output[key + suffix].append(np.broadcast_to(getattr(value, attribute), cosine.shape))
            output["cosine"].append(cosine)
    return {key: np.concatenate(values) for key, values in output.items()}, radial_weights, scaled.value


def basis_derivatives(basis, frequency):
    frequency = np.asarray(frequency)
    compact = (frequency - basis.pivot) / (frequency + basis.pivot)
    compact_first = 2 * basis.pivot / (frequency + basis.pivot) ** 2
    compact_second = -4 * basis.pivot / (frequency + basis.pivot) ** 3
    values = np.empty(frequency.shape + (basis.count,))
    first = np.zeros_like(values)
    second = np.zeros_like(values)
    values[..., 0] = 1 / basis.norms[0]
    values[..., 1] = (frequency - basis.mean) / basis.norms[1]
    first[..., 1] = 1 / basis.norms[1]
    for degree in range(2, basis.count):
        value = compact * values[..., degree - 1]
        derivative = compact_first * values[..., degree - 1] + compact * first[..., degree - 1]
        curvature = (compact_second * values[..., degree - 1]
                     + 2 * compact_first * first[..., degree - 1] + compact * second[..., degree - 1])
        for repeat in range(2):
            projection = basis.projections[degree, repeat, :degree]
            value -= values[..., :degree] @ projection
            derivative -= first[..., :degree] @ projection
            curvature -= second[..., :degree] @ projection
        values[..., degree] = value / basis.norms[degree]
        first[..., degree] = derivative / basis.norms[degree]
        second[..., degree] = curvature / basis.norms[degree]
    return values, first, second


def pair_curvature(basis, theta, events, index):
    incident = Jet(events["incident"], events["incident_t"], events["incident_tt"])
    outgoing = Jet(events["outgoing"], events["outgoing_t"], events["outgoing_tt"])
    weight = Jet(events["weight"], events["weight_t"], events["weight_tt"])
    temperature = Jet(theta, theta, theta)
    frequency = basis.nodes[index]
    ratio = 1 / (1 + temperature * incident * frequency * (1 - events["cosine"]))
    extra = (1 - ratio) ** 2 / ratio
    final = frequency * incident * ratio * outgoing
    bose = (1 + 1 / final.expm1()) / (1 + 1 / np.expm1(frequency))
    conductance = (basis.measure[index] / 2 * weight * 1.5 * ratio ** 2 * bose
                   * (1 + events["cosine"] ** 2 + extra))
    return final, conductance


def derive():
    assert read(ROOT / "progress.json")["state"] in ["prepared", "curvature_running"]
    assert not (ROOT / "results/frozen-curvature.npz").exists()
    (ROOT / "results").mkdir(exist_ok=True)
    bank, basis, theta = old.setup()
    checks = []
    events, radial_weights, scaled = event_curvature(theta, 6)
    original = old.event_tangent(theta, 6)
    for key in original:
        check(checks, "jet reproduces Stage185 geometry " + key, relative(events[key], original[key]))
    check(checks, "normalized radial weight first derivative sums to zero", radial_weights.first.sum())
    check(checks, "normalized radial weight second derivative sums to zero", radial_weights.second.sum())
    logarithmic = scaled / (1 + scaled) + scaled / (2 * (2 + scaled))
    logarithmic_first = scaled / (1 + scaled) ** 2 + scaled / (2 + scaled) ** 2
    mean = radial_weights.value @ logarithmic
    variance = radial_weights.value @ (logarithmic - mean) ** 2
    predicted_radial_second = radial_weights.value * ((logarithmic - mean) ** 2 + logarithmic_first
                                                    - radial_weights.value @ logarithmic_first - variance)
    check(checks, "independent normalized-weight curvature formula",
          relative(radial_weights.second, predicted_radial_second))
    for step in [1e-4, 5e-5]:
        plus, minus = [old.event_tangent(theta * np.exp(sign * step), 6) for sign in [1, -1]]
        for key in ["incident", "outgoing", "weight"]:
            finite = (plus[key + "_t"] - minus[key + "_t"]) / (2 * step)
            check(checks, f"event second derivative {key} {step}", relative(events[key + "_tt"], finite), .01, "derivative")
    probes = np.geomspace(basis.minimum, basis.maximum, 91)
    values, first, second = basis_derivatives(basis, probes)
    check(checks, "basis values unchanged", relative(values, basis.evaluate(probes)))
    check(checks, "basis first derivative unchanged", relative(first, basis.derivative(probes)))
    for step in [1e-6, 5e-7]:
        finite = (basis.derivative(probes * np.exp(step)) - basis.derivative(probes * np.exp(-step))) / (2 * step * probes[:, None])
        check(checks, f"basis second derivative {step}", relative(second, finite), .01, "derivative")
    assert all(row["passed"] for row in checks), checks
    block, tangent = np.zeros_like(basis.mass), np.zeros_like(basis.mass)
    pieces = np.zeros((4,) + basis.mass.shape)
    masks = []
    began = time.monotonic()
    for index, initial in enumerate(basis.values):
        final, conductance = pair_curvature(basis, theta, events, index)
        inside = (final.value >= basis.minimum) & (final.value <= basis.maximum)
        masks.append(inside)
        values, first, second = basis_derivatives(basis, final.value[inside])
        difference = initial[None, :] - values
        derivative = -first * final.first[inside, None]
        curvature = -(second * final.first[inside, None] ** 2 + first * final.second[inside, None])
        weight, weight_first, weight_second = conductance.value[inside], conductance.first[inside], conductance.second[inside]
        block -= .5 * (difference.T * weight) @ difference
        mixed = (derivative.T * weight) @ difference
        tangent -= .5 * ((difference.T * weight_first) @ difference + mixed + mixed.T)
        pieces[0] -= .5 * (difference.T * weight_second) @ difference
        mixed_first = (derivative.T * weight_first) @ difference
        pieces[1] -= mixed_first + mixed_first.T
        second_basis = (curvature.T * weight) @ difference
        pieces[2] -= .5 * (second_basis + second_basis.T)
        pieces[3] -= (derivative.T * weight) @ derivative
        if (index + 1) % 100 == 0:
            write(ROOT / "progress.json", dict(state="curvature_running", nodes_done=index + 1,
                                               elapsed_seconds=time.monotonic() - began))
    curvature = pieces.sum(axis=0)
    with np.load(PARENT / "results/frozen-tangent.npz") as packet:
        check(checks, "anchor reproduces saved matrix", relative(block, packet["block"]))
        check(checks, "first derivative reproduces saved analytic tangent", relative(tangent, packet["derivative"]))
        assert np.array_equal(np.array(masks), packet["masks"])
        anchor = packet["block"].copy()
        inherited_tangent = packet["derivative"].copy()
    check(checks, "curvature symmetry", relative(curvature.T, curvature))
    check(checks, "curvature photon-number null", np.linalg.norm(curvature @ basis.chemical)
          / (np.linalg.norm(curvature) * np.linalg.norm(basis.chemical)))
    assert all(row["passed"] for row in checks), checks
    predictions = np.array([anchor + offset * inherited_tangent + .5 * offset ** 2 * curvature for offset in OFFSETS])
    np.savez_compressed(ROOT / "results/frozen-curvature.npz", block=anchor, tangent=inherited_tangent,
                        curvature=curvature, parts=pieces, offsets=np.array(OFFSETS), predictions=predictions)
    np.savez_compressed(ROOT / "results/anchor-events.npz", **events)
    write(ROOT / "results/frozen-curvature.json", dict(frozen_at_utc=datetime.now(timezone.utc).isoformat(),
          sha256=saved.digest(ROOT / "results/frozen-curvature.npz"), checks=checks,
          target_values_loaded_in_child=False, targets_previously_seen_in_stage185=True,
          no_fitted_coefficients=True, offsets=OFFSETS, part_names=PARTS,
          curvature_norm=float(np.linalg.norm(curvature)), part_norms=[float(np.linalg.norm(part)) for part in pieces],
          elapsed_seconds=time.monotonic() - began))
    write(ROOT / "progress.json", dict(state="curvature_frozen"))
    print(json.dumps(dict(state="curvature_frozen", checks=len(checks), norm=float(np.linalg.norm(curvature)),
                          elapsed_seconds=time.monotonic() - began)), flush=True)


if __name__ == "__main__":
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "derive"])
    arguments = parser.parse_args()
    dict(prepare=prepare, derive=derive)[arguments.phase]()

