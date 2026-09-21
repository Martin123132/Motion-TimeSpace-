from derive_annular_source_gravity_20260914 import EvidenceRun
import json
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-reference-cut-cell-kinetics-attempt01', __file__)
    try:
        audit_path = evidence.root / 'source-intake/navier-stokes/20260914/annular-trace-static-force-phase-audit-attempt01/status.json'
        audit = json.loads(audit_path.read_text())
        evidence.check('static_audit_complete_not_general_force_pass', audit['state'] == 'complete'
                       and not audit['verdict']['reference_interpolated_trace']['passes_half_percent_pressure_gate'])
        evidence.own(audit_path)
        left_value, right_value, position = sp.symbols('q_left q_right b', real=True)
        left_rate, right_rate, velocity = sp.symbols('u_left u_right V', real=True)
        source_mass = sp.symbols('S', positive=True)
        fraction = sp.symbols('xi', real=True)
        left_length, right_length = position, 1-position
        left_time = (1-fraction)*left_rate + left_value*velocity*fraction/left_length
        right_time = fraction*right_rate - right_value*velocity*(1-fraction)/right_length
        kinetic_integral = sp.integrate(left_length*left_time**2/2 + right_length*right_time**2/2,
                                       (fraction, 0, 1))
        kinetic = (left_length*left_rate**2 + right_length*right_rate**2
                   + velocity*(left_value*left_rate-right_value*right_rate)
                   + velocity**2*(left_value**2/left_length+right_value**2/right_length))/6
        potential = left_value**2/(2*left_length) + right_value**2/(2*right_length)
        lagrangian = kinetic-potential-source_mass*sp.sqrt(1-velocity**2)
        coordinates = sp.Matrix([left_value, right_value, position])
        rates = sp.Matrix([left_rate, right_rate, velocity])
        momenta = sp.Matrix([sp.diff(lagrangian, entry) for entry in rates])
        inertia = momenta.jacobian(rates)
        force = sp.Matrix([sp.diff(lagrangian, entry) for entry in coordinates])-momenta.jacobian(coordinates)*rates
        energy = sp.simplify((momenta.T*rates)[0]-lagrangian)
        evidence.check('fixed_physical_radius_kinetic_integrals_exact', sp.simplify(kinetic_integral-kinetic) == 0)
        expected_momentum = (source_mass*velocity/sp.sqrt(1-velocity**2)
                             +(left_value*left_rate-right_value*right_rate)/6
                             +velocity*(left_value**2/left_length+right_value**2/right_length)/3)
        evidence.check('source_canonical_momentum_includes_cut_field_inertia',
                       sp.simplify(momenta[-1]-expected_momentum) == 0)
        schur = sp.simplify(inertia[2, 2]-inertia[0, 2]**2/inertia[0, 0]
                            -inertia[1, 2]**2/inertia[1, 1])
        expected_schur = source_mass/(1-velocity**2)**sp.Rational(3, 2)+(left_value**2/left_length+right_value**2/right_length)/4
        evidence.check('strictly_positive_velocity_schur_complement', sp.simplify(schur-expected_schur) == 0)
        evidence.check('exact_autonomous_energy',
                       sp.simplify(energy-kinetic-potential-source_mass/sp.sqrt(1-velocity**2)) == 0)
        static_force = sp.diff(lagrangian, position).subs({left_rate: 0, right_rate: 0, velocity: 0})
        evidence.check('static_shape_force_is_pressure_difference',
                       sp.simplify(static_force-left_value**2/(2*left_length**2)+right_value**2/(2*right_length**2)) == 0)
        arguments = [*coordinates, *rates, source_mass]
        evaluate_lagrangian = sp.lambdify(arguments, lagrangian, 'numpy', cse=True)
        evaluate_gradient = sp.lambdify(arguments, [sp.diff(lagrangian, entry) for entry in arguments[:-1]], 'numpy', cse=True)
        evaluate_inertia = sp.lambdify(arguments, inertia, 'numpy', cse=True)
        evaluate_force = sp.lambdify(arguments, force, 'numpy', cse=True)
        evaluate_energy = sp.lambdify(arguments, energy, 'numpy', cse=True)
        quadrature, weights = np.polynomial.legendre.leggauss(8)
        quadrature, weights = (quadrature+1)/2, weights/2

        def independent_action(state):
            left_amplitude, right_amplitude, source_position, left_speed, right_speed, source_speed, mass = state
            left_points = source_position*quadrature
            right_points = source_position+(1-source_position)*quadrature
            left_field_time = (source_position-left_points)*left_speed/source_position + left_amplitude*source_speed*left_points/source_position**2
            right_field_time = (right_points-source_position)*right_speed/(1-source_position) + right_amplitude*source_speed*(right_points-1)/(1-source_position)**2
            integral = (source_position*np.dot(weights, left_field_time**2-(left_amplitude/source_position)**2)
                        +(1-source_position)*np.dot(weights, right_field_time**2-(right_amplitude/(1-source_position))**2))/2
            return integral-mass*np.sqrt(1-source_speed**2)

        random = np.random.default_rng(20260915)
        for source_position in [.02, .2, .5, .8, .98]:
            state = np.array([*.03*random.normal(size=2), source_position,
                              *.04*random.normal(size=2), .2, .07])
            matrix = evaluate_inertia(*state)
            acceleration = np.linalg.solve(matrix, evaluate_force(*state).ravel())
            direction = np.concatenate([state[3:6], acceleration, [0.]])
            step = 1e-5
            gradient = []
            for coordinate in range(6):
                displacement = np.eye(7)[coordinate]*step
                gradient.append((-independent_action(state+2*displacement)+8*independent_action(state+displacement)
                                 -8*independent_action(state-displacement)+independent_action(state-2*displacement))/(12*step))
            gradient_error = float(np.max(abs(np.array(gradient)-evaluate_gradient(*state))))
            energy_rate = (-evaluate_energy(*(state+2*step*direction))+8*evaluate_energy(*(state+step*direction))
                           -8*evaluate_energy(*(state-step*direction))+evaluate_energy(*(state-2*step*direction)))/(12*step)
            minimum_inertia = float(np.linalg.eigvalsh(matrix).min())
            evidence.check(str(source_position)+'_independent_continuum_trial_action',
                           abs(independent_action(state)-evaluate_lagrangian(*state)) < 2e-13 and gradient_error < 2e-8)
            evidence.check(str(source_position)+'_positive_inertia_and_unprojected_energy',
                           minimum_inertia > 0 and abs(energy_rate) < 2e-8)
            evidence.report['cases'].append(dict(source_position=source_position, minimum_inertia=minimum_inertia,
                                                 action_gradient_error=gradient_error, independent_energy_rate=float(energy_rate)))
        evidence.report.update(scope='Exact restriction of a flat planar reference scalar plus a massive reflecting source to a split linear cut cell.',
                               kinetic_action=str(kinetic), source_canonical_momentum=str(expected_momentum),
                               positive_schur_complement=str(expected_schur),
                               static_reference_correction_has_derived_dynamic_inertia=True,
                               curved_time_link_and_metric_current_derived=False,
                               full_MTS_Gram_boundary_completion_derived=False,
                               evolving_cut_cell_global_waveform_qualified=False,
                               source_cell_crossing_transfer_derived=False,
                               no_interpolated_trace_multiplier_retained=True,
                               complete_parent_source_action_derived=False, full_GR_limit_proven=False,
                               valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
