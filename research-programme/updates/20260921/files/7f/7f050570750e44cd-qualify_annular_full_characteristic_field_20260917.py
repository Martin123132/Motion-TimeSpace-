from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from derive_annular_characteristic_source_20260917 import traces, force, rhs
from run_annular_source_fitted_crossing_20260915 import profile
from scipy.integrate import quad
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            full_characteristic_reference_not_full_GR=True, force_fit=False, force_correction=False,
            original_physical_gates_unchanged=True, interval_time_integration=False,
            continuous_first_derivatives_across_initial_fronts=True, second_derivative_at_front_not_unique=True)
        root = evidence.root/'source-intake/navier-stokes/20260914'
        for label in ['annular-characteristic-source-attempt01', 'annular-characteristic-energy-gate-attempt01']:
            path = root/label/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        standard, tight = FullCharacteristicField(), FullCharacteristicField(tight=True)
        times = np.linspace(0., .4, 81)
        radius = np.unique(np.concatenate([np.linspace(5.2, 6.8, 513), [5.48, 5.83, 6.03, 6.23, 6.58]]))
        old_profile, old_gradient = profile(radius)
        evidence.check('independent_original_profile', np.max(abs(tight.initial.profile(radius)-old_profile)) < 3e-14
            and np.max(abs(tight.initial.profile(radius, 1)-old_gradient)) < 3e-13)
        initial = tight.sample(0., radius)
        evidence.check('original_initial_field_and_rates', np.max(abs(initial['phi']-old_profile)) < 3e-14
            and np.max(abs(initial['phi_r']-old_gradient)) < 3e-13
            and np.max(abs(initial['phi_t']+.06*old_gradient)) < 3e-13)
        primitive_errors = []
        for point in np.linspace(5.2, 6.8, 31):
            lower, upper = sorted([6.03, point])
            sign = 1. if point >= 6.03 else -1.
            edges = [lower]+[edge for edge in [5.48, 5.83, 6.23, 6.58] if lower < edge < upper]+[upper]
            integral = sign*sum(quad(lambda location: float(profile(np.array([location]))[0][0]), left, right,
                epsabs=2e-15, epsrel=2e-13)[0] for left, right in zip(edges[:-1], edges[1:]))
            primitive_errors.append(abs(integral-tight.initial.integral(point)))
        evidence.check('initial_primitive_independent_quadrature', max(primitive_errors) < 3e-14, float(max(primitive_errors)))
        all_standard, all_tight = [], []
        source_defects, outer_defects, second_source_defects, force_defects, bulk_defects = [], [], [], [], []
        energy16, energy24 = [], []
        keys = ['phi', 'phi_t', 'phi_r', 'phi_tt', 'phi_tr', 'phi_rr']
        for instant in times:
            normal = standard.sample(instant, radius)
            exact = tight.sample(instant, radius)
            all_standard.append(np.array([normal[key] for key in keys]))
            all_tight.append(np.array([exact[key] for key in keys]))
            bulk_defects.append(float(np.max(abs(exact['phi_tt']-exact['phi_rr']-2*exact['phi_r']/radius))))
            state = tight.source.sol(instant)
            position, velocity = state[:2]
            acceleration = rhs(instant, state)[1]
            gradients = []
            for side in ['left', 'right']:
                boundary = tight.sample(instant, [position], source_side=side)
                source_defects.extend([abs(boundary['phi'][0]), abs(boundary['phi_t'][0]+velocity*boundary['phi_r'][0])])
                if instant > 0.:
                    second_source_defects.append(abs(boundary['phi_tt'][0]+2*velocity*boundary['phi_tr'][0]
                        +velocity**2*boundary['phi_rr'][0]+acceleration*boundary['phi_r'][0]))
                gradients.append(boundary['phi_r'][0])
            expected_traces = traces(instant, state)
            force_defects.append(max(abs(np.asarray(gradients)-expected_traces)))
            force_defects.append(abs(position**2*(1-velocity**2)*(gradients[0]**2-gradients[1]**2)/2-force(instant, state)))
            outer = tight.sample(instant, [5.2, 6.8])
            outer_defects.extend(abs(outer['phi_r']))
            energy16.append(tight.energy(instant, 16))
            energy24.append(tight.energy(instant, 24))
        evidence.check('pointwise_bulk_equation_off_fronts', max(bulk_defects) < 2e-14, max(bulk_defects))
        evidence.check('moving_Dirichlet_and_first_compatibility', max(source_defects) < 3e-12, float(max(source_defects)))
        evidence.check('second_source_compatibility_positive_times_only', max(second_source_defects) < 3e-11, float(max(second_source_defects)))
        evidence.check('source_traces_and_force_independent_reconstruction', max(force_defects) < 3e-12, float(max(force_defects)))
        evidence.check('outer_Neumann_not_even_chi_reflection', max(outer_defects) < 3e-12, float(max(outer_defects)))
        all_standard, all_tight = np.array(all_standard), np.array(all_tight)
        controls = np.max(abs(all_standard-all_tight), axis=(0, 2))
        evidence.check('full_field_tighter_time_control', max(controls) < 3e-9, dict(zip(keys, controls.tolist())))
        source_control = float(np.max(abs(standard.source.sol(times)-tight.source.sol(times))))
        evidence.check('source_tighter_time_control', source_control < 3e-12, source_control)
        analytic_energy = 944767173293/441000000000000+.03/np.sqrt(1-.06**2)
        energy_error = float(max(abs(np.asarray(energy24)-analytic_energy)))
        energy_control = float(max(abs(np.asarray(energy16)-energy24)))
        evidence.check('full_field_conserved_original_energy', energy_error < 3e-11, energy_error)
        evidence.check('split_quadrature_energy_control', energy_control < 3e-12, energy_control)
        for instant in [.05, .21, .4]:
            for side, front, expected in [('left', 6.03-instant, -.02/(1+.06)**2),
                    ('right', 6.03+instant, -.02/(1-.06)**2)]:
                sampled = tight.sample(instant, [front-1e-8, front+1e-8])
                first_error = max(abs(sampled[key][1]-sampled[key][0]) for key in ['phi', 'phi_t', 'phi_r'])
                measured = (sampled['phi_rr'][1]-sampled['phi_rr'][0])*front
                if side == 'right':
                    measured = -measured
                evidence.check(side+str(instant)+'_C1_front', first_error < 2e-8, float(first_error))
                evidence.check(side+str(instant)+'_derived_curvature_jump', abs(measured-expected) < 2e-6,
                    dict(measured=float(measured), derived=float(expected)))
        probe_errors = []
        for instant in [.11, .23, .37]:
            edges = tight.breakpoints(instant)
            centers = (edges[:-1]+edges[1:])/2
            centers = centers[np.diff(edges) > .015]
            delta = 2e-5
            values = tight.sample(instant, centers)
            radial = [tight.sample(instant, centers+offset*delta)['phi'] for offset in [-2, -1, 1, 2]]
            temporal = [tight.sample(instant+offset*delta, centers)['phi'] for offset in [-2, -1, 1, 2]]
            derivative_r = (radial[0]-8*radial[1]+8*radial[2]-radial[3])/(12*delta)
            derivative_t = (temporal[0]-8*temporal[1]+8*temporal[2]-temporal[3])/(12*delta)
            first_error = max(np.max(abs(derivative_r-values['phi_r'])), np.max(abs(derivative_t-values['phi_t'])))
            delta = 2e-4
            radial = [tight.sample(instant, centers+offset*delta)['phi'] for offset in [-2, -1, 1, 2]]
            temporal = [tight.sample(instant+offset*delta, centers)['phi'] for offset in [-2, -1, 1, 2]]
            second_r = (-radial[0]+16*radial[1]-30*values['phi']+16*radial[2]-radial[3])/(12*delta**2)
            second_t = (-temporal[0]+16*temporal[1]-30*values['phi']+16*temporal[2]-temporal[3])/(12*delta**2)
            second_error = max(np.max(abs(second_r-values['phi_rr'])), np.max(abs(second_t-values['phi_tt'])))
            evidence.check(str(instant)+'_independent_first_differences', first_error < 2e-9, float(first_error))
            evidence.check(str(instant)+'_independent_second_differences', second_error < 2e-7, float(second_error))
            probe_errors.append(dict(time=instant, first=float(first_error), second=float(second_error)))
        outer_integral_errors = []
        for kind, boundary, direction, solution in [('F', 5.2, -1., tight.left), ('G', 6.8, 1., tight.right)]:
            initial_value = float(solution.y[0, 0])
            for instant in [.1, .3, .4]:
                def forcing(time):
                    argument = time+boundary if kind == 'F' else time-boundary
                    value, first, unused = tight.initial.incoming(argument, 'G' if kind == 'F' else 'F')
                    return float(np.exp(-direction*time/boundary)*(first+direction*value/boundary))
                split = .28 if kind == 'F' else .22
                points = [split] if split < instant else None
                integrated = np.exp(direction*instant/boundary)*(initial_value+quad(forcing, 0., instant,
                    epsabs=2e-15, epsrel=2e-12, points=points)[0])
                outer_integral_errors.append(abs(integrated-float(solution.sol(instant)[0])))
        evidence.check('outer_reflection_independent_integrating_factor', max(outer_integral_errors) < 3e-13,
            float(max(outer_integral_errors)))
        states = tight.source.sol(times).T
        forces = np.array([force(instant, state) for instant, state in zip(times, states)])
        path = root/'annular-characteristic-source-attempt01/characteristic-source.npz'
        evidence.own(path)
        previous = json.loads((path.parent/'status.json').read_text())
        evidence.check('previous_source_pack_hash', hashlib.sha256(path.read_bytes()).hexdigest() == previous['outputs'][str(path.relative_to(evidence.root))])
        with np.load(path, allow_pickle=False) as saved:
            evidence.check('previous_source_reproduced', np.array_equal(times, saved['times'])
                and np.max(abs(states-saved['states'])) < 3e-12 and np.max(abs(forces-saved['forces'])) < 3e-12)
        destination = evidence.output/'full-characteristic-reference.npz'
        np.savez_compressed(destination, times=times, radius=radius, fields=all_tight, standard_fields=all_standard,
            field_names=np.array(keys), source_states=states, forces=forces, energies=energy24,
            standard_source_states=standard.source.sol(times).T)
        evidence.own(destination, 'outputs')
        evidence.report['cases'].append(dict(maximum_source_boundary_defect=float(max(source_defects)),
            maximum_outer_boundary_defect=float(max(outer_defects)), energy_absolute_error=energy_error,
            energy_quadrature_control=energy_control, tighter_field_controls=dict(zip(keys, controls.tolist())),
            independent_derivative_probes=probe_errors, comparison_data_not_yet_opened=True))
        evidence.report['reference_frozen_at'] = datetime.now(timezone.utc).isoformat()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
