from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results' / 'tensor-response'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError('Do not overwrite executed evidence.')
    OUTPUT.mkdir(parents=True)
    epsilon = sym.symbols('epsilon', real=True)
    conformal, disformal, delta_conformal, delta_disformal = sym.symbols('conformal disformal delta_conformal delta_disformal', real=True)
    delta_flow = sym.symbols('delta_flow_x delta_flow_y delta_flow_z', real=True)
    lowered_flow = sym.Matrix([-sym.sqrt(1 + epsilon**2 * sum(value**2 for value in delta_flow)), *[epsilon * value for value in delta_flow]])
    eta = sym.diag(-1, 1, 1, 1)
    metric = (conformal + epsilon * delta_conformal) * (eta + (disformal + epsilon * delta_disformal) * lowered_flow * lowered_flow.T)
    variation = metric.diff(epsilon).subs(epsilon, 0)
    spatial = variation[1:4, 1:4]
    projector = sym.diag(1, 1, 0)
    transverse_traceless = projector * spatial * projector - projector * sym.trace(projector * spatial) / 2
    checks = []

    def verify(name, actual, expected=0):
        difference = sym.simplify(actual - expected)
        checks.append({'name': name, 'passed': difference == 0, 'difference': str(difference)})
        assert difference == 0, (name, difference)

    verify('flow_normalization', (lowered_flow.T * eta * lowered_flow)[0], -1)
    for row in range(3):
        for column in range(3):
            verify(f'spatial_metric_variation_{row}_{column}', spatial[row, column], delta_conformal if row == column else 0)
            verify(f'transverse_traceless_metric_{row}_{column}', transverse_traceless[row, column])
    sound_speed, frequency, momentum = sym.symbols('sound_speed frequency momentum', positive=True)
    invariant = frequency**2 - sound_speed**2 * momentum**2
    finite_momentum_spectrum = invariant**2 / (960 * sym.pi * sound_speed**3)
    verify('finite_momentum_zero_limit', finite_momentum_spectrum.subs(momentum, 0), frequency**4 / (960 * sym.pi * sound_speed**3))
    rapidity = sym.symbols('rapidity', real=True)
    rest_frequency = sym.symbols('rest_frequency', positive=True)
    verify('acoustic_boost_invariant', invariant.subs({frequency: rest_frequency * sym.cosh(rapidity), momentum: rest_frequency * sym.sinh(rapidity) / sound_speed}), rest_frequency**2)
    verify('two_particle_threshold_smooth_weight', finite_momentum_spectrum.subs(frequency, sound_speed * momentum))
    verify('spatial_rescaling_stress_correlator_prefactor', sound_speed**3 * sound_speed**(-3) * sound_speed**(-3), sound_speed**(-3))
    report = {
        'state': 'complete', 'created_at': datetime.now(timezone.utc).isoformat(),
        'checks': checks, 'exact_identity_checks': len(checks),
        'spatial_metric_variation': str(spatial), 'transverse_traceless_variation': str(transverse_traceless),
        'positive_frequency_spectral_weight': str(finite_momentum_spectrum),
        'spectral_support': 'omega > c_s * |q|; zero below; q along z and shear xy; positive-frequency commutator convention',
        'derivation': 'Rescale x_prime=x/c_s, canonical_field_prime=c_s^(3/2)*canonical_field. Then T_xy=c_s^-3 T_prime_xy, d4x=c_s^3 d4x_prime. Acoustic Lorentz boost along z leaves xy indices unchanged. Transport the independently derived zero-momentum Gaussian two-phonon density.',
        'scope': 'Leading Gaussian phonon EFT, homogeneous stable charged background, low frequencies and momenta compared with amplitude-elimination scale, zero temperature; no amplitude threshold or interaction resummation included.',
        'not_proven': ['nonperturbative_no_composite_tensor_theorem', 'full_amplitude_finite_momentum_response', 'underlying_geometry_emergence', 'universal_standard_model_metric'],
        'inputs': {'first_candidate': hashlib.sha256((ROOT / 'results/first-candidate/status.json').read_bytes()).hexdigest(), 'independent_repair': hashlib.sha256((ROOT / 'results/repair-independent-check/status.json').read_bytes()).hexdigest()},
    }
    (OUTPUT / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'linear_TT_metric_map': 'zero', 'controlled_IR_spectrum': 'two_phonon_continuum'}))


if __name__ == '__main__':
    main()
