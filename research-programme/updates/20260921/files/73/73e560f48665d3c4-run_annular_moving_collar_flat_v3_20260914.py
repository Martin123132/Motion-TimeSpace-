import run_annular_moving_collar_flat_20260914 as original
from annular_moving_collar_sparse_20260914 import SparseMovingCollarAction
from annular_dynamical_source_20260914 import flat_mirror_rhs
from annular_exact_flat_wave_v2_20260914 import ExactFlatWave
from annular_reference_continuum_shell_20260914 import EvidenceRun
from scipy.integrate import solve_ivp
import numpy as np
import hashlib
import json
import warnings


def inherit(evidence,path):
    status=json.loads(path.read_text())
    evidence.own(path)
    for table in ['inputs','outputs']:
        for filename,digest in status[table].items():
            source=evidence.root/filename
            if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
                raise RuntimeError('Changed inherited evidence: '+filename)
            evidence.own(source)
    return status


def main():
    evidence=EvidenceRun('annular-moving-collar-flat-attempt03',__file__)
    try:
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        old=inherit(evidence,intake/'annular-moving-collar-flat-attempt02/status.json')
        equivalence=inherit(evidence,intake/'annular-moving-collar-sparse-equivalence-attempt01/status.json')
        evidence.check('second_underresolved_attempt_preserved',old['state']=='failed' and
                       'finest_original_accuracy_gates' in old['error'] and len(old['cases'])==16)
        evidence.check('sparse_equivalence_complete',equivalence['state']=='complete' and
                       all(row['passed'] for row in equivalence['checks']))
        original.MovingCollarAction=SparseMovingCollarAction
        evidence.report.update(cases=old['cases'].copy(),gates=old['gates'],
                               constructor_binding='SparseMovingCollarAction; inherited RHS, action, diagnostic and integration functions unchanged.',
                               external_force_history_prescribed=False,full_Gram_factors_retained=True,
                               finite_collar_motion_minimal_extension_assumed=True,
                               all_layers_rigidly_locked=False,
                               refinement_only_no_action_or_accuracy_gate_change=True,warnings=[])
        evidence.save()
        sample_times=np.linspace(0,1.1,33)
        for initial in [5.98,6.,6.02]:
            exact=original.ExactLayer(initial)
            timed=solve_ivp(flat_mirror_rhs(.003,.01),(0,1.1),[initial,0,0,0],
                            method='DOP853',rtol=2e-12,atol=2e-14,max_step=.002,t_eval=sample_times)
            targets=np.array([exact.source(time) for time in sample_times])
            position_error=float(np.max(abs(targets[:,0]-timed.y[0])))
            speed_error=float(np.max(abs(targets[:,1]-np.tanh(timed.y[1]))))
            evidence.check(str(initial)+'_independent_time_vs_null_source_target',
                           timed.success and max(position_error,speed_error)<2e-8,
                           dict(position_error=position_error,velocity_error=speed_error))
        central=original.ExactLayer(6.)
        previous=ExactFlatWave(.01)
        for time in [0,.4,.8,1.1]:
            radius=np.linspace(3.,central.source(time)[0],123)
            scalar,rate,gradient=central.field(time,radius)
            before=previous.wave(time,radius)
            errors=[float(np.max(abs(scalar-before['scalar']))),
                    float(np.max(abs(rate-(before['outgoing']+before['incoming'])/(2*radius)))),
                    float(np.max(abs(gradient-(before['incoming']-before['outgoing'])/(2*radius))))]
            evidence.check(str(time)+'_independent_old_flat_field_target',max(errors)<2e-8,errors)
        for gram in [False,True]:
            branch='MTS' if gram else 'reference'
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                result=original.run_case(evidence,257,gram,max_step_factor=.05,tag='-half-step')
            result['role']='half_step_control'
            for item in caught:
                evidence.report['warnings'].append(dict(category=item.category.__name__,message=str(item.message),
                                                       filename=item.filename,line=item.lineno))
            old_raw=intake/'annular-moving-collar-flat-attempt01'/(branch+'-257.npz')
            new_raw=evidence.output/(branch+'-257-half-step.npz')
            evidence.own(old_raw)
            before=np.load(old_raw)
            after=np.load(new_raw)
            difference=float(np.max(abs(before['states']-after['states'])))
            evidence.check(branch+'_independent_half_step_state_difference',difference<2e-9,difference)
        for gram in [False,True]:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                original.run_case(evidence,8193,gram)
            for item in caught:
                evidence.report['warnings'].append(dict(category=item.category.__name__,message=str(item.message),
                                                       filename=item.filename,line=item.lineno))
            evidence.save()
        for branch in ['reference','MTS']:
            rows=[row for row in evidence.report['cases'] if row['branch']==branch and row.get('role')!='half_step_control']
            evidence.check(branch+'_last_three_grids_refine',
                           all(rows[index][key]<rows[index-1][key] for index in [-2,-1] for key in
                               ['max_wave_error','max_scalar_error','max_position_error','max_velocity_error']))
            evidence.check(branch+'_finest_original_accuracy_gates',
                           all(rows[-1][key]<threshold for key,threshold in evidence.report['gates'].items()),rows[-1])
        evidence.check('no_unexplained_numeric_warnings',all(row['category']=='FutureWarning' and
                       'Input has data type int64' in row['message'] and
                       row['filename'].endswith('annular_moving_collar_sparse_20260914.py')
                       for row in evidence.report['warnings']),evidence.report['warnings'])
        evidence.report.update(finite_flat_source_and_wave_accuracy_qualified=True,
                               coupled_curved_finite_collar_evolution_completed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

