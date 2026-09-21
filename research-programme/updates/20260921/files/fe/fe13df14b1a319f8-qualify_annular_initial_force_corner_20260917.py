from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import InitialPrimitives
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint
from annular_instantaneous_force_bridge_20260917 import force_diagnostics, reference_force_rate
from run_annular_source_fitted_crossing_20260915 import initial
import argparse
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_forward_trajectory_rerun=True, initial_data_only=True, old_peak_force_gates_unchanged=True,
            finite_initial_rate_limit_not_proven=True, sampled_scaling_not_uniform_bound=True,
            original_incompatible_corner_retained=True, initial_data_not_replaced=True)
        radius, speed, slope = sp.symbols('radius speed slope', positive=True)
        left_rate = slope*(2+speed)*(speed-1)/(radius*(1+speed))-slope*speed/radius
        right_rate = slope*(2-speed)*(speed+1)/(radius*(1-speed))-slope*speed/radius
        initial_force_rate = radius**2*(1-speed**2)*slope*(left_rate-right_rate)
        evidence.check('exact_reference_initial_force_slope', sp.simplify(initial_force_rate+4*radius*slope**2) == 0)
        corner = sp.Rational(2)*sp.Rational(1, 100)/sp.Rational(603, 100)
        evidence.check('unchanged_source_corner_defect', corner == sp.Rational(2, 603))
        reference_rate = reference_force_rate(0., np.array([6.03, .06, 0.]), InitialPrimitives())['rate']
        evidence.check('symbolic_numeric_reference_rate', abs(reference_rate+.002412) < 3e-17)
        evidence.report.update(reference_initial_force_rate=reference_rate,
            original_initial_corner_curvature_defect=float(corner))
        for count in [33, 65, 129, 257, 513, 1025, 2049, 4097, 8193]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(count, gram, background_mass=0., source_splits=8)
                adjoint = MatrixFreeAdjoint(FlatPreassembledFlow(system))
                state = initial(system)
                data = force_diagnostics(adjoint, state)
                key = branch+str(count)
                evidence.check(key+'_complex_derivative', abs(data['rate']-data['complex_rate']) < 3e-10)
                evidence.check(key+'_canonical_pairing', abs(data['rate']-data['canonical_rate']) < 3e-10)
                evidence.check(key+'_positive_sensitivity', data['energy_dual_sensitivity'] > 0
                    and np.isfinite(list(data.values())).all())
                phase = (system.anchor-system.base_radii[0])/system.gram_spacing
                row = dict(branch=branch, base_count=count, h=system.gram_spacing, source_phase=float(phase-np.floor(phase)),
                    initial_force=data['force'], initial_force_rate=data['rate'],
                    initial_force_rate_error=data['rate']-reference_rate,
                    energy_dual_sensitivity=data['energy_dual_sensitivity'],
                    h_times_energy_dual_sensitivity=system.gram_spacing*data['energy_dual_sensitivity'],
                    canonical_flow_energy_norm=data['canonical_flow_energy_norm'])
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
