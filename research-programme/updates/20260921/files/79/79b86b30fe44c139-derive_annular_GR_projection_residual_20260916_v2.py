from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_GR_projection_20260916 import GRProjection
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import solve_banded
import argparse
import hashlib
import json
import numpy as np


def momentum_residual(model, state, derivative):
    count = model.count
    field,position,rates,speed = state[:count],state[count],state[count+1:-2],state[-2]
    matrices = model.matrices(position)
    cross = band_product(matrices['transport'],field)
    square_field = band_product(matrices['square'],field)
    mass_b_rate = band_product(matrices['mass_b'],rates)
    transport_rate = band_product(matrices['transport'],rates)
    drift = mass_b_rate+transport_rate-band_product(matrices['transport'],rates,True)
    factor = model.lifted @ field
    stiffness = band_product(matrices['bulk'],field)+model.lifted_transpose @ (matrices['gram']*factor)
    field_rhs = -speed*drift-stiffness-speed**2*(band_product(matrices['transport_b'],field)-square_field)
    source_rhs = rates @ (mass_b_rate/2-transport_rate)-2*speed*rates @ square_field
    source_rhs -= speed**2*(field @ band_product(matrices['square_b'],field))/2
    source_rhs -= (field @ band_product(matrices['bulk_b'],field)+factor @ (matrices['gram_b']*factor))/2
    inertia = model.system.source_mass/(1-speed**2)**1.5
    total_inertia = inertia+field @ square_field
    field_residual = field_rhs-band_product(matrices['mass'],derivative[count+1:-2])-cross*derivative[-2]
    source_residual = source_rhs-cross @ derivative[count+1:-2]-total_inertia*derivative[-2]
    solved = solve_banded((2,2),matrices['mass'],np.column_stack([field_residual,cross]),check_finite=False)
    schur = total_inertia-cross @ solved[:,1]
    direct = inertia*source_residual/schur
    feedback = -inertia*(cross @ solved[:,0])/schur
    return dict(field=field_residual,source=source_residual,source_force_part=direct,
        field_force_part=feedback,force=direct+feedback,schur=schur)


def original_momentum_residual(system, state, derivative, instant):
    coordinates,rates = np.split(state[:-1],2)
    data = system.evaluate(instant,coordinates,rates)
    moved = system.evaluate(instant+1e-24j,coordinates+1e-24j*rates,rates)
    right = np.append(data['scalar_covector'],system.source_covector(instant,coordinates,rates))-moved['momenta'].imag/1e-24
    field = right[:-1]-band_product(data['mass_bands'],derivative[system.count+1:-2])-data['cross']*derivative[-2]
    source = right[-1]-data['cross'] @ derivative[system.count+1:-2]-data['source_inertia']*derivative[-2]
    return field,source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for label in ['annular-GR-projection-qualification-attempt01','annular-dense-GR-references-attempt01']:
            path = intake/label/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        evidence.report.update(finite_future_trajectories_read=False,force_fit=False,force_correction=False,
            original_action_unchanged=True,all_modes_and_Gram_rows_retained=True,
            projection_kinematic_defect_retained=True,prescribed_flat_background_only=True,
            independent_reference_resolution_not_rigorous_error_bound=True)
        oracle_status = status
        for degree in [384,512,768]:
            oracle = TwoSidedGRCharacteristics(degree,mass=0.,source=.03)
            path = intake/'annular-dense-GR-references-attempt01'/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            evidence.check(str(degree)+'_input_hash',hashlib.sha256(path.read_bytes()).hexdigest()==oracle_status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path,allow_pickle=False) as saved:
                times,oracle_states,oracle_forces = saved['times'].copy(),saved['states'].copy(),saved['forces'].copy()
            for count in [257,513,1025]:
                systems = {name:LocallyRefinedSourceAction(count,name=='MTS',background_mass=0.,source_splits=8)
                    for name in ['reference','MTS']}
                models = {name:FlatPreassembledFlow(system) for name,system in systems.items()}
                system = systems['reference']
                projector = GRProjection(oracle,system)
                states,derivatives = [],[]
                for instant,state in zip(times,oracle_states):
                    projected,derivative = projector.reconstruct(state,oracle.rhs(instant,state))
                    states.append(projected)
                    derivatives.append(derivative)
                states,derivatives = np.array(states),np.array(derivatives)
                initial_error = initial(system)-states[0]
                kinematic = states[:,system.count+1:-2]-derivatives[:,:system.count]
                prefix = str(degree)+'-'+str(count)
                source_identity_error = float(np.max(abs(system.source_mass*derivatives[:,-2]/(1-states[:,-2]**2)**1.5-oracle_forces)))
                evidence.check(prefix+'_material_source_identity',source_identity_error<2e-13,source_identity_error)
                evidence.check(prefix+'_finite_full_projection',np.isfinite(states).all() and np.isfinite(derivatives).all())
                outputs = dict(times=times,states=states,derivatives=derivatives,oracle_forces=oracle_forces,initial_error=initial_error)
                for branch,model in models.items():
                    forces,residuals,momentum_fields,momentum_sources,source_parts,field_parts = [],[],[],[],[],[]
                    identities,original_errors = [],[]
                    for index,(instant,state,derivative) in enumerate(zip(times,states,derivatives)):
                        value = model.evaluate(state)
                        residual = value['flow']-derivative
                        momentum = momentum_residual(model,state,derivative)
                        forces.append(value['force'])
                        residuals.append(residual)
                        momentum_fields.append(momentum['field'])
                        momentum_sources.append(momentum['source'])
                        source_parts.append(momentum['source_force_part'])
                        field_parts.append(momentum['field_force_part'])
                        identities.append(abs(momentum['force']-(value['force']-oracle_forces[index])))
                        if index in [0,37,42,80]:
                            original_field,original_source = original_momentum_residual(systems[branch],state,derivative,instant)
                            original_errors.append(float(max(np.max(abs(original_field-momentum['field'])),abs(original_source-momentum['source']))))
                    forces,residuals = np.array(forces),np.array(residuals)
                    evidence.check(prefix+branch+'_original_momentum_covectors',max(original_errors)<2e-10,max(original_errors))
                    evidence.check(prefix+branch+'_coupled_force_defect_identity',max(identities)<2e-11,float(max(identities)))
                    evidence.check(prefix+branch+'_source_clock_kinematics',np.max(abs(residuals[:,system.count]))<2e-13 and np.max(abs(residuals[:,-1]))<2e-13)
                    for name,values in [('force',forces),('residual',residuals),('momentum_field',momentum_fields),
                        ('momentum_source',momentum_sources),('source_part',source_parts),('field_part',field_parts)]:
                        outputs[branch+'_'+name] = np.asarray(values)
                    signed = forces-oracle_forces
                    row = dict(degree=degree,count=count,splits=8,branch=branch,
                        max_kinematic_defect=float(np.max(abs(kinematic))),
                        max_field_acceleration_defect=float(np.max(abs(residuals[:,system.count+1:-2]))),
                        max_source_acceleration_defect=float(np.max(abs(residuals[:,-2]))),
                        max_projected_force_defect=float(np.max(abs(signed))),
                        force_defect_at_021=float(signed[42]),force_defect_at_end=float(signed[-1]),
                        max_initial_projection_error=float(np.max(abs(initial_error))),
                        max_source_part=float(np.max(np.abs(source_parts))),max_field_part=float(np.max(np.abs(field_parts))),
                        original_covector_error=max(original_errors),force_identity_error=float(max(identities)))
                    evidence.report['cases'].append(row)
                    evidence.save()
                    print(row,flush=True)
                destination = evidence.output/('projection-'+prefix+'.npz')
                np.savez_compressed(destination,**outputs)
                evidence.own(destination,'outputs')
                evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
