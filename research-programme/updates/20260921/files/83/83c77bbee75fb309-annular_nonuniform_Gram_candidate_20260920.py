from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_compatible_current_restoring_20260909 import unit_gram_template
from scipy.sparse import coo_matrix, csr_matrix
import numpy as np


def template_rows(count):
    if count < 17:
        raise ValueError('The sourced closure requires at least 17 Gram knots.')
    margins, adjacent, extras = unit_gram_template(count)
    rows, columns, values = [], [], []
    locations = []
    for index, margin in enumerate(margins):
        rows.append(len(locations))
        columns.append(index)
        values.append(np.sqrt(margin))
        locations.append(index+1.5)
    for index, coupling in enumerate(adjacent):
        rows.extend([len(locations)]*2)
        columns.extend([index, index+1])
        values.extend([np.sqrt(abs(coupling)), np.sign(coupling)*np.sqrt(abs(coupling))])
        locations.append(index+2.)
    for first, second, coupling in extras:
        rows.extend([len(locations)]*2)
        columns.extend([first, second])
        values.extend([np.sqrt(abs(coupling)), np.sign(coupling)*np.sqrt(abs(coupling))])
        locations.append((first+second)/2+1.5)
    template = coo_matrix((values, (rows, columns)), shape=(len(locations), count-3)).tocsr()
    locations = np.asarray(locations)
    lower = np.floor(locations).astype(int)
    fraction = locations-lower
    sampling = coo_matrix((np.concatenate([1-fraction, fraction]),
        (np.tile(np.arange(len(locations)), 2), np.concatenate([lower, lower+1]))),
        shape=(len(locations), count)).tocsr()
    return template, sampling


def divided_rows(knots, displacement=None):
    knots = np.asarray(knots)
    if knots.ndim != 1 or len(knots) < 17 or not np.all(np.isfinite(knots)) or np.any(np.diff(knots.real) <= 0):
        raise ValueError('Finite strictly increasing Gram knots, count >=17, required.')
    count = len(knots)
    width = (knots[3:]-knots[:-3])/3
    coefficients = np.empty((count-3, 4), dtype=np.result_type(knots, float))
    derivatives = None if displacement is None else np.empty_like(coefficients)
    if displacement is not None:
        displacement = np.asarray(displacement)
        if displacement.shape != knots.shape or not np.all(np.isfinite(displacement)):
            raise ValueError('Invalid knot variation.')
        width_rate = (displacement[3:]-displacement[:-3])/3
    for local in range(4):
        denominator = np.ones(count-3, dtype=coefficients.dtype)
        logarithmic = np.zeros(count-3, dtype=coefficients.dtype)
        for other in range(4):
            if other == local:
                continue
            distance = knots[local:count-3+local]-knots[other:count-3+other]
            denominator *= distance
            if displacement is not None:
                logarithmic += (displacement[local:count-3+local]-displacement[other:count-3+other])/distance
        coefficients[:, local] = 6*width**2.5/denominator
        if displacement is not None:
            derivatives[:, local] = coefficients[:, local]*(2.5*width_rate/width-logarithmic)
    row_indices = np.repeat(np.arange(count-3), 4)
    column_indices = (np.arange(count-3)[:, None]+np.arange(4)[None, :]).ravel()
    mapping = coo_matrix((coefficients.ravel(), (row_indices, column_indices)), shape=(count-3, count)).tocsr()
    derivative = None if derivatives is None else coo_matrix((derivatives.ravel(), (row_indices, column_indices)), shape=mapping.shape).tocsr()
    return mapping, derivative, width


def gram_action(knots, values, jump, anchor, coefficient, variation=None, include_gram=True):
    knots, values, coefficient = map(np.asarray, (knots, values, coefficient))
    if values.shape != knots.shape or coefficient.shape != knots.shape or np.any(coefficient.real <= 0):
        raise ValueError('Values and positive coefficient must be supplied at every Gram knot.')
    if not np.all(np.isfinite(values)) or not np.all(np.isfinite(coefficient)):
        raise ValueError('Nonfinite action input.')
    if np.any(knots.real == np.real(anchor)):
        raise ValueError('This differentiable chart excludes a knot crossing or touching the source.')
    template, sampling = template_rows(len(knots))
    kernel, derivative, width = divided_rows(knots, None if variation is None else variation['knots'])
    operator = template @ kernel
    if not include_gram:
        operator = csr_matrix(operator.shape, dtype=operator.dtype)
        if derivative is not None:
            derivative = csr_matrix(derivative.shape, dtype=derivative.dtype)
    hinge = np.where(knots.real > np.real(anchor), knots-anchor, 0.)
    compensated = values-jump*hinge
    factor = operator @ compensated
    row_weight = sampling @ coefficient
    weighted = row_weight*factor
    result = dict(energy=np.dot(factor, weighted)/2, factor=factor, operator=operator,
        sampling=sampling, kernel=kernel, row_weight=row_weight, width=width,
        values_covector=-(operator.T @ weighted), jump_covector=np.dot(operator @ hinge, weighted))
    if variation is not None:
        hinge_rate = np.where(knots.real > np.real(anchor), variation['knots']-variation['anchor'], 0.)
        compensated_rate = variation['values']-variation['jump']*hinge-jump*hinge_rate
        operator_rate = template @ derivative
        factor_rate = operator_rate @ compensated+operator @ compensated_rate
        weight_rate = sampling @ variation['coefficient']
        result.update(variation=np.dot(weighted, factor_rate)+np.dot(factor**2, weight_rate)/2,
            stencil_variation=np.dot(weighted, operator_rate @ compensated),
            coefficient_variation=np.dot(factor**2, weight_rate)/2,
            trace_and_field_variation=np.dot(weighted, operator @ compensated_rate))
    return result

