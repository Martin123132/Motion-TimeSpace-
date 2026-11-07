from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_stable_current_20260930 import stable_density_rows
from functools import partial
import numpy as np


stable_material = partial(stable_density_rows, material=True)


def stable_identity_rows(evaluator, packet, offsets):
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
    eulerian = stable_density_rows(packet, radius, values+amount*position,
        radial+amount*position_r, time+amount*mixed, amount).imag/amount.imag
    material = stable_material(packet, radius+amount*movement, values+amount*(position+value_r*movement),
        radial+amount*(position_r+radial_r*movement), time+amount*(mixed+time_r*movement), amount)
    material = (material*(1+amount*dilation)).imag/amount.imag
    shifted = dict(packet, local=packet['local']+amount/packet['width'])
    spatial = stable_material(shifted, radius+amount, values+amount*value_r,
        radial+amount*radial_r, time+amount*time_r)
    transport = movement*(spatial.imag/amount.imag)+dilation*spatial.real
    defect = material-eulerian-transport
    wrong_shift = material-eulerian+transport
    return dict(material=material, eulerian=eulerian, transport=transport,
        defect=defect, wrong_sign=wrong_shift, metric_derivative_gap=value_r-radial)
