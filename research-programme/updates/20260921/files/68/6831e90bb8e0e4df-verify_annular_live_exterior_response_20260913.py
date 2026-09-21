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
    from annular_live_exterior_response_20260913 import LiveExteriorResponse, TimeFit, load_prepared_system, PROBE_NAMES
    from annular_live_factor_response_20260913 import FiniteFactorExteriorResponse

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260913'
    evidence = intake/'annular-live-exterior-response-attempt01'
    destination = intake/'annular-live-exterior-response-final-integrity.json'
    snapshot = intake/'annular-live-exterior-response-resume-snapshot.md'
    extra = intake/'annular-live-exterior-response-independent-attempt01'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Do not overwrite executed evidence.')
    extra.mkdir(exist_ok=False)
    report = {'state':'running', 'checks':[], 'inputs':{}, 'outputs':{}, 'cases':[],
              'valid_for_physics_claim':False, 'full_GR_limit_proven':False,
              'trace_only_physical_port_derived':False, 'global_causal_wellposedness_proven':False,
              'original_affine_inner_history_enforced':False, 'new_forcing_added':False,
              'baseline_refitted':False, 'apparatus_support_stresses_derived':False,
              'conditional_live_boundary_response_complete':False,
              'protected_scan_scope':'mtime since 2026-09-13T21:27:19Z; not pre-turn hashes'}

    def save():
        destination.write_text(json.dumps(report, indent=2)+'\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name':name, 'passed':bool(passed), 'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def rk4(equation, initial, start, end, steps):
        state = initial.copy()
        step = (end-start)/steps
        for index in range(steps):
            time = start+index*step
            first = equation(time, state)
            second = equation(time+step/2, state+step*first/2)
            third = equation(time+step/2, state+step*second/2)
            fourth = equation(time+step, state+step*third)
            state += step*(first+2*second+2*third+fourth)/6
        return state

    save()
    try:
        main = json.loads((evidence/'status.json').read_text())
        check('main_complete_two_branches_twelve_central_probe_pairs',
              main['state']=='complete' and len(main['cases'])==2 and len(main['finite_probes'])==12
              and all(entry['passed'] for entry in main['checks']))
        report['main_checks'] = len(main['checks'])
        for table in ['inputs', 'outputs']:
            for filename, expected in main[table].items():
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed inherited source: '+filename)
                    report['inputs'][filename] = expected
        own(evidence/'status.json')
        for path in evidence.iterdir():
            if path.suffix=='.npz':
                with np.load(path, allow_pickle=False) as archive:
                    check(path.name+'_all_arrays_finite', all(np.isfinite(archive[key]).all() for key in archive.files))
        for stem in ['annular_live_exterior_response', 'derive_annular_live_exterior_response', 'annular_live_factor_response', 'verify_annular_live_exterior_response']:
            path = root/'scripts'/(stem+'_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            copied = extra/('executed-'+path.name)
            copied.write_bytes(path.read_bytes())
            own(copied, 'outputs')
        check('four_scripts_compile_without_bytecode', True)
        for branch in ['GR', 'metric_Gram']:
            report['active_branch'] = branch
            save()
            with np.load(evidence/(branch+'_live_operator.npz'), allow_pickle=False) as archive:
                samples = {key:archive[key].copy() for key in archive.files}
            system, matched = load_prepared_system(root, branch)
            response = LiveExteriorResponse(system)
            check(branch+'_original_baseline_exact_and_no_partition_overlap',
                  np.array_equal(system.initial_state, samples['reference_states'][:, 0])
                  and np.array_equal(samples['initial_directions'], response.directions)
                  and not response.retained[response.exterior].any()
                  and response.retained.sum()+len(response.exterior)==len(system.initial_state))
            state_fit = TimeFit(samples['reference_states'].T, response.duration)
            matrix_fit = TimeFit(samples['Aee'], response.duration)
            output_fit = TimeFit(samples['output_e'], response.duration)
            drive_fit = TimeFit(samples['retained_drive'], response.duration)
            offgrid = []
            for time in [.00071, .00213, .00369]:
                state = state_fit(time)
                exterior_direction = .3*np.sin(np.arange(response.exterior_size)+.7)
                exterior_direction[:response.exterior_size//2] *= .02
                direction = np.zeros(response.state_size)
                direction[response.exterior] = exterior_direction
                rhs, output = response.differential(time, state, direction)
                interpolation = max(float(abs(rhs[response.exterior]-matrix_fit(time) @ exterior_direction).max()),
                                    float(abs(output-output_fit(time) @ exterior_direction).max()))
                alternate_rhs, alternate_output = response.differential(time, state, direction, step=1e-25)
                step_error = max(float(abs(rhs-alternate_rhs).max()), float(abs(output-alternate_output).max()))
                finite_errors = []
                for amplitude in [2e-5, 1e-5]:
                    plus = system.evaluate(time, state+amplitude*direction)
                    minus = system.evaluate(time, state-amplitude*direction)
                    finite_rhs = (plus['rhs']-minus['rhs'])/(2*amplitude)
                    finite_output = (response.outputs(plus)-response.outputs(minus))/(2*amplitude)
                    finite_errors.append(max(float((abs(finite_rhs-rhs)/(1+abs(rhs))).max()),
                                             float((abs(finite_output-output)/(1+abs(output))).max())))
                offgrid.append({'time':time, 'operator_interpolation_error':interpolation,
                                'complex_step_size_error':step_error, 'central_difference_scaled_errors':finite_errors})
            check(branch+'_offgrid_jacobian_checked_by_real_finite_differences',
                  max(max(row['central_difference_scaled_errors']) for row in offgrid)<2e-7, offgrid)
            check(branch+'_offgrid_operator_time_interpolation_and_complex_step_control',
                  max(max(row['operator_interpolation_error'], row['complex_step_size_error']) for row in offgrid)<1e-8)
            size = response.exterior_size
            initial = np.column_stack([np.eye(size), np.zeros((size, 3))])

            def equation(time, values):
                derivative = matrix_fit(time) @ values
                derivative[:, size:] += drive_fit(time)
                return derivative

            coarse = rk4(equation, initial, 0., response.duration, 64)
            fine = rk4(equation, initial, 0., response.duration, 128)
            expected = samples['full_tangent_states'][-1, response.exterior]
            fine_tangent = fine[:, :size] @ response.directions[response.exterior]+fine[:, size:]
            coarse_tangent = coarse[:, :size] @ response.directions[response.exterior]+coarse[:, size:]
            midpoint = response.duration*.437
            first = rk4(lambda time, values:matrix_fit(time) @ values, np.eye(size), 0., midpoint, 96)
            second = rk4(lambda time, values:matrix_fit(time) @ values, np.eye(size), midpoint, response.duration, 96)
            propagator_error = float(abs(fine[:, :size]-samples['propagators'][-1]).max())
            memory_error = float(abs(fine_tangent-expected).max())
            refinement = float(abs(fine_tangent-coarse_tangent).max())
            semigroup = float(abs(second @ first-fine[:, :size]).max())
            check(branch+'_independent_RK4_memory_and_transition_composition',
                  max(propagator_error, memory_error, refinement, semigroup)<1e-8,
                  {'propagator':propagator_error, 'tangents':memory_error, 'refinement':refinement, 'composition':semigroup})
            controls = []
            for index, name in enumerate(PROBE_NAMES):
                for amplitude in [.001, .0005]:
                    pair = []
                    for sign in ['minus', 'plus']:
                        path = evidence/(branch+'_'+name+'_'+str(amplitude)+'_'+sign+'.npz')
                        with np.load(path, allow_pickle=False) as archive:
                            payload = {key:archive[key].copy() for key in archive.files}
                        expected_initial = system.initial_state+(-1 if sign=='minus' else 1)*amplitude*response.directions[:, index]
                        check(path.stem+'_declared_initial_state_unchanged', np.array_equal(expected_initial, payload['initial_state']))
                        first_output = response.outputs(system.evaluate(0., payload['initial_state']))
                        final_output = response.outputs(system.evaluate(response.duration, payload['states'][:, -1]))
                        check(path.stem+'_saved_output_recomputed_and_energy_conserved',
                              abs(final_output-payload['final_outputs']).max()<1e-12
                              and abs(final_output[6]-first_output[6])<1e-10
                              and min(system.unpack(state)[0][:, -1].min() for state in payload['states'].T)>0)
                        pair.append(payload)
                    derivative = (pair[1]['states'][:, -1]-pair[0]['states'][:, -1])/(2*amplitude)
                    observable = (pair[1]['final_outputs']-pair[0]['final_outputs'])/(2*amplitude)
                    errors = [float(abs(derivative-samples['full_tangent_states'][-1, :, index]).max()),
                              float(abs(observable-samples['full_output_tangent'][-1, :, index]).max())]
                    check(branch+'_'+name+'_'+str(amplitude)+'_central_trajectory_derivative_independent_recheck', max(errors)<1e-7, errors)
                    controls.append({'probe':name, 'amplitude':amplitude, 'errors':errors})
            factor = FiniteFactorExteriorResponse(system, response, samples)
            factor_record, factor_arrays = factor.run(samples)
            positive_offsets = np.linspace(1e-8, .5, 13)
            lower = np.minimum(system.anchor_base, system.target_base)[None, :]+system.width*positive_offsets[:, None]
            upper = np.maximum(system.anchor_base, system.target_base)[None, :]+system.width*positive_offsets[:, None]
            positive_crossings = int(((lower<system.radii[0]) & (upper>system.radii[0])).sum())
            check(branch+'_no_omitted_positive_half_cut_crossings', positive_crossings==0, positive_crossings)
            check(branch+'_exact_finite_factor_exterior_equation_and_live_current_replay',
                  max(factor_record[key] for key in ['force_algebra_error', 'live_factor_state_error', 'live_factor_current_error'])<1e-9,
                  factor_record)
            alternative = FiniteFactorExteriorResponse(system, response, samples, quadrature_order=32)
            current_check = max(abs(alternative.current(time, factor_arrays['factor_states'][:, index])-factor_arrays['factor_currents'][index])
                                for index, time in enumerate(samples['times']))
            check(branch+'_independent_crossing_current_quadrature_refinement', current_check<1e-10, float(current_check))
            check(branch+'_freezing_live_factor_coefficients_is_resolved',
                  factor_record['frozen_kinetic_stiffness_state_error']>max(100*factor_record['live_factor_state_error'], 1e-10))
            path = extra/(branch+'_finite_factor_response.npz')
            np.savez_compressed(path, **factor_arrays, rk4_coarse=coarse, rk4_fine=fine, transition_first=first, transition_second=second)
            own(path, 'outputs')
            report['cases'].append({'branch':branch, 'offgrid':offgrid, 'finite_controls':controls, 'factor_response':factor_record,
                                    'current_quadrature_refinement':float(current_check), 'RK4_tangent_error':memory_error,
                                    'RK4_propagator_error':propagator_error, 'RK4_refinement':refinement, 'transition_composition_error':semigroup})
            save()
            print(json.dumps(report['cases'][-1]), flush=True)
        note = root/'DERIVATION-20260913-live-exterior-response-and-energy-exchange.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_source_exists_'+citation, (root/citation).is_file())
        own(note, 'outputs')
        check('no_python_cache', not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T21:27:19+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update({'state':'complete', 'conditional_live_boundary_response_complete':True,
                       'finite_factor_input_response_tested':True, 'protected_changed_count':len(changed)})
        save()
        print(json.dumps({'state':report['state'], 'checks':len(report['checks']), 'main_checks':report['main_checks'],
                          'protected_changed_count':len(changed)}), flush=True)
    except Exception as error:
        report.update({'state':'failed', 'error':repr(error), 'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()

