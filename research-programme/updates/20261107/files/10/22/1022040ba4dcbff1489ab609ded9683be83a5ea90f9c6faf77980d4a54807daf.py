from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity, reference_offsets
from fractions import Fraction
from time import perf_counter
from decimal import localcontext
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-centered-integrals-diagnostic-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1800
    try:
        parent_path = evidence.output.parent / 'annular-position-reaction-attempt02/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        loads, action, sources = restore_case(evidence, digests, 'reference-reference', 'fine', deadline)
        edges = reference_offsets(action)
        widths = np.asarray([float(right - left) for left, right in zip(action.edges[:-1], action.edges[1:])])
        anchor = float(Fraction(action.mesh['anchor']))
        element_indices = np.asarray(action.mesh['elements'])
        selected_elements = element_indices >= 0
        points, weights = np.polynomial.legendre.leggauss(64)
        labels, weights = points / 2, weights / 2
        weights *= 6 * (labels + .5) * (.5 - labels)
        exact_mass, exact_force = np.zeros_like(loads.rates), np.zeros_like(loads.rates)
        for label, weight in zip(labels, weights):
            cardinal = np.asarray(action.cardinal(label)).ravel()
            source = cardinal @ (action.source - anchor)
            jacobian = np.where((edges[:-1] + edges[1:]) / 2 < 0.,
                1 + (source - action.owner.width * label) / (-edges[0]),
                1 - (source - action.owner.width * label) / edges[-1])
            coefficients = np.einsum('cpl,l->cp', action.gradient, cardinal)
            mass = jacobian[:, None] * widths[:, None] * np.array([1/6, 2/3, 1/6])
            force = -(coefficients[:, 0, None] * np.array([-1., 0., 1.])
                + coefficients[:, 1, None] * np.array([-1/6, -2/3, 5/6])) / jacobian[:, None]
            for array, local in [(exact_mass, mass), (exact_force, force)]:
                vector = np.zeros(loads.rates.shape[1])
                np.add.at(vector, element_indices[selected_elements], local[selected_elements])
                array += weight * np.outer(cardinal, vector)
        archives = []
        for radial_order, label_order in [(24, 28), (32, 36)]:
            points, weights = np.polynomial.legendre.leggauss(radial_order)
            radial_edges = action.solver.edges - anchor
            centers = (radial_edges[:-1] + radial_edges[1:]) / 2
            radii = (centers[:, None] + action.solver.lengths[:, None] * points / 2).ravel()
            radial_weights = (action.solver.lengths[:, None] * weights / 2).ravel()
            mass, force = np.zeros_like(loads.rates), np.zeros_like(loads.rates)
            for start in range(0, len(radii), 16):
                if perf_counter() > deadline:
                    raise RuntimeError('Safe centered integral diagnostic boundary')
                section = slice(start, start + 16)
                density = CenteredLabelDensity(action, radii[section], label_order)
                labels, cardinal = density.offsets, density.interpolation
                radius = radii[section][density.indices]
                source = density.source_offset(labels)
                left = radius < source
                jacobian = np.where(left, 1 + (source - action.owner.width * labels) / (-edges[0]),
                    1 - (source - action.owner.width * labels) / edges[-1])
                reference = (radius - source) / jacobian
                active = (radius >= edges[0] + action.owner.width * labels) & (radius <= edges[-1] + action.owner.width * labels)
                cells = np.clip(np.searchsorted(edges, reference, side='right') - 1, 0, len(edges) - 2)
                local = (reference - edges[cells]) / widths[cells]
                indices = element_indices[cells]
                selected = (indices >= 0) & active[:, None]
                shape = np.column_stack([(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)])
                test_gradient = np.column_stack([4*local-3, 4-8*local, 4*local-1]) / (widths[cells] * jacobian)[:, None]
                coefficients = np.einsum('qpl,ql->qp', action.gradient[cells], cardinal)
                gradient = (coefficients[:, 0] + local * coefficients[:, 1]) / jacobian
                measure = radial_weights[section][density.indices] * density.label_weights
                for array, factors in [(mass, shape), (force, -gradient[:, None] * test_gradient)]:
                    for column in range(3):
                        mask = selected[:, column]
                        np.add.at(array.T, indices[mask, column], (measure[mask] * factors[mask, column])[:, None] * cardinal[mask])
            path = evidence.output / ('integrals-' + str(radial_order) + '-' + str(label_order) + '.npz')
            np.savez_compressed(path, mass=mass, force=force, exact_mass=exact_mass, exact_force=exact_force)
            evidence.own(path, 'outputs')
            summary = dict(radial_order=radial_order, label_order=label_order, mass_error=float(np.max(abs(mass-exact_mass))),
                force_error=float(np.max(abs(force-exact_force))), mass_scale=float(np.max(abs(exact_mass))),
                force_scale=float(np.max(abs(exact_force))), seconds=perf_counter()-started)
            evidence.report['cases'].append(summary)
            evidence.save()
            print(json.dumps(summary), flush=True)
            archives.append((mass,force))
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
