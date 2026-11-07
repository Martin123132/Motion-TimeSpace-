from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authorities', nargs='+', required=True)
    parser.add_argument('--reader', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    hashes, reports, tables = {}, {}, {}

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope evidence: '+str(path))
        relative = str(path.relative_to(root))
        if relative not in hashes:
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[relative] != expected:
            raise RuntimeError('Evidence changed: '+relative)

    prior_path = intake/'annular-wave-flux-stage-integrity-20260929.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete' or not prior['fine_wave_two_pairs_each_passed'] or not prior['fine_live_update_complete']:
        raise RuntimeError('Prior wave seal incomplete')
    own(prior_path)
    for relative, expected in prior['hashes'].items():
        if relative != 'CURRENT_LOCAL_RESUME.md':
            own(root/relative, expected)
    replay_path = intake/'annular-wave-recovery-preflight-history-attempt02/status.json'
    replay_report = json.loads(replay_path.read_text())
    if replay_report['state'] != 'complete' or not all(row['passed'] for row in replay_report['checks']):
        raise RuntimeError('Historical status replay incomplete')
    replay = replay_report['historical_input_replay']
    if replay['owner'] != str((intake/'annular-wave-flux-events-reference-third-attempt02/status.json').relative_to(root)) or replay['original_path'] != str((intake/'annular-wave-flux-events-reference-third-attempt01/status.json').relative_to(root)):
        raise RuntimeError('Unexpected historical status alias')
    own(replay_path)
    own(root/replay['recovered_snapshot'], replay['expected_sha256'])
    replay_hits = 0
    for name in args.authorities:
        path = intake/name/'status.json'
        status = json.loads(path.read_text())
        if status['state'] not in ['complete', 'failed']:
            raise RuntimeError('Unsettled authority: '+name)
        if status['state'] == 'complete' and not all(row['passed'] for row in status['checks']):
            raise RuntimeError('False completion: '+name)
        if any(status.get(key, False) for key in ['accepted_for_C0', 'valid_for_physics_claim', 'full_GR_limit_proven']):
            raise RuntimeError('Unexpected promotion: '+name)
        own(path)
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative != 'CURRENT_LOCAL_RESUME.md':
                    if category == 'inputs' and str(path.relative_to(root)) == replay['owner'] and relative == replay['original_path']:
                        if expected != replay['expected_sha256']:
                            raise RuntimeError('Historical input digest changed')
                        own(root/replay['recovered_snapshot'], expected)
                        replay_hits += 1
                    else:
                        own(root/relative, expected)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root/relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: '+relative)
                    if any(row.get('valid_for_claim', 'false').lower() != 'false' for row in rows):
                        raise RuntimeError('Unexpected public claim: '+relative)
                    tables[relative] = len(rows)
        log = intake/(name+'.log')
        if log.is_file():
            own(log)
        reports[name] = dict(state=status['state'], checks=len(status['checks']), cases=len(status['cases']),
            error=status.get('error'), all_fresh_equation_checks_passed=status.get('all_fresh_equation_checks_passed'),
            summaries=[row.get('summary', row) for row in status['cases']])
    for name in ['DERIVATION-20260930-refined-wave-and-fresh-Euler-check.md', 'OPERATIONS-20260930-refined-wave-recovery.md', args.reader]:
        path = root/name
        own(path)
        for citation in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz', '.csv')) and not (root/citation).is_file():
                raise RuntimeError('Missing citation: '+citation)
    names = ['diagnose_annular_wave_flux_third_20260930.py', 'diagnose_annular_wave_flux_third_recovery_20260930.py',
        'archive_annular_recovery_preflight_history_20260930.py', 'archive_annular_recovery_preflight_history_v2_20260930.py',
        'assemble_annular_wave_flux_third_candidates_20260930.py',
        'derive_annular_wave_flux_third_response_20260930.py',
        'annular_position_reaction_registered_20260930.py',
        'validate_annular_flux_corrected_Euler_20260930.py',
        'seal_annular_refined_wave_stage_20260930.py']
    for name in names:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root/'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache')
    since = datetime.fromisoformat('2026-09-29T23:48:55+00:00').timestamp()
    changed = [str(path) for path in (root.parent/'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench modified: '+repr(changed))
    own(root/'CURRENT_LOCAL_RESUME.md')
    for name in ['save_annular_wave_rule_boundary_20260930.ps1', 'save_annular_wave_rule_boundary_v2_20260930.ps1']:
        own(root/'scripts'/name)
    paired_names = ['annular-wave-flux-events-reference-third-attempt03', 'annular-wave-flux-events-MTS-third-attempt02']
    third_pairs = all(name in reports and reports[name]['state'] == 'complete' and reports[name]['cases'] == 3
        and all(row['pair_passed'] for row in reports[name]['summaries'][1:]) for name in paired_names)
    forcing = reports.get('annular-wave-flux-third-candidates-attempt01', {})
    response = reports.get('annular-wave-flux-live-response-third-attempt01', {})
    fresh_cases = [row for name, item in reports.items() if name.startswith('annular-flux-corrected-Euler-')
        and item['state'] == 'complete' and item['all_fresh_equation_checks_passed'] for row in item['summaries']]
    fresh_keys = {(row['branch'], row['level']) for row in fresh_cases}
    fine_fresh_complete = all((branch, 'fine') in fresh_keys for branch in ['reference-reference', 'MTS-primary'])
    fresh_complete = all((branch, level) in fresh_keys for branch in ['reference-reference', 'MTS-primary'] for level in ['fine', 'third'])
    if replay_hits != 1:
        raise RuntimeError('Historical status alias not consumed exactly once')
    report = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=reports, csv_tables=tables,
        csv_rows=sum(tables.values()), scripts_compiled=len(names), accepted_for_C0=False,
        fine_wave_two_pairs_each_passed=prior['fine_wave_two_pairs_each_passed'],
        fine_live_update_complete=prior['fine_live_update_complete'], third_wave_two_pairs_each_passed=third_pairs,
        third_combined_forcing_pairs_passed=forcing.get('state') == 'complete' and forcing.get('cases') == 2
            and all(row['combined_forcing_pair_passed'] for row in forcing.get('summaries', [])),
        third_live_update_complete=response.get('state') == 'complete' and response.get('cases') == 2,
        all_four_fresh_Euler_checks_complete_and_passed=fresh_complete,
        fine_fresh_Euler_checks_complete_and_passed=fine_fresh_complete,
        unchanged_force_components_reused=True, all_force_components_newly_integrated=False,
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False,
        historical_mutable_status_replay=replay,
        github_action=False, subagents_used=False)
    with (intake/args.output).open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'authorities', 'csv_tables']}))


if __name__ == '__main__':
    main()
