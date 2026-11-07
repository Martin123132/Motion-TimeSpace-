from __future__ import annotations

from datetime import datetime, timezone
import sympy as sp

from carrier import ROOT, PRIOR, digest, write_json, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        residual = sp.factor(sp.cancel(expression))
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, passed=True, residual=str(residual)))

    semilatus, mass = sp.symbols('p M', positive=True)
    eccentricity, cosine = sp.symbols('e c', real=True)
    time_rate = mass*semilatus**2*sp.sqrt((semilatus-2)**2-4*eccentricity**2)/(
        (semilatus-2-2*eccentricity*cosine)*(1+eccentricity*cosine)**2*sp.sqrt(semilatus-6-2*eccentricity*cosine))
    phase_rate = sp.sqrt(semilatus/(semilatus-6-2*eccentricity*cosine))
    time_linear = 2/(semilatus-2)-2+1/(semilatus-6)
    time_constant = -2/(semilatus-2)**2
    time_cosine = (4/(semilatus-2)**2+3+sp.Rational(3, 2)/(semilatus-6)**2-4/(semilatus-2)
                   +2/((semilatus-2)*(semilatus-6))-2/(semilatus-6))
    time_mean = time_constant+time_cosine/2
    phase_mean = sp.Rational(3, 4)/(semilatus-6)**2
    alpha_phi = sp.factor(phase_mean-time_mean)
    exact('Darwin time second variation', sp.diff(time_rate, eccentricity, 2).subs(eccentricity, 0)/(2*time_rate.subs(eccentricity, 0))-time_constant-time_cosine*cosine**2)
    exact('Darwin phase second variation', sp.diff(phase_rate, eccentricity, 2).subs(eccentricity, 0)/(2*phase_rate.subs(eccentricity, 0))-2*phase_mean*cosine**2)
    exact('Newtonian angular clock correction', sp.limit(alpha_phi, semilatus, sp.oo)+sp.Rational(3, 2))
    energy = sp.sqrt(((semilatus-2)**2-4*eccentricity**2)/(semilatus*(semilatus-3-eccentricity**2)))
    angular = mass*semilatus/sp.sqrt(semilatus-3-eccentricity**2)
    energy_second = energy.subs(eccentricity, 0)*(1/(2*(semilatus-3))-2/(semilatus-2)**2)
    angular_second = angular.subs(eccentricity, 0)/(2*(semilatus-3))
    exact('specific energy second variation', sp.diff(energy, eccentricity, 2).subs(eccentricity, 0)/2-energy_second)
    exact('specific angular action second variation', sp.diff(angular, eccentricity, 2).subs(eccentricity, 0)/2-angular_second)

    anomaly = sp.symbols('chi', real=True)
    orbit_radius, radial_frequency, azimuth, wobble, weight_linear, weight_cosine, phase_second = sp.symbols('r0 wr m k a b d', real=True)
    base, radial, radial_second, velocity, velocity_second, mixed, energy_term, angular_term = sp.symbols('T Tr Trr Tv Tvv Trv Eterm hterm')
    cosine, sine = sp.cos(anomaly), sp.sin(anomaly)
    radius_first = -orbit_radius*cosine
    radius_second = orbit_radius*cosine**2
    velocity_first = orbit_radius*radial_frequency*sine
    velocity_second_orbit = -(2+weight_linear)*orbit_radius*radial_frequency*sine*cosine
    first = radius_first*radial+velocity_first*velocity
    second = radius_second*radial+velocity_second_orbit*velocity+radius_first**2*radial_second/2
    second += velocity_first**2*velocity_second/2+radius_first*velocity_first*mixed+energy_term+angular_term
    weight_first = weight_linear*cosine-sp.I*azimuth*wobble*sine
    weight_second = weight_cosine*(cosine**2-sp.Rational(1, 2))+sp.I*phase_second*sp.sin(2*anomaly)
    weight_second -= azimuth**2*wobble**2*sine**2/2+sp.I*azimuth*wobble*weight_linear*sine*cosine
    averaged = sp.integrate(sp.expand(second+weight_first*first+weight_second*base), (anomaly, 0, 2*sp.pi))/(2*sp.pi)
    expected = (energy_term+angular_term+orbit_radius*(1-weight_linear)*radial/2+orbit_radius**2*radial_second/4
                +orbit_radius**2*radial_frequency**2*velocity_second/4-sp.I*azimuth*wobble*orbit_radius*radial_frequency*velocity/2
                -azimuth**2*wobble**2*base/4)
    exact('general normalized second-order carrier average', averaged-expected)
    exact('normalized anomaly weight', sp.integrate(weight_cosine*(cosine**2-sp.Rational(1, 2)), (anomaly, 0, 2*sp.pi)))
    newtonian_quad = expected.subs({energy_term:0, angular_term:0, weight_linear:-2, azimuth:2, wobble:2,
                                   base:orbit_radius**2, radial:2*orbit_radius, radial_second:2, velocity:0, velocity_second:0})
    exact('Newtonian carrier STF coefficient', newtonian_quad+orbit_radius**2/2)
    power_second = -10+sp.Rational(729, 64)+sp.Rational(9, 64)+sp.Rational(1, 96)
    angular_second_flux = -10+sp.Rational(3, 2)+sp.Rational(2, 3)*sp.Rational(729, 64)+2*sp.Rational(9, 64)
    exact('Newtonian energy flux coefficient at fixed p', power_second-sp.Rational(37, 24))
    exact('Newtonian shrinkage coefficient at fixed p', angular_second_flux+sp.Rational(5, 8))
    initial = sp.symbols('pi', positive=True)
    clock_primitive = sp.Rational(75, 11008)/initial**sp.Rational(19, 6)*(initial**sp.Rational(43, 6)-semilatus**sp.Rational(43, 6))
    phase_primitive = sp.Rational(105, 8704)/initial**sp.Rational(19, 6)*(semilatus**sp.Rational(17, 3)-initial**sp.Rational(17, 3))
    exact('postcircular Newtonian time primitive', sp.diff(clock_primitive, semilatus)+sp.Rational(25, 512)*semilatus**3*(semilatus/initial)**sp.Rational(19, 6))
    exact('postcircular Newtonian phase primitive', sp.diff(phase_primitive, semilatus)-sp.Rational(35, 512)*semilatus**sp.Rational(3, 2)*(semilatus/initial)**sp.Rational(19, 6))
    angular_slope, angular_cross, angular_z, base_shrink, gamma, correction, flux_second = sp.symbols('hp hpz hz P0 Gamma P2 L2', nonzero=True)
    derived = (-flux_second-angular_cross*base_shrink-angular_z*gamma)/angular_slope
    exact('P2 from angular action balance', angular_slope*derived+angular_cross*base_shrink+angular_z*gamma+flux_second)
    directory = ROOT/'results/derivation'
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory/'status.json', dict(state='complete', script_sha256=digest(__file__),
          time_utc=datetime.now(timezone.utc).isoformat(), input_hashes={str(PRIOR/'results/stage-integrity.json'):digest(PRIOR/'results/stage-integrity.json')},
          checks=checks, angular_frequency_fraction=str(alpha_phi), time_mean=str(sp.factor(time_mean)),
          carrier_average=str(expected), newtonian_clock_coefficient=str(clock_primitive), newtonian_phase_coefficient=str(phase_primitive),
          domain='fixed p, p>6, small e; carrier average at fixed frequency followed by frequency-response derivative'), exclusive=True)
    print(len(checks), 'exact checks passed', flush=True)


if __name__ == '__main__':
    main()

