from __future__ import annotations

import argparse
from pathlib import Path
import time

import numpy as np
from scipy import linalg

from polar_energy import Background, basis, quadrature, solve_constraint, even_form, hessian_form, spectral_data, tail, modest_process, save, dependencies, digest, BRANCH


def padded(values, offset, size):
    result = np.zeros((values.shape[0], size))
    result[:, offset:offset+values.shape[1]] = values
    return result


def coupled(matter_count, gravity_count, body_cells, outer_cells, extent, order):
    background = Background()
    radius = background.radius
    outer = extent*radius
    edges = np.r_[np.linspace(0, radius, body_cells+1), np.linspace(radius, outer, outer_cells+1)[1:]]
    position, weights, cells, shape_left, shape_right = quadrature(edges, order)
    values = background.values(position)
    field, gradient, second_gradient, metric, lapse, energy, force, rotation2, metric_prime, log_lapse_prime = [values[key] for key in ['field', 'gradient', 'second_gradient', 'metric', 'lapse', 'energy', 'force', 'rotation2', 'metric_prime', 'log_lapse_prime']]
    measure = position**2/np.sqrt(metric)
    gravity_basis = basis(position, outer, gravity_count, 4)
    matter_basis = basis(position, radius, matter_count, 2)
    size = gravity_count+2*matter_count
    geometric = padded(gravity_basis[0], 0, size)*np.sqrt(background.alpha)
    geometric_prime = padded(gravity_basis[1], 0, size)*np.sqrt(background.alpha)
    amplitude = padded(matter_basis[0], gravity_count, size)
    amplitude_prime = padded(matter_basis[1], gravity_count, size)
    phase_momentum = padded(matter_basis[0], gravity_count+matter_count, size)
    source = -metric[:, None]*geometric_prime/position[:, None]-(4/position**2-2*background.alpha*energy)[:, None]*geometric+2*background.alpha*((force-rotation2*field)[:, None]*amplitude+(metric*gradient)[:, None]*amplitude_prime+(background.frequency*field/lapse)[:, None]*phase_momentum)
    angular, angular_prime, tail_amplitude, constraint_residual, solution = solve_constraint(background, edges, position, weights, cells, shape_left, shape_right, source)
    radial = geometric+angular
    even = even_form(background, position, weights, radial, angular, angular_prime, amplitude, amplitude_prime, phase_momentum)
    tail_nodes, tail_weights = np.polynomial.legendre.leggauss(96)
    inverse_radius = (tail_nodes+1)/2
    tail_position = outer/inverse_radius
    tail_quadrature = tail_weights*outer/(2*inverse_radius**2)
    tail_value, tail_derivative = tail(tail_position, background.mass, outer)
    tail_angular = tail_value[:, None]*tail_amplitude[None, :]
    tail_gradient = tail_derivative[:, None]*tail_amplitude[None, :]
    zero_tail = np.zeros_like(tail_angular)
    tail_even = even_form(background, tail_position, tail_quadrature, tail_angular, tail_angular, tail_gradient, zero_tail, zero_tail, zero_tail)
    even += tail_even
    momentum = padded(gravity_basis[0], 0, size)/np.sqrt(background.alpha)
    momentum_prime = padded(gravity_basis[1], 0, size)/np.sqrt(background.alpha)
    momentum_second = padded(gravity_basis[2], 0, size)/np.sqrt(background.alpha)
    amplitude_momentum = padded(matter_basis[0], gravity_count, size)
    amplitude_momentum_prime = padded(matter_basis[1], gravity_count, size)
    phase = padded(matter_basis[0], gravity_count+matter_count, size)
    phase_prime = padded(matter_basis[1], gravity_count+matter_count, size)
    phase_second = padded(matter_basis[2], gravity_count+matter_count, size)
    transport = field[:, None]*phase_prime-gradient[:, None]*phase
    mixed_source = momentum_prime+3*momentum/position[:, None]-gradient[:, None]*amplitude_momentum/2-background.frequency/(2*lapse[:, None])*transport
    mixed_source_prime = momentum_second+3*momentum_prime/position[:, None]-3*momentum/position[:, None]**2-(second_gradient[:, None]*amplitude_momentum+gradient[:, None]*amplitude_momentum_prime)/2-background.frequency/(2*lapse[:, None])*(field[:, None]*phase_second-second_gradient[:, None]*phase-log_lapse_prime[:, None]*transport)
    mixed = position[:, None]**2*mixed_source/6
    mixed_prime = position[:, None]*mixed_source/3+position[:, None]**2*mixed_source_prime/6
    tensor = (metric[:, None]*mixed_prime+(metric_prime/2+2*metric/position)[:, None]*mixed-momentum/2-(background.frequency*field/(2*lapse))[:, None]*phase)/2
    odd = np.zeros_like(even)
    hessian_form(odd, weights, lapse*measure*6*background.alpha, momentum)
    hessian_form(odd, weights, lapse*measure*48*background.alpha*metric/position**2, mixed)
    hessian_form(odd, weights, lapse*measure*48*background.alpha, tensor)
    hessian_form(odd, weights, lapse*measure/2, amplitude_momentum)
    field_log = np.divide(gradient, field, out=np.zeros_like(field), where=field > 0)
    hessian_form(odd, weights, lapse*measure*metric/2, phase_prime-field_log[:, None]*phase)
    hessian_form(odd, weights, lapse*measure*3/position**2, phase)
    gravity_gram = gravity_basis[0].T@((weights*measure)[:, None]*gravity_basis[0])
    matter_gram = matter_basis[0].T@((weights*measure)[:, None]*matter_basis[0])
    gram = linalg.block_diag(gravity_gram, matter_gram, matter_gram)
    spectral = spectral_data(even, odd, gram, gravity_count, matter_count)
    report = dict(**spectral, constraint_residual=constraint_residual,
        alpha=background.alpha, radius=radius, mass=background.mass, background_frequency=background.frequency,
        configuration=dict(matter_count=matter_count, gravity_count=gravity_count, body_cells=body_cells, outer_cells=outer_cells, extent=extent, order=order),
        tail_fraction_matrix_norm=float(np.linalg.norm(tail_even)/np.linalg.norm(even)),
        input_hashes=dependencies(background.profile), projected_positive=bool(spectral['even_min'] > 0 and spectral['odd_min'] > 0),
        scope='Full constraints; finite Galerkin form-domain test only. Exact decaying constraint tail; compact gravity trial coordinates. Ritz frequencies are not outgoing resonances or a continuum gap.')
    arrays = dict(even=even, odd=odd, gram=gram, edges=edges, conformal_solution=solution, tail_even=tail_even)
    return report, arrays


def flat(matter_count, body_cells, order):
    background = Background(0.)
    edges = np.linspace(0, background.radius, body_cells+1)
    position, weights, *_ = quadrature(edges, order)
    values = background.values(position)
    matter, derivative, _ = basis(position, background.radius, matter_count, 2)
    mass = matter.T@((weights*position**2)[:, None]*matter)
    gradient = derivative.T@((weights*position**2)[:, None]*derivative)
    angular = matter.T@((weights*6)[:, None]*matter)
    potential = matter.T@((weights*position**2*(values['second']+3*background.frequency**2))[:, None]*matter)
    shifted = derivative-(values['gradient']/values['field'])[:, None]*matter
    phase = shifted.T@((weights*position**2)[:, None]*shifted)+angular
    even = np.block([[gradient+angular+potential, -2*background.frequency*mass], [-2*background.frequency*mass, mass]])
    odd = linalg.block_diag(mass, phase)
    gram = linalg.block_diag(mass, mass)
    spectral = spectral_data(even, odd, gram, 0, matter_count)
    deletion = linalg.block_diag(gradient+angular+potential, mass)
    negative_control = spectral_data(deletion, odd, gram, 0, matter_count)
    reference_path = BRANCH/'dynamical-tides-20261004/results/flat-crosscheck/status.json'
    reference = .0188117251133
    return dict(**spectral, configuration=dict(matter_count=matter_count, body_cells=body_cells, order=order),
        reference_frequency=reference, relative_reference_difference=float(abs(spectral['frequencies'][0]/reference-1)),
        deleted_cross_frequency=negative_control['frequencies'][0],
        input_hashes=dependencies(background.profile),
        reference_source=str(BRANCH/'dynamical-tides-20261004/check_flat_mode.py'),
        reference_source_sha256=digest(BRANCH/'dynamical-tides-20261004/check_flat_mode.py'),
        scope='Independent flat gyroscopic mode control; phase mixing deletion is deliberately not a physical alternative.'), dict(even=even, odd=odd, gram=gram)


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--flat', action='store_true')
    parser.add_argument('--matter', type=int, default=12)
    parser.add_argument('--gravity', type=int, default=6)
    parser.add_argument('--cells', type=int, default=512)
    parser.add_argument('--outer-cells', type=int, default=256)
    parser.add_argument('--extent', type=float, default=4.)
    parser.add_argument('--order', type=int, default=8)
    args = parser.parse_args()
    started = time.monotonic()
    report, arrays = flat(args.matter, args.cells, args.order) if args.flat else coupled(args.matter, args.gravity, args.cells, args.outer_cells, args.extent, args.order)
    report['elapsed_seconds'] = time.monotonic()-started
    save(args.label, Path(__file__), report, arrays)
    print(dict(label=args.label, even_min=report['even_min'], odd_min=report['odd_min'], frequencies=report['frequencies'][:5], seconds=report['elapsed_seconds'], reference_error=report.get('relative_reference_difference')), flush=True)


if __name__ == '__main__':
    main()
