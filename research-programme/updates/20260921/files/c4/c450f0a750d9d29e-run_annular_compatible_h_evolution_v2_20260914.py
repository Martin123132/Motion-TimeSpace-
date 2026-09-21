import argparse
import hashlib
import json
import time as wallclock
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution,gram_energy_triplet,regular_chart_constants,trajectory_arrays,integrated_energy_rate
    from annular_gram_geometry_bound_20260914 import propagation_bounds
    from annular_horizontal_clock_evolution_20260913 import HorizontalEvolution

    parser = argparse.ArgumentParser()
    parser.add_argument('--tag',required=True)
    parser.add_argument('--counts',nargs='+',type=int,default=[33,65,129])
    parser.add_argument('--degree',type=int,default=8)
    parser.add_argument('--duration',type=float,default=.06)
    arguments = parser.parse_args()
    if not arguments.tag.replace('-','').isalnum() or arguments.duration<=0:
        raise ValueError('Invalid run tag or duration.')
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    output = intake/('annular-compatible-h-evolution-'+arguments.tag)
    output.mkdir(exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],'comparisons':[],
              'configuration':vars(arguments),'same_initial_scalar_and_free_momenta':True,
              'source_protocol':'D(theta)=0, v=0, a=0; E=.003; reaction retained, zero source work',
              'full_GR_limit_proven':False,'uniform_H3_solution_bound_proven':False,
              'uniform_in_h_dynamical_energy_estimate_proven':False,'valid_for_physics_claim':False,
              'physical_spacing_varied':len(arguments.counts)>1,'stationary_source_only':True,
              'geometric_units':'pilot units, not SI','regular_chart_constants':regular_chart_constants()}

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
        predecessor_path=intake/'annular-gram-geometry-bound-final-integrity.json'
        predecessor=json.loads(predecessor_path.read_text())
        check('predecessor_sealed',predecessor['state']=='complete' and all(row['passed'] for row in predecessor['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in predecessor[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed predecessor evidence: '+filename)
                report['inputs'][filename]=expected
        own(predecessor_path)
        check('all_inherited_hashes_match',True)
        for path in [Path(__file__),root/'scripts/annular_compatible_h_evolution_20260914.py']:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            copy=output/('executed-'+path.name)
            copy.write_bytes(path.read_bytes())
            own(copy,'outputs')
        check('conditional_uniform_regular_chart_barrier',report['regular_chart_constants']['F_lower_if_exact_mass_conserved']>.5)
        for count in arguments.counts:
            pair_data=[]
            for gram in [False,True]:
                label=('metric_Gram' if gram else 'GR_control')+'_count'+str(count)
                report['active_case']=label
                save()
                started=wallclock.monotonic()
                system=CompatibleEvolution(count,gram,arguments.degree)
                initial=system.evaluate(0.,system.initial_state)
                initial_data=initial['data']
                boundary_error=max(float(abs(initial_data[key][:,[0,-1]]).max()) for key in ['chi','p','q','Gchi'])
                check(label+'_initial_boundary_fields_rates_and_forces_zero',boundary_error<1e-13,boundary_error)
                check(label+'_optimized_rhs_equals_full_source_equations_initially',
                      abs(system.rhs(0.,system.initial_state)-initial['rhs']).max()<1e-13)
                solution=system.integrate(arguments.duration)
                arrays=trajectory_arrays(system,solution,arguments.duration)
                check(label+'_finite_arrays',all(np.isfinite(value).all() for value in arrays.values()))
                check(label+'_positive_geometry_and_reservoir',arrays['minimums_and_defect'][:,:3].min()>0 and arrays['minimums_and_defect'][:,0].min()>.5)
                check(label+'_constraint_and_full_mass_conservation',arrays['minimums_and_defect'][:,3].max()<1e-10
                      and np.max(abs(arrays['total_mass']-arrays['total_mass'][0]))<1e-9,
                      {'mass_drift':float(np.max(abs(arrays['total_mass']-arrays['total_mass'][0]))),
                       'constraint_defect':float(arrays['minimums_and_defect'][:,3].max())})
                last=system.evaluate(arguments.duration,solution.y[:,-1])
                check(label+'_optimized_rhs_equals_full_source_equations_finally',
                      abs(system.rhs(arguments.duration,solution.y[:,-1])-last['rhs']).max()<1e-13)
                check(label+'_stationary_source_energy_is_not_omitted_or_changed',
                      abs(system.unpack(solution.y[:,-1])[0][:,-1]-.003).max()<1e-14
                      and abs(last['energy_rate']).max()==0 and abs(last['source_p_rate']).max()==0)
                energies=arrays['energies']
                cauchy=np.maximum(0.,abs(energies[:,2])-2*np.sqrt(energies[:,0]*energies[:,1]))
                check(label+'_exact_energy_rate_Cauchy_bound',cauchy.max()<1e-12,float(cauchy.max()))
                coarse=integrated_energy_rate(system,solution,arguments.duration,16)
                fine=integrated_energy_rate(system,solution,arguments.duration,32)
                error=abs(energies[-1,0]-energies[0,0]-fine[0])
                propagation=(np.sqrt(energies[0,0])+fine[1])**2
                check(label+'_integrated_energy_rate_and_quadrature',max(error,float(abs(coarse-fine).max()))<1e-9,
                      {'balance_error':float(error),'quadrature_change':float(abs(coarse-fine).max())})
                check(label+'_finite_time_square_root_energy_bound',energies[-1,0]<=propagation+1e-11,
                      {'final_energy':float(energies[-1,0]),'bound':float(propagation)})
                changing=float(abs(arrays['profiles'][-1]-arrays['profiles'][0]).max())
                check(label+'_nontrivial_bulk_evolution',changing>1e-5,changing)
                archive=output/(label+'.npz')
                np.savez_compressed(archive,**arrays)
                own(archive,'outputs')
                record={'label':label,'count':count,'gram':gram,'spacing':system.spacing,'width':system.width,
                        'degree':arguments.degree,'state_size':len(system.initial_state),'duration':arguments.duration,
                        'rhs_calls':system.calls,'wall_seconds':wallclock.monotonic()-started,
                        'initial_extra_energy':float(energies[0,0]),'final_extra_energy':float(energies[-1,0]),
                        'maximum_extra_energy':float(energies[:,0].max()),
                        'maximum_extra_energy_over_h4':float(energies[:,0].max()/system.spacing**4),
                        'maximum_velocity_Gram_energy_over_h4':float(energies[:,1].max()/system.spacing**4),
                        'propagation_bound':float(propagation),'energy_rate_integral_error':float(error),
                        'max_scalar_and_momentum_change':changing,
                        'full_mass_drift':float(np.max(abs(arrays['total_mass']-arrays['total_mass'][0]))),
                        'minimum_F':float(arrays['minimums_and_defect'][:,0].min())}
                report['cases'].append(record)
                pair_data.append((system,solution,arrays))
                save()
                print(json.dumps(record),flush=True)
            base,base_solution,base_arrays=pair_data[0]
            mts,mts_solution,mts_arrays=pair_data[1]
            check('count'+str(count)+'_identical_initial_full_state',np.array_equal(base.initial_state,mts.initial_state))
            shadow_fields=[]
            for time,state in zip(mts_arrays['times'],mts_arrays['states']):
                metric=base.geometry(time,state).metric(mts_arrays['radii'])
                shadow_fields.append(np.stack([metric['mu'],metric['log_N']]))
            shadow_fields=np.array(shadow_fields)
            direct=mts_arrays['fields']-shadow_fields
            feedback=shadow_fields-base_arrays['fields']
            total=mts_arrays['fields']-base_arrays['fields']
            check('count'+str(count)+'_exact_direct_plus_data_response_split',abs(total-direct-feedback).max()<1e-13)
            bounds=[propagation_bounds(extra,0.) for extra in mts_arrays['energies'][:,0]]
            check('count'+str(count)+'_matched_shadow_geometry_obeys_derived_bound',
                  direct[:,0].min()>-1e-12 and direct[:,1].max()<1e-12
                  and all(direct[index,0].max()<=bound['mass_difference_bound']+1e-11
                          and -direct[index,1].min()<=bound['log_lapse_difference_bound']+1e-11
                          for index,bound in enumerate(bounds)))
            comparison={'count':count,'spacing':base.spacing,
                        'final_state_difference':float(abs(mts_arrays['profiles'][-1]-base_arrays['profiles'][-1]).max()),
                        'maximum_total_mass_difference':float(abs(total[:,0]).max()),
                        'maximum_total_log_lapse_difference':float(abs(total[:,1]).max()),
                        'maximum_direct_mass_difference':float(abs(direct[:,0]).max()),
                        'maximum_feedback_mass_difference':float(abs(feedback[:,0]).max()),
                        'final_total_mass_difference':float(abs(total[-1,0]).max()),
                        'final_total_log_lapse_difference':float(abs(total[-1,1]).max())}
            archive=output/('comparison_count'+str(count)+'.npz')
            np.savez_compressed(archive,times=mts_arrays['times'],radii=mts_arrays['radii'],direct=direct,feedback=feedback,total=total,
                                shadow_fields=shadow_fields)
            own(archive,'outputs')
            report['comparisons'].append(comparison)
            save()
            print(json.dumps(comparison),flush=True)
        report['orders']={}
        if len(arguments.counts)>1:
            for gram in [False,True]:
                rows=[row for row in report['cases'] if row['gram']==gram]
                report['orders']['extra_energy_'+str(gram)]=[float(np.log(first['maximum_extra_energy']/second['maximum_extra_energy'])/
                          np.log(first['spacing']/second['spacing'])) for first,second in zip(rows[:-1],rows[1:])]
            for key in ['final_state_difference','final_total_mass_difference','final_total_log_lapse_difference']:
                report['orders'][key]=[float(np.log(first[key]/second[key])/np.log(first['spacing']/second['spacing']))
                                      for first,second in zip(report['comparisons'][:-1],report['comparisons'][1:])]
        report['state']='complete'
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'orders':report['orders']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()
