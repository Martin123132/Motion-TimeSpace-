from derive_annular_source_gravity_20260914 import EvidenceRun
from diagnose_annular_wave_flux_third_20260930 import verified_sources
from annular_native_precision_context_20260929 import restore_native
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs, DecimalSparseResidual
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import hashlib
import ctypes
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-wave-flux-live-response-third-attempt01', __file__)
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 16):
        raise OSError('Cannot set single-core CPU4 affinity')
    started, deadline = perf_counter(), perf_counter()+3000
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, full_corrected_material_reintegrated=False,
            residual_update_uses_linearity=True, old_weak_evaluator_gate_retained=True,
            github_action=False, subagents_used=False, original_workbench_write=False,
            scope='Wave-only update of saved reference and native-repaired MTS third-grid reactions')
        evidence.own(evidence.root/'DERIVATION-20260929-wave-flux-live-update.md')
        digests = verified_sources(evidence)
        path = evidence.output.parent/'annular-wave-flux-third-candidates-attempt01/status.json'
        candidates = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('both_forcing_candidates_complete', candidates['state'] == 'complete'
            and len(candidates['cases']) == 2 and all(row['passed'] for row in candidates['checks']))
        evidence.check('both_combined_forcing_pairs_pass', all(row['summary']['combined_forcing_pair_passed'] for row in candidates['cases']))
        for category in ['inputs', 'outputs']:
            for relative, expected in candidates[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                if relative in digests and digests[relative] != expected:
                    raise RuntimeError('Conflicting forcing authority: '+relative)
                digests[relative] = expected
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed forcing authority: '+relative)
                evidence.own(path)

        def progress(stage):
            if perf_counter() > deadline:
                raise RuntimeError('Safe wave live response boundary')
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)

        def save(name, **arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        with localcontext() as context:
            context.prec = 70
            for branch in ['reference-reference', 'MTS-primary']:
                progress(branch+':restore')
                setup = restore_native(evidence, digests, branch, 'third', deadline)
                read, inverse = setup['read'], setup['inverse']
                report = lambda name: read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
                norm = lambda value: float(np.max(np.abs(inverse.solve(np.asarray(value, float).ravel()))))
                item = next(row for row in candidates['cases'] if row['summary']['branch'] == branch)
                forcing = read(item['path'])
                old_report = report('annular-position-reaction-diagnostic-attempt04')
                old = next(row for row in old_report['cases'] if row['branch'] == branch and row['level'] == 'third')
                if branch == 'MTS-primary':
                    native = report('annular-native-precision-live-response-attempt01')
                    native_case = next(row for row in native['cases'] if row['summary']['level'] == 'third')
                    base = read(native_case['paths']['candidate'])
                    old_reaction = base['acceleration_change']
                    old_metric = base
                    old_checked = base['residual_by_linear_update']
                    baseline = 'Saved native-precision-updated reaction'
                else:
                    old_reaction = read(old['paths']['reaction'])['acceleration_change']
                    old_metric = read(old['paths']['corrected_metric_time'])
                    old_checked = read(old['paths']['corrected_material'])['complete_residual']
                    baseline = 'Saved reference position reaction'
                short, extension = ('reference', 'reference') if branch.startswith('reference') else ('MTS-primary', 'primary')
                owner = report('annular-'+short+'-third-current-attempt02')
                centre = owner['centres'][0]
                matrix_path = evidence.root/centre['matrix_path']
                if hashlib.sha256(matrix_path.read_bytes()).hexdigest() != digests[centre['matrix_path']]:
                    raise RuntimeError('Changed live matrix')
                evidence.own(matrix_path)
                matrix = load_npz(matrix_path)
                radial = RadialResponse(setup['loads'], setup['action'], extension, deadline, lambda stage: progress(branch+':'+stage))
                momentum = MomentumMetricResponse(setup['action'], deadline, lambda stage: progress(branch+':'+stage))
                evidence.check(branch+':background_unchanged', radial.base_constraint_residual <= 2e-12, radial.base_constraint_residual)
                answers, histories = {}, {}
                for name, rhs in [('correction', forcing['wave_only_live_rhs']), ('sensitivity', -forcing['paired_full_residual'])]:
                    records = []
                    record = lambda row, direction, coupling, residual, metric: records.append(dict(row))
                    answers[name] = solve_joint_rhs(dict(matrix=matrix, inverse=inverse), radial, momentum, rhs, record)
                    histories[name] = records
                    evidence.check(branch+':'+name+':live_equation', records[-1]['relative_residual'] <= 2e-11
                        and records[-1]['maximum_correction'] <= 2e-12, records[-1])
                    progress(branch+':'+name+':solved')
                direction, metric, coupling, unused, history = answers['correction']
                sensitivity, sensitive_metric, unused, unused2, unused3 = answers['sensitivity']
                evidence.check(branch+':combined_live_sensitivity', float(np.max(np.abs(sensitivity))) <= 2e-11,
                    float(np.max(np.abs(sensitivity))))
                independent = momentum.accumulate(metric.values, complex_step=1e-25)
                evidence.check(branch+':metric_momentum_oracle', norm(independent-coupling) <= 2e-11, norm(independent-coupling))
                residual = DecimalSparseResidual(matrix).evaluate(direction, independent, forcing['wave_only_live_rhs'])
                evidence.check(branch+':correction_equation', norm(residual) <= 2e-11, norm(residual))
                evidence.check(branch+':metric_grid_unchanged', np.array_equal(old_metric['edges'], metric.solver.edges))
                changed_metric = {key: old_metric[key]+metric.solution[key] for key in ['state', 'rhs_coefficients', 'primitives', 'left']}
                paths = dict(correction=save(branch+'-wave-live-correction', acceleration_change=direction,
                    correction_residual=residual, independent_coupling=independent, edges=metric.solver.edges,
                    **{'metric_'+key: value for key, value in metric.solution.items()}),
                    sensitivity=save(branch+'-full-forcing-sensitivity', acceleration_change=sensitivity,
                    paired_rhs=-forcing['paired_full_residual'], edges=sensitive_metric.solver.edges,
                    **{'metric_'+key: value for key, value in sensitive_metric.solution.items()}),
                    candidate=save(branch+'-wave-updated-reaction', acceleration_change=old_reaction+direction,
                    residual_by_linear_update=old_checked+residual, edges=metric.solver.edges, **changed_metric))
                row = dict(branch=branch, level='third', starting_reaction=baseline,
                    wave_force_change_inverse=norm(forcing['wave_only_live_rhs']),
                    wave_k0_correction_max=float(np.max(np.abs(direction))),
                    updated_k0_max=float(np.max(np.abs(old_reaction+direction))),
                    metric_time_correction_max=float(np.max(np.abs(metric.solution['state']))),
                    combined_live_pair_max=float(np.max(np.abs(sensitivity))),
                    independent_coupling_inverse=norm(independent-coupling),
                    correction_equation_inverse=norm(residual),
                    updated_equation_via_linear_update=norm(old_checked+residual),
                    full_material_reintegration=False, valid_for_claim=False)
                evidence.report['cases'].append(dict(summary=row, paths=paths, iterations=histories))
                evidence.save()
                print(json.dumps(row), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
