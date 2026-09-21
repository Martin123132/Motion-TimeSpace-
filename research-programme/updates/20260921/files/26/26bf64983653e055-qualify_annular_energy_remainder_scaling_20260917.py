from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_canonical_energy_20260917 import CanonicalEnergy, dense_bands
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from scipy.linalg import eigh, solve
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            uniform_basic_energy_quadratic_remainder_claimed=False,physical_instability_claimed=False,
            prescribed_flat_background_only=True,interval_arithmetic=False)
        for count in [33,65,129,257]:
            for gram in [False,True]:
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=8)
                model = FlatPreassembledFlow(system)
                energy = CanonicalEnergy(model)
                state = np.zeros(2*(system.count+1)+1)
                state[system.count] = system.anchor
                blocks = energy.evaluate(state)
                matrices = energy.matrices(system.anchor)
                mass = blocks['kinetic'][:-1,:-1]
                stiffness = -blocks['coordinate'][:-1,:-1]
                eigenvalues,eigenvectors = eigh(stiffness,mass,subset_by_index=[system.count-1,system.count-1])
                frequency = float(np.sqrt(eigenvalues[0]))
                mode = eigenvectors[:,0]/frequency
                stiffness_b = dense_bands(matrices['bulk_b'])+(model.lifted.T @ model.lifted.multiply(matrices['gram_b'][:,None])).toarray()
                mass_b = dense_bands(matrices['mass_b'])
                acceleration = solve(mass,stiffness @ mode,assume_a='pos')
                mixed = solve(mass,mass_b @ acceleration-stiffness_b @ mode,assume_a='pos')
                mixed_norm = float(np.sqrt(mixed @ mass @ mixed))
                derivative_errors = []
                for step in [2e-5,1e-5]:
                    probe = np.zeros_like(state)
                    probe[:system.count] = mode
                    values = []
                    for displacement in [-step,step]:
                        moved = state.astype(complex)+1e-25j*probe
                        moved[system.count] += displacement
                        values.append(model.evaluate(moved)['flow'][system.count+1:2*system.count+1].imag/1e-25)
                    approximation = (values[1]-values[0])/(2*step)
                    derivative_errors.append(float(np.sqrt((mixed-approximation) @ mass @ (mixed-approximation))/mixed_norm))
                prefix = str(count)+'_'+('MTS' if gram else 'reference')
                evidence.check(prefix+'_unit_energy_high_mode',abs(mode @ stiffness @ mode-1)<2e-11)
                evidence.check(prefix+'_mixed_source_field_derivative',max(derivative_errors)<2e-7,derivative_errors)
                evidence.report['cases'].append(dict(count=count,branch='MTS' if gram else 'reference',
                    frequency=frequency,mixed_derivative_energy_norm=mixed_norm,
                    mixed_over_frequency=mixed_norm/frequency,
                    independent_derivative_errors=derivative_errors,
                    source_position_direction_energy_norm=1.,field_direction_energy_norm=1.,
                    instability_diagnosis=False))
                evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
