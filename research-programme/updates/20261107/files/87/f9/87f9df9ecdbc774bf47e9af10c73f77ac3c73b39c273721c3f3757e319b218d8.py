from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'angular-source-gravity-bridge-20261027'
REFERENCE = BRANCH / 'angular-mixed-source-20261027'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import common238 as previous
from common238 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from common238 import scalar, precise, source, angular, statistics, geometry, projected
sys.path.insert(0, str(BRANCH / 'finite-real-mixed-source-20261026'))
import integrate236 as integration
from density236 import Direction
from factors236 import precise_context
SEAL = '10b84daaeefd16fe91d98b42e052be2b3dee4b71682e64b12a83ac7d04655204'
START = '2026-10-27T05:32:25+00:00'


def modules(inputs):
    previous.modules(inputs)
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    return config


def prepare():
    modest()
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    parent_seal = read(PARENT / 'results/stage-integrity.json')
    assert parent_seal['qualified']
    inputs = dict(parent_seal['directly_consumed_inputs'])
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    parent_files = {name.replace('\\', '/'): value for name, value in parent_seal['file_hashes'].items()}
    for name in ('NEXT.md', 'DERIVATION.md', 'RESULTS.md', 'results/completion.json'):
        register(inputs, PARENT / name, parent_files[name])
    reference = read(REFERENCE / 'configuration.json')
    register(inputs, REFERENCE / 'configuration.json')
    register(inputs, BRANCH / 'finite-real-mixed-source-20261026/results/density-pilot.json')
    for module in (integration, sys.modules[Direction.__module__]):
        register(inputs, module.__file__)
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=239, started_at=START, frozen_at=now(), previous_goal_turn='progress',
        parent_seal=SEAL, events=reference['events'], states=reference['states'], heat=reference['heat'],
        reference_configuration=str(REFERENCE / 'configuration.json'),
        point_angular_order=4, point_rays=[0, 11, 23], point_frequencies=[1.2e-6, 1e-4, .01, 1., 3.],
        independent_frequency=1.37123456789, digits=60, control_digits=80,
        identity_tolerance=1e-10, same_discretization_replay_tolerance=1e-7, physical_refinement_tolerance=.002,
        minimum_event_speedup=1., no_numerical_fit=True, original_bank_changed=False, original_tolerances_changed=False,
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, inputs=len(inputs))), flush=True)


if __name__ == '__main__':
    prepare()
