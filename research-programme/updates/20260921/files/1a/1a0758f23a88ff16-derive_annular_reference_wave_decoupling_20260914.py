import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution
    from annular_reference_wave_decoupling_20260914 import (
        extended_constants,reference_acceleration,MassJet,higher_energy,flux_control)

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    output = intake/'annular-reference-wave-decoupling-attempt01'
    output.mkdir(exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
              'stationary_source_only':True,'conditional_short_time_relative_decoupling_derived':True,
              'continuum_GR_identified':False,'full_GR_limit_proven':False,'valid_for_physics_claim':False}

    def save():
        (output/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        predecessor = intake/'annular-constrained-mass-relative-energy-final-integrity.json'
        inherited = json.loads(predecessor.read_text())
        check('predecessor_sealed_complete',inherited['state']=='complete' and all(row['passed'] for row in inherited['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in inherited[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed inherited evidence: '+filename)
                report['inputs'][filename] = expected
        own(predecessor)
        for source in [Path(__file__),root/'scripts/annular_reference_wave_decoupling_20260914.py']:
            compile(source.read_bytes(),str(source),'exec')
            own(source)
            snapshot = output/('executed-'+source.name)
            snapshot.write_bytes(source.read_bytes())
            own(snapshot,'outputs')
        check('inherited_hashes_match_sources_compile',True)
        constants = extended_constants()
        report['constants'] = constants
        check('uniform_constants_finite_positive',all(np.isfinite(value) and value>0 for value in constants.values()))
        main = intake/'annular-compatible-h-evolution-main-attempt01'
        for count in [33,65,129]:
            system = CompatibleEvolution(count,False)
            with np.load(main/('GR_control_count'+str(count)+'.npz'),allow_pickle=False) as archive:
                times,states = archive['times'].copy(),archive['states'].copy()
            for index in [0,8,16]:
                time,state = float(times[index]),states[index]
                velocity,acceleration = reference_acceleration(system,time,state)
                geometry = system.geometry(time,state)
                control = flux_control(system,time,state,velocity,acceleration,constants)
                jet = MassJet(system,geometry,velocity,acceleration)
                higher,terms = higher_energy(jet,constants)
                energy_v,energy_a = control['velocity_energy'],control['acceleration_energy']
                label = 'count'+str(count)+'_sample'+str(index)
                check(label+'_free_endpoint_flux_recursion',control['flux_error']<2e-10,control['flux_error'])
                check(label+'_differentiated_flux_with_live_metric',control['differentiated_flux_error']<2e-9,control['differentiated_flux_error'])
                check(label+'_BV_gradient_bound',control['gradient_variation_norm']<=control['gradient_variation_bound']+1e-9)
                check(label+'_Gram_second_difference_bound',control['Gram_velocity_energy']<=control['second_difference_Gram_bound']+1e-10)
                check(label+'_Gram_BV_bound',control['Gram_velocity_energy']<=control['variation_Gram_bound']+1e-10)
                check(label+'_analytic_Gram_bound',control['Gram_velocity_energy']<=control['analytic_Gram_bound']+1e-10)
                check(label+'_higher_modulated_coercivity',higher>=constants['coercivity']*energy_a/2+energy_v**2-1e-6)
                check(label+'_fourth_phase_derivative_bound',abs(jet.derivative(4,0))<=constants['phase_fourth']*energy_v**2+1e-8)
                check(label+'_mixed_third_derivative_bound',abs(jet.derivative(2,1))<=constants['phase_third']*energy_v*np.sqrt(energy_a)+1e-8)
                check(label+'_higher_energy_rate_bound',abs(terms.sum())<=constants['higher_rate']*np.sqrt(energy_v)*higher+1e-6)
                check(label+'_h_times_higher_energy_forcing_bound',control['Gram_velocity_energy']<=constants['forcing_h_Q_constant']*system.spacing*higher+1e-8)
                if index==0:
                    check(label+'_analytic_initial_acceleration_bound',energy_a<=constants['initial_acceleration_energy_bound'])
                    check(label+'_analytic_initial_higher_energy_bound',higher<=constants['initial_higher_energy_bound'])
                row = dict(count=count,time=time,**control,higher_energy=higher,higher_rate=float(terms.sum()),
                    higher_rate_terms=terms.tolist(),mixed_mass_derivatives={str(powers):float(jet.derivative(*powers)) for powers in
                    [(2,0),(0,2),(2,1),(1,2),(3,0),(3,1),(4,0),(1,1)]},
                    clock_derivatives={str(powers):float(jet.clock_derivative(*powers)) for powers in [(1,0),(0,1),(2,0)]})
                report['cases'].append(row)
                save()
                print(json.dumps(row),flush=True)
        report['state'] = 'complete'
        save()
        print(json.dumps({'state':'complete','checks':len(report['checks']),'constants':constants}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

