from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from analyze_annular_source_flat_state_20261002 import read_archive
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_product_basis_20261003 import product_basis_values
from construct_annular_septic_response_20261003 import pin
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import argparse
import json
import numpy as np


def exact_number(value):
    fraction = Fraction(value)
    return Decimal(fraction.numerator) / Decimal(fraction.denominator)


def exact_flat_force(polynomial, rational_basis):
    degree = len(polynomial) - 1
    answer = []
    for column in range(degree + 1):
        total = Decimal(0)
        for first in range(1, degree + 1):
            for second in range(1, degree + 1):
                total -= polynomial[first] * first * exact_number(rational_basis[second, column]) * second / Decimal(first + second - 1)
        answer.append(total)
    return np.asarray(answer, float)


def layer_forces(loads, action, label, order, polynomial, curvature):
    sample = action.samples(label, order)
    quad, geometry, cardinal = sample['quadrature'], sample['geometry'], sample['cardinal']
    count = loads.native_engine.count
    width = np.array([float(upper - lower) for lower, upper in zip(action.edges[:-1], action.edges[1:])])[quad['cells']]
    shape = product_basis_values(quad['local'], action.basis.degree)
    radial = product_basis_values(quad['local'], action.basis.degree, 1) / width[:, None]
    selected = loads.native_engine.indices[quad['cells']] >= 0
    shape *= selected
    radial *= selected
    weak_old, weak_product, bulk = [np.zeros(count) for unused in range(3)]
    density = -quad['measure'] * geometry['gradient'] * sample['gradient']
    np.add.at(weak_old, quad['indices'].ravel(), (density[:, None] * quad['radial']).ravel())
    np.add.at(weak_product, quad['indices'].ravel(), (density[:, None] * radial).ravel())
    coefficients = np.einsum('cpl,l->cp', curvature, cardinal, optimize=False)[quad['cells']]
    second = np.polynomial.polynomial.polyval(quad['local'], coefficients.T, tensor=False)
    logarithmic = 2 / geometry['radius'] + geometry['lapse_log_radial'] + geometry['metric_radial'] / (2 * geometry['metric'])
    integrand = geometry['gradient'] * (second + geometry['jacobian'] * logarithmic * sample['gradient'])
    np.add.at(bulk, quad['indices'].ravel(), (quad['measure'][:, None] * integrand[:, None] * shape).ravel())
    with localcontext() as context:
        context.prec = 75
        data = physical_data(loads.native_engine, loads, action, label)
        result = loads.native_engine.evaluate(data['edges'], data['field'], data['beta'], data['beta_radial'])
        radius = np.asarray(data['edges'], float)
        values = action.solver.values(action.solution, radius)[0]
        beta = decimal_array(radius**2 * np.exp(values[1]) * np.sqrt(1 - 2 * values[0] / radius))
        atom = result['atoms']
        edge_load = np.r_[beta[0] * atom['slope_left'][0], beta[1:-1] * (atom['slope_left'][1:] - atom['slope_right'][:-1]), -beta[-1] * atom['slope_right'][-1]]
        edge_indices = np.r_[loads.native_engine.indices[:, 0], loads.native_engine.indices[-1, -1]]
        traction = np.full(count, Decimal(0), dtype=object)
        np.add.at(traction, edge_indices[edge_indices >= 0], edge_load[edge_indices >= 0])
        native = np.asarray(result['field_gradient'], float)
        balanced = bulk + np.asarray(traction - result['field_gradient'], float)
        layer_polynomial = polynomial @ decimal_array(cardinal)
        cells = sorted(set([572, int(np.argmax(np.max(abs(np.asarray(layer_polynomial[:, 1:], float)), axis=1)))]))
        flat_rows = []
        points, weights = np.polynomial.legendre.leggauss(order)
        points, weights = (points + 1) / 2, weights / 2
        for cell in cells:
            derivative = np.asarray(layer_polynomial[cell, 1:] * np.arange(1, action.basis.degree + 1), float)
            gradient = np.polynomial.polynomial.polyval(points, derivative)
            old_flat = -(weights * gradient) @ action.basis.values(points, 1)
            product_flat = -(weights * gradient) @ product_basis_values(points, action.basis.degree, 1)
            exact_flat = exact_flat_force(layer_polynomial[cell], action.basis.rational)
            scale = float(np.max(abs(exact_flat)))
            flat_rows.append(dict(cell=cell, scale=scale, old_absolute=float(np.max(abs(old_flat - exact_flat))),
                product_absolute=float(np.max(abs(product_flat - exact_flat))),
                old_relative=float(np.max(abs(old_flat - exact_flat))) / scale,
                product_relative=float(np.max(abs(product_flat - exact_flat))) / scale))
    return dict(old=weak_old-native, product=weak_product-native, balanced=balanced, flat_rows=flat_rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['primary', 'reference'], required=True)
    parser.add_argument('--cpu', type=int, required=True)
    args = parser.parse_args()
    pin(args.cpu)
    evidence = EvidenceRun('annular-force-basis-diagnostic-' + args.branch + '-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 2700
    try:
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base + 'annular-all-native-jump-live-' + args.branch + '-attempt01/status.json')
        mesh = json.loads((evidence.root / parent['mesh_path']).read_text())
        saved = read_archive(evidence.root / parent['states'][0]['path'])
        seal = evidence.output.parent / 'annular-septic-coupled-response-integrity-20261003.json'
        evidence.own(seal)
        evidence.report.update(branch=args.branch, results=[], diagnostic_only=True, physical_state_unchanged=True,
            field_force_only=True, full_coupled_adoption=False, valid_for_claim=False)
        with localcontext() as context:
            context.prec = 75
            unused, original, sources = restore_case(evidence, json.loads(seal.read_text())['hashes'], 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            loads = HighLoads(owner, decimals(saved['coordinates']), saved['rates'], mesh, args.branch, deadline)
            solver, solution = reconstructed_solver(saved)
            action = HighAction(loads, mesh, solver, solution)
            polynomial = loads.native_engine.basis.polynomial(loads.native_engine.indices, loads.coordinates[:, :-1].T)
            widths = np.array([exact_number(upper-lower) for lower, upper in zip(action.edges[:-1], action.edges[1:])])
            powers = np.arange(2, action.basis.degree+1)
            curvature = np.asarray(polynomial[:, 2:] * (powers*(powers-1))[None, :, None] / widths[:, None, None]**2, float)
        basis_points = np.r_[0., 1., np.polynomial.legendre.leggauss(32)[0]/2+.5]
        basis_values = product_basis_values(basis_points, 7)
        derivatives = product_basis_values(basis_points, 7, 1)
        evidence.check('product_partition_of_unity', float(np.max(abs(basis_values.sum(axis=1)-1))) < 5e-14)
        evidence.check('product_derivative_partition', float(np.max(abs(derivatives.sum(axis=1)))) < 2e-13)
        evidence.check('product_nodal_values', float(np.max(abs(product_basis_values(np.arange(8)/7, 7)-np.eye(8)))) < 5e-14)
        for label in [-.5, 0., .5]:
            for order in [12, 16, 24]:
                if perf_counter() > deadline:
                    raise RuntimeError('Diagnostic safe wall boundary')
                result = layer_forces(loads, action, label, order, polynomial, curvature)
                scale = max(float(np.max(abs(result['old']))), float(np.max(abs(result['balanced']))))
                row = dict(label=label, order=order, force_scale=scale, flat_rows=result['flat_rows'])
                for first, second in [('old', 'balanced'), ('product', 'balanced'), ('old', 'product')]:
                    difference = abs(result[first]-result[second])
                    row[first+'_'+second] = dict(absolute=float(np.max(difference)), relative=float(np.max(difference))/scale,
                        node=int(np.argmax(difference)))
                row['original_equivalence_gate_passed'] = row['product_balanced']['relative'] < 2e-10
                path = evidence.output / ('layer-'+str(label)+'-order-'+str(order)+'.npz')
                np.savez_compressed(path, **{key:result[key] for key in ['old', 'product', 'balanced']})
                evidence.own(path, 'outputs')
                row['path'] = str(path.relative_to(evidence.root))
                evidence.report['results'].append(row)
                evidence.save()
                print(json.dumps(row), flush=True)
        evidence.report['seconds'] = perf_counter()-started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
