from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, IndexedP2Material
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.integrate import simpson
from time import perf_counter
import argparse
import contextlib
import ctypes
import json
import os
import numpy as np


def own_core(core):
    if os.name == 'nt':
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << core):
            raise ctypes.WinError(ctypes.get_last_error())


def trajectory(evidence, branch, count, steps):
    if count == 257:
        folder = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01')
        initial = checked_load(evidence, 'annular-P2-joint-refinement-257-cap2e-05-attempt01', branch+'-initial.npz')
        states = [np.stack([initial['coordinates'], initial['momenta']])]
        for index in range(1, steps+1):
            saved = checked_load(evidence, folder, 'steps'+str(steps)+'-accepted'+str(index).zfill(3)+'.npz')
            states.append(saved['state'])
        times = np.linspace(0., 4e-5, steps+1)
        return folder, times, np.array(states)
    folder = 'annular-P2-bulk513-MTS-time128-attempt01' if steps == 128 else 'annular-P2-bulk513-evolution-'+branch+'-attempt01'
    saved = checked_load(evidence, folder, 'trajectory-steps'+str(steps)+'.npz')
    return folder, saved['times'], saved['states']


def integrated_rows(samples, duration):
    times = np.array([row['time'] for row in samples])
    wave_raw = np.array([row['raw_wave'] for row in samples])
    dust_raw = np.array([row['raw_material'] for row in samples])
    total_raw = np.array([row['raw_total'] for row in samples])
    wave_momentum = np.array([row['wave_momentum'] for row in samples])
    dust_momentum = np.array([row['material_momentum'] for row in samples])
    total_momentum = np.array([row['canonical_source_momentum'] for row in samples])
    result = []
    for fraction in [.25, .5, .75, 1.]:
        end = int(round((len(samples)-1)*fraction))
        for stride in [1, 2, 4]:
            selected = np.arange(0, end+1, stride)
            if (len(selected)-1) % 2 or selected[-1] != end:
                continue
            points = times[selected]
            for power in [0, 1, 2]:
                weight = (points/duration)**power
                derivative = np.zeros_like(points) if power == 0 else power/duration*(points/duration)**(power-1)
                raw_integral = float(simpson(weight*wave_raw[selected], x=points))
                wave_change = wave_momentum[end]-wave_momentum[0]
                dust_change = dust_momentum[end]-dust_momentum[0]
                weighted_momentum = float(simpson(derivative*(wave_momentum[selected]-wave_momentum[0]), x=points))
                impulse = raw_integral-weight[-1]*wave_change+weighted_momentum
                dust_integral = float(simpson(weight*dust_raw[selected], x=points))
                dust_weighted = float(simpson(derivative*(dust_momentum[selected]-dust_momentum[0]), x=points))
                material_impulse = weight[-1]*dust_change-dust_weighted-dust_integral
                total_integral = float(simpson(weight*total_raw[selected], x=points))
                total_weighted = float(simpson(derivative*(total_momentum[selected]-total_momentum[0]), x=points))
                canonical_defect = total_integral-weight[-1]*(total_momentum[end]-total_momentum[0])+total_weighted
                result.append(dict(fraction=fraction, power=power, stride=stride,
                    sample_intervals=len(selected)-1, impulse=impulse, material_impulse=material_impulse,
                    independent_momentum_balance_difference=impulse-material_impulse,
                    canonical_quadrature_balance_defect=canonical_defect,
                    raw_wave_integral=raw_integral, weighted_wave_endpoint_change=float(weight[-1]*wave_change),
                    wave_momentum_weight_integral=weighted_momentum,
                    cancellation_scale=abs(raw_integral)+abs(weight[-1]*wave_change)+abs(weighted_momentum),
                    valid_for_claim=False))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    own_core(0 if args.branch == 'MTS' else 1)
    evidence = EvidenceRun('annular-P2-saved-impulse-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch=args.branch,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            unchanged_instantaneous_force_requirement=True, no_mode_filtering_or_force_replacement=True,
            duration=4e-5, maximum_wall_seconds=6000., core=0 if args.branch == 'MTS' else 1,
            original_full_interval_not_retested=True, finite_weight_family_not_weak_convergence_proof=True,
            empirical_quadrature_difference_not_rigorous_enclosure=True)
        configurations = [(257, 2e-5, 32), (513, 1e-5, 64 if args.branch == 'MTS' else 32),
            (513, 1e-5, 128 if args.branch == 'MTS' else 64)]
        for count, cap, steps in configurations:
            folder, times, states = trajectory(evidence, args.branch, count, steps)
            evidence.check(str(count)+'_'+str(steps)+'_complete_same_interval', len(times) == steps+1
                and times[0] == 0 and times[-1] == evidence.report['duration'] and np.all(np.isfinite(states)))
            system = IndexedGradedP2System(count, args.branch == 'MTS', cap)
            samples = []
            for index, (time, state) in enumerate(zip(times, states)):
                if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                    raise RuntimeError('Safe budget reached; every completed sample is preserved.')
                coordinates, momenta = state
                rates, geometry = system.solve(coordinates, momenta)
                interpolation = IndexedP2Material(system, coordinates).interpolation(np.array([0.]))[0]
                values, speeds = interpolation @ coordinates, interpolation @ rates
                layer = system.layer(0., geometry)
                data = layer.evaluate(0., values, speeds)
                wave_raw = float(layer.source_covector(0., values, speeds, wave=True))
                total_raw = float(layer.source_covector(0., values, speeds))
                lapse, root = layer.metric(0., complex(values[-1], 1e-24))
                dust_raw = float(-layer.source_mass*np.sqrt(lapse**2-speeds[-1]**2/root**2).imag/1e-24)
                projected, unused = row_bounds(layer, values, speeds)
                target = float((interpolation @ momenta)[-1])
                row = dict(time=float(time), source_position=float(values[-1]), source_velocity=float(speeds[-1]),
                    clock=float(data['clock']), wave_momentum=float(data['field_momenta'][-1]),
                    material_momentum=float(data['material_momentum']), canonical_source_momentum=target,
                    reconstructed_source_momentum=float(data['momenta'][-1]),
                    raw_wave=wave_raw, raw_material=dust_raw, raw_total=total_raw,
                    source_covector_split_error=abs(total_raw-wave_raw-dust_raw),
                    source_momentum_inverse_error=abs(float(data['momenta'][-1])-target),
                    explicit_Gram_drive=projected['explicit_drive'])
                path = evidence.output/(str(count)+'-steps'+str(steps)+'-sample'+str(index).zfill(3)+'.json')
                path.write_text(json.dumps(row, indent=2)+'\n', encoding='utf-8')
                evidence.own(path, 'outputs')
                samples.append(row)
                evidence.report.update(active_count=count, active_steps=steps, accepted_samples=len(samples),
                    accepted_time=float(time), seconds=perf_counter()-started)
                evidence.save()
                if index % 8 == 0:
                    print(json.dumps(dict(branch=args.branch, count=count, steps=steps, sample=index,
                        seconds=perf_counter()-started)), flush=True)
            evidence.check(str(count)+'_'+str(steps)+'_pointwise_algebra_and_inverse',
                max(row['source_covector_split_error'] for row in samples) < 2e-12
                and max(row['source_momentum_inverse_error'] for row in samples) < 2e-12)
            integrals = integrated_rows(samples, evidence.report['duration'])
            evidence.check(str(count)+'_'+str(steps)+'_finite_integral_data', all(
                np.isfinite(row['impulse']) and np.isfinite(row['material_impulse']) for row in integrals))
            result = dict(base_count=count, source_cap=cap, steps=steps, samples=samples, integrals=integrals,
                source_path=str((evidence.output.parent/folder/'status.json').relative_to(evidence.root)), valid_for_claim=False)
            path = evidence.output/(str(count)+'-steps'+str(steps)+'-results.json')
            path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
            evidence.own(path, 'outputs')
            evidence.report['cases'].append(result)
            evidence.save()
            endpoint = next(row for row in integrals if row['fraction'] == 1 and row['power'] == 0 and row['stride'] == 1)
            print(json.dumps(dict(branch=args.branch, count=count, steps=steps, result=endpoint,
                seconds=perf_counter()-started)), flush=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', branch=args.branch, checks=len(evidence.report['checks']),
            seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
