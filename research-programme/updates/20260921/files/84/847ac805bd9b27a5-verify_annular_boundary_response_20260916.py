from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_boundary_response_20260916 import field_matrices, matrix_derivatives, nested_coordinates, split_vector, blocks
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from scipy.linalg import eigh, solve
from scipy.sparse.linalg import spsolve
from scipy.integrate import solve_ivp
import json
import numpy as np


def maximum(matrix):
    return float(np.max(abs(matrix)))


def main():
    evidence = EvidenceRun('annular-boundary-dynamic-response-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        path = intake/'annular-local-refinement-crossing-attempt02/status.json'
        status = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('paired_saved_trajectories_complete', status['state']=='complete' and len(status['cases'])==4)
        for count, splits in [(257, 8), (513, 4)]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                prefix = branch+str(count)
                coarse = QuadraticSourceFittedAction(count, gram, background_mass=0.)
                system = LocallyRefinedSourceAction(count, gram, background_mass=0., source_splits=splits)
                embedding, bubbles, retained, new = nested_coordinates(coarse, system)
                evidence.check(prefix+'_hierarchical_coordinates_exact', maximum(embedding[retained].toarray()-np.eye(coarse.count)) < 3e-12
                               and len(new)==4*(splits-1))
                original_bubble = system.original @ bubbles
                gram_difference = system.lifted @ bubbles + np.outer(system.lifted_hinge, system.jump @ bubbles)
                evidence.check(prefix+'_local_Gram_dependence_is_rank_one', original_bubble.nnz==0 and maximum(gram_difference) < 2e-10)
                path = intake/'annular-local-refinement-crossing-attempt02'/(branch+'-'+str(count)+'.npz')
                evidence.own(path)
                saved = np.load(path)
                rows = []
                errors = dict(action=0., momentum=0., source_covector=0., field_equation=0., source_equation=0., local_equation=0., reconstruction=0.)
                for instant, state in zip(saved['times'], saved['states']):
                    coordinates, rates = np.split(state[:-1], 2)
                    field, field_rate, position, velocity = coordinates[:-1], rates[:-1], coordinates[-1], rates[-1]
                    acceleration = system.acceleration(instant, coordinates, rates)
                    data = system.evaluate(instant, coordinates, rates)
                    matrices = field_matrices(system, position)
                    derivatives = matrix_derivatives(system, position)
                    mass, transport, square, stiffness = [matrices[name] for name in ['mass', 'transport', 'transport_square', 'stiffness']]
                    mass_b, transport_b, square_b, stiffness_b = [derivatives[name] for name in ['mass', 'transport', 'transport_square', 'stiffness']]
                    reconstructed = (field_rate @ (mass @ field_rate)/2 + velocity*field_rate @ (transport @ field)
                                     + velocity**2*field @ (square @ field)/2 - field @ (stiffness @ field)/2 - system.source_mass*np.sqrt(1-velocity**2))
                    momenta = mass @ field_rate + velocity*(transport @ field)
                    current = field_rate @ (transport @ field) + velocity*field @ (square @ field)
                    source_rhs = field_rate @ (mass_b @ field_rate)/2 + velocity*field_rate @ (transport_b @ field)
                    source_rhs += velocity**2*field @ (square_b @ field)/2 - field @ (stiffness_b @ field)/2
                    damping = velocity*(mass_b+transport-transport.T)
                    dynamic_stiffness = stiffness+acceleration[-1]*transport+velocity**2*(transport_b-square)
                    field_residual = mass @ acceleration[:-1]+damping @ field_rate+dynamic_stiffness @ field
                    current_rate = acceleration[:-1] @ (transport @ field)+field_rate @ (transport @ field_rate)
                    current_rate += velocity*field_rate @ (transport_b @ field)+acceleration[-1]*field @ (square @ field)
                    current_rate += 2*velocity*field_rate @ (square @ field)+velocity**2*field @ (square_b @ field)
                    mechanical = system.source_mass*acceleration[-1]/(1-velocity**2)**1.5
                    coarse_field, local_field = split_vector(field, embedding, retained, new)
                    coarse_rate, local_rate = split_vector(field_rate, embedding, retained, new)
                    coarse_accel, local_accel = split_vector(acceleration[:-1], embedding, retained, new)
                    local_mass = (bubbles.T @ mass @ bubbles).toarray()
                    forcing = bubbles.T @ (mass @ (embedding @ coarse_accel)+damping @ field_rate+dynamic_stiffness @ field)
                    derived_accel = solve(local_mass, -forcing, assume_a='pos')
                    errors['action'] = max(errors['action'], abs(float(reconstructed-data['action'])))
                    errors['momentum'] = max(errors['momentum'], maximum(momenta-data['momenta'][:-1]), abs(float(current-data['field_momenta'][-1])))
                    errors['source_covector'] = max(errors['source_covector'], abs(float(source_rhs-system.source_covector(instant, coordinates, rates))))
                    errors['field_equation'] = max(errors['field_equation'], maximum(field_residual))
                    errors['source_equation'] = max(errors['source_equation'], abs(float(mechanical+current_rate-source_rhs)))
                    errors['local_equation'] = max(errors['local_equation'], maximum(derived_accel-local_accel))
                    errors['reconstruction'] = max(errors['reconstruction'], maximum(embedding @ coarse_field+bubbles @ local_field-field))
                    denominator = float(system.lifted_hinge @ (matrices['gram_weights']*system.lifted_hinge))
                    value = system.original @ field
                    jump_star = float(system.lifted_hinge @ (matrices['gram_weights']*value)/denominator) if denominator>0 else None
                    rows.append(dict(time=float(instant), actual_jump=float(system.jump @ field), coarse_jump=float(coarse.jump @ coarse_field),
                                     local_jump=float(system.jump @ (bubbles @ local_field)), static_Gram_jump=jump_star,
                                     local_mode_norm=float(np.linalg.norm(local_field)), source_field_current=float(current),
                                     source_field_current_rate=float(current_rate), mechanical_force=float(mechanical)))
                for key, tolerance in dict(action=2e-12, momentum=2e-12, source_covector=2e-10, field_equation=2e-10,
                                           source_equation=2e-10, local_equation=2e-7, reconstruction=2e-14).items():
                    evidence.check(prefix+'_'+key, errors[key]<tolerance, errors[key])
                evidence.report['cases'].append(dict(branch=branch, count=count, source_splits=splits,
                                                     local_modes=len(new), errors=errors, trajectory=rows))
                evidence.save()
        evidence.report['frozen_controls'] = []
        for count, splits in [(33, 2), (65, 4), (257, 8), (513, 4)]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                prefix = branch+str(count)+'frozen'
                coarse = QuadraticSourceFittedAction(count, gram, background_mass=0.)
                system = LocallyRefinedSourceAction(count, gram, background_mass=0., source_splits=splits)
                embedding, bubbles, retained, new = nested_coordinates(coarse, system)
                matrices = field_matrices(system, system.anchor)
                mass, stiffness = [blocks(matrices[name], embedding, bubbles) for name in ['mass', 'stiffness']]
                values, modes = eigh(stiffness['local'], mass['local'])
                frequencies = np.sqrt(values)
                evidence.check(prefix+'_positive_local_spectrum', values.min()>0)
                identity_error = maximum(modes.T @ mass['local'] @ modes-np.eye(len(new)))
                evidence.check(prefix+'_mass_normalized_modes', identity_error < 2e-11, identity_error)
                coarse_vector = np.sin(np.arange(coarse.count)*.31)*.001
                frequency_rows = []
                for scale in [0., .1, 1., 3.]:
                    spectral = (0.17+1j)*scale*frequencies[0]
                    fine_operator = matrices['stiffness']+spectral**2*matrices['mass']
                    local_operator = stiffness['local']+spectral**2*mass['local']
                    coupling = stiffness['coupling']+spectral**2*mass['coupling']
                    local = solve(local_operator, -coupling @ coarse_vector)
                    full = embedding @ coarse_vector+bubbles @ local
                    residual = fine_operator @ full
                    recovered = spsolve(fine_operator.tocsc(), residual)
                    error = maximum(recovered-full)
                    local_residual = maximum(bubbles.T @ residual)/max(1., maximum(residual))
                    evidence.check(prefix+'_resolvent_'+str(scale), error < 2e-9 and local_residual < 2e-11,
                                   dict(full_solve_error=error, local_equation_relative_residual=local_residual))
                    static = solve(stiffness['local'], -stiffness['coupling'] @ coarse_vector, assume_a='pos')
                    frequency_rows.append(dict(scale=scale, dynamic_jump_abs=float(abs(system.jump @ full)),
                                               static_local_relative_error=float(np.linalg.norm(static-local)/max(1e-30, np.linalg.norm(local)))))
                forcing_frequency = .3*frequencies[0]
                forcing = -(stiffness['coupling']-forcing_frequency**2*mass['coupling']) @ coarse_vector
                modal_forcing = modes.T @ forcing
                duration = 4/frequencies[0]
                times = np.linspace(0., duration, 25)
                analytic = np.array([modes @ (modal_forcing*(np.cos(forcing_frequency*instant)-np.cos(frequencies*instant))/(values-forcing_frequency**2)) for instant in times])
                def flow(instant, state):
                    position, velocity = np.split(state, 2)
                    return np.concatenate([velocity, solve(mass['local'], forcing*np.cos(forcing_frequency*instant)-stiffness['local'] @ position, assume_a='pos')])
                solution = solve_ivp(flow, (0., duration), np.zeros(2*len(new)), t_eval=times, method='DOP853',
                                     rtol=2e-11, atol=2e-13, max_step=.2/frequencies[-1])
                error = maximum(solution.y[:len(new)].T-analytic)
                evidence.check(prefix+'_retarded_solution_with_initial_term', solution.success and error < 2e-10, error)
                no_initial_term = np.array([modes @ (modal_forcing*np.cos(forcing_frequency*instant)/(values-forcing_frequency**2)) for instant in times])
                evidence.report['frozen_controls'].append(dict(branch=branch, count=count, local_modes=len(new),
                    minimum_frequency=float(frequencies[0]), maximum_frequency=float(frequencies[-1]),
                    retarded_state_error=error, omitted_initial_term_error=maximum(no_initial_term-analytic),
                    frequency_comparisons=frequency_rows, duration=duration, prescribed_source=True))
                evidence.save()
        evidence.report.update(scope='Exact finite moving-source field and source-current decomposition; frozen prescribed-source retarded controls are not a full moving-source reduced solver.',
                               static_trace_constraint_imposed=False, all_original_Gram_rows_retained=True,
                               live_quadratic_geometry_qualified=False, moving_source_reduced_memory_solver_implemented=False,
                               uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
