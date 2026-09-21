from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_horizontal_shift_step_scan_20260921 import shift_spot_scan
from annular_candidate_horizontal_shift_20260921 import CachedTangent
from annular_candidate_energy_current_20260921 import build_base
from annular_candidate_Ward_source_20260921 import probe_action
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from time import perf_counter
import contextlib
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-horizontal-shift-step-scan-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        for name in ['scripts/annular_horizontal_shift_step_scan_20260921.py',
            'DERIVATION-20260921-horizontal-shift-step-size-refinement.md']:
            evidence.own(evidence.root/name)
        prior_path = evidence.output.parent/'annular-moving-Legendre-current-final-integrity.json'
        evidence.own(prior_path)
        prior = json.loads(prior_path.read_text())
        initial_path = evidence.output.parent/'annular-candidate-horizontal-shift-attempt01/status.json'
        evidence.own(initial_path)
        initial = json.loads(initial_path.read_text())
        evidence.check('original_run_finished_before_refinement',initial['state']=='complete')
        evidence.report.update(scientific_checks=[],step_rows=[],post_failure_refinement=True,
            original_coarse_failures_preserved=[row for row in initial['scientific_checks'] if not row['passed']],
            original_action_and_tolerance_unchanged=True,github_action=False,subagents_used=False)
        def owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key,prior['outputs'].get(key))
            evidence.check(path.name+'_sealed',expected is not None and hashlib.sha256(path.read_bytes()).hexdigest()==expected)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}
        def scientific(case,quantity,passed,value):
            evidence.report['scientific_checks'].append(dict(case=case,quantity=quantity,passed=bool(passed),
                value=float(value),valid_for_claim=False))
        replays = owned(evidence.output.parent/'annular-candidate-reaction-balance-attempt02/status.json')['replays']
        steps = np.array([.001,.0005,.00025,.000125,.0000625,.00003125])
        for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            name = branch+'-'+extension
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            original = owned(evidence.output.parent/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(evidence.output.parent/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(evidence.output.parent/'annular-complete-frozen-candidate-attempt01'/(name+'-action.json'))
            owner,unused,unused_rates = common_material(native,original,overlay)
            selected = [row for row in replays if row['branch']==branch and row['extension']==extension and row['label']=='endpoint-wide']
            states = {(row['index'],row['sign']):owned(evidence.root/row['source_path']) for row in selected}
            archives = {(row['index'],row['sign']):owned(evidence.root/row['replay_path']) for row in selected}
            loads,action = build_base(owner,overlay['overlay'],packet,extension,states[-1,0],archives[-1,0],deadline)
            probes = {key:probe_action(action,states[key],archives[key]) for key in states if key!=(-1,0)}
            system = owned(evidence.output.parent/'annular-moving-Legendre-current-attempt01'/(name+'-system.npz'))
            tangent = CachedTangent(probes,system['steps'])
            for label in [-.31,0.,.27]:
                case = name+'-label'+str(label)
                raw = shift_spot_scan(action,loads,tangent,states[-1,0],system['archived_acceleration'][-1],label,0,steps)
                old_path = evidence.output.parent/'annular-candidate-horizontal-shift-attempt01'/(case+'-profile0-shift.npz')
                evidence.own(old_path)
                with np.load(old_path,allow_pickle=False) as archive:
                    old = {key:archive[key].copy() for key in archive.files}
                evidence.check(case+'_coarse_data_unchanged',np.array_equal(raw['values'][:2],old['values'])
                    and np.array_equal(raw['raw'],old['raw']) and np.array_equal(raw['finite'][0],old['finite']))
                path = evidence.output/(case+'-scan.npz')
                np.savez_compressed(path,**raw)
                evidence.own(path,'outputs')
                for index,sector in enumerate(['wave','Gram','dust']):
                    tolerance = (2e-18 if sector=='Gram' else 2e-12)+2e-7*abs(raw['raw'][index])
                    scientific(case,sector+'_finest_original_tolerance',raw['error'][-1,index]<=tolerance,raw['error'][-1,index])
                    for level in range(len(steps)-1):
                        evidence.report['step_rows'].append(dict(branch=branch,extension=extension,label=label,sector=sector,
                            coarse_step=float(steps[level]),fine_step=float(steps[level+1]),raw=float(raw['raw'][index]),
                            estimate=float(raw['finite'][level,index]),error=float(raw['error'][level,index]),tolerance=float(tolerance),
                            passed=bool(raw['error'][level,index]<=tolerance),valid_for_claim=False))
                if branch=='MTS':
                    ratios = raw['error'][:2,1]/raw['error'][1:3,1]
                    for index,ratio in enumerate(ratios):
                        scientific(case,'Gram_fourth_order_ratio_'+str(index),8<ratio<32,ratio)
                summary = dict(branch=branch,extension=extension,label=label,coarse_Gram_error=float(raw['error'][0,1]),
                    finest_Gram_error=float(raw['error'][-1,1]),source_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
                evidence.report['cases'].append(summary)
                evidence.report['progress'] = dict(case=case,seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(summary),flush=True)
        evidence.report.update(seconds=perf_counter()-started,refined_passed=all(row['passed'] for row in evidence.report['scientific_checks']))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],refined_passed=evidence.report['refined_passed'])),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
