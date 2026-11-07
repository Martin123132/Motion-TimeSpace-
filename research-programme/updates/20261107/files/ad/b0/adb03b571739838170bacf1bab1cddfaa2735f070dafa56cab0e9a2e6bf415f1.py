from nonlocal_dc import *


def main():
    modest()
    folder = ROOT / 'results/history-comparison'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, paths = [], [], []
    basis, specification = current_basis()
    banks = {}
    for name in ['s450-i96', 's700-i160', 's960-i256']:
        path = ROOT / 'banks' / name
        banks[name] = dict(np.load(path / 'matrix.npz'))
        paths.extend([path / 'matrix.npz', path / 'status.json'])
    checks.append(check('Three-frequency matrix refinement700/160 to960/256',
                        relative(banks['s700-i160']['nonlocal_matrix'], banks['s960-i256']['nonlocal_matrix']), 1e-6))
    for model in ['heavy', 'cold']:
        def load(name, root=ROOT):
            path = root / 'backgrounds' / name
            paths.extend([path / 'history.npz', path / 'status.json'])
            packet = json.loads((path / 'status.json').read_text())
            assert packet['all_checks_passed']
            return dict(np.load(path / 'history.npz')), packet
        old, old_report = load(model + '-derived-gaunt', KINETIC)
        control, control_report = load(model + '-local-derived-6400')
        for key in ['profiles', 'energy_scaled', 'temperature_scaled', 'number_scaled',
                    'expansion_work', 'integrated_number_source']:
            checks.append(check('Unchanged retained control reproduced: ' + model + key, relative(control[key], old[key]), 1e-13))
        leading_local, local_report = load(model + '-local-leading-6400')
        nonlocal_result, nonlocal_report = load(model + '-nonlocal-leading-6400')
        local_coarse, coarse_local_report = load(model + '-local-leading-3200')
        nonlocal_coarse, coarse_report = load(model + '-nonlocal-leading-3200')
        refined, refined_report = load(model + '-nonlocal-refined-6400')
        gaunt_result, gaunt_report = load(model + '-nonlocal-soft-gaunt-6400')
        fine_change = nonlocal_report['final_photon_number_fraction'] - local_report['final_photon_number_fraction']
        coarse_change = coarse_report['final_photon_number_fraction'] - coarse_local_report['final_photon_number_fraction']
        time_error = abs(coarse_change / fine_change - 1)
        matrix_effect = refined_report['final_photon_number_fraction'] - nonlocal_report['final_photon_number_fraction']
        checks.append(check('Structural number-source change itself refines in time: ' + model, time_error, .002))
        checks.append(check('Source-matrix refinement smaller than structural change: ' + model,
                            abs(matrix_effect / fine_change), .001))
        delta_profile = nonlocal_result['profiles'][-1] - leading_local['profiles'][-1]
        profile_fraction = math.sqrt(float(delta_profile @ basis.mass @ delta_profile)
                              / float(leading_local['profiles'][-1] @ basis.mass @ leading_local['profiles'][-1]))
        profile = nonlocal_result['profiles'][len(nonlocal_result['profiles']) // 2]
        chemical = basis.chemical
        energy_identity = float(basis.temperature @ banks['s960-i256']['nonlocal_matrix'] @ profile)
        photon_rate = float(chemical @ banks['s960-i256']['nonlocal_matrix'] @ profile)
        checks.append(check('Actual midpoint profile retains DC photon-energy identity: ' + model,
                            abs(energy_identity) / max(abs(photon_rate), 1e-30), 1e-8))
        rows.append(dict(model=model,
             old_derived_number_fraction=old_report['final_photon_number_fraction'],
             leading_local_number_fraction=local_report['final_photon_number_fraction'],
             leading_nonlocal_number_fraction=nonlocal_report['final_photon_number_fraction'],
             structural_number_change=fine_change,
             structural_number_change_relative_to_local=abs(fine_change / local_report['final_photon_number_fraction']),
             structural_change_time_refinement=time_error,
             matrix_refinement_fraction_of_structural_change=abs(matrix_effect / fine_change),
             final_profile_mass_norm_relative_change=profile_fraction,
             gas_temperature_fraction_change=nonlocal_report['final_temperature_fraction'] - local_report['final_temperature_fraction'],
             nonlocal_soft_gaunt_number_fraction=gaunt_report['final_photon_number_fraction'],
             soft_gaunt_extension_change=gaunt_report['final_photon_number_fraction'] - nonlocal_report['final_photon_number_fraction'],
             old_and_new_gaunt_comparison_change=gaunt_report['final_photon_number_fraction'] - old_report['final_photon_number_fraction'],
             radiation_energy_fraction=nonlocal_report['final_energy_fraction']))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
           rows=rows, same_parent_and_observational_parameters=True, structural_response_not_new_likelihood=True,
           leading_nonrelativistic_replacement_tested=True,
           soft_gaunt_extension_is_sensitivity_not_full_finite_frequency_derivation=True),
           __file__, paths)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
