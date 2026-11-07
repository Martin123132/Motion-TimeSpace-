from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction
from annular_high_order_coupled_v2_20261003 import transport_shapes
from annular_source_flat_native_20261002 import movements
from annular_candidate_hamiltonian_20260921 import decimals
from annular_candidate_energy_current_20260921 import reconstructed_solver
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal, localcontext
from time import perf_counter
import ctypes
import json
import numpy as np


def hinge_transport(engine, atom, movement):
    endpoints = np.r_[atom['slope_left'][:1], (atom['slope_right'][:-1] + atom['slope_left'][1:]) / 2, atom['slope_right'][-1:]]
    rates = []
    for cell, weights, source_slope in [
            (engine.anchor - 1, engine.basis.right_first, atom['slope_right'][engine.anchor - 1]),
            (engine.anchor, engine.basis.left_first, atom['slope_left'][engine.anchor])]:
        field_rate = []
        for index, node in enumerate(engine.indices[cell]):
            local = Decimal(index) / engine.basis.degree
            slope = Decimal(0)
            for power in reversed(range(1, engine.basis.degree + 1)):
                slope = slope * local + power * atom['polynomial'][cell, power]
            slope /= atom['widths'][cell]
            if index == 0:
                slope = endpoints[cell]
            if index == engine.basis.degree:
                slope = endpoints[cell + 1]
            shift = (1 - local) * movement[cell] + local * movement[cell + 1]
            field_rate.append(slope * shift if node >= 0 else np.full(movement.shape[1], Decimal(0), dtype=object))
        changed = weights @ np.array(field_rate) / atom['widths'][cell]
        changed -= source_slope * (movement[cell + 1] - movement[cell]) / atom['widths'][cell]
        rates.append(changed)
    return rates[1] - rates[0]


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-high-order-source-hinge-separation-attempt01', __file__)
    deadline = perf_counter() + 3600
    try:
        base = 'source-intake/navier-stokes/20260914/'
        jet = verify_report(evidence, base + 'annular-high-order-time-jet-attempt01/status.json')
        live = verify_report(evidence, base + 'annular-high-order-live-primary-attempt02/status.json')
        mesh = json.loads((evidence.root / live['mesh_path']).read_text())
        seal = evidence.output.parent / 'annular-high-order-live-repair-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        results = []
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            for number, probe in enumerate(jet['probes']):
                state = read_archive(evidence.root / probe['path'])
                loads = HighLoads(owner, decimals(state['coordinates']), state['rates'], mesh, 'primary', deadline)
                solver, solution = reconstructed_solver(state)
                action = HighAction(loads, mesh, solver, solution)
                engine = loads.native_engine
                full, ordinary, hinge, point, covectors, jump_changes = [], [], [], [], [], []
                for label in jet['labels']:
                    data = physical_data(engine, loads, action, label)
                    result = engine.evaluate(data['edges'], data['field'], data['beta'], data['beta_radial'])
                    movement = movements(engine, data['edges'], data['source'])
                    atom = result['atoms']
                    nodal_mean = np.r_[atom['slope_left'][:1], (atom['slope_right'][:-1] + atom['slope_left'][1:]) / 2, atom['slope_right'][-1:]]
                    local_point = result['native_field'] * nodal_mean[engine.native_edges] + result['native_shape']
                    jump_change = hinge_transport(engine, atom, movement)
                    channel = result['jump_covector'] * jump_change
                    represented = transport_shapes(engine, result, movement)
                    projected = np.asarray(local_point @ movement[engine.native_edges], float)
                    channel_float = np.asarray(channel, float)
                    scale = max(np.max(abs(represented)), np.max(abs(projected)), np.max(abs(channel_float)), 1e-50)
                    error = float(np.max(abs(represented - projected - channel_float)) / scale)
                    evidence.check('jet' + str(number) + ':' + str(label) + ':exact_source_hinge_chain_rule', error < 2e-12, error)
                    full.append(represented)
                    ordinary.append(projected)
                    hinge.append(channel_float)
                    point.append(np.asarray(local_point[1:-1], float))
                    covectors.append(float(result['jump_covector']))
                    jump_changes.append(np.asarray(jump_change, float))
                arrays = dict(full=np.array(full), ordinary=np.array(ordinary), hinge=np.array(hinge),
                    ordinary_point=np.array(point), source_covector=np.array(covectors),
                    transported_jump=np.array(jump_changes), amount=np.array(probe['amount']))
                results.append(arrays)
                path = evidence.output / ('jet' + str(number) + '-separated.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
        witnesses = {}
        for name in ['full', 'ordinary', 'hinge', 'ordinary_point']:
            estimates = [(row[name] - results[0][name]) / float(row['amount']) for row in results[1:]]
            coarse = (4 * estimates[1] - estimates[0]) / 3
            fine = (4 * estimates[2] - estimates[1]) / 3
            index = np.unravel_index(np.argmax(abs(fine)), fine.shape)
            witnesses[name] = dict(maximum=float(np.max(abs(fine))), label=jet['labels'][index[0]],
                column=int(index[1]), signed=float(fine[index]),
                Richardson_difference=float(np.max(abs(fine - coarse))))
        evidence.report.update(witnesses=witnesses, decomposition='full_shape = ordinary_native_work + U_J * delta_J',
            source_hinge_omitted=False, full_shape_derivative_unchanged=True,
            ordinary_formula_must_use_partial_covectors=True, trajectory_computed=False,
            github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

