import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_independent_continuum_20260914 import ContinuumEvolution


def run():
    evidence = EvidenceRun('annular-independent-continuum-verification-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        directory = intake/'annular-independent-continuum-attempt01'
        status_path = directory/'status.json'
        evidence.own(status_path)
        main = json.loads(status_path.read_text())
        evidence.check('continuum_main_passed',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        for key in ['gradient_constraint','mass_constraint','lapse_constraint','mass_time_identity']:
            values = [max(row[key] for row in case['diagnostics']) for case in main['cases']]
            evidence.check(key+'_fourth_order_range',values[1]<values[0]/8 and values[2]<values[1]/8,values)
        path = directory/'continuum_count2049.npz'
        evidence.own(path)
        saved = np.load(path,allow_pickle=False)
        system = ContinuumEvolution(2049)
        state = saved['states'][-1]
        scalar,gradient,momentum = system.unpack(state)
        gradient_spline = CubicSpline(system.radii,gradient)
        momentum_spline = CubicSpline(system.radii,momentum)
        def radial(radius,values):
            density = .5*(radius**2*float(gradient_spline(radius))**2+
                          float(momentum_spline(radius))**2/radius**2)
            geometry = 1-2*values[0]/radius
            return [.1*geometry*density,values[0]/(radius**2*geometry)+.1*density/radius]
        result = solve_ivp(radial,(5.,6.),[.8,0.],method='DOP853',rtol=2e-12,atol=1e-14,
                           max_step=.001,dense_output=True)
        evidence.check('adaptive_radial_solution',result.success)
        inner = np.sqrt(1-2*result.y[0,-1]/6)
        outer = inner-.1*.003/6
        normalization = np.log((inner+outer)/2)-result.y[1,-1]
        probes = np.linspace(5.,6.,513)
        actual = system.geometry(state)
        independent = result.sol(probes)
        mass_error = float(abs(independent[0]-CubicSpline(system.radii,actual['mass'])(probes)).max())
        lapse_error = float(abs(independent[1]+normalization-CubicSpline(system.radii,actual['log_N'])(probes)).max())
        evidence.check('independent_adaptive_radial_mass',mass_error<2e-9,mass_error)
        evidence.check('independent_original_logN_equation',lapse_error<2e-9,lapse_error)
        evidence.report['radial_check'] = dict(mass_error=mass_error,log_lapse_error=lapse_error)
        coarse_path = directory/'continuum_count1025.npz'
        evidence.own(coarse_path)
        coarse = np.load(coarse_path)
        temporal_system = ContinuumEvolution(1025)
        rk_state = temporal_system.initial_state.copy()
        step = .0002/8
        for index in range(8):
            time = index*step
            first = temporal_system.rhs(time,rk_state)
            second = temporal_system.rhs(time+step/2,rk_state+step*first/2)
            third = temporal_system.rhs(time+step/2,rk_state+step*second/2)
            fourth = temporal_system.rhs(time+step,rk_state+step*third)
            rk_state += step*(first+2*second+2*third+fourth)/6
        temporal_error = float(abs(rk_state-coarse['states'][1]).max())
        evidence.check('independent_RK4_short_time',temporal_error<2e-10,temporal_error)
        evidence.report['temporal_error'] = temporal_error
        direction = system.rhs(.06,state)
        delta = 2e-6
        mass_rate_fd = (system.geometry(state+delta*direction)['mass']-system.geometry(state-delta*direction)['mass'])/(2*delta)
        flux = .1*actual['F']*actual['L']*momentum*gradient
        good_error = float(abs(mass_rate_fd-flux).max())
        wrong_error = float(abs(mass_rate_fd+flux).max())
        evidence.check('real_direction_mass_flux_check',good_error<2e-8,good_error)
        evidence.check('wrong_mass_flux_sign_detected',wrong_error>100*good_error and wrong_error>1e-5,wrong_error)
        wrong_clock = ContinuumEvolution(2049,clock='outer').geometry(state)
        wrong_source = ContinuumEvolution(2049,reservoir=0.).geometry(state)
        clock_difference = float(abs(wrong_clock['log_N']-actual['log_N']).max())
        source_difference = float(abs(wrong_source['mass_plus']-actual['mass_plus']))
        evidence.check('wrong_outer_clock_detected',clock_difference>1e-5,clock_difference)
        evidence.check('deleted_source_detected',source_difference>2e-4,source_difference)
        evidence.report['negative_controls'] = dict(wrong_clock_log_lapse=clock_difference,
                                                   deleted_source_mass=source_difference,
                                                   wrong_flux_sign=wrong_error)
        vacuum_system = ContinuumEvolution(513)
        vacuum = np.zeros_like(vacuum_system.initial_state)
        fields = vacuum_system.geometry(vacuum)
        exact_lapse = np.log(fields['N_shell'])+.5*np.log(fields['F']/fields['F'][-1])
        evidence.check('vacuum_mass_constant',float(abs(fields['mass']-.8).max())<1e-14)
        evidence.check('vacuum_Schwarzschild_lapse',float(abs(fields['log_N']-exact_lapse).max())<1e-11)
        evidence.check('vacuum_scalar_equilibrium',float(abs(vacuum_system.rhs(0.,vacuum)).max())==0)
        evidence.report['no_new_physical_data_or_fitted_parameters'] = True
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

