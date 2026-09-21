from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
import sympy as sp
import numpy as np


def derivative(values, step):
    return (values[0]-8*values[1]+8*values[2]-values[3])/(12*step)


def onset(system, state, step):
    flow, geometry, data = system.rhs_with_geometry(state)
    source = geometry.material.source
    position = source[:, 0]
    lapse, root = geometry.metric(position)
    speed = lapse*root
    velocity = data['velocity']
    ratio = velocity/speed
    fixed_speed, velocities, forces = [], [], []
    for multiple in [-2, -1, 1, 2]:
        unused, adjacent, adjacent_data = system.rhs_with_geometry(state+multiple*step*flow)
        adjacent_lapse, adjacent_root = adjacent.metric(position)
        fixed_speed.append(adjacent_lapse*adjacent_root)
        velocities.append(adjacent_data['velocity'])
        forces.append(adjacent_data['radiation'])
    speed_time = derivative(np.array(fixed_speed), step)
    acceleration = derivative(np.array(velocities), step)
    measured = derivative(np.array(forces), step)
    mass_radial, log_lapse_radial = geometry.gradients(position)
    mass = geometry.evaluate(position, geometry.mass_coefficients)
    speed_radial = speed*(log_lapse_radial+(mass/position**2-mass_radial/position)/root**2)
    mismatch = acceleration+2*speed**2/position+speed*speed_radial-velocity*speed_time/speed
    expected = -2*position**2*.01**2*mismatch
    ratio_derivative = acceleration/speed-ratio*(speed_time+velocity*speed_radial)/speed
    field_flow, unused = system.unpack(flow)
    left_derivative = -(field_flow[:, 0, 1, -1]+.01*ratio_derivative)/(1+ratio)
    right_derivative = (field_flow[:, 1, 0, 0]+.01*ratio_derivative)/(1-ratio)
    discrete_expected = position**2*speed*(1-ratio**2)*.01*(left_derivative-right_derivative)
    return dict(step=step, initial_force=float(np.max(abs(data['radiation']))),
        compatibility_mismatch=mismatch.tolist(), coordinate_acceleration=acceleration.tolist(),
        fixed_radius_speed_time_derivative=speed_time.tolist(),
        force_slope_measured=measured.tolist(), affine_law_slope=expected.tolist(),
        discrete_outgoing_characteristic_slope=discrete_expected.tolist(),
        affine_law_absolute_error=float(np.max(abs(measured-expected))),
        affine_law_relative_error=float(np.max(abs(measured-expected))/np.max(abs(expected))),
        exact_discrete_characteristic_error=float(np.max(abs(measured-discrete_expected))))


def main():
    evidence = EvidenceRun('annular-initial-force-onset-attempt01', __file__)
    try:
        radius, speed, velocity, acceleration, speed_radial, speed_time, gradient = sp.symbols('R s V a s_R s_t H', nonzero=True, real=True)
        ratio = velocity/speed
        ratio_rate = acceleration/speed-ratio*(speed_time+velocity*speed_radial)/speed
        outgoing_rate = gradient*((1+ratio**2)*speed_radial+2*speed/radius)
        left_rate = -(outgoing_rate+gradient*ratio_rate)/(1+ratio)
        right_rate = (outgoing_rate+gradient*ratio_rate)/(1-ratio)
        pressure_rate = radius**2*speed*(1-ratio**2)*gradient*(left_rate-right_rate)
        mismatch = acceleration+2*speed**2/radius+speed*speed_radial-velocity*speed_time/speed
        evidence.check('two_characteristic_pressure_onset_identity', sp.factor(pressure_rate+2*radius**2*gradient**2*mismatch) == 0)
        wave_time_time = -velocity*gradient*speed_time/speed+(2*speed**2/radius+speed*speed_radial)*gradient
        evidence.check('second_trace_compatibility_residual', sp.factor(wave_time_time+acceleration*gradient-gradient*mismatch) == 0)
        evidence.check('compatible_affine_preparation_removes_linear_onset', sp.factor(pressure_rate.subs(acceleration, -2*speed**2/radius-speed*speed_radial+velocity*speed_time/speed)) == 0)
        for degree, folder in [(384, 'annular-live-continuum-refinement-attempt02'), (512, 'annular-live-continuum-degree512-attempt01')]:
            path = evidence.output.parent/folder/f'degree{degree}.npz'
            evidence.own(path)
            state = np.load(path)['states'][0]
            system = BarycentricLiveContinuum(degree, 8, 18, radial_spacing=.025, label_order=12)
            row = onset(system, state, 2e-5)
            row['degree'] = degree
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
            evidence.check(str(degree)+'_outgoing_characteristics_match_independent_force_derivative', row['exact_discrete_characteristic_error'] < 2e-8, row)
            evidence.check(str(degree)+'_initial_pressure_equal_but_second_compatibility_nonzero', row['initial_force'] < 1e-12
                and min(abs(value) for value in row['compatibility_mismatch']) > .01, row)
        refined = onset(system, state, 1e-5)
        difference = np.max(abs(np.array(refined['force_slope_measured'])-np.array(evidence.report['cases'][-1]['force_slope_measured'])))
        evidence.report['difference_step_control'] = refined
        evidence.check('force_onset_difference_step_control', difference < 2e-8, float(difference))
        evidence.check('analytic_affine_onset_agrees_with_resolved_oracle', refined['affine_law_relative_error'] < .01, refined)
        evidence.report.update(initial_force_onset_derived_from_wave_and_source_equations=True,
            second_trace_incompatibility_diagnosed_not_initial_data_replaced=True,
            law_is_one_sided_initial_time_slope_not_full_time_fit=True,
            result_explains_shared_benchmark_transient_not_MTS_observational_prediction=True,
            full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
