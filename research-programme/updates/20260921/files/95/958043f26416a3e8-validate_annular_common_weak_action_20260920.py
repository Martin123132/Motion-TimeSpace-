from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import decimal_fraction, apply_rational_rows, polynomial_products, contract
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from derive_annular_common_weak_action_20260920 import dec_saved
from run_annular_P2_continuum_bridge_20260918 import checked_load
from bisect import bisect_right
from decimal import Decimal, localcontext
from fractions import Fraction
import contextlib
import json
import numpy as np


def direct_pairing(mesh, cuts, quadrature, values):
    edges = list(map(Fraction, mesh['edges']))
    fractions = [Decimal.from_float(float(value)) for value in quadrature['fractions']]
    weights = [Decimal.from_float(float(value)) for value in quadrature['gauss_weights']]
    result = dict(mass=Decimal(0), gradient=Decimal(0))
    for segment, (first, last) in enumerate(zip(cuts[:-1], cuts[1:])):
        lower, upper = Fraction.from_float(float(first)), Fraction.from_float(float(last))
        parent = bisect_right(edges, (lower+upper)/2)-1
        length = edges[parent+1]-edges[parent]
        offset = decimal_fraction((lower-edges[parent])/length)
        span = decimal_fraction((upper-lower)/length)
        measure = decimal_fraction(upper-lower)
        local = [values[index] if index >= 0 else np.full(4, Decimal(0), dtype=object) for index in mesh['elements'][parent]]
        for node, fraction in enumerate(fractions):
            coordinate = offset+span*fraction
            shape = [(1-coordinate)*(1-2*coordinate), 4*coordinate*(1-coordinate), coordinate*(2*coordinate-1)]
            radial = [(4*coordinate-3)/decimal_fraction(length), (4-8*coordinate)/decimal_fraction(length),
                (4*coordinate-1)/decimal_fraction(length)]
            field = sum((factor*value for factor, value in zip(shape, local)), np.full(4, Decimal(0), dtype=object))
            derivative = sum((factor*value for factor, value in zip(radial, local)), np.full(4, Decimal(0), dtype=object))
            result['mass'] += measure*weights[node]*Decimal.from_float(float(quadrature['fine_mass_density'][segment, node]))*field[2]*field[3]
            result['gradient'] += measure*weights[node]*Decimal.from_float(float(quadrature['fine_gradient_density'][segment, node]))*derivative[0]*derivative[1]
    return result


def main():
    evidence = EvidenceRun('annular-common-weak-controls-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            original_physical_force_mismatch_unchanged=True, independent_unexpanded_quadrature=True)
        path = evidence.output.parent/'annular-common-weak-action-attempt01/status.json'
        source = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('weighted_forms_complete_and_precision_qualified', source['state'] == 'complete'
            and source['weighted_forms_precision_qualified'] and all(row['passed'] for row in source['checks']))
        prior_path = evidence.output.parent/'annular-commutator-riesz-bound-attempt01/status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                mesh = packet['overlay']
                fields = owned_json(evidence, 'annular-common-weak-action-attempt01', branch+'-probe-fields.json')
                saved = owned_json(evidence, 'annular-common-weak-action-attempt01', branch+'-order16-moments.json')
                moments = {name:dec_saved(values) for name, values in saved.items()}
                geometry = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
                quadrature = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-order16-densities.npz')
                true = dec_saved(fields['common']['true'])
                direct = direct_pairing(mesh, geometry['integration_cuts'], quadrature, true)
                products = polynomial_products(mesh, true)
                for kind in ['mass', 'gradient']:
                    measured = sum(contract(moments['fine_'+kind], products[kind]), Decimal(0))
                    error = abs(direct[kind]-measured)
                    row = next(row for row in source['channels'] if row['branch'] == branch and row['sector'] == kind and row['order'] == 16)
                    gate = Decimal(row['literal_predecessor_gate'])
                    evidence.check(branch+'_'+kind+'_independent_unexpanded_weighted_integral', error <= gate,
                        dict(error=str(error), literal_gate=str(gate)))
                    evidence.report['cases'].append(dict(branch=branch, control='independent_direct_'+kind,
                        direct=str(direct[kind]), moment_result=str(measured), error=str(error), valid_for_claim=False))
                native_sum = sum((Decimal(value) for value in fields['native_forms'][0].values()), Decimal(0))
                original = next(row for row in prior['cases'] if row['branch'] == branch and row['comparison'] == 'spatial64')
                error = abs(native_sum+Decimal(original['residual_pairing'])-Decimal(original['original_commutator']))
                evidence.check(branch+'_original_coarse_force_derived_probe_reproduced', error <= Decimal(original['unchanged_numerical_tolerance']), str(error))
                anchor = Fraction(mesh['anchor'])
                native_nodes = list(map(Fraction, packet['native'][0]['nodes']))
                smooth = np.array([[decimal_fraction(location-anchor), decimal_fraction((location-anchor)**2),
                    decimal_fraction((location-anchor)**2), decimal_fraction(location-anchor)] for location in native_nodes], dtype=object)
                common = apply_rational_rows(packet['embeddings'][0], smooth)
                fine = apply_rational_rows(packet['left_inverses'][1], common)
                reconstructed = apply_rational_rows(packet['embeddings'][1], fine)
                smooth_error = max(map(abs, (common-reconstructed).flat))
                evidence.check(branch+'_shared_linear_quadratic_fields_not_changed', smooth_error < Decimal('1e-48'), str(smooth_error))
                witness = np.full((len(native_nodes), 4), Decimal(0), dtype=object)
                witness[265, :] = Decimal(1)
                common = apply_rational_rows(packet['embeddings'][0], witness)
                fine = apply_rational_rows(packet['left_inverses'][1], common)
                evidence.check(branch+'_canonical_fine_sampler_still_misses_witness', all(value == 0 for value in fine.flat))
                products = polynomial_products(mesh, common)
                mass = sum(contract(moments['fine_mass'], products['mass']), Decimal(0))
                gradient = sum(contract(moments['fine_gradient'], products['gradient']), Decimal(0))
                evidence.check(branch+'_original_weighted_common_action_recovers_erased_witness', mass > 0 and gradient > 0)
                evidence.report['cases'].append(dict(branch=branch, control='erased_basis_265_weighted_witness',
                    weighted_mass=str(mass), weighted_gradient=str(gradient), fine_sampled_mass='0', fine_sampled_gradient='0',
                    shared_polynomial_coefficient_error=str(smooth_error), valid_for_claim=False))
                evidence.save()
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=len(evidence.report['cases']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
