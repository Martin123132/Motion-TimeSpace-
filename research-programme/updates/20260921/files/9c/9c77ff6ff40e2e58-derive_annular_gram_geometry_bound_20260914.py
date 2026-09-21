import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_gram_geometry_bound_20260914 import MatchedConstraintSystem, analytic_constants, propagation_bounds

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    output = intake/'annular-gram-geometry-bound-attempt01'
    output.mkdir(exist_ok=False)
    report = {'state':'running', 'checks':[], 'inputs':{}, 'outputs':{}, 'cases':[],
              'manufactured_constraint_family_only':True, 'physical_spacing_varied':True,
              'dynamical_h_family_evolved':False, 'uniform_H3_solution_bound_proven':False,
              'full_GR_limit_proven':False, 'valid_for_physics_claim':False,
              'physical_node_interval':[5., 6.], 'counts':[17,33,65,129], 'width_to_spacing':.5,
              'parameters_fitted':False, 'geometric_units':'declared pilot units, not SI'}

    def save():
        (output/'status.json').write_text(json.dumps(report, indent=2)+'\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name':name, 'passed':bool(passed), 'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        previous_path = intake/'annular-closure-continuation-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('predecessor_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        for table in ['inputs','outputs']:
            for filename, expected in previous[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed inherited evidence: '+filename)
                report['inputs'][filename] = expected
        own(previous_path)
        check('inherited_source_and_evidence_hashes_match', True)
        for path in [Path(__file__), root/'scripts/annular_gram_geometry_bound_20260914.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = output/('executed-'+path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        check('new_scripts_compile_without_bytecode', True)
        radii = np.linspace(5., 6., 513)
        for profile in ['smooth', 'bounded_energy_rough']:
            for count in report['counts']:
                label = profile+'_count'+str(count)
                report['active_case'] = label
                save()
                geometries = []
                metrics = []
                for gamma in [0., .5, 1.]:
                    system = MatchedConstraintSystem(count, gamma, profile=profile)
                    geometry = system.geometry()
                    geometries.append(geometry)
                    metrics.append(geometry.metric(radii))
                integrals = system.integrated_densities()
                refined_integrals = system.integrated_densities(72)
                check(label+'_density_quadrature_converged', max(abs(integrals[key]-refined_integrals[key]) for key in integrals)<1e-11)
                constants = analytic_constants(system.spacing)
                tight = propagation_bounds(integrals['extra'], integrals['kinetic'])
                mass_difference = metrics[-1]['mu']-metrics[0]['mu']
                log_difference = metrics[-1]['log_N']-metrics[0]['log_N']
                check(label+'_matched_free_fields_and_proper_source', all(np.array_equal(geometry.system.initial_state, geometries[0].system.initial_state) for geometry in geometries))
                check(label+'_positive_mass_and_negative_interior_lapse_response', mass_difference.min()>-2e-13 and log_difference.max()<2e-13)
                check(label+'_homotopy_ordering', all((second['mu']-first['mu']).min()>-2e-13 and (second['log_N']-first['log_N']).max()<2e-13 for first,second in zip(metrics[:-1],metrics[1:])))
                check(label+'_regular_radial_constraints', min(geometry.minimum_F for geometry in geometries)>.5 and max(geometry.collocation_defect for geometry in geometries)<1e-11)
                check(label+'_exact_integral_geometry_bounds', mass_difference.max()<=tight['mass_difference_bound']+2e-13 and -log_difference.min()<=tight['log_lapse_difference_bound']+2e-13)
                if profile == 'smooth':
                    check(label+'_analytic_smooth_energy_and_geometry_bounds', integrals['extra']<=constants['extra_integral_bound'] and mass_difference.max()<=constants['mass_difference_bound']+2e-13 and -log_difference.min()<=constants['log_lapse_difference_bound']+2e-13)
                    check(label+'_uniform_regular_chart_proved_by_energy_barrier', constants['proven_uniform_F_lower']>.5)
                record = {'label':label, 'profile':profile, 'count':count, 'spacing':system.spacing, 'width':system.width,
                          'radial_degree':32, 'integrals':integrals, 'minimum_F_sampled':min(geometry.minimum_F for geometry in geometries),
                          'maximum_constraint_defect':max(geometry.collocation_defect for geometry in geometries),
                          'max_mass_difference':float(mass_difference.max()), 'max_log_lapse_difference':float(-log_difference.min()),
                          'outer_mass_difference':float(mass_difference[-1]), 'analytic_bounds':constants if profile=='smooth' else None,
                          'measured_integral_bounds':tight}
                archive = output/(label+'.npz')
                np.savez_compressed(archive, radii=radii, initial_state=system.initial_state,
                                    masses=np.stack([metric['mu'] for metric in metrics]),
                                    log_lapses=np.stack([metric['log_N'] for metric in metrics]),
                                    mass_difference=mass_difference, log_lapse_difference=log_difference)
                own(archive, 'outputs')
                report['cases'].append(record)
                save()
                print(json.dumps(record), flush=True)
        for profile in ['smooth','bounded_energy_rough']:
            rows = [row for row in report['cases'] if row['profile']==profile]
            orders = {key:[float(np.log(first[key]/second[key])/np.log(2)) for first,second in zip(rows[:-1],rows[1:])]
                      for key in ['max_mass_difference','max_log_lapse_difference']}
            report[profile+'_orders'] = orders
        check('smooth_geometry_differences_approach_fourth_order', min(values[-1] for values in report['smooth_orders'].values())>3.5)
        rough = [row for row in report['cases'] if row['profile']=='bounded_energy_rough']
        check('bounded_energy_rough_control_does_not_decouple', rough[-1]['max_mass_difference']>1e-4 and rough[-1]['max_mass_difference']>.5*rough[0]['max_mass_difference'])
        report['state'] = 'complete'
        save()
        print(json.dumps({'state':report['state'], 'checks':len(report['checks']), 'cases':len(report['cases'])}), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    run()
