from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_wave_resume_20260930 import integrate_wave
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent',required=True)
    parser.add_argument('--label',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=10800)
    args = parser.parse_args()
    if not 0 < args.seconds <= 12600:
        parser.error('Invalid time budget')
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin one core')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.seconds

    def ingest(name):
        path = (evidence.output.parent/name/'status.json').resolve()
        if path.parent.parent != evidence.output.parent or not path.is_file():
            raise ValueError('Invalid evidence parent')
        report = json.loads(path.read_text())
        evidence.own(path)
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                source = (evidence.root/relative).resolve()
                if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed continuation input '+relative)
                evidence.own(source)
        return report

    def read(relative):
        path = (evidence.root/relative).resolve()
        key = str(path.relative_to(evidence.root))
        if key not in evidence.report['inputs'] or hashlib.sha256(path.read_bytes()).hexdigest()!=evidence.report['inputs'][key]:
            raise RuntimeError('Unowned continuation archive '+relative)
        with np.load(path,allow_pickle=False) as source:
            return {name:source[name].copy() for name in source.files}

    def progress(stage):
        evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe higher-grid continuation boundary')

    def save(name,**arrays):
        path = evidence.output/(name+'.npz')
        if path.exists():
            raise FileExistsError(path)
        np.savez_compressed(path,**arrays)
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        parent = ingest(args.parent)
        validation = ingest('annular-C0-wave-resume-validation-attempt01')
        evidence.check('resume_validation',validation['state']=='complete' and all(row['passed'] for row in validation['checks']))
        evidence.check('safe_saved_parent',parent['branch']==args.branch and parent['level']=='third'
            and parent['state']=='failed' and 'Safe higher-grid' in parent['error']
            and all(row['passed'] for row in parent['checks']))
        evidence.report.update(branch=args.branch,level='third',rule_outputs=[],github_action=False,subagents_used=False,
            units='code-normalized',coupled_amplitudes_solved=False,reused_parent=args.parent)
        paths = parent['component_paths'].copy()
        evidence.report['component_paths'] = paths.copy()
        with localcontext() as context:
            context.prec = 70
            restored = restore(evidence,args.branch,'third',deadline)
            events = read(paths['events'])
            for order,matter_order in [(24,48),(32,64)]:
                if 'wave'+str(order) in paths:
                    wave = read(paths['wave'+str(order)])
                else:
                    partial = evidence.output.parent/args.parent/('partial-wave-'+str(order)+'.npz')
                    if partial.exists():
                        read(str(partial.relative_to(evidence.root)))
                    wave,paths['wave'+str(order)] = integrate_wave(restored['evaluator'],restored['metric_time'],
                        order,evidence,progress,save,resume=partial if partial.exists() else None)
                matter,gravity = read(paths['matter'+str(matter_order)]),read(paths['gravity'+str(order)])
                full = wave['complete']+matter['native']+events['native_atoms']
                full[1:] += matter['dust']+events['dust_atoms']+gravity['column']
                baseline = wave['base']+matter['native_base']
                baseline[1:] += matter['dust_base']+gravity['base']
                difference = float(wave['force_difference'])
                force = float(full[0]+difference)
                evidence.check('finite-full-'+str(order),np.isfinite(np.r_[full,baseline,force]).all())
                previous = evidence.report['rule_outputs']
                pair = None if not previous else full-np.array(previous[-1]['summary']['C0'])
                force_pair = None if not previous else force-previous[-1]['summary']['independent_force']
                summary = dict(order=order,C0=full.tolist(),independent_force=force,independent_difference=difference,
                    independent_passed=abs(difference)<=2e-17,pair=None if pair is None else pair.tolist(),
                    pair_passed=None if pair is None else bool(np.max(abs(pair))<=2e-17),independent_pair=force_pair,
                    independent_pair_passed=None if force_pair is None else abs(force_pair)<=2e-17,valid_for_claim=False)
                path = save('complete-'+str(order),C0=full,baseline=baseline,independent_force=force,independent_difference=difference)
                evidence.report['rule_outputs'].append(dict(summary=summary,path=path))
                evidence.report['component_paths'] = paths.copy()
                evidence.save()
                print(json.dumps(summary),flush=True)
        high = evidence.report['rule_outputs'][-1]['summary']
        evidence.report.update(complete_integral_constructed=True,all_requested_pairs_passed=high['pair_passed'],
            independent_force_both_orders_passed=all(row['summary']['independent_passed'] for row in evidence.report['rule_outputs']),
            independent_force_pair_passed=high['independent_pair_passed'],seconds=perf_counter()-started,valid_for_claim=False)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
