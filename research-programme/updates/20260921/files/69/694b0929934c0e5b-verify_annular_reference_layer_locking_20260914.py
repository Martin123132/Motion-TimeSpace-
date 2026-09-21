import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
import sympy as sp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_reference_layer_locking_20260914 import pair_diagnostics


def exact_pair_identity():
    count = 4
    spacing = sp.Rational(1,count)
    weights = [spacing/2]+[spacing]*(count-1)
    def sequence(base):
        return [sp.Rational(base+index,base+index+3) for index in range(count)]
    a_first,a_second = sequence(2),sequence(5)
    c_first,c_second = sequence(7),sequence(11)
    b_first,b_second = sequence(13),sequence(17)
    d_first,d_second = sequence(19),sequence(23)
    q_first,q_second = sequence(29),sequence(31)
    force_first,force_second = sequence(37),sequence(41)
    def evolve(a_value,c_value,b_value,d_value,q_value,force_value):
        divergence = [(force_value[index]-(force_value[index-1] if index else 0))/weights[index] for index in range(count)]
        gradient = [((q_value[index+1] if index+1<count else 0)-q_value[index])/spacing for index in range(count)]
        return ([a_value[index]*divergence[index]+b_value[index]*q_value[index] for index in range(count)],
                [c_value[index]*gradient[index]+d_value[index]*force_value[index] for index in range(count)],
                divergence,gradient)
    first = evolve(a_first,c_first,b_first,d_first,q_first,force_first)
    second = evolve(a_second,c_second,b_second,d_second,q_second,force_second)
    direct,metric,forcing = sp.S.Zero,sp.S.Zero,sp.S.Zero
    for index in range(count):
        dq = q_first[index]-q_second[index]
        df = force_first[index]-force_second[index]
        qa = weights[index]/a_first[index]
        fc = spacing/c_first[index]
        direct += qa*dq*(first[0][index]-second[0][index])+fc*df*(first[1][index]-second[1][index])
        direct -= (qa*b_first[index]*dq**2+fc*d_first[index]*df**2)/2
        metric += (qa*b_first[index]*dq**2+fc*d_first[index]*df**2)/2
        rq = (a_first[index]-a_second[index])*second[2][index]+(b_first[index]-b_second[index])*q_second[index]
        rf = (c_first[index]-c_second[index])*second[3][index]+(d_first[index]-d_second[index])*force_second[index]
        forcing += qa*dq*rq+fc*df*rf
    return sp.factor(direct-metric-forcing),metric


def run():
    evidence = EvidenceRun('annular-reference-layer-locking-independent-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        main_path = intake/'annular-reference-layer-locking-attempt01/status.json'
        main = json.loads(main_path.read_text())
        evidence.own(main_path)
        evidence.check('main_passed',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        residual,metric = exact_pair_identity()
        evidence.check('rational_pair_balance_exact',residual==0,str(residual))
        evidence.check('dropping_live_time_coefficients_fails',metric!=0,str(metric))
        original_path = intake/'annular-reference-layer-locking-attempt01/reference_count33.npz'
        evidence.own(original_path)
        saved = np.load(original_path)
        original_system = CompatibleEvolution(33,False,degree=8)
        refined_system = CompatibleEvolution(33,False,degree=12)
        refined = refined_system.integrate(duration=.0002,divisor=8,rtol=3e-12,atol=3e-14)
        values = refined_system.grid.evaluate(refined_system.grid.coefficients(refined_system.unpack(refined.y[:,-1])[0]),
                                             original_system.grid.offsets)
        packed = original_system.pack(values,refined.y[-1,-1])
        state_error = float(abs(packed-saved['states'][-1]).max())
        evidence.check('fresh_layer_and_time_refinement',state_error<1e-9,state_error)
        archive = evidence.output/'reference_count33_degree12.npz'
        np.savez_compressed(archive,final_state=refined.y[:,-1])
        evidence.own(archive,'outputs')
        row,raw = pair_diagnostics(refined_system,.0002,refined.y[:,-1],order=16)
        old = next(case for case in main['cases'] if case['count']==33 and case['time']==.0002)
        evidence.check('pair_energy_refinement',abs(row['pair_energy']-old['pair_energy'])<1e-9)
        evidence.check('forcing_norm_refinement',abs(row['forcing_square']-old['forcing_square'])<1e-7)
        evidence.report['cases'].append(dict(kind='fresh_refinement',max_state_error=state_error,
                                            pair_energy=row['pair_energy'],forcing_square=row['forcing_square']))
        base = refined.y[:,-1]
        direction = refined_system.rhs(.0002,base)
        step = 2e-7
        plus = pair_diagnostics(refined_system,.0002+step,base+step*direction,order=16)[0]
        minus = pair_diagnostics(refined_system,.0002-step,base-step*direction,order=16)[0]
        fd_rate = (plus['pair_energy']-minus['pair_energy'])/(2*step)
        evidence.check('independent_centered_state_direction_rate',abs(fd_rate-row['direct_rate'])<1e-8,
                       dict(finite_difference=fd_rate,identity=row['direct_rate']))
        synthetic = []
        for intervals in [32,64,128,256]:
            spacing = 1/intervals
            midpoint = 1-spacing/2
            coefficient_first,coefficient_second = 1.,1.2
            residual = (coefficient_first-coefficient_second)*midpoint/coefficient_second
            norm_square = spacing*residual**2/coefficient_first
            synthetic.append(dict(h=spacing,forcing_square=norm_square,normalized=norm_square/spacing))
        evidence.check('boundary_coefficient_control_does_not_vanish',
                       all(case['normalized']>.02 for case in synthetic))
        evidence.check('boundary_energy_control_vanishes_with_width',
                       all(second['forcing_square']<first['forcing_square'] for first,second in zip(synthetic,synthetic[1:])))
        evidence.report['synthetic_boundary_control'] = synthetic
        evidence.report['synthetic_scope'] = 'Algebraic localized-coefficient control; not a parent trajectory or an optimal-rate proof.'
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

