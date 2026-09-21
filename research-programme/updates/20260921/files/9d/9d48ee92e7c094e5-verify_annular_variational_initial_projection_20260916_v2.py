from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_variational_initial_projection_20260916_v2 import variational_initial
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import initial,diagnostics,field_comparison
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
import numpy as np
import json


def main():
    evidence = EvidenceRun('annular-variational-initial-projection-attempt02',__file__)
    try:
        evidence.own(evidence.root/'scripts/annular_variational_initial_projection_20260916.py')
        evidence.own(evidence.root/'source-intake/navier-stokes/20260914/annular-variational-initial-projection-attempt01/status.json')
        prior_path = evidence.root/'source-intake/navier-stokes/20260914/annular-quadratic-crossing-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.check('previous_checkpoint_sealed',prior['state'] == 'complete' and all(row['passed'] for row in prior['checks']))
        evidence.own(prior_path)
        oracle_path = evidence.root/'source-intake/navier-stokes/20260914/annular-source-fitted-fine-crossing-attempt01/oracle-512.npz'
        evidence.own(oracle_path)
        oracle_state = np.load(oracle_path)['states'][0]
        oracle = TwoSidedGRCharacteristics(512,mass=0.)
        for degree,constructor in [(1,SourceFittedAction),(2,QuadraticSourceFittedAction)]:
            for count in [33,65,129,257,513,1025]:
                for gram in [False,True]:
                    branch = 'MTS' if gram else 'reference'
                    system = constructor(count,gram,background_mass=0.)
                    old = initial(system)
                    variants = []
                    for configuration,velocity in [(False,False),(False,True),(True,False),(True,True)]:
                        state,projection = variational_initial(system,configuration,velocity)
                        diagnostic = diagnostics(system,np.array([0.]),state[None,:])
                        field_error = field_comparison(system,state,oracle,oracle_state,order=24)
                        variant = dict(configuration=configuration,velocity=velocity,projection=projection,
                            force=diagnostic['final_force'],maximum_euler_residual=diagnostic['maximum_euler_residual'],field_error=field_error,
                            initial_force_gate=bool(abs(diagnostic['final_force']) < 2e-7),state_finite=bool(np.isfinite(state).all()))
                        variants.append(variant)
                        if configuration and velocity:
                            check = projection['configuration_normal_residual'] < 2e-9 and projection['velocity_normal_residual'] < 2e-11
                            evidence.check(str(degree)+branch+str(count)+'_variational_normal_equations',check,projection)
                            evidence.check(str(degree)+branch+str(count)+'_original_source_and_finite_state',np.isfinite(state).all()
                                and state[system.count] == 6.03 and state[2*system.count+1] == .06 and state[-1] == 0.)
                            destination = evidence.output/('degree'+str(degree)+'-'+branch+'-'+str(count)+'.npz')
                            np.savez_compressed(destination,state=state)
                            evidence.own(destination,'outputs')
                    row = dict(degree=degree,count=count,scalar_dofs=system.count,branch=branch,variants=variants)
                    evidence.report['cases'].append(row)
                    evidence.save()
                    print(json.dumps(dict(degree=degree,count=count,branch=branch,forces=[item['force'] for item in variants],fields=[item['field_error'] for item in variants])),flush=True)
        evidence.report.update(scope='Action-metric Ritz and kinetic projection of the same analytic initial profile; initial controls only, not a moving-source evolution pass.',
            original_physical_profile_and_velocity_preserved=True,no_force_zero_constraint=True,
            projected_source_reaction_is_action_derived=True,live_quadratic_geometry_qualified=False,
            uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
