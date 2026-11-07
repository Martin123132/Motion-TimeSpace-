from __future__ import annotations

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
    coordinates = sp.symbols('position_x position_y position_z', real=True)
    spatial_potential = sp.Function('Psi')(*coordinates)
    lapse_potential = sp.Function('Phi')(*coordinates)
    metric = sp.exp(-2*spatial_potential)*sp.eye(3)
    inverse = sp.exp(2*spatial_potential)*sp.eye(3)
    connection = [[[sp.S.Zero for second in range(3)] for first in range(3)] for upper in range(3)]
    for upper in range(3):
        for first in range(3):
            for second in range(3):
                connection[upper][first][second] = sp.simplify(sum(inverse[upper, contracted]*(
                    sp.diff(metric[contracted, second], coordinates[first])
                    +sp.diff(metric[contracted, first], coordinates[second])
                    -sp.diff(metric[first, second], coordinates[contracted]))/2 for contracted in range(3)))
    ricci = sp.zeros(3)
    for first in range(3):
        for second in range(3):
            ricci[first, second] = sum(sp.diff(connection[upper][first][second], coordinates[upper])
                                      -sp.diff(connection[upper][first][upper], coordinates[second]) for upper in range(3))
            ricci[first, second] += sum(connection[upper][first][second]*connection[contracted][upper][contracted]
                                       -connection[upper][first][contracted]*connection[contracted][second][upper]
                                       for upper in range(3) for contracted in range(3))
    scalar_curvature = sp.simplify(sum(inverse[first, second]*ricci[first, second]
                                       for first in range(3) for second in range(3)))
    laplacian_spatial = sum(sp.diff(spatial_potential, coordinate, 2) for coordinate in coordinates)
    laplacian_lapse = sum(sp.diff(lapse_potential, coordinate, 2) for coordinate in coordinates)
    spatial_gradient_squared = sum(sp.diff(spatial_potential, coordinate)**2 for coordinate in coordinates)
    crossed_gradient = sum(sp.diff(lapse_potential, coordinate)*sp.diff(spatial_potential, coordinate) for coordinate in coordinates)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('three_curvature_from_connection', scalar_curvature-sp.exp(2*spatial_potential)*(4*laplacian_spatial-2*spatial_gradient_squared))
    density = sp.exp(lapse_potential-3*spatial_potential)*scalar_curvature
    exact('einstein_static_density', density-sp.exp(lapse_potential-spatial_potential)*(4*laplacian_spatial-2*spatial_gradient_squared))
    quadratic_before_parts = 4*(lapse_potential-spatial_potential)*laplacian_spatial-2*spatial_gradient_squared
    divergence = sum(sp.diff(4*(lapse_potential-spatial_potential)*sp.diff(spatial_potential, coordinate), coordinate) for coordinate in coordinates)
    exact('quadratic_bulk_after_boundary_separation', quadratic_before_parts-divergence-(2*spatial_gradient_squared-4*crossed_gradient))
    coupling = sp.symbols('G_R', positive=True)
    density_source = sp.Function('rho')(*coordinates)
    lagrangian = (spatial_gradient_squared-2*crossed_gradient)/(8*sp.pi*coupling)-density_source*lapse_potential

    def euler_lagrange(function):
        return sp.diff(lagrangian, function)-sum(sp.diff(sp.diff(lagrangian, sp.diff(function, coordinate)), coordinate) for coordinate in coordinates)

    exact('lapse_constraint_is_poisson', euler_lagrange(lapse_potential)-(laplacian_spatial/(4*sp.pi*coupling)-density_source))
    exact('spatial_potential_equation', euler_lagrange(spatial_potential)-(laplacian_lapse-laplacian_spatial)/(4*sp.pi*coupling))
    exact('eliminated_field_gradient_sign', ((spatial_gradient_squared-2*crossed_gradient)/(8*sp.pi*coupling)).subs(lapse_potential, spatial_potential).doit()
          +spatial_gradient_squared/(8*sp.pi*coupling))
    output = ROOT/'results/weak-metric'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Connection-to-curvature and quadratic static Einstein-action checks; pressureless matched monopoles, weak external field, boundary terms separated explicitly.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
