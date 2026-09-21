from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_test_energy_20260919 import differentiated_energy, energy_growth_bound, whiten, operator_bound
from scipy.linalg import cholesky
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-action-test-energy-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, synthetic_controls_not_physical_evidence=True)
        random = np.random.default_rng(19092026)
        for case in range(4):
            raw = random.normal(size=(8, 8))
            mass = raw.T @ raw+np.eye(8)
            raw = random.normal(size=(8, 8))
            stiffness = raw.T @ raw+2*np.eye(8)
            mass_rate = random.normal(size=(8, 8))
            mass_rate = (mass_rate+mass_rate.T)/2
            stiffness_rate = random.normal(size=(8, 8))
            stiffness_rate = (stiffness_rate+stiffness_rate.T)/2
            displacement,velocity,acceleration,jerk = random.normal(size=(4, 8))
            residual_rate = mass @ jerk+mass_rate @ acceleration+stiffness_rate @ displacement+stiffness @ velocity
            result = differentiated_energy(mass,stiffness,mass_rate,stiffness_rate,displacement,velocity,acceleration,residual_rate)
            direct = float(acceleration @ mass @ jerk+.5*acceleration @ mass_rate @ acceleration
                +velocity @ stiffness @ acceleration+.5*velocity @ stiffness_rate @ velocity)
            evidence.check(str(case)+'_independent_differentiated_energy_identity',abs(direct-result['rate']) < 2e-12)
            for name,value in result['channels'].items():
                evidence.check(str(case)+'_'+name+'_omission_detected',abs(direct-(result['rate']-value)) > 1e-5)
            bound = energy_growth_bound(mass,stiffness,mass_rate,stiffness_rate,displacement,velocity,acceleration,residual_rate)
            evidence.check(str(case)+'_conditional_energy_growth_bound',abs(result['rate']) <= bound['energy_rate_upper_bound'])
            lower = cholesky(mass,lower=True)
            whitened = whiten(mass_rate,lower,lower)
            probe = random.normal(size=8)
            original = np.linalg.solve(lower.T,probe)
            evidence.check(str(case)+'_whitening_orientation',abs(probe @ whitened @ probe-original @ mass_rate @ original) < 2e-13)
            rectangular = random.normal(size=(7, 11))
            constant,vector = operator_bound(rectangular)
            singular = float(np.linalg.svd(rectangular,compute_uv=False)[0]**2)
            evidence.check(str(case)+'_independent_singular_value_and_upper_bound',abs(constant['sharp_squared']-singular) < 2e-12
                and singular <= constant['row_sum_squared_bound']+1e-12)
            evidence.check(str(case)+'_worst_direction_reconstruction',abs(float(np.linalg.norm(rectangular @ vector)**2)-singular) < 2e-12)
            evidence.report['cases'].append(dict(case=case,energy=result['energy'],direct_rate=direct,
                predicted_rate=result['rate'],conditional_upper_bound=bound['energy_rate_upper_bound'],
                operator_sharp_squared=singular,operator_upper_squared=constant['row_sum_squared_bound'],valid_for_claim=False))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
