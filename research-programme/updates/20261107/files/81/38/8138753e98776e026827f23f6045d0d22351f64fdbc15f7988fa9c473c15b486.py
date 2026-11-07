from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_transport_identity_20260930 import identity_rows
from time import perf_counter
from decimal import localcontext
import ctypes
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot pin one core')
    evidence = EvidenceRun('annular-C0-transport-probe-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter()+1000
    try:
        with localcontext() as context:
            context.prec = 70
            for branch in ['reference-reference', 'MTS-primary']:
                restored = restore(evidence, branch, 'fine', deadline)
                evaluator = restored['evaluator']
                cells = np.unique(np.linspace(0, len(evaluator.widths)-1, 37).astype(int))
                indices = np.repeat(cells, 9)
                labels = np.tile(np.repeat([-.37, .03, .29], 3), len(cells))
                local = np.tile([.13, .47, .83], 3*len(cells))
                left = evaluator.geometry.geometry(evaluator.edges[indices], labels)[0]
                right = evaluator.geometry.geometry(evaluator.edges[indices+1], labels)[0]
                offsets = left+(right-left)*local
                packet, active = evaluator.packet(labels, offsets)
                rows = identity_rows(evaluator, packet, offsets)
                scale = np.maximum.reduce([abs(rows['material']),abs(rows['eulerian']),abs(rows['transport'])])
                error = float(np.max(abs(rows['defect'])/np.maximum(scale, 1e-100)))
                evidence.check(branch+':active', active.all() and len(offsets)>0)
                evidence.check(branch+':pointwise_transport', error < 1e-10, error)
                evidence.check(branch+':wrong_sign_detected', np.max(abs(rows['wrong_sign'])) > 100*np.max(abs(rows['defect'])))
                width_gap = (packet['node_right']-packet['node_left'])-packet['width']
                coordinate_gap = evaluator.anchor+offsets-packet['node_left']-packet['local']*packet['width']
                geometry_source_gap = evaluator.geometry.source_offset(labels)-evaluator.action.cardinal(labels)@(evaluator.action.source-evaluator.anchor)
                path = evidence.output/(branch+'-probes.npz')
                np.savez_compressed(path, **rows, offsets=offsets, labels=labels, cells=indices,
                    width_gap=width_gap, coordinate_gap=coordinate_gap, geometry_source_gap=geometry_source_gap)
                evidence.own(path,'outputs')
                summary = dict(branch=branch, points=len(offsets), relative_transport_error=error,
                    defect_max=np.max(abs(rows['defect']),axis=1).tolist(),
                    width_gap=float(np.max(abs(width_gap))), coordinate_gap=float(np.max(abs(coordinate_gap))),
                    geometry_source_gap=float(np.max(abs(geometry_source_gap))),
                    metric_derivative_gap=float(np.max(abs(rows['metric_derivative_gap']))))
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary),flush=True)
        evidence.report.update(seconds=perf_counter()-started, full_integral_repeated=False,valid_for_claim=False,github_action=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
