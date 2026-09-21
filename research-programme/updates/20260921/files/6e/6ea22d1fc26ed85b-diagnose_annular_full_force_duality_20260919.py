from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_full_force_transport_20260919 import homogeneous,dual_initial
from derive_annular_action_response_time_halving_20260919 import restore_action
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def precise_dot(first,last):
    return float(np.sum(first.astype(np.longdouble)*last.astype(np.longdouble),dtype=np.longdouble))


def main():
    evidence = EvidenceRun('annular-full-force-duality-diagnostic-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,roundoff_budget_not_exponential_error_certificate=True)
        failed_path = evidence.output.parent/'annular-full-force-transport-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        evidence.check('strict_duality_failure_retained',failed['state'] == 'failed')
        for branch in ['reference','MTS']:
            coarse_action = restore_action(checked_load(evidence,'annular-action-exponential-response-attempt01',branch+'-coarse-action.npz'))
            fine_action = restore_action(checked_load(evidence,'annular-action-exponential-response-attempt01',branch+'-fine-action.npz'))
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            initial = checked_load(evidence,'annular-moving-duhamel-trajectory-attempt01',branch+'-point032.npz')
            phases = [np.stack([initial[str(level)+'_position'],-initial[str(level)+'_reverse_velocity']]) for level in [0,1]]
            coarse_free = homogeneous(coarse_action,phases[0][:,:,None])[:,:,0]
            fine_free = homogeneous(fine_action,phases[1][:,:,None])[:,:,0]
            for name in ['spatial32','spatial64']:
                saved = checked_load(evidence,'annular-full-force-endpoints-attempt01',branch+'-'+name+'-force-covector.npz')
                covector = saved['covector']
                transferred = np.stack([interpolation.T @ item for item in covector])
                fine_dual,coarse_dual = dual_initial(fine_action,covector),dual_initial(coarse_action,transferred)
                delta_initial = phases[1]-np.stack([interpolation @ item for item in phases[0]])
                dual_difference = np.stack([interpolation.T @ item for item in fine_dual])-coarse_dual
                raw = float(np.sum(fine_dual*phases[1])-np.sum(coarse_dual*phases[0]))
                compensated = precise_dot(fine_dual,phases[1])-precise_dot(coarse_dual,phases[0])
                split = precise_dot(fine_dual,delta_initial)+precise_dot(dual_difference,phases[0])
                forward_vector = fine_free-np.stack([interpolation @ item for item in coarse_free])
                forward = precise_dot(covector,forward_vector)
                absolute_products = float(np.sum(abs(fine_dual*phases[1]))+np.sum(abs(coarse_dual*phases[0])))
                operations = fine_dual.size+coarse_dual.size
                gamma = operations*np.finfo(float).eps/(1-operations*np.finfo(float).eps)
                row = dict(branch=branch,comparison=name,raw_dual=raw,compensated_dual=compensated,
                    split_dual=split,forward=forward,raw_error=abs(raw-forward),
                    compensated_error=abs(compensated-forward),split_error=abs(split-forward),
                    absolute_dot_products=absolute_products,standard_dot_roundoff_bound=gamma*absolute_products,
                    old_tolerance=2e-10*max(abs(raw),abs(forward),1e-9)+3e-16,
                    longdouble_bits=int(np.finfo(np.longdouble).nmant+1),valid_for_claim=False)
                evidence.report['cases'].append(row)
                evidence.check(branch+'_'+name+'_finite_diagnostic',all(np.isfinite(value) for value in row.values()
                    if isinstance(value,(float,int))))
                evidence.save()
                print(json.dumps(row),flush=True)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
