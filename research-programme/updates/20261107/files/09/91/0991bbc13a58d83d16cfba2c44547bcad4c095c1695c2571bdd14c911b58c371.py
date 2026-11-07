from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
from copy import copy
import json
import numpy as np


def main():
    pin(4)
    evidence = EvidenceRun('annular-septic-feedback-validation-attempt01', __file__)
    deadline = perf_counter() + 2400
    try:
        base = 'source-intake/navier-stokes/20260914/'
        feedback = verify_report(evidence, base + 'annular-septic-source-feedback-attempt02/status.json')
        parent = verify_report(evidence, base + 'annular-septic-live-primary-attempt01/status.json')
        saved = read_archive(evidence.root / feedback['initial_path'])
        state = read_archive(evidence.root / parent['states'][0]['path'])
        arrays = read_archive(evidence.root / next(row for row in parent['results'] if row['material'] == 64)['path'])
        acceleration = arrays['acceleration']
        mesh = json.loads((evidence.root / parent['mesh_path']).read_text())
        seal = evidence.output.parent / 'annular-high-order-source-separation-integrity-20261003.json'
        evidence.own(seal)
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, json.loads(seal.read_text())['hashes'], 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            loads = HighLoads(owner, decimals(state['coordinates']), state['rates'], mesh, 'primary', deadline)
            solver, solution = reconstructed_solver(state)
            action = HighAction(loads, mesh, solver, solution)
            directions = decimals(saved['directions'])
            coefficients = loads.basis.polynomial(np.array(mesh['elements']), directions.T)
            widths = np.array([Decimal((Fraction(upper) - Fraction(lower)).numerator) / Decimal((Fraction(upper) - Fraction(lower)).denominator)
                for lower, upper in zip(mesh['edges'][:-1], mesh['edges'][1:])], dtype=object)
            gradient = np.asarray(coefficients[:, 1:] * np.arange(1, 8)[None, :, None] / widths[:, None, None], float)
        parameter_direction = np.sin(np.arange(15) + .37)
        step = 1e-20
        changed = copy(action)
        changed.gradient = action.gradient.astype(complex) + 1j * step * gradient * parameter_direction
        response = np.zeros_like(acceleration, dtype=complex)
        points, weights = np.polynomial.legendre.leggauss(64)
        points, weights = points / 2, weights / 2
        weights *= 6 * (points + .5) * (.5 - points)
        for label, weight in zip(points, weights):
            row = changed.samples(label, 16)
            quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
            source_acceleration = cardinal @ acceleration[:, -1]
            nodal = cardinal @ acceleration[:, :-1]
            field_acceleration = np.sum(quad['shape'] * nodal[quad['indices']], axis=1)
            temporal_acceleration = field_acceleration + source_acceleration * row['motion']
            field = np.zeros(len(action.knots), dtype=complex)
            flux = -quad['measure'] * geometry['gradient'] * row['gradient']
            inertia = -quad['measure'] * geometry['kinetic'] * temporal_acceleration
            np.add.at(field, quad['indices'].ravel(), (flux[:, None] * quad['radial'] + inertia[:, None] * quad['shape']).ravel())
            source = -quad['measure'] @ (geometry['gradient_source'] * row['gradient']**2 / 2 + geometry['kinetic'] * row['motion'] * temporal_acceleration)
            response += weight * np.outer(cardinal, np.r_[field, source])
        direct = response.imag / step
        expected = np.einsum('ijk,k->ij', saved['tangent_rhs'], parameter_direction, optimize=False)
        relative = float(np.max(abs(direct - expected)) / np.max(abs(expected)))
        evidence.check('independent_complex_step_force_minus_Ha', relative < 2e-10, relative)
        source_relative = float(np.max(abs(direct[:, -1] - expected[:, -1])) / np.max(abs(expected[:, -1])))
        evidence.check('independent_source_cross_and_inertia_factors', source_relative < 2e-10, source_relative)
        residual = saved['response_matrix'] @ saved['correction'] + saved['target']
        evidence.check('linear_source_solve_replay', np.array_equal(residual, saved['residual']))
        evidence.report.update(force_Hessian_tangent_error=relative, source_tangent_error=source_relative,
            metric_feedback_frozen=True, fresh_geometry_verification_separate=True, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
