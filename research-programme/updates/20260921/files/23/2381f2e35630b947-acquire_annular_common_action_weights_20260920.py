from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from fractions import Fraction
from time import perf_counter
import contextlib
import json
import numpy as np


def densities(layer, position, reference):
    radius, jacobian, unused = layer.mapping(reference, position)
    coefficient = layer.coefficient(0., radius)
    return jacobian*radius**4/coefficient, coefficient/jacobian


def reference_geometry_cuts(layer, position):
    lower, upper = layer.radii[[0, -1]]
    physical_edges, unused, unused2 = layer.mapping(np.array([lower, upper]), position)
    unused, jacobian, unused2 = layer.mapping(np.array([(lower+layer.anchor)/2, (upper+layer.anchor)/2]), position)
    points = np.asarray(layer.geometry.edges)
    reference = np.where(points < position, lower+(points-physical_edges[0])/jacobian[0],
        upper-(physical_edges[1]-points)/jacobian[1])
    return reference[(reference > lower) & (reference < upper)]


def main():
    evidence = EvidenceRun('annular-common-action-weights-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            frozen_original_geometry_reconstructed=True, all_integration_cuts_retained=True,
            parent_coefficient_precision='saved/reconstructed binary64; high-precision accumulation cannot improve it',
            maximum_wall_seconds=7200)
        for branch in ['reference', 'MTS']:
            saved = checked_load(evidence, 'annular-live-compensated-rate-attempt01', branch+'-1e-07-compensated-rate.npz')
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            pair = evaluate_pair(systems, [saved[str(level)+'_state'] for level in range(2)])
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            edges = np.array([float(Fraction(value)) for value in packet['overlay']['edges']])
            cuts = np.unique(np.concatenate([edges]+[reference_geometry_cuts(item['layer'], item['values'][-1]) for item in pair]))
            evidence.check(branch+'_all_positive_segments', bool(np.all(np.diff(cuts) > 0)))
            evidence.check(branch+'_common_edges_retained', bool(np.all(np.isin(edges, cuts))))
            arrays = dict(common_edges=edges, integration_cuts=cuts)
            rows = []
            for level, (name, item) in enumerate(zip(['coarse', 'fine'], pair)):
                data = checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+name+'-action.npz')
                layer, position = item['layer'], item['values'][-1]
                mass, gradient = densities(layer, position, layer.reference_radius)
                gradient_error = float(np.max(abs(layer.reference_weight*gradient-data['gradient_weights']))
                    /max(1., np.max(abs(data['gradient_weights']))))
                mass_error = float(np.max(abs(item['mass']-data['mass_bands']))/np.max(abs(data['mass_bands'])))
                gram_error = float(np.max(abs(item['weights']-data['gram_weights']), initial=0.)
                    /max(1., np.max(abs(data['gram_weights']), initial=0.)))
                evidence.check(branch+'_'+name+'_original_frozen_action_weights',
                    max(mass_error, gradient_error, gram_error) < 3e-12,
                    dict(mass_relative_error=mass_error, gradient_relative_error=gradient_error, gram_relative_error=gram_error))
                rows.append(dict(branch=branch, level=name, mass_relative_error=mass_error,
                    gradient_relative_error=gradient_error, gram_relative_error=gram_error,
                    geometry_cells=len(layer.geometry.edges)-1, source_position=float(position), valid_for_claim=False))
                arrays[name+'_native_radius'] = layer.reference_radius
                arrays[name+'_native_reference_weight'] = layer.reference_weight
                arrays[name+'_native_mass_density'] = mass
                arrays[name+'_native_gradient_density'] = gradient
                arrays[name+'_source_position'] = np.array(position)
            fine_layer = pair[1]['layer']
            coarse_layer = pair[0]['layer']
            unused, counter_gradient = densities(coarse_layer, pair[0]['values'][-1], fine_layer.radii)
            arrays['fine_gram_weights_at_coarse_geometry'] = np.asarray(fine_layer.sampling @ counter_gradient)/fine_layer.gram_spacing
            output = evidence.output/(branch+'-native-and-cuts.npz')
            np.savez_compressed(output, **arrays)
            evidence.own(output, 'outputs')
            evidence.report['cases'].extend(rows)
            for order in [16, 32, 64]:
                if perf_counter()-started > 7200:
                    raise RuntimeError('Safe saved acquisition boundary reached.')
                nodes, weights = np.polynomial.legendre.leggauss(order)
                fractions, reference_weights = (nodes+1)/2, weights/2
                reference = (cuts[:-1, None]+np.diff(cuts)[:, None]*fractions).ravel()
                result = dict(fractions=fractions, gauss_weights=reference_weights)
                for name, item in zip(['coarse', 'fine'], pair):
                    mass, gradient = densities(item['layer'], item['values'][-1], reference)
                    evidence.check(branch+'_'+name+'_'+str(order)+'_finite_positive_weight_densities',
                        bool(np.all(np.isfinite(mass)) and np.all(np.isfinite(gradient)) and np.all(mass > 0) and np.all(gradient > 0)))
                    result[name+'_mass_density'] = mass.reshape(-1, order)
                    result[name+'_gradient_density'] = gradient.reshape(-1, order)
                output = evidence.output/(branch+'-order'+str(order)+'-densities.npz')
                np.savez_compressed(output, **result)
                evidence.own(output, 'outputs')
                evidence.report['progress'] = dict(branch=branch, order=order, segments=len(cuts)-1,
                    quadrature_nodes=len(reference), seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report['seconds'] = perf_counter()-started
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
