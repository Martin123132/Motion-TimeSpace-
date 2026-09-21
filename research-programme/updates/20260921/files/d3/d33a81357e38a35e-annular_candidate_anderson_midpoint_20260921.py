from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_midpoint_20260921 import advance_coordinates
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
import numpy as np


def midpoint_step(evaluator, coordinates, momenta, seed, step, preconditioner, record):
    rates = seed.copy()
    scale = max(preconditioner.residual_norm(np.asarray(momenta, float)), 1e-30)
    history, residuals, images = [], [], []
    previous = None
    proposal = 'initial_seed'
    coefficient_norm = 0.
    rank = 0
    for iteration in range(40):
        midpoint = advance_coordinates(coordinates, rates, step/2, evaluator.precision)
        current = evaluator.evaluate(midpoint, rates)
        with localcontext() as context:
            context.prec = evaluator.precision
            residual = np.asarray(decimal_array(current['momentum'])-momenta-
                Decimal.from_float(float(step/2))*current['force_decimal'], float)
        correction = preconditioner.solve(residual.ravel()).reshape(rates.shape)
        norm = preconditioner.residual_norm(residual)/scale
        maximum = float(np.max(abs(correction)))
        row = dict(iteration=iteration, relative_residual=norm, maximum_correction=maximum,
            radial_residual=current['radial_residual'], minimum_F=current['minimum_F'],
            maximum_speed_ratio=current['maximum_speed_ratio'], residual_ratio=None if previous is None else norm/previous,
            proposal=proposal, coefficient_norm=coefficient_norm, history_rank=rank)
        history.append(row)
        record(row, midpoint, rates, current, residual)
        if norm < 5e-12 and maximum < 2e-12:
            result = advance_coordinates(coordinates, rates, step, evaluator.precision)
            with localcontext() as context:
                context.prec = evaluator.precision
                updated = momenta+Decimal.from_float(float(step))*current['force_decimal']
            return result, updated, rates, current, history
        if not np.isfinite(norm) or norm > 1e4*max(history[0]['relative_residual'], 1e-12):
            raise RuntimeError('Accelerated midpoint residual exceeded its declared safety bound.')
        weighted = residual.ravel()/preconditioner.original_scale
        image = (rates-correction).ravel()
        if residuals:
            differences = np.column_stack([item-weighted for item in residuals])
            coefficients, unused, rank_value, unused_singular = np.linalg.lstsq(differences, -weighted, rcond=1e-12)
            coefficient_norm = float(np.linalg.norm(coefficients, ord=1))
            rank = int(rank_value)
            if np.all(np.isfinite(coefficients)) and coefficient_norm <= 1e6:
                changes = np.column_stack([item-image for item in images])
                proposed = image+changes @ coefficients
                proposal = 'residual_minimizing_history'
            else:
                proposed = (rates-.1*correction).ravel()
                proposal = 'explicit_recorded_damped_fallback'
        else:
            proposed = image
            proposal = 'mass_preconditioned_first_step'
        if not np.all(np.isfinite(proposed)):
            raise RuntimeError('Nonfinite accelerated midpoint proposal.')
        residuals.append(weighted.copy())
        images.append(image.copy())
        residuals, images = residuals[-12:], images[-12:]
        rates = proposed.reshape(rates.shape)
        previous = norm
    raise RuntimeError('Accelerated midpoint did not reach both unchanged stopping gates in 40 trials.')
