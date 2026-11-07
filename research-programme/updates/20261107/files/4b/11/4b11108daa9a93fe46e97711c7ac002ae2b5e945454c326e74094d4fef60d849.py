import time
from datetime import datetime, timezone
from common import ROOT, CLOSURE, GATE, ALGEBRA, modest, guard, require, check_prior, native_background, other_density, dense_values, read, write, digest, load
import numpy as np
from scipy.integrate import solve_ivp

CASES = [("dop-base", "DOP853", 2e-10, 1.), ("dop-fine", "DOP853", 2e-12, 1.), ("dop-half-cap", "DOP853", 2e-12, .5), ("rk-independent", "RK45", 2e-11, 1.)]


def main():
    modest()
    check_prior()
    frozen = read(ROOT / "input-result.json")
    for path, checksum in frozen["local_sources"].items():
        require(digest(path) == checksum, "changed retained source")
    destination = ROOT / "runs"
    destination.mkdir(exist_ok=False)
    write(ROOT / "run-config.json", dict(created_utc=datetime.now(timezone.utc).isoformat(), cases=CASES, frozen_sha256=digest(ROOT / "input-result.json"), source_sha256=digest(__file__), initial_data_only=True, no_new_parameters=True))
    reports, failure = [], None
    try:
        for owner in frozen["reports"]:
            guard()
            model = owner["model"]
            require(digest(ROOT / "inputs" / owner["input"]) == owner["input_sha256"], "frozen input ownership")
            require(digest(owner["original_parameter_table"]) == owner["original_parameter_sha256"], "background parameters changed")
            packet = load(ROOT / "inputs" / owner["input"])
            efold, units, fields0, masses = packet["efold"], packet["units"], packet["initial_fields"], packet["masses"]
            native = native_background(model)
            model_root = destination / model
            model_root.mkdir()
            last_guard = time.monotonic()
            def rhs(stamp, state):
                nonlocal last_guard
                if time.monotonic() - last_guard > 2:
                    guard()
                    last_guard = time.monotonic()
                scale = np.exp(stamp)
                physical = state * units
                fields = fields0 + physical[[0, 2]]
                velocities = physical[[1, 3]]
                density = np.sum((velocities ** 2 + (scale * masses * fields) ** 2) / 2)
                hubble = np.sqrt((other_density(native, scale)[0] + density) / 3)
                return np.array([velocities[0] / hubble, -2 * velocities[0] - (scale * masses[0]) ** 2 * fields[0] / hubble,
                                 velocities[1] / hubble, -2 * velocities[1] - (scale * masses[1]) ** 2 * fields[1] / hubble, 1 / hubble]) / units
            cases = []
            for tag, method, tolerance, cap_factor in CASES:
                guard()
                started = time.monotonic()
                cap = float(packet["step_cap"]) * cap_factor
                solution = solve_ivp(rhs, (float(efold[0]), float(efold[-1])), packet["initial"], method=method, rtol=tolerance, atol=tolerance / 100, first_step=min(cap / 8, float(efold[-1] - efold[0]) / 128), max_step=cap, dense_output=True)
                write(model_root / (tag + "-status.json"), dict(success=solution.success, message=solution.message, nfev=solution.nfev, last_efold=float(solution.t[-1]), steps=len(solution.t) - 1))
                require(solution.success and np.isfinite(solution.y).all(), "background integration failed")
                segments = solution.sol.interpolants
                continuous = dict(segment_start=np.array([segment.t_old for segment in segments]), segment_end=np.array([segment.t for segment in segments]),
                                  segment_initial=np.array([segment.y_old for segment in segments]), coefficients=np.array([segment.F if method == "DOP853" else segment.Q.T for segment in segments]),
                                  method=np.array(method))
                values, derivatives = dense_values(continuous, efold)
                direct = solution.sol(efold).T
                dense_error = float(np.max(abs(values - direct)) / max(float(np.max(abs(direct))), 1e-80))
                require(dense_error < ALGEBRA, "serialized dense polynomial changed")
                physical = values * units
                rates = derivatives * units
                fields = fields0 + physical[:, [0, 2]]
                velocities = physical[:, [1, 3]]
                scale = np.exp(efold)
                external = other_density(native, scale)
                scalar_density = (velocities ** 2 + (scale[:, None] * masses * fields) ** 2) / 2
                scalar_pressure = (velocities ** 2 - (scale[:, None] * masses * fields) ** 2) / 2
                hubble = np.sqrt((external + scalar_density.sum(axis=1)) / 3)
                path = model_root / (tag + ".npz")
                np.savez_compressed(path, **continuous, efold=efold, units=units, initial_fields=fields0, masses=masses, normalized=values, normalized_derivative=derivatives,
                                    displacements=physical[:, [0, 2]], fields=fields, velocities=velocities, field_efold_derivative=rates[:, [0, 2]], velocity_efold_derivative=rates[:, [1, 3]],
                                    clock_increment=physical[:, 4], clock_efold_derivative=rates[:, 4], times=float(packet["initial_time"]) + physical[:, 4],
                                    a=scale, H=hubble, other_density=external, scalar_density=scalar_density, scalar_pressure=scalar_pressure,
                                    solver_nodes=solution.t, solver_node_states=solution.y.T)
                record = dict(tag=tag, method=method, rtol=tolerance, atol=tolerance / 100, cap_factor=cap_factor, max_step=cap, file=path.name, sha256=digest(path),
                              seconds=time.monotonic() - started, nfev=solution.nfev, steps=len(solution.t) - 1, dense_replay_error=dense_error)
                cases.append(record)
                write(model_root / (tag + ".json"), record)
                print(model, tag, "steps", record["steps"], "seconds", record["seconds"], flush=True)
                del solution, segments, continuous, values, derivatives, direct
            report = dict(model=model, cases=cases, input_sha256=owner["input_sha256"], original_parameter_sha256=owner["original_parameter_sha256"], scalar_initial_data_unchanged=True, future_scalar_reference_used_in_rhs=False)
            reports.append(report)
            write(model_root / "result.json", report)
            del native
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        write(ROOT / "run-result.json", dict(state="complete" if failure is None and len(reports) == 2 else "failed", error=failure, reports=reports, source_sha256=digest(__file__), frozen_sha256=digest(ROOT / "input-result.json"), run_config_sha256=digest(ROOT / "run-config.json"), no_perturbation_rerun=True))


if __name__ == "__main__":
    main()
