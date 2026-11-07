import csv
from common import ROOT, SECOND, ALGEBRA, GATE, modest, guard, require, read, write, digest, check_parent
from mean_math import *
import numpy as np


def relative(left, right):
    return sup(left - right) / norm(right)


def repeat(values, count):
    return {name: np.repeat(value, count, axis=0) for name, value in values.items()}


def physical_phase_checks(provider, points, wave):
    original, mean, cosine, sine = phase_background(provider, points)
    lifted = phased(mean, cosine, sine, original["phase"])
    reference = transform(original, wave, include_fast=False)
    continuum = transform(lifted, wave, include_fast=False)
    checks = dict(native_continuum_hessian=relative(continuum["hessian"], reference["hessian"]),
                  native_continuum_map=relative(continuum["transform"], reference["transform"]))
    diagnostics = dict(native_continuum_derivative=relative(continuum["rate"], reference["rate"]),
                       hlog=relative(lifted["hlog"], original["hlog"]),
                       mu_rate=relative(lifted["mu_rate"], original["mu_rate"]),
                       amplitude_rate=relative(lifted["background_rate"], original["background_rate"]))
    return original, mean, cosine, sine, reference, checks, diagnostics


def family_coefficients(provider, points, wave):
    original, mean, cosine, sine, native, checks, diagnostics = physical_phase_checks(provider, points, wave)
    hessian, exponent, exponent_rate, units = polynomials(mean, cosine, sine, wave)
    orders = action_orders(hessian, exponent, exponent_rate)
    constraint = constraint_polynomial(mean, wave, units)
    constraint_orders = [product(constraint, order["coordinate_map"]) for order in orders]
    phases = original["phase"]
    checks["generator_reconstruction"] = relative(evaluate(exponent, phases), JFULL @ generator(phased(mean, cosine, sine, phases), wave)[1] * units[:, :, None] * units[:, None, :])
    checks.pop("generator_reconstruction")
    full_generator = generator(phased(mean, cosine, sine, phases), wave)
    hscale = units[:, :, None] * units[:, None, :]
    checks["hessian_polynomial"] = relative(evaluate(hessian, phases), full_generator[0] * hscale)
    checks["exponent_polynomial"] = relative(evaluate(exponent, phases), JFULL @ (full_generator[1] * hscale))
    checks["derivative_polynomial"] = relative(evaluate(exponent_rate, phases), JFULL @ (full_generator[2] * hscale))
    checks["conjugate_reality"] = max(relative(value.conjugate(), exponent[-harmonic]) for harmonic, value in exponent.items())
    averages = {}
    truncation = []
    for count in (32, 64):
        guard()
        angles = np.tile(2 * np.pi * np.arange(count) / count, len(points))
        phase_mean, phase_cos, phase_sin = [repeat(item, count) for item in (mean, cosine, sine)]
        data = transform(phased(phase_mean, phase_cos, phase_sin, angles), wave)
        balancing = data["balance"]
        hessian_balanced = data["hessian"] * balancing[:, :, None] * balancing[:, None, :]
        matrix, rate = data["transform"], data["rate"]
        exact_hessian = transpose(matrix) @ hessian_balanced @ matrix + transpose(matrix) @ JFULL @ rate
        exact_source = transpose(matrix)
        phase_constraint = evaluate({key: np.repeat(value, count, axis=0) for key, value in constraint.items()}, angles)
        exact_constraint = phase_constraint @ matrix
        average = dict(hessian=exact_hessian.reshape(len(points), count, 8, 8).mean(axis=1),
                       source=exact_source.reshape(len(points), count, 8, 8).mean(axis=1),
                       constraint=exact_constraint.reshape(len(points), count, 2, 8).mean(axis=1))
        averages[count] = average
        for order_index, order in enumerate(orders):
            approximate = evaluate({key: np.repeat(value, count, axis=0) for key, value in order["hessian"].items()}, angles)
            source_map = evaluate({key: np.repeat(value, count, axis=0) for key, value in order["source_map"].items()}, angles)
            constraint_map = evaluate({key: np.repeat(value, count, axis=0) for key, value in constraint_orders[order_index].items()}, angles)
            for name, polynomial, phase_values in (("hessian", order["hessian"], approximate), ("source", order["source_map"], source_map),
                                                    ("constraint", constraint_orders[order_index], constraint_map)):
                shape = phase_values.shape[-2:]
                mean_value = phase_values.reshape(len(points), count, *shape).mean(axis=1)
                checks["order" + str(order_index) + "_" + name + "_phase" + str(count)] = relative(polynomial.get(0, np.zeros_like(mean_value)), mean_value)
            if count == 64:
                truncation.append(dict(order=order_index, instantaneous_hessian=relative(approximate, exact_hessian),
                                       mean_hessian=relative(order["hessian"][0], average["hessian"]),
                                       mean_source=relative(order["source_map"][0], average["source"]),
                                       mean_constraint=relative(constraint_orders[order_index][0], average["constraint"])))
    for name in ("hessian", "source", "constraint"):
        checks["exact_mean_phase_refinement_" + name] = relative(averages[32][name], averages[64][name])
    for index, order in enumerate(orders):
        value = order["hessian"][0]
        checks["order" + str(index) + "_mean_symmetry"] = relative(value, transpose(value))
        checks["order" + str(index) + "_mean_reality"] = sup(value.imag) / norm(value)
    frozen_exponent_rate = {key: JFULL @ value for key, value in hessian.items() if key != 0}
    frozen_orders = action_orders(hessian, exponent, frozen_exponent_rate)
    diagnostics["frozen_derivative_mean_hessian_difference"] = relative(frozen_orders[2]["hessian"][0], orders[2]["hessian"][0])
    diagnostics["truncations"] = truncation
    diagnostics["highest_harmonics"] = [max(abs(key) for key in order["hessian"]) for order in orders]
    candidate = orders[2]
    npz = dict(points=points, units=units, native_transform=native["transform"], native_rate=native["rate"],
               mean_hessian=candidate["hessian"][0].real, mean_source=candidate["source_map"][0].real,
               mean_constraint=constraint_orders[2][0].real,
               exact_mean_hessian=averages[64]["hessian"].real, exact_mean_source=averages[64]["source"].real,
               exact_mean_constraint=averages[64]["constraint"].real)
    for index, order in enumerate(orders):
        npz["order" + str(index) + "_hessian"] = order["hessian"][0].real
        npz["order" + str(index) + "_source"] = order["source_map"][0].real
    return npz, checks, diagnostics


def state_checks(packet, wave, model, probes, tables):
    extracted = joint_extractor()[0](packet, wave, model)
    checks = dict(extracted["checks"])
    if model == "cold":
        return checks, dict(identity=True, zero=not np.any(extracted["state"]), candidate_qualified=True)
    units, matrix = tables["units"], tables["native_transform"]
    state = extracted["state"][probes] / units
    inverse = -JFULL @ transpose(matrix) @ JFULL
    transformed = multiply(inverse, state)
    source = extracted["linear"][probes] * units
    reference = multiply(JFULL, multiply(tables["exact_mean_hessian"], transformed) + multiply(tables["exact_mean_source"], source))
    scales = np.maximum(np.max(abs(reference), axis=0), 1e-80)
    errors = []
    for index in range(4):
        response = multiply(JFULL, multiply(tables["order" + str(index) + "_hessian"], transformed)
                            + multiply(tables["order" + str(index) + "_source"], source))
        component = np.max(abs(response - reference), axis=0) / scales
        errors.append(dict(order=index, components=component.tolist(), maximum=float(np.max(component))))
    checks["source_map_roundtrip"] = relative(units * multiply(matrix, transformed), extracted["state"][probes])
    return checks, dict(identity=False, zero=not np.any(extracted["state"]), force_truncation_errors=errors,
                        candidate_qualified=errors[2]["maximum"] < GATE, source_scope="rest variables held fixed in fast-phase projection, not saved future rest forcing in a prediction")


def main():
    modest()
    check_parent()
    frozen = {str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")}
    write(ROOT / "frozen-inputs.json", dict(sources=frozen, orders=[0, 1, 2, 3], intended_order=2, phases=[32, 64], algebra=ALGEBRA, numerical=GATE))
    provider = Background("heavy")
    anchors = np.unique(np.linspace(0, len(provider.efold) - 1, 33, dtype=int))
    extra = np.array([first + max(1, int(.37 * (second - first))) for first, second in zip(anchors[:-1], anchors[1:])])
    probes = np.unique(np.r_[anchors, extra])
    points = provider.efold[probes]
    owner = read(SECOND / "prediction-result.json")
    (ROOT / "profiles").mkdir(exist_ok=False)
    (ROOT / "records").mkdir(exist_ok=False)
    families, histories = [], []
    for family in owner["reports"]:
        guard()
        tables = None
        name = family["model"] + "-" + family["label"]
        if family["model"] == "heavy":
            tables, checks, diagnostics = family_coefficients(provider, points, family["wave"])
            passed = all(np.isfinite(value) and 0 <= value < ALGEBRA for value in checks.values())
            native_ok = diagnostics["native_continuum_derivative"] < GATE
            candidate_ok = max(diagnostics["truncations"][2][key] for key in ("instantaneous_hessian", "mean_hessian", "mean_source", "mean_constraint")) < GATE
            profile = ROOT / "profiles" / (name + ".npz")
            np.savez_compressed(profile, indices=probes, **tables)
            report = dict(family=name, wave=family["wave"], checks=checks, diagnostics=diagnostics,
                          profile=str(profile), sha256=digest(profile), passed=bool(passed and native_ok and candidate_ok))
            families.append(report)
            print(name, "algebra", max(checks.values()), "native derivative", diagnostics["native_continuum_derivative"],
                  "truncations", diagnostics["truncations"], "passed", report["passed"], flush=True)
        for case in family["cases"]:
            guard()
            path = SECOND / "runs-second" / name / case["file"]
            require(digest(path) == case["sha256"], "saved history changed")
            packet = load(path)
            checks, diagnostics = state_checks(packet, family["wave"], family["model"], probes, tables)
            passed = all(np.isfinite(value) and 0 <= value < ALGEBRA for value in checks.values()) and diagnostics["candidate_qualified"]
            row = dict(family=name, tag=case["tag"], input=str(path), sha256=case["sha256"], checks=checks, diagnostics=diagnostics, passed=bool(passed))
            write(ROOT / "records" / (name + "-" + case["tag"] + ".json"), row)
            histories.append(row)
            print(name, case["tag"], "passed", row["passed"], diagnostics.get("force_truncation_errors", []), flush=True)
            del packet
    check_parent()
    passed = all(row["passed"] for row in families + histories)
    write(ROOT / "result.json", dict(state="complete", passed=passed, families=families, histories=histories,
          anchors=len(anchors), interior_probes=len(extra), intended_order=2, algebra=ALGEBRA, numerical=GATE,
          coefficient_derivation="finite Laurent convolution with correlated background derivative",
          new_trajectories=0, closed_cosmological_mean_forward_qualified=False))
    with (ROOT / "summary.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["family", "case", "algebra", "order2_force_error", "passed"])
        for row in histories:
            errors = row["diagnostics"].get("force_truncation_errors")
            writer.writerow([row["family"], row["tag"], max(row["checks"].values()), errors[2]["maximum"] if errors else 0, row["passed"]])
    print("Complete; candidate algebra/action-order qualification", passed, flush=True)


if __name__ == "__main__":
    main()
