from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report,validate_result,compare_orders
import ctypes
import json


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<4):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-null-acceleration-summary-recovery-attempt02',__file__)
    try:
        failed_recovery = verify_report(evidence,'source-intake/navier-stokes/20260914/annular-native-null-acceleration-summary-recovery-attempt01/status.json')
        evidence.check('recognized_replay_notation_failure',failed_recovery['state']=='failed' and 'too many subscripts' in failed_recovery['error'])
        for level in ['fine','third']:
            relative = 'source-intake/navier-stokes/20260914/annular-native-null-acceleration-'+level+'-attempt01/status.json'
            report = verify_report(evidence,relative)
            evidence.check(level+':recognized_summary_only_failure',report['state']=='failed'
                and report['error']=='TypeError("bad operand type for abs(): \'list\'")'
                and 'quadrature_gate_relative_difference' in report['traceback'])
            evidence.check(level+':both_scientific_orders_saved',[(row['spatial'],row['material']) for row in report['results']]==[(12,48),(16,64)])
            validated = []
            corrected = []
            for result in report['results']:
                prefix = str(result['spatial'])+'-'+str(result['material'])
                validated.append(validate_result(evidence,result,level+':'+prefix))
                independent = next(row for row in report['checks'] if row['name']==prefix+':independent_momentum_Jacobian')
                item = dict(result)
                item['momentum_oracle_relative_error'] = independent['detail']
                corrected.append(item)
            evidence.report['cases'].append(dict(level=level,source_report=relative,
                source_state='failed_metadata_only',scientific_outputs_independently_replayed=True,
                momentum_summary_corrected_from_original_check=True,results=corrected,
                **compare_orders(*validated)))
            evidence.save()
        evidence.report.update(original_files_changed=False,scope='Recovery of final list/array summary error only; no scientific rerun or altered acceleration.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
