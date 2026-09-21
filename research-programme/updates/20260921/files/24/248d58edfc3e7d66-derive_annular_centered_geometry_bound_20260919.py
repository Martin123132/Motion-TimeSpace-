from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_force_coefficient_bounds_20260919 import quadrature_values
from annular_Gram_projection_commutator_20260919 import field_extension
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def centered_pairing(weighted_defect, multiplier):
    absolute = abs(weighted_defect)
    if np.sum(absolute) > 0:
        order = np.argsort(multiplier)
        position = np.searchsorted(np.cumsum(absolute[order]), np.sum(absolute)/2)
        center = float(multiplier[order[position]])
    else:
        center = 0.
    orthogonality = float(np.sum(weighted_defect))
    centered = (multiplier-center)*weighted_defect
    correction = center*orthogonality
    return dict(direct_pairing=float(multiplier @ weighted_defect), centered_pairing=float(np.sum(centered)),
        floating_orthogonality_correction=correction, weighted_median_center=center,
        orthogonality_defect=orthogonality, centered_absolute_bound=float(np.sum(abs(centered))+abs(correction)),
        uncentered_absolute_bound=float(np.sum(abs(multiplier*weighted_defect))), valid_for_claim=False)


def main():
    evidence = EvidenceRun('annular-centered-geometry-bound-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, all_quadrature_terms_retained=True, floating_orthogonality_residual_retained=True,
            weighted_median_is_bound_optimization_not_a_physical_fit=True, full_nonlinear_stability_proven=False)
        terms = np.array([1., -2., 1.])
        for name, multiplier in [('uniform', np.full(3, 3.)), ('nearly_uniform', 3.+1e-9*np.array([1., -1., 0.])),
                ('variable', np.array([-.2, 1.1, 2.3]))]:
            result = centered_pairing(terms, multiplier)
            evidence.check(name+'_exact_centered_identity', abs(result['direct_pairing']-result['centered_pairing']
                -result['floating_orthogonality_correction']) < 3e-15)
            evidence.check(name+'_centered_bound', abs(result['direct_pairing']) <= result['centered_absolute_bound']+3e-15)
            if name == 'uniform':
                evidence.check('uniform_weight_rescaling_has_zero_response', result['centered_absolute_bound'] == 0.
                    and result['uncentered_absolute_bound'] > 1.)
            if name == 'nearly_uniform':
                evidence.check('discarded_cancellation_negative_control', result['centered_absolute_bound']
                    < 1e-8*result['uncentered_absolute_bound'])
            evidence.report.setdefault('controls', []).append(dict(fixture=name, **result))
        for branch in ['reference', 'MTS']:
            folder = 'annular-live-coefficient-rate-'+branch+'-attempt01'
            saved = checked_load(evidence, folder, 'endpoint-rate-data.npz')
            status_path = evidence.output.parent/folder/'status.json'
            status = json.loads(status_path.read_text())
            evidence.own(status_path)
            system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(system.labels)))
            state = saved['full_state']
            unused, geometry = system.solve(*state)
            layer = system.layer(system.labels[center], geometry)
            coordinates = state[0, center]
            base = field_extension(layer, system.model, coordinates, coordinates[-1])
            for partition in ['all_rows', 'source_straddling', 'remaining']:
                mask = np.ones(len(base['factor']), dtype=bool) if partition == 'all_rows' else base['source_rows']
                if partition == 'remaining':
                    mask = ~mask
                covector = np.asarray(layer.lifted.T @ (mask*base['weights']*base['factor'])).ravel()
                dual = solve_banded((2, 2), base['bands'], covector, check_finite=False)
                dual_values = quadrature_values(layer, dual)
                for side in range(2):
                    weighted_defect = saved['kinetic_weights']*dual_values*saved['projection_defects'][:, side]
                    for step in [2e-7, 1e-7, 5e-8, 2.5e-8]:
                        multiplier = saved['kinetic_rate_'+str(step)]/saved['kinetic_weights']
                        result = centered_pairing(weighted_defect, multiplier)
                        prior = next(row for row in status['cases'] if row['partition'] == partition and row['side'] == side
                            and row['tangent_step'] == step)
                        error = abs(result['direct_pairing']-result['centered_pairing']-result['floating_orthogonality_correction'])
                        tag = branch+'_'+partition+'_'+str(side)+'_'+str(step)
                        evidence.check(tag+'_original_rate_and_centering_retained', abs(result['direct_pairing']-prior['mass_response_rate']) < 3e-18
                            and error < 3e-18)
                        evidence.check(tag+'_centered_upper_bound', abs(result['direct_pairing']) <= result['centered_absolute_bound']+3e-18)
                        evidence.report['cases'].append(dict(branch=branch, partition=partition, side=side, tangent_step=step,
                            **result, centered_identity_error=error))
            evidence.save()
            print(json.dumps(dict(branch=branch, finest=[row for row in evidence.report['cases'] if row['branch'] == branch
                and row['partition'] == 'all_rows' and row['tangent_step'] == 2.5e-8])), flush=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
