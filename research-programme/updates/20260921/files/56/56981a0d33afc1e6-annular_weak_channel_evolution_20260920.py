from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import zero_array
from decimal import Decimal, getcontext
from time import perf_counter
import numpy as np


def forward_rate(coarse, fine, pairs, scale, source, response):
    acceleration = coarse.acceleration(source[0])
    forcing = np.column_stack([mass.apply(acceleration)-stiffness.apply(source[0]) for mass, stiffness in pairs])
    return (np.stack([scale*source[1], -acceleration/scale]),
        np.stack([scale*response[1], fine.solve(forcing-fine.stiffness(response[0]))/scale]))


def adjoint_rate(coarse, fine, pairs, scale, source, response):
    lifted = fine.solve(source[1])
    mass = np.column_stack([mapping.apply(lifted, True) for mapping, unused in pairs])
    stiffness = np.column_stack([mapping.apply(lifted, True) for unused, mapping in pairs])
    forcing = coarse.acceleration(mass, True)-stiffness
    return (np.stack([-fine.stiffness(lifted)/scale, scale*source[0]]),
        np.stack([(forcing-coarse.acceleration(response[1], True))/scale, scale*response[0]]))


def evolve_channels(coarse, fine, all_pairs, source_phase, duration, degree,
        transpose=False, progress=None, deadline=None):
    active = [index for index, (mass, stiffness) in enumerate(all_pairs) if len(mass.values) or len(stiffness.values)]
    if not active:
        raise ValueError('At least one active channel required; no physical mode filtering is allowed.')
    pairs = [all_pairs[index] for index in active]
    scale = max(coarse.frequency_bound, fine.frequency_bound)
    steps = max(1, int((abs(duration)*scale/Decimal(4)).to_integral_value(rounding='ROUND_CEILING')))
    step = duration/steps
    source = source_phase.copy()
    count = coarse.count if transpose else fine.count
    response = zero_array((2, count, len(pairs)))
    source[0] = source[0]/scale if transpose else source[0]*scale
    rate = adjoint_rate if transpose else forward_rate
    maximum_tail = Decimal(0)
    for index in range(steps):
        if deadline is not None and perf_counter() > deadline:
            raise RuntimeError('Safe weak-channel time limit reached; existing evidence retained.')
        source_term, response_term = rate(coarse, fine, pairs, scale, source, response)
        source_term *= step
        response_term *= step
        source_next, response_next = source+source_term, response+response_term
        for order in range(2, degree+1):
            source_term, response_term = rate(coarse, fine, pairs, scale, source_term, response_term)
            source_term *= step/Decimal(order)
            response_term *= step/Decimal(order)
            source_next += source_term
            response_next += response_term
        source, response = source_next, response_next
        maximum_tail = max(maximum_tail, max(map(abs, source_term.flat)), max(map(abs, response_term.flat)))
        if progress is not None and ((index+1) % 8 == 0 or index+1 == steps):
            progress(index+1, steps)
    source[0] = source[0]*scale if transpose else source[0]/scale
    response[0] = response[0]*scale if transpose else response[0]/scale
    full_response = zero_array((2, count, len(all_pairs)))
    full_response[:, :, active] = response
    return full_response, source, dict(substeps=steps, degree=degree, digits=getcontext().prec,
        active_channels=active, exactly_zero_channels=[index for index in range(len(all_pairs)) if index not in active],
        maximum_scaled_last_term=str(maximum_tail), transpose=transpose)
