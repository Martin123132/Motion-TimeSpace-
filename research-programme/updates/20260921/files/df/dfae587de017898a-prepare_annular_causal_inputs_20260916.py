from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-causal-inputs-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-force-response-paths-attempt01'
        evidence.own(folder/'status.json')
        status = json.loads((folder/'status.json').read_text())
        evidence.check('source_replays_complete', status['state']=='complete')
        evidence.report.update(predictor_keys=['times', 'reduced_states', 'reduced_derivatives', 'initial_state'],
            input_isolation_not_blind_discovery=True, future_full_arrays_loaded=False,
            model=dict(base_count=129, source_splits=8, background_mass=0., anchor=6.03),
            planned_cases=['reference-stride1', 'reference-stride2', 'MTS-stride1', 'MTS-stride2',
                           'reference-tight', 'MTS-tight'],
            configuration=dict(standard_rtol=2e-8, standard_atol=1e-14, tight_rtol=2e-10,
                tight_atol=1e-16, force_control=2e-10, isolated_force_budget=2e-7,
                state_controls=dict(field=1e-9, source=1e-11, field_rate=1e-6, source_rate=1e-9, clock=1e-11)))
        for branch in ['reference', 'MTS']:
            path = folder/(branch+'-physical-paths.npz')
            evidence.own(path)
            with np.load(path, allow_pickle=False) as saved:
                data = {key:saved[key].copy() for key in ['times', 'reduced_states', 'reduced_derivatives']}
            system = LocallyRefinedSourceAction(129, branch=='MTS', background_mass=0., source_splits=8)
            data['initial_state'] = initial(system)
            evidence.check(branch+'_finite_fixed_shapes', data['reduced_states'].shape==(321,575)
                and data['reduced_derivatives'].shape==(321,575) and data['initial_state'].shape==(575,)
                and all(np.isfinite(value).all() for value in data.values()))
            evidence.check(branch+'_time_domain', np.all(np.diff(data['times'])>0.)
                and data['times'][0]==0. and data['times'][-1]==.005)
            destination = evidence.output/(branch+'-predictor-inputs.npz')
            np.savez_compressed(destination, **data)
            evidence.own(destination, 'outputs')
            evidence.report['cases'].append(dict(branch=branch, initial_state_from_original_function=True,
                future_full_arrays_loaded=False, restricted_arrays_only=True))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
