from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_seed_resampling_v2_20260922 import seed_arrays
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, live_refined
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_cut_initial_data_20260915 import compatible_initial_state
from annular_joint_first_tangent_20260922 import ZeroTangent, shifted_coordinates, ProbeMetricRate, RadialResponse, MomentumMetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_moving_Legendre_current_20260921 import full_system
from annular_radial_Ward_moments_20260921 import KernelPrimitive, averaged_moments
from annular_candidate_hamiltonian_20260921 import decimals
from scipy.sparse import save_npz
from time import perf_counter
import argparse
import contextlib
import gc
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds', type=float, default=8500)
    parser.add_argument('--label', default='annular-matched-seed-flow-attempt01')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.max_seconds
    try:
        intake = evidence.output.parent
        digests = {}
        for folder in ['annular-interface-acceleration-flux-validation-attempt01', 'annular-seed-resampling-attempt02']:
            path = intake/folder/'status.json'
            authority = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(folder+':complete', authority['state']=='complete')
            digests.update(authority['inputs'])
            digests.update(authority['outputs'])
        evidence.own(evidence.root/'DERIVATION-20260922-matched-seed-initialization.md')
        evidence.report.update(scientific_checks=[], iterations=[], physical_time=0., pressure_adjusted=False,
            new_fitted_parameters=False, old_canonical_momenta_preserved=False, velocity_seeded_initialization=True,
            full_outer_radial_residual_recomputed=False, github_action=False, subagents_used=False, maximum_seconds=args.max_seconds)

        def owned(path):
            relative = str(path.relative_to(evidence.root))
            evidence.check(relative+':hash', relative in digests and hashlib.sha256(path.read_bytes()).hexdigest()==digests[relative])
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as packed:
                return {key:packed[key].copy() for key in packed.files}

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Saved time-budget boundary; completed case files retained')

        def save(label, **arrays):
            path = evidence.output/(label+'.npz')
            if path.exists():
                raise FileExistsError(str(path))
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            evidence.save()
            return str(path.relative_to(evidence.root))

        def science(case, quantity, error, tolerance):
            evidence.report['scientific_checks'].append(dict(case=case, quantity=quantity, error=float(error), tolerance=float(tolerance),
                passed=bool(np.isfinite(error) and error<=tolerance)))
            evidence.save()

        steps = np.array([7.8125e-7, 3.90625e-7, 1.953125e-7])
        for name in ['reference-reference', 'MTS-primary', 'MTS-alternative']:
            branch, extension = name.split('-')
            native = IndexedGradedP2System(257, branch=='MTS', 2e-5)
            original = owned(intake/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(intake/'annular-nested-refinement-preparation-attempt02'/(name+'-refined-action.json'))
            base, unused, unused2 = common_material(native, original, overlay)
            owner = adapt_owner(base, packet['mesh'])
            field, rate, unused = compatible_initial_state(native.model, 0.)
            unused, unused2, displacement = native.model.mapping(native.model.radii, native.model.anchor)
            rate[:-1] *= 1-displacement
            evidence.check(name+':original_field_recipe', np.max(abs(original['coordinates'][:, :-1]-field[:-1]))<=1e-16)
            evidence.check(name+':original_velocity_recipe', np.max(abs(original['fixed_rates']-rate))<=4e-13)
            evidence.check(name+':original_source_positions', np.max(abs(original['coordinates'][:, -1]-(field[-1]+native.width*native.labels)))<=1e-14)
            for route in ['inherited', 'resampled']:
                case = name+'-'+route
                progress(case+'-start')
                initial_path = intake/'annular-seed-resampling-attempt02'/(name+'-refined-'+route+'.npz')
                initial = owned(initial_path)
                coordinates, rates = decimals(initial['coordinates']), initial['rates']
                evidence.check(case+':initial_source_exact', np.array_equal(np.asarray(coordinates[:, -1], float), original['coordinates'][:, -1])
                    and np.array_equal(rates[:, -1], original['fixed_rates'][:, -1]))
                loads, action = live_refined(owner, coordinates, rates, packet['mesh'], packet, extension, deadline)
                evidence.check(case+':nonlinear_constraint', action.solution['maximum_residual']<=2e-12, action.solution['maximum_residual'])
                state_path = save(case+'-state', coordinates=np.array(coordinates, dtype=str), rates=rates, edges=action.solver.edges,
                    **{key:action.solution[key] for key in ['state','rhs_coefficients','primitives','left']})
                progress(case+'-metric-saved')
                system = full_system(action, ZeroTangent(), deadline, lambda stage:progress(case+'-'+stage))
                matrix_path = evidence.output/(case+'-Hessian.npz')
                save_npz(matrix_path, system['matrix'])
                evidence.own(matrix_path, 'outputs')
                momentum = MomentumMetricResponse(action, deadline, lambda stage:progress(case+'-'+stage))
                evidence.check(case+':independent_momentum', np.max(abs(momentum.base_momentum()-system['momentum']))<=2e-15)
                energies = []
                for material_order in [48,64]:
                    values = action.momentum_and_force(12, material_order, deadline)
                    energies.append(float(np.sum(values['momentum']*rates)-values['matter_action']))
                science(case, 'matter_energy_quadrature', abs(energies[1]-energies[0]), 2e-11)
                probes = {}
                probe_paths = []
                for index, step in enumerate(steps):
                    for sign in [-1,1]:
                        label = case+'-inner'+str(index)+'-sign'+str(sign)
                        progress(label)
                        shifted = shifted_coordinates(coordinates, rates, sign*step)
                        local_loads, local_action = live_refined(owner, shifted, rates, packet['mesh'], packet, extension, deadline)
                        evidence.check(label+':constraint', local_action.solution['maximum_residual']<=2e-12)
                        path = save(label, coordinates=np.array(shifted, dtype=str), rates=rates, edges=local_action.solver.edges,
                            **{key:local_action.solution[key] for key in ['state','rhs_coefficients','primitives','left']})
                        probe_paths.append(path)
                        probes[index,sign] = local_action
                coordinate = ProbeMetricRate(probes, steps)
                coordinate_momentum = np.array([momentum.accumulate(lambda radius:coordinate.values(radius)[estimate]) for estimate in range(2)])
                coordinate.cache.clear()
                response = RadialResponse(loads, action, extension, deadline, lambda stage:progress(case+'-'+stage))
                evidence.check(case+':radial_response_constraint', response.base_constraint_residual<=2e-12)
                accelerations, responses, couplings = [], [], []
                for estimate in range(2):
                    def record(row, acceleration, coupling, residual, metric):
                        path = save(case+'-estimate'+str(estimate)+'-iteration'+str(row['iteration']), acceleration=acceleration,
                            coupling=coupling, residual=residual, forcing=metric.forcing,
                            **{'metric_'+key:value for key,value in metric.solution.items()})
                        evidence.report['iterations'].append(dict(row, case=case, estimate=estimate, output=path))
                    rhs = system['force']-system['convection'][-1]-coordinate_momentum[estimate]
                    acceleration, metric, coupling, unused, history = solve_joint_rhs(system, response, momentum, rhs, record)
                    accelerations.append(acceleration)
                    responses.append(metric)
                    couplings.append(coupling)
                accelerations = np.array(accelerations)
                science(case, 'paired_acceleration', np.max(abs(accelerations[1]-accelerations[0])), 2e-8)
                tangent = JointMetricTangent(coordinate, responses)
                radius = np.linspace(action.solver.edges[0], action.solver.edges[-1], 257)
                flow_path = save(case+'-flow', accelerations=accelerations, force=system['force'], momentum=system['momentum'],
                    coordinate_convection=system['convection'][-1], coordinate_momentum=coordinate_momentum, coupling=np.array(couplings),
                    radius=radius, metric_values=action.solver.values(action.solution,radius)[0], metric_rate=tangent.values(radius),
                    inner_steps=steps, matter_energies=np.array(energies), dust_block=system['dust_block'])
                moments, moment_paths = [], []
                for spatial, material, kernel_order in [(8,48,16),(12,64,24)]:
                    progress(case+'-moments'+str(spatial))
                    kernel = KernelPrimitive(action, kernel_order)
                    raw = averaged_moments(action, loads, tangent, kernel, accelerations[-1], spatial, material, deadline)
                    moment_paths.append(save(case+'-moments'+str(spatial), **raw))
                    moments.append(raw)
                    for sector in ['wave','dust']:
                        science(case+'-moments'+str(spatial), sector+'_radial_identity', np.max(abs(raw['label_'+sector+'_identity_error'])), 2e-11)
                    coordinate.cache.clear()
                science(case, 'paired_current_quadrature', np.max(abs(moments[1]['sum_horizontal']-moments[0]['sum_horizontal'])), 2e-10)
                summary = dict(case=case, branch=name, route=route, initial=str(initial_path.relative_to(evidence.root)),
                    state_path=state_path, flow_path=flow_path, matrix_path=str(matrix_path.relative_to(evidence.root)),
                    probe_paths=probe_paths, moment_paths=moment_paths, maximum_acceleration=float(np.max(abs(accelerations[-1]))),
                    maximum_field_acceleration=float(np.max(abs(accelerations[-1,:,:-1]))), source_acceleration=accelerations[-1,:,-1].tolist(),
                    matter_energy=energies[-1], outer_mass=float(action.solution['state'][0,-1,-1]),
                    radial_residual=action.solution['maximum_residual'], horizontal_current=moments[1]['sum_horizontal'].tolist(),
                    physical_time=0., complete=True)
                evidence.report['cases'].append(summary)
                progress(case+'-complete')
                del action, loads, local_action, local_loads, probes, coordinate, response, momentum, system, tangent, responses, moments
                gc.collect()
        evidence.report.update(seconds=perf_counter()-started, science_passed=sum(row['passed'] for row in evidence.report['scientific_checks']),
            science_total=len(evidence.report['scientific_checks']), new_nonlinear_solves=42)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', seconds=evidence.report['seconds'], science_passed=evidence.report['science_passed'],
            science_total=evidence.report['science_total'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
