from derive_annular_source_gravity_20260914 import EvidenceRun
from fractions import Fraction
import contextlib
import csv
import hashlib
import json


def verified_status(evidence, name):
    path = evidence.output.parent/name/'status.json'
    status = json.loads(path.read_text())
    evidence.own(path)
    if status['state'] != 'complete':
        raise RuntimeError('Source run is not complete: '+name)
    root = evidence.output.parents[3]
    for category in ['inputs', 'outputs']:
        for relative, expected in status[category].items():
            source = root/relative
            if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                raise RuntimeError('Changed input: '+str(source))
            evidence.own(source)
    return status


def main():
    evidence = EvidenceRun('annular-P2-evolved-force-error-split-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, duration=4e-5,
            saved_state_algebra_only=True, new_evolution_performed=False,
            holding_drives_fixed_is_not_a_dynamical_Q_zero_limit=True,
            continuum_oracle_error_not_certified=True)
        for sign in [-1, 1]:
            inertia, projection = Fraction(7, 3), Fraction(2, 5)
            wave, dust = Fraction(sign*11, 13), Fraction(17, 19)
            force = (inertia*wave-projection*dust)/(inertia+projection)
            correction = -projection*(wave+dust)/(inertia+projection)
            evidence.check('rational_identity_sign_'+str(sign), force == wave+correction)
            evidence.check('omitted_projection_negative_control_'+str(sign), force != wave)
        rows = []
        for branch, attempt in [('reference', '01'), ('MTS', '02')]:
            name = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+attempt
            status = verified_status(evidence, name)
            target = status['continuum_force']
            final = status['cases'][-1]
            cases = [(4e-5, status['baseline_force'], status['baseline_force_decomposition']['schur'], 'RK'),
                (2e-5, final['force'], final['schur'], 'exponential32')]
            for source_cap, measured, schur, method in cases:
                inertia = schur['dust_inertia']
                projection = schur['field_projection_inertia']
                wave = schur['free_wave_drive']
                dust = schur['dust_drive']
                correction = -projection*(wave+dust)/(inertia+projection)
                direct = (inertia*wave-projection*dust)/(inertia+projection)
                algebra_difference = abs(direct-wave-correction)
                identity_residual = measured-wave-correction
                drive_gap = wave-target
                error = measured-target
                upper = abs(drive_gap)+abs(correction)+abs(identity_residual)
                lower = max(0., abs(drive_gap)-abs(correction)-abs(identity_residual))
                key = branch+'_'+str(source_cap)
                evidence.check(key+'_positive_inertias', inertia > 0 and projection >= 0)
                evidence.check(key+'_Schur_algebra', algebra_difference < 1e-20
                    and abs(direct-schur['predicted_reduced_force']) < 1e-20
                    and abs(identity_residual) < 2e-9)
                evidence.check(key+'_two_sided_triangle_bound',
                    lower <= abs(error)+1e-20 and abs(error) <= upper+1e-20)
                evidence.check(key+'_signed_error_decomposition',
                    abs(error-drive_gap-correction-identity_residual) < 1e-20)
                row = dict(branch=branch, source_cap=source_cap, method=method,
                    force=measured, continuum_force=target, force_error=error,
                    free_wave_drive=wave, drive_gap=drive_gap,
                    field_projection_inertia=projection, dust_inertia=inertia,
                    projection_correction=correction, force_identity_residual=identity_residual,
                    noncancellation_upper=upper, reverse_triangle_lower=lower,
                    correction_fraction_of_observed_error=abs(correction)/abs(error),
                    valid_for_claim=False,
                    source_path=str((evidence.output.parent/name/'status.json').relative_to(evidence.output.parents[3])))
                rows.append(row)
        table = evidence.output/'saved-force-error-split.csv'
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(table, 'outputs')
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        evidence.check('four_nonclaim_CSV_rows', len(parsed) == 4
            and all(None not in row and row['valid_for_claim'] == 'False' for row in parsed))
        evidence.report['cases'] = rows
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), rows=rows)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
