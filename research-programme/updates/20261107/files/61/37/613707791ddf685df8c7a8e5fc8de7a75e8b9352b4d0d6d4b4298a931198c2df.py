from decimal import Decimal
from bisect import bisect_right
import numpy as np


ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
HALF = ONE/TWO


def decimal(value):
    return value if isinstance(value, Decimal) else Decimal.from_float(float(value))


def polynomial(coefficients, coordinate):
    future, following = ZERO, ZERO
    for coefficient in coefficients[:0:-1]:
        future, following = coefficient+TWO*coordinate*future-following, future
    return coefficients[0]+coordinate*future-following


def derivative(coefficients):
    result = [ZERO]*(len(coefficients)-1)
    for index in range(len(result)-1, -1, -1):
        result[index] = TWO*(index+1)*coefficients[index+1]
        if index+2<len(result):
            result[index] += result[index+2]
    result[0] /= TWO
    return [TWO*value for value in result]


class SourceMap:
    def __init__(self, inverse, source, velocity, mode):
        if mode not in ('nodal_contraction', 'rounded_coefficients'):
            raise ValueError(mode)
        def coefficients(values):
            if mode=='rounded_coefficients':
                return [decimal(value) for value in inverse@values]
            return [sum((decimal(coefficient)*decimal(value) for coefficient,value in zip(row,values)), ZERO)
                for row in inverse]
        self.position = coefficients(source)
        self.velocity = coefficients(velocity)
        self.position_derivative = derivative(self.position)
        self.lower, self.upper = self.at(-HALF)[0], self.at(HALF)[0]
        if self.lower>=self.upper:
            raise ValueError('Nonmonotone source endpoints')
        self.minimum_derivative_bound = self.position[1]*TWO-sum(
            (TWO*index**2*abs(value) for index,value in enumerate(self.position) if index>=2), ZERO)
        if self.minimum_derivative_bound<=ZERO:
            raise ValueError('Source monotonicity not certified')

    def at(self, label):
        coordinate = TWO*label
        return polynomial(self.position,coordinate), polynomial(self.position_derivative,coordinate), polynomial(self.velocity,coordinate)

    def inverse(self, radius):
        label = (radius-self.lower)/(self.upper-self.lower)-HALF
        for unused in range(12):
            value, jacobian, velocity = self.at(label)
            change = (value-radius)/jacobian
            label -= change
            if abs(change)<Decimal('1e-58'):
                if abs(self.at(label)[0]-radius)>Decimal('1e-56') or abs(label)>HALF+Decimal('1e-50'):
                    raise ValueError('Invalid source inverse')
                return min(HALF,max(-HALF,label))
        raise ValueError('Source inverse did not converge')


class MetricPolynomial:
    def __init__(self, solver, solution, components):
        self.edges = [decimal(value) for value in solver.edges]
        self.centres = [decimal(value) for value in solver.centers]
        self.lengths = [decimal(value) for value in solver.lengths]
        self.components = components
        self.left = [[decimal(value) for value in solution['left'][component]] for component in components]
        self.primitive = [[[decimal(value) for value in row] for row in solution['primitives'][component]] for component in components]

    def cell(self, radius):
        return min(len(self.lengths)-1,max(0,bisect_right(self.edges,radius)-1))

    def at(self, radius, cell=None):
        cell = self.cell(radius) if cell is None else cell
        coordinate = TWO*(radius-self.centres[cell])/self.lengths[cell]
        return [left[cell]+polynomial(primitive[cell],coordinate) for left,primitive in zip(self.left,self.primitive)]


def densities(radius, values, mass_time, source, mass, coupling):
    enclosed, logarithm = values
    metric = ONE-TWO*enclosed/radius
    lapse = logarithm.exp()
    if metric<=ZERO:
        raise ValueError('Trapped chart')
    coefficient = lapse/(coupling*metric.sqrt())
    dust_loading, dust_current, speed = ZERO, ZERO, ZERO
    if source.lower<radius<source.upper:
        label = source.inverse(radius)
        unused,jacobian,speed = source.at(label)
        clock_squared = lapse*lapse-speed*speed/metric
        if clock_squared<=ZERO:
            raise ValueError('Non-timelike source')
        weight = 6*(label+HALF)*(HALF-label)/jacobian
        dust_loading = coupling*mass*weight*metric.sqrt()*lapse/clock_squared.sqrt()
        dust_current = mass*weight*lapse*lapse*speed/clock_squared.sqrt()
    gravity = coefficient*mass_time
    remainder = mass_time+speed*dust_loading
    combined = coefficient*remainder
    return gravity,dust_current,combined,combined-gravity-dust_current,remainder
