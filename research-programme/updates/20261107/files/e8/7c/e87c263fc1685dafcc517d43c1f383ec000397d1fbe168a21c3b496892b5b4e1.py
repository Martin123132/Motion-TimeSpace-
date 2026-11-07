from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import density_rows
from annular_position_support_column_20260930 import wave_densities, analytic_volume_column
from validate_annular_position_support_manufactured_20260930 import family
import ctypes
import numpy as np


def coefficients(nodes, count):
    left, middle, right = nodes
    return np.tile([left, -3*left+4*middle-right, 2*left-4*middle+2*right], (count, 1))


def toy_data(radius, cell=0, single=False):
    lower, upper = (5.5, 6.7) if single else [(5.5, 6.), (6., 6.7)][cell]
    motions = [-.12, .25] if single else [[-.12, .2], [.2, .25]][cell]
    eta = [.13, -.21] if single else [[.13, -.05], [-.05, -.21]][cell]
    left = cell == 0 or single
    nodes = dict(field=[.13, -.21, .08] if left else [.08, .16, -.13],
        rate=[.21, .03, -.08] if left else [-.08, .04, .11],
        acceleration=[-.2, .12, .07] if left else [.07, -.12, .09],
        field_change=[.17, -.04, .23] if left else [.23, -.11, .2],
        rate_change=[.05, -.11, .03] if left else [.03, -.02, .07],
        acceleration_change=[.13, .19, -.12] if left else [-.12, .08, .03],
        test=[.1, .26, -.14] if left else [-.14, .05, .09])
    packet = {name:coefficients(values, len(radius)) for name, values in nodes.items()}
    packet.update(width=np.full(len(radius), upper-lower), local=(radius-lower)/(upper-lower),
        movement_left=np.full(len(radius), motions[0]), movement_right=np.full(len(radius), motions[1]),
        source=np.full(len(radius), 6.1), source_change=np.full(len(radius), .08),
        source_velocity=np.full(len(radius), .09), source_rate_change=np.full(len(radius), -.031),
        source_acceleration=np.full(len(radius), -.07), source_acceleration_change=np.full(len(radius), .045),
        displacement_left=np.full(len(radius), .8 if left else 1.), displacement_right=np.full(len(radius), 1. if left else .5),
        eta_left=np.full(len(radius), eta[0]), eta_right=np.full(len(radius), eta[1]),
        node_left=np.full(len(radius), lower), node_right=np.full(len(radius), upper))
    return packet


def metric(radius, branch, amount=0.):
    constants = np.array([.23, -.01]) if branch == 0 else np.array([.29, .005])
    slopes = np.array([.011, .002]) if branch == 0 else np.array([.013, -.004])
    values = constants[:, None]+slopes[:, None]*radius+amount*np.array([.003, -.007])[:, None]
    radial = slopes[:, None]*np.ones((2, len(radius)))
    time = np.array([.003, -.002])[:, None]+np.array([.002, -.001])[:, None]*radius
    time = time+amount*np.array([.0005, -.0007])[:, None]
    return values, radial, time


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun('annular-C0-boundaries-manufactured-attempt01', __file__)
    try:
        evidence.report.update(actual_C0_integrated=False, github_action=False, subagents_used=False)
        local = np.array([.07, .29, .63, .91])
        radius = 5.5+1.2*local
        for branch in [0, 1]:
            old, direction = family(local, branch)
            new = density_rows(toy_data(radius, single=True), radius, *metric(radius, branch))
            evidence.check('independent_density_replay:'+str(branch), np.max(abs(new-wave_densities(old))) < 2e-12)
            eulerian = density_rows(toy_data(radius, single=True), radius, *metric(radius, branch, 1e-25j), 1e-25j).imag/1e-25
            spatial = density_rows(toy_data(radius+1e-25j, single=True), radius+1e-25j, *metric(radius+1e-25j, branch)).imag/1e-25
            recovered = eulerian+direction['movement']*spatial+direction['movement_r']*new
            evidence.check('independent_material_Eulerian_identity:'+str(branch), np.max(abs(recovered-analytic_volume_column(old, direction))) < 2e-11)
        points, weights = np.polynomial.legendre.leggauss(32)

        def integrated(amount, derivative=False):
            cuts = [5.5-.12*amount, 6.+.2*amount, 6.15, 6.7+.25*amount]
            rows = np.zeros(4)
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                radius = lower+(upper-lower)*(points+1)/2
                cell, branch = int((lower+upper)/2 > cuts[1]), int((lower+upper)/2 > 6.15)
                delta = 1e-25j if derivative else amount
                value = density_rows(toy_data(radius, cell), radius, *metric(radius, branch, delta), delta)
                rows += (value.imag/1e-25 if derivative else value)@((upper-lower)*weights/2)
            return rows

        volume = integrated(0., True)
        face = .2*(density_rows(toy_data(np.array([6.]), 0), np.array([6.]), *metric(np.array([6.]), 0))[:, 0]
            -density_rows(toy_data(np.array([6.]), 1), np.array([6.]), *metric(np.array([6.]), 0))[:, 0])
        outer = .25*density_rows(toy_data(np.array([6.7]), 1), np.array([6.7]), *metric(np.array([6.7]), 1))[:, 0]
        outer += .12*density_rows(toy_data(np.array([5.5]), 0), np.array([5.5]), *metric(np.array([5.5]), 0))[:, 0]
        complete = volume+face+outer
        errors = []
        for step in [2e-4, 1e-4, 5e-5]:
            finite = (integrated(step)-integrated(-step))/(2*step)
            errors.append(float(np.max(abs(finite-complete))))
        evidence.check('moving_family_complete_derivative', errors[-1] < 1e-5, errors)
        evidence.check('moving_family_refinement', errors[-1] < errors[0]/5, errors)
        evidence.check('omitted_material_face_negative_control', np.max(abs(face)) > 100*errors[-1], face.tolist())
        evidence.check('omitted_outer_negative_control', np.max(abs(outer)) > 100*errors[-1], outer.tolist())
        evidence.report['wave_rows'] = dict(volume=volume.tolist(), faces=face.tolist(), outer=outer.tolist(), complete=complete.tolist(), finite_errors=errors)

        def atom_integral(amount):
            crossing = (.12-.07*amount)/.8
            total = 0.
            for lower, upper, coefficient in [(-.5, crossing, 1.3), (crossing, .5, 2.1)]:
                labels = lower+(upper-lower)*(points+1)/2
                values = coefficient*(1+labels**2+amount*(.4-labels))*6*(labels+.5)*(.5-labels)
                total += values@((upper-lower)*weights/2)
            return total

        crossing = .12/.8
        regular = 0.
        for lower, upper, coefficient in [(-.5, crossing, 1.3), (crossing, .5, 2.1)]:
            labels = lower+(upper-lower)*(points+1)/2
            regular += (coefficient*(.4-labels)*6*(labels+.5)*(.5-labels))@((upper-lower)*weights/2)
        atom = .07/.8*(2.1-1.3)*(1+crossing**2)*6*(crossing+.5)*(.5-crossing)
        finite = (atom_integral(1e-5)-atom_integral(-1e-5))/2e-5
        evidence.check('coefficient_cut_label_atom', abs(finite-regular-atom) < 2e-10, float(finite-regular-atom))
        evidence.check('coefficient_cut_omission_negative_control', abs(finite-regular) > .01)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
