import math


MAX_ORDER = 5


KEYS = [(degree_u, degree_v, degree_r) for degree_u in range(2) for degree_v in range(MAX_ORDER + 1) for degree_r in range(MAX_ORDER + 1 - degree_v)]
INDEX = {key: position for position, key in enumerate(KEYS)}
PRODUCT = {(left, right): INDEX.get(tuple(first + second for first, second in zip(KEYS[left], KEYS[right]))) for left in range(len(KEYS)) for right in range(len(KEYS))}


class Jet:
    __array_priority__ = 1000
    numpy = None
    count = 1

    def __init__(self, data, active):
        self.data = data
        self.active = tuple(active)

    @classmethod
    def constant(cls, value):
        data = cls.numpy.zeros((len(KEYS), cls.count))
        data[0] = value
        return cls(data, [] if cls.numpy.all(data[0] == 0) else [0])

    @classmethod
    def variable(cls, value, axis):
        result = cls.constant(value)
        powers = [0, 0, 0]
        powers[axis] = 1
        position = INDEX[tuple(powers)]
        result.data[position] = 1
        result.active = tuple(set(result.active) | {position})
        return result

    def __add__(self, other):
        other = other if isinstance(other, Jet) else Jet.constant(other)
        return Jet(self.data + other.data, set(self.active) | set(other.active))

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.data, self.active)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Jet) else -self.numpy.asarray(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, Jet):
            return Jet(self.data * other, self.active)
        data = self.numpy.zeros_like(self.data)
        active = set()
        for left in self.active:
            for right in other.active:
                position = PRODUCT[left, right]
                if position is not None:
                    data[position] += self.data[left] * other.data[right]
                    active.add(position)
        return Jet(data, active)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Jet):
            return self * other**-1
        return Jet(self.data / other, self.active)

    def __rtruediv__(self, other):
        return self**-1 * other

    def remainder(self):
        data = self.data.copy()
        data[0] = 0
        return Jet(data, [position for position in self.active if position != 0])

    def __pow__(self, exponent):
        if isinstance(exponent, int) and exponent >= 0:
            result = Jet.constant(1)
            base = self
            remaining = exponent
            while remaining:
                if remaining % 2:
                    result = result * base
                remaining //= 2
                if remaining:
                    base = base * base
            return result
        if self.numpy.any(self.data[0] == 0):
            raise ZeroDivisionError("Taylor expansion about a zero denominator")
        relative = self.remainder() / self.data[0]
        result = Jet.constant(1)
        power = Jet.constant(1)
        coefficient = 1.0
        for degree in range(1, MAX_ORDER + 2):
            power = power * relative
            coefficient *= (exponent - degree + 1) / degree
            result = result + coefficient * power
        return result * self.data[0]**exponent

    def exp(self):
        result = Jet.constant(1)
        power = Jet.constant(1)
        remainder = self.remainder()
        for degree in range(1, MAX_ORDER + 2):
            power = power * remainder
            result = result + power / math.factorial(degree)
        return result * self.numpy.exp(self.data[0])

    def log(self):
        if self.numpy.any(self.data[0] <= 0):
            raise ValueError("Real logarithm outside positive branch")
        result = Jet.constant(self.numpy.log(self.data[0]))
        relative = self.remainder() / self.data[0]
        power = Jet.constant(1)
        for degree in range(1, MAX_ORDER + 2):
            power = power * relative
            result = result + (-1)**(degree + 1) * power / degree
        return result

    def derivative(self, axis):
        data = self.numpy.zeros_like(self.data)
        active = set()
        for position in self.active:
            powers = list(KEYS[position])
            degree = powers[axis]
            if degree:
                powers[axis] -= 1
                target = INDEX[tuple(powers)]
                data[target] = degree * self.data[position]
                active.add(target)
        return Jet(data, active)

    def extract(self, degree_u=0):
        return self.data[INDEX[degree_u, 0, 0]]


def jet_log(value):
    return value.log() if isinstance(value, Jet) else Jet.numpy.log(value)
