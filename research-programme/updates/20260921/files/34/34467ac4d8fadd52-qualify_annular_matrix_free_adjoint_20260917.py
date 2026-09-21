from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_canonical_energy_20260917 import CanonicalEnergy
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_GR_projection_20260916 import GRProjection
import argparse
import hashlib
import json
import numpy as np


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            all_modes_and_Gram_rows_retained=True,interval_arithmetic=False,
            full_time_adjoint_performed=False,off_solution_correction_not_omitted=True)
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        path=intake/'annular-dense-GR-references-attempt01/status.json'
        status=json.loads(path.read_text())
        evidence.own(path)
        path=path.parent/'oracle-768.npz'
        evidence.own(path)
        evidence.check('reference_hash',status['state']=='complete' and hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
        with np.load(path,allow_pickle=False) as saved:
            times,states=saved['times'].copy(),saved['states'].copy()
        oracle=TwoSidedGRCharacteristics(768,mass=0.,source=.03)
        for count in [33,129]:
            for gram in [False,True]:
                system=LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=8)
                model=FlatPreassembledFlow(system)
                adjoint=MatrixFreeAdjoint(model)
                dense=FullForceLinearization(system)
                canonical=CanonicalEnergy(model)
                projection=GRProjection(oracle,system)
                reference_model=FlatPreassembledFlow(LocallyRefinedSourceAction(count,False,background_mass=0.,source_splits=8))
                for index in [0,42,80]:
                    state,derivative=projection.reconstruct(states[index],oracle.rhs(times[index],states[index]))
                    context=adjoint.context(state)
                    generator=np.random.default_rng(947+index)
                    covector,direction=generator.normal(size=(2,len(state)))
                    transpose=adjoint.transpose(state,covector,context)
                    dense_value=dense.evaluate(state,True)
                    expected=dense_value['jacobian'].T @ covector
                    relative=float(np.linalg.norm(transpose-expected)/max(1.,np.linalg.norm(expected)))
                    prefix=str(count)+'_'+str(gram)+'_'+str(index)
                    evidence.check(prefix+'_dense_transpose',relative<3e-11,relative)
                    tangent=model.evaluate(state.astype(complex)+1e-25j*direction)['flow'].imag/1e-25
                    dot_error=float(abs(transpose @ direction-covector @ tangent)/max(1.,abs(covector @ tangent)))
                    evidence.check(prefix+'_independent_dot_product',dot_error<3e-10,dot_error)
                    gradient=adjoint.force_gradient(state,context)
                    force_error=float(np.linalg.norm(gradient-dense_value['force_gradient'])/max(1.,np.linalg.norm(dense_value['force_gradient'])))
                    evidence.check(prefix+'_force_gradient',force_error<3e-11,force_error)
                    blocks=canonical.stability(state,derivative)
                    mapped=adjoint.canonical_covector(state,covector,context)
                    expected=blocks['inverse_transform'].T @ covector[:-1]
                    evidence.check(prefix+'_Legendre_dual_map',np.linalg.norm(mapped-expected)/max(1.,np.linalg.norm(expected))<3e-11)
                    density=adjoint.gram_density(state,covector,context)
                    difference=context['value']['flow']-reference_model.evaluate(state)['flow']
                    evidence.check(prefix+'_Gram_dual_density',abs(density-covector @ difference)<3e-10*max(1.,abs(density)))
                    canonical_derivative=-(blocks['inverse_transform'].T @ (transpose[:-1]+blocks['transform_rate'].T @ mapped))
                    expected=-blocks['generator'].T @ mapped
                    if covector[-1]!=0.:
                        clock_gradient=np.zeros_like(expected)
                        velocity_clock=np.zeros(len(state)-1)
                        velocity_clock[-1]=-state[-2]/np.sqrt(1-state[-2]**2)
                        expected-=covector[-1]*(blocks['inverse_transform'].T @ velocity_clock)
                    evidence.check(prefix+'_off_solution_adjoint_identity',np.linalg.norm(canonical_derivative-expected)/max(1.,np.linalg.norm(expected))<3e-10)
                    evidence.report['cases'].append(dict(count=count,branch='MTS' if gram else 'reference',time=float(times[index]),
                        transpose_relative_error=relative,dot_relative_error=dot_error,force_gradient_relative_error=force_error))
                    evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
