from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
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


def exact(values):
    return np.array([Decimal.from_float(float(value)) for value in np.asarray(values).ravel()]).reshape(np.shape(values))


def stored(values):
    return np.array([Decimal(value) for value in values.ravel()]).reshape(values.shape)


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-endpoint-energy'
    destination = intake/(prefix+'-final-integrity.json')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    executed = intake/(prefix+'-executed-sealer.py')
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', inputs={}, outputs={}, checks=[], github_action=False, subagents_used=False,
        candidate_only=True, polar_zero_shift_only=True, full_GR_limit_proven=False, valid_for_physics_claim=False,
        original_live_action_unchanged=True, modes_deleted=False, physical_force_mismatch_fixed=False,
        spatial_convergence_proven=False, global_stability_proven=False, total_energy_conservation_proven=False,
        no_Newton_constant_derivation=True, independent_energy_checks=[],
        protected_scan_scope='mtime since2026-09-21T00:36:52Z; not a pre-turn whole-tree hash baseline')
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
        flat = []
        for original in rows:
            row = {name:value for name, value in original.items() if name != 'energy'}
            row.update(original.get('energy', {}))
            row['source_path'] = str(source_path.relative_to(root))
            flat.append(row)
        fields = list(dict.fromkeys(field for row in flat for field in row))
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(flat)
        with path.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(label+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and (count is None or len(parsed) == count)
            and all(None not in row and None not in row.values() and row['valid_for_claim'] == 'False'
                and (root/row['source_path']).is_file() for row in parsed))
        own(path, 'outputs')
        return len(parsed)

    save()
    try:
        prior = inherit(intake/'annular-candidate-coupled-midpoint-final-integrity.json')
        check('preceding_coupled_trajectory_seal_unchanged', prior['state'] == 'complete'
            and prior['trajectories_qualified'] and all(row['passed'] for row in prior['checks']))
        failed_path = intake/'annular-candidate-endpoint-energy-attempt01/status.json'
        failed = inherit(failed_path)
        check('zero_step_rounding_failure_preserved', failed['state'] == 'failed'
            and 'endpoint_state_unchanged' in failed['error'])
        interrupted_path = intake/'annular-candidate-endpoint-energy-attempt02/status.json'
        interrupted = inherit(interrupted_path)
        own(interrupted_path.parent/'latest-endpoint-recovery.npz')
        ledger_path = intake/'annular-candidate-endpoint-energy-failure-ledger.json'
        own(ledger_path)
        ledger = json.loads(ledger_path.read_text())
        check('serialization_failure_and_stale_checkpoint_preserved', interrupted['state'] == 'running'
            and len(interrupted['cases']) == 6 and len(ledger['failures']) == 2
            and all(row['exit_code'] == 1 for row in ledger['failures']) and not ledger['valid_for_claim'])
        status_path = intake/'annular-candidate-endpoint-energy-attempt03/status.json'
        run = inherit(status_path)
        check('endpoint_run_complete_all_checks', run['state'] == 'complete' and all(row['passed'] for row in run['checks']))
        check('scope_flags_remain_conditional_nonclaim', run['candidate_only'] and run['polar_zero_shift_only']
            and run['original_live_action_unchanged'] and not run['new_coupled_evolution']
            and not run['github_action'] and not run['subagents_used'] and not run['modes_deleted']
            and not run['total_energy_conservation_proven'] and not run['full_GR_limit_proven']
            and not run['valid_for_physics_claim'] and not run['physical_force_mismatch_fixed']
            and not run['spatial_convergence_proven'] and run['no_Newton_constant_derivation']
            and run['interval_not_assigned_seconds'] and run['long_run_not_started'])
        branches = [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
        labels = ['initial', 'one_step', 'two_steps', 'four_steps', 'fine_initial', 'fine_step']
        check('all_three_branches_receive_equal_energy_tests', len(run['cases']) == 18
            and {(row['branch'], row['extension'], row['label']) for row in run['cases']} ==
            {(branch, extension, label) for branch, extension in branches for label in labels})
        inverses = {}
        for branch, extension in branches:
            case = branch+'-'+extension
            path = intake/'annular-candidate-full-canonical-inverse-attempt01'/(case+'-22-fixed-metric-mass.npz')
            own(path)
            inverses[case] = BandedSourceInverse(load_npz(path), (15, 1095))
        by_case = {}
        for row in run['cases']:
            case = row['branch']+'-'+row['extension']
            name = case+'-'+row['label']
            raw = loaded(status_path.parent/(name+'-energy-inputs.npz'))
            original = loaded(root/row['source_state'])
            check(name+'_original_q_p_preserved_exactly', np.array_equal(raw['coordinates'], original['coordinates'])
                and np.array_equal(raw['target_momenta'], original['momenta']) and raw['endpoint_rates'].shape == (15, 1095))
            radius, mass, lapse = raw['radius'], raw['mass'], np.exp(raw['log_lapse'])
            coupling, source_mass, central = [float(raw[key]) for key in ['coupling', 'source_mass', 'central_mass']]
            metric = 1-2*mass/radius
            clock = np.sqrt(lapse**2-raw['source_velocity']**2/metric)
            kinetic = radius**2*raw['temporal_square']/(2*lapse*np.sqrt(metric))
            potential = radius**2*lapse*np.sqrt(metric)*(raw['gradient_square']/2+raw['gram'])
            dust = source_mass*raw['source_density']*lapse**2/clock
            matter_density = kinetic+potential+dust
            gravity_density = lapse*raw['mass_rhs']/(coupling*np.sqrt(metric))
            reconstructed_rhs = coupling*radius**2*metric*(raw['temporal_square']/(2*lapse**2*metric)
                +raw['gradient_square']/2+raw['gram'])+coupling*source_mass*raw['source_density']*np.sqrt(metric)*lapse/clock
            check(name+'_independent_constraint_and_density_identity',
                np.max(abs(reconstructed_rhs-raw['mass_rhs'])) < 2e-12*np.max(abs(raw['mass_rhs']))
                and np.max(abs(matter_density-gravity_density)) < 2e-12*np.max(abs(matter_density)))
            with localcontext() as context:
                context.prec = 64
                weights, rates, measured, target = exact(raw['weights']), exact(raw['endpoint_rates']), exact(raw['computed_momenta']), stored(raw['target_momenta'])
                pairing, computed = np.sum(target*rates), np.sum(measured*rates)
                action = Decimal.from_float(float(raw['matter_action']))
                gravity = np.sum(weights*exact(gravity_density))
                boundary = np.sum(weights*exact(raw['mass_rhs']))/Decimal.from_float(coupling)
                boundary_endpoint = (Decimal.from_float(float(mass[-1]))-Decimal.from_float(central))/Decimal.from_float(coupling)
                full = pairing-action-gravity+boundary
                recovered = dict(target_pairing=pairing, computed_pairing=computed, matter_action=action,
                    gravity_bulk=gravity, boundary_integral=boundary, boundary_endpoint=boundary_endpoint,
                    full_shifted_hamiltonian=full, mixed_quadrature_Legendre_defect=computed-action-gravity,
                    inverse_energy_error=pairing-computed, without_boundary=full-boundary, without_gravity_bulk=full+gravity)
                check(name+'_independent_high_precision_energy_accounting',
                    all(abs(value-Decimal(row['energy'][key])) < Decimal('1e-55') for key, value in recovered.items()))
                residual = np.asarray(measured-target, float)
            inverse = inverses[case]
            relative = inverse.residual_norm(residual)/inverse.residual_norm(np.asarray(target, float))
            correction = float(np.max(abs(inverse.solve(residual.ravel()))))
            bound = float(np.linalg.norm(residual.ravel()/inverse.original_scale)*np.linalg.norm(inverse.original_scale*raw['endpoint_rates'].ravel()))
            check(name+'_independent_full_endpoint_inverse', relative < 5e-12 and correction < 2e-12
                and abs(float(pairing-computed)) <= bound*(1+1e-10)+1e-30)
            record = dict(case=name, relative_residual=relative, maximum_correction=correction,
                inverse_energy_Cauchy_bound=bound, full_shifted_hamiltonian=str(full), boundary_integral=str(boundary),
                mixed_quadrature_Legendre_defect=str(recovered['mixed_quadrature_Legendre_defect']), valid_for_claim=False)
            report['independent_energy_checks'].append(record)
            by_case[(row['branch'], row['extension'], row['label'])] = row
        for row in run['drifts']:
            branch, extension, label = row['branch'], row['extension'], row['label']
            before = by_case[(branch, extension, 'fine_initial' if label == 'fine_step' else 'initial')]
            after = by_case[(branch, extension, label)]
            with localcontext() as context:
                context.prec = 64
                baseline = Decimal(before['energy']['full_shifted_hamiltonian'])
                drift = Decimal(after['energy']['full_shifted_hamiltonian'])-baseline
            floor = before['diagnostic_resolution_scale']+after['diagnostic_resolution_scale']
            check(branch+'-'+extension+'-'+label+'_independent_drift_and_nonclaim_gate', str(drift) == row['energy_drift']
                and row['smoke_passed'] == (abs(drift) < Decimal('1e-9')*abs(baseline))
                and row['drift_resolved'] == (abs(float(drift)) > 4*floor)
                and not row['conservation_proven'] and not row['valid_for_claim'])
        check('resolved_order_not_promoted_from_floor', all(row['resolved_energy_time_order'] ==
            (row['differences_resolved'] and row['ratio'] < .4) and row['floor_limited'] == (not row['differences_resolved'])
            for row in run['refinement']) and run['energy_time_order_resolved'] ==
            all(row['resolved_energy_time_order'] for row in run['refinement']))
        check('smoke_flag_matches_all_drift_rows', len(run['drifts']) == 12 and run['energy_drift_smoke_passed'] ==
            all(row['smoke_passed'] for row in run['drifts']))
        for branch, extension in branches:
            drifts = {row['label']:row for row in run['drifts'] if row['branch'] == branch and row['extension'] == extension}
            refinement = next(row for row in run['refinement'] if row['branch'] == branch and row['extension'] == extension)
            quadrature = next(row for row in run['quadrature'] if row['branch'] == branch and row['extension'] == extension)
            with localcontext() as context:
                context.prec = 64
                first, second, third = [Decimal(drifts[label]['energy_drift']) for label in ['one_step', 'two_steps', 'four_steps']]
                first_difference, second_difference = abs(first-second), abs(second-third)
                quadrature_difference = Decimal(drifts['fine_step']['energy_drift'])-first
                initial_offset = Decimal(by_case[(branch, extension, 'fine_initial')]['energy']['full_shifted_hamiltonian'])-Decimal(by_case[(branch, extension, 'initial')]['energy']['full_shifted_hamiltonian'])
            floor = float(max(drifts[label]['diagnostic_resolution_scale'] for label in ['one_step', 'two_steps', 'four_steps']))
            resolved = float(first_difference) > 4*floor and float(second_difference) > 4*floor
            check(branch+'-'+extension+'_independent_refinement_and_quadrature',
                abs(first_difference-Decimal(refinement['first_difference'])) < Decimal('1e-43')
                and abs(second_difference-Decimal(refinement['second_difference'])) < Decimal('1e-43')
                and refinement['differences_resolved'] == resolved
                and abs(float(second_difference/max(first_difference, Decimal('1e-90')))-refinement['ratio']) < 1e-12
                and quadrature['energy_drift_difference'] == str(quadrature_difference)
                and quadrature['initial_energy_offset'] == str(initial_offset)
                and quadrature['matched_physical_initial_state'] and not quadrature['spatial_convergence_claim'])
        counts = [table(key, run[key], status_path, count) for key, count in
            [('cases', 18), ('iterations', None), ('drifts', 12), ('refinement', 3), ('quadrature', 3)]]
        counts.append(table('independent-energy', report['independent_energy_checks'], destination, 18))
        note = root/'DERIVATION-20260921-endpoint-Hamiltonian-and-boundary-energy.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('report_complete_and_all_local_citations_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            if (root/name).resolve() != destination.resolve():
                own(root/name)
        own(note)
        for name in ['annular_candidate_hamiltonian_20260921.py', 'annular_endpoint_legendre_inverse_20260921.py',
                'derive_annular_candidate_endpoint_energy_20260921.py', 'derive_annular_candidate_endpoint_energy_v2_20260921.py',
                'derive_annular_candidate_endpoint_energy_v3_20260921.py',
                'seal_annular_candidate_endpoint_energy_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('scripts_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 21, 0, 36, 52, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            boundary_energy_identity_symbolically_derived=run['boundary_energy_identity_symbolically_derived'],
            weak_field_dust_energy_form_derived=run['weak_field_dust_energy_form_derived'],
            endpoint_velocities_recovered=run['endpoint_velocities_recovered'], full_hamiltonian_computed=run['full_hamiltonian_computed'],
            energy_drift_smoke_passed=run['energy_drift_smoke_passed'], energy_time_order_resolved=run['energy_time_order_resolved'],
            implementation_checks=len(run['checks']), total_failed_attempts_preserved=prior['total_failed_attempts_preserved']+2,
            new_failures=[str(failed_path.relative_to(root)), str(interrupted_path.relative_to(root))], distinct_files_rehashed=len(cache), table_rows=counts,
            next_target='Extend the same three-branch coupled pilot in bounded saved blocks; keep endpoint inverses and complete boundary-inclusive energy. Resolve energy drift above integration/roundoff floors before claiming time-order or conservation. No full-GR or old force/spatial-mismatch repair claim.')
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), files_rehashed=len(cache), table_rows=counts,
            energy_smoke_passed=report['energy_drift_smoke_passed'], resolved_order=report['energy_time_order_resolved'],
            failed_attempts_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
