from common import require, guard, ALGEBRA
from math import comb
import heapq
import numpy as np
from scipy.interpolate import CubicSpline


def scaled_power(grid, values):
    coefficients = np.moveaxis(CubicSpline(grid, values, axis=0).c[::-1], 0, -1)
    widths = np.diff(grid).reshape((-1,) + (1,) * (coefficients.ndim - 1))
    return coefficients * widths ** np.arange(4)


def bernstein(power):
    degree = power.shape[-1] - 1
    result = np.zeros_like(power)
    for target in range(degree + 1):
        for origin in range(target + 1):
            result[..., target] += power[..., origin] * comb(target, origin) / comb(degree, origin)
    return result


def multiply(left, right):
    degree = left.shape[-1] + right.shape[-1] - 2
    shape = np.broadcast_shapes(left.shape[:-1], right.shape[:-1])
    result = np.zeros(shape + (degree + 1,))
    for first in range(left.shape[-1]):
        for second in range(right.shape[-1]):
            result[..., first + second] += left[..., first] * right[..., second]
    return result


def signed_integral(grid, power):
    widths = np.diff(grid).reshape((-1,) + (1,) * (power.ndim - 2))
    return np.sum(widths * np.sum(power / np.arange(1, power.shape[-1] + 1), axis=-1), axis=0)


def absolute_integral(grid, power):
    controls = bernstein(power)
    degree = controls.shape[-1] - 1
    widths = np.diff(grid)
    flat = controls.reshape(len(widths), -1, degree + 1)
    upper_rows = widths[:, None] * np.mean(abs(flat), axis=2)
    lower_rows = widths[:, None] * abs(np.mean(flat, axis=2))
    uncertain = np.argwhere(np.any(flat < 0., axis=2) & np.any(flat > 0., axis=2))
    for count, (index, column) in enumerate(uncertain):
        if count % 256 == 0:
            guard()
        stack = [(flat[index, column], widths[index], 1e-12 * upper_rows[index, column], 0)]
        total_upper, total_lower = 0., 0.
        while stack:
            values, width, tolerance, depth = stack.pop()
            upper = width * np.mean(abs(values))
            lower = width * abs(np.mean(values))
            if upper - lower <= tolerance or depth >= 60:
                total_upper += upper
                total_lower += lower
                continue
            levels = [values]
            for order in range(degree):
                levels.append((levels[-1][:-1] + levels[-1][1:]) / 2)
            left = np.array([level[0] for level in levels])
            right = np.array([level[-1] for level in levels[::-1]])
            stack.append((right, width / 2, tolerance / 2, depth + 1))
            stack.append((left, width / 2, tolerance / 2, depth + 1))
        upper_rows[index, column], lower_rows[index, column] = total_upper, total_lower
    shape = power.shape[1:-1]
    upper = upper_rows.sum(axis=0).reshape(shape)
    lower = lower_rows.sum(axis=0).reshape(shape)
    gap = float(np.max((upper - lower) / np.maximum(upper, 1e-80)))
    require(np.isfinite(upper).all() and gap < ALGEBRA, "absolute polynomial enclosure")
    return upper, lower, gap


def supremum_upper(power):
    controls = bernstein(power)
    flat = controls.reshape(len(controls), -1, controls.shape[-1])
    answers = []
    for column in range(flat.shape[1]):
        values = flat[:, column]
        lower = float(np.max(abs(values[:, [0, -1]])))
        upper_rows = np.max(abs(values), axis=1)
        heap = [(-float(upper_rows[index]), int(index), values[index], 0) for index in np.flatnonzero(upper_rows > lower)]
        heapq.heapify(heap)
        serial = len(values)
        while heap and -heap[0][0] - lower > 1e-12 * max(-heap[0][0], 1e-80):
            if serial % 256 == 0:
                guard()
            negative_upper, _, values, depth = heapq.heappop(heap)
            require(depth < 60, "source supremum subdivision depth")
            levels = [values]
            for order in range(len(values) - 1):
                levels.append((levels[-1][:-1] + levels[-1][1:]) / 2)
            children = (np.array([level[0] for level in levels]), np.array([level[-1] for level in levels[::-1]]))
            lower = max(lower, abs(float(levels[-1][0])))
            for child in children:
                upper = float(np.max(abs(child)))
                if upper > lower:
                    heapq.heappush(heap, (-upper, serial, child, depth + 1))
                    serial += 1
        answers.append(max(lower, -heap[0][0] if heap else lower))
    return np.array(answers).reshape(power.shape[1:-1])


def unit_checks():
    grid = np.linspace(0., 1., 13)
    polynomials = [np.poly1d([1.]), np.poly1d([1., -.5]), np.poly1d([1., 0., 0.]),
                   np.poly1d(np.poly([.2, .5, .8]))]
    reports = []
    for left in polynomials:
        for right in polynomials:
            product = left * right
            coefficients = multiply(scaled_power(grid, left(grid)), scaled_power(grid, right(grid)))
            primitive = product.integ()
            exact_signed = float(primitive(1.) - primitive(0.))
            roots = sorted(float(root.real) for root in product.r if abs(root.imag) < 1e-6 and 0 < root.real < 1)
            points = [0., *roots, 1.]
            exact_absolute = sum(abs(float(primitive(end) - primitive(start))) for start, end in zip(points[:-1], points[1:]))
            upper, lower, gap = absolute_integral(grid, coefficients)
            predicted = float(signed_integral(grid, coefficients))
            passed = abs(predicted - exact_signed) < 1e-12 and upper + 1e-12 >= exact_absolute and lower - 1e-12 <= exact_absolute
            require(passed, "known degree-six polynomial product")
            reports.append(dict(left=left.c.tolist(), right=right.c.tolist(), signed=predicted, expected=exact_signed,
                                upper=float(upper), lower=float(lower), absolute_expected=exact_absolute, gap=gap, passed=True))
    sample = np.linspace(0., 1., 1001)
    for polynomial in polynomials:
        upper = float(supremum_upper(scaled_power(grid, polynomial(grid))))
        require(upper + 1e-14 >= float(np.max(abs(polynomial(sample)))), "source supremum bound")
    return reports

