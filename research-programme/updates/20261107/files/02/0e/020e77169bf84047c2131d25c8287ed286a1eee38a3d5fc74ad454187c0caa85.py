from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_stable_transport_identity_20260930 import stable_identity_rows as identity_rows
from annular_C0_stable_current_20260930 import stable_density_rows
import hashlib
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from decimal import localcontext
from time import perf_counter
from math import fsum
import argparse
import ctypes
import json
import numpy as np


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=7000)
    args=parser.parse_args()
    kernel=ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin one core')
    evidence=EvidenceRun(args.label,__file__)
    started,deadline=perf_counter(),perf_counter()+args.seconds
    try:
        evidence.report.update(branch=args.branch,level='fine',github_action=False,subagents_used=False,
            diagnostic_only=True,complete_C0_accepted=False,rule_outputs=[])
        evidence.own(evidence.root/'DERIVATION-20260930-C0-stable-current.md')
        validation_path=evidence.output.parent/'annular-C0-stable-current-validation-attempt01/status.json'
        validation=json.loads(validation_path.read_text())
        evidence.own(validation_path)
        evidence.check('stable_current_validation',validation['state']=='complete' and all(row['passed'] for row in validation['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in validation[category].items():
                source=(evidence.root/relative).resolve()
                if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed stable validation source '+relative)
                evidence.own(source)
        with localcontext() as context:
            context.prec=70
            restored=restore(evidence,args.branch,'fine',deadline)
            evaluator,read,report=restored['evaluator'],restored['read'],restored['report']
            short='reference' if args.branch=='reference-reference' else 'MTS'
            material=report('annular-C0-material-'+short+'-fine-attempt01')
            euler=report('annular-C0-integral-reference-attempt01' if short=='reference'
                else 'annular-C0-integral-MTS-native-recovery-attempt02')
            original=next(row for row in euler['cases'] if row['summary']['level']=='fine')
            endpoints=np.concatenate([evaluator.geometry.geometry(evaluator.edges,label)[0] for label in [-.5,.5]])
            cuts=np.unique(np.r_[evaluator.radial_cuts,endpoints])
            lengths=np.diff(cuts)
            for order in [24,32]:
                points,weights=np.polynomial.legendre.leggauss(order)
                radii=(cuts[:-1,None]+lengths[:,None]*(points+1)/2).ravel()
                measures=(lengths[:,None]*weights/2).ravel()
                names=['material','eulerian','transport','defect']
                totals={name:np.zeros(4) for name in names}
                corrections={name:np.zeros(4) for name in names}
                absolute_defect=np.zeros(4)
                maximum_local_defect=np.zeros(4)
                for start in range(0,len(radii),16):
                    if start%2048==0:
                        state={'total_'+name:totals[name] for name in names}
                        state.update({'correction_'+name:corrections[name] for name in names})
                        state.update(next_index=np.array(start),order=np.array(order),complete=np.array(False),
                            absolute_defect=absolute_defect,maximum_local_defect=maximum_local_defect)
                        partial=evidence.output/('partial-'+str(order)+'.npz')
                        with partial.with_suffix('.npz.tmp').open('wb') as stream:
                            np.savez_compressed(stream,**state)
                        partial.with_suffix('.npz.tmp').replace(partial)
                        evidence.report['progress']=dict(order=order,index=start,total=len(radii),seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                        if perf_counter()>deadline:
                            raise RuntimeError('Safe transport integration boundary')
                    section=slice(start,start+16)
                    density=CenteredLabelDensity(evaluator.action,radii[section],order+4)
                    offsets=radii[section][density.indices]
                    packet,active=evaluator.packet(density.offsets,offsets)
                    rows=identity_rows(evaluator,packet,offsets)
                    measure=measures[section][density.indices]*density.label_weights*active
                    for name in names:
                        block=rows[name]@measure
                        updated=totals[name]+block
                        corrections[name]+=np.where(abs(totals[name])>=abs(block),(totals[name]-updated)+block,(block-updated)+totals[name])
                        totals[name]=updated
                    absolute_defect+=abs(rows['defect'])@measure
                    maximum_local_defect=np.maximum(maximum_local_defect,np.max(abs(rows['defect']),axis=1))
                totals={name:totals[name]+corrections[name] for name in names}
                old_material=read(next(row['path'] for row in material['rule_outputs'] if row['summary']['order']==order))
                old_euler=read(original['paths']['wave'+str(order)])
                face_indices,face_labels,face_measures,face_offsets=evaluator.face_rule(order+4)
                faces,outer=np.zeros(4),np.zeros(4)
                face_correction,outer_correction=np.zeros(4),np.zeros(4)
                for first in range(0,len(face_labels),2048):
                    if first%65536==0:
                        evidence.report['progress']=dict(order=order,stage='stable-faces',index=first,total=len(face_labels),seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                        if perf_counter()>deadline:
                            raise RuntimeError('Safe stable faces boundary')
                    section=slice(first,first+2048)
                    face,label,measure,offset=face_indices[section],face_labels[section],face_measures[section],face_offsets[section]
                    lower,upper=np.clip(face-1,0,len(evaluator.widths)-1),np.clip(face,0,len(evaluator.widths)-1)
                    left=evaluator.packet(label,offset,lower,np.ones(len(face)))[0]
                    right=evaluator.packet(label,offset,upper,np.zeros(len(face)))[0]
                    values,unused,radial,unused2=evaluator.metric.evaluate(offset,evaluator.metric.cells(offset))
                    time=sum(item.evaluate(offset,item.cells(offset))[0] for item in evaluator.time_traces)
                    left_rows=stable_density_rows(left,evaluator.anchor+offset,values,radial,time)
                    right_rows=stable_density_rows(right,evaluator.anchor+offset,values,radial,time)
                    inner,outer_mask=face==0,face==len(evaluator.widths)
                    movement=np.where(outer_mask,left['movement_right'],right['movement_left'])
                    block=-(right_rows-left_rows)@(measure*movement*~(inner|outer_mask))
                    updated=faces+block
                    face_correction+=np.where(abs(faces)>=abs(block),(faces-updated)+block,(block-updated)+faces)
                    faces=updated
                    block=left_rows@(measure*movement*outer_mask)-right_rows@(measure*movement*inner)
                    updated=outer+block
                    outer_correction+=np.where(abs(outer)>=abs(block),(outer-updated)+block,(block-updated)+outer)
                    outer=updated
                faces+=face_correction
                outer+=outer_correction
                material_wave=totals['material']+old_material['radial_cut_atoms']
                euler_wave=totals['eulerian']+faces+outer
                ftc=np.array([fsum([totals['transport'][component],old_material['radial_cut_atoms'][component],-faces[component],-outer[component]])
                    for component in range(4)])
                observed=material_wave-euler_wave
                closure=observed-(ftc+totals['defect'])
                parent_total=read(original['paths']['combined'])
                events=read(original['paths']['events'])
                matter=read(original['paths']['matter'+str(48 if order==24 else 64)])
                common=matter['native']+events['native_atoms']
                common[1:]+=matter['dust']+events['dust_atoms']+parent_total['gravity'+str(order)]
                material_C0,euler_C0=material_wave+common,euler_wave+common
                evidence.check('finite-'+str(order),np.isfinite(np.r_[material_C0,euler_C0,observed,closure]).all())
                evidence.check('stable_transport_decomposition-'+str(order),np.max(abs(closure))<=2e-17,closure.tolist())
                path=evidence.output/('stable-'+str(order)+'.npz')
                np.savez_compressed(path,**totals,ftc_defect=ftc,cross_difference=observed,closure=closure,
                    material_C0=material_C0,euler_C0=euler_C0,material_wave=material_wave,euler_wave=euler_wave,
                    faces=faces,outer=outer,radial_cut_atoms=old_material['radial_cut_atoms'],
                    old_material_shift=material_C0-old_material['full_C0'],old_euler_shift=euler_wave-old_euler['complete'],
                    sampled_absolute_identity_defect=absolute_defect,maximum_local_identity_defect=maximum_local_defect)
                evidence.own(path,'outputs')
                previous=evidence.report['rule_outputs']
                summary=dict(order=order,material_C0=material_C0.tolist(),euler_C0=euler_C0.tolist(),
                    cross_difference=observed.tolist(),cross_passed=bool(np.max(abs(observed))<=2e-17),
                    material_pair=None if not previous else (material_C0-np.asarray(previous[-1]['summary']['material_C0'])).tolist(),
                    euler_pair=None if not previous else (euler_C0-np.asarray(previous[-1]['summary']['euler_C0'])).tolist(),
                    sampled_absolute_defect=absolute_defect.tolist(),valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(summary=summary,path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(summary),flush=True)

        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        high=evidence.report['rule_outputs'][-1]['summary']
        evidence.report.update(seconds=perf_counter()-started,stable_integration_complete=True,
            material_pair_passed=bool(np.max(np.abs(high['material_pair']))<=2e-17),
            euler_pair_passed=bool(np.max(np.abs(high['euler_pair']))<=2e-17),
            both_cross_comparisons_passed=all(row['summary']['cross_passed'] for row in evidence.report['rule_outputs']),
            inherited_native_source_gravity_and_radial_atoms_reused=True,valid_for_claim=False)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
