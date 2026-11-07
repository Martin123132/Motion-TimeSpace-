from exact_angular_factor import *


class FastSplit(SplitReal):
    def __init__(self, spectra, mode, density=48001):
        super().__init__(spectra, mode, density)
        self.angular_cache = {}

    def intensity_batch(self, energy, soft, hard_direction, soft_direction):
        key = tuple(hard_direction) + tuple(soft_direction)
        if key not in self.angular_cache:
            self.angular_cache[key] = angular_basis(hard_direction, soft_direction)
        return factorized_intensity(energy, soft, hard_direction, soft_direction, self.angular_cache[key])

    def event_products(self, parameters, soft, direction, chemical=False):
        saved = weak.intensity_batch
        weak.intensity_batch = self.intensity_batch
        try:
            return super().event_products(parameters, soft, direction, chemical)
        finally:
            weak.intensity_batch = saved
