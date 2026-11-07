from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_physical_native_kernel_20260928 import NativeKernel, decimals, maximum
from annular_position_time_loads_20260929 import native_label, decimal_rule
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def native_corner(engine, mode_rate, label, step):
    unused, unused2, data, edge_position, field_position = engine.native_direct(label)
    cardinal = decimals(data['cardinal'])
    field_mixed = decimals(mode_rate[:, :-1].T) @ cardinal
    edge_time = data['displacement'] * data['source_velocity']
    edge_mixed = data['displacement'] * (decimals(mode_rate[:, -1]) @ cardinal)
    answer = np.full(engine.native.template.shape[0], Decimal(0), object)
    for position_sign in [-1, 1]:
        for time_sign in [-1, 1]:
            position, time = position_sign * step, time_sign * step
            edges = data['edges'] + position * edge_position + time * edge_time + position * time * edge_mixed
            fields = data['field'] + position * field_position + time * data['rate'] + position * time * field_mixed
            image = engine.native.apply('template', engine.native.kernel_values(edges, engine.native.atoms(edges, fields)))
            answer += position_sign * time_sign * image
    return answer / (4 * step**2)


def source_corner(engine, mode_rate, step):
    total = np.full(3, Decimal(0), object)
    for label, quadrature in decimal_rule(64):
        cardinal = decimals(engine.material.interpolation(np.array([float(label)]))[0])
        source = decimals(engine.material.coordinates[:, -1]) @ cardinal
        movement = decimals(engine.direction[:, -1]) @ cardinal
        speed = decimals(engine.loads.rates[:, -1]) @ cardinal
        mixed = decimals(mode_rate[:, -1]) @ cardinal
        weight = Decimal('1.5') - 6 * label**2
        for position_sign in [-1, 1]:
            for time_sign in [-1, 1]:
                position, time = position_sign * step, time_sign * step
                radius = source + position * movement + time * speed + position * time * mixed
                for power in range(3):
                    total[power] += position_sign * time_sign * quadrature * weight * (radius - 6)**power
    return np.asarray(total / (4 * step**2), float)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-position-time-loads-attempt01')
    parser.add_argument('--label', default='annular-position-time-load-validation-attempt01')
    parser.add_argument('--max-seconds', type=float, default=3600)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        parent_path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('parent_completed_four_cases', parent['state'] == 'complete' and len(parent['cases']) == 4)
        evidence.report.update(scope='Independent original-kernel mixed finite-family replay and source mass test',
            github_action=False, subagents_used=False, original_workbench_write=False, new_trajectories=0,
            B0_radial_solved=False, C0_current_column_computed=False, uncertainty_is_rigorous_bound=False)
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[relative] = expected
                    evidence.own(path)
        evidence.check('input_hashes_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live = status('annular-live-support-acceleration-attempt01')
        jets = status('annular-position-metric-jet-validation-attempt01')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe independent mixed-loading boundary')

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, jet = match(live), match(jets)
                directions = read(previous['direction_path'])
                correction = read(previous['paths']['projection'])['correction']
                mode_rate = read(jet['paths']['completed_metric_time'])['mode_rate']
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
                engine = PositionLoads(loads, action, native, directions, correction)
                source = read(case['paths']['source_density64'])
                corner = source_corner(engine, mode_rate, Decimal('1e-10'))
                error = float(np.max(abs(corner - source['weak'])))
                tolerance = 2e-8 * float(np.max(abs(source['weak']))) + 1e-23
                evidence.check(name + ':source_direct_four_corner', error <= tolerance, dict(error=error, tolerance=tolerance))
                evidence.check(name + ':source_number_mixed_zero', abs(corner[0]) <= 1e-40, float(corner[0]))
                native_error, native_scale, halving_error = 0., 0., 0.
                if native.enabled:
                    for label in [-.31, .14, .39]:
                        progress(name + ':native-direct-corners:' + str(label))
                        first = native_corner(engine, mode_rate, label, Decimal('1e-10'))
                        second = native_corner(engine, mode_rate, label, Decimal('5e-11'))
                        tangent = native_label(engine, mode_rate, label)[0][3]
                        difference = float(np.max(abs(np.asarray(second, float) - tangent)))
                        scale = float(maximum(second))
                        truncation = float(maximum(first - second))
                        tolerance = 2e-9 * scale + 1e-25
                        evidence.check(name + ':native_original_kernel:' + str(label), difference <= tolerance,
                            dict(error=difference, tolerance=tolerance, step_difference=truncation))
                        evidence.check(name + ':native_corner_halving:' + str(label), truncation <= tolerance, truncation)
                        native_error, native_scale = max(native_error, difference), max(native_scale, scale)
                        halving_error = max(halving_error, truncation)
                summary = dict(branch=branch, level=level, source_corner_error=error,
                    source_mass_mixed=float(corner[0]), native_corner_error=native_error,
                    native_corner_scale=native_scale, native_step_difference=halving_error, valid_for_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, summary=summary))
                progress(name + ':complete')
                del loads, action, engine, native
                gc.collect()
        path = evidence.output / 'mixed-loading-independent-validation.csv'
        with path.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
