from integrate236 import *


def sum_rays(anchor, order, config, checks, inputs):
    result, compensation = {}, {}
    expected = len(list(angular.inherited.source.angular_nodes(config['angular_order'])))
    for ray in range(expected):
        stem = ROOT / 'rays' / anchor / f'order{order}' / f'ray-{ray:02d}'
        report = read(stem.with_suffix('.json'))
        assert report['configuration_sha256'] == digest(ROOT / 'integration-configuration.json')
        assert report['anchor'] == anchor and report['order'] == order and report['ray'] == ray
        register(inputs, stem.with_suffix('.npz'), report['sha256'])
        register(inputs, stem.with_suffix('.json'))
        values = packet(stem.with_suffix('.npz'))
        for key, value in values.items():
            if key not in result:
                result[key] = np.zeros_like(value)
                compensation[key] = np.zeros_like(value)
            change = value - compensation[key]
            updated = result[key] + change
            compensation[key] = (updated - result[key]) - change
            result[key] = updated
        check(checks, f'{anchor}:order{order}:ray{ray}:independent event four-force', report['maximum_independent_four_force_residual'])
    return result


def main(anchor):
    modest()
    config, frozen = run_protocol()
    target = ROOT / 'results' / f'{anchor}-assessment.json'
    assert not target.exists()
    inputs, checks, records, output = {}, [], [], {}
    totals = {order: sum_rays(anchor, order, config, checks, inputs) for order in frozen['orders']}
    virtual = packet(PARENT / 'results/virtual-state-combined.npz')
    register(inputs, PARENT / 'results/virtual-state-combined.npz')
    row = next(row for row in config['events'] if row['label'] == anchor)
    saved_linear = packet(row['operator_path'])
    register(inputs, row['operator_path'], row['operator_sha256'])
    active = list(range(96)) + [98]
    for join in (0, 1):
        for degree in (0, 1, 2):
            for mode in ('control', 'difference'):
                key = f'{mode}:join{join}:l{degree}:total'
                coarse, fine = (totals[order][key] for order in frozen['orders'])
                for state in range(7):
                    prefix = f'{anchor}:join{join}:l{degree}:{mode}:state{state}'
                    error = relative(coarse[state], fine[state])
                    check(checks, prefix + ':radial refinement', error, config['refinement_tolerance'])
                    gas_error = relative(coarse[state, -1], fine[state, -1])
                    if degree < 2:
                        check(checks, prefix + ':gas radial refinement', gas_error, config['refinement_tolerance'])
                        force = np.linalg.norm(fine[state, 0] + fine[state, -1]) / max(np.linalg.norm(fine[state, 0]) + np.linalg.norm(fine[state, -1]), 1e-300)
                        check(checks, prefix + ':independent integrated gas force', force)
                    records.append(dict(anchor=anchor, join=join, degree=degree, mode=mode, state=state,
                        refinement=error, gas_refinement=gas_error, norm=float(np.linalg.norm(fine[state]))))
                if degree == 0:
                    component = 0 if mode == 'control' else 1
                    reference = saved_linear['high'][component, :, :, join] + saved_linear['low'][component, :, :, join]
                    replay = relative(fine[0][:, active], reference)
                    check(checks, f'{anchor}:join{join}:{mode}:inherited linear limit different quadrature', replay, config['refinement_tolerance'])
                    records.append(dict(anchor=anchor, join=join, degree=degree, mode=mode, inherited_linear_replay=replay,
                        comparison='fine union rule versus saved original separate spontaneous/thermal radial18 rule'))
                for order in frozen['orders']:
                    for part in ('finite', 'logarithm', 'total'):
                        output[f'order{order}:{mode}:join{join}:l{degree}:{part}'] = totals[order][f'{mode}:join{join}:l{degree}:{part}']
            for state_index, history in enumerate(config['states']):
                prefix = f'{anchor}:join{join}:{history["model"]}:{history["history"]}:l{degree}'
                coarse = totals[18][f'difference:join{join}:l{degree}:total'][state_index + 1] + virtual[prefix + ':coarse']
                fine = totals[26][f'difference:join{join}:l{degree}:total'][state_index + 1] + virtual[prefix + ':fine']
                output[prefix + ':finite_matched_coarse'] = coarse
                output[prefix + ':finite_matched_fine'] = fine
                error = relative(coarse, fine)
                check(checks, prefix + ':real plus virtual plus state refinement', error, config['refinement_tolerance'])
                if degree < 2:
                    check(checks, prefix + ':real plus virtual plus state force',
                        np.linalg.norm(fine[0] + fine[-1]) / max(np.linalg.norm(fine[0]) + np.linalg.norm(fine[-1]), 1e-300))
                records.append(dict(anchor=anchor, join=join, degree=degree, model=history['model'], history=history['history'],
                    matched_refinement=error, real_over_matched=float(np.linalg.norm(totals[26][f'difference:join{join}:l{degree}:total'][state_index + 1]) / max(np.linalg.norm(fine), 1e-300))))
    save(target.with_suffix('.npz'), **output)
    failures = [row for row in checks if not row['passed']]
    write(target, dict(state='complete', qualified=not failures, checks=checks, failed=failures, records=records,
        directly_consumed_inputs=inputs, output_sha256=digest(target.with_suffix('.npz')), script_sha256=digest(Path(__file__)), finished_at=now(),
        full_finite_real_anchor_integrated=True, inclusive_physical_claim=False, exterior_supplied=False,
        scope='Original angular4 and radial18/26 finite-domain real control/remainder; six mixed states plus saved virtual/state, not an angular/exterior completion'))
    print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=failures[:12], failure_count=len(failures),
        maximum_radial_refinement=max(row['refinement'] for row in records if 'refinement' in row))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('anchor', choices=['warm', 'middle', 'cold'])
    main(parser.parse_args().anchor)
