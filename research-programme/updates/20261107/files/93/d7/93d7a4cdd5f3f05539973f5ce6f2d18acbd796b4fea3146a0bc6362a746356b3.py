from fractions import Fraction
import numpy as np


def product_basis_values(coordinate, degree, derivative=0):
    if derivative not in (0, 1):
        raise ValueError('Only value and first derivative are implemented')
    coordinate = np.asarray(coordinate)
    nodes = [Fraction(index, degree) for index in range(degree + 1)]
    output = np.empty(coordinate.shape + (degree + 1,))
    for column, node in enumerate(nodes):
        others = [point for index, point in enumerate(nodes) if index != column]
        denominator = Fraction(1)
        for point in others:
            denominator *= node - point
        if derivative == 0:
            value = np.ones_like(coordinate)
            for point in others:
                value *= coordinate - float(point)
        else:
            value = np.zeros_like(coordinate)
            for omitted in range(len(others)):
                term = np.ones_like(coordinate)
                for index, point in enumerate(others):
                    if index != omitted:
                        term *= coordinate - float(point)
                value += term
        output[..., column] = value / float(denominator)
    return output
