from derive_annular_source_gravity_20260914 import EvidenceRun
from validate_annular_native_shape_stress_v2_20260928 import DirectNodalKernel, archive, decimal_array
from validate_annular_native_time_current_20260928 import direct_gradient, positions_and_columns, interval_moments
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_directional_coupled_Euler_20260928 import restore_flow, layer
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_moving_Legendre_current_20260921 import samples
from annular_radial_Ward_moments_20260921 import prepare
from annular_support_shift_jet_20260928 import make_packet, wave_blocks
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


def continuum_identity(evidence):
    alpha, beta, alpha_r, beta_r, beta_t, temporal, gradient, gradient_r, rate_r, speed, speed_r, accel, mesh_accel = sp.symbols('alpha beta alpha_r beta_r beta_t T g g_r qdot_r W W_r a Wdot')
    alpha_t = -alpha * beta_t / beta
    gradient_dot = rate_r - speed_r * gradient
    temporal_dot = accel - mesh_accel * gradient - speed * gradient_dot
    temporal_r = rate_r - speed_r * gradient - speed * gradient_r
    alpha_dot, beta_dot = alpha_t + speed * alpha_r, beta_t + speed * beta_r
    energy = (alpha * temporal**2 + beta * gradient**2) / 2
    energy_dot = (alpha_dot * temporal**2 + beta_dot * gradient**2) / 2 + alpha * temporal * temporal_dot + beta * gradient * gradient_dot
    energy_r = (alpha_r * temporal**2 + beta_r * gradient**2) / 2 + alpha * temporal * temporal_r + beta * gradient * gradient_r
    momentum_dot = (alpha_dot + speed_r * alpha) * temporal + alpha * temporal_dot
    flux_r = alpha_r * speed * temporal + alpha * speed_r * temporal + alpha * speed * temporal_r + beta_r * gradient + beta * gradient_r
    euler = momentum_dot - flux_r
    energy_flux_r = beta_r * temporal * gradient + beta * temporal_r * gradient + beta * temporal * gradient_r
    evidence.check('continuum_wave_current_Euler_reduction', sp.simplify(energy_dot - beta_t * energy / beta - euler * temporal - energy_flux_r - speed * energy_r) == 0)
    time = sp.symbols('time')
    support, shift = sp.Function('s')(time), sp.Function('v')(time)
    coeff = [sp.Function('C' + str(index))(time) for index in range(3)]
    density = shift * (coeff[0] * support + coeff[1] * sp.diff(support, time) + coeff[2] * sp.diff(support, time, 2))
    euler_support = -sp.diff(density, support) + sp.diff(sp.diff(density, sp.diff(support, time)), time) - sp.diff(sp.diff(density, sp.diff(support, time, 2)), time, 2)
    expected = -coeff[0] * shift + sp.diff(coeff[1] * shift, time) - sp.diff(coeff[2] * shift, time, 2)
    evidence.check('full_time_jet_adjoint_reaction', sp.expand(euler_support - expected) == 0)


def high_precision_acceleration(packet, power):
    def convert(key):
        return np.array([Decimal.from_float(float(value)) for value in np.asarray(packet[key]).ravel()], dtype=object).reshape(np.shape(packet[key]))
    source = Decimal.from_float(float(packet['source']))
    radii, node_radii = convert('radius'), convert('node_radius')
    integral = ((radii - 6)**(power + 1) - (source - 6)**(power + 1)) / (power + 1)
    node_integral = ((node_radii - 6)**(power + 1) - (source - 6)**(power + 1)) / (power + 1)
    local = convert('local')
    shapes = np.array([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)], dtype=object).T
    indices = packet['indices']
    nodes = convert('node_rate') * node_integral
    weighted = np.sum(shapes * nodes[np.maximum(indices, 0)] * (indices >= 0), axis=1)
    temporal = convert('rate') - convert('speed') * convert('gradient')
    defect = convert('direction_rate') - convert('direction_speed') * convert('gradient')
    density = convert('measure') * convert('alpha') * defect * (temporal * integral - weighted)
    return sum(density, Decimal(0)), sum(abs(density), Decimal(0))


def main():
    evidence = EvidenceRun('annular-support-shift-jet-validation-attempt01', __file__)
    started = perf_counter()
    try:
        path = evidence.output.parent / 'annular-support-shift-jet-attempt01/status.json'
        parent = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('main_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        bad, digests = [], {}
        for category in ['inputs', 'outputs']:
            for relative, digest in parent[category].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    bad.append(relative)
                else:
                    evidence.own(path)
                    digests[str(path.relative_to(evidence.root))] = digest
        evidence.check('main_provenance_unchanged', not bad, bad)
        continuum_identity(evidence)
        rows, quadrature_rows = [], []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                mesh = json.loads((evidence.root / case['sources']['packet']).read_text())
                direct = DirectNodalKernel(mesh['mesh'], mesh['gram_support'], case['branch'] == 'MTS-primary')
                material = archive(evidence.root / case['material_paths'][1])
                channels = list(material['channels'])
                loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], perf_counter() + 3600)
                flow, tangent, unused_centre = restore_flow(evidence, digests, action, sources, case['level'])
                acceleration = flow['accelerations'][-1]
                polynomial, unused = prepare(action, loads, acceleration)
                directions = archive(evidence.root / case['direction_path'])
                correction = archive(evidence.root / case['correction_path'])['correction']
                engine = NativeKernel(mesh['mesh'], mesh['gram_support'], case['branch'] == 'MTS-primary')
                label = float(material['labels'][31])
                unused_values, raw, unused_pins = layer(engine, loads, action, tangent, acceleration, polynomial,
                    directions['edge_vertices'], directions['field_vertices'], label, 8)
                sampled = samples(action, label, 8)
                data = physical_data(engine, loads, action, label)
                cardinal = data['cardinal']
                for mode in [0, 1]:
                    source_direction = -float(cardinal @ correction[:, -1]) if mode else 0.
                    field_direction = cardinal @ directions['field_vertices'] - (cardinal @ correction[:, :-1] if mode else 0)
                    edge_direction = cardinal @ directions['edge_vertices'] + np.asarray(data['displacement'], float) * source_direction
                    packet8, direction8 = make_packet(engine, data, raw, sampled, acceleration, field_direction, edge_direction, source_direction)
                    for power in range(3):
                        values8 = wave_blocks(packet8, direction8, power)
                        expected = material['values'][31, mode, power, [0, 4, 8]]
                        error = float(np.max(abs(values8 - expected)))
                        evidence.check(name + ':spatial8_12:' + str(mode) + ':' + str(power), error <= 2e-15, error)
                        quadrature_rows.append(dict(branch=case['branch'], level=case['level'], mode=mode, power=power, max_difference=error))
                for relative in case['material_paths']:
                    saved = archive(evidence.root / relative)
                    evidence.check(relative + ':finite', np.isfinite(saved['values']).all())
                    error = np.max(abs(np.tensordot(saved['weights'], saved['values'], axes=(0, 0)) - saved['average']))
                    evidence.check(relative + ':independent_average', error <= 2e-20)
                    values = saved['values']
                    evidence.check(relative + ':sector_sum', np.max(abs(values[..., 0] + values[..., 1] + values[..., 2] - values[..., 3])) <= 2e-20)
                for relative in case['probe_paths']:
                    packet = archive(evidence.root / relative)
                    mode = 1 if '-compensated-' in relative else 0
                    label_index = int(np.argmin(abs(material['labels'] - float(packet['label']))))
                    evidence.check(relative + ':exact_material_label', material['labels'][label_index] == float(packet['label']))
                    edges, field, beta, beta_r, field_rate, edge_rate = [decimal_array(packet[key]) for key in
                        ['native_edges', 'native_field', 'native_beta', 'native_beta_r', 'native_direction_field', 'native_direction_edges']]
                    base = direct.evaluate(edges, field, beta)
                    field_gradient = direct_gradient(direct, edges, field, beta, base)
                    positions, unused = positions_and_columns(direct, edges, len(field))
                    rates = []
                    for step in [Decimal('.0001'), Decimal('.00005'), Decimal('.000025')]:
                        plus = direct.evaluate(edges + step * edge_rate, field + step * field_rate, beta)['image']
                        minus = direct.evaluate(edges - step * edge_rate, field - step * field_rate, beta)['image']
                        rates.append((plus - minus) / (2 * step))
                    image_rate = (4 * rates[2] - rates[1]) / 3
                    load_rate = direct.apply(1, base['image'] * image_rate, True)
                    atom_rate = beta * load_rate + beta_r * edge_rate[direct.native] * base['load']
                    local = beta * base['load'] * edge_rate[direct.native]
                    moments, tail = interval_moments(edges[direct.anchor], positions, field_gradient * field_rate,
                        edges[direct.native], atom_rate, local)
                    evidence.check(relative + ':interval_tail_cancels', abs(tail) <= Decimal('1e-50'))
                    for power in range(3):
                        expected = material['values'][label_index, mode, power]
                        gram_error = moments[power] - Decimal.from_float(float(expected[channels.index('gram_velocity')]))
                        evidence.check(relative + ':independent_Gram_interval:' + str(power), abs(gram_error) <= Decimal('1e-22') + Decimal('2e-7') * abs(moments[power]), str(gram_error))
                        high, scale = high_precision_acceleration(packet, power)
                        high_error = high - Decimal.from_float(float(expected[channels.index('wave_acceleration')]))
                        evidence.check(relative + ':70digit_acceleration:' + str(power), abs(high_error) <= Decimal('2e-20'), str(high_error))
                        rows.append(dict(branch=case['branch'], level=case['level'], mode='compensated' if mode else 'original',
                            label=float(packet['label']), power=power, gram_direct=str(moments[power]), gram_difference=str(gram_error),
                            acceleration_70digit=str(high), acceleration_float=float(expected[channels.index('wave_acceleration')]),
                            acceleration_difference=str(high_error), acceleration_absolute_scale=str(scale)))
        path = evidence.output / 'independent-mixed-blocks.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        path = evidence.output / 'spatial-quadrature-checks.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(quadrature_rows[0]))
            writer.writeheader()
            writer.writerows(quadrature_rows)
        evidence.own(path, 'outputs')
        for relative in parent['outputs']:
            if relative.endswith('.csv'):
                with (evidence.root / relative).open(newline='', encoding='utf-8') as stream:
                    parsed = list(csv.DictReader(stream))
                evidence.check(relative + ':CSV', bool(parsed) and all(None not in row and None not in row.values() for row in parsed))
        evidence.report.update(seconds=perf_counter() - started, independent_rows=len(rows), new_nonlinear_solves=0,
            acceleration_precision=70, scope='Independent direct nodal/interval current and represented-jet precision checks; continuum Euler identity and full time-jet adjoint reaction derived')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
