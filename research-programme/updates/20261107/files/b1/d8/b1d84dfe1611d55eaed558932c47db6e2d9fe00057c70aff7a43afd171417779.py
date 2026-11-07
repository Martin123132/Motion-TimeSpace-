from bridge200 import *
import hashlib


class Equation(history.previous.ProbeEquation):
    def __init__(self, model):
        super().__init__(model, 'candidate')
        self.coefficients = bridge_packet()

    def stiffness(self, coordinate):
        local = self.operator.background.at(float(coordinate))
        offset = float(np.log(local['thermal_parameter']/self.theta0))
        block = evaluate(offset, self.coefficients)
        damping = self.operator.emission.at(local['thermal_parameter'], 'dcbr')
        rate = local['coefficient']/local['thermal_parameter']
        return smooth.corner.mp_matrix(rate*(block-damping))


def schedule(model, grid):
    seed = read(PARENT/f'histories/{model}/{grid}/complete.json')
    assert not seed['failed_checks']
    start, origin, step = float(seed['coordinate']), float(seed['source_start']), float(seed['step'])
    previous_coordinate = origin+(seed['done']-1)*step
    assert previous_coordinate < start
    target_coordinate = .90625*math.log(10)
    index = int(math.floor((start-origin)/step))+1
    coordinates = []
    while origin+index*step < target_coordinate-1e-14:
        coordinate = origin+index*step
        if coordinate > start+1e-14:
            coordinates.append(coordinate)
        index += 1
    coordinates.append(target_coordinate)
    return seed, previous_coordinate, coordinates


def run(model, grid, seconds):
    config = protocol()
    qualification = read(ROOT/'results/qualification.json')
    assert qualification['qualified']
    folder = ROOT/f'histories/{model}/{grid}'
    if (folder/'complete.json').exists():
        print(json.dumps(dict(reused=str(folder))), flush=True)
        return
    run_protocol = ROOT/'evolution-configuration.json'
    if not run_protocol.exists():
        write(run_protocol, dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
            runner_sha256=digest(Path(__file__)), bridge_sha256=digest(ROOT/'frozen/bridge.npz'),
            qualification_sha256=digest(ROOT/'results/qualification.json'), state_digits=80, audit_digits=100,
            identity_tolerance=1e-10, mesh_tolerance=.01, models=['heavy', 'cold'], grids=['half', 'quarter'],
            scheduling='existing regular lattice, actual saved previous partial step, exact final target'))
    frozen = read(run_protocol)
    assert frozen['runner_sha256'] == digest(Path(__file__))
    assert frozen['bridge_sha256'] == digest(ROOT/'frozen/bridge.npz')
    seed, previous_coordinate, coordinates = schedule(model, grid)
    restart_path = folder/'restart.json'
    if restart_path.exists():
        record = read(restart_path)
        assert record['runner_sha256'] == frozen['runner_sha256']
        chain = digest(PARENT/f'histories/{model}/{grid}/complete.json')
        for block_path in sorted((folder/'blocks').glob('*.json')):
            block = read(block_path)
            if block['stop'] > record['done']:
                continue
            assert block['previous_chain'] == chain
            chain = hashlib.sha256((chain+digest(block_path)).encode()).hexdigest()
        assert chain == record['chain']
    else:
        record = dict(done=0, total=len(coordinates), current=seed['current'], older=seed['older'],
            coordinate=seed['coordinate'], previous_coordinate=previous_coordinate,
            source_seed_sha256=digest(PARENT/f'histories/{model}/{grid}/complete.json'),
            chain=digest(PARENT/f'histories/{model}/{grid}/complete.json'), runner_sha256=frozen['runner_sha256'])
    began = time.monotonic()
    with mp.workdps(80):
        equation = Equation(model)
        current, older = history.parse_state(record['current']), history.parse_state(record['older'])
        before, older_coordinate = float(record['coordinate']), float(record['previous_coordinate'])
        block_states, block_diagnostics, block_checks = [], [], []
        block_start = record['done']
        for ordinal in range(record['done'], len(coordinates)):
            coordinate = coordinates[ordinal]
            delta, previous_delta = mp.mpf(coordinate)-mp.mpf(before), mp.mpf(before)-mp.mpf(older_coordinate)
            updated, diagnostic = equation.advance(current, older, mp.mpf(coordinate), delta, previous_delta)
            checks = history.identity_rows([dict(diagnostic, ordinal=ordinal)])
            if ordinal == len(coordinates)-1:
                with mp.workdps(100):
                    audit_equation = Equation(model)
                    audit, audit_diagnostic = audit_equation.advance(current, older, mp.mpf(coordinate), delta, previous_delta)
                    norm = lambda vector: mp.sqrt(mp.fsum(value*value for value in vector))
                    check(checks, '80/100 endpoint profile', norm(audit['profile']-updated['profile'])/norm(audit['profile']), 1e-10)
                    check(checks, '80/100 endpoint gas', (audit['gas']-updated['gas'])/max(abs(audit['gas']), mp.mpf('1e-90')), 1e-10)
            assert all(row['passed'] for row in checks), checks
            older, current = current, updated
            older_coordinate, before = before, coordinate
            serial = history.previous.serial_state(current)
            block_states.append(dict(coordinate=coordinate, state=serial))
            block_diagnostics.append(diagnostic)
            block_checks.extend(checks)
            final = ordinal == len(coordinates)-1
            if len(block_states) == 8 or final:
                block_path = folder/f'blocks/{block_start:04d}-{ordinal+1:04d}.json'
                write(block_path, dict(start=block_start, stop=ordinal+1, previous_chain=record['chain'],
                    states=block_states, diagnostics=block_diagnostics, checks=block_checks))
                chain = hashlib.sha256((record['chain']+digest(block_path)).encode()).hexdigest()
                record = dict(done=ordinal+1, total=len(coordinates), current=serial, older=history.previous.serial_state(older),
                    coordinate=coordinate, previous_coordinate=older_coordinate, source_seed_sha256=record['source_seed_sha256'],
                    chain=chain, runner_sha256=frozen['runner_sha256'], nominal_step=seed['step'],
                    last_block_sha256=digest(block_path), elapsed_session_seconds=time.monotonic()-began)
                write(restart_path, record)
                write(ROOT/'progress.json', dict(state='histories_running', model=model, grid=grid,
                    done=ordinal+1, total=len(coordinates), seconds=time.monotonic()-began))
                print(json.dumps(dict(model=model, grid=grid, done=ordinal+1, total=len(coordinates), seconds=time.monotonic()-began)), flush=True)
                block_states, block_diagnostics, block_checks = [], [], []
                block_start = ordinal+1
                if final:
                    record.update(failed_checks=[], target_fraction=.90625, operator_sha256=frozen['bridge_sha256'])
                    write(folder/'complete.json', record)
                    break
                if time.monotonic()-began >= seconds:
                    print(json.dumps(dict(safe_checkpoint=True, model=model, grid=grid)), flush=True)
                    break


def assess():
    protocol()
    inputs = read(ROOT/'inputs.json')
    original, theta = previous.source.context(.90625)
    for path in original.inputs:
        saved.register(inputs, path)
    kernels_path = curvature.ROOT/'results/gas-responses.npz'
    kernels_data = packet(kernels_path)
    kernels, components = kernels_data['kernels'], list(kernels_data['components'])
    ladder, basis, theta0 = old.setup()
    rows, records = [], []
    with mp.workdps(80):
        mass = smooth.corner.mp_matrix(basis.mass)
        norm = lambda vector: mp.sqrt((vector.T*mass*vector)[0])
        for model_index, model in enumerate(('heavy', 'cold')):
            complete = {grid: read(ROOT/f'histories/{model}/{grid}/complete.json') for grid in ('half','quarter')}
            states = {grid: history.parse_state(data['current']) for grid, data in complete.items()}
            original_profile = mp.matrix([mp.mpf(float(value)) for value in original.epochs[0].original[model]])
            original_gas = mp.mpf(float(original.epochs[0].gas[model_index]))
            difference = states['half']['profile']-states['quarter']['profile']
            correction = states['quarter']['profile']-original_profile
            gas_difference = states['half']['gas']-states['quarter']['gas']
            gas_correction = states['quarter']['gas']-original_gas
            values = dict(profile_mesh=float(norm(difference)/norm(states['quarter']['profile'])),
                profile_correction_mesh=float(norm(difference)/norm(correction)),
                gas_mesh=float(abs(gas_difference/states['quarter']['gas'])),
                gas_correction_mesh=float(abs(gas_difference/gas_correction)),
                gas_correction=str(gas_correction), original_gas=str(original_gas),
                quarter_gas=str(states['quarter']['gas']), half_gas=str(states['half']['gas']))
            for key in ('profile_mesh', 'profile_correction_mesh', 'gas_mesh', 'gas_correction_mesh'):
                check(rows, model+':'+key, values[key], .01)
            for component in (0,4,5):
                for join in (0,1):
                    kernel = kernels[component,:,2*model_index+join]
                    check(rows, f'{model}:{components[component]}:join{join}:gas-kernel mesh', values['gas_correction_mesh'], .01)
                    scale=max(abs(kernel[0]),abs(kernel[-1]),1e-300)
                    check(rows, f'{model}:{components[component]}:join{join}:saved kernel exchange', (kernel[0]+kernel[-1])/scale, 1e-10)
            diagnostics=[]
            for grid in ('half','quarter'):
                for path in sorted((ROOT/f'histories/{model}/{grid}/blocks').glob('*.json')):
                    data=read(path)
                    rows.extend(dict(row,name=f'{model}:{grid}:'+row['name']) for row in data['checks'])
                    diagnostics.extend(data['diagnostics'])
            values.update(model=model, maximum_step_ratio=max(float(item['ratio']) for item in diagnostics),
                minimum_capacity=min(float(item['denominator']) for item in diagnostics))
            records.append(values)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs.json', inputs)
    write(ROOT/'results/history-validation.json',dict(checks=rows, failed_checks=failed, records=records,
        full_source_retested=False, original_reference='saved original bank history at fraction .90625',
        kernel_scope='gas-only projection with fixed saved anchor kernels; full temperature-dependent source pending'))
    print(json.dumps(dict(checks=len(rows),failed=failed,records=records)),flush=True)


if __name__ == '__main__':
    previous.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase', choices=['run','assess'])
    parser.add_argument('--model', choices=['heavy','cold'])
    parser.add_argument('--grid', choices=['half','quarter'])
    parser.add_argument('--seconds', type=float, default=2400)
    args=parser.parse_args()
    if args.phase=='run':
        run(args.model,args.grid,args.seconds)
    else:
        assess()
