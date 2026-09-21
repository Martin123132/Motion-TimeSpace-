from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import LiveP2System, inverse_momenta, wave_kinematics
from annular_repaired_live_geometry_20260915 import VacuumGeometry
from scipy.linalg import solve_banded
import numpy as np
import time


class MetricVariation:
    def __init__(self, base, parameter):
        self.base, self.parameter = base, parameter

    def metric(self, radius):
        lapse, root = self.base.metric(radius)
        lapse_direction, root_direction = directions(radius)
        return lapse*np.exp(self.parameter*lapse_direction), root*np.exp(self.parameter*root_direction)


def directions(radius):
    radius = np.asarray(radius)
    return .013*(1+.2*np.sin(radius)), .009*(1+.3*np.cos(radius))


def tangent_checks(evidence, prefix, system, coordinates, momenta, rates, geometry):
    index = len(system.labels)//2
    position, momentum, velocity = coordinates[index], momenta[index], rates[index]
    label = system.labels[index]
    layer = system.layer(label, geometry)
    data = layer.evaluate(0., position, velocity)
    recovered, inverse = inverse_momenta(layer, position, momentum)
    radius, shape, indices, motion, measure = wave_kinematics(layer, position)
    temporal = np.sum(shape*velocity[:-1][indices], axis=1)+motion*velocity[-1]
    lapse_direction, root_direction = directions(radius)
    log_speed_direction = lapse_direction+root_direction
    field_rhs = layer.assemble_quadratic(indices, shape*(measure*log_speed_direction*temporal)[:, None])
    lapse, root = layer.metric(0., position[-1])
    lapse_source, root_source = directions(position[-1])
    clock = data['clock']
    material_momentum = system.source_mass*velocity[-1]/(root**2*clock)
    material_direction = material_momentum*(-2*root_source-(lapse**2*lapse_source+velocity[-1]**2/root**2*root_source)/clock**2)
    source_rhs = measure @ (log_speed_direction*motion*temporal)-material_direction
    solved = solve_banded((2, 2), data['mass_bands'], np.column_stack([field_rhs, data['cross']]))
    source_tangent = (source_rhs-data['cross'] @ solved[:, 0])/inverse['total_schur']
    tangent = np.append(solved[:, 0]-solved[:, 1]*source_tangent, source_tangent)
    field_tangent = np.sum(shape*tangent[:-1][indices], axis=1)+motion*tangent[-1]
    kinetic_norm = np.sqrt(measure @ field_tangent**2+inverse['proper_inertia']*source_tangent**2)
    norm_bound = (.013*1.2+.009*1.3)*np.sqrt(measure @ temporal**2)+abs(material_direction)/np.sqrt(inverse['proper_inertia'])
    evidence.check(prefix+'_metric_tangent_natural_norm_bound', kinetic_norm <= norm_bound+2e-12,
        dict(norm=float(kinetic_norm), bound=float(norm_bound)))
    step = .0002
    samples, energies = [], []
    for factor in [-2, -1, 1, 2]:
        changed = system.layer(label, MetricVariation(geometry, factor*step))
        changed_rates, unused = inverse_momenta(changed, position, momentum)
        samples.append(changed_rates)
        energies.append(float(momentum @ changed_rates-changed.evaluate(0., position, changed_rates)['action']))
    finite = (samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*step)
    evidence.check(prefix+'_implicit_metric_tangent_vs_full_inverse_difference', float(max(abs(tangent-finite))) < 2e-9,
        float(max(abs(tangent-finite))))
    nodal_radius = layer.mapping(layer.radii, position[-1])[0]
    nodal_direction = sum(directions(nodal_radius))
    action_variation = data['weight'] @ (data['density_dual']*data['coefficient']*log_speed_direction)
    action_variation += data['nodal_dual'] @ (data['nodal']*nodal_direction)
    action_variation -= system.source_mass*(lapse**2*lapse_source+velocity[-1]**2/root**2*root_source)/clock
    envelope = (energies[0]-8*energies[1]+8*energies[2]-energies[3])/(12*step)
    evidence.check(prefix+'_finite_Legendre_metric_envelope_identity', abs(envelope+action_variation) < 2e-9,
        dict(hamiltonian_derivative=envelope, minus_action_derivative=float(-action_variation), error=float(abs(envelope+action_variation))))
    naive = lapse*root**2*momentum[-1]/np.sqrt(system.source_mass**2+root**2*momentum[-1]**2)
    evidence.check(prefix+'_omitted_field_source_momentum_detected', abs(naive-velocity[-1]) > 1e-6,
        dict(correct_source_rate=float(velocity[-1]), wrong_material_only_rate=float(naive)))
    evidence.check(prefix+'_projection_Schur_identity', inverse['schur_error'] < 2e-12 and inverse['field_schur'] >= 0, inverse)
    return dict(metric_tangent_error=float(max(abs(tangent-finite))), metric_norm=float(kinetic_norm),
        metric_norm_bound=float(norm_bound), metric_envelope_error=float(abs(envelope+action_variation)), **inverse)


def main():
    evidence = EvidenceRun('annular-live-P2-canonical-attempt02', __file__)
    try:
        evidence.report.update(actual_finite_P2_banded_inverse=True,
            supersedes_machine_width_radial_partition_failure='annular-live-P2-canonical-attempt01',
            coincident_edges_merged_within_32_scaled_machine_eps=True, continuum_pointwise_momentum_not_substituted=True,
            all_Gram_rows_retained=True, material_method='Chebyshev collocation; not an exact finite-label Galerkin action.',
            no_forward_evolution=True, original_stored_actions_and_data_unchanged=True,
            full_live_P2_force_convergence_proven=False, independent_temporal_current_tested=False,
            global_coupled_fixed_point_uniqueness_proven=False, github_action=False, subagents_used=False)
        configurations = [(17, 4, 12, False), (17, 8, 12, False), (17, 6, 18, True), (33, 4, 14, False)]
        for base_count, layer_degree, radial_degree, deformed in configurations:
            for gram in [False, True]:
                started = time.perf_counter()
                branch = 'MTS' if gram else 'reference'
                system = LiveP2System(base_count, gram, layer_degree, radial_degree)
                coordinates, momenta, expected, prepared = system.initial(deformed=deformed)
                rates, geometry = system.solve(coordinates, momenta)
                nodal = system.canonical_residual(coordinates, momenta, rates, geometry)
                off_grid = system.canonical_residual(coordinates, momenta, rates, geometry, True)
                radial = geometry.off_grid_residual(rates)
                difference = float(max(abs(rates-expected).ravel()))
                prefix = branch+str((base_count, layer_degree, radial_degree, deformed))
                row = dict(branch=branch, base_count=base_count, scalar_free_count=system.count, layer_degree=layer_degree,
                    radial_degree=radial_degree, deformed=deformed, action_order=20, label_order=12,
                    canonical_roundtrip=difference, nodal_momentum_error=nodal, off_grid_momentum_error=off_grid,
                    mass_radial_residual=radial[0], lapse_radial_residual=radial[1],
                    exterior_mass=float(geometry.mass_nodes[-1, -1]), source_rate=float(rates[len(system.labels)//2, -1]),
                    minimum_source_jacobian=geometry.material.minimum_jacobian,
                    minimum_spatial_jacobian=geometry.material.minimum_spatial_jacobian,
                    radial_iterations=geometry.radial_iterations, canonical_history=geometry.canonical_history,
                    seconds=time.perf_counter()-started)
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                evidence.check(prefix+'_finite_canonical_roundtrip', difference < 2e-10 and nodal < 2e-10, row)
                evidence.check(prefix+'_independent_radial_equations', max(radial) < 2e-7, radial)
                evidence.check(prefix+'_nonzero_live_load_and_ordered_map', row['exterior_mass'] > .7001
                    and min(row['minimum_source_jacobian'], row['minimum_spatial_jacobian']) > 0)
                if base_count == 17 and layer_degree == 4:
                    row['tangent'] = tangent_checks(evidence, prefix, system, coordinates, momenta, rates, geometry)
                    frozen = np.array([inverse_momenta(system.layer(label, VacuumGeometry(.7)), position, momentum)[0]
                        for label, position, momentum in zip(system.labels, coordinates, momenta)])
                    wrong = system.canonical_residual(coordinates, momenta, frozen, geometry)
                    evidence.check(prefix+'_frozen_metric_inverse_is_detectably_wrong', wrong > 1e-8, wrong)
                output = evidence.output/(branch+'-'+str(base_count)+'-'+str(layer_degree)+'-'+str(deformed)+'.npz')
                np.savez_compressed(output, coordinates=coordinates, momenta=momenta, rates=rates,
                    radial_nodes=geometry.nodes, mass=geometry.mass_nodes, log_lapse=geometry.log_lapse_nodes)
                evidence.own(output, 'outputs')
                evidence.save()
        for branch in ['reference', 'MTS']:
            rows = [row for row in evidence.report['cases'] if row['branch'] == branch and row['base_count'] == 17 and not row['deformed']]
            evidence.check(branch+'_off_grid_label_refinement', rows[1]['off_grid_momentum_error'] < 2e-9
                and rows[1]['off_grid_momentum_error'] <= max(rows[0]['off_grid_momentum_error']*.3, 2e-12), rows)
        dust = []
        for gram in [False, True]:
            system = LiveP2System(17, gram)
            coordinates, momenta, expected, unused = system.initial(wave=False)
            rates, geometry = system.solve(coordinates, momenta)
            dust.append((rates, geometry.mass_nodes, geometry.log_lapse_nodes))
        evidence.check('reference_MTS_zero_wave_identity', all(np.array_equal(first, second) for first, second in zip(*dust)))
        system = LiveP2System(17, True, coupling=0.)
        coordinates, momenta, expected, unused = system.initial()
        rates, geometry = system.solve(coordinates, momenta)
        lapse, root = geometry.metric(geometry.nodes.ravel())
        vacuum = np.sqrt(1-1.4/geometry.nodes.ravel())
        evidence.check('zero_coupling_recovers_Schwarzschild_not_flat_space', max(float(max(abs(lapse-vacuum))),
            float(max(abs(root-vacuum))), float(max(abs(rates-expected).ravel()))) < 2e-10)
        evidence.report.update(coupled_live_P2_canonical_snapshots_solved=True, metric_tangent_derived_and_qualified=True,
            finite_metric_Legendre_envelope_qualified=True, natural_norm_bound_not_inverse_mesh_estimate=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
