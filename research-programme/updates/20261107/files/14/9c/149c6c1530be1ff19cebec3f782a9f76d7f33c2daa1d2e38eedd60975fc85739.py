from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_live_compensation_derivative_20260928 import CompensationLoads as CoefficientLoads
from annular_compensation_cardinal_source_20260928 import CompensationLoads
from annular_compensation_complex_oracle_20260928 import complex_mixed_wave as coefficient_oracle
from annular_compensation_complex_oracle_v2_20260928 import complex_mixed_wave as cardinal_oracle
from time import perf_counter
from decimal import localcontext
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-compensation-replay-diagnostic-attempt01', __file__)
    try:
        parent_path = evidence.output.parent / 'annular-live-compensation-time-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live = status('annular-live-support-acceleration-attempt01')['cases'][0]
        geometric = status('annular-geometric-support-jet-attempt01')['cases'][0]
        direct = status('annular-direct-background-coupled-current-attempt01')['cases'][0]
        with localcontext() as context:
            context.prec = 70
            loads, action, unused = restore_case(evidence, digests, 'reference-reference', 'fine', perf_counter() + 1800)
            arguments = (loads, action, read(direct['paths']['flow'])['acceleration'], read(live['direction_path']),
                read(live['paths']['projection'])['correction'], read(geometric['vertex_path'])['vertices'] / 2)
            baseline = read(live['paths']['live_response'])
            initial = read(str((evidence.output / '../annular-live-compensation-time-attempt01/reference-reference-fine-mixed-density.npz').resolve().relative_to(evidence.root)))
            errors = abs(initial['temporal'] - baseline['delta_temporal'])
            indices = np.argsort(errors)[-16:]
            radius = initial['nodes'].ravel()[indices]
            centres = (baseline['edges'][1:] + baseline['edges'][:-1]) / 2
            widths = np.diff(baseline['edges'])
            selected = np.linspace(0, len(widths) - 1, 41, dtype=int)
            probes = centres[selected] + .173 * widths[selected]
            loads.owner.label_order = 28
            rows = []
            for label, constructor in [('coefficient', CoefficientLoads), ('cardinal', CompensationLoads)]:
                engine = constructor(*arguments)
                values, unused = engine.mixed_wave(radius)
                unused, derivative = engine.mixed_wave(probes)
                old_oracle = coefficient_oracle(engine, probes, 1j * 1e-25).imag / 1e-25
                new_oracle = cardinal_oracle(engine, probes, 1j * 1e-25).imag / 1e-25
                row = dict(convention=label, density_error=float(np.max(abs(values - baseline['delta_temporal'][indices]))),
                    coefficient_oracle_error=float(np.max(abs(derivative - old_oracle))),
                    cardinal_oracle_error=float(np.max(abs(derivative - new_oracle))), derivative_scale=float(np.max(abs(derivative))))
                rows.append(row)
                path = evidence.output / (label + '-diagnostic.npz')
                np.savez_compressed(path, radius=radius, evaluated=values, archived=baseline['delta_temporal'][indices],
                    probe_radius=probes, analytic=derivative, coefficient=old_oracle, cardinal=new_oracle)
                evidence.own(path, 'outputs')
            evidence.report.update(summaries=rows, scope='Exploratory cancellation localization; not a new physical authority')
            print(json.dumps(rows), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
