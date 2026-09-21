from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System, PrimitiveP2Geometry
from annular_live_P2_current_20260918 import P2Material
from run_annular_P2_continuum_bridge_20260918 import checked_load
import argparse
import hashlib
import json
import numpy as np


def trace_pressure(system, coordinates, rates, geometry):
    material = P2Material(system, coordinates)
    interpolation = material.interpolation([0.])[0]
    values, velocity = interpolation @ coordinates, interpolation @ rates
    layer = system.layer(0., geometry)
    source_edge = np.searchsorted(layer.edges, layer.anchor)
    gradients = []
    for element, derivative in [(source_edge-1, np.array([1.,-4.,3.])),
            (source_edge, np.array([-3.,4.,-1.]))]:
        indices = layer.element_indices[element]
        valid = indices >= 0
        reference_length = layer.edges[element+1]-layer.edges[element]
        middle = (layer.edges[element+1]+layer.edges[element])/2
        unused, jacobian, unused2 = layer.mapping(middle, values[-1])
        gradients.append(float(derivative[valid] @ values[:-1][indices[valid]]/(reference_length*jacobian)))
    lapse, root = geometry.metric(values[-1])
    coefficient = float(values[-1]**2*lapse*root*(1-(velocity[-1]/(lapse*root))**2)/2)
    pressure = coefficient*(gradients[0]**2-gradients[1]**2)
    return dict(one_sided_gradients=gradients, pressure_coefficient=coefficient, finite_trace_pressure=float(pressure))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counts', nargs='+', type=int, default=[17,33,65])
    args = parser.parse_args()
    tag = '-'.join(map(str,args.counts))
    evidence = EvidenceRun('annular-P2-traction-gap-'+tag+'-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            finite_action_force_not_replaced_with_trace_pressure=True,
            defect_definition='r_h=F_h-P_h; F_h-F_ref=r_h+(P_h-F_ref)',
            continuum_trace_law_not_assumed_exact_at_finite_resolution=True,
            full_live_P2_force_convergence_proven=False, force_labels=[0.], width=.02, duration=.004)
        for count in args.counts:
            comparison_folder = evidence.output.parent/('annular-P2-continuum-comparison-'+str(count)+'-attempt01')
            status = json.loads((comparison_folder/'status.json').read_text())
            evidence.own(comparison_folder/'status.json')
            evidence.check(str(count)+'_comparison_execution_complete', status['state'] == 'complete')
            for branch in ['reference','MTS']:
                key = branch+'-'+str(count)
                path = comparison_folder/(key+'.json')
                evidence.check(key+'_force_data_hash', hashlib.sha256(path.read_bytes()).hexdigest()
                    == status['outputs'][str(path.relative_to(evidence.root))])
                evidence.own(path)
                measured = json.loads(path.read_text())
                if count == 17:
                    data = checked_load(evidence, 'annular-P2-tight-budget-'+branch+'-attempt01', 'principal.npz')
                else:
                    data = checked_load(evidence, 'annular-P2-continuum-bridge-'+key+'-attempt01', 'trajectory.npz')
                system = PrimitiveP2System(count, branch == 'MTS', layer_degree=14, radial_degree=18, action_order=32, label_order=20)
                states = data['states'].reshape(5,2,len(system.labels),system.count+1)
                rows = []
                for time, state, rates, observed in zip(data['times'],states,data['rates'],measured['times']):
                    if time != observed['time']:
                        raise ValueError('Force and state timestamps differ.')
                    coordinates, momenta = state
                    geometry = PrimitiveP2Geometry(system, P2Material(system,coordinates), rates)
                    row = trace_pressure(system,coordinates,rates,geometry)
                    force, reference = observed['force']['reduced_wave_force'], observed['continuum_wave_force']
                    pressure = row['finite_trace_pressure']
                    row.update(time=float(time), finite_action_force=force, reference_force=reference,
                        finite_action_traction_defect=force-pressure, trace_and_geometry_difference=pressure-reference,
                        signed_total_force_error=force-reference)
                    error = abs(row['signed_total_force_error']-row['finite_action_traction_defect']-row['trace_and_geometry_difference'])
                    evidence.check(key+'_signed_force_decomposition_'+str(time), error < 1e-15, error)
                    rows.append(row)
                summary = dict(key=key, base_count=count, branch=branch,
                    maximum_action_traction_defect=max(abs(row['finite_action_traction_defect']) for row in rows),
                    maximum_trace_geometry_difference=max(abs(row['trace_and_geometry_difference']) for row in rows),
                    maximum_total_force_error=max(abs(row['signed_total_force_error']) for row in rows),
                    final_action_traction_defect=rows[-1]['finite_action_traction_defect'],
                    final_trace_geometry_difference=rows[-1]['trace_and_geometry_difference'])
                destination = evidence.output/(key+'.json')
                destination.write_text(json.dumps(dict(summary=summary,times=rows),indent=2,allow_nan=False)+'\n',encoding='utf-8')
                evidence.own(destination,'outputs')
                evidence.report['cases'].append(summary)
                evidence.save()
                print(summary,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
