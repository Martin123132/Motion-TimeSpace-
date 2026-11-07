from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_high_order_native_v2_20261003 import adapt_owner, HighKernel, HighLoads, HighAction, HighInverse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from analyze_annular_P7_bisection_20261003 import selected_archive
from construct_annular_septic_response_20261003 import pin, metric_jets
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import json
import numpy as np


def jet_value(root, report, key):
    values=[selected_archive(root/row['path'],[key])[key] for row in report['probes']]
    slopes=[(value-values[0])/amount for value,amount in zip(values[1:],report['amounts'])]
    return (4*slopes[2]-slopes[1])/3


def main():
    pin(4)
    evidence=EvidenceRun('annular-jump-dual-bound-attempt01',__file__)
    deadline=perf_counter()+3600
    try:
        base='source-intake/navier-stokes/20260914/'
        fine_report=verify_report(evidence,base+'annular-P7-bisected-live-primary-attempt01/status.json')
        old_report=verify_report(evidence,base+'annular-product-source-corrected-live-primary-attempt01/status.json')
        fine_jet=verify_report(evidence,base+'annular-P7-bisected-balanced-time-response-attempt01/status.json')
        old_jet=verify_report(evidence,base+'annular-product-source-corrected-balanced-time-response-attempt01/status.json')
        prepared=verify_report(evidence,base+'annular-P7-bisection-preparation-attempt01/status.json')
        fine_mesh=json.loads((evidence.root/fine_report['mesh_path']).read_text())
        old_mesh=json.loads((evidence.root/old_report['mesh_path']).read_text())
        saved=read_archive(evidence.root/fine_report['states'][0]['path'])
        high=next(row for row in fine_report['balanced_results'] if row['material']==64)
        old_high=next(row for row in old_report['balanced_results'] if row['material']==64)
        fine_acceleration=selected_archive(evidence.root/high['path'],['acceleration'])['acceleration']
        old_acceleration=selected_archive(evidence.root/old_high['path'],['acceleration'])['acceleration']
        matrix=load_npz(evidence.root/high['matrix_path'])
        inverse=HighInverse(matrix,fine_acceleration.shape,7)
        mapping=json.loads((evidence.root/prepared['map_path']).read_text())
        seal=evidence.output.parent/'annular-all-native-jump-integrity-20261003.json'
        evidence.own(seal)
        new_jump=jet_value(evidence.root,fine_jet,'jump')
        old_jump=jet_value(evidence.root,old_jet,'jump')
        auxiliary_jump=jet_value(evidence.root,fine_jet,'auxiliary_jump')
        cases=[dict(name='new_native_maximum',kind='native',label=.5,column=600),
            dict(name='old_native_maximum',kind='native',label=-.5,column=609),
            dict(name='new_midpoint_maximum',kind='auxiliary',label=.5,column=601)]
        evidence.report.update(results=[],bound_scope='Fixed initial geometry, field-linear contribution to moving-jump second response.',
            full_nonlinear_bound_proven=False,source_acceleration_fitted=False,valid_for_claim=False)
        with localcontext() as context:
            context.prec=75
            unused,original,sources=restore_case(evidence,json.loads(seal.read_text())['hashes'],'MTS-primary','third',deadline)
            owner=adapt_owner(original.owner,fine_mesh)
            loads=HighLoads(owner,decimals(saved['coordinates']),saved['rates'],fine_mesh,'primary',deadline)
            solver,solution=reconstructed_solver(saved)
            action=HighAction(loads,fine_mesh,solver,solution)
            engine=loads.native_engine
            old_engine=HighKernel(old_mesh,old_mesh['gram_support'])
            old_exact=decimal_array(old_acceleration)
            extended=np.full(fine_acceleration.shape,Decimal(0),dtype=object)
            extended[:,-1]=old_exact[:,-1]
            templates=np.array([[[Decimal(Fraction(value).numerator)/Decimal(Fraction(value).denominator) for value in row]
                for row in half] for half in mapping['templates']],dtype=object)
            for cell,old_indices in enumerate(old_engine.indices):
                nodal=np.full((8,len(extended)),Decimal(0),dtype=object)
                valid=old_indices>=0
                nodal[valid]=old_exact[:,old_indices[valid]].T
                for half in range(2):
                    values=templates[half]@nodal
                    for local_index,target in enumerate(engine.indices[2*cell+half]):
                        if target>=0:
                            extended[:,target]=values[local_index]
            delta=decimal_array(fine_acceleration)-extended
            delta_float=np.asarray(delta,float)
            norm_square=float(delta_float.ravel()@(matrix@delta_float.ravel()))
            evidence.check('positive_full_kinetic_defect',norm_square>0,norm_square)
            for case in cases:
                data=physical_data(engine,loads,action,case['label'])
                if case['kind']=='native':
                    native_index=case['column']+1
                    edge=engine.native_edges[native_index]
                    beta=data['beta'][native_index]
                else:
                    edge=fine_jet['auxiliary_edge_indices'][case['column']]
                    beta=metric_jets(solver,solution,np.array([float(data['edges'][edge])]))['beta'][0]
                widths=np.diff(data['edges'])
                covector=np.full(engine.count,Decimal(0),dtype=object)
                for cell,weights,sign in [(edge-1,engine.basis.right_first,-1),(edge,engine.basis.left_first,1)]:
                    chosen=engine.indices[cell]>=0
                    covector[engine.indices[cell,chosen]]+=sign*beta*weights[chosen]/widths[cell]
                if case['kind']=='native':
                    unit=np.full(engine.count,Decimal(0),dtype=object)
                    unit[engine.native_indices[native_index]]=Decimal(1)
                    response=engine.evaluate(data['edges'],unit,data['beta'])
                    evidence.check(case['name']+':unit_native_variation_has_zero_source_jump',response['source_jump']==0)
                    covector-=response['field_gradient']
                goal=np.zeros(fine_acceleration.shape)
                goal[:,:-1]=np.outer(data['cardinal'],np.asarray(covector,float))
                adjoint=inverse.solve(goal.ravel()).reshape(goal.shape)
                for repeat in range(2):
                    residual=(matrix@adjoint.ravel()).reshape(goal.shape)-goal
                    adjoint-=inverse.solve(residual.ravel()).reshape(goal.shape)
                residual=(matrix@adjoint.ravel()).reshape(goal.shape)-goal
                relative=float(inverse.residual_norm(residual)/inverse.residual_norm(goal))
                evidence.check(case['name']+':adjoint_equation',relative<2e-10,relative)
                dual_square=float(goal.ravel()@adjoint.ravel())
                evidence.check(case['name']+':positive_dual_norm',dual_square>0,dual_square)
                field_delta=delta[:,:-1].T@decimal_array(data['cardinal'])
                observed=float(sum(covector*field_delta,Decimal(0)))
                direct=float(goal.ravel()@delta_float.ravel())
                roundoff_budget=5e-13*float(np.sum(abs(goal*delta_float)))
                evidence.check(case['name']+':decimal_linear_functional',abs(observed-direct)<=roundoff_budget,
                    dict(error=abs(observed-direct),budget=roundoff_budget))
                bound=float(np.sqrt(dual_square*norm_square))
                evidence.check(case['name']+':Cauchy_Schwarz_bound',abs(observed)<=bound*(1+2e-10),dict(observed=observed,bound=bound))
                label_index=fine_jet['labels'].index(case['label'])
                if case['kind']=='native':
                    new_value=float(new_jump[label_index,case['column']])
                    old_value=float(old_jump[label_index,case['column']])
                else:
                    new_value=float(auxiliary_jump[label_index,case['column']])
                    old_value=0.
                row=dict(case,dual_norm=float(np.sqrt(dual_square)),kinetic_defect_norm=float(np.sqrt(norm_square)),
                    field_response_change=observed,conditional_bound=bound,old_total_response=old_value,new_total_response=new_value,
                    total_response_change=new_value-old_value,unexplained_by_fixed_geometry_field_change=(new_value-old_value)-observed,
                    adjoint_relative_residual=relative,valid_for_claim=False)
                path=evidence.output/(case['name']+'-adjoint.npz')
                np.savez_compressed(path,goal=goal,adjoint=adjoint,residual=residual)
                evidence.own(path,'outputs')
                row['path']=str(path.relative_to(evidence.root))
                evidence.report['results'].append(row)
                evidence.save()
                print(json.dumps(row),flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
