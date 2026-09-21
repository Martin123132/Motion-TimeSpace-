from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime,timezone
import argparse
import hashlib
import json
import numpy as np


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        specifications=[('small','annular-force-adjoint-small-attempt01',33,.05,12),
            ('small_tight','annular-force-adjoint-small-tight-attempt01',33,.05,12),
            ('large','annular-force-adjoint-513-attempt01',513,.4,10),
            ('large_tight','annular-force-adjoint-513-tight-attempt01',513,.4,10)]
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            original_forward_trajectories_reused_not_rerun=True,force_fit=False,force_correction=False,
            only_terminal_04_force_not_entire_force_curve=True,full_GR_gate_upgraded=False,
            duality_gate=2e-9,control_gate=2e-10,interval_arithmetic=False)
        predictions,statuses={},{}
        for name,label,count,terminal,checks in specifications:
            folder=intake/label
            path=folder/'status.json'
            status=json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete',status['state']=='complete' and len(status['checks'])==checks
                and len(status['cases'])==2 and all(row['passed'] for row in status['checks']))
            evidence.check(name+'_independent_unchanged_action',not status['preexisting_forward_predictions_read']
                and not status['finite_future_trajectories_read'] and status['original_action_unchanged']
                and not status['force_fit'] and not status['force_correction']
                and status['count']==count and status['terminal_time']==terminal)
            for branch in ['reference','MTS']:
                path=folder/(branch+'-adjoint.npz')
                evidence.own(path)
                if hashlib.sha256(path.read_bytes()).hexdigest()!=status['outputs'][str(path.relative_to(evidence.root))]:
                    raise RuntimeError('Changed frozen adjoint output.')
                with np.load(path,allow_pickle=False) as saved:
                    predictions[(name,branch)]={key:saved[key].copy() for key in saved.files}
            statuses[name]=status
        frozen=datetime.now(timezone.utc)
        evidence.report['all_adjoint_outputs_verified_at']=frozen.isoformat()
        evidence.check('adjoints_frozen_before_forward_reads',all(datetime.fromisoformat(status['prediction_frozen_at'])<frozen for status in statuses.values()))
        evidence.report['forward_read_phase_started_at']=datetime.now(timezone.utc).isoformat()
        path=intake/'annular-GR-causal-standard-attempt01/status.json'
        forward=json.loads(path.read_text())
        evidence.own(path)
        evidence.check('old_forward_source_complete',forward['state']=='complete' and forward['count']==513
            and forward['configuration']['degree']==768 and forward['configuration']['stride']==1)
        for branch in ['reference','MTS']:
            path=intake/'annular-GR-causal-standard-attempt01'/(branch+'-prediction.npz')
            evidence.own(path)
            if hashlib.sha256(path.read_bytes()).hexdigest()!=forward['outputs'][str(path.relative_to(evidence.root))]:
                raise RuntimeError('Changed preexisting forward result.')
            with np.load(path,allow_pickle=False) as saved:
                terminal_correction=saved['corrections'][-1].copy()
                target=float(saved['force_linear'][-1]-saved['oracle_forces'][-1])
            for name in ['large','large_tight']:
                prediction=predictions[(name,branch)]
                value=float(prediction['predicted_linear_GR_difference'])
                endpoint=float(prediction['decomposition'][0]+prediction['terminal_force_gradient'] @ terminal_correction)
                error=abs(value-target)
                evidence.check(name+'_'+branch+'_existing_forward_duality',error<2e-9,error)
                evidence.check(name+'_'+branch+'_terminal_gradient_consistency',abs(endpoint-target)<2e-11,abs(endpoint-target))
                row=next(row for row in statuses[name]['cases'] if row['branch']==branch)
                denominator=abs(value)
                evidence.report['cases'].append(dict(branch=branch,run=name,count=513,terminal_time=.4,
                    adjoint_GR_difference=value,existing_forward_GR_difference=target,duality_error=error,
                    terminal_gradient_error=abs(endpoint-target),
                    terminal_defect=float(prediction['decomposition'][0]),initial_pairing=float(prediction['decomposition'][1]),
                    base_residual_integral=float(prediction['decomposition'][2]),Gram_residual_integral=float(prediction['decomposition'][3]),
                    absolute_Gram_integral=row['absolute_Gram_integral'],
                    absolute_base_integral=row['absolute_base_integral'],
                    algebraic_cancellation_ratio=float(sum(abs(prediction['decomposition']))/denominator) if denominator else None,
                    physical_GR_claim=False))
        evidence.report['controls']=[]
        for pair in [('small','small_tight'),('large','large_tight')]:
            for branch in ['reference','MTS']:
                standard,tight=[predictions[(name,branch)] for name in pair]
                total_change=abs(float(standard['predicted_linear_GR_difference']-tight['predicted_linear_GR_difference']))
                term_change=float(np.max(abs(standard['decomposition']-tight['decomposition'])))
                evidence.check(pair[0]+'_'+branch+'_total_control',total_change<2e-10,total_change)
                evidence.check(pair[0]+'_'+branch+'_signed_term_control',term_change<2e-10,term_change)
                evidence.report['controls'].append(dict(size=pair[0],branch=branch,total_change=total_change,
                    maximum_signed_term_change=term_change,
                    absolute_Gram_integral_change=float(abs(standard['integrals'][0,-1]-tight['integrals'][0,-1])),
                    absolute_integral_not_an_interval_certified_bound=True))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
