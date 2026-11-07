from pathlib import Path

import sympy as sp

from interior_energy import dependencies, save, modest_process


def main():
    modest_process()
    radius, mass = sp.symbols('r M', positive=True)
    master, slope, slope_prime = sp.symbols('Z V Vprime', real=True)
    metric = 1-2*mass/radius

    def derivative(value):
        return sp.diff(value, radius)+sp.diff(value, master)*slope/metric+sp.diff(value, slope)*slope_prime

    angular = (6*radius**2+6*mass*radius+6*mass**2)/(radius**2*(2*radius+3*mass))*master+slope
    shift = (2*radius**2-6*mass*radius-3*mass**2)/((radius-2*mass)*(2*radius+3*mass))*master+radius*slope/metric
    shift_prime = derivative(shift)
    time_metric = metric*shift_prime+sp.diff(metric, radius)*shift-angular
    radial_rate = time_metric-2*metric*shift_prime-sp.diff(metric, radius)*shift
    angular_rate = angular-2*metric*shift/radius
    density = sp.factor(radius**2/(8*metric)*(-4*radial_rate*angular_rate-2*angular_rate**2+12*metric*shift**2/radius**2))
    boundary_base = sp.integrate(sp.diff(density, slope_prime), slope)
    remainder = sp.factor(density-derivative(boundary_base))
    mixed = sp.diff(remainder, master, slope)
    boundary = sp.factor(boundary_base+metric*mixed*master**2/2)
    reduced = sp.factor(density-derivative(boundary))
    coefficient = sp.factor(metric*reduced/master**2)
    check = sp.factor(density-derivative(boundary)-coefficient*master**2/metric)
    assert check == 0
    assert not (coefficient.free_symbols & {master, slope, slope_prime, radius, mass}), coefficient
    result = save('vacuum-canonical', Path(__file__), dict(input_hashes=dependencies(),
        canonical_normalization_times_alpha=str(coefficient),
        boundary_contact_times_alpha=str(boundary),
        density_times_alpha=str(density), residual=str(check),
        convention='ADM mass coefficient = canonical mass density + radial derivative of contact; no static wave equation used.',
        variables=['r', 'M', 'Z', 'V', 'Vprime']))
    print({key:result[key] for key in ['canonical_normalization_times_alpha', 'boundary_contact_times_alpha', 'residual']}, flush=True)


if __name__ == '__main__':
    main()

