import argparse
from grid_common import *
from compare_responses import load_run, compare


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    assert not folder.exists()
    rows, checks, inputs = [], [], [ROOT / 'compare_responses.py']
    for fixture in ['heavy', 'cold', 'synthetic']:
        labels = [fixture + '-' + arguments.first, fixture + '-' + arguments.second]
        left, right = load_run(labels[0]), load_run(labels[1])
        if fixture == 'synthetic':
            elastic_left, elastic_right = None, None
        else:
            labels += [labels[0] + '-elastic', labels[1] + '-elastic']
            elastic_left, elastic_right = load_run(labels[2]), load_run(labels[3])
        sectors, diagnostics, equilibrium_error = compare(left, right, elastic_left, elastic_right)
        checks.extend(dict(name=fixture + ':' + row['sector'] + ': relative response refinement',
                           passed=row['meets_accuracy_gate'], relative_error=row['relative_discrepancy'])
                      for row in sectors)
        checks.append(dict(name=fixture + ': same-grid elastic equilibrium agreement',
                           passed=equilibrium_error < 1e-14, value=equilibrium_error))
        rows.append(dict(fixture=fixture, sectors=sectors, degree_diagnostics=diagnostics))
        for label in labels:
            inputs.append(ROOT / 'runs' / label / 'status.json')
            inputs.extend((ROOT / 'runs' / label).glob('*.npz'))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        first=arguments.first, second=arguments.second, rows=rows, gate=.002,
                        comparison='Same response norm and fixed gate as the retained original failed trials.',
                        common_frequency_domain_only=True), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          rows=[dict(fixture=row['fixture'], sectors=row['sectors']) for row in rows])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--first', required=True)
    parser.add_argument('--second', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
