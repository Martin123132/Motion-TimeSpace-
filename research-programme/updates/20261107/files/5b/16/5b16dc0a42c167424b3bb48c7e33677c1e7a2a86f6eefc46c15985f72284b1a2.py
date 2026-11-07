from probe_stage188 import *


def curve_decimal(values, digits=80):
    with mp.workdps(digits):
        terms = [mp.mpf(value) for value in values]
        coarse = (terms[1] - 2 * terms[0] + terms[2]) * 10000
        fine = (terms[3] - 2 * terms[0] + terms[4]) * 40000
        return [str(coarse), str(fine), str(coarse - fine)]


def relative_change(actual, reference):
    with mp.workdps(100):
        reference = mp.mpf(reference)
        if reference == 0:
            return None
        return float(abs((mp.mpf(actual) - reference) / reference))


def comparison_check(checks, name, value, category, tolerance=.01):
    if value is None:
        checks.append(dict(name=name, value=None, tolerance=tolerance, passed=False,
                           category=category, reason="undefined: zero reference"))
    else:
        check(checks, name, value, tolerance, category)


def assess():
    assert read(ROOT / "progress.json")["state"] == "samples_complete"
    assert not (ROOT / "results/assessment.json").exists()
    config = protocol()
    checks = list(read(ROOT / "results/rule-checks.json")["checks"])
    curves = np.zeros((2, 2, 3, 3, 3))
    decimal_curves = {}
    audit_curves = {}
    records = {}
    total_solves = 0
    samples = []
    for model_index, model in enumerate(MODELS):
        for kind_index, kind in enumerate(KINDS):
            for grid_index, grid in enumerate(GRIDS):
                probes = []
                for index in range(5):
                    result = read(destination(model, kind, grid, index))
                    assert result["state"] == "complete" and not result["failed_checks"]
                    assert result["protocol_hashes"] == config["protocol_hashes"]
                    assert result["candidate_sha256"] == config["candidate_sha256"]
                    probes.append(result)
                    checks.extend([dict(row, name=f"{model}:{kind}:{grid}:{index}: " + row["name"]) for row in result["checks"]])
                    total_solves += result["solves"]
                records[(model, kind, grid)] = probes
                with mp.workdps(80):
                    methods = [[str(mp.mpf(float(result["linear_gas"]))) for result in probes],
                               [result["partial"]["gas"] for result in probes],
                               [result["split"]["gas"] for result in probes]]
                for method_index, method in enumerate(METHODS):
                    values = curve_decimal(methods[method_index])
                    decimal_curves[(model, kind, method, grid)] = values
                    curves[model_index, kind_index, method_index, grid_index] = [float(value) for value in values]
                    samples.append(dict(model=model, kind=kind, method=method, grid=grid, values=methods[method_index], curvatures=values))
                if grid == "quarter":
                    values = curve_decimal([result["audit"]["gas"] for result in probes], 100)
                    audit_curves[(model, kind)] = values
                    for quantity, actual, reference in zip(QUANTITIES, values, decimal_curves[(model, kind, "partial", grid)]):
                        error = relative_change(actual, reference)
                        comparison_check(checks, model + ":" + kind + ":" + quantity + ": 80/100-digit curvature",
                                         error, "identity", 1e-10)
    assert total_solves == 208
    inherited = packet(PARENT / "results/comparison.npz")
    assert np.array_equal(curves[:, :, 0], inherited["curves"])
    check(checks, "Stage187 linear-sampling curvatures reproduced bitwise", 0)
    rows, split_rows, reductions = [], [], []
    for model_index, model in enumerate(MODELS):
        for kind_index, kind in enumerate(KINDS):
            for method_index, method in enumerate(METHODS):
                for coarse_index in [0, 1]:
                    coarse_grid, fine_grid = GRIDS[coarse_index:coarse_index + 2]
                    coarse = decimal_curves[(model, kind, method, coarse_grid)]
                    fine = decimal_curves[(model, kind, method, fine_grid)]
                    for quantity, coarse_value, fine_value in zip(QUANTITIES, coarse, fine):
                        error = relative_change(coarse_value, fine_value)
                        comparison_check(checks, f"{model}:{kind}:{method}:{coarse_grid}/{fine_grid}:{quantity}",
                                         error, "step_comparison")
                        rows.append(dict(model=model, kind=kind, method=method, coarse_grid=coarse_grid, fine_grid=fine_grid,
                                         quantity=quantity, coarse=coarse_value, fine=fine_value,
                                         relative_change=error, passed=bool(error is not None and error <= .01)))
            for grid_index, grid in enumerate(GRIDS):
                single = decimal_curves[(model, kind, "partial", grid)]
                split = decimal_curves[(model, kind, "split", grid)]
                for quantity, single_value, split_value in zip(QUANTITIES, single, split):
                    error = relative_change(single_value, split_value)
                    comparison_check(checks, f"{model}:{kind}:{grid}:{quantity}: partial/split",
                                     error, "split_comparison")
                    with mp.workdps(100):
                        absolute = str(abs(mp.mpf(single_value) - mp.mpf(split_value)))
                    split_rows.append(dict(model=model, kind=kind, grid=grid, quantity=quantity, single=single_value,
                                           split=split_value, relative_change=error, absolute_change=absolute,
                                           passed=bool(error is not None and error <= .01)))
                linear_curve = curves[model_index, kind_index, 0, grid_index]
                for method_index, method in enumerate(METHODS[1:], 1):
                    direct = curves[model_index, kind_index, method_index, grid_index]
                    reductions.append(dict(model=model, kind=kind, method=method, grid=grid,
                                           linear=linear_curve.tolist(), direct=direct.tolist(),
                                           width_reduction_fraction=float(1 - abs(direct[2] / linear_curve[2])),
                                           width_over_fine=float(abs(direct[2] / direct[1]))))
    kernels, components = inherited["kernels"], list(inherited["components"])
    assert np.array_equal(kernels, packet(previous.old.ROOT / "results/gas-responses.npz")["kernels"])
    factor = linear.cholesky(packet(source.ROOT / "results/preparation/basis.npz")["mass"], lower=True)

    def norm(vector):
        return float(np.linalg.norm(linear.solve_triangular(factor, vector[1:97], lower=True)))

    responses = np.empty((2, 3, 3, 3, 6, 98, 4))
    for kind_index, method_index, grid_index, quantity_index, component, column in np.ndindex(2, 3, 3, 3, 6, 4):
        responses[kind_index, method_index, grid_index, quantity_index, component, :, column] = (
            curves[column // 2, kind_index, method_index, grid_index, quantity_index] * kernels[component, :, column])
    assert np.array_equal(responses[:, 0], inherited["responses"])
    check(checks, "Stage187 linear baseline/MTS response arrays reproduced bitwise", 0)
    source_rows = []
    for kind_index, kind in enumerate(KINDS):
        for method_index, method in enumerate(METHODS):
            for component in [0, 4, 5]:
                for quantity_index, quantity in enumerate(QUANTITIES):
                    for column in range(4):
                        fine = responses[kind_index, method_index, 2, quantity_index, component, :, column]
                        coarse = responses[kind_index, method_index, 1, quantity_index, component, :, column]
                        denominator = norm(fine)
                        error = norm(fine - coarse) / denominator if denominator else None
                        comparison_check(checks, f"{kind}:{method}:{components[component]}:{column}:{quantity}: half/quarter source",
                                         error, "source_step_comparison")
                        values = curves[column // 2, kind_index, method_index, :, quantity_index]
                        expected = abs((values[2] - values[1]) / values[2]) if values[2] else None
                        if error is not None and expected is not None:
                            check(checks, f"{kind}:{method}:{components[component]}:{column}:{quantity}: gas-source fraction",
                                  error - expected)
                        source_rows.append(dict(kind=kind, method=method, component=str(components[component]), column=column,
                                                quantity=quantity, relative_change=error, passed=bool(error is not None and error <= .01),
                                                quarter_norm=norm(fine)))
    for kind_index, method_index, grid_index, quantity_index, component, column in np.ndindex(2, 3, 3, 3, 6, 4):
        vector = responses[kind_index, method_index, grid_index, quantity_index, component, :, column]
        check(checks, f"{kind_index}:{method_index}:{grid_index}:{quantity_index}:{component}:{column}: source energy",
              (vector[0] + vector[-1]) / max(abs(vector[0]), abs(vector[-1]), 1e-300))
    for kind_index, method_index, grid_index, quantity_index, column in np.ndindex(2, 3, 3, 3, 4):
        array = responses[kind_index, method_index, grid_index, quantity_index, :, :, column]
        check(checks, f"{kind_index}:{method_index}:{grid_index}:{quantity_index}:{column}: matched source closure",
              norm(array[4] - array[1] - array[2] - array[3]) / max(norm(array[4]), 1e-300))
        check(checks, f"{kind_index}:{method_index}:{grid_index}:{quantity_index}:{column}: total source closure",
              norm(array[5] - array[0] - array[4]) / max(norm(array[5]), 1e-300))
    np.savez_compressed(ROOT / "results/comparison.npz", curves=curves, responses=responses, kernels=kernels,
                        components=np.array(components), models=np.array(MODELS), kinds=np.array(KINDS),
                        methods=np.array(METHODS), grids=np.array(GRIDS), quantities=np.array(QUANTITIES))
    write(ROOT / "results/decimal-probes.json", samples)
    write(ROOT / "results/saved-baseline-controls.json", read(PARENT / "results/saved-baseline-controls.json"))
    failed = [row for row in checks if not row["passed"]]
    write(ROOT / "results/assessment.json", dict(checks=checks, failed_checks=failed, step_comparisons=rows,
          split_comparisons=split_rows, sampling_changes=reductions, source_rows=source_rows, solves=total_solves,
          right_hand_sides_per_solve=2, exact_reused_probes=12, new_off_node_probes=48,
          working_digits=80, audit_digits=100, new_source_integrations=0, new_scattering_integrations=0,
          no_original_histories_overwritten=True, reused_gas_events=36))
    write(ROOT / "progress.json", dict(state="assessed"))
    print(json.dumps(dict(count=len(checks), failures=len(failed),
          identity_failures=[row for row in failed if row["category"] == "identity"],
          quarter_sampling=[row for row in reductions if row["grid"] == "quarter"],
          direct_quarter_checks=[row for row in rows if row["method"] == "partial" and row["fine_grid"] == "quarter"],
          quarter_split=[row for row in split_rows if row["grid"] == "quarter"])), flush=True)


def validate():
    assert read(ROOT / "progress.json")["state"] == "assessed"
    assert not (ROOT / "results/status.json").exists()
    config = protocol()
    paths = authenticate()
    assert paths == read(ROOT / "authenticated-inputs.json")
    for path, checksum in config["bookmark_hashes"].items():
        assert saved.digest(path) == checksum
    rows = list(read(ROOT / "results/assessment.json")["checks"])
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    check(rows, "scripts compile without bytecode", 0)
    check(rows, "all consumed/immediate files rehashed unchanged", 0)
    check(rows, "original source decision preserved", 0 if read(ROOT / "results/saved-baseline-controls.json") == read(PARENT / "results/saved-baseline-controls.json") else 1)
    protected = BRANCH.parent.parent / "formalization-workbench"
    started = datetime.fromisoformat(config["started_utc"]).timestamp()
    changed = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime >= started]
    check(rows, "protected workbench recent modification count", len(changed), 0, "integrity")
    failed = [row for row in rows if not row["passed"]]
    assessment = read(ROOT / "results/assessment.json")
    write(ROOT / "results/status.json", dict(stage=188, state="validated", count=len(rows), passed_checks=len(rows) - len(failed),
          checks=rows, failed_checks=failed, identity_failures=[row for row in failed if row["category"] in ["identity", "integrity"]],
          all_checks_passed=not failed, authenticated_inputs=paths, candidate_sha256=config["candidate_sha256"],
          protocol_hashes=config["protocol_hashes"], previous_failures_retained_via_seal=True,
          original_bank_changed=False, candidate_coefficients_changed=False, emission_bank_changed=False,
          original_histories_changed=False, source_curve_changed=False, tolerances_changed=False,
          reused_saved_histories=12, probe_records=60, exact_node_reuses=12, off_node_probes=48,
          coupled_partial_and_control_solves=assessment["solves"], right_hand_sides_per_solve=2,
          reused_gas_events=36, new_scattering_integrations=0, new_source_integrations=0, new_virtual_integrals=0,
          full_source_gate_retested=False, new_observational_test=False, maximum_active_workers=1,
          threads_per_worker=1, protected_workbench_recent_modified_file_count=len(changed),
          protected_check_scope="Recent mtime since preparation; consumed paths hashed, not full older archive rehash",
          completed_at_utc=datetime.now(timezone.utc).isoformat()))
    write(ROOT / "progress.json", dict(state="validated"))
    print(json.dumps(dict(checks=len(rows), passed=len(rows) - len(failed), failures=len(failed),
                          identity_failures=[row for row in failed if row["category"] in ["identity", "integrity"]],
                          inputs=len(paths))), flush=True)


if __name__ == "__main__":
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["assess", "validate"])
    arguments = parser.parse_args()
    dict(assess=assess, validate=validate)[arguments.phase]()

