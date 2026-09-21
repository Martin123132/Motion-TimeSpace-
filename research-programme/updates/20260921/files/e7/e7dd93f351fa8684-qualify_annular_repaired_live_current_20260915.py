from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem
from annular_repaired_live_current_20260915 import LiveTangent
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-repaired-live-current-attempt01', __file__)
    try:
        targets = np.unique(np.concatenate([np.linspace(5.31, 6.69, 9), [5.995, 6.005, 6.021, 6.026, 6.031, 6.036, 6.039, 6.095]]))
        for gram in [False, True]:
            started = time.perf_counter()
            system = RepairedLiveSystem(17, gram, 8, 10)
            coordinates, momenta, unused, unused2 = system.initial()
            tangent = LiveTangent(system, coordinates, momenta)
            comparison = tangent.compare(targets)
            balances = [tangent.noether(offset) for offset in np.linspace(-.5, .5, 7)]
            row = dict(branch='MTS' if gram else 'reference', current_error=comparison['error'],
                       on_shell_current_error=comparison['on_shell_error'],
                       material_Euler_current_correction=comparison['current_euler_correction'],
                       maximum_mass_rate=float(np.max(abs(comparison['radial_time_derivative']))),
                       maximum_wave_current=float(np.max(abs(comparison['wave']))),
                       noether_error=max(item['noether'] for item in balances),
                       scalar_Euler_error=max(item['scalar_euler'] for item in balances),
                       source_Euler_error=max(item['source_euler'] for item in balances),
                       seconds=time.perf_counter()-started)
            evidence.report['cases'].append(row)
            raw = evidence.output/(row['branch']+'.npz')
            np.savez_compressed(raw, **comparison, coordinates=coordinates, momenta=momenta,
                                rates=tangent.rates, forces=tangent.forces, acceleration=tangent.acceleration)
            evidence.own(raw, 'outputs')
            print(row, flush=True)
            evidence.check(row['branch']+'_off_shell_moving_Noether', row['noether_error'] < 2e-9, row)
            evidence.check(row['branch']+'_canonical_tangent_equations', max(row['scalar_Euler_error'], row['source_Euler_error']) < 2e-8, row)
            evidence.check(row['branch']+'_independent_temporal_mass_equation', row['on_shell_current_error'] < 2e-8, row)
            evidence.check(row['branch']+'_nonzero_mass_and_wave_transport', row['maximum_mass_rate'] > 1e-4 and row['maximum_wave_current'] > 1e-9, row)
        evidence.report.update(live_repaired_canonical_tangent_tested=True,
                               current_imposed_or_energy_projected=False,
                               current_from_differentiated_radial_constraint=False,
                               material_label_collocation_not_exact_variational_truncation=True,
                               finite_difference_step=2e-5, live_evolution_completed=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
