import argparse
from infrared_ladder import *


def main(arguments):
    modest()
    parent = ROOT / 'banks' / arguments.parent
    ladder = InfraredLadder(parent)
    source = json.loads((parent / 'status.json').read_text())
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    temperatures = np.sort(np.r_[ladder.temperatures, (ladder.temperatures[:-1] + ladder.temperatures[1:]) / 2])
    checks = []
    started = time.perf_counter()
    for index, theta in enumerate(temperatures):
        if index % 2 == 0:
            block = ladder.blocks[index // 2]
            with np.load(parent / ('planck-' + str(index // 2) + '.npz')) as saved:
                discarded = float(saved['discarded_pair_weight'])
        else:
            events = thermal_wave.prior.event_geometry(theta, source['event_order'])
            block, discarded = scalar_physical_block(ladder.basis, theta, events)
        values = linalg.eigh(block, ladder.basis.mass, eigvals_only=True)
        null = float(linalg.norm(block @ ladder.basis.chemical) / (linalg.norm(block) * linalg.norm(ladder.basis.chemical)))
        checks.extend([dict(name='Dissipation at temperature' + str(index), passed=float(max(values)) < 1e-9, value=float(max(values))),
                       dict(name='Compton number null at temperature' + str(index), passed=null < 1e-10, value=null)])
        np.savez_compressed(folder / ('planck-' + str(index) + '.npz'), stiffness=block, mass=ladder.basis.mass,
                            theta=theta, discarded_pair_weight=discarded, eigenvalues=values)
        print(json.dumps(dict(temperature=index, elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        basis_spec=ladder.specification, event_order=source['event_order'], temperatures=temperatures.tolist(),
        parent=arguments.parent, exact_new_midpoint_kernels=True), __file__,
        [ROOT / 'infrared_ladder.py', *ladder.inputs, THERMAL_STAGE / 'build_spectral_kernel.py'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
