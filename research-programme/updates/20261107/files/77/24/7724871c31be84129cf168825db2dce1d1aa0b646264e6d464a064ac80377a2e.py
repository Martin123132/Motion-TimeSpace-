from smooth_stage187 import *


def curvature(values):
    with mp.workdps(80):
        samples = [mp.mpf(float(value)) for value in values]
        coarse = (samples[1] - 2 * samples[0] + samples[2]) * 10000
        fine = (samples[3] - 2 * samples[0] + samples[4]) * 40000
        return np.array([float(coarse), float(fine), float(coarse - fine)])


def assess():
    assert not (ROOT / "results/assessment.json").exists()
    frozen_candidate()
    checks = list(read(ROOT / "results/structure.json")["checks"])
    for index in range(2):
        checks.extend(read(ROOT / "edges" / str(index) / "status.json")["checks"])
    curves = np.zeros((2, 2, 3, 3))
    samples = np.zeros((2, 2, 3, 5))
    histories = {}
    updates = 0
    for model_index, model in enumerate(MODELS):
        for grid_index, grid in enumerate(GRIDS):
            directory = ROOT / "histories" / model / grid
            status = read(directory / "status.json")
            assert status["state"] == "complete"
            assert saved.digest(directory / "history.npz") == status["history_sha256"]
            checks.extend(status["checks"])
            updates += status["updates"]
            candidate_history = packet(directory / "history.npz")
            bank_history = corner.history(model, grid)
            for name in ["expansion", "coordinates", "initial_profile", "initial_previous_profile", "initial_gas", "initial_previous_gas"]:
                assert np.array_equal(candidate_history[name], bank_history[name]), name
            histories[(model, grid)] = candidate_history
            for kind_index, gas in enumerate([bank_history["temperature_scaled"], candidate_history["candidate_gas"]]):
                samples[model_index, kind_index, grid_index] = np.interp(bank_history["coordinates"], bank_history["expansion"], gas)
                curves[model_index, kind_index, grid_index] = curvature(samples[model_index, kind_index, grid_index])
            delta_samples = np.interp(bank_history["coordinates"], bank_history["expansion"], candidate_history["bank_minus_candidate_gas"])
            delta_curvature = curvature(delta_samples)
            discrepancy = curves[model_index, 0, grid_index] - curves[model_index, 1, grid_index] - delta_curvature
            stencil_weights = np.array([[-20000, 10000, 10000, 0, 0],
                                        [-80000, 0, 0, 40000, 40000],
                                        [60000, 10000, 10000, -40000, -40000]])
            condition_scales = np.sum(abs(stencil_weights), axis=1) * max(abs(samples[model_index, :, grid_index]).ravel())
            check(checks, model + "/" + grid + ": condition-scaled curvature reconstruction", max(abs(discrepancy) / condition_scales))
    inherited = packet(corner.prior.ROOT / "results/history-curvature.npz")
    assert np.array_equal(curves[:, 0], inherited["curves"][:, [0, 1, 4]])
    check(checks, "saved native/half/quarter bank curvatures reproduced bitwise", 0)
    comparison, bank_changes, split_rows = [], [], []
    for model_index, model in enumerate(MODELS):
        for kind_index, kind in enumerate(KINDS):
            for quantity_index, quantity in enumerate(QUANTITIES):
                values = curves[model_index, kind_index, :, quantity_index]
                for coarse_index in [0, 1]:
                    relative = abs((values[coarse_index + 1] - values[coarse_index]) / values[coarse_index + 1])
                    check(checks, f"{model}:{kind}:{GRIDS[coarse_index]}/{GRIDS[coarse_index+1]}:{quantity}",
                          relative, .01, "step_comparison")
                    comparison.append(dict(model=model, kind=kind, coarse_grid=GRIDS[coarse_index], fine_grid=GRIDS[coarse_index + 1],
                                           quantity=quantity, relative_change=float(relative), passed=bool(relative <= .01),
                                           coarse_value=float(values[coarse_index]), fine_value=float(values[coarse_index + 1])))
                coarse_history, fine_history = histories[(model, "half")], histories[(model, "quarter")]
                assert np.array_equal(fine_history["expansion"][::2], coarse_history["expansion"])
                gas = (corner.history(model, "quarter")["temperature_scaled"] if kind == "bank" else fine_history["candidate_gas"])
                thinned = curvature(np.interp(fine_history["coordinates"], fine_history["expansion"][::2], gas[::2]))
                total = values[2] - values[1]
                evolution = thinned[quantity_index] - values[1]
                sampling = values[2] - thinned[quantity_index]
                check(checks, model + ":" + kind + ":" + quantity + ": evolution/sampling split",
                      (total - evolution - sampling) / max(abs(values[2]), 1e-300))
                split_rows.append(dict(model=model, kind=kind, quantity=quantity, total=float(total),
                                       common_node_evolution=float(evolution), sampling=float(sampling)))
        for grid_index, grid in enumerate(GRIDS):
            bank_curves, new_curves = curves[model_index, :, grid_index]
            bank_changes.append(dict(model=model, grid=grid, bank=bank_curves.tolist(), candidate=new_curves.tolist(),
                                     width_discrepancy_reduction_fraction=float(1 - abs(new_curves[2] / bank_curves[2])),
                                     bank_width_over_fine=float(abs(bank_curves[2] / bank_curves[1])),
                                     candidate_width_over_fine=float(abs(new_curves[2] / new_curves[1])),
                                     fine_curvature_relative_change=float(abs((new_curves[1] - bank_curves[1]) / bank_curves[1]))))
    kernels_path = old.ROOT / "results/gas-responses.npz"
    kernels_packet = packet(kernels_path)
    kernels, components = kernels_packet["kernels"], list(kernels_packet["components"])
    assert np.array_equal(kernels, packet(PARENT / "results/gas-responses.npz")["kernels"])
    check(checks, "36-event summed kernels reused bitwise", 0)
    factor = linear.cholesky(packet(source.ROOT / "results/preparation/basis.npz")["mass"], lower=True)

    def norm(vector):
        return float(np.linalg.norm(linear.solve_triangular(factor, vector[1:97], lower=True)))

    responses = np.empty((2, 3, 3, 6, 98, 4))
    for kind_index, grid_index, quantity_index, component, column in np.ndindex(2, 3, 3, 6, 4):
        responses[kind_index, grid_index, quantity_index, component, :, column] = (
            curves[column // 2, kind_index, grid_index, quantity_index] * kernels[component, :, column])
    response_rows = []
    for kind_index, kind in enumerate(KINDS):
        for component in [0, 4, 5]:
            for quantity_index, quantity in enumerate(QUANTITIES):
                for column in range(4):
                    fine = responses[kind_index, 2, quantity_index, component, :, column]
                    coarse = responses[kind_index, 1, quantity_index, component, :, column]
                    relative = norm(fine - coarse) / norm(fine)
                    gas_values = curves[column // 2, kind_index, :, quantity_index]
                    expected = abs((gas_values[2] - gas_values[1]) / gas_values[2])
                    check(checks, f"{kind}:{components[component]}:{column}:{quantity}: gas-source fraction", relative - expected)
                    check(checks, f"{kind}:{components[component]}:{column}:{quantity}: half/quarter source",
                          relative, .01, "source_step_comparison")
                    response_rows.append(dict(kind=kind, component=str(components[component]), column=column, quantity=quantity,
                                              relative_change=relative, passed=relative <= .01, quarter_norm=norm(fine)))
    for kind_index, grid_index, quantity_index, component, column in np.ndindex(2, 3, 3, 6, 4):
        vector = responses[kind_index, grid_index, quantity_index, component, :, column]
        check(checks, f"{kind_index}:{grid_index}:{quantity_index}:{component}:{column}: source energy exchange",
              (vector[0] + vector[-1]) / max(abs(vector[0]), abs(vector[-1]), 1e-300))
    for kind_index, grid_index, quantity_index, column in np.ndindex(2, 3, 3, 4):
        array = responses[kind_index, grid_index, quantity_index, :, :, column]
        check(checks, f"{kind_index}:{grid_index}:{quantity_index}:{column}: matched kernel closure",
              norm(array[4] - array[1] - array[2] - array[3]) / norm(array[4]))
        check(checks, f"{kind_index}:{grid_index}:{quantity_index}:{column}: total kernel closure",
              norm(array[5] - array[0] - array[4]) / norm(array[5]))
    comparison_payload = dict(curves=curves, samples=samples, responses=responses,
                              kernels=kernels, components=np.array(components), models=np.array(MODELS),
                              grids=np.array(GRIDS), kinds=np.array(KINDS), quantities=np.array(QUANTITIES))
    comparison_path = ROOT / "results/comparison.npz"
    if comparison_path.exists():
        previous_payload = packet(comparison_path)
        assert all(np.array_equal(previous_payload[key], value) for key, value in comparison_payload.items())
    else:
        np.savez_compressed(comparison_path, **comparison_payload)
    controls = read(PARENT / "results/saved-baseline-controls.json")
    controls_path = ROOT / "results/saved-baseline-controls.json"
    if controls_path.exists():
        assert read(controls_path) == controls
    else:
        write(controls_path, controls)
    assert saved.digest(PARENT / "results/saved-baseline-controls.json") == read(ROOT / "authenticated-inputs.json")[str(PARENT / "results/saved-baseline-controls.json")]
    check(checks, "old full-source gate decision retained without retest", 0)
    failed = [row for row in checks if not row["passed"]]
    write(ROOT / "results/assessment.json", dict(checks=checks, failed_checks=failed, comparison=comparison,
          operator_changes=bank_changes, evolution_sampling=split_rows, source_rows=response_rows,
          updates=updates, solves=updates, reused_gas_events=36, new_source_integrations=0,
          original_source_decisions=controls,
          scope="Photon and gas histories evolved together in the existing reduced model; microscopic source response remains a fixed-anchor gas-only projection"))
    write(ROOT / "progress.json", dict(state="assessed"))
    print(json.dumps(dict(check_count=len(checks), failed=failed, operator_changes=bank_changes,
                          candidate_quarter_checks=[row for row in comparison if row["kind"] == "candidate" and row["fine_grid"] == "quarter"])), flush=True)


def validate():
    assert read(ROOT / "progress.json")["state"] == "assessed"
    assert not (ROOT / "results/status.json").exists()
    config = read(ROOT / "configuration.json")
    paths = authenticate()
    assert paths == read(ROOT / "authenticated-inputs.json")
    frozen_candidate()
    rows = list(read(ROOT / "results/assessment.json")["checks"])
    for path, checksum in config["bookmark_hashes"].items():
        assert saved.digest(path) == checksum
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    check(rows, "scripts compile without bytecode", 0)
    check(rows, "all 1909 consumed/immediate paths rehashed unchanged", 0)
    protected = BRANCH.parent.parent / "formalization-workbench"
    started = datetime.fromisoformat(config["started_utc"]).timestamp()
    changed = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime >= started]
    check(rows, "protected workbench recent modification count", len(changed), 0, "integrity")
    failed = [row for row in rows if not row["passed"]]
    write(ROOT / "results/status.json", dict(stage=187, state="validated", count=len(rows),
          passed_checks=len(rows) - len(failed), checks=rows, failed_checks=failed,
          identity_failures=[row for row in failed if row["category"] in ["identity", "integrity"]],
          all_checks_passed=not failed, authenticated_inputs=paths,
          previous_failures_retained_via_seal=True, original_bank_changed=False,
          emission_bank_changed=False, source_curve_changed=False, original_histories_changed=False,
          tolerances_changed=False, new_candidate_histories=6, new_physical_edge_temperatures=2,
          new_source_integrations=0, new_virtual_integrals=0, reused_gas_events=36,
          coupled_updates=read(ROOT / "results/assessment.json")["updates"],
          maximum_active_workers=1, threads_per_worker=1, no_fitted_coefficients=True,
          full_source_gate_retested=False, new_observational_test=False,
          protected_workbench_recent_modified_file_count=len(changed),
          protected_check_scope="Recent mtime since preparation; consumed paths hashed, not full older archive rehash",
          completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT / "progress.json", dict(state="validated"))
    print(json.dumps(dict(checks=len(rows), failed=failed, inputs=len(paths))), flush=True)


if __name__ == "__main__":
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["assess", "validate"])
    arguments = parser.parse_args()
    dict(assess=assess, validate=validate)[arguments.phase]()

