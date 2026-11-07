from curvature_stage186 import *


def load_packets():
    frozen = read(ROOT / "results/frozen-curvature.json")
    assert saved.digest(ROOT / "results/frozen-curvature.npz") == frozen["sha256"]
    with np.load(ROOT / "results/frozen-curvature.npz") as packet:
        analytic = {key: packet[key].copy() for key in packet.files}
    targets = []
    for index, offset in enumerate(OFFSETS):
        folder = PARENT / "targets" / f"target-{index}"
        status = read(folder / "status.json")
        assert status["offset"] == offset
        assert saved.digest(folder / "matrices.npz") == status["matrix_sha256"]
        with np.load(folder / "matrices.npz") as packet:
            targets.append({key: packet[key].copy() for key in packet.files})
    return analytic, targets


def matrix_analysis(analytic, targets):
    checks = list(read(ROOT / "results/frozen-curvature.json")["checks"])
    rows, centered, negatives, boundaries = [], [], [], []
    anchor, tangent, curvature = [analytic[key] for key in ["block", "tangent", "curvature"]]
    for offset, packet in zip(OFFSETS, targets):
        for kind in ["block", "fixed_mask"]:
            change = packet[kind] - anchor
            remainder = change - offset * tangent
            quadratic = .5 * offset ** 2 * curvature
            small_error = relative(offset * tangent + quadratic, change)
            curvature_error = relative(quadratic, remainder)
            check(checks, f"{offset}:{kind}: quadratic small-change prediction", small_error, .01, "prediction")
            check(checks, f"{offset}:{kind}: quadratic remainder prediction", curvature_error, .01, "curvature")
            negative_error = relative(np.zeros_like(remainder), remainder)
            assert negative_error > .01
            negatives.append(dict(offset=offset, kind=kind, error=negative_error, rejected=True))
            rows.append(dict(offset=offset, kind=kind, small_change_error=small_error,
                             curvature_remainder_error=curvature_error, curvature_passed=curvature_error <= .01,
                             remainder_norm=float(np.linalg.norm(remainder)), quadratic_norm=float(np.linalg.norm(quadratic))))
        check(checks, f"{offset}: saved boundary split", relative(packet["fixed_mask"] + packet["boundary"], packet["block"]))
    for index in range(0, len(OFFSETS), 2):
        step = OFFSETS[index]
        plus, minus = targets[index:index + 2]
        for kind in ["block", "fixed_mask"]:
            actual = ((plus[kind] - anchor) + (minus[kind] - anchor)) / step ** 2
            error = relative(curvature, actual)
            check(checks, f"{step}:{kind}: centered second derivative", error, .01, "curvature")
            centered.append(dict(step=step, kind=kind, relative_error=error, passed=error <= .01,
                                 observed_norm=float(np.linalg.norm(actual))))
        boundary = (plus["boundary"] + minus["boundary"]) / step ** 2
        live = ((plus["block"] - anchor) + (minus["block"] - anchor)) / step ** 2
        fixed = ((plus["fixed_mask"] - anchor) + (minus["fixed_mask"] - anchor)) / step ** 2
        split_error = float(np.linalg.norm(live - fixed - boundary) / np.linalg.norm(live))
        check(checks, f"{step}: centered boundary algebra with saved rounding", split_error, 1e-10)
        boundaries.append(dict(step=step, boundary_over_live_curvature=float(np.linalg.norm(boundary) / np.linalg.norm(live)),
                               split_relative_error=split_error))
    return dict(checks=checks, predictions=rows, centered=centered, boundary_curvature=boundaries,
                negative_controls=negatives)


def gas_state(model, basis, bank, analytic):
    operator = prior.Operators(model, bank)
    history = prior.history(model, "quarter")
    coordinate = float(history["coordinates"][0])
    profile = prior.mp_vector(np.array([np.interp(coordinate, history["expansion"], history["profiles"][:, index])
                                       for index in range(96)]))
    dual = mp.lu_solve(prior.mp_matrix(basis.mass).T, prior.mp_vector(basis.energy)).T
    template = prior.mp_vector(basis.temperature)
    stiffness = prior.mp_matrix(operator.at(coordinate)[0])
    heat = mp.mpf(operator.background.chi)
    local = operator.background.at(coordinate)
    rate = mp.mpf(local["coefficient"] / local["thermal_parameter"])
    capacity = heat - (dual * stiffness * template)[0]
    numerator = 1 + (dual * stiffness * profile)[0]
    equilibrium = -numerator / capacity
    first_row = rate * dual * prior.mp_matrix(analytic["tangent"])
    second_row = rate * dual * prior.mp_matrix(analytic["curvature"])
    capacity_first, capacity_second = -(first_row * template)[0], -(second_row * template)[0]
    numerator_first, numerator_second = (first_row * profile)[0], (second_row * profile)[0]
    first = -(numerator_first + equilibrium * capacity_first) / capacity
    linear_second = -(numerator_second + equilibrium * capacity_second) / capacity
    capacity_second_term = -2 * first * capacity_first / capacity
    second = linear_second + capacity_second_term
    return dict(model=model, dual=dual, profile=profile, template=template, rate=rate, capacity=capacity,
                numerator=numerator, equilibrium=equilibrium, first=first, second=second,
                linear_second=linear_second, capacity_second_term=capacity_second_term,
                capacity_first=capacity_first, capacity_second=capacity_second,
                numerator_first=numerator_first, numerator_second=numerator_second)


def gas_analysis(analytic, targets, basis, bank):
    checks, models = [], []
    saved_slopes = read(PARENT / "results/gas-projection.json")["results"]
    with mp.workdps(80):
        anchor = prior.mp_matrix(analytic["block"])
        for model_index, model in enumerate(old.MODELS):
            state = gas_state(model, basis, bank, analytic)
            capacity, numerator = state["capacity"], state["numerator"]
            equilibrium, first, second = [state[key] for key in ["equilibrium", "first", "second"]]
            check(checks, model + ": gas implicit identity", (capacity * equilibrium + numerator) / numerator)
            check(checks, model + ": gas first derivative identity",
                  (capacity * first + state["capacity_first"] * equilibrium + state["numerator_first"])
                  / max(abs(capacity * first), abs(state["numerator_first"])))
            check(checks, model + ": gas second derivative identity",
                  (capacity * second + 2 * state["capacity_first"] * first
                   + state["capacity_second"] * equilibrium + state["numerator_second"])
                  / max(abs(capacity * second), abs(state["numerator_second"])))
            inherited = mp.mpf(saved_slopes[model_index]["physical_collision_gas_slope"])
            check(checks, model + ": t derivative is minus saved u derivative", (first + inherited) / inherited)
            target_values, rows = {}, []
            for offset, packet in zip(OFFSETS, targets):
                increment = mp.mpf(offset)
                for kind in ["block", "fixed_mask"]:
                    delta = prior.mp_matrix(packet[kind]) - anchor
                    change_row = state["rate"] * state["dual"] * delta
                    capacity_change = -(change_row * state["template"])[0]
                    numerator_change = (change_row * state["profile"])[0]
                    actual_value = -(numerator + numerator_change) / (capacity + capacity_change)
                    actual_change = actual_value - equilibrium
                    remainder = actual_change - increment * first
                    predicted = increment ** 2 * second / 2
                    small_error = float(abs(increment * first + predicted - actual_change) / abs(actual_change))
                    error = float(abs(predicted - remainder) / abs(remainder))
                    check(checks, f"{model}:{offset}:{kind}: gas quadratic small-change prediction", small_error, .01, "gas_prediction")
                    check(checks, f"{model}:{offset}:{kind}: gas second-order remainder", error, .01, "gas_curvature")
                    target_values[(offset, kind)] = actual_value
                    rows.append(dict(offset=offset, kind=kind, change=str(actual_change), remainder=str(remainder),
                                     predicted_remainder=str(predicted), curvature_remainder_error=error,
                                     small_change_error=small_error, passed=error <= .01))
            centered = []
            for step in OFFSETS[::2]:
                for kind in ["block", "fixed_mask"]:
                    actual = (target_values[(step, kind)] + target_values[(-step, kind)] - 2 * equilibrium) / mp.mpf(step) ** 2
                    error = float(abs(second - actual) / abs(actual))
                    check(checks, f"{model}:{step}:{kind}: centered gas second derivative", error, .01, "gas_curvature")
                    centered.append(dict(step=step, kind=kind, observed=str(actual), relative_error=error, passed=error <= .01))
            with mp.workdps(100):
                high = gas_state(model, basis, bank, analytic)
                for key in ["equilibrium", "first", "second", "linear_second", "capacity_second_term"]:
                    check(checks, model + ": 80/100 digit " + key, abs((state[key] - high[key]) / high[key]))
            models.append(dict(model=model, equilibrium=str(equilibrium), first=str(first), second=str(second),
                               linear_second=str(state["linear_second"]), capacity_term=str(state["capacity_second_term"]),
                               capacity_term_fraction=str(state["capacity_second_term"] / second),
                               capacity=str(capacity), predictions=rows, centered=centered))
    return dict(checks=checks, models=models,
                scope="Collision-only local slaved gas curvature at fixed photon state, emission, rate and heat capacity")


def response_analysis(gas):
    with np.load(PARENT / "results/gas-responses.npz") as packet:
        kernels, components = packet["kernels"].copy(), list(packet["components"])
    with np.load(old.PARENT / "results/gas-response.npz") as packet:
        assert np.array_equal(kernels, packet["kernels"])
    with np.load(source.ROOT / "results/preparation/basis.npz") as packet:
        factor = linear.cholesky(packet["mass"], lower=True)
    def norm(vector):
        return float(np.linalg.norm(linear.solve_triangular(factor, vector[1:97], lower=True)))
    checks, rows = [], []
    check(checks, "36-event aggregate gas kernels unchanged bitwise", 0)
    derivatives = np.empty((6, 98, 4))
    for component, column in np.ndindex(6, 4):
        model = gas["models"][column // 2]
        derivatives[component, :, column] = float(model["second"]) * kernels[component, :, column]
    for component in [0, 4, 5]:
        for column in range(4):
            model = gas["models"][column // 2]
            kernel = kernels[component, :, column]
            for record in model["predictions"]:
                actual = float(record["remainder"]) * kernel
                predicted = float(record["predicted_remainder"]) * kernel
                error = norm(predicted - actual) / norm(actual)
                check(checks, f"{components[component]}:{column}:{record['offset']}:{record['kind']}: curvature response",
                      error, .01, "source_curvature")
                check(checks, f"{components[component]}:{column}:{record['offset']}:{record['kind']}: gas-source linearity",
                      error - record["curvature_remainder_error"])
                rows.append(dict(component=str(components[component]), column=column, model=model["model"],
                                 offset=record["offset"], kind=record["kind"], relative_error=error,
                                 passed=error <= .01, actual_remainder_norm=norm(actual), predicted_remainder_norm=norm(predicted),
                                 second_derivative_norm=norm(derivatives[component, :, column])))
    for component, column in np.ndindex(6, 4):
        vector = derivatives[component, :, column]
        check(checks, f"{components[component]}:{column}: energy exchange cancellation",
              (vector[0] + vector[-1]) / max(abs(vector[0]), abs(vector[-1])))
    for column in range(4):
        check(checks, f"{column}: matched response closure", norm(derivatives[4, :, column]
              - derivatives[1, :, column] - derivatives[2, :, column] - derivatives[3, :, column])
              / norm(derivatives[4, :, column]))
        check(checks, f"{column}: total response closure", norm(derivatives[5, :, column]
              - derivatives[0, :, column] - derivatives[4, :, column]) / norm(derivatives[5, :, column]))
    np.savez_compressed(ROOT / "results/gas-responses.npz", kernels=kernels, derivatives=derivatives, components=np.array(components))
    return dict(checks=checks, rows=rows, reused_gas_events=36, new_source_integrations=0)


def analyse():
    assert read(ROOT / "progress.json")["state"] == "curvature_frozen"
    assert not (ROOT / "results/matrix-analysis.json").exists()
    analytic, targets = load_packets()
    bank, basis, theta = old.setup()
    matrix = matrix_analysis(analytic, targets)
    write(ROOT / "results/matrix-analysis.json", matrix)
    gas = gas_analysis(analytic, targets, basis, bank)
    write(ROOT / "results/gas-analysis.json", gas)
    responses = response_analysis(gas)
    write(ROOT / "results/source-analysis.json", responses)
    write(ROOT / "progress.json", dict(state="analysis_complete"))
    checks = matrix["checks"] + gas["checks"] + responses["checks"]
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row["passed"]],
                          matrix_centered=matrix["centered"],
                          gas_curvature=[{key: row[key] for key in ["model", "second", "capacity_term_fraction"]} for row in gas["models"]],
                          worst_response=max(row["relative_error"] for row in responses["rows"]))), flush=True)


def validate():
    assert read(ROOT / "progress.json")["state"] == "analysis_complete"
    paths = authenticate()
    assert paths == read(ROOT / "authenticated-inputs.json")
    config = read(ROOT / "configuration.json")
    assert config["identity_tolerance"] == 1e-10 and config["source_prediction_tolerance"] == .01
    for path, checksum in config["bookmark_hashes"].items():
        assert saved.digest(path) == checksum
    analytic, targets = load_packets()
    checks = sum([read(ROOT / "results" / filename)["checks"]
                  for filename in ["matrix-analysis.json", "gas-analysis.json", "source-analysis.json"]], [])
    negatives = read(ROOT / "results/matrix-analysis.json")["negative_controls"]
    assert len(negatives) == 16 and all(row["rejected"] for row in negatives)
    check(checks, "zero curvature fails sixteen second-order operator controls", 0)
    controls = read(PARENT / "results/saved-baseline-controls.json")
    write(ROOT / "results/saved-baseline-controls.json", controls)
    assert controls == read(ROOT / "results/saved-baseline-controls.json")
    check(checks, "previous full-source decisions preserved", 0)
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    check(checks, "scripts compile without bytecode", 0)
    protected = BRANCH.parent.parent / "formalization-workbench"
    started = datetime.fromisoformat(config["started_utc"]).timestamp()
    recent = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime >= started]
    check(checks, "protected workbench recent-mtime count", len(recent), 0, "integrity")
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum
    check(checks, "consumed/immediate files rehashed unchanged", 0)
    failed = [row for row in checks if not row["passed"]]
    parent_status = read(PARENT / "results/status.json")
    import scipy
    status = dict(stage=186, state="diagnostic_complete", completed_at_utc=datetime.now(timezone.utc).isoformat(),
                  count=len(checks), passed_checks=len(checks) - len(failed), failed_checks=failed, checks=checks,
                  all_checks_passed=not failed, identity_failures=[row for row in failed if row["category"] in ["identity", "integrity"]],
                  authenticated_inputs=paths, inherited_stage185_failures=parent_status["failed_checks"],
                  older_failures_retained_via_parent_seal=True, no_fitted_coefficients=True,
                  original_bank_changed=False, emission_bank_changed=False, source_curve_changed=False,
                  temperature_history_changed=False, tolerances_changed=False, full_source_gate_retested=False,
                  retained_anchor_curvature_integrations=1, attempted_anchor_curvature_integrations=2,
                  first_attempt_failed_before_saving=True, new_target_collision_integrations=0,
                  reused_temperature_targets=8, reused_gas_events=36, new_microscopic_source_events=0,
                  new_virtual_integrals=0, protected_workbench_recent_modified_file_count=len(recent),
                  protected_check_scope="Recent mtime since preparation; not a full-tree hash",
                  global_continuum_derivative_bound=None, retrospective_saved_target_validation=True,
                  runtime=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__, mpmath=mp.__version__,
                               thread_environment={name: os.environ[name] for name in
                                ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]}))
    write(ROOT / "results/status.json", status)
    write(ROOT / "progress.json", dict(state="validation_complete"))
    print(json.dumps(dict(count=len(checks), passed=status["passed_checks"], failed=failed, authenticated=len(paths))), flush=True)


if __name__ == "__main__":
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["analyse", "validate"])
    arguments = parser.parse_args()
    dict(analyse=analyse, validate=validate)[arguments.phase]()

