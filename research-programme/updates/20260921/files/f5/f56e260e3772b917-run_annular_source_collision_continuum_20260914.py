import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
from time import perf_counter
import numpy as np
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_reflecting_boundary_20260914 import ReflectingContinuum, boundary_derivative


def run():
    evidence = EvidenceRun('annular-source-collision-continuum-attempt01', __file__)
    try:
        prior = evidence.root/'source-intake/navier-stokes/20260914/annular-reflecting-boundary-attempt01/status.json'
        audit = json.loads(prior.read_text())
        evidence.own(prior)
        evidence.check('boundary_qualified', audit['state'] == 'complete' and audit['energy_boundary_numerically_qualified_on_this_mode'])
        evidence.report.update(scope='Original compact pulse, independent coupled spherical Einstein-scalar with supported fixed source; first collision through t=.45.',
                               arbitrary_nonlinear_boundary_stability_proven=False,
                               time_beyond_analytic_uniform_interval=True,
                               parent_source_support_action_derived=False,
                               flat_energy_identity_is_not_exact_nonlinear_mass_conservation=True)
        times = np.linspace(0., .45, 46)
        records = {}
        for count in [513, 1025, 2049]:
            started = perf_counter()
            system = ReflectingContinuum(count)
            solution = system.integrate(duration=.45)
            states = solution.sol(times).T
            masses, lapses, energies, diagnostics = [], [], [], []
            for time, state in zip(times, states):
                geometry = system.geometry(state)
                scalar, gradient, momentum = system.unpack(state)
                rate = geometry['L']*momentum/system.radii**2
                wall_flux = system.radii[-1]**2*geometry['L'][-1]*gradient[-1]
                wall_power = rate[-1]*wall_flux
                inward = rate+geometry['L']*gradient
                outward = rate-geometry['L']*gradient
                diagnostics.append(dict(time=float(time), mass_plus=float(geometry['mass_plus']),
                    minimum_F=float(geometry['F'].min()), wall_gradient=float(gradient[-1]),
                    wall_force=float(wall_flux), wall_power=float(wall_power),
                    source_pressure=float(geometry['P']), source_density=float(geometry['Sigma']),
                    wall_characteristic_residual=float(inward[-1]+outward[-1]),
                    left_gradient=float(gradient[0]), right_scalar=float(scalar[-1]), right_momentum=float(momentum[-1]),
                    interior_gradient_constraint=float(abs(boundary_derivative(scalar, system.spacing)[4:-4]-gradient[4:-4]).max()),
                    full_gradient_constraint=float(abs(boundary_derivative(scalar, system.spacing)-gradient).max())))
                masses.append(geometry['mass'])
                lapses.append(geometry['log_N'])
                energies.append(geometry['energy'])
            drift = max(abs(row['mass_plus']-diagnostics[0]['mass_plus']) for row in diagnostics)
            case = dict(count=count, seconds=perf_counter()-started, calls=system.calls,
                        mass_drift=drift, peak_wall_force=max(abs(row['wall_force']) for row in diagnostics),
                        minimum_source_pressure=min(row['source_pressure'] for row in diagnostics), diagnostics=diagnostics)
            evidence.report['cases'].append(case)
            path = evidence.output/('continuum_count'+str(count)+'.npz')
            np.savez_compressed(path, times=times, radii=system.radii, states=states,
                                masses=np.array(masses), log_lapses=np.array(lapses), energies=np.array(energies))
            evidence.own(path, 'outputs')
            evidence.check(str(count)+'_regular_active_collision', case['peak_wall_force'] > .1 and min(row['minimum_F'] for row in diagnostics) > .5)
            evidence.check(str(count)+'_no_work_fixed_reflection', all(abs(row[key]) < 1e-13 for row in diagnostics
                for key in ['wall_power', 'wall_characteristic_residual', 'left_gradient', 'right_scalar', 'right_momentum']))
            evidence.check(str(count)+'_mass_drift_gate', drift < 1e-5, drift)
            records[count] = dict(states=states.reshape(len(times), 3, count), masses=np.array(masses), lapses=np.array(lapses))
            evidence.save()
            print({key:value for key,value in case.items() if key != 'diagnostics'}, flush=True)
        differences = []
        for coarse, fine in [(513, 1025), (1025, 2049)]:
            fields = np.max(abs(records[coarse]['states']-records[fine]['states'][:, :, ::2]), axis=(0, 2))
            row = dict(coarse=coarse, fine=fine, field_max_errors=fields.tolist(),
                       mass_max_error=float(abs(records[coarse]['masses']-records[fine]['masses'][:, ::2]).max()),
                       log_lapse_max_error=float(abs(records[coarse]['lapses']-records[fine]['lapses'][:, ::2]).max()))
            differences.append(row)
        evidence.report['refinement'] = differences
        evidence.check('all_three_fields_refine', all(later < earlier for earlier, later in zip(differences[0]['field_max_errors'], differences[1]['field_max_errors'])))
        evidence.check('both_metric_fields_refine', all(differences[1][key] < differences[0][key] for key in ['mass_max_error', 'log_lapse_max_error']))
        evidence.check('mass_drift_refines', all(later['mass_drift'] < earlier['mass_drift'] for earlier, later in zip(evidence.report['cases'], evidence.report['cases'][1:])))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
