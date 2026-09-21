import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import numpy as np
import sympy as sym
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_moving_collar_action_20260914 import MovingCollarAction


def run():
    evidence=EvidenceRun('annular-moving-collar-variation-attempt01',__file__)
    try:
        evidence.report.update(scope='Constant-source-energy Routh reduction, minimal embedding extension, and exact finite moving scalar/action derivatives; flat metric for scalar transport test.',
                               material_motion_extension_unique_from_fixed_action=False,
                               nodal_transport_lift='Positive base node pairing inverse times S_base.T B_base, then multiply by reference node coordinate.',
                               coupled_moving_finite_collar_GR_completed=False)
        mass,lapse,root,shift,velocity,source_momentum=sym.symbols('S N U beta V p',positive=True)
        proper=sym.sqrt(lapse**2-(velocity+shift)**2/root**2)
        source_lagrangian=-mass*proper
        evidence.check('proper_source_canonical_momentum',sym.simplify(sym.diff(source_lagrangian,velocity)-mass*(velocity+shift)/(root**2*proper))==0)
        momentum_expression=mass*(velocity+shift)/(root**2*proper)
        legendre=sym.factor(momentum_expression*velocity-source_lagrangian+shift*momentum_expression)
        evidence.check('source_Hamiltonian_mass_shell_squared',sym.simplify(legendre**2-lapse**2*(mass**2+root**2*momentum_expression**2))==0)
        energy,clock_rate,multiplier,scalar=sym.symbols('E theta_dot lambda chi',real=True)
        old_action=energy*(clock_rate-proper)+proper*multiplier*scalar
        routh=(old_action-energy*clock_rate).subs({energy:mass,scalar:0})
        evidence.check('constant_energy_unforced_Routh_reduction',sym.simplify(routh-source_lagrangian)==0)
        random=np.random.default_rng(141121)
        for gram in [False,True]:
            system=MovingCollarAction(33,gram,offsets=[-.3,.3],weights=[.5,.5])
            state=system.initial_state.copy()
            scalar,momentum,position,velocity=system.unpack(state)
            scalar[:]=.001*random.normal(size=scalar.shape)
            momentum[:]=.0001*random.normal(size=momentum.shape)
            velocity[:]=[.12,-.08]
            vector=system.rhs(0.,state)
            rate,momentum_rate,position_rate,acceleration=system.unpack(vector)
            data=system.fields(state)
            complex_energy=system.energy(state.astype(complex)+1e-25j*vector)['total']
            energy_derivative=float(np.imag(complex_energy)/1e-25)
            evidence.check(str(gram)+'_exact_energy_vector_field_identity',abs(energy_derivative)<1e-14,energy_derivative)
            canonical_derivative=np.imag(system.source_canonical(state.astype(complex)+1e-25j*vector))/1e-25
            position_gradient=[]
            for layer in range(system.layers):
                varied=position.astype(complex).copy()
                varied[layer]+=1e-25j
                action=system.lagrangian(scalar,rate,varied,velocity)
                position_gradient.append(np.imag(action)/1e-25/system.weights[layer])
            evidence.check(str(gram)+'_source_Euler_Lagrange_from_action',max(abs(canonical_derivative-position_gradient))<2e-13,float(max(abs(canonical_derivative-position_gradient))))
            selected=[(0,0),(0,16),(0,31),(1,2),(1,31)]
            scalar_errors=[]
            momentum_errors=[]
            for layer,node in selected:
                varied=scalar.astype(complex).copy()
                varied[layer,node]+=1e-25j
                action=system.lagrangian(varied,rate,position,velocity)
                scalar_errors.append(abs(np.imag(action)/1e-25/system.weights[layer]-momentum_rate[layer,node]))
                varied_rate=rate.astype(complex).copy()
                varied_rate[layer,node]+=1e-25j
                action=system.lagrangian(scalar,varied_rate,position,velocity)
                momentum_errors.append(abs(np.imag(action)/1e-25/system.weights[layer]-momentum[layer,node]))
            evidence.check(str(gram)+'_scalar_Euler_Lagrange_from_action',max(scalar_errors)<2e-13,max(scalar_errors))
            evidence.check(str(gram)+'_canonical_scalar_momentum_from_action',max(momentum_errors)<2e-13,max(momentum_errors))
            static=system.lagrangian(scalar,rate,position,np.zeros_like(velocity))
            fixed_expected=system.weights @ (np.sum(data['mass']*rate**2,axis=1)/2-
                                            np.sum(data['coefficient']*data['amplitudes']**2,axis=1)/2-system.source_mass)
            evidence.check(str(gram)+'_original_static_scalar_and_reservoir_action',abs(static-fixed_expected)<2e-15)
            shift_no_edge=vector.copy()
            shift_no_edge[-system.layers:]*=(system.source_mass/(1-velocity**2)**1.5+data['edge_inertia'])/(system.source_mass/(1-velocity**2)**1.5)
            wrong=float(np.imag(system.energy(state.astype(complex)+1e-25j*shift_no_edge)['total'])/1e-25)
            evidence.check(str(gram)+'_omitted_endpoint_inertia_detected',abs(wrong)>1e-9,wrong)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

