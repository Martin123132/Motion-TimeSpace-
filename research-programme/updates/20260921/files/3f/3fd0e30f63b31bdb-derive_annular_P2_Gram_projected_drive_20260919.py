from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_graded_source_20260919 import force_schur_identity
from annular_live_P2_current_20260918 import LiveP2Tangent
from run_annular_P2_continuum_bridge_20260918 import checked_load
from verify_annular_P2_live_exponential_direct_20260919 import encode
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def gram_energy(layer, values):
    nodes, jacobian, unused = layer.mapping(layer.radii, values[-1])
    weights = np.asarray(layer.sampling @ (layer.coefficient(0., nodes)/jacobian))/layer.gram_spacing
    factors = layer.lifted @ values[:-1]
    return np.dot(weights, factors**2)/2


def main():
    evidence = EvidenceRun('annular-P2-Gram-projected-drive-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            actual_live_geometry_tangent_held_for_algebraic_split=True,
            residual_drive_contains_implicit_Gram_geometry_feedback=True,
            removing_explicit_Gram_is_not_a_physical_counterfactual=True)
        for branch in ['reference', 'MTS']:
            configurations = [(257, 2e-5, 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01'),
                    'steps32-accepted032.npz'),
                (513, 1e-5, 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS'
                    else 'annular-P2-bulk513-evolution-reference-attempt01',
                    'steps128-accepted128.npz' if branch == 'MTS' else 'steps64-accepted064.npz')]
            for count, cap, folder, filename in configurations:
                saved = checked_load(evidence, folder, filename)
                source_path = evidence.output.parent/folder/'status.json'
                status = json.loads(source_path.read_text())
                expected = status['cases'][-1]
                if branch == 'MTS' and count == 513:
                    prior_folder = 'annular-P2-bulk513-evolution-MTS-attempt01'
                    basis = checked_load(evidence, prior_folder, 'frozen-canonical-basis.npz')
                    prior_state = checked_load(evidence, prior_folder, 'steps64-accepted064.npz')['state']
                    scale = np.linalg.norm(encode(basis, basis['initial'])[:, :, :-1])
                    difference = float(np.linalg.norm(encode(basis, saved['state']-prior_state)[:, :, :-1])/scale)
                    evidence.report['common_basis_64_to_128_time_state_difference'] = difference
                    evidence.check('physical_time_difference_in_one_sealed_basis', difference < 1e-6
                        and abs(difference-status['time_state_difference']) < 2e-12)
                system = IndexedGradedP2System(count, branch == 'MTS', cap)
                tangent = LiveP2Tangent(system, *saved['state'])
                current = tangent.layer_data(0.)
                layer, values, data = current.layer, current.coordinates, current.data
                schur = force_schur_identity(current)
                projection = solve_banded((2, 2), data['mass_bands'], data['cross'], check_finite=False)
                nodes, jacobian, unused = layer.mapping(layer.radii, values[-1])
                weights = np.asarray(layer.sampling @ (layer.coefficient(0., nodes)/jacobian))/layer.gram_spacing
                factors, projected_factors = layer.lifted @ values[:-1], layer.lifted @ projection
                scalar_covector = -layer.lifted.T @ (weights*factors)
                projected_variation = float(weights @ (factors*projected_factors))
                changed_source = values.astype(complex).copy()
                changed_source[-1] += 1j*current.step
                shape_force = float(-gram_energy(layer, changed_source).imag/current.step)
                changed_field = values.astype(complex).copy()
                changed_field[:-1] += 1j*current.step*projection
                derivative = float(gram_energy(layer, changed_field).imag/current.step)
                explicit_drive = shape_force+projected_variation
                remainder = schur['free_wave_drive']-explicit_drive
                energy = float(gram_energy(layer, values))
                projected_energy = float(weights @ projected_factors**2/2)
                projected_bound = 2*float(np.sqrt(max(0., energy*projected_energy)))
                key = branch+str(count)
                evidence.check(key+'_same_saved_force_and_drive',
                    abs(-current.wave_source_euler-expected['force']) < 2e-10
                    and abs(schur['free_wave_drive']-expected['schur']['free_wave_drive']) < 2e-10)
                evidence.check(key+'_source_shape_from_existing_energy',
                    abs(shape_force-expected['lift']['explicit_Gram_shape_force']) < 2e-12)
                evidence.check(key+'_scalar_projection_two_independent_forms',
                    abs(projected_variation+projection @ scalar_covector) < 2e-12
                    and abs(projected_variation-derivative) < 2e-12)
                evidence.check(key+'_conditional_Cauchy_bound', energy >= 0 and projected_energy >= 0
                    and abs(projected_variation) <= projected_bound+1e-20
                    and abs(explicit_drive) <= abs(shape_force)+projected_bound+1e-20)
                if branch == 'reference':
                    evidence.check(key+'_zero_Gram_reference_control', explicit_drive == 0)
                else:
                    evidence.check(key+'_omitted_projection_negative_control', abs(explicit_drive-shape_force) > 1e-10)
                row = dict(branch=branch, base_count=count, source_cap=cap, time=float(saved['time']),
                    force=float(-current.wave_source_euler), continuum_force=status['continuum_force'],
                    total_free_drive=schur['free_wave_drive'], explicit_Gram_shape_force=shape_force,
                    kinetic_projected_Gram_variation=projected_variation,
                    explicit_Gram_drive=explicit_drive, remaining_drive=remainder,
                    total_drive_gap=schur['free_wave_drive']-status['continuum_force'],
                    remaining_drive_gap=remainder-status['continuum_force'],
                    Gram_energy=energy, projected_Gram_energy=projected_energy,
                    projected_variation_bound=projected_bound,
                    explicit_drive_bound=abs(shape_force)+projected_bound,
                    conforming_combined_Gram_work=expected['lift']['combined_Gram_work'],
                    source_path=str(source_path.relative_to(evidence.root)), valid_for_claim=False)
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
