from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin
import json
import numpy as np


def main():
    pin(4)
    evidence = EvidenceRun('annular-jump-projection-decomposition-attempt01', __file__)
    try:
        base = 'source-intake/navier-stokes/20260914/'
        names = ['annular-all-native-jump-time-response-attempt01',
            'annular-product-basis-product-time-response-attempt01', 'annular-product-basis-balanced-time-response-attempt01',
            'annular-product-source-corrected-product-time-response-attempt01', 'annular-product-source-corrected-balanced-time-response-attempt01']
        evidence.report.update(results=[], strong_residual_is_inferred_at_same_metric_response=True,
            projection_convergence_proven=False, separate_spatial_material_errors_identified=False, valid_for_claim=False)
        for name in names:
            report = verify_report(evidence, base + name + '/status.json')
            jets = [read_archive(evidence.root / row['path']) for row in report['probes']]
            response_path = evidence.root / base / name / 'strong-weak-response.npz'
            evidence.own(response_path)
            response = read_archive(response_path)
            estimates = [(jet['jump']-jets[0]['jump'])/amount for jet, amount in zip(jets[1:], report['amounts'])]
            measured = (4*estimates[2]-estimates[1])/3
            slope_difference = (response['weak_after']-response['weak_before'])-(response['strong_after']-response['strong_before'])
            transfer = jets[0]['beta'][:, 1:-1]*slope_difference
            inferred_strong = measured-transfer
            index = np.unravel_index(np.argmax(abs(measured)), measured.shape)
            maximum = float(np.max(abs(measured)))
            evidence.check(name + ':time_probe_replayed', maximum == report['witnesses']['jump']['maximum'])
            error = float(np.max(abs(measured-inferred_strong-transfer)))
            evidence.check(name + ':decomposition', error < 5e-15*maximum, error)
            row = dict(run=name, maximum_jump=maximum, maximum_weak_strong_transfer=float(np.max(abs(transfer))),
                maximum_inferred_strong_jump=float(np.max(abs(inferred_strong))),
                witness_label=float(report['labels'][index[0]]), witness_column=int(index[1]),
                at_measured_witness=dict(measured=float(measured[index]), weak_strong_transfer=float(transfer[index]),
                    inferred_strong=float(inferred_strong[index])),
                measured_time_step_spread=report['witnesses']['jump']['Richardson_difference'])
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, measured=measured, weak_strong_transfer=transfer, inferred_strong=inferred_strong)
            evidence.own(path, 'outputs')
            row['path'] = str(path.relative_to(evidence.root))
            evidence.report['results'].append(row)
            evidence.save()
        evidence.complete()
        print(json.dumps(evidence.report['results']), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
