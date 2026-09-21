from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_live_radial_response_20260918 import SnapshotLoads, bump
from annular_live_radial_response_v2_20260918 import RadialResponse
from copy import copy
import hashlib
import json
import numpy as np
import sympy as sp


class PotentialResponse(RadialResponse):
    def __init__(self, loads, potential):
        self.potential = potential
        augmented = copy(loads)
        augmented.edges = np.unique(np.concatenate([loads.edges, [potential[0]-potential[1], potential[0]+potential[1]]]))
        super().__init__(augmented, tight=True)

    def coefficients(self, radius, mass):
        data = super().coefficients(radius, mass)
        loading = bump(radius, *self.potential)
        data['mass_rhs'] += self.coupling*loading
        data['lapse_rhs'] -= self.coupling*loading/(radius*data['metric'])
        data['speed_log_radial'] -= 2*self.coupling*loading/(radius*data['metric'])
        return data


def main():
    evidence = EvidenceRun('annular-live-stress-response-attempt01', __file__)
    try:
        radius, metric, mass, coupling, rho, pressure, source, momentum, density = sp.symbols(
            'R F m kappa rho pr S p d', positive=True)
        mass_radial = coupling*radius**2*rho
        lapse_log_radial = mass/(radius**2*metric)+coupling*radius*pressure/metric
        raw = lapse_log_radial+(mass/radius**2-mass_radial/radius)/metric
        reduced = 2*mass/(radius**2*metric)-coupling*radius*(rho-pressure)/metric
        evidence.check('exact_radial_stress_difference_identity', sp.simplify(raw-reduced) == 0)
        loading = sp.sqrt(metric*(source**2+metric*momentum**2))
        source_rho = loading*density/radius**2
        source_pressure = metric**2*momentum**2*density/(radius**2*loading)
        evidence.check('moving_source_stress_difference_is_rest_mass_term', sp.simplify(
            source_rho-source_pressure-metric*source**2*density/(radius**2*loading)) == 0)
        snapshot = evidence.root/'source-intake/navier-stokes/20260914/annular-live-continuum-snapshot-attempt01/degree64.npz'
        status_path = snapshot.parent/'status.json'
        status = json.loads(status_path.read_text())
        evidence.check('source_snapshot_hash', status['state'] == 'complete' and hashlib.sha256(snapshot.read_bytes()).hexdigest()
            == status['outputs'][str(snapshot.relative_to(evidence.root))])
        evidence.own(snapshot)
        evidence.own(status_path)
        system = BarycentricLiveContinuum(64, 4, 10, radial_spacing=.1, label_order=8)
        with np.load(snapshot) as saved:
            loads = SnapshotLoads(system, system.solve(saved['state']), 24)
        base = RadialResponse(loads, tight=True)
        for width in [.04, .01, .0025, .000625]:
            candidate = PotentialResponse(loads, (5.6, width, .002))
            probes = np.unique(np.concatenate([loads.nodes, np.linspace(5.6-width, 5.6+width, 301)]))
            before, after = base.sample(probes), candidate.sample(probes)
            error = float(max(abs(after['speed_radial']-after['cancelled_speed_radial'])))
            response = float(max(abs(after['speed_radial']-before['speed_radial'])))
            row = dict(width=width, integrated_potential_loading=.002, maximum_speed_gradient_change=response,
                width_times_gradient_change=width*response, exact_stress_identity_error=error,
                minimum_metric=float(min(after['metric'])))
            evidence.report['cases'].append(row)
            evidence.check(str(width)+'_general_stress_identity_not_scalar_shortcut', error < 2e-12, row)
            evidence.check(str(width)+'_counterexample_remains_untrapped', row['minimum_metric'] > .5)
            print(json.dumps(row), flush=True)
        cases = evidence.report['cases']
        growth = cases[-1]['maximum_speed_gradient_change']/cases[0]['maximum_speed_gradient_change']
        evidence.check('stress_difference_counterexample_exposes_false_generalization', growth > 50, growth)
        evidence.report.update(counterexample_not_MTS_stress_identification=True, no_new_physical_initial_data=True,
            prescribed_radial_loading_test_not_full_conserved_potential_solution=True,
            MTS_Gram_stress_not_replaced_with_scalar_stress=True, no_forward_evolution=True,
            all_preexisting_physics_gates_unchanged=True, no_GitHub_action=True, subagents_used=False,
            bounds_not_from_probe_samples=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
