from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import density_rows
from annular_C0_material_integral_v3_20260930 import material_density_rows
import numpy as np


def identity_rows(evaluator, packet, offsets):
    amount = 1e-25j
    values, value_r, radial, radial_r = evaluator.metric.evaluate(offsets, evaluator.metric.cells(offsets))
    positions = [item.evaluate(offsets, item.cells(offsets)) for item in evaluator.responses]
    times = [item.evaluate(offsets, item.cells(offsets)) for item in evaluator.time_traces]
    time, time_r = sum(row[0] for row in times), sum(row[1] for row in times)
    mixed = sum(item.evaluate(offsets, item.cells(offsets))[0] for item in evaluator.mixed_traces)
    position, position_r = sum(row[0] for row in positions), sum(row[2] for row in positions)
    radius = evaluator.anchor+offsets
    movement = packet['movement_left']+(packet['movement_right']-packet['movement_left'])*packet['local']
    dilation = (packet['movement_right']-packet['movement_left'])/packet['width']
    eulerian = density_rows(packet, radius, values+amount*position,
        radial+amount*position_r, time+amount*mixed, amount).imag/amount.imag
    material = material_density_rows(packet, radius+amount*movement, values+amount*(position+value_r*movement),
        radial+amount*(position_r+radial_r*movement), time+amount*(mixed+time_r*movement), amount)
    material = (material*(1+amount*dilation)).imag/amount.imag
    shifted = dict(packet, local=packet['local']+amount/packet['width'])
    spatial = material_density_rows(shifted, radius+amount, values+amount*value_r,
        radial+amount*radial_r, time+amount*time_r)
    transport = movement*(spatial.imag/amount.imag)+dilation*spatial.real
    defect = material-eulerian-transport
    wrong_shift = material-eulerian+transport
    return dict(material=material, eulerian=eulerian, transport=transport,
        defect=defect, wrong_sign=wrong_shift, metric_derivative_gap=value_r-radial)
