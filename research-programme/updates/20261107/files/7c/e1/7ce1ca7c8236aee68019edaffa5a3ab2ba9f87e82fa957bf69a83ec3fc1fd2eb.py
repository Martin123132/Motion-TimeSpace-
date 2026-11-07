from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-wave-flux-fine-candidates-attempt01', __file__)
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, full_live_reaction_recomputed=False,
            github_action=False, subagents_used=False, original_workbench_write=False,
            source_wave_force_reused=True, momentum_rate_reused=True,
            scope='Assemble fine-grid wave/native forcing candidates and matched sensitivity; no reaction replacement')
        intake = evidence.output.parent
        seal_path = intake/'annular-native-precision-repair-integrity-20260929.json'
        prior = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests = {key: value for key, value in prior['hashes'].items() if key != 'CURRENT_LOCAL_RESUME.md'}

        def read(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if hashlib.sha256(path.read_bytes()).hexdigest() != digests[key]:
                raise RuntimeError('Changed candidate input: '+key)
            evidence.own(path)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {name: archive[name].copy() for name in archive.files}

        def registered(name):
            path = intake/name/'status.json'
            return read(str(path.relative_to(evidence.root)))

        def new_report(name):
            path = intake/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+':complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            for category in ['inputs', 'outputs']:
                for relative, digest in status[category].items():
                    if relative == 'CURRENT_LOCAL_RESUME.md':
                        continue
                    if relative in digests and digests[relative] != digest:
                        raise RuntimeError('Conflicting candidate authority: '+relative)
                    digests[relative] = digest
                    path = evidence.root/relative
                    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                        raise RuntimeError('Unverified candidate input: '+relative)
                    evidence.own(path)
            return status

        with localcontext() as context:
            context.prec = 70
            monotonicity = new_report('annular-wave-label-monotonicity-attempt01')
            evidence.check('all_four_maps_certified', len(monotonicity['cases']) == 4)
            native = registered('annular-native-tangent-precision-repair-attempt01')
            parent = registered('annular-position-reaction-diagnostic-attempt04')
            for branch, authority in [('reference-reference', 'annular-wave-flux-events-reference-attempt02'),
                    ('MTS-primary', 'annular-wave-flux-events-MTS-fine-attempt01')]:
                report = new_report(authority)
                selected = {row['summary']['radial_order']: row for row in report['cases']}
                evidence.check(branch+':three_rules', sorted(selected) == [16, 24, 32])
                evidence.check(branch+':two_wave_pairs', all(selected[order]['summary']['pair_passed'] for order in [24, 32]))
                if branch == 'reference-reference':
                    evidence.check(branch+':baseline2048_replay', all(row['summary']['baseline_replay_passed'] for row in selected.values()))
                waves = {order: read(selected[order]['path']) for order in [24, 32]}
                old_case = next(row for row in parent['cases'] if row['branch'] == branch and row['level'] == 'fine')
                old = {order: read(old_case['paths']['material'+str(order)]) for order in [48, 64]}
                short = 'reference' if branch.startswith('reference') else branch
                owner = registered('annular-'+short+'-matched-current-attempt01')
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled')
                matrix_path = evidence.root/centre['matrix_path']
                if hashlib.sha256(matrix_path.read_bytes()).hexdigest() != digests[centre['matrix_path']]:
                    raise RuntimeError('Changed live mass matrix')
                evidence.own(matrix_path)
                shape = waves[32]['complete_flux'].shape
                inverse = BandedSourceInverse(load_npz(matrix_path), shape)
                norm = lambda values: float(np.max(np.abs(inverse.solve(np.asarray(values, float).ravel()))))
                native_force = {order: np.zeros(shape) for order in [64, 96]}
                if branch == 'MTS-primary':
                    chosen = {row['summary']['order']: row for row in native['cases'] if row['summary']['level'] == 'fine'}
                    for order in [64, 96]:
                        data = read(chosen[order]['path'])['force_decimal']
                        native_force[order] = np.asarray([float(Decimal(value)) for value in data.ravel()]).reshape(shape)
                new_wave = {}
                for wave_order, old_order in [(24, 48), (32, 64)]:
                    vector = waves[wave_order]['complete_flux'].copy()
                    vector[:, -1] = old[old_order]['force_wave'][:, -1]
                    new_wave[wave_order] = vector
                wave_change = new_wave[32]-old[64]['force_wave']
                evidence.check(branch+':field_only_wave_change', np.all(wave_change[:, -1] == 0.))
                full_force_change = wave_change+native_force[96]-old[64]['force_native']
                paired_momentum = old[64]['momentum_rate']-old[48]['momentum_rate']
                paired_wave = new_wave[32]-new_wave[24]
                paired_native = native_force[96]-native_force[64]
                paired_residual = paired_momentum-paired_wave-paired_native
                source_difference = np.zeros(shape)
                source_difference[:, -1] = paired_wave[:, -1]
                row = dict(branch=branch, level='fine', wave_field_change_inverse=norm(wave_change),
                    original_to_repaired_force_inverse=norm(full_force_change),
                    wave_pair_inverse=norm(waves[32]['complete_flux']-waves[24]['complete_flux']),
                    retained_source_wave_pair_inverse=norm(source_difference),
                    retained_momentum_pair_inverse=norm(paired_momentum), native_pair_inverse=norm(paired_native),
                    combined_forcing_pair_inverse=norm(paired_residual),
                    combined_forcing_pair_passed=norm(paired_residual) <= 2e-11,
                    old_weak_new_flux_gap_inverse=selected[32]['summary']['weak_flux_inverse'],
                    old_weak_new_flux_gate_passed=selected[32]['summary']['weak_flux_passed'],
                    old_evaluator_gate_retained=True, reaction_updated=False, valid_for_claim=False)
                path = evidence.output/(branch+'-fine-forcing-candidate.npz')
                np.savez_compressed(path, wave_only_live_rhs=wave_change,
                    original_to_repaired_live_rhs=full_force_change,
                    paired_full_residual=paired_residual, high_wave_force=new_wave[32],
                    high_native_force=native_force[96])
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(summary=row, path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(row), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
