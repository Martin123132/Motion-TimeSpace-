from derive_annular_source_gravity_20260914 import EvidenceRun
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-wave-error-energy-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            independent_dense_controls=True, nonnested_transfer_allowed=True, kinetic_potential_exchange_retained=True)
        generator = np.random.default_rng(2026091914)
        for case in range(4):
            coarse_count, fine_count = 5, 8
            matrices = []
            for count in [coarse_count, fine_count]:
                seed = generator.normal(size=(count, count))
                mass = seed @ seed.T+np.eye(count)
                gradient = generator.normal(size=(count+2, count))
                gram = generator.normal(size=(3, count))
                matrices.append((mass, gradient.T @ gradient+gram.T @ gram))
            (coarse_mass, coarse_stiffness), (fine_mass, fine_stiffness) = matrices
            transfer = generator.normal(size=(fine_count, coarse_count))
            covector_map = np.linalg.solve(coarse_mass.T, (fine_mass @ transfer).T).T
            coarse_values, fine_values = generator.normal(size=coarse_count), generator.normal(size=fine_count)
            coarse_extra, fine_extra = generator.normal(size=coarse_count), generator.normal(size=fine_count)
            coarse_acceleration = np.linalg.solve(coarse_mass, -coarse_stiffness @ coarse_values+coarse_extra)
            fine_acceleration = np.linalg.solve(fine_mass, -fine_stiffness @ fine_values+fine_extra)
            displacement = fine_values-transfer @ coarse_values
            acceleration = fine_acceleration-transfer @ coarse_acceleration
            velocity = generator.normal(size=fine_count)
            residual = fine_mass @ acceleration+fine_stiffness @ displacement
            stiffness_transfer = covector_map @ coarse_stiffness @ coarse_values-fine_stiffness @ transfer @ coarse_values
            extra = fine_extra-covector_map @ coarse_extra
            load_error = float(max(abs(residual-stiffness_transfer-extra)))
            mass_rate = generator.normal(size=(fine_count, fine_count))
            mass_rate = (mass_rate+mass_rate.T)/2
            stiffness_rate = generator.normal(size=(fine_count, fine_count))
            stiffness_rate = (stiffness_rate+stiffness_rate.T)/2
            kinetic_rate = float(velocity @ fine_mass @ acceleration+.5*velocity @ mass_rate @ velocity)
            potential_rate = float(velocity @ fine_stiffness @ displacement+.5*displacement @ stiffness_rate @ displacement)
            prediction = float(velocity @ residual+.5*velocity @ mass_rate @ velocity+.5*displacement @ stiffness_rate @ displacement)
            rate_error = abs(kinetic_rate+potential_rate-prediction)
            evidence.check(str(case)+'_stiffness_transfer_load_identity', load_error < 3e-12, load_error)
            evidence.check(str(case)+'_full_energy_rate_identity', rate_error < 3e-11, rate_error)
            evidence.check(str(case)+'_omitting_stiffness_transfer_fails', np.linalg.norm(stiffness_transfer) > .1)
            evidence.check(str(case)+'_omitting_potential_rate_fails', abs(potential_rate) > .1)
            evidence.check(str(case)+'_omitting_stiffness_rate_fails', abs(.5*displacement @ stiffness_rate @ displacement) > .01)
            evidence.check(str(case)+'_positive_energy_for_nonzero_displacement_velocity',
                displacement @ fine_stiffness @ displacement+velocity @ fine_mass @ velocity > 0.)
            evidence.report['cases'].append(dict(fixture=case, load_identity_error=load_error,
                energy_rate_identity_error=rate_error, kinetic_rate=kinetic_rate, potential_rate=potential_rate,
                total_rate=prediction, valid_for_claim=False))
        evidence.check('stationary_unit_oscillator_energy_exchange_is_not_growth',
            abs((-np.sin(.7))*(-np.cos(.7))+np.cos(.7)*(-np.sin(.7))) < 1e-15)
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
