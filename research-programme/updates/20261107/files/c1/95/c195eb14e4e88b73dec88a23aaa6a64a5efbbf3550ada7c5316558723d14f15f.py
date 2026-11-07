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
PARENT = BRANCH / 'local-half-step-gas-curvature-20261020'
PARENT_SHA = '121dc212392f9a51b6c949a2fd24f903d2e4379da1a8ef09ea55c73fb24cf4ef'
STARTED = '2026-10-20T22:17:56+00:00'
sys.path.insert(0, str(PARENT))
import restart_stage182 as prior

source, saved, np, mp, native, linear = prior.source, prior.saved, prior.np, prior.mp, prior.native, prior.linear
read, write, check = prior.read, prior.write, prior.check
MODELS = ['heavy', 'cold']
BRANCHES = ['native', 'half', 'half_thinned', 'half_early', 'quarter', 'quarter_halfgrid', 'quarter_nativegrid', 'quarter_early']
QUANTITIES = ['coarse_curvature', 'fine_curvature', 'width_discrepancy']


def authenticate():
    seal_path = PARENT / 'results/stage-integrity.json'
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal['consumed_and_immediate_rehashed'])
    paths.update({str(PARENT / name): checksum for name, checksum in seal['file_hashes'].items()})
    paths[str(seal_path)] = PARENT_SHA
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    paths = authenticate()
    parent = read(PARENT / 'configuration.json')
    assert parent['source_prediction_tolerance'] == .01 and parent['identity_tolerance'] == 1e-10
    config = dict(stage=183, started_utc=STARTED, parent_seal_sha256=PARENT_SHA,
        source_prediction_tolerance=.01, identity_tolerance=1e-10,
        primary_start=parent['primary_start'], early_start=parent['early_start'], end_index=parent['end_index'],
        step_divisor=4, branches=['quarter', 'quarter_early'], history_tags=parent['history_tags'],
        offsets=parent['offsets'], expansion_span=parent['expansion_span'], anchor_fraction=parent['anchor_fraction'],
        selected=parent['selected'], source_operator_tag=parent['source_operator_tag'],
        source_scope='fixed-anchor isolated gas response; reuse saved summed and event kernels; no source integration',
        prior_bookmark_normalized_sha256={str(path): hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
            for path in [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']})
    assert len(config['selected']) == 36
    write(ROOT / 'configuration.json', config)
    write(ROOT / 'authenticated-inputs.json', paths)
    write(ROOT / 'progress.json', dict(state='prepared'))
    rows = []
    with mp.workdps(80):
        for ratio in [mp.mpf(1), mp.mpf('.5'), mp.mpf('.25')]:
            step = mp.mpf('.0001')
            alpha = (1 + 2 * ratio) / ((1 + ratio) * step)
            beta = (1 + ratio) / step
            gamma = ratio**2 / ((1 + ratio) * step)
            for degree in range(3):
                value = alpha * mp.mpf(0)**degree - beta * (-step)**degree + gamma * (-step - step / ratio)**degree
                check(rows, f'variable BDF2 ratio={ratio} degree={degree}', value - (1 if degree == 1 else 0))
    assert all(row['passed'] for row in rows)
    write(ROOT / 'results/rule-checks.json', dict(checks=rows))
    print(json.dumps(dict(prepared=True, authenticated_paths=len(paths))), flush=True)


def evolve():
    began = time.monotonic()
    config = read(ROOT / 'configuration.json')
    paths = read(ROOT / 'authenticated-inputs.json')
    ladder = native.infrared_ladder.InfraredLadder(native.BACKGROUND / 'banks/infrared96-q700')
    basis = ladder.basis
    consumed = set(ladder.inputs)
    for model in MODELS:
        with np.load(prior.PARENT / 'results' / model / 'state.npz') as packet:
            original = {name: packet[name].copy() for name in packet.files}
        background = native.thermal_wave.thermal.ThermalBackground(model)
        emission = native.NonlocalEmission(basis, background, 'nonlocal-leading', native.ROOT / 'banks/s960-i256')
        consumed.update(emission.inputs)
        consumed.update([background.parent.source, background.native_constants])
        assert np.array_equal(basis.energy, original['energy_row'])
        assert np.array_equal(basis.temperature, original['temperature_template'])
        step = float(original['step']) / 4
        heat = float(original['heat'])
        assert heat == background.chi
        for branch in config['branches']:
            destination = ROOT / 'histories' / model / branch
            if (destination / 'status.json').exists():
                status = read(destination / 'status.json')
                assert status['state'] == 'complete'
                assert saved.digest(destination / 'history.npz') == status['history_sha256']
                print(json.dumps(dict(reused_completed_history=str(destination))), flush=True)
                continue
            if time.monotonic() - began > 3 * 3600:
                write(ROOT / 'progress.json', dict(state='safe_restart', next_model=model, next_branch=branch))
                return
            destination.mkdir(parents=True, exist_ok=True)
            start = config['early_start'] if branch == 'quarter_early' else config['primary_start']
            profile, older_profile = original['profiles'][start].copy(), original['profiles'][start - 1].copy()
            gas, older_gas = float(original['temperature_scaled'][start]), float(original['temperature_scaled'][start - 1])
            work, older_work = float(original['expansion_work'][start]), float(original['expansion_work'][start - 1])
            series = [[float(original['expansion'][start]), float(basis.energy @ profile), gas, work]]
            profiles, diagnostics = [profile.copy()], []
            for ordinal, tick in enumerate(range(start * 4 + 1, config['end_index'] * 4 + 1), 1):
                coordinate = tick * step
                local = background.at(coordinate)
                rate = local['coefficient'] / local['thermal_parameter']
                stiffness = ladder.at(local['thermal_parameter'], 0)[:basis.count, :basis.count] - emission.at(local['thermal_parameter'], 'dcbr')
                if ordinal == 1:
                    ratio = .25
                    alpha = (1 + 2 * ratio) / ((1 + ratio) * step)
                    vector = ((1 + ratio) * profile - ratio**2 / (1 + ratio) * older_profile) / step
                    scalar = ((1 + ratio) * gas - ratio**2 / (1 + ratio) * older_gas) / step
                    work_history = ((1 + ratio) * work - ratio**2 / (1 + ratio) * older_work) / step
                else:
                    alpha = 1.5 / step
                    vector = (2 * profile - .5 * older_profile) / step
                    scalar = (2 * gas - .5 * older_gas) / step
                    work_history = (2 * work - .5 * older_work) / step
                thermal_source = -rate * stiffness @ basis.temperature
                solution = linear.solve(alpha * basis.mass - rate * stiffness,
                    np.column_stack([basis.mass @ vector, thermal_source]), assume_a='pos')
                free, response = solution[:, 0], solution[:, 1]
                new_gas = (heat * scalar - 1 - basis.energy @ (alpha * free - vector)) / (heat * (alpha + 1) + alpha * (basis.energy @ response))
                new_profile = free + response * new_gas
                new_work = (work_history + 1 + heat * new_gas) / alpha
                rhs = rate * stiffness @ (new_profile - basis.temperature * new_gas)
                kinetic = alpha * basis.mass @ new_profile - basis.mass @ vector - rhs
                diagnostics.append(dict(tick=tick, kinetic_relative=float(np.linalg.norm(kinetic) / np.linalg.norm(rhs)),
                    gas_energy_residual=float(basis.energy @ (alpha * new_profile - vector) + heat * ((alpha + 1) * new_gas - scalar) + 1),
                    work_residual=float(alpha * new_work - work_history - 1 - heat * new_gas)))
                older_profile, profile = profile, new_profile
                older_gas, gas = gas, float(new_gas)
                older_work, work = work, float(new_work)
                series.append([coordinate, float(basis.energy @ profile), gas, work])
                profiles.append(profile.copy())
            series, profiles = np.asarray(series), np.asarray(profiles)
            rows = []
            check(rows, 'Integrated energy balance', np.max(abs(series[:, 1] + heat * series[:, 2] + series[:, 3])))
            for field in ['kinetic_relative', 'gas_energy_residual', 'work_residual']:
                check(rows, field, max(abs(row[field]) for row in diagnostics))
            history_path = destination / 'history.npz'
            np.savez_compressed(history_path, expansion=series[:, 0], energy_scaled=series[:, 1], temperature_scaled=series[:, 2],
                expansion_work=series[:, 3], profiles=profiles, heat=heat, step=step, start_index=start, end_index=config['end_index'],
                initial_profile=original['profiles'][start], initial_previous_profile=original['profiles'][start - 1],
                initial_gas=original['temperature_scaled'][start], initial_previous_gas=original['temperature_scaled'][start - 1],
                coordinates=original['coordinates'])
            write(destination / 'status.json', dict(state='complete', checks=rows, all_checks_passed=all(row['passed'] for row in rows),
                diagnostics=diagnostics, updates=len(diagnostics), start_index=start, step=step, startup_ratio=.25,
                history_sha256=saved.digest(history_path)))
            print(json.dumps(dict(model=model, branch=branch, updates=len(diagnostics), checks_pass=all(row['passed'] for row in rows))), flush=True)
            write(ROOT / 'progress.json', dict(state='histories', model=model, branch=branch))
    expected_bank = read(PARENT / 'bank-inputs.json')
    actual_bank = {str(path): saved.digest(path) for path in sorted(consumed)}
    assert actual_bank == expected_bank
    assert all(paths[path] == checksum for path, checksum in actual_bank.items())
    write(ROOT / 'bank-inputs.json', actual_bank)
    write(ROOT / 'progress.json', dict(state='histories_complete', elapsed_seconds=time.monotonic() - began))


def assess():
    assert read(ROOT / 'progress.json')['state'] == 'histories_complete'
    config = read(ROOT / 'configuration.json')
    checks = list(read(ROOT / 'results/rule-checks.json')['checks'])
    outcomes, all_curves, all_samples = [], [], []
    with np.load(PARENT / 'results/history-curvature.npz') as packet:
        old_samples, old_curves = packet['samples'].copy(), packet['curves'].copy()
        assert list(packet['branches']) == BRANCHES[:4]
    for model_index, model in enumerate(MODELS):
        samples = {label: old_samples[model_index, index] for index, label in enumerate(BRANCHES[:4])}
        for branch in config['branches']:
            folder = ROOT / 'histories' / model / branch
            checks.extend([dict(row, name=model + '/' + branch + ': ' + row['name']) for row in read(folder / 'status.json')['checks']])
            with np.load(folder / 'history.npz') as packet:
                coordinate, gas, targets = packet['expansion'], packet['temperature_scaled'], packet['coordinates']
                assert np.all(np.diff(coordinate) > 0) and coordinate[0] <= min(targets) <= max(targets) <= coordinate[-1]
                check(checks, model + '/' + branch + ': uniform grid', np.max(abs(np.diff(coordinate) / float(packet['step']) - 1)))
                samples[branch] = np.interp(targets, coordinate, gas)
                if branch == 'quarter':
                    samples['quarter_halfgrid'] = np.interp(targets, coordinate[::2], gas[::2])
                    samples['quarter_nativegrid'] = np.interp(targets, coordinate[::4], gas[::4])
                    for name, stride in [('half', 2), ('native', 4)]:
                        with np.load(PARENT / 'histories' / model / name / 'history.npz') as ancestor:
                            assert np.array_equal(coordinate[::stride], ancestor['expansion'])
                            for field in ['initial_profile', 'initial_previous_profile', 'initial_gas', 'initial_previous_gas', 'coordinates']:
                                assert np.array_equal(packet[field], ancestor[field]), field
                            assert float(packet['step']) * stride == float(ancestor['step'])
                    check(checks, model + ': same restart seeds and aligned half/native grids', 0)
        curves = {label: prior.curvature(values) for label, values in samples.items()}
        assert np.array_equal(np.array([curves[label] for label in BRANCHES[:4]]), old_curves[model_index])
        comparison = []
        for index, quantity in enumerate(QUANTITIES):
            values = {label: float(curves[label][index]) for label in BRANCHES}
            previous_change = values['half'] - values['native']
            change = values['quarter'] - values['half']
            evolution = values['quarter_halfgrid'] - values['half']
            sampling = values['quarter'] - values['quarter_halfgrid']
            relative = abs(change / values['quarter'])
            startup = abs((values['quarter_early'] - values['quarter']) / values['quarter_early'])
            check(checks, model + ': half/quarter ' + quantity, relative, .01, 'step_comparison')
            check(checks, model + ': early/primary quarter ' + quantity, startup, .01, 'startup')
            check(checks, model + ': split closure ' + quantity, abs(change - evolution - sampling) / max(abs(values['quarter']), 1e-300))
            comparison.append(dict(quantity=quantity, **values, relative_change=relative, startup_relative=startup,
                previous_change=previous_change, change=change, absolute_increment_ratio=abs(change / previous_change) if previous_change else None,
                evolution_change_on_half_nodes=evolution, interpolation_change=sampling,
                quarter_vs_native_common_nodes=values['quarter_nativegrid'] - values['native']))
        outcome = dict(model=model, comparison=comparison,
            width_relative={label: float(abs(curves[label][2] / curves[label][1])) for label in BRANCHES})
        outcomes.append(outcome)
        all_curves.append([curves[label] for label in BRANCHES])
        all_samples.append([samples[label] for label in BRANCHES])
        print(json.dumps(outcome), flush=True)
    np.savez_compressed(ROOT / 'results/history-curvature.npz', models=np.array(MODELS), branches=np.array(BRANCHES),
        quantities=np.array(QUANTITIES), curves=np.array(all_curves), samples=np.array(all_samples))
    write(ROOT / 'results/history-comparison.json', outcomes)
    write(ROOT / 'results/history-checks.json', dict(checks=checks))
    write(ROOT / 'progress.json', dict(state='history_assessment_complete'))


def response():
    assert read(ROOT / 'progress.json')['state'] == 'history_assessment_complete'
    config = read(ROOT / 'configuration.json')
    paths = read(ROOT / 'authenticated-inputs.json')
    kernel_path = PARENT / 'results/gas-response.npz'
    assert saved.digest(kernel_path) == paths[str(kernel_path)]
    with np.load(kernel_path) as packet:
        kernels = packet['kernels'].copy()
        components = list(packet['components'])
        original_responses = packet['responses'].copy()
    with np.load(source.ROOT / 'results/preparation/basis.npz') as packet:
        mass = packet['mass'].copy()
    factor = linear.cholesky(mass, lower=True)

    def norm(values):
        reshaped = np.moveaxis(values[..., 1:97, :], -2, 0).reshape(96, -1)
        return np.linalg.norm(linear.solve_triangular(factor, reshaped, lower=True), axis=0).reshape(values.shape[:-2] + (values.shape[-1],))

    checks = []
    event_pairs = []
    consumed = {str(kernel_path): saved.digest(kernel_path)}
    for node in config['selected']:
        path = PARENT / 'gas-events' / saved.angle_label(node['cosine']) / f"electron-{node['electron_index']:02d}.npz"
        assert saved.digest(path) == paths[str(path)]
        with np.load(path) as packet:
            assert json.loads(str(packet['node'])) == node
            event_pairs.append((packet['high'][1].copy(), packet['low'][1].copy()))
        consumed[str(path)] = saved.digest(path)
    reconstructed = np.empty_like(kernels)
    with mp.workdps(80):
        for index in np.ndindex(kernels.shape):
            reconstructed[index] = float(mp.fsum(mp.mpf(float(high[index])) + mp.mpf(float(low[index])) for high, low in event_pairs))
    assert np.array_equal(reconstructed, kernels)
    check(checks, '36 saved gas event kernels reproduce summed kernel bitwise', 0)
    for component, name in enumerate(components):
        scale = np.maximum(np.maximum(abs(kernels[component, 0]), abs(kernels[component, -1])), 1e-300)
        check(checks, name + ': cached gas kernel energy exchange', np.max(abs(kernels[component, 0] + kernels[component, -1]) / scale))
    check(checks, 'cached matched kernel closure', np.max(norm(kernels[4] - kernels[1] - kernels[2] - kernels[3]) / np.maximum(norm(kernels[4]), 1e-300)))
    check(checks, 'cached total kernel closure', np.max(norm(kernels[5] - kernels[0] - kernels[4]) / np.maximum(norm(kernels[5]), 1e-300)))
    with np.load(ROOT / 'results/history-curvature.npz') as packet:
        curves = packet['curves'].copy()
    responses = np.empty((len(BRANCHES), 3, 6, 98, 4))
    for branch_index, quantity_index, component, column in np.ndindex(len(BRANCHES), 3, 6, 4):
        responses[branch_index, quantity_index, component, :, column] = kernels[component, :, column] * curves[column // 2, branch_index, quantity_index]
    assert np.array_equal(responses[:4], original_responses)
    check(checks, 'all previous baseline/MTS response arrays reproduced bitwise', 0)
    response_rows = []
    for component in [0, 4, 5]:
        for quantity_index, quantity in enumerate(QUANTITIES):
            delta = responses[4, quantity_index, component] - responses[1, quantity_index, component]
            relative = norm(delta) / norm(responses[4, quantity_index, component])
            for column in range(4):
                expected = abs((curves[column // 2, 4, quantity_index] - curves[column // 2, 1, quantity_index]) / curves[column // 2, 4, quantity_index])
                check(checks, f'{components[component]}:{column}:{quantity}: source/gas fractional law', abs(relative[column] - expected) / max(expected, 1e-300))
                check(checks, f'{components[component]}:{column}:{quantity}: half/quarter', relative[column], .01, 'step_comparison')
                response_rows.append(dict(component=components[component], column=column, quantity=quantity,
                    half_norm=float(norm(responses[1, quantity_index, component])[column]),
                    quarter_norm=float(norm(responses[4, quantity_index, component])[column]),
                    relative_change=float(relative[column]), tolerance=.01, passed=bool(relative[column] <= .01)))
    np.savez_compressed(ROOT / 'results/gas-response.npz', kernels=kernels, responses=responses,
        branches=np.array(BRANCHES), components=np.array(components))
    write(ROOT / 'results/gas-response-comparison.json', response_rows)
    write(ROOT / 'results/gas-response-checks.json', dict(checks=checks,
        reused_unit_gas_events=len(event_pairs), new_real_response_events=0, new_real_integrator_calls=0, new_virtual_loop_integrations=0))
    write(ROOT / 'response-inputs.json', consumed)
    write(ROOT / 'progress.json', dict(state='response_assessment_complete'))
    print(json.dumps(dict(response_checks=len(checks), failed=[row for row in checks if not row['passed']], new_response_integrations=0)), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'evolve', 'assess', 'response'])
    arguments = parser.parse_args()
    dict(prepare=prepare, evolve=evolve, assess=assess, response=response)[arguments.phase]()
