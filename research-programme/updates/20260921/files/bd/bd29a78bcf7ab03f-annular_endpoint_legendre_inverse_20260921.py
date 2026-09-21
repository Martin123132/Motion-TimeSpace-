from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import localcontext
import numpy as np


def endpoint_inverse(evaluator, coordinates, momenta, seed, preconditioner, record):
    rates = seed.copy()
    scale = max(preconditioner.residual_norm(np.asarray(momenta, float)), 1e-30)
    history = []
    previous = None
    for iteration in range(20):
        current = evaluator.evaluate(coordinates, rates)
        with localcontext() as context:
            context.prec = evaluator.precision
            residual = np.asarray(decimal_array(current['momentum'])-momenta, float)
        correction = preconditioner.solve(residual.ravel()).reshape(rates.shape)
        norm = preconditioner.residual_norm(residual)/scale
        maximum = float(np.max(abs(correction)))
        row = dict(iteration=iteration, relative_residual=norm, maximum_correction=maximum,
            radial_residual=current['radial_residual'], minimum_F=current['minimum_F'],
            maximum_speed_ratio=current['maximum_speed_ratio'],
            residual_ratio=None if previous is None else norm/previous)
        history.append(row)
        record(row, coordinates, rates, current, residual)
        if norm < 5e-12 and maximum < 2e-12:
            return coordinates.copy(), momenta.copy(), rates, current, history
        if previous is not None and norm > 1.25*previous:
            raise RuntimeError('Endpoint Legendre inverse is not contracting.')
        previous = norm
        rates -= correction
    raise RuntimeError('Endpoint inverse did not reach both stopping gates.')
