import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from annular_common_source_history_20260913 import ExteriorModePreparation, FixedInnerClockJet, CommonHistorySearch, exterior_modes

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-common-source-history-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'searches': [], 'cases': [], 'gauge_controls': [],
              'valid_for_physics_claim': False, 'full_GR_limit_proven': False, 'full_geometric_evolution': False,
              'complete_boundary_histories_matched': False, 'full_physical_radial_port_action_signed': False,
              'unique_parent_regularizer_derived': False, 'unique_exterior_profile_derived': False,
              'apparatus_microphysics_derived': False, 'point_force_adopted': False,
              'same_microscopic_exterior_initial_state_claimed': False,
              'common_inner_coordinate_mass_acceleration': 0., 'common_inner_log_lapse_rate': 0.,
              'target_is_declared_trial_history_not_archival_measurement': True,
              'exterior_amplitudes_are_prepared_initial_data_not_fundamental_couplings': True,
              'scalar_field_bulk_source_and_Gram_factor_coefficients_not_fitted': True,
              'no_C2_residual_used_in_matching': True, 'full_C2_evaluated': False}

    def save():
        (destination/'status.json').write_text(json.dumps(report, indent=2)+'\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        previous_path = intake/'annular-source-second-jet-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_second_jet_seal_complete', previous['state']=='complete' and previous['C2_all_pass'])
        for table in ['inputs', 'outputs']:
            for filename, expected in previous[table].items():
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting inherited evidence: '+filename)
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed evidence: '+filename)
                    report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__), root/'scripts/annular_common_source_history_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            executed=destination/('executed-'+path.name)
            executed.write_bytes(path.read_bytes())
            own(executed, 'outputs')
        coordinate=sp.symbols('z', real=True)
        bump=256**2*coordinate**4*(coordinate+sp.Rational(1,2))**4
        for index, mode in enumerate([bump,bump*(4*coordinate+1)]):
            check('exterior_mode_'+str(index)+'_zero_traces_through_order_three', all(sp.diff(mode,coordinate,order).subs(coordinate,endpoint)==0 for order in range(4) for endpoint in [0,-sp.Rational(1,2)]))
        mass1, mass2, rate, lapse, shift=sp.symbols('m1 m2 L N zeta', real=True)
        invariant=(mass2-rate*mass1)/lapse**2
        check('proper_mass_acceleration_gauge_invariant', sp.simplify((mass2+shift*mass1-(rate+shift)*mass1)/lapse**2-invariant)==0)
        strength, variance, mass_factor=sp.symbols('s variance prefactor', positive=True)
        check('flat_link_zero_mean_velocity_variance_lowers_mass_acceleration', sp.diff(-mass_factor*strength**2*variance,strength,2)==-2*mass_factor*variance)
        prior=json.loads((intake/'annular-clock-reservoir-coupling-attempt01/status.json').read_text())
        selected=[row for row in prior['cases'] if row['reservoir_energy']==.001]
        selected.sort(key=lambda row:(row['case'],row['branch']))
        for row in selected:
            branch, case, label=row['branch'],row['case'],row['label']
            source_path=root/'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03'/(branch+'_source_snapshot.npz')
            prepared_path=intake/'annular-finite-width-boundary-cut-attempt01'/(branch+'_'+str(case)+'_prepared_collar.npz')
            history_path=root/'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'/('canonical_N16_'+branch+'_sample0.npz')
            with np.load(source_path,allow_pickle=False) as archive:
                source={key:archive[key].copy() for key in archive.files}
            with np.load(prepared_path,allow_pickle=False) as archive:
                prepared={key:archive[key].copy() for key in archive.files}
            with np.load(history_path,allow_pickle=False) as archive:
                clock=archive['affine_clock'].copy()
                outer_acceleration=float(archive['endpoint_acceleration'][-1])
            preparation=ExteriorModePreparation(source,branch!='GR',prepared['kinetic_seed'],float(prepared['outer_clock']),prepared['drive'],row['width'],row['shape'],reservoir_energy=row['reservoir_energy'],base_coefficients=row['coefficients'])
            search=CommonHistorySearch(preparation,float(clock[1]),outer_acceleration)
            search_row={'label':label,'trials':search.records,'state':'running'}
            report['searches'].append(search_row)
            search.on_record=save
            base_model,base_driver=search.model_and_driver([0.,0.])
            base_jet=FixedInnerClockJet(base_model,base_driver,degree=56,primitive_degree=36)
            reference_radii=np.unique(np.concatenate([base_model.radii,np.linspace(base_model.radii[0],base_model.radii[-1],31)]))
            base_metric=base_model.metric(reference_radii)
            baseline_fields=base_jet.first_fields(reference_radii)
            baseline_second=base_jet.current_second(reference_radii)
            if case==0:
                shifted=FixedInnerClockJet(base_model,base_driver,gauge_shift=.3,degree=56,primitive_degree=36)
                shifted_fields=shifted.first_fields(reference_radii)
                shifted_second=shifted.current_second(reference_radii)
                fraction=(reference_radii-base_model.radii[0])/(base_model.radii[-1]-base_model.radii[0])
                zeta=.3*(1-3*fraction**2+2*fraction**3)
                gauge_error=float(max(abs(shifted_second['mu2']-baseline_second['mu2']-zeta*baseline_fields['mu1']).max(),abs(shifted_second['K1']-baseline_second['K1']-2*zeta*baseline_fields['K']).max()))
                proper_base=(baseline_second['mu2']-baseline_fields['L']*baseline_fields['mu1'])/baseline_fields['N']**2
                proper_shifted=(shifted_second['mu2']-shifted_fields['L']*shifted_fields['mu1'])/shifted_fields['N']**2
                check(branch+'_actual_clock_change_cannot_change_proper_acceleration',max(gauge_error,float(abs(proper_base-proper_shifted).max()))<1e-9,gauge_error)
                report['gauge_controls'].append({'branch':branch,'gauge_error':gauge_error,'proper_acceleration_error':float(abs(proper_base-proper_shifted).max()),'gauge_shift':.3,'adopted':False})
            amplitudes,root_status=search.solve(sign=1.)
            search_row.update({'state':root_status['status'],'root':root_status,'flux_evaluations':len(search.cached_flux)})
            save()
            if amplitudes is None:
                report['cases'].append({'label':label,'matched':False,'reason':root_status})
                continue
            model,driver=search.model_and_driver(amplitudes)
            jet=FixedInnerClockJet(model,driver,degree=56,primitive_degree=36)
            first_checks=driver.checks(40)
            second_checks=[jet.check_second(order) for order in [24,40]]
            high=second_checks[-1]
            endpoint_fields=jet.first_fields(model.radii[[0,-1]])
            endpoint_second=jet.current_second(model.radii[[0,-1]])
            center=jet.completed_layer([0.])
            metric=model.metric(reference_radii)
            interior_change=float(max(abs(metric[key]-base_metric[key]).max() for key in ['mu','N','U','epsilon','P1']))
            boundary_error=float(max(abs(endpoint_fields['mu'][0]-source['mu'][0]),abs(endpoint_fields['mu1'][0]-prepared['drive'][0]),abs(endpoint_second['mu2'][0]),abs(endpoint_fields['L'][0]),abs(endpoint_fields['P1']).max(),abs(endpoint_fields['P2']).max(),abs(endpoint_fields['N'][-1]/endpoint_fields['U'][-1]-clock[0]),abs(center['q'][0,-1]-prepared['drive'][2]),abs(center['q1'][0,-1]-outer_acceleration)))
            max_c0=float(abs(first_checks['C0']).max())
            max_c1=float(abs(first_checks['C1']).max())
            max_c2=float(max(abs(output['C2']).max() for output in second_checks))
            check(label+'_matching_changes_exterior_not_initial_interior_fields',interior_change<1e-10,interior_change)
            check(label+'_common_mass_history_and_clock_jet_matched',boundary_error<1e-10,boundary_error)
            check(label+'_all_constraint_orders_are_separate_holdout_checks',max(max_c0,max_c1,max_c2)<1e-10,{'C0':max_c0,'C1':max_c1,'C2':max_c2})
            sample_offsets=np.linspace(-.5,.5,201)
            before=base_model.initial_scalar(sample_offsets)
            after=model.initial_scalar(sample_offsets)
            delta_p=after['p']-before['p']
            check(label+'_changed_momenta_only_in_left_exterior_half_band',abs(delta_p[:,1:]).max()==0 and abs(delta_p[sample_offsets>=0,0]).max()==0)
            maximum_momentum_change=float(abs(delta_p).max())
            points,weights=np.polynomial.legendre.leggauss(48)
            offsets=-.25+.25*points
            from annular_finite_width_bulk_current_20260913 import shape_weight
            bare_energy_change=float(.25*weights@(shape_weight(offsets,model.shape)*(model.initial_scalar(offsets)['energy'][:,0]-base_model.initial_scalar(offsets)['energy'][:,0])))
            result={'label':label,'branch':branch,'case':case,'width':row['width'],'shape':row['shape'],'reservoir_energy':row['reservoir_energy'],
                    'matched':True,'exterior_amplitudes':amplitudes.tolist(),'initial_interior_field_change':interior_change,'boundary_error':boundary_error,
                    'maximum_C0':max_c0,'maximum_C1':max_c1,'maximum_C2':max_c2,'C2_quadrature_difference':float(abs(second_checks[0]['C2']-high['C2']).max()),
                    'inner_mass_value':float(endpoint_fields['mu'][0]),'inner_mass_rate':float(endpoint_fields['mu1'][0]),'inner_mass_acceleration':float(endpoint_second['mu2'][0]),
                    'inner_proper_mass_acceleration':float((endpoint_second['mu2'][0]-endpoint_fields['L'][0]*endpoint_fields['mu1'][0])/endpoint_fields['N'][0]**2),
                    'inner_log_lapse_rate':float(endpoint_fields['L'][0]),'outer_mass_acceleration':float(endpoint_second['mu2'][1]),
                    'maximum_exterior_momentum_change':maximum_momentum_change,'exterior_bare_scalar_energy_change':bare_energy_change,
                    'minimum_F':float((high['U']**2).min()),'source_energy_second_at_outer_cut':float(center['reservoir_E2'][0]),
                    'same_macroscopic_two_jet_not_same_exterior_state':True}
            report['cases'].append(result)
            path=destination/(label+'_matched_common_history.npz')
            np.savez_compressed(path,**high,exterior_amplitudes=amplitudes,first_C0=first_checks['C0'],first_C1=first_checks['C1'],lower_C2=second_checks[0]['C2'],sample_offsets=sample_offsets,initial_delta_p=delta_p,reference_radii=reference_radii,**{'center_'+key:value for key,value in center.items() if isinstance(value,np.ndarray)})
            own(path,'outputs')
            report['full_C2_evaluated']=True
            print(json.dumps(result),flush=True)
            save()
        check('all_six_declared_cases_attempted',len(report['cases'])==6)
        for module in tuple(sys.modules.values()):
            filename=getattr(module,'__file__',None)
            if filename:
                path=Path(filename).resolve()
                if path.parent==root/'scripts' and path.suffix=='.py':
                    own(path)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        report['common_two_jet_all_matched']=all(row['matched'] for row in report['cases'])
        report['state']='complete'
        save()
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()
