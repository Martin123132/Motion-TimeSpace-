from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
from annular_moving_collar_sparse_20260914 import sparse_factors
from fractions import Fraction
import contextlib
import json
import numpy as np


def front_profile(position, time, speed, velocity, forcing):
    position = np.asarray(position)
    crossing = np.where(position < 0, -position/(speed+velocity), position/(speed-velocity))
    remaining = np.maximum(time-crossing, 0.)
    return forcing*(time**2-remaining**2)/2


def main():
    evidence = EvidenceRun('annular-P2-unresolved-front-Gram-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_live_evolution=True,
            constant_coefficient_local_fixture_not_parent_solution=True,
            no_force_or_initial_data_replacement=True, energy_limit_not_force_limit=True)
        fixtures = []
        speed, velocity, forcing, time = .77, .03, 1., 4e-5
        analytic_jump = forcing*time*(1/(speed-velocity)+1/(speed+velocity))
        gradient_energy = forcing**2*time**3*(1/(speed-velocity)+1/(speed+velocity))/6
        points, weights = np.polynomial.legendre.leggauss(8)
        integrated = 0.
        for characteristic_speed in [speed-velocity, speed+velocity]:
            length = characteristic_speed*time
            radius = length*(points+1)/2
            gradient = forcing*(time-radius/characteristic_speed)/characteristic_speed
            integrated += length*np.dot(weights, gradient**2)/4
        evidence.check('continuum_front_gradient_energy_integral', abs(integrated-gradient_energy) < 2e-14*gradient_energy)
        for count, cap in [(257, 2e-5), (513, 1e-5)]:
            layer = GradedSourceAction(count, True, source_cap=cap)
            source = int(np.searchsorted(layer.edges, layer.anchor))
            local_lengths = np.diff(layer.edges)[source-1:source+1]
            source_cell = int(np.searchsorted(layer.base_radii, layer.anchor))
            vertex_distances = np.array([layer.anchor-layer.base_radii[source_cell-1],
                layer.base_radii[source_cell]-layer.anchor])
            front_lengths = np.array([speed+velocity, speed-velocity])*time
            exact_edges = [Fraction.from_float(float(value)) for value in layer.edges]
            exact_anchor = Fraction.from_float(float(layer.anchor))
            natural_nodes = sorted(exact_edges+[(lower+upper)/2 for lower, upper in zip(exact_edges[:-1], exact_edges[1:])])
            offsets = np.array([float(value-exact_anchor) for value in natural_nodes if value != exact_anchor])
            values = front_profile(offsets, time, speed, velocity, forcing)
            jump = float(layer.jump @ values)
            factors = layer.lifted @ values
            energy = float(factors @ factors/(2*layer.gram_spacing))
            coefficient = float(layer.lifted_hinge @ layer.lifted_hinge/layer.gram_spacing)
            predicted = coefficient*analytic_jump**2/2
            original = layer.original @ values
            evidence.check(str(count)+'_resolved_source_but_unresolved_base_front',
                np.all(local_lengths < front_lengths) and np.all(front_lengths < vertex_distances))
            evidence.check(str(count)+'_exact_quadratic_source_jump', abs(jump-analytic_jump) < 2e-15)
            evidence.check(str(count)+'_base_vertices_only_see_common_plateau', np.max(abs(original)) < 2e-20)
            evidence.check(str(count)+'_unresolved_front_energy_identity',
                abs(energy-predicted) < 2e-12*predicted)
            fixtures.append(dict(base_count=count, source_cap=cap, bulk_spacing=layer.gram_spacing,
                source_lengths=local_lengths.tolist(), front_lengths=front_lengths.tolist(),
                nearest_base_vertex_distances=vertex_distances.tolist(),
                actual_energy=energy, predicted_energy=predicted,
                continuum_response_gradient_energy=gradient_energy,
                Gram_to_response_gradient_energy_ratio=energy/gradient_energy,
                analytic_jump=analytic_jump, measured_jump=jump, valid_for_claim=False))
        count, phase = 257, .6
        all_factors, unused = sparse_factors(count, True)
        original = all_factors[count-1:].tocsr()
        sweep = []
        for front_per_cell in [1/64, 1/16, 1/4, 1., 4., 16., 64.]:
            spacing = 1/front_per_cell
            positions = (np.arange(count)-128-phase)*spacing
            values = front_profile(positions, 1., 1., 0., 1.)
            hinge = np.maximum(positions, 0.)
            factor = original @ values-2*(original @ hinge)
            energy = float(factor @ factor/(2*spacing))
            jump_penalty = float((original @ hinge) @ (original @ hinge)/spacing)
            unresolved_prediction = 2*jump_penalty
            if front_per_cell < min(phase, 1-phase):
                evidence.check('uniform_unresolved_'+str(front_per_cell),
                    abs(energy-unresolved_prediction) < 2e-11*unresolved_prediction)
            sweep.append(dict(front_per_bulk_cell=front_per_cell, spacing=spacing,
                Gram_energy=energy, energy_over_h_cubed=energy/spacing**3,
                unresolved_prediction=unresolved_prediction))
        evidence.check('resolved_front_fixture_energy_decreases',
            sweep[-1]['Gram_energy'] < sweep[-2]['Gram_energy'] < sweep[-3]['Gram_energy'])
        evidence.report.update(cases=fixtures, local_fixture_coefficients=dict(speed=speed, velocity=velocity,
            forcing=forcing, time=time, coefficients_not_fitted_to_live_results=True),
            constant_phase_resolved_sweep=sweep, refinement_sweep_phase=phase,
            continuum_gradient_energy_not_total_coupled_energy=True,
            full_live_force_convergence_not_tested=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), fixtures=fixtures, sweep=sweep)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
