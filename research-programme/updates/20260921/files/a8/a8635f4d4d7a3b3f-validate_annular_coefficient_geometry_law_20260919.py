from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
from annular_force_coefficient_bounds_20260919 import off_space_peano
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-coefficient-geometry-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            independent_dense_geometry_and_rate_control=True, nonzero_ordinary_jump_negative_control=True)
        generator = np.random.default_rng(20260919)
        basis = generator.normal(size=(13, 5))
        operator = generator.normal(size=(7, 5))
        sides = np.column_stack([np.arange(13) < 6, np.arange(13) >= 6]).astype(float)
        initial = generator.normal(size=5)
        velocity = generator.normal(size=5)
        kinetic_rates = generator.uniform(-.8, .8, 13)
        gram_rates = generator.uniform(-.5, .5, 7)

        def data(time, targets=sides):
            kinetic = np.exp(time*kinetic_rates)
            weights = np.exp(time*gram_rates)
            mass = basis.T @ (kinetic[:, None]*basis)
            load = basis.T @ (kinetic[:, None]*targets)
            response = np.linalg.solve(mass, load)
            field = initial+time*velocity
            factor = operator @ field
            covector = operator.T @ (weights*factor)
            dual = np.linalg.solve(mass, covector)
            return kinetic, weights, mass, response, factor, covector, dual

        for time in [0., .2, .7]:
            kinetic, weights, mass, response, factor, covector, dual = data(time)
            defects = sides-basis @ response
            derivative_load = basis.T @ ((kinetic*kinetic_rates)[:, None]*sides)
            derivative_mass = basis.T @ ((kinetic*kinetic_rates)[:, None]*basis)
            derivative_response = np.linalg.solve(mass, derivative_load-derivative_mass @ response)
            residual_response = np.linalg.solve(mass, basis.T @ ((kinetic*kinetic_rates)[:, None]*defects))
            evidence.check(str(time)+'_mass_derivative_defect_identity', np.max(abs(derivative_response-residual_response)) < 3e-13)
            projected = operator @ response
            field_terms = (weights*(operator @ velocity))[:, None]*projected
            mass_terms = (kinetic*kinetic_rates*(basis @ dual))[:, None]*defects
            weight_terms = (weights*gram_rates*factor)[:, None]*projected
            rate = np.sum(field_terms, axis=0)+np.sum(mass_terms, axis=0)+np.sum(weight_terms, axis=0)
            independent = derivative_response.T @ covector+response.T @ operator.T @ (
                weights*(operator @ velocity)+weights*gram_rates*factor)
            evidence.check(str(time)+'_coefficient_rate_identity', max(abs(rate-independent)) < 3e-12)
            bound = (np.sum(abs(field_terms), axis=0)
                +max(abs(kinetic_rates))*np.sqrt(covector @ dual)*np.sqrt(np.sum(kinetic[:, None]*defects**2, axis=0))
                +max(abs(gram_rates))*np.sqrt(np.sum(weights*factor**2))*np.sqrt(np.sum(weights[:, None]*projected**2, axis=0)))
            evidence.check(str(time)+'_conditional_rate_bound', np.all(abs(rate) <= bound+3e-12))
            errors = []
            for step in [.002, .001, .0005, .00025]:
                before, after = data(time-step), data(time+step)
                finite_rate = (after[3].T @ after[5]-before[3].T @ before[5])/(2*step)
                errors.append(float(max(abs(finite_rate-rate))))
            evidence.check(str(time)+'_independent_difference_convergence', errors[-1] < errors[0]/40 and errors[-1] < 3e-6, errors)
            evidence.check(str(time)+'_omitting_geometry_is_detected', max(abs(rate-np.sum(field_terms, axis=0))) > 1e-4)
            evidence.report['cases'].append(dict(time=time, coefficient_rate_left=float(rate[0]), coefficient_rate_right=float(rate[1]),
                bound_left=float(bound[0]), bound_right=float(bound[1]), finest_difference_error=errors[-1], valid_for_claim=False))
        targets = basis @ generator.normal(size=(5, 2))
        kinetic, unused, mass, response, unused, unused, unused = data(.2, targets)
        response_rate = np.linalg.solve(mass, basis.T @ ((kinetic*kinetic_rates)[:, None]*(targets-basis @ response)))
        evidence.check('representable_targets_have_zero_geometry_response', max(abs(response_rate).ravel()) < 3e-13)
        first, last = data(.1), data(.3)
        defects = sides-basis @ first[3]
        residual = basis.T @ ((last[0]-first[0])[:, None]*defects)
        correction = np.linalg.solve(last[2], residual)
        evidence.check('finite_geometry_response_identity', max(abs(last[3]-first[3]-correction).ravel()) < 3e-13)
        for side in range(2):
            actual = float(last[5] @ (last[3][:, side]-first[3][:, side]))
            quadrature = (last[0]-first[0])*(basis @ last[6])*defects[:, side]
            bound = np.sqrt(last[5] @ last[6])*np.sqrt(np.sum(((last[0]-first[0])**2/last[0])*defects[:, side]**2))
            evidence.check('finite_geometry_side'+str(side)+'_pairing_and_bounds', abs(actual-np.sum(quadrature)) < 3e-12
                and abs(actual) <= np.sum(abs(quadrature))+3e-12 and abs(actual) <= bound+3e-12)
        coarse = GradedSourceAction(65, True, source_cap=4e-5)
        fine = GradedSourceAction(129, True, source_cap=2e-5)
        knot = coarse.edges[np.searchsorted(coarse.edges, coarse.anchor+.15)]
        values = .3*(coarse.radii-coarse.anchor)+.2*(coarse.radii-coarse.anchor)**2+.7*np.maximum(coarse.radii-knot, 0.)
        split = off_space_peano(fine, coarse, values)
        residual = abs(split['actual']-split['regular']-split['ordinary_jumps']-split['polynomial_moments'])
        evidence.check('independent_nonnested_Peano_reconstruction', np.all(residual <= split['tolerance']),
            dict(error=float(max(residual)), tolerance=float(max(split['tolerance']))))
        evidence.check('discarding_ordinary_jumps_fails', max(abs(split['ordinary_jumps'])) > 1e-3)
        evidence.check('source_knot_and_ordinary_knot_distinct', knot != coarse.anchor)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
