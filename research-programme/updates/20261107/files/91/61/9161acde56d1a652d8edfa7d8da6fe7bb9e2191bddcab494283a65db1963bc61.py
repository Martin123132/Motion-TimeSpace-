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

    prior_path = intake/'annular-native-precision-repair-integrity-20260929.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete' or not prior['native_pairs_passed']:
        raise RuntimeError('Native repair seal incomplete')
    own(prior_path)
    for relative, expected in prior['hashes'].items():
        if relative != 'CURRENT_LOCAL_RESUME.md':
            own(root/relative, expected)
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
            error=status.get('error'), summaries=[row.get('summary', row) for row in status['cases']])
    documents = ['DERIVATION-20260929-actual-wave-flux-integration.md',
        'DERIVATION-20260929-wave-flux-trace-precision.md', 'DERIVATION-20260929-event-split-wave-flux.md',
        'DERIVATION-20260929-wave-support-endpoint-rounding.md',
        'OPERATIONS-20260929-wave-force-workers.md', 'DERIVATION-20260929-wave-flux-live-update.md', args.reader]
    for name in documents:
        path = root/name
        own(path)
        for citation in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz', '.csv')) and not (root/citation).is_file():
                raise RuntimeError('Missing citation: '+citation)
    names = ['annular_wave_flux_form_20260929.py', 'annular_wave_flux_form_v2_20260929.py',
        'diagnose_annular_wave_flux_form_20260929.py', 'diagnose_annular_wave_flux_form_v2_20260929.py',
        'validate_annular_wave_flux_form_20260929.py', 'annular_wave_flux_events_20260929.py',
        'annular_wave_flux_events_v2_20260929.py', 'annular_wave_flux_events_v3_20260929.py',
        'annular_wave_flux_events_v4_20260929.py', 'validate_annular_wave_flux_events_20260929.py',
        'validate_annular_wave_flux_events_v2_20260929.py', 'validate_annular_wave_flux_events_v3_20260929.py',
        'validate_annular_wave_flux_events_v4_20260929.py', 'diagnose_annular_wave_flux_events_20260929.py',
        'diagnose_annular_wave_flux_events_v2_20260929.py', 'diagnose_annular_wave_support_extent_20260929.py',
        'validate_annular_wave_label_partition_20260929.py',
        'assemble_annular_wave_flux_candidates_20260929.py',
        'derive_annular_wave_flux_live_response_20260929.py', 'seal_annular_wave_flux_stage_20260929.py']
    for name in names:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root/'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache')
    since = datetime.fromisoformat('2026-09-29T20:34:27+00:00').timestamp()
    changed = [str(path) for path in (root.parent/'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench modified: '+repr(changed))
    own(root/'CURRENT_LOCAL_RESUME.md')
    paired_names = ['annular-wave-flux-events-reference-attempt02', 'annular-wave-flux-events-MTS-fine-attempt01']
    fine_wave_pairs = len([name for name in paired_names if name in reports]) == 2 and all(
        reports[name]['state'] == 'complete' and len(reports[name]['summaries']) == 3
        and all(row['pair_passed'] for row in reports[name]['summaries'][1:]) for name in paired_names)
    forcing = reports.get('annular-wave-flux-fine-candidates-attempt01', {})
    response = reports.get('annular-wave-flux-live-response-fine-attempt01', {})
    report = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=reports, csv_tables=tables,
        csv_rows=sum(tables.values()), scripts_compiled=len(names),
        actual_flux_by_parts_implemented=True, all_boundary_terms_retained=True,
        native_repair_preserved=True, accepted_for_C0=False, full_live_reaction_recomputed=False,
        fine_wave_two_pairs_each_passed=fine_wave_pairs,
        fine_combined_forcing_pairs_passed=forcing.get('state') == 'complete' and forcing.get('cases') == 2
            and all(row['combined_forcing_pair_passed'] for row in forcing.get('summaries', [])),
        fine_live_update_complete=response.get('state') == 'complete' and response.get('cases') == 2,
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False,
        github_action=False, subagents_used=False)
    with (intake/args.output).open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'authorities', 'csv_tables']}))


if __name__ == '__main__':
    main()
