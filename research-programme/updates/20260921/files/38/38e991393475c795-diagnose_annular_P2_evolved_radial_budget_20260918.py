from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_current_20260918 import EvolvingP2System, P2Material, P2Density
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
import hashlib
import json
import numpy as np


def detailed_residual(system, rates, geometry):
    points, unused = np.polynomial.legendre.leggauss(system.radial_degree+3)
    radius = (geometry.centers[:, None]+geometry.lengths[:, None]*points/2).ravel()
    density = P2Density(geometry.material, radius)
    density.update(rates)
    mass, lapse, mass_radial, lapse_radial = geometry.values(radius)
    mass_rhs, lapse_rhs = density.rhs(mass, lapse)
    mass_error, lapse_error = abs(mass_radial-mass_rhs), abs(lapse_radial-lapse_rhs)
    index = int(np.argmax(mass_error))
    interval = index//len(points)
    changed = geometry.values(radius.astype(complex)+1e-24j)
    derivative_identity = max(float(max(abs(changed[0].imag/1e-24-mass_radial))),
        float(max(abs(changed[1].imag/1e-24-lapse_radial))))
    return dict(mass_error=float(max(mass_error)), lapse_error=float(max(lapse_error)),
        worst_radius=float(radius[index]), worst_interval_length=float(geometry.lengths[interval]),
        minimum_interval_length=float(min(geometry.lengths)),
        value_at_worst=float(mass[index]), rhs_at_worst=float(mass_rhs[index]),
        offset_roundoff_scale=float(np.finfo(float).eps*system.radial_degree**2*abs(mass[index])/geometry.lengths[interval]),
        derivative_is_derivative_of_reported_geometry=derivative_identity)


def main():
    evidence = EvidenceRun('annular-P2-evolved-radial-budget-attempt01', __file__)
    try:
        evidence.report.update(no_forward_evolution=True, github_action=False, subagents_used=False,
            saved_canonical_states_unchanged=True, equations_and_physical_action_unchanged=True,
            derivative_not_replaced_by_ODE_at_query_point=True,
            full_live_P2_force_convergence_proven=False)
        folder = evidence.root/'source-intake/navier-stokes/20260914/annular-live-P2-current-evolution-attempt01'
        status = json.loads((folder/'status.json').read_text())
        evidence.own(folder/'status.json')
        evidence.check('preceding_evolution_complete', status['state'] == 'complete')
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            path = folder/(branch+'_principal.npz')
            evidence.check(branch+'_saved_state_hash', hashlib.sha256(path.read_bytes()).hexdigest() == status['outputs'][str(path.relative_to(evidence.root))])
            evidence.own(path)
            with np.load(path) as data:
                coordinates, momenta = data['states'][-1]
            baseline = None
            for method, degree, action_order, label_order in [('old',18,20,12), ('old',24,20,12),
                    ('primitive',18,20,12), ('primitive',24,20,12), ('primitive',18,32,16)]:
                system = (EvolvingP2System if method == 'old' else PrimitiveP2System)(17, gram, layer_degree=6,
                    radial_degree=degree, action_order=action_order, label_order=label_order)
                rates, geometry = system.solve(coordinates, momenta)
                forces = system.forces(coordinates, rates, geometry)
                probes = np.linspace(5.19,6.81,701)
                values = geometry.values(probes)
                if baseline is None:
                    baseline = (rates, forces, values)
                response = dict(rates=float(max(abs(rates-baseline[0]).ravel())),
                    force=float(max(abs(forces-baseline[1]).ravel())),
                    mass=float(max(abs(values[0]-baseline[2][0]))), lapse=float(max(abs(values[1]-baseline[2][1]))))
                row = dict(branch=branch, method=method, radial_degree=degree, action_order=action_order, label_order=label_order,
                    **detailed_residual(system, rates, geometry), response_to_baseline=response,
                    dense_output_node_change=getattr(geometry, 'dense_output_node_change', None))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                key=branch+method+str(degree)+str(action_order)
                evidence.check(key+'_geometry_derivative_not_faked', row['derivative_is_derivative_of_reported_geometry'] < 2e-12)
                evidence.check(key+'_same_state_small_operator_response', max(response.values()) < 2e-8, response)
                if method == 'primitive':
                    evidence.check(key+'_tightened_offgrid_radial_gate', max(row['mass_error'], row['lapse_error']) < 2e-9, row)
                    evidence.check(key+'_same_collocation_integral_equations', row['dense_output_node_change'] < 2e-13)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
