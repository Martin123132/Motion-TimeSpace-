from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_frozen_candidate_20260920 import gram_rows, gram_matrix, sum_rows, forms_from_moments, FrozenCandidate, source_force
from annular_common_weighted_moments_20260920 import decimal_fraction, apply_rational_rows
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
from bisect import bisect_right
from time import perf_counter
import contextlib
import json
import numpy as np


def coefficients(layer, position, reference):
    radius, jacobian, displacement = layer.mapping(reference, position)
    lapse, root = layer.metric(0., radius)
    physical = radius**2*lapse*root
    mass = jacobian*radius**4/physical
    gradient = physical/jacobian
    transport = displacement/jacobian
    return dict(mass=mass, gradient=gradient, transport=transport, radius=radius,
        jacobian=jacobian, displacement=displacement, coefficient=physical)


def derivative_coefficients(layer, position, reference):
    result = coefficients(layer, position, reference)
    radius, jacobian = result['radius'], result['jacobian']
    mass, log_lapse, mass_radial, lapse_radial = layer.geometry.values(radius)
    metric = 1-2*mass/radius
    log_coefficient_radial = 2/radius+lapse_radial+(-mass_radial/radius+mass/radius**2)/metric
    jacobian_rate = np.where(reference < layer.anchor, 1/(layer.anchor-layer.radii[0]), -1/(layer.radii[-1]-layer.anchor))
    mass_rate = result['mass']*(jacobian_rate/jacobian+result['displacement']*(4/radius-log_coefficient_radial))
    gradient_rate = result['gradient']*(result['displacement']*log_coefficient_radial-jacobian_rate/jacobian)
    transport_rate = -result['transport']*jacobian_rate/jacobian
    result.update(mass_X=mass_rate, gradient_X=gradient_rate, transport_X=transport_rate)
    return result


def integrate_moments(mesh, cuts, fractions, weights, densities):
    edges = list(map(Fraction, mesh['edges']))
    cuts = [Fraction.from_float(float(value)) for value in cuts]
    parents, lengths, offsets, spans = [], [], [], []
    for lower, upper in zip(cuts, cuts[1:]):
        parent = bisect_right(edges, (lower+upper)/2)-1
        if lower < edges[parent] or upper > edges[parent+1]:
            raise ValueError('Quadrature crosses a common cell.')
        width = edges[parent+1]-edges[parent]
        parents.append(parent)
        lengths.append(decimal_fraction(upper-lower))
        offsets.append(decimal_fraction((lower-edges[parent])/width))
        spans.append(decimal_fraction((upper-lower)/width))
    local = np.asarray(offsets, dtype=object)[:, None]+np.asarray(spans, dtype=object)[:, None]*decimal_array(fractions)
    measure = np.asarray(lengths, dtype=object)[:, None]*decimal_array(weights)
    moments = {name:np.full((len(edges)-1, 5), Decimal(0), dtype=object) for name in densities}
    converted = {name:decimal_array(values) for name, values in densities.items()}
    power = np.full(local.shape, Decimal(1), dtype=object)
    for degree in range(5):
        for name, values in converted.items():
            np.add.at(moments[name][:, degree], np.asarray(parents), np.sum(measure*power*values, axis=1))
        power *= local
    return moments


def dust_data(layer, position, velocity):
    lapse, root = layer.metric(0., np.array([position]))
    mass, unused, mass_radial, log_lapse_radial = layer.geometry.values(np.array([position]))
    lapse, root = float(lapse[0]), float(root[0])
    lapse_radial = lapse*float(log_lapse_radial[0])
    root_radial = (-float(mass_radial[0])/position+float(mass[0])/position**2)/root
    clock = np.sqrt(lapse**2-velocity**2/root**2)
    inertia = layer.source_mass*lapse**2/(root**2*clock**3)
    clock_numerator = lapse*lapse_radial+velocity**2*root_radial/root**3
    partial = -layer.source_mass*clock_numerator/clock
    momentum_X = -2*layer.source_mass*velocity*root_radial/(root**3*clock)-layer.source_mass*velocity*clock_numerator/(root**2*clock**3)
    return dict(source_position=float(position), source_velocity=float(velocity), dust_inertia=float(inertia),
        dust_drive=float(partial-velocity*momentum_X), lapse=lapse, root=root,
        lapse_radial=lapse_radial, root_radial=root_radial, source_mass=float(layer.source_mass))


def main():
    evidence = EvidenceRun('annular-complete-frozen-candidate-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, physical_force_mismatch_fixed=False,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            self_consistent_candidate_metric_solved=False, frozen_background_only=True,
            full_candidate_assembly_qualified=False)
        evidence.report['derivatives'], evidence.report['refinement'], evidence.report['forces'] = [], [], []
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                mesh, count = packet['overlay'], packet['overlay']['count']
                initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
                phase = np.stack([apply_rational_rows(packet['embeddings'][0], decimal_array(initial['0_position'])[:, None])[:, 0],
                    apply_rational_rows(packet['embeddings'][0], -decimal_array(initial['0_reverse_velocity'])[:, None])[:, 0]])
                geometry = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
                saved = checked_load(evidence, 'annular-live-compensated-rate-attempt01', branch+'-1e-07-compensated-rate.npz')
                systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
                pair = evaluate_pair(systems, [saved[str(level)+'_state'] for level in range(2)])
                layer, position = pair[0]['layer'], pair[0]['values'][-1]
                dust = dust_data(layer, position, pair[0]['rates'][-1])
                maps_by_order = {}
                for order in [32, 64]:
                    old_quadrature = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-order'+str(order)+'-densities.npz')
                    cuts = geometry['integration_cuts']
                    fractions, weights = old_quadrature['fractions'], old_quadrature['gauss_weights']
                    reference = (cuts[:-1, None]+np.diff(cuts)[:, None]*fractions).ravel()
                    fields = derivative_coefficients(layer, position, reference)
                    moved = coefficients(layer, position+1j*1e-24, reference)
                    for name in ['mass', 'gradient', 'transport']:
                        error = float(np.max(abs(fields[name+'_X']-moved[name].imag/1e-24))/max(1., np.max(abs(fields[name+'_X']))))
                        evidence.check(branch+'_'+str(order)+'_'+name+'_source_derivative', error < 3e-10, error)
                        evidence.report['derivatives'].append(dict(branch=branch, order=order, coefficient=name,
                            complex_step_relative_error=error, fixed_physical_metric=True, valid_for_claim=False))
                    shape = (len(cuts)-1, order)
                    densities = {name:fields[name].reshape(shape) for name in ['mass', 'mass_X', 'gradient', 'gradient_X']}
                    densities['transport'] = (fields['mass']*fields['transport']).reshape(shape)
                    densities['transport_X'] = (fields['mass_X']*fields['transport']+fields['mass']*fields['transport_X']).reshape(shape)
                    densities['inertia'] = (fields['mass']*fields['transport']**2).reshape(shape)
                    densities['inertia_X'] = (fields['mass_X']*fields['transport']**2+2*fields['mass']*fields['transport']*fields['transport_X']).reshape(shape)
                    for name in ['mass', 'gradient']:
                        evidence.check(branch+'_'+str(order)+'_'+name+'_old_density_exact', np.array_equal(densities[name], old_quadrature['coarse_'+name+'_density']))
                    moments = integrate_moments(mesh, cuts, fractions, weights, densities)
                    old_moments = owned_json(evidence, 'annular-common-weak-action-attempt01', branch+'-order'+str(order)+'-moments.json')
                    for name in ['mass', 'gradient']:
                        error = max(abs(value-Decimal(old)) for value, old in zip(moments[name].flat, np.asarray(old_moments['coarse_'+name], dtype=object).flat))
                        evidence.check(branch+'_'+str(order)+'_'+name+'_old_moments_preserved', error < Decimal('1e-40'), str(error))
                    maps_by_order[order] = forms_from_moments(mesh, moments)
                for name in maps_by_order[64]:
                    first, last = maps_by_order[32][name], maps_by_order[64][name]
                    maximum = max((abs(value-first[index].get(column, Decimal(0))) for index, row in enumerate(last) for column, value in row.items()), default=Decimal(0))
                    scale = max(Decimal(1), max(abs(value) for row in last for value in row.values()))
                    evidence.check(branch+'_'+name+'_quadrature_matrix_refinement', maximum/scale < Decimal('3e-10'), str(maximum/scale))
                    evidence.report['refinement'].append(dict(branch=branch, matrix=name, relative_change=str(maximum/scale),
                        gate='3e-10', not_a_physical_force_gate=True, valid_for_claim=False))
                knots = sorted(map(Fraction, mesh['nodes']))
                coordinate = np.array([float(value) for value in knots])
                node_fields = derivative_coefficients(layer, position, coordinate)
                source_profile = checked_load(evidence, 'annular-nonuniform-Gram-parent-probes-attempt02', branch+'-profile0-initial-profile.npz')
                evidence.check(branch+'_old_Gram_node_weight_exact', np.array_equal(node_fields['gradient'], source_profile['coefficient']))
                for extension in (['reference'] if branch == 'reference' else ['primary', 'alternative']):
                    if extension == 'reference':
                        factors, row_weights, derivative_weights = [], [], []
                        gram, gram_X = [[{} for unused in range(count)] for unused in range(2)]
                    else:
                        factors, sampling = gram_rows(mesh, knots, extension == 'alternative')
                        from qualify_annular_nonuniform_Gram_precision_20260920 import sparse_apply
                        row_weights = sparse_apply(sampling, list(decimal_array(node_fields['gradient'])))
                        derivative_weights = sparse_apply(sampling, list(decimal_array(node_fields['gradient_X'])))
                        gram = gram_matrix(factors, row_weights, count)
                        gram_X = gram_matrix(factors, derivative_weights, count)
                    maps = dict(maps_by_order[64])
                    maps['stiffness'] = sum_rows(maps['gradient'], gram)
                    maps['stiffness_X'] = sum_rows(maps['gradient_X'], gram_X)
                    serial = dict(count=count, branch=branch, extension=extension, dust=dust, phase=phase.tolist(),
                        maps={name:MixedMap(rows, count).serialize() for name, rows in maps.items()},
                        gram_factor=MixedMap(factors, count).serialize(), gram_weights=list(map(str, row_weights)),
                        gram_weights_X=list(map(str, derivative_weights)), valid_for_claim=False)
                    action = FrozenCandidate(serial)
                    for name in ['mass', 'mass_X', 'gradient', 'gradient_X', 'inertia', 'inertia_X', 'stiffness', 'stiffness_X']:
                        symmetric = all(value == maps[name][column].get(row, Decimal(0)) for row, entries in enumerate(maps[name]) for column, value in entries.items())
                        evidence.check(branch+'_'+extension+'_'+name+'_symmetric', symmetric)
                    probe = np.array([[Decimal((index*7)%17-8)/16] for index in range(count)], dtype=object)
                    solve_error = max(abs(value) for value in (action.maps['mass'].apply(action.solve(probe))-probe).flat)
                    evidence.check(branch+'_'+extension+'_mass_solve', solve_error < Decimal('1e-45'), str(solve_error))
                    if factors:
                        factor_map = MixedMap(factors, count)
                        mapped = factor_map.apply(phase[0, :, None])[:, 0]
                        direct = sum((weight*value**2 for weight, value in zip(row_weights, mapped)), Decimal(0))
                        assembled = sum(phase[0]*MixedMap(gram, count).apply(phase[0, :, None])[:, 0], Decimal(0))
                        evidence.check(extension+'_assembled_positive_Gram_identity', abs(direct-assembled) < Decimal('1e-38') and direct >= 0, str(abs(direct-assembled)))
                    force = source_force(action, *phase, Decimal.from_float(dust['source_velocity']),
                        Decimal.from_float(dust['dust_inertia']), Decimal.from_float(dust['dust_drive']))
                    evidence.check(branch+'_'+extension+'_field_inertia_nonnegative', force['field_inertia_complement'] >= -Decimal('1e-30'))
                    evidence.report['forces'].append(dict(branch=branch, extension=extension,
                        **{name:str(value) for name, value in force.items()}, actual_coupled_evolution=False, valid_for_claim=False))
                    output = evidence.output/(branch+'-'+extension+'-action.json')
                    output.write_text(json.dumps(serial, default=str)+'\n', encoding='utf-8')
                    evidence.own(output, 'outputs')
                    evidence.report['cases'].append(dict(branch=branch, extension=extension, count=count,
                        mass_jacobi_ratio=str(action.mass_jacobi_ratio), unfiltered_frequency_bound=str(action.frequency_bound),
                        steps_at_4e_5=int((Decimal.from_float(4e-5)*action.frequency_bound/4).to_integral_value(rounding='ROUND_CEILING')),
                        minimum_mass_pivot=str(min(action.diagonal)), valid_for_claim=False))
                evidence.report['progress'] = dict(branch=branch, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report.update(full_candidate_assembly_qualified=True, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

