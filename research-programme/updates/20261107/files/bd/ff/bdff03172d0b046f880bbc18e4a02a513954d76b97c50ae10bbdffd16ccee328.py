from source_tangent import *
sys.path.insert(0, str(BRANCH / "heldout-final-spectrum-20261019"))
import stage168_common as ancestry


def main():
    modest()
    folder = ROOT / "results/validation"
    folder.mkdir(parents=True, exist_ok=False)
    checks, packets, hashes, retained = [], {}, {}, []
    for path in sorted(ROOT.rglob("status.json")):
        if path.parent == folder:
            continue
        packet = json.loads(path.read_text())
        assert packet["state"] == "complete" and (path.parent / "COMPLETE").exists()
        label = path.parent.relative_to(ROOT).as_posix()
        packets[label] = packet
        for filename, checksum in packet["input_hashes"].items():
            assert filename not in hashes or hashes[filename] == checksum, filename
            hashes[filename] = checksum
        failed = [dict(row, packet=label) for row in packet["checks"] if not row["passed"]]
        retained.extend(failed)
        checks.append(dict(name="Completed packet with failures retained:"+label, passed=True, failures=len(failed)))
    required = ["results/preparation", "results/closed-factor-identities", "results/frozen",
                "results/prediction-test", "results/tangent-interpretation", "results/batch-validation",
                *["events/"+name for name in [*OFFSETS, "target"]]]
    assert set(required) <= set(packets)
    for label in ["results/preparation", "results/closed-factor-identities", "results/batch-validation"]:
        assert packets[label]["all_checks_passed"], label
    for filename, checksum in hashes.items():
        assert digest(filename) == checksum, filename
    checks.append(dict(name="All unique consumed hashes unchanged", count=len(hashes), passed=True))
    basis = np.load(ROOT / "results/preparation/basis.npz")
    mass = basis["mass"]
    raw_checks = []
    event_paths = sorted((ROOT / "events").rglob("event-*.npz"))
    assert len(event_paths) == 72
    with mp.workdps(80):
        norm0, norm1 = map(lambda value: mp.mpf(float(value)), basis["norms"][:2])
        mean = mp.mpf(float(basis["mean"]))
        for path in event_paths:
            with np.load(path) as saved:
                high, low = saved["high"], saved["low"]
                assert high.shape == low.shape == (2, 6, 98, 4)
                assert np.isfinite(high).all() and np.isfinite(low).all()
                if path.parent.name == "anchor":
                    assert np.array_equal(high[0], high[1]) and np.array_equal(low[0], low[1])
                for branch, component, history in np.ndindex(2, 6, 4):
                    def number(row):
                        return mp.mpf(float(high[branch, component, row, history]))+mp.mpf(float(low[branch, component, row, history]))
                    energy, gas = number(0), number(97)
                    represented = mean*norm0*number(1)+norm1*number(2)
                    scale = max(abs(energy), abs(gas), mp.mpf("1e-300"))
                    label = f"{path.parent.name}/{path.name}/{branch}/{COMPONENTS[component]}/{history}"
                    check(raw_checks, "Energy coordinate:"+label, float(abs(represented-energy)/scale), 1e-10)
                    check(raw_checks, "Independent gas exchange:"+label, float(abs(energy+gas)/scale), 1e-10)
                for component, indices in [(4, [1, 2, 3]), (5, [0, 1, 2, 3])]:
                    combined = precise_combine([(high[:, index], low[:, index]) for index in indices], [1]*len(indices))
                    error = precise_combine([combined, (high[:, component], low[:, component])], [1, -1])
                    relative = photon_norm(error[0]+error[1], mass)/np.maximum(
                        photon_norm(high[:, component]+low[:, component], mass), 1e-300)
                    check(checks, f"Component sum:{path.parent.name}/{path.name}/{component}", np.max(relative), 1e-10)
    write_json(folder / "raw-moment-checks.json", raw_checks)
    raw_failures = [row for row in raw_checks if not row["passed"]]
    retained.extend(dict(row, packet="independent_current_event_moments") for row in raw_failures)
    checks.append(dict(name="Independent current event moment outcomes retained", passed=True,
                       count=len(raw_checks), failures=len(raw_failures)))
    parent = json.loads((PARENT / "results/stage-integrity.json").read_text())
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SHA
    intermediate = BRANCH / "heldout-final-spectrum-20261019/results/stage-integrity.json"
    assert digest(intermediate) == parent["parent_seal_sha256"]
    chain = {PARENT / "results/stage-integrity.json": parent,
             intermediate: json.loads(intermediate.read_text()), **ancestry.ancestors()}
    prior = {PARENT / name for name in parent["file_hashes"]}
    prior.update(Path(filename) for filename in hashes if not Path(filename).is_relative_to(ROOT))
    authenticated = ancestry.authenticate(prior, chain)
    checks.append(dict(name="Parent payloads and consumed ancestry authenticated", count=len(authenticated), passed=True))
    scripts = list(ROOT.glob("*.py"))
    for path in scripts:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    checks.append(dict(name="All Python scripts compile without caches", count=len(scripts), passed=True))
    protected = BRANCH.parent.parent / "formalization-workbench"
    start = datetime(2026, 10, 19, 18, 11, 27, tzinfo=timezone.utc).timestamp()
    changed = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime > start]
    checks.append(dict(name="Protected workbench mtime guard", passed=not changed, count=len(changed)))
    final = packets["results/prediction-test"]
    prediction_summary = final["summary"]
    primary_second = all(prediction_summary[f"order2/{branch}/{component}"]["passed"] ==
                         prediction_summary[f"order2/{branch}/{component}"]["count"]
                         for branch in ["moving_history", "fixed_incident"] for component in ["control", "remainder", "total"])
    primary_derivative = all(row["passed"] for row in packets["results/frozen"]["checks"]
                             if any(":"+name+":" in row["name"] for name in ["control", "remainder", "total"]))
    all_event_identity = all(packets["events/"+name]["all_checks_passed"] for name in [*OFFSETS, "target"])
    write_json(folder / "retained-failures.json", retained)
    inputs = [*map(Path, hashes), *[ROOT / label / "status.json" for label in packets],
              folder / "raw-moment-checks.json", folder / "retained-failures.json",
              ROOT / "run_stage170.ps1", ROOT / "SECOND-DERIVATIVE.md"]
    report = finish(folder, checks, inputs, protocol_validation_only=True,
                    prediction_summary=prediction_summary, retained_failed_check_count=len(retained),
                    primary_second_order_predictions_pass=primary_second,
                    primary_derivative_stability_pass=primary_derivative,
                    current_event_identity_pass=all_event_identity and not raw_failures,
                    current_raw_moment_checks=len(raw_checks), current_raw_moment_failures=len(raw_failures),
                    consumed_and_immediate_rehashed=authenticated, rehashed_prior_files=len(authenticated),
                    compiled_scripts=len(scripts), source_curve_changed=False, current_history_replaced=False,
                    full_population_integral=False, raw_source_failures_inherited=40,
                    native_incident_histories_are_inputs=True, tolerances_changed=False,
                    protected_modified_file_count=len(changed),
                    protected_check_scope="Mtime guard since 2026-10-19 18:11:27 UTC; not a pre-turn content snapshot")
    print(json.dumps(dict(protocol_checks=report["count"], protocol_pass=report["all_checks_passed"],
                          retained_failures=len(retained), primary_second=primary_second,
                          primary_derivatives=primary_derivative, raw_moment_failures=len(raw_failures),
                          prior_files=len(authenticated))), flush=True)


if __name__ == "__main__":
    main()
