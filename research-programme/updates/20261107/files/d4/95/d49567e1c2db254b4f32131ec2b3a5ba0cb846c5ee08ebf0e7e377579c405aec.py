from outer_inputs import *
from compare_source_vectors import dual_norm
import sampled_gould_control as leading


def compact_rule(order, minimum, maximum, pivot=.1):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    lower, upper = (minimum - pivot) / (minimum + pivot), (maximum - pivot) / (maximum + pivot)
    compact = (lower + upper) / 2 + (upper - lower) * nodes / 2
    frequency = pivot * (1 + compact) / (1 - compact)
    measure = (upper - lower) * weights * pivot / (1 - compact)**2
    return list(zip(frequency, measure))


def main():
    modest()
    folder = ROOT / 'runs/compact-control-pilot'
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    spectra = Spectra(.5)
    assert spectra.basis.pivot == .1
    source_path = ROOT / 'runs/s4-h3-g2-2-4/status.json'
    theta = json.loads(source_path.read_text())['configuration']['temperature']
    identities = list(population_nodes(theta, 4))
    velocities = np.array(list(dict.fromkeys(tuple(item['velocity']) for item in identities)))
    first = velocities[0]
    second = velocities[np.argmin(np.linalg.norm(velocities + first, axis=1))]
    assert np.linalg.norm(first + second) < 1e-14
    selected = [first, second]
    model, radial = SplitReal(spectra, 'control'), PanelRule(.5)
    hard_nodes, hard_weights = np.polynomial.legendre.leggauss(3)
    checks, inputs, sources, rows = [], [source_path], {}, []
    started = time.monotonic()
    for order in [96, 128, 160]:
        total = np.zeros((98, 4))
        incoming = compact_rule(order, 1e-5, 24.)
        normalization_error = abs(sum(weight for frequency, weight in incoming) / (24. - 1e-5) - 1)
        maximum_null = 0.
        index = 0
        for velocity in selected:
            for frequency, seed_weight in incoming:
                for cosine, hard_weight in zip(hard_nodes, hard_weights):
                    path = folder / 'nodes' / f'n{order}' / f'{index // 500:03d}' / f'{index:05d}.npz'
                    identity = dict(frequency=float(frequency), seed_weight=float(seed_weight),
                        cosine=float(cosine), hard_weight=float(hard_weight), velocity=velocity.tolist())
                    parameters = weak.source.context(theta * frequency, cosine, velocity, theta)
                    weight = .5 * seed_weight * frequency**2 / math.expm1(frequency) / I3
                    weight *= 2 * np.pi * hard_weight * parameters['born_differential_over_thomson']
                    if path.exists():
                        saved = dict(np.load(path))
                        assert json.loads(str(saved['identity'])) == identity
                        assert abs(float(saved['weight']) / weight - 1) < 1e-14
                    else:
                        result = model.real(parameters, angular=4, radial=18, rule=radial)
                        saved = dict(control=result['total'], event_energy_null=result['event_energy_null'],
                            identity=json.dumps(identity, sort_keys=True), weight=weight)
                        path.parent.mkdir(parents=True, exist_ok=True)
                        temporary = path.with_suffix('.tmp')
                        with temporary.open('wb') as handle:
                            np.savez(handle, **saved)
                        temporary.replace(path)
                    total -= weight * saved['control']
                    maximum_null = max(maximum_null, float(saved['event_energy_null']))
                    inputs.append(path)
                    index += 1
                    if index % 96 == 0:
                        progress = dict(state='running', order=order, completed_nodes=index,
                            total_nodes=6 * order, elapsed_seconds=time.monotonic() - started, pid=os.getpid())
                        write_json(folder / 'progress.json', progress)
                        print(json.dumps(progress), flush=True)
        original_incoming, original_radial = leading.incoming_rule, leading.logarithmic_rule
        leading.incoming_rule, leading.logarithmic_rule = compact_rule, radial
        try:
            sampled = leading.sampled(spectra, model.tests, theta, order, 18)
        finally:
            leading.incoming_rule, leading.logarithmic_rule = original_incoming, original_radial
        sources[order] = total - sampled
        np.savez(folder / f'compact-{order}.npz', control=total, sampled_leading=sampled,
            kinematic_remainder=sources[order], mass=spectra.basis.mass)
        checks.extend([
            dict(name=f'Positive compact frequency measure and normalization: n{order}',
                value=float(normalization_error), passed=bool(normalization_error < 1e-7 and min(weight for frequency, weight in incoming) > 0)),
            dict(name=f'All96 four-profile conditional control and exact event exchange: n{order}',
                value=maximum_null, passed=bool(np.isfinite(sources[order]).all() and maximum_null < 1e-10)),
        ])
        print(json.dumps(dict(order=order, nodes=index, complete=True)), flush=True)
    for lower, upper in [(96, 128), (128, 160)]:
        relative = dual_norm((sources[lower] - sources[upper])[1:-1], spectra.basis.mass)
        relative /= dual_norm(sources[upper][1:-1], spectra.basis.mass)
        rows.append(dict(lower=lower, upper=upper, relative_change=relative.tolist()))
        checks.append(dict(name=f'Conditional full96 control compact-grid refinement within1percent: n{lower}-n{upper}',
            value=float(relative.max()), passed=bool(relative.max() < .01)))
    finish(folder, dict(checks=checks, comparisons=rows, nodes=6 * (96 + 128 + 160),
        electron_pair=np.array(selected).tolist(), electron_pair_weights=[.5, .5],
        scope='Conditional actual antipodal electron pair, control-minus-leading only; not the full16-electron source.',
        basis_coordinate='z=(x-pivot)/(x+pivot)', original_frequency_window=[1e-5, 24.],
        all_dimension_remainder_gate_closed=False, incoming_frequency_gate_closed=False,
        new_virtual_loop_evaluations=0, new_parent_history=False, full_parent_feedback_applied=False),
        __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(checks=checks, comparisons=rows)), flush=True)


if __name__ == '__main__':
    main()
