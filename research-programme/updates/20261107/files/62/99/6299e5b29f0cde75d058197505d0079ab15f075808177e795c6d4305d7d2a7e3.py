from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_matter_gravity_transport_20261001 import SourceMap, MetricPolynomial, densities, decimal, ZERO, ONE, TWO, HALF
from decimal import Decimal, localcontext
from time import perf_counter
from mpmath import mp
import argparse
import ctypes
import hashlib
import json
import numpy as np
import sympy as sp


def algebra(evidence):
    lapse,metric,clock,mass,coupling,weight,jacobian = sp.symbols('N F ell M k w J',positive=True)
    speed,time = sp.symbols('v m_t',real=True)
    coefficient = lapse/(coupling*sp.sqrt(metric))
    loading = coupling*mass*weight*sp.sqrt(metric)*lapse/(jacobian*clock)
    current = mass*weight*lapse**2*speed/(jacobian*clock)
    evidence.check('symbolic:dust_advective_identity',sp.simplify(coefficient*speed*loading-current)==0)
    combined = coefficient*(time+speed*loading)
    evidence.check('symbolic:off_shell_remainder',sp.simplify(combined-coefficient*time-current)==0)
    evidence.check('symbolic:pure_dust_control',sp.simplify(combined.subs(time,-speed*loading))==0)
    extra = sp.symbols('extra',nonzero=True)
    evidence.check('symbolic:nonzero_remainder_retained',sp.simplify(combined.subs(time,extra-speed*loading)-coefficient*extra)==0)
    amplitude,lapse_time,forcing,advective,advective_radial,remainder = sp.symbols('A lapse_time forcing advective advective_radial R')
    time_radial = amplitude*(remainder-advective)+lapse_time+forcing
    result = amplitude*remainder+lapse_time+forcing+advective_radial-amplitude*advective
    evidence.check('symbolic:remainder_radial_equation',sp.expand(time_radial+advective_radial-result)==0)
    tiny = Decimal('1e-45')
    evidence.check('manufactured:tiny_remainder_not_zeroed', (Decimal('0.03')+tiny)-Decimal('0.03')==tiny)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--seconds',type=float,default=3600)
    args = parser.parse_args()
    if not 0<args.seconds<=7200:
        parser.error('Unsafe time budget')
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin CPU')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.seconds
    digests = {}

    def read(relative):
        path = (evidence.root/relative).resolve()
        key = str(path.relative_to(evidence.root))
        if key not in digests or hashlib.sha256(path.read_bytes()).hexdigest()!=digests[key]:
            raise RuntimeError('Unowned or changed source '+key)
        evidence.own(path)
        if path.suffix=='.json':
            return json.loads(path.read_text())
        with np.load(path,allow_pickle=False) as archive:
            return {name:archive[name].copy() for name in archive.files}

    def report(name):
        return read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))

    def save(name,data):
        path = evidence.output/(name+'.json')
        if path.exists():
            raise FileExistsError(path)
        path.write_text(json.dumps(data,indent=2)+'\n')
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    def progress(phase,index,total):
        evidence.report['progress'] = dict(phase=phase,index=index,total=total,seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe matter-gravity boundary')

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-matter-gravity-transport-remainder.md')
        seal_path = evidence.output.parent/'annular-integrated-baseline-stage-integrity-20261001.json'
        evidence.own(seal_path)
        seal = json.loads(seal_path.read_text())
        evidence.check('complete_parent_seal',seal['state']=='complete' and not seal['mismatches'])
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Parent integrity failure '+relative)
            digests[str(path.relative_to(evidence.root))] = expected
        evidence.check('all_parent_hashes_unchanged',len(digests)==len(seal['hashes']),len(digests))
        with localcontext() as context:
            context.prec = 70
            algebra(evidence)
            loads,action,sources = restore_case(evidence,digests,args.branch,'third',deadline)
            for relative in sources.values():
                evidence.own(evidence.root/relative)
            flow = next(row for row in report('annular-direct-background-coupled-current-attempt01')['cases']
                if row['branch']==args.branch and row['level']=='third')
            responses = [MetricPolynomial(*reconstructed_solver(read(flow['paths'][key])),[0])
                for key in ['background_response','velocity_response']]
            metric = MetricPolynomial(action.solver,action.solution,[0,1])
            mass,coupling = decimal(action.owner.source_mass),decimal(action.owner.coupling)
            short = 'reference' if args.branch=='reference-reference' else 'MTS'
            parent = report('annular-C0-higher-'+short+'-third-attempt02')
            historical = {name:read(parent['component_paths'][name]) for name in ['matter48','matter64','gravity24','gravity32']}
            historical_rows = {str(order):dict(dust=historical['matter'+str(material)]['dust_base'].tolist(),
                gravity=historical['gravity'+str(order)]['base'].tolist()) for order,material in [(24,48),(32,64)]}
            maps = {mode:SourceMap(action.owner.layer_rule.inverse,action.source,action.velocity,mode)
                for mode in ['nodal_contraction','rounded_coefficients']}
            mp.dps = 85
            rules = {}
            for order in [12,20]:
                nodes,weights = mp.gauss_quadrature(order,'legendre')
                rules[order] = ([Decimal(str(value)) for value in nodes],[Decimal(str(value)) for value in weights])
            results = []
            evidence.report.update(branch=args.branch,source_paths=sources,historical=historical_rows,
                precision=70,results=results,source_modes=list(maps),columns_unchanged=True,
                wave_and_native_unchanged=True,metric_time_not_replaced=True,valid_for_claim=False,github_action=False,subagents_used=False)
            base_cuts = sorted(set(metric.edges+sum([item.edges for item in responses],[])))
            for mode,source in maps.items():
                cuts = sorted(set(base_cuts+[source.lower,source.upper]))
                cuts = [value for value in cuts if metric.edges[0]<=value<=metric.edges[-1]]
                evidence.check(mode+':source_inside_domain',metric.edges[0]<source.lower<source.upper<metric.edges[-1])
                evidence.check(mode+':monotone_source',source.minimum_derivative_bound>ZERO,str(source.minimum_derivative_bound))
                labels = {cut:source.inverse(cut) for cut in cuts if source.lower<=cut<=source.upper}
                for order,(nodes,weights) in rules.items():
                    totals = [[ZERO]*3 for unused in range(4)]
                    absolute = [[ZERO]*3 for unused in range(3)]
                    maximum_identity,maximum_inverse = ZERO,ZERO
                    panel_rows = []
                    for index,(lower,upper) in enumerate(zip(cuts[:-1],cuts[1:])):
                        midpoint,half = (lower+upper)/TWO,(upper-lower)/TWO
                        cells = [item.cell(midpoint) for item in [metric]+responses]
                        panel = [[ZERO]*3 for unused in range(4)]
                        for node,weight in zip(nodes,weights):
                            radius = midpoint+half*node
                            values = metric.at(radius,cells[0])
                            mass_time = sum((item.at(radius,cell)[0] for item,cell in zip(responses,cells[1:])),ZERO)
                            gravity,dust,combined,identity,remainder = densities(radius,values,mass_time,source,mass,coupling)
                            maximum_identity = max(maximum_identity,abs(identity))
                            factor = half*weight
                            offset = radius-6
                            for power in range(3):
                                moment = factor*offset**power
                                for column,value in enumerate([gravity,dust,combined]):
                                    panel[column][power] += moment*value
                                    absolute[column][power] += abs(moment*value)
                        if lower in labels and upper in labels:
                            label_mid,label_half = (labels[lower]+labels[upper])/TWO,(labels[upper]-labels[lower])/TWO
                            for node,weight in zip(nodes,weights):
                                label = label_mid+label_half*node
                                radius,jacobian,speed = source.at(label)
                                values = metric.at(radius,cells[0])
                                geometry = ONE-TWO*values[0]/radius
                                lapse = values[1].exp()
                                clock = (lapse*lapse-speed*speed/geometry).sqrt()
                                amount = mass*6*(label+HALF)*(HALF-label)*lapse*lapse*speed/clock
                                for power in range(3):
                                    panel[3][power] += label_half*weight*amount*(radius-6)**power
                        for column in range(4):
                            for power in range(3):
                                totals[column][power] += panel[column][power]
                        panel_rows.append([[str(value) for value in row] for row in panel])
                        if index%128==127:
                            partial = evidence.output/(mode+'-'+str(order)+'-partial.json')
                            temporary = partial.with_suffix('.json.tmp')
                            temporary.write_text(json.dumps(dict(mode=mode,order=order,next_panel=index+1,
                                totals=[[str(value) for value in row] for row in totals],panels=panel_rows,
                                cuts=list(map(str,cuts)),complete=False)))
                            temporary.replace(partial)
                            progress(mode+'-'+str(order),index+1,len(cuts)-1)
                    transform = [totals[1][power]-totals[3][power] for power in range(3)]
                    sum_check = [totals[2][power]-totals[0][power]-totals[1][power] for power in range(3)]
                    evidence.check(mode+':identity-'+str(order),maximum_identity<Decimal('1e-58'),str(maximum_identity))
                    evidence.check(mode+':integrated_identity-'+str(order),max(map(abs,sum_check))<Decimal('1e-58'),list(map(str,sum_check)))
                    evidence.check(mode+':independent_label_transform-'+str(order),max(map(abs,transform))<Decimal('1e-28'),list(map(str,transform)))
                    result = dict(mode=mode,order=order,panels=len(cuts)-1,
                        gravity=list(map(str,totals[0])),dust_radial=list(map(str,totals[1])),combined=list(map(str,totals[2])),
                        dust_label=list(map(str,totals[3])),label_transform=list(map(str,transform)),
                        absolute=[[str(value) for value in row] for row in absolute],maximum_identity=str(maximum_identity),valid_for_claim=False)
                    path = save(mode+'-'+str(order),dict(summary=result,panels=panel_rows,cuts=list(map(str,cuts))))
                    results.append(dict(summary=result,path=path))
                    evidence.save()
                    print(json.dumps(result),flush=True)
            comparisons = []
            for mode in maps:
                selected = [item['summary'] for item in results if item['summary']['mode']==mode]
                comparisons.append(dict(mode=mode,pair={key:[str(Decimal(last)-Decimal(first)) for first,last in zip(selected[0][key],selected[1][key])]
                    for key in ['gravity','dust_radial','combined']},valid_for_claim=False))
            evidence.report.update(comparisons=comparisons,seconds=perf_counter()-started,complete_integrals=True,
                no_continuum_precision_inferred=True)
        for path in evidence.output.glob('*-partial.json'):
            evidence.own(path,'outputs')
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('*-partial.json'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
