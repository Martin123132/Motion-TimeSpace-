from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from integrate_annular_C0_higher_grid_20260930 import material_rows
from annular_compact_baseline_current_v2_20261001 import compact_rows
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from decimal import localcontext
from time import perf_counter
from math import fsum
import argparse
import ctypes
import hashlib
import json
import os
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--branch', choices=['reference-reference', 'MTS-primary'], required=True)
    parser.add_argument('--cpu', choices=[2, 4], type=int, required=True)
    parser.add_argument('--seconds', type=float, default=10200)
    parser.add_argument('--resume-from')
    args = parser.parse_args()
    if not 0<args.seconds<=10800:
        parser.error('Time budget outside safe range')
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1<<args.cpu):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    verified = {}

    def verify(relative, expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Invalid baseline source '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key]!=expected:
            raise RuntimeError('Changed baseline source '+relative)
        return path

    def status(name, complete=True):
        path = (evidence.output.parent/name/'status.json').resolve()
        if path.parent.parent!=evidence.output.parent:
            raise ValueError('Invalid baseline parent')
        report = json.loads(verify(str(path.relative_to(evidence.root))).read_text())
        if complete:
            evidence.check(name+':complete', report['state']=='complete' and all(row['passed'] for row in report['checks']))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                if relative!='CURRENT_LOCAL_RESUME.md':
                    verify(relative, expected)
        return report

    def archive(relative):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned baseline archive '+relative)
        with np.load(path, allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in saved.files}

    def save(name, **arrays):
        path = evidence.output/(name+'.npz')
        if path.exists():
            raise FileExistsError(path)
        np.savez_compressed(path, **arrays)
        evidence.own(path, 'outputs')
        return str(path.relative_to(evidence.root))

    def progress(order, index, count):
        evidence.report['progress'] = dict(order=order, next_index=index, radial_nodes=count, seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']), flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe coefficient-baseline boundary')

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-integrated-baseline-current-contract.md')
        prior_path = evidence.output.parent/'annular-repaired-compatibility-stage-integrity-20261001.json'
        prior = json.loads(verify(str(prior_path.relative_to(evidence.root))).read_text())
        evidence.check('prior_stage_complete', prior['state']=='complete' and not prior['mismatches'])
        for relative, expected in prior['hashes'].items():
            verify(relative, expected)
        short = 'reference' if args.branch=='reference-reference' else 'MTS'
        parent_name = 'annular-C0-higher-'+short+'-third-attempt02'
        parent = status(parent_name)
        evidence.check('matched_complete_parent', parent['branch']==args.branch and parent['level']=='third'
            and parent['complete_integral_constructed'] and parent['all_requested_pairs_passed'])
        evidence.report.update(branch=args.branch, level='third', baseline_parent=parent_name, rule_outputs=[],
            all_nonwave_terms_held=True, force_row_held=True, original_control='material_rows.real',
            github_action=False, subagents_used=False, parent_coefficients_not_fitted=True, valid_for_claim=False)
        resume_directory, reusable = None, {}
        if args.resume_from:
            saved = status(args.resume_from, complete=False)
            evidence.check('safe_resume', saved['state']=='failed' and saved.get('error')=="RuntimeError('Safe coefficient-baseline boundary')"
                and saved['branch']==args.branch and saved['baseline_parent']==parent_name and all(row['passed'] for row in saved['checks']))
            key = str((evidence.root/'scripts/integrate_annular_coefficient_baseline_20261001.py').relative_to(evidence.root))
            evidence.check('same_resume_algorithm', saved['inputs'][key]==evidence.report['inputs'][key])
            resume_directory = evidence.output.parent/args.resume_from
            reusable = {row['summary']['order']:row for row in saved['rule_outputs']}
        parent_rules = {row['summary']['order']:archive(row['path']) for row in parent['rule_outputs']}
        with localcontext() as context:
            context.prec = 70
            restored = restore(evidence, args.branch, 'third', deadline)
            evaluator = restored['evaluator']
            endpoints = np.concatenate([evaluator.geometry.geometry(evaluator.edges, label)[0] for label in [-.5, .5]])
            cuts = np.unique(np.r_[evaluator.radial_cuts, endpoints])
            for order, material_order in [(24, 48), (32, 64)]:
                if order in reusable:
                    archive(reusable[order]['path'])
                    evidence.report['rule_outputs'].append(reusable[order])
                    evidence.save()
                    continue
                paths = parent['component_paths']
                wave = archive(paths['wave'+str(order)])
                matter = archive(paths['matter'+str(material_order)])
                gravity = archive(paths['gravity'+str(order)])
                points, weights = np.polynomial.legendre.leggauss(order)
                lengths = np.diff(cuts)
                offsets = (cuts[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
                measures = (lengths[:, None]*weights/2).ravel()
                node_hash = hashlib.sha256(cuts.tobytes()+offsets.tobytes()+measures.tobytes()).hexdigest()
                evidence.check('same_parent_quadrature-'+str(order), np.array_equal(wave['quadrature'], [order, order+4, len(offsets)]))
                total, correction, absolute = np.zeros((3, 4)), np.zeros((3, 4)), np.zeros((3, 4))
                next_index = 0
                if resume_directory is not None:
                    partial = resume_directory/('partial-baseline-'+str(order)+'.npz')
                    if partial.exists():
                        stored = archive(str(partial.relative_to(evidence.root)))
                        if bool(stored['complete']) or int(stored['order'])!=order or str(stored['node_hash'])!=node_hash:
                            raise RuntimeError('Changed baseline partial')
                        total, correction, absolute = [stored[name] for name in ['total', 'correction', 'absolute']]
                        next_index = int(stored['next_index'])
                        if any(value.shape!=(3, 4) or not np.isfinite(value).all() for value in [total, correction, absolute]) or next_index%16 or not 0<=next_index<=len(offsets):
                            raise RuntimeError('Invalid baseline partial state')
                for start in range(next_index, len(offsets), 16):
                    if start%2048==0:
                        path = evidence.output/('partial-baseline-'+str(order)+'.npz')
                        temporary = path.with_suffix('.npz.tmp')
                        with temporary.open('wb') as stream:
                            np.savez_compressed(stream, total=total, correction=correction, absolute=absolute, order=order,
                                next_index=start, total_nodes=len(offsets), node_hash=node_hash, complete=False)
                            stream.flush()
                            os.fsync(stream.fileno())
                        temporary.replace(path)
                        progress(order, start, len(offsets))
                    section = slice(start, start+16)
                    density = CenteredLabelDensity(evaluator.action, offsets[section], order+4)
                    selected = offsets[section][density.indices]
                    packet, active = evaluator.packet(density.offsets, selected)
                    old = material_rows(evaluator, packet, selected).real
                    values, unused, radial, unused2 = evaluator.metric.evaluate(selected, evaluator.metric.cells(selected))
                    time = sum(item.evaluate(selected, item.cells(selected))[0] for item in evaluator.time_traces)
                    new = compact_rows(packet, evaluator.anchor+selected, values, radial, time)
                    new[0] = old[0]
                    rows = np.array([old, new, new-old])
                    measure = measures[section][density.indices]*density.label_weights*active
                    block = rows@measure
                    updated = total+block
                    correction += np.where(abs(total)>=abs(block), (total-updated)+block, (block-updated)+total)
                    total = updated
                    absolute += abs(rows)@measure
                accumulated = total+correction
                replay_difference = accumulated[0]-wave['base']
                replay_budget = 256*np.finfo(float).eps*(absolute[0]+abs(wave['base'])+abs(accumulated[0]))
                evidence.check('actual_old_wave_replay-'+str(order), np.all(abs(replay_difference)<=replay_budget),
                    dict(difference=replay_difference.tolist(), budget=replay_budget.tolist()))
                original = parent_rules[order]['baseline']
                assembled = wave['base']+matter['native_base']
                assembled[1:] += matter['dust_base']+gravity['base']
                evidence.check('original_held_terms_reconstruct-'+str(order), np.array_equal(assembled, original))
                baseline = original+accumulated[2]
                direct = np.array([original[0]]+[fsum([accumulated[1, index], matter['native_base'][index],
                    matter['dust_base'][index-1], gravity['base'][index-1]]) for index in range(1, 4)])
                evidence.check('held_force_and_finite_baselines-'+str(order), baseline[0]==original[0]
                    and accumulated[2, 0]==0 and np.isfinite(np.r_[baseline, direct, accumulated.ravel()]).all())
                delta_replay = accumulated[1]-accumulated[0]-accumulated[2]
                evidence.check('difference_accumulation_replay-'+str(order), np.all(abs(delta_replay)<=
                    256*np.finfo(float).eps*(absolute[0]+absolute[1]+absolute[2])))
                previous = evidence.report['rule_outputs']
                pair = None if not previous else baseline-np.array(previous[-1]['summary']['baseline'])
                path = save('baseline-'+str(order), baseline=baseline, direct_baseline=direct, original_baseline=original,
                    accumulated=accumulated, sampled_absolute=absolute, old_wave_replay_difference=replay_difference,
                    old_wave_replay_budget=replay_budget, assembly_difference=direct-baseline,
                    delta_replay=delta_replay, held_native=matter['native_base'], held_dust=matter['dust_base'],
                    held_gravity=gravity['base'], quadrature=np.array([order, order+4, len(offsets)]), node_hash=node_hash)
                summary = dict(order=order, baseline=baseline.tolist(), direct_baseline=direct.tolist(),
                    correction=accumulated[2].tolist(), old_wave_replay_difference=replay_difference.tolist(),
                    assembly_difference=(direct-baseline).tolist(), pair=None if pair is None else pair.tolist(),
                    node_hash=node_hash, valid_for_claim=False)
                evidence.report['rule_outputs'].append(dict(path=path, summary=summary))
                evidence.save()
                print(json.dumps(summary), flush=True)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path, 'outputs')
        evidence.report.update(both_integral_rules_completed=True, seconds=perf_counter()-started,
            parent_source_precision_proven=False, physical_uncertainty_shrunk=False)
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path, 'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
