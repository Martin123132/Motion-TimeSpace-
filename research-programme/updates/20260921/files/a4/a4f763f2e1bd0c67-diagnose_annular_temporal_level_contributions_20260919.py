from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_action_response_time_halving_20260919 import restore_action
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-temporal-level-contributions-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,signed_temporal_telescope_not_physical_causal_proof=True,
            full_Gram_and_fixed_interpolation_retained=True)
        evidence.report['points'] = []
        for branch in ['reference','MTS']:
            action = restore_action(checked_load(evidence,'annular-action-exponential-response-attempt01',branch+'-fine-action.npz'))
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            all_vectors = []
            for index in range(17):
                low = checked_load(evidence,'annular-action-response-time-halving-attempt01',branch+'-lower-point'+str(index).zfill(3)+'.npz')
                high = checked_load(evidence,'annular-moving-duhamel-trajectory-attempt01',branch+'-point'+str(2*index).zfill(3)+'.npz')
                fine_velocity = low['1_reverse_velocity']-high['1_reverse_velocity']
                fine_acceleration = low['1_acceleration']-high['1_acceleration']
                coarse_velocity = interpolation @ (low['0_reverse_velocity']-high['0_reverse_velocity'])
                coarse_acceleration = interpolation @ (low['0_acceleration']-high['0_acceleration'])
                fine_squared = 2*action.energy(fine_velocity,fine_acceleration)
                coarse_squared = 2*action.energy(coarse_velocity,coarse_acceleration)
                signed_cross = -2*float(fine_acceleration @ action.mass(coarse_acceleration)
                    +fine_velocity @ action.stiffness(coarse_velocity))
                total_squared = 2*action.energy(fine_velocity-coarse_velocity,fine_acceleration-coarse_acceleration)
                error = abs(total_squared-fine_squared-coarse_squared-signed_cross)
                evidence.check(branch+'_'+str(index)+'_signed_temporal_norm_telescope',error < 1e-10*max(
                    total_squared,fine_squared,coarse_squared,abs(signed_cross),1e-30)+1e-25)
                row = dict(branch=branch,reverse_time=float(low['reverse_time']),physical_time=float(4e-5-low['reverse_time']),
                    fine_temporal_norm=float(np.sqrt(max(fine_squared,0.))),coarse_temporal_norm=float(np.sqrt(max(coarse_squared,0.))),
                    combined_temporal_norm=float(np.sqrt(max(total_squared,0.))),signed_cross_energy_twice=signed_cross,
                    reconstruction_error=error,valid_for_claim=False)
                evidence.report['points'].append(row)
                all_vectors.append(np.stack([fine_velocity,fine_acceleration,coarse_velocity,coarse_acceleration]))
            rows = [row for row in evidence.report['points'] if row['branch'] == branch]
            evidence.report['cases'].append(dict(branch=branch,endpoint_fine_temporal_norm=rows[0]['fine_temporal_norm'],
                endpoint_coarse_temporal_norm=rows[0]['coarse_temporal_norm'],endpoint_combined_norm=rows[0]['combined_temporal_norm'],
                max_fine_temporal_norm=max(row['fine_temporal_norm'] for row in rows),
                max_coarse_temporal_norm=max(row['coarse_temporal_norm'] for row in rows),
                shared_initial_temporal_norm=rows[-1]['combined_temporal_norm'],valid_for_claim=False))
            path = evidence.output/(branch+'-temporal-level-differences.npz')
            np.savez_compressed(path,reverse_times=[row['reverse_time'] for row in rows],vectors=all_vectors)
            evidence.own(path,'outputs')
            evidence.save()
            print(json.dumps(evidence.report['cases'][-1]),flush=True)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
