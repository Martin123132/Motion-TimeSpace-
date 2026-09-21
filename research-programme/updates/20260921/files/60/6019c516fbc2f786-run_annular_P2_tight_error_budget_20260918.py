from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_P2_current_20260918 import P2Material, LiveP2Tangent
from scipy.integrate import solve_ivp
from time import perf_counter
import argparse
import hashlib
import json
import numpy as np


def compare_runs(coarse, fine):
    coarse_system, coarse_states, coarse_rates, coarse_mass = coarse
    fine_system, fine_states, fine_rates, fine_mass = fine
    interpolation = P2Material(fine_system, fine_states[-1, 0]).interpolation(coarse_system.labels)
    states = np.einsum('ij,tkjm->tkim', interpolation, fine_states)
    rates = np.einsum('ij,tjm->tim', interpolation, fine_rates)
    return dict(state=float(max(abs(states-coarse_states).ravel())), rates=float(max(abs(rates-coarse_rates).ravel())),
        scalar_rates=float(max(abs(rates[:, :, :-1]-coarse_rates[:, :, :-1]).ravel())),
        source_rates=float(max(abs(rates[:, :, -1]-coarse_rates[:, :, -1]).ravel())),
        mass=float(max(abs(fine_mass-coarse_mass).ravel())))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    branch, gram = args.branch, args.branch == 'MTS'
    evidence = EvidenceRun('annular-P2-tight-budget-'+branch+'-attempt01', __file__)
    try:
        diagnosis = evidence.root/'source-intake/navier-stokes/20260914/annular-P2-evolved-radial-budget-attempt01/status.json'
        status = json.loads(diagnosis.read_text())
        evidence.own(diagnosis)
        evidence.check('radial_repair_qualified_before_evolution', status['state'] == 'complete')
        evidence.report.update(branch=branch, no_forward_evolution=False, github_action=False, subagents_used=False,
            physical_action_and_Gram_rows_unchanged=True, no_mass_current_or_force_projection=True,
            primitive_dense_output_not_ODE_derivative_substitution=True,
            unique_parent_shift_extension_proven=False, full_live_P2_force_convergence_proven=False,
            same_preparation_and_parameters_in_matched_controls=True,
            targets=dict(radial=2e-9, velocity_refinement=2e-9, current=2e-9, mass_drift=2e-11))
        trajectories = {}
        probes = np.array([5.28, 5.57, 5.91, 6.024, 6.0313, 6.037, 6.25, 6.72])
        for mode, degree, maximum_step in [('principal',14,.0005), ('half_step',14,.00025), ('label_refined',18,.0005)]:
            started = perf_counter()
            print('Starting '+branch+' '+mode, flush=True)
            system = PrimitiveP2System(17, gram, layer_degree=degree, radial_degree=18, action_order=32, label_order=20)
            coordinates, momenta, unused, unused2 = system.initial()
            initial = np.stack([coordinates, momenta]).ravel()
            solution = solve_ivp(system.rhs, (0., .004), initial, method='DOP853', rtol=2e-12, atol=2e-14,
                max_step=maximum_step, t_eval=np.linspace(0.,.004,5))
            states = solution.y.T.reshape(-1, 2, len(system.labels), system.count+1)
            diagnostics, all_rates, masses = [], [], []
            for time, state in zip(solution.t, states):
                position, momentum = state
                rates, geometry = system.solve(position, momentum)
                material = P2Material(system, position)
                lapse, root = geometry.metric(position[:, -1])
                diagnostics.append(dict(time=float(time), exterior_mass=float(geometry.mass_nodes[-1, -1]),
                    minimum_source_jacobian=material.minimum_jacobian, minimum_spatial_jacobian=material.minimum_spatial_jacobian,
                    timelike_ratio=float(max(abs(rates[:, -1]/(lapse*root)))),
                    canonical_residual=system.canonical_residual(position,momentum,rates,geometry)))
                all_rates.append(rates)
                masses.append(geometry.values(probes)[0])
            destination = evidence.output/(mode+'.npz')
            np.savez_compressed(destination, times=solution.t, states=states, rates=np.array(all_rates),
                masses=np.array(masses), probes=probes, labels=system.labels)
            evidence.own(destination,'outputs')
            row = dict(branch=branch, mode=mode, layer_degree=degree, radial_degree=18, action_order=32,label_order=20,
                maximum_step=maximum_step, rtol=2e-12, atol=2e-14, duration=.004, success=bool(solution.success),
                evaluations=int(solution.nfev), mass_drift=max(abs(item['exterior_mass']-diagnostics[0]['exterior_mass']) for item in diagnostics),
                diagnostics=diagnostics, final_radial_residual=geometry.off_grid_residual(rates))
            evidence.report['cases'].append(row)
            evidence.save()
            evidence.check(mode+'_completed_short_interval', solution.success and len(states) == 5 and solution.t[-1] == .004)
            evidence.check(mode+'_unprojected_tight_mass_drift', row['mass_drift'] < 2e-11, row['mass_drift'])
            evidence.check(mode+'_canonical_ordered_timelike', all(item['canonical_residual'] < 2e-10
                and min(item['minimum_source_jacobian'],item['minimum_spatial_jacobian']) > 0
                and item['timelike_ratio'] < 1 for item in diagnostics))
            evidence.check(mode+'_tight_radial_equations', max(row['final_radial_residual']) < 2e-9,row['final_radial_residual'])
            evidence.check(mode+'_nontrivial_dynamics', float(max(abs(masses[-1]-masses[0]))) > 1e-7)
            if mode == 'principal':
                tangent = LiveP2Tangent(system,*states[-1])
                compared = tangent.compare(probes,label_order=16)
                row['final_current'] = compared
                evidence.check(mode+'_tight_independent_current', max(item['error'] for item in compared) < 2e-9,compared)
                evidence.check(mode+'_tight_on_shell_current', max(item['on_shell_error'] for item in compared) < 2e-9)
            trajectories[mode]=(system,states,np.array(all_rates),np.array(masses))
            row['seconds']=perf_counter()-started
            evidence.save()
            print(dict(branch=branch,mode=mode,seconds=row['seconds'],evaluations=solution.nfev,
                mass_drift=row['mass_drift'],radial=row['final_radial_residual']),flush=True)
        for mode in ['half_step','label_refined']:
            difference=compare_runs(trajectories['principal'],trajectories[mode])
            evidence.report.setdefault('refinement_comparisons',{})[mode]=difference
            evidence.check(mode+'_tight_whole_state_and_velocity_refinement',max(difference.values())<2e-9,difference)
        old_folder=evidence.root/'source-intake/navier-stokes/20260914/annular-live-P2-current-evolution-attempt01'
        old_status=json.loads((old_folder/'status.json').read_text())
        evidence.own(old_folder/'status.json')
        old_path=old_folder/(branch+'_principal.npz')
        evidence.check('old_baseline_hash_preserved',hashlib.sha256(old_path.read_bytes()).hexdigest()==old_status['outputs'][str(old_path.relative_to(evidence.root))])
        evidence.own(old_path)
        with np.load(old_path) as old:
            old_system=PrimitiveP2System(17,gram,layer_degree=6,radial_degree=18)
            difference=compare_runs((old_system,old['states'],old['rates'],old['masses']),trajectories['principal'])
        evidence.report.update(old_to_new_combined_change_not_an_isolated_error=difference,
            tight_short_evolution_qualified=True,continuum_accuracy_or_long_horizon_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
