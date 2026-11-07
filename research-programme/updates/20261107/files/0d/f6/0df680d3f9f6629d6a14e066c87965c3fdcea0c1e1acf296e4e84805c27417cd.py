from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_compensated_acceleration_polynomial_v2_20261001 import CompensatedPolynomial
from annular_resolved_acceleration_channels_20261001 import channel_geometry,density_from_geometry,directions
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
from annular_candidate_energy_current_20260921 import reconstructed_solver
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import os
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=10800)
    parser.add_argument('--resume-from')
    args = parser.parse_args()
    if not 0<args.seconds<=10800:
        parser.error('Time budget outside safe range')
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin one core')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.seconds
    verified = {}

    def progress(stage):
        evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe compensated-C2 boundary')

    def verify(relative,expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Invalid compensated input '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key]!=expected:
            raise RuntimeError('Changed compensated input '+relative)
        return path

    def status(name,complete=True):
        path = (evidence.output.parent/name/'status.json').resolve()
        if path.parent.parent!=evidence.output.parent:
            raise ValueError('Invalid parent label')
        verify(str(path.relative_to(evidence.root)))
        record = json.loads(path.read_text())
        if complete:
            evidence.check(name+':complete',record['state']=='complete' and all(row['passed'] for row in record['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in record[category].items():
                verify(relative,expected)
        return record

    def archive(relative,keys=None):
        path = (evidence.root/relative).resolve()
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            raise RuntimeError('Unverified archive '+relative)
        with np.load(path,allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in (saved.files if keys is None else keys)}

    def save(name,**arrays):
        path = evidence.output/(name+'.npz')
        if path.exists():
            raise FileExistsError(path)
        np.savez_compressed(path,**arrays)
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-compensated-acceleration-polynomial.md')
        evidence.own(evidence.root/'DERIVATION-20261001-compensated-source-binding.md')
        short = 'reference' if args.branch=='reference-reference' else 'MTS'
        probe_name = 'annular-compensated-polynomial-'+short+'-third-attempt02'
        parent_name = 'annular-resolved-channels-'+short+'-third-attempt'+('01' if short=='reference' else '02')
        probe,parent = status(probe_name),status(parent_name)
        evidence.check('matched_sourced_columns',probe['branch']==parent['branch']==args.branch
            and probe['level']==parent['level']=='third' and probe['polynomial_constructed'] and parent['resolved_C2_complete'])
        evidence.report.update(branch=args.branch,level='third',rule_outputs=[],github_action=False,subagents_used=False,
            probe_parent=probe_name,resolved_parent=parent_name,old_metric_and_weights_held=True,
            parent_coefficients_not_fitted=True,inherited_flags_retained=True,valid_for_claim=False)
        resume_directory,reusable = None,{}
        if args.resume_from:
            saved_run = status(args.resume_from,False)
            evidence.check('safe_compensated_resume',saved_run['state']=='failed' and saved_run.get('error')=="RuntimeError('Safe compensated-C2 boundary')"
                and saved_run['branch']==args.branch and saved_run['probe_parent']==probe_name and saved_run['resolved_parent']==parent_name
                and all(row['passed'] for row in saved_run['checks']))
            key = str((evidence.root/'scripts/integrate_annular_compensated_C2_20261001.py').relative_to(evidence.root))
            evidence.check('identical_resume_algorithm',saved_run['inputs'][key]==evidence.report['inputs'][key])
            resume_directory = evidence.output.parent/args.resume_from
            reusable = {row['summary']['order']:row for row in saved_run['rule_outputs']}
        parent_rules = {row['summary']['order']:archive(row['path']) for row in parent['rule_outputs']}
        polynomial = object.__new__(CompensatedPolynomial)
        polynomial.coefficients = {}
        for variant in ['rounded_coefficients','parent_nodal']:
            path = evidence.output.parent/probe_name/(variant+'-coefficients.npz')
            data = archive(str(path.relative_to(evidence.root)),['numerator','denominator','widths','degree'])
            polynomial.coefficients[variant] = data['numerator']
            polynomial.denominator,polynomial.widths,polynomial.degree = data['denominator'],data['widths'],int(data['degree'])
        with localcontext() as context:
            context.prec = 80
            progress('restore-identical-quadrature')
            restored = restore(evidence,args.branch,'third',deadline)
            evaluator,read,report = [restored[key] for key in ['evaluator','read','report']]
            evidence.check('same_material_widths',np.array_equal(polynomial.widths,evaluator.widths))
            live = next(row for row in report('annular-live-support-acceleration-attempt01')['cases'] if row['branch']==args.branch and row['level']=='third')
            owner = report('annular-wave-flux-live-response-third-attempt01')
            case = next(row for row in owner['cases'] if row['summary']['branch']==args.branch)
            uncertainty = read(case['paths']['sensitivity'])
            metric_uncertainty = dict(edges=uncertainty['edges'])
            metric_uncertainty.update({name:uncertainty['metric_'+name] for name in ['state','rhs_coefficients','primitives','left']})
            traces = []
            for data in [metric_uncertainty,read(live['paths']['live_response'])]:
                solver,solution = reconstructed_solver(data)
                traces.append(PolynomialTrace(solver,solution,evaluator.anchor))
            evaluator.polynomials = {name:value for name,value in evaluator.polynomials.items() if name in ['field','rate','test','field_change']}
            endpoints = np.concatenate([evaluator.geometry.geometry(evaluator.edges,label)[0] for label in [-.5,.5]])
            cuts = np.unique(np.r_[evaluator.radial_cuts,traces[0].edges,traces[1].edges,endpoints])
            lengths = np.diff(cuts)
            for order in [24,32]:
                if order in reusable:
                    evidence.report['rule_outputs'].append(reusable[order])
                    evidence.save()
                    continue
                points,weights = np.polynomial.legendre.leggauss(order)
                offsets = (cuts[:-1,None]+lengths[:,None]*(points+1)/2).ravel()
                measures = (lengths[:,None]*weights/2).ravel()
                quadrature = np.array([order,order+4,len(offsets)])
                evidence.check('same_rule-'+str(order),np.array_equal(quadrature,parent_rules[order]['quadrature']))
                node_hash = hashlib.sha256(offsets.tobytes()+measures.tobytes()).hexdigest()
                total,correction,absolute = np.zeros((4,4)),np.zeros((4,4)),np.zeros((4,4))
                next_index = 0
                partial = None if resume_directory is None else resume_directory/('partial-compensated-'+str(order)+'.npz')
                if partial is not None and partial.exists():
                    saved = archive(str(partial.relative_to(evidence.root)))
                    if bool(saved['complete']) or int(saved['order'])!=order or str(saved['node_hash'])!=node_hash:
                        raise RuntimeError('Changed compensated partial quadrature')
                    total,correction,absolute = [saved[name] for name in ['total','correction','absolute']]
                    next_index = int(saved['next_index'])
                    if any(value.shape!=(4,4) or not np.isfinite(value).all() for value in [total,correction,absolute]) or not 0<=next_index<=len(offsets) or next_index%16:
                        raise RuntimeError('Invalid compensated partial')
                for start in range(next_index,len(offsets),16):
                    if start%2048==0:
                        path = evidence.output/('partial-compensated-'+str(order)+'.npz')
                        temporary = path.with_suffix('.npz.tmp')
                        with temporary.open('wb') as stream:
                            np.savez_compressed(stream,total=total,correction=correction,absolute=absolute,
                                order=order,next_index=start,total_nodes=len(offsets),node_hash=node_hash,complete=False)
                            stream.flush()
                            os.fsync(stream.fileno())
                        temporary.replace(path)
                        progress('compensated'+str(order)+':'+str(start)+'/'+str(len(offsets)))
                    section = slice(start,start+16)
                    density = CenteredLabelDensity(evaluator.action,offsets[section],order+4)
                    selected = offsets[section][density.indices]
                    labels = density.offsets
                    packet,active = evaluator.packet(labels,selected)
                    values = evaluator.metric.evaluate(selected,evaluator.metric.cells(selected))[0]
                    geometry = channel_geometry(packet,evaluator.anchor+selected,values)
                    metric_time = traces[1].evaluate(selected,traces[1].cells(selected))[0]
                    acceleration,movement = directions(packet,'C2')
                    old_rows = density_from_geometry(evaluator.anchor+selected,geometry,acceleration,movement,metric_time)
                    old_remainder = acceleration-movement*geometry[3]
                    cells = polynomial.cells(evaluator,labels,selected)
                    rows = [old_rows[0],old_rows[1]]
                    for variant in ['rounded_coefficients','parent_nodal']:
                        remainder = polynomial.evaluate(variant,cells,labels,packet['local'])
                        rows.append(geometry[0]*(remainder-old_remainder)*geometry[4])
                    rows = np.array(rows)
                    measure = measures[section][density.indices]*density.label_weights*active
                    block = rows@measure
                    updated = total+block
                    correction += np.where(abs(total)>=abs(block),(total-updated)+block,(block-updated)+total)
                    total = updated
                    absolute += abs(rows)@measure
                accumulated = total+correction
                old_wave = accumulated[:2].sum(axis=0)
                old_column = old_wave.copy()
                old_column[1:] += parent_rules[order]['gravity'][1]
                old_difference = old_column-parent_rules[order]['complete'][1]
                replay_budget = 256*np.finfo(float).eps*(absolute[:2].sum(axis=0)+abs(old_column)+abs(parent_rules[order]['complete'][1]))
                evidence.check('held_old_column_replay-'+str(order),np.all(abs(old_difference)<=replay_budget),dict(difference=old_difference.tolist(),budget=replay_budget.tolist()))
                complete = np.array([old_column,old_column+accumulated[2],old_column+accumulated[3]])
                evidence.check('finite_compensated_columns-'+str(order),np.isfinite(np.r_[complete.ravel(),absolute.ravel()]).all())
                previous = evidence.report['rule_outputs']
                pair = None if not previous else complete-np.array(previous[-1]['summary']['columns'])
                path = save('compensated-'+str(order),columns=complete,old_replay_difference=old_difference,
                    old_replay_budget=replay_budget,accumulated=accumulated,sampled_absolute=absolute,quadrature=quadrature,node_hash=node_hash)
                summary = dict(order=order,columns=complete.tolist(),changes=accumulated[2:].tolist(),pair=None if pair is None else pair.tolist(),
                    node_hash=node_hash,valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(path=path,summary=summary))
                evidence.save()
                print(json.dumps(summary),flush=True)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.report.update(integrated_ablation_complete=True,seconds=perf_counter()-started,
            parent_coefficient_precision_proven=False,physical_uncertainty_shrunk=False)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
