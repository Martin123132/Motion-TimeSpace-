from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from budget import ROOT, read_json, digest, save, dependencies, modest_process, RateCurve


def main():
    modest_process()
    source = ROOT/'results/nodes/status.json'
    integral_source = ROOT/'results/integrals/status.json'
    report = read_json(source)
    target = np.array(read_json(integral_source)['budget']['full_outgoing'])
    body = next(row for row in report['static_boundaries'] if row['settings'] == 'fine')
    mass, radius = body['mass'], body['radius']
    nodes = [row for row in report['nodes'] if row['settings'] == 'fine']
    names = ['point_out', 'frozen_polar', 'dynamic_polar', 'odd_response']
    curves = {name:RateCurve(nodes, name, mass, radius) for name in names}
    scale = np.maximum(abs(target), 1e-30)
    rows = []
    for strength in [1., .5, .25]:
        def derivative(separation, state):
            semilatus = separation*radius/mass
            baseline = curves['point_out'].rates(separation)
            parts = [curves[name].rates(separation) for name in names[1:]]
            shrink, gamma, second = [baseline[key] for key in ['P0', 'G_action', 'X2']]
            delta_shrink, delta_gamma, delta_second = [strength*sum(row[key] for row in parts) for key in ['P0', 'G_action', 'X2']]
            body_shrink, body_second = shrink+delta_shrink, second+delta_second
            assert shrink < 0 and body_shrink < 0
            log_difference = state[1]*scale[0]
            log_prime = (delta_gamma*shrink-gamma*delta_shrink)/(shrink*body_shrink)
            time0 = -delta_shrink/(mass**2*shrink*body_shrink)
            second_ratio_difference = (delta_second*shrink**2-second*(2*shrink*delta_shrink+delta_shrink**2))/(shrink**2*body_shrink**2)
            time2 = -np.exp(state[0])/mass**2*(second_ratio_difference+body_second/body_shrink**2*np.expm1(log_difference))
            return np.concatenate([[gamma/shrink], np.array([log_prime,time0,time0*semilatus**-1.5,time2,time2*semilatus**-1.5])/scale])*radius/mass
        solution = solve_ivp(derivative, (10., 5.), np.zeros(6), method='DOP853', rtol=2e-12, atol=2e-14)
        assert solution.success
        endpoint = solution.y[1:, -1]*scale
        residual = endpoint-strength*target
        rows.append(dict(strength=strength, endpoint=endpoint.tolist(), linear=(strength*target).tolist(),
            residual=residual.tolist(), relative_to_first_order=(residual/(strength*target)).tolist()))
    ratios = [(np.array(first['residual'])/np.array(second['residual'])).tolist()
              for first, second in zip(rows, rows[1:])]
    assert all(3.98 < value < 4.02 for row in ratios for value in row), ratios
    maximum = max(abs(value) for value in rows[0]['relative_to_first_order'])
    assert maximum < 1e-4, maximum
    save('response-order', __file__, dict(input_hashes={**dependencies(), str(source):digest(source), str(integral_source):digest(integral_source)},
        controls=rows, halving_remainder_ratios=ratios, maximum_relative_first_order_remainder=maximum,
        interpretation='Resummed rational-flux order control of the retained ell2 system; artificial response strengths are not refitted physical bodies.'))
    print(dict(state='complete', maximum_relative_first_order_remainder=maximum, ratios=ratios), flush=True)


if __name__ == '__main__':
    main()
