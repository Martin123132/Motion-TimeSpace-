from emission_common import *


def polynomial_derivative(segment, expansion):
    coordinate = (expansion - segment.t_old) / segment.h
    value = np.zeros_like(segment.y_old)
    derivative = np.zeros_like(value)
    for index, coefficient in enumerate(reversed(segment.F)):
        intermediate = value + coefficient
        factor = coordinate if index % 2 == 0 else 1 - coordinate
        slope = 1 if index % 2 == 0 else -1
        derivative = derivative * factor + intermediate * slope
        value = intermediate * factor
    return derivative / segment.h


def solution_derivative(solution, expansion):
    dense = solution.sol
    index = int(np.clip(np.searchsorted(dense.ts, expansion, side='left') - 1, 0, len(dense.interpolants) - 1))
    return polynomial_derivative(dense.interpolants[index], expansion)
