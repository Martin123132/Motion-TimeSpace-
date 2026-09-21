import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_dynamical_source_20260914 import outgoing_profile


def run():
    evidence = EvidenceRun('annular-flat-bulk-energy-attempt01', __file__)
    try:
        prior = evidence.output.parent/'annular-exact-flat-recoil-attempt02/status.json'
        previous = json.loads(prior.read_text())
        evidence.own(prior)
        evidence.check('recoil_control_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        evidence.report.update(scope='Independent null-coordinate reconstruction and direct integral of the spherical scalar stress energy; flat space only, before centre return.',
                               coupled_moving_GR_scalar_PDE_tested=False,
                               scalar_energy_not_inferred_from_shell_energy=True,
                               quadrature_is_not_a_numerical_PDE_evolution=True)
        reservoir = .003
        for amplitude in [.005, .01, .02]:
            def null_rhs(retarded, state):
                derivative = float(outgoing_profile(retarded, amplitude)[1])
                return [2*derivative**2/reservoir, state[0]**2]
            solution = solve_ivp(null_rhs, (-6., -5.2), [1., 6.], method='DOP853',
                                 dense_output=True, rtol=2e-12, atol=2e-14, max_step=.0005)
            evidence.check(str(amplitude)+'_null_reconstruction_finished', solution.success)
            final_factor, final_advanced = solution.y[:, -1]
            final_time = (-5.2+final_advanced)/2
            total_incident = quad(lambda retarded: float(outgoing_profile(retarded, amplitude)[1])**2,
                                  -5.8, -5.2, epsabs=2e-14, epsrel=2e-12)[0]
            old_case = next(row for row in previous['cases'] if row['amplitude'] == amplitude)
            evidence.check(str(amplitude)+'_independent_null_ODE_matches_time_ODE',
                           abs(final_time-old_case['final_time']) < 2e-10 and
                           abs((final_factor**2-1)/(final_factor**2+1)-old_case['final_speed']) < 2e-10)

            def reflected(advanced):
                if advanced <= 6.2 or advanced >= final_advanced:
                    return 0., 0.
                emission = brentq(lambda retarded: float(solution.sol(retarded)[1])-advanced,
                                 -5.8, -5.2, xtol=5e-15)
                factor = solution.sol(emission)[0]
                value, derivative = outgoing_profile(emission, amplitude)
                return -float(value), -float(derivative)/factor**2

            for fraction in [0., .25, .5, .75, 1.]:
                time = fraction*final_time
                shell_retarded = brentq(lambda retarded: (retarded+solution.sol(retarded)[1])/2-time,
                                       -6., -5.2, xtol=5e-15) if 0 < fraction < 1 else [-6., -5.2][int(fraction)]
                factor, shell_advanced = solution.sol(shell_retarded)
                radius = (shell_advanced-shell_retarded)/2
                incident_value, incident_rate = outgoing_profile(shell_retarded, amplitude)
                reflected_value, reflected_rate = reflected(time+radius)
                boundary_defect = abs(float(incident_value)+reflected_value)
                evidence.check(str(amplitude)+'_'+str(fraction)+'_reconstructed_Dirichlet_boundary', boundary_defect < 2e-11)

                def energy_density(position):
                    if position < 1e-14:
                        return 0.
                    incident, incident_derivative = outgoing_profile(time-position, amplitude)
                    returning, returning_derivative = reflected(time+position)
                    scalar_time = (float(incident_derivative)+returning_derivative)/position
                    scalar_radial = (-float(incident_derivative)+returning_derivative)/position-(float(incident)+returning)/position**2
                    return position**2*(scalar_time**2+scalar_radial**2)/2

                split = sorted(set(value for value in [time+5.2, time+5.8, 6.2-time, final_advanced-time] if 0 < value < radius))
                field_energy, quadrature_error = quad(energy_density, 0., radius, points=split,
                                                     epsabs=2e-12, epsrel=2e-10, limit=250)
                shell_energy = reservoir*(factor+1/factor)/2
                defect = field_energy+shell_energy-reservoir-total_incident
                evidence.check(str(amplitude)+'_'+str(fraction)+'_direct_bulk_plus_shell_energy',
                               abs(defect) < 2e-10 and quadrature_error < 2e-10,
                               dict(defect=float(defect), quadrature_estimate=float(quadrature_error)))
                evidence.report['cases'].append(dict(amplitude=amplitude, time=float(time), radius=float(radius),
                                                      reconstructed_field_energy=float(field_energy),
                                                      shell_energy=float(shell_energy), total_initial_energy=float(reservoir+total_incident),
                                                      boundary_value_defect=float(boundary_defect), energy_defect=float(defect)))
                evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
