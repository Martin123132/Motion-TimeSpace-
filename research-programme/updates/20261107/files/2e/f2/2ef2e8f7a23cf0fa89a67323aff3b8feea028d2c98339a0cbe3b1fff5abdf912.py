from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
from scipy import integrate

from matching_common import ROOT, PARENT, previous, modest_process, read_json, save


def coupled_replay():
    rows = []
    for light_mass, bath_mass, mixing in [(.88, 5., .2), (.88, 20., .05), (1.9, 10., .1)]:
        gap2 = bath_mass**2 - light_mass**2
        coupling = mixing * gap2
        bare2 = light_mass**2 + mixing**2 * gap2
        heavy2 = bath_mass**2 + mixing**2 * gap2
        matrix = np.array([[bare2, -coupling], [-coupling, bath_mass**2]])
        rotation = np.array([[1., -mixing], [mixing, 1.]]) / math.sqrt(1 + mixing**2)
        grid = np.linspace(0., 3., 1601)
        initial_new = np.array([.7, .2 / math.sqrt(heavy2), -.1, .1])
        initial_old = np.concatenate([rotation @ initial_new[:2], rotation @ initial_new[2:]])

        def rhs_original(elapsed, state):
            hubble = 1 / (1 + 1.5 * elapsed)
            return np.concatenate([state[2:], -3 * hubble * state[2:] - matrix @ state[:2]])

        def rhs_modes(elapsed, state):
            hubble = 1 / (1 + 1.5 * elapsed)
            return np.concatenate([state[2:], -3 * hubble * state[2:] - np.array([light_mass**2, heavy2]) * state[:2]])

        full = integrate.solve_ivp(rhs_original, (0., 3.), initial_old, t_eval=grid, method='DOP853', rtol=2e-11, atol=2e-13)
        modes = integrate.solve_ivp(rhs_modes, (0., 3.), initial_new, t_eval=grid, method='DOP853', rtol=2e-11, atol=2e-13)
        assert full.success and modes.success
        reconstructed = np.vstack([rotation @ modes.y[:2], rotation @ modes.y[2:]])
        field_error = float(np.max(abs(full.y - reconstructed)))
        old_energy = .5 * np.sum(full.y[2:]**2, axis=0) + .5 * np.einsum('ij,ij->j', full.y[:2], matrix @ full.y[:2])
        new_energy = .5 * np.sum(modes.y[2:]**2, axis=0) + .5 * (light_mass**2 * modes.y[0]**2 + heavy2 * modes.y[1]**2)
        energy_error = float(np.max(abs(old_energy - new_energy) / old_energy))
        wrong_energy = .5 * np.sum(full.y[2:]**2, axis=0) + .5 * (bare2 * full.y[0]**2 + bath_mass**2 * full.y[1]**2)
        omitted_interaction_error = float(np.max(abs(wrong_energy - new_energy) / new_energy))
        rows.append(dict(light_mass=light_mass, bath_mass=bath_mass, mixing=mixing,
                         max_field_error=field_error, max_relative_stress_error=energy_error,
                         omitted_interaction_negative_control_error=omitted_interaction_error,
                         minimum_mass_eigenvalue=float(np.linalg.eigvalsh(matrix)[0]),
                         original_nfev=full.nfev, rotated_nfev=modes.nfev))
        assert field_error < 2e-9 and energy_error < 2e-8
        assert omitted_interaction_error > .001
    return rows


def envelope_replay():
    rows = []
    grid = np.linspace(0., 40., 2001)
    for wave_ratio in [.4, .2, .1, .05]:
        carrier = 1.
        frequency = math.sqrt(1 + wave_ratio**2)
        position = np.cos(frequency * grid)
        momentum = -frequency * np.sin(frequency * grid)
        envelope = np.exp(1j * grid) * (position + 1j * momentum) / math.sqrt(2)
        envelope_dot = 1j * envelope + np.exp(1j * grid) * (momentum - 1j * frequency**2 * position) / math.sqrt(2)
        exact_rhs = wave_ratio**2 / 2 * (envelope + np.exp(2j * grid) * envelope.conjugate())
        residual = float(np.max(abs(1j * envelope_dot - exact_rhs)))
        slow = envelope[0] * np.exp(-1j * wave_ratio**2 * grid / 2)
        discrepancy = float(np.max(abs(slow - envelope)) / abs(envelope[0]))
        rows.append(dict(wave_over_mass=wave_ratio, exact_equation_residual=residual,
                         rotating_wave_relative_error=discrepancy,
                         neglected_fast_term_magnitude=float(np.max(abs(wave_ratio**2 / 2 * envelope.conjugate())))))
        assert residual < 2e-14
    assert all(rows[index + 1]['rotating_wave_relative_error'] < rows[index]['rotating_wave_relative_error'] for index in range(len(rows) - 1))
    return rows


def observational_replay():
    data = previous.inherited.load_likelihood_data()
    fits = read_json(PARENT / 'results/comparison/status.json')['fits']
    retained = [row for row in fits if row['model'] in ['ParentScalar_Lambda_free', 'ParentScalar_Lambda_zero']]
    observations = []
    dimensions = []
    light_speed = 299792458.
    hubble0 = previous.inherited.H0_KM_S_MPC * 1000 / previous.inherited.MPC_METRES
    radius = .01 * previous.inherited.MPC_METRES
    velocity = 200000.
    required_frequency = light_speed**2 / (radius * velocity)
    required_ratio = required_frequency / hubble0
    for archived in retained:
        parameters = dict(archived['parameters'], **archived['fixed'])
        result = previous.inherited.evaluate_model(archived['evaluator'], parameters, data)
        score = float(result['chi2_total'])
        assert abs(score - archived['chi2_total']) < 1e-7
        expansion = np.asarray(result['E'])
        matter = parameters['Omega_m'] * (1 + data.z_grid)**3
        remainder = expansion**2 - matter
        splits = []
        for share in [0., .25, .75]:
            dust_original = (1 - share) * matter
            dust_heavy = share * matter
            replaced = np.sqrt(remainder + dust_original + dust_heavy)
            delta_expansion = float(np.max(abs(replaced / expansion - 1)))
            score_split = float(previous.inherited.profile_likelihood(replaced, data)['chi2_total'])
            assert delta_expansion < 5e-15 and abs(score_split - score) < 1e-7
            splits.append(dict(heavy_share_of_existing_dust=share, chi2=score_split, delta_chi2=score_split - score,
                              max_relative_expansion_difference=delta_expansion))
        bad_expansion = np.sqrt(expansion**2 + .75 * matter)
        bad_score = float(previous.inherited.profile_likelihood(bad_expansion, data)['chi2_total'])
        assert abs(bad_score - score) > 1
        observations.append(dict(model=archived['model'], parameters=parameters, chi2=score,
            archived_chi2=archived['chi2_total'], dust_replacement_replays=splits,
            double_count_negative_control_chi2=bad_score,
            exact_finite_mass_cosmology_rerun=False,
            interpretation='Same actual SN/BAO likelihood in the leading cold dust limit; not detection or extra fit improvement.'))
        light_ratio = 10**parameters['log10_mu']
        separation = required_ratio / light_ratio
        hierarchy = []
        for share in [1e-6, 1e-4, .01, .1]:
            mass_shift = share / (1 - share) * (separation**2 - 1)
            hierarchy.append(dict(motion_overlap_in_heavy_mode=share,
                                  required_relative_bare_light_mass2_shift=mass_shift))
        dimensions.append(dict(model=archived['model'], fitted_light_mass_over_H0=light_ratio,
            H0_over_fitted_mass=1 / light_ratio, required_heavy_over_light=separation,
            required_frequency_over_H0=required_ratio,
            reduced_wavelength_kpc_if_velocity_nonrelativistic=light_speed**2 / (light_ratio * hubble0 * velocity) / (previous.inherited.MPC_METRES / 1000),
            heavy_motion_overlap_for_relative_mass_shift_at_most_one=1 / separation**2,
            hierarchy_cost_examples=hierarchy,
            cold_frequency_is_galaxy_scale_illustration_not_fit_or_limit=True))
    return dict(replays=observations, scale_checks=dimensions, SN_light_curve_rows=len(data.sn['z']),
                BAO_elements=len(data.bao['rows']), shape_only=True,
                H0_fiducial_km_s_Mpc=previous.inherited.H0_KM_S_MPC,
                H0_fitted_or_predicted=False, illustrative_radius_kpc=10., illustrative_velocity_km_s=200.,
                minimum_illustrative_cold_frequency_s_inverse=required_frequency,
                primordial_abundance_fitted=False, growth_or_galaxy_likelihood_run=False)


def main():
    modest_process()
    assert read_json(ROOT / 'results/derivation/status.json')['state'] == 'complete'
    started = time.monotonic()
    coupled = coupled_replay()
    envelopes = envelope_replay()
    report = observational_replay()
    save('replay', __file__, dict(coupled_real_field_replays=coupled, real_envelope_replays=envelopes,
                                elapsed_seconds=time.monotonic() - started, **report),
         [ROOT / 'results/derivation/status.json'])
    print(dict(state='complete', seconds=time.monotonic() - started,
               fitted_light_masses=[row['fitted_light_mass_over_H0'] for row in report['scale_checks']],
               hierarchy_ratio=report['scale_checks'][0]['required_heavy_over_light'],
               chi2=[row['chi2'] for row in report['replays']]), flush=True)


if __name__ == '__main__':
    main()
