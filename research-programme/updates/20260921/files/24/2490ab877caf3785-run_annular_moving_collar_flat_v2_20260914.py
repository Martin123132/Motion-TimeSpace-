from run_annular_moving_collar_flat_20260914 import run_case, EvidenceRun
import hashlib
import json


def main():
    evidence=EvidenceRun('annular-moving-collar-flat-attempt02',__file__)
    try:
        old_path=evidence.root/'source-intake/navier-stokes/20260914/annular-moving-collar-flat-attempt01/status.json'
        old=json.loads(old_path.read_text())
        evidence.check('first_underresolved_attempt_preserved',old['state']=='failed' and
                       'finest_original_accuracy_gates' in old['error'] and len(old['cases'])==10)
        evidence.own(old_path)
        for table in ['inputs','outputs']:
            for filename,digest in old[table].items():
                path=evidence.root/filename
                if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
                    raise RuntimeError('Changed first-attempt evidence: '+filename)
                evidence.own(path)
        evidence.report.update(external_force_history_prescribed=False,full_Gram_factors_retained=True,
                               finite_collar_motion_minimal_extension_assumed=True,
                               all_layers_rigidly_locked=False,gates=old['gates'],cases=old['cases'].copy(),
                               refinement_only_no_action_or_accuracy_gate_change=True)
        evidence.save()
        for gram in [False,True]:
            for count in [1025,2049,4097]:
                run_case(evidence,count,gram)
        for branch in ['reference','MTS']:
            rows=[row for row in evidence.report['cases'] if row['branch']==branch]
            evidence.check(branch+'_last_three_grids_refine',
                           all(rows[index][key]<rows[index-1][key] for index in [-2,-1] for key in
                               ['max_wave_error','max_scalar_error','max_position_error','max_velocity_error']))
            evidence.check(branch+'_finest_original_accuracy_gates',
                           all(rows[-1][key]<threshold for key,threshold in evidence.report['gates'].items()),rows[-1])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

