from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import decimal_array
from derive_annular_native_shape_stress_20260928 import physical_data
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import numpy as np


def balanced_field_force(loads, action, spatial, material, deadline, progress):
    engine = loads.native_engine
    with localcontext() as context:
        context.prec = 75
        polynomial = engine.basis.polynomial(engine.indices, loads.coordinates[:, :-1].T)
        widths = np.array([Decimal((Fraction(upper) - Fraction(lower)).numerator) / Decimal((Fraction(upper) - Fraction(lower)).denominator)
            for lower, upper in zip(action.mesh['edges'][:-1], action.mesh['edges'][1:])], dtype=object)
        powers = np.arange(2, engine.basis.degree + 1)
        curvature = np.asarray(polynomial[:, 2:] * (powers * (powers - 1))[None, :, None] / widths[:, None, None]**2, float)
    force = np.zeros((len(action.source), engine.count))
    bulk_force = np.zeros_like(force)
    traction_force = np.zeros_like(force)
    points, weights = np.polynomial.legendre.leggauss(material)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    for number, (label, weight) in enumerate(zip(points, weights)):
        if perf_counter() > deadline:
            raise RuntimeError('Balanced-force assembly deadline')
        sample = action.samples(label, spatial)
        quad, geometry, cardinal = sample['quadrature'], sample['geometry'], sample['cardinal']
        coefficients = np.einsum('cpl,l->cp', curvature, cardinal, optimize=False)[quad['cells']]
        second = np.polynomial.polynomial.polyval(quad['local'], coefficients.T, tensor=False)
        logarithmic = 2 / geometry['radius'] + geometry['lapse_log_radial'] + geometry['metric_radial'] / (2 * geometry['metric'])
        integrand = geometry['gradient'] * (second + geometry['jacobian'] * logarithmic * sample['gradient'])
        bulk = np.zeros(engine.count)
        np.add.at(bulk, quad['indices'].ravel(), (quad['measure'][:, None] * integrand[:, None] * quad['shape']).ravel())
        with localcontext() as context:
            context.prec = 75
            data = physical_data(engine, loads, action, label)
            result = engine.evaluate(data['edges'], data['field'], data['beta'], data['beta_radial'])
            radius = np.asarray(data['edges'], float)
            values = action.solver.values(action.solution, radius)[0]
            beta = decimal_array(radius**2 * np.exp(values[1]) * np.sqrt(1 - 2 * values[0] / radius))
            atom = result['atoms']
            edge_load = np.r_[beta[0] * atom['slope_left'][0],
                beta[1:-1] * (atom['slope_left'][1:] - atom['slope_right'][:-1]), -beta[-1] * atom['slope_right'][-1]]
            edge_indices = np.r_[engine.indices[:, 0], engine.indices[-1, -1]]
            traction = np.full(engine.count, Decimal(0), dtype=object)
            selected = edge_indices >= 0
            np.add.at(traction, edge_indices[selected], edge_load[selected])
            balanced = np.asarray(traction - result['field_gradient'], float)
        force += weight * np.outer(cardinal, bulk + balanced)
        bulk_force += weight * np.outer(cardinal, bulk)
        traction_force += weight * np.outer(cardinal, np.asarray(traction, float))
        if number % 16 == 15:
            progress('balanced field layer ' + str(number + 1))
    return dict(force=force, bulk=bulk_force, traction=traction_force)
