from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import quadratic, density_rows
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from time import perf_counter
import numpy as np


def reaction_rows(packet, radius, values, mixed_uncertainty):
    local, width = packet['local'], packet['width']
    gradient = quadratic(packet['field'], local, width)[1]
    rate = quadratic(packet['rate'], local, width)[0]
    displacement = packet['displacement_left']+(packet['displacement_right']-packet['displacement_left'])*local
    speed = displacement*packet['source_velocity']
    temporal = rate-speed*gradient
    uncertainty = quadratic(packet['acceleration_uncertainty'], local, width)[0]
    uncertainty -= displacement*packet['source_uncertainty']*gradient
    metric = 1-2*values[0]/radius
    alpha = radius**2/(np.exp(values[1])*np.sqrt(metric))
    alpha_t_uncertainty = -alpha*(mixed_uncertainty[1]-mixed_uncertainty[0]/(radius*metric))
    momentum_uncertainty = alpha_t_uncertainty*temporal+alpha*uncertainty
    test = quadratic(packet['test'], local, width)[0]
    eta = packet['eta_left']+(packet['eta_right']-packet['eta_left'])*local
    rows = [momentum_uncertainty*(test-eta*gradient)]
    shape = [(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)]
    for power in range(3):
        integral = (radius-packet['source'])*sum((radius-6)**(power-index)*(packet['source']-6)**index
            for index in range(power+1))/(power+1)
        difference = np.zeros_like(rate)
        for fraction, basis in zip([0., .5, 1.], shape):
            node_radius = packet['node_left']+(packet['node_right']-packet['node_left'])*fraction
            node_rate = packet['rate'][:, 0]+fraction*(packet['rate'][:, 1]+fraction*packet['rate'][:, 2])
            primitive_difference = width*(local-fraction)*sum((radius-6)**(power-index)*(node_radius-6)**index
                for index in range(power+1))/(power+1)
            difference += basis*node_rate*primitive_difference
        difference -= speed*gradient*integral
        rows.append(momentum_uncertainty*difference)
    return np.array(rows)


def integrate_reaction(evaluator, acceleration_uncertainty, mixed_uncertainty, radial_order, label_order, deadline, progress):
    evaluator.polynomials['acceleration_uncertainty'] = local_polynomials(evaluator.action.mesh, decimals(acceleration_uncertainty[:, :-1].T))[0]
    trace = PolynomialTrace(mixed_uncertainty.solver, mixed_uncertainty.solution, evaluator.anchor)
    endpoints = np.concatenate([evaluator.geometry.geometry(evaluator.edges, label)[0] for label in [-.5, .5]])
    cuts = np.unique(np.r_[evaluator.radial_cuts, trace.edges, endpoints])
    points, weights = np.polynomial.legendre.leggauss(radial_order)
    lengths = np.diff(cuts)
    offsets = (cuts[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
    measures = (lengths[:, None]*weights/2).ravel()
    total, absolute, correction = np.zeros(4), np.zeros(4), np.zeros(4)
    oracle_error, oracle_relative_error, oracle_samples = 0., 0., 0
    oracle_blocks = set(np.linspace(0, (len(offsets)-1)//16, 13).astype(int)*16)
    for start in range(0, len(offsets), 16):
        if start % 2048 == 0:
            if perf_counter() > deadline:
                raise RuntimeError('Safe C0 sensitivity boundary')
            progress('sensitivity-'+str(radial_order)+':'+str(start)+'/'+str(len(offsets)))
        section = slice(start, start+16)
        density = CenteredLabelDensity(evaluator.action, offsets[section], label_order)
        selected = offsets[section][density.indices]
        packet, active = evaluator.packet(density.offsets, selected)
        packet['source_uncertainty'] = evaluator.action.cardinal(density.offsets)@acceleration_uncertainty[:, -1]
        values, unused, radial, unused2 = evaluator.metric.evaluate(selected, evaluator.metric.cells(selected))
        uncertainty = trace.evaluate(selected, trace.cells(selected))[0]
        rows = reaction_rows(packet, evaluator.anchor+selected, values, uncertainty)
        measure = measures[section][density.indices]*density.label_weights*active
        block = rows@measure
        updated = total+block
        correction += np.where(abs(total) >= abs(block), (total-updated)+block, (block-updated)+total)
        total = updated
        absolute += abs(rows)@measure
        if start in oracle_blocks or (oracle_samples == 0 and np.any(active)):
            moved = dict(packet, acceleration=packet['acceleration']+1e-25j*packet['acceleration_uncertainty'],
                source_acceleration=packet['source_acceleration']+1e-25j*packet['source_uncertainty'])
            time = sum(item.evaluate(selected, item.cells(selected))[0] for item in evaluator.time_traces)
            oracle = density_rows(moved, evaluator.anchor+selected, values, radial, time+1e-25j*uncertainty).imag/1e-25
            if np.any(active):
                error = float(np.max(abs(oracle[:, active]-rows[:, active])))
                scale = max(float(np.max(abs(oracle[:, active]))), float(np.max(abs(rows[:, active]))), 1e-300)
                oracle_error = max(oracle_error, error)
                oracle_relative_error = max(oracle_relative_error, error/scale)
                oracle_samples += int(np.count_nonzero(active))
    selected = (offsets >= evaluator.metric.edges[0])&(offsets <= evaluator.metric.edges[-1])
    radius = evaluator.anchor+offsets[selected]
    values = evaluator.metric.evaluate(offsets[selected], evaluator.metric.cells(offsets[selected]))[0]
    uncertainty = trace.evaluate(offsets[selected], trace.cells(offsets[selected]))[0][0]
    coefficient = np.exp(values[1])/(evaluator.action.owner.coupling*np.sqrt(1-2*values[0]/radius))
    gravity = np.array([measures[selected]@(coefficient*uncertainty*(radius-6)**power) for power in range(3)])
    complete = total+correction
    complete[1:] += gravity
    return dict(wave=total+correction, gravity=gravity, complete=complete,
        sampled_absolute_wave=absolute, pointwise_oracle_error=np.array(oracle_error),
        pointwise_oracle_relative_error=np.array(oracle_relative_error), oracle_active_samples=np.array(oracle_samples))
