import argparse
from matched_weak import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--virtual-order', type=int, required=True)
    parser.add_argument('--angular', type=int, default=6)
    parser.add_argument('--radial', type=int, default=40)
    arguments = parser.parse_args()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    metadata = json.loads((PARENT / 'results/saved-state/status.json').read_text())
    temperature = metadata['reference_temperature']
    velocity = np.array([.02, .005, -.01]) * math.sqrt(temperature / .00045962015785263325)
    parameters = source.context(temperature, .1, velocity, temperature)
    started = time.monotonic()
    tensor, virtual = source.virtual_map(parameters, arguments.virtual_order)
    result = matched(parameters, virtual[0, 0], arguments.angular, arguments.radial)
    total = result['total']
    null = np.array([1., 0., 0., 1.])
    checks = [
        dict(name='New-temperature matched weak matrix is finite', passed=bool(np.isfinite(total).all())),
        check('New-temperature common-energy null',
              np.linalg.norm(total @ null) / np.linalg.norm(total), 2e-7),
        check('New-temperature symmetry', relative(total, total.T), 1e-12)]
    np.savez(folder / 'matrix.npz', total=total, born=result['born'], virtual_map=virtual,
             tensor=tensor, real=result['real']['total'], state=result['state']['total'])
    finish(folder, dict(checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), arguments=vars(arguments),
           temperature=temperature, velocity=velocity.tolist(), elapsed_seconds=time.monotonic() - started,
           matched_norm=float(np.linalg.norm(total)),
           correction_over_born_norm=float(np.linalg.norm(total) / np.linalg.norm(result['born'])),
           thermal_virtual_scalar=float(virtual[0, 0]),
           new_loop_evaluated_not_rescaled=True,
           scope='A conditional kinetic probe at the inherited midpoint reference temperature; velocity scaled to the thermal range, not a population average.'),
           __file__, [PARENT / 'results/saved-state/status.json',
                      PARENT / 'backgrounds/heavy-derived-gaunt/history.npz'])
    print(json.dumps(dict(name=arguments.name, seconds=time.monotonic() - started,
                         failed=[row for row in checks if not row['passed']],
                         norm=float(np.linalg.norm(total)),
                         virtual=float(virtual[0, 0]))), flush=True)


if __name__ == '__main__':
    main()
