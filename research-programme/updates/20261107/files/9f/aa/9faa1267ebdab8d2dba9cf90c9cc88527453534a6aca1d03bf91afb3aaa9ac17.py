from __future__ import annotations

import os
for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'bank-knot-gas-curvature-20261020'
PARENT_SHA = 'dbfb36d591f3feb466a90f832de7c5854d0e0e8a95d1224848f28f1f762db77f'
STARTED = '2026-10-20T22:58:21+00:00'
sys.path.insert(0, str(PARENT))
import corner_stage184 as prior
source, saved, np, mp, native, linear = prior.source, prior.saved, prior.np, prior.mp, prior.native, prior.linear
read, write, check = prior.read, prior.write, prior.check
ladder_module = native.infrared_ladder
geometry_module = ladder_module.thermal_wave.prior
MODELS = ['heavy', 'cold']
OFFSETS = [.001, -.001, .0005, -.0005]


def all_offsets():
    path = ROOT / 'results/wider-predictions.json'
    return OFFSETS + read(path)['offsets'] if path.exists() else OFFSETS


def freeze_wider():
    assert read(ROOT / 'progress.json')['state'] == 'gas_projection_complete'
    assert not (ROOT / 'results/wider-predictions.json').exists()
    offsets = [.005, -.005, .01, -.01]
    with np.load(ROOT / 'results/frozen-tangent.npz') as packet:
        predictions = np.array([packet['block'] + offset * packet['derivative'] for offset in offsets])
    np.savez_compressed(ROOT / 'results/wider-predictions.npz', offsets=np.array(offsets), predictions=predictions)
    write(ROOT / 'results/initial-near-tests.json', dict(matrix=read(ROOT / 'results/matrix-analysis.json'),
        gas=read(ROOT / 'results/gas-projection.json')))
    write(ROOT / 'results/wider-predictions.json', dict(offsets=offsets,
        frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        original_tangent_sha256=saved.digest(ROOT / 'results/frozen-tangent.npz'),
        prediction_sha256=saved.digest(ROOT / 'results/wider-predictions.npz'),
        rationale='Prospective extension to the unchanged original curvature probes after successful near tests; same tangent, no retuning',
        source_prediction_tolerance=.01, identity_tolerance=1e-10))
    write(ROOT / 'progress.json', dict(state='predictions_frozen'))
    print(json.dumps(dict(frozen_additional_offsets=offsets, tangent_unchanged=True)), flush=True)


def authenticate():
    seal_path = PARENT / 'results/stage-integrity.json'
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal['consumed_and_immediate_rehashed'])
    paths.update({str(PARENT / name): checksum for name, checksum in seal['file_hashes'].items()})
    paths[str(seal_path)] = PARENT_SHA
    bank_status = native.BACKGROUND / 'banks/infrared96-q700/status.json'
    paths.update(read(bank_status)['input_hashes'])
    for module in [ladder_module, geometry_module, geometry_module.prior]:
        path = Path(module.__file__)
        checksum = saved.digest(path)
        if str(path) in paths:
            assert paths[str(path)] == checksum
        paths[str(path)] = checksum
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def setup():
    ladder = ladder_module.InfraredLadder(native.BACKGROUND / 'banks/infrared96-q700')
    return ladder, ladder.basis, float(ladder.temperatures[1])


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    paths = authenticate()
    ladder, basis, theta = setup()
    config = dict(stage=185, started_utc=STARTED, parent_sha256=PARENT_SHA, theta=theta,
        offsets=OFFSETS, event_order=6, basis_spec=ladder.specification,
        source_prediction_tolerance=.01, identity_tolerance=1e-10,
        prediction_scope='Fixed dimensionless incoming frequency, ordinary scalar thermal collision operator; cached baseline/MTS gas channels',
        prior_bookmark_normalized_sha256={str(path): hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
            for path in [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']})
    write(ROOT / 'configuration.json', config)
    write(ROOT / 'authenticated-inputs.json', paths)
    (ROOT / 'results').mkdir(exist_ok=True)
    np.savez_compressed(ROOT / 'quadrature.npz', nodes=basis.nodes, measure=basis.measure, values=basis.values, mass=basis.mass,
        temperature=basis.temperature, chemical=basis.chemical, energy=basis.energy)
    write(ROOT / 'progress.json', dict(state='prepared'))
    print(json.dumps(dict(authenticated_paths=len(paths), theta=theta)), flush=True)


def event_tangent(theta, order):
    radial, radial_base = geometry_module.special.roots_genlaguerre(order, .5)
    scaled = theta * radial
    gamma = 1 + scaled
    speed = np.sqrt(scaled * (2 + scaled)) / gamma
    speed_t = speed / ((2 + scaled) * gamma)
    radial_weights = radial_base * gamma * np.sqrt(2 + scaled)
    radial_weights /= radial_weights.sum()
    logarithmic = scaled / gamma + scaled / (2 * (2 + scaled))
    radial_t = radial_weights * (logarithmic - radial_weights @ logarithmic)
    electron, electron_weights = np.polynomial.legendre.leggauss(order)
    scattering, scattering_weights = np.polynomial.legendre.leggauss(order)
    azimuth = 2 * np.pi * (np.arange(2 * order) + .5) / (2 * order)
    cosine = np.repeat(scattering, len(azimuth))
    transverse_cosine = np.repeat(np.sqrt(1 - scattering**2), len(azimuth)) * np.tile(np.cos(azimuth), order)
    angular_weights = np.repeat(scattering_weights / (2 * len(azimuth)), len(azimuth))
    result = {key: [] for key in ['incident', 'outgoing', 'cosine', 'weight', 'incident_t', 'outgoing_t', 'weight_t']}
    for index in range(order):
        beta, beta_t = speed[index], speed_t[index]
        for mu, angular_weight in zip(electron, electron_weights / 2):
            denominator = 1 - beta * mu
            denominator_t = -beta_t * mu
            incident = gamma[index] * denominator
            incident_t = scaled[index] * denominator + gamma[index] * denominator_t
            parallel = (beta * mu - beta**2) / denominator
            parallel_t = (beta_t * (mu - 2 * beta) - parallel * denominator_t) / denominator
            transverse = beta * np.sqrt(1 - mu**2) / incident
            transverse_t = beta_t * np.sqrt(1 - mu**2) / incident - transverse * incident_t / incident
            bracket = 1 + cosine * parallel + transverse_cosine * transverse
            outgoing = gamma[index] * bracket
            outgoing_t = scaled[index] * bracket + gamma[index] * (cosine * parallel_t + transverse_cosine * transverse_t)
            weights = radial_weights[index] * angular_weight * denominator * angular_weights
            weights_t = angular_weight * angular_weights * (radial_t[index] * denominator + radial_weights[index] * denominator_t)
            result['incident'].append(np.full_like(cosine, incident))
            result['incident_t'].append(np.full_like(cosine, incident_t))
            result['outgoing'].append(outgoing)
            result['outgoing_t'].append(outgoing_t)
            result['cosine'].append(cosine)
            result['weight'].append(weights)
            result['weight_t'].append(weights_t)
    return {key: np.concatenate(value) for key, value in result.items()}


def physical_pairs(basis, theta, events, index):
    frequency = basis.nodes[index]
    ratio = 1 / (1 + theta * frequency * events['incident'] * (1 - events['cosine']))
    extra = (1 - ratio)**2 / ratio
    final = frequency * events['incident'] * ratio * events['outgoing']
    bose = (1 + 1 / np.expm1(final)) / (1 + 1 / np.expm1(frequency))
    conductance = basis.measure[index] / 2 * events['weight'] * 1.5 * ratio**2 * bose * (1 + events['cosine']**2 + extra)
    return ratio, extra, final, conductance


def build_tangent(basis, theta, events):
    block, derivative = np.zeros_like(basis.mass), np.zeros_like(basis.mass)
    masks = []
    discarded, total = 0., 0.
    began = time.monotonic()
    for index, initial in enumerate(basis.values):
        ratio, extra, final, conductance = physical_pairs(basis, theta, events, index)
        ratio_t = -ratio**2 * theta * basis.nodes[index] * (events['incident'] + events['incident_t']) * (1 - events['cosine'])
        final_t = final * (events['incident_t'] / events['incident'] + ratio_t / ratio + events['outgoing_t'] / events['outgoing'])
        extra_t = ratio_t * (1 - 1 / ratio**2)
        conductance_t = conductance * (events['weight_t'] / events['weight'] + 2 * ratio_t / ratio
            - final_t / np.expm1(final) + extra_t / (1 + events['cosine']**2 + extra))
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        masks.append(inside)
        discarded += float(conductance[~inside].sum())
        total += float(conductance.sum())
        difference = initial[None, :] - basis.evaluate(final[inside])
        tangent = -basis.derivative(final[inside]) * final_t[inside, None]
        block -= .5 * (difference.T * conductance[inside]) @ difference
        mixed = (tangent.T * conductance[inside]) @ difference
        derivative -= .5 * ((difference.T * conductance_t[inside]) @ difference + mixed + mixed.T)
        if (index + 1) % 100 == 0:
            write(ROOT / 'progress.json', dict(state='anchor_tangent_running', nodes_done=index + 1, elapsed=time.monotonic() - began))
    return block, derivative, np.array(masks), discarded / total


def freeze():
    assert read(ROOT / 'progress.json')['state'] == 'prepared'
    ladder, basis, theta = setup()
    checks = []
    events = event_tangent(theta, 6)
    original = geometry_module.event_geometry(theta, 6)
    for key in ['incident', 'outgoing', 'cosine', 'weight']:
        check(checks, 'analytic geometry reproduces original ' + key,
            np.linalg.norm(events[key] - original[key]) / np.linalg.norm(original[key]))
    for step in [1e-4, 5e-5]:
        plus, minus = [geometry_module.event_geometry(theta * np.exp(sign * step), 6) for sign in [1, -1]]
        for key in ['incident', 'outgoing', 'weight']:
            numerical = (plus[key] - minus[key]) / (2 * step)
            check(checks, f'event tangent {key} at {step}', np.linalg.norm(numerical - events[key + '_t']) / np.linalg.norm(events[key + '_t']), .01, 'derivative')
    block, derivative, masks, discarded = build_tangent(basis, theta, events)
    check(checks, 'analytic construction reproduces original anchor bank', np.linalg.norm(block - ladder.blocks[1]) / np.linalg.norm(ladder.blocks[1]))
    check(checks, 'tangent matrix symmetry', np.linalg.norm(derivative - derivative.T) / np.linalg.norm(derivative))
    check(checks, 'tangent number null', np.linalg.norm(derivative @ basis.chemical) / (np.linalg.norm(derivative) * np.linalg.norm(basis.chemical)))
    check(checks, 'anchor number null', np.linalg.norm(block @ basis.chemical) / (np.linalg.norm(block) * np.linalg.norm(basis.chemical)))
    assert np.isfinite(derivative).all()
    assert all(row['passed'] for row in checks), checks
    assert not (ROOT / 'results/frozen-tangent.npz').exists()
    np.savez_compressed(ROOT / 'results/frozen-tangent.npz', block=block, derivative=derivative, masks=masks, theta=theta,
        offsets=np.array(OFFSETS), predictions=np.array([block + offset * derivative for offset in OFFSETS]))
    np.savez_compressed(ROOT / 'results/anchor-events.npz', **events)
    write(ROOT / 'results/frozen-tangent.json', dict(checks=checks, discarded_weight_fraction=discarded,
        frozen_at_utc=datetime.now(timezone.utc).isoformat(), offsets=OFFSETS,
        tangent_sha256=saved.digest(ROOT / 'results/frozen-tangent.npz'), geometry_events=len(events['weight']),
        derivative_scope='Exact analytic tangent of the retained discrete fixed-membership integral',
        no_fitted_coefficients=True, future_targets_not_evaluated=True))
    write(ROOT / 'progress.json', dict(state='predictions_frozen'))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], discarded=discarded)), flush=True)


def evaluate_target(index):
    assert read(ROOT / 'progress.json')['state'] in ['predictions_frozen', 'targets_running']
    folder = ROOT / 'targets' / f'target-{index}'
    assert not folder.exists()
    ladder, basis, theta0 = setup()
    offset = all_offsets()[index]
    theta = theta0 * np.exp(offset)
    frozen_hash = saved.digest(ROOT / 'results/frozen-tangent.npz')
    assert frozen_hash == read(ROOT / 'results/frozen-tangent.json')['tangent_sha256']
    with np.load(ROOT / 'results/frozen-tangent.npz') as packet:
        anchor_masks = packet['masks'].copy()
    events = geometry_module.event_geometry(theta, 6)
    began = time.monotonic()
    block, discarded = ladder_module.scalar_physical_block(basis, theta, events)
    boundary = np.zeros_like(block)
    crossing_count, crossing_weight = 0, 0.
    for node, initial in enumerate(basis.values):
        ratio, extra, final, conductance = physical_pairs(basis, theta, events, node)
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        changed = inside != anchor_masks[node]
        if not np.any(changed):
            continue
        difference = initial[None, :] - basis.evaluate(final[changed])
        sign = inside[changed].astype(int) - anchor_masks[node, changed].astype(int)
        boundary -= .5 * (difference.T * (conductance[changed] * sign)) @ difference
        crossing_count += int(changed.sum())
        crossing_weight += float(conductance[changed].sum())
    folder.mkdir(parents=True)
    np.savez_compressed(folder / 'matrices.npz', block=block, boundary=boundary, fixed_mask=block - boundary, theta=theta, offset=offset)
    write(folder / 'status.json', dict(state='complete', offset=offset, theta=theta, frozen_tangent_sha256=frozen_hash,
        crossings=crossing_count, crossing_conductance=crossing_weight, discarded_weight_fraction=discarded,
        elapsed_seconds=time.monotonic() - began, matrix_sha256=saved.digest(folder / 'matrices.npz')))
    write(ROOT / 'progress.json', dict(state='targets_running', last_completed=index))
    print(json.dumps(read(folder / 'status.json')), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'freeze', 'wider', 'target'])
    parser.add_argument('--index', type=int, choices=range(8))
    arguments = parser.parse_args()
    if arguments.phase == 'target':
        evaluate_target(arguments.index)
    else:
        dict(prepare=prepare, freeze=freeze, wider=freeze_wider)[arguments.phase]()
