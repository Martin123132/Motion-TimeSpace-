from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from scipy.integrate import solve_ivp
from time import perf_counter
import argparse
import hashlib
import json
import numpy as np


def checked_load(evidence, folder, filename):
    status_path = evidence.output.parent/folder/'status.json'
    status = json.loads(status_path.read_text())
    path = status_path.parent/filename
    expected = status['outputs'][str(path.relative_to(evidence.root))]
    evidence.check(folder+'_complete_and_hash_'+filename, status['state'] == 'complete'
        and hashlib.sha256(path.read_bytes()).hexdigest() == expected)
    evidence.own(status_path)
    evidence.own(path)
    with np.load(path, allow_pickle=False) as data:
        return {name:data[name].copy() for name in data.files}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=['continuum', 'reference', 'MTS'], required=True)
    parser.add_argument('--resolution', type=int, required=True)
    args = parser.parse_args()
    key = args.kind+'-'+str(args.resolution)
    evidence = EvidenceRun('annular-P2-continuum-bridge-'+key+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(kind=args.kind, resolution=args.resolution, duration=.004,
            github_action=False, subagents_used=False, equations_unchanged=True,
            finite_Gram_retained=args.kind == 'MTS', no_projection=True,
            common_analytic_preparation_not_identical_discrete_initial_states=True,
            continuum_comparison_qualified=False, full_live_P2_force_convergence_proven=False,
            rtol=2e-12, atol=2e-14, maximum_wall_seconds=7200)
        if args.kind == 'continuum':
            if args.resolution not in [384, 512]:
                raise ValueError('Only source-backed continuum initial states384/512 are qualified here.')
            system = BarycentricLiveContinuum(args.resolution, 8, 18, radial_spacing=.025, label_order=12)
            folder = 'annular-live-continuum-degree512-attempt01' if args.resolution == 512 else 'annular-live-continuum-refinement-attempt02'
            status_path = evidence.output.parent/folder/'status.json'
            status = json.loads(status_path.read_text())
            path = status_path.parent/('degree'+str(args.resolution)+'.npz')
            evidence.check('source_initial_state_hash', hashlib.sha256(path.read_bytes()).hexdigest()
                == status['outputs'][str(path.relative_to(evidence.root))])
            evidence.own(status_path)
            evidence.own(path)
            evidence.report['initial_state_source_status'] = status['state']
            with np.load(path, allow_pickle=False) as data:
                initial = data['states'][0].copy()
                evidence.check('initial_timestamp_zero', data['times'][0] == 0.)
            maximum_step = 8/args.resolution**2
            evidence.report.update(layer_degree=8, radial_degree=18, radial_spacing=.025, label_order=12)
        else:
            system = PrimitiveP2System(args.resolution, args.kind == 'MTS', layer_degree=14,
                radial_degree=18, action_order=32, label_order=20)
            coordinates, momenta, unused, unused2 = system.initial()
            initial = np.stack([coordinates, momenta]).ravel()
            maximum_step = .0005
            evidence.report.update(layer_degree=14, radial_degree=18, action_order=32, label_order=20)
        evidence.report['maximum_step'] = maximum_step
        times = np.linspace(0., .004, 5)
        states, calls = [initial], 0

        def rhs(time, state):
            if perf_counter()-started > 7200:
                raise RuntimeError('Safe budget reached; accepted segments preserved.')
            return system.rhs(time, state)

        for lower, upper in zip(times[:-1], times[1:]):
            solution = solve_ivp(rhs, (lower, upper), states[-1], method='DOP853', rtol=2e-12, atol=2e-14,
                max_step=maximum_step, t_eval=[upper])
            evidence.check('accepted_segment_'+format(upper,'.3f'), solution.success
                and solution.t[-1] == upper and np.all(np.isfinite(solution.y)))
            states.append(solution.y[:, -1])
            calls += solution.nfev
            path = evidence.output/('accepted-'+format(upper,'.3f')+'.npz')
            np.savez_compressed(path, time=upper, state=states[-1])
            evidence.own(path, 'outputs')
            evidence.report.update(accepted_time=float(upper), evaluations=calls, seconds=perf_counter()-started)
            evidence.save()
            print(dict(key=key, accepted_time=float(upper), calls=calls, seconds=perf_counter()-started), flush=True)
        rates, masses, diagnostics = [], [], []
        for time, state in zip(times, states):
            if args.kind == 'continuum':
                flow, geometry, forces = system.rhs_with_geometry(state)
                source = geometry.material.source
                lapse, root = geometry.metric(source[:, 0])
                ratio = float(max(abs(forces['velocity']/(lapse*root))))
                row = dict(time=float(time), minimum_jacobian=geometry.material.minimum_jacobian, timelike_ratio=ratio)
            else:
                coordinates, momenta = state.reshape(2, len(system.labels), system.count+1)
                velocity, geometry = system.solve(coordinates, momenta)
                rates.append(velocity)
                lapse, root = geometry.metric(coordinates[:, -1])
                row = dict(time=float(time), minimum_jacobian=geometry.material.minimum_jacobian,
                    timelike_ratio=float(max(abs(velocity[:,-1]/(lapse*root)))),
                    canonical_residual=system.canonical_residual(coordinates, momenta, velocity, geometry))
            masses.append(float(geometry.mass_nodes[-1,-1]))
            diagnostics.append(row)
        destination = evidence.output/'trajectory.npz'
        arrays = dict(times=times, states=np.array(states), exterior_mass=masses)
        if rates:
            arrays['rates'] = np.array(rates)
            arrays['labels'] = system.labels
        np.savez_compressed(destination, **arrays)
        evidence.own(destination, 'outputs')
        drift = float(max(abs(np.array(masses)-masses[0])))
        radial = geometry.check_radial() if args.kind == 'continuum' else geometry.off_grid_residual(velocity)
        evidence.report.update(diagnostics=diagnostics, exterior_mass_drift=drift,
            final_radial_residual=radial, seconds=perf_counter()-started)
        evidence.check('ordered_timelike_throughout', all(row['minimum_jacobian'] > 0 and row['timelike_ratio'] < 1 for row in diagnostics))
        evidence.check('unprojected_mass_drift', drift < (2e-9 if args.kind == 'continuum' else 2e-11), drift)
        evidence.check('radial_constraints', max(radial) < (2e-8 if args.kind == 'continuum' else 2e-9), radial)
        if args.kind != 'continuum':
            evidence.check('canonical_inverse', max(row['canonical_residual'] for row in diagnostics) < 2e-10)
        evidence.report['short_trajectory_completed_not_comparison_pass'] = True
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
