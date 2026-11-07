from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C1_response_context_20261001 import restore_velocity, metric_packet
from annular_C1_coefficient_response_20261001 import analytic_response, current_values
from annular_moving_Legendre_current_20260921 import samples
from annular_reacted_support_columns_20260929 import columns_layer, move_metric_packet
from annular_support_shift_jet_20260928 import make_packet, perturb, interpolate, wave_current
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_radial_Ward_moments_20260921 import prepare
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse, CoordinateAdapter
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import os
import numpy as np


def historical_wave(restored, row, label, inputs):
    evaluator, setup = restored['evaluator'], restored['setup']
    action, native, loads = evaluator.action, setup['native'], setup['loads']
    data = physical_data(native, loads, action, label)
    cardinal = data['cardinal']
    geometry, quad = row['geometry'], row['quadrature']
    cells, local = quad['cells'], quad['local']
    coefficients = np.einsum('cpl,l->cp', inputs['polynomial'], cardinal)[cells]
    acceleration = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
    source_acceleration = float(inputs['acceleration'][:, -1]@cardinal)
    raw = dict(measure=quad['measure']*geometry['jacobian'],
        gradient=row['gradient']/geometry['jacobian'], rate=row['rate'],
        rate_r=row['rate_gradient']/geometry['jacobian'], acceleration=acceleration,
        speed=geometry['displacement']*row['velocity'],
        speed_r=geometry['jacobian_source']*row['velocity']/geometry['jacobian'],
        speed_rate=geometry['displacement']*source_acceleration)
    source_direction = -float(cardinal@inputs['correction'][:, -1])
    field_direction = cardinal@(inputs['directions']['field_vertices']-inputs['correction'][:, :-1])
    edge_direction = cardinal@inputs['directions']['edge_vertices']+np.asarray(data['displacement'], float)*source_direction
    packet, direction = make_packet(native, data, raw, row, inputs['acceleration'],
        field_direction, edge_direction, source_direction)
    direction['edge_speed'] = edge_direction
    amount = 1e-25j
    changed = perturb(packet, direction, amount)
    nodes = cardinal@restored['reaction']['acceleration_change'][:, :-1]
    source_reaction = float(cardinal@restored['reaction']['acceleration_change'][:, -1])
    changed['acceleration'] = packet['acceleration']+amount*interpolate(packet, nodes)[0]
    changed['speed_rate'] = packet['speed_rate']+amount*geometry['displacement']*source_reaction
    changed = move_metric_packet(changed, row, action, inputs['velocity'],
        inputs['changed_time'], inputs['baseline_time'], amount)
    wave = np.array([wave_current(changed, power).imag/amount.imag for power in range(3)])
    radius = float(data['source'])
    values = action.solver.values(action.solution, np.array([radius]))[0][:, 0]
    values = values+amount*inputs['velocity'].values(np.array([radius]))[:, 0]
    speed = float(data['source_velocity'])+amount*source_direction
    lapse, geometry_value = np.exp(values[1]), 1-2*values[0]/radius
    dust = (action.owner.source_mass*lapse**2*speed/np.sqrt(lapse**2-speed**2/geometry_value)).imag/amount.imag
    return wave, dust*(radius-6)**np.arange(3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--branch', choices=['reference-reference', 'MTS-primary'], required=True)
    parser.add_argument('--cpu', type=int, choices=[2,4], required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1<<args.cpu):
        raise OSError('Affinity not applied')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+5400
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-C1-integral-contract.md')
        probe_path = evidence.output.parent/'annular-C1-coefficient-probe-attempt02/status.json'
        probe = json.loads(probe_path.read_text())
        evidence.own(probe_path)
        evidence.check('point_gate_complete', probe['state']=='complete' and all(row['passed'] for row in probe['checks']))
        for category in ['inputs', 'outputs']:
            for relative, expected in probe[category].items():
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed point gate input '+relative)
        with localcontext() as context:
            context.prec = 70
            restored = restore_velocity(evidence, args.branch, deadline)
            evaluator, read, report = [restored[key] for key in ['evaluator', 'read', 'report']]
            action, setup = evaluator.action, restored['setup']
            match = lambda status:next(row for row in status['cases'] if row['branch']==args.branch and row['level']=='third')
            historical = match(report('annular-reacted-support-columns-attempt02'))
            flow = match(report('annular-direct-background-coupled-current-attempt01'))
            make_response = lambda data:MetricResponse(*reconstructed_solver(data), data.get('forcing'), 0., [])
            background = make_response(read(flow['paths']['background_response']))
            base_velocity = make_response(read(flow['paths']['velocity_response']))
            inputs = dict(acceleration=read(flow['paths']['flow'])['acceleration'],
                directions=read(restored['live']['direction_path']),
                correction=read(restored['live']['paths']['projection'])['correction'],
                velocity=make_response(read(restored['live']['paths']['live_response'])),
                changed_time=make_response(read(restored['reacted']['paths']['corrected_metric_time'])),
                baseline_time=TotalResponse(background, base_velocity))
            inputs['polynomial'] = prepare(action, setup['loads'], inputs['acceleration'])[0]
            tangent = JointMetricTangent(CoordinateAdapter(background), [base_velocity])
            evidence.report.update(branch=args.branch, level='third', rule_outputs=[],
                channels=['historical_wave', 'shared_expanded_wave', 'coefficient_analytic_wave', 'historical_dust'],
                force_native_held=True, source_geometry_spread_retained=True,
                github_action=False, subagents_used=False, valid_for_claim=False)
            for order in [48,64]:
                owned = read(historical['paths']['material'+str(order)])
                labels, weights = owned['labels'], owned['weights']
                layers = []
                for index, (label, weight) in enumerate(zip(labels, weights)):
                    if perf_counter()>deadline:
                        raise RuntimeError('Safe C1 material integration boundary')
                    row = samples(action, label, 12)
                    old, dust = historical_wave(restored, row, label, inputs)
                    radius = row['geometry']['radius']
                    offsets = radius-evaluator.anchor
                    data, active = evaluator.packet(np.full(len(radius), label), offsets,
                        cells=row['quadrature']['cells'], local=row['quadrature']['local'])
                    if not active.all():
                        raise RuntimeError('Inactive material point')
                    metric = metric_packet(restored, offsets)
                    measure = row['quadrature']['measure']*row['geometry']['jacobian']
                    raw = current_values(data, radius, *metric, amount=1e-25j, original=True).imag/1e-25
                    new = analytic_response(data, radius, *metric)
                    layers.append(np.array([old, raw[1:]@measure, new[1:]@measure, dust]))
                    if index==order//2:
                        checked = columns_layer(setup['native'], setup['loads'], action, tangent,
                            inputs['acceleration'], inputs['polynomial'], inputs['directions'], inputs['correction'],
                            restored['reaction']['acceleration_change'], inputs['velocity'], inputs['changed_time'],
                            inputs['baseline_time'], label)
                        difference = old+dust+checked['native_column'][1:]-checked['column1'][1:]
                        evidence.check('original_decomposition-'+str(order), np.max(abs(difference))<=2e-24, difference.tolist())
                        recorded = owned['layers'][index, 1, 1:]
                        discrepancy = checked['column1'][1:]-recorded
                        evidence.check('historical_layer_replay-'+str(order), np.max(abs(discrepancy))<=2e-24, discrepancy.tolist())
                    if index%8==7 or index+1==order:
                        path = evidence.output/('partial-'+str(order)+'.npz')
                        temporary = path.with_suffix('.npz.tmp')
                        with temporary.open('wb') as stream:
                            np.savez_compressed(stream, layers=np.array(layers), labels=labels, weights=weights,
                                next_label=index+1, complete=index+1==order)
                            stream.flush()
                            os.fsync(stream.fileno())
                        temporary.replace(path)
                        evidence.report['progress'] = dict(order=order, next_label=index+1, seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']), flush=True)
                accumulated = np.einsum('l,lrc->rc', weights, np.array(layers))
                revised = owned['total'][1].copy()
                revised[1:] += accumulated[2]-accumulated[0]
                density_delta = np.einsum('l,lc->c', weights, np.array(layers)[:,2]-np.array(layers)[:,0])
                rounding_spread = revised[1:]-(owned['total'][1,1:]+density_delta)
                output = evidence.output/('material-'+str(order)+'.npz')
                np.savez_compressed(output, labels=labels, weights=weights, layers=np.array(layers),
                    accumulated=accumulated, revised_wave_only=revised, historical_total=owned['total'][1],
                    gravity=owned['gravity'][1], density_delta=density_delta, rounding_spread=rounding_spread,
                    quadrature=np.array([12,order]))
                evidence.own(output, 'outputs')
                evidence.check('finite_integral-'+str(order), np.isfinite(accumulated).all() and np.isfinite(revised).all())
                summary = dict(order=order, accumulated=accumulated.tolist(), revised_wave_only=revised.tolist(),
                    wave_delta=(accumulated[2]-accumulated[0]).tolist(),
                    formula_delta=(accumulated[2]-accumulated[1]).tolist(),
                    geometry_spread=(accumulated[1]-accumulated[0]).tolist(),
                    rounding_spread=rounding_spread.tolist())
                evidence.report['rule_outputs'].append(dict(path=str(output.relative_to(evidence.root)), summary=summary))
                evidence.save()
                print(json.dumps(summary), flush=True)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter()-started, complete_integrals=True)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path, 'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
