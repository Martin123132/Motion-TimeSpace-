from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import psutil


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def strict_json(path):
    def unique(pairs):
        document = {}
        for key, value in pairs:
            assert key not in document, (path, key)
            document[key] = value
        return document

    def reject(value):
        raise ValueError(f'Nonfinite JSON constant {value} in {path}')

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    paths = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*5+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    previous = []
    for path, base in zip(paths, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    for index, key in enumerate(keys):
        assert previous[index][key] == digest(paths[index+1])
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    sources = previous[0]['local_source_documents']
    for row in sources:
        assert Path(row['path']).is_file() and digest(Path(row['path'])) == row['sha256']
    derivation_path = ROOT/'results/derivation/status.json'
    derivation = strict_json(derivation_path)
    assert derivation['state'] == 'complete' and derivation['exact_check_count'] == len(derivation['checks']) == 13
    assert all(row['passed'] for row in derivation['checks'])
    assert derivation['script_sha256'] == digest(ROOT/'derive_pulsations.py')
    assert derivation['parent_seal_sha256'] == digest(paths[0])
    spectral_rows = []
    counts = [('pilot', 4), ('convergence', 27), ('large-body-refinement', 3), ('large-body-fine', 3),
              ('flat-controls', 6), ('flat-controls-fine', 1), ('quadrature', 9)]
    for label, count in counts:
        report = strict_json(ROOT/f'results/{label}/status.json')
        assert report['state'] == 'complete' and len(report['rows']) == count
        assert report['script_sha256'] == digest(ROOT/'solve_pulsations.py')
        assert report['parent_seal_sha256'] == digest(paths[0]) and report['derivation_sha256'] == digest(derivation_path)
        for row in report['rows']:
            assert digest(Path(row['profile_path'])) == row['profile_sha256']
            assert np.all(np.array(row['frequency_squared']) > 0)
            assert row['constrained_polar_energy_minimum'] > 0
            assert row['phase_null_relative_residual'] < 1e-12
            assert row['maximum_charge_tangent_relative_residual'] < 1e-12
            assert row['maximum_second_order_relative_residual'] < 1e-4
            assert (ROOT/f'results/{label}'/row['archive']).is_file()
        spectral_rows.extend(report['rows'])
    validation = strict_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete'
    assert validation['script_sha256'] == digest(ROOT/'validate_pulsations.py')
    assert validation['solver_sha256'] == digest(ROOT/'solve_pulsations.py')
    for source, expected in validation['input_hashes'].items():
        assert digest(Path(source)) == expected
    assert validation['spectral_calculations'] == 53 and validation['physical_cases'] == 9
    assert len(validation['finest_spectra']) == len(validation['comparisons']) == 9
    assert len(validation['dynamic_checks']) == len(validation['flat_formulation_controls']) == 3
    max_mesh = max(max(row['last_relative_frequency_mesh_changes']) for row in validation['comparisons'])
    max_quad = max(row['quadrature_relative_omega_squared_difference'] for row in validation['comparisons'])
    max_flat = max(row['maximum_relative_flat_formulation_difference'][-1] for row in validation['flat_formulation_controls'])
    max_spectral_residual = max(row['maximum_second_order_relative_residual'] for row in spectral_rows)
    max_kg = max(row['independently_reconstructed_KG_gradient_relative_difference'] for row in validation['dynamic_checks'])
    time_rows = [item for row in validation['dynamic_checks'] for item in row['time_evolution']]
    assert len(time_rows) == 9
    max_energy = max(row['maximum_relative_quadratic_energy_drift'] for row in time_rows)
    max_time_prediction = max(row['phase_difference_from_midpoint_dispersion'] for row in time_rows)
    assert max_mesh < .000913 and max_quad < 1.31e-10 and max_flat < 2.13e-5
    assert max_spectral_residual < 6.35e-6 and max_kg < 2.61e-12
    assert max_energy < 1.30e-12 and max_time_prediction < 1.36e-10
    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as archive:
            assert all(np.all(np.isfinite(archive[name])) for name in archive.files)
            if 'frequency_squared' in archive:
                assert archive['frequency_squared'].shape == (5,)
                assert np.all(archive['frequency_squared'] > 0)
                assert np.allclose(archive['frequencies']**2, archive['frequency_squared'], rtol=1e-14)
            if 'trace' in archive:
                assert archive['trace'].shape[1] == 4 and np.all(np.diff(archive['trace'][:, 0]) > 0)
        archives.append(path.relative_to(ROOT).as_posix())
    assert len(archives) == 65
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *paths, *[Path(row['path']) for row in sources]]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/2103.15012', 'https://doi.org/10.1088/1361-6382/ac0160']
    assert all(url in prose for url in urls)
    parsed, compiled = [], []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        if isinstance(report, dict) and 'state' in report:
            assert report['state'] == 'complete'
        parsed.append(path.relative_to(ROOT).as_posix())
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 21, 46, 40, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    report = {'state': 'complete', 'sealed_at': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(paths[0]), 'prior_sealed_entries_unchanged': sum(len(row['file_hashes']) for row in previous),
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_03': urls, 'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'exact_check_count': 13, 'spectral_calculations': 53, 'physical_configurations': 9,
              'reconstructed_modes': 3, 'linear_time_evolution_runs': 9, 'archives_verified': len(archives),
              'maximum_last_frequency_mesh_relative_change': max_mesh,
              'maximum_quadrature_frequency_squared_relative_change': max_quad,
              'maximum_flat_independent_formulation_relative_difference': max_flat,
              'maximum_second_order_spectral_relative_residual': max_spectral_residual,
              'maximum_independent_KG_gradient_relative_error': max_kg,
              'maximum_linear_quadratic_energy_drift': max_energy,
              'maximum_midpoint_phase_prediction_error': max_time_prediction,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since21:46:40UTC; not a full content-hash baseline.',
              'coupled_physical_radial_pulsation_operator_derived': True,
              'positive_radial_squared_frequencies_numerically_supported': True,
              'global_phase_response_reconstructed': True, 'continuum_spectral_error_bound_certified': False,
              'nonlinear_or_strong_gravity_endpoint_claimed': False, 'new_physical_parameter_fitted': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_priority_single_core_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': report['prior_sealed_entries_unchanged'],
                      'spectra': 53, 'exact_checks': 13, 'time_evolutions': 9, 'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
