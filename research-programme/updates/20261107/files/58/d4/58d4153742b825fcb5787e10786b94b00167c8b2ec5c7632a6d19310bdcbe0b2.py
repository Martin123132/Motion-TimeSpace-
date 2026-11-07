from __future__ import annotations

from pathlib import Path
import numpy as np

from polar_energy import Background, quadrature, solve_constraint, modest_process, save, dependencies


def main():
    modest_process()
    background = Background()
    outer = 4*background.radius
    rows = []
    for body_cells in [128, 256, 512, 1024]:
        edges = np.r_[np.linspace(0, background.radius, body_cells+1), np.linspace(background.radius, outer, body_cells//2+1)[1:]]
        position, weights, cells, shape_left, shape_right = quadrature(edges, 10)
        coordinate = position/outer
        exact = coordinate**2*(1-coordinate)**4
        exact_prime = (2*coordinate*(1-coordinate)**4-4*coordinate**2*(1-coordinate)**3)/outer
        exact_second = (2*(1-coordinate)**4-16*coordinate*(1-coordinate)**3+12*coordinate**2*(1-coordinate)**2)/outer**2
        values = background.values(position)
        metric, metric_prime, lapse, lapse_log, field, rotation2, energy = [values[key] for key in ['metric', 'metric_prime', 'lapse', 'log_lapse_prime', 'field', 'rotation2', 'energy']]
        measure = position**2/np.sqrt(metric)
        potential = 6/position**2+2*background.alpha*(rotation2*field**2-energy)
        source = -metric*exact_second-(2*metric/position+metric_prime/2)*exact_prime+potential*exact
        solution, derivative, tail_amplitude, residual, _ = solve_constraint(background, edges, position, weights, cells, shape_left, shape_right, source[:, None])
        l2_error = float(np.sqrt(np.sum(weights*measure*(solution[:, 0]-exact)**2)/np.sum(weights*measure*exact**2)))
        gradient_error = float(np.sqrt(np.sum(weights*measure*metric*(derivative[:, 0]-exact_prime)**2)/np.sum(weights*measure*metric*exact_prime**2)))
        original = np.sum(weights*measure*(metric*exact_prime**2+potential*exact**2))
        transformed = np.sum(weights*measure*(metric*(exact_prime-lapse_log*exact)**2+6*exact**2/position**2))
        ground_state_error = float(abs(original/transformed-1))
        rows.append(dict(body_cells=body_cells, outer_cells=body_cells//2, l2_relative_error=l2_error,
             gradient_relative_error=gradient_error, linear_solve_relative_residual=residual,
             numerical_tail_amplitude=float(tail_amplitude[0]), exact_tail_amplitude=0.,
             background_ground_state_form_error=ground_state_error))
    assert all(row['linear_solve_relative_residual'] < 1e-9 and row['background_ground_state_form_error'] < 1e-8 for row in rows)
    ratios = dict(l2=rows[-2]['l2_relative_error']/rows[-1]['l2_relative_error'], gradient=rows[-2]['gradient_relative_error']/rows[-1]['gradient_relative_error'])
    assert 3.9 < ratios['l2'] < 4.1 and 1.95 < ratios['gradient'] < 2.05, ratios
    save('constraint-control', Path(__file__), dict(input_hashes=dependencies(background.profile), rows=rows, last_halving_ratios=ratios,
         scope='Manufactured elliptic solution using independently differentiated compact polynomial; background ground-state form numerical cross-check. Manufactured forcing is not a physical mode.'))
    print(dict(rows=len(rows), ratios=ratios, finest=rows[-1]), flush=True)


if __name__ == '__main__':
    main()
