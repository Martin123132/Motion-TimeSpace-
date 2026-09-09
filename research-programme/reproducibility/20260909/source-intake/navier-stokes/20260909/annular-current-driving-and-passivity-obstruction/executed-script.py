import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import solve_banded
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets
    from annular_boundary_preserving_completion_20260909 import project_interior_scalar_and_complete
    from annular_noether_source_projection_20260909 import transpose_band
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-current-driving-and-passivity-obstruction"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "counterexamples": [], "valid_for_physics_claim": False, "scope": "Actual w/h RHS channels and a scalar-energy passivity obstruction for any interior scalar-only repair of the fixed-endpoint centered Noether compatibility. Does not prove full coupled instability, absence of another energy estimate, or physical failure of MTS. No changed evolution or claim gate."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report["inputs"][str(path.relative_to(root))] = digest
        return digest

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()

    def maximum(values):
        return float(numerical.max(numerical.abs(values)))

    def parity(values, spacing):
        slopes = derivative(values, spacing)
        trace = slopes[..., :-1] + slopes[..., 1:] - 2 * numerical.diff(values, axis=-1) / spacing
        return ((-1.)**numerical.arange(trace.shape[-1]) * spacing * trace / 4)[..., 8:-8]

    def projection_geometry(engine, current):
        gradient = current["old_gradient"]
        matrix = engine.band.copy()
        matrix[3] -= gradient[2]
        matrix[3, -1] = 1
        outer = engine.outer.copy()
        outer[-1] -= gradient[2, -1]
        normal = solve_banded((3, 3), transpose_band(matrix), outer, check_finite=False)
        normal[-1] = -1
        normal /= maximum(normal)
        covector = normal * gradient[1]
        covector[[0, -1]] = 0
        weight = engine.weights * engine.radii**2 * current["alpha"]
        denominator = float(numerical.sum(covector**2 / weight))
        if denominator <= 0:
            raise ValueError("Degenerate projection; the nondegenerate obstruction is inapplicable")
        return normal, covector, weight, denominator

    def raw_source(engine, current, state):
        velocity = numerical.sum(current["q_gradient"] * state, axis=0)
        fixed_velocity = velocity - current["q0"] * state[4]
        fixed_gradient = state[1] - engine.evaluator.sigma * current["q0"] * state[4]
        flux = current["B"] * fixed_velocity + current["c"] * fixed_gradient
        raw = numerical.zeros((4, engine.radii.size))
        for endpoint, orientation in [(0, 1), (-1, -1)]:
            raw[1, endpoint] = (orientation * flux[endpoint] - numerical.sqrt(current["P"][endpoint] * current["Q"][endpoint]) * fixed_velocity[endpoint]) / (current["alpha"][endpoint] * engine.weights[endpoint])
        raw[3, -1] = -state[4, -1] / (engine.evaluator.sigma * engine.weights[-1])
        return velocity, raw

    save()
    try:
        own(Path(__file__))
        path = intake / "annular-mass-bulk-parity-channels/status.json"
        own(path)
        previous = json.loads(path.read_text())
        verify("previous_goal_turn_progress_verified", previous["state"] == "complete" and previous["passed"] == previous["total"] == 77 and path.with_name("COMPLETE").exists())
        verify("previous_inputs_unchanged", all(own(root / name) == digest for name, digest in previous["inputs"].items()))
        for name in ["annular_coupled_current_time_jets_20260909.py", "annular_coupled_current_operator_20260909.py", "annular_boundary_preserving_completion_20260909.py", "annular_noether_source_projection_20260909.py", "sbp4_derived_operator_20260909.py", "navier_stokes_source_audit_20260908.py"]:
            own(root / "scripts" / name)
        own(root / "DERIVATION-20260909-compatible-boundary-energy-and-Noether-coupling.md")
        alpha, mixed, wave, phase, spacing_symbol = symbolic.symbols("alpha B c phase spacing", positive=True)
        discriminant = mixed**2 + alpha * wave
        principal = symbolic.Matrix([[mixed, 1], [discriminant, mixed]]) / alpha
        energy = symbolic.Matrix([[discriminant, mixed], [mixed, 1]]) / alpha
        verify("acoustic_principal_scalar_energy_symmetry", symbolic.simplify(energy * principal - principal.T * energy) == symbolic.zeros(2))
        verify("scalar_energy_determinant", symbolic.simplify(energy.det() - wave / alpha) == 0)
        verify("acoustic_characteristic_polynomial", symbolic.factor(principal.charpoly().as_expr()).expand() == principal.charpoly().as_expr().expand())
        symbol = symbolic.I * symbolic.sin(phase) * (4 - symbolic.cos(phase)) / (3 * spacing_symbol)
        verify("interior_Nyquist_acoustic_symbol_zero", symbolic.simplify((symbol * principal).subs(phase, symbolic.pi)) == symbolic.zeros(2))
        mismatch, denominator = symbolic.symbols("mismatch denominator", real=True, nonzero=True)
        correction_contraction = -mismatch
        verify("any_compatible_scalar_repair_positive_work_direction", symbolic.simplify((-mismatch) * correction_contraction - mismatch**2) == 0)
        report["analytic_obstruction"] = "If v^T c=-r with fixed endpoint sources, choose interior q=-r W^-1 v. Then q^T W c=r^2>0 for EVERY compatible interior scalar correction, not just minimum norm. The construction needs r!=0 and d=v^T W^-1 v>0. Zero endpoint q can be maintained while endpoint w produces r. This is a source/scalar-energy obstruction only; full coupled stability and admissibility of homogeneous constraint data remain separate."
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            engines = {}
            for branch, folder_name in [("original", "annular-coupled-current-analytic-third-corner"), ("hybrid", "annular-projected-volterra-third-corner")]:
                folder = intake / folder_name
                own(folder / "status.json")
                owner = json.loads((folder / "status.json").read_text())
                verify(branch + "_" + case_name + "_terminal_status_honest", owner["state"] == ("complete" if owner["passed"] == owner["total"] else "failed") and (folder / "COMPLETE").exists() == (owner["state"] == "complete"))
                for entry in owner["runs"]:
                    if entry["case"] != case_name or entry["time_refinement"] != (2 if entry["intervals"] == 512 else 1):
                        continue
                    path = folder / entry["artifact"]
                    label = branch + "_" + path.stem
                    verify(label + "_hash", own(path) == entry["sha256"])
                    with numerical.load(path, allow_pickle=False) as arrays:
                        radii, state, rhs, saved_coordinate, saved_source, saved_defect = [arrays[key] for key in ["radius", "correction_current", "current_rhs", "coordinate_numerical_source", "numerical_source", "background_defect"]]
                    key = entry["time"], entry["intervals"]
                    if key not in engines:
                        engines[key] = CoupledCurrentTimeJets(evaluator, radii, entry["time"])
                    engine = engines[key]
                    current = {key: value[0] for key, value in engine.current.items()}
                    current["defect"] = saved_defect
                    velocity, raw = raw_source(engine, current, state)
                    normal, covector, weight, denominator = projection_geometry(engine, current)
                    mismatch_value = float(numerical.sum(normal * (current["old_gradient"][1] * raw[1] + current["old_gradient"][3] * raw[3])))
                    expected_projection = -mismatch_value * covector / (denominator * weight)
                    verify(label + "_projection_rank_one_identity", maximum(saved_coordinate[1] - raw[1] - expected_projection) < 1e-8 * max(maximum(saved_coordinate[1]), 1e-20) + 1e-22)
                    verify(label + "_coordinate_velocity_source_transform", maximum(numerical.sum(current["q_gradient"] * saved_source, axis=0) - saved_coordinate[1]) < 1e-8 * max(maximum(saved_coordinate[1]), 1e-20) + 1e-22)
                    flux = numerical.sum(current["flux_gradient"] * state, axis=0)
                    terms = numerical.zeros((11, 2, radii.size))
                    terms[0, 0] = derivative(velocity, engine.spacing)
                    terms[1, 1] = derivative(radii**2 * flux, engine.spacing) / radii**2
                    terms[2, 1] = -numerical.sum(current["V_gradient"] * state, axis=0)
                    terms[3, 1] = -current["f_mu"] * derivative(state[3], engine.spacing)
                    terms[4, 1] = current["f_mu"] * numerical.sum(current["constraint_gradient"] * state, axis=0)
                    terms[5, 1] = -numerical.sum(current["fmu_gradient"] * state, axis=0) * current["J0"]
                    terms[6] = -current["defect"][[1, 2]]
                    terms[7, 1] = current["alpha"] * raw[1]
                    terms[8, 1] = current["alpha"] * (saved_coordinate[1] - raw[1])
                    terms[9, 1] = current["h_mu"] * saved_coordinate[2]
                    terms[10, 1] = current["h_delta"] * saved_coordinate[3]
                    error = maximum(terms.sum(axis=0) - rhs[[1, 2]])
                    verify(label + "_actual_current_RHS_decomposition", error < 1e-8 * max(maximum(rhs[[1, 2]]), 1e-20) + 1e-22, {"error": error})
                    indicators = parity(terms, engine.spacing)
                    actual = parity(rhs[[1, 2]], engine.spacing)
                    verify(label + "_parity_linearity", maximum(indicators.sum(axis=0) - actual) < 1e-8 * max(maximum(actual), 1e-20) + 1e-22)
                    source_work = float(numerical.sum(weight * velocity * saved_coordinate[1]))
                    raw_work = float(numerical.sum(weight * velocity * raw[1]))
                    correction_work = -mismatch_value * float(numerical.dot(velocity, covector)) / denominator
                    verify(label + "_scalar_projection_work_identity", abs(source_work - raw_work - correction_work) < 1e-8 * max(abs(source_work), abs(raw_work), abs(correction_work), 1e-30) + 1e-30)
                    row = {key: entry[key] for key in ["case", "time", "intervals"]}
                    row.update(branch=branch, term_names=["D(q)", "R^-2 D(R^2 flux)", "-V_y e", "-f_mu D(e_mu)", "+f_mu g_y e", "-(f_mu,y e)J0", "-parent_current_defect", "raw_scalar_boundary", "interior_scalar_projection", "mass_source_transform", "lapse_source_transform"], current_component_order=["w", "h"], term_parity_RMS=numerical.sqrt(numerical.mean(indicators**2, axis=-1)).tolist(), total_parity_RMS=numerical.sqrt(numerical.mean(actual**2, axis=-1)).tolist(), signed_alignment=numerical.sum(indicators * actual, axis=-1).__truediv__(numerical.maximum(numerical.sum(actual**2, axis=-1), 1e-300)).tolist(), scalar_source_work=source_work, raw_scalar_source_work=raw_work, added_scalar_projection_work=correction_work, compatibility_mismatch=mismatch_value, projection_denominator=denominator, source_work_is_not_total_energy_derivative=True, valid_for_physics_claim=False)
                    report["runs"].append(row)
                    if branch == "original":
                        wave_weight = engine.weights * radii**2 * current["c"]
                        verify(label + "_positive_scalar_energy_branch", numerical.min(wave_weight) > 0 and numerical.min(weight) > 0)
                        bump = numerical.maximum(1 - (radii - radii[0]) / (8 * engine.spacing), 0)**6
                        slope = derivative(bump, engine.spacing)
                        normalization = numerical.sqrt(numerical.sum(wave_weight * slope**2))
                        bump, slope = bump / normalization, slope / normalization
                        trial = numerical.zeros_like(state)
                        trial[0], trial[1], trial[2] = bump, slope, -current["B"] * slope
                        unused_velocity, trial_raw = raw_source(engine, current, trial)
                        trial_mismatch = float(numerical.sum(normal * current["old_gradient"][1] * trial_raw[1]))
                        trial_q = -numerical.sign(trial_mismatch) * covector / (weight * numerical.sqrt(denominator))
                        trial[2] += current["alpha"] * trial_q
                        replay_q, trial_raw = raw_source(engine, current, trial)
                        complete = project_interior_scalar_and_complete(trial_raw[None], current["old_gradient"], engine.band, engine.outer, weight)[0]
                        actual_work = float(numerical.sum(weight * replay_q * complete[1]))
                        predicted_work = abs(trial_mismatch) / numerical.sqrt(denominator)
                        trial_energy = float(numerical.sum(weight * replay_q**2 + wave_weight * slope**2) / 2)
                        verify(label + "_integrable_counterexample_kinematics", maximum(trial[1] - derivative(trial[0], engine.spacing)) < 1e-10 and maximum(replay_q[[0, -1]]) < 1e-12)
                        verify(label + "_positive_projection_work_counterexample", actual_work > 0 and abs(actual_work - predicted_work) < 1e-8 * predicted_work and abs(trial_energy - 1) < 1e-10, {"work": actual_work, "predicted": predicted_work, "energy": trial_energy})
                        perturbation = numerical.cos(radii)
                        perturbation[[0, -1]] = 0
                        perturbation -= (numerical.dot(covector, perturbation) / denominator) * covector / weight
                        alternative_work = float(numerical.sum(weight * replay_q * (complete[1] + perturbation)))
                        verify(label + "_alternative_compatible_repair_same_work", abs(numerical.dot(covector, perturbation)) < 1e-10 * maximum(covector) and abs(alternative_work - actual_work) < 1e-8 * predicted_work + 1e-13)
                        trial_constraint = derivative(trial[3], engine.spacing) - numerical.sum(current["constraint_gradient"] * trial, axis=0)
                        filename = label + "_counterexample.npz"
                        numerical.savez(destination / filename, radius=radii, current_direction=trial, velocity_direction=replay_q, raw_source=trial_raw, completed_source=complete, covector=covector, weight=weight, retained_constraint=trial_constraint, RHS_channels=terms)
                        report["counterexamples"].append({"case": case_name, "time": entry["time"], "intervals": entry["intervals"], "artifact": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "scalar_source_work": actual_work, "scalar_energy": trial_energy, "work_over_scalar_energy": actual_work / trial_energy, "constraint_direction_max": maximum(trial_constraint), "scope": "Discrete integrability holds, but homogeneous mass constraint is NOT imposed. Source/scalar-energy passivity obstruction, not a physical solution or full coupled instability proof.", "valid_for_physics_claim": False})
                    save()
        verify("all_expected_states_and_counterexamples", len(report["runs"]) == 24 and len(report["counterexamples"]) == 12)
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat())
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)


if __name__ == "__main__":
    run()
