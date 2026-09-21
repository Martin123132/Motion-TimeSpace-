from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_fitted_action_20260915 import SourceFittedAction
from verify_annular_source_fitted_action_20260915 import manufactured
from scipy.optimize import brentq
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-source-fitted-live-pullback-attempt01', __file__)
    try:
        reference, anchor, width, label, displacement = sp.symbols('r bstar w z k', real=True)
        source = sp.Function('b')(label)
        location = reference+displacement*(source-anchor)+(1-displacement)*width*label
        evidence.check('every_node_label_Jacobian_derived', sp.simplify(sp.diff(location, label)-((1-displacement)*width+displacement*sp.diff(source, label))) == 0)
        evidence.check('source_label_and_boundary_Jacobians_recovered', sp.diff(location, label).subs(displacement, 1) == sp.diff(source, label)
                       and sp.diff(location, label).subs(displacement, 0) == width)
        lapse, root, radius, jacobian, momentum, radial, velocity, mesh_factor = sp.symbols('N U R J Pi Href V k', positive=True)
        temporal = sp.symbols('W', real=True)
        action = (radius**2/(lapse*root)*jacobian*temporal**2-radius**2*lapse*root*radial**2/jacobian)/2
        density = (temporal**2/(lapse**2*root**2)+(radial/jacobian)**2)/2
        evidence.check('lapse_variation_is_physical_density_times_pullback_measure', sp.simplify(sp.diff(action, lapse)+jacobian*radius**2*root*density) == 0)
        evidence.check('radial_metric_variation_is_physical_density_times_pullback_measure', sp.simplify(sp.diff(action, root)+jacobian*radius**2*lapse*density) == 0)
        pulled_rate = momentum*lapse*root/(jacobian*radius**2)+mesh_factor*velocity*radial/jacobian
        physical_time = pulled_rate-mesh_factor*velocity*radial/jacobian
        zeta = -radius**2/(lapse*root)*mesh_factor*radial*physical_time
        evidence.check('continuum_source_momentum_shift_metric_independent', sp.simplify(zeta+mesh_factor*radial*momentum/jacobian) == 0)
        system = SourceFittedAction(33, True, background_mass=.7)
        coordinates, rates = manufactured(system, .12, 6.05)
        data = system.evaluate(.12, coordinates, rates)
        analytic = np.append(data['scalar_covector'], system.source_covector(.12, coordinates, rates))
        direction = np.sin(np.arange(system.count+1)+.3)
        direction[-1] = .4
        step = 2e-5
        sample = [system.evaluate(.12, coordinates+multiple*step*direction, rates)['action'] for multiple in [-2, -1, 1, 2]]
        derivative = (sample[0]-8*sample[1]+8*sample[2]-sample[3])/(12*step)
        evidence.check('independent_real_action_coordinate_difference', abs(derivative-analytic @ direction) < 2e-10, float(abs(derivative-analytic @ direction)))
        sample = [system.evaluate(.12, coordinates, rates+multiple*step*direction)['action'] for multiple in [-2, -1, 1, 2]]
        derivative = (sample[0]-8*sample[1]+8*sample[2]-sample[3])/(12*step)
        evidence.check('independent_real_action_velocity_difference', abs(derivative-data['momenta'] @ direction) < 2e-10, float(abs(derivative-data['momenta'] @ direction)))
        scalar = .012*(system.radii-system.anchor)*np.exp(-((system.radii-system.anchor)/.3)**2)
        factors, unused, unused2 = system.gram_data(system.anchor, scalar)
        gamma = np.asarray(system.sampling.T @ factors**2)/(2*system.spacing)
        unused, unused2, mesh_factors = system.mapping(system.radii, system.anchor)
        points, weights = np.polynomial.legendre.leggauss(48)
        labels, label_weights = points/2, weights/2
        material_weights = 6*(labels+.5)*(.5-labels)

        def position(offset, instant=0.):
            return system.anchor+.02+.022*offset+.004*offset**2+instant*(.06+.004*offset)

        def node_data(index, offset, instant=0.):
            mesh_factor = mesh_factors[index]
            physical = system.radii[index]+mesh_factor*(position(offset, instant)-system.anchor)+(1-mesh_factor)*.02*offset
            label_jacobian = (1-mesh_factor)*.02+mesh_factor*(.022+.008*offset+.004*instant)
            jacobian = 1+(position(offset, instant)-system.anchor-.02*offset)/(system.anchor-system.radii[0]) if system.radii[index] < system.anchor else 1-(position(offset, instant)-system.anchor-.02*offset)/(system.radii[-1]-system.anchor)
            coefficient = gamma[index]*(1+.15*offset+.03*instant)**2/jacobian
            return physical, label_jacobian, coefficient

        pullback_moments, physical_moments, wrong_moments = [], [], []
        for power in [0, 1, 2]:
            pulled_total, physical_total, wrong_total = 0., 0., 0.
            for index in range(system.count):
                physical, unused, coefficient = node_data(index, labels)
                pulled_total += np.dot(label_weights*material_weights, coefficient*physical**power)
                lower, unused, unused2 = node_data(index, -.5)
                upper, unused, unused2 = node_data(index, .5)
                targets = (lower+upper)/2+(upper-lower)*points/2
                inverse = np.array([brentq(lambda offset: node_data(index, offset)[0]-target, -.5, .5, xtol=5e-15) for target in targets])
                physical, label_jacobian, coefficient = node_data(index, inverse)
                material = 6*(inverse+.5)*(.5-inverse)
                physical_total += np.dot(weights*(upper-lower)/2, material*coefficient/label_jacobian*physical**power)
                wrong_total += np.dot(weights*(upper-lower)/2, material*coefficient/.02*physical**power)
            pullback_moments.append(float(pulled_total))
            physical_moments.append(float(physical_total))
            wrong_moments.append(float(wrong_total))
        errors = abs(np.array(pullback_moments)-physical_moments)/np.maximum(abs(np.array(pullback_moments)), 1e-30)
        wrong_errors = abs(np.array(pullback_moments)-wrong_moments)/np.maximum(abs(np.array(pullback_moments)), 1e-30)
        evidence.check('inverse_pushforward_Gram_density_matches_three_weak_moments', max(errors) < 2e-10, errors.tolist())
        evidence.check('old_constant_width_Jacobian_is_detectably_wrong', min(wrong_errors) > .001, wrong_errors.tolist())
        instant_step = 2e-5
        def moment(instant):
            total = 0.
            for index in range(system.count):
                physical, unused, coefficient = node_data(index, labels, instant)
                total += np.dot(label_weights*material_weights, coefficient*np.sin(physical))
            return total
        samples = [moment(multiple*instant_step) for multiple in [-2, -1, 1, 2]]
        direct_time = (samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*instant_step)
        transport, local_rate = 0., 0.
        for index in range(system.count):
            physical, unused, coefficient = node_data(index, labels)
            unused, unused2, complex_coefficient = node_data(index, labels, 1e-24j)
            coefficient_dot = complex_coefficient.imag/1e-24
            speed = mesh_factors[index]*(.06+.004*labels)
            local_rate += np.dot(label_weights*material_weights, coefficient_dot*np.sin(physical))
            transport += np.dot(label_weights*material_weights, coefficient*speed*np.cos(physical))
        evidence.check('moving_Gram_atoms_weak_transport_law', abs(direct_time-local_rate-transport) < 2e-12, float(abs(direct_time-local_rate-transport)))
        evidence.check('omitting_whole_mesh_atom_transport_fails', abs(direct_time-local_rate) > 1e-9, float(abs(direct_time-local_rate)))
        evidence.report.update(scope='Exact continuum pullback, finite-atom pushforward and measure variation; not an evolved live-geometry implementation.',
            mesh_label_Jacobian='(1-k_i)*width+k_i*db/dz',
            Gram_dual='sum_i weight(z_i)*gamma_i(z_i)/(J_i(z_i)*dR_i/dz)',
            parent_source_action_uniquely_derived=False, live_source_fitted_geometry_qualified=False,
            label_ordering_implies_mesh_ordering=True, all_Gram_rows_retained=True,
            continuum_momentum_shift_is_not_finite_mass_matrix_identity=True,
            weak_pushforward_moments=pullback_moments, weak_physical_moments=physical_moments,
            wrong_old_Jacobian_relative_errors=wrong_errors.tolist(),
            full_Einstein_mass_current_not_yet_qualified=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
