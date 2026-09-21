import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

from navier_stokes_source_audit_20260908 import limit_process
limit_process()

from annular_reference_continuum_shell_20260914 import EvidenceRun, continuum_initial, initial_case


def run():
    evidence = EvidenceRun('annular-reference-continuum-shell-attempt01',__file__)
    try:
        continuum = continuum_initial()
        evidence.report['continuum_initial_shell'] = continuum[2]
        evidence.report['continuum_initial_mass_minus'] = float(continuum[0].y[0,-1])
        evidence.report['continuum_energy_moments'] = continuum[3].tolist()
        evidence.report['test_scope'] = 'Initial radial constraints and stationary vacuum-adjacent shell only; not an evolving continuum convergence test.'
        for count in [33,65,129,257]:
            case = initial_case(count,12,continuum)
            evidence.report['cases'].append(case)
            evidence.check(str(count)+'_radial_constraints',case['collocation_defect']<1e-11,case['collocation_defect'])
            evidence.check(str(count)+'_regular_chart',case['minimum_F']>.5,case['minimum_F'])
            evidence.check(str(count)+'_physical_midpoint_clock',case['midpoint_clock_error']<1e-13)
            evidence.check(str(count)+'_initial_shell_has_no_scalar_gradient',case['source_scalar_potential']<1e-25)
            evidence.check(str(count)+'_mass_source_not_zero',case['shell_mass_jump']>2e-4)
            evidence.check(str(count)+'_supported_not_pressureless_shell',case['required_surface_pressure']>1e-6)
            print(str(count)+' done',flush=True)
        cases = evidence.report['cases']
        for key in ['bulk_mass_error','bulk_log_lapse_error','weak_energy_moment_error',
                    'shell_U_jump_error','shell_half_U_jump_error','shell_mass_jump_error',
                    'shell_lapse_jump','shell_lapse_prediction_error','outer_clock_prediction_error',
                    'surface_density_error','surface_pressure_error']:
            values = [case[key] for case in cases]
            evidence.check(key+'_refines',all(later<earlier for earlier,later in zip(values,values[1:])),values)
        finest = cases[-1]
        evidence.check('bulk_mass_resolved',finest['bulk_mass_error']<5e-5,finest['bulk_mass_error'])
        evidence.check('bulk_lapse_resolved',finest['bulk_log_lapse_error']<5e-5,finest['bulk_log_lapse_error'])
        evidence.check('source_jump_prediction_resolved',finest['shell_mass_jump_error']<1e-7)
        evidence.check('deleting_source_is_not_discretization_error',
                       finest['no_source_mass_error']>100*finest['shell_mass_jump_error'])
        evidence.check('midpoint_not_exterior_mass',
                       finest['midpoint_as_exterior_mass_error']>100*finest['shell_mass_jump_error'])
        evidence.check('outer_clock_not_one',
                       finest['forced_unit_outer_clock_error']>100*finest['outer_clock_prediction_error'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()
