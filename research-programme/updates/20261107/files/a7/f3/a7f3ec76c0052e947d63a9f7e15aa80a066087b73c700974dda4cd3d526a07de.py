from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_matter_gravity_transport_20261001 import SourceMap, MetricPolynomial, decimal, ZERO, ONE, TWO, HALF
from decimal import Decimal, localcontext
from time import perf_counter
from mpmath import mp
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-matter-gravity-high-order-attempt01',__file__)
    verified = {}
    started,deadline = perf_counter(),perf_counter()+1800

    def own(relative,expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Invalid verifier input '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key]!=expected:
            raise RuntimeError('Changed verifier input '+relative)
        return path

    def read(relative):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned verifier input '+relative)
        if path.suffix=='.json':
            return json.loads(path.read_text())
        with np.load(path,allow_pickle=False) as archive:
            return {name:archive[name].copy() for name in archive.files}

    try:
        path = evidence.output.parent/'annular-integrated-baseline-stage-integrity-20261001.json'
        seal = json.loads(own(str(path.relative_to(evidence.root))).read_text())
        evidence.check('prior_complete',seal['state']=='complete' and not seal['mismatches'])
        for relative,expected in seal['hashes'].items():
            own(relative,expected)
        with localcontext() as context:
            context.prec = 90
            mp.dps = 105
            nodes,weights = mp.gauss_quadrature(28,'legendre')
            nodes,weights = [Decimal(str(value)) for value in nodes],[Decimal(str(value)) for value in weights]
            for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
                report_path = evidence.output.parent/('annular-matter-gravity-'+short+'-third-attempt01')/'status.json'
                report = json.loads(own(str(report_path.relative_to(evidence.root))).read_text())
                evidence.check(short+':complete',report['state']=='complete' and all(row['passed'] for row in report['checks']))
                for category in ['inputs','outputs']:
                    for relative,expected in report[category].items():
                        own(relative,expected)
                unused,action,unused2 = restore_case(evidence,verified,branch,'third',deadline)
                flow = read(str((evidence.output.parent/'annular-direct-background-coupled-current-attempt01/status.json').relative_to(evidence.root)))
                selected = next(row for row in flow['cases'] if row['branch']==branch and row['level']=='third')
                metric = MetricPolynomial(action.solver,action.solution,[0,1])
                times = [MetricPolynomial(*reconstructed_solver(read(selected['paths'][key])),[0])
                    for key in ['background_response','velocity_response']]
                mass,coupling = decimal(action.owner.source_mass),decimal(action.owner.coupling)
                for mode in ['nodal_contraction','rounded_coefficients']:
                    parent = next(row for row in report['results'] if row['summary']['mode']==mode and row['summary']['order']==20)
                    parent = read(parent['path'])
                    source = SourceMap(action.owner.layer_rule.inverse,action.source,action.velocity,mode)
                    cuts = sorted(set(metric.edges+sum([item.edges for item in times],[])+[source.lower,source.upper]))
                    labels = {cut:source.inverse(cut) for cut in cuts if source.lower<=cut<=source.upper}
                    gravity,dust = [ZERO]*3,[ZERO]*3
                    for index,(lower,upper) in enumerate(zip(cuts[:-1],cuts[1:])):
                        middle,half = (lower+upper)/TWO,(upper-lower)/TWO
                        cells = [item.cell(middle) for item in [metric]+times]
                        for node,weight in zip(nodes,weights):
                            radius = middle+half*node
                            values = metric.at(radius,cells[0])
                            time = sum((item.at(radius,cell)[0] for item,cell in zip(times,cells[1:])),ZERO)
                            value = values[1].exp()*time/(coupling*(ONE-TWO*values[0]/radius).sqrt())
                            for power in range(3):
                                gravity[power] += half*weight*value*(radius-6)**power
                        if lower in labels and upper in labels:
                            middle_label,half_label = (labels[lower]+labels[upper])/TWO,(labels[upper]-labels[lower])/TWO
                            for node,weight in zip(nodes,weights):
                                label = middle_label+half_label*node
                                radius,unused,speed = source.at(label)
                                values = metric.at(radius,cells[0])
                                geometry,lapse = ONE-TWO*values[0]/radius,values[1].exp()
                                value = mass*6*(label+HALF)*(HALF-label)*lapse*lapse*speed/(lapse*lapse-speed*speed/geometry).sqrt()
                                for power in range(3):
                                    dust[power] += half_label*weight*value*(radius-6)**power
                        if index%512==511:
                            progress = dict(branch=branch,mode=mode,index=index+1,seconds=perf_counter()-started)
                            evidence.report['progress'] = progress
                            evidence.save()
                            print(json.dumps(progress),flush=True)
                            if perf_counter()>deadline:
                                raise RuntimeError('Safe high-order verification boundary')
                    combined = [first+last for first,last in zip(gravity,dust)]
                    differences = {name:[str(value-Decimal(old)) for value,old in zip(array,parent['summary'][name])]
                        for name,array in [('gravity',gravity),('dust_label',dust),('combined',combined)]}
                    for name,values in differences.items():
                        evidence.check(branch+':'+mode+':28_vs20:'+name,max(abs(Decimal(value)) for value in values)<Decimal('1e-30'),values)
                    evidence.check(branch+':'+mode+':wrong_sign_control',abs(gravity[0]-dust[0]-combined[0])>Decimal('1e-3'))
                    evidence.check(branch+':'+mode+':nonzero_actual_remainder',abs(combined[0])>Decimal('1e-5'))
                    result = dict(branch=branch,mode=mode,order=28,precision=90,gravity=list(map(str,gravity)),
                        dust_label=list(map(str,dust)),combined=list(map(str,combined)),differences=differences,
                        valid_for_claim=False)
                    path = evidence.output/(short+'-'+mode+'.json')
                    with path.open('x') as stream:
                        stream.write(json.dumps(result,indent=2)+'\n')
                    evidence.own(path,'outputs')
                    evidence.report['cases'].append(dict(branch=branch,mode=mode,path=str(path.relative_to(evidence.root)),differences=differences))
                    evidence.save()
            evidence.report.update(seconds=perf_counter()-started,independent_label_measure=True,order20_confirmed=True,
                parent_fields_not_resolved_again=True,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
