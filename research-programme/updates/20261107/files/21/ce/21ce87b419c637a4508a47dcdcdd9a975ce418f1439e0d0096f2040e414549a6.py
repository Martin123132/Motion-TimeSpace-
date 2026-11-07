from angular232 import *


def load_packet(probe, degree, angular, radial, variant, inputs):
    folder = ROOT / 'runs' / f'{probe}-{degree}-{angular}-{radial}-{variant}'
    folder = ROOT / 'runs' / f'{probe}-l{degree}-{angular}-{radial}-{variant}'
    report = read(register(inputs, folder / 'status.json'))
    assert report['state'] == 'complete'
    path = register(inputs, folder / 'matrix.npz')
    assert digest(path) == report['matrix_sha256']
    with np.load(path) as archive:
        values = dict(archive)
    return report, values


def main():
    modest()
    config = protocol()
    frozen = read(ROOT / 'assessment-configuration.json')
    for name, expected in frozen['hashes'].items():
        assert digest(ROOT / name) == expected
    assert read(ROOT / 'progress.json')['state'] == 'complete'
    preflight = read(ROOT / 'results/preflight.json')
    inputs = read(ROOT / 'results/preflight-inputs.json')
    checks = list(preflight['checks'])
    comparisons = []
    for probe in config['probes']:
        label = probe['label']
        for degree in config['degrees']:
            coarse_report, coarse = load_packet(label, degree, 6, 40, 'original', inputs)
            fine_report, fine = load_packet(label, degree, 8, 56, 'original', inputs)
            for name, report in [('coarse', coarse_report), ('fine', fine_report)]:
                checks.extend(dict(row, name=f'{label}:l{degree}:{name}:' + row['name']) for row in report['checks'])
            error = relative(coarse['total'], fine['total'])
            check(checks, f'{label}:l{degree}: actual matched correction refinement', error, .002)
            row = dict(probe=label, degree=degree, quadrature_relative_error=error,
                correction_norm=float(np.linalg.norm(fine['total'])), born_norm=float(np.linalg.norm(fine['born'])),
                correction_over_born=float(np.linalg.norm(fine['total']) / np.linalg.norm(fine['born'])),
                diagonal=float(fine['total'][0, 0]))
            if degree == 0:
                with np.load(register(inputs, Path(probe['source']) / 'matrix.npz')) as old:
                    replay = relative(fine['total'], old['total'])
                check(checks, label + ': independent original monopole replay', replay, 1e-7)
                row['monopole_replay'] = replay
            else:
                variants = {}
                for variant in ('profile', 'separator', 'floor1e3', 'floor1e4'):
                    report, matrix = load_packet(label, degree, 8, 56, variant, inputs)
                    checks.extend(dict(entry, name=f'{label}:l{degree}:{variant}:' + entry['name']) for entry in report['checks'])
                    variants[variant] = relative(matrix['total'], fine['total'])
                check(checks, f'{label}:l{degree}: thermal subtraction profile with finite conversion', variants['profile'], 2e-7)
                check(checks, f'{label}:l{degree}: vacuum matching separator', variants['separator'], 2e-7)
                check(checks, f'{label}:l{degree}: lower floor approaches zero-floor source', int(variants['floor1e4'] >= variants['floor1e3']), 0)
                row.update(variants)
                row['floor_error_ratio'] = variants['floor1e4'] / variants['floor1e3']
            comparisons.append(row)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=232, state='complete', finished_at=now(), qualified=all(row['passed'] for row in checks),
        checks=checks, failed=[row for row in checks if not row['passed']], comparisons=comparisons,
        scope='Conditional scalar-intensity multipole0/1/2 matching with independent gas momentum; no population or polarization closure')
    assert not (ROOT / 'results/assessment.json').exists()
    write(ROOT / 'results/assessment-inputs.json', inputs)
    write(ROOT / 'results/assessment.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], comparisons=comparisons)), flush=True)


if __name__ == '__main__':
    main()
