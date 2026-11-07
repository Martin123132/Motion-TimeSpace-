from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_20260919 import DecimalAction as StoredBandAction
from annular_decimal_transport_20260919 import DecimalMap, decimal_array, zero_array, dot, propagate
import numpy as np


class DecimalAction(StoredBandAction):
    def __init__(self, data):
        canonical = dict(data)
        bands = data['mass_bands'].copy()
        count = bands.shape[1]
        discrepancy = 0.
        for offset in [1, 2]:
            discrepancy = max(discrepancy, float(np.max(abs(bands[2-offset, offset:]-bands[2+offset, :count-offset]))))
            bands[2-offset, offset:] = bands[2+offset, :count-offset]
        canonical['mass_bands'] = bands
        self.unused_upper_triangle_discrepancy = discrepancy
        self.mass_convention = 'Same lower triangle consumed by original scipy cholesky_banded(lower=True); upper storage unused.'
        super().__init__(canonical)
