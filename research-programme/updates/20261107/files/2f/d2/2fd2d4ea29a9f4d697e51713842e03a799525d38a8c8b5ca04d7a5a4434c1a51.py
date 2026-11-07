import argparse
from mixed_common import *
from mixed_wave_system import MixedSystem


def norm(values, mass):
    return np.sqrt(np.maximum(0., np.einsum('...i,ij,...j->...', values.conj(), mass, values).real))


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        source = ROOT / 'waves' / (model + arguments.suffix) / 'evolution.npz'
        parent = PARENT / 'paired' / (model + '24-high8-3200') / 'evolution.npz'
        inputs.extend([source, source.parent / 'status.json', parent, parent.parent / 'status.json'])
        with np.load(source) as saved:
            expansion = saved['expansion'].copy()
            baseline, response = saved['baseline_states'].copy(), saved['scaled_differences'].copy()
            heat = float(saved['heat'])
            background = saved['background_corrections'].copy()
        with np.load(parent) as saved:
            parent_response = saved['differences'].copy()
        system = MixedSystem(model, 24, 8, arguments.bank)
        basis = system.basis
        vectors = np.column_stack([basis.chemical, basis.temperature])
        moments = np.vstack([basis.number, basis.energy])
        moment_lift = vectors @ linalg.inv(moments @ vectors)
        radiation = response[:, system.mode_slice(0)]
        moment_part = radiation @ moments.T @ moment_lift.T
        orthogonal = radiation - moment_part
        shape_fraction = float(np.max(norm(orthogonal, basis.mass)) / np.max(norm(radiation, basis.mass)))
        moment_fraction = float(np.max(norm(moment_part, basis.mass)) / np.max(norm(radiation, basis.mass)))
        for degree in range(9):
            for mode in system.names[degree]:
                section = system.mode_slice(degree, mode)
                original = float(np.max(norm(parent_response[:, section], basis.mass)))
                physical = heat * float(np.max(norm(response[:, section], basis.mass)))
                rows.append(dict(model=model, mode=str(degree) + mode, mixed_spectral_norm=physical,
                                 parent_angular_spectral_norm=original,
                                 ratio=physical / original if original > 1e-35 else None))
        instantaneous, relaxation, constraint_errors = [], [], []
        for point, state, delta_state in zip(expansion, baseline, response):
            mass, original, _ = system.matrices(point)
            correction = system.correction(point)
            operator = original + heat * correction
            row = operator.getrow(10).toarray()[0]
            forcing = (correction @ state)[10]
            diagonal = row[10]
            row[10] = 0
            assert abs(diagonal.imag) < 1e-12
            instantaneous.append(-(row @ delta_state + forcing) / diagonal)
            relaxation.append(float(-diagonal.real / heat))
            raw, scale = system.constraints(point, delta_state)
            constraint_errors.append(float(np.max(abs(raw)) / scale))
        instantaneous = np.asarray(instantaneous)
        thermal_error = float(np.max(abs(instantaneous - response[:, 10])) / np.max(abs(response[:, 10])))
        baseline_temperature = float(np.max(abs(baseline[:, 10])))
        weighted_gas = heat ** 2 * float(np.max(abs(response[:, 10])))
        photon_energy = heat * float(np.max(abs(radiation @ basis.energy)))
        rows.append(dict(model=model, monopole_energy_number_free_shape_fraction=shape_fraction,
                         monopole_energy_number_moment_fraction=moment_fraction,
                         mixed_temperature_fraction_of_baseline=heat * float(np.max(abs(response[:, 10]))) / baseline_temperature,
                         gas_internal_energy_response_in_photon_reference_units=weighted_gas,
                         photon_energy_response_in_photon_reference_units=photon_energy,
                         thermal_quasistatic_relative_discrepancy=thermal_error,
                         thermal_relaxation_per_log_a_min=min(relaxation), thermal_relaxation_per_log_a_max=max(relaxation),
                         correction_scale_constraint_residual=max(constraint_errors),
                         background_final_spectral_correction_norm=heat ** 2 * float(norm(background[-1, :-1], basis.mass))))
        checks.extend([
            dict(name=model + ': fast thermal restoring coefficient positive at all saved times', passed=min(relaxation) > 0),
            dict(name=model + ': derived energy-row quasistatic thermal response resolves full temperature correction',
                 passed=thermal_error < .002, value=thermal_error),
            dict(name=model + ': gravity constraints at mixed corrections own source scale',
                 passed=max(constraint_errors) < .002, value=max(constraint_errors)),
            dict(name=model + ': moment projection exactly removes number and energy',
                 passed=float(np.max(abs(orthogonal @ moments.T))) < 1e-10 * max(float(np.max(norm(orthogonal, basis.mass))), 1e-100))])
        np.savez_compressed(folder / (model + '-thermal-law.npz'), expansion=expansion,
                            scaled_temperature=response[:, 10], quasistatic_temperature=instantaneous,
                            thermal_relaxation=relaxation, correction_constraints=constraint_errors)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        thermal_law='chi z_T_prime = -chi lambda_T (z_T-q_T); q_T derived from the remaining exact collision/gas row, no fitted coefficient.',
                        quasistatic_law_tested_along_coupled_solution_not_independent_reduced_wave=True,
                        spectrum_not_replaced_by_bolometric_energy=True,
                        figures_are_for_inherited_normalized_wave_not_observed_CMB_temperature=True), __file__,
           [ROOT / 'mixed_wave_system.py', *system.bank.inputs, *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          key_rows=[row for row in rows if 'monopole_energy_number_free_shape_fraction' in row])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--suffix', default='24-3200')
    parser.add_argument('--bank', default='fine16')
    main(parser.parse_args())
