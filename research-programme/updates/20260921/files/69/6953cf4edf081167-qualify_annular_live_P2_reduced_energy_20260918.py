from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import LiveP2System, P2Material
from annular_repaired_live_geometry_20260915 import material_weight
from annular_flat_preassembled_flow_20260916 import band_product
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-P2-reduced-energy-attempt01', __file__)
    try:
        folder = evidence.root/'source-intake/navier-stokes/20260914/annular-live-P2-canonical-attempt02'
        status_path = folder/'status.json'
        status = json.loads(status_path.read_text())
        evidence.check('canonical_snapshot_qualification_complete', status['state'] == 'complete')
        evidence.own(status_path)
        evidence.report.update(no_forward_evolution=True, constrained_mass_not_matter_energy_only=True,
            pointwise_continuum_momentum_not_substituted=True,
            finite_label_collocation_not_exact_Galerkin=True, independent_temporal_current_tested=False,
            full_live_P2_force_convergence_proven=False, github_action=False, subagents_used=False)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            source = folder/(branch+'-17-8-False.npz')
            evidence.check(branch+'_snapshot_hash', hashlib.sha256(source.read_bytes()).hexdigest() == status['outputs'][str(source.relative_to(evidence.root))])
            evidence.own(source)
            with np.load(source) as saved:
                coordinates, momenta = saved['coordinates'], saved['momenta']
            system = LiveP2System(17, gram, layer_degree=8, radial_degree=12)
            rates, geometry = system.solve(coordinates, momenta)
            material = P2Material(system, coordinates)
            nodes, weights = np.polynomial.legendre.leggauss(24)
            labels, measure = nodes/2, weights/2*material_weight(nodes/2)
            interpolation = material.interpolation(labels)
            sampled_coordinates, sampled_rates = interpolation @ coordinates, interpolation @ rates
            forces = []
            for label, position, velocity in zip(labels, sampled_coordinates, sampled_rates):
                layer = system.layer(label, geometry)
                data = layer.evaluate(0., position, velocity)
                forces.append(np.append(data['scalar_covector'], layer.source_covector(0., position, velocity)))
            forces = np.array(forces)
            directions = {}
            field_momentum = np.zeros_like(momenta)
            for index, label in enumerate(system.labels):
                layer = system.layer(label, geometry)
                data = layer.evaluate(0., coordinates[index], rates[index])
                field_momentum[index, :-1] = band_product(data['mass_bands'], .01*np.ones(system.count))
            directions['field_momentum'] = (np.zeros_like(coordinates), field_momentum)
            source_momentum = np.zeros_like(momenta)
            source_momentum[:, -1] = .001*(1+.2*system.labels)
            directions['source_momentum'] = (np.zeros_like(coordinates), source_momentum)
            field_position = np.zeros_like(coordinates)
            field_position[:, :-1] = .3*coordinates[:, :-1]
            directions['field_coordinate'] = (field_position, np.zeros_like(momenta))
            source_position = np.zeros_like(coordinates)
            source_position[:, -1] = .02*(1+.1*system.labels)
            directions['source_coordinate'] = (source_position, np.zeros_like(momenta))
            step = .001
            for name, (position_direction, momentum_direction) in directions.items():
                expected = float(measure @ np.sum(sampled_rates*(interpolation @ momentum_direction)
                    -forces*(interpolation @ position_direction), axis=1))
                energies = []
                iterations = []
                for factor in [-2, -1, 1, 2]:
                    changed_rates, changed = system.solve(coordinates+factor*step*position_direction, momenta+factor*step*momentum_direction)
                    energies.append(float(changed.mass_nodes[-1, -1]/system.coupling))
                    iterations.append(len(changed.canonical_history))
                finite = (energies[0]-8*energies[1]+8*energies[2]-energies[3])/(12*step)
                row = dict(branch=branch, direction=name, step=step, constrained_mass_derivative=finite,
                    canonical_pairing=expected, error=abs(finite-expected), maximum_canonical_iterations=max(iterations))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                evidence.check(branch+'_'+name+'_reduced_mass_gradient', row['error'] < 2e-8, row)
            refined = LiveP2System(17, gram, layer_degree=8, radial_degree=16, action_order=32, label_order=16)
            refined_rates, refined_geometry = refined.solve(coordinates, momenta)
            probes = np.linspace(5.19, 6.81, 701)
            before, after = geometry.values(probes), refined_geometry.values(probes)
            changes = dict(rates=float(max(abs(refined_rates-rates).ravel())),
                mass=float(max(abs(after[0]-before[0]))), log_lapse=float(max(abs(after[1]-before[1]))))
            evidence.check(branch+'_independent_quadrature_radial_control', max(changes.values()) < 2e-8, changes)
        evidence.report.update(momentum_mass_gradient_derived_and_qualified=True,
            coordinate_mass_gradient_tested_not_general_conservation_theorem=True,
            coupled_constraint_canonical_solve_used_in_every_perturbation=True,
            no_trajectory_or_total_mass_conservation_claim=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
