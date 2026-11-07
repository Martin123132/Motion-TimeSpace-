from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_matter_gravity_transport_20261001 import SourceMap, MetricPolynomial, decimal, ZERO, ONE, TWO, HALF
from decimal import Decimal, localcontext
from time import perf_counter
from mpmath import mp
import argparse
import ctypes
import hashlib
import json
import numpy as np


def source_dust(radius, values, change, speed, speed_change, density, mass):
    geometry = ONE-TWO*values[0]/radius
    lapse = values[1].exp()
    clock_squared = lapse*lapse-speed*speed/geometry
    if geometry<=ZERO or clock_squared<=ZERO:
        raise ValueError('Invalid source chart or clock')
    clock_log_change = (lapse*lapse*change[1]-speed*speed_change/geometry
        -speed*speed*change[0]/(radius*geometry*geometry))/clock_squared
    return mass*density*lapse*lapse/clock_squared.sqrt()*(speed_change+speed*(TWO*change[1]-clock_log_change))


def densities(radius, values, mass_time, change, time_change, source, velocity_change, mass, coupling):
    geometry = ONE-TWO*values[0]/radius
    lapse = values[1].exp()
    if geometry<=ZERO:
        raise ValueError('Trapped chart')
    coefficient = lapse/(coupling*geometry.sqrt())
    coefficient_log_change = change[1]+change[0]/(radius*geometry)
    gravity = coefficient*(time_change+coefficient_log_change*mass_time)
    loading, loading_change, dust, speed, speed_change = [ZERO]*5
    if source.lower<radius<source.upper:
        label = source.inverse(radius)
        unused, jacobian, speed = source.at(label)
        speed_change = velocity_change.at(label)[2]
        density = 6*(label+HALF)*(HALF-label)/jacobian
        clock_squared = lapse*lapse-speed*speed/geometry
        if clock_squared<=ZERO:
            raise ValueError('Non-timelike source')
        loading = coupling*mass*density*geometry.sqrt()*lapse/clock_squared.sqrt()
        clock_log_change = (lapse*lapse*change[1]-speed*speed_change/geometry
            -speed*speed*change[0]/(radius*geometry*geometry))/clock_squared
        loading_change = loading*(-change[0]/(radius*geometry)+change[1]-clock_log_change)
        dust = source_dust(radius, values, change, speed, speed_change, density, mass)
    remainder = mass_time+speed*loading
    combined = coefficient*(time_change+speed_change*loading+speed*loading_change+coefficient_log_change*remainder)
    return gravity, dust, combined, combined-gravity-dust


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--branch', choices=['reference-reference','MTS-primary'], required=True)
    parser.add_argument('--cpu', type=int, choices=[2,4], required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin CPU')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    digests = {}

    def read(relative):
        path = (evidence.root/relative).resolve()
        key = str(path.relative_to(evidence.root))
        if key not in digests or hashlib.sha256(path.read_bytes()).hexdigest()!=digests[key]:
            raise RuntimeError('Changed or unowned input '+key)
        evidence.own(path)
        if path.suffix=='.json':
            return json.loads(path.read_text())
        with np.load(path,allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in saved.files}

    def report(name):
        return read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))

    def save(name,data):
        path = evidence.output/(name+'.json')
        with path.open('x') as stream:
            stream.write(json.dumps(data,indent=2)+'\n')
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-C1-integral-contract.md')
        seal_path = evidence.output.parent/'annular-matter-gravity-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('complete_parent',seal['state']=='complete' and not seal['mismatches'])
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
            digests[str(path.relative_to(evidence.root))] = expected
        evidence.check('parent_hashes_verified',len(digests)==len(seal['hashes']),len(digests))
        probe_path = evidence.output.parent/'annular-C1-coefficient-probe-attempt02/status.json'
        probe = json.loads(probe_path.read_text())
        evidence.own(probe_path)
        evidence.check('derivative_oracle_passed',probe['state']=='complete' and all(row['passed'] for row in probe['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in probe[category].items():
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed oracle '+relative)
        with localcontext() as context:
            context.prec = 70
            loads,action,sources = restore_case(evidence,digests,args.branch,'third',deadline)
            for relative in sources.values():
                evidence.own(evidence.root/relative)
            match = lambda data:next(row for row in data['cases'] if row['branch']==args.branch and row['level']=='third')
            flow = match(report('annular-direct-background-coupled-current-attempt01'))
            live = match(report('annular-live-support-acceleration-attempt01'))
            reacted = match(report('annular-old-field-reaction-attempt01'))
            time = [MetricPolynomial(*reconstructed_solver(read(flow['paths'][key])),[0])
                for key in ['background_response','velocity_response']]
            metric = MetricPolynomial(action.solver,action.solution,[0,1])
            change = MetricPolynomial(*reconstructed_solver(read(live['paths']['live_response'])),[0,1])
            changed_time = MetricPolynomial(*reconstructed_solver(read(reacted['paths']['corrected_metric_time'])),[0])
            speed_change = -read(live['paths']['projection'])['correction'][:,-1]
            mass,coupling = decimal(action.owner.source_mass),decimal(action.owner.coupling)
            maps = {mode:(SourceMap(action.owner.layer_rule.inverse,action.source,action.velocity,mode),
                SourceMap(action.owner.layer_rule.inverse,action.source,speed_change,mode))
                for mode in ['nodal_contraction','rounded_coefficients']}
            traces = [metric]+time+[change,changed_time]
            base_cuts = sorted(set(sum([item.edges for item in traces],[])))
            mp.dps = 85
            rules = {}
            for order in [12,20]:
                nodes,weights = mp.gauss_quadrature(order,'legendre')
                rules[order] = ([Decimal(str(value)) for value in nodes],[Decimal(str(value)) for value in weights])
            results = []
            evidence.report.update(branch=args.branch,level='third',precision=70,source_modes=list(maps),
                results=results,force_native_held=True,metric_time_owner='old_field_reaction',
                source_position_fixed=True,nonzero_transport_remainder_retained=True,
                github_action=False,subagents_used=False,valid_for_claim=False)
            for mode,(source,velocity_change) in maps.items():
                cuts = sorted(set(base_cuts+[source.lower,source.upper]))
                cuts = [value for value in cuts if metric.edges[0]<=value<=metric.edges[-1]]
                evidence.check(mode+':source_domain',metric.edges[0]<source.lower<source.upper<metric.edges[-1])
                evidence.check(mode+':source_monotone',source.minimum_derivative_bound>ZERO,str(source.minimum_derivative_bound))
                labels = {cut:source.inverse(cut) for cut in cuts if source.lower<=cut<=source.upper}
                for order,(nodes,weights) in rules.items():
                    totals,absolute = [[ZERO]*3 for unused in range(4)],[[ZERO]*3 for unused in range(3)]
                    maximum_identity = ZERO
                    panels = []
                    for index,(lower,upper) in enumerate(zip(cuts[:-1],cuts[1:])):
                        midpoint,half = (lower+upper)/TWO,(upper-lower)/TWO
                        cells = [item.cell(midpoint) for item in traces]
                        panel = [[ZERO]*3 for unused in range(4)]
                        for node,weight in zip(nodes,weights):
                            radius = midpoint+half*node
                            values = metric.at(radius,cells[0])
                            mass_time = sum((item.at(radius,cell)[0] for item,cell in zip(time,cells[1:3])),ZERO)
                            metric_change = change.at(radius,cells[3])
                            time_change = changed_time.at(radius,cells[4])[0]
                            gravity,dust,combined,identity = densities(radius,values,mass_time,metric_change,
                                time_change,source,velocity_change,mass,coupling)
                            maximum_identity = max(maximum_identity,abs(identity))
                            for power in range(3):
                                moment = half*weight*(radius-6)**power
                                for column,value in enumerate([gravity,dust,combined]):
                                    panel[column][power] += moment*value
                                    absolute[column][power] += abs(moment*value)
                        if lower in labels and upper in labels:
                            label_mid,label_half = (labels[lower]+labels[upper])/TWO,(labels[upper]-labels[lower])/TWO
                            for node,weight in zip(nodes,weights):
                                label = label_mid+label_half*node
                                radius,jacobian,speed = source.at(label)
                                amount = source_dust(radius,metric.at(radius,cells[0]),change.at(radius,cells[3]),
                                    speed,velocity_change.at(label)[2],6*(label+HALF)*(HALF-label),mass)
                                for power in range(3):
                                    panel[3][power] += label_half*weight*amount*(radius-6)**power
                        for column in range(4):
                            for power in range(3):
                                totals[column][power] += panel[column][power]
                        panels.append([[str(value) for value in row] for row in panel])
                        if index%128==127:
                            path = evidence.output/(mode+'-'+str(order)+'-partial.json')
                            temporary = path.with_suffix('.json.tmp')
                            temporary.write_text(json.dumps(dict(next_panel=index+1,totals=[[str(value) for value in row] for row in totals],
                                panels=panels,cuts=list(map(str,cuts)),complete=False)))
                            temporary.replace(path)
                            evidence.report['progress'] = dict(mode=mode,order=order,panel=index+1,total=len(cuts)-1,seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']),flush=True)
                            if perf_counter()>deadline:
                                raise RuntimeError('Safe C1 matter-gravity boundary')
                    transform = [totals[1][power]-totals[3][power] for power in range(3)]
                    sum_check = [totals[2][power]-totals[0][power]-totals[1][power] for power in range(3)]
                    evidence.check(mode+':point_identity-'+str(order),maximum_identity<Decimal('1e-58'),str(maximum_identity))
                    evidence.check(mode+':integral_identity-'+str(order),max(map(abs,sum_check))<Decimal('1e-58'),list(map(str,sum_check)))
                    evidence.check(mode+':independent_label_transform-'+str(order),max(map(abs,transform))<Decimal('1e-28'),list(map(str,transform)))
                    result = dict(mode=mode,order=order,panels=len(panels),gravity=list(map(str,totals[0])),
                        dust_radial=list(map(str,totals[1])),combined=list(map(str,totals[2])),
                        dust_label=list(map(str,totals[3])),label_transform=list(map(str,transform)),
                        absolute=[[str(value) for value in row] for row in absolute],maximum_identity=str(maximum_identity),
                        valid_for_claim=False)
                    path = save(mode+'-'+str(order),dict(summary=result,panels=panels,cuts=list(map(str,cuts))))
                    results.append(dict(summary=result,path=path))
                    evidence.save()
                    print(json.dumps(result),flush=True)
            evidence.report['comparisons'] = [dict(mode=mode,
                pair=[str(Decimal(high)-Decimal(low)) for low,high in zip(results[2*index]['summary']['combined'],results[2*index+1]['summary']['combined'])])
                for index,mode in enumerate(maps)]
        for path in evidence.output.glob('*-partial.json'):
            evidence.own(path,'outputs')
        evidence.report.update(seconds=perf_counter()-started,complete_integrals=True,no_continuum_precision_inferred=True)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('*-partial.json'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
