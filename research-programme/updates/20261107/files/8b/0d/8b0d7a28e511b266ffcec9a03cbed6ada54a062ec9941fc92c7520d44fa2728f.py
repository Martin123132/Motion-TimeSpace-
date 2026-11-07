import mpmath as mp
import numpy as np

from full_tail_action import FullTailActionFactors, panel_action as original_panel, reference_action
from full_tail_integrand import retained


def panel_action(factors, frequency, measure, densities, factors_data, mode, join, degree,
                 event_weight, angular_weight, emission_allowed, absorption_allowed):
    if emission_allowed or not absorption_allowed:
        return original_panel(factors, frequency, measure, densities, factors_data, mode, join, degree,
                              event_weight, angular_weight, emission_allowed, absorption_allowed)
    if not isinstance(factors, FullTailActionFactors) or mp.mp.dps < 60 or mode not in ('control','difference'):
        raise ValueError('Retained high-precision source factors required')
    frequency, measure = np.asarray(frequency,dtype=float), np.asarray(measure,dtype=float)
    if (frequency.ndim != 1 or not len(frequency) or frequency.shape != measure.shape or not np.isfinite(frequency).all()
            or not np.isfinite(measure).all() or np.any(frequency<=0) or -1 not in densities or -1 not in factors_data
            or len(densities[-1]) != len(frequency) or not np.isfinite(float(event_weight)) or not np.isfinite(float(angular_weight))):
        raise ValueError('Original finite absorption nodes, weights and densities required')
    reference = reference_action(factors,frequency,measure,mode,join,degree,event_weight,angular_weight)
    temperature = factors.owner.temperature / factors.owner.doppler
    population = [1/mp.expm1(retained.scalar(value)) for value in frequency]
    weighted = measure * float(temperature) * np.array([float(value*record[mode]) for value,record in zip(population,densities[-1])])
    data = factors_data[-1]
    left = factors.left[degree][None] + data[degree,'left_delta']
    right = data[join,degree,'reference'] + data[join,degree,'right_delta']
    absorption = retained.contract(left,weighted[:,None,None,None]*right) * (.5*event_weight*angular_weight/(2*degree+1))
    return reference + absorption
