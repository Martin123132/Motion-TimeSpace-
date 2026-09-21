from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_boundary_response_20260916 import field_matrices, nested_coordinates, blocks, split_vector
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from scipy.linalg import eigh, solve
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-trace-susceptibility-attempt02', __file__)
    try:
        stiffness_symbol, susceptibility, free_jump = sp.symbols('D chi delta0', positive=True)
        result = free_jump/(1+stiffness_symbol*susceptibility)
        evidence.check('rank_one_feedback_algebra', sp.simplify(result-free_jump+stiffness_symbol*susceptibility*result)==0)
        evidence.check('static_attenuation_is_between_zero_and_one', sp.ask(sp.Q.positive(1/(1+stiffness_symbol*susceptibility)))
                       and sp.ask(sp.Q.positive(sp.factor(1-1/(1+stiffness_symbol*susceptibility)))))
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for count, splits in [(257, 8), (513, 4)]:
            coarse = QuadraticSourceFittedAction(count, True, background_mass=0.)
            system = LocallyRefinedSourceAction(count, True, background_mass=0., source_splits=splits)
            embedding, bubbles, retained, new = nested_coordinates(coarse, system)
            path = intake/'annular-local-refinement-crossing-attempt02'/('MTS-'+str(count)+'.npz')
            evidence.own(path)
            saved = np.load(path)
            for index in [1, 4, 8]:
                instant, state = float(saved['times'][index]), saved['states'][index]
                coordinates, rates = np.split(state[:-1], 2)
                coarse_field, actual_local = split_vector(coordinates[:-1], embedding, retained, new)
                matrices = field_matrices(system, coordinates[-1])
                mass, bulk, full = [blocks(matrices[name], embedding, bubbles) for name in ['mass', 'bulk', 'stiffness']]
                hinge, weight = system.lifted_hinge, matrices['gram_weights']
                denominator = float(hinge @ (weight*hinge))
                jump_local = np.asarray(system.jump @ bubbles).ravel()
                target = np.asarray((system.original @ embedding).T @ (weight*hinge)).ravel()/denominator
                mismatch_map = np.asarray(system.jump @ embedding).ravel()-target
                stiffness_error = float(np.max(abs(full['local']-bulk['local']-denominator*np.outer(jump_local, jump_local))))
                coupling_error = float(np.max(abs(full['coupling']-bulk['coupling']-denominator*np.outer(jump_local, mismatch_map))))
                prefix = str(count)+'t'+str(instant)
                evidence.check(prefix+'_exact_rank_one_local_and_cross_stiffness', stiffness_error < 2e-7 and coupling_error < 2e-7,
                               dict(stiffness_absolute=stiffness_error, coupling_absolute=coupling_error))
                eigenvalues, modes = eigh(bulk['local'], mass['local'])
                residues = (modes.T @ jump_local)**2
                evidence.check(prefix+'_nonnegative_residues_and_positive_free_spectrum', bool(np.min(residues)>=0 and np.min(eigenvalues)>0))
                frequency_rows = []
                for scale in [0., .1, 1., 10.]:
                    spectral = scale*np.sqrt(eigenvalues[0])*(.17+1j)
                    free_operator = bulk['local']+spectral**2*mass['local']
                    free_coupling = bulk['coupling']+spectral**2*mass['coupling']
                    free_local = solve(free_operator, -free_coupling @ coarse_field)
                    response = solve(free_operator, jump_local)
                    chi = jump_local @ response
                    spectral_chi = np.sum(residues/(spectral**2+eigenvalues))
                    delta_free = mismatch_map @ coarse_field+jump_local @ free_local
                    delta = delta_free/(1+denominator*chi)
                    recovered = free_local-denominator*response*delta
                    direct = solve(full['local']+spectral**2*mass['local'], -(full['coupling']+spectral**2*mass['coupling']) @ coarse_field)
                    error = float(np.max(abs(recovered-direct)))
                    contact_error = float(abs(mismatch_map @ coarse_field+jump_local @ direct-delta))
                    evidence.check(prefix+'_frequency_'+str(scale), error < 2e-10 and contact_error < 2e-8
                                   and abs(spectral_chi-chi) < 2e-10*max(1., abs(chi)),
                                   dict(local_state_error=error, trace_mismatch_error=contact_error))
                    frequency_rows.append(dict(scale=scale, attenuation_real=float(np.real(1/(1+denominator*chi))),
                        attenuation_imag=float(np.imag(1/(1+denominator*chi))), local_state_error=error,
                        trace_mismatch_error=contact_error, frozen_forced_jump_mismatch_abs=float(abs(delta))))
                static_chi = float(jump_local @ solve(bulk['local'], jump_local, assume_a='pos'))
                evidence.report['cases'].append(dict(count=count, source_splits=splits, trajectory_time=instant,
                    fixed_source_position=float(coordinates[-1]), Gram_stiffness=denominator,
                    static_compliance=static_chi, static_attenuation=float(1/(1+denominator*static_chi)),
                    actual_moving_trace_mismatch=float(mismatch_map @ coarse_field+jump_local @ actual_local),
                    no_claim_actual_trajectory_is_static=True, frequency_results=frequency_rows))
                evidence.save()
        evidence.report.update(scope='Exact finite frozen-source rank-one trace feedback from the unchanged action. Full moving-source source-current and initial-state terms are still required.',
            fitted_response_coefficients=False, original_Gram_terms_retained=True,
            moving_source_force_problem_solved=False, static_constraint_applied_to_saved_runs=False,
            continuum_or_parent_GR_limit_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
