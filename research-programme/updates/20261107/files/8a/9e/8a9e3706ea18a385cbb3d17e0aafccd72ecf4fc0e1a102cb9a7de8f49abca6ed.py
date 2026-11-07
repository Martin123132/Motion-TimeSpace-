from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import psutil
from scipy.interpolate import PPoly


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT / 'results/stage-integrity.json'


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def strict_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key {key} in {path}')
            result[key] = value
        return result
    def reject(value):
        raise ValueError(f'Nonfinite JSON constant {value} in {path}')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    paths = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256', 'parent_seal_sha256', 'previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    reports = []
    for path, base in zip(paths, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            source = base/relative
            assert source.is_file() and digest(source) == expected, str(source)
        reports.append(report)
    for index, key in enumerate(keys):
        assert reports[index][key] == digest(paths[index+1])
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == reports[0]['checkpoint_manifest_sha256']
    source_documents = []
    for row in reports[0]['parent_source_map']:
        source = Path(row['path'])
        assert source.is_file() and digest(source) == row['sha256']
        source_documents.append({'path': str(source), 'sha256': digest(source), 'role': row['role']})

    numerical_path = ROOT/'results/regular-center-bodies/status.json'
    identities_path = ROOT/'results/identities/status.json'
    numerical = strict_json(numerical_path)
    identities = strict_json(identities_path)
    provenance = strict_json(ROOT/'results/regular-center-bodies/execution-provenance.json')
    assert numerical['state'] == identities['state'] == 'complete'
    assert numerical['parent_seal_sha256'] == digest(paths[0])
    assert identities['profile_report_sha256'] == digest(numerical_path)
    assert numerical['script_sha256'] == digest(ROOT/'validate_finite_bodies.py')
    assert identities['script_sha256'] == digest(ROOT/'derive_finite_body_identities.py')
    assert provenance['wrapper_sha256'] == digest(ROOT/'regular_center_solver.py')
    assert provenance['base_runner_sha256'] == digest(ROOT/'validate_finite_bodies.py')
    assert provenance['spline_loader_sha256'] == digest(ROOT/'run_verified_profiles.py')
    for name, expected in numerical['imported_source_sha256'].items():
        assert digest(ROOT/name) == expected
    assert identities['exact_check_count'] == len(identities['checks']) == 21
    assert all(row['passed'] for row in identities['checks'])
    assert len(numerical['rows']) == len(numerical['spectra']) == len(numerical['convergence']) == 7
    max_convergence = max(max(row['relative_differences'].values()) for row in numerical['convergence'])
    max_virial = max(row['virial_relative'] for row in numerical['rows'])
    max_mass_error = max(abs(row['active_to_inertial_mass_ratio']-1) for row in numerical['rows'])
    assert max_convergence < 4.78e-9 and max_virial < 7.32e-11 and max_mass_error < 1e-12
    assert max(row['independent_quadrature_relative_error'] for row in numerical['rows']) < 1e-8
    assert all(row['bvp_success'] and row['frequency'] > 1 and row['energy'] > row['frequency']*row['charge']
               for row in numerical['rows'])
    for index in range(6):
        assert numerical['rows'][index+1]['charge'] > numerical['rows'][index]['charge']
        assert numerical['rows'][index+1]['frequency'] < numerical['rows'][index]['frequency']
        assert numerical['rows'][index+1]['surface_excess_ratio'] < numerical['rows'][index]['surface_excess_ratio']
    for row in numerical['spectra']:
        assert len(row['levels']) == 3
        final = row['levels'][-1]
        assert final['amplitude_radial_unconstrained'][0] < 0 < final['amplitude_radial_unconstrained'][1]
        assert final['fixed_charge_radial'][0] > 0 and final['amplitude_l2'][0] > 0
        assert max(final['fixed_charge_eigenpair_residuals']) < 1e-7
        for field in ['phase_l0', 'amplitude_l1_translation']:
            assert abs(final[field][0]) < abs(row['levels'][0][field][0])/8
    assert all(row['fixed_charge_lowest_relative_change'] < .001 for row in identities['spectral_convergence'])
    assert all(row['scaling_hessian_eigenvalues_per_energy'][0] > 0 for row in identities['numerical_scaling_tests'])
    assert all(trial['relative_energy_increase'] > 0 for row in identities['numerical_scaling_tests']
               for trial in row['finite_fixed_charge_trials'])
    profile_archives = []
    for row in numerical['rows']:
        path = ROOT/f"results/regular-center-bodies/profile-R{row['support_radius']:g}.npz"
        with np.load(path, allow_pickle=False) as archive:
            assert all(np.all(np.isfinite(archive[name])) for name in archive.files)
            coefficients, knots = archive['spline_coefficients'], archive['spline_knots']
            assert coefficients.shape == (4, len(knots)-1, 2) and np.all(np.diff(knots) > 0)
            spline = PPoly.construct_fast(coefficients, knots, axis=1)
            assert np.isclose(spline(0)[0], row['central_amplitude'], rtol=1e-12)
            assert np.isclose(spline(1)[0], 1e-9, rtol=1e-9)
            assert np.isclose(float(archive['frequency2']), row['frequency']**2, rtol=1e-13)
        profile_archives.append(str(path.resolve()))
    primary_urls = ['https://arxiv.org/abs/hep-th/0103189', 'https://arxiv.org/abs/1604.08871']
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    assert all(url in prose for url in primary_urls)
    quoted_local_files = set(re.findall(r'`([^`\n]+\.(?:md|json))`', prose))
    required = [ROOT/'08-finite-charge-compact-bodies.md', ROOT/'09-fixed-charge-stability-and-gravitating-source.md',
                ROOT/'RESULTS.md', ROOT/'RESUME.md', numerical_path, identities_path, manifest, *paths]
    for relative in quoted_local_files:
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    parsed = []
    for path in sorted(ROOT.rglob('*.json')):
        strict_json(path)
        parsed.append(path.relative_to(ROOT).as_posix())
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 17, 25, 30, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    assert (ROOT/'results/regular-center-bodies/execution-provenance.json').is_file()
    assert (ROOT/'results/verified-bodies/execution-provenance.json').is_file()
    assert (ROOT/'results/validated-bodies/prior-attempts.json').is_file()
    assert (ROOT/'results/refined-family/prior-attempt.json').is_file()
    assert (ROOT/'results/family/progress.json').is_file()
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path != OUTPUT}
    report = {'state': 'complete', 'sealed_at': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(paths[0]),
              'prior_sealed_entries_unchanged': sum(len(row['file_hashes']) for row in reports),
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'accepted_numerical_report': str(numerical_path), 'accepted_identities_report': str(identities_path),
              'exact_checks': 21, 'accepted_profiles': 7, 'spectral_resolutions': 21, 'finite_fixed_charge_trials': 42,
              'max_profile_convergence_relative_change': max_convergence, 'max_virial_relative': max_virial,
              'max_active_inertial_integral_relative_error': max_mass_error,
              'max_last_radial_spectral_relative_change': max(row['fixed_charge_lowest_relative_change'] for row in identities['spectral_convergence']),
              'largest_body_surface_excess_ratio': numerical['rows'][-1]['surface_excess_ratio'],
              'retained_failed_attempts_count': 4,
              'failed_attempts_classified': ['continuation mesh limit', 'missing spline output axis', 'canonical spline coefficient constructor misuse', 'singular center mesh limit'],
              'local_source_documents': source_documents, 'primary_source_urls_checked_2026_10_03': primary_urls,
              'required_local_paths': sorted(set(str(path.resolve()) for path in required)),
              'profile_archives_reconstructed': profile_archives, 'compiled_scripts': compiled, 'parsed_json_files': parsed,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since 17:25:30 UTC; not a full content-hash baseline.',
              'compact_profile_existence_numerically_supported': True, 'interval_certified_existence_theorem': False,
              'radial_constrained_energy_hessian_checked': True, 'conditional_angular_positivity_derived': True,
              'nonlinear_orbital_stability_theorem_proved': False, 'self_gravitating_profiles_solved': False,
              'integrated_static_stress_cancellation_derived': True,
              'weak_Einstein_source_equality_conditional_on_retained_parent': True,
              'physical_scale_or_cosmological_abundance_fitted': False,
              'original_parent_action_modified': False, 'github_action': False, 'subagents': 0}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes),
                      'prior_unchanged': report['prior_sealed_entries_unchanged'], 'exact_checks': 21,
                      'profiles': 7, 'spectral_resolutions': 21, 'protected_changes': len(changed),
                      'max_mass_integral_error': max_mass_error}))


if __name__ == '__main__':
    main()
