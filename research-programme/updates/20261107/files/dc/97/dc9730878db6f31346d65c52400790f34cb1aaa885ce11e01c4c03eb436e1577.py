from derive_annular_source_gravity_20260914 import EvidenceRun
from integrate_annular_C0_20260930 import verified_sources
from annular_C0_boundary_integral_20260930 import PositionIntegral, metric_beta_jump, dust_event_atoms
from annular_C0_boundary_integral_v2_20260930 import native_coefficient_rows
from annular_position_support_column_20260930 import gravity_position_rows
from annular_native_precision_context_20260929 import restore_native
from annular_native_tangent_precision_repair_20260929 import repair_engine
from annular_physical_native_kernel_20260928 import decimals
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from scipy.fft import dct
from decimal import localcontext
from time import perf_counter
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 16):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun('annular-C0-integral-MTS-native-recovery-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter()+2400.
    try:
        evidence.report.update(branch='MTS-primary', level='fine', github_action=False, subagents_used=False,
            original_workbench_write=False, native_events_interpolated=True, interpolation_error_is_rigorous_bound=False,
            reaction_sensitivity_propagated=False, complete_C0_accepted=False)
        digests = verified_sources(evidence)
        path = evidence.output.parent/'annular-C0-integral-MTS-attempt02/status.json'
        parent = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('saved_parent_boundary', parent.get('external_safe_boundary_stop') and not parent['numerical_failure']
            and parent.get('unsaved_native_event_partial_discarded') and all(row['passed'] for row in parent['checks']))
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                source = (evidence.root/relative).resolve()
                if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed reusable component: '+relative)
                digests[str(source.relative_to(evidence.root))] = expected
                evidence.own(source)
        evidence.own(evidence.root/'DERIVATION-20260930-native-coefficient-event-interpolation.md')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe native event interpolation boundary')

        def save(name, **arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        with localcontext() as context:
            context.prec = 70
            setup = restore_native(evidence, digests, 'MTS-primary', 'fine', deadline)
            loads, action, read = [setup[key] for key in ['loads', 'action', 'read']]
            precision = repair_engine(setup['precision'])
            report = lambda name:read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
            match = lambda status:next(row for row in status['cases'] if row['branch'] == 'MTS-primary' and row['level'] == 'fine')
            live, jets, flow = [match(report(name)) for name in ['annular-live-support-acceleration-attempt01',
                'annular-position-metric-jet-validation-attempt01', 'annular-direct-background-coupled-current-attempt01']]
            directions, correction = read(live['direction_path']), read(live['paths']['projection'])['correction']
            mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
            acceleration = read(flow['paths']['flow'])['acceleration']
            metric_time = ResponseSum(response(read(flow['paths']['background_response'])), response(read(flow['paths']['velocity_response'])))
            owner = report('annular-wave-flux-live-response-fine-attempt01')
            candidate = read(next(row for row in owner['cases'] if row['summary']['branch'] == 'MTS-primary')['paths']['candidate'])
            mixed = response(candidate)
            evaluator = PositionIntegral(action, directions, correction, mode_rate, acceleration,
                candidate['acceleration_change'], precision.position, metric_time, mixed)
            geometry, engine = evaluator.geometry, precision.native
            references = geometry.references[engine.native_edges]
            cuts = action.solver.edges[1:-1]-geometry.anchor
            events = []
            for index, reference in enumerate(references):
                ends = [geometry.geometry(reference, label)[0] for label in [-.5, .5]]
                if ends[1] <= ends[0]:
                    raise RuntimeError('Nonmonotone native map')
                selected = cuts[(cuts > ends[0])&(cuts < ends[1])]
                labels = geometry.inverse(selected, np.full(len(selected), reference))
                events.extend((index, float(label), float(offset)) for label, offset in zip(labels, selected))
            evidence.check('native_events_nonempty', len(events) > 0, len(events))
            event_nodes = np.array([row[0] for row in events], int)
            event_labels = np.array([row[1] for row in events])
            event_offsets = np.array([row[2] for row in events])
            jump_table = {float(offset):np.asarray(metric_beta_jump(precision, float(offset)), float) for offset in np.unique(event_offsets)}
            jumps = np.array([jump_table[offset] for offset in event_offsets])
            root_error = float(np.max(abs(geometry.geometry(references[event_nodes], event_labels)[0]-event_offsets)))
            evidence.check('event_root_residual', root_error <= 2e-15, root_error)
            save('event-locations', nodes=event_nodes, labels=event_labels, offsets=event_offsets, jumps=jumps)
            progress('enumerated-'+str(len(events))+'-events')
            cache = {}

            def covectors(label):
                if label in cache:
                    return cache[label]
                data, unused, movement, unused2, unused3 = precision.packet(label, 'decimal_tangents')
                cardinal = data['cardinal']
                beta, beta_r = native_coefficient_rows(engine, data, cardinal@decimals(directions['field_vertices']),
                    cardinal@decimals(directions['edge_vertices']))
                slope = geometry.geometry(references, label)[1]
                prefactor = np.asarray(movement[engine.native_edges], float)*6*(label+.5)*(.5-label)/slope
                result = np.array([beta, beta_r], float)*prefactor
                cache[label] = result
                return result

            outputs, paths, checks = [], [], []
            for order in [16, 24, 32]:
                nodes = np.cos(np.pi*np.arange(order+1)/order)
                values = np.array([covectors(float(value/2)) for value in nodes])
                coefficients = dct(values, type=1, axis=0)/order
                coefficients[[0, -1]] /= 2
                contributions = np.zeros((4, len(events)))
                for native_index in np.unique(event_nodes):
                    selected = np.flatnonzero(event_nodes == native_index)
                    for component in range(2):
                        interpolated = np.polynomial.chebyshev.chebval(2*event_labels[selected], coefficients[:, component, :, native_index])
                        contributions[:, selected] += interpolated*jumps[selected, component]
                total = np.sum(contributions, axis=1)
                path = save('interpolation-'+str(order), nodes=nodes, coefficients=coefficients, contributions=contributions,
                    total=total, absolute_total=np.sum(abs(contributions), axis=1))
                if outputs:
                    pair = float(np.max(abs(total-outputs[-1])))
                    evidence.check('native_atom_interpolation_pair-'+str(order), pair <= 2e-20, pair)
                    checks.append(pair)
                outputs.append(total)
                paths.append(path)
                progress('interpolation-'+str(order))
            selected = np.unique(np.r_[np.linspace(0, len(events)-1, 16).astype(int),
                np.argsort(np.max(abs(contributions), axis=0))[-8:]])
            errors = []
            for index in selected:
                direct = covectors(float(event_labels[index]))[:, :, event_nodes[index]]
                expected = direct[0]*jumps[index, 0]+direct[1]*jumps[index, 1]
                errors.append(expected-contributions[:, index])
            spot_error = float(np.max(abs(errors)))
            evidence.check('direct_event_spot_checks', spot_error <= 2e-20, spot_error)
            save('direct-event-checks', indices=selected, errors=np.array(errors))
            dust_events = dust_event_atoms(precision, geometry)
            event_path = save('fine-events', native_atoms=outputs[-1], native_absolute_atoms=np.sum(abs(contributions), axis=1),
                native_events=np.array(len(events)), **{'dust_'+key:value for key,value in dust_events.items()})
            gravity = {order:gravity_position_rows(action, precision.position, metric_time, mixed, order) for order in [24, 32]}
            paths = {'events':event_path}
            total, baseline = [], []
            for wave_order, matter_order in [(24, 48), (32, 64)]:
                wave_path = next(row['path'] for row in parent['rule_outputs'] if row['component'] == 'wave' and row['order'] == wave_order)
                matter_path = next(row['path'] for row in parent['rule_outputs'] if row['component'] == 'native-and-dust' and row['order'] == matter_order)
                wave, matter = read(wave_path), read(matter_path)
                paths['wave'+str(wave_order)], paths['matter'+str(matter_order)] = wave_path, matter_path
                full = wave['complete']+matter['native']+outputs[-1]
                full[1:] += matter['dust']+dust_events['atoms']+gravity[wave_order]['column']
                base = wave['base']+matter['native_base']
                base[1:] += matter['dust_base']+gravity[wave_order]['base']
                total.append(full)
                baseline.append(base)
            difference = abs(total[1]-total[0])
            paths['combined'] = save('fine-combined', coarse=total[0], fine=total[1], paired_difference=difference,
                baseline_coarse=baseline[0], baseline_fine=baseline[1], gravity24=gravity[24]['column'], gravity32=gravity[32]['column'])
            summary = dict(branch='MTS-primary', level='fine', C0=total[1].tolist(), paired_difference=difference.tolist(),
                paired_passed=bool(np.max(difference) <= 2e-17), complete_integral_constructed=True,
                native_event_count=len(events), native_event_max=float(np.max(abs(outputs[-1]))),
                interpolation_pairs=checks, direct_spot_error=spot_error, valid_for_claim=False)
            evidence.report['cases'].append(dict(summary=summary, paths=paths))
            evidence.report['seconds'] = perf_counter()-started
            evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
