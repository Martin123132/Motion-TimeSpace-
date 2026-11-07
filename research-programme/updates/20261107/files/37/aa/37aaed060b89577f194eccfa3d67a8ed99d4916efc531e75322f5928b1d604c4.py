from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose, reduce_force
from annular_exact_envelope_20261001 import envelope_search
from itertools import product
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun('annular-repaired-compatibility-attempt02', __file__)
    verified = {}

    def verify(relative, expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope input '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key] != expected:
            raise RuntimeError('Changed input '+relative)
        return path

    def status(name):
        path = evidence.output.parent/name/'status.json'
        report = json.loads(verify(str(path.relative_to(evidence.root))).read_text())
        evidence.check(name+':complete', report['state']=='complete' and all(row['passed'] for row in report['checks']))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                if relative != 'CURRENT_LOCAL_RESUME.md':
                    verify(relative, expected)
        return report

    def archive(relative):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned archive '+relative)
        with np.load(path, allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in saved.files}

    def named_archive(name, filename):
        return archive(str((evidence.output.parent/name/filename).relative_to(evidence.root)))

    def save_json(name, value):
        path = evidence.output/(name+'.json')
        with path.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(value, indent=2, allow_nan=False)+'\n')
        evidence.own(path, 'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-repaired-coupled-compatibility.md')
        evidence.own(evidence.root/'DERIVATION-20261001-exact-envelope-vertices.md')
        seal_path = evidence.output.parent/'annular-compensated-polynomial-stage-integrity-20261001.json'
        prior = json.loads(verify(str(seal_path.relative_to(evidence.root))).read_text())
        evidence.check('prior_seal_complete', prior['state']=='complete' and not prior['mismatches'])
        for relative, expected in prior['hashes'].items():
            verify(relative, expected)
        matrix = np.array([[1., 2., -1.], [2., -1., 3.], [0., 1., 1.], [1., 0., 2.]])
        amplitudes = np.array([.3, -.4, .2])
        baseline = -matrix@amplitudes
        manufactured = envelope_search(baseline, matrix, np.full(4, 1e-12), np.full((4, 3), 1e-12))
        evidence.check('manufactured_feasible_orthant_replayed', manufactured['any_replayed_witness'])
        incompatible = baseline.copy()
        incompatible[3] += .1
        impossible = envelope_search(incompatible, matrix, np.full(4, 1e-12), np.full((4, 3), 1e-12))
        evidence.check('manufactured_incompatible_system_rejected', impossible['exact_infeasibility_proven'])
        for name, test_base, test_columns, test_base_error, test_error, expected in [
                ('zero_feasible', np.zeros(4), np.zeros((4, 3)), np.zeros(4), np.zeros((4, 3)), True),
                ('zero_infeasible', np.ones(4), np.zeros((4, 3)), np.zeros(4), np.zeros((4, 3)), False),
                ('error_opens_feasibility', np.ones(4), np.zeros((4, 3)), np.zeros(4), np.ones((4, 3)), True)]:
            test = envelope_search(test_base, test_columns, test_base_error, test_error)
            evidence.check(name, test['any_replayed_witness']==expected)
        for signs in product([-1., 1.], repeat=3):
            trial = np.array(signs)*np.array([.2, .3, .7])
            positive = envelope_search(-matrix@trial, matrix, np.full(4, 1e-12), np.full((4, 3), 1e-12))
            evidence.check('manufactured_sign_'+str(signs), positive['any_replayed_witness'])
            uncertainty = np.arange(12).reshape(4, 3)*1e-4
            actual = abs(incompatible+matrix@trial)-(.01+uncertainty@abs(trial))
            signed = matrix*np.array(signs)
            upper = (signed-uncertainty)@abs(trial)-(.01-incompatible)
            lower = (-signed-uncertainty)@abs(trial)-(.01+incompatible)
            evidence.check('orthant_algebra_'+''.join('p' if value>0 else 'm' for value in signs),
                np.allclose(actual, np.maximum(upper, lower), rtol=1e-13, atol=1e-15))
        parents = status('annular-reacted-support-columns-attempt02')
        sensitivities = status('annular-reacted-column-sensitivity-attempt01')
        status('annular-position-enabled-third-attempt01')
        summaries, budgets = [], []
        for short, branch in [('reference', 'reference-reference'), ('MTS', 'MTS-primary')]:
            match = lambda report:next(row for row in report['cases'] if row['branch']==branch and row['level']=='third')
            case = match(parents)
            combined = archive(case['paths']['combined'])
            material = [archive(case['paths']['material'+str(order)]) for order in [48, 64]]
            sensitivity = archive(match(sensitivities)['paths']['response'])
            old = named_archive('annular-position-enabled-third-attempt01', short+'-assembled.npz')
            gravity_error = np.zeros((3, 4))
            gravity_error[:, 1:] = abs(combined['gravity32']-combined['gravity24'])
            old_parts = dict(material_pair=abs(combined['fine']-combined['coarse']), gravity_pair=gravity_error,
                material_reaction=np.zeros((3, 4)), raw_C2_disagreement=np.zeros((3, 4)), position_oracle=np.zeros((3, 4)))
            old_parts['material_reaction'][1] = np.maximum(abs(material[0]['reaction_delta']), abs(material[1]['reaction_delta']))
            old_parts['raw_C2_disagreement'][2] = np.maximum(*[abs(row['total'][2]-row['raw_complete_C2']) for row in material])
            old_parts['position_oracle'][1] = np.maximum(abs(sensitivity['position_oracle48']), abs(sensitivity['position_oracle64']))
            reconstructed = sum(old_parts.values())
            evidence.check(short+':old_uncertainty_exact_decomposition',
                np.allclose(reconstructed, sensitivity['augmented_uncertainty'], rtol=8e-15, atol=0),
                (reconstructed-sensitivity['augmented_uncertainty']).tolist())
            evidence.check(short+':assembly_matches_parent_columns', np.array_equal(old['historical_columns'], combined['fine'])
                and np.array_equal(old['historical_error'], sensitivity['augmented_uncertainty']))
            compensated_name = 'annular-compensated-C2-'+short+'-third-attempt01'
            replay_name = 'annular-compensated-material-'+short+'-third-attempt02'
            status(compensated_name)
            status(replay_name)
            resolved = [named_archive(compensated_name, 'compensated-'+str(order)+'.npz') for order in [24, 32]]
            replay = [named_archive(replay_name, 'material-'+str(order)+'.npz') for order in [48, 64]]
            source_spread = abs(resolved[1]['columns'][1]-resolved[1]['columns'][2])
            source_results = {}
            for index, variant in [(1, 'rounded_coefficients'), (2, 'parent_nodal')]:
                acceleration = resolved[1]['columns'][index]
                parts = dict(resolved_pair=abs(acceleration-resolved[0]['columns'][index]),
                    material_pair=abs(replay[1]['columns'][index+2]-replay[0]['columns'][index+2]),
                    cross_method=abs(replay[1]['columns'][index+2]-acceleration), source_spread=source_spread,
                    inherited_gravity_pair=gravity_error[2],
                    sampled_arithmetic=256*np.finfo(float).eps*(resolved[1]['sampled_absolute'][[0, 1, index+1]].sum(axis=0)
                        +abs(acceleration)+abs(replay[1]['columns'][index+2])))
                acceleration_error = sum(parts.values())
                evidence.check(short+':'+variant+':finite_complete_error',
                    np.isfinite(acceleration_error).all() and np.all(acceleration_error>=source_spread))
                source_results[variant] = dict(C2=acceleration.tolist(), error_components={key:value.tolist() for key, value in parts.items()},
                    C2_error=acceleration_error.tolist(), retired_historical_components={key:old_parts[key][2].tolist()
                        for key in ['material_pair', 'raw_C2_disagreement']}, physical_source_precision_established=False)
                columns = np.column_stack([old['C0'], old['historical_columns'][1], acceleration])
                column_error = np.column_stack([old['C0_error'], old['historical_error'][1], acceleration_error])
                for baseline_variant in ['historical', 'separate_C0_baseline']:
                    base = old['historical_columns'][0] if baseline_variant=='historical' else old['independent_baseline']
                    base_error = old['historical_error'][0].copy()
                    if baseline_variant!='historical':
                        base_error += old['independent_baseline_pair']+abs(old['baseline_difference'])
                    diagnostic = diagnose(base, columns, base_error, column_error)
                    search = envelope_search(base, columns, base_error, column_error)
                    evidence.check(short+':'+variant+':'+baseline_variant+':solver_outcomes_declared',
                        all(row['solver_status'] in [0, 2] for row in search['orthants']))
                    ablations = {}
                    for group in ['C0', 'C1', 'C2']:
                        altered = column_error.copy()
                        altered[:, ['C0', 'C1', 'C2'].index(group)] = 0
                        diagnostic_ablation = diagnose(base, columns, base_error, altered)
                        ablations[group] = {key:diagnostic_ablation[key] for key in
                            ['rank_resolved', 'sampled_normalized_column_uncertainty', 'any_candidate_within_sampled_uncertainty']}
                    reduced, reduced_columns = reduce_force(base, columns)
                    left_null = np.array(diagnostic['null_obstruction']['left_null'])
                    scale = np.max(abs(reduced_columns), axis=0)
                    evidence.check(short+':'+variant+':'+baseline_variant+':left_null_replay',
                        np.max(abs(left_null@(reduced_columns/scale)))<1e-12)
                    for candidate in diagnostic['candidates']:
                        values = np.array(candidate['amplitudes'])
                        contributions = np.column_stack([base_error, column_error*abs(values)])
                        arithmetic = 64*np.finfo(float).eps*(abs(base)+abs(columns)@abs(values))
                        evidence.check(short+':'+variant+':'+baseline_variant+':'+candidate['method']+':budget_decomposition',
                            np.allclose(contributions.sum(axis=1)+arithmetic, candidate['sampled_uncertainty'], rtol=1e-14, atol=0))
                        candidate['budget_by_origin'] = dict(zip(['baseline', 'C0', 'C1', 'C2'], contributions.T.tolist()))
                        candidate['budget_arithmetic'] = arithmetic.tolist()
                        for condition in range(4):
                            budgets.append(dict(branch=branch, source_variant=variant, baseline_variant=baseline_variant,
                                method=candidate['method'], row=['force', 'h0', 'h1', 'h2'][condition],
                                residual=candidate['residual'][condition], total_budget=candidate['sampled_uncertainty'][condition],
                                baseline_budget=contributions[condition, 0], C0_budget=contributions[condition, 1],
                                C1_budget=contributions[condition, 2], C2_budget=contributions[condition, 3], valid_for_claim=False))
                    detail = dict(branch=branch, source_variant=variant, baseline_variant=baseline_variant,
                        baseline=base.tolist(), columns=columns.tolist(), baseline_error=base_error.tolist(), column_error=column_error.tolist(),
                        diagnostic=diagnostic, envelope_search=search, uncertainty_group_ablations=ablations,
                        inherited_flags_retained=True, spatial_convergence_established=False, finite_history_established=False,
                        uncertainties_are_rigorous_bounds=False, valid_for_claim=False)
                    path = save_json(short+'-'+variant+'-'+baseline_variant, detail)
                    representative = diagnostic['candidates'][0]
                    row = dict(branch=branch, source_variant=variant, baseline_variant=baseline_variant,
                        rank_resolved=diagnostic['rank_resolved'], sigma_min=diagnostic['singular_values'][-1],
                        matrix_uncertainty=diagnostic['sampled_normalized_column_uncertainty'],
                        representative_within=representative['within_sampled_uncertainty'],
                        any_sampled_candidate=diagnostic['any_candidate_within_sampled_uncertainty'],
                        any_envelope_witness=search['any_replayed_witness'],
                        representative_h2=representative['residual'][3], representative_h2_budget=representative['sampled_uncertainty'][3],
                        left_null_obstruction=diagnostic['null_obstruction']['value'], path=path, valid_for_claim=False)
                    summaries.append(row)
                    print(json.dumps(row), flush=True)
            decomposition = dict(branch=branch, old_error_components={key:value.tolist() for key, value in old_parts.items()},
                source_variants=source_results, baseline_difference=old['baseline_difference'].tolist(),
                baseline_pair=old['independent_baseline_pair'].tolist(), valid_for_claim=False)
            evidence.report['cases'].append(dict(branch=branch, decomposition=save_json(short+'-error-provenance', decomposition)))
            evidence.save()
        for name, rows in [('summary', summaries), ('residual-budget', budgets)]:
            path = evidence.output/(name+'.csv')
            with path.open('x', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(newline='', encoding='utf-8') as stream:
                parsed = list(csv.DictReader(stream, strict=True))
            evidence.check(name+':csv_valid', len(parsed)==len(rows) and all(None not in row and row['valid_for_claim']=='False' for row in parsed))
            evidence.own(path, 'outputs')
        evidence.report.update(summaries=summaries, old_error_decomposition_replayed=True,
            central_C2_arithmetic_bias_replaced=True, C0_C1_source_sensitivities_retained=True,
            new_quadrature_launched=False, claim_scope='sampled_discrete_jet_diagnostic_only',
            github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
