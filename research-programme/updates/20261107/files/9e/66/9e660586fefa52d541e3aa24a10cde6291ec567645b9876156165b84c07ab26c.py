from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_candidate_hamiltonian_20260921 import decimals
from annular_common_weighted_moments_20260920 import apply_rational_rows
from decimal import Decimal, localcontext
from fractions import Fraction
import numpy as np


def rational_seed(point, anchor, lower, upper):
    offset = point-anchor
    distance = abs(offset)
    if distance >= Fraction(11, 20):
        envelope, derivative = Fraction(0), Fraction(0)
    elif distance <= Fraction(1, 5):
        envelope, derivative = Fraction(1), Fraction(0)
    else:
        fraction = (distance-Fraction(1, 5))/Fraction(7, 20)
        envelope = 1-10*fraction**3+15*fraction**4-6*fraction**5
        derivative = (-30*fraction**2+60*fraction**3-30*fraction**4)/Fraction(7, 20)
        derivative *= 1 if offset > 0 else -1
    field = offset*envelope/100
    gradient = (envelope+offset*derivative)/100
    displacement = (point-lower)/(anchor-lower) if point < anchor else (upper-point)/(upper-anchor)
    return field, gradient, -Fraction(3, 100)*gradient*(1-displacement)


def seed_arrays(mesh, sources, velocities):
    edges = list(map(Fraction, mesh['edges']))
    anchor = Fraction(mesh['anchor'])
    fields, rates = [], []
    with localcontext() as context:
        context.prec = 64
        for point in map(Fraction, mesh['nodes']):
            field, gradient, rate = rational_seed(point, anchor, edges[0], edges[-1])
            fields.append(Decimal(field.numerator)/Decimal(field.denominator))
            rates.append(float(rate))
        coordinates = np.column_stack([np.tile(fields, (len(sources), 1)), decimals(np.asarray(sources)[:, None])[:, 0]])
    rates = np.column_stack([np.tile(rates, (len(sources), 1)), np.asarray(velocities, float)])
    return coordinates, rates


def prolong(values, rows):
    with localcontext() as context:
        context.prec = 64
        return apply_rational_rows(rows, decimals(values).T).T


def analytic_seed(radius, mesh):
    anchor = float(Fraction(mesh['anchor']))
    offset = radius-anchor
    distance = abs(offset)
    fraction = np.clip((distance-.2)/.35, 0., 1.)
    envelope = 1-10*fraction**3+15*fraction**4-6*fraction**5
    derivative = (-30*fraction**2+60*fraction**3-30*fraction**4)*np.sign(offset)/.35
    envelope[distance >= .55] = 0.
    derivative[(distance <= .2) | (distance >= .55)] = 0.
    field = offset*envelope/100
    gradient = (envelope+offset*derivative)/100
    lower, upper = float(Fraction(mesh['edges'][0])), float(Fraction(mesh['edges'][-1]))
    displacement = np.where(radius < anchor, (radius-lower)/(anchor-lower), (upper-radius)/(upper-anchor))
    return field, gradient, -.03*gradient*(1-displacement)


def representation(mesh, coordinates, rates, order=8):
    edges = np.array([float(Fraction(value)) for value in mesh['edges']])
    anchor = float(Fraction(mesh['anchor']))
    with localcontext() as context:
        context.prec = 64
        polynomial, gradient = local_polynomials(mesh, decimals(coordinates[:, :-1]).T)
        rate_polynomial, unused = local_polynomials(mesh, decimals(rates[:, :-1]).T)
    joins = anchor+np.array([-.55, -.2, .2, .55])
    cuts = np.unique(np.r_[edges, joins])
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = ((cuts[:-1, None]+cuts[1:, None])/2+np.diff(cuts)[:, None]*points/2).ravel()
    measure = (np.diff(cuts)[:, None]*weights/2).ravel()
    cells = np.clip(np.searchsorted(edges, radius, side='right')-1, 0, len(edges)-2)
    local = (radius-edges[cells])/np.diff(edges)[cells]
    field = polynomial[cells, 0]+local[:, None]*(polynomial[cells, 1]+local[:, None]*polynomial[cells, 2])
    slope = gradient[cells, 0]+local[:, None]*gradient[cells, 1]
    rate = rate_polynomial[cells, 0]+local[:, None]*(rate_polynomial[cells, 1]+local[:, None]*rate_polynomial[cells, 2])
    truth = analytic_seed(radius, mesh)
    metrics = {}
    for name, value, expected in zip(['field', 'gradient', 'rate'], [field, slope, rate], truth):
        error = value-expected[:, None]
        metrics[name+'_L2_error'] = float(np.max(np.sqrt(measure@error**2)))
        metrics[name+'_sample_max_error'] = float(np.max(abs(error)))
    jumps = gradient[1:, 0]-(gradient[:-1, 0]+gradient[:-1, 1])
    metrics.update(jump_max=float(np.max(abs(jumps))), jump_l2=float(np.max(np.sqrt(np.sum(jumps**2, axis=0)))),
        field_gradient_integral=float(np.mean(measure@(field**2+slope**2))), quadrature_order=order)
    return metrics, dict(edges=edges, jumps=jumps, polynomial=polynomial, gradient=gradient, rate_polynomial=rate_polynomial)
