from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut
import numpy as np


def manufactured(system, time, position0, velocity0):
    acceleration = .02
    position = position0+velocity0*time+acceleration*time**2/2
    velocity = velocity0+acceleration*time
    offset = system.radii-position
    left = offset.real < 0
    slope = np.where(left, .015+.003*time, -.01+.002*time)
    slope_rate = np.where(left, .003, .002)
    curvature = np.where(left, .004, -.003)
    cubic = np.where(left, -.002, .001)
    scalar = slope*offset+curvature*offset**2/2+cubic*offset**3/6
    rates = slope_rate*offset-velocity*(slope+curvature*offset+cubic*offset**2/2)
    return np.append(scalar, position), np.append(rates, velocity)


def main():
    evidence = EvidenceRun('annular-continuum-moving-force-limit-attempt01', __file__)
    try:
        for count in [17, 33, 65, 129, 257, 513, 1025]:
            for gram in [False, True]:
                system = SparseRepairedCut(count, gram, order=10)
                for phase in [.2, .5, .8]:
                    for velocity in [.03, .25]:
                        position = 6.+phase*system.spacing
                        coordinates, rates = manufactured(system, 0., position, velocity)
                        step = 1e-24
                        changed_coordinates, changed_rates = manufactured(system, 1j*step, position, velocity)
                        momentum_rate = system.evaluate(1j*step, changed_coordinates, changed_rates)['field_momenta'][-1].imag/step
                        coordinate_force = system.source_covector(0., coordinates, rates, wave=True)
                        force = coordinate_force-momentum_rate
                        coefficient = system.coefficient(0., position)
                        continuum = .5*(coefficient-position**4*velocity**2/coefficient)*(.015**2-.01**2)
                        static_only = .5*coefficient*(.015**2-.01**2)
                        row = dict(count=count, spacing=system.spacing, phase=phase, velocity=velocity,
                                   branch='MTS' if gram else 'reference', force=float(force), continuum=float(continuum),
                                   absolute_error=float(abs(force-continuum)), relative_error=float(abs(force-continuum)/abs(continuum)),
                                   source_field_momentum_rate=float(momentum_rate), static_factor_error=float(abs(static_only-continuum)))
                        evidence.report['cases'].append(row)
                evidence.save()
        limits = {}
        for branch in ['reference', 'MTS']:
            worst = [max(row['absolute_error'] for row in evidence.report['cases'] if row['branch'] == branch and row['count'] == count)
                     for count in [17, 33, 65, 129, 257, 513, 1025]]
            order = float(np.log2(worst[-2]/worst[-1]))
            finest = [row for row in evidence.report['cases'] if row['branch'] == branch and row['count'] == 1025]
            relative = max(row['relative_error'] for row in finest)
            limits[branch] = dict(worst_errors=worst, final_order=order, finest_relative_error=relative)
            evidence.check(branch+'_full_moving_force_first_order_or_better', order > .8, limits[branch])
            evidence.check(branch+'_finest_relative_force_gate', relative < .005, limits[branch])
            fast = [row for row in finest if row['velocity'] == .25]
            evidence.check(branch+'_static_pressure_factor_is_not_adequate', all(row['static_factor_error'] > 20*row['absolute_error'] for row in fast))
        evidence.report.update(scope='Manufactured piecewise smooth moving zero-trace histories on a time-dependent curved metric; local force consistency, not an evolving waveform theorem.',
                               refinements=limits, phase_margin=.2,
                               physical_force_uses_L_b_minus_zeta_dot=True,
                               all_Gram_factors_retained=True,
                               conditional_force_bound='For bounded one-sided spatial/time jets, smooth positive metric and fixed phase margin: F_h-F_cont=O(h), including source kinetic momentum and the full lifted Gram contribution.',
                               original_factory_future_dtype_warning='Inherited SciPy sparse integer-to-float FutureWarning; explicit dense equivalence checked separately, no executed source changed.',
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        print(limits, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
