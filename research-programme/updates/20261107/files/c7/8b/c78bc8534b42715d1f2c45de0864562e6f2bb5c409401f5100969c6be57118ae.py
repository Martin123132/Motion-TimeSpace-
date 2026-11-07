from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_position_time_eulerian_v2_20260929 import PositionTimeLoads
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse
from annular_background_time_tangent_20260928 import FIELD_NAMES
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-position-time-radial-attempt03')
    parser.add_argument('--label', default='annular-position-time-radial-validation-attempt01')
    parser.add_argument('--max-seconds', type=float, default=2400)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        parent_path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('parent_complete', parent['state'] == 'complete' and len(parent['cases']) == 4 and not parent['probe_only'])
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
        evidence.check('all_inputs_unchanged', not bad, bad)
        evidence.report.update(scope='Fresh off-grid mixed radial equation check',
            github_action=False, subagents_used=False, original_workbench_write=False, new_trajectories=0,
            C0_current_column_computed=False, uncertainty_is_rigorous_bound=False)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live, jets, direct, positions, mixed = [status(name) for name in ['annular-live-support-acceleration-attempt01',
            'annular-position-metric-jet-validation-attempt01', 'annular-direct-background-coupled-current-attempt01',
            'annular-compensated-position-attempt04', 'annular-position-time-loads-attempt01']]
        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                loads.owner.label_order = 28
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, jet, flow, position_case, mixed_case = map(match, [live, jets, direct, positions, mixed])
                directions, correction = read(previous['direction_path']), read(previous['paths']['projection'])['correction']
                mode_rate = read(jet['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(flow['paths']['flow'])['acceleration']
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
                position_engine = PositionLoads(loads, action, native, directions, correction)
                expansion = read(mixed_case['paths']['native']) if native.enabled else None
                engine = PositionTimeLoads(position_engine, mode_rate, acceleration, None if expansion is None else expansion['coefficients'])
                restore = lambda archive: MetricResponse(*reconstructed_solver(archive), archive.get('forcing'), 0., [])
                position_response = TotalResponse(restore(read(position_case['paths']['response'])), restore(read(jet['paths']['transported_old_metric'])))
                time_response = TotalResponse(restore(read(flow['paths']['background_response'])), restore(read(flow['paths']['velocity_response'])))
                response = restore(read(case['paths']['response']))
                solver = response.solver
                cells = np.unique(np.linspace(0, len(solver.lengths) - 1, 257, dtype=int))
                radius = (solver.centers[cells, None] + solver.lengths[cells, None] * np.array([-.319, .047, .283])).ravel()
                fields = {key: np.zeros((4, len(radius))) for key in FIELD_NAMES}
                for start in range(0, len(radius), 32):
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe off-grid mixed response boundary')
                    section = slice(start, start + 32)
                    sampled = engine.sample(radius[section])
                    for key in FIELD_NAMES:
                        fields[key][:, section] = sampled[key]
                values = action.solver.values(action.solution, radius)[0]
                position_values, time_values = position_response.values(radius), time_response.values(radius)
                unused, local = radial_rhs(radius, *values, *[fields[key][0] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass, True)
                amount = 1e-25j
                changed = {key: fields[key][0] + amount * fields[key][1] for key in FIELD_NAMES}
                unused, changed_local = radial_rhs(radius, *(values + amount * position_values), *[changed[key] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass, True)
                forcing = explicit_time_forcing(radius, *(values + amount * position_values),
                    changed['source_density'], changed['velocity'], *[fields[key][2] + amount * fields[key][3] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass).imag / 1e-25
                forcing += np.einsum('abn,bn->an', changed_local.imag / 1e-25, time_values)
                response_values, response_radial = solver.values(response.solution, radius)
                expected = np.einsum('abn,bn->an', local, response_values) + forcing
                error = np.max(abs(response_radial - expected), axis=1)
                scale = np.max(abs(expected), axis=1)
                tolerance = 2e-6 * scale + 2e-15
                path = evidence.output / (name + '-offgrid.npz')
                np.savez_compressed(path, radius=radius, calculated=response_radial, expected=expected,
                    difference=response_radial - expected)
                evidence.own(path, 'outputs')
                for component in range(2):
                    evidence.check(name + ':offgrid_component:' + str(component), error[component] <= tolerance[component],
                        dict(error=float(error[component]), scale=float(scale[component]), tolerance=float(tolerance[component])))
                summary = dict(branch=branch, level=level, points=len(radius), mass_error=float(error[0]),
                    lapse_error=float(error[1]), mass_scale=float(scale[0]), lapse_scale=float(scale[1]), valid_for_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, summary=summary, path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(summary), flush=True)
        table = evidence.output / 'position-time-radial-offgrid.csv'
        with table.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(table, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
