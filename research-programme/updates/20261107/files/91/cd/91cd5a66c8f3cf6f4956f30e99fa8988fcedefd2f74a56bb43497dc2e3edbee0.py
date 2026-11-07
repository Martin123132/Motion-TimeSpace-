from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import restore_native
from annular_native_tangent_precision_repair_20260929 import repair_engine
from annular_position_support_column_20260930 import wave_densities, moved_packet, analytic_volume_column, native_position_probe, dust_rows, dust_position_column, gravity_position_rows
from annular_support_shift_jet_20260928 import make_packet, interpolate, wave_current
from annular_directional_coupled_Euler_20260928 import layer, evaluate_wave
from annular_moving_Legendre_current_20260921 import samples
from annular_position_reaction_20260929 import ResponseSum, second_radial
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from derive_annular_direct_background_coupled_current_20260928 import CoordinateAdapter
from annular_candidate_energy_current_20260921 import reconstructed_solver
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_radial_Ward_moments_20260921 import prepare
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import csv
import hashlib
import json
import numpy as np


def verified_inputs(evidence):
    path = evidence.output.parent / 'annular-refined-wave-stage-integrity-20260930.json'
    seal = json.loads(path.read_text())
    evidence.own(path)
    evidence.check('latest_inherited_seal_complete', seal['state'] == 'complete'
        and seal['third_live_update_complete'] and not seal['mismatches'])
    digests = {}

    def own(relative, expected):
        if relative == 'CURRENT_LOCAL_RESUME.md':
            return
        path = (evidence.root / relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope C0 source: '+relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Changed C0 source: '+relative)
        key = str(path.relative_to(evidence.root))
        if key in digests and digests[key] != expected:
            raise RuntimeError('Conflicting C0 authority: '+relative)
        digests[key] = expected
        evidence.own(path)

    for relative, expected in seal['hashes'].items():
        own(relative, expected)
    authorities = ['annular-position-support-manufactured-attempt01']
    authorities += ['annular-flux-corrected-Euler-'+branch+suffix+'-attempt01'
        for branch in ['reference', 'MTS'] for suffix in ['', '-third']]
    for name in authorities:
        path = evidence.output.parent/name/'status.json'
        status = json.loads(path.read_text())
        own(str(path.relative_to(evidence.root)), hashlib.sha256(path.read_bytes()).hexdigest())
        evidence.check(name+':complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        if 'Euler' in name:
            evidence.check(name+':fresh_equations', status['all_fresh_equation_checks_passed'])
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                own(relative, expected)
    evidence.check('all_inherited_sources_rehashed', len(digests) >= len(seal['hashes']))
    return digests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--branch', choices=['reference-reference', 'MTS-primary'], required=True)
    parser.add_argument('--cpu', type=int, choices=[2, 4], required=True)
    parser.add_argument('--seconds', type=float, default=4000.)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Cannot set single-core affinity')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    try:
        evidence.report.update(scope='Actual four-case C0 pointwise construction; not a complete C0 integral',
            branch=args.branch, logical_cpu=args.cpu, all_four_fresh_Euler_checks_verified=False,
            actual_integrated_C0_complete=False, cut_atoms_integrated=False, pointwise_derivative_only=True,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            inherited_raw_C2_warnings=2, old_weak_flux_flags_retained=True,
            github_action=False, subagents_used=False, original_workbench_write=False, units='code-normalized')
        digests = verified_inputs(evidence)
        evidence.report['all_four_fresh_Euler_checks_verified'] = True
        evidence.own(evidence.root/'DERIVATION-20260930-position-support-C0.md')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe C0 pointwise boundary')

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        def save(name, **arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for level in ['fine', 'third']:
                progress(level+':restore')
                setup = restore_native(evidence, digests, args.branch, level, deadline)
                loads, action, native, read = [setup[key] for key in ['loads', 'action', 'native', 'read']]
                report = lambda name: read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
                match = lambda status: next(row for row in status['cases'] if row['branch'] == args.branch and row['level'] == level)
                live = match(report('annular-live-support-acceleration-attempt01'))
                jets = match(report('annular-position-metric-jet-validation-attempt01'))
                flow = match(report('annular-direct-background-coupled-current-attempt01'))
                directions = read(live['direction_path'])
                correction = read(live['paths']['projection'])['correction']
                mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(flow['paths']['flow'])['acceleration']
                background = response(read(flow['paths']['background_response']))
                velocity = response(read(flow['paths']['velocity_response']))
                metric_time = ResponseSum(background, velocity)
                tangent = JointMetricTangent(CoordinateAdapter(background), [velocity])
                owner = report('annular-wave-flux-live-response-'+level+'-attempt01')
                selected = next(row for row in owner['cases'] if row['summary']['branch'] == args.branch and row['summary']['level'] == level)
                candidate = read(selected['paths']['candidate'])
                mixed = response(candidate)
                position = setup['precision'].position
                precision = repair_engine(setup['precision'])
                polynomial = prepare(action, loads, acceleration)[0]
                gravity24 = gravity_position_rows(action, position, metric_time, mixed, 24)
                gravity32 = gravity_position_rows(action, position, metric_time, mixed, 32)
                gravity_pair = float(np.max(abs(gravity24['column']-gravity32['column'])))
                gravity_oracle = float(np.max(abs(gravity32['column']-gravity32['oracle'])))
                evidence.check(level+':gravity_pair', gravity_pair <= 2e-17, gravity_pair)
                evidence.check(level+':gravity_oracle', gravity_oracle <= 2e-17, gravity_oracle)
                save(level+'-gravity', **{'order24_'+key:value for key, value in gravity24.items()},
                    **{'order32_'+key:value for key, value in gravity32.items()})
                for label_index, label in enumerate([-.31, .07, .33]):
                    progress(level+':layer-'+str(label))
                    baseline, raw, pins = layer(native, loads, action, tangent, acceleration, polynomial,
                        directions['edge_vertices'], directions['field_vertices'], label, 12)
                    evidence.check(level+':pins-'+str(label_index), pins <= 2e-14, pins)
                    row = samples(action, label, 12)
                    data = physical_data(native, loads, action, label)
                    cardinal = data['cardinal']
                    field_change = cardinal @ (directions['field_vertices']-correction[:, :-1])
                    source_change = -float(cardinal @ correction[:, -1])
                    edge_change = cardinal @ directions['edge_vertices'] + np.asarray(data['displacement'], float)*source_change
                    packet, movement = make_packet(native, data, raw, row, acceleration, field_change, edge_change, source_change)
                    values, radial = action.solver.values(action.solution, packet['radius'])
                    second = second_radial(action.solver, action.solution, packet['radius'])
                    pos, pos_r = position.at(packet['radius'])
                    time, time_r = metric_time.at(packet['radius'])
                    nodes_rate = cardinal @ mode_rate[:, :-1]
                    rate_change, rate_r_change = interpolate(packet, nodes_rate)
                    source_rate = float(cardinal @ mode_rate[:, -1])
                    accel_change = interpolate(packet, cardinal @ candidate['acceleration_change'][:, :-1])[0]
                    source_accel_change = float(cardinal @ candidate['acceleration_change'][:, -1])
                    geometry = row['geometry']
                    direction = dict(movement=movement['speed'], movement_r=movement['speed_r'],
                        source=source_change, node_movement=movement['node_speed'], node_rate=nodes_rate,
                        gradient=interpolate(packet, field_change)[1], rate=rate_change, rate_r=rate_r_change,
                        acceleration=accel_change, speed=geometry['displacement']*source_rate,
                        speed_r=geometry['jacobian_source']*source_rate/geometry['jacobian'],
                        speed_rate=geometry['displacement']*source_accel_change,
                        values=values, radial=radial, time=time,
                        material_values=pos+radial*movement['speed'], material_radial=pos_r+second*movement['speed'],
                        material_time=mixed.values(packet['radius'])+time_r*movement['speed'])
                    original = packet
                    packet = moved_packet(original, direction, 0.)
                    replay = np.array([evaluate_wave(packet)['wave_direct']]+[wave_current(packet, power) for power in range(3)])
                    densities = wave_densities(packet)
                    base = densities @ packet['measure']
                    replay_error = float(np.max(abs(base-replay)))
                    evidence.check(level+':density_replay-'+str(label_index), replay_error <= 2e-11*max(1., float(np.max(abs(replay)))), replay_error)
                    analytic = analytic_volume_column(packet, direction)
                    direct_columns, errors = [], []
                    for step in [1e-20, 1e-25]:
                        moved = moved_packet(packet, direction, 1j*step)
                        direct = (wave_densities(moved)*(1+1j*step*direction['movement_r'])).imag/step
                        error = float(np.max(abs(direct-analytic)))
                        scale = max(1., float(np.max(abs(analytic))), float(np.max(abs(direct))))
                        evidence.check(level+':product_rule-'+str(label_index)+':'+str(step), error <= 2e-11*scale,
                            dict(absolute_error=error, comparison_scale=scale, scaled_error=error/scale))
                        direct_columns.append(direct @ packet['measure'])
                        errors.append(error/scale)
                    volume = analytic @ packet['measure']
                    source_values, source_radial = action.solver.values(action.solution, np.array([packet['source']]))
                    source_material = position.values(np.array([packet['source']]))[:, 0]+source_radial[:, 0]*source_change
                    dust = dust_position_column(packet['source'], packet['source_velocity'], source_values[:, 0],
                        action.owner.source_mass, source_change, source_rate, source_material)
                    dust_oracle = dust_rows(packet['source']+1e-25j*source_change,
                        packet['source_velocity']+1e-25j*source_rate, source_values[:, 0]+1e-25j*source_material,
                        action.owner.source_mass).imag/1e-25
                    evidence.check(level+':dust_product_rule-'+str(label_index), np.max(abs(dust-dust_oracle)) <= 2e-17, float(np.max(abs(dust-dust_oracle))))
                    native_probe = native_position_probe(precision, mode_rate, directions, label)
                    native_error = float(np.max(abs(native_probe['finite_differences'])))
                    evidence.check(level+':native_product_rule-'+str(label_index), native_error <= 2e-17, native_error)
                    evidence.check(level+':native_baseline-'+str(label_index), np.max(abs(native_probe['baseline_replay'])) <= 2e-30,
                        float(np.max(abs(native_probe['baseline_replay']))))
                    if not native.enabled:
                        evidence.check(level+':reference_native_disabled-'+str(label_index),
                            np.count_nonzero(native_probe['base'])+np.count_nonzero(native_probe['derivative']) == 0)
                    path = save(level+'-layer'+str(label_index), regular_volume=volume,
                        complex_volume=np.array(direct_columns), dust=dust, dust_oracle=dust_oracle,
                        **{'native_'+key:value for key, value in native_probe.items()})
                    summary = dict(branch=args.branch, level=level, label=label,
                        wave_scaled_derivative_error=max(errors), native_absolute_derivative_error=native_error,
                        gravity_pair_error=gravity_pair, density_baseline_replay_error=replay_error,
                        regular_force_C0=float(volume[0]), native_force_C0=float(native_probe['derivative'][0]),
                        complete_C0_integral=False, valid_for_claim=False)
                    summaries.append(summary)
                    evidence.report['cases'].append(dict(summary=summary, path=path))
                    evidence.save()
                    print(json.dumps(summary), flush=True)
        table = evidence.output/'position-support-probes.csv'
        with table.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(table, 'outputs')
        evidence.report['seconds'] = perf_counter()-started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
