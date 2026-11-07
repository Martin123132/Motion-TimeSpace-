from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_support_column_20260930 import wave_densities, moved_packet, analytic_volume_column, dust_rows, dust_position_column
from annular_support_shift_jet_20260928 import wave_current
from annular_directional_coupled_Euler_20260928 import evaluate_wave, interpolate_nodal
from annular_old_field_reaction_20260929 import coefficient_data
import argparse
import ctypes
import numpy as np


def family(local, branch, amount=0.):
    left, width = 5.5, 1.2
    edge_change = np.array([-.12, .25])
    dilation = (edge_change[1] - edge_change[0]) / width
    movement = edge_change[0] * (1-local) + edge_change[1] * local
    radius = left + width * local + amount * movement
    widths = np.full(len(local), width + amount * (edge_change[1] - edge_change[0]))
    indices = np.tile([0, 1, 2], (len(local), 1))
    field_nodes = np.array([.13, -.21, .08]) + amount * np.array([.17, -.04, .23])
    rate_nodes = np.array([.21, .03, -.08]) + amount * np.array([.05, -.11, .03])
    acceleration_nodes = np.array([-.2, .12, .07]) + amount * np.array([.13, .19, -.12])
    evaluate = lambda nodes: interpolate_nodal(nodes, indices, local, widths)
    gradient = evaluate(field_nodes)[1]
    rate, rate_r = evaluate(rate_nodes)
    acceleration = evaluate(acceleration_nodes)[0]
    displacement = .8 + .2 * local
    speed = displacement * (.09 - amount * .031)
    speed_r = .2 * (.09 - amount * .031) / widths
    speed_rate = displacement * (-.07 + amount * .045)
    eta = .13 * (1-local) - .21 * local
    eta_r = -.34 / widths
    test, test_r = evaluate(np.array([.1, .26, -.14]))
    constants = np.array([.23, -.01]) if branch == 0 else np.array([.29, .005])
    slopes = np.array([.011, .002]) if branch == 0 else np.array([.013, -.004])
    position = np.array([.003, -.007])[:, None] * np.ones((2, len(local)))
    values = constants[:, None] + slopes[:, None] * radius + amount * position
    radial = slopes[:, None] * np.ones((2, len(local)))
    time_slopes = np.array([.002, -.001])[:, None]
    time = np.array([.003, -.002])[:, None] + time_slopes * radius
    mixed = np.array([.0005, -.0007])[:, None] * np.ones((2, len(local)))
    time = time + amount * mixed
    alpha, beta, alpha_r, beta_r = coefficient_data(radius, values, radial)
    metric = 1 - 2 * values[0] / radius
    packet = dict(measure=widths / width, widths=widths, indices=indices, local=local,
        radius=radius, source=6.1 + amount * .08,
        node_radius=left + width * np.array([0., .5, 1.]) + amount * np.array([-.12, .065, .25]),
        node_rate=rate_nodes, rate=rate, rate_r=rate_r, acceleration=acceleration,
        gradient=gradient, speed=speed, speed_r=speed_r, speed_rate=speed_rate,
        alpha=alpha, beta=beta, alpha_r=alpha_r, beta_r=beta_r,
        alpha_t=-alpha * (time[1] - time[0] / (radius * metric)),
        field=test, field_r=test_r, eta=eta, eta_r=eta_r,
        gradient_r=np.zeros(len(local)), star=np.zeros(len(local)), star_r=np.zeros(len(local)),
        face_eta=np.array([]), face_density_jump=np.array([]))
    direction = dict(movement=movement, movement_r=np.full(len(local), dilation),
        source=.08, node_movement=np.array([-.12, .065, .25]), node_rate=np.array([.05, -.11, .03]),
        rate=evaluate(np.array([.05, -.11, .03]))[0], rate_r=evaluate(np.array([.05, -.11, .03]))[1],
        gradient=evaluate(np.array([.17, -.04, .23]))[1], acceleration=evaluate(np.array([.13, .19, -.12]))[0],
        speed=-.031 * displacement, speed_r=-.031 * .2 / widths, speed_rate=.045 * displacement,
        values=values, radial=radial, time=time, material_values=position + radial * movement,
        material_radial=np.zeros((2, len(local))), material_time=mixed + time_slopes * movement)
    return packet, direction


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--cpu', type=int, choices=[2, 4], required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Cannot set one-core affinity')
    evidence = EvidenceRun(args.label, __file__)
    try:
        evidence.report.update(scope='Independent C0 regular derivative and moving-cut manufactured checks',
            actual_integrated_C0_complete=False, github_action=False, subagents_used=False)
        evidence.own(evidence.root / 'DERIVATION-20260930-position-support-C0.md')
        local = np.array([.07, .29, .63, .91])
        for branch in [0, 1]:
            packet, direction = family(local, branch)
            base = wave_densities(packet)
            replay = np.array([evaluate_wave(packet)['wave_direct']] + [wave_current(packet, power) for power in range(3)])
            evidence.check('baseline_existing_force_current_replay:'+str(branch), np.max(abs(base @ packet['measure'] - replay)) < 2e-12)
            analytic = analytic_volume_column(packet, direction)
            for step in [1e-20, 1e-25]:
                moved = moved_packet(packet, direction, 1j * step)
                direct = (wave_densities(moved) * moved['measure']).imag / step
                independently_built = family(local, branch, 1j * step)[0]
                independent = (wave_densities(independently_built) * independently_built['measure']).imag / step
                error = float(np.max(abs(analytic-direct)))
                evidence.check('analytic_complex:'+str(branch)+':'+str(step), error < 2e-11, error)
                error = float(np.max(abs(analytic-independent)))
                evidence.check('independently_rebuilt_family:'+str(branch)+':'+str(step), error < 2e-11, error)
            zero = {name: np.zeros_like(value) if name not in ['values', 'radial', 'time'] else value for name, value in direction.items()}
            evidence.check('zero_direction:'+str(branch), np.max(abs(analytic_volume_column(packet, zero))) == 0.)
        points, weights = np.polynomial.legendre.leggauss(32)
        cut = 6.15
        local_cut = (cut-5.5)/1.2
        regular, base = np.zeros(4), np.zeros(4)
        for branch, lower, upper in [(0, 0., local_cut), (1, local_cut, 1.)]:
            local = lower + (upper-lower) * (points+1)/2
            measure = 1.2 * (upper-lower) * weights/2
            packet, direction = family(local, branch)
            regular += analytic_volume_column(packet, direction) @ measure
            base += wave_densities(packet) @ measure
        traces = [wave_densities(family(np.array([local_cut]), branch)[0])[:, 0] for branch in [0, 1]]
        movement = -.12 * (1-local_cut) + .25 * local_cut
        atom = movement * (traces[1]-traces[0])
        complete = regular + atom

        def integral(amount):
            local_cut = (cut-5.5 + amount*.12)/(1.2 + amount*.37)
            result = np.zeros(4)
            for branch, lower, upper in [(0, 0., local_cut), (1, local_cut, 1.)]:
                local = lower + (upper-lower) * (points+1)/2
                packet = family(local, branch, amount)[0]
                measure = (1.2+amount*.37) * (upper-lower)*weights/2
                result += wave_densities(packet) @ measure
            return result

        errors = []
        for step in [2e-4, 1e-4, 5e-5]:
            finite = (integral(step)-integral(-step))/(2*step)
            errors.append(float(np.max(abs(finite-complete))))
        evidence.check('full_moving_cut_family_derivative', errors[-1] < 2e-7, errors)
        evidence.check('moving_cut_refinement', errors[-1] < errors[0]/5, errors)
        evidence.check('omitted_cut_negative_control', np.max(abs(atom)) > 100*errors[-1], atom.tolist())
        evidence.check('wrong_cut_sign_negative_control', np.max(abs(complete-(regular-atom))) > 100*errors[-1])
        evidence.report['cut_rows'] = dict(base=base.tolist(), regular=regular.tolist(), cut_atom=atom.tolist(), complete=complete.tolist(), finite_errors=errors)
        for source, velocity in [(6.1, .09), (6., 0.)]:
            values, changed = np.array([.3, -.02]), np.array([.011, -.007])
            expected = dust_position_column(source, velocity, values, .07, .08, -.031, changed)
            direct = dust_rows(source+1e-25j*.08, velocity-1e-25j*.031, values+1e-25j*changed, .07).imag/1e-25
            evidence.check('dust_source_and_clock:'+str(source), np.max(abs(expected-direct)) < 2e-15)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
