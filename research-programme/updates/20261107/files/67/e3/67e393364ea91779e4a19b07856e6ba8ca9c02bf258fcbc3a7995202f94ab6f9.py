from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal, getcontext
import numpy as np


def legendre_pair(degree, point):
    previous, current = Decimal(1), point
    if degree == 0:
        return previous, Decimal(0)
    for index in range(2, degree + 1):
        previous, current = current, ((2 * index - 1) * point * current - (index - 1) * previous) / index
    derivative = degree * (point * current - previous) / (point * point - 1)
    return current, derivative


def decimal_label_rule(order):
    if order < 2:
        raise ValueError('Label quadrature requires order at least two')
    initial = np.polynomial.legendre.leggauss(order)[0]
    roots, weights = [Decimal(0)] * order, [Decimal(0)] * order
    tolerance = Decimal(10) ** (8 - getcontext().prec)
    for index in range((order + 1) // 2):
        root = Decimal.from_float(float(initial[index]))
        for iteration in range(20):
            value, derivative = legendre_pair(order, root)
            correction = value / derivative
            root -= correction
            if abs(correction) < tolerance:
                break
        else:
            raise RuntimeError('Decimal Gauss root failed to converge')
        value, derivative = legendre_pair(order, root)
        if abs(value) > tolerance * 100:
            raise RuntimeError('Decimal Gauss root residual')
        weight = 2 / ((1 - root * root) * derivative * derivative)
        opposite = order - index - 1
        roots[index], roots[opposite] = root, -root
        weights[index] = weights[opposite] = weight
    labels = np.array([value / 2 for value in roots], dtype=object)
    weights = np.array([weight / 2 * 6 * (label + Decimal('.5')) * (Decimal('.5') - label)
        for label, weight in zip(labels, weights)], dtype=object)
    return labels, weights


def exact_weighted_moment(power):
    if power % 2:
        return Decimal(0)
    return Decimal(3) / (Decimal(2) ** power * (power + 1) * (power + 3))
