from common import ALGEBRA, require
from scipy.interpolate import CubicSpline
import numpy as np


def polynomial_absolute(spline, grid):
    widths = np.diff(grid)
    shape = (len(widths),) + (1,) * (spline.c.ndim - 2)
    interval = widths.reshape(shape)
    cubic, quadratic, linear, constant = (spline.c[0] * interval**3, spline.c[1] * interval**2,
                                         spline.c[2] * interval, spline.c[3])
    controls = np.stack([constant, constant + linear / 3,
                         constant + 2 * linear / 3 + quadratic / 3,
                         constant + linear + quadratic + cubic], axis=-1)
    flat = controls.reshape(len(widths), -1, 4)
    upper_rows = widths[:, None] * abs(flat).sum(axis=2) / 4
    lower_rows = widths[:, None] * abs(flat.sum(axis=2)) / 4
    uncertain = np.argwhere(np.any(flat < 0., axis=2) & np.any(flat > 0., axis=2))
    for index, column in uncertain:
        initial_upper = upper_rows[index, column]
        stack = [(flat[index, column], widths[index], 1e-12 * initial_upper, 0)]
        upper_total, lower_total = 0., 0.
        while stack:
            values, width, tolerance, depth = stack.pop()
            upper = width * np.sum(abs(values)) / 4
            lower = width * abs(np.sum(values)) / 4
            if upper - lower <= tolerance or depth >= 60:
                upper_total += upper
                lower_total += lower
                continue
            first = (values[:-1] + values[1:]) / 2
            second = (first[:-1] + first[1:]) / 2
            middle = np.sum(second) / 2
            left = np.array([values[0], first[0], second[0], middle])
            right = np.array([middle, second[1], first[2], values[3]])
            stack.append((right, width / 2, tolerance / 2, depth + 1))
            stack.append((left, width / 2, tolerance / 2, depth + 1))
        upper_rows[index, column], lower_rows[index, column] = upper_total, lower_total
    output_shape = spline.c.shape[2:]
    upper = upper_rows.sum(axis=0).reshape(output_shape)
    lower = lower_rows.sum(axis=0).reshape(output_shape)
    gap = float(np.max((upper - lower) / np.maximum(upper, 1e-80)))
    require(np.isfinite(upper).all() and gap < ALGEBRA, "polynomial absolute enclosure precision")
    return upper, lower, gap


def integrate_budget(grid, contributions, stride):
    keep = np.unique(np.r_[np.arange(0, len(grid), stride), len(grid) - 1])
    selected = grid[keep]
    channels = CubicSpline(selected, contributions[keep], axis=0)
    combined = CubicSpline(selected, contributions[keep].sum(axis=2), axis=0)
    signed = channels.integrate(float(selected[0]), float(selected[-1]))
    channel_upper, channel_lower, channel_gap = polynomial_absolute(channels, selected)
    combined_upper, combined_lower, combined_gap = polynomial_absolute(combined, selected)
    return dict(stride=stride, signed_channels=signed.tolist(), signed_prediction=signed.sum(axis=1).tolist(),
                channel_absolute_budgets=channel_upper.tolist(), channel_absolute_lower=channel_lower.tolist(),
                combined_absolute_budget=combined_upper.tolist(), combined_absolute_lower=combined_lower.tolist(),
                enclosure_relative_gap=max(channel_gap, combined_gap),
                meaning="adaptive Bernstein absolute-integral enclosure for saved cubic interpolant; floating-point, not full continuum certification")


def unit_checks():
    grid = np.linspace(0., 1., 9)
    polynomials = [np.poly1d([1.]), np.poly1d([1., -.5]), np.poly1d([1., 0., 0.]),
                   np.poly1d(np.poly([.2, .5, .8]))]
    reports = []
    for polynomial in polynomials:
        values = polynomial(grid)
        contributions = np.stack([np.stack([values, -.4 * values], axis=1),
                                  np.stack([-2 * values, .8 * values], axis=1)], axis=1)
        roots = sorted(float(root.real) for root in polynomial.r if abs(root.imag) < 1e-12 and 0 < root.real < 1)
        endpoints = [0., *roots, 1.]
        integral = polynomial.integ()
        exact = sum(abs(float(integral(right) - integral(left))) for left, right in zip(endpoints[:-1], endpoints[1:]))
        expected = np.array([.6, 1.2]) * exact
        for stride in (1, 2):
            budget = integrate_budget(grid, contributions, stride)
            upper, lower = np.array(budget["combined_absolute_budget"]), np.array(budget["combined_absolute_lower"])
            require(np.all(upper + 1e-14 >= expected) and np.all(lower - 1e-14 <= expected), "known polynomial enclosure")
            reports.append(dict(coefficients=polynomial.c.tolist(), stride=stride, exact=expected.tolist(),
                                upper=upper.tolist(), lower=lower.tolist(), passed=True))
    return reports

