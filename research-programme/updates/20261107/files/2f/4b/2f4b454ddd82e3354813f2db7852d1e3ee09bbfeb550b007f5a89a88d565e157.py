from derive_annular_source_gravity_20260914 import EvidenceRun
from integrate_annular_C0_20260930 import verified_sources
from annular_C0_material_integral_v3_20260930 import MaterialPositionIntegral
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
    parser.add_argument('--level', choices=['fine', 'third'], default='fine')
    parser.add_argument('--cpu', type=int, choices=[2, 4], required=True)
    parser.add_argument('--seconds', type=float, default=6000.)
    parser.add_argument('--orders', type=int, nargs='+', choices=[16, 24, 32], default=[24, 32])
    args = parser.parse_args()
    if args.orders != sorted(set(args.orders)):
        parser.error('Orders must be distinct and ascending')
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    try:
        evidence.report.update(branch=args.branch, level=args.level, github_action=False, subagents_used=False,
            complete_C0_accepted=False, reaction_sensitivity_propagated=False, rule_outputs=[],
            method='material regular volume plus exact Decimal radial-cut jumps', inherited_flags_retained=True)
        digests = verified_sources(evidence)

        def ingest(name):
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            safe_partial = name == args.parent and status.get('external_safe_boundary_stop', False) and not status.get('numerical_failure', True)
            evidence.check(name+':complete_or_saved_parent', (status['state'] == 'complete' or safe_partial)
                and all(row['passed'] for row in status['checks']))
            for category in ['inputs', 'outputs']:
                for relative, expected in status[category].items():
                    if relative == 'CURRENT_LOCAL_RESUME.md':
                        continue
                    source = (evidence.root/relative).resolve()
                    if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed material C0 source: '+relative)
                    digests[str(source.relative_to(evidence.root))] = expected
                    evidence.own(source)
            return status

        parent = ingest(args.parent)
        ingest('annular-C0-material-manufactured-attempt03')
        evidence.check('same_branch_parent', parent['branch'] == args.branch)
        evidence.own(evidence.root/'DERIVATION-20260930-C0-material-cancellation-repair.md')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe material C0 boundary')

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        with localcontext() as context:
            context.prec = 70
            setup = restore_native(evidence, digests, args.branch, args.level, deadline)
            loads, action, read = [setup[key] for key in ['loads', 'action', 'read']]
            report = lambda name:read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
            match = lambda status:next(row for row in status['cases'] if row['branch'] == args.branch and row['level'] == args.level)
            live = match(report('annular-live-support-acceleration-attempt01'))
            jets = match(report('annular-position-metric-jet-validation-attempt01'))
            flow = match(report('annular-direct-background-coupled-current-attempt01'))
            directions = read(live['direction_path'])
            correction = read(live['paths']['projection'])['correction']
            mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
            acceleration = read(flow['paths']['flow'])['acceleration']
            time = ResponseSum(response(read(flow['paths']['background_response'])), response(read(flow['paths']['velocity_response'])))
            owner = report('annular-wave-flux-live-response-'+args.level+'-attempt01')
            selected = next(row for row in owner['cases'] if row['summary']['branch'] == args.branch)
            candidate = read(selected['paths']['candidate'])
            progress('prepare-precise-traces')
            evaluator = MaterialPositionIntegral(action, directions, correction, mode_rate, acceleration,
                candidate['acceleration_change'], setup['precision'].position, time, response(candidate))
            old = next(row for row in parent['cases'] if row['summary']['level'] == args.level)
            old_total = read(old['paths']['combined'])
            events = read(old['paths']['events'])
            results, totals = {}, []
            evaluator.checkpoint_root = evidence.output
            evidence.report['requested_orders'] = args.orders
            for radial_order in args.orders:
                label_order, matter_order = radial_order+4, 64 if radial_order == 32 else 48
                progress('wave-'+str(radial_order))
                result = evaluator.integrate_rows(radial_order, label_order, deadline, progress)
                matter = read(old['paths']['matter'+str(matter_order)])
                full = result['complete']+matter['native']+events['native_atoms']
                full[1:] += matter['dust']+events['dust_atoms']+old_total['gravity24' if radial_order < 32 else 'gravity32']
                evidence.check('finite-'+str(radial_order), np.isfinite(full).all())
                path = evidence.output/('material-wave-'+str(radial_order)+'.npz')
                np.savez_compressed(path, **result, full_C0=full)
                evidence.own(path, 'outputs')
                summary = dict(order=radial_order, C0=full.tolist(),
                    pair=None if not totals else float(np.max(abs(full-totals[-1]))),
                    paired_passed=None if not totals else bool(np.max(abs(full-totals[-1])) <= 2e-17),
                    radial_cut_max=float(np.max(abs(result['radial_cut_atoms']))),
                    old_Eulerian_difference=None if radial_order != 32 else (full-old_total['fine']).tolist(),
                    valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(summary=summary, path=str(path.relative_to(evidence.root))))
                totals.append(full)
                results[radial_order] = result
                evidence.save()
                print(json.dumps(summary), flush=True)
            for partial in evidence.output.glob('partial-material-*.npz'):
                evidence.own(partial, 'outputs')
            evidence.report.update(all_requested_pairs_passed=len(totals) >= 2 and all(row['summary']['paired_passed'] for row in evidence.report['rule_outputs'][1:]),
                all_two_pairs_passed=len(totals) == 3 and all(row['summary']['paired_passed'] for row in evidence.report['rule_outputs'][1:]),
                complete_C0_constructed=True, native_source_gravity_reused=True, seconds=perf_counter()-started)
            evidence.complete()
    except Exception as error:
        for partial in evidence.output.glob('partial-material-*.npz'):
            evidence.own(partial, 'outputs')
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
