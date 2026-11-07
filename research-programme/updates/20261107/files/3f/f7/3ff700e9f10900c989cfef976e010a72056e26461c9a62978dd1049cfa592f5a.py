import argparse
from gould_overlap import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--fraction', required=True, type=float)
    parser.add_argument('--seed-order', default=24, type=int)
    parser.add_argument('--soft-order', default=48, type=int)
    arguments = parser.parse_args()
    folder = ROOT / 'overlaps' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(arguments.fraction)
    tests = TestFunctions(spectra.basis)
    background = thermal_wave.thermal.ThermalBackground('heavy')
    theta = background.at(spectra.coordinate)['thermal_parameter']
    arrays, metrics = {}, {}
    configurations = [
        ('joined_new_domain', 1e-6, 24., True),
        ('joined_old_overlap', 1e-5, 24., True),
        ('original_old_overlap', 1e-5, 24., False),
        ('original_full_parent', 1e-5, 60., False),
    ]
    started = time.monotonic()
    for name, floor, maximum, joined in configurations:
        forward, forward_metrics = overlap(spectra, tests, theta, arguments.seed_order, arguments.soft_order, floor, maximum, joined)
        if name == 'original_full_parent':
            arrays[name], metrics[name] = forward, forward_metrics
        else:
            inverse, inverse_metrics = overlap(spectra, tests, theta, arguments.seed_order, arguments.soft_order, floor, maximum, joined, inverse=True)
            arrays[name] = .5 * (forward + inverse)
            metrics[name] = dict(forward=forward_metrics, inverse=inverse_metrics,
                selector='One half of window(z) plus one half of window(h), with s<=h.')
    bank = inherited.SOURCE / 'banks/s960-i256/matrix.npz'
    with np.load(bank) as saved:
        matrix = saved['nonlocal_matrix']
    originals = np.repeat(np.column_stack([spectra.original['heavy'], spectra.original['cold']]), 2, axis=1)
    reference = -prior.inherited.integrated_dc.DC_CONSTANT * theta**2 * matrix @ originals
    comparison = arrays['original_full_parent'][1:-1] - reference
    norm = lambda values: np.sqrt(np.maximum(np.sum(values * linalg.solve(spectra.basis.mass, values, assume_a='pos'), axis=0), 0.))
    parent_error = float(np.max(norm(comparison) / norm(reference)))
    energy = max(float(np.max(abs(spectra.basis.temperature @ value[1:-1]))) for value in arrays.values())
    arrays['tail_domain_increment'] = arrays['joined_new_domain'] - arrays['joined_old_overlap']
    arrays['joined_state_increment'] = arrays['joined_old_overlap'] - arrays['original_old_overlap']
    arrays['domain_state_increment'] = arrays['joined_new_domain'] - arrays['original_old_overlap']
    arrays['parent_bank_reference'] = reference
    identity = arrays['domain_state_increment'] - arrays['tail_domain_increment'] - arrays['joined_state_increment']
    checks = [
        dict(name='All overlap arrays finite', passed=all(np.isfinite(value).all() for value in arrays.values())),
        dict(name='Leading Gould energy vanishes by event identity', value=energy, passed=energy < 1e-15),
        dict(name='Domain and state changes telescope without adding a second leading source', value=float(np.max(abs(identity))), passed=np.max(abs(identity)) < 1e-20),
        dict(name='Original full-domain overlap reproduces saved parent bank within1percent', value=parent_error, passed=parent_error < .01),
    ]
    np.savez(folder / 'overlap.npz', **arrays, mass=spectra.basis.mass, temperature=spectra.basis.temperature,
             chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, arguments=vars(arguments), temperature=theta, metrics=metrics,
        parent_bank_relative_error=parent_error, elapsed_seconds=time.monotonic() - started,
        inserted_in_parent=False, additional_tail_requires_consistent_companion_sources=True),
        __file__, [*spectra.inputs, bank, bank.parent / 'status.json', background.parent.source, background.native_constants])
    print(json.dumps(dict(name=arguments.name, checks=len(checks), failed=[row for row in checks if not row['passed']],
        parent_error=parent_error, elapsed=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    main()
