from derive_annular_source_gravity_20260914 import EvidenceRun
from integrate_annular_C0_20260930 import verified_sources
from annular_C0_boundary_integral_20260930 import PositionIntegral
from annular_C0_reaction_sensitivity_20260930 import integrate_reaction
from annular_native_precision_context_20260929 import restore_native
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--parent', required=True)
    parser.add_argument('--branch', choices=['reference-reference', 'MTS-primary'], required=True)
    parser.add_argument('--cpu', type=int, choices=[2, 4], required=True)
    parser.add_argument('--seconds', type=float, default=4000.)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    try:
        evidence.report.update(branch=args.branch, level='fine', github_action=False, subagents_used=False,
            reaction_sensitivity_integrated=False, rigorous_error_bound=False, rule_outputs=[],
            inherited_flags_retained=True, valid_for_claim=False)
        digests = verified_sources(evidence)

        def ingest(name):
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+':complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            for category in ['inputs', 'outputs']:
                for relative, expected in status[category].items():
                    if relative == 'CURRENT_LOCAL_RESUME.md':
                        continue
                    source = (evidence.root/relative).resolve()
                    if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed C0 sensitivity input: '+relative)
                    digests[str(source.relative_to(evidence.root))] = expected
                    evidence.own(source)
            return status

        parent = ingest(args.parent)
        ingest('annular-C0-reaction-sensitivity-manufactured-attempt01')
        evidence.check('matched_material_parent', parent['branch'] == args.branch and parent['level'] == 'fine'
            and parent['all_requested_pairs_passed'] and parent['requested_orders'] == [24, 32])
        evidence.own(evidence.root/'DERIVATION-20260930-C0-reaction-sensitivity.md')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe sensitivity boundary')

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        with localcontext() as context:
            context.prec = 70
            setup = restore_native(evidence, digests, args.branch, 'fine', deadline)
            action, read = setup['action'], setup['read']
            report = lambda name:read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
            match = lambda status:next(row for row in status['cases'] if row['branch'] == args.branch and row['level'] == 'fine')
            live = match(report('annular-live-support-acceleration-attempt01'))
            jets = match(report('annular-position-metric-jet-validation-attempt01'))
            flow = match(report('annular-direct-background-coupled-current-attempt01'))
            directions = read(live['direction_path'])
            correction = read(live['paths']['projection'])['correction']
            mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
            acceleration = read(flow['paths']['flow'])['acceleration']
            time = ResponseSum(response(read(flow['paths']['background_response'])), response(read(flow['paths']['velocity_response'])))
            owner = report('annular-wave-flux-live-response-fine-attempt01')
            selected = next(row for row in owner['cases'] if row['summary']['branch'] == args.branch)
            candidate, uncertainty = read(selected['paths']['candidate']), read(selected['paths']['sensitivity'])
            evaluator = PositionIntegral(action, directions, correction, mode_rate, acceleration,
                candidate['acceleration_change'], setup['precision'].position, time, response(candidate))
            totals = []
            for order in [24, 32]:
                progress('reaction-'+str(order))
                result = integrate_reaction(evaluator, uncertainty['acceleration_change'], response(uncertainty),
                    order, order+4, deadline, progress)
                evidence.check('finite-'+str(order), all(np.isfinite(value).all() for value in result.values()))
                evidence.check('nonempty_oracle-'+str(order), int(result['oracle_active_samples']) > 0)
                evidence.check('sampled_independent_oracle-'+str(order), float(result['pointwise_oracle_relative_error']) < 2e-11,
                    float(result['pointwise_oracle_relative_error']))
                path = evidence.output/('reaction-'+str(order)+'.npz')
                np.savez_compressed(path, **result)
                evidence.own(path, 'outputs')
                summary = dict(order=order, reaction_C0=result['complete'].tolist(),
                    pair=None if not totals else float(np.max(abs(result['complete']-totals[-1]))),
                    valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(summary=summary, path=str(path.relative_to(evidence.root))))
                totals.append(result['complete'])
                evidence.save()
                print(json.dumps(summary), flush=True)
            material = {row['summary']['order']:read(row['path'])['full_C0'] for row in parent['rule_outputs']}
            wave_pair = abs(material[32]-material[24])
            reaction_pair = abs(totals[1]-totals[0])
            diagnostic_budget = wave_pair+abs(totals[1])+reaction_pair
            evidence.report.update(reaction_sensitivity_integrated=True,
                reaction_quadrature_difference=reaction_pair.tolist(), material_quadrature_difference=wave_pair.tolist(),
                diagnostic_budget=diagnostic_budget.tolist(), diagnostic_budget_passed=bool(np.max(diagnostic_budget) <= 2e-17),
                gate=2e-17, seconds=perf_counter()-started, native_source_boundary_sensitivity_zero_by_formula=True)
            evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
