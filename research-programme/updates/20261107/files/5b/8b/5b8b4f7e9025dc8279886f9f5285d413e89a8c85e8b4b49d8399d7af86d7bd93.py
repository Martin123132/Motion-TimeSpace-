import argparse
from polar_nodes import *


def run_part(part, shard, deadline):
    folder = ROOT / 'runs' / f'{part}-p3-shard{shard}'
    if (folder / 'COMPLETE').exists():
        report = json.loads((folder / 'status.json').read_text())
        assert report['all_checks_passed'] and report['script_sha256'] == digest(__file__)
        for filename, expected in report['input_hashes'].items():
            assert digest(filename) == expected, filename
        print(json.dumps(dict(part=part, shard=shard, state='already_complete')), flush=True)
        return True
    proof_path = ROOT / 'results/symmetry/status.json'
    proof = json.loads(proof_path.read_text())
    assert proof['all_checks_passed'] and (proof_path.parent / 'COMPLETE').exists()
    for filename, expected in proof['input_hashes'].items():
        assert digest(filename) == expected, filename
    parent_source = PARENT / 'results/combined-source/source.npz'
    parent_status = PARENT / 'runs/expensive-h5-az8/status.json'
    theta = json.loads(parent_status.read_text())['configuration']['temperature']
    spectra = Spectra(.5)
    model = FastSplit(spectra, 'difference') if part == 'expensive' else SplitReal(spectra, 'control')
    keys = ['difference', 'virtual', 'state'] if part == 'expensive' else ['control']
    rule = PanelRule(.5)
    nodes = [identity for identity in physical_nodes(theta, part) if identity['index'] % 2 == shard]
    config = dict(part=part, shard=shard, shards=2, hard_order=5, electron_radial=2, electron_polar=3, electron_azimuthal=8,
        physical_electrons=48, scalar_representatives=30, incoming_rule='seed4' if part == 'expensive' else 'compact128',
        temperature=theta, soft_angular=4, panel_order=18, panel_width=.5, virtual_order=2,
        fingerprints={str(path):digest(path) for path in [Path(__file__), ROOT / 'polar_common.py', ROOT / 'polar_nodes.py',
            ROOT / 'ACCEPTANCE.md', proof_path, parent_source, PARENT / 'results/stage-integrity.json']})
    folder.mkdir(parents=True, exist_ok=True)
    config_path = folder / 'configuration.json'
    if config_path.exists():
        assert json.loads(config_path.read_text()) == config
    else:
        write_json(config_path, config)
    started, maximum_null = time.monotonic(), 0.
    totals = {key:np.zeros((98,4)) for key in keys}
    inputs = [config_path, proof_path, parent_source, parent_status]
    for ordinal, identity in enumerate(nodes):
        if time.monotonic() >= deadline:
            progress = dict(state='paused_at_saved_node', part=part, shard=shard, completed_nodes=ordinal,
                total_nodes=len(nodes), elapsed_seconds=time.monotonic()-started, pid=os.getpid(),
                reason='Worker wall-time budget; resume same configuration without deleting completed nodes.')
            write_json(folder / 'progress.json', progress)
            print(json.dumps(progress), flush=True)
            return False
        index = identity['index']
        path = folder / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
        parameters, weight = parameters_and_weight(theta, identity)
        if path.exists():
            saved = dict(np.load(path))
            assert json.loads(str(saved['identity'])) == identity
            assert abs(float(saved['weight']) / weight - 1) < 1e-14
        else:
            result = model.real(parameters, angular=4, radial=18, rule=rule)
            saved = dict(event_energy_null=result['event_energy_null'])
            if part == 'expensive':
                scalar, loop_path = owned_loop(parameters)
                weak.vacuum.mp.mp.dps = 60
                vacuum = float(weak.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
                    + weak.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
                jump, product = model.born_data(parameters)
                saved.update(difference=result['total'], virtual=.5 * (vacuum + scalar) * product,
                    state=model.state_correction(parameters)['total'], loop_scalar=scalar, loop_path=str(loop_path))
            else:
                saved['control'] = result['total']
            saved.update(identity=json.dumps(identity, sort_keys=True), weight=weight)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle, **saved)
            temporary.replace(path)
        for key in keys:
            assert saved[key].shape == (98,4) and np.isfinite(saved[key]).all()
            totals[key] -= weight * saved[key]
        maximum_null = max(maximum_null, float(saved['event_energy_null']))
        inputs.append(path)
        if part == 'expensive':
            loop_path = Path(str(saved['loop_path']))
            loop = json.loads(loop_path.read_text())
            assert loop['identity'] == virtual_identity(parameters) and loop['scalar'] == float(saved['loop_scalar'])
            inputs.append(loop_path)
        progress = dict(state='running', part=part, shard=shard, completed_nodes=ordinal+1,
            total_nodes=len(nodes), elapsed_seconds=time.monotonic()-started, pid=os.getpid())
        write_json(folder / 'progress.json', progress)
        if (ordinal+1) % max(1,len(nodes)//4) == 0:
            print(json.dumps(progress), flush=True)
    checks = [dict(name='All96 source modes and four profiles finite: ' + part + str(shard), passed=True),
        dict(name='Exact event photon/gas energy exchange: ' + part + str(shard), value=maximum_null, passed=maximum_null < 1e-10)]
    np.savez(folder / 'source.npz', **totals, mass=spectra.basis.mass, temperature=spectra.basis.temperature, chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, configuration=config, nodes=len(nodes),
        elapsed_seconds=time.monotonic()-started, reflection_folded_scalar=True, physical_electrons=48,
        new_parent_history=False, full_parent_feedback_applied=False), __file__, [*inputs,*spectra.inputs])
    print(json.dumps(dict(part=part, shard=shard, state='complete', nodes=len(nodes), checks=checks)), flush=True)
    return True


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--shard',type=int,choices=[0,1],required=True)
    parser.add_argument('--parts',nargs='+',choices=['expensive','control'],default=['expensive','control'])
    parser.add_argument('--max-seconds',type=float,default=11600.)
    arguments = parser.parse_args()
    deadline = time.monotonic() + arguments.max_seconds
    for part in arguments.parts:
        if not run_part(part,arguments.shard,deadline):
            raise SystemExit(75)
