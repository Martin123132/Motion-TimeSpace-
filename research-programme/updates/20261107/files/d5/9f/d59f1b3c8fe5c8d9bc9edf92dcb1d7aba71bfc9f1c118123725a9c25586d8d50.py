from common229 import *


def validate():
    protocol()
    preflight = read(ROOT / 'results/preflight.json')
    assert preflight['qualified']
    checks = list(preflight['checks'])
    inputs = read(ROOT / 'results/preflight-inputs.json')
    reports = []
    for model in ('heavy', 'cold'):
        runs = {}
        for count in (3200, 6400):
            folder = ROOT / f'runs/{model}-{count}'
            report = read(register(inputs, folder / 'status.json'))
            assert report['state'] == 'complete' and report['qualified']
            assert digest(folder / 'history.npz') == report['history_sha256']
            with np.load(register(inputs, folder / 'history.npz')) as saved:
                runs[count] = dict(saved)
            for path, expected in read(folder / 'inputs.json').items():
                assert path not in inputs or inputs[path] == expected
                inputs[path] = expected
            checks.extend([dict(row, name=f'{model}:{count}:' + row['name']) for row in report['checks']])
        coarse, fine = runs[3200], runs[6400]
        check(checks, model + ': matched refinement coordinates', np.max(abs(coarse['rows'][:, 0] - fine['rows'][::2, 0])), 1e-14)
        comparisons = {}
        for label, column in (('density', 9), ('pressure', 11), ('gas', 4)):
            error = relative(coarse['rows'][:, column], fine['rows'][::2, column])
            comparisons[label] = error
            check(checks, model + ': EOS difference time refinement ' + label, error, .01)
        error = relative(coarse['profiles'][:, :, 1], fine['profiles'][::2, :, 1])
        comparisons['spectrum'] = error
        check(checks, model + ': EOS difference time refinement spectrum', error, .01)
        heat = float(fine['chi'])
        rows = fine['rows']
        step = float(rows[-1, 0] / 6400)
        excess_energy = rows[:, 2] + rows[:, 5]
        derivative = (1.5 * excess_energy[2:] - 2 * excess_energy[1:-1] + .5 * excess_energy[:-2]) / step
        residual = derivative - excess_energy[2:] + rows[2:, 2] + 2 * heat * rows[2:, 4]
        residual_ratio = float(np.max(abs(residual)) / max(np.max(abs(excess_energy)), 1e-300))
        reports.append(dict(model=model, refinement=comparisons,
            density_prediction_error=relative(rows[:, 9], fine['density_prediction']),
            pressure_prediction_error=relative(rows[:, 11], fine['pressure_prediction']),
            final_density=float(rows[-1, 9]), final_pressure=float(rows[-1, 11]),
            final_photon_energy_increment=float(heat * rows[-1, 2]),
            final_gas_temperature_increment=float(heat * rows[-1, 4]),
            final_NR_gas_temperature_departure=float(heat * rows[-1, 3]),
            discrete_stress_continuity_residual_diagnostic=residual_ratio,
            maximum_raw_residual=np.max(fine['raw_residuals'], axis=0).tolist(),
            relative_density_pointwise_error=float(np.max(abs(rows[:, 9] / fine['density_prediction'] - 1)))))
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    since = datetime.fromisoformat(START).timestamp()
    protected = BRANCH.parent.parent / 'formalization-workbench'
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    check(checks, 'Protected workbench recent-mtime guard', len(recent), 0)
    check(checks, 'No local bytecode', len(list(ROOT.rglob('__pycache__'))), 0)
    assert not (ROOT / 'results/completion.json').exists()
    write(ROOT / 'results/inputs-complete.json', inputs)
    report = dict(stage=229, state='complete', finished_at=now(), checks=checks,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        models=reports, inputs_rehashed=len(inputs), protected_recent_mtime_count=len(recent),
        scope='Conservative finite-capacity electron-EOS kinetic realization against frozen Stage228 source; no new gravity or spatial-wave evolution')
    write(ROOT / 'results/completion.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], inputs=len(inputs), models=reports)), flush=True)


def seal():
    report = read(ROOT / 'results/completion.json')
    assert report['qualified']
    path = ROOT / 'results/stage-integrity.json'
    assert not path.exists()
    files = {str(item.relative_to(ROOT)): digest(item) for item in sorted(ROOT.rglob('*')) if item.is_file()}
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    for bookmark in bookmarks:
        assert bookmark.read_text(encoding='utf-8').startswith('# Stage229 SAVED')
    write(path, dict(stage=229, state='complete', qualified=True, sealed_at=now(), file_hashes=files,
        bookmarks={str(item): digest(item) for item in bookmarks},
        directly_consumed_inputs=read(ROOT / 'results/inputs-complete.json'), scope=report['scope']))
    print(json.dumps(dict(seal_sha256=digest(path), payloads=len(files))), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'validate':
        validate()
    elif sys.argv[1] == 'seal':
        seal()
    else:
        raise ValueError(sys.argv[1])
