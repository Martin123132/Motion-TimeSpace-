from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_position_matched_oracle_20260928 import complex_position
from annular_physical_native_kernel_20260928 import NativeKernel
from decimal import localcontext
from time import perf_counter
import json
import numpy as np


evidence = EvidenceRun('annular-position-oracle-diagnostic-attempt01', __file__)
try:
    path = evidence.output.parent / 'annular-compensated-position-attempt02/status.json'
    parent = json.loads(path.read_text())
    evidence.own(path)
    digests = dict(parent['inputs'], **parent['outputs'])
    read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
    live = read(str((evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))
    with localcontext() as context:
        context.prec = 70
        loads, action, sources = restore_case(evidence, digests, 'reference-reference', 'fine', perf_counter() + 600)
        loads.owner.label_order = 28
        packet = read(sources['packet'])
        native = NativeKernel(packet['mesh'], packet['gram_support'], False)
        case = next(row for row in live['cases'] if row['branch'] == 'reference-reference' and row['level'] == 'fine')
        engine = PositionLoads(loads, action, native, read(case['direction_path']), read(case['paths']['projection'])['correction'])
        saved = read(next(relative for relative in parent['outputs'] if relative.endswith('density-check.npz')))
        oracle = complex_position(engine, saved['radius'], 1j * 1e-24)
        rows = []
        for key, values in oracle.items():
            error = float(np.max(abs(saved['analytic_' + key] - values.imag / 1e-24)))
            prior = float(np.max(abs(saved['analytic_' + key] - saved['oracle_' + key])))
            rows.append(dict(field=key, prior_error=prior, matched_base_error=error, scale=float(np.max(abs(saved['analytic_' + key])))))
        evidence.report['diagnostic'] = rows
        evidence.complete()
        print(json.dumps(rows), flush=True)
except BaseException as error:
    evidence.fail(error)
    raise
