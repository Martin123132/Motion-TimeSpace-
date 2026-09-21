from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_force_coefficient_bounds_20260919 import kinetic_weights, quadrature_values
from annular_Gram_projection_commutator_20260919 import field_extension
from derive_annular_projection_source_trace_v2_20260919 import constant_trace_response
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_saved_impulse_20260919 import own_core
from scipy.linalg import solve_banded
import argparse
import contextlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    options = parser.parse_args()
    own_core(0 if options.branch == 'MTS' else 1)
    evidence = EvidenceRun('annular-live-coefficient-rate-'+options.branch+'-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            branch=options.branch, no_new_evolution=True, all_scalar_modes_retained=True,
            full_global_canonical_direction=True, all_Gram_rows_retained=True,
            symmetric_tangent_probes_not_evolved_states=True, rate_not_a_uniform_time_certificate=True,
            geometry_rates_finite_difference_not_certified_derivatives=True, full_nonlinear_stability_proven=False)
        prerequisite = evidence.output.parent/'annular-coefficient-geometry-algebra-attempt01/status.json'
        checked = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('independent_rate_algebra_complete', checked['state'] == 'complete' and all(row['passed'] for row in checked['checks']))
        unused, state = state_pair(evidence, options.branch, True)
        system = IndexedGradedP2System(513, options.branch == 'MTS', 1e-5)
        center = int(np.argmin(abs(system.labels)))
        rates, geometry = system.solve(*state)
        flow = np.stack([rates, system.forces(state[0], rates, geometry)])
        evidence.check('full_canonical_direction_finite', flow.shape == state.shape and np.all(np.isfinite(flow)))

        def evaluate(snapshot, ready=None):
            current_geometry = ready if ready is not None else system.solve(*snapshot)[1]
            layer = system.layer(system.labels[center], current_geometry)
            coordinates = snapshot[0, center]
            extension = field_extension(layer, system.model, coordinates, coordinates[-1])
            response = constant_trace_response(layer, extension, coordinates[-1])
            return layer, extension, response['response'], kinetic_weights(layer, coordinates[-1])

        layer, base, response, kinetic = evaluate(state, geometry)
        response_factor = np.column_stack([layer.lifted @ response[:, side] for side in range(2)])
        response_values = np.column_stack([quadrature_values(layer, response[:, side]) for side in range(2)])
        sides = np.column_stack([layer.reference_radius < layer.anchor, layer.reference_radius > layer.anchor])
        defects = sides-response_values
        field_rate_factor = layer.lifted @ rates[center, :-1]
        saved = dict(full_state=state, full_canonical_direction=flow, response=response, kinetic_weights=kinetic,
            Gram_weights=base['weights'], field_factors=base['factor'], field_rate_factor=field_rate_factor,
            projection_defects=defects)
        for step in [2e-7, 1e-7, 5e-8, 2.5e-8]:
            unused, before, response_before, kinetic_before = evaluate(state-step*flow)
            unused, after, response_after, kinetic_after = evaluate(state+step*flow)
            kinetic_rate = (kinetic_after-kinetic_before)/(2*step)
            gram_rate = (after['weights']-before['weights'])/(2*step)
            gamma = float(max(abs(kinetic_rate/kinetic)))
            eta = float(np.max(abs(gram_rate/base['weights']), initial=0.))
            for partition in ['all_rows', 'source_straddling', 'remaining']:
                mask = np.ones(len(base['factor']), dtype=bool) if partition == 'all_rows' else base['source_rows']
                if partition == 'remaining':
                    mask = ~mask
                covector = np.asarray(layer.lifted.T @ (mask*base['weights']*base['factor'])).ravel()
                dual = solve_banded((2, 2), base['bands'], covector, check_finite=False)
                dual_values = quadrature_values(layer, dual)
                for side in range(2):
                    field_terms = mask*base['weights']*field_rate_factor*response_factor[:, side]
                    mass_terms = kinetic_rate*dual_values*defects[:, side]
                    weight_terms = mask*gram_rate*base['factor']*response_factor[:, side]
                    field_rate, mass_rate, weight_rate = [float(np.sum(terms)) for terms in [field_terms, mass_terms, weight_terms]]
                    predicted = field_rate+mass_rate+weight_rate
                    first_coefficient = float(np.sum(mask*before['weights']*before['factor']*(layer.lifted @ response_before[:, side])))
                    last_coefficient = float(np.sum(mask*after['weights']*after['factor']*(layer.lifted @ response_after[:, side])))
                    direct = (last_coefficient-first_coefficient)/(2*step)
                    error = abs(predicted-direct)
                    localized_bound = float(np.sum(abs(field_terms))+np.sum(abs(mass_terms))+np.sum(abs(weight_terms)))
                    conditional_bound = (float(np.sum(abs(field_terms)))
                        +gamma*np.sqrt(covector @ dual)*np.sqrt(np.sum(kinetic*defects[:, side]**2))
                        +eta*np.sqrt(np.sum(mask*base['weights']*base['factor']**2))
                            *np.sqrt(np.sum(mask*base['weights']*response_factor[:, side]**2)))
                    tolerance = 3e-5*max(abs(direct), abs(predicted), 1e-8)+3e-9
                    tag = partition+'_'+str(side)+'_'+str(step)
                    evidence.check(tag+'_rate_formula_tangent_control', error <= tolerance,
                        dict(error=error, numerical_control_tolerance=tolerance))
                    evidence.check(tag+'_finite_rate_estimate_bounds', abs(predicted) <= localized_bound+3e-15
                        and abs(predicted) <= conditional_bound+3e-15)
                    evidence.report['cases'].append(dict(partition=partition, side=side, tangent_step=step,
                        coefficient_rate=predicted, direct_directional_rate=direct, rate_comparison_error=error,
                        field_rate=field_rate, mass_response_rate=mass_rate, Gram_weight_rate=weight_rate,
                        localized_rate_bound=localized_bound, conditional_rate_bound=float(conditional_bound),
                        sampled_relative_kinetic_rate=gamma, sampled_relative_Gram_rate=eta,
                        validity_scope='instantaneous_saved_endpoint_with_finite_difference_geometry_rates', valid_for_claim=False))
            saved['kinetic_rate_'+str(step)] = kinetic_rate
            saved['Gram_rate_'+str(step)] = gram_rate
            path = evidence.output/('tangent-'+str(step)+'.npz')
            np.savez_compressed(path, state_before=state-step*flow, state_after=state+step*flow,
                kinetic_before=kinetic_before, kinetic_after=kinetic_after,
                factors_before=before['factor'], factors_after=after['factor'],
                response_before=response_before, response_after=response_after)
            evidence.own(path, 'outputs')
            evidence.save()
            print(json.dumps(dict(branch=options.branch, step=step, total=[row for row in evidence.report['cases']
                if row['tangent_step'] == step and row['partition'] == 'all_rows'])), flush=True)
        path = evidence.output/'endpoint-rate-data.npz'
        np.savez_compressed(path, **saved)
        evidence.own(path, 'outputs')
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), branch=options.branch)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
