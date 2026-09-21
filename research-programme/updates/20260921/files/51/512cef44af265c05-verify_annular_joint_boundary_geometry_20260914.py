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
    from annular_live_exterior_response_20260913 import load_prepared_system, TimeFit
    from annular_joint_boundary_geometry_20260914 import ProtocolEvolution, JointSchurResponse
    from annular_radial_response_20260914 import RadialGeometryVariation

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    main_dir = intake/'annular-joint-boundary-geometry-attempt01'
    output_dir = intake/'annular-joint-boundary-geometry-independent-attempt01'
    seal = intake/'annular-joint-boundary-geometry-final-integrity.json'
    snapshot = intake/'annular-joint-boundary-geometry-resume-snapshot.md'
    if seal.exists() or snapshot.exists():
        raise FileExistsError('Preserve executed evidence.')
    output_dir.mkdir(exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
              'valid_for_physics_claim':False,'full_GR_limit_proven':False,'one_point_boundary_action_derived':False,
              'continuum_wellposedness_proven':False,'apparatus_support_stresses_derived':False,
              'original_affine_inner_history_enforced':False,'baseline_refitted':False,'new_parent_coefficient_fitted':False,
              'perturbed_metric_histories_supplied':False,'conditional_joint_boundary_geometry_complete':False,
              'protected_scan_scope':'mtime since 2026-09-13T23:06:13Z; not pre-turn hashes'}

    def save():
        seal.write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def rk4(system,parameter,steps,duration=.004):
        state = system.initial_state.copy()
        step = duration/steps
        for index in range(steps):
            time = index*step
            first = system.evaluate_protocol(time,state,parameter)['rhs']
            second = system.evaluate_protocol(time+step/2,state+step*first/2,parameter)['rhs']
            third = system.evaluate_protocol(time+step/2,state+step*second/2,parameter)['rhs']
            fourth = system.evaluate_protocol(time+step,state+step*third,parameter)['rhs']
            state += step*(first+2*second+2*third+fourth)/6
        return state

    save()
    try:
        main = json.loads((main_dir/'status.json').read_text())
        check('main_complete_two_branches_eight_joint_protocol_solutions',
              main['state']=='complete' and len(main['cases'])==2 and all(row['passed'] for row in main['checks'])
              and all(len(row['finite_protocols'])==4 for row in main['cases']))
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
        for stem in ['annular_joint_boundary_geometry','derive_annular_joint_boundary_geometry','annular_radial_response','verify_annular_joint_boundary_geometry']:
            path = root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            copied = output_dir/('executed-'+path.name)
            copied.write_bytes(path.read_bytes())
            own(copied,'outputs')
        check('four_scripts_compile_without_bytecode',True)
        for branch in ['GR','metric_Gram']:
            report['active_branch'] = branch
            save()
            base,matched = load_prepared_system(root,branch)
            system = ProtocolEvolution(base)
            with np.load(main_dir/(branch+'_predicted_response_before_reference.npz'),allow_pickle=False) as archive:
                predicted = {key:archive[key].copy() for key in archive.files}
            with np.load(main_dir/(branch+'_joint_protocol_1.0.npz'),allow_pickle=False) as archive:
                joint = {key:archive[key].copy() for key in archive.files}
            with np.load(root/'source-intake/navier-stokes/20260913/annular-live-exterior-response-attempt01'/(branch+'_live_operator.npz'),allow_pickle=False) as archive:
                old = {key:archive[key].copy() for key in archive.files}
            joint_fit = TimeFit(joint['states'],.004)
            record = {'branch':branch,'radial_variations':[]}
            for name,time,parameter_direction in [('mixed_field_and_protocol',.00213,1.),('source_protocol_only',.00369,1.)]:
                state = joint_fit(time)
                evaluation = system.evaluate_protocol(time,state,1.)
                if name=='source_protocol_only':
                    direction = np.zeros_like(state)
                else:
                    values = np.zeros_like(system.unpack(state)[0])
                    free = len(system.radii)-1
                    values[:,:free] = .0001*np.sin(np.arange(free)[None,:]+system.grid.offsets[:,None])
                    values[:,free:2*free] = .01*np.cos(np.arange(free)[None,:]+system.grid.offsets[:,None])
                    values[:,2*free] = .001
                    values[:,-1] = .0001*(1-4*system.grid.offsets**2)
                    direction = system.pack(values,0.)
                radial = RadialGeometryVariation(system,evaluation,direction,parameter_direction)
                radii = np.unique(np.concatenate([system.radii,system.radii[:-1]+np.diff(system.radii)/2,
                                                 system.radii-system.width/4,system.radii+system.width/4]))
                derived = radial.evaluate(radii)
                varied = system.evaluate_protocol(time,state+1j*1e-20*direction,1.+1j*1e-20*parameter_direction)
                exact = {key:value.imag/1e-20 for key,value in varied['geometry'].metric(radii).items()}
                errors = {key:float(abs(derived[key]-exact[key]).max()) for key in derived}
                check(branch+'_'+name+'_derived_radial_Green_response',max(errors.values())<1e-10,errors)
                outer = np.array([system.radii[-1]])
                outer_variation = radial.evaluate(outer)
                outer_fields = evaluation['geometry'].metric(outer)
                clock_error = float(abs(outer_variation['log_N'][0]+outer_variation['mu'][0]/(outer[0]*outer_fields['U'][0]**2)))
                check(branch+'_'+name+'_outer_clock_normalization_owned',clock_error<1e-12,clock_error)
                record['radial_variations'].append({'name':name,'time':time,'errors':errors,
                                                    'mass_response_max':float(abs(derived['mu']).max()),
                                                    'lapse_response_max':float(abs(derived['N']).max())})
                path = output_dir/(branch+'_'+name+'_radial_response.npz')
                np.savez_compressed(path,radii=radii,direction=direction,state=state,
                                    **{('derived_'+key):value for key,value in derived.items()},
                                    **{('complex_'+key):value for key,value in exact.items()})
                own(path,'outputs')
            solver = JointSchurResponse(system,old,full_exterior_columns=predicted['exterior_columns'])
            initial_probe = old['initial_directions'][:,0]
            homogeneous,homogeneous_log = solver.solve(np.tile(initial_probe,(len(solver.times),1)))
            one_way,one_way_log = solver.solve(np.tile(initial_probe,(len(solver.times),1)),coupled=False)
            homogeneous_outputs = np.stack([solver.response.outputs(system.evaluate(time,state+1j*1e-20*direction)).imag/1e-20
                                            for time,state,direction in zip(solver.times,solver.states,homogeneous)])
            homogeneous_error = float(abs(homogeneous-old['full_tangent_states'][:,:,0]).max())
            homogeneous_output_error = float(abs(homogeneous_outputs-old['full_output_tangent'][:,:,0]).max())
            feedback_state = float(abs(homogeneous-one_way).max())
            check(branch+'_closed_response_also_predicts_old_exterior_initial_probe',
                  max(homogeneous_error,homogeneous_output_error)<1e-8,
                  {'state_error':homogeneous_error,'output_error':homogeneous_output_error,'solver':homogeneous_log})
            record.update({'homogeneous_state_error':homogeneous_error,'homogeneous_output_error':homogeneous_output_error,
                           'homogeneous_feedback_state_difference':feedback_state,
                           'homogeneous_feedback_resolved':feedback_state>max(100*homogeneous_error,1e-10)})
            report['phase'] = 'independent_full_nonlinear_RK4'
            save()
            coarse = rk4(system,1.,64)
            fine = rk4(system,1.,128)
            fine_output = solver.response.outputs(system.evaluate_protocol(.004,fine,1.))
            state_error = float(abs(fine-joint['states'][-1]).max())
            refinement = float(abs(fine-coarse).max())
            output_error = float(abs(fine_output-joint['outputs'][-1]).max())
            check(branch+'_joint_nonlinear_prediction_matches_independent_RK4',max(state_error,refinement,output_error)<1e-9,
                  {'state_error':state_error,'refinement':refinement,'output_error':output_error})
            check(branch+'_independent_RK4_source_energy_positive',system.unpack(fine)[0][:,-1].min()>0)
            record.update({'RK4_state_error':state_error,'RK4_refinement':refinement,'RK4_output_error':output_error})
            for parameter in [-1.,-.5,.5,1.]:
                output = solver.response.outputs(system.evaluate_protocol(0.,system.initial_state,parameter))
                baseline_output = solver.response.outputs(system.evaluate(0.,system.initial_state))
                check(branch+'_'+str(parameter)+'_no_changed_initial_source_energy_or_geometry',float(abs(output-baseline_output).max())<1e-12)
            path = output_dir/(branch+'_independent_time_controls.npz')
            np.savez_compressed(path,rk4_coarse=coarse,rk4_fine=fine,homogeneous=homogeneous,homogeneous_outputs=homogeneous_outputs,
                                one_way_homogeneous=one_way,times=solver.times)
            own(path,'outputs')
            report['cases'].append(record)
            save()
            print(json.dumps(record),flush=True)
        note = root/'DERIVATION-20260914-joint-boundary-geometry-closure.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_source_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T23:06:13+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update({'state':'complete','conditional_joint_boundary_geometry_complete':True,'protected_changed_count':len(changed)})
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'main_checks':report['main_checks'],
                          'protected_changed_count':len(changed)}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()

