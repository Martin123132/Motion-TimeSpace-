from factored_epoch_response import FactoredEpochResponse


class BoundedFactoredEpochResponse(FactoredEpochResponse):
    def __init__(self, factors, high, low, event_capacity=4):
        if type(event_capacity) is not int or not 1 <= event_capacity <= 8:
            raise ValueError('Use an integer event-cache capacity between1 and8')
        super().__init__(factors, high, low)
        self.event_capacity = event_capacity
        self.evictions = 0

    def current(self, join, degree, soft_value, event, sign):
        result = super().current(join, degree, soft_value, event, sign)
        while len(self.current_operators) > self.event_capacity:
            oldest = next(iter(self.current_operators))
            del self.current_operators[oldest]
            for key in tuple(self.current_readouts):
                if key[0] == oldest:
                    del self.current_readouts[key]
            self.evictions += 1
        return result
