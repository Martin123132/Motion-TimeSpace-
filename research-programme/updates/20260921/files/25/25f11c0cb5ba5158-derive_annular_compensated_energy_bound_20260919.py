from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def row_absolute_sum(bands):
    result = abs(bands[2]).copy()
    count = len(result)
    for offset in [-2, -1, 1, 2]:
        columns = np.arange(max(0, -offset), min(count, count-offset))
        result[columns+offset] += abs(bands[2+offset, columns])
    return result


def main():
    evidence = EvidenceRun('annular-compensated-energy-bound-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, finite_difference_rate_inputs=True, no_time_uniform_certificate=True,
            generalized_mass_bound_from_row_dominance=True, full_nonlinear_stability_proven=False)
        generator = np.random.default_rng(2026091903)
        controls = []
        for case in range(4):
            fine_count, coarse_count = 7, 4
            fine_seed, coarse_seed = generator.normal(size=(fine_count, fine_count)), generator.normal(size=(coarse_count, coarse_count))
            fine_mass = fine_seed @ fine_seed.T+np.eye(fine_count)
            coarse_mass = coarse_seed @ coarse_seed.T+np.eye(coarse_count)
            fine_rate = generator.normal(size=(fine_count, fine_count))
            fine_rate = (fine_rate+fine_rate.T)/2
            coarse_rate = generator.normal(size=(coarse_count, coarse_count))
            coarse_rate = (coarse_rate+coarse_rate.T)/2
            transfer = generator.normal(size=(fine_count, coarse_count))
            fine_velocity, coarse_velocity = generator.normal(size=fine_count), generator.normal(size=coarse_count)
            fine_force, coarse_force = generator.normal(size=fine_count), generator.normal(size=coarse_count)
            fine_acceleration = np.linalg.solve(fine_mass, fine_force-fine_rate @ fine_velocity)
            coarse_acceleration = np.linalg.solve(coarse_mass, coarse_force-coarse_rate @ coarse_velocity)
            difference = fine_velocity-transfer @ coarse_velocity
            difference_rate = fine_acceleration-transfer @ coarse_acceleration
            covector_map = np.linalg.solve(coarse_mass.T, (fine_mass @ transfer).T).T
            load = fine_force-covector_map @ coarse_force+(covector_map @ coarse_rate-fine_rate @ transfer) @ coarse_velocity
            error = float(max(abs(fine_mass @ difference_rate+fine_rate @ difference-load)))
            energy_rate = float(difference @ fine_mass @ difference_rate+.5*difference @ fine_rate @ difference)
            paired = float(difference @ load-.5*difference @ fine_rate @ difference)
            omitted_commutator = float(np.linalg.norm((covector_map @ coarse_rate-fine_rate @ transfer) @ coarse_velocity))
            evidence.check(str(case)+'_combined_load_evolution_identity', error < 2e-12, error)
            evidence.check(str(case)+'_energy_sign_and_half_factor', abs(energy_rate-paired) < 2e-11)
            evidence.check(str(case)+'_dropping_mass_transport_commutator_fails', omitted_commutator > 1e-3)
            stiffness_seed = generator.normal(size=(fine_count, fine_count))
            stiffness = stiffness_seed @ stiffness_seed.T+np.eye(fine_count)
            stiffness_rate = generator.normal(size=(fine_count, fine_count))
            stiffness_rate = (stiffness_rate+stiffness_rate.T)/2
            displacement = generator.normal(size=fine_count)
            wave_load = fine_mass @ difference_rate+stiffness @ displacement
            potential_rate = float(difference @ stiffness @ displacement+.5*displacement @ stiffness_rate @ displacement)
            full_rate = energy_rate+potential_rate
            wave_pairing = float(difference @ wave_load+.5*difference @ fine_rate @ difference
                +.5*displacement @ stiffness_rate @ displacement)
            wave_error = abs(full_rate-wave_pairing)
            evidence.check(str(case)+'_kinetic_plus_potential_rate_identity', wave_error < 3e-11)
            evidence.check(str(case)+'_omitting_potential_rate_fails', abs(potential_rate) > 1e-3)
            controls.append(dict(fixture=case, load_identity_error=error, energy_identity_error=abs(energy_rate-paired),
                omitted_commutator_norm=omitted_commutator, wave_energy_identity_error=wave_error,
                potential_rate=potential_rate, valid_for_claim=False))
        evidence.report['controls'] = controls
        position, velocity, acceleration = np.cos(np.pi/6), -np.sin(np.pi/6), -np.cos(np.pi/6)
        kinetic_growth = float(velocity*acceleration)
        potential_growth = float(position*velocity)
        evidence.check('oscillator_kinetic_growth_not_an_instability_certificate', kinetic_growth > .4
            and abs(kinetic_growth+potential_growth) < 1e-15)
        evidence.report['oscillator_control'] = dict(kinetic_growth=kinetic_growth, potential_growth=potential_growth,
            total_growth=kinetic_growth+potential_growth, scope='independent_unit_frequency_fixture_not_MTS', valid_for_claim=False)
        path = evidence.output.parent/'annular-live-compensated-rate-attempt01/status.json'
        status = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('actual_compensated_rates_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        for row in status['energy_rows']:
            branch, step = row['branch'], row['tangent_step']
            path = evidence.output.parent/'annular-live-compensated-rate-attempt01'/(branch+'-'+str(step)+'-compensated-rate.npz')
            evidence.own(path)
            with np.load(path) as arrays:
                mass, mass_rate = arrays['1_mass_bands'], arrays['1_mass_rate']
                difference, acceleration = arrays['velocity_difference'], arrays['acceleration_difference']
                load = band_action(mass, acceleration)+band_action(mass_rate, difference)
                margin = 2*mass[2]-row_absolute_sum(mass)
                evidence.check(branch+'_'+str(step)+'_positive_mass_dominance_margin', np.all(margin > 0.), float(min(margin)))
                gamma = float(max(row_absolute_sum(mass_rate)/margin))
                dual = solve_banded((2, 2), mass, load, check_finite=False)
                force_norm = float(np.sqrt(max(0., load @ dual)))
                energy = .5*float(difference @ band_action(mass, difference))
                signed_mass = .5*float(difference @ band_action(mass_rate, difference))
                predicted = float(difference @ load)-signed_mass
                energy_bound = np.sqrt(2*energy)*force_norm+gamma*energy
                error = abs(predicted-row['total_rate'])
                evidence.check(branch+'_'+str(step)+'_compensated_energy_identity', error < 3e-15*max(abs(predicted), 1e-15), error)
                evidence.check(branch+'_'+str(step)+'_conditional_energy_bound', abs(predicted) <= energy_bound+1e-25
                    and abs(signed_mass) <= gamma*energy+1e-30)
                evidence.report['cases'].append(dict(branch=branch, tangent_step=step, energy=energy,
                    energy_rate=predicted, compensated_load_dual_norm=force_norm, sampled_mass_relative_rate_bound=gamma,
                    energy_rate_absolute_bound=float(energy_bound), velocity_norm=float(np.sqrt(2*energy)),
                    velocity_norm_rate_bound=float(force_norm+.5*gamma*np.sqrt(2*energy)),
                    source_path=str(path.relative_to(evidence.root)), valid_for_claim=False))
                output = evidence.output/(branch+'-'+str(step)+'-energy-load.npz')
                np.savez_compressed(output, compensated_load=load, load_dual=dual, mass_dominance_margin=margin)
                evidence.own(output, 'outputs')
                evidence.save()
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), finest=evidence.report['cases'][-1])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
