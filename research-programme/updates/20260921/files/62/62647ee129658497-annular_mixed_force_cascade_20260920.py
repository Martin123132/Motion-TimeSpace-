from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import zero_array
from annular_mixed_weak_maps_20260920 import stiffness_apply
from derive_annular_commutator_riesz_bound_20260919 import mass_apply
from decimal import Decimal, getcontext
from time import perf_counter
import numpy as np


def forward_generator(coarse, fine, transfer, maps, scale, source, response):
    acceleration = coarse.acceleration(source[0])
    mixed_acceleration = maps['mass'].apply(acceleration)
    mixed_stiffness = stiffness_apply(maps, source[0])
    mass_defect = mass_apply(fine, transfer.apply(acceleration))-mixed_acceleration
    stiffness_defect = mixed_stiffness-fine.stiffness(transfer.apply(source[0]))
    weak_defect = mixed_acceleration-mixed_stiffness
    forcing = np.column_stack([mass_defect, stiffness_defect, weak_defect])
    source_rate = np.stack([scale*source[1], -acceleration/scale])
    response_rate = np.stack([scale*response[1], fine.solve(forcing-fine.stiffness(response[0]))/scale])
    return source_rate, response_rate


def adjoint_generator(coarse, fine, transfer, maps, scale, source, response):
    lifted_velocity = fine.solve(source[1])
    stiffness_velocity = fine.stiffness(lifted_velocity)
    mixed_mass_dual = maps['mass'].apply(lifted_velocity, True)
    mixed_stiffness_dual = stiffness_apply(maps, lifted_velocity, True)
    mass_defect = coarse.acceleration(transfer.apply(source[1], True)-mixed_mass_dual, True)
    stiffness_defect = mixed_stiffness_dual-transfer.apply(stiffness_velocity, True)
    weak_defect = coarse.acceleration(mixed_mass_dual, True)-mixed_stiffness_dual
    forcing = np.column_stack([mass_defect, stiffness_defect, weak_defect])
    source_rate = np.stack([-stiffness_velocity/scale, scale*source[0]])
    response_rate = np.stack([(forcing-coarse.acceleration(response[1], True))/scale, scale*response[0]])
    return source_rate, response_rate


def integrate_channels(coarse, fine, transfer, maps, source_phase, duration, degree,
        transpose=False, progress=None, deadline=None):
    scale = max(coarse.frequency_bound, fine.frequency_bound)
    steps = max(1, int((abs(duration)*scale/Decimal(4)).to_integral_value(rounding='ROUND_CEILING')))
    step = duration/steps
    source = source_phase.copy()
    response = zero_array((2, coarse.count if transpose else fine.count, 3))
    source[0] = source[0]/scale if transpose else source[0]*scale
    generator = adjoint_generator if transpose else forward_generator
    maximum_tail = Decimal(0)
    for index in range(steps):
        if deadline is not None and perf_counter() > deadline:
            raise RuntimeError('Safe frozen-cascade wall-time boundary reached; saved evidence retained.')
        source_term, response_term = generator(coarse, fine, transfer, maps, scale, source, response)
        source_term *= step
        response_term *= step
        source_next, response_next = source+source_term, response+response_term
        for order in range(2, degree+1):
            source_term, response_term = generator(coarse, fine, transfer, maps, scale, source_term, response_term)
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
    return response, source, dict(substeps=steps, degree=degree, digits=getcontext().prec,
        maximum_scaled_last_term=str(maximum_tail), transpose=transpose)
