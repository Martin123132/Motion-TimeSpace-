import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import numpy as np
import sympy as sym
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_moving_wave_20260914 import MovingWave


def run():
    evidence = EvidenceRun('annular-moving-wave-algebra-attempt01', __file__)
    try:
        evidence.report.update(scope='Moving-coordinate characteristic system and SBP/SAT flat combined energy identity; not a nonlinear curved-space stability theorem.',
                               coupled_moving_GR_scalar_PDE_tested=False)
        beta, rate, outgoing, incoming, radius = sym.symbols('beta w outgoing incoming radius', real=True)
        reflection = (beta-rate)/(beta+rate)
        boundary_energy = -(beta-rate)*outgoing**2/4+(beta+rate)*incoming**2/4
        penalty_work = -(beta+rate)*incoming*(incoming+reflection*outgoing)/2
        dissipation = (beta+rate)*(incoming+reflection*outgoing)**2/4
        mechanical_work = rate*(beta-rate)*outgoing**2/(2*(beta+rate))
        evidence.check('right_SAT_flux_exact_completed_square', sym.factor(boundary_energy+penalty_work+dissipation+mechanical_work)==0)
        geometry = beta**2-rate**2
        normal_from_characteristic = -(beta-rate)*outgoing/radius
        projected_radial = -outgoing/(1+rate/beta)
        evidence.check('projected_normal_trace_exact', sym.factor(normal_from_characteristic-geometry*projected_radial/(beta*radius))==0)
        speed, length, derivative_speed = sym.symbols('L H L_R', positive=True)
        derivative_a, derivative_b = sym.symbols('a_x b_x')
        advection_a = -((speed-rate)*derivative_a+(speed-rate)*derivative_a+(length*derivative_speed-rate)*outgoing)/ (2*length)
        advection_a -= (derivative_speed+rate/length)*outgoing/2
        evidence.check('split_outgoing_consistency', sym.factor(advection_a+(speed-rate)*derivative_a/length+derivative_speed*outgoing)==0)
        advection_b = ((speed+rate)*derivative_b+(speed+rate)*derivative_b+(length*derivative_speed+rate)*incoming)/(2*length)
        advection_b += (derivative_speed-rate/length)*incoming/2
        evidence.check('split_incoming_consistency', sym.factor(advection_b-(speed+rate)*derivative_b/length-derivative_speed*incoming)==0)
        random = np.random.default_rng(2026091420)
        largest_defect = 0.
        wrong_defects = []
        for count in [33,65,129]:
            system = MovingWave(count)
            for proper_rate in [-.4, 0., .7, 1.5]:
                state = system.initial_state.copy()
                state[:2*count] = .1*random.normal(size=2*count)
                state[-4] = proper_rate
                data = system.geometry(state)
                vector = system.rhs(0., state)
                outgoing_values,incoming_values,source = system.unpack(state)
                out_rate,in_rate,source_rate = system.unpack(vector)
                energy_rate = proper_rate*(system.weights @ data['density'])
                energy_rate += data['length']/2*(system.weights @ (outgoing_values*out_rate+incoming_values*in_rate))
                energy_rate += data['reservoir']*proper_rate*source_rate[1]/np.sqrt(1+proper_rate**2)+source_rate[3]
                largest_defect = max(largest_defect,abs(energy_rate))
                evidence.check(str(count)+'_'+str(proper_rate)+'_flat_energy_including_SAT_loss', abs(energy_rate)<2e-14, float(energy_rate))
                wrong = system.rhs(0.,state,frozen_reflection=True)
                out_bad,in_bad,source_bad = system.unpack(wrong)
                wrong_energy = proper_rate*(system.weights @ data['density'])
                wrong_energy += data['length']/2*(system.weights @ (outgoing_values*out_bad+incoming_values*in_bad))
                wrong_energy += data['reservoir']*proper_rate*source_bad[1]/np.sqrt(1+proper_rate**2)+source_bad[3]
                if proper_rate != 0:
                    wrong_defects.append(abs(wrong_energy))
        evidence.check('frozen_reflection_negative_control_detected', max(wrong_defects)>1e-4, float(max(wrong_defects)))
        evidence.report['maximum_arbitrary_grid_energy_identity_defect']=largest_defect
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()

