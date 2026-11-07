from tail243 import *
import hashlib


def gate(checks, name, value, limit):
    check(checks, name, value, limit)


def sample(values, frequency, targets):
    return interp1d(np.log(frequency), values, axis=1, bounds_error=True)(np.log(targets))


def moments(frequency):
    weights = np.empty(len(frequency))
    weights[1:-1] = (frequency[2:] - frequency[:-2]) / 2
    weights[0], weights[-1] = (frequency[1] - frequency[0]) / 2, (frequency[-1] - frequency[-2]) / 2
    bose = np.exp(-frequency) / (-np.expm1(-frequency))**2
    return weights * frequency**3 * bose / (2 * tail.owner.special.zeta(3)), weights * frequency**4 * bose / tail.owner.I3


def all_arms(state):
    return np.stack([state[:, :, 0], state[:, :, 0] + state[:, :, 1],
        state[:, :, 0] + state[:, :, 2], state[:, :, 1], state[:, :, 2]], axis=2)


def compare(model, title, before, after, checks, frozen):
    core = np.geomspace(1e-5, 1e-4, 101)
    frequency = after['frequency']
    old = interp1d(before['expansion'], before['state'], axis=0)(after['expansion'])
    first, second = all_arms(old), all_arms(after['state'])
    difference = first - second
    labels = ['baseline', 'repaired-half', 'repaired-quarter', 'difference-half', 'difference-quarter']
    records = []
    sampled_before, sampled_after = sample(first, frequency, core), sample(second, frequency, core)
    moment_grid = np.geomspace(max(before['frequency'][0], frequency[0]), 1e-4, 401)
    moments_before = sample(first, frequency, moment_grid)
    moments_after = sample(second, frequency, moment_grid)
    for column, label in enumerate(labels):
        name = f'{model}:{title}:{label}'
        core_error = float(np.max(abs(sampled_before[:, :, column] - sampled_after[:, :, column])))
        gate(checks, name + ':inherited absolute core gate', core_error, frozen['retained_gate_core_absolute'])
        maximum_difference = float(np.max(np.linalg.norm(difference[:, :, column], axis=1)))
        maximum_reference = float(np.max(np.linalg.norm(second[:, :, column], axis=1)))
        relative_error = maximum_difference / max(maximum_reference, 1e-300)
        gate(checks, name + ':history time refinement', relative_error, frozen['history_mesh_tolerance'])
        reports = []
        for label_moment, weight in zip(('number', 'energy'), moments(moment_grid)):
            values = moments_after[:, :, column] @ weight
            deltas = (moments_before[:, :, column] - moments_after[:, :, column]) @ weight
            amplitude_envelope = float(np.max(abs(moments_after[:, :, column])) * np.sum(abs(weight)))
            magnitude, error = float(np.max(abs(values))), float(np.max(abs(deltas)))
            limit = max(frozen['retained_gate_moment_relative'] * magnitude,
                frozen['retained_gate_moment_envelope'] * amplitude_envelope)
            gate(checks, name + ':' + label_moment + ':inherited moment gate', error, limit)
            reports.append(dict(moment=label_moment, error=error, magnitude=magnitude, limit=limit))
        records.append(dict(model=model, comparison=title, arm=label, core_max_absolute=core_error,
            global_history_relative=relative_error, moments=reports))
    return records


def refinement_envelope(model, coarse, fine, data, layout, forces, checks):
    sampled = interp1d(coarse['expansion'], coarse['state'], axis=0)(fine['expansion'])
    envelope = np.zeros_like(sampled[0])
    envelope_max = np.zeros(3)
    excess, residual_max = -float('inf'), 0.
    for ordinal, coordinate in enumerate(fine['expansion'][1:], 1):
        local = operator(data, layout, coordinate)
        step = float(coordinate - fine['expansion'][ordinal - 1])
        selected = int(np.searchsorted(forces['expansion'], coordinate))
        assert forces['expansion'][selected] == coordinate
        forcing_value = forces['high'][selected] + forces['low'][selected]
        defect = sampled[ordinal] - sampled[ordinal - 1] - step * (
            local['generator'] @ sampled[ordinal] + forcing_value)
        system = sparse.eye(len(layout['frequency']), format='csc') - step * local['generator']
        right = envelope + abs(defect)
        envelope = splu(system).solve(right)
        numerical_residual = fine['state'][ordinal] - fine['state'][ordinal - 1] - step * (
            local['generator'] @ fine['state'][ordinal] + forcing_value)
        residual_max = max(residual_max, float(np.max(abs(numerical_residual))))
        error = abs(fine['state'][ordinal] - sampled[ordinal])
        excess = max(excess, float(np.max(error - envelope)))
        envelope_max = np.maximum(envelope_max, np.max(envelope, axis=0))
    scale = max(float(np.max(abs(fine['state']))), 1e-300)
    gate(checks, model + ':executed coarse-fine defect envelope', max(0, excess) / scale, 1e-10)
    return dict(final_envelope=envelope, maximum_envelope=envelope_max, maximum_excess=excess,
        maximum_BE_absolute_residual=residual_max,
        scope='Componentwise bound on compared discrete trajectories, up to recorded solve rounding; not continuum certificate')


def independent_rhs(model, baseline, data, layout, fine, checks):
    coordinate = float(fine['expansion'][-1])
    step = mp.mpf(coordinate) - mp.mpf(float(fine['expansion'][-2]))
    profiles = [list(map(lambda value: mp.mpf(float(value)), interp1d(baseline['expansion'], baseline['profiles'], axis=0)(coordinate)))]
    gases = [mp.mpf(float(np.interp(coordinate, baseline['expansion'], baseline['temperature_scaled'])))]
    for grid in ('half', 'quarter'):
        endpoint = read(DATA / f'drives/{model}-{grid}.json')['points'][-1]['state']
        parsed = history.parse_state(endpoint)
        profiles.append(parsed['profile'])
        gases.append(parsed['gas'])
    states = all_arms(fine['state'])
    for column, label in enumerate(('baseline', 'half', 'quarter')):
        slope = mp.matrix(list(map(lambda value: mp.mpf(float(value)), states[-1, :, column])))
        before = mp.matrix(list(map(lambda value: mp.mpf(float(value)), states[-2, :, column])))
        rhs, diagnostic = tail.local_rhs(data, layout, coordinate, profiles[column], gases[column], slope)
        residue = slope - before - step * rhs
        scale = prior.norm(slope) + prior.norm(before) + step * prior.norm(diagnostic['scale'])
        gate(checks, f'{model}:{label}:independent physical RHS BE identity', prior.norm(residue) / scale, 1e-10)


def freeze_assessment():
    frozen = tail_protocol()
    assert not (ROOT / 'assessment-configuration.json').exists()
    write(ROOT / 'assessment-configuration.json', dict(script_sha256=digest(__file__),
        tail_configuration_sha256=digest(ROOT / 'tail-configuration.json'), frozen_at=now(),
        comparisons=['time1 versus time2', 'time2 versus time4', 'half versus quarter on time4'],
        independent_rhs=True, discrete_defect_envelope=True, inherited_gates_unchanged=True))


def run_assessment():
    modest()
    frozen = tail_protocol()
    assessment_config = read(ROOT / 'assessment-configuration.json')
    assert assessment_config['script_sha256'] == digest(__file__)
    assert assessment_config['tail_configuration_sha256'] == digest(ROOT / 'tail-configuration.json')
    inputs, checks, refinements, summaries, output_arrays = dict(frozen['inputs']), [], [], [], {}
    for model in ('heavy', 'cold'):
        report = read(register(inputs, DATA / f'tails/{model}/complete.json'))
        checks.extend(report['checks'])
        assert report['qualified']
        config, baseline, data, layout = loaded(model, inputs)
        cases = {}
        for subdivision in (1, 2, 4):
            path = DATA / f'tails/{model}/time{subdivision}.npz'
            metadata = read(register(inputs, path.with_suffix('.json')))
            cases[subdivision] = packet(register(inputs, path, metadata['sha256']))
        for first, second in ((1, 2), (2, 4)):
            refinements.extend(compare(model, f'time{first}-time{second}', cases[first], cases[second], checks, frozen))
        fine = cases[4]
        delta_difference = fine['state'][:, :, 1] - fine['state'][:, :, 2]
        repaired_quarter = fine['state'][:, :, 0] + fine['state'][:, :, 2]
        scale = max(float(np.max(np.linalg.norm(fine['state'][:, :, 2], axis=1))), 1e-300)
        history_difference = float(np.max(np.linalg.norm(delta_difference, axis=1))) / scale
        gate(checks, model + ':half/quarter direct difference history', history_difference, frozen['history_mesh_tolerance'])
        core = np.geomspace(1e-5, 1e-4, 101)
        history_core = float(np.max(abs(sample(delta_difference, fine['frequency'], core))))
        gate(checks, model + ':half/quarter inherited core gate', history_core, frozen['retained_gate_core_absolute'])
        forces_path = DATA / f'tails/{model}/forcing.npz'
        force_meta = read(register(inputs, forces_path.with_suffix('.json')))
        forces = packet(register(inputs, forces_path, force_meta['sha256']))
        envelope = refinement_envelope(model, cases[2], fine, data, layout, forces, checks)
        with mp.workdps(80):
            independent_rhs(model, baseline, data, layout, fine, checks)
        final_state = fine['state'][-1]
        original = fine['original_stored'][-1]
        delta = final_state[:, 2]
        reference_change = final_state[:, 0] - original
        stationary = fine['stationary_diagnostic'][:, 2]
        for name, values in dict(frequency=fine['frequency'], baseline=final_state[:, 0],
                difference_half=final_state[:, 1], difference_quarter=delta,
                repaired_quarter=repaired_quarter[-1], original=original, baseline_change=reference_change,
                rhs=fine['derivative'], stationary_diagnostic=fine['stationary_diagnostic'],
                refinement_envelope=envelope['final_envelope']).items():
            output_arrays[model + ':' + name] = values
        heat = float(data['heat'])
        final_moments = []
        frequencies = np.geomspace(float(fine['frequency'][0]), 1e-4, 401)
        tail_delta = interp1d(np.log(fine['frequency']), delta)(np.log(frequencies))
        for label, weights in zip(('number', 'energy'), moments(frequencies)):
            final_moments.append(dict(moment=label, physical_fraction=heat * float(tail_delta @ weights),
                scope='Tail-only moment on [original minimum,1e-4]; not final total spectrum or gravity'))
        summaries.append(dict(model=model, heat=heat, start=float(fine['expansion'][0]), stop=float(fine['expansion'][-1]),
            conservative_damping_lower=report['conservative_whole_interval_damping'],
            baseline_change_relative_to_stored=relative(reference_change, original),
            drive_change_relative_to_baseline=relative(delta, final_state[:, 0]),
            direct_drive_change_l2=norm(delta), half_quarter_history_relative=history_difference,
            half_quarter_core_absolute=history_core,
            final_stationary_delta_error_relative=relative(delta - stationary, delta),
            final_drive_derivative_l2=norm(fine['derivative'][:, 2]),
            final_moments=final_moments,
            discrete_refinement_envelope={key: value.tolist() if hasattr(value, 'tolist') else value for key, value in envelope.items() if key != 'final_envelope'}))
    modules(inputs)
    for path, checksum in inputs.items():
        assert digest(path) == checksum, path
    destination = DATA / 'assessment/final-tails.npz'
    save(destination, **output_arrays)
    failed = [row for row in checks if not row['passed']]
    write(DATA / 'assessment/result.json', dict(qualified=not failed, checks=checks, failed=failed,
        refinements=refinements, summaries=summaries, consumed_inputs=inputs, output_sha256=digest(destination),
        script_sha256=digest(__file__), finished_at=now(), source_contracted=False, final_gravity_propagated=False))
    print(dict(checks=len(checks), failed=failed, summaries=summaries), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['freeze', 'run'])
    arguments = parser.parse_args()
    if arguments.phase == 'freeze':
        freeze_assessment()
    else:
        run_assessment()

