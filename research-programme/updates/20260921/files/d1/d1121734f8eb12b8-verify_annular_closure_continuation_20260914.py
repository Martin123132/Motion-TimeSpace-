import hashlib
import json
import re
import traceback
from datetime import datetime
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_live_exterior_response_20260913 import load_prepared_system,LiveExteriorResponse
    from annular_joint_boundary_geometry_20260914 import ProtocolEvolution
    from annular_radial_response_20260914 import RadialGeometryVariation
    from annular_gram_smooth_limit_20260914 import smooth_limit_checks
    from annular_gram_joint_action_20260909 import gram_matrices

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    main_dir = intake/'annular-closure-continuation-attempt01'
    output_dir = intake/'annular-closure-continuation-independent-attempt01'
    destination = intake/'annular-closure-continuation-final-integrity.json'
    snapshot = intake/'annular-closure-continuation-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Preserve executed evidence.')
    output_dir.mkdir(exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
              'valid_for_physics_claim':False,'full_GR_limit_proven':False,'regulator_removed':False,
              'continuum_limit_proven':False,'global_stability_proven':False,'horizon_crossing_proven':False,
              'original_affine_inner_history_enforced':False,'initial_amplitudes_retuned':False,
              'perturbed_metric_histories_supplied':False,'conditional_continuation_complete':False,
              'protected_scan_scope':'mtime since 2026-09-13T23:38:53Z; not pre-turn hashes'}

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def load(path):
        with np.load(path,allow_pickle=False) as archive:
            return {key:archive[key].copy() for key in archive.files}

    def rk4(system,steps,duration=.032):
        state = system.initial_state.copy()
        step = duration/steps
        for index in range(steps):
            time = index*step
            first = system.evaluate_protocol(time,state,1.)['rhs']
            second = system.evaluate_protocol(time+step/2,state+step*first/2,1.)['rhs']
            third = system.evaluate_protocol(time+step/2,state+step*second/2,1.)['rhs']
            fourth = system.evaluate_protocol(time+step,state+step*third,1.)['rhs']
            state += step*(first+2*second+2*third+fourth)/6
        return state

    save()
    try:
        main = json.loads((main_dir/'status.json').read_text())
        check('main_matrix_completed_and_gates_passed',main['state']=='complete' and len(main['cases'])==6
              and all(row['state']=='complete' for row in main['cases']) and not main['failures']
              and all(row['passed'] for row in main['checks']))
        report['main_checks'] = len(main['checks'])
        for table in ['inputs','outputs']:
            for filename,expected in main[table].items():
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed source: '+filename)
                    report['inputs'][filename] = expected
        own(main_dir/'status.json')
        for path in main_dir.glob('*.npz'):
            with np.load(path,allow_pickle=False) as archive:
                check(path.name+'_all_arrays_finite',all(np.isfinite(archive[key]).all() for key in archive.files))
        for stem in ['annular_closure_continuation','derive_annular_closure_continuation','annular_gram_smooth_limit','verify_annular_closure_continuation']:
            path = root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            copy = output_dir/('executed-'+path.name)
            copy.write_bytes(path.read_bytes())
            own(copy,'outputs')
        check('four_new_scripts_compile_without_bytecode',True)
        smooth = smooth_limit_checks()
        check('exact_uniform_Gram_row_bound_and_positive_decomposition',smooth['row_bound_proven'] and smooth['positive_margins'],smooth['exact_row_bounds'])
        check('conditional_smooth_action_and_weak_variation_bounds',smooth['all_bounds_satisfied'],smooth['smooth_cases'])
        check('rough_fields_do_not_automatically_decouple',smooth['rough_nondecoupling_demonstrated'],smooth['rough_cases'])
        bounded_energy_rough = [{'count':row['count'],
                                 'extra_energy':row['extra_energy']/(row['count']-1)**2,
                                 'base_energy':row['base_energy']/(row['count']-1)**2} for row in smooth['rough_cases']]
        check('bounded_energy_alone_does_not_force_Gram_energy_to_zero',
              all(abs(row['base_energy']-2.)<1e-12 and 2.<row['extra_energy']<3. for row in bounded_energy_rough),bounded_energy_rough)
        smooth['bounded_energy_rough_controls'] = bounded_energy_rough
        nonzero_variations = []
        for count in [17,33,65,129]:
            radius = np.linspace(0.,1.,count)
            spacing = 1/(count-1)
            factors,sampling = gram_matrices(count)
            scalar = np.sin(2*np.pi*radius)+.1*radius**3
            variation = .4*scalar+np.cos(2*np.pi*radius)
            coefficient = 1+.2*np.cos(2*np.pi*radius)
            amplitude = factors @ scalar
            changed = factors @ variation
            derivative = float((sampling @ coefficient) @ (amplitude*changed)/spacing)
            epsilon = .001
            plus = factors @ (scalar+epsilon*variation)
            minus = factors @ (scalar-epsilon*variation)
            finite = float((sampling @ coefficient) @ (plus**2-minus**2)/(4*spacing*epsilon))
            scalar_norm_sq = (2*np.pi)**6/2+.36
            variation_norm_sq = 1.16*(2*np.pi)**6/2+.16*.36
            bound = float(3*coefficient.max()*spacing**4*np.sqrt(scalar_norm_sq*variation_norm_sq)/8)
            nonzero_variations.append({'count':count,'derivative':derivative,'finite_difference':finite,'bound':bound})
        check('nonzero_scalar_weak_variations_match_energy_differences',
              all(1e-8<abs(row['derivative'])<=row['bound'] and abs(row['derivative']-row['finite_difference'])<1e-10 for row in nonzero_variations),nonzero_variations)
        smooth['nonzero_scalar_variation_controls'] = nonzero_variations
        smooth_path = output_dir/'conditional_Gram_smooth_limit.json'
        smooth_path.write_text(json.dumps(smooth,indent=2)+'\n')
        own(smooth_path,'outputs')
        report['conditional_smooth_Gram_bound'] = smooth
        for branch in ['GR','metric_Gram']:
            report.update({'active_branch':branch,'phase':'independent_RK4_long_interval'})
            save()
            base,matched = load_prepared_system(root,branch,degree=20)
            system = ProtocolEvolution(base)
            response = LiveExteriorResponse(system,.032)
            label = branch+'_degree20'
            predicted = load(main_dir/(label+'_protocol_1.0_prediction.npz'))
            reference = load(main_dir/(label+'_protocol_1.0_reference.npz'))
            linear = load(main_dir/(label+'_linear_prediction.npz'))
            linear_reference = load(main_dir/(label+'_linear_reference.npz'))
            check(branch+'_same_unmodified_initial_profile',np.array_equal(system.initial_state,predicted['initial_state'])
                  and np.array_equal(system.initial_state,reference['initial_state']))
            coarse = rk4(system,128)
            fine = rk4(system,256)
            outputs = response.outputs(system.evaluate_protocol(.032,fine,1.))
            errors = {'state':float(abs(fine-predicted['states'][-1]).max()),
                      'temporal_refinement':float(abs(fine-coarse).max()),
                      'outputs':float(abs(outputs-predicted['outputs'][-1]).max())}
            check(branch+'_long_interval_joint_prediction_matches_independent_RK4',max(errors.values())<1e-8,errors)
            record = {'branch':branch,'RK4':errors,'prefixes':[]}
            for end in [.008,.016]:
                prefix = system.integrate_protocol(1.,duration=end,divisor=int(round(end/.001)))
                index = int(np.flatnonzero(reference['times']==end)[0])
                prefix_error = float(abs(prefix.y[:,-1]-reference['states'][index]).max())
                check(branch+'_prefix_'+str(end)+'_agrees_without_future_history_input',prefix_error<1e-9,prefix_error)
                record['prefixes'].append({'end':end,'state_error':prefix_error})
            baseline_state = linear['baseline_states'][-1]
            direction = linear['tangent'][-1]
            evaluation = system.evaluate(.032,baseline_state)
            radial = RadialGeometryVariation(system,evaluation,direction,1.)
            radii = np.unique(np.concatenate([system.radii,system.radii-system.width/4,system.radii+system.width/4]))
            derived = radial.evaluate(radii)
            exact = system.evaluate_protocol(.032,baseline_state+1j*1e-20*direction,1j*1e-20)['geometry'].metric(radii)
            radial_errors = {key:float(abs(value-exact[key].imag/1e-20).max()) for key,value in derived.items()}
            check(branch+'_derived_radial_response_survives_long_interval',max(radial_errors.values())<1e-10,radial_errors)
            record['radial_response_errors'] = radial_errors
            tangent_error = float(abs(linear['tangent']-linear_reference['states']).max())
            output_error = float(abs(linear['output_tangent']-linear_reference['outputs']).max())
            current_error = float(abs(linear['output_tangent'][:,0]-linear_reference['outputs'][:,0]).max())
            feedback = {'state_difference':float(abs(linear['one_way_tangent']-linear['tangent']).max()),
                        'output_difference':float(abs(linear['one_way_outputs']-linear['output_tangent']).max()),
                        'current_difference':float(abs(linear['one_way_outputs'][:,0]-linear['output_tangent'][:,0]).max()),
                        'state_comparison_error':tangent_error,'output_comparison_error':output_error,'current_comparison_error':current_error}
            feedback['output_resolved'] = feedback['output_difference']>max(100*output_error,1e-13)
            feedback['current_resolved'] = feedback['current_difference']>max(100*current_error,1e-13)
            record['feedback'] = feedback
            expected = next(row for row in main['cases'] if row['label']==label)['linear_response']
            check(branch+'_feedback_resolution_flag_recomputed_without_promotion',
                  feedback['output_resolved']==expected['one_way_output_effect_resolved']
                  and feedback['current_resolved']==expected['one_way_current_effect_resolved'],feedback)
            for parameter in [-1.,0.,1.]:
                key = str(parameter).replace('-','minus')
                archives = {degree:load(main_dir/(branch+'_degree'+str(degree)+'_protocol_'+key+'_reference.npz')) for degree in [12,16,20]}
                errors_by_pair = []
                for low,high in [(12,16),(16,20)]:
                    errors_by_pair.append({'low':low,'high':high,
                                           'initial':float(abs(archives[low]['profiles'][0]-archives[high]['profiles'][0]).max()),
                                           'profiles':float(abs(archives[low]['profiles']-archives[high]['profiles']).max()),
                                           'outputs':float(abs(archives[low]['outputs']-archives[high]['outputs']).max())})
                check(branch+'_'+str(parameter)+'_common_coordinate_spatial_replay',
                      max(max(row['profiles'],row['outputs']) for row in errors_by_pair)<1e-8
                      and max(row['initial'] for row in errors_by_pair)<1e-10,errors_by_pair)
            minimum_energy = float(system.unpack(fine)[0][:,-1].min())
            check(branch+'_RK4_preserves_positive_source_energy',minimum_energy>0,minimum_energy)
            initial_outputs = response.outputs(system.evaluate_protocol(0.,system.initial_state,1.))
            check(branch+'_RK4_total_mass_conserved',abs(outputs[6]-initial_outputs[6])<1e-9,float(abs(outputs[6]-initial_outputs[6])))
            output = output_dir/(branch+'_independent_long_run.npz')
            np.savez_compressed(output,rk4_coarse=coarse,rk4_fine=fine,rk4_outputs=outputs,radii=radii,
                                **{('radial_'+key):value for key,value in derived.items()})
            own(output,'outputs')
            report['cases'].append(record)
            save()
            print(json.dumps(record),flush=True)
        note = root/'DERIVATION-20260914-closure-continuation-and-resolution.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_source_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T23:38:53+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update({'state':'complete','conditional_continuation_complete':True,'protected_changed_count':len(changed)})
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'main_checks':report['main_checks'],
                          'protected_changed_count':len(changed)}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()
