from bridge200 import *


def main():
    config = protocol()
    coefficients = bridge_packet()
    ladder, basis, theta0 = old.setup()
    factor = linear.cholesky(basis.mass, lower=True)
    orthogonal = linear.null_space((factor.T @ basis.chemical)[None, :])
    rows, spectra, capacities, projections = [], [], [], []
    rows.extend(read(ROOT / 'frozen/bridge.json')['checks'])
    for index in range(3):
        rows.extend(dict(row, name=f'probe{index}:'+row['name']) for row in read(ROOT / f'physical/probe-{index}/validation.json')['checks'])
    for index, block in enumerate(coefficients['controls']):
        norm = np.linalg.norm(block)
        check(rows, f'Bernstein{index}:symmetry', np.linalg.norm(block-block.T)/norm, 1e-10)
        check(rows, f'Bernstein{index}:chemical null', np.linalg.norm(block@basis.chemical)/(norm*np.linalg.norm(basis.chemical)), 1e-10)
        eigenvalues = linear.eigvalsh(orthogonal.T@smooth.whiten(block, factor)@orthogonal)
        check(rows, f'Bernstein{index}:nonpositive', max(0., float(eigenvalues[-1]))/max(abs(eigenvalues)), 1e-10)
        spectra.append(dict(control=index, minimum=float(eigenvalues[0]), maximum=float(eigenvalues[-1])))
    check(rows, 'energy row equals M times temperature mode', relative(basis.energy, basis.mass@basis.temperature), 1e-10)
    for power in range(4):
        value_warm, value_cold = WARM**power, COLD**power
        slope_warm = 0 if power == 0 else power*WARM**(power-1)
        slope_cold = 0 if power == 0 else power*COLD**(power-1)
        controls = np.array([value_warm, value_warm+(COLD-WARM)*slope_warm/3,
                             value_cold-(COLD-WARM)*slope_cold/3, value_cold])
        for offset in coefficients['offsets']:
            check(rows, f'cubic polynomial identity {power}:{offset}', evaluate(offset, dict(controls=controls))-offset**power, 1e-10)
    targets = [(f'probe-{index}', float(offset)) for index, offset in enumerate(coefficients['offsets'])] + [('cold', COLD)]
    kernels_path = curvature.ROOT/'results/gas-responses.npz'
    kernels_data = packet(kernels_path)
    kernels, components = kernels_data['kernels'], list(kernels_data['components'])
    inputs = read(ROOT/'inputs.json')
    saved.register(inputs, kernels_path)
    with mp.workdps(80):
        convert = smooth.corner.mp_matrix
        mass = convert(basis.mass)
        energy = mp.matrix(list(basis.energy)).T
        dual = mp.lu_solve(mass.T, energy.T).T
        template = mp.matrix(list(basis.temperature))
        warm_block = convert(coefficients['controls'][0])
        for model_index, model in enumerate(('heavy', 'cold')):
            operator = smooth.corner.Operators(model, ladder)
            for path in operator.inputs:
                saved.register(inputs, path)
            start = read(PARENT/f'histories/{model}/quarter/complete.json')
            state = history.parse_state(start['current'])
            warm_coordinate = float(start['coordinate'])
            local = operator.background.at(warm_coordinate)
            rate = mp.mpf(local['coefficient']/local['thermal_parameter'])
            emission = convert(operator.emission.at(local['thermal_parameter'], 'dcbr'))
            heat = mp.mpf(operator.background.chi)
            def gas(block):
                stiffness = rate*(block-emission)
                capacity = heat-(dual*stiffness*template)[0]
                numerator = 1+(dual*stiffness*state['profile'])[0]
                assert capacity > 0
                return -numerator/capacity, capacity
            warm_gas, warm_capacity = gas(warm_block)
            for tag, offset in targets:
                actual = packet(ROOT/f'physical/{tag}/result.npz')['actual']
                prediction = evaluate(offset, coefficients)
                actual_mp, predicted_mp = convert(actual), convert(prediction)
                actual_gas, actual_capacity = gas(actual_mp)
                predicted_gas, predicted_capacity = gas(predicted_mp)
                exact_difference = -(rate*dual*(predicted_mp-actual_mp)*(state['profile']-template*actual_gas))[0]/predicted_capacity
                observed_difference = predicted_gas-actual_gas
                scale = max(abs(actual_gas-warm_gas), mp.mpf('1e-90'))
                check(rows, f'{model}:{tag}:gas resolvent identity', (observed_difference-exact_difference)/scale, 1e-10)
                error = float(abs(observed_difference)/scale)
                check(rows, f'{model}:{tag}:fixed-state gas change', error, .01)
                for component in (0, 4, 5):
                    for join in (0, 1):
                        column = 2*model_index+join
                        kernel = kernels[component, :, column]
                        actual_response = float(actual_gas-warm_gas)*kernel
                        predicted_response = float(predicted_gas-warm_gas)*kernel
                        def norm(vector):
                            return np.linalg.norm(linear.solve_triangular(factor, vector[1:97], lower=True))
                        response_error = norm(predicted_response-actual_response)/norm(actual_response)
                        check(rows, f'{model}:{tag}:{components[component]}:join{join}:gas kernel', response_error, .01)
                        check(rows, f'{model}:{tag}:{components[component]}:join{join}:linearity', response_error-error, 1e-10)
                        exchange_scale = max(abs(actual_response[0]), abs(actual_response[-1]), 1e-300)
                        check(rows, f'{model}:{tag}:{components[component]}:join{join}:exchange', (actual_response[0]+actual_response[-1])/exchange_scale, 1e-10)
                projections.append(dict(model=model, target=tag, offset=offset, relative_gas_error=error,
                    actual_gas_change=str(actual_gas-warm_gas), predicted_gas_change=str(predicted_gas-warm_gas),
                    capacity=str(predicted_capacity), scope='fixed warm photon state, rate and emission; saved gas kernels'))
            for offset in [WARM, *coefficients['offsets'], COLD]:
                coordinate=.875*config['expansion_span']-float(offset)
                local=operator.background.at(coordinate)
                damping=operator.emission.at(local['thermal_parameter'], 'dcbr')
                check(rows, f'{model}:{offset}:emission symmetry', relative(damping, damping.T), 1e-10)
                eigen=linear.eigvalsh(smooth.whiten(damping, factor))
                check(rows, f'{model}:{offset}:emission PSD', max(0., -float(eigen[0]))/max(abs(eigen)), 1e-10)
                stiffness=local['coefficient']/local['thermal_parameter']*(evaluate(float(offset), coefficients)-damping)
                eigen=linear.eigvalsh(smooth.whiten(stiffness, factor))
                check(rows, f'{model}:{offset}:K NSD', max(0., float(eigen[-1]))/max(abs(eigen)), 1e-10)
                for grid in ('half', 'quarter'):
                    step=read(PARENT/f'histories/{model}/{grid}/complete.json')['step']
                    alpha=1.5/step
                    response=linear.solve(alpha*basis.mass-stiffness, -stiffness@basis.temperature)
                    projected=float(basis.energy@response)
                    lower=operator.background.chi*(alpha+1)
                    denominator=lower+alpha*projected
                    check(rows, f'{model}:{offset}:{grid}:positive capacity', int(lower<=0 or denominator<=0 or projected<0), 0)
                    capacities.append(dict(model=model, offset=float(offset), grid=grid, lower_bound=lower, denominator=denominator))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs.json', inputs)
    write(ROOT/'results/qualification.json', dict(checks=rows, failed_checks=failed, spectra=spectra, capacities=capacities,
        projections=projections, qualified=not failed, qualifier_sha256=digest(Path(__file__)),
        scope='Finite operator and fixed-state gas-kernel tests; not full microscopic source or observations'))
    write(ROOT/'progress.json', dict(state='bridge_qualified' if not failed else 'bridge_not_qualified'))
    print(json.dumps(dict(checks=len(rows), failed=failed, worst_gas_error=max(row['relative_gas_error'] for row in projections))), flush=True)


if __name__ == '__main__':
    previous.source.modest()
    main()
