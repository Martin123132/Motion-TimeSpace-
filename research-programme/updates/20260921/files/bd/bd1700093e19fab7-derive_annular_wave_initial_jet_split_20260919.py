from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_wave_error_energy_20260919 import stiffness_terms, wave_energy
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
import contextlib
import json
import numpy as np


def polarized_split(mass_action, stiffness_action, mass_rate_action, stiffness_rate_action,
        displacement, velocity, acceleration, initial_displacement, initial_velocity, time):
    baseline_displacement = initial_displacement+time*initial_velocity
    baseline_velocity = initial_velocity
    increment_displacement = displacement-baseline_displacement
    increment_velocity = velocity-baseline_velocity
    baseline_energy = .5*float(baseline_velocity @ mass_action(baseline_velocity)
        +baseline_displacement @ stiffness_action(baseline_displacement))
    increment_energy = .5*float(increment_velocity @ mass_action(increment_velocity)
        +increment_displacement @ stiffness_action(increment_displacement))
    cross_energy = float(baseline_velocity @ mass_action(increment_velocity)
        +baseline_displacement @ stiffness_action(increment_displacement))
    baseline_rate = float(.5*baseline_velocity @ mass_rate_action(baseline_velocity)
        +baseline_velocity @ stiffness_action(baseline_displacement)
        +.5*baseline_displacement @ stiffness_rate_action(baseline_displacement))
    increment_rate = float(increment_velocity @ mass_action(acceleration)
        +.5*increment_velocity @ mass_rate_action(increment_velocity)
        +increment_velocity @ stiffness_action(increment_displacement)
        +.5*increment_displacement @ stiffness_rate_action(increment_displacement))
    cross_rate = float(baseline_velocity @ mass_action(acceleration)
        +baseline_velocity @ mass_rate_action(increment_velocity)
        +baseline_velocity @ stiffness_action(increment_displacement)
        +baseline_displacement @ stiffness_action(increment_velocity)
        +baseline_displacement @ stiffness_rate_action(increment_displacement))
    return dict(baseline_energy=baseline_energy, increment_energy=increment_energy, cross_energy=cross_energy,
        baseline_rate=baseline_rate, increment_rate=increment_rate, cross_rate=cross_rate)


def main():
    evidence = EvidenceRun('annular-wave-initial-jet-split-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, diagnostic_baseline_not_a_physical_solution=True,
            both_initial_displacement_and_velocity_retained=True, cross_energy_not_dropped=True,
            original_hierarchy_error_not_replaced=True, full_nonlinear_stability_proven=False)
        generator = np.random.default_rng(2026091915)
        evidence.report['controls'] = []
        for case in range(4):
            count = 6
            seed = generator.normal(size=(count, count))
            mass = seed @ seed.T+np.eye(count)
            seed = generator.normal(size=(count, count))
            stiffness = seed @ seed.T+np.eye(count)
            mass_rate, stiffness_rate = generator.normal(size=(2, count, count))
            mass_rate, stiffness_rate = (mass_rate+mass_rate.T)/2, (stiffness_rate+stiffness_rate.T)/2
            displacement, velocity, acceleration, initial_displacement, initial_velocity = generator.normal(size=(5, count))
            row = polarized_split(lambda values:mass @ values, lambda values:stiffness @ values,
                lambda values:mass_rate @ values, lambda values:stiffness_rate @ values,
                displacement, velocity, acceleration, initial_displacement, initial_velocity, .3)
            energy = .5*float(velocity @ mass @ velocity+displacement @ stiffness @ displacement)
            rate = float(velocity @ mass @ acceleration+.5*velocity @ mass_rate @ velocity
                +velocity @ stiffness @ displacement+.5*displacement @ stiffness_rate @ displacement)
            energy_error = abs(energy-row['baseline_energy']-row['increment_energy']-row['cross_energy'])
            rate_error = abs(rate-row['baseline_rate']-row['increment_rate']-row['cross_rate'])
            evidence.check(str(case)+'_independent_dense_energy_polarization', energy_error < 4e-12)
            evidence.check(str(case)+'_independent_dense_rate_polarization', rate_error < 4e-12)
            evidence.check(str(case)+'_discarding_cross_terms_fails', abs(row['cross_energy']) > .01 and abs(row['cross_rate']) > .01)
            evidence.report['controls'].append(dict(fixture=case, energy_error=energy_error, rate_error=rate_error,
                **row, valid_for_claim=False))
        path = evidence.output.parent/'annular-live-wave-error-energy-attempt01/status.json'
        status = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('full_wave_energy_run_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        for branch in ['reference', 'MTS']:
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            center = int(np.argmin(abs(systems[1].labels)))
            states = state_pair(evidence, branch, False)
            initial_rates = [system.solve(*state)[0][center] for system, state in zip(systems, states)]
            indices, shape, unused = systems[0].model.features_quadratic(systems[1].model.radii)

            def transfer(values):
                return np.sum(shape*values[indices], axis=1)

            initial_displacement = states[1][0, center, :-1]-transfer(states[0][0, center, :-1])
            initial_velocity = initial_rates[1][:-1]-transfer(initial_rates[0][:-1])
            expected = next(row for row in status['energy_snapshots'] if row['branch'] == branch and row['time'] == 0.)
            evidence.check(branch+'_same_initial_field_and_velocity_defect',
                abs(max(abs(initial_displacement))-expected['maximum_displacement']) < 1e-20
                and abs(max(abs(initial_velocity))-expected['maximum_velocity_difference']) < 1e-20)
            for step in [2e-7, 1e-7, 5e-8, 2.5e-8]:
                path = evidence.output.parent/'annular-live-wave-error-energy-attempt01'/(branch+'-'+str(step)+'-wave-energy.npz')
                evidence.own(path)
                with np.load(path) as stored:
                    wave = {key:stored[key] for key in stored.files}
                path = evidence.output.parent/'annular-live-compensated-rate-attempt01'/(branch+'-'+str(step)+'-compensated-rate.npz')
                evidence.own(path)
                with np.load(path) as stored:
                    mass, mass_rate = stored['1_mass_bands'], stored['1_mass_rate']
                weights = dict(gradient=wave['gradient_weights'], gram=wave['Gram_weights'])
                weight_rate = dict(gradient=wave['gradient_weight_rate'], gram=wave['Gram_weight_rate'])
                model = systems[1].model
                row = polarized_split(lambda values:band_action(mass, values),
                    lambda values:stiffness_terms(model, weights, values)['load'],
                    lambda values:band_action(mass_rate, values),
                    lambda values:stiffness_terms(model, weight_rate, values)['load'],
                    wave['displacement'], wave['velocity_difference'], wave['acceleration_difference'],
                    initial_displacement, initial_velocity, 4e-5)
                expected = next(item for item in status['cases'] if item['branch'] == branch and item['tangent_step'] == step)
                energy_error = abs(expected['total']-row['baseline_energy']-row['increment_energy']-row['cross_energy'])
                rate_error = abs(expected['full_wave_energy_rate']-row['baseline_rate']-row['increment_rate']-row['cross_rate'])
                energy_scale = max(abs(row['baseline_energy']), abs(row['increment_energy']), abs(row['cross_energy']), 1e-20)
                rate_scale = max(abs(row['baseline_rate']), abs(row['increment_rate']), abs(row['cross_rate']), 1e-20)
                evidence.check(branch+'_'+str(step)+'_full_energy_and_rate_polarization',
                    energy_error < 2e-12*energy_scale+1e-25 and rate_error < 2e-10*rate_scale+1e-23,
                    dict(energy_error=energy_error, rate_error=rate_error))
                evidence.check(branch+'_'+str(step)+'_positive_baseline_and_increment_energy',
                    row['baseline_energy'] >= 0. and row['increment_energy'] >= 0.)
                evidence.report['cases'].append(dict(branch=branch, tangent_step=step, **row,
                    energy_identity_error=energy_error, rate_identity_error=rate_error,
                    increment_fraction_of_total=row['increment_energy']/expected['total'], valid_for_claim=False))
                path = evidence.output/(branch+'-'+str(step)+'-initial-jet.npz')
                np.savez_compressed(path, initial_displacement=initial_displacement, initial_velocity=initial_velocity,
                    baseline_displacement=initial_displacement+4e-5*initial_velocity,
                    increment_displacement=wave['displacement']-initial_displacement-4e-5*initial_velocity,
                    increment_velocity=wave['velocity_difference']-initial_velocity)
                evidence.own(path, 'outputs')
                evidence.save()
            print(json.dumps(evidence.report['cases'][-1]), flush=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
