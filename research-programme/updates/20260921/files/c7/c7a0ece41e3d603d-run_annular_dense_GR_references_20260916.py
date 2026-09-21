from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import profile
from scipy.integrate import solve_ivp
import json
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-dense-GR-references-attempt01',__file__)
    try:
        times = np.linspace(0.,.4,81)
        evidence.report.update(configuration=dict(degrees=[384,512,768],rtol=2e-12,atol=2e-14,
            maximum_step='.05/degree',samples=81),same_original_GR_reference=True,continuum_certificate=False)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for degree in [384,512,768]:
            started = time.monotonic()
            model = TwoSidedGRCharacteristics(degree,mass=0.,source=.03)
            radius,unused,unused2 = model.mesh(6.03,.06)
            unused,gradient = profile(radius)
            temporal = -.06*gradient
            fields = np.stack([temporal+gradient,temporal-gradient],axis=1)
            seed = model.pack(fields,np.array([6.03,.03*.06/np.sqrt(1-.06**2),0.]))
            result = solve_ivp(model.rhs,(0.,.4),seed,t_eval=times,method='DOP853',rtol=2e-12,atol=2e-14,max_step=.05/degree)
            evidence.check(str(degree)+'_integration',result.success)
            states = result.y.T
            values = [model.unpack(state) for state in states]
            forces = np.array([model.source_force(value[0],value[1],value[3]) for value in values])
            energies = np.array([model.energy(state)[0] for state in states])
            drift = float(np.max(abs(energies-energies[0]))/abs(energies[0]))
            evidence.check(str(degree)+'_finite_energy_control',np.isfinite(states).all() and drift<2e-6,drift)
            folder = 'annular-crossing-oracle768-attempt01' if degree==768 else 'annular-source-fitted-fine-crossing-attempt01'
            old = intake/folder/('oracle-'+str(degree)+'.npz')
            evidence.own(old)
            with np.load(old,allow_pickle=False) as saved:
                previous = saved['states'].copy()
                evidence.check(str(degree)+'_same_old_times',np.max(abs(saved['times']-times[::10]))<2e-16)
            previous_values = [model.unpack(state) for state in previous]
            previous_force = np.array([model.source_force(value[0],value[1],value[3]) for value in previous_values])
            force_change = float(np.max(abs(forces[::10]-previous_force)))
            evidence.check(str(degree)+'_old_force_time_control',force_change<2e-8,force_change)
            destination = evidence.output/('oracle-'+str(degree)+'.npz')
            np.savez_compressed(destination,times=times,states=states,forces=forces,energies=energies)
            evidence.own(destination,'outputs')
            evidence.report['cases'].append(dict(degree=degree,seconds=time.monotonic()-started,rhs_evaluations=result.nfev,
                old_force_time_change=force_change,energy_relative_drift=drift))
            evidence.save()
            print(evidence.report['cases'][-1],flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
