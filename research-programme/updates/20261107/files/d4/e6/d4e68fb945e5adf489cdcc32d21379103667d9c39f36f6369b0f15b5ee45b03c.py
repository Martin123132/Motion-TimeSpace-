from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'hard-angle-source-expansion-20261027'
PORTS = BRANCH / 'angular-source-gravity-bridge-20261027'
REFERENCE = BRANCH / 'angular-mixed-source-20261027'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PORTS))
import common238 as retained
import coupling238 as coupling
import repair238 as repair
import frame238 as frame_owner
from common238 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime, scalar, precise
SEAL = '9979c496be0da67c72ab95a8b760d486d7c078a92cb45ef1f406e6d4a5df1cf5'
PORT_SEAL = '10b84daaeefd16fe91d98b42e052be2b3dee4b71682e64b12a83ac7d04655204'
START = '2026-10-27T09:04:20+00:00'
COMPONENTS = ['leading_control', 'real_correction', 'virtual', 'state', 'MTS_correction', 'combined']


def modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def sealed_input(inputs, owner, seal, name):
    hashes = {key.replace('\\', '/'): value for key, value in seal['file_hashes'].items()}
    return register(inputs, owner / name, hashes[name])


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for path, expected in read(ROOT / 'inputs.json').items():
        assert digest(path) == expected, path
    return config


def prepare():
    modest()
    assert not (ROOT / 'configuration.json').exists()
    inputs = {}
    parent_seal = read(register(inputs, PARENT / 'results/stage-integrity.json', SEAL))
    port_seal = read(register(inputs, PORTS / 'results/stage-integrity.json', PORT_SEAL))
    assert parent_seal['qualified'] and port_seal['qualified']
    parent = read(sealed_input(inputs, PARENT, parent_seal, 'configuration.json'))
    ports = read(sealed_input(inputs, PORTS, port_seal, 'configuration.json'))
    for key in ('heat', 'states', 'target_fraction', 'target_theta'):
        assert parent[key] == ports[key], key
    for name in ('results/completion.json', 'NEXT.md', 'DERIVATION.md'):
        sealed_input(inputs, PARENT, parent_seal, name)
    for name in ('coupling238.py', 'repair238.py', 'frame238.py', 'frozen/basis.npz',
            'results/repaired-ports.json', 'results/frame.json', 'DERIVATION.md', 'PRECISION-REPAIR.md'):
        sealed_input(inputs, PORTS, port_seal, name)
    for anchor in ('warm', 'middle', 'cold'):
        for name in (f'results/{anchor}-three-hard-angle-sum.npz', f'results/{anchor}-assessment.json',
                f'results/{anchor}-e1-components.npz', f'results/{anchor}-e2-components.npz'):
            sealed_input(inputs, PARENT, parent_seal, name)
        for name in (f'results/{anchor}-contexts.json', f'results/{anchor}-ports.npz', f'results/{anchor}-protected-ports.npz'):
            sealed_input(inputs, PORTS, port_seal, name)
        source_report = read(register(inputs, REFERENCE / 'results' / f'{anchor}-assessment.json'))
        register(inputs, REFERENCE / 'results' / f'{anchor}-assessment.npz', source_report['output_sha256'])
    for model in ('heavy', 'cold'):
        retained.gravity.prior.System(model, 6400, inputs)
        register(inputs, BRANCH / 'two-way-thermal-gravity-20261026' / 'runs' / f'{model}-6400/history.npz')
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=241, started_at=START, frozen_at=now(), previous_goal_turn='progress',
        parent_seal=SEAL, port_seal=PORT_SEAL, states=parent['states'], heat=parent['heat'],
        target_theta=parent['target_theta'], target_fraction=parent['target_fraction'],
        events=parent['reused_event_zero'], joins=parent['joins'], multipoles=parent['multipoles'],
        angular_orders=[4, 6], components=COMPONENTS, identity_tolerance=parent['identity_tolerance'],
        response_tolerance=parent['refinement_tolerance'], negative_control_minimum=1e-7,
        wave_number=ports['wave_number'], units=ports['units'], baseline_scope=ports['baseline_scope'],
        source_scope='Stage240 partial quadrature at x14, first electron node and three saved hard angles',
        response_scope='Exact local source/stress and first nonzero metric Taylor coefficient; finite-time evolution requires its actual temporal source owner',
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        tail_closure_added=False, bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, consumed_inputs=len(inputs))), flush=True)


if __name__ == '__main__':
    prepare()
