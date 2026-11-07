from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'physical-source-history-tangent-20261027'
DATA = ROOT / 'data'
sys.path.insert(0, str(PARENT))
import history242 as prior
import tail242 as tail
from scipy.interpolate import interp1d
from history242 import np, mp, read, write, save, packet, digest, register, check, modest, now, precise, connection
SEAL = '57f45393b1f2350ac21dc2bdefa3ef4459400a88dc373d0dbc3fe036cc7356c3'
history = connection.evolution.history
continued = connection.evolution.previous


def modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def own(inputs, path, seal):
    path = Path(path)
    expected = seal['directly_consumed_inputs'].get(str(path.resolve()))
    if path.is_relative_to(PARENT):
        expected = seal['file_hashes'][path.relative_to(PARENT).as_posix()]
    return register(inputs, path, expected)


def prepare():
    modest()
    assert DATA.is_dir() and DATA.resolve().drive.upper() == 'C:'
    assert not (ROOT / 'configuration.json').exists()
    seal = read(PARENT / 'results/stage-integrity.json')
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL and seal['qualified']
    inputs = {}
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    for name in ('history242.py', 'tail242.py', 'TAIL-REPAIR-LAW.md', 'NEXT.md', 'configuration.json',
            'results/history.json', 'results/tail-rhs.json', 'results/history-tangents.npz'):
        own(inputs, PARENT / name, seal)
    parent = read(PARENT / 'configuration.json')
    original_target, unused = connection.source.context(parent['target_fraction'])
    cases = []
    with mp.workdps(80):
        for model_index, model in enumerate(('heavy', 'cold')):
            original_data = packet(own(inputs, original_target.inputs[4 * model_index], seal))
            for grid in ('half', 'quarter'):
                directory = history.directory(model, 'candidate', grid)
                reference = read(own(inputs, directory / 'reference.json', seal))
                data = packet(own(inputs, directory / 'reference.npz', seal))
                assert digest(directory / 'reference.npz') == reference['sha256']
                states, old_checks, chain = history.read_history(model, 'candidate', grid)
                assert len(states) == len(data['expansion']) and all(row['passed'] for row in old_checks)
                for path in (directory / 'blocks').glob('*.json'):
                    own(inputs, path, seal)
                endpoint = read(own(inputs, continued.ROOT / f'histories/{model}/{grid}/complete.json', seal))
                assert endpoint['source_chain_sha256'] == chain and not endpoint['failed_checks']
                expected_seed, unused = history.seeds(model, grid)
                parsed_seed = history.parse_state(states[0])
                assert parsed_seed['profile'] == expected_seed['profile'] and parsed_seed['gas'] == expected_seed['gas']
                start, stop, step = float(data['expansion'][0]), float(data['expansion'][-1]), float(data['step'])
                original_profile = mp.matrix([mp.mpf(float(value)) for value in interp1d(
                    original_data['expansion'], original_data['profiles'], axis=0)(start)])
                original_gas = mp.mpf(float(np.interp(start, original_data['expansion'], original_data['temperature_scaled'])))
                cases.append(dict(model=model, grid=grid, start=start, stage189_stop=stop, step=step,
                    stage189_states=len(states), stage189_chain=chain, stage199_stop=endpoint['coordinate'],
                    missing_steps=endpoint['done'], target_coordinate=parent['coordinate'],
                    initial_profile_relative=float(prior.relative(parsed_seed['profile'], original_profile)),
                    initial_gas_difference=float(parsed_seed['gas'] - original_gas)))
    modules(inputs)
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=243, prepared_at=now(), previous_goal_turn='progress',
        parent_seal=SEAL, cases=cases, target_coordinate=parent['coordinate'], target_theta=parent['target_theta'],
        heat=parent['heat'], identity_tolerance=1e-10, history_mesh_tolerance=.01, source_tolerance=.002,
        working_digits=80, audit_digits=100, tail_time_subdivisions=[1, 2, 4],
        source_scope='Retained driven leading soft-tail equation, fixed bank/mesh/exterior rules; both drives evolved together',
        frozen_tail_tangent_substituted=False, photon_gas_bank_changed=False, original_tolerances_changed=False,
        data_location=str(DATA.resolve()), expected_output_bytes_upper=200000000,
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(dict(prepared=True, cases=cases, inputs=len(inputs)), flush=True)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for path, expected in read(ROOT / 'inputs.json').items():
        assert digest(path) == expected, path
    return config


if __name__ == '__main__':
    prepare()
