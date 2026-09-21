from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_canonical_energy_20260917 import CanonicalEnergy
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import solve
from fractions import Fraction
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            interval_arithmetic=False,continuum_regularities_established=False,
            full_time_adjoint_performed=False,uniform_output_continuity_proven=False,
            conditional_C2_consistency_theorem=True,clock_is_passive_observable=True,
            prescribed_flat_background_only=True,force_fit=False,force_correction=False)
        width = Fraction(3,7)
        positive_area = width*(Fraction(1,3)-Fraction(3,2)*Fraction(1,3)**2)
        signed_area = width*(Fraction(1,2)-Fraction(3,2)*Fraction(1,2)**2
            +Fraction(1,2)-1-Fraction(1,2)*Fraction(1,2)**2+Fraction(1,2))
        evidence.check('P2_C2_trace_kernel_zero_mean_and_L1',signed_area==0 and 2*positive_area==width/3)
        evidence.report['C2_not_C3_cases'] = []
        for count in [33,65,129,257,513,1025,2049]:
            system = LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=8)
            offsets = system.radii-system.anchor
            cusp,power,amplitude = -.247,2.5,.13
            slopes = np.array([.7,1.1])
            curvatures = np.array([-.2,.3])
            sides = (offsets>0.).astype(int)
            base_slope = power*np.sign(-cusp)*abs(cusp)**(power-1)
            values = slopes[sides]*offsets+curvatures[sides]*offsets**2/2
            values += amplitude*(abs(offsets-cusp)**power-abs(cusp)**power-base_slope*offsets)
            factor = system.lifted @ values
            spacing = system.gram_spacing
            modulus = lambda distance: abs(amplitude)*power*(power-1)*distance**.5
            maximum_curvature = max(abs(curvatures))+abs(amplitude)*power*(power-1)*max(abs(offsets-cusp))**.5
            bulk_offsets = system.base_radii-system.anchor
            raw_bounds = []
            for index in range(count-3):
                nodes = bulk_offsets[index:index+4]
                if nodes[0]<0.<nodes[-1]:
                    raw_bounds.append(maximum_curvature*np.array([1.,3.,3.,1.]) @ nodes**2/2)
                else:
                    raw_bounds.append(spacing**2*modulus(spacing))
            edge = np.searchsorted(system.edges,system.anchor)
            left,right = system.anchor-system.edges[edge-1],system.edges[edge+1]-system.anchor
            trace_bound = (left*modulus(left)+right*modulus(right))/3
            factor_bound = np.linalg.norm(raw_bounds)/np.sqrt(8)+np.linalg.norm(system.lifted_hinge)*trace_bound
            actual = float(np.linalg.norm(factor))
            evidence.check(str(count)+'_C2_Holder_consistency_bound',actual<=factor_bound+3e-13,
                dict(actual=actual,bound=float(factor_bound)))
            evidence.report['C2_not_C3_cases'].append(dict(count=count,spacing=spacing,
                factor_norm=actual,bound=float(factor_bound),factor_over_h_squared=actual/spacing**2,
                curvature_holder_exponent=.5,third_derivative_unbounded_at_cusp=True))
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        status_path = intake/'annular-canonical-energy-attempt01/status.json'
        evidence.own(status_path)
        status = json.loads(status_path.read_text())
        evidence.check('canonical_qualification_complete',status['state']=='complete' and len(status['cases'])==24)
        for count in [33,65,129,257]:
            for gram in [False,True]:
                branch = 'MTS' if gram else 'reference'
                path = status_path.parent/(str(count)+'_'+branch+'_42.npz')
                evidence.own(path)
                if hashlib.sha256(path.read_bytes()).hexdigest()!=status['outputs'][str(path.relative_to(evidence.root))]:
                    raise RuntimeError('Canonical source changed.')
                with np.load(path,allow_pickle=False) as saved:
                    state,derivative = saved['state'].copy(),saved['derivative'].copy()
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=8)
                model = FlatPreassembledFlow(system)
                energy = CanonicalEnergy(model)
                blocks = energy.stability(state,derivative)
                complete = FullForceLinearization(system).evaluate(state,True)
                prefix = str(count)+'_'+branch
                velocity_metric = np.block([[-blocks['coordinate'],np.zeros_like(blocks['coordinate'])],
                    [np.zeros_like(blocks['kinetic']),blocks['kinetic']]])
                velocity_metric[system.count,system.count] += 1.
                mapped_metric = blocks['transform'].T @ blocks['metric'] @ blocks['transform']
                evidence.check(prefix+'_Jacobi_energy_pullback',np.linalg.norm(mapped_metric-velocity_metric)/np.linalg.norm(velocity_metric)<2e-11)
                flow = model.evaluate(state)['flow']
                flow_derivatives = energy.lagrangian(state.astype(complex)+1e-25j*flow,True)
                reference_derivatives = energy.lagrangian(state.astype(complex)+1e-25j*derivative,True)
                source_shift = np.zeros_like(blocks['coordinate'])
                source_shift[system.count,system.count] = 1.
                mixed_rate = flow_derivatives['mixed'].imag/1e-25
                jacobi_rate = np.block([[-reference_derivatives['coordinate'].imag/1e-25,source_shift-mixed_rate.T],
                    [source_shift-mixed_rate,reference_derivatives['kinetic'].imag/1e-25-2*flow_derivatives['kinetic'].imag/1e-25]])
                actual_rate = blocks['transform'].T @ blocks['symmetric_rate'] @ blocks['transform']
                evidence.check(prefix+'_off_solution_Jacobi_rate',np.linalg.norm(actual_rate-jacobi_rate)/max(1.,np.linalg.norm(jacobi_rate))<2e-10)
                force_gradient = complete['force_gradient'][:-1]
                force_dual = float(np.sqrt(force_gradient @ solve(velocity_metric,force_gradient,assume_a='pos')))
                clock_gradient = np.zeros_like(force_gradient)
                clock_gradient[-1] = -state[-2]/np.sqrt(1-state[-2]**2)
                clock_dual = float(np.sqrt(clock_gradient @ solve(velocity_metric,clock_gradient,assume_a='pos')))
                direction = np.random.default_rng(105+count).normal(size=len(state))
                check_gradient = model.evaluate(state.astype(complex)+1e-25j*direction)['force'].imag/1e-25
                evidence.check(prefix+'_independent_force_gradient',abs(check_gradient-complete['force_gradient'] @ direction)<2e-9*max(1.,abs(check_gradient)))
                if gram:
                    reference = FlatPreassembledFlow(LocallyRefinedSourceAction(count,False,background_mass=0.,source_splits=8))
                    difference = flow-reference.evaluate(state)['flow']
                    canonical_difference = blocks['transform'] @ difference[:-1]
                    matrices = model.matrices(state[system.count])
                    factor = system.lifted @ state[:system.count]
                    covector = np.append(-system.lifted.T @ (matrices['gram']*factor),-factor @ (matrices['gram_b']*factor)/2)
                    expected = np.concatenate([np.zeros(system.count+1),covector])
                    evidence.check(prefix+'_pure_potential_canonical_defect',np.linalg.norm(canonical_difference-expected)<3e-11)
                    adjoint = np.random.default_rng(192+count).normal(size=len(expected))
                    momentum_adjoint = adjoint[system.count+1:]
                    dual_row = -(system.lifted @ momentum_adjoint[:-1]) @ (matrices['gram']*factor)
                    dual_row -= momentum_adjoint[-1]*factor @ (matrices['gram_b']*factor)/2
                    evidence.check(prefix+'_exact_adjoint_Gram_row_identity',abs(adjoint @ canonical_difference-dual_row)<3e-11)
                evidence.report['cases'].append(dict(count=count,branch=branch,time=.21,
                    force_energy_dual_norm=force_dual,clock_rate_energy_dual_norm=clock_dual,
                    force_bound_from_unit_energy_error=force_dual,full_time_adjoint_performed=False))
                evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
