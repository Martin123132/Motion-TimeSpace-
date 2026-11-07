from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_stable_current_20260930 import stable_density_rows
from annular_C0_stable_transport_identity_20260930 import stable_identity_rows
from annular_C0_force_product_rule_20260930 import force_packet, analytic_force
from annular_C0_material_integral_v3_20260930 import metric_traces, base_kinematics, decimal_density
from annular_C0_boundary_integral_v2_20260930 import native_coefficient_rows, metric_beta_jump, dust_event_atoms
from annular_position_support_column_20260930 import native_position_probe, native_rows, dust_rows, dust_position_column, gravity_position_rows
from annular_native_tangent_precision_repair_20260929 import repair_engine
from annular_physical_native_kernel_20260928 import decimals
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from probe_annular_C0_precise_transport_20260930 import precise_probe
from scipy.fft import dct
from mpmath import mp
from decimal import Decimal, localcontext
from pathlib import Path
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import os
import numpy as np


def material_rows(evaluator, packet, offsets):
    amount = 1e-25j
    values, value_r, radial, radial_r = evaluator.metric.evaluate(offsets, evaluator.metric.cells(offsets))
    positions = [item.evaluate(offsets, item.cells(offsets)) for item in evaluator.responses]
    times = [item.evaluate(offsets, item.cells(offsets)) for item in evaluator.time_traces]
    mixed = sum(item.evaluate(offsets, item.cells(offsets))[0] for item in evaluator.mixed_traces)
    movement = packet['movement_left']+(packet['movement_right']-packet['movement_left'])*packet['local']
    dilation = (packet['movement_right']-packet['movement_left'])/packet['width']
    return stable_density_rows(packet, evaluator.anchor+offsets+amount*movement,
        values+amount*(sum(item[0] for item in positions)+value_r*movement),
        radial+amount*(sum(item[2] for item in positions)+radial_r*movement),
        sum(item[0] for item in times)+amount*(mixed+sum(item[1] for item in times)*movement),
        amount, material=True)*(1+amount*dilation)


def integrate_wave(evaluator, metric_time, order, evidence, progress, save):
    totals = {name:np.zeros(size) for name, size in [('base',4), ('volume',4), ('atoms',4), ('force',1)]}
    corrections = {name:np.zeros_like(value) for name, value in totals.items()}

    def deposit(name, block):
        updated = totals[name]+block
        corrections[name] += np.where(abs(totals[name]) >= abs(block), (totals[name]-updated)+block, (block-updated)+totals[name])
        totals[name] = updated

    def checkpoint(phase, index):
        path = evidence.output/('partial-wave-'+str(order)+'.npz')
        temporary = path.with_suffix('.npz.tmp')
        with temporary.open('wb') as stream:
            np.savez_compressed(stream, **{'total_'+name:value for name,value in totals.items()},
                **{'correction_'+name:value for name,value in corrections.items()},
                phase=phase, next_index=index, order=order, complete=False)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
        progress('wave'+str(order)+':'+phase+':'+str(index))

    endpoints = np.concatenate([evaluator.geometry.geometry(evaluator.edges, label)[0] for label in [-.5,.5]])
    cuts = np.unique(np.r_[evaluator.radial_cuts,endpoints])
    points, weights = np.polynomial.legendre.leggauss(order)
    lengths = np.diff(cuts)
    radii = (cuts[:-1,None]+lengths[:,None]*(points+1)/2).ravel()
    measures = (lengths[:,None]*weights/2).ravel()
    for start in range(0,len(radii),16):
        if start % 2048 == 0:
            checkpoint('volume',start)
        section = slice(start,start+16)
        density = CenteredLabelDensity(evaluator.action,radii[section],order+4)
        offsets = radii[section][density.indices]
        packet, active = evaluator.packet(density.offsets,offsets)
        rows = material_rows(evaluator,packet,offsets)
        measure = measures[section][density.indices]*density.label_weights*active
        deposit('base',rows.real@measure)
        deposit('volume',(rows.imag/1e-25)@measure)
        deposit('force',np.array([analytic_force(*force_packet(evaluator,packet,offsets))@measure]))
    checkpoint('traces',0)
    base_traces = metric_traces(evaluator.action.solver,evaluator.action.solution,evaluator.radial_cuts,evaluator.anchor)
    time_traces = sum(metric_traces(item.solver,item.solution,evaluator.radial_cuts,evaluator.anchor)[:,0]
        for item in getattr(metric_time,'responses',(metric_time,)))
    absolute_atoms = np.zeros(4)
    for start in range(0,len(evaluator.radial_cuts),8):
        if start % 256 == 0:
            checkpoint('radial-cuts',start)
        section = slice(start,start+8)
        density = CenteredLabelDensity(evaluator.action,evaluator.radial_cuts[section],order+4)
        offsets = evaluator.radial_cuts[section][density.indices]
        packet, active = evaluator.packet(density.offsets,offsets)
        columns = np.arange(len(evaluator.radial_cuts))[section][density.indices]
        kinematics = base_kinematics(packet,evaluator.anchor+offsets)
        radius = np.array([Decimal.from_float(evaluator.anchor)+Decimal.from_float(float(value)) for value in offsets],dtype=object)
        traces = [decimal_density(kinematics,radius,base_traces[side,0][:,columns],
            base_traces[side,1][:,columns],time_traces[side][:,columns]) for side in [0,1]]
        jump = np.asarray(traces[1]-traces[0],float)
        movement = packet['movement_left']+(packet['movement_right']-packet['movement_left'])*packet['local']
        measure = density.label_weights*movement*active
        deposit('atoms',jump@measure)
        absolute_atoms += abs(jump)@abs(measure)
    result = {name:totals[name]+corrections[name] for name in totals}
    result.update(complete=result['volume']+result['atoms'],absolute_atoms=absolute_atoms,
        force_difference=result['force'][0]-result['volume'][0],quadrature=np.array([order,order+4,len(radii)]))
    path = save('wave-'+str(order),**result)
    return result,path


def native_events(precision,directions,geometry,evidence,progress,save):
    engine = precision.native
    if not engine.enabled:
        return dict(atoms=np.zeros(4),absolute_atoms=np.zeros(4),events=np.array(0))
    references = geometry.references[engine.native_edges]
    cuts = precision.action.solver.edges[1:-1]-geometry.anchor
    events = []
    for index,reference in enumerate(references):
        lower,upper = [geometry.geometry(reference,label)[0] for label in [-.5,.5]]
        if upper <= lower:
            raise RuntimeError('Nonmonotone native map')
        selected = cuts[(cuts>lower)&(cuts<upper)]
        labels = geometry.inverse(selected,np.full(len(selected),reference))
        events.extend((index,float(label),float(offset)) for label,offset in zip(labels,selected))
    evidence.check('native_events_nonempty',len(events)>0,len(events))
    nodes = np.array([row[0] for row in events],int)
    labels = np.array([row[1] for row in events])
    offsets = np.array([row[2] for row in events])
    jumps_by_offset = {float(offset):np.asarray(metric_beta_jump(precision,float(offset)),float) for offset in np.unique(offsets)}
    jumps = np.array([jumps_by_offset[offset] for offset in offsets])
    error = float(np.max(abs(geometry.geometry(references[nodes],labels)[0]-offsets)))
    evidence.check('native_event_roots',error<=2e-15,error)
    save('event-locations',nodes=nodes,labels=labels,offsets=offsets,jumps=jumps)
    cache = {}

    def covectors(label):
        if label not in cache:
            data,unused,movement,unused2,unused3 = precision.packet(label,'decimal_tangents')
            beta,radial = native_coefficient_rows(engine,data,data['cardinal']@decimals(directions['field_vertices']),
                data['cardinal']@decimals(directions['edge_vertices']))
            factor = np.asarray(movement[engine.native_edges],float)*6*(label+.5)*(.5-label)/geometry.geometry(references,label)[1]
            cache[label] = np.array([beta,radial],float)*factor
        return cache[label]

    previous = None
    for degree in [16,24,32]:
        progress('native-events-degree'+str(degree))
        knots = np.cos(np.pi*np.arange(degree+1)/degree)
        coefficients = dct(np.array([covectors(float(value/2)) for value in knots]),type=1,axis=0)/degree
        coefficients[[0,-1]] /= 2
        contributions = np.zeros((4,len(events)))
        for native_index in np.unique(nodes):
            selected = np.flatnonzero(nodes==native_index)
            for component in range(2):
                interpolated = np.polynomial.chebyshev.chebval(2*labels[selected],coefficients[:,component,:,native_index])
                contributions[:,selected] += interpolated*jumps[selected,component]
        total = np.sum(contributions,axis=1)
        if previous is not None:
            error = float(np.max(abs(total-previous)))
            evidence.check('native_event_pair-'+str(degree),error<=2e-20,error)
        previous = total
        save('event-interpolation-'+str(degree),coefficients=coefficients,contributions=contributions,total=total)
    selected = np.unique(np.r_[np.linspace(0,len(events)-1,16).astype(int),np.argsort(np.max(abs(contributions),axis=0))[-8:]])
    errors = []
    for index in selected:
        direct = covectors(float(labels[index]))[:,:,nodes[index]]
        errors.append(direct[0]*jumps[index,0]+direct[1]*jumps[index,1]-contributions[:,index])
    error = float(np.max(np.abs(errors)))
    evidence.check('native_direct_event_checks',error<=2e-20,error)
    save('event-direct-checks',indices=selected,errors=np.array(errors))
    return dict(atoms=total,absolute_atoms=np.sum(abs(contributions),axis=1),events=np.array(len(events)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=10800)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    if not 0 < args.seconds <= 12600:
        parser.error('Seconds must be between zero and12600')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    output = (directory/args.label).resolve()
    if output.parent != directory or output.exists():
        parser.error('Label must be a fresh direct child of the evidence directory')
    if args.dry_run:
        print(json.dumps(dict(branch=args.branch,level='third',orders=[24,32],output=str(output),
            seconds=args.seconds,workers=1,logical_cpu=args.cpu,will_write=False)))
        return
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.seconds

    def progress(stage):
        evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe higher-grid boundary')

    def save(name,**arrays):
        path = evidence.output/(name+'.npz')
        if path.exists():
            raise FileExistsError(path)
        np.savez_compressed(path,**arrays)
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.report.update(branch=args.branch,level='third',rule_outputs=[],github_action=False,subagents_used=False,
            units='code-normalized',coupled_amplitudes_solved=False,old_failing_diagnostics_retained=True)
        evidence.own(root/'DERIVATION-20260930-C0-higher-grid-completion.md')
        seal_path = directory/'annular-C0-stable-current-stage-integrity-20260930.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('stable_parent_seal',seal['state']=='complete' and not seal['mismatches']
            and seal['stable_current_cross_checks_pass'] and seal['independent_force_both_pass'])
        for relative,expected in seal['hashes'].items():
            path = (root/relative).resolve()
            if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed higher-grid input '+relative)
            evidence.own(path)
        with localcontext() as context:
            context.prec = 70
            restored = restore(evidence,args.branch,'third',deadline)
            evaluator,setup,read,report = [restored[key] for key in ['evaluator','setup','read','report']]
            precision = repair_engine(setup['precision'])
            match = lambda status:next(row for row in status['cases'] if row['branch']==args.branch and row['level']=='third')
            live = match(report('annular-live-support-acceleration-attempt01'))
            jets = match(report('annular-position-metric-jet-validation-attempt01'))
            directions = read(live['direction_path'])
            correction = read(live['paths']['projection'])['correction']
            mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
            progress('actual-point-validation')
            cells = np.linspace(0,len(evaluator.widths)-1,24).astype(int)
            labels,local = np.tile([-.37,.03,.29],8),np.tile([.13,.47,.83],8)
            lower = evaluator.geometry.geometry(evaluator.edges[cells],labels)[0]
            upper = evaluator.geometry.geometry(evaluator.edges[cells+1],labels)[0]
            offsets = lower+(upper-lower)*local
            packet,active = evaluator.packet(labels,offsets)
            rows = material_rows(evaluator,packet,offsets).imag/1e-25
            identity = stable_identity_rows(evaluator,packet,offsets)
            evidence.check('active_actual_points',active.all())
            evidence.check('material_implementation_replay',np.array_equal(rows,identity['material']))
            relative = float(np.max(abs(identity['defect']))/max(np.max(abs(identity['material'])),1e-300))
            evidence.check('sampled_transport_identity',relative<1e-10,relative)
            mp.dps = 96
            oracle = precise_probe(evaluator,packet,offsets)[-1]
            force = analytic_force(*force_packet(evaluator,packet,offsets))
            error = float(np.max(abs(force-oracle['result'][1,0])))
            evidence.check('independent_force_oracle',oracle['relative']<1e-40 and error<2e-14*max(1.,np.max(abs(force))),error)
            evidence.check('force_probe_nonvacuous',np.max(abs(force))>100*error)
            save('actual-probes',material=rows,defect=identity['defect'],force=force,force_oracle=oracle['result'][1,0])
            wave,paths,matter,gravity = {},{},{},{}
            for order in [48,64]:
                progress('matter-'+str(order))
                labels,weights = np.polynomial.legendre.leggauss(order)
                labels,weights = labels/2,weights/2
                weights *= 6*(labels+.5)*(.5-labels)
                native_columns,dust_columns,native_base,dust_base = [],[],[],[]
                for index,label in enumerate(labels):
                    data,unused,unused2,unused3,unused4 = precision.packet(float(label),'decimal_tangents')
                    if setup['native'].enabled:
                        probe = native_position_probe(precision,mode_rate,directions,float(label),steps=())
                        native_columns.append(probe['derivative'])
                        native_base.append(probe['base'])
                        if index==0:
                            field_test = data['cardinal']@decimals(directions['field_vertices'])
                            edge_test = data['cardinal']@decimals(directions['edge_vertices'])
                            beta,radial = native_coefficient_rows(setup['native'],data,field_test,edge_test)
                            error = float(np.max(abs(beta@data['beta']+radial@data['beta_radial']-np.array(native_rows(setup['native'],data,field_test,edge_test),dtype=object))))
                            evidence.check('native_coefficient_replay-'+str(order),error<=1e-35,error)
                    else:
                        native_columns.append(np.zeros(4))
                        native_base.append(np.zeros(4))
                    source,velocity = float(data['source']),float(data['source_velocity'])
                    cardinal = np.asarray(data['cardinal'],float)
                    source_change = -float(cardinal@correction[:,-1])
                    velocity_change = float(cardinal@mode_rate[:,-1])
                    values,radial = evaluator.action.solver.values(evaluator.action.solution,np.array([source]))
                    material_values = precision.position.values(np.array([source]))[:,0]+radial[:,0]*source_change
                    dust_columns.append(dust_position_column(source,velocity,values[:,0],evaluator.action.owner.source_mass,source_change,velocity_change,material_values))
                    dust_base.append(dust_rows(source,velocity,values[:,0],evaluator.action.owner.source_mass))
                    if index%16==15:
                        progress('matter'+str(order)+':'+str(index+1))
                matter[order] = dict(native=weights@np.array(native_columns),dust=weights@np.array(dust_columns),
                    native_base=weights@np.array(native_base),dust_base=weights@np.array(dust_base))
                paths['matter'+str(order)] = save('matter-'+str(order),**matter[order],labels=labels,weights=weights,
                    native_layers=np.array(native_columns),dust_layers=np.array(dust_columns))
                evidence.report['component_paths'] = paths.copy()
                evidence.save()
            progress('coefficient-events')
            events = native_events(precision,directions,evaluator.geometry,evidence,progress,save)
            dust_events = dust_event_atoms(precision,evaluator.geometry)
            paths['events'] = save('events',**{'native_'+key:value for key,value in events.items()},
                **{'dust_'+key:value for key,value in dust_events.items()})
            for order in [24,32]:
                progress('gravity-'+str(order))
                gravity[order] = gravity_position_rows(evaluator.action,precision.position,restored['metric_time'],restored['mixed'],order)
                paths['gravity'+str(order)] = save('gravity-'+str(order),**gravity[order])
            evidence.report['component_paths'] = paths.copy()
            evidence.save()
            for order,matter_order in [(24,48),(32,64)]:
                wave[order],paths['wave'+str(order)] = integrate_wave(evaluator,restored['metric_time'],order,evidence,progress,save)
                full = wave[order]['complete']+matter[matter_order]['native']+events['atoms']
                full[1:] += matter[matter_order]['dust']+dust_events['atoms']+gravity[order]['column']
                baseline = wave[order]['base']+matter[matter_order]['native_base']
                baseline[1:] += matter[matter_order]['dust_base']+gravity[order]['base']
                independent_difference = float(wave[order]['force_difference'])
                independent_force = full[0]+independent_difference
                evidence.check('finite-full-'+str(order),np.isfinite(np.r_[full,baseline,independent_force]).all())
                previous = evidence.report['rule_outputs']
                pair = None if not previous else full-np.array(previous[-1]['summary']['C0'])
                force_pair = None if not previous else independent_force-previous[-1]['summary']['independent_force']
                summary = dict(order=order,C0=full.tolist(),independent_force=float(independent_force),
                    independent_difference=independent_difference,independent_passed=abs(independent_difference)<=2e-17,
                    pair=None if pair is None else pair.tolist(),pair_passed=None if pair is None else bool(np.max(abs(pair))<=2e-17),
                    independent_pair=force_pair,independent_pair_passed=None if force_pair is None else bool(abs(force_pair)<=2e-17),valid_for_claim=False)
                path = save('complete-'+str(order),C0=full,baseline=baseline,independent_force=independent_force,independent_difference=independent_difference)
                evidence.report['rule_outputs'].append(dict(summary=summary,path=path))
                evidence.report['component_paths'] = paths.copy()
                evidence.save()
                print(json.dumps(summary),flush=True)
            high = evidence.report['rule_outputs'][-1]['summary']
            evidence.report.update(complete_integral_constructed=True,all_requested_pairs_passed=high['pair_passed'],
                independent_force_both_orders_passed=all(row['summary']['independent_passed'] for row in evidence.report['rule_outputs']),
                independent_force_pair_passed=high['independent_pair_passed'],native_event_count=int(events['events']),
                dust_event_count=int(dust_events['events']),seconds=perf_counter()-started,valid_for_claim=False)
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
