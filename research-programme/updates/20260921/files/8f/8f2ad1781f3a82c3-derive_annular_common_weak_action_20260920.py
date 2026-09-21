from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import decimal_fraction, apply_rational_rows, polynomial_products, weighted_moments, contract
from annular_common_P2_overlay_20260919 import forms
from annular_decimal_transport_v2_20260919 import DecimalAction, DecimalMap, decimal_array
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from derive_annular_commutator_riesz_bound_20260919 import mass_apply
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def dec_saved(values):
    values = np.asarray(values, dtype=object)
    return np.array([Decimal(value) for value in values.flat], dtype=object).reshape(values.shape)


def factor_mapping(data, name):
    return DecimalMap(csr_matrix((data[name+'_data'], data[name+'_indices'], data[name+'_indptr']),
        shape=tuple(data[name+'_shape'])))


def native_forms(action, data, fields):
    result = dict(mass=sum(fields[:, 2]*mass_apply(action, fields[:, 3:4])[:, 0], Decimal(0)))
    for name in ['gradient', 'gram']:
        values = factor_mapping(data, name).apply(fields[:, :2])
        result[name] = sum(decimal_array(data[name+'_weights'])*values[:, 0]*values[:, 1], Decimal(0))
    return result


def fixture(evidence, mesh):
    count = mesh['count']
    fractions = [[Fraction((index*13+column*7) % 31-15, 16) for column in range(4)] for index in range(count)]
    values = np.array([[decimal_fraction(value) for value in row] for row in fractions], dtype=object)
    products = polynomial_products(mesh, values)
    moments = np.array([[decimal_fraction((Fraction(upper)-Fraction(lower))/(degree+1)) for degree in range(5)]
        for lower, upper in zip(mesh['edges'][:-1], mesh['edges'][1:])], dtype=object)
    rational_mesh = dict(mesh, edges=list(map(Fraction, mesh['edges'])))
    for name, first, last, number in [('gradient', 0, 1, 1), ('mass', 2, 3, 0)]:
        plus = [row[first]+row[last] for row in fractions]
        minus = [row[first]-row[last] for row in fractions]
        exact = (forms(rational_mesh, plus)[number]-forms(rational_mesh, minus)[number])/4
        actual = sum(contract(moments, products[name]), Decimal(0))
        error = abs(actual-decimal_fraction(exact))
        evidence.check(name+'_moment_polynomial_independent_polarization', error < Decimal('1e-44'), str(error))


def main():
    evidence = EvidenceRun('annular-common-weak-action-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, all_native_components_retained=True, no_singular_projected_mass_inverse=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            original_physical_force_mismatch_unchanged=True, frozen_source_force_derived_probe_not_dynamic_force_budget=True,
            parent_coefficient_precision='binary64', decimal_accumulation_digits=64,
            weighted_forms_precision_qualified=False, maximum_wall_seconds=7200)
        evidence.report['channels'], evidence.report['regions'], evidence.report['controls'], evidence.report['refinement'] = [], [], [], []
        prior_path = evidence.output.parent/'annular-decimal-duality-attempt02/status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('previous_strict_frozen_duality_preserved', prior['state'] == 'complete' and prior['original_strict_dual_gate_pass'])
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                mesh = packet['overlay']
                fixture(evidence, mesh)
                geometry = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
                data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+name+'-action.npz')
                    for name in ['coarse', 'fine']]
                actions = [DecimalAction(item) for item in data]
                initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
                representers = owned_json(evidence, 'annular-commutator-riesz-bound-attempt01', branch+'-riesz-representers.json')
                position = dec_saved(representers['position'])[:, 1]
                velocity = dec_saved(representers['velocity'])[:, 1]
                fields = np.column_stack([position, decimal_array(initial['0_position']), velocity, -decimal_array(initial['0_reverse_velocity'])])
                matrices = checked_load(evidence, 'annular-action-adjoint-stability-attempt01', branch+'_final-action-matrices.npz')
                legacy = DecimalMap(csr_matrix(matrices['interpolation'])).apply(fields)
                true = apply_rational_rows(packet['embeddings'][0], fields)
                canonical = apply_rational_rows(packet['left_inverses'][1], true)
                variants = dict(true=true, canonical=apply_rational_rows(packet['embeddings'][1], canonical),
                    legacy=apply_rational_rows(packet['embeddings'][1], legacy))
                products = {name:polynomial_products(mesh, values) for name, values in variants.items()}
                native = [native_forms(actions[0], data[0], fields), native_forms(actions[1], data[1], legacy)]
                coarse_gram = factor_mapping(data[0], 'gram').apply(fields[:, :2])
                fine_gram_legacy = factor_mapping(data[1], 'gram').apply(legacy[:, :2])
                fine_gram_true = factor_mapping(data[1], 'gram').apply(canonical[:, :2])
                coarse_gram_product = coarse_gram[:, 0]*coarse_gram[:, 1]
                fine_true_product = fine_gram_true[:, 0]*fine_gram_true[:, 1]
                fine_legacy_product = fine_gram_legacy[:, 0]*fine_gram_legacy[:, 1]
                fine_weights = decimal_array(data[1]['gram_weights'])
                counter_weights = decimal_array(geometry['fine_gram_weights_at_coarse_geometry'])
                gram_sampler = sum(fine_weights*(fine_legacy_product-fine_true_product), Decimal(0))
                gram_geometry = sum((fine_weights-counter_weights)*fine_true_product, Decimal(0))
                gram_stencil = (sum(counter_weights*fine_true_product, Decimal(0))
                    -sum(decimal_array(data[0]['gram_weights'])*coarse_gram_product, Decimal(0)))
                evidence.check(branch+'_exact_original_Gram_stencil_telescope',
                    abs(native[1]['gram']-native[0]['gram']-gram_sampler-gram_geometry-gram_stencil) < Decimal('1e-40'))
                anchor = Fraction(mesh['anchor'])
                source_touching = np.array([Fraction(lower) == anchor or Fraction(upper) == anchor
                    for lower, upper in zip(mesh['edges'][:-1], mesh['edges'][1:])])
                erased = {265, 266, 267, 271, 272, 273}
                coarse_edges = list(map(Fraction, packet['native'][0]['edges']))
                erased_cells = []
                from bisect import bisect_right
                for lower, upper in zip(mesh['edges'][:-1], mesh['edges'][1:]):
                    parent = bisect_right(coarse_edges, (Fraction(lower)+Fraction(upper))/2)-1
                    erased_cells.append(bool(erased.intersection(packet['native'][0]['elements'][parent])))
                erased_cells = np.array(erased_cells) & ~source_touching
                groups = [('source_touching', source_touching), ('erased_basis_support', erased_cells),
                    ('remaining', ~(source_touching | erased_cells))]
                prior_row = next(row for row in prior['cases'] if row['branch'] == branch
                    and row['comparison'] == 'spatial64' and row['digits'] == 48)
                literal_gate = Decimal(prior_row['unchanged_numerical_tolerance'])
                by_order = {}
                for order in [16, 32, 64]:
                    if perf_counter()-started > 7200:
                        raise RuntimeError('Safe common-form saved boundary reached.')
                    quadrature = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-order'+str(order)+'-densities.npz')
                    moments = weighted_moments(mesh, geometry['integration_cuts'], quadrature)
                    unit_error = max(abs(moments['unit'][index, degree]/decimal_fraction((Fraction(upper)-Fraction(lower))/(degree+1))-1)
                        for index, (lower, upper) in enumerate(zip(mesh['edges'][:-1], mesh['edges'][1:])) for degree in range(5))
                    evidence.check(branch+'_'+str(order)+'_positive_unit_moment_control', unit_error < Decimal('2e-14'), str(unit_error))
                    sums = {}
                    for kind in ['mass', 'gradient']:
                        fine_moments, coarse_moments = moments['fine_'+kind], moments['coarse_'+kind]
                        common_fine = {name:sum(contract(fine_moments, item[kind]), Decimal(0)) for name, item in products.items()}
                        common_coarse = sum(contract(coarse_moments, products['true'][kind]), Decimal(0))
                        row_sampler = contract(fine_moments, products['legacy'][kind]-products['canonical'][kind])
                        row_alias = contract(fine_moments, products['canonical'][kind]-products['true'][kind])
                        row_geometry = contract(fine_moments-coarse_moments, products['true'][kind])
                        row = dict(branch=branch, order=order, sector=kind,
                            fine_native_quadrature_and_basis=native[1][kind]-common_fine['legacy'],
                            legacy_sampler_arithmetic=sum(row_sampler, Decimal(0)),
                            representation_alias=sum(row_alias, Decimal(0)),
                            geometry_weight_difference=sum(row_geometry, Decimal(0)), stencil_difference=Decimal(0),
                            coarse_native_quadrature_and_basis=common_coarse-native[0][kind],
                            native_difference=native[1][kind]-native[0][kind],
                            fine_true_common_form=common_fine['true'], coarse_true_common_form=common_coarse,
                            common_true_geometry_difference=common_fine['true']-common_coarse)
                        keys = ['fine_native_quadrature_and_basis', 'legacy_sampler_arithmetic', 'representation_alias',
                            'geometry_weight_difference', 'stencil_difference', 'coarse_native_quadrature_and_basis']
                        error = abs(sum((row[key] for key in keys), Decimal(0))-row['native_difference'])
                        evidence.check(branch+'_'+str(order)+'_'+kind+'_literal_prior_precision_telescope', error <= literal_gate,
                            dict(error=str(error), literal_gate=str(literal_gate)))
                        row['reconstruction_error'] = error
                        row['literal_predecessor_gate'] = literal_gate
                        sums[kind] = row
                        evidence.report['channels'].append({key:str(value) if isinstance(value, Decimal) else value for key, value in row.items()} | dict(valid_for_claim=False))
                        for term, local_values in [('representation_alias', row_alias), ('geometry_weight_difference', row_geometry)]:
                            for label, selected in groups:
                                evidence.report['regions'].append(dict(branch=branch, order=order, sector=kind, term=term,
                                    region=label, cells=int(sum(selected)), signed_value=str(sum(local_values[selected], Decimal(0))),
                                    absolute_cell_sum=str(sum(abs(local_values[selected]), Decimal(0))), valid_for_claim=False))
                    sums['gram'] = dict(legacy_sampler_arithmetic=gram_sampler, representation_alias=Decimal(0),
                        geometry_weight_difference=gram_geometry, stencil_difference=gram_stencil,
                        fine_native_quadrature_and_basis=Decimal(0), coarse_native_quadrature_and_basis=Decimal(0),
                        native_difference=native[1]['gram']-native[0]['gram'])
                    by_order[order] = sums
                    evidence.report['controls'].append(dict(branch=branch, order=order,
                        unit_moment_maximum_relative_error=str(unit_error), parent_geometry_precision='binary64', valid_for_claim=False))
                    output = evidence.output/(branch+'-order'+str(order)+'-moments.json')
                    output.write_text(json.dumps({name:values.tolist() for name, values in moments.items()}, default=str)+'\n', encoding='utf-8')
                    evidence.own(output, 'outputs')
                    evidence.report['progress'] = dict(branch=branch, order=order, seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
                for first, last in [(16, 32), (32, 64)]:
                    for kind in ['mass', 'gradient']:
                        keys = ['representation_alias', 'geometry_weight_difference', 'coarse_native_quadrature_and_basis',
                            'fine_native_quadrature_and_basis', 'legacy_sampler_arithmetic']
                        change = max(abs(by_order[last][kind][key]-by_order[first][kind][key]) for key in keys)
                        evidence.report['refinement'].append(dict(branch=branch, sector=kind, first_order=first, last_order=last,
                            maximum_channel_change=str(change), literal_predecessor_gate=str(literal_gate),
                            literal_gate_pass=bool(change <= literal_gate), valid_for_claim=False))
                for kind in ['mass', 'gradient', 'gram']:
                    row = by_order[64][kind]
                    evidence.report['cases'].append(dict(branch=branch, sector=kind, order=64,
                        **{key:str(value) for key, value in row.items() if isinstance(value, Decimal)}, valid_for_claim=False))
                output = evidence.output/(branch+'-probe-fields.json')
                output.write_text(json.dumps(dict(coarse=fields.tolist(), fine_legacy=legacy.tolist(), fine_canonical=canonical.tolist(),
                    common={name:values.tolist() for name, values in variants.items()},
                    products={name:{kind:values.tolist() for kind, values in item.items()} for name, item in products.items()},
                    native_forms=native), default=str)+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
                evidence.save()
            evidence.report['weighted_forms_precision_qualified'] = all(row['literal_gate_pass']
                for row in evidence.report['refinement'] if row['last_order'] == 64)
        evidence.report['seconds'] = perf_counter()-started
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started,
            weighted_forms_precision_qualified=evidence.report['weighted_forms_precision_qualified'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
