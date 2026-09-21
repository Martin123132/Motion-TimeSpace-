from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_radial_response_20260918 import RadialResponse as OriginalRadialResponse
from copy import copy
import numpy as np


class RadialResponse(OriginalRadialResponse):
    def __init__(self, loads, **parameters):
        aligned = copy(loads)
        aligned.edges = np.unique(np.concatenate([loads.edges, loads.nodes]))
        super().__init__(aligned, **parameters)
