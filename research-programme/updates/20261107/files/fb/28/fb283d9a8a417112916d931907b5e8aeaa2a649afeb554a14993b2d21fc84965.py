from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_resolved_acceleration_channels_20261001 import weights_and_density, directions, precise_check, channel_geometry, density_from_geometry
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import os
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--parent',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=7200)
    parser.add_argument('--resume-from')
    parser.add_argument('--probe-only',action='store_true')
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

    def progress(stage):
        evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe resolved-channel boundary')

    def save(name,**arrays):
        path = evidence.output/(name+'.npz')
        if path.exists():
            raise FileExistsError(path)
        np.savez_compressed(path,**arrays)
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-resolved-acceleration-current.md')
        evidence.own(evidence.root/'scripts/annular_resolved_acceleration_channels_20261001.py')
        evidence.report.update(branch=args.branch,level='third',rule_outputs=[],github_action=False,subagents_used=False,
            finite_history_established=False,valid_for_claim=False,uncertainty_is_rigorous_bound=False,
            historical_C2_not_overwritten=True,inherited_flags_retained=True,C0_parent=args.parent,probe_only=args.probe_only)
        parent_path = (evidence.output.parent/args.parent/'status.json').resolve()
        if parent_path.parent.parent!=evidence.output.parent:
            raise ValueError('Invalid parent')
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('completed_matched_C0',parent['state']=='complete' and parent['branch']==args.branch
            and parent['level']=='third' and parent['complete_integral_constructed'] and all(row['passed'] for row in parent['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in parent[category].items():
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed resolved-channel parent '+relative)
                evidence.own(path)
        reusable = {}
        resume_directory = None
        if args.resume_from:
            resume_directory = (evidence.output.parent/args.resume_from).resolve()
            if resume_directory.parent!=evidence.output.parent:
                raise ValueError('Invalid resolved-channel resume path')
            resume_status = resume_directory/'status.json'
            saved_run = json.loads(resume_status.read_text())
            evidence.own(resume_status)
            evidence.check('safe_resolved_resume',saved_run['state']=='failed'
                and saved_run['error']=="RuntimeError('Safe resolved-channel boundary')"
                and saved_run['branch']==args.branch and saved_run['C0_parent']==args.parent
                and all(row['passed'] for row in saved_run['checks']))
            own_key = str((evidence.root/'scripts/integrate_annular_resolved_channels_20261001.py').relative_to(evidence.root))
            evidence.check('identical_resume_algorithm',saved_run['inputs'][own_key]==evidence.report['inputs'][own_key])
            for category in ['inputs','outputs']:
                for relative,expected in saved_run[category].items():
                    path = (evidence.root/relative).resolve()
                    if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed resolved-channel resume input '+relative)
                    evidence.own(path)
            reusable = {row['summary']['order']:row for row in saved_run['rule_outputs']}
            evidence.report['resumed_from'] = args.resume_from
        alpha,beta,temporal,gradient,delta_alpha_t,delta_temporal_t,integral,weighted = sp.symbols(
            'alpha beta temporal gradient delta_alpha_t delta_temporal_t integral weighted',nonzero=True)
        energy = (alpha*temporal**2+beta*gradient**2)/2
        delta_energy_dot = (delta_alpha_t*temporal**2-beta*delta_alpha_t*gradient**2/alpha)/2+alpha*temporal*delta_temporal_t
        delta_momentum = delta_alpha_t*temporal+alpha*delta_temporal_t
        original = -delta_momentum*weighted+(delta_energy_dot+delta_alpha_t*energy/alpha)*integral
        reduced = delta_momentum*(temporal*integral-weighted)
        evidence.check('exact_current_reduction',sp.simplify(original-reduced)==0)
        evidence.check('missing_logarithmic_energy_negative_control',sp.simplify(original-delta_alpha_t*energy*integral/alpha-reduced)!=0)
        with localcontext() as context:
            context.prec = 70
            restored = restore(evidence,args.branch,'third',deadline)
            evaluator,read,report = [restored[key] for key in ['evaluator','read','report']]
            live = next(row for row in report('annular-live-support-acceleration-attempt01')['cases']
                if row['branch']==args.branch and row['level']=='third')
            owner = report('annular-wave-flux-live-response-third-attempt01')
            case = next(row for row in owner['cases'] if row['summary']['branch']==args.branch)
            uncertainty = read(case['paths']['sensitivity'])
            metric_uncertainty = dict(edges=uncertainty['edges'])
            metric_uncertainty.update({name:uncertainty['metric_'+name] for name in ['state','rhs_coefficients','primitives','left']})

            def trace(archive):
                solver,solution = reconstructed_solver(archive)
                return PolynomialTrace(solver,solution,evaluator.anchor)

            traces = [trace(metric_uncertainty),trace(read(live['paths']['live_response']))]
            evaluator.polynomials['acceleration_uncertainty'] = local_polynomials(evaluator.action.mesh,
                decimals(uncertainty['acceleration_change'][:,:-1].T))[0]

            def packet_at(labels,offsets):
                packet,active = evaluator.packet(labels,offsets)
                packet['source_uncertainty'] = evaluator.action.cardinal(labels)@uncertainty['acceleration_change'][:,-1]
                return packet,active

            progress('actual-channel-oracles')
            cells = np.linspace(0,len(evaluator.widths)-1,12).astype(int)
            labels,local = np.tile([-.37,.03,.29],4),np.tile([.13,.47,.83],4)
            lower = evaluator.geometry.geometry(evaluator.edges[cells],labels)[0]
            upper = evaluator.geometry.geometry(evaluator.edges[cells+1],labels)[0]
            offsets = lower+(upper-lower)*local
            packet,active = packet_at(labels,offsets)
            values,unused,radial,unused2 = evaluator.metric.evaluate(offsets,evaluator.metric.cells(offsets))
            time = sum(item.evaluate(offsets,item.cells(offsets))[0] for item in evaluator.time_traces)
            evidence.check('oracle_points_active',active.all())
            oracle_errors = []
            for channel,item,tolerance in zip(['reaction','C2'],traces,[2e-11,2e-8]):
                delta_time = item.evaluate(offsets,item.cells(offsets))[0]
                oracle = precise_check(packet,evaluator.anchor+offsets,values,radial,time,delta_time,channel)
                actual = weights_and_density(packet,evaluator.anchor+offsets,values,*directions(packet,channel),delta_time).sum(axis=0)
                scale = max(float(np.max(abs(oracle['oracle']))),1e-300)
                relative = float(np.max(abs(actual-oracle['oracle'])))/scale
                evidence.check(channel+':96digit_identity',oracle['identity_relative']<1e-38,oracle['identity_relative'])
                evidence.check(channel+':96digit_steps',oracle['step_relative']<1e-38,oracle['step_relative'])
                evidence.check(channel+':binary64_oracle',relative<tolerance,dict(relative=relative,tolerance=tolerance))
                evidence.check(channel+':nonvacuous',scale>100*float(np.max(abs(actual-oracle['oracle']))))
                save('oracle-'+channel,actual=actual,oracle=oracle['oracle'],exact=oracle['exact'],offsets=offsets,labels=labels)
                oracle_errors.append(relative)
            if args.probe_only:
                evidence.report.update(actual_channel_oracles_complete=True,oracle_relative_errors=oracle_errors,
                    reaction_sensitivity_integrated=False,resolved_C2_complete=False,seconds=perf_counter()-started)
                evidence.complete()
                return
            evaluator.polynomials = {name:polynomial for name,polynomial in evaluator.polynomials.items()
                if name in ['field','rate','test','field_change','acceleration_uncertainty']}
            endpoints = np.concatenate([evaluator.geometry.geometry(evaluator.edges,label)[0] for label in [-.5,.5]])
            cuts = np.unique(np.r_[evaluator.radial_cuts,traces[0].edges,traces[1].edges,endpoints])
            lengths = np.diff(cuts)
            parent_rows = {row['summary']['order']:row['summary'] for row in parent['rule_outputs']}
            evidence.report['C0_parent_pair_passed'] = bool(parent['all_requested_pairs_passed'])
            for order in [24,32]:
                if order in reusable:
                    evidence.report['rule_outputs'].append(reusable[order])
                    evidence.save()
                    continue
                points,weights = np.polynomial.legendre.leggauss(order)
                offsets = (cuts[:-1,None]+lengths[:,None]*(points+1)/2).ravel()
                measures = (lengths[:,None]*weights/2).ravel()
                total,correction,absolute = np.zeros((2,2,4)),np.zeros((2,2,4)),np.zeros((2,2,4))
                next_index = 0
                partial = None if resume_directory is None else resume_directory/('partial-channels-'+str(order)+'.npz')
                if partial is not None and partial.exists():
                    key = str(partial.relative_to(evidence.root))
                    if key not in evidence.report['inputs']:
                        raise RuntimeError('Unowned channel partial')
                    with np.load(partial,allow_pickle=False) as saved:
                        if bool(saved['complete']) or int(saved['order'])!=order or int(saved['total_nodes'])!=len(offsets):
                            raise RuntimeError('Mismatched partial quadrature')
                        total,correction,absolute = [saved[name].copy() for name in ['total','correction','absolute']]
                        next_index = int(saved['next_index'])
                    if any(value.shape!=(2,2,4) or not np.isfinite(value).all() for value in [total,correction,absolute]):
                        raise RuntimeError('Invalid channel accumulator')
                    if not 0<=next_index<=len(offsets) or next_index%16:
                        raise RuntimeError('Invalid channel block boundary')
                for start in range(next_index,len(offsets),16):
                    if start%2048==0:
                        path = evidence.output/('partial-channels-'+str(order)+'.npz')
                        temporary = path.with_suffix('.npz.tmp')
                        with temporary.open('wb') as stream:
                            np.savez_compressed(stream,total=total,correction=correction,absolute=absolute,
                                next_index=start,order=order,total_nodes=len(offsets),complete=False)
                            stream.flush()
                            os.fsync(stream.fileno())
                        temporary.replace(path)
                        progress('resolved'+str(order)+':'+str(start)+'/'+str(len(offsets)))
                    section = slice(start,start+16)
                    density = CenteredLabelDensity(evaluator.action,offsets[section],order+4)
                    selected = offsets[section][density.indices]
                    packet,active = packet_at(density.offsets,selected)
                    values = evaluator.metric.evaluate(selected,evaluator.metric.cells(selected))[0]
                    measure = measures[section][density.indices]*density.label_weights*active
                    geometry = channel_geometry(packet,evaluator.anchor+selected,values)
                    for channel_index,(channel,item) in enumerate(zip(['reaction','C2'],traces)):
                        delta_time = item.evaluate(selected,item.cells(selected))[0]
                        rows = density_from_geometry(evaluator.anchor+selected,geometry,*directions(packet,channel),delta_time)
                        block = rows@measure
                        updated = total[channel_index]+block
                        correction[channel_index] += np.where(abs(total[channel_index])>=abs(block),
                            (total[channel_index]-updated)+block,(block-updated)+total[channel_index])
                        total[channel_index] = updated
                        absolute[channel_index] += abs(rows)@measure
                selected = (offsets>=evaluator.metric.edges[0])&(offsets<=evaluator.metric.edges[-1])
                radius = evaluator.anchor+offsets[selected]
                values = evaluator.metric.evaluate(offsets[selected],evaluator.metric.cells(offsets[selected]))[0]
                coefficient = np.exp(values[1])/(evaluator.action.owner.coupling*np.sqrt(1-2*values[0]/radius))
                gravity = []
                for item in traces:
                    temporal_mass = item.evaluate(offsets[selected],item.cells(offsets[selected]))[0][0]
                    gravity.append([measures[selected]@(coefficient*temporal_mass*(radius-6)**power) for power in range(3)])
                gravity = np.array(gravity)
                complete = (total+correction).sum(axis=1)
                complete[:,1:] += gravity
                evidence.check('finite_channels-'+str(order),np.isfinite(np.r_[complete.ravel(),absolute.ravel()]).all())
                previous = evidence.report['rule_outputs']
                difference = None if not previous else complete-np.array(previous[-1]['summary']['channels'])
                path = save('channels-'+str(order),complete=complete,fixed_and_metric=total+correction,gravity=gravity,
                    sampled_absolute_wave=absolute,quadrature=np.array([order,order+4,len(offsets)]))
                summary = dict(order=order,channels=complete.tolist(),pair=None if difference is None else difference.tolist(),
                    valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(summary=summary,path=path))
                evidence.save()
                print(json.dumps(summary),flush=True)
            low,high = [np.array(row['summary']['channels']) for row in evidence.report['rule_outputs']]
            c0_pair = abs(np.array(parent_rows[32]['C0'])-np.array(parent_rows[24]['C0']))
            reaction_pair = abs(high[0]-low[0])
            evidence.report.update(reaction_sensitivity_integrated=True,reaction_quadrature_difference=reaction_pair.tolist(),
                diagnostic_C0_budget=(c0_pair+abs(high[0])+reaction_pair).tolist(),
                diagnostic_C0_budget_passed=bool(np.max(c0_pair+abs(high[0])+reaction_pair)<=2e-17),
                C2_resolved_pair=abs(high[1]-low[1]).tolist(),oracle_relative_errors=oracle_errors,
                resolved_C2_complete=True,seconds=perf_counter()-started)
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
