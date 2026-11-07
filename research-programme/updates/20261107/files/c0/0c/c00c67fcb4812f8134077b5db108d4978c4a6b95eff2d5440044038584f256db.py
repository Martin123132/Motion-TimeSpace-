import os
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import psutil
import mpmath as mp
import numpy as np

sys.dont_write_bytecode = True
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / 'final-epoch-real-source-ray000'
OUTPUT = DESTINATION / 'order18-vs26.json'
if OUTPUT.exists():
    raise RuntimeError('Existing quadrature diagnostic preserved')
if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists():
    raise RuntimeError('Owner stop preserved')


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


protocol = read(DESTINATION / 'protocol.json')
budget = protocol['source_refinement_budget']
inputs = {str(DESTINATION / 'protocol.json'): digest(DESTINATION / 'protocol.json'),
          str(Path(__file__)): digest(__file__)}
for order in (18, 26):
    job = DESTINATION / f'order-{order}'
    independent = read(job / 'independent.json')
    if not independent['passed'] or independent['protocol_sha256'] != digest(DESTINATION / 'protocol.json'):
        raise RuntimeError('Both independently verified original radial rules required')
    for name, expected in (('complete.json', independent['complete_sha256']),
                           ('complete.npz', independent['complete_packet_sha256'])):
        path = job / name
        if digest(path) != expected:
            raise RuntimeError('Radial evidence changed')
        inputs[str(path)] = expected
    inputs[str(job / 'independent.json')] = digest(job / 'independent.json')


def vector(packet, mode, suffix):
    modes = ('control', 'difference') if mode == 'combined' else (mode,)
    values = []
    for kernel_mode in modes:
        key = kernel_mode + ':' + suffix
        high, low = packet['total:' + key], packet['total_low:' + key]
        values.append([mp.mpf(float(upper)) + mp.mpf(float(lower)) for upper, lower in zip(high, low)])
    return [mp.fsum(elements) for elements in zip(*values)]


rows = []
with mp.workdps(80), np.load(DESTINATION / 'order-18/complete.npz', allow_pickle=False) as coarse, np.load(DESTINATION / 'order-26/complete.npz', allow_pickle=False) as fine:
    for mode in ('control', 'difference', 'combined'):
        for join in (0, 1):
            for degree in (0, 1, 2):
                for model in ('heavy', 'cold'):
                    for subdivision in (1, 2, 4):
                        for component in ('bank', 'candidate', 'bilinear_delta', 'equilibrium_delta'):
                            suffix = f'join{join}:l{degree}:{model}-s{subdivision}:{component}'
                            first, second = vector(coarse, mode, suffix), vector(fine, mode, suffix)
                            error = mp.sqrt(mp.fsum((left - right)**2 for left, right in zip(first, second)))
                            scale = mp.sqrt(mp.fsum(value**2 for value in second))
                            relative = error / max(scale, mp.mpf('1e-300'))
                            if not mp.isfinite(relative):
                                raise FloatingPointError('Nonfinite quadrature diagnostic')
                            rows.append(dict(mode=mode, join=join, degree=degree, model=model,
                                subdivision=subdivision, component=component, absolute=float(error),
                                scale=float(scale), relative=float(relative), budget=budget,
                                within_component_budget=bool(relative <= budget)))
summary = {}
for component in ('bank', 'candidate', 'bilinear_delta', 'equilibrium_delta'):
    selected = [row for row in rows if row['component'] == component]
    summary[component] = dict(rows=len(selected), above_budget=sum(not row['within_component_budget'] for row in selected),
                              maximum_relative=max(row['relative'] for row in selected),
                              worst=max(selected, key=lambda row: row['relative']))
record = dict(executed=True, finite=True, rows=rows, summary=summary, compared_rules=[18, 26],
              inputs=inputs, process=dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline()),
              finished_at=datetime.now(timezone.utc).isoformat(), budget=budget,
              all_component_rows_within_budget=all(row['within_component_budget'] for row in rows),
              scope='Single final-epoch x14/event0/ray0 finite real/pole source plus separator; includes control+difference kernel combination',
              absolute_quantities_units='Retained weak-source output coordinates, not final-spectrum observables',
              distinction='Two quadrature rules measure a difference, not a certified remaining-error bound',
              full_source_budget_assessed=False, matched_virtual_state_conversion_included=False,
              original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False)
with OUTPUT.open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2, allow_nan=False)
with (DESTINATION / 'order18-vs26.csv').open('x', encoding='utf-8', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(json.dumps(dict(rows=len(rows), all_component_rows_within_budget=record['all_component_rows_within_budget'],
                     summary=summary, full_source_budget_assessed=False)))
