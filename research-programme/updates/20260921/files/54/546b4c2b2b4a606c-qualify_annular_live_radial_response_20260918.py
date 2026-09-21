from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_live_radial_response_20260918 import SnapshotLoads, RadialResponse, adjoint_integrals
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import sympy as sp


def symbolic_checks(evidence):
    radius, metric, source, momentum, mass, density, energy, coupling, lapse = sp.symbols(
        'R F S p m d e kappa N', positive=True)
    loading = sp.sqrt(metric*(source**2+metric*momentum**2))
    mass_derivative = lambda expression: -2*sp.diff(expression, metric)/radius
    loading_m = mass_derivative(loading)
    loading_p = sp.diff(loading, momentum)
    identities = dict(q_m=loading_m+(source**2+2*metric*momentum**2)/(radius*loading),
        q_p=loading_p-metric**2*momentum/loading,
        q_mm=mass_derivative(loading_m)+source**4/(radius**2*loading**3),
        q_mp=sp.diff(loading_m, momentum)+metric**2*momentum*(3*source**2+2*metric*momentum**2)/(radius*loading**3),
        q_pp=sp.diff(loading_p, momentum)-metric**3*source**2/loading**3)
    mass_rhs = coupling*(metric*energy+loading*density)
    lapse_rhs = mass/(radius**2*metric)+coupling*energy/radius+coupling*density*metric*momentum**2/(radius*loading)
    lapse_m = sp.diff(lapse_rhs, mass)+mass_derivative(lapse_rhs)
    identities['lapse_m_on_F_relation'] = (lapse_m-(1/(radius**2*metric**2)
        -coupling*density*metric*source**2*momentum**2/(radius**2*loading**3))).subs(mass, radius*(1-metric)/2)
    identities['lapse_p'] = sp.diff(lapse_rhs, momentum)-coupling*density*metric**2*momentum*(2*source**2+metric*momentum**2)/(radius*loading**3)
    identities['adjoint_damping'] = (lapse_rhs-(mass/radius**2-mass_rhs/radius)/metric
        -coupling*(2*energy/radius-density*loading_m))
    identities['wave_speed_radial_cancellation'] = (lapse_rhs+(mass/radius**2-mass_rhs/radius)/metric
        -2*mass/(radius**2*metric)+coupling*source**2*density/(radius*loading))
    source_energy = loading/sp.sqrt(metric)
    identities['momentum_adjoint_is_velocity'] = lapse/sp.sqrt(metric)*loading_p-lapse*metric*momentum/source_energy
    identities['rest_mass_adjoint_is_clock'] = lapse/sp.sqrt(metric)*sp.diff(loading, source)-lapse*source/source_energy
    gravity = lapse*(source_energy*lapse_rhs+momentum**2/source_energy*(mass/radius**2-mass_rhs/radius))
    identities['translation_gravity_reduction'] = gravity-(lapse*mass/radius**2*(source_energy/metric+momentum**2/source_energy)
        +coupling*lapse*source**2*energy/(radius*source_energy))
    for name, expression in identities.items():
        evidence.check('symbolic_'+name, sp.simplify(expression) == 0)


def main():
    evidence = EvidenceRun('annular-live-radial-response-attempt01', __file__)
    try:
        evidence.own(evidence.root/'scripts/annular_live_radial_response_20260918.py')
        evidence.report.update(no_forward_evolution=True, frozen_canonical_density_radial_variations_only=True,
            continuum_initial_snapshot_not_finite_P2_trajectory=True, no_flat_proof_transfer=True,
            no_new_parent_coefficients=True, no_GitHub_action=True, subagents_used=False,
            inherited_force_gates_unchanged=True, full_live_force_convergence_proven=False,
            radial_metric_response_derived=True, independently_reviewed_proof=False)
        symbolic_checks(evidence)
        snapshot = evidence.root/'source-intake/navier-stokes/20260914/annular-live-continuum-snapshot-attempt01/degree64.npz'
        status_path = snapshot.parent/'status.json'
        status = json.loads(status_path.read_text())
        expected = status['outputs'][str(snapshot.relative_to(evidence.root))]
        evidence.check('source_snapshot_complete_and_hash_verified', status['state'] == 'complete'
            and hashlib.sha256(snapshot.read_bytes()).hexdigest() == expected)
        evidence.own(snapshot)
        evidence.own(status_path)
        system = BarycentricLiveContinuum(64, 4, 10, radial_spacing=.1, label_order=8)
        with np.load(snapshot) as saved:
            geometry = system.solve(saved['state'])
        loads = SnapshotLoads(system, geometry, 24)
        started = time.perf_counter()
        base = RadialResponse(loads, tangent=True, tight=True)
        identities = adjoint_integrals(base)
        evidence.report['base_diagnostics'] = identities
        evidence.save()
        print('Base radial variation solved: '+json.dumps(identities), flush=True)
        for name in ['gradient_reduction_error', 'adjoint_metric_identity', 'speed_cancellation_error']:
            evidence.check(name, identities[name] < 2e-10, identities[name])
        first = base.final[3]/system.coupling
        second = base.final[5]/system.coupling
        adjoint = sum(identities[name] for name in ['wave', 'source_density', 'momentum'])
        evidence.check('moving_combined_first_variation_equals_adjoint', abs(first-adjoint) < 5e-9,
            dict(tangent=first, adjoint=adjoint, error=abs(first-adjoint)))
        radius = np.unique(np.concatenate([np.linspace(loads.lower, loads.upper, 1201), loads.nodes]))
        data = base.sample(radius)
        old_lapse, old_root = geometry.metric(radius)
        snapshot_errors = dict(lapse=float(max(abs(data['lapse']-old_lapse))),
            root=float(max(abs(data['root']-old_root))))
        evidence.check('positive_frozen_density_tracks_actual_snapshot', max(snapshot_errors.values()) < 2e-6, snapshot_errors)
        finer = RadialResponse(SnapshotLoads(system, geometry, 48), tight=True)
        refined = finer.sample(radius)
        evidence.check('density_tabulation_control', max(float(max(abs(data[name]-refined[name])))
            for name in ['mass', 'log_lapse', 'speed']) < 2e-6)
        independent = RadialResponse(loads, method='RK45', tight=True)
        control = independent.sample(radius)
        integrator_errors = {name: float(max(abs(data[name]-control[name]))) for name in ['mass', 'log_lapse', 'speed']}
        evidence.check('independent_RK45_radial_control', max(integrator_errors.values()) < 2e-9, integrator_errors)
        for key, parameter, step in [('wave', 'energy_parameter', .001), ('source_density', 'density_parameter', .001),
                ('momentum', 'momentum_parameter', .0001), ('rest_mass', 'mass_parameter', .00001), ('translation', 'shift', .0001)]:
            solutions = {factor: RadialResponse(loads, tight=True, **{parameter: factor*step}) for factor in [-2, -1, 1, 2]}
            finite = (solutions[-2].hamiltonian-8*solutions[-1].hamiltonian+8*solutions[1].hamiltonian-solutions[2].hamiltonian)/(12*step)
            row = dict(kind=key, step=step, finite_derivative=finite, adjoint=identities[key], error=abs(finite-identities[key]))
            evidence.report['cases'].append(row)
            evidence.check(key+'_independent_mass_difference_matches_adjoint', row['error'] < 2e-8, row)
            print(json.dumps(row), flush=True)
        step = .0002
        solutions = {factor: RadialResponse(loads, energy_parameter=factor*step, density_parameter=factor*step,
            momentum_parameter=factor*step, tight=True) for factor in [-2, -1, 1, 2]}
        finite_second = (-solutions[2].hamiltonian+16*solutions[1].hamiltonian-30*base.hamiltonian
            +16*solutions[-1].hamiltonian-solutions[-2].hamiltonian)/(12*step**2)
        evidence.check('moving_combined_second_radial_variation', abs(second-finite_second) < 3e-5,
            dict(tangent=second, finite_difference=finite_second, error=abs(second-finite_second)))
        profiles = {factor: solution.sample(radius) for factor, solution in solutions.items()}
        profile_errors = {}
        for field, tangent in [('mass', 'mass_first'), ('log_lapse', 'log_lapse_first'), ('speed', 'speed_first')]:
            finite = (profiles[-2][field]-8*profiles[-1][field]+8*profiles[1][field]-profiles[2][field])/(12*step)
            profile_errors[field] = float(max(abs(finite-data[tangent])))
        evidence.check('moving_variation_full_profiles', max(profile_errors.values()) < 2e-8, profile_errors)
        lower, floor, source, coupling = loads.lower, .5, system.source_mass, system.coupling
        density_integral, density_peak, momentum_cap, energy_cap = 1., 1.5/loads.width, .005, .05
        mass_cap = system.central_mass+coupling*(energy_cap+np.sqrt(source**2+momentum_cap**2)*density_integral)
        derived_floor = 1-2*mass_cap/lower
        momentum_polynomial_bound = float(sum(abs(loads.momentum_coefficients)))
        eta_constant = 2*coupling/lower+coupling**2*source*density_integral/(lower**2*floor**1.5)
        speed_constant = 2*coupling/(lower*floor)+eta_constant
        radial_max = 2*mass_cap/(lower**2*floor)+coupling*source*density_peak/(lower*np.sqrt(floor))
        radial_mass_max = 2/(lower**2*floor**2)+coupling*density_peak*(source**2+2*momentum_cap**2)/(lower**2*source*floor**1.5)
        derivative_constant = coupling*radial_mass_max+radial_max*speed_constant
        constants = dict(radius_min=lower, metric_floor=floor, derived_metric_floor=derived_floor,
            mass_cap=mass_cap, momentum_cap=momentum_cap, actual_momentum_polynomial_bound=momentum_polynomial_bound,
            density_L1=density_integral, density_Linfinity=density_peak, wave_energy_cap=energy_cap,
            log_eta_constant=eta_constant, speed_constant=speed_constant, speed_radial_constant=derivative_constant)
        evidence.report['analytic_constants'] = constants
        evidence.check('analytic_tube_follows_from_positive_loading_not_samples', derived_floor > floor
            and momentum_polynomial_bound < momentum_cap and identities['wave_energy_integral']+.002 < energy_cap
            and abs(identities['density_integral']-1) < 1e-10, constants)
        for width in [.04, .01, .0025, .000625]:
            solution = RadialResponse(loads, extra=(5.6, width, .002), tight=True)
            probes = np.unique(np.concatenate([radius, np.linspace(5.6-width, 5.6+width, 301)]))
            before, after = base.sample(probes), solution.sample(probes)
            differences = {name: float(max(abs(after[name]-before[name]))) for name in
                ['mass', 'speed', 'speed_radial', 'lapse_rhs']}
            row = dict(kind='localized_energy', width=width, added_energy=.002,
                peak_added_density=15*.002/(16*width), differences=differences,
                mass_bound=coupling*.002, speed_bound=speed_constant*.002, speed_radial_bound=derivative_constant*.002,
                cancellation_error=float(max(abs(after['speed_radial']-after['cancelled_speed_radial']))))
            evidence.report['cases'].append(row)
            evidence.check('localized_'+str(width)+'_uniform_mass_response', differences['mass'] <= row['mass_bound']+2e-10, row)
            evidence.check('localized_'+str(width)+'_uniform_speed_response', differences['speed'] <= row['speed_bound']+2e-10)
            evidence.check('localized_'+str(width)+'_uniform_speed_gradient_response', differences['speed_radial'] <= row['speed_radial_bound']+2e-10)
            evidence.check('localized_'+str(width)+'_exact_cancellation', row['cancellation_error'] < 2e-12)
            output = evidence.output/('width-'+str(width)+'.npz')
            np.savez_compressed(output, radius=probes, **{'base_'+name: before[name] for name in ['mass', 'speed', 'speed_radial', 'lapse_rhs']},
                **{'perturbed_'+name: after[name] for name in ['mass', 'speed', 'speed_radial', 'lapse_rhs']})
            evidence.own(output, 'outputs')
            print(json.dumps(row), flush=True)
        spike = RadialResponse(loads, extra=(5.6, .000625, .002), method='RK45', tight=True)
        spike_control = spike.sample(probes)
        spike_errors = {name: float(max(abs(after[name]-spike_control[name]))) for name in ['mass', 'speed', 'speed_radial']}
        evidence.check('narrowest_spike_independent_integrator', max(spike_errors.values()) < 2e-9, spike_errors)
        evidence.check('nonzero_moving_source_not_stationary_retest', abs(identities['momentum']) > .001
            and identities['maximum_source_ratio'] > .01)
        evidence.report.update(seconds=time.perf_counter()-started, tabulation_control_not_exact_original_density=True,
            uniform_bounds_derived_not_inferred_from_samples=True, physical_source_width_fixed=.02,
            zero_width_limit_proven=False, moving_chart_force_convergence_proven=False,
            metric_loading_tests_not_new_physical_initial_data=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
