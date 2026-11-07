from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    radius, mass, velocity, angular_speed, strength = sp.symbols('r M v Omega A', nonzero=True)
    azimuth, frequency = sp.symbols('m omega', real=True)
    metric = 1-2*mass/radius
    metric_prime = sp.diff(metric, radius)
    small_lambda = 2+3*mass/radius
    large_lambda = 2*small_lambda
    acceleration = -metric*metric_prime/2+3*metric_prime*velocity**2/(2*metric)+metric*radius*angular_speed**2
    angular_acceleration = angular_speed*velocity*(metric_prime/metric-2/radius)
    strength_rate = strength*(-velocity*metric_prime/metric-sp.I*azimuth*angular_speed)

    def time_derivative(expression):
        return (sp.diff(expression, radius)*velocity+sp.diff(expression, velocity)*acceleration
                +sp.diff(expression, angular_speed)*angular_acceleration+sp.diff(expression, strength)*strength_rate)

    checks = []
    def exact(name, expression):
        print('Checking '+name, flush=True)
        residual = sp.factor(expression)
        if residual != 0:
            raise AssertionError((name, str(residual)))
        checks.append({'name': name, 'passed': True})

    qtt, qtr, qrr = strength/radius**2, strength*velocity/radius**2, strength*velocity**2/radius**2
    qt, qr = -sp.I*azimuth*strength*angular_speed/3, -sp.I*azimuth*strength*angular_speed*velocity/3
    qflat = strength*angular_speed**2
    qsharp = strength*radius**2*angular_speed**2*(3-azimuth**2)/6
    qtrace = -metric*qtt+qrr/metric
    temporal_tt = (strength_rate/radius**2, -velocity*qtt)
    temporal_tr = ((strength_rate*velocity+strength*acceleration)/radius**2, -velocity*qtr)
    temporal_qt = (-sp.I*azimuth*(strength_rate*angular_speed+strength*angular_acceleration)/3, -velocity*qt)
    exact('time Bianchi delta prime', temporal_tt[1]+qtr)
    exact('time Bianchi delta', temporal_tt[0]+sp.diff(qtr, radius)+(metric_prime/metric+2/radius)*qtr-3*qt/radius**2)
    exact('radial Bianchi delta prime', temporal_tr[1]+qrr)
    exact('radial Bianchi delta', temporal_tr[0]+sp.diff(qrr, radius)+metric*metric_prime*qtt/2
          -metric_prime*qrr/(2*metric)+2*qrr/radius-3*qr/radius**2-metric*qflat/radius)
    exact('angular Bianchi delta prime', temporal_qt[1]+qr)
    exact('angular Bianchi delta', temporal_qt[0]+sp.diff(qr, radius)+2*qr/radius-2*qsharp/radius**2+qflat)
    polynomial = 8+12*mass/radius+84*mass**2/radius**2
    raw_F = sp.factor(metric*(-2*radius**2*metric*qtrace)/(3*large_lambda))
    raw_G = sp.factor(metric*(4*qr/large_lambda-qsharp/radius
                     +(-2*radius**2*metric*sp.diff(qtrace, radius)+24*mass*qrr/large_lambda
                       +2*radius*metric*qflat+radius*polynomial*qtrace/large_lambda)/(3*large_lambda)))
    canonical_F = raw_F
    canonical_G = sp.factor(raw_G-sp.diff(raw_F, radius))
    delta_prime = sp.factor(canonical_F/metric**2)
    delta = sp.factor(canonical_G/metric+canonical_F*metric_prime/metric**2)
    tortoise_speed = velocity/metric
    jump = sp.factor(delta_prime/(1-tortoise_speed**2))
    exact('moving value jump', jump-strength*metric/(3*small_lambda))
    jump_rate = sp.factor(time_derivative(jump))
    tortoise_acceleration = sp.factor(time_derivative(tortoise_speed))
    slope_jump = sp.factor((delta-2*tortoise_speed*jump_rate-tortoise_acceleration*jump)/(1-tortoise_speed**2))
    temporal_jump = sp.factor(jump_rate-tortoise_speed*slope_jump)
    exact('jump derivative compatibility', temporal_jump+tortoise_speed*slope_jump-jump_rate)
    exact('wave delta prime reconstructed', (1-tortoise_speed**2)*jump-delta_prime)
    exact('wave delta reconstructed', (1-tortoise_speed**2)*slope_jump+2*tortoise_speed*jump_rate+tortoise_acceleration*jump-delta)
    circular = {velocity: 0, angular_speed**2: mass/radius**3}
    previous_a = strength*(radius-2*mass)/(3*(2*radius+3*mass))
    previous_b = -strength*(12*radius**3-16*radius**2*mass-24*radius*mass**2-33*mass**3)/(6*radius**2*(2*radius+3*mass)**2)
    previous_b += strength*mass*(azimuth**2-4)/(6*radius**2)
    exact('circular value regression all m', jump-previous_a)
    exact('circular slope regression all m', slope_jump.subs(circular)-previous_b)
    exact('circular time jump regression', temporal_jump.subs(velocity, 0)+sp.I*azimuth*angular_speed*jump)

    energy, angular, radial_proper, particle, harmonic = sp.symbols('E h w mu Ybar', nonzero=True)
    substitution = {strength: 8*sp.pi*particle*energy/metric*harmonic,
                    velocity: metric*radial_proper/energy, angular_speed: metric*angular/(energy*radius**2)}
    effective_potential = metric*(1+angular**2/radius**2)
    mass_shell = energy**2-effective_potential
    martel_F = 8*sp.pi*particle*harmonic/3*metric**2*effective_potential/(small_lambda*energy)
    martel_G = 8*sp.pi*particle*harmonic/3*metric**2/(radius*small_lambda**2)*(6*mass/radius*energy
              -small_lambda/energy*(3-3*mass/radius+angular**2/radius**2*(5-7*mass/radius)))
    martel_G += -sp.I*azimuth*16*sp.pi*particle*harmonic/3*angular/energy*metric**2/(radius**2*small_lambda)*radial_proper
    martel_G += 8*sp.pi*particle*harmonic/3*angular**2/energy*metric**3/(radius**3*small_lambda)
    martel_G += -4*sp.pi*particle*harmonic/3*angular**2/energy*metric**2/radius**3*(3-azimuth**2)
    exact('independent Martel eccentric F', (canonical_F.subs(substitution)-martel_F).subs(radial_proper**2, mass_shell))
    exact('independent Martel eccentric canonical G',
          (canonical_G.subs(substitution)-martel_G+sp.diff(martel_F, radius)).subs(radial_proper**2, mass_shell))

    master, slope = sp.symbols('y y_x')
    potential = metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)
    angular_coefficient = (6*radius**2+6*mass*radius+6*mass**2)/(radius**2*(2*radius+3*mass))
    shift_coefficient = (2*radius**2-6*mass*radius-3*mass**2)/(radius*(radius-2*mass)*(2*radius+3*mass))
    angular_metric = angular_coefficient*master+slope
    angular_metric_prime = sp.diff(angular_coefficient, radius)*master+angular_coefficient*slope/metric+(potential-frequency**2)*master/metric
    lapse_metric = small_lambda/metric*(3*master/radius-angular_metric)+radius*angular_metric_prime
    shift_metric_dual = sp.I*frequency*radius*(shift_coefficient*master+slope/metric)
    metric_contraction = (metric+velocity**2/metric)*lapse_metric+2*velocity*shift_metric_dual+radius**2*angular_speed**2*angular_metric
    overlap = delta*master-delta_prime*slope
    boundary = strength*radius*(tortoise_speed*slope+(sp.I*frequency-strength_rate/strength-velocity/radius+2*velocity*shift_coefficient)*master)
    boundary = sp.factor(boundary)
    metric_contraction = sp.factor(metric_contraction)
    overlap = sp.factor(overlap)
    boundary_derivative = (time_derivative(boundary)+sp.diff(boundary, master)*tortoise_speed*slope
                           +sp.diff(boundary, slope)*tortoise_speed*(potential-frequency**2)*master
                           +sp.I*frequency*boundary)
    boundary_derivative = sp.factor(boundary_derivative)
    exact('integrated moving-source metric reciprocity', strength*metric_contraction+6*overlap-boundary_derivative)

    inside, inside_slope, horizon, horizon_slope, outgoing, outgoing_slope = sp.symbols('U Ux H Hx V Vx')
    overlap_U, overlap_H, overlap_V = sp.symbols('I_U I_H I_V')
    WUV = inside*outgoing_slope-inside_slope*outgoing
    WHV = horizon*outgoing_slope-horizon_slope*outgoing
    WUH = inside*horizon_slope-inside_slope*horizon
    linear_U = (WUV*overlap_H-WUH*overlap_V)/WHV
    exact('linear-source smooth difference functional', linear_U/WUV-overlap_H/WHV+WUH*overlap_V/(WUV*WHV))
    positive, negative = sp.symbols('positive negative')
    exact('negative-frequency reality pairing', (azimuth/frequency)-((-azimuth)/(-frequency)))
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    expressions = {'raw_F': raw_F, 'raw_G': raw_G, 'canonical_F': canonical_F, 'canonical_G': canonical_G,
                   'tortoise_delta': delta, 'tortoise_delta_prime': delta_prime, 'master_jump': jump,
                   'master_jump_rate': jump_rate, 'tortoise_slope_jump': slope_jump, 'time_slope_jump': temporal_jump,
                   'reciprocity_boundary': sp.factor(boundary), 'metric_contraction_dual': metric_contraction}
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'expressions': {key: str(value) for key, value in expressions.items()},
              'source': 'MP2005 eq4.17-4.27 and independent Martel2004 A6; ell2, equatorial arbitrary geodesic',
              'scope': 'Source, moving jumps, Fourier functional and integrated metric reciprocity; no new radiative flux yet.'}
    with (output/'status.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
    (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'jump': str(jump), 'delta': str(delta)}))


if __name__ == '__main__':
    main()


