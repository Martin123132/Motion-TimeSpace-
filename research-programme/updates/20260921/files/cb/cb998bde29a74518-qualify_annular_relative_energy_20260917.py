from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_relative_hamiltonian_20260917 import RelativeHamiltonian
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import eigh,cholesky
from scipy.special import roots_legendre
import argparse
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            interval_arithmetic=False,nonlinear_relative_energy_identity=True,
            uniform_reference_regularities_established=False,nonlinear_full_GR_limit_proven=False,
            auxiliary_energy_shift_not_action_change=True,beta=1.,finite_samples_only=True)
        speed,mass,complement,loading_direction,complement_direction=sp.symbols('speed mass complement loading_direction complement_direction',real=True)
        inertia=mass/(1-speed**2)**sp.Rational(3,2)
        schur=complement+inertia
        direction=loading_direction-speed*complement_direction
        second=direction**2/schur
        third=sp.diff(second,speed)*direction/schur+sp.diff(second,complement)*complement_direction
        expected=-3*complement_direction*direction**2/schur**2-sp.diff(inertia,speed)*direction**3/schur**3
        evidence.check('exact_reduced_Hamiltonian_third_derivative',sp.simplify(third-expected)==0)
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        folder=intake/'annular-canonical-energy-attempt01'
        path=folder/'status.json'
        status=json.loads(path.read_text())
        evidence.own(path)
        evidence.check('sealed_reference_states_complete',status['state']=='complete')
        for count in [33,65,129,257]:
            for gram in [False,True]:
                branch='MTS' if gram else 'reference'
                path=folder/(str(count)+'_'+branch+'_42.npz')
                evidence.own(path)
                if hashlib.sha256(path.read_bytes()).hexdigest()!=status['outputs'][str(path.relative_to(evidence.root))]:
                    raise RuntimeError('Changed sealed reference state.')
                with np.load(path,allow_pickle=False) as saved:
                    reference,derivative=saved['state'].copy(),saved['derivative'].copy()
                system=LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=8)
                model=FlatPreassembledFlow(system)
                relative=RelativeHamiltonian(model)
                base=relative.energy.evaluate(reference)
                mass=base['kinetic'][:-1,:-1]
                stiffness=-base['coordinate'][:-1,:-1]
                eigenvalues,eigenvectors=eigh(stiffness,mass,subset_by_index=[system.count-1,system.count-1])
                frequency=float(np.sqrt(eigenvalues[0]))
                mode=eigenvectors[:,0]/frequency
                direction=np.concatenate([mode,[1.],.3*frequency*mode,[-.4,0.]])
                for amplitude in [1e-4,5e-5]:
                    actual=reference+amplitude*direction
                    actual_map=relative.energy.lagrangian(actual)
                    restored=relative.inverse_legendre(actual_map['canonical_state'],actual[-1])
                    prefix=str(count)+'_'+branch+'_'+str(amplitude)
                    evidence.check(prefix+'_inverse_Legendre',max(abs(restored-actual))<3e-11)
                    evidence.check(prefix+'_reduced_Hamiltonian_value',abs(relative.reduced_value(actual_map['canonical_state'])-model.evaluate(actual,True)['energy'])<3e-13)
                    distance=float(relative.distance(actual,reference))
                    rate=relative.rate(actual,reference,derivative)
                    actual_flow=model.evaluate(actual)['flow']
                    complex_rate=float(relative.distance(actual.astype(complex)+1e-25j*actual_flow,
                        reference.astype(complex)+1e-25j*derivative).imag/1e-25)
                    evidence.check(prefix+'_exact_nonlinear_rate',abs(complex_rate-rate['rate'])<3e-11,
                        dict(direct=complex_rate,identity=rate['rate']))
                    artificial_derivative=derivative.copy()
                    artificial_derivative[system.count]+=.013
                    artificial_derivative[-2]-=.004
                    artificial_derivative[:system.count]+=1e-3*mode
                    artificial_rate=relative.rate(actual,reference,artificial_derivative)
                    artificial_direct=float(relative.distance(actual.astype(complex)+1e-25j*actual_flow,
                        reference.astype(complex)+1e-25j*artificial_derivative).imag/1e-25)
                    artificial_error=abs(artificial_direct-artificial_rate['rate'])
                    evidence.check(prefix+'_nonzero_reference_position_defect',artificial_error<3e-11,artificial_error)
                    integrals=[]
                    for order in [4,8]:
                        points,weights=roots_legendre(order)
                        quadratic,cubic=0.,0.
                        for coordinate,weight in zip((points+1)/2,weights/2):
                            canonical=rate['reference_canonical']+coordinate*rate['difference']
                            state=relative.inverse_legendre(canonical)
                            blocks=relative.energy.evaluate(state)
                            metric=blocks['hessian'].copy()
                            metric[system.count,system.count]+=1.
                            cholesky(metric,lower=True)
                            quadratic+=weight*(1-coordinate)*(rate['difference'] @ metric @ rate['difference'])
                            tangent=blocks['inverse_transform'] @ rate['reference_flow']
                            tangent=np.append(tangent,0.)
                            shifted=relative.energy.evaluate(state.astype(complex)+1e-25j*tangent)
                            cubic+=weight*(1-coordinate)*(rate['difference'] @ (shifted['hessian'].imag/1e-25) @ rate['difference'])
                        integrals.append((float(quadratic),float(cubic)))
                    evidence.check(prefix+'_positive_Bregman_energy',distance>0. and abs(distance-integrals[1][0])<3e-13)
                    evidence.check(prefix+'_third_Hamiltonian_contraction',abs(rate['principal']-integrals[1][1])<3e-11)
                    evidence.check(prefix+'_independent_segment_quadrature',max(abs(np.array(integrals[0])-integrals[1]))<3e-13)
                    row=dict(count=count,branch=branch,amplitude=amplitude,frequency=frequency,
                        relative_energy=distance,raw_rate=rate['rate'],forcing_rate=rate['forcing'],
                        homogeneous_rate_over_energy=(rate['principal']+rate['shift'])/distance,
                        Hamiltonian_third_contraction_over_energy=rate['principal']/distance,
                        direct_rate_error=abs(complex_rate-rate['rate']),artificial_reference_rate_error=artificial_error,segment_integrals=integrals,
                        positive_sampled_segment=True,uniform_bound_claim=False)
                    evidence.report['cases'].append(row)
                    destination=evidence.output/(prefix+'.npz')
                    np.savez_compressed(destination,reference=reference,reference_derivative=derivative,
                        actual=actual,direction=direction,canonical_difference=rate['difference'],
                        relative_energy=distance,exact_rate=rate['rate'],direct_rate=complex_rate,
                        segment_integrals=np.array(integrals),frequency=frequency,amplitude=amplitude)
                    evidence.own(destination,'outputs')
                    evidence.save()
                    print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
