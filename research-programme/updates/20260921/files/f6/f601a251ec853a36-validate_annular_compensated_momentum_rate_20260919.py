from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_compensated_momentum_rate_20260919 import compensated_acceleration, velocity_energy_rate
from validate_annular_canonical_driver_residual_20260919 import banded
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-compensated-rate-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            independent_dense_derivative_controls=True, all_four_omission_negative_controls=True)
        generator = np.random.default_rng(2026091902)
        for case in range(4):
            count = 8
            lower = np.diag(generator.uniform(.8, 1.4, count))+np.diag(generator.normal(0., .2, count-1), -1)
            mass = lower @ lower.T
            mass_rate = np.diag(generator.normal(size=count))
            cross, cross_rate = generator.normal(size=(2, count))
            rates, acceleration = generator.normal(size=(2, count+1))
            residual_rate = .1*generator.normal(size=count)
            force = mass @ acceleration[:-1]+mass_rate @ rates[:-1]+cross_rate*rates[-1]+cross*acceleration[-1]+residual_rate
            data = dict(mass_bands=banded(mass), cross=cross)
            result = compensated_acceleration(data, rates, force, banded(mass_rate), cross_rate, acceleration[-1], residual_rate)
            error = float(max(abs(result['acceleration']-acceleration[:-1])))
            evidence.check(str(case)+'_dense_independent_acceleration_identity', error < 4e-14, error)
            for name in ['cross_transport', 'source_acceleration', 'mass_transport', 'inverse_residual']:
                evidence.check(str(case)+'_omitting_'+name+'_fails', np.linalg.norm(result['channels'][name]) > 1e-3)
            difference = generator.normal(size=count)
            difference_rate = generator.normal(size=count)
            energy = velocity_energy_rate(data['mass_bands'], banded(mass_rate), difference, difference_rate)
            expected = float(difference @ mass @ difference_rate+.5*difference @ mass_rate @ difference)
            evidence.check(str(case)+'_energy_identity_and_absolute_bound', abs(energy['total_rate']-expected) < 3e-14
                and abs(expected) <= energy['absolute_bound']+3e-14 and energy['energy'] > 0.)
            other_mass = np.diag(generator.uniform(.7, 1.5, count))
            other_cross = generator.normal(size=count)
            other_rates = generator.normal(size=count+1)
            other_residual = generator.normal(size=count)*.01
            residual = generator.normal(size=count)*.01
            momenta = mass @ rates[:-1]+cross*rates[-1]+residual
            other_momenta = other_mass @ other_rates[:-1]+other_cross*other_rates[-1]+other_residual
            mass_mid = (mass+other_mass)/2
            rates_mid = (rates+other_rates)/2
            cross_mid = (cross+other_cross)/2
            step = .025
            finite = compensated_acceleration(dict(mass_bands=banded(mass_mid), cross=cross_mid), rates_mid,
                (other_momenta-momenta)/(2*step), banded((other_mass-mass)/(2*step)),
                (other_cross-cross)/(2*step), (other_rates[-1]-rates[-1])/(2*step), (other_residual-residual)/(2*step))
            finite_error = float(max(abs(finite['acceleration']-(other_rates[:-1]-rates[:-1])/(2*step))))
            evidence.check(str(case)+'_finite_centered_product_identity', finite_error < 1e-12, finite_error)
            evidence.report['cases'].append(dict(fixture=case, acceleration_error=error,
                centered_product_error=finite_error, **energy, valid_for_claim=False))
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
