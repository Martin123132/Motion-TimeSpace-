from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_live_gram_stress_20260918 import GramPushforward
from annular_live_radial_response_20260918 import integration_nodes
import numpy as np


def main():
    evidence = EvidenceRun('annular-Gram-shape-L1-bound-attempt01', __file__)
    try:
        for count in [33, 129, 257]:
            system = LocallyRefinedSourceAction(count, True, background_mass=.7, source_splits=8)
            field = .004*np.sin(1.7*np.arange(system.count)+.3)
            atoms = GramPushforward(system, field)
            field *= np.sqrt(.002/atoms.weak(lambda radius: radius**2))
            atoms = GramPushforward(system, field)
            points, weights = np.polynomial.legendre.leggauss(16)
            labels, weights = points/2, weights/2
            gamma_sum = float(sum(atoms.gamma))
            amplitude = atoms.amplitudes(labels)
            amplitude_derivative = atoms.amplitude[1]+2*atoms.amplitude[2]*labels
            unweighted = gamma_sum*float(weights @ amplitude**2)
            label_derivative = gamma_sum*float(weights @ abs(2*amplitude*amplitude_derivative))
            jacobian_floor, label_floor = .9, .017
            slope = float(max(abs(atoms.jacobian_slope)))
            weight_bound, weight_derivative_bound = 1.5, 6.
            source_first_cap, source_second_cap = .027, .009
            jacobian_label_cap = slope*(source_first_cap+atoms.width)
            position_direction, derivative_direction = .525, .5
            atom_mass = weight_bound*unweighted/jacobian_floor
            atom_label_derivative = (weight_derivative_bound*unweighted+weight_bound*label_derivative)/jacobian_floor
            atom_label_derivative += weight_bound*jacobian_label_cap*unweighted/jacobian_floor**2
            bound = weight_bound*slope*unweighted*position_direction/jacobian_floor**2
            bound += position_direction*atom_label_derivative/label_floor+atom_mass*derivative_direction/label_floor
            bound += atom_mass*source_second_cap*position_direction/label_floor**2
            values = []
            for step in [.0001, .00005]:
                edges = np.unique(np.concatenate([atoms.edges(-step), atoms.edges(), atoms.edges(step)]))
                radius, measure = integration_nodes(edges, order=24)
                derivative = (atoms.density(radius, step)-atoms.density(radius, -step))/(2*step)
                norm = float(measure @ abs(derivative))
                radius_bound = 6.81**2*bound
                energy_norm = float(measure @ (radius**2*abs(derivative)))
                for parameter in [-step, 0., step]:
                    unused, spatial, label = atoms.geometry([-.5, .5], parameter)
                    evidence.check(str(count)+'_'+str(step)+'_'+str(parameter)+'_common_ordered_tube',
                        min(spatial.ravel()) > jacobian_floor and min(label.ravel()) > label_floor)
                evidence.check(str(count)+'_'+str(step)+'_density_shape_L1_bound', norm <= bound,
                    dict(norm=norm, analytic_bound=bound))
                evidence.check(str(count)+'_'+str(step)+'_canonical_energy_shape_L1_bound', energy_norm <= radius_bound)
                values.append(dict(step=step, measured_L1=norm, measured_energy_L1=energy_norm))
            row = dict(base_count=count, gamma_unweighted_L1=unweighted, gamma_label_derivative_L1=label_derivative,
                analytic_density_L1_bound=bound, analytic_energy_L1_bound=6.81**2*bound, samples=values)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
        evidence.report.update(internal_fixed_width_source_shape_tame_bound_derived=True,
            unweighted_label_Gram_and_derivative_control_required=True,
            weighted_energy_alone_not_asserted_sufficient=True,
            uniform_in_scalar_mesh_under_declared_label_bounds=True,
            uniform_in_label_resolution_proven=False, zero_width_limit_proven=False,
            no_forward_evolution=True, full_live_P2_force_convergence_proven=False,
            original_action_unchanged=True, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
