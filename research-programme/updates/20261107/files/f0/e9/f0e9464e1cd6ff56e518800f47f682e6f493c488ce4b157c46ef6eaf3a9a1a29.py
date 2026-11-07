from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import adapt_owner
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_quadratic_core_20261002 import live_core, core_forms
from annular_source_flat_native_20261002 import movements
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import ctypes
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', choices=['third', 'fourth'], required=True)
    parser.add_argument('--cpu', type=int, default=2)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-live-transmission-time-jet-' + args.level + '-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        evidence.own(evidence.root / 'DERIVATION-20261002-live-transmission-time-jet.md')
        base = 'source-intake/navier-stokes/20260914/'
        authority = 'annular-live-native-transmission-third-attempt02' if args.level == 'third' else 'annular-live-native-transmission-fourth-primary-attempt03'
        parent = verify_report(evidence, base + authority + '/status.json')
        evidence.check('complete_parent', parent['state'] == 'complete')
        packet = json.loads((evidence.root / parent['packet_path']).read_text())
        state_path = next(row['path'] for row in parent['states'] if row['name'] == 'iteration0') if args.level == 'third' else parent['state_path']
        state = read_archive(evidence.root / state_path)
        high = next(row for row in parent['results'] if row['name'] == 'primary-16-64')
        acceleration = read_archive(evidence.root / high['path'])['acceleration']
        evidence.check('action_derived_acceleration', high['Euler_relative'] < 2e-11 and acceleration.shape == state['rates'].shape)
        seal_path = evidence.output.parent / 'annular-quadratic-transmission-integrity-20261002.json'
        evidence.own(seal_path)
        digests = json.loads(seal_path.read_text())['hashes']
        with localcontext() as context:
            context.prec = 64
            unused, old_action, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(old_action.owner, packet['mesh'])
            coordinates = decimals(state['coordinates'])
            acceleration_exact = decimal_array(acceleration)
            engine = NativeKernel(packet['mesh'], packet['gram_support'], True)
        labels = np.unique(np.r_[-.5, np.polynomial.legendre.leggauss(9)[0] / 2, .5])
        amounts = [2e-8, 5e-9, 1.25e-9]
        evidence.report.update(level=args.level, probes=[], labels=labels.tolist(), amounts=amounts,
            actual_acceleration_source=high['path'], fixed_profile=True, trajectory_computed=False,
            includes_velocity_squared_radial_response=True, uniform_material_claim=False, github_action=False, subagents_used=False)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe time-jet boundary')
        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))
        baseline = None
        for number, amount in enumerate([0.] + amounts):
            progress('radial jet ' + str(number))
            with localcontext() as context:
                context.prec = 64
                changed = coordinates + Decimal.from_float(amount) * acceleration_exact
            rates = np.sqrt(2 * amount) * acceleration
            loads, action = live_core(owner, changed, rates, packet['mesh'], packet, 'primary', deadline)
            residual = float(np.max(abs(action.solver.residual(action.solution['state'], 'primary'))))
            evidence.check('jet' + str(number) + ':radial_equations', residual < 8e-14, residual)
            forms, direct, metric, cancellation_scales = [], [], [], []
            with localcontext() as context:
                context.prec = 64
                for label in labels:
                    data = physical_data(engine, loads, action, label)
                    cardinal = decimal_array(data['cardinal'])
                    columns = np.column_stack([coordinates[:, :-1].T @ cardinal, acceleration_exact[:, :-1].T @ cardinal])
                    movement = movements(engine, data['edges'], data['source'])
                    assembled = core_forms(engine, data, columns, movement)
                    current, image, tangent = assembled[0], assembled[2], assembled[3]
                    image_now = np.asarray(image[:, 0] + Decimal.from_float(amount) * image[:, 1], float)
                    tangent_now = np.asarray(tangent[:, :, 0] + Decimal.from_float(amount) * tangent[:, :, 1], float)
                    coefficient = np.asarray(engine.apply('sampling', data['beta']), float)
                    changed_beta = engine.sampling @ np.asarray(data['beta_radial'][:, None] * movement[engine.native_edges], float)
                    cancellation_scales.append(np.sum(abs((image_now * coefficient)[:, None] * tangent_now), axis=0)
                        + np.sum(abs(image_now[:, None]**2 * changed_beta), axis=0) / 2)
                    scalar = core_forms(engine, data, data['field'][:, None], movement)[0][:, 0, 0]
                    forms.append(current)
                    direct.append(scalar)
                    metric.append(np.r_[np.asarray(data['beta'], float), np.asarray(data['beta_radial'], float)])
            forms, direct, metric = np.array(forms), np.array(direct), np.array(metric)
            represented = forms[:, :, 0, 0] + 2 * amount * forms[:, :, 0, 1] + amount**2 * forms[:, :, 1, 1]
            scale = float(np.max(cancellation_scales))
            replay_error = float(np.max(abs(direct - represented)) / max(scale, 1e-30))
            evidence.check('jet' + str(number) + ':quadratic_full_form_replay', replay_error < 1e-10, replay_error)
            if amount == 0:
                baseline = forms.copy()
                path = save('baseline', forms=forms, labels=labels, metric=metric, direct=direct)
                evidence.report.update(baseline_path=path, baseline_shape_max=float(np.max(abs(forms[:, :, 0, 0]))),
                    exact_field_contribution_max=float(np.max(abs(2 * forms[:, :, 0, 1]))))
            else:
                geometry = (forms[:, :, 0, 0] - baseline[:, :, 0, 0]) / amount
                corrected = 2 * forms[:, :, 0, 1] + geometry
                raw = (direct - baseline[:, :, 0, 0]) / amount
                path = save('jet' + str(number), forms=forms, labels=labels, direct=direct, metric=metric,
                    geometry=geometry, corrected=corrected, raw=raw, amount=np.array(amount),
                    field_at_zero=2 * baseline[:, :, 0, 1], quadratic_term=amount * forms[:, :, 1, 1])
                evidence.report['probes'].append(dict(amount=amount, path=path, corrected_max=float(np.max(abs(corrected))),
                    geometry_max=float(np.max(abs(geometry))), raw_max=float(np.max(abs(raw))), radial_residual=residual,
                    valid_for_claim=False))
            evidence.save()
        evidence.report.update(seconds=perf_counter() - started, propagation_pass_claimed=False,
            result='Computed second-jet estimates; cross-step and cross-grid analysis required.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
