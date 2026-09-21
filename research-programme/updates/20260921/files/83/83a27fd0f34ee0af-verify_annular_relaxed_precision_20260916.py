from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_relaxed_trace_action_20260916 import RelaxedTraceSourceAction, relaxed_shape_force, relaxed_spectral_step
from run_annular_relaxed_branch_smoke_20260916 import integrate_interval
from run_annular_source_fitted_crossing_20260915 import initial, diagnostics
from annular_boundary_response_20260916 import field_matrices
from scipy.sparse import coo_matrix
import warnings
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-relaxed-precision-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-relaxed-branch-smoke-attempt01'
        path = folder/'status.json'
        status = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('paired_smoke_complete', status['state']=='complete' and len(status['cases'])==4 and all(row['passed'] for row in status['checks']))
        for gram in [False, True]:
            branch = 'relaxed_MTS' if gram else 'reference'
            system = RelaxedTraceSourceAction(129, gram, background_mass=0.)
            path = folder/(branch+'-129.npz')
            evidence.own(path)
            saved = np.load(path)
            initial_state = initial(system)
            spectrum = relaxed_spectral_step(system, initial_state)
            tight, evaluations = integrate_interval(system, initial_state, 0., .05, spectrum['maximum_step'], tight=True)
            control = np.array([initial_state, tight])
            times = np.array([0., .05])
            destination = evidence.output/(branch+'-129-tight-first-eighth.npz')
            np.savez_compressed(destination, times=times, states=control)
            evidence.own(destination, 'outputs')
            difference = float(np.max(abs(control-saved['states'][:2])))
            evidence.check(branch+'_tight_temporal_state', difference<2e-8, difference)
            tight_forces = [relaxed_shape_force(system, instant, *np.split(state[:-1], 2))['canonical_force'] for instant, state in zip(times, control)]
            old_row = next(row for row in status['cases'] if row['base_count']==129 and row['branch']==branch)
            force_difference = float(max(abs(np.array(tight_forces)-old_row['forces'][:2])))
            evidence.check(branch+'_tight_temporal_force', force_difference<2e-8, force_difference)
            data = diagnostics(system, times, control)
            evidence.check(branch+'_tight_energy_and_EL', data['energy_relative_drift']<2e-8 and data['maximum_euler_residual']<2e-10)
            evidence.report['cases'].append(dict(branch=branch, count=129, duration=.05, rtol=2e-12, atol=2e-14,
                maximum_step=spectrum['maximum_step']/2, state_difference=difference, force_difference=force_difference,
                rhs_evaluations=evaluations, full_duration_temporal_control=False))
            evidence.save()
        evidence.report['coefficient_type_controls'] = []
        for background in [0., .7]:
            for gram in [False, True]:
                system = RelaxedTraceSourceAction(65, gram, background_mass=background)
                branch = 'relaxed_MTS' if gram else 'reference'
                coordinates, rates = np.split(initial(system)[:-1], 2)
                data = system.evaluate(0., coordinates, rates)
                original_coefficient = system.coefficient
                probe = lambda radius: .3+np.sin(2.7*np.asarray(radius))
                expected = np.dot(data['weight']*data['density_dual'], data['coefficient']*probe(data['radius']))
                nodes = system.mapping(system.radii, coordinates[-1])[0]
                expected += np.dot(data['nodal_dual'], data['nodal']*probe(nodes))
                try:
                    system.coefficient = lambda instant, radius: original_coefficient(instant, radius)*(1+1e-24j*probe(radius))
                    with warnings.catch_warnings():
                        warnings.simplefilter('error', np.exceptions.ComplexWarning)
                        perturbed = system.evaluate(0j, coordinates.astype(complex), rates.astype(complex))
                        independent_mass = field_matrices(system, complex(coordinates[-1]))['mass']
                finally:
                    system.coefficient = original_coefficient
                rows, columns, values = [], [], []
                for band in range(5):
                    for column in range(system.count):
                        row = column+band-2
                        if 0<=row<system.count:
                            rows.append(row)
                            columns.append(column)
                            values.append(perturbed['mass_bands'][band, column])
                assembled = coo_matrix((values, (rows, columns)), shape=(system.count, system.count)).tocsr()
                mass_error = float(np.max(abs((assembled-independent_mass).imag.toarray()/1e-24)))
                prefix = branch+str(background)
                evidence.check(prefix+'_complex_coefficient_control_no_casting_loss', np.iscomplexobj(perturbed['mass_bands']))
                evidence.check(prefix+'_action_coefficient_dual_with_explicit_complex_dtype', abs(perturbed['action'].imag/1e-24-expected)<2e-12)
                evidence.check(prefix+'_independent_kinetic_coefficient_derivative', mass_error<2e-10, mass_error)
                evidence.report['coefficient_type_controls'].append(dict(branch=branch, background_mass=background, mass_derivative_error=mass_error))
                evidence.save()
        evidence.report.update(scope='Tighter temporal first-eighth controls plus explicit-complex coefficient Hessian controls. Not a whole-trajectory temporal proof.',
            qualification_warning_explained='The first coefficient probe supplied complex coefficients with real coordinate/rate dtypes: only the unused returned mass bands discarded imaginary parts. The action dual tested there did not use those bands. Explicit-complex controls now validate both action and bands without suppressing that warning.',
            whole_duration_temporal_convergence_proven=False, live_geometry_qualified=False,
            unrelaxed_dynamic_limit_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
