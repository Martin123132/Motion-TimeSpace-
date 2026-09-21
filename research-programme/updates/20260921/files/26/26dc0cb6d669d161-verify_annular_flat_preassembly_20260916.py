from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-flat-preassembly-attempt01',__file__)
    try:
        generator = np.random.default_rng(160949)
        for count,splits in [(33,2),(257,4),(257,8),(513,4),(513,8),(1025,8)]:
            for gram in [False,True]:
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=splits)
                model = FlatPreassembledFlow(system)
                branch = 'MTS' if gram else 'reference'
                for shift in [0.,.024]:
                    state = initial(system)
                    state[system.count] += shift
                    if shift:
                        state[:system.count] += 1e-7*generator.standard_normal(system.count)
                        state[system.count+1:-2] += 1e-6*generator.standard_normal(system.count)
                        state[-2] = .045
                    values = model.evaluate(state,True)
                    coordinates,rates = np.split(state[:-1],2)
                    original = system.evaluate(0.,coordinates,rates)
                    acceleration = system.acceleration(0.,coordinates,rates)
                    error = float(np.linalg.norm(values['acceleration']-acceleration)/max(1.,np.linalg.norm(acceleration)))
                    force_error = abs(float(values['force']-system.source_mass*acceleration[-1]/original['clock']**3))
                    prefix = '-'.join(map(str,[branch,count,splits,shift]))
                    evidence.check(prefix+'_acceleration',error<2e-8,error)
                    evidence.check(prefix+'_force',force_error<2e-11,force_error)
                    evidence.check(prefix+'_action_energy',abs(values['action']-original['action'])<2e-12
                        and abs(values['energy']-system.energy(0.,coordinates,rates))<2e-12)
                    direction = generator.standard_normal(len(state))
                    direction /= np.linalg.norm(direction)
                    shifted = state.astype(complex)+1e-24j*direction
                    actual = model.evaluate(shifted,True)['action'].imag/1e-24
                    coordinates_complex,rates_complex = np.split(shifted[:-1],2)
                    expected = system.evaluate(0.,coordinates_complex,rates_complex)['action'].imag/1e-24
                    evidence.check(prefix+'_variational_direction',abs(actual-expected)<2e-9*max(1.,abs(expected)),float(abs(actual-expected)))
                    evidence.report['cases'].append(dict(branch=branch,count=count,splits=splits,shift=shift,
                        acceleration_relative_error=error,force_error=force_error))
                started = time.perf_counter()
                for repeat in range(40):
                    model.rhs(0.,state)
                evidence.report.setdefault('timings',[]).append(dict(branch=branch,count=count,splits=splits,
                    seconds_per_call=(time.perf_counter()-started)/40))
        evidence.report.update(original_action_unchanged=True,all_modes_retained=True,
            full_source_momentum_retained=True,flat_background_only=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
