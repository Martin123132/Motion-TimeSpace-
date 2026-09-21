from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_dynamic_reduction_bound_20260916 import build_reduction, evolution, source_load
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import initial
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-force-aware-modes-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        parent = intake/'annular-invariant-modal-force-bound-attempt01'
        path = parent/'status.json'
        evidence.own(path)
        status = json.loads(path.read_text())
        evidence.check('invariant_tail_bound_complete', status['state']=='complete' and all(row['passed'] for row in status['checks']))
        budget = 2e-7
        times = np.linspace(0., .4, 1601)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            path = parent/(branch+'-modal-budget.npz')
            evidence.own(path)
            saved = np.load(path)
            contribution = saved['force_contribution_envelope']
            contribution = np.maximum(contribution, contribution.T)
            retained = list(range(len(contribution)))
            removed, ledger = [], []
            current_bound = 0.
            while retained:
                principal = contribution[np.ix_(retained, retained)]
                costs = np.sum(principal, axis=1)-np.diag(principal)/2
                candidate = int(np.argmin(costs))
                if current_bound+costs[candidate]>budget:
                    break
                mode = retained.pop(candidate)
                removed.append(mode)
                current_bound = float(np.sum(contribution[np.ix_(retained, removed)])+np.sum(contribution[np.ix_(removed, removed)])/2)
                ledger.append(dict(removed_index=mode, resulting_bound=current_bound, remaining_modes=len(retained)))
            evidence.check(branch+'_greedy_envelope_within_budget', current_bound<=budget and all(row['resulting_bound']<=budget for row in ledger))
            coarse = QuadraticSourceFittedAction(129, gram, background_mass=0.)
            fine = LocallyRefinedSourceAction(129, gram, background_mass=0., source_splits=8)
            data = build_reduction(coarse, fine)
            evidence.check(branch+'_same_original_eigenfrequencies', np.allclose(data['full_frequencies'], saved['frequencies'], rtol=2e-12, atol=2e-10))
            coordinates, rates = np.split(initial(fine)[:-1], 2)
            position, velocity = coordinates[:-1], rates[:-1]
            full_q, full_v, full_a = evolution(data['mass'], data['full_frequencies'], data['full_vectors'], position, velocity, times)
            reduced_q, reduced_v, reduced_a = evolution(data['mass'], data['full_frequencies'][retained], data['full_vectors'][:, retained], position, velocity, times)
            full_load = source_load(data, full_q, full_v, full_a)
            reduced_load = source_load(data, reduced_q, reduced_v, reduced_a)
            error = abs(full_load-reduced_load)
            evidence.check(branch+'_source_specific_bound_controls_observed_error', np.max(error)<=current_bound*(1+2e-8)+2e-10,
                dict(maximum_observed=float(np.max(error)), uniform_envelope=current_bound))
            path = evidence.output/(branch+'-force-aware.npz')
            np.savez_compressed(path, times=times, full_source_load=full_load, reduced_source_load=reduced_load,
                absolute_error=error, uniform_bound=current_bound, retained_indices=retained, removed_indices=removed)
            evidence.own(path, 'outputs')
            evidence.report['cases'].append(dict(branch=branch, fine_dof=fine.count, retained_mode_count=len(retained), removed_mode_count=len(removed),
                retained_indices=retained, removed_indices=removed, removal_ledger=ledger, source_load_budget=budget,
                uniform_source_load_tail_bound=current_bound, maximum_sampled_source_load_error=float(np.max(error)),
                highest_frequency_mode_retained=bool(fine.count-1 in retained), nontrivial_reduction=bool(removed),
                exact_arithmetic_uniform_bound=True, interval_roundoff_certified=False, globally_minimal_mode_count_claimed=False))
            evidence.save()
        evidence.report.update(scope='Force-observable-aware greedy truncation of invariant full-field normal modes at frozen source. No re-fitting, new physical coefficient, or modified original trajectory.',
            original_initial_data_retained_in_error_budget=True, original_action_changed=False, damping_added=False,
            local_trace_axiom_added=False, moving_source_certified=False, GR_oracle_comparison=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
