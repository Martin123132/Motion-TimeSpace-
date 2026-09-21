import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
from annular_reference_continuum_shell_20260914 import EvidenceRun,continuum_initial
from annular_independent_continuum_20260914 import ContinuumEvolution,derivative


def run():
    evidence = EvidenceRun('annular-independent-continuum-attempt01',__file__)
    try:
        evidence.report['scope'] = 'Independent fourth-order continuum method of lines and radial integrating-factor quadrature; no collar/Gram/reference evolution operators.'
        evidence.report['long_interval_is_diagnostic_not_an_extension_of_proof'] = True
        times = np.array([0.,.0002,.03,.06])
        initial_reference = continuum_initial()
        solutions = {}
        for count in [513,1025,2049]:
            system = ContinuumEvolution(count)
            for degree in range(5):
                coordinate = system.radii-5
                expected = degree*coordinate**(degree-1) if degree else np.zeros_like(coordinate)
                error = float(abs(derivative(coordinate**degree,system.spacing)-expected).max())
                evidence.check(str(count)+'_polynomial_derivative_'+str(degree),error<2e-9,error)
            solution = system.integrate()
            states = solution.sol(times).T
            masses,lapses,energies = [],[],[]
            diagnostics = []
            for time,state in zip(times,states):
                geometry = system.geometry(state)
                masses.append(geometry['mass'])
                lapses.append(geometry['log_N'])
                energies.append(geometry['energy'])
                row = system.diagnostics(time,state)
                diagnostics.append(row)
                label = str(count)+'_'+str(time)
                evidence.check(label+'_regular',row['minimum_F']>.5)
                evidence.check(label+'_boundary_conditions',row['left_flux']<1e-14 and
                               row['right_momentum']<1e-14 and row['midpoint_clock_error']<1e-14)
                evidence.check(label+'_mass_time_identity',row['mass_time_identity']<1e-5,row['mass_time_identity'])
            mass_drift = max(abs(row['mass_plus']-diagnostics[0]['mass_plus']) for row in diagnostics)
            evidence.check(str(count)+'_conserved_mass_drift',mass_drift<2e-6,mass_drift)
            initial_mass_error = float(abs(masses[0]-initial_reference[0].sol(system.radii)[0]).max())
            evidence.check(str(count)+'_independent_initial_IVP',initial_mass_error<2e-6,initial_mass_error)
            path = evidence.output/('continuum_count'+str(count)+'.npz')
            np.savez_compressed(path,times=times,radii=system.radii,states=states,
                                masses=np.array(masses),log_lapses=np.array(lapses),energies=np.array(energies))
            evidence.own(path,'outputs')
            case = dict(count=count,calls=system.calls,mass_drift=mass_drift,
                        initial_mass_error=initial_mass_error,diagnostics=diagnostics)
            evidence.report['cases'].append(case)
            evidence.save()
            solutions[count] = (system,states,np.array(masses),np.array(lapses))
            print(str(count)+' complete; mass drift '+str(mass_drift),flush=True)
        differences = []
        for coarse_count,fine_count in [(513,1025),(1025,2049)]:
            coarse,states_coarse,mass_coarse,lapse_coarse = solutions[coarse_count]
            fine,states_fine,mass_fine,lapse_fine = solutions[fine_count]
            fine_fields = states_fine.reshape(len(times),3,fine_count)[:,:,::2]
            errors = np.max(abs(states_coarse.reshape(len(times),3,coarse_count)-fine_fields),axis=(0,2))
            differences.append(dict(coarse=coarse_count,fine=fine_count,
                                    field_max_errors=errors.tolist(),
                                    mass_max_error=float(abs(mass_coarse-mass_fine[:,::2]).max()),
                                    log_lapse_max_error=float(abs(lapse_coarse-lapse_fine[:,::2]).max())))
        evidence.report['continuum_refinement'] = differences
        evidence.check('continuum_field_refinement',all(second<first for first,second in
                       zip(differences[0]['field_max_errors'],differences[1]['field_max_errors'])))
        evidence.check('continuum_metric_refinement',differences[1]['mass_max_error']<differences[0]['mass_max_error'] and
                       differences[1]['log_lapse_max_error']<differences[0]['log_lapse_max_error'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

