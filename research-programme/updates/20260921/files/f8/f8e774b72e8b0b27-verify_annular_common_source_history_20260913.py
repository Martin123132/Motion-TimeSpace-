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
    import sympy as sp
    from annular_common_source_history_20260913 import ExteriorModePreparation, FixedInnerClockJet, exterior_modes
    from annular_clock_reservoir_coupling_20260913 import ProperClockDrive
    from annular_finite_width_bulk_current_20260913 import shape_weight

    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260913'
    destination=intake/'annular-common-source-history-final-integrity.json'
    snapshot=intake/'annular-common-source-history-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Existing evidence must not be overwritten.')
    report={'state':'running','checks':[],'inputs':{},'outputs':{},'independent_cases':[],'response_rank_controls':[],
            'valid_for_physics_claim':False,'full_GR_limit_proven':False,'full_geometric_evolution':False,
            'complete_boundary_histories_matched':False,'full_physical_radial_port_action_signed':False,
            'unique_parent_regularizer_derived':False,'unique_exterior_profile_derived':False,
            'apparatus_microphysics_derived':False,'point_force_adopted':False,
            'same_microscopic_exterior_initial_state_claimed':False,
            'full_C2_evaluated':True,'common_two_jet_is_declared_boundary_preparation_not_prediction':True,
            'protected_scan_scope':'mtime since 2026-09-13T18:43:05Z; not pre-turn content hashes'}

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n')

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    save()
    try:
        amplitude, left_speed, right_speed, left_acceleration, right_acceleration, coefficient, spacing = sp.symbols('A q_left q_right a_left a_right C h', real=True)
        factor_current = amplitude*(coefficient*(right_speed-left_speed)/2-right_speed*coefficient)/spacing
        current_expected = -coefficient*amplitude*(right_speed+left_speed)/(2*spacing)
        check('flat_link_current_derived_from_factor_weights',sp.simplify(factor_current-current_expected)==0)
        current_rate = sp.diff(factor_current,amplitude)*(right_speed-left_speed)+sp.diff(factor_current,left_speed)*left_acceleration+sp.diff(factor_current,right_speed)*right_acceleration
        current_rate_expected = -coefficient*(right_speed**2-left_speed**2+amplitude*(right_acceleration+left_acceleration))/(2*spacing)
        check('flat_link_current_rate_includes_velocity_square_difference',sp.simplify(current_rate-current_rate_expected)==0)
        perturbation = sp.symbols('delta_q',real=True)
        difference = sp.expand(current_rate.subs(left_speed,left_speed+perturbation)-current_rate)
        check('flat_link_variance_formula_retains_linear_cross_term',sp.simplify(difference-coefficient*(2*left_speed*perturbation+perturbation**2)/(2*spacing))==0)
        lapse, coupling, root_f, first_momentum, connection, rate, mass_term, shift, shift_r = sp.symbols('N kappa U P1 c2 L v zeta zeta_R',real=True)
        second_momentum = lapse*connection/(coupling*root_f)+2*(rate+mass_term)*first_momentum
        changed_momentum = second_momentum.subs({connection:connection-shift_r-shift*coupling*root_f*first_momentum/lapse,rate:rate+shift},simultaneous=True)
        check('second_momentum_clock_transformation_derived',sp.simplify(changed_momentum-second_momentum-shift*first_momentum+lapse*shift_r/(coupling*root_f))==0)
        directory=intake/'annular-common-source-history-attempt01'
        batch=json.loads((directory/'status.json').read_text())
        check('six_completed_matched_boundary_preparations',batch['state']=='complete' and len(batch['cases'])==6 and batch['common_two_jet_all_matched'] and all(row['passed'] for row in batch['checks']))
        for key,value in report.items():
            if value is False:
                check(key+'_remains_false',batch[key] is False)
        for table in ['inputs','outputs']:
            for filename,expected in batch[table].items():
                if filename in report['inputs'] and report['inputs'][filename]!=expected:
                    raise RuntimeError('Conflicting evidence: '+filename)
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed evidence: '+filename)
                    report['inputs'][filename]=expected
        check('inherited_hashes_match',True,len(report['inputs']))
        for path in directory.iterdir():
            if path.is_file():
                own(path,'outputs')
                if path.name.startswith('executed-'):
                    check(path.name+'_matches_executed_source',path.read_bytes()==(root/'scripts'/path.name.removeprefix('executed-')).read_bytes())
                if path.suffix=='.npz':
                    with np.load(path,allow_pickle=False) as archive:
                        check(path.name+'_finite_arrays',all(np.isfinite(archive[key]).all() for key in archive.files))
        for field in ['inner_mass_value','inner_mass_rate','inner_mass_acceleration','inner_log_lapse_rate']:
            values=[row[field] for row in batch['cases']]
            check(field+'_common_across_all_cases',max(values)-min(values)<1e-10,values)
        check('proper_inner_accelerations_are_zero_not_just_gauge_matched',max(abs(row['inner_proper_mass_acceleration']) for row in batch['cases'])<1e-10)
        check('initial_exterior_data_not_claimed_identical',len({tuple(row['exterior_amplitudes']) for row in batch['cases']})>1)
        prior=json.loads((intake/'annular-clock-reservoir-coupling-attempt01/status.json').read_text())
        old_rows={row['label']:row for row in prior['cases']}
        for row in batch['cases']:
            branch,case,label=row['branch'],row['case'],row['label']
            old=old_rows[label]
            with np.load(root/'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03'/(branch+'_source_snapshot.npz'),allow_pickle=False) as archive:
                source={key:archive[key].copy() for key in archive.files}
            with np.load(intake/'annular-finite-width-boundary-cut-attempt01'/(branch+'_'+str(case)+'_prepared_collar.npz'),allow_pickle=False) as archive:
                prepared={key:archive[key].copy() for key in archive.files}
            history_path=root/'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'/('canonical_N16_'+branch+'_sample0.npz')
            with np.load(history_path,allow_pickle=False) as archive:
                clock=archive['affine_clock'].copy()
                acceleration=float(archive['endpoint_acceleration'][-1])
            preparation=ExteriorModePreparation(source,branch!='GR',prepared['kinetic_seed'],float(prepared['outer_clock']),prepared['drive'],row['width'],row['shape'],reservoir_energy=row['reservoir_energy'],base_coefficients=old['coefficients'])
            amplitudes=np.asarray(row['exterior_amplitudes'])

            def build(values,degree=64,primitive_degree=44):
                model=preparation.build(values)
                driver=ProperClockDrive(model,float(clock[1]),acceleration,degree=degree)
                jet=FixedInnerClockJet(model,driver,degree=degree,primitive_degree=primitive_degree)
                return model,driver,jet

            model,driver,jet=build(amplitudes)
            endpoints=jet.first_fields(model.radii[[0,-1]])
            second=jet.current_second(model.radii[[0,-1]])
            proper=(second['mu2']-endpoints['L']*endpoints['mu1'])/endpoints['N']**2
            direct_current=model.direct_flux(model.radii[0],order=48)
            direct_mass_rate=-model.coupling*endpoints['U'][0]*direct_current/endpoints['N'][0]
            check(label+'_direct_crossing_integral_preserves_mass_rate',abs(direct_mass_rate-prepared['drive'][0])<1e-10,float(direct_mass_rate-prepared['drive'][0]))
            refined_error=float(max(abs(endpoints['mu1'][0]-prepared['drive'][0]),abs(second['mu2'][0]),abs(proper[0]),abs(endpoints['P2']).max()))
            check(label+'_refined_maps_preserve_unretuned_boundary_match',refined_error<1e-10,refined_error)
            points,weights=np.polynomial.legendre.leggauss(48)
            offsets=-.25+.25*points
            original=preparation.build([0.,0.])
            before,after=original.initial_scalar(offsets),model.initial_scalar(offsets)
            momentum_difference=exterior_modes(offsets)@amplitudes
            kinetic_increment=model.node_weights[0]*(2*before['p'][:,0]*momentum_difference+momentum_difference**2)/(2*after['R'][:,0]**2)
            independent_energy=.25*weights@(shape_weight(offsets,model.shape)*kinetic_increment)
            check(label+'_exterior_energy_cost_independently_recomputed',abs(independent_energy-row['exterior_bare_scalar_energy_change'])<1e-12 and independent_energy>0)
            source_jet=jet.transport_jet(np.linspace(-.49,.49,17))
            source_clock_error=source_jet['q1'][:,-1]-source_jet['metric1']['L'][:,-1]*source_jet['q'][:,-1]-source_jet['metric1']['N'][:,-1]**2*driver.proper_acceleration
            check(label+'_whole_source_layer_obeys_prescribed_proper_acceleration',abs(source_clock_error).max()<1e-10,float(abs(source_clock_error).max()))
            sample_radii=np.unique(np.concatenate([model.edges,model.radii,np.linspace(model.edges[0],model.edges[-1],300)]))
            chart=model.metric(sample_radii)
            check(label+'_whole_support_positive_geometry_and_energy',chart['U'].min()>0 and chart['N'].min()>0 and model.energy_density(sample_radii).min()>=-1e-13)
            lower_seed=model.metric(np.array([model.edges[0]]))['mu'][0]
            baseline_seed=original.metric(np.array([original.edges[0]]))['mu'][0]
            check(label+'_left_mass_seed_rebalance_is_recorded_and_positive',0<lower_seed<baseline_seed)
            outer_radius=model.radii[-1]
            root_first=-endpoints['mu1'][-1]/(outer_radius*endpoints['U'][-1])
            root_second=-second['mu2'][-1]/(outer_radius*endpoints['U'][-1])-endpoints['mu1'][-1]**2/(outer_radius**2*endpoints['U'][-1]**3)
            lapse_first=endpoints['N'][-1]*endpoints['L'][-1]
            lapse_second=2*clock[1]*root_first+clock[0]*root_second
            clock_second=lapse_second/endpoints['U'][-1]-2*lapse_first*root_first/endpoints['U'][-1]**2-endpoints['N'][-1]*root_second/endpoints['U'][-1]**2+2*endpoints['N'][-1]*root_first**2/endpoints['U'][-1]**3
            check(label+'_inherited_affine_outer_clock_second_jet',abs(clock_second)<1e-12)
            high_c2=None
            if case==0:
                high=jet.check_second(48)
                high_c2=float(abs(high['C2']).max())
                check(branch+'_independent_higher_quadrature_C2',high_c2<1e-10,high_c2)
                step=.001
                columns=[]
                for direction in np.eye(2):
                    measurements=[]
                    for sign in [-1.,1.]:
                        trial_model,trial_driver,trial=build(amplitudes+sign*step*direction,degree=56,primitive_degree=36)
                        first=trial.first_fields(np.array([trial_model.radii[0]]))
                        trial_second=trial.current_second(np.array([trial_model.radii[0]]))
                        measurements.append(np.array([first['mu1'][0],trial_second['mu2'][0]]))
                    columns.append((measurements[1]-measurements[0])/(2*step))
                jacobian=np.column_stack(columns)
                scaled=jacobian/np.array([.001,.02])[:,None]
                singular=np.linalg.svd(scaled,compute_uv=False)
                check(branch+'_two_physical_boundary_responses_locally_resolved',singular[-1]>1e-5 and singular[0]/singular[-1]<1e5,singular.tolist())
                report['response_rank_controls'].append({'branch':branch,'jacobian':jacobian.tolist(),'scaled_singular_values':singular.tolist(),'condition_number':float(singular[0]/singular[-1]),'finite_difference_step':step,'not_interval_uniqueness_proof':True})
            report['independent_cases'].append({'label':label,'refined_boundary_error':refined_error,'refined_proper_inner_acceleration':float(proper[0]),
                                                'independent_exterior_energy_increment':float(independent_energy),'higher_C2':high_c2,
                                                'lower_support_mass_seed':float(lower_seed),'lower_support_mass_seed_change':float(lower_seed-baseline_seed),
                                                'derived_outer_N2_for_affine_Cclock':float(lapse_second),'outer_Cclock2_error':float(abs(clock_second))})
            save()
        affine_owner=root/'scripts/derive_annular_parent_root_residence_20260910.py'
        check('inherited_affine_clock_owner_exists',affine_owner.is_file())
        own(affine_owner)
        note=root/'DERIVATION-20260913-common-source-two-jet-and-exterior-preparation.md'
        for citation in re.findall(r'`([^`]+)`',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_path_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        for stem in ['annular_common_source_history','derive_annular_common_source_history','verify_annular_common_source_history']:
            path=root/'scripts'/(stem+'_20260913.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('three_new_scripts_compile_without_bytecode',True)
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-13T18:43:05+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update({'state':'complete','main_run_checks':len(batch['checks']),'matched_cases':len(batch['cases']),
                       'common_two_jet_all_matched':True,'protected_changed_count':len(changed),
                       'maximum_C2':max(row['maximum_C2'] for row in batch['cases']),
                       'maximum_boundary_error':max(row['boundary_error'] for row in batch['cases'])})
        save()
        print(json.dumps({key:report[key] for key in ['state','main_run_checks','matched_cases','maximum_C2','maximum_boundary_error','protected_changed_count']}|{'seal_checks':len(report['checks'])}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()
