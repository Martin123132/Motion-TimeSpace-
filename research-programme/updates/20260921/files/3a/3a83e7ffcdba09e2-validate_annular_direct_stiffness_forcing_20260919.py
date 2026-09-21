from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_direct_stiffness_forcing_20260919 import transfer_rate, dual_norm, forcing_constant
from scipy.linalg import cholesky
import contextlib
import json
import numpy as np


def banded(matrix):
    count = len(matrix)
    result = np.zeros((5, count))
    for offset in [-2,-1,0,1,2]:
        columns = np.arange(max(0,-offset),min(count,count-offset))
        result[2+offset,columns] = matrix[columns+offset,columns]
    return result


def main():
    evidence = EvidenceRun('annular-direct-stiffness-forcing-algebra-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,synthetic_controls_not_physical_evidence=True)
        random = np.random.default_rng(19091659)
        for case in range(3):
            masses,mass_rates,stiffnesses,stiffness_rates = [],[],[],[]
            for count in [7,11]:
                off = random.uniform(-.1,.1,count-1)
                mass = np.diag(random.uniform(1.,2.,count))+np.diag(off,1)+np.diag(off,-1)
                mass_rate = np.diag(random.normal(size=count))
                raw = random.normal(size=(count,count))
                stiffness = raw.T @ raw+np.eye(count)
                raw = random.normal(size=(count,count))
                masses.append(mass)
                mass_rates.append(mass_rate)
                stiffnesses.append(stiffness)
                stiffness_rates.append((raw+raw.T)/2)
            interpolation = random.normal(size=(11,7))
            values,velocity = random.normal(size=(2,7))
            result = transfer_rate(banded(masses[0]),masses[1],*mass_rates,*stiffnesses,*stiffness_rates,interpolation,values,velocity)
            inverse = np.linalg.inv(masses[0])
            dense_transport = masses[1] @ interpolation @ inverse
            dense_rate = mass_rates[1] @ interpolation @ inverse-dense_transport @ mass_rates[0] @ inverse
            expected = dense_rate @ stiffnesses[0] @ values+dense_transport @ stiffness_rates[0] @ values
            expected += dense_transport @ stiffnesses[0] @ velocity-stiffness_rates[1] @ interpolation @ values-stiffnesses[1] @ interpolation @ velocity
            evidence.check(str(case)+'_independent_dense_product_rule',np.max(abs(expected-result['derivative'])) < 2e-12)
            for name,channel in result['channels'].items():
                evidence.check(str(case)+'_'+name+'_omission_detected',np.max(abs(expected-(sum(result['channels'].values())-channel))) > 1e-4)
            step = 1e-6
            endpoints = []
            for sign in [-1,1]:
                moved_mass = [mass+sign*step*rate for mass,rate in zip(masses,mass_rates)]
                moved_stiffness = [stiffness+sign*step*rate for stiffness,rate in zip(stiffnesses,stiffness_rates)]
                moved_values = values+sign*step*velocity
                mismatch = moved_mass[1] @ interpolation @ np.linalg.solve(moved_mass[0],moved_stiffness[0])-moved_stiffness[1] @ interpolation
                endpoints.append(mismatch @ moved_values)
            secant = (endpoints[1]-endpoints[0])/(2*step)
            evidence.check(str(case)+'_direct_perturbed_matrix_control',np.max(abs(secant-expected)) < 2e-7)
            mass_lower = cholesky(masses[1],lower=True)
            stiffness_lower = cholesky(stiffnesses[0],lower=True)
            first = forcing_constant(result['mismatch'],mass_lower,stiffness_lower)
            second = forcing_constant(result['mismatch_rate'],mass_lower,stiffness_lower)
            bound = first['upper']*np.sqrt(velocity @ stiffnesses[0] @ velocity)+second['upper']*np.sqrt(values @ stiffnesses[0] @ values)
            norm = dual_norm(mass_lower,expected)
            evidence.check(str(case)+'_coarse_energy_forcing_bound',norm <= bound)
            zero = transfer_rate(banded(masses[0]),masses[1],*mass_rates,
                np.zeros_like(stiffnesses[0]),np.zeros_like(stiffnesses[1]),
                np.zeros_like(stiffnesses[0]),np.zeros_like(stiffnesses[1]),interpolation,values,velocity)
            evidence.check(str(case)+'_absent_sector_exactly_zero',np.max(abs(zero['derivative'])) == 0.)
            evidence.report['cases'].append(dict(case=case,dense_error=float(np.max(abs(expected-result['derivative']))),
                finite_probe_error=float(np.max(abs(secant-expected))),forcing_norm=norm,coarse_energy_bound=float(bound),valid_for_claim=False))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
