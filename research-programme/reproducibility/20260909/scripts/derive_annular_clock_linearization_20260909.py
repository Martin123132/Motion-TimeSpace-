import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import mpmath as multiprecision
    import numpy as numerical
    import sympy as symbolic
    from annular_clock_connection_20260909 import clock_hessian, quadratic_clock_potential
    from annular_clock_linearization_20260909 import clock_covector, clock_field_cross, clock_hessian_matrix, connection_integration, connection_metric_jets
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_gram_joint_action_20260909 import coefficient_jets, gram_matrices, principal_coefficient

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-clock-linearized-coupling-derived"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "samples": [], "high_precision_controls": [], "valid_for_physics_claim": False, "scope": "Clock-clock, field-clock and isolated face-geometry chain-rule Hessian blocks of the proposed action germ. Not a completed mixed-grid gravity action or evolution. Clock Hessian eigenvalues are potential/coupling diagnostics, not a kinetic stability test. Higher-precision temporal remainder controls use frozen Float64 discrete coefficients and exact rational parent-profile expressions; still not directed-rounding interval certificates."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report["inputs"][str(path.relative_to(root))] = digest
        return digest

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()
        print(name + ": " + str(bool(condition)), flush=True)

    def maximum(values):
        return float(numerical.max(numerical.abs(values)))

    def mp_profile(case):
        advanced, radius = symbolic.symbols("v r", real=True)
        expression = symbolic.S.Zero
        bound_terms = []
        epsilon = symbolic.Rational(1, 10)
        for order, harmonics in case["fields"]["scalar_ref"].items():
            for key, coefficient in harmonics.items():
                mode = int(key[3:])
                amplitude = epsilon**int(order) * symbolic.sympify(coefficient, locals={"v": advanced, "r": radius})
                phase = mode * advanced / epsilon
                expression += amplitude * (symbolic.cos(phase) if key[:3] == "cos" else symbolic.sin(phase))
                for differentiated in range(4):
                    polynomial = symbolic.Poly(symbolic.diff(amplitude, advanced, differentiated), advanced)
                    for powers, value in polynomial.terms():
                        bound_terms.append((math.comb(3, differentiated) * (10 * mode)**(3 - differentiated), powers[0], symbolic.lambdify(radius, value, "mpmath", cse=True, docstring_limit=0)))
        functions = [symbolic.lambdify((advanced, radius), symbolic.diff(expression, advanced, order), "mpmath", cse=True, docstring_limit=0) for order in range(3)]
        return functions, bound_terms

    def high_precision(arrays, time_value, clock_size, functions, bound_terms, digits):
        with multiprecision.workdps(digits):
            radii = [multiprecision.mpf(float(value)) for value in arrays["radius"]]
            coefficient = [multiprecision.mpf(float(value)) for value in arrays["coefficient"]]
            spacing = radii[1] - radii[0]
            factors, sampling = gram_matrices(len(radii))
            clock_double = clock_size * (numerical.sin(1.3 * arrays["radius"]) + 0.2 * numerical.cos(2.1 * arrays["radius"]))
            clocks = [multiprecision.mpf(float(value)) for value in clock_double]
            advanced = [multiprecision.mpf(float(time_value)) + multiprecision.mpf(1) / 20 * (radius - 4) for radius in radii]
            scalar = [functions[0](time, radius) for time, radius in zip(advanced, radii)]
            velocity = [functions[1](time, radius) for time, radius in zip(advanced, radii)]
            acceleration = [functions[2](time, radius) for time, radius in zip(advanced, radii)]
            offsets_max = [multiprecision.mpf(0) for unused in radii]
            rows = []
            for row in range(factors.shape[0]):
                coefficient_indices = numerical.flatnonzero(sampling[row])
                weighted = [(int(index), multiprecision.mpf(float(sampling[row, index])) * coefficient[index]) for index in coefficient_indices]
                total_coefficient = sum(value for index, value in weighted)
                center = sum(value * clocks[index] for index, value in weighted) / total_coefficient
                entries = []
                for index in numerical.flatnonzero(factors[row]):
                    offset = clocks[index] - center
                    offsets_max[index] = max(offsets_max[index], abs(offset))
                    entries.append((int(index), multiprecision.mpf(float(factors[row, index])), offset))
                rows.append((total_coefficient, entries))
            third_bounds = []
            for time, radius, offset in zip(advanced, radii, offsets_max):
                third_bounds.append(sum(factor * abs(evaluator(radius)) * (abs(time) + offset)**degree for factor, degree, evaluator in bound_terms))
            exact_total = multiprecision.mpf(0)
            quadratic_total = multiprecision.mpf(0)
            bound_total = multiprecision.mpf(0)
            for weight, entries in rows:
                leading = sum(factor * scalar[index] for index, factor, offset in entries)
                first = -sum(factor * offset * velocity[index] for index, factor, offset in entries)
                second = sum(factor * offset**2 * acceleration[index] for index, factor, offset in entries) / 2
                remainder = sum(abs(factor) * abs(offset)**3 * third_bounds[index] for index, factor, offset in entries) / 6
                exact = sum(factor * functions[0](advanced[index] - offset, radii[index]) for index, factor, offset in entries)
                exact_total += weight * exact**2 / (2 * spacing)
                quadratic_total += weight * (leading**2 + 2 * leading * first + first**2 + 2 * leading * second) / (2 * spacing)
                bound_total += weight * (2 * abs(first * second) + second**2 + 2 * abs(leading + first + second) * remainder + remainder**2) / (2 * spacing)
            error = abs(exact_total - quadratic_total)
            return {"digits": digits, "absolute_error": multiprecision.nstr(error, 45), "analytic_bound": multiprecision.nstr(bound_total, 45), "error_over_bound": multiprecision.nstr(error / bound_total, 45), "bound_holds_without_float_allowance": bool(error <= bound_total)}

    save()
    try:
        own(Path(__file__))
        own(root / "scripts/annular_clock_linearization_20260909.py")
        prior_path = intake / "annular-clock-coframe-current-derived/status.json"
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify("clock_coframe_owner_complete", prior["state"] == "complete" and prior["passed"] == prior["total"] == 308 and prior_path.with_name("COMPLETE").exists())
        verify("clock_coframe_inputs_unchanged", all(own(root / name) == digest for name, digest in prior["inputs"].items()))
        evaluators, cases, saved = {}, {}, {}
        for entry in prior["samples"]:
            path = prior_path.parent / entry["artifact"]
            tag = path.stem
            verify(tag + "_array_hash", own(path) == entry["sha256"])
            with numerical.load(path, allow_pickle=False) as loaded:
                arrays = {key: loaded[key] for key in loaded.files}
            saved[entry["case"], entry["intervals"], entry["time"]] = arrays
            if entry["case"] not in evaluators:
                case_path = intake / "annular-constraint-correction-initial" / (entry["case"] + ".json")
                own(case_path)
                cases[entry["case"]] = json.loads(case_path.read_text())
                evaluators[entry["case"]] = AnnularFields(cases[entry["case"]])
            evaluator = evaluators[entry["case"]]
            radii = arrays["radius"]
            spacing = float(radii[1] - radii[0])
            scalar, velocity, acceleration, coefficient = [arrays[key] for key in ["scalar", "velocity", "acceleration", "coefficient"]]
            full_hessian = clock_hessian_matrix(scalar, velocity, acceleration, coefficient, spacing)
            scale = max(maximum(full_hessian), 1e-25)
            verify(tag + "_complete_clock_matrix_symmetric", maximum(full_hessian - full_hessian.T) < 1e-10 * scale)
            verify(tag + "_constant_clock_null_direction", maximum(full_hessian @ numerical.ones_like(radii)) < 1e-9 * scale)
            first_clock, second_clock = numerical.sin(1.3 * radii), numerical.cos(0.7 * radii)
            expected = clock_hessian(scalar, velocity, acceleration, coefficient, first_clock, second_clock, spacing)
            verify(tag + "_matrix_matches_independent_bilinear", abs(numerical.dot(first_clock, full_hessian @ second_clock) - expected) < 1e-8 * max(abs(expected), scale, 1e-25))
            snapshot = evaluator.evaluate(numerical.full_like(radii, entry["time"]), radii, 0.1)
            state = snapshot["state"][0]
            primitive = numerical.stack([state[0], state[1], snapshot["state_space"][0, 0], state[2], state[3], numerical.zeros_like(radii)])
            unused_coefficient, coefficient_gradient, unused_hessian = coefficient_jets(primitive, radii, evaluator.constants, evaluator.sigma)
            cross_columns = []
            for component in range(6):
                variation = numerical.zeros_like(primitive)
                variation[component] = 0.1 * numerical.sin((component + 0.7) * radii)
                coefficient_variation = numerical.sum(coefficient_gradient * variation[1:], axis=0)
                expected = clock_field_cross(scalar, velocity, coefficient, variation[0], variation[1], coefficient_variation, spacing)
                varied = primitive.astype(complex) + 1j * 1e-25 * variation
                varied_coefficient = principal_coefficient(varied, radii, evaluator.constants, evaluator.sigma)
                measured = clock_covector(scalar + 1j * 1e-25 * variation[0], velocity + 1j * 1e-25 * variation[1], varied_coefficient, spacing).imag / 1e-25
                verify(tag + "_independent_field_clock_block_" + str(component), maximum(measured - expected) < 1e-8 * max(maximum(measured), maximum(expected), 1e-25) + 1e-22)
                cross_columns.append(expected)
            integration = connection_integration(numerical.diff(radii))
            face_radii, face_exponential = arrays["face_radius"], arrays["face_exponential"]
            face_lapse = 1 / (face_exponential * (evaluator.sigma - arrays["connection"]))
            metric_gradient, metric_hessian = connection_metric_jets(face_exponential, face_lapse, face_radii)
            metric_first = numerical.stack([0.1 * numerical.cos(face_radii), 0.03 * numerical.sin(2 * face_radii)])
            metric_second = numerical.stack([0.07 * numerical.sin(1.5 * face_radii), 0.02 * numerical.cos(0.6 * face_radii)])
            first_connection = numerical.sum(metric_gradient * metric_first, axis=0)
            second_connection = numerical.sum(metric_gradient * metric_second, axis=0)
            mixed_connection = numerical.einsum("ijn,in,jn->n", metric_hessian, metric_first, metric_second)
            main_term = float(numerical.dot(integration @ first_connection, full_hessian @ (integration @ second_connection)))
            chain_term = float(numerical.dot(arrays["edge_covector"], mixed_connection))
            expected = main_term + chain_term
            errors = []
            for step in [0.001, 0.0005]:
                values = []
                for first_sign, second_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    change = step * (first_sign * metric_first + second_sign * metric_second)
                    changed_exponential = face_exponential * numerical.exp(change[1])
                    changed_lapse = face_lapse - 2 * change[0] / face_radii
                    changed_connection = evaluator.sigma - 1 / (changed_exponential * changed_lapse)
                    clock = integration @ (changed_connection - arrays["connection"])
                    values.append(quadratic_clock_potential(scalar, velocity, acceleration, coefficient, clock, spacing))
                measured = (values[0] - values[1] - values[2] + values[3]) / (4 * step**2)
                tolerance = 1e-4 * max(abs(main_term), abs(chain_term), 1e-25) + 256 * numerical.finfo(float).eps * max(abs(value) for value in values) / step**2
                errors.append(float(abs(measured - expected)))
                verify(tag + "_metric_Hessian_includes_connection_curvature_" + str(step), abs(measured - expected) <= tolerance)
            eigenvalues = numerical.linalg.eigvalsh((full_hessian + full_hessian.T) / 2)
            artifact = destination / (tag + "_linearization.npz")
            numerical.savez_compressed(artifact, radius=radii, clock_clock_Hessian=full_hessian, clock_field_directional_columns=numerical.stack(cross_columns), connection_integration=integration, connection_metric_gradient=metric_gradient, connection_metric_Hessian=metric_hessian)
            report["samples"].append({"case": entry["case"], "intervals": entry["intervals"], "time": entry["time"], "artifact": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "minimum_clock_potential_eigenvalue": float(eigenvalues[0]), "maximum_clock_potential_eigenvalue": float(eigenvalues[-1]), "metric_hessian_main_term": main_term, "metric_hessian_second_connection_term": chain_term, "metric_hessian_FD_errors": errors, "kinetic_stability_claim": False, "valid_for_physics_claim": False})
            save()
        for case_name in cases:
            functions, bound_terms = mp_profile(cases[case_name])
            controls = [(entry, check) for entry in prior["samples"] if entry["case"] == case_name for check in entry["remainder_checks"]]
            selected = [max(controls, key=lambda pair: pair[1]["error"] / pair[1]["analytic_bound"]), min(controls, key=lambda pair: pair[1]["analytic_bound"])]
            for selection, (entry, check) in zip(["worst_observed_ratio", "smallest_analytic_bound"], selected):
                arrays = saved[case_name, entry["intervals"], entry["time"]]
                control = {"case": case_name, "intervals": entry["intervals"], "time": entry["time"], "selection": selection, "clock_amplitude": check["clock_amplitude"], "results": []}
                for digits in [60, 90]:
                    result = high_precision(arrays, entry["time"], check["clock_amplitude"], functions, bound_terms, digits)
                    control["results"].append(result)
                    verify(case_name + "_" + selection + "_remainder_without_allowance_" + str(digits), result["bound_holds_without_float_allowance"])
                with multiprecision.workdps(95):
                    first = multiprecision.mpf(control["results"][0]["absolute_error"])
                    second = multiprecision.mpf(control["results"][1]["absolute_error"])
                    verify(case_name + "_" + selection + "_60vs90_digit_agreement", abs(first - second) < multiprecision.mpf("1e-35") * max(abs(first), abs(second)))
                control["interval_certified"] = False
                report["high_precision_controls"].append(control)
                save()
        verify("all18_linearizations_and4_extremal_precision_controls", len(report["samples"]) == 18 and len(report["high_precision_controls"]) == 4)
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        for path in [Path(__file__), root / "scripts/annular_clock_linearization_20260909.py"]:
            compile(path.read_bytes(), str(path), "exec")
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        save()
        raise
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
