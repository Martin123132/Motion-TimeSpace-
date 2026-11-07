from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose, reduce_force
import numpy as np


def main():
    evidence = EvidenceRun('annular-position-enabled-algebra-attempt01',__file__)
    try:
        evidence.own(evidence.root/'DERIVATION-20260930-C0-force-eliminated-compatibility.md')
        columns = np.array([[2.,3.,-1.],[1.,2.,3.],[-2.,1.,4.],[.5,-3.,2.]])
        amplitudes = np.array([.2,-.3,.7])
        baseline = -columns@amplitudes
        errors = np.full((4,3),1e-12)
        result = diagnose(baseline,columns,np.full(4,1e-12),errors)
        evidence.check('manufactured_rank',result['rank_resolved'])
        evidence.check('all_manufactured_candidates',len(result['candidates'])==5 and all(row['within_sampled_uncertainty'] for row in result['candidates']))
        evidence.check('recovered_jet',max(np.max(abs(np.array(row['amplitudes'])-amplitudes)) for row in result['candidates'])<1e-12)
        reduced,operator = reduce_force(baseline,columns)
        evidence.check('exact_elimination',np.max(abs(reduced+operator@amplitudes[1:]))<1e-14)
        null = np.array(result['null_obstruction']['left_null'])
        incompatible = baseline.copy()
        incompatible[1:] += .1*null
        rejected = diagnose(incompatible,columns,np.full(4,1e-12),errors)
        evidence.check('incompatibility_negative_control',not rejected['any_candidate_within_sampled_uncertainty'])
        evidence.check('null_obstruction',abs(rejected['null_obstruction']['value']-.1)<1e-14)
        scale = np.array([1e12,1e-9,1e5])
        scaled = diagnose(baseline,columns*scale,np.full(4,1e-12),errors*scale)
        evidence.check('column_units_covariance',max(np.max(abs(np.array(row['amplitudes'])*scale-amplitudes)) for row in scaled['candidates'])<1e-12)
        row_scale = np.array([3.,.2,9.,4.])
        scaled_rows = diagnose(baseline*row_scale,columns*row_scale[:,None],np.full(4,1e-12)*row_scale,errors*row_scale[:,None])
        evidence.check('compatible_row_units_covariance',all(row['within_sampled_uncertainty'] for row in scaled_rows['candidates']))
        dependent = columns.copy()
        dependent[:,2] = 2*dependent[:,1]+dependent[:,0]
        result = diagnose(-dependent@amplitudes,dependent,np.full(4,1e-12),errors)
        evidence.check('dependent_columns_not_promoted',not result['rank_resolved'] and result['null_obstruction'] is None)
        unresolved = errors.copy()
        unresolved[0,0] = 3.
        result = diagnose(baseline,columns,np.full(4,1e-12),unresolved)
        evidence.check('unresolved_position_pivot',not result['position_pivot_resolved'] and not result['rank_resolved'])
        zero = columns.copy()
        zero[0,0] = 0.
        raised = False
        try:
            reduce_force(baseline,zero)
        except ValueError:
            raised = True
        evidence.check('zero_pivot_rejected',raised)
        negative = errors.copy()
        negative[2,1] = -1.
        raised = False
        try:
            diagnose(baseline,columns,np.full(4,1e-12),negative)
        except ValueError:
            raised = True
        evidence.check('negative_error_rejected',raised)
        evidence.report.update(manufactured_only=True,actual_amplitudes_solved=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
