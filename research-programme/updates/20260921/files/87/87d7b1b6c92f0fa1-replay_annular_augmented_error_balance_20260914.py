import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution
    from annular_covariant_scalar_action_20260912 import full_spatial_factors
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_finite_width_bulk_current_20260913 import shape_weight

    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    main_dir=intake/'annular-compatible-h-evolution-main-attempt01'
    output=intake/'annular-augmented-error-balance-attempt01'
    output.mkdir(exist_ok=False)
    report={'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
            'uniform_relative_energy_estimate_proven':False,'full_GR_limit_proven':False,'valid_for_physics_claim':False}

    def save():
        (output/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        main=json.loads((main_dir/'status.json').read_text())
        check('main_complete',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in main[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed evidence: '+filename)
                report['inputs'][filename]=expected
        own(main_dir/'status.json')
        own(Path(__file__))
        compile(Path(__file__).read_bytes(),str(Path(__file__)),'exec')
        snapshot=output/('executed-'+Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        check('all_inherited_hashes_match_and_script_compiles',True)
        points,weights=np.polynomial.legendre.leggauss(24)
        offsets=np.concatenate([-.25+.25*points,.25+.25*points])
        weights=np.concatenate([.25*weights,.25*weights])*shape_weight(offsets,'beta22')
        for count in [33,65,129]:
            systems=[CompatibleEvolution(count,gram) for gram in [False,True]]
            saved=[]
            for label in ['GR_control','metric_Gram']:
                with np.load(main_dir/(label+'_count'+str(count)+'.npz'),allow_pickle=False) as archive:
                    saved.append({'states':archive['states'].copy(),'times':archive['times'].copy()})
            base_factors,base_sampling=full_spatial_factors(count,False)
            extra_factors,extra_sampling=gram_matrices(count)
            spacing=systems[0].spacing
            omega=systems[0].node_weights

            def ingredients(first,second):
                radius=second['R']
                scalar_error=second['chi']-first['chi']
                momentum_error=second['p']-first['p']
                coefficient=second['N']*second['U']/radius**2
                base_weight=second['C'] @ base_sampling.T
                extra_weight=second['C'] @ extra_sampling.T
                scalar_amplitude=scalar_error @ base_factors.T
                extra_amplitude=second['chi'] @ extra_factors.T
                norm=.5*weights @ (np.sum(omega*coefficient*momentum_error**2,axis=1)
                                   +np.sum(base_weight*scalar_amplitude**2,axis=1)/spacing
                                   +np.sum(extra_weight*extra_amplitude**2,axis=1)/spacing)
                return norm,scalar_error,momentum_error,coefficient,base_weight,extra_weight,scalar_amplitude,extra_amplitude

            for index in [0,8,16]:
                time=saved[0]['times'][index]
                states=[row['states'][index] for row in saved]
                directions=[system.rhs(time,state) for system,state in zip(systems,states)]
                data=[system.geometry(time,state).layer(offsets) for system,state in zip(systems,states)]
                step=1e-20
                complex_data=[system.geometry(time+1j*step,state+1j*step*direction).layer(offsets)
                              for system,state,direction in zip(systems,states,directions)]
                norm,scalar_error,momentum_error,coefficient,base_weight,extra_weight,scalar_amplitude,extra_amplitude=ingredients(*data)
                norm_derivative=float(ingredients(*complex_data)[0].imag/step)
                reference_coefficient=data[0]['N']*data[0]['U']/data[0]['R']**2
                delta_velocity=(coefficient-reference_coefficient)*data[0]['p']
                delta_base_weight=base_weight-data[0]['C'] @ base_sampling.T
                reference_amplitude=data[0]['chi'] @ base_factors.T
                delta_base_force=(delta_base_weight*reference_amplitude) @ base_factors/spacing
                coefficient_rate=(complex_data[1]['N']*complex_data[1]['U']/complex_data[1]['R']**2).imag/step
                base_rate=(complex_data[1]['C'] @ base_sampling.T).imag/step
                extra_rate=(complex_data[1]['C'] @ extra_sampling.T).imag/step
                local_terms=np.array([
                    np.sum(extra_weight*extra_amplitude*(data[0]['q'] @ extra_factors.T),axis=1)/spacing,
                    np.sum(extra_weight*extra_amplitude*(delta_velocity @ extra_factors.T),axis=1)/spacing,
                    -np.sum(momentum_error*coefficient*delta_base_force,axis=1),
                    np.sum(base_weight*scalar_amplitude*(delta_velocity @ base_factors.T),axis=1)/spacing,
                    .5*np.sum(omega*coefficient_rate*momentum_error**2,axis=1),
                    .5*np.sum(base_rate*scalar_amplitude**2,axis=1)/spacing,
                    .5*np.sum(extra_rate*extra_amplitude**2,axis=1)/spacing])
                terms=local_terms @ weights
                rate_error=abs(terms.sum()-norm_derivative)
                reference_extra=.5*weights @ np.sum(extra_weight*(data[0]['q'] @ extra_factors.T)**2,axis=1)/spacing
                cauchy=2*np.sqrt(max(0.,norm)*max(0.,reference_extra))
                label='count'+str(count)+'_sample'+str(index)
                check(label+'_positive_augmented_energy',norm>=0,float(norm))
                check(label+'_exact_live_metric_error_balance',rate_error<max(1e-11,1e-9*abs(norm_derivative)),
                      {'direct_rate':norm_derivative,'sum_of_terms':float(terms.sum()),'error':float(rate_error)})
                check(label+'_reference_Gram_Cauchy_bound',abs(terms[0])<=cauchy+1e-11)
                report['cases'].append({'count':count,'time':float(time),'augmented_energy':float(norm),
                                        'direct_rate':norm_derivative,'terms':terms.tolist(),'rate_error':float(rate_error),
                                        'reference_term_bound':float(cauchy),'omitted_live_terms':float(terms[1:].sum())})
                save()
                print(json.dumps(report['cases'][-1]),flush=True)
        check('live_terms_are_resolved_not_silently_frozen',max(abs(row['omitted_live_terms']) for row in report['cases'])>1e-10)
        report['term_names']=['reference_Gram_pairing','extra_metric_difference','base_metric_force_difference',
                              'base_velocity_metric_difference','kinetic_coefficient_rate','base_stiffness_rate','Gram_stiffness_rate']
        report['state']='complete'
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'cases':len(report['cases'])}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()
