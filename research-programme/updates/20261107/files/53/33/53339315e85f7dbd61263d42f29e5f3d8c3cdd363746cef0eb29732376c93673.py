from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_wave_flux_form_v2_20260929 import WaveFlux
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from decimal import localcontext
from fractions import Fraction
from types import SimpleNamespace
import json
import numpy as np


def metric_fixture(edges, response=False):
    edges = np.asarray(edges)
    lengths = np.diff(edges)
    centers = (edges[:-1]+edges[1:])/2
    scale = .015 if response else 1.
    primitive = np.zeros((2, len(lengths), 3))
    primitive[0, :, 1] = scale*.001
    primitive[0, :, 2] = scale*.00003
    primitive[1, :, 1] = scale*.0007
    primitive[1, :, 2] = -scale*.00004
    left = scale*np.array([[.65, .675, .662], [-.2, -.194, -.203]])
    derivative = np.polynomial.chebyshev.chebder(primitive, axis=2)*2/lengths[None, :, None]
    rhs = np.pad(derivative, ((0, 0), (0, 0), (0, 1)))
    return SimpleNamespace(solver=SimpleNamespace(edges=edges, lengths=lengths, centers=centers),
        solution=dict(primitives=primitive, left=left, rhs_coefficients=rhs))


def fixture():
    mesh = dict(anchor='6', edges=['5', '6', '7'], elements=[[0, 1, -1], [-1, 2, 3]])
    metric = metric_fixture([4.8, 5.37, 6.23, 7.2])
    response = metric_fixture([4.8, 5.61, 6.72, 7.2], True)
    field = np.array([[.2], [.25], [-.1], [.15]])
    rates = np.array([[.01], [-.02], [.03], [.005]])
    action = SimpleNamespace(mesh=mesh, edges=list(map(Fraction, mesh['edges'])),
        owner=SimpleNamespace(model=SimpleNamespace(anchor=6.), width=.1),
        source=np.array([6.04]), velocity=np.array([.03]), cardinal=lambda label: np.array([1.]),
        gradient=local_polynomials(mesh, decimals(field))[1],
        rate_polynomial=local_polynomials(mesh, decimals(rates))[0], solver=metric.solver, solution=metric.solution)
    directions = dict(field_vertices=np.array([[.017, -.012, .006, .018]]),
        edge_vertices=np.array([[.03, -.02, .01]]))
    correction = np.array([[0., 0., 0., 0., -.006]])
    mode = np.array([[.003, -.002, .001, .004, .005]])
    return WaveFlux(action, directions, correction, mode, response)


def family_force(wave, label, amount, order=48):
    data = wave.label_data(label)
    displacement_edges = np.where(wave.edges < 0., 1+wave.edges/(-wave.edges[0]), 1-wave.edges/wave.edges[-1])
    moved = data['mapped']+amount*(data['edge']+displacement_edges*data['source_mode'])
    jacobians = np.diff(moved)/wave.widths
    cuts = np.unique(np.r_[moved, wave.radial_cuts[(wave.radial_cuts > moved[0]) & (wave.radial_cuts < moved[-1])]])
    middle = cuts[:-1]+np.diff(cuts)/2
    cells = np.searchsorted(moved, middle, side='right')-1
    nodes, weights = np.polynomial.legendre.leggauss(order)
    offsets = (cuts[:-1, None]+np.diff(cuts)[:, None]*(nodes+1)/2).ravel()
    measure = (np.diff(cuts)[:, None]*weights/2).ravel()
    cells = np.repeat(cells, order)
    local = (offsets-moved[cells])/(wave.widths[cells]*jacobians[cells])
    reference = wave.edges[cells]+wave.widths[cells]*local
    displacement = np.where(reference < 0., 1+reference/(-wave.edges[0]), 1-reference/wave.edges[-1])
    coefficients = data['gradient']+amount*data['field_gradient']
    gradient = (coefficients[cells, 0]+local*coefficients[cells, 1])/jacobians[cells]
    rate_coefficients = data['rate']+amount*data['mode']
    rate = rate_coefficients[cells, 0]+local*(rate_coefficients[cells, 1]+local*rate_coefficients[cells, 2])
    speed = displacement*(data['velocity']+amount*data['source_rate'])
    values = wave.metric.evaluate(offsets, wave.metric.cells(offsets))[0]
    values += amount*sum(item.evaluate(offsets, item.cells(offsets))[0] for item in wave.responses)
    radius = wave.anchor+offsets
    metric, lapse = 1-2*values[0]/radius, np.exp(values[1])
    alpha, beta = radius**2/(lapse*np.sqrt(metric)), radius**2*lapse*np.sqrt(metric)
    flux = alpha*(rate-speed*gradient)*speed+beta*gradient
    test_r = np.column_stack([4*local-3, 4-8*local, 4*local-1])/(wave.widths[cells]*jacobians[cells])[:, None]
    force = np.zeros((1, 5))
    indices = wave.indices[cells]
    for column in range(3):
        active = indices[:, column] >= 0
        np.add.at(force[0], indices[active, column], -measure[active]*flux[active]*test_r[active, column])
    return force


def main():
    evidence = EvidenceRun('annular-wave-flux-manufactured-validation-attempt01', __file__)
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, manufactured_data_only=True,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.own(evidence.root/'scripts/annular_wave_flux_form_v2_20260929.py')
        maximum = lambda values: float(np.max(np.abs(values)))
        with localcontext() as context:
            context.prec = 70
            wave = fixture()
            result, diagnostics = wave.fixed_label(.13, 32, (1, 5))
            regular = result['volume']+result['jumps']+result['endpoints']
            complete = regular+result['moving_cuts']
            base = result['base_volume']+result['base_jumps']+result['base_endpoints']
            evidence.check('nonzero_jump_fixture_unambiguous', diagnostics['coincident_cuts'] == 0)
            evidence.check('actual_code_weak_flux_identity', maximum(regular-result['weak']) < 2e-11, maximum(regular-result['weak']))
            evidence.check('actual_code_base_identity', maximum(base-result['base_weak']) < 2e-11, maximum(base-result['base_weak']))
            evidence.check('independent_base_family_replay', maximum(base-family_force(wave, .13, 0.)) < 2e-11,
                maximum(base-family_force(wave, .13, 0.)))
            rows = []
            differences = []
            for step in [1e-4, 5e-5, 2.5e-5]:
                finite = (family_force(wave, .13, step)-family_force(wave, .13, -step))/(2*step)
                differences.append(finite)
                rows.append(dict(step=step, full_error=maximum(finite-complete), without_cut_error=maximum(finite-regular)))
            richardson = (4*differences[-1]-differences[-2])/3
            evidence.check('independent_moving_family_derivative', maximum(richardson-complete) < 2e-8,
                maximum(richardson-complete))
            for name in ['moving_cuts', 'jumps', 'endpoints']:
                evidence.check('omitted_'+name+'_negative_control', maximum(richardson-(complete-result[name])) > 1e-6,
                    maximum(richardson-(complete-result[name])))
            data = wave.label_data(.13)
            offsets = np.array([-.8, -.25, .15, .85])
            cells = np.searchsorted(data['mapped'], offsets, side='right')-1
            selected = wave.metric.cells(offsets)
            selected_responses = [item.cells(offsets) for item in wave.responses]
            packet = wave.evaluate(data, offsets, cells, selected, selected_responses)
            shifted = wave.evaluate(data, offsets+1e-25j, cells, selected, selected_responses)
            spatial_error = maximum(shifted['change'].imag/1e-25-packet['change_r'])
            evidence.check('independent_complex_spatial_H_derivative', spatial_error < 2e-11, spatial_error)
            evidence.check('complex_material_flux_derivative', maximum(result['oracle_difference']) < 2e-11,
                maximum(result['oracle_difference']))
            archive = evidence.output/'manufactured-complete-force.npz'
            np.savez_compressed(archive, **result, independent_richardson=richardson)
            evidence.own(archive, 'outputs')
            evidence.report['cases'].append(dict(finite_difference_checks=rows, diagnostics=diagnostics,
                final_error=maximum(richardson-complete), valid_for_claim=False))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
