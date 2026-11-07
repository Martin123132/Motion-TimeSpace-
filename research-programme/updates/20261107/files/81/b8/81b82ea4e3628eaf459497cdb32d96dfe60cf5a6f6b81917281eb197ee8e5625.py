from common import *
from adjoint_operator import open_owned, relative, sup
from physical_energy_map import PhysicalEnergyMap
from comparison_math import controls, symbolic as energy_symbolic
from stress_math import StressEnergy, SPECIES, GROUPS, symbolic
from scipy.interpolate import make_interp_spline
import numpy as np
import csv


def main():
    modest()
    check_parent()
    (ROOT / 'contexts').mkdir(exist_ok=False)
    write(ROOT / 'inputs.json', dict(sources=frozen_sources(), parent_seal=PARENT_SEAL, numerical=GATE, algebra=ALGEBRA))
    write(ROOT / 'symbolic.json', dict(shear=symbolic(), inherited_energy=energy_symbolic()))
    reports = []
    for model in ('heavy', 'cold'):
        guard()
        path = POISSON / 'evolution' / (model + '-gr.npz')
        reference = load(path)
        system = open_owned(model, 'contexts')
        energy = PhysicalEnergyMap(system)
        kinetic = StressEnergy(system, energy)
        grid, states, terms = reference['efold'], reference['evolved_state'], reference['terms']
        hubble = reference['H']
        alpha = states[:, system.alpha_slot]
        values = {name: reference['values'][:, index] for index, name in enumerate(reference['value_names'])}
        current = terms[:, :, 1] + terms[:, :, 5] * (system.wave * alpha)[:, None]
        density = terms[:, :, 0] - terms[:, :, 5] * (3 * hubble * alpha)[:, None]
        shear = terms[:, :, 6]
        errors = dict(physical_current_sum=relative(current.sum(axis=1) - values['Q'], values['Q']),
                      physical_density_sum=relative(density.sum(axis=1) - values['D'], values['D']),
                      physical_shear_sum=relative(shear.sum(axis=1) - values['Pi'], values['Pi']),
                      scalar_linear_shear=sup(shear[:, [5, 6]]))
        require(max(errors.values()) < ALGEBRA, 'physical species reconstruction')
        histories = kinetic.histories(reference)
        indices = np.unique(np.linspace(1, len(grid) - 2, 97, dtype=int))
        qualification, samples = {}, []
        generator = np.random.default_rng(713)
        for number, index in enumerate(indices):
            guard()
            for perturbed in ((False, True) if number % 16 == 0 else (False,)):
                state = states[index].copy()
                if perturbed:
                    state += .01 * system.units * generator.standard_normal(len(state))
                record = kinetic.qualification(float(grid[index]), state)
                for name, value in record.items():
                    if name not in ('norms', 'source_norms'):
                        qualification[name] = max(qualification.get(name, 0.), float(value))
                if not perturbed:
                    qualification['direct_history_norm'] = max(qualification.get('direct_history_norm', 0.), relative(record['norms'] - histories['norms'][index], record['norms']))
                    qualification['direct_history_force'] = max(qualification.get('direct_history_force', 0.), relative(record['source_norms'] - np.linalg.norm(histories['source'][index], axis=1), record['source_norms']))
                samples.append(dict(index=int(index), perturbed=perturbed, **{key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in record.items()}))
        passed = max(qualification.values()) < GATE and max(qualification[name] for name in ('photon_symmetric_excess', 'massless_symmetric_excess', 'scalar_shear')) < ALGEBRA
        write(ROOT / (model + '-qualification.json'), dict(passed=passed, errors=qualification, species_errors=errors, samples=samples))
        print(LABEL, model, 'qualified', passed, qualification, flush=True)
        require(passed, 'preserve native energy identity discrepancy')
        source_spline = make_interp_spline(grid, histories['source'], k=5, axis=0)
        forcing = np.empty((len(grid) - 1, 3))
        for first in range(0, len(grid) - 1, 256):
            guard()
            last = min(first + 256, len(grid) - 1)
            coefficients = controls(source_spline, grid[first:last], grid[first + 1:last + 1])
            forcing[first:last] = np.linalg.norm(coefficients, axis=-1).max(axis=1) * (1 + 64 * np.finfo(float).eps)
        upper = np.empty_like(histories['norms'])
        upper[0] = histories['norms'][0]
        for index, width in enumerate(np.diff(grid)):
            decay = np.exp(-width)
            upper[index + 1] = decay * upper[index] - np.expm1(-width) * forcing[index]
        energy_excess = sup(np.maximum(histories['norms'] - upper, 0)) / max(sup(upper), 1e-80)
        direct_shear_upper = histories['factors'] * histories['norms'] + histories['endpoints']
        propagated_shear_upper = histories['factors'] * upper + histories['endpoints']
        radiative_shear = abs(shear[:, [2, 3, 4]])
        projection_excess = sup(np.maximum(radiative_shear - direct_shear_upper, 0)) / max(sup(radiative_shear), 1e-80)
        bound_excess = sup(np.maximum(radiative_shear - propagated_shear_upper, 0)) / max(sup(radiative_shear), 1e-80)
        require(energy_excess < GATE and bound_excess < GATE and projection_excess < ALGEBRA, 'kinetic comparison gate')
        cdm_envelope = sup(values['delta_c'])
        rows = []
        for column, name in enumerate(SPECIES):
            row = dict(family=LABEL, model=model, species=name, raw_units='Mpc^-2', cdm_envelope=cdm_envelope)
            for label, packet in (('Q', current), ('Pi', shear)):
                vector = packet[:, column]
                row[label + '_raw_sup'] = sup(vector)
                row[label + '_raw_rms_N'] = float(np.sqrt(np.trapezoid(vector**2, grid) / (grid[-1] - grid[0])))
                row[label + '_normalized_sup'] = sup(vector / (hubble**2 * cdm_envelope))
                row[label + '_raw_final'] = float(vector[-1])
            rows.append(row)
        with (ROOT / (model + '-species.csv')).open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        file = ROOT / (model + '-stress.npz')
        np.savez_compressed(file, efold=grid, H=hubble, current=current, density=density, shear=shear,
                            norms=histories['norms'], factors=histories['factors'], endpoints=histories['endpoints'],
                            source=histories['source'], forcing=forcing, energy_upper=upper,
                            shear_upper=propagated_shear_upper, cdm_envelope=cdm_envelope,
                            radiative_density=histories['density'][:, 2:4], massive=histories['massive'], speeds=histories['speeds'])
        normalized = radiative_shear / (hubble**2 * cdm_envelope)[:, None]
        normalized_upper = propagated_shear_upper / (hubble**2 * cdm_envelope)[:, None]
        report = dict(model=model, passed=True, original_nodes=len(grid), qualification_count=len(samples), ufa=kinetic.ufa,
                      current_sum_errors=errors, qualification=qualification, energy_excess=energy_excess,
                      projection_excess=projection_excess, bound_excess=bound_excess, cdm_envelope=cdm_envelope,
                      original_input=str(path), original_sha256=digest(path), output=str(file), output_sha256=digest(file),
                      groups=GROUPS, normalized_actual_shear_sup=normalized.max(axis=0).tolist(),
                      normalized_bound_shear_sup=normalized_upper.max(axis=0).tolist(),
                      total_shear_raw_sup=sup(values['Pi']), total_shear_normalized_sup=sup(values['Pi'] / (hubble**2 * cdm_envelope)),
                      total_current_raw_sup=sup(values['Q']), total_current_normalized_sup=sup(values['Q'] / (hubble**2 * cdm_envelope)),
                      cancellation_shear_rms=float(np.sqrt(np.trapezoid(values['Pi']**2, grid)) / sum(np.sqrt(np.trapezoid(shear[:, column]**2, grid)) for column in range(7))),
                      minimum_speed=float(histories['speeds'].min()), maximum_speed=float(histories['speeds'].max()),
                      new_physical_ode_solves=0, numerical_scope='Exact kinetic estimate with Bernstein envelope of original-grid quintic forcing; unsupplied continuum interpolation remainder not certified')
        write(ROOT / (model + '-result.json'), report)
        print(LABEL, model, 'species', [(row['species'], row['Pi_raw_sup'], row['Pi_normalized_sup']) for row in rows], flush=True)
        reports.append(report)
        del reference, system, energy, kinetic, histories, source_spline, states, terms
    for path, expected in read(ROOT / 'inputs.json')['sources'].items():
        require(digest(path) == expected, 'frozen stage source')
    check_parent()
    write(ROOT / 'result.json', dict(passed=True, reports=reports))


if __name__ == '__main__':
    main()
