from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_compensated_acceleration_polynomial_v2_20261001 import CompensatedPolynomial
from annular_resolved_acceleration_channels_20261001 import channel_geometry
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_support_radial_response_20260928 import gravitational_moments
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
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
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin one core')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+4200
    verified = {}

    def status(name):
        path = evidence.output.parent/name/'status.json'
        record = json.loads(path.read_text())
        evidence.own(path)
        evidence.check(name+':complete',record['state']=='complete' and all(row['passed'] for row in record['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in record[category].items():
                source = (evidence.root/relative).resolve()
                if not source.is_relative_to(evidence.root):
                    raise RuntimeError('Invalid material replay source')
                key = str(source.relative_to(evidence.root))
                if key not in verified:
                    verified[key] = hashlib.sha256(source.read_bytes()).hexdigest()
                    evidence.own(source)
                if verified[key]!=expected:
                    raise RuntimeError('Changed replay source '+relative)
        return record

    def archive(relative,keys=None):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned replay archive')
        with np.load(path,allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in (saved.files if keys is None else keys)}

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-material-rule-C2-replay.md')
        evidence.own(evidence.root/'DERIVATION-20261001-material-replay-arithmetic-binding.md')
        short = 'reference' if args.branch=='reference-reference' else 'MTS'
        probe_name = 'annular-compensated-polynomial-'+short+'-third-attempt02'
        status(probe_name)
        resolved = status('annular-compensated-C2-'+short+'-third-attempt01')
        historical = status('annular-reacted-column-sensitivity-attempt01')
        owned_case = next(row for row in historical['cases'] if row['branch']==args.branch and row['level']=='third')
        owned = archive(owned_case['paths']['response'])
        resolved_high = archive(resolved['rule_outputs'][-1]['path'])['columns']
        polynomial = object.__new__(CompensatedPolynomial)
        polynomial.coefficients = {}
        for variant in ['rounded_coefficients','parent_nodal']:
            data = archive(str((evidence.output.parent/probe_name/(variant+'-coefficients.npz')).relative_to(evidence.root)),['numerator','denominator','widths','degree'])
            polynomial.coefficients[variant] = data['numerator']
            polynomial.denominator,polynomial.widths = data['denominator'],data['widths']
        evidence.report.update(branch=args.branch,level='third',rule_outputs=[],variants=['original_material','remainder_only_rounded',
            'remainder_only_nodal','shared_kernel_rounded','shared_kernel_nodal'],github_action=False,subagents_used=False,
            historical_replay_tolerance=2e-24,physical_uncertainty_shrunk=False,valid_for_claim=False)
        with localcontext() as context:
            context.prec = 80
            restored = restore(evidence,args.branch,'third',deadline)
            evaluator,read,report = [restored[key] for key in ['evaluator','read','report']]
            action,loads = evaluator.action,restored['setup']['loads']
            live = next(row for row in report('annular-live-support-acceleration-attempt01')['cases'] if row['branch']==args.branch and row['level']=='third')
            directions = read(live['direction_path'])
            correction = read(live['paths']['projection'])['correction']
            acceleration = np.column_stack([directions['field_vertices']-correction[:,:-1],-correction[:,-1]])
            saved_response = read(live['paths']['live_response'])
            solver,solution = reconstructed_solver(saved_response)
            response = MetricResponse(solver,solution,saved_response.get('forcing'),0.,[])
            trace = PolynomialTrace(solver,solution,evaluator.anchor)
            gravity = gravitational_moments(action,response,32)
            evaluator.polynomials = {name:value for name,value in evaluator.polynomials.items() if name in ['field','rate','test','field_change']}
            edges = np.array([float(value) for value in action.edges])
            for order in [48,64]:
                points,weights = np.polynomial.legendre.leggauss(order)
                points,weights = points/2,weights/2
                weights *= 6*(points+.5)*(.5-points)
                total,compensation = np.zeros((5,4)),np.zeros((5,4))
                for label_index,(label,weight) in enumerate(zip(points,weights)):
                    partial = evidence.output/('partial-material-'+str(order)+'.npz')
                    temporary = partial.with_suffix('.npz.tmp')
                    with temporary.open('wb') as stream:
                        np.savez_compressed(stream,total=total,compensation=compensation,order=order,next_label=label_index,complete=False)
                        stream.flush()
                        os.fsync(stream.fileno())
                    temporary.replace(partial)
                    if perf_counter()>deadline:
                        raise RuntimeError('Safe material-C2 replay boundary')
                    if label_index%8==0:
                        evidence.report['progress'] = dict(order=order,next_label=label_index,seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                    row = samples(action,label,12)
                    quadrature,geometry,cardinal = row['quadrature'],row['geometry'],row['cardinal']
                    cells,local = quadrature['cells'],quadrature['local']
                    indices = np.asarray(action.mesh['elements'])[cells]
                    widths = np.diff(edges)[cells]*geometry['jacobian']
                    interpolate = lambda nodes:interpolate_nodal(nodes,indices,local,widths)[0]
                    edge = cardinal@directions['edge_vertices']
                    eta = edge[cells]*(1-local)+edge[cells+1]*local
                    field_test = interpolate(cardinal@directions['field_vertices'])
                    gradient = row['gradient']/geometry['jacobian']
                    radius,metric = geometry['radius'],geometry['metric']
                    alpha = radius**2/(geometry['lapse']*np.sqrt(metric))
                    remainder = interpolate(cardinal@acceleration[:,:-1])
                    remainder -= (geometry['displacement']*(cardinal@acceleration[:,-1])+eta)*row['gradient']/geometry['jacobian']
                    metric_change = response.values(radius)
                    metric_density = alpha*row['temporal']*(metric_change[0]/(radius*metric)-metric_change[1])
                    measure = quadrature['measure']*geometry['jacobian']
                    node_radius = action.geometry(action.knots,row['source'],label)['radius']
                    node_rate = cardinal@loads.rates[:,:-1]
                    factors = [field_test-eta*gradient]
                    for power in range(3):
                        integral = ((radius-6)**(power+1)-(row['source']-6)**(power+1))/(power+1)
                        node_integral = ((node_radius-6)**(power+1)-(row['source']-6)**(power+1))/(power+1)
                        factors.append(row['temporal']*integral-interpolate(node_rate*node_integral))
                    factors = np.array(factors)
                    labels = np.full(len(radius),label)
                    remainders = [polynomial.evaluate(variant,cells,labels,local) for variant in ['rounded_coefficients','parent_nodal']]
                    contributions = [(alpha*value*factors)@measure+(metric_density*factors)@measure for value in [remainder]+remainders]
                    contributions[0][0] = measure@((alpha*remainder+metric_density)*factors[0])
                    offsets = radius-evaluator.anchor
                    packet,active = evaluator.packet(labels,offsets,cells=cells,local=local)
                    if not active.all():
                        raise RuntimeError('Material rule includes inactive physical points')
                    values = evaluator.metric.evaluate(offsets,evaluator.metric.cells(offsets))[0]
                    shared = channel_geometry(packet,radius,values)
                    metric_change = trace.evaluate(offsets,trace.cells(offsets))[0]
                    shared_metric = shared[0]*shared[1]*(metric_change[0]/(radius*shared[2])-metric_change[1])
                    contributions += [(shared[0]*value*shared[4])@measure+(shared_metric*shared[4])@measure for value in remainders]
                    block = weight*np.array(contributions)
                    updated = total+block
                    compensation += np.where(abs(total)>=abs(block),(total-updated)+block,(block-updated)+total)
                    total = updated
                complete = total+compensation
                complete[:,1:] += gravity
                evidence.check('finite_material-'+str(order),np.isfinite(complete).all())
                historical_column = owned['coarse_columns'][2] if order==48 else owned['columns'][2]
                replay_difference = complete[0]-historical_column
                evidence.check('original_material_replay-'+str(order),np.max(abs(replay_difference))<=2e-24,replay_difference.tolist())
                pair = None if not evidence.report['rule_outputs'] else complete-np.array(evidence.report['rule_outputs'][-1]['summary']['columns'])
                output = evidence.output/('material-'+str(order)+'.npz')
                np.savez_compressed(output,columns=complete,gravity=gravity,original_replay_difference=replay_difference,
                    shared_kernel_cross=complete[3:]-resolved_high[1:],quadrature=np.array([12,order]))
                evidence.own(output,'outputs')
                summary = dict(order=order,columns=complete.tolist(),pair=None if pair is None else pair.tolist(),
                    shared_kernel_cross=(complete[3:]-resolved_high[1:]).tolist(),valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(path=str(output.relative_to(evidence.root)),summary=summary))
                evidence.save()
                print(json.dumps(summary),flush=True)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.report.update(material_rule_ablation_complete=True,seconds=perf_counter()-started,candidate_refit_performed=False)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
