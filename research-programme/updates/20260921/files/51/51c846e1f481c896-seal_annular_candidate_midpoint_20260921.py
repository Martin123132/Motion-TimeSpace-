from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
from datetime import datetime, timezone
from pathlib import Path
from scipy.sparse import load_npz
import csv
import hashlib
import json
import re
import traceback
import numpy as np


def decimals(values):
    return np.array([[Decimal(value) for value in row] for row in values])


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-coupled-midpoint'
    destination = intake/(prefix+'-final-integrity.json')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    executed = intake/(prefix+'-executed-sealer.py')
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', inputs={}, outputs={}, checks=[], github_action=False, subagents_used=False,
        candidate_only=True, polar_zero_shift_only=True, full_GR_limit_proven=False, valid_for_physics_claim=False,
        original_live_action_unchanged=True, modes_deleted=False, physical_force_mismatch_fixed=False,
        spatial_convergence_proven=False, full_live_P2_force_convergence_proven=False,
        exact_finite_label_Galerkin_evolution_qualified=False, global_stability_proven=False,
        general_nonzero_shift_or_temporal_current_derived=False, total_energy_conservation_qualified=False,
        state_identities=[], native_subspace_diagnostics=[],
        protected_scan_scope='mtime since2026-09-20T23:51:39Z; not a pre-turn whole-tree hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path] = hasher.hexdigest()
        return cache[path]

    def own(path, category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs', 'outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed input: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed input: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    def loaded(path):
        own(path)
        with np.load(path, allow_pickle=False) as data:
            return {name:data[name].copy() for name in data.files}

    def table(label, rows, source_path, count):
        path = intake/(prefix+'-'+label+'.csv')
        if path.exists():
            raise FileExistsError(str(path))
        rows = [dict(**row, source_path=str(source_path.relative_to(root))) for row in rows]
        fields = list(dict.fromkeys(field for row in rows for field in row))
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        with path.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(label+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and (count is None or len(parsed) == count)
            and all(None not in row and None not in row.values() and row['valid_for_claim'] == 'False'
                and (root/row['source_path']).is_file() for row in parsed))
        own(path, 'outputs')
        return len(parsed)

    save()
    try:
        prior = inherit(intake/'annular-candidate-coordinate-covectors-final-integrity.json')
        check('preceding_force_envelope_unchanged', prior['state'] == 'complete'
            and prior['coordinate_envelope_qualified'] and all(row['passed'] for row in prior['checks']))
        paths = {'main':intake/'annular-candidate-coupled-midpoint-attempt01/status.json',
            'fine':intake/'annular-candidate-midpoint-quadrature-attempt01/status.json'}
        runs = {key:inherit(path) for key, path in paths.items()}
        for key, status in runs.items():
            check(key+'_complete_all_implementation_checks', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']))
            check(key+'_conditional_private_evolution_scope', status['candidate_only'] and status['polar_zero_shift_only']
                and status['original_live_action_unchanged'] and status['new_coupled_evolution']
                and not status['github_action'] and not status['subagents_used'] and not status['modes_deleted']
                and not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['physical_force_mismatch_fixed'] and not status['spatial_convergence_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['global_stability_proven']
                and not status['general_nonzero_shift_or_temporal_current_derived']
                and not status['exact_finite_label_Galerkin_evolution_qualified'])
            check(key+'_all_nonlinear_radial_and_chart_gates', all(row['full_components'] == 16425
                and row['relative_residual'] < 5e-12 and row['maximum_correction'] < 2e-12
                and row['radial_residual'] < 2e-12 and row['minimum_F'] > 0
                and row['maximum_speed_ratio'] < 1 for row in status['cases']))
        main_run, fine_run = runs['main'], runs['fine']
        check('full_common_state_and_live_resolves', main_run['common_state_not_projected_to_native']
            and main_run['gravity_resolved_at_every_trial'] and main_run['full_saved_mass_is_preconditioner_only']
            and main_run['momentum_and_force_same_reference_material_rule'])
        check('all_three_branches_equal_forward_reverse_precision_controls', len(main_run['cases']) == 27
            and {(row['branch'], row['extension'], row['label'], row['index']) for row in main_run['cases']} ==
            {(branch, extension, label, index) for branch, extension in
                [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
                for label, count in [('forward1', 1), ('forward2', 2), ('forward4', 4), ('reverse', 1), ('digits40', 1)]
                for index in range(1, count+1)})
        check('temporal_reversal_and_arithmetic_flags_match_rows', main_run['trajectories_qualified'] ==
            all(row['passed'] for key in ['refinement', 'reversals', 'arithmetic'] for row in main_run[key])
            and all(len(main_run[key]) == 12 for key in ['refinement', 'reversals', 'arithmetic']))
        check('finer_rule_preserves_initial_physical_state_not_artificial_momenta',
            fine_run['initial_physical_fields_and_velocities_preserved']
            and fine_run['comparison_uses_momentum_impulses_not_unequal_initial_quadrature_momenta']
            and fine_run['independent_quadrature_qualified'] == all(row['passed'] for row in fine_run['comparisons'])
            and len(fine_run['cases']) == 6 and len(fine_run['comparisons']) == 12)
        check('independent_reverse_uses_full_perturbed_seed', fine_run['independent_reverse_qualified']
            == all(row['passed'] for row in fine_run['perturbed_reversals'])
            and len(fine_run['perturbed_reversals']) == 12
            and all(row['all_16425_seed_components_perturbed'] for row in fine_run['perturbed_reversals']))
        preconditioners = {}
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            path = intake/'annular-candidate-full-canonical-inverse-attempt01'/(case+'-22-fixed-metric-mass.npz')
            own(path)
            preconditioners[case] = BandedSourceInverse(load_npz(path), (15, 1095))
        for run_name, status in runs.items():
            for row in status['cases']:
                case = row['branch']+'-'+row['extension']
                if run_name == 'main':
                    name = case+'-'+row['label']+'-step'+str(row['index'])
                    if row['label'] == 'reverse':
                        previous = case+'-forward1-step1'
                    elif row['index'] == 1:
                        previous = case+'-initial'
                    else:
                        previous = case+'-'+row['label']+'-step'+str(row['index']-1)
                else:
                    name, previous = ((case+'-perturbed-reverse', case+'-forward1-step1')
                        if row['label'] == 'perturbed_reverse' else (case+'-fine-step', case+'-initial'))
                previous_folder = paths['main'].parent if run_name == 'fine' and row['label'] == 'perturbed_reverse' else paths[run_name].parent
                before = loaded(previous_folder/(previous+'.npz'))
                after = loaded(paths[run_name].parent/(name+'.npz'))
                initial_coordinates, initial_momenta = decimals(before['coordinates']), decimals(before['momenta'])
                coordinates, momenta, force = [decimals(after[key]) for key in ['coordinates', 'momenta', 'force_decimal']]
                with localcontext() as context:
                    context.prec = row['digits']
                    step = Decimal.from_float(row['step'])
                    position_match = np.all(coordinates == initial_coordinates+step*decimal_array(after['midpoint_rates']))
                    momentum_match = np.all(momenta == initial_momenta+step*force)
                with localcontext() as context:
                    context.prec = 64
                    residual = np.asarray(decimal_array(after['midpoint_momentum'])-(initial_momenta+momenta)/2, float)
                preconditioner = preconditioners[case]
                relative = preconditioner.residual_norm(residual)/preconditioner.residual_norm(np.asarray(initial_momenta, float))
                correction = float(np.max(abs(preconditioner.solve(residual.ravel()))))
                identity = dict(run=run_name, case=name, position_update_exact=bool(position_match), momentum_update_exact=bool(momentum_match),
                    reconstructed_midpoint_relative_residual=relative, reconstructed_maximum_correction=correction, valid_for_claim=False)
                report['state_identities'].append(identity)
                check(name+'_independent_full_state_midpoint_identities', position_match and momentum_match
                    and relative < 5e-12 and correction < 2e-12, identity)
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            mesh_path = intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json')
            own(mesh_path)
            packet = json.loads(mesh_path.read_text())
            defects = []
            for suffix in ['initial', 'forward4-step4']:
                data = loaded(paths['main'].parent/(case+'-'+suffix+'.npz'))
                fields = decimals(data['coordinates'])[:, :-1].T
                with localcontext() as context:
                    context.prec = 64
                    restricted = apply_rational_rows(packet['left_inverses'][0], fields)
                    reembedded = apply_rational_rows(packet['embeddings'][0], restricted)
                    defects.append(max(abs(fields-reembedded).ravel()))
            report['native_subspace_diagnostics'].append(dict(branch=branch, extension=extension,
                initial_defect=str(defects[0]), evolved_defect=str(defects[1]),
                non_native_component_resolved=bool(defects[1] > max(Decimal('1e-28'), 1000*defects[0])),
                diagnostic_projection_never_applied_to_trajectory=True, valid_for_claim=False))
        check('native_subspace_diagnostic_is_read_only', len(report['native_subspace_diagnostics']) == 3
            and all(row['diagnostic_projection_never_applied_to_trajectory'] for row in report['native_subspace_diagnostics']))
        counts = []
        specifications = [('cases', 'main', 'cases', 27), ('initial', 'main', 'initial_checks', 3),
            ('iterations', 'main', 'iterations', None), ('refinement', 'main', 'refinement', 12),
            ('reversal', 'main', 'reversals', 12), ('arithmetic', 'main', 'arithmetic', 12),
            ('quadrature-cases', 'fine', 'cases', 6), ('quadrature-comparisons', 'fine', 'comparisons', 12),
            ('perturbed-reversal', 'fine', 'perturbed_reversals', 12),
            ('quadrature-iterations', 'fine', 'iterations', None)]
        for label, run, key, count in specifications:
            counts.append(table(label, runs[run][key], paths[run], count))
        counts.append(table('state-identities', report['state_identities'], destination, 33))
        counts.append(table('native-subspace', report['native_subspace_diagnostics'], destination, 3))
        note = root/'DERIVATION-20260921-first-coupled-canonical-midpoint.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('report_complete_and_cited_sources_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_candidate_midpoint_20260921.py', 'derive_annular_candidate_midpoint_20260921.py',
                'check_annular_candidate_midpoint_quadrature_20260921.py', 'seal_annular_candidate_midpoint_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_scripts_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 23, 51, 39, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), new_coupled_evolution=True,
            trajectories_qualified=main_run['trajectories_qualified'], independent_quadrature_qualified=fine_run['independent_quadrature_qualified'],
            independent_reverse_qualified=fine_run['independent_reverse_qualified'],
            implementation_checks={key:len(status['checks']) for key, status in runs.items()},
            total_failed_attempts_preserved=prior['total_failed_attempts_preserved'], new_failures=[],
            distinct_files_rehashed=len(cache), table_rows=counts,
            next_target='Use the qualified midpoint map to lengthen the coupled interval with equal branch/step controls; independently invert endpoint momenta and check the complete reduced Hamiltonian. Keep high-precision common-state derivative atoms. No old force-mismatch, spatial-convergence, long-time stability or full-GR claim from a 1e-7 coordinate-time pilot.')
        save()
        print(json.dumps(dict(state='complete', implementation_checks=report['implementation_checks'],
            integrity_checks=len(report['checks']), files_rehashed=len(cache), table_rows=counts,
            trajectories_qualified=report['trajectories_qualified'], quadrature_qualified=report['independent_quadrature_qualified'],
            failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
