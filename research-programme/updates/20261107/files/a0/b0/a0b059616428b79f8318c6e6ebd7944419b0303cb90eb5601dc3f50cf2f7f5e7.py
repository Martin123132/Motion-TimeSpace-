from angular232 import *


def packet(probe, degree, angular, radial, variant):
    folder = ROOT / 'runs' / f'{probe["label"]}-l{degree}-{angular}-{radial}-{variant}'
    if (folder / 'status.json').exists():
        report = read(folder / 'status.json')
        if report['state'] == 'complete':
            assert digest(folder / 'matrix.npz') == report['matrix_sha256']
            return report
        raise RuntimeError('Inspect existing worker before retrying incomplete packet: ' + str(folder))
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / 'status.json', dict(state='running', pid=os.getpid(), started_at=now()))
    parameters = inherited.source.context(probe['temperature'], probe['lab_cosine'], probe['velocity'], probe['temperature'])
    arguments = dict(profile=.2 if variant == 'profile' else None,
        separator=.2 if variant == 'separator' else 1.,
        floor=1e-3 if variant == 'floor1e3' else (1e-4 if variant == 'floor1e4' else 0.))
    started = time.monotonic()
    lift = AngularWeak(degree)
    result = lift.matched(parameters, probe['virtual_scalar'], angular, radial, **arguments)
    checks = []
    check(checks, 'Finite projected matched source', int(not np.isfinite(result['total']).all()), 0)
    check(checks, 'Symmetric matched intensity block', relative(result['total'], result['total'].T), 1e-12)
    check(checks, 'Real events conserve photon plus gas energy', result['event_energy'], 1e-12)
    check(checks, 'Real events conserve photon plus gas momentum', result['event_momentum'], 1e-12)
    if degree <= 1:
        null = np.array([1., 0., 0., 1.])
        check(checks, 'Matched joint gas-photon common mode', np.linalg.norm(result['total'] @ null) / np.linalg.norm(result['total']), 2e-7)
    total_with_born = result['born'] + result['total']
    eigenvalues = np.linalg.eigvalsh(total_with_born)
    check(checks, 'Born plus matched source on tested probes', max(0., -float(eigenvalues[0])) / np.linalg.norm(total_with_born), 1e-10)
    save_npz(folder / 'matrix.npz', total=result['total'], born=result['born'], virtual=result['virtual'],
        state=result['state']['total'], phase=result['state']['phase'], observable=result['state']['observable'],
        canonical=result['state']['canonical'], population=result['state']['population'],
        real=result['real']['total'], spontaneous=result['real']['spontaneous'], thermal=result['real']['thermal'],
        logarithm=result['real']['logarithm'], conversion=result['real']['profile_conversion'])
    report = dict(stage=232, state='complete', pid=os.getpid(), finished_at=now(), probe=probe['label'], degree=degree,
        angular=angular, radial=radial, variant=variant, arguments=arguments, checks=checks,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        elapsed_seconds=time.monotonic() - started, matrix_sha256=digest(folder / 'matrix.npz'),
        matched_norm=float(np.linalg.norm(result['total'])), born_norm=float(np.linalg.norm(result['born'])),
        photon_energy_diagonal=float(result['total'][0, 0]),
        source_config_sha256=digest(ROOT / 'configuration.json'), new_virtual_amplitudes=False,
        scope='Conditional unpolarized intensity angular weak source, not an averaged cosmological collision bank')
    write(folder / 'status.json', report)
    print(json.dumps({name: report[name] for name in ('probe', 'degree', 'angular', 'radial', 'variant', 'qualified', 'elapsed_seconds', 'failed')}), flush=True)
    return report


def main():
    modest()
    config = protocol()
    assert read(ROOT / 'results/preflight.json')['qualified']
    started = time.monotonic()
    completed = []
    for probe in config['probes']:
        for degree in config['degrees']:
            tasks = [(6, 40, 'original'), (8, 56, 'original')]
            if degree > 0:
                tasks += [(8, 56, variant) for variant in ('profile', 'separator', 'floor1e3', 'floor1e4')]
            for angular, radial, variant in tasks:
                report = packet(probe, degree, angular, radial, variant)
                completed.append(dict(probe=probe['label'], degree=degree, angular=angular, radial=radial, variant=variant))
                write(ROOT / 'progress.json', dict(state='running', pid=os.getpid(), completed=completed, updated_at=now()))
                if time.monotonic() - started >= 3 * 3600:
                    write(ROOT / 'progress.json', dict(state='saved_time_limit', completed=completed, updated_at=now()))
                    return
    write(ROOT / 'progress.json', dict(state='complete', completed=completed, updated_at=now()))


if __name__ == '__main__':
    main()
