from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_cut_initial_data_20260915 import compatible_initial_state
from annular_live_gram_stress_20260918 import GramPushforward, GramLoadedSnapshot
from annular_live_radial_response_20260918 import SnapshotLoads, integration_nodes
from annular_live_radial_response_v2_20260918 import RadialResponse
import hashlib
import json
import numpy as np


def radial_coefficient(solution, derivative=False):
    def evaluate(radius):
        radius = np.asarray(radius)
        data = solution.sample(radius.ravel())
        value = 2*radius.ravel()*data['speed']+radius.ravel()**2*data['speed_radial'] if derivative else radius.ravel()**2*data['speed']
        return value.reshape(radius.shape)
    return evaluate


def main():
    evidence = EvidenceRun('annular-live-P2-Gram-radial-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        snapshot = intake/'annular-live-continuum-snapshot-attempt01/degree64.npz'
        source_status = snapshot.parent/'status.json'
        status = json.loads(source_status.read_text())
        evidence.check('actual_initial_snapshot_hash', status['state'] == 'complete' and hashlib.sha256(snapshot.read_bytes()).hexdigest()
            == status['outputs'][str(snapshot.relative_to(evidence.root))])
        evidence.own(snapshot)
        evidence.own(source_status)
        preceding = intake/'annular-live-radial-response-attempt02/status.json'
        previous = json.loads(preceding.read_text())
        evidence.check('prior_analytic_bound_qualification_complete', previous['state'] == 'complete')
        evidence.own(preceding)
        constants = previous['analytic_constants']
        system = BarycentricLiveContinuum(64, 4, 10, radial_spacing=.1, label_order=8)
        with np.load(snapshot) as saved:
            baseline = SnapshotLoads(system, system.solve(saved['state']), 24)
        reference = RadialResponse(baseline, tight=True)
        evidence.report.update(no_forward_evolution=True, actual_action_Gram_not_potential_substitution=True,
            original_action_unchanged=True, original_initial_data_unchanged=True,
            offshell_canonical_density_constraint_resolves_only=True,
            finite_P2_canonical_momentum_inverse_not_qualified=True,
            complete_parent_source_action_derived=False, full_live_P2_force_convergence_proven=False,
            all_Gram_rows_retained=True, github_action=False, subagents_used=False,
            physical_source_width_fixed=.02, analytic_constants=constants)
        for count in [33, 129, 257]:
            model = LocallyRefinedSourceAction(count, True, order=10, background_mass=.7, source_splits=8)
            smooth = compatible_initial_state(model, 0.)[0][:-1]
            oscillatory = .004*np.sin(1.7*np.arange(model.count)+.3)
            for profile, field in [('original_profile', smooth), ('oscillatory_control', oscillatory)]:
                atoms = GramPushforward(model, field, material=(0., .02, 0.), amplitude=(1., 0., 0.))
                if profile == 'oscillatory_control':
                    field = field*np.sqrt(.002/atoms.weak(lambda radius: radius**2))
                    atoms = GramPushforward(model, field, material=(0., .02, 0.), amplitude=(1., 0., 0.))
                loading = GramLoadedSnapshot(baseline, atoms)
                solved = RadialResponse(loading, tight=True)
                radius = np.unique(np.concatenate([np.linspace(baseline.lower, baseline.upper, 1501), atoms.edges(), baseline.nodes]))
                before, after = reference.sample(radius), solved.sample(radius)
                energy = float(atoms.weak(lambda radius: radius**2))
                differences = {name: float(max(abs(after[name]-before[name]))) for name in ['mass', 'speed', 'speed_radial']}
                bound = dict(mass=system.coupling*energy, speed=constants['speed_constant']*energy,
                    speed_radial=constants['speed_radial_constant']*energy)
                prefix = str(count)+'_'+profile
                for name in differences:
                    evidence.check(prefix+'_derived_'+name+'_bound', differences[name] <= bound[name]+2e-12,
                        dict(change=differences[name], bound=bound[name]))
                evidence.check(prefix+'_Gram_preserves_exact_speed_cancellation', max(abs(after['speed_radial']-after['cancelled_speed_radial'])) < 2e-12)
                nodes, measure = integration_nodes(np.unique(np.concatenate([atoms.edges(), baseline.nodes])), order=12)
                total_loading = float(measure @ loading.energy(nodes))
                evidence.check(prefix+'_inside_analytic_loading_tube', total_loading < constants['wave_energy_cap'])
                force = -atoms.shape_derivative(radial_coefficient(solved), radial_coefficient(solved, True))[0]
                old_force = -atoms.shape_derivative(radial_coefficient(reference), radial_coefficient(reference, True))[0]
                derivative_cap = max(abs(atoms.jacobian_slope))
                force_response_bound = .525*((2/baseline.lower+derivative_cap)*constants['speed_constant']
                    +constants['speed_radial_constant'])*energy**2
                evidence.check(prefix+'_Gram_shape_metric_response_bound', abs(force-old_force) <= force_response_bound+2e-12)
                row = dict(base_count=count, profile=profile, canonical_Gram_loading=energy,
                    radial_changes=differences, radial_bounds=bound, total_canonical_loading=total_loading,
                    source_Gram_shape_force=force, fixed_Gram_metric_force_change=abs(force-old_force),
                    fixed_Gram_metric_force_bound=force_response_bound,
                    smallest_metric=float(min(after['metric'])))
                evidence.report['cases'].append(row)
                evidence.save()
                output = evidence.output/(str(count)+'-'+profile+'.npz')
                np.savez_compressed(output, radius=radius, mass=after['mass'], speed=after['speed'], speed_radial=after['speed_radial'],
                    reference_mass=before['mass'], reference_speed=before['speed'], reference_speed_radial=before['speed_radial'])
                evidence.own(output, 'outputs')
                print(row, flush=True)
                if count == 129 and profile == 'oscillatory_control':
                    independent = RadialResponse(loading, method='RK45', tight=True).sample(radius)
                    error = max(float(max(abs(after[name]-independent[name]))) for name in ['mass', 'speed', 'speed_radial'])
                    evidence.check('independent_radial_integrator_with_nontrivial_Gram', error < 2e-9, error)
            first = GramPushforward(model, oscillatory)
            field_first = oscillatory*np.sqrt(.002/first.weak(lambda radius: radius**2))
            alternate = .003*np.cos(.73*np.arange(model.count)-.4)
            other = GramPushforward(model, alternate)
            alternate *= np.sqrt(.002/other.weak(lambda radius: radius**2))
            field_second = .7*field_first+.3*alternate
            first, second, delta = [GramPushforward(model, value) for value in [field_first, field_second, field_first-field_second]]
            nodes, measure = integration_nodes(first.edges(), order=24)
            difference = float(measure @ (nodes**2*abs(first.density(nodes)-second.density(nodes))))
            norms = [np.sqrt(2*item.weak(lambda radius: radius**2)) for item in [first, second, delta]]
            bound = (norms[0]+norms[1])*norms[2]/2
            evidence.check(str(count)+'_quadratic_Gram_L1_difference_bound', difference <= bound+2e-12,
                dict(difference=difference, bound=bound))
        evidence.report.update(scalar_response_estimates_extended_to_retained_Gram_loading=True,
            uniform_bounds_derived_not_fitted_to_samples=True,
            total_force_or_trajectory_error_not_certified=True, no_other_stress_sector_assumed_equal_pressure=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
