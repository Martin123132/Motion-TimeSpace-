from derive_annular_source_gravity_20260914 import EvidenceRun
from run_annular_source_fitted_crossing_20260915 import profile
from scipy.integrate import solve_ivp
import argparse
import hashlib
import json
import numpy as np


def traces(instant,state):
    position,speed=state[:2]
    feet=np.array([position-instant,position+instant])
    scalar,gradient=profile(feet)
    numerator=scalar+(1+np.array([.06,-.06]))*feet*gradient
    return numerator/(position*np.array([1+speed,1-speed]))


def force(instant,state):
    position,speed=state[:2]
    left,right=traces(instant,state)
    return position**2*(1-speed**2)*(left**2-right**2)/2


def rhs(instant,state):
    speed=state[1]
    if abs(speed)>=1.:
        raise ValueError('Timelike branch lost.')
    return np.array([speed,force(instant,state)*(1-speed**2)**1.5/.03,np.sqrt(1-speed**2)])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            exact_characteristic_source_reduction_before_outer_returns=True,
            interval_certified_source_enclosure=False,numerical_reference_not_closed_form_solution=True,
            force_fit=False,force_correction=False,physical_GR_gate_upgraded=False,
            only_flat_spherical_reference_not_MTS_or_full_GR=True)
        seed=np.array([6.03,.06,0.])
        evidence.check('original_initial_gradient_traces',max(abs(traces(0.,seed)-.01))<3e-16)
        evidence.check('original_initial_source_force_zero',abs(force(0.,seed))<3e-16)
        times=np.linspace(0.,.4,81)
        solutions=[]
        for tolerance in [2e-12,2e-13]:
            solution=solve_ivp(rhs,(0.,.4),seed,method='DOP853',rtol=tolerance,atol=tolerance/100,
                max_step=.001,t_eval=times,dense_output=True)
            evidence.check('ODE_'+str(tolerance)+'_complete',solution.success and np.isfinite(solution.y).all())
            solutions.append(solution)
        standard,tight=solutions
        standard_forces=np.array([force(instant,state) for instant,state in zip(times,standard.y.T)])
        tight_forces=np.array([force(instant,state) for instant,state in zip(times,tight.y.T)])
        evidence.check('source_time_control',np.max(abs(standard.y-tight.y))<2e-11
            and max(abs(standard_forces-tight_forces))<2e-12)
        probes=np.linspace(0.,.4,1601)
        sampled=tight.sol(probes).T
        feet=np.column_stack([sampled[:,0]-probes,sampled[:,0]+probes])
        evidence.check('sampled_characteristic_foot_domain',min(feet[:,0])>5.2 and max(feet[:,1])<6.8
            and np.all(feet[:,0]<=6.03+1e-12) and np.all(feet[:,1]>=6.03-1e-12)
            and max(abs(sampled[:,1]))<1.)
        evidence.report['source_domain']=dict(minimum_left_foot=float(min(feet[:,0])),
            maximum_right_foot=float(max(feet[:,1])),maximum_absolute_speed=float(max(abs(sampled[:,1]))),
            interval_certificate=False)
        evidence.report['initial_curvature_fronts']=dict(left_chi_second_jump=-.02/(1+.06)**2,
            right_chi_second_jump=-.02/(1-.06)**2,
            left_phi_second_jump_at_emission=-.02/(6.03*(1+.06)**2),
            right_phi_second_jump_at_emission=-.02/(6.03*(1-.06)**2),
            front_rays='r_left=6.03-t; r_right=6.03+t before outer reflection')
        evidence.report['prediction_frozen_before_spectral_comparison']=True
        destination=evidence.output/'characteristic-source.npz'
        np.savez_compressed(destination,times=times,states=tight.y.T,forces=tight_forces,
            standard_states=standard.y.T,standard_forces=standard_forces)
        evidence.own(destination,'outputs')
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        folder=intake/'annular-dense-GR-references-attempt01'
        path=folder/'status.json'
        status=json.loads(path.read_text())
        evidence.own(path)
        evidence.check('spectral_comparator_complete',status['state']=='complete')
        for degree in [384,512,768]:
            path=folder/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            evidence.check(str(degree)+'_spectral_hash',hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path,allow_pickle=False) as saved:
                evidence.check(str(degree)+'_same_sample_times',np.array_equal(saved['times'],times))
                states,forces=saved['states'].copy(),saved['forces'].copy()
            position,momentum,clock=states[:,-3],states[:,-2],states[:,-1]
            speed=momentum/np.sqrt(.03**2+momentum**2)
            row=dict(degree=degree,maximum_position_difference=float(max(abs(position-tight.y[0]))),
                maximum_speed_difference=float(max(abs(speed-tight.y[1]))),
                maximum_clock_difference=float(max(abs(clock-tight.y[2]))),
                maximum_force_difference=float(max(abs(forces-tight_forces))),
                terminal_force_difference=float(forces[-1]-tight_forces[-1]),
                force_comparison_within_previous_2e8_control=bool(max(abs(forces-tight_forces))<2e-8),
                reference_comparison_not_MTS_physical_gate=True)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
