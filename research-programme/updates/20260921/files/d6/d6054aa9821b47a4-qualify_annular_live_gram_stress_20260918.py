from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_cut_initial_data_20260915 import compatible_initial_state
from annular_live_gram_stress_20260918 import GramPushforward, metric, coefficient, coefficient_radial
from annular_live_radial_response_20260918 import integration_nodes
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-live-P2-Gram-stress-attempt01', __file__)
    try:
        radius, lapse, root, jacobian, gamma, displacement, slope = sp.symbols('R N U J gamma k kr', positive=True)
        atom_action = -gamma*radius**2*lapse*root/jacobian
        rho = -root*sp.diff(atom_action, lapse)/radius**2
        pressure = -root**2*sp.diff(atom_action, root)/(lapse*radius**2)
        evidence.check('independent_lapse_and_radial_metric_variations_agree', sp.simplify(rho-pressure) == 0)
        evidence.check('positive_Gram_energy_density', sp.simplify(rho-root**2*gamma/jacobian) == 0)
        spatial_coefficient, spatial_derivative = sp.symbols('C CR', real=True)
        pulled_energy = gamma*spatial_coefficient/jacobian
        shape_derivative = sp.diff(pulled_energy, spatial_coefficient)*spatial_derivative*displacement+sp.diff(pulled_energy, jacobian)*slope
        evidence.check('source_shape_derivative_retains_both_terms', sp.simplify(shape_derivative
            -gamma*(displacement*spatial_derivative/jacobian-spatial_coefficient*slope/jacobian**2)) == 0)
        evidence.report.update(actual_retained_P2_Gram_stress_derived=True, arbitrary_parent_MTS_stress_derived=False,
            continuous_label_average=True, source_shift_current_fully_derived=False,
            no_forward_evolution=True, full_live_P2_force_convergence_proven=False,
            reference_and_MTS_action_difference_used=True, all_Gram_rows_retained=True,
            original_action_unchanged=True, original_initial_data_unchanged=True,
            test_fields_not_new_physical_initial_conditions=True, github_action=False, subagents_used=False)
        for count in [33, 129, 257]:
            system = LocallyRefinedSourceAction(count, True, order=10, background_mass=.7, source_splits=8)
            reference = LocallyRefinedSourceAction(count, False, order=10, background_mass=.7, source_splits=8)
            evidence.check(str(count)+'_same_reference_and_MTS_chart', np.array_equal(system.radii, reference.radii)
                and np.all(system.sampling.data >= 0) and system.sampling.shape[0] == system.original.shape[0])
            smooth = compatible_initial_state(system, 0.)[0][:-1]
            oscillatory = .004*np.sin(1.7*np.arange(system.count)+.3)
            for name, field in [('original_profile', smooth), ('oscillatory_control', oscillatory)]:
                atoms = GramPushforward(system, field)
                if name == 'oscillatory_control':
                    field = field*np.sqrt(.002/atoms.weak(lambda radius: radius**2))
                    atoms = GramPushforward(system, field)
                prefix = str(count)+'_'+name
                position = system.anchor+.035
                coordinates = np.append(field, position).astype(complex)
                rates = np.append(.002*np.sin(system.radii), .037).astype(complex)

                def difference(nvalue=0., uvalue=0., moved=0., direction=None):
                    def varied_metric(instant, radius):
                        lapse, root = metric(radius)
                        probe = .5+.2*np.cos(1.7*radius)
                        return lapse*np.exp(nvalue*probe), root*np.exp(uvalue*probe)
                    system.metric = varied_metric
                    reference.metric = varied_metric
                    varied = coordinates.copy()
                    varied[-1] += moved
                    if direction is not None:
                        varied[:-1] += direction
                    return system.evaluate(0., varied, rates)['action']-reference.evaluate(0., varied, rates)['action']

                nodal_radius, nodal_jacobian, nodal_displacement = system.mapping(system.radii, position)
                full_gamma = np.asarray(system.sampling.T @ (system.lifted @ field)**2)/(2*system.gram_spacing)
                direct = -np.sum(full_gamma*coefficient(nodal_radius)/nodal_jacobian)
                evidence.check(prefix+'_exact_original_action_isolation', abs(difference()-direct) < 2e-12, float(abs(difference()-direct)))
                expected_log_metric = -np.sum(full_gamma*coefficient(nodal_radius)/nodal_jacobian*(.5+.2*np.cos(1.7*nodal_radius)))
                complex_step = 1e-24
                lapse_variation = difference(nvalue=1j*complex_step).imag/complex_step
                root_variation = difference(uvalue=1j*complex_step).imag/complex_step
                metric_error = max(abs(lapse_variation-expected_log_metric), abs(root_variation-expected_log_metric))
                evidence.check(prefix+'_independent_metric_variations_of_existing_action', metric_error < 2e-11,
                    dict(lapse=float(lapse_variation), root=float(root_variation), expected=float(expected_log_metric), error=float(metric_error)))
                step = .0002
                real_values = [difference(nvalue=factor*step).real for factor in [-2, -1, 1, 2]]
                real_derivative = (real_values[0]-8*real_values[1]+8*real_values[2]-real_values[3])/(12*step)
                evidence.check(prefix+'_independent_real_metric_difference', abs(real_derivative-expected_log_metric) < 2e-8)
                jacobian_slope = np.where(system.radii < system.anchor,
                    1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))
                source_force = -np.sum(full_gamma*(nodal_displacement*coefficient_radial(nodal_radius)/nodal_jacobian
                    -coefficient(nodal_radius)*jacobian_slope/nodal_jacobian**2))
                source_numeric = difference(moved=1j*complex_step).imag/complex_step
                evidence.check(prefix+'_source_shape_matches_original_action', abs(source_numeric-source_force) < 2e-11,
                    dict(force=float(source_force), error=float(abs(source_numeric-source_force))))
                direction = .003*np.cos(2.3*system.radii)
                weights = system.sampling @ (coefficient(nodal_radius)/nodal_jacobian)
                field_covector = -system.lifted.T @ (weights*(system.lifted @ field)/system.gram_spacing)
                field_numeric = difference(direction=1j*complex_step*direction).imag/complex_step
                evidence.check(prefix+'_full_retained_Gram_field_covector', abs(field_numeric-field_covector @ direction) < 2e-11)
                difference()
                momentum_difference = system.evaluate(0., coordinates, rates)['momenta']-reference.evaluate(0., coordinates, rates)['momenta']
                evidence.check(prefix+'_Gram_adds_no_velocity_momentum', float(max(abs(momentum_difference))) < 2e-13)
                physical_radius, physical_measure = integration_nodes(atoms.edges(), order=16)
                physical_density = atoms.density(physical_radius)
                tests = [(lambda radius: np.ones_like(radius), lambda radius: np.zeros_like(radius)),
                    (lambda radius: radius, lambda radius: np.ones_like(radius)),
                    (lambda radius: radius**2, lambda radius: 2*radius),
                    (lambda radius: np.sin(1.7*radius), lambda radius: 1.7*np.cos(1.7*radius))]
                weak_errors, shape_errors = [], []
                for index, (test, test_radial) in enumerate(tests):
                    pulled = atoms.weak(test)
                    pushed = physical_measure @ (physical_density*test(physical_radius))
                    error = float(abs(pulled-pushed)/max(abs(pulled), 1e-20))
                    weak_errors.append(error)
                    evidence.check(prefix+'_physical_pushforward_'+str(index), error < 3e-9, error)
                    shape, transport, dilation = atoms.shape_derivative(test, test_radial)
                    shifted = []
                    for factor in [-2, -1, 1, 2]:
                        moved = factor*step
                        nodes, measure = integration_nodes(atoms.edges(moved), order=16)
                        shifted.append(measure @ (atoms.density(nodes, moved)*test(nodes)))
                    finite = (shifted[0]-8*shifted[1]+8*shifted[2]-shifted[3])/(12*step)
                    shape_error = float(abs(finite-shape)/max(atoms.weak(lambda radius: np.ones_like(radius)), 1e-20))
                    shape_errors.append(shape_error)
                    evidence.check(prefix+'_physical_source_shape_'+str(index), shape_error < 3e-7, shape_error)
                wrong = physical_measure @ (atoms.density(physical_radius, wrong_label_jacobian=True)*physical_radius**2)
                energy = float(atoms.weak(lambda radius: radius**2))
                wrong_relative = abs(wrong-energy)/energy
                evidence.check(prefix+'_wrong_constant_width_detected', wrong_relative > .001, float(wrong_relative))
                test = lambda radius: np.sin(1.7*radius)
                test_radial = lambda radius: 1.7*np.cos(1.7*radius)
                shape, transport, dilation = atoms.shape_derivative(test, test_radial)
                amplitude_rate = np.array([.07, -.03, .02])
                points, label_weights = np.polynomial.legendre.leggauss(48)
                labels, label_weights = points/2, label_weights/2
                radius, jacobian, unused = atoms.geometry(labels)
                amplitude_work = np.sum(label_weights[:, None]*6*(labels[:, None]+.5)*(.5-labels[:, None])
                    *2*atoms.gamma[None, :]*atoms.amplitudes(labels)[:, None]
                    *np.polynomial.polynomial.polyval(labels, amplitude_rate)[:, None]*test(radius)/jacobian)
                samples = []
                for factor in [-2, -1, 1, 2]:
                    moved = factor*step
                    current = GramPushforward(system, field, atoms.material+moved*atoms.direction,
                        atoms.amplitude+moved*amplitude_rate)
                    samples.append(current.weak(test))
                finite = (samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*step)
                transport_error = abs(finite-amplitude_work-transport-dilation)/max(energy, 1e-20)
                evidence.check(prefix+'_full_weak_transport_with_factor_work', transport_error < 2e-8, float(transport_error))
                evidence.check(prefix+'_dropping_atom_transport_detected', abs(transport)/energy > 1e-5)
                force, unused, unused2 = atoms.shape_derivative(coefficient, coefficient_radial)
                potential = float(atoms.weak(coefficient))
                map_radius, map_jacobian, map_label = atoms.geometry([-.5, 0., .5])
                radius_floor, jacobian_floor = 5.19, .9
                coefficient_log_bound = 2/radius_floor+1.4/(radius_floor**2*.5)+.013+.0042
                bound = .525*(coefficient_log_bound+max(abs(atoms.jacobian_slope))/jacobian_floor)*potential
                evidence.check(prefix+'_mesh_independent_shape_force_bound', abs(force) <= bound and min(map_jacobian.ravel()) > jacobian_floor)
                row = dict(base_count=count, profile=name, gram_rows=system.lifted.shape[0], atom_count=len(atoms.nodes),
                    canonical_Gram_loading=energy, prescribed_Gram_energy=potential,
                    source_shape_force=-force, force_bound=bound, metric_variation_error=float(metric_error),
                    weak_relative_error=max(weak_errors), shape_scaled_error=max(shape_errors),
                    incorrect_width_relative_error=float(wrong_relative), minimum_label_jacobian=float(min(map_label.ravel())),
                    minimum_spatial_jacobian=float(min(map_jacobian.ravel())))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
        evidence.report.update(Gram_rho_equals_radial_pressure=True,
            scalar_metric_cancellation_preserved_by_actual_Gram=True,
            full_four_dimensional_parent_covariance_derived=False,
            finite_mesh_Gram_vanishing_not_physical_coupling_decoupling=True,
            physical_source_width_fixed=.02, moving_material_map_tested=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
