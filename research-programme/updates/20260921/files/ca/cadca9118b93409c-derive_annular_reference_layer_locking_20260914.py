import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_reference_layer_locking_20260914 import locking_constants,pair_diagnostics


def run():
    evidence = EvidenceRun('annular-reference-layer-locking-attempt01',__file__)
    try:
        constants = locking_constants()
        evidence.report['constants'] = constants
        evidence.report['test_scope'] = 'Fresh short reference evolution; finite-layer numerical replay, not a formal proof certificate.'
        for count in [33,65,129]:
            system = CompatibleEvolution(count,False,degree=8)
            duration = .0002
            solution = system.integrate(duration=duration,divisor=4)
            archive = evidence.output/('reference_count'+str(count)+'.npz')
            np.savez_compressed(archive,times=np.array([0.,duration]),
                                states=np.stack([system.initial_state,solution.y[:,-1]]))
            evidence.own(archive,'outputs')
            for time,state in [(0.,system.initial_state),(duration,solution.y[:,-1])]:
                row,raw = pair_diagnostics(system,time,state)
                evidence.report['cases'].append(row)
                label = str(count)+'_'+str(time)
                scale = max(1e-12,abs(row['direct_rate']),abs(row['forcing_pairing']))
                evidence.check(label+'_exact_pair_balance',row['balance_error']<2e-10*scale+1e-14,row['balance_error'])
                evidence.check(label+'_variance_identity',row['variance_identity_error']<1e-16)
                evidence.check(label+'_positive_energy',row['pair_energy']>0 and row['forcing_square']>=0)
                evidence.check(label+'_Cauchy_forcing',abs(row['forcing_pairing'])<=
                               np.sqrt(2*row['pair_energy']*row['forcing_square'])+1e-13)
                evidence.check(label+'_bulk_a_translation',row['max_a_difference']<=
                               system.spacing*constants['delta_a_multiplier']+1e-12)
                evidence.check(label+'_bulk_c_translation',row['max_bulk_c_difference']<=
                               system.spacing*constants['delta_c_multiplier']+1e-12)
                evidence.check(label+'_clock_time_bound',row['max_log_rate']<=
                               constants['time_log_multiplier']*np.sqrt(row['velocity_energy'])+1e-12)
                evidence.check(label+'_bulk_b_translation',row['max_b_difference']<=
                               system.spacing*constants['delta_b_multiplier']*np.sqrt(row['velocity_energy'])+1e-12)
                evidence.check(label+'_bulk_d_translation',row['max_bulk_d_difference']<=
                               system.spacing*constants['delta_d_multiplier']*np.sqrt(row['velocity_energy'])+1e-12)
                evidence.check(label+'_source_retained_forcing_bound',
                               row['forcing_square']<=row['analytic_forcing_square_bound']+1e-12)
                evidence.check(label+'_proved_comparison_interval',time<constants['uniform_tangent_comparison_time'])
                print(str(count)+' t='+str(time)+' pair='+str(row['pair_energy']),flush=True)
        for time in [0.,.0002]:
            rows = [row for row in evidence.report['cases'] if row['time']==time]
            evidence.check(str(time)+'_pair_energy_refines',
                           all(second['pair_energy']<first['pair_energy'] for first,second in zip(rows,rows[1:])))
            evidence.check(str(time)+'_phase_variance_refines',
                           all(second['phase_variance']<first['phase_variance'] for first,second in zip(rows,rows[1:])))
        evidence.report['paper_derivation_status'] = 'Layer locking and strong-compactness argument recorded separately; broad physics flags unchanged.'
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

