from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, math, time

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'colder-source-continuation-20261022'
sys.path.insert(0, str(PARENT))
import continue199 as previous
np, linear, mp = previous.np, previous.linear, previous.mp
saved, smooth, history = previous.saved, previous.smooth, previous.history
old, curvature = smooth.old, smooth.previous
read, write, packet, save, digest, check = previous.read, previous.write, previous.packet, previous.save, previous.digest, previous.check
PARENT_SHA = '911f6c16bf2898a896b3a85c69cf5d71bc81a40a8a85b487b24afc1eb1242d6a'
WARM = -.015
COLD = (.875 - .90625) * math.log(10)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, checksum in config['protocol_hashes'].items():
        assert digest(ROOT / name) == checksum, name
    for name, checksum in config['prediction_hashes'].items():
        assert digest(ROOT / name) == checksum, name
    return config


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    seal_path = PARENT / 'results/stage-integrity.json'
    assert digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    inputs = dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT / name): value for name, value in seal['file_hashes'].items()})
    inputs[str(seal_path)] = PARENT_SHA
    for name, checksum in inputs.items():
        assert digest(name) == checksum, name
    frozen = smooth.frozen_candidate()
    ladder, basis, theta0 = old.setup()
    save(ROOT / 'frozen/old-prediction.npz', **{name: frozen[name] for name in ('block', 'tangent', 'curvature')},
         prediction=smooth.candidate(COLD, frozen), offset=COLD)
    for module in list(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name and Path(name).suffix == '.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs, name)
    config = dict(stage=200, started_utc=datetime.now(timezone.utc).isoformat(), parent_sha256=PARENT_SHA,
        target_fraction=.90625, offset=COLD, warm=WARM, theta0=theta0, expansion_span=math.log(10),
        event_order=6, source_prediction_tolerance=.01, identity_tolerance=1e-10,
        independent_bridge_coordinates=[.25, .5, .75],
        protocol_hashes={name: digest(ROOT / name) for name in ('bridge200.py', 'ACCEPTANCE.md', 'DERIVATION.md')},
        prediction_hashes={'frozen/old-prediction.npz': digest(ROOT / 'frozen/old-prediction.npz')},
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')})
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', config)
    write(ROOT / 'progress.json', dict(state='old_prediction_frozen'))
    print(json.dumps(dict(state='old_prediction_frozen', offset=COLD, theta=theta0*math.exp(COLD), inputs=len(inputs))), flush=True)


def relative(actual, expected):
    denominator = np.linalg.norm(expected)
    assert np.isfinite(denominator) and denominator > 0
    return float(np.linalg.norm(actual - expected) / denominator)


def physical(offset, directory, derivatives=False):
    protocol()
    assert not (directory / 'result.npz').exists()
    ladder, basis, theta0 = old.setup()
    theta = theta0 * math.exp(offset)
    began = time.monotonic()
    if derivatives:
        events, weights, scaled = curvature.event_curvature(theta, 6)
        block = np.zeros_like(basis.mass)
        tangent = np.zeros_like(block)
        second = np.zeros_like(block)
        masks = []
        for index, initial in enumerate(basis.values):
            final, conductance = curvature.pair_curvature(basis, theta, events, index)
            inside = (final.value >= basis.minimum) & (final.value <= basis.maximum)
            masks.append(inside)
            values, first, curvature_values = curvature.basis_derivatives(basis, final.value[inside])
            difference = initial[None, :] - values
            derivative = -first * final.first[inside, None]
            derivative_second = -(curvature_values * final.first[inside, None]**2 + first * final.second[inside, None])
            weight, weight_first, weight_second = conductance.value[inside], conductance.first[inside], conductance.second[inside]
            block -= .5 * (difference.T * weight) @ difference
            mixed = (derivative.T * weight) @ difference
            tangent -= .5 * ((difference.T * weight_first) @ difference + mixed + mixed.T)
            mixed_first = (derivative.T * weight_first) @ difference
            mixed_second = (derivative_second.T * weight) @ difference
            second -= (.5 * (difference.T * weight_second) @ difference + mixed_first + mixed_first.T
                       + .5 * (mixed_second + mixed_second.T) + (derivative.T * weight) @ derivative)
            if (index + 1) % 100 == 0:
                write(directory / 'progress.json', dict(state='deriving', nodes=index+1, seconds=time.monotonic()-began))
        save(directory / 'result.npz', actual=block, tangent=tangent, curvature=second, masks=np.array(masks), theta=theta, offset=offset)
        write(directory / 'status.json', dict(seconds=time.monotonic()-began, sha256=digest(directory / 'result.npz'), derivatives='analytic fixed-membership'))
    else:
        events = old.geometry_module.event_geometry(theta, 6)
        block, discarded = old.ladder_module.scalar_physical_block(basis, theta, events)
        masks = packet(old.ROOT / 'results/frozen-tangent.npz')['masks']
        boundary = np.zeros_like(block)
        crossings = 0
        for index, initial in enumerate(basis.values):
            ratio, extra, final, conductance = old.physical_pairs(basis, theta, events, index)
            inside = (final >= basis.minimum) & (final <= basis.maximum)
            changed = inside != masks[index]
            if np.any(changed):
                difference = initial[None, :] - basis.evaluate(final[changed])
                sign = inside[changed].astype(int) - masks[index, changed].astype(int)
                boundary -= .5 * (difference.T * (conductance[changed] * sign)) @ difference
                crossings += int(changed.sum())
        save(directory / 'result.npz', actual=block, boundary=boundary, theta=theta, offset=offset)
        write(directory / 'status.json', dict(seconds=time.monotonic()-began, sha256=digest(directory / 'result.npz'), crossings=crossings, discarded_weight_fraction=discarded))
    print(json.dumps(dict(physical=str(directory.name), derivatives=derivatives, seconds=time.monotonic()-began)), flush=True)


def old_test():
    protocol()
    path = ROOT / 'physical/cold'
    physical(COLD, path)
    frozen, actual = packet(ROOT / 'frozen/old-prediction.npz'), packet(path / 'result.npz')
    rows = []
    for name, block in [('live', actual['actual']), ('fixed_mask', actual['actual']-actual['boundary'])]:
        change = block-frozen['block']
        remainder = change-COLD*frozen['tangent']
        check(rows, name+':small change', relative(frozen['prediction']-frozen['block'], change), .01)
        check(rows, name+':curvature remainder', relative(.5*COLD*COLD*frozen['curvature'], remainder), .01)
    failed = [row for row in rows if not row['passed']]
    write(ROOT / 'results/old-prediction.json', dict(checks=rows, failed_checks=failed))
    write(ROOT / 'progress.json', dict(state='old_test_complete', failed=len(failed)))
    print(json.dumps(dict(checks=rows)), flush=True)


def evaluate(offset, coefficients):
    phase = (offset-WARM)/(COLD-WARM)
    assert -1e-12 <= phase <= 1+1e-12
    controls = coefficients['controls']
    return ((1-phase)**3*controls[0] + 3*phase*(1-phase)**2*controls[1]
            + 3*phase**2*(1-phase)*controls[2] + phase**3*controls[3])


def derive_bridge():
    config = protocol()
    assert read(ROOT / 'results/old-prediction.json')['failed_checks']
    physical(COLD, ROOT / 'physical/cold-derivatives', derivatives=True)
    cold = packet(ROOT / 'physical/cold/result.npz')['actual']
    derived = packet(ROOT / 'physical/cold-derivatives/result.npz')
    frozen = packet(ROOT / 'frozen/old-prediction.npz')
    warm = smooth.candidate(WARM, frozen)
    slope = frozen['tangent'] + WARM*frozen['curvature']
    span = COLD-WARM
    controls = np.array([warm, warm+span*slope/3, cold-span*derived['tangent']/3, cold])
    offsets = np.array([WARM+phase*span for phase in config['independent_bridge_coordinates']])
    predictions = np.array([evaluate(offset, dict(controls=controls)) for offset in offsets])
    rows = []
    check(rows, 'independent analytic accumulator reproduces cold physical matrix', relative(derived['actual'], cold), 1e-10)
    check(rows, 'warm value matches existing candidate', relative(controls[0], warm), 1e-10)
    check(rows, 'warm derivative matches existing candidate', relative(3*(controls[1]-controls[0])/span, slope), 1e-10)
    check(rows, 'cold derivative matches physical analytic slope', relative(3*(controls[3]-controls[2])/span, derived['tangent']), 1e-10)
    failed = [row for row in rows if not row['passed']]
    assert not failed, failed
    save(ROOT / 'frozen/bridge.npz', controls=controls, offsets=offsets, predictions=predictions,
         cold_tangent=derived['tangent'], cold_curvature=derived['curvature'])
    write(ROOT / 'frozen/bridge.json', dict(frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        sha256=digest(ROOT / 'frozen/bridge.npz'), checks=rows, failed_checks=failed, offsets=offsets.tolist(),
        endpoint_is_input=True, independent_targets_loaded=False))
    write(ROOT / 'progress.json', dict(state='bridge_predictions_frozen'))
    print(json.dumps(dict(state='bridge_predictions_frozen', offsets=offsets.tolist())), flush=True)


def bridge_packet():
    protocol()
    record = read(ROOT / 'frozen/bridge.json')
    assert digest(ROOT / 'frozen/bridge.npz') == record['sha256']
    return packet(ROOT / 'frozen/bridge.npz')


def target(index):
    coefficients = bridge_packet()
    offset = float(coefficients['offsets'][index])
    directory = ROOT / f'physical/probe-{index}'
    physical(offset, directory)
    frozen, actual = packet(ROOT / 'frozen/old-prediction.npz'), packet(directory / 'result.npz')
    predicted = coefficients['predictions'][index]
    rows = []
    for name, block in [('live', actual['actual']), ('fixed_mask', actual['actual']-actual['boundary'])]:
        change = block-frozen['block']
        remainder = change-offset*frozen['tangent']
        check(rows, name+':small change', relative(predicted-frozen['block'], change), .01)
        check(rows, name+':curvature remainder', relative(predicted-frozen['block']-offset*frozen['tangent'], remainder), .01)
        check(rows, name+':warm-relative change', relative(predicted-coefficients['controls'][0], block-coefficients['controls'][0]), .01)
    failed = [row for row in rows if not row['passed']]
    write(directory / 'validation.json', dict(checks=rows, failed_checks=failed, offset=offset))
    print(json.dumps(dict(probe=index, checks=rows)), flush=True)


if __name__ == '__main__':
    previous.source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'old-test', 'derive', 'target'])
    parser.add_argument('--index', type=int, choices=range(3))
    args = parser.parse_args()
    if args.phase == 'target':
        target(args.index)
    else:
        {'prepare': prepare, 'old-test': old_test, 'derive': derive_bridge}[args.phase]()
