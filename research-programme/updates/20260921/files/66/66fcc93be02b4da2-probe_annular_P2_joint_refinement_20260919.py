from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_embedding_exact_20260919 import GradedP2System, force_schur_identity, frequency_diagnostic
from annular_live_P2_current_20260918 import LiveP2Tangent
from derive_annular_P2_conforming_force_lift_20260918 import conforming_force_lift
from budget_annular_P2_saved_force_20260918 import checked_json
from scipy.integrate._ivp.rk import DOP853
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def endpoint_mass(lengths):
    lengths = np.asarray(lengths)
    tail = lengths[-1]/8
    for vertex in range(len(lengths)-1, 0, -1):
        tail = (lengths[vertex-1]+lengths[vertex])/8-(lengths[vertex]/24)**2/tail
    return float(lengths[0]/8-(lengths[0]/24)**2/tail) if len(lengths) > 1 else float(lengths[0]/9)


def dop853_imaginary_limit():
    stages = DOP853.n_stages
    matrix, weights = DOP853.A[:stages, :stages], DOP853.B[:stages]
    vector = np.ones(stages)
    polynomial = [1.]
    for unused in range(stages):
        polynomial.append(float(weights @ vector))
        vector = matrix @ vector

    def excess(value):
        return abs(np.polynomial.polynomial.polyval(1j*value, polynomial))-1

    last = .5
    for value in np.linspace(.55, 20., 390):
        if excess(value) > 1e-8:
            return float(brentq(excess, last, value)), polynomial
        last = value
    raise RuntimeError('DOP853 imaginary-axis stability crossing not found.')


def source_mass_law(tangent, schur):
    current = tangent.layer_data(0.)
    layer, values = current.layer, current.coordinates
    source = int(np.searchsorted(layer.edges, layer.anchor))
    boundaries, unused, unused2 = layer.mapping(layer.edges, values[-1])
    element = np.clip(np.searchsorted(layer.edges, layer.reference_radius)-1, 0, len(layer.edges)-2)
    fraction = (layer.reference_radius-layer.edges[element])/np.diff(layer.edges)[element]
    source_basis = np.where(element == source-1, fraction*(2*fraction-1),
        np.where(element == source, (1-fraction)*(1-2*fraction), 0.))
    radius, jacobian, unused = layer.mapping(layer.reference_radius, values[-1])
    weight = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    cross = layer.assemble_quadratic(layer.reference_indices,
        layer.reference_shape*(weight*source_basis)[:, None])
    solved = solve_banded((2, 2), current.data['mass_bands'], cross, check_finite=False)
    weighted_mass = float(weight @ source_basis**2-cross @ solved)
    constant_mass = endpoint_mass(np.diff(boundaries)[:source][::-1])+endpoint_mass(np.diff(boundaries)[source:])
    coefficient = layer.coefficient(0., values[-1])
    kinetic = values[-1]**4/coefficient
    radial = layer.coefficient(0., complex(values[-1], current.step)).imag/current.step
    kinetic_time = (values[-1]**4/current.tangent_layer.coefficient(0., values[-1])).imag/current.step
    forcing = schur['dust_drive']/schur['dust_inertia']+radial/kinetic+current.rates[-1]*kinetic_time/kinetic
    slope = .01
    corner_inertia = slope**2*weighted_mass
    predicted = -corner_inertia*forcing/(1+corner_inertia/schur['dust_inertia'])
    return dict(weighted_source_mass_schur=weighted_mass, frozen_coefficient_graded_mass=float(kinetic*constant_mass),
        frozen_coefficient_relative_error=float(abs(kinetic*constant_mass/weighted_mass-1)),
        source_projection_inertia=corner_inertia, actual_total_projection_inertia=schur['field_projection_inertia'],
        source_lengths=[float(boundaries[source]-boundaries[source-1]), float(boundaries[source+1]-boundaries[source])],
        local_linear_initial_slope=slope, local_corner_forcing=float(forcing),
        leading_source_force_prediction=float(predicted),
        leading_initial_local_model_not_exact_total_force=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-count', type=int, choices=[129, 257], required=True)
    parser.add_argument('--source-cap', type=float, default=4e-5)
    args = parser.parse_args()
    tag = str(args.base_count)+'-cap'+format(args.source_cap, '.0e')
    evidence = EvidenceRun('annular-P2-joint-refinement-'+tag+'-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            full_live_P2_force_convergence_proven=False, full_coupled_stability_theorem=False,
            no_modes_discarded=True, no_force_correction_applied=True, finite_Gram_retained=True,
            same_analytic_initial_preparation=True, source_cap=args.source_cap,
            static_force_gate_not_evolved_gate=True, spectral_cost_estimate_not_guaranteed_runtime=True)
        prerequisite = evidence.output.parent/'annular-P2-graded-source-algebra-attempt04/status.json'
        status = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('nested_action_preflight_passed', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        limit, polynomial = dop853_imaginary_limit()
        evidence.report.update(dop853_imaginary_axis_limit=limit, dop853_stability_polynomial=polynomial)
        evidence.check('RK_stability_crossing_bracket', abs(np.polynomial.polynomial.polyval(.99j*limit, polynomial)) < 1
            and abs(np.polynomial.polynomial.polyval(1.01j*limit, polynomial)) > 1)
        for lengths in [np.array([.3]), np.array([.01, .02, .04, .1]), np.ones(20)*.03]:
            matrix = np.zeros((len(lengths)+1, len(lengths)+1))
            for index, length in enumerate(lengths):
                matrix[index:index+2, index:index+2] += length*np.array([[3., -1.], [-1., 3.]])/24
            expected = matrix[0, 0]-matrix[0, 1:] @ np.linalg.solve(matrix[1:, 1:], matrix[1:, 0])
            evidence.check('graded_mass_recursion_'+str(len(lengths)), abs(endpoint_mass(lengths)-expected) < 2e-15)
        for branch in ['reference', 'MTS']:
            started = perf_counter()
            comparison = checked_json(evidence, 'annular-P2-continuum-comparison-65-attempt01', branch+'-65.json')
            system = GradedP2System(args.base_count, branch == 'MTS', args.source_cap)
            coordinates, momenta, prepared_rates, unused = system.initial()
            tangent = LiveP2Tangent(system, coordinates, momenta)
            current = tangent.layer_data(0.)
            row = conforming_force_lift(tangent)
            schur = force_schur_identity(current)
            mass_law = source_mass_law(tangent, schur)
            spectral = frequency_diagnostic(current.layer, current.coordinates)
            rhs_started = perf_counter()
            flow = system.rhs(0., np.stack([coordinates, momenta]).ravel())
            rhs_seconds = perf_counter()-rhs_started
            canonical = float(system.canonical_residual(coordinates, momenta, tangent.rates, tangent.geometry))
            radial = [float(value) for value in tangent.geometry.off_grid_residual(tangent.rates)]
            initial = evidence.output/(branch+'-initial.npz')
            np.savez_compressed(initial, coordinates=coordinates, momenta=momenta, rates=tangent.rates, labels=system.labels)
            evidence.own(initial, 'outputs')
            scale = 5.401196245463084e-6
            error = row['force']-comparison['times'][0]['continuum_wave_force']
            cost = {}
            for duration in [.001, .004]:
                steps = int(np.ceil(duration*spectral['maximum_angular_frequency']/limit))
                cost[str(duration)] = dict(frozen_stability_steps=steps,
                    optimistic_RHS_seconds=steps*DOP853.n_stages*rhs_seconds,
                    ignores_error_control_rejections_and_full_coupled_spectrum=True)
            row.update(branch=branch, base_count=args.base_count, scalar_nodes=system.count,
                source_bisections=system.model.source_bisections, source_cap=args.source_cap, time=0.,
                force_error_from_continuum=float(error), initial_absolute_gate_pass=abs(error) <= 2e-7,
                initial_combined_gate_pass=abs(error) <= min(2e-7, .005*scale),
                evolved_accuracy_claim=False, canonical_residual=canonical, radial_residual=radial,
                rhs_seconds=rhs_seconds, spectral=spectral, spectral_cost=cost,
                schur=schur, mass_law=mass_law, seconds=perf_counter()-started)
            evidence.report['cases'].append(row)
            evidence.save()
            key = branch+str(args.base_count)
            evidence.check(key+'_canonical_radial_constraints', canonical < 2e-10 and max(radial) < 2e-9)
            evidence.check(key+'_conforming_force_identity', row['identity_error'] < 2e-9, row['identity_error'])
            evidence.check(key+'_Schur_force_identity', schur['force_identity_error'] < 2e-10, schur)
            evidence.check(key+'_positive_kinetic_projection', schur['field_projection_inertia'] > 0 and mass_law['weighted_source_mass_schur'] > 0
                and schur['inertia_subtraction_error'] < 2e-12)
            evidence.check(key+'_positive_frozen_pencil', spectral['minimum_eigenvalue'] > 0 and np.isfinite(spectral['maximum_angular_frequency']))
            evidence.check(key+'_spectral_stiffness_matches_action', spectral['stiffness_action_error'] < 2e-8, spectral)
            evidence.check(key+'_finite_RHS', np.all(np.isfinite(flow)))
            print(json.dumps({name:value for name,value in row.items() if name != 'elements'}), flush=True)
        log = evidence.output/'completion-log.txt'
        with log.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(log, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
