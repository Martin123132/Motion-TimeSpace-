from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_common_weighted_moments_20260920 import decimal_fraction
from decimal import Decimal
from fractions import Fraction
import numpy as np


ZERO = Decimal(0)
HALF = Decimal('0.5')


def decimals(values):
    return np.array([Decimal.from_float(float(value)) for value in np.asarray(values).ravel()], dtype=object).reshape(np.shape(values))


def maximum(values):
    return max(map(abs, np.asarray(values).ravel()), default=ZERO)


class NativeKernel:
    def __init__(self, mesh, support, enabled=True):
        self.mesh, self.enabled = mesh, enabled
        self.references = [decimal_fraction(Fraction(value)) for value in mesh['edges']]
        lookup = {Fraction(value): index for index, value in enumerate(mesh['edges'])}
        self.native_edges = np.array([lookup[Fraction(value)] for value in support], dtype=int)
        self.anchor = lookup[Fraction(mesh['anchor'])]
        self.indices = np.array(mesh['elements'])
        self.count = mesh['count']
        self.template, self.sampling = template_rows(len(support))
        self.maps = {}
        for name, mapping in [('template', self.template), ('sampling', self.sampling)]:
            row, column = mapping.nonzero()
            coo = mapping.tocoo()
            self.maps[name] = (coo.row, coo.col, decimals(coo.data), coo.shape)

    def apply(self, name, values, transpose=False):
        rows, columns, coefficients, shape = self.maps[name]
        if transpose:
            rows, columns, shape = columns, rows, shape[::-1]
        output = np.full(shape[0], ZERO, dtype=object)
        np.add.at(output, rows, coefficients * values[columns])
        return output

    def atoms(self, edges, field, hinge=True, curvature=True):
        widths = np.diff(edges)
        if min(widths) <= 0:
            raise ValueError('Physical cells must remain ordered')
        values = np.zeros(self.indices.shape, dtype=object)
        values.fill(ZERO)
        selected = self.indices >= 0
        values[selected] = field[self.indices[selected]]
        left, middle, right = values.T
        slope_left = (-3 * left + 4 * middle - right) / widths
        slope_right = (left - 4 * middle + 3 * right) / widths
        second = 4 * (left - 2 * middle + right) / widths**2
        first_jump = slope_left[1:] - slope_right[:-1]
        second_jump = second[1:] - second[:-1]
        if hinge:
            first_jump[self.anchor - 1] = ZERO
        if not curvature:
            second_jump.fill(ZERO)
        return dict(widths=widths, slope_left=slope_left, slope_right=slope_right,
                    second=second, first_jump=first_jump, second_jump=second_jump)

    def stencil(self, points):
        width = (points[-1] - points[0]) / 3
        weights = []
        for local in range(4):
            denominator = Decimal(1)
            for other in range(4):
                if other != local:
                    denominator *= points[local] - points[other]
            weights.append(6 * width**3 / denominator)
        return width, weights

    def kernel_values(self, edges, atoms):
        native = edges[self.native_edges]
        values = np.full(len(native) - 3, ZERO, dtype=object)
        if not self.enabled:
            return values
        for index in range(len(values)):
            points = native[index:index + 4]
            width, weights = self.stencil(points)
            total = ZERO
            for edge_index in range(self.native_edges[index] + 1, self.native_edges[index + 3]):
                hinge = [max(point - edges[edge_index], ZERO) for point in points]
                first = sum((weight * value for weight, value in zip(weights, hinge)), ZERO)
                second = sum((weight * value**2 / 2 for weight, value in zip(weights, hinge)), ZERO)
                total += atoms['first_jump'][edge_index - 1] * first + atoms['second_jump'][edge_index - 1] * second
            values[index] = total / width.sqrt()
        return values

    def evaluate(self, edges, field, beta, adjoint=True, hinge=True, curvature=True):
        atoms = self.atoms(edges, field, hinge, curvature)
        kernel = self.kernel_values(edges, atoms)
        image = self.apply('template', kernel)
        weights = self.apply('sampling', beta)
        if min(weights) <= 0:
            raise ValueError('Physical Gram weights must be positive')
        energy = sum(weights * image**2 / 2, ZERO)
        load = self.apply('sampling', image**2 / 2, True)
        result = dict(energy=energy, image=image, kernel=kernel, weights=weights, load=load, atoms=atoms)
        if not adjoint:
            return result
        covector = self.apply('template', weights * image, True)
        edge_gradient = np.full(len(edges), ZERO, dtype=object)
        native_gradient = np.full(len(beta), ZERO, dtype=object)
        first_gradient = np.full(len(edges) - 2, ZERO, dtype=object)
        second_gradient = np.full(len(edges) - 2, ZERO, dtype=object)
        native = edges[self.native_edges]
        if self.enabled:
            for index, multiplier in enumerate(covector):
                points = native[index:index + 4]
                width, coefficients = self.stencil(points)
                scale = multiplier / width.sqrt()
                point_gradient = [ZERO] * 4
                point_moments = [ZERO] * 4
                for edge_index in range(self.native_edges[index] + 1, self.native_edges[index + 3]):
                    location = edges[edge_index]
                    hinge_values = [max(point - location, ZERO) for point in points]
                    first_jump, second_jump = atoms['first_jump'][edge_index - 1], atoms['second_jump'][edge_index - 1]
                    first_response = sum((coefficient * value for coefficient, value in zip(coefficients, hinge_values)), ZERO)
                    second_response = sum((coefficient * value**2 / 2 for coefficient, value in zip(coefficients, hinge_values)), ZERO)
                    first_gradient[edge_index - 1] += scale * first_response
                    second_gradient[edge_index - 1] += scale * second_response
                    for local, (point, value, coefficient) in enumerate(zip(points, hinge_values, coefficients)):
                        point_moments[local] += first_jump * value + second_jump * value**2 / 2
                        if point > location:
                            term = scale * coefficient * (first_jump + second_jump * value)
                            point_gradient[local] += term
                            edge_gradient[edge_index] -= term
                width_gradient = multiplier * Decimal('2.5') * kernel[index] / width
                point_gradient[0] -= width_gradient / 3
                point_gradient[3] += width_gradient / 3
                for local in range(4):
                    weighted = scale * coefficients[local] * point_moments[local]
                    for other in range(4):
                        if local != other:
                            term = weighted / (points[local] - points[other])
                            point_gradient[local] -= term
                            point_gradient[other] += term
                native_gradient[index:index + 4] += np.array(point_gradient, dtype=object)
        if hinge:
            first_gradient[self.anchor - 1] = ZERO
        if not curvature:
            second_gradient.fill(ZERO)
        left_gradient = np.r_[ZERO, first_gradient]
        right_gradient = np.r_[-first_gradient, ZERO]
        curvature_gradient = np.r_[-second_gradient, ZERO] + np.r_[ZERO, second_gradient]
        width_gradient = -(left_gradient * atoms['slope_left'] + right_gradient * atoms['slope_right']
                           + 2 * curvature_gradient * atoms['second']) / atoms['widths']
        edge_gradient[:-1] -= width_gradient
        edge_gradient[1:] += width_gradient
        field_gradient = np.full(self.count, ZERO, dtype=object)
        for local in range(3):
            values = left_gradient * [-3, 4, -1][local] / atoms['widths']
            values += right_gradient * [1, -4, 3][local] / atoms['widths']
            values += curvature_gradient * [4, -8, 4][local] / atoms['widths']**2
            selected = self.indices[:, local] >= 0
            np.add.at(field_gradient, self.indices[selected, local], values[selected])
        interface_gradient = edge_gradient.copy()
        np.add.at(edge_gradient, self.native_edges, native_gradient)
        result.update(edge_gradient=edge_gradient, field_gradient=field_gradient,
            native_gradient=native_gradient, interface_gradient=interface_gradient)
        return result

    def tangent(self, edges, field, edge_rate, field_rate):
        atoms, rates = self.atoms(edges, field), self.atoms(edges, field_rate)
        width_rate = np.diff(edge_rate)
        slope_left_rate = rates['slope_left'] - atoms['slope_left'] * width_rate / atoms['widths']
        slope_right_rate = rates['slope_right'] - atoms['slope_right'] * width_rate / atoms['widths']
        second_rate = rates['second'] - 2 * atoms['second'] * width_rate / atoms['widths']
        first_rate = slope_left_rate[1:] - slope_right_rate[:-1]
        first_rate[self.anchor - 1] = ZERO
        second_rate = second_rate[1:] - second_rate[:-1]
        native, native_rate = edges[self.native_edges], edge_rate[self.native_edges]
        derivative = np.full(len(native) - 3, ZERO, dtype=object)
        if not self.enabled:
            return self.apply('template', derivative)
        for index in range(len(derivative)):
            points, velocities = native[index:index + 4], native_rate[index:index + 4]
            width, coefficients = self.stencil(points)
            delta_width = (velocities[-1] - velocities[0]) / 3
            coefficient_rates = []
            for local in range(4):
                logarithm = 3 * delta_width / width
                for other in range(4):
                    if local != other:
                        logarithm -= (velocities[local] - velocities[other]) / (points[local] - points[other])
                coefficient_rates.append(coefficients[local] * logarithm)
            value, rate = ZERO, ZERO
            for edge_index in range(self.native_edges[index] + 1, self.native_edges[index + 3]):
                hinges = [max(point - edges[edge_index], ZERO) for point in points]
                hinge_rates = [velocities[local] - edge_rate[edge_index] if point > edges[edge_index] else ZERO
                               for local, point in enumerate(points)]
                first = sum((coefficient * hinge for coefficient, hinge in zip(coefficients, hinges)), ZERO)
                second = sum((coefficient * hinge**2 / 2 for coefficient, hinge in zip(coefficients, hinges)), ZERO)
                delta_first = sum((dc * hinge + coefficient * dh for dc, hinge, coefficient, dh
                                   in zip(coefficient_rates, hinges, coefficients, hinge_rates)), ZERO)
                delta_second = sum((dc * hinge**2 / 2 + coefficient * hinge * dh for dc, hinge, coefficient, dh
                                    in zip(coefficient_rates, hinges, coefficients, hinge_rates)), ZERO)
                face = edge_index - 1
                value += atoms['first_jump'][face] * first + atoms['second_jump'][face] * second
                rate += first_rate[face] * first + atoms['first_jump'][face] * delta_first
                rate += second_rate[face] * second + atoms['second_jump'][face] * delta_second
            derivative[index] = (rate - value * delta_width / (2 * width)) / width.sqrt()
        return self.apply('template', derivative)
