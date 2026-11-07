from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_reaction_sensitivity_20260930 import reaction_rows
from annular_C0_boundary_integral_20260930 import density_rows
from validate_annular_C0_boundaries_20260930 import toy_data, metric
import ctypes
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun('annular-C0-reaction-sensitivity-manufactured-attempt01', __file__)
    try:
        radius = 5.5+1.2*np.array([.07, .29, .63, .91])
        for branch in [0, 1]:
            values, radial, time = metric(radius, branch)
            for mode in ['field', 'source', 'metric', 'combined']:
                packet = toy_data(radius, single=True)
                packet['acceleration_uncertainty'] = np.zeros_like(packet['acceleration'])
                packet['source_uncertainty'] = np.zeros_like(radius)
                mixed = np.zeros_like(values)
                if mode in ['field', 'combined']:
                    packet['acceleration_uncertainty'][:] = [.17, -.09, .12]
                if mode in ['source', 'combined']:
                    packet['source_uncertainty'][:] = .23
                if mode in ['metric', 'combined']:
                    mixed[:] = np.array([[.04], [-.08]])
                closed = reaction_rows(packet, radius, values, mixed)
                amount = 1e-25j
                moved = dict(packet, acceleration=packet['acceleration']+amount*packet['acceleration_uncertainty'],
                    source_acceleration=packet['source_acceleration']+amount*packet['source_uncertainty'])
                oracle = density_rows(moved, radius, values, radial, time+amount*mixed).imag/amount.imag
                scale = max(float(np.max(abs(oracle))), 1e-300)
                error = float(np.max(abs(closed-oracle)))/scale
                evidence.check(f'{branch}:{mode}:independent_derivative', error < 2e-13 and np.max(abs(closed)) > 0., error)
                positive = dict(packet, acceleration=packet['acceleration']+.31*packet['acceleration_uncertainty'],
                    source_acceleration=packet['source_acceleration']+.31*packet['source_uncertainty'])
                negative = dict(packet, acceleration=packet['acceleration']-.31*packet['acceleration_uncertainty'],
                    source_acceleration=packet['source_acceleration']-.31*packet['source_uncertainty'])
                finite = (density_rows(positive, radius, values, radial, time+.31*mixed)
                    -density_rows(negative, radius, values, radial, time-.31*mixed))/.62
                error = float(np.max(abs(finite-closed)))/scale
                evidence.check(f'{branch}:{mode}:finite_linearity', error < 2e-12, error)
                evidence.check(f'{branch}:{mode}:omission_negative_control', np.max(abs(oracle))/scale > .5)
        evidence.own(evidence.root/'DERIVATION-20260930-C0-reaction-sensitivity.md')
        evidence.report.update(actual_sensitivity_integrated=False, valid_for_claim=False, github_action=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
