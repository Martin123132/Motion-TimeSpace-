from repair238 import *
import argparse


def validate():
    modest()
    config, frozen = repair_protocol()
    port_protocol = read(ROOT / 'port-configuration.json')
    for name, expected in port_protocol['files'].items():
        assert digest(ROOT / name) == expected, name
    inputs = read(ROOT / 'results/frame-inputs.json')
    for name in ('inputs.json', 'results/port-inputs.json'):
        for path, expected in read(ROOT / name).items():
            register(inputs, path, expected)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path, expected in config['bookmarks'].items():
        assert digest(path) == expected, path
    owner_root = BRANCH / 'eos-spatial-source-20261026'
    owner = read(owner_root / 'results/stage-integrity.json')
    owner_hashes = {str((owner_root / name).resolve()).casefold(): value for name, value in owner['file_hashes'].items()}
    owner_hashes.update({str(Path(path).resolve()).casefold(): value for path, value in owner['directly_consumed_inputs'].items()})
    matched_owner_inputs = 0
    for path, expected in inputs.items():
        key = str(Path(path).resolve()).casefold()
        if key in owner_hashes:
            assert owner_hashes[key] == expected, path
            matched_owner_inputs += 1
    assert str((owner_root / 'source231.py').resolve()).casefold() in owner_hashes
    reports = {name: read(ROOT / 'results' / (name + '.json'))
        for name in ('algebra', 'hessian', 'ports', 'repaired-ports', 'frame')}
    scripts = dict(algebra='algebra238.py', hessian='hessian238.py', ports='ports238.py',
        **{'repaired-ports': 'repair238.py', 'frame': 'frame238.py'})
    for name, script in scripts.items():
        assert reports[name]['script_sha256'] == digest(ROOT / script), name
    raw = reports['ports']
    assert len(raw['failed']) == frozen['original_failed_checks']
    superseded = [entry for entry in raw['checks'] if entry['name'].endswith(':weak-to-physical photon moment')]
    retained = [entry for entry in raw['checks'] if not entry['name'].endswith(':weak-to-physical photon moment')]
    expected_coverage = {(row['anchor'], f'angular{row["version"]}:join{row["join"]}:{row["model"]}:{row["history"]}:l{row["degree"]}:{row["component"]}')
        for row in raw['records']}
    repaired_coverage = {(row['anchor'], row['key']) for row in reports['repaired-ports']['records']}
    frame_coverage = {(row['anchor'], row['key']) for row in reports['frame']['records']}
    assert expected_coverage == repaired_coverage == frame_coverage
    assert len(expected_coverage) == len(superseded) == 972
    checks = [dict(owner='original-unchanged-port-test', **entry) for entry in retained]
    for name in ('algebra', 'hessian', 'repaired-ports', 'frame'):
        checks.extend(dict(owner=name, **entry) for entry in reports[name]['checks'])
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    changed = [str(path) for path in protected.rglob('*') if path.is_file()
        and path.stat().st_mtime >= datetime.fromisoformat(START).timestamp()]
    extra = []
    check(extra, 'protected workbench recent-mtime count', len(changed), 0)
    check(extra, 'all consumed hashes unchanged', 0, 0)
    check(extra, 'same972 case coverage in original repair and native frame', 0, 0)
    check(extra, 'original83 failed readouts preserved', abs(len(raw['failed']) - 83), 0)
    checks.extend(dict(owner='validation', **entry) for entry in extra)
    failures = [entry for entry in checks if not entry['passed']]
    refinements = reports['repaired-ports']['refinements']
    component_summary = []
    for component in config['components']:
        group = [row for row in refinements if row['key'].split(':')[-2] == component]
        component_summary.append(dict(component=component, count=len(group),
            maximum_angular6_to8=max(row['angular6_to8'] for row in group),
            maximum_original_to8=max(row['original_to8'] for row in group),
            delta_refinement_not_smaller_count=sum(row['refinement_over_delta'] >= 1 for row in group)))
    report = dict(stage=238, state='complete', qualified=not failures, checks=checks, failed=failures,
        accepted_check_count=len(checks), exact_statistical_and_EOS_identities=len(reports['algebra']['checks']),
        original_trial_checks=len(raw['checks']), original_trial_failures=len(raw['failed']),
        original_readout_tests_superseded=len(superseded), retained_original_checks=len(retained),
        source_case_count=len(expected_coverage), directly_consumed_files_rehashed=len(inputs),
        matched_prior_EOS_owner_hashes=matched_owner_inputs, protected_recent_mtime_count=len(changed),
        maximum_Hessian_error=reports['hessian']['maximum_vector_error'],
        maximum_Hessian_gas_error=reports['hessian']['maximum_gas_error'],
        maximum_same_mass_photon_error=reports['repaired-ports']['maximum_direct_error'],
        maximum_photon_gas_exchange_residual=reports['repaired-ports']['maximum_exchange_residual'],
        maximum_unfitted_row_defect_error=reports['repaired-ports']['maximum_defect_identity_error'],
        maximum_native_frame_error=reports['frame']['maximum_frame_error'],
        minimum_uncorrected_NR_stress_defect=reports['frame']['minimum_nonzero_NR_defect'],
        component_summary=component_summary,
        quadratic_density_source='Derived C2(B)=JB B/2 at retained order; one-electron processes at fixed composition',
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        photon_and_gas_solutions_changed_by_readout_repair=False, source_symmetrized=False,
        explicit_low_frequency_tail_ports=True, closed_wave_evolved=False, full_event_bank_lifted=False,
        scope='Three saved x14,event0 temperatures; scalar-intensity l0/1/2; two joins; six heavy/cold histories; original/angular6/angular8; leading/MTS/combined',
        interpretation='Source-to-existing-gravity interface and density/transfer derivatives, not a new fit or full propagated spectrum',
        report_hashes={str(path.relative_to(ROOT)): digest(path) for path in sorted((ROOT / 'results').iterdir()) if path.is_file()},
        finished_at=now())
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', report)
    print(json.dumps({key: value for key, value in report.items() if key not in ('checks', 'failed', 'report_hashes')}, indent=2), flush=True)


def seal():
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    completion = read(ROOT / 'results/completion.json')
    assert completion['qualified']
    repair_protocol()
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for name, expected in completion['report_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage238 SAVED') for path in bookmarks)
    files = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=238, state='complete', qualified=True, sealed_at=now(), file_hashes=files,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=completion['scope'], original_trial_preserved=True, accepted_check_count=completion['accepted_check_count']))
    print(json.dumps(dict(seal_sha256=digest(target), payloads=len(files), qualified=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    {'validate': validate, 'seal': seal}[parser.parse_args().mode]()
