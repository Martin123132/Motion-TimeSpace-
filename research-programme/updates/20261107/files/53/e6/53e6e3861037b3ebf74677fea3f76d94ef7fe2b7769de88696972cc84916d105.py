from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from construct_annular_septic_response_20261003 import pin
import csv
import json
import numpy as np


def selected_archive(path, keys):
    with np.load(path, allow_pickle=False) as archive:
        return {key:archive[key] for key in keys}


def main():
    pin(4)
    evidence=EvidenceRun('annular-P7-bisection-analysis-attempt01',__file__)
    try:
        base='source-intake/navier-stokes/20260914/'
        evidence.report.update(refinement_rows=[],time_comparisons=[],asymptotic_convergence_proven=False,
            material_refinement_done=False,profile_refitted=False,valid_for_claim=False)
        for branch in ['primary','reference']:
            live=verify_report(evidence,base+'annular-P7-bisected-live-'+branch+'-attempt01/status.json')
            evidence.check(branch+':two_own_metric_quadrature_results',len(live['results'])==len(live['balanced_results'])==2)
            for row in live['refinement_comparisons']:
                evidence.report['refinement_rows'].append(dict(branch=branch,**row))
            if branch=='primary':
                evidence.check('all_primary_initial_gates',all(row['initial_candidate'] for row in live['results']+live['balanced_results']))
        for mode in ['product','balanced']:
            old=verify_report(evidence,base+'annular-product-source-corrected-'+mode+'-time-response-attempt01/status.json')
            new=verify_report(evidence,base+'annular-P7-bisected-'+mode+'-time-response-attempt01/status.json')
            evidence.check(mode+':same_labels_and_steps',old['labels']==new['labels'] and old['amounts']==new['amounts'])
            jets=[selected_archive(evidence.root/probe['path'],['jump','beta','auxiliary_jump']) for probe in new['probes']]
            response_path=evidence.root/base/('annular-P7-bisected-'+mode+'-time-response-attempt01')/'strong-weak-response.npz'
            evidence.own(response_path)
            response=selected_archive(response_path,['weak_before','weak_after','strong_before','strong_after'])
            derivative=[(jet['jump']-jets[0]['jump'])/amount for jet,amount in zip(jets[1:],new['amounts'])]
            measured=(4*derivative[2]-derivative[1])/3
            transfer=jets[0]['beta'][:,1:-1]*((response['weak_after']-response['weak_before'])-(response['strong_after']-response['strong_before']))
            inferred=measured-transfer
            index=np.unravel_index(np.argmax(abs(measured)),measured.shape)
            evidence.check(mode+':jump_replay',float(np.max(abs(measured)))==new['witnesses']['jump']['maximum'])
            evidence.check(mode+':weak_strong_split',float(np.max(abs(measured-inferred-transfer)))<5e-15*np.max(abs(measured)))
            path=evidence.output/(mode+'-jump-split.npz')
            np.savez_compressed(path,measured=measured,weak_strong_transfer=transfer,inferred_strong=inferred)
            evidence.own(path,'outputs')
            comparison=dict(mode=mode,witnesses=new['witnesses'],ratios={key:new['witnesses'][key]['maximum']/old['witnesses'][key]['maximum']
                    for key in ['shape','point','jump','T']},
                maximum_any_ordinary_interface_jump=max(new['witnesses']['jump']['maximum'],new['witnesses']['auxiliary_jump']['maximum']),
                old_maximum_native_jump=old['witnesses']['jump']['maximum'],
                slope_gap=new['slope_response_strong_weak_gap'],value_gap=new['value_response_strong_weak_gap'],
                old_slope_gap=old['slope_response_strong_weak_gap'],old_value_gap=old['value_response_strong_weak_gap'],
                maximum_inferred_strong_jump=float(np.max(abs(inferred))),
                at_native_jump_witness=dict(label=float(new['labels'][index[0]]),column=int(index[1]),
                    measured=float(measured[index]),weak_strong_transfer=float(transfer[index]),inferred_strong=float(inferred[index])),
                split_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
            evidence.report['time_comparisons'].append(comparison)
            evidence.save()
        path=evidence.output/'P7-refinement-comparison.csv'
        with path.open('w',encoding='utf-8',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(evidence.report['refinement_rows'][0]))
            writer.writeheader(); writer.writerows(evidence.report['refinement_rows'])
        evidence.own(path,'outputs')
        evidence.check('eight_comparison_rows',len(evidence.report['refinement_rows'])==8)
        evidence.complete()
        print(json.dumps(evidence.report['time_comparisons']),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
