from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_force_product_rule_20260930 import force_packet,analytic_force
from probe_annular_C0_precise_transport_20260930 import precise_probe
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from mpmath import mp
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--parent',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=4200)
    args=parser.parse_args()
    kernel=ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot set one core')
    evidence=EvidenceRun(args.label,__file__)
    started,deadline=perf_counter(),perf_counter()+args.seconds
    try:
        evidence.report.update(branch=args.branch,level='fine',rule_outputs=[],github_action=False,
            new_physical_parameter=False,valid_for_claim=False,complete_C0_accepted=False)
        evidence.own(evidence.root/'DERIVATION-20260930-C0-independent-force-check.md')
        parent_path=evidence.output.parent/args.parent/'status.json'
        parent=json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('matched_stable_parent',parent['state']=='complete' and parent['branch']==args.branch
            and parent['material_pair_passed'] and all(row['passed'] for row in parent['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in parent[category].items():
                source=(evidence.root/relative).resolve()
                if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed product-rule input '+relative)
                evidence.own(source)
        mp.dps=96
        with localcontext() as context:
            context.prec=70
            restored=restore(evidence,args.branch,'fine',deadline)
            evaluator,report,read=restored['evaluator'],restored['report'],restored['read']
            cells=np.linspace(0,len(evaluator.widths)-1,24).astype(int)
            labels=np.tile([-.37,.03,.29],8)
            local=np.tile([.13,.47,.83],8)
            lower=evaluator.geometry.geometry(evaluator.edges[cells],labels)[0]
            upper=evaluator.geometry.geometry(evaluator.edges[cells+1],labels)[0]
            offsets=lower+(upper-lower)*local
            packet,active=evaluator.packet(labels,offsets)
            force=analytic_force(*force_packet(evaluator,packet,offsets))
            oracle=precise_probe(evaluator,packet,offsets)[-1]
            expected=oracle['result'][1,0]
            error=float(np.max(abs(force-expected)))
            evidence.check('active_actual_points',active.all())
            evidence.check('96digit_force_oracle',oracle['relative']<1e-40 and error<2e-14*max(1.,np.max(abs(expected))),error)
            evidence.check('force_check_nonvacuous',np.max(abs(expected))>100*error)
            path=evidence.output/'force-probes.npz'
            np.savez_compressed(path,force=force,oracle=expected,error=force-expected,labels=labels,offsets=offsets)
            evidence.own(path,'outputs')
            endpoints=np.concatenate([evaluator.geometry.geometry(evaluator.edges,label)[0] for label in [-.5,.5]])
            cuts=np.unique(np.r_[evaluator.radial_cuts,endpoints])
            lengths=np.diff(cuts)
            for order in [24,32]:
                points,weights=np.polynomial.legendre.leggauss(order)
                radii=(cuts[:-1,None]+lengths[:,None]*(points+1)/2).ravel()
                measures=(lengths[:,None]*weights/2).ravel()
                total,correction,absolute=0.,0.,0.
                for start in range(0,len(radii),16):
                    if start%2048==0:
                        path=evidence.output/('partial-'+str(order)+'.npz')
                        with path.with_suffix('.npz.tmp').open('wb') as stream:
                            np.savez_compressed(stream,total=total,correction=correction,absolute=absolute,next_index=start,complete=False,order=order)
                        path.with_suffix('.npz.tmp').replace(path)
                        evidence.report['progress']=dict(order=order,index=start,total=len(radii),seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                        if perf_counter()>deadline:
                            raise RuntimeError('Safe product-rule boundary')
                    section=slice(start,start+16)
                    density=CenteredLabelDensity(evaluator.action,radii[section],order+4)
                    offsets=radii[section][density.indices]
                    packet,active=evaluator.packet(density.offsets,offsets)
                    rows=analytic_force(*force_packet(evaluator,packet,offsets))
                    measure=measures[section][density.indices]*density.label_weights*active
                    block=float(rows@measure)
                    updated=total+block
                    correction+=(total-updated)+block if abs(total)>=abs(block) else (block-updated)+total
                    total=updated
                    absolute+=float(abs(rows)@measure)
                parent_row=next(row for row in parent['rule_outputs'] if row['summary']['order']==order)
                with np.load(evidence.root/parent_row['path']) as archive:
                    stable_volume=float(archive['material'][0])
                    complete=float(archive['material_C0'][0])
                difference=total+correction-stable_volume
                force=complete+difference
                evidence.check('independent_force_agreement-'+str(order),np.isfinite(force) and abs(difference)<=2e-17,difference)
                previous=evidence.report['rule_outputs']
                summary=dict(order=order,force=force,stable_force=complete,independent_difference=difference,
                    paired_difference=None if not previous else force-previous[-1]['summary']['force'],
                    sampled_absolute_bulk=absolute,valid_for_claim=False)
                path=evidence.output/('force-'+str(order)+'.npz')
                np.savez_compressed(path,bulk=total+correction,complete_force=force,stable_force=complete,
                    independent_difference=difference,sampled_absolute_bulk=absolute)
                evidence.own(path,'outputs')
                evidence.report['rule_outputs'].append(dict(summary=summary,path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(summary),flush=True)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        paired=evidence.report['rule_outputs'][-1]['summary']['paired_difference']
        evidence.check('independent_force_pair',abs(paired)<=2e-17,paired)
        evidence.report.update(seconds=perf_counter()-started,independent_force_complete=True,
            shared_radial_and_native_terms_reused=True,old_Eulerian_failures_retained=True)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
