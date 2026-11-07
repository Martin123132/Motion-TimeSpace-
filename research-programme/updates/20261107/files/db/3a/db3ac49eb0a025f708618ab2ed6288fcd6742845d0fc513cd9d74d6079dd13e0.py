import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import psutil
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
import numpy as np
import mpmath as mp

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'execution-v3'
SCIENCE_HASH = '508063733ce6897fc455c4e2f0419614b557abb46f84d1b88a8b45540a2537e1'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def spatial(values, frequency, targets):
    nodes, query = np.log(frequency), np.log(targets)
    positions = np.clip(np.searchsorted(nodes, query, side='right') - 1, 0, len(nodes) - 2)
    fraction = (query - nodes[positions]) / (nodes[positions + 1] - nodes[positions])
    assert np.all(fraction >= -1e-14) and np.all(fraction <= 1 + 1e-14)
    return values[:, positions] + (values[:, positions + 1] - values[:, positions]) * fraction


def metrics_for(before, after, frequency):
    core = np.geomspace(1e-5, 1e-4, 101)
    targets = np.geomspace(float(frequency[0]), 1e-4, 401)
    widths = np.r_[(targets[1] - targets[0]) / 2, (targets[2:] - targets[:-2]) / 2, (targets[-1] - targets[-2]) / 2]
    bose = np.exp(-targets) / (-np.expm1(-targets)) ** 2
    with mp.workdps(50):
        zeta_three = float(mp.zeta(3))
    weights = (widths * targets ** 3 * bose / (2 * zeta_three), widths * targets ** 4 * bose / (np.pi ** 4 / 15))
    core_error = float(np.max(abs(spatial(before, frequency, core) - spatial(after, frequency, core))))
    norm_error = float(np.max(np.linalg.norm(before - after, axis=1)))
    norm_scale = max(float(np.max(np.linalg.norm(after, axis=1))), 1e-300)
    result = [('core', core_error, 1e-4, core_error < 1e-4), ('history_L2', norm_error / norm_scale, .01, norm_error / norm_scale <= .01)]
    sampled_before, sampled_after = (spatial(value, frequency, targets) for value in (before, after))
    for name, weight in zip(('number', 'energy'), weights):
        error = float(np.max(abs((sampled_before - sampled_after) @ weight)))
        magnitude = float(np.max(abs(sampled_after @ weight)))
        envelope = float(np.max(abs(sampled_after))) * float(np.sum(abs(weight)))
        limit = max(.01 * magnitude, 1e-5 * envelope)
        result.append((name, error, limit, error < limit))
    return result


def main(first_cell, last_cell):
    assert 1 <= first_cell <= last_cell and (first_cell - 1) % 8 == 0
    assert last_cell == min(first_cell + 7, 450)
    output = ROOT / f'supervisor-cells{first_cell}-{last_cell}.json'
    assert not output.exists(), 'preserve existing independent report'
    assert digest(RUN / 'science-config.json') == SCIENCE_HASH
    science = read(RUN / 'science-config.json')
    for name, expected in science['code_hashes'].items():
        assert digest(RUN / name) == expected
    assert digest(science['execution_grids']) == science['execution_grids_sha256']
    with np.load(science['execution_grids'], allow_pickle=False) as saved:
        coarse, union, frequency = (saved[name].copy() for name in ('coarse', 'comparison_union', 'frequency'))
    histories, case_heads, new_checks, references, linked_packets = {}, {}, [], [], 0
    prior_hashes = {}
    for case in science['cases']:
        identifier = case['id']
        assert digest(case['driver_history']) == case['driver_history_sha256']
        assert digest(case['seed_metadata']) == case['seed_metadata_sha256']
        times, tails = [], []
        for ordinal, packet in enumerate(case['startup_packets']):
            assert digest(packet['npz']) == packet['sha256']
            assert digest(packet['metadata']) == packet['metadata_sha256']
            with np.load(packet['npz'], allow_pickle=False) as saved:
                selection = slice(1, None) if ordinal else slice(None)
                times.extend(saved['times'][selection])
                tails.extend(saved['tail'][selection])
        assert np.array_equal(times, union[union <= coarse[1]])
        prior_hashes[identifier] = case['seed_metadata_sha256']
        with np.load(case['driver_history'], allow_pickle=False) as driver:
            for cell in range(1, last_cell + 1):
                path = RUN / 'checkpoints' / identifier / f'cell-{cell:04d}.json'
                meta = read(path)
                assert meta['previous_hash'] == prior_hashes[identifier]
                assert meta['science_config_sha256'] == SCIENCE_HASH and meta['state'] == 'committed'
                assert meta['case'] == identifier and meta['cell'] == cell
                assert digest(path.with_suffix('.npz')) == meta['packet_sha256']
                approval_path = RUN / 'attempts' / meta['attempt_id'] / 'approval.json'
                assert digest(approval_path) == meta['attempt_approval_sha256']
                approval = read(approval_path)
                assert approval['approved'] and approval['first_cell'] <= cell <= approval['last_cell']
                assert approval['science_config_sha256'] == SCIENCE_HASH
                endpoint = (cell + 1) * case['subdivision']
                step_tail, step_times, step_rows = np.asarray(tails[-1]), [], []
                step_checks = []
                assert len(meta['step_packets']) == case['subdivision']
                for offset, packet in enumerate(meta['step_packets']):
                    ordinal = cell * case['subdivision'] + offset
                    assert digest(packet['npz']) == packet['sha256']
                    assert digest(packet['metadata']) == packet['metadata_sha256']
                    detail = read(packet['metadata'])
                    info = detail['details']
                    assert detail['state'] == 'complete'
                    assert info['cell'] == cell and info['physical_step_index'] == ordinal
                    assert info['attempt_approval_sha256'] == meta['attempt_approval_sha256']
                    midpoint = (info['start'] + info['stop']) / 2
                    expected_owner = 'bank' if case['kind'] == 'bank' else '189' if midpoint < coarse[science['joins']['join189']] else '199' if midpoint < coarse[science['joins']['join199']] else '200'
                    assert info['owner'] == expected_owner
                    assert not any(info['start'] < coarse[node] < info['stop'] for node in science['joins'].values())
                    assert info['start'] == driver['coordinates'][ordinal] and info['stop'] == driver['coordinates'][ordinal + 1]
                    with np.load(packet['npz'], allow_pickle=False) as saved:
                        assert np.array_equal(saved['carried_initial_tail'], step_tail)
                        assert np.array_equal(saved['tail'][0], step_tail)
                        assert np.array_equal(saved['seed_profile'], driver['profiles'][ordinal])
                        assert np.array_equal(saved['seed_gas'], driver['gas'][ordinal])
                        assert np.array_equal(saved['unchanged_work'], driver['work'][ordinal + 1])
                        assert np.array_equal(saved['force80'], saved['force100'])
                        assert np.isfinite(saved['tail']).all()
                        selection = slice(1, None) if offset else slice(None)
                        step_times.extend(saved['times'][selection])
                        step_rows.extend(saved['tail'][selection])
                        step_tail = saved['tail'][-1].copy()
                    step_checks.extend(detail['checks'])
                    if cell >= first_cell:
                        references.extend(info['reference_comparisons'])
                        linked_packets += 1
                assert step_checks == meta['checks'] and all(row['passed'] for row in step_checks)
                if cell >= first_cell:
                    new_checks.extend(step_checks)
                with np.load(path.with_suffix('.npz'), allow_pickle=False) as saved:
                    wanted = union[(union >= coarse[cell]) & (union <= coarse[cell + 1])]
                    assert np.array_equal(saved['times'], wanted)
                    assert np.array_equal(saved['tail'][0], tails[-1])
                    lookup = {float(value): index for index, value in enumerate(step_times)}
                    selected = np.asarray(step_rows)[[lookup[float(value)] for value in wanted]]
                    assert np.array_equal(saved['tail'], selected)
                    assert np.array_equal(saved['endpoint_tail'], step_tail)
                    for name, original in (('profile', 'profiles'), ('gas', 'gas'), ('work', 'work')):
                        assert np.array_equal(saved[name], driver[original][endpoint])
                    times.extend(saved['times'][1:])
                    tails.extend(saved['tail'][1:])
                prior_hashes[identifier] = digest(path)
                case_heads[(identifier, cell)] = digest(path)
        histories[identifier] = np.asarray(times), np.asarray(tails)
    assert len({row['name'] for row in new_checks}) == len(new_checks)
    reconstructed = []
    previous = science['startup_manifest_sha256']
    for cell in range(1, last_cell + 1):
        path = RUN / 'paired' / f'cell-{cell:04d}.json'
        meta = read(path)
        assert meta['previous_hash'] == previous and meta['state'] == 'paired_passed'
        assert meta['science_config_sha256'] == SCIENCE_HASH
        assert digest(path.with_suffix('.npz')) == meta['packet_sha256']
        assert meta['case_heads'] == {case['id']: case_heads[(case['id'], cell)] for case in science['cases']}
        recorded = {row['name']: row for row in meta['checks']}
        assert len(recorded) == 48 and all(row['passed'] for row in recorded.values())
        wanted = union[union <= coarse[cell + 1]]
        if cell < first_cell:
            previous = digest(path)
            continue
        with np.load(path.with_suffix('.npz'), allow_pickle=False) as saved:
            assert np.array_equal(saved['times'], wanted)
            for model in ('heavy', 'cold'):
                cases = {}
                for subdivision in (1, 2, 4):
                    for kind in ('bank', 'candidate'):
                        times, tails = histories[f'{model}-{kind}-s{subdivision}']
                        assert np.array_equal(times[:len(wanted)], wanted)
                        cases[(kind, subdivision)] = tails[:len(wanted)]
                    response = cases[('candidate', subdivision)] - cases[('bank', subdivision)]
                    cases[('candidate_minus_bank', subdivision)] = response
                    assert np.array_equal(response, saved[f'{model}_response_s{subdivision}'])
                for arm in ('bank', 'candidate', 'candidate_minus_bank'):
                    for coarse_step, fine_step in ((1, 2), (2, 4)):
                        for name, error, limit, passed in metrics_for(cases[(arm, coarse_step)], cases[(arm, fine_step)], frequency):
                            key = f'paired:cell{cell}:{model}:{arm}:{coarse_step}vs{fine_step}:{name}'
                            assert key in recorded
                            assert np.isclose(recorded[key]['value'], error, rtol=1e-8, atol=1e-35), key
                            assert np.isclose(recorded[key]['limit'], limit, rtol=1e-12, atol=1e-35), key
                            reconstructed.append(dict(name=key, error=error, limit=limit, fraction=error / limit, passed=passed))
        previous = digest(path)
    assert len(reconstructed) == 48 * (last_cell - first_cell + 1)
    record = dict(passed=all(row['passed'] for row in reconstructed), verified_cells=list(range(first_cell, last_cell + 1)),
                  full_chain_verified_from_cell=1,
                  through_coarse_node=last_cell + 1, coordinate=float(coarse[last_cell + 1]), common_times=len(wanted),
                  step_packets_verified=linked_packets, unique_local_checks=len(new_checks), independent_metrics=reconstructed,
                  worst_metric=max(reconstructed, key=lambda row: row['fraction']), reference_queries=len(references),
                  maximum_total_tail_reference_raw=max(row['total_tail']['raw'] for row in references),
                  maximum_fast_memory_reference_scaled=max(row['fast_memory']['scaled'] for row in references),
                  source_config_sha256=SCIENCE_HASH, final_paired_sha256=previous, script_sha256=digest(__file__),
                  scope='Independent exact-node chain, saved-driver, seed continuity and manual log-spatial interpolation/trapezoid reconstruction; no production comparison or Store imports',
                  timestamp=datetime.now(timezone.utc).isoformat())
    with output.open('x', encoding='utf-8') as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({key: value for key, value in record.items() if key != 'independent_metrics'}), flush=True)
    assert record['passed']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--first-cell', type=int, default=9)
    parser.add_argument('--last-cell', type=int, default=16)
    arguments = parser.parse_args()
    main(arguments.first_cell, arguments.last_cell)
