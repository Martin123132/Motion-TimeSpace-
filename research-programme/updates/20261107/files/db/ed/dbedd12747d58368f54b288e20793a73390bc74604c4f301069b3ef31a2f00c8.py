from virtual240 import secondary_protocol
from common240 import *
import state235
import argparse


def run(hard_event, control=False):
    modest()
    config = secondary_protocol()
    original, features, models = setup(config)
    tests_owner = models[0]['difference'].tests
    mass_root = BRANCH / 'matched-mixed-state-20261026'
    moments = packet(mass_root / 'results/mass-coefficients.npz')
    mass_config = read(mass_root / 'configuration.json')
    assert config['heat'] == mass_config['heat'] and config['states'] == mass_config['states']
    assert config['spectral_domain'] == mass_config['spectral_domain']
    rows = config['reused_event_zero'][:1] if control else [row for row in config['events'] if row['event'] == hard_event]
    if not control:
        assert read(ROOT / 'results/secondary-control.json')['qualified']
    for row in rows:
        target = ROOT / ('control' if control else 'state') / event_key(row) / 'state.npz'
        if target.exists():
            metadata = read(target.with_suffix('.json'))
            assert metadata['qualified'] and digest(target) == metadata['sha256']
            continue
        parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
        assert next(entry['theta'] for entry in mass_config['events'] if entry['label'] == row['label']) == row['theta']
        checks, output = [], {}
        began = time.monotonic()
        with mp.workdps(80):
            planck = state235.phase_geometry(parameters)['planck_mass_squared']
            analytic = 2 * mp.pi * mp.mpf(str(angular.inherited.source.ALPHA)) * scalar(row['theta'])**2 / 3
            check(checks, event_key(row) + ':hard-angle-independent Planck mass functional', abs(planck / analytic - 1))
            for join in config['joins']:
                mass_coefficients = moments[f'{row["label"]}:join{join}:order6:mass_coefficients']
                mass_vector = np.r_[mass_coefficients, 0.]
                for state_index, state in enumerate(config['states']):
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                    mass_background = state235.contraction(mass_coefficients, physical[:98])
                    for degree in config['multipoles']:
                        values = {}
                        for step in config['canonical_steps']:
                            unit = state235.unit_state(parameters, features, tests_owner, join, physical, degree, step)
                            first = float(planck) * unit['mixed']['total']
                            second = float(mass_background) * unit['equilibrium']['total']
                            equilibrium_source = unit['equilibrium']['total'] @ np.array(list(map(float, physical))) if degree == 0 else np.zeros(98)
                            third = np.outer(equilibrium_source, mass_vector) if degree == 0 else np.zeros_like(first)
                            values[step] = weight * (first + second + third)
                            prefix = f'join{join}:state{state_index}:l{degree}:step{step}'
                            for name, matrix in [('statistical', weight * first), ('background_mass', weight * second),
                                ('wave_mass', weight * third), ('total', values[step])]:
                                output[prefix + ':' + name] = matrix
                                if degree < 2 and np.linalg.norm(matrix) > 0:
                                    check(checks, event_key(row) + ':' + prefix + ':' + name + ':independent gas force',
                                        np.linalg.norm(matrix[0] + matrix[-1]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300))
                            output[prefix + ':equilibrium'] = weight * float(planck) * unit['equilibrium']['total']
                        check(checks, event_key(row) + ':' + prefix + ':canonical step refinement',
                            relative(values[config['canonical_steps'][0]], values[config['canonical_steps'][1]]), config['refinement_tolerance'])
        if control:
            reference = packet(mass_root / 'runs' / row['label'] / 'state.npz')
            for name in output:
                check(checks, event_key(row) + ':saved displaced-state replay:' + name, relative(output[name], reference[name]))
        assert all(np.all(np.isfinite(value)) for value in output.values())
        save(target, **output)
        failures = [entry for entry in checks if not entry['passed']]
        write(target.with_suffix('.json'), dict(qualified=not failures, checks=checks, failed=failures,
            sha256=digest(target), event=event_key(row), script_sha256=digest(__file__),
            configuration_sha256=digest(ROOT / 'secondary-configuration.json'), seconds=time.monotonic() - began, finished_at=now()))
        print(json.dumps(dict(state=event_key(row), checks=len(checks), failures=len(failures), seconds=time.monotonic() - began)), flush=True)
        assert not failures, failures[:3]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('event', type=int, choices=[0, 1, 2])
    arguments = parser.parse_args()
    run(arguments.event, control=arguments.event == 0)
