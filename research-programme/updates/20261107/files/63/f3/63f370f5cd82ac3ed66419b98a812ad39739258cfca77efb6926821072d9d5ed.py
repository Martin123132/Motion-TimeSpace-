from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'exact-dirac-density-20261027'
REFERENCE = BRANCH / 'angular-mixed-source-20261027'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import common239 as previous
from common239 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from common239 import scalar, precise, source, angular, statistics, geometry, projected, integration, Direction, precise_context
from rational239 import RationalDirection
import types
import os
SEAL = '21f5ea024167574a07fbbac7f1b16459da9dbe0a6789cd8a70a8a8f2dadad163'
START = '2026-10-27T05:50:36+00:00'


def modules(inputs):
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
    for path, expected in config['retained_code'].items():
        assert digest(path) == expected, path
    return config


def setup(config):
    return integration.setup(config)


def candidate_integrator():
    namespace = dict(integration.ray_integral.__globals__)
    namespace['Direction'] = RationalDirection
    assert integration.ray_integral.__globals__['Direction'] is Direction
    return types.FunctionType(integration.ray_integral.__code__, namespace, 'qualified_rational_integrator',
        integration.ray_integral.__defaults__, integration.ray_integral.__closure__)


def event_key(row):
    return f'{row["label"]}-e{row["event"]}'


def prepare():
    modest()
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    seal = read(PARENT / 'results/stage-integrity.json')
    assert seal['qualified']
    inputs = dict(seal['directly_consumed_inputs'])
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    parent_files = {name.replace('\\', '/'): value for name, value in seal['file_hashes'].items()}
    for name in ('rational239.py', 'results/completion.json', 'DERIVATION.md'):
        register(inputs, PARENT / name, parent_files[name])
    catalogue_path = register(inputs, BRANCH / 'complete-panel-operator-final-20261026/configuration.json')
    catalogue = read(catalogue_path)
    inherited = read(REFERENCE / 'configuration.json')
    selected = [row for row in catalogue['events'] if row['frequency_index'] == 3 and row['event'] in (0, 1, 2)]
    assert len(selected) == 9
    for row in selected:
        assert row['node']['frequency'] == 14 and row['node']['electron_index'] == 0
        assert row['node']['azimuth_index'] == 0 and row['node']['reflection_multiplicity'] == 1
        for kind in ('source', 'loop'):
            register(inputs, row[kind + '_path'], row[kind + '_sha256'])
        parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
        assert weight == row['weight']
        assert read(row['loop_path'])['identity'] == source.physics.event_owner.inherited.virtual_identity(parameters)
        if row['event'] == 0:
            old = next(event for event in inherited['events'] if event['label'] == row['label'])
            for key in ('node', 'theta', 'source_sha256', 'loop_sha256', 'weight'):
                assert old[key] == row[key], key
    for name in ('state235.py', 'mass235.py', 'results/mass-coefficients.npz', 'results/mass.json'):
        register(inputs, BRANCH / 'matched-mixed-state-20261026' / name)
    for name in ('virtual237.py', 'configuration.json'):
        register(inputs, REFERENCE / name)
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=240, started_at=START, frozen_at=now(), previous_goal_turn='progress',
        parent_seal=SEAL, events=[row for row in selected if row['event'] != 0], all_events=selected,
        reused_event_zero=[row for row in selected if row['event'] == 0], states=inherited['states'], heat=inherited['heat'],
        target_fraction=inherited['target_fraction'], target_theta=inherited['target_theta'],
        spectral_domain=inherited['spectral_domain'], maximum_log_width=inherited['maximum_log_width'],
        angular_orders=[4, 6], radial_order=26, virtual_radial_order=6, digits=60, virtual_digits=80,
        joins=[0, 1], multipoles=[0, 1, 2], canonical_steps=[.001, .0005],
        identity_tolerance=1e-10, refinement_tolerance=.002, same_discretization_replay_tolerance=1e-7,
        deadline_timestamp=datetime.fromisoformat(START).timestamp() + 3.7 * 3600,
        weights='Original incident-frequency, hard-angle and electron weights already included exactly once',
        original_bank_changed=False, original_tolerances_changed=False, tail_closure_added=False,
        retained_code={str(path): digest(path) for path in (Path(integration.__file__), PARENT / 'rational239.py')},
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, new_events=6, reused_events=3, inputs=len(inputs), real_rays=624)), flush=True)


if __name__ == '__main__':
    prepare()
