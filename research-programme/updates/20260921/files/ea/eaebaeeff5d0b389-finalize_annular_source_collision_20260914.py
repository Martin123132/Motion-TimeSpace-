import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import csv
import json
import numpy as np
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_reflecting_boundary_20260914 import ReflectingContinuum
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from compare_annular_regulators_to_continuum_20260914 import compare, target_refinement_noise
from run_annular_source_collision_regulators_20260914 import physical_errors
from verify_annular_collision_and_support_20260914 import support


def run():
    evidence = EvidenceRun('annular-source-collision-final-comparison-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        paths = dict(regulators=intake/'annular-source-collision-regulators-attempt01/status.json',
                     target=intake/'annular-collision-refined-target-attempt01/status.json')
        reports = {}
        for label, path in paths.items():
            evidence.own(path)
            reports[label] = json.loads(path.read_text())
            evidence.check(label+'_completed', reports[label]['state'] == 'complete' and all(row['passed'] for row in reports[label]['checks']))
        archives = {}
        for count, folder in [(2049, 'annular-source-collision-continuum-attempt01'), (4097, 'annular-collision-refined-target-attempt01')]:
            path = intake/folder/('continuum_count'+str(count)+'.npz')
            evidence.own(path)
            archives[count] = dict(np.load(path, allow_pickle=False))
        evidence.report.update(target_nodes=4097, target_noise_nodes=2049,
                               boundary_force_convention='Scalar-conjugate reaction b^2 L chi_R, not radial mechanical force.',
                               identical_two_percent_resolution_gate_for_both_branches=True,
                               no_production_parameters_refitted=True, counterfactual_source_parameter_check_is_not_a_fit=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False,
                               original_failed_radial_gate_preserved=True,
                               original_boundary_solver_failed_active_control=True)
        for count in [33, 65, 129]:
            for gram, label in [(False, 'reference'), (True, 'MTS')]:
                system = CompatibleEvolution(count, gram, degree=8)
                path = paths['regulators'].parent/(label+'_count'+str(count)+'.npz')
                evidence.own(path)
                trajectory = dict(np.load(path, allow_pickle=False))
                for time, state in zip(trajectory['times'], trajectory['states']):
                    index = int(np.argmin(abs(archives[4097]['times']-time)))
                    evidence.check(label+str(count)+'_'+str(time)+'_time_match', abs(archives[4097]['times'][index]-time) < 1e-14)
                    old = next(row for row in reports['regulators']['cases'] if row['branch'] == label and row['count'] == count and row['time'] == time)
                    row = dict(old)
                    updated, profiles = compare(system, time, state, archives[4097], index)
                    row.update(updated)
                    row.update(physical_errors(system, state, time, archives[4097], archives[2049], index))
                    noise = target_refinement_noise(count, archives[4097], archives[2049], index)
                    row.update(target_noise=noise, target_wall_force=reports['target']['diagnostics'][index]['wall_force'],
                               target_required_surface_pressure=reports['target']['diagnostics'][index]['source_pressure'])
                    row['wall_force_error'] = abs(row['holding_reaction_mean']-row['target_wall_force'])
                    row['valid_for_physics_claim'] = False
                    row['largest_target_noise_fraction'] = max([value/max(row[key], 1e-300) for key, value in noise.items()]+
                        [row['physical_target_noise_norm']/max(row['physical_energy_norm'], 1e-300)])
                    evidence.report['cases'].append(row)
                    prefix = label+str(count)+'_'+str(time)
                    evidence.check(prefix+'_same_target_resolution_gate', row['largest_target_noise_fraction'] < .02, row['largest_target_noise_fraction'])
                    evidence.check(prefix+'_finite_same_fields', all(np.isfinite(row[key]) for key in
                        ['energy_error', 'physical_energy_error', 'chi_L2', 'mass_max_error', 'log_lapse_max_error', 'wall_force_error']))
                    if time == .45:
                        output = evidence.output/(label+'_count'+str(count)+'_final_profiles.npz')
                        np.savez_compressed(output, **profiles)
                        evidence.own(output, 'outputs')
        refinement = []
        for label in ['reference', 'MTS']:
            for time in [.3, .4, .45]:
                rows = [row for row in evidence.report['cases'] if row['branch'] == label and row['time'] == time]
                for key in ['energy_error', 'physical_energy_error', 'chi_L2', 'mass_max_error', 'log_lapse_max_error']:
                    values = [row[key] for row in rows]
                    refinement.append(dict(branch=label, time=time, quantity=key, values=values,
                                           decreases=all(later < earlier for earlier, later in zip(values, values[1:]))))
        evidence.report['collision_refinement'] = refinement
        evidence.report['both_branches_refine_all_declared_collision_norms'] = all(row['decreases'] for row in refinement)
        force_refinement = []
        for label in ['reference', 'MTS']:
            values = [max(row['wall_force_error'] for row in evidence.report['cases'] if row['branch'] == label and row['count'] == count and row['time'] >= .3) for count in [33, 65, 129]]
            force_refinement.append(dict(branch=label, sampled_max_force_errors=values,
                                         decreases=all(later < earlier for earlier, later in zip(values, values[1:]))))
        evidence.report['wall_force_refinement'] = force_refinement
        normal = ReflectingContinuum(4097)
        alternative = ReflectingContinuum(4097, reservoir=.8)
        ratios, loading = [], []
        for index in [0, 30, 37, 45]:
            state = archives[4097]['states'][index]
            time = archives[4097]['times'][index]
            first = normal.geometry(state)
            second = alternative.geometry(state)
            ratio = second['N_shell']/first['N_shell']
            error = float(abs(alternative.rhs(time, state)-ratio*normal.rhs(time, state)).max())
            ratios.append(float(ratio))
            evidence.check('source_clock_rescaling_'+str(index), error < 5e-11 and np.array_equal(first['mass'], second['mass']), error)
        evidence.check('source_clock_ratio_constant_to_numerical_mass_accuracy', np.ptp(ratios) < 1e-10, ratios)
        for state, row in zip(archives[4097]['states'], reports['target']['diagnostics']):
            geometry = normal.geometry(state)
            sigma, pressure, root_plus = support(6., .1, .8, geometry['U_minus'], geometry['density'][-1])
            loading.append(dict(time=row['time'], candidate_surface_density=float(sigma), candidate_pressure=float(pressure),
                                candidate_nec=float(sigma+pressure), candidate_dominant_margin=float(sigma-abs(pressure)),
                                candidate_root_plus=float(root_plus)))
        evidence.report['counterfactual_source_loading'] = dict(reservoir=.8, production_reservoir=.003, rows=loading,
            scope='Only sampled continuum orbit under proved conditional clock rescaling; not a fitted or parent-derived source, not a continuous-time maximum proof.')
        evidence.check('counterfactual_sampled_classical_margins', min(row['candidate_dominant_margin'] for row in loading) > 0 and min(row['candidate_root_plus'] for row in loading) > 0)
        pressures = [row['source_pressure'] for row in reports['target']['diagnostics']]
        evidence.check('fixed_density_requires_nonconstant_pressure', np.ptp(pressures) > .01)
        evidence.report['fixed_radius_single_barotropic_surface_cannot_supply_recorded_pressure'] = True
        evidence.report['surface_energy_first_law'] = 'Sigma=S(b)/b^2; P=-S_prime(b)/(2b), for adiabatic fixed-particle-number isotropic surface matter.'
        table = evidence.output/'collision-comparison.csv'
        columns = ['branch', 'count', 'time', 'energy_error', 'physical_energy_error', 'chi_L2', 'mass_max_error',
                   'log_lapse_max_error', 'holding_reaction_mean', 'target_wall_force', 'wall_force_error', 'largest_target_noise_fraction', 'valid_for_physics_claim']
        with table.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(evidence.report['cases'])
        with table.open(newline='', encoding='utf-8') as stream:
            parsed = list(csv.DictReader(stream))
        evidence.check('csv_all42_rows_parse', len(parsed) == 42 and all(set(row) == set(columns) for row in parsed))
        evidence.own(table, 'outputs')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
