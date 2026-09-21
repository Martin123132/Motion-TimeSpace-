from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_P2_Gram_source_reaction_20260919 import graded_trace_coefficient
from annular_moving_collar_sparse_20260914 import sparse_factors
from scipy.linalg import solve_banded
from types import SimpleNamespace
import contextlib
import json
import numpy as np
import sympy as symbolic


def local_mesh(spacing, phase, power):
    half_count = int(round(1/spacing))
    base = (np.arange(2*half_count+1)-half_count-phase)*spacing
    edge_list = list(base)+[0.]
    left, right = base[half_count], base[half_count+1]
    edge_list.extend(np.linspace(left, 0., 9))
    edge_list.extend(np.linspace(0., right, 9))
    edges = np.unique(edge_list)
    for unused in range((power-1)*int(round(np.log2(1/spacing)))):
        source = int(np.searchsorted(edges, 0.))
        edges = np.sort(np.append(edges, [edges[source-1]/2, edges[source+1]/2]))
    nodes = np.sort(np.concatenate([edges, (edges[:-1]+edges[1:])/2]))
    free = nodes != 0
    node_map = np.full(len(nodes), -1, dtype=int)
    node_map[free] = np.arange(np.sum(free))
    elements = node_map[np.column_stack([np.arange(0, len(nodes)-2, 2),
        np.arange(1, len(nodes)-1, 2), np.arange(2, len(nodes), 2)])]
    radii = nodes[free]
    lengths = np.diff(edges)
    source = int(np.searchsorted(edges, 0.))
    jump = np.zeros(len(radii))
    for element, derivative in [(source-1, -np.array([1., -4., 3.])),
            (source, np.array([-3., 4., -1.]))]:
        indices = elements[element]
        selected = indices >= 0
        jump[indices[selected]] += derivative[selected]/lengths[element]
    factors, unused = sparse_factors(len(base), True)
    original = factors[len(base)-1:].tocsr()
    vertices = np.searchsorted(radii, base)
    coefficients = [graded_trace_coefficient(lengths[:source][::-1]),
        graded_trace_coefficient(lengths[source:])]
    return SimpleNamespace(base=base, radii=radii, edges=edges, lengths=lengths,
        elements=elements, jump=jump, original=original, vertices=vertices,
        source=source, coefficients=coefficients, source_lengths=lengths[source-1:source+1])


def project_affine(mesh, left_trace, right_trace, left_curvature, right_curvature):
    count = len(mesh.radii)
    bands = np.zeros((5, count))
    right_side = np.zeros(count)
    constant_side = np.zeros(count)
    local_mass = np.array([[4., 2., -1.], [2., 16., 2.], [-1., 2., 4.]])/30
    for element, (indices, length) in enumerate(zip(mesh.elements, mesh.lengths)):
        positions = np.array([mesh.edges[element], np.mean(mesh.edges[element:element+2]), mesh.edges[element+1]])
        trace, curvature = (left_trace, left_curvature) if element < mesh.source else (right_trace, right_curvature)
        integrals = length*local_mass @ (-trace-curvature*positions)
        for first in range(3):
            row = indices[first]
            if row >= 0:
                right_side[row] += integrals[first]
                constant_side[row] -= length*np.sum(local_mass[first])
                for second in range(3):
                    column = indices[second]
                    if column >= 0:
                        bands[2+row-column, column] += length*local_mass[first, second]
    solved = solve_banded((2, 2), bands, np.column_stack([right_side, constant_side]), check_finite=False)
    return solved[:, 0], 1+solved[:, 1]


def fixture(spacing, phase, power, left_trace=.01, right_trace=.012, left_curvature=-.8, right_curvature=-1.1):
    mesh = local_mesh(spacing, phase, power)
    projection, mass_defect = project_affine(mesh, left_trace, right_trace, left_curvature, right_curvature)
    radii = mesh.radii
    positive = np.maximum(radii, 0.)
    trace_jump = right_trace-left_trace
    curvature_jump = right_curvature-left_curvature
    field = left_trace*radii+left_curvature*radii**2/2+trace_jump*positive+curvature_jump*positive**2/2
    derivative = np.where(radii < 0, left_trace+left_curvature*radii, right_trace+right_curvature*radii)
    trace_weights = np.where(radii < 0, left_trace, right_trace)
    tail = trace_weights*mass_defect
    original = mesh.original
    hinge = original @ np.maximum(mesh.base, 0.)
    quadratic = original @ np.maximum(mesh.base, 0.)**2
    step = original @ (mesh.base > 0).astype(float)
    field_factor = original @ field[mesh.vertices]-hinge*(mesh.jump @ field)
    projected_factor = original @ projection[mesh.vertices]-hinge*(mesh.jump @ projection)
    exact_field_factor = curvature_jump*quadratic/2
    trace_amplification = np.dot(mesh.coefficients, np.array([left_trace, right_trace])/mesh.source_lengths)
    tail_factor = original @ tail[mesh.vertices]
    exact_projection_factor = trace_amplification*hinge-trace_jump*step+tail_factor
    direct_force = float(field_factor @ projected_factor/spacing)
    main = float(curvature_jump*trace_amplification*(quadratic @ hinge)/(2*spacing))
    step_work = float(-curvature_jump*trace_jump*(quadratic @ step)/(2*spacing))
    tail_work = float(curvature_jump*(quadratic @ tail_factor)/(2*spacing))
    energy = float(field_factor @ field_factor/(2*spacing))
    row_norm = np.asarray(abs(original).sum(axis=1)).ravel()
    tail_bound = float(abs(curvature_jump)*np.max(abs(trace_weights))*np.sum(abs(quadratic)*row_norm)/(2*spacing))
    return dict(spacing=spacing, phase=phase, source_power=power, count=len(radii),
        source_lengths=mesh.source_lengths.tolist(), trace_coefficients=mesh.coefficients,
        trace_amplification=float(trace_amplification), direct_force=direct_force,
        reaction_main=main, derivative_step_work=step_work, mass_defect_tail_work=tail_work,
        reconstructed_force=main+step_work+tail_work, exact_force_split_error=abs(direct_force-main-step_work-tail_work),
        Gram_energy=energy, energy_over_h_cubed=energy/spacing**3,
        force_over_mesh_scale=direct_force/spacing**(2-power),
        source_polynomial_coefficient=float(quadratic @ hinge/spacing**3),
        step_polynomial_coefficient=float(quadratic @ step/spacing**2),
        energy_polynomial_coefficient=float(quadratic @ quadratic/spacing**4),
        projection_identity_error=float(np.max(abs(projection+derivative-tail))),
        field_factor_identity_error=float(np.max(abs(field_factor-exact_field_factor))),
        projected_factor_relative_error=float(np.max(abs(projected_factor-exact_projection_factor))/max(1., np.max(abs(projected_factor)))),
        mass_defect_maximum=float(np.max(abs(mass_defect))), tail_bound=tail_bound,
        all_rows_in_numerical_products=True, valid_for_claim=False)


def main():
    evidence = EvidenceRun('annular-P2-Gram-force-mesh-law-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_live_evolution=True,
            constant_weight_local_projection_fixture=True, no_new_fitted_coupling=True,
            source_motion_tangent_is_rigid_local_translation=True,
            source_shape_weight_derivative_zero_only_in_this_fixture=True,
            not_a_parent_trajectory_or_force_replacement=True,
            no_terms_deleted_from_actual_parent_action=True)
        phase = symbolic.symbols('theta', real=True)
        hinge = symbolic.Matrix([1-phase, 2*phase-1, -phase])
        quadratic = symbolic.Matrix([(1-phase)**2, 1+2*phase-2*phase**2, phase**2])
        step = symbolic.Matrix([1, -2, 1])
        gram = symbolic.Matrix([[10, -1, 0], [-1, 10, -1], [0, -1, 10]])/144
        cross = symbolic.factor((quadratic.T*gram*hinge)[0])
        step_cross = symbolic.factor((quadratic.T*gram*step)[0])
        energy_coefficient = symbolic.factor((quadratic.T*gram*quadratic)[0])
        evidence.report['exact_polynomials'] = dict(source_cross=str(cross), step_cross=str(step_cross),
            energy=str(energy_coefficient), force_formula='Db/2 * (K_H*h^2*T(theta) - DH*h*U(theta) + d2.T*Dtail/h)',
            Gram_energy='Db^2*h^3*V(theta)/8',
            sufficient_local_force_condition='h -> 0, h^2/delta_min -> 0, bounded traces/curvatures and positive constant coefficients',
            warning='This condition is for the source-local projected Gram term on piecewise quadratic data, not the complete evolving parent.')
        evidence.check('symmetry_source_cross_zero', symbolic.simplify(cross.subs(phase, symbolic.Rational(1, 2))) == 0)
        evidence.check('offcentre_source_cross_nonzero', cross.subs(phase, symbolic.Rational(3, 5)) != 0)
        expected_cross = float(cross.subs(phase, symbolic.Rational(3, 5)))
        expected_step = float(step_cross.subs(phase, symbolic.Rational(3, 5)))
        expected_energy = float(energy_coefficient.subs(phase, symbolic.Rational(3, 5)))
        for power in [1, 2, 3]:
            for denominator in [8, 16, 32, 64, 128, 256, 512]:
                row = fixture(1/denominator, .6, power)
                key = str(power)+'_'+str(denominator)
                evidence.check(key+'_exact_phase_and_energy',
                    abs(row['source_polynomial_coefficient']-expected_cross) < 2e-10
                    and abs(row['step_polynomial_coefficient']-expected_step) < 2e-10
                    and abs(row['energy_polynomial_coefficient']-expected_energy) < 2e-10
                    and abs(row['energy_over_h_cubed']-.3**2*expected_energy/8) < 2e-10)
                evidence.check(key+'_independent_mass_projection', row['projection_identity_error'] < 2e-12
                    and row['mass_defect_maximum'] <= 1+2e-12
                    and row['projected_factor_relative_error'] < 2e-9)
                evidence.check(key+'_complete_force_split', row['field_factor_identity_error'] < 2e-13
                    and row['exact_force_split_error'] < 5e-10*max(1., abs(row['direct_force']))
                    and abs(row['mass_defect_tail_work']) <= row['tail_bound']+1e-18)
                evidence.report['cases'].append(row)
                evidence.save()
        for power in [1, 2, 3]:
            selected = [row for row in evidence.report['cases'] if row['source_power'] == power]
            evidence.check(str(power)+'_energy_decays_while_force_scale_is_measured',
                selected[-1]['Gram_energy'] < selected[-2]['Gram_energy']/7.9)
        control = fixture(1/64, .5, 2)
        evidence.check('symmetric_phase_is_not_universal_suppression', abs(control['reaction_main']) < 2e-14
            and abs(expected_cross) > 1e-4)
        evidence.report.update(symmetric_control=control,
            coefficients=dict(left_trace=.01, right_trace=.012, left_curvature=-.8, right_curvature=-1.1),
            coefficients_not_fitted_to_live_result=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), polynomials=evidence.report['exact_polynomials'],
            finest=[row for row in evidence.report['cases'] if row['spacing'] == 1/512])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
