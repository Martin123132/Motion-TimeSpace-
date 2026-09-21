from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-action-adjoint-amplification-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            worst_direction_not_actual_trajectory=True,operator_not_modified=True)
        evidence.report['elements'] = []
        for branch in ['reference','MTS']:
            models = [GradedSourceAction(257,branch == 'MTS',source_cap=2e-5),GradedSourceAction(513,branch == 'MTS',source_cap=1e-5)]
            saved = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            fine = saved['maximizing_direction']
            coarse = saved['adjoint_operator'] @ fine
            for name,model,values in zip(['coarse','fine'],models,[coarse,fine]):
                gradient = np.sum(model.reference_radial*values[model.reference_indices],axis=1)
                cells = np.sum((saved[name+'_gradient_weights']*gradient**2).reshape(len(model.edges)-1,-1),axis=1)
                gram = float(np.sum(saved[name+'_Gram_weights']*(model.lifted @ values)**2))
                total = float(values @ saved[name+'_stiffness'] @ values)
                source = (model.edges[:-1] == model.anchor) | (model.edges[1:] == model.anchor)
                evidence.check(branch+'_'+name+'_cell_energy_reconstruction',abs(np.sum(cells)+gram-total) < 2e-8*max(total,1.))
                top = np.argsort(cells)[-5:][::-1]
                lengths = np.diff(model.edges)
                for index in top:
                    evidence.report['elements'].append(dict(branch=branch,level=name,lower=float(model.edges[index]),
                        upper=float(model.edges[index+1]),length=float(lengths[index]),gradient_energy=float(cells[index]),
                        fraction_of_total=float(cells[index]/total),source_adjacent=bool(source[index]),valid_for_claim=False))
                row = dict(branch=branch,level=name,total_stiffness=total,gradient_stiffness=float(np.sum(cells)),Gram_stiffness=gram,
                    source_adjacent_gradient_fraction=float(np.sum(cells[source])/total),
                    top5_gradient_fraction=float(np.sum(cells[top])/total),
                    maximum_neighbor_cell_ratio=float(max(np.max(lengths[:-1]/lengths[1:]),np.max(lengths[1:]/lengths[:-1]))),
                    minimum_cell_length=float(min(lengths)),source_jump=float(model.jump @ values),valid_for_claim=False)
                evidence.report['cases'].append(row)
                print(json.dumps(row),flush=True)
            path = evidence.output/(branch+'-worst-direction.npz')
            np.savez_compressed(path,coarse_radius=models[0].radii,coarse_projection=coarse,
                fine_radius=models[1].radii,fine_maximizer=fine)
            evidence.own(path,'outputs')
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
