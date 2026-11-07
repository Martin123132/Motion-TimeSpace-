from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_support_radial_response_20260928 import gravitational_moments
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
from decimal import localcontext
from time import perf_counter
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot pin one core')
    evidence = EvidenceRun('annular-compensated-C2-attribution-attempt01',__file__)
    verified = {}
    deadline = perf_counter()+900

    def status(name):
        path = evidence.output.parent/name/'status.json'
        record = json.loads(path.read_text())
        evidence.own(path)
        evidence.check(name+':complete',record['state']=='complete' and all(row['passed'] for row in record['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in record[category].items():
                source = (evidence.root/relative).resolve()
                if not source.is_relative_to(evidence.root):
                    raise RuntimeError('Out-of-scope source')
                key = str(source.relative_to(evidence.root))
                if key not in verified:
                    verified[key] = hashlib.sha256(source.read_bytes()).hexdigest()
                    evidence.own(source)
                if verified[key]!=expected:
                    raise RuntimeError('Changed attribution source '+relative)
        return record

    def archive(relative):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned attribution archive')
        with np.load(path,allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in saved.files}

    try:
        historical = status('annular-reacted-column-sensitivity-attempt01')
        rows = []
        for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
            current = status('annular-compensated-C2-'+short+'-third-attempt01')
            parent = status(current['resolved_parent'])
            evidence.check(short+':completed_same_node_ablation',current['integrated_ablation_complete'] and current['branch']==branch)
            low,high = [archive(row['path']) for row in current['rule_outputs']]
            evidence.check(short+':rule_shapes',low['columns'].shape==high['columns'].shape==(3,4))
            case = next(row for row in historical['cases'] if row['branch']==branch and row['level']=='third')
            owned = archive(case['paths']['response'])
            old,old_error = owned['columns'][2],owned['augmented_uncertainty'][2]
            resolved = archive(parent['rule_outputs'][-1]['path'])
            gap = high['columns'][0]-old
            case_summary = dict(branch=branch,old_C2=old.tolist(),old_error=old_error.tolist(),resolved_gap=gap.tolist(),variants=[])
            for index,variant in [(1,'rounded_coefficients'),(2,'parent_nodal')]:
                corrected = high['columns'][index]
                shift = corrected-high['columns'][0]
                pair = abs(corrected-low['columns'][index])
                remaining = corrected-old
                variant_summary = dict(variant=variant,column=corrected.tolist(),change=shift.tolist(),pair=pair.tolist(),
                    remaining_old_difference=remaining.tolist(),valid_for_claim=False)
                case_summary['variants'].append(variant_summary)
                for component,name in enumerate(['force','h0','h1','h2']):
                    rows.append(dict(branch=branch,variant=variant,component=name,old=old[component],resolved=high['columns'][0,component],
                        corrected=corrected[component],arithmetic_change=shift[component],old_gap=gap[component],remaining=remaining[component],
                        signed_fraction_of_gap_removed=-shift[component]/gap[component] if gap[component]!=0 else '',
                        remaining_over_old_error=abs(remaining[component])/old_error[component] if old_error[component]>0 else '',
                        paired_difference=pair[component],valid_for_claim=False))
            with localcontext() as context:
                context.prec = 80
                restored = restore(evidence,branch,'third',deadline)
                evaluator,read,report = [restored[key] for key in ['evaluator','read','report']]
                live = next(row for row in report('annular-live-support-acceleration-attempt01')['cases'] if row['branch']==branch and row['level']=='third')
                saved_response = read(live['paths']['live_response'])
                solver,solution = reconstructed_solver(saved_response)
                response = MetricResponse(solver,solution,saved_response.get('forcing'),0.,[])
                old_gravity = gravitational_moments(evaluator.action,response,32)
                points,weights = np.polynomial.legendre.leggauss(32)
                radius = (solver.centers[:,None]+solver.lengths[:,None]*points/2).ravel()
                measure = (solver.lengths[:,None]*weights/2).ravel()
                offsets = radius-evaluator.anchor
                trace = PolynomialTrace(solver,solution,evaluator.anchor)
                values = evaluator.metric.evaluate(offsets,evaluator.metric.cells(offsets))[0]
                coefficient = np.exp(values[1])/(evaluator.action.owner.coupling*np.sqrt(1-2*values[0]/radius))
                temporal_mass = trace.evaluate(offsets,trace.cells(offsets))[0][0]
                centered_gravity = np.array([measure@(coefficient*temporal_mass*(radius-6)**power) for power in range(3)])
                resolved_gravity = resolved['gravity'][1]
                gravity_change = resolved_gravity-old_gravity
                remaining_wave = gap[1:]-gravity_change
                evidence.check(short+':finite_gravity_attribution',np.isfinite(np.r_[old_gravity,centered_gravity,resolved_gravity,remaining_wave]).all())
                output = evidence.output/(short+'-attribution.npz')
                np.savez_compressed(output,old_C2=old,old_error=old_error,columns=high['columns'],coarse_columns=low['columns'],
                    old_gravity=old_gravity,centered_same_node_gravity=centered_gravity,resolved_gravity=resolved_gravity,
                    gravity_change=gravity_change,remaining_wave_difference=remaining_wave)
                evidence.own(output,'outputs')
                case_summary.update(old_gravity=old_gravity.tolist(),centered_same_node_gravity=centered_gravity.tolist(),
                    resolved_gravity=resolved_gravity.tolist(),gravity_change=gravity_change.tolist(),
                    remaining_wave_difference=remaining_wave.tolist(),path=str(output.relative_to(evidence.root)))
            evidence.report['cases'].append(case_summary)
            evidence.save()
            print(json.dumps(case_summary),flush=True)
        table = evidence.output/'attribution.csv'
        with table.open('x',newline='',encoding='utf-8') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with table.open(newline='',encoding='utf-8') as stream:
            parsed = list(csv.DictReader(stream,strict=True))
        evidence.check('attribution_CSV_clean',len(parsed)==16 and all(None not in row and all(value is not None for value in row.values()) for row in parsed))
        evidence.own(table,'outputs')
        evidence.report.update(same_node_acceleration_ablation_complete=True,gravity_attribution_complete=True,
            candidate_refit_performed=False,inherited_flags_retained=True,uncertainty_shrunk=False,
            valid_for_claim=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
