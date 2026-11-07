from common230 import *


def identity():
    names = ['finish230.py', 'FINAL-CHECKS.md', 'results/preflight.json', 'results/branch-bounds.json']
    for model in ('heavy', 'cold'):
        for count in (3200, 6400):
            names.extend([f'runs/{model}-{count}/history.npz', f'runs/{model}-{count}/status.json'])
    return {name: digest(ROOT / name) for name in names}


def stress_residual(system, saved, component):
    rows, fields = saved['rows'], saved['fields']
    scale = system.background.start_scale * np.exp(rows[:, 0])
    base = fields[:, :, :, 0] if component == 1 else fields[:, :, :, 0] + fields[:, :, :, 1]
    delta = fields[:, :, :, component]
    kinetic = np.sum(base[:, 1] * delta[:, 1] + .5 * delta[:, 1]**2, axis=1) / scale**2
    potential = np.sum(system.mass**2 * (base[:, 0] * delta[:, 0] + .5 * delta[:, 0]**2), axis=1)
    photon = system.background.parent.photons / scale**4
    density = kinetic + potential + photon * rows[:, 7 + component]
    pressure = kinetic - potential + photon * rows[:, 9 + component]
    step = rows[-1, 0] / (len(rows) - 1)
    derivative = (1.5 * density[2:] - 2 * density[1:-1] + .5 * density[:-2]) / step
    work = 3 * (density[2:] + pressure[2:])
    return float(np.max(abs(derivative + work)) / np.max(abs(derivative) + abs(work)))


def validate():
    modest()
    protocol()
    assert read(ROOT / 'final-configuration.json')['input_hashes'] == identity()
    preflight, bounds = read(ROOT / 'results/preflight.json'), read(ROOT / 'results/branch-bounds.json')
    assert preflight['qualified'] and bounds['qualified']
    checks = list(preflight['checks']) + list(bounds['checks'])
    inputs = read(ROOT / 'results/bound-inputs.json')
    reports = []
    for model in ('heavy', 'cold'):
        system = System(model, 6400, inputs)
        runs, run_reports = {}, {}
        for count in (3200, 6400):
            folder = ROOT / f'runs/{model}-{count}'
            status = read(register(inputs, folder / 'status.json'))
            assert status['state'] == 'complete' and status['qualified']
            assert digest(folder / 'history.npz') == status['history_sha256']
            with np.load(register(inputs, folder / 'history.npz')) as saved:
                runs[count] = dict(saved)
            for path, expected in read(folder / 'inputs.json').items():
                assert path not in inputs or inputs[path] == expected
                inputs[path] = expected
            checks.extend([dict(row, name=f'{model}:{count}:' + row['name']) for row in status['checks']])
            run_reports[count] = status
        coarse, fine = runs[3200], runs[6400]
        check(checks, model + ': matched time-refinement nodes', np.max(abs(coarse['rows'][:, 0] - fine['rows'][::2, 0])), 1e-14)
        refinement = {}
        for label, component in (('NR', 1), ('EOS', 2)):
            mappings = dict(H=(coarse['rows'][:, 12 + component], fine['rows'][::2, 12 + component]),
                fields=(coarse['fields'][:, :, :, component], fine['fields'][::2, :, :, component]),
                clocks=(coarse['clocks'][:, :, component], fine['clocks'][::2, :, component]),
                gas=(coarse['rows'][:, 2 + component], fine['rows'][::2, 2 + component]),
                spectrum=(coarse['profiles'][:, :, component - 1], fine['profiles'][::2, :, component - 1]))
            for quantity, (left, right) in mappings.items():
                error = relative(left, right)
                refinement[label + '_' + quantity] = error
                check(checks, model + ':' + label + ': paired ' + quantity + ' refinement', error, .01)
        continuity = {}
        for label, component in (('NR', 1), ('EOS', 2)):
            values = [stress_residual(system, runs[count], component) for count in (3200, 6400)]
            continuity[label] = dict(coarse=values[0], fine=values[1], ratio=values[1] / values[0])
            check(checks, model + ':' + label + ': finite-step total-stress continuity', values[1], .01)
            check(checks, model + ':' + label + ': total-stress continuity convergence', values[1] / values[0], .8)
        finest = run_reports[6400]
        reports.append(dict(model=model, refinement=refinement, continuity=continuity,
            final_NR=finest['final_fraction_NR'], final_EOS=finest['final_EOS_fraction_relative_no_heat'],
            minimum_scaled_slope_over_two=finest['minimum_root_J'],
            fine_reference_comparisons=[row for row in finest['checks'] if 'Stage228' in row['name'] or 'independent retained' in row['name']],
            elapsed_seconds=finest['elapsed_seconds']))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for name, expected in read(ROOT / 'bound-configuration.json')['input_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    since = datetime.fromisoformat(START).timestamp()
    protected = BRANCH.parent.parent / 'formalization-workbench'
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    check(checks, 'Protected workbench recent-mtime guard', len(recent), 0)
    check(checks, 'No local bytecode', len(list(ROOT.rglob('__pycache__'))), 0)
    assert not (ROOT / 'results/completion.json').exists()
    write(ROOT / 'results/inputs-complete.json', inputs)
    report = dict(stage=230, state='complete', finished_at=now(), models=reports, checks=checks,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        inputs_rehashed=len(inputs), protected_recent_mtime_count=len(recent),
        scope='Two-way homogeneous kinetic/field/Friedmann benchmark in retained weak model; numerical convergence and conditional physical branch bound')
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
        assert bookmark.read_text(encoding='utf-8').startswith('# Stage230 SAVED')
    write(path, dict(stage=230, state='complete', qualified=True, sealed_at=now(), file_hashes=files,
        bookmarks={str(item): digest(item) for item in bookmarks},
        directly_consumed_inputs=read(ROOT / 'results/inputs-complete.json'), scope=report['scope']))
    print(json.dumps(dict(seal_sha256=digest(path), payloads=len(files))), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'freeze':
        assert not (ROOT / 'final-configuration.json').exists()
        write(ROOT / 'final-configuration.json', dict(frozen_at=now(), input_hashes=identity(),
            refinement_gate=.01, continuity_convergence_ratio=.8, continuity_numerical_gate=.01))
        print('Final comparisons frozen', flush=True)
    elif sys.argv[1] == 'validate':
        validate()
    elif sys.argv[1] == 'seal':
        seal()
    else:
        raise ValueError(sys.argv[1])
