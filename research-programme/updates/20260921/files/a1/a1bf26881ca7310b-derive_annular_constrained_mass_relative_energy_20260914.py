import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution
    from annular_constrained_mass_relative_energy_20260914 import (
        uniform_constants, density_energy, mass_gradient, mass_hessian, outer_data, fixed_source_direction)

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    output = intake/'annular-constrained-mass-relative-energy-attempt01'
    output.mkdir(exist_ok=False)
    report = {'state':'running', 'checks':[], 'inputs':{}, 'outputs':{}, 'cases':[],
              'conditional_live_relative_energy_theorem':True, 'unconditional_uniform_convergence':False,
              'full_GR_limit_proven':False, 'valid_for_physics_claim':False, 'stationary_source_only':True}

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
        predecessor = intake/'annular-compatible-h-evolution-final-integrity.json'
        inherited = json.loads(predecessor.read_text())
        check('predecessor_sealed_complete', inherited['state']=='complete' and all(row['passed'] for row in inherited['checks']))
        for table in ['inputs','outputs']:
            for filename, expected in inherited[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed inherited evidence: '+filename)
                report['inputs'][filename] = expected
        own(predecessor)
        for source in [Path(__file__), root/'scripts/annular_constrained_mass_relative_energy_20260914.py']:
            compile(source.read_bytes(), str(source), 'exec')
            own(source)
            snapshot = output/('executed-'+source.name)
            snapshot.write_bytes(source.read_bytes())
            own(snapshot, 'outputs')
        check('all_inherited_hashes_match_new_sources_compile', True)
        constants = uniform_constants()
        report['constants'] = constants
        check('connecting_density_chart_uniform', constants['connecting_F_floor']>constants['chosen_F_floor'])
        check('constrained_mass_strictly_coercive', constants['coercivity']>0, constants['coercivity'])
        check('explicit_uniform_reference_tangent_interval_positive', constants['uniform_tangent_comparison_time']>0)
        main = intake/'annular-compatible-h-evolution-main-attempt01'
        largest_normalization_error = 0.
        for count in [33,65,129]:
            systems = [CompatibleEvolution(count, gram) for gram in [False,True]]
            saved = []
            for label in ['GR_control','metric_Gram']:
                with np.load(main/(label+'_count'+str(count)+'.npz'), allow_pickle=False) as archive:
                    saved.append({name:archive[name].copy() for name in ['times','states']})
            for index in [0,8,16]:
                time = float(saved[0]['times'][index])
                states = [entry['states'][index] for entry in saved]
                directions = [system.rhs(time,state) for system,state in zip(systems,states)]
                geometries = [system.geometry(time,state) for system,state in zip(systems,states)]
                delta = states[1]-states[0]
                masses, clocks = zip(*[outer_data(geometry) for geometry in geometries])
                ratio = clocks[1]/clocks[0]
                first = mass_gradient(systems[0], geometries[0], delta)
                relative = float(masses[1]-masses[0]-first)
                error_energy = float(density_energy(systems[0],delta))
                extra_energy = float(density_energy(systems[1],states[1],extra=True))
                reference_energy = float(density_energy(systems[0],directions[0]))
                reference_extra = float(density_energy(systems[0],directions[0],extra=True))
                step = 1e-20
                changed_states = [state+1j*step*direction for state,direction in zip(states,directions)]
                changed_geometry = [system.geometry(time,state) for system,state in zip(systems,changed_states)]
                changed_masses = [outer_data(geometry)[0] for geometry in changed_geometry]
                changed_first = mass_gradient(systems[0],changed_geometry[0],changed_states[1]-changed_states[0])
                direct_rate = float((changed_masses[1]-changed_masses[0]-changed_first).imag/step)
                hessian_pair = float(mass_hessian(systems[0],time,states[0],directions[0],delta))
                reference_pair = mass_gradient(systems[0],geometries[0],directions[0])
                actual_pair = mass_gradient(systems[1],geometries[1],directions[0])
                predicted_rate = float(ratio*(actual_pair-reference_pair)-hessian_pair)
                shadow = systems[0].geometry(time,states[1])
                shadow_pair = mass_gradient(systems[0],shadow,directions[0])
                nonlinear = float(shadow_pair-reference_pair-hessian_pair)
                correction = float(actual_pair-shadow_pair)
                clock_term = float((ratio-1)*hessian_pair)
                lower = constants['coercivity']*error_energy+constants['weight_lower']*extra_energy
                upper = (1+2*constants['density_second']*constants['energy_ceiling'])*error_energy+extra_energy
                nonlinear_bound = .5*constants['phase_third']*error_energy*np.sqrt(reference_energy)
                correction_bound = 2*constants['density_second']*np.sqrt(constants['energy_ceiling']*reference_energy)*extra_energy
                correction_bound += 2*np.sqrt(extra_energy*reference_extra)
                total_bound = constants['relative_rate']*np.sqrt(reference_energy)*relative
                total_bound += 2*constants['forcing_coefficient']*np.sqrt(max(0.,relative)*reference_extra)
                label = 'count'+str(count)+'_sample'+str(index)
                check(label+'_positive_coercive_mass_energy', relative>=lower-2e-11 and relative<=upper+2e-11,
                      {'relative':relative,'lower':lower,'upper':upper})
                check(label+'_exact_live_mass_relative_rate',abs(predicted_rate-direct_rate)<2e-10,
                      {'direct':direct_rate,'predicted':predicted_rate})
                check(label+'_nonlinear_remainder_uniform_bound',abs(nonlinear)<=nonlinear_bound+2e-10)
                check(label+'_Gram_feedback_uniform_bound',abs(correction)<=correction_bound+2e-10)
                check(label+'_complete_live_rate_bound',abs(direct_rate)<=total_bound+2e-10)
                check(label+'_three_term_identity',abs(ratio*(nonlinear+correction)+clock_term-predicted_rate)<2e-12)
                normalization_errors = []
                for branch,(system,state,geometry) in enumerate(zip(systems,states,geometries)):
                    test = fixed_source_direction(system,state)
                    analytic = mass_gradient(system,geometry,test)
                    mass_rate = outer_data(system.geometry(time,state+1j*step*test))[0].imag/step
                    difference = abs(analytic-mass_rate)
                    check(label+'_branch'+str(branch)+'_mass_variational_gradient',difference<2e-10,float(difference))
                    wrong = clocks[branch]*analytic
                    normalization_errors.append(float(abs(wrong-mass_rate)))
                largest_normalization_error = max(largest_normalization_error,*normalization_errors)
                tangent = .5*float(mass_hessian(systems[0],time,states[0],directions[0],directions[0]))
                check(label+'_reference_tangent_coercivity',tangent>=constants['coercivity']*reference_energy-2e-9)
                if index==0:
                    check(label+'_analytic_initial_reference_rate_bound',reference_energy<=constants['reference_initial_energy_bound'])
                    check(label+'_initial_matching',error_energy==0.)
                row = dict(count=count,time=time,relative_energy=relative,error_energy=error_energy,extra_energy=extra_energy,
                           reference_rate_energy=reference_energy,reference_Gram_rate_energy=reference_extra,
                           direct_rate=direct_rate,predicted_rate=predicted_rate,rate_error=abs(direct_rate-predicted_rate),
                           nonlinear_remainder=nonlinear,Gram_feedback=correction,clock_remainder=clock_term,
                           live_rate_bound=total_bound,outer_clocks=[float(value) for value in clocks],
                           omitted_outer_normalization_error=normalization_errors,reference_tangent_energy=tangent)
                report['cases'].append(row)
                save()
                print(json.dumps(row),flush=True)
        check('omitted_outer_clock_normalization_is_resolved',largest_normalization_error>1e-8,largest_normalization_error)
        report['state'] = 'complete'
        save()
        print(json.dumps({'state':'complete','checks':len(report['checks']),'constants':constants}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

