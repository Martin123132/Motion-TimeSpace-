from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, IndexedP2Material
from annular_P2_graded_source_20260919 import GradedSourceAction
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-Gram-trajectory-defect-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            frozen_fine_geometry_and_source_position=True,
            embedded_coarse_field_not_a_separately_evolved_fine_state=True,
            hierarchical_field_difference_not_known_continuum_error=True,
            full_geometry_feedback_difference_not_in_this_split=True,
            actual_Gram_and_cross_terms_retained=True)
        for branch in ['reference', 'MTS']:
            fine_folder = 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS' else 'annular-P2-bulk513-evolution-reference-attempt01'
            fine_name = 'steps128-accepted128.npz' if branch == 'MTS' else 'steps64-accepted064.npz'
            fine = checked_load(evidence, fine_folder, fine_name)
            coarse = checked_load(evidence, 'annular-P2-local-Gram-bound-attempt01', branch+'257-row-data.npz')
            system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            coordinates, momenta = fine['state']
            rates, geometry = system.solve(coordinates, momenta)
            interpolation = IndexedP2Material(system, coordinates).interpolation(np.array([0.]))[0]
            values, speeds = interpolation @ coordinates, interpolation @ rates
            layer = system.layer(0., geometry)
            coarse_model = GradedSourceAction(257, branch == 'MTS', source_cap=2e-5)
            indices, shapes, unused = coarse_model.features_quadratic(layer.radii)
            base = np.append(np.sum(shapes*coarse['coordinates'][:-1][indices], axis=1), values[-1])
            difference = np.append(values[:-1]-base[:-1], values[-1])
            fine_report, fine_rows = row_bounds(layer, values, speeds)
            base_report, base_rows = row_bounds(layer, base, speeds)
            difference_report, difference_rows = row_bounds(layer, difference, speeds)
            field, field_error = base_rows['field_factors'], difference_rows['field_factors']
            direction, direction_error = base_rows['direction_factors'], difference_rows['direction_factors']
            changed, jacobian, unused = layer.mapping(layer.radii, complex(values[-1], 1e-25))
            weight_derivative = np.asarray(layer.sampling @ (layer.coefficient(0., changed)/jacobian)).imag/(1e-25*layer.gram_spacing)
            weights = fine_rows['weights']
            terms = dict(shape_mixed=-weight_derivative*field*field_error,
                shape_quadratic=-.5*weight_derivative*field_error**2,
                projection_direction_mixed=weights*direction_error*field,
                projection_field_mixed=weights*direction*field_error,
                projection_quadratic=weights*direction_error*field_error)
            measured = fine_report['explicit_drive']-base_report['explicit_drive']
            predicted = sum(float(np.sum(term)) for term in terms.values())
            evidence.check(branch+'_fixed_geometry_linear_projection', np.max(abs(
                fine_rows['projection']-base_rows['projection']-difference_rows['projection']), initial=0.) < 2e-13)
            evidence.check(branch+'_exact_quadratic_trajectory_defect', abs(predicted-measured) < 2e-15)
            components = []
            for name, mask in [('source_straddling', fine_rows['source_rows']), ('remaining', ~fine_rows['source_rows'])]:
                norm_field = np.sqrt(weights[mask] @ field[mask]**2)
                norm_error = np.sqrt(weights[mask] @ field_error[mask]**2)
                norm_direction = np.sqrt(weights[mask] @ direction[mask]**2)
                norm_direction_error = np.sqrt(weights[mask] @ direction_error[mask]**2)
                shape_bound = float(np.sum(abs(terms['shape_mixed'][mask])+abs(terms['shape_quadratic'][mask])))
                bound = shape_bound+norm_direction_error*norm_field+norm_direction*norm_error+norm_direction_error*norm_error
                signed = sum(float(np.sum(term[mask])) for term in terms.values())
                absolute = sum(float(np.sum(abs(term[mask]))) for term in terms.values())
                evidence.check(branch+'_'+name+'_localized_defect_bound', abs(signed) <= absolute+2e-20
                    and absolute <= bound+2e-20)
                components.append(dict(name=name, signed_difference=signed, absolute_row_bound=absolute,
                    partitioned_Cauchy_bound=float(bound), error_Gram_norm=float(norm_error),
                    projected_error_Gram_norm=float(norm_direction_error)))
            row = dict(branch=branch, coarse_count=257, fine_count=513,
                fine_explicit_drive=fine_report['explicit_drive'],
                embedded_coarse_drive_at_fine_geometry=base_report['explicit_drive'],
                measured_difference=measured, reconstructed_difference=predicted,
                field_nodal_maximum_difference=float(max(abs(difference[:-1]))),
                source_jump_difference=float(layer.jump @ difference[:-1]),
                components=components, terms={name:float(np.sum(term)) for name,term in terms.items()},
                valid_for_claim=False, no_error_bound_to_continuum_claim=True)
            evidence.report['cases'].append(row)
            evidence.save()
            print(json.dumps(row), flush=True)
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
