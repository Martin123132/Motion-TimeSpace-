from __future__ import annotations

import csv
from pathlib import Path

from bound_common import ROOT, PARENT, read_json, digest, modest_process, save


def main():
    modest_process()
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))
        assert passed, (name, value)

    exact_total = 0
    for label, count in [('completion', 7), ('vacuum', 8), ('uniform', 6), ('phase-block', 4)]:
        report = read_json(ROOT/'results'/label/'status.json')
        check(label+' exact identities', len(report['exact_checks']) == count and all(row['passed'] and row['residual'] == '0' for row in report['exact_checks']))
        exact_total += count
    check('local completion does not freeze K', read_json(ROOT/'results/completion/status.json')['frozen_K_completion_negative_control_detected'])
    uniform = read_json(ROOT/'results/uniform/status.json')
    bound = uniform['rational_bounds']
    check('positive analytic metric floor', bound['metric_lower']['numeric'] > .73)
    check('uniform phase-completed elliptic bound', bound['phase_load_upper']['numeric'] < .6)
    check('uniform bare scalar energy bound', bound['scalar_load_upper']['numeric'] < 1.06)
    check('saved candidate falls inside explicit box', uniform['saved_background_membership']['inside_box'])
    check('background existence not silently certified', uniform['background_existence_proved'] is False)
    phase = read_json(ROOT/'results/phase-block/status.json')
    check('actual reduced phase block uniformly coercive', phase['phase_coercivity_numeric'] > .77)
    check('phase proof does not use spatial sampling', phase['spatial_sampling_used'] is False)
    background = read_json(ROOT/'results/background/status.json')
    for row in background['rows']:
        check(str(row['cells'])+' sampled phase load inside majorant', row['max_phase_load'] < bound['phase_load_upper']['numeric'])
        check(str(row['cells'])+' sampled scalar load inside majorant', row['max_scalar_load'] < bound['scalar_load_upper']['numeric'])
        check(str(row['cells'])+' sampled background signs', row['min_metric'] > 0 and row['max_metric'] < 1 and row['min_lapse_gradient'] > 0 and row['max_field_gradient'] < 0)
    for row in background['form_rows']:
        check(str(row['cells'])+' scalar factorization replay', row['scalar_ground_state_relative_error'] < 1e-10, row['scalar_ground_state_relative_error'])
        check(str(row['cells'])+' shifted constraint replay', row['phase_ground_state_relative_error'] < 1e-10)
    schur = read_json(ROOT/'results/schur/status.json')
    for row in schur['rows']:
        check(row['label']+' exact phase square replay', row['phase_square_completion_error'] < 1e-12)
        check(row['label']+' discrete relative coupling below one', 0 < row['gravity_scalar_contraction'] < 1)
        check(row['label']+' normalized Schur identity', abs(row['scalar_schur_relative_bound']-row['independent_scalar_schur_relative_min']) < 1e-9)
        check(row['label']+' not labelled continuum bound', row['is_continuum_bound'] is False)
    replay = read_json(ROOT/'results/replay/status.json')
    by_label = {row['label']:row for row in replay['phase_rows']}
    for row in replay['phase_rows']:
        check(row['label']+' full phase energy identity', row['bulk_integration_identity_relative_error'] < 1e-12)
    ratios = []
    for coarse, fine in [('standard', 'refined-mesh'), ('resolved-more', 'resolved-mesh'), ('resolved-support', 'support-mesh')]:
        ratio = by_label[coarse]['weighted_constraint_relative_residual']/by_label[fine]['weighted_constraint_relative_residual']
        ratios.append(ratio)
        check(coarse+' weighted source converges quadratically', 3.9 < ratio < 4.1, ratio)
    for index, row in enumerate(replay['vacuum_rows']):
        check(str(index)+' vacuum energy contact match', row['matched_relative_error'] < 1e-10)
        check(str(index)+' contact omission detected', row['contact_omission_relative_error'] > 1)
        check(str(index)+' finite-inner-boundary ADM energy not mistaken for positive master bulk', row['original_ADM_energy'] < 0 and row['positive_master_bulk'] > 0)
    inputs = []
    for path in ROOT.rglob('*.json'):
        inputs.append(path)
        report = read_json(path)
        assert report['state'] == 'complete'
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    check('no bytecode caches', not list(ROOT.rglob('__pycache__')))
    report = save('validation', Path(__file__), dict(checks=checks, validation_checks=len(checks), exact_checks=exact_total,
        phase_coercivity_lower=.77, bare_scalar_angular_margin=2.94, shifted_constraint_angular_margin=5.4,
        proof_scope='Uniform bounds for regular positive compact solutions within alpha<=.0002,R<=20,b(0)<=1.1; not an existence enclosure.',
        finest_discrete_contraction=schur['rows'][-1]['gravity_scalar_contraction'],
        finest_discrete_scalar_schur_margin=schur['rows'][-1]['scalar_schur_relative_bound'],
        contraction_is_continuum_upper_bound=False, full_joint_even_block_coercivity_proved=False,
        weighted_source_halving_ratios=ratios, vacuum_contact_replays=len(replay['vacuum_rows']),
        new_background_or_wave_solves=0, csv_rows=len(schur['rows'])), inputs)
    with (ROOT/'results/validation/schur-summary.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(schur['rows'][0]))
        writer.writeheader()
        writer.writerows(schur['rows'])
    print(dict(state=report['state'], checks=len(checks), exact_checks=exact_total,
        analytic_phase_margin=.77, discrete_coupling=report['finest_discrete_contraction']), flush=True)


if __name__ == '__main__':
    main()
