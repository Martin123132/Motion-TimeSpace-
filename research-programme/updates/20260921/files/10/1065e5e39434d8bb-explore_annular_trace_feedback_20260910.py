import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_homogeneous_trace_feedback_20260910 import trace_feedback, released_slope_moments, normal_form

    root = Path(__file__).resolve().parents[1]
    case = json.loads((root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json').read_text())
    constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
    kappa = float(symbolic.sympify(case['normalization_kappa']))
    for intervals in [16, 32, 64, 128]:
        basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
        count = basis.radii.size
        system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, kappa, numerical.zeros(count), numerical.zeros(count), 1., MetricLinkQuadrature(basis))
        packed = numerical.zeros(system.count)
        packed[system.slices[0]], packed[system.slices[1]] = 1., .82
        for branch in ['GR', 'metric_Gram']:
            for kind in ['constant', 'linear', 'quadratic']:
                centered = basis.radii - 6.
                theta = .001 * (numerical.ones(count) if kind == 'constant' else centered if kind == 'linear' else centered**2)
                speed = numerical.zeros_like(packed)
                speed[system.slices[1]] = .82 * theta
                result = trace_feedback(system, packed, speed, branch != 'GR')
                normal = normal_form(system, packed, speed, numerical.zeros_like(packed), result)
                moments = released_slope_moments(system, packed, speed, result)
                row = {'intervals': intervals, 'branch': branch, 'kind': kind, 'G': result['operators']['growth_rate'], 'G_regular': result['regular_growth'], 'trace_norm': result['feedback_K_to_R2'], 'gradient_trace_norm': result['gradient_trace_K_to_R2'], 'identity_error': float(abs(result['reconstructed'] - result['operators']['configuration_transport']).max()), 'slope_second_error': max(float(abs(part['predicted_second'] - part['direct_second']).max()) for part in moments)}
                row.update(G_gradient_regular=result['gradient_regular_growth'], G_normal=normal['growth'])
                print(json.dumps(row), flush=True)


if __name__ == '__main__':
    run()
