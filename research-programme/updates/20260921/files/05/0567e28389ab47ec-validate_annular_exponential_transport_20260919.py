from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_exponential_transport_20260919 import ExponentialTransport
from scipy.linalg import expm
import contextlib
import json
import numpy as np


def exact_forced(frequency, step, initial, forcing, slope, curvature=None):
    blocks = 3 if curvature is None else 4
    matrix = np.zeros((2*blocks, 2*blocks))
    matrix[:2, :2] = [[0., frequency], [-frequency, 0.]]
    for index in range(blocks-1):
        matrix[2*index:2*index+2, 2*index+2:2*index+4] = np.eye(2)
    values = [initial, forcing, slope] if curvature is None else [initial, forcing, slope, curvature]
    return (expm(step*matrix) @ np.concatenate(values))[:2]


def main():
    evidence = EvidenceRun('annular-exponential-transport-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            independent_augmented_matrix_exponential_control=True,
            fixture_not_a_live_parent_evolution=True, all_frequencies_retained=True,
            curvature_bound_requires_actual_remainder_derivative_control=True)
        initial, forcing, slope = np.array([.7, -.2]), np.array([.3, .9]), np.array([-.4, .6])
        for frequency in [0., 1e-12, 1e-6, .1, 3.2, 100., 1e4]:
            flow = ExponentialTransport(np.array([frequency]))
            step = .73
            predicted = flow.exponential(step, initial[:, None])+flow.affine_forcing(step,
                forcing[:, None], (forcing+step*slope)[:, None])
            exact = exact_forced(frequency, step, initial, forcing, slope)
            error = float(np.max(abs(predicted[:, 0]-exact)))
            evidence.check(str(frequency)+'_independent_affine_forcing', error < 3e-10, error)
            covector = np.array([[.2], [-.8]])
            pairing = float(np.sum(covector*flow.exponential(step, initial[:, None])))
            evidence.check(str(frequency)+'_backward_dual_sign', abs(pairing-np.sum(flow.dual(step, covector)*initial[:, None])) < 2e-14)
            evidence.check(str(frequency)+'_unitary_rotation', abs(np.linalg.norm(flow.exponential(step, initial[:, None]))-np.linalg.norm(initial)) < 2e-14)
            evidence.report['cases'].append(dict(kind='affine_exactness', frequency=frequency, error=error, valid_for_claim=False))
        frequency, duration = 43.21, 1.
        flow = ExponentialTransport(np.array([frequency]))
        covector = np.array([[.2], [-.8]])
        for intervals in [4, 8, 16, 32]:
            times = np.linspace(0., duration, intervals+1)
            states = np.array([exact_forced(frequency, time, initial, forcing, slope)[:, None] for time in times])
            remainders = np.array([(forcing+time*slope)[:, None] for time in times])
            row = flow.budget(times, states, remainders, covector)
            evidence.check(str(intervals)+'_exact_linear_remainder_not_endpoint_fitted',
                abs(row['forcing_only_endpoint_difference']) < 3e-13 and row['endpoint_reconstruction_error'] < 3e-13)
            evidence.check(str(intervals)+'_ordinary_trapezoid_negative_control',
                abs(row['ordinary_weighted_trapezoid']-row['exponential_forcing']) > 1e-4)
            row.update(kind='oscillatory_forcing', valid_for_claim=False)
            evidence.report['cases'].append(row)
        curvature = np.array([.9, -.3])
        for frequency in [0., 3.2, 100., 1e4]:
            flow = ExponentialTransport(np.array([frequency]))
            step = .037
            exact = exact_forced(frequency, step, np.zeros(2), forcing, slope, curvature)
            last = forcing+step*slope+step**2*curvature/2
            approximation = flow.affine_forcing(step, forcing[:, None], last[:, None])[:, 0]
            bound = step**3*np.linalg.norm(curvature)/12
            error = float(np.linalg.norm(approximation-exact))
            evidence.check(str(frequency)+'_frequency_independent_curvature_bound', error <= bound+2e-13,
                dict(error=error, bound=bound))
            evidence.report['cases'].append(dict(kind='conditional_curvature_bound', frequency=frequency,
                error=error, bound=float(bound), valid_for_claim=False))
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
