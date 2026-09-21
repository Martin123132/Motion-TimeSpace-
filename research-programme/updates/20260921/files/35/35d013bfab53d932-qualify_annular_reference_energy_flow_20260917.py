from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from annular_characteristic_galerkin_defect_20260917 import nodal_reference, canonical_defect, mass_dual_norm
from run_annular_source_fitted_crossing_20260915 import initial
import argparse
import json
import numpy as np


def momenta(model, state):
    count = model.count
    field, position, rate, speed = state[:count], state[count], state[count+1:-2], state[-2]
    data = model.matrices(position)
    cross = band_product(data['transport'], field)
    momentum = band_product(data['mass'], rate)+speed*cross
    source = rate @ cross+speed*field @ band_product(data['square'], field)+model.system.source_mass*speed/np.sqrt(1-speed**2)
    return np.append(momentum, source)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_forward_trajectory_rerun=True, passive_clock_defect_zero=True,
            reference_norms_only_not_evolved_MTS_regularity=True, finite_samples_not_uniform_certificate=True,
            canonical_flow_not_velocity_flow=True, full_GR_limit_proven=False)
        path = evidence.root/'source-intake/navier-stokes/20260914/annular-coupled-galerkin-defect-attempt01/status.json'
        evidence.own(path)
        previous = json.loads(path.read_text())
        evidence.check('coupled_defect_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        reference = FullCharacteristicField(tight=True)
        for count in [33, 65, 129, 257, 513, 1025, 2049]:
            cases = []
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(count, gram, background_mass=0., source_splits=8)
                model = FlatPreassembledFlow(system)
                seed, unused = nodal_reference(system, reference, 0.)
                difference = seed-initial(system)
                evidence.check(branch+str(count)+'_original_initial_state', max(abs(difference)) < 2e-12, float(max(abs(difference))))
                for instant in [0., .071, .173, .21, .317, .4]:
                    state, derivative = nodal_reference(system, reference, instant)
                    residual, unused, matrices, unused2 = canonical_defect(model, state, derivative)
                    count_field = system.count
                    field, rate, speed = state[:count_field], state[count_field+1:-2], state[-2]
                    momentum_rate = momenta(model, state.astype(complex)+1e-25j*derivative).imag/1e-25
                    gradient = momentum_rate+residual
                    rate_square = rate @ band_product(matrices['bulk'], rate)+speed**2
                    reference_rate = np.sqrt(rate_square+mass_dual_norm(momentum_rate, matrices)**2)
                    canonical_flow = np.sqrt(rate_square+mass_dual_norm(gradient, matrices)**2)
                    residual_norm = mass_dual_norm(residual, matrices)
                    evidence.check(branch+str(count)+'_'+str(instant)+'_reference_flow_triangle',
                        canonical_flow <= reference_rate+residual_norm+2e-12 and np.isfinite(canonical_flow))
                    cases.append(dict(branch=branch, time=instant, reference_derivative_energy_norm=float(reference_rate),
                        canonical_flow_energy_norm=float(canonical_flow), canonical_residual_norm=residual_norm))
            row = dict(base_count=count, maximum_reference_derivative_norm=max(value['reference_derivative_energy_norm'] for value in cases),
                maximum_reference_canonical_flow_norm=max(value['canonical_flow_energy_norm'] for value in cases), cases=cases)
            evidence.report['cases'].append(row)
            evidence.save()
            print({name: value for name, value in row.items() if name != 'cases'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
