from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from interior_energy import Interior, dependencies, digest, save, modest_process


def cycle_mass(interior, radius, epsilon, frequency):
    position = np.array([radius])
    state, flow, metric_time, background = interior.fields(position)
    angular, shift, response, response_prime, phase, phase_prime = state[:, 0]/interior.master_surface
    angular_prime, shift_prime = flow[:2, 0]/interior.master_surface
    time_metric = metric_time[0]/interior.master_surface
    field, gradient, metric, lapse, metric_prime = [value[0] for value in background]
    lapse_prime = interior.problem.background(position)[8][0]
    time_metric_prime = angular_prime-2*lapse_prime*time_metric+4*interior.alpha*gradient*response
    angles, weights = leggauss(32)
    harmonic = np.sqrt(5/(16*np.pi))*(3*angles**2-1)[None, :]
    angular_derivative = (-6*np.sqrt(5/(16*np.pi))*angles*np.sqrt(1-angles**2))[None, :]
    times = (2*np.pi*np.arange(64)/64)[:, None]
    displacement = epsilon*np.cos(times)
    velocity = -epsilon*frequency*np.sin(times)
    acceleration = -epsilon*frequency**2*np.cos(times)
    spatial_radial = (1+time_metric*displacement*harmonic)/metric
    spatial_angular = radius**2*(1+angular*displacement*harmonic)
    shifted_lapse = lapse*np.sqrt(1-time_metric*displacement*harmonic)
    volume = np.sqrt(spatial_radial)*spatial_angular
    gamma_rr = -metric_prime/(2*metric)+time_metric_prime*displacement*harmonic/(2*(1+time_metric*displacement*harmonic))
    gamma_rtheta = time_metric*displacement*angular_derivative/(2*(1+time_metric*displacement*harmonic))
    gamma_thetatheta = -(2*radius*(1+angular*displacement*harmonic)+radius**2*angular_prime*displacement*harmonic)/(2*spatial_radial)
    curvature_rr = (time_metric*velocity*harmonic/metric
                    -2*(shift_prime*velocity*harmonic-gamma_rr*shift*velocity*harmonic))/(2*shifted_lapse)
    curvature_rtheta = (-shift*velocity*angular_derivative+2*gamma_rtheta*shift*velocity*harmonic)/(2*shifted_lapse)
    curvature_thetatheta = (radius**2*angular*velocity*harmonic+2*gamma_thetatheta*shift*velocity*harmonic)/(2*shifted_lapse)
    trace = curvature_rr/spatial_radial+2*curvature_thetatheta/spatial_angular
    contraction = curvature_rr**2/spatial_radial**2+2*curvature_thetatheta**2/spatial_angular**2+2*curvature_rtheta**2/(spatial_radial*spatial_angular)
    gravity = shifted_lapse*volume/(4*interior.alpha)*(contraction-trace**2)
    shifted_field = field+response*displacement*harmonic
    shifted_gradient = gradient+response_prime*displacement*harmonic
    contravariant_shift = shift*velocity*harmonic/spatial_radial
    amplitude_flow = response*velocity*harmonic-contravariant_shift*shifted_gradient
    phase_radial = -phase_prime*velocity*harmonic
    phase_angular = -phase*velocity*angular_derivative
    phase_flow_change = -phase*acceleration*harmonic-contravariant_shift*phase_radial
    matter = volume/(2*shifted_lapse)*(amplitude_flow**2+shifted_field**2*phase_flow_change*(2*interior.frequency+phase_flow_change))
    matter -= shifted_lapse*volume/2*shifted_field**2*(phase_radial**2/spatial_radial+phase_angular**2/spatial_angular)
    average = float(np.mean((gravity+matter)@(2*np.pi*weights)))
    return 4*average/(epsilon**2*frequency**2), float(np.max(abs(shifted_field/field-1)))


def main():
    modest_process()
    interior = Interior('refined')
    rows = []
    for fraction in [.15, .4, .7, .9, .97]:
        radius = fraction*interior.radius
        expected = float(sum(interior.density(np.array([radius]))[:, 0])/interior.master_surface**2)
        for epsilon in [.002, .001, .0005]:
            first, field_fraction = cycle_mass(interior, radius, epsilon, .0006)
            second, _ = cycle_mass(interior, radius, epsilon, .0012)
            extrapolated = (4*first-second)/3
            row = dict(radius_fraction=fraction, epsilon=epsilon, expected_mass_density=expected,
                       nonlinear_cycle_mass=float(extrapolated),
                       relative_error=float(extrapolated/expected-1),
                       largest_fractional_amplitude_change=field_fraction)
            rows.append(row)
            print(row, flush=True)
    inputs = dependencies()
    inputs[str(interior.archive_path)] = digest(interior.archive_path)
    inputs[str(interior.profile.path)] = digest(interior.profile.path)
    save('nonlinear-action-check', Path(__file__), dict(input_hashes=inputs, rows=rows,
        method='Full local nonlinear ADM extrinsic-curvature and scalar kinetic action; cycle average, static subtraction, two-frequency removal of the explicit acceleration-squared term.',
        nonlinear_field_equations_solved=False, independent_functional_check=True,
        quadrature=dict(angular_gauss=32, temporal_trapezoid=64), frequencies=[.0006, .0012]))


if __name__ == '__main__':
    main()

