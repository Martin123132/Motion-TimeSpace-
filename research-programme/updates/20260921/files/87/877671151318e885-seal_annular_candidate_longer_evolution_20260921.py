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
    prefix = 'annular-candidate-longer-evolution'
    destination = intake/(prefix+'-final-integrity.json')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    executed = intake/(prefix+'-executed-sealer.py')
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', inputs={}, outputs={}, checks=[], github_action=False, subagents_used=False,
        candidate_only=True, polar_zero_shift_only=True, full_GR_limit_proven=False, valid_for_physics_claim=False,
        original_live_action_unchanged=True, modes_deleted=False, physical_force_mismatch_fixed=False,
        spatial_convergence_proven=False, global_stability_proven=False, total_energy_conservation_proven=False,
        no_Newton_constant_derivation=True, independent_energy_checks=[], independent_step_checks=[],
        protected_scan_scope='mtime since2026-09-21T01:15:04Z; not a pre-turn whole-tree hash baseline')
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
        prior = inherit(intake/'annular-candidate-endpoint-energy-final-integrity.json')
        check('prior_energy_seal_unchanged', prior['state'] == 'complete' and prior['energy_drift_smoke_passed']
            and all(row['passed'] for row in prior['checks']))
        baseline_path = intake/'annular-candidate-endpoint-energy-attempt03/status.json'
        baseline_run = inherit(baseline_path)
        selected = {label:intake/('annular-candidate-longer-'+label+'-attempt01/status.json') for label in ['1e-6', '1e-5']}
        selected['1e-5'] = intake/'annular-candidate-longer-1e-5-attempt04/status.json'
        control = inherit(intake/'annular-candidate-accelerated-midpoint-control-attempt01/status.json')
        check('independent_acceleration_control', control['state'] == 'complete' and all(row['passed'] for row in control['checks'])
            and control['unchanged_residual_gates'] and control['no_physical_modes_deleted'])
        control2 = inherit(intake/'annular-candidate-accelerated-midpoint-control-attempt02/status.json')
        check('expanded_history_independent_control', control2['state'] == 'complete'
            and all(row['passed'] for row in control2['checks']))
        new_failures = []
        for path in sorted(intake.glob('annular-candidate-longer-*-attempt*/status.json')):
            if path in selected.values():
                continue
            extra = inherit(path)
            check(path.parent.name+'_not_active', extra['state'] in ['complete', 'failed'])
            if extra['state'] == 'failed':
                new_failures.append(str(path.relative_to(root)))
        runs = {label:inherit(path) for label, path in selected.items()}
        inverses = {}
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            path = intake/'annular-candidate-full-canonical-inverse-attempt01'/(case+'-22-fixed-metric-mass.npz')
            own(path)
            inverses[case] = BandedSourceInverse(load_npz(path), (15, 1095))
        counts = {}
        for label, run in runs.items():
            check(label+'_complete_all_implementation_checks', run['state'] == 'complete' and all(row['passed'] for row in run['checks']))
            check(label+'_unchanged_action_and_all_components', run['original_live_action_unchanged'] and run['new_coupled_evolution']
                and run['full_saved_mass_is_preconditioner_only'] and run['gravity_resolved_at_every_trial']
                and run['common_state_not_projected_to_native'] and run['momentum_and_force_same_reference_material_rule']
                and not run['modes_deleted'] and not run['github_action'] and not run['subagents_used']
                and not run['valid_for_physics_claim'] and run['horizon_has_no_seconds_assignment'])
            check(label+'_equal_branches', len(run['cases']) == (27 if run['controls'] else 21)
                and len(run['endpoints']) == (12 if run['controls'] else 9)
                and {(row['branch'], row['extension']) for row in run['cases']} ==
                {('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')})
            states = {}
            for row in run['cases']:
                name = label+'-'+Path(row['path']).stem
                before, after = loaded(root/row['previous_path']), loaded(root/row['path'])
                position, momentum = stored(after['coordinates']), stored(after['momenta'])
                initial_q, initial_p = stored(before['coordinates']), stored(before['momenta'])
                with localcontext() as context:
                    context.prec = 64
                    step = Decimal.from_float(row['step'])
                    position_match = np.array_equal(position, initial_q+step*exact(after['midpoint_rates']))
                    momentum_match = np.array_equal(momentum, initial_p+step*stored(after['force_decimal']))
                    residual = np.asarray(exact(after['midpoint_momentum'])-initial_p-step*stored(after['force_decimal'])/2, float)
                inverse = inverses[row['branch']+'-'+row['extension']]
                relative = inverse.residual_norm(residual)/inverse.residual_norm(np.asarray(initial_p, float))
                correction = float(np.max(abs(inverse.solve(residual.ravel()))))
                check(name+'_exact_updates_and_full_midpoint_residual', position_match and momentum_match
                    and relative < 5e-12 and correction < 2e-12 and row['full_components'] == 16425
                    and row['radial_residual'] < 2e-12 and row['minimum_F'] > 0 and row['maximum_speed_ratio'] < 1)
                report['independent_step_checks'].append(dict(horizon=label, case=name, exact_position=bool(position_match),
                    exact_momentum=bool(momentum_match), relative_residual=relative, maximum_correction=correction, valid_for_claim=False))
                states[(row['branch'], row['extension'], row['label'], row['index'])] = (position, momentum)
            energies = {}
            for row in run['endpoints']:
                name = label+'-'+row['branch']+'-'+row['extension']+'-'+row['label']
                raw, endpoint = loaded(root/row['path']), loaded(root/row['source_state'])
                check(name+'_fixed_endpoint_identity', np.array_equal(raw['coordinates'], endpoint['coordinates'])
                    and np.array_equal(raw['target_momenta'], endpoint['momenta']))
                radius, mass, lapse = raw['radius'], raw['mass'], np.exp(raw['log_lapse'])
                metric = 1-2*mass/radius
                coupling, source_mass = float(raw['coupling']), float(raw['source_mass'])
                clock = np.sqrt(lapse**2-raw['source_velocity']**2/metric)
                gravity_density = lapse*raw['mass_rhs']/(coupling*np.sqrt(metric))
                matter_density = radius**2*raw['temporal_square']/(2*lapse*np.sqrt(metric))
                matter_density += radius**2*lapse*np.sqrt(metric)*(raw['gradient_square']/2+raw['gram'])
                matter_density += source_mass*raw['source_density']*lapse**2/clock
                check(name+'_matter_constraint_density_identity', np.max(abs(matter_density-gravity_density)) <
                    2e-12*np.max(abs(matter_density)))
                with localcontext() as context:
                    context.prec = 64
                    measured, target, velocity = exact(raw['computed_momenta']), stored(raw['target_momenta']), exact(raw['endpoint_rates'])
                    pairing, computed = np.sum(target*velocity), np.sum(measured*velocity)
                    gravity = np.sum(exact(raw['weights'])*exact(gravity_density))
                    boundary = np.sum(exact(raw['weights'])*exact(raw['mass_rhs']))/Decimal.from_float(coupling)
                    action = Decimal.from_float(float(raw['matter_action']))
                    full = pairing-action-gravity+boundary
                    residual = np.asarray(measured-target, float)
                    baseline = next(candidate for candidate in baseline_run['cases'] if candidate['branch'] == row['branch']
                        and candidate['extension'] == row['extension'] and candidate['label'] == row['baseline_label'])
                    base = Decimal(baseline['energy']['full_shifted_hamiltonian'])
                    drift = full-base
                    matches = all(abs(value-Decimal(row['energy'][key])) < Decimal('1e-55') for key, value in
                        dict(target_pairing=pairing, computed_pairing=computed, gravity_bulk=gravity,
                            boundary_integral=boundary, full_shifted_hamiltonian=full).items())
                inverse = inverses[row['branch']+'-'+row['extension']]
                relative = inverse.residual_norm(residual)/inverse.residual_norm(np.asarray(target, float))
                correction = float(np.max(abs(inverse.solve(residual.ravel()))))
                check(name+'_independent_energy_and_endpoint_inverse', matches and relative < 5e-12
                    and correction < 2e-12 and str(drift) == row['energy_drift']
                    and row['smoke_passed'] == (abs(drift) < Decimal('1e-9')*abs(base))
                    and row['drift_resolved'] == (abs(float(drift)) > 4*row['paired_diagnostic_resolution']))
                report['independent_energy_checks'].append(dict(horizon=label, case=name, energy=str(full), drift=str(drift),
                    relative_residual=relative, maximum_correction=correction, smoke_passed=row['smoke_passed'], valid_for_claim=False))
                energies[(row['branch'], row['extension'], row['label'])] = row
            for row in run['refinement']:
                branch, extension, component = row['branch'], row['extension'], row['component']
                section = slice(None, -1) if row['block'] == 'field' else slice(-1, None)
                initial_row = next(item for item in run['initial_sources'] if item['branch'] == branch and item['extension'] == extension)
                original = loaded(root/initial_row['path'])
                initial = stored(original['coordinates' if component == 0 else 'momenta'])[:, section]
                endpoints = [states[(branch, extension, 'forward'+str(count), count)][component][:, section] for count in [1, 2, 4]]
                with localcontext() as context:
                    context.prec = 64
                    coarse = float(np.max(abs(np.asarray(endpoints[0]-endpoints[1], float))))
                    fine = float(np.max(abs(np.asarray(endpoints[1]-endpoints[2], float))))
                    signal = float(np.max(abs(np.asarray(endpoints[2]-initial, float))))
                scale = max(float(np.max(abs(np.asarray(initial, float)))), 1e-30)
                floor = (2e-15 if component == 0 else 5e-12)*scale
                tolerance = 2e-3*signal+floor
                check(label+'-'+branch+'-'+extension+'-'+str(component)+'-'+row['block']+'_independent_refinement',
                    coarse == row['coarse_difference'] and fine == row['fine_difference'] and signal == row['motion_signal']
                    and row['passed'] == (fine < tolerance and fine <= .4*coarse+2*floor))
            for row in run['energy_refinement']:
                with localcontext() as context:
                    context.prec = 64
                    values = [Decimal(energies[(row['branch'], row['extension'], 'forward'+str(count))]['energy_drift']) for count in [1, 2, 4]]
                    first, second = abs(values[0]-values[1]), abs(values[1]-values[2])
                floor = max(energies[(row['branch'], row['extension'], 'forward'+str(count))]['paired_diagnostic_resolution'] for count in [1, 2, 4])
                ratio = float(second/max(first, Decimal('1e-90')))
                resolved = min(float(first), float(second)) > 4*floor
                check(label+'-'+row['branch']+'-'+row['extension']+'_energy_refinement', str(first) == row['first_difference']
                    and str(second) == row['second_difference'] and row['ratio'] == ratio
                    and row['differences_resolved'] == resolved and row['resolved_order'] == (resolved and ratio < .4))
            for key in ['quadrature', 'reversals']:
                for row in run[key]:
                    branch, extension, component = row['branch'], row['extension'], row['component']
                    section = slice(None, -1) if row['block'] == 'field' else slice(-1, None)
                    initial_row = next(item for item in run['initial_sources'] if item['branch'] == branch and item['extension'] == extension)
                    original = loaded(root/initial_row['path'])
                    initial = stored(original['coordinates' if component == 0 else 'momenta'])[:, section]
                    scale = max(float(np.max(abs(np.asarray(initial, float)))), 1e-30)
                    with localcontext() as context:
                        context.prec = 64
                        if key == 'reversals':
                            reversed_state = states[(branch, extension, 'reverse', 1)][component][:, section]
                            error = float(np.max(abs(np.asarray(reversed_state-initial, float))))
                            tolerance = (2e-14 if component == 0 else 2e-10)*scale
                            expected = row['error']
                        else:
                            fine_row = next(item for item in run['cases'] if item['branch'] == branch and item['extension'] == extension and item['label'] == 'fine')
                            initial_fine = loaded(root/fine_row['previous_path'])
                            fine_initial = stored(initial_fine['coordinates' if component == 0 else 'momenta'])[:, section]
                            fine_state = states[(branch, extension, 'fine', 1)][component][:, section]
                            coarse_state = states[(branch, extension, 'forward1', 1)][component][:, section]
                            fine_increment = np.asarray(fine_state-fine_initial, float)
                            coarse_increment = np.asarray(coarse_state-initial, float)
                            error = float(np.max(abs(fine_increment-coarse_increment)))
                            signal = float(np.max(abs(coarse_increment)))
                            tolerance = 2e-3*signal+(2e-15 if component == 0 else 5e-12)*scale
                            expected = row['increment_difference']
                    check(label+'-'+branch+'-'+extension+'-'+str(component)+'-'+row['block']+'_'+key+'_reconstructed',
                        error == expected and tolerance == row['tolerance'] and row['passed'] == (error < tolerance))
            if run['controls']:
                for case in inverses:
                    seed = loaded(selected[label].parent/(case+'-reverse-seed.npz'))
                    check(label+'-'+case+'_all_reverse_seed_directions', np.count_nonzero(seed['seed']-seed['forward_midpoint']) == 16425)
            check(label+'_summary_flags_match_rows', run['trajectories_qualified'] ==
                all(row['passed'] for key in ['refinement', 'quadrature', 'reversals'] for row in run[key])
                and run['energy_smoke_passed'] == all(row['smoke_passed'] for row in run['endpoints'])
                and run['energy_time_order_resolved'] == all(row['resolved_order'] for row in run['energy_refinement']))
            counts[label] = [table(label+'-'+key, run[key], selected[label], None) for key in
                ['cases', 'iterations', 'endpoints', 'refinement', 'energy_refinement', 'quadrature', 'reversals'] if run[key]]
        counts['independent'] = [table('state-updates', report['independent_step_checks'], destination, None),
            table('energy-checks', report['independent_energy_checks'], destination, None)]
        note = root/'DERIVATION-20260921-longer-coupled-evolution.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('report_complete_sources_exist', 'RESULTS_PENDING' not in content and bool(cited) and all((root/name).is_file() for name in cited))
        for name in cited:
            if (root/name).resolve() != destination.resolve():
                own(root/name)
        own(note)
        for name in ['run_annular_candidate_longer_evolution_20260921.py', 'run_annular_candidate_longer_evolution_v2_20260921.py',
                'run_annular_candidate_longer_evolution_v3_20260921.py',
                'run_annular_candidate_longer_evolution_v4_20260921.py',
                'annular_candidate_anderson_midpoint_20260921.py', 'check_annular_anderson_midpoint_20260921.py',
                'annular_candidate_anderson_midpoint_v2_20260921.py', 'check_annular_anderson_midpoint_v2_20260921.py',
                'seal_annular_candidate_longer_evolution_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('scripts_compile_no_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 21, 1, 15, 4, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), new_coupled_evolution=True,
            implementation_checks={label:len(run['checks']) for label, run in runs.items()},
            trajectories_qualified=all(run['trajectories_qualified'] for run in runs.values()),
            energy_smoke_passed=all(run['energy_smoke_passed'] for run in runs.values()),
            energy_time_order_resolved={label:run['energy_time_order_resolved'] for label, run in runs.items()},
            total_failed_attempts_preserved=prior['total_failed_attempts_preserved']+len(new_failures), new_failures=new_failures,
            distinct_files_rehashed=len(cache), table_rows=counts,
            next_target='Use the measured longer evolution and energy budgets to choose the next dynamical or spatial/physical-force convergence calculation.')
        save()
        print(json.dumps({key:report[key] for key in ['state', 'implementation_checks', 'distinct_files_rehashed',
            'trajectories_qualified', 'energy_smoke_passed', 'energy_time_order_resolved', 'total_failed_attempts_preserved', 'table_rows']}), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
