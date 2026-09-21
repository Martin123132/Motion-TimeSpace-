from derive_annular_source_gravity_20260914 import EvidenceRun
import verify_annular_boundary_response_20260916 as original
import numpy as np


def maximum(matrix):
    return float(np.max(abs(np.asarray(matrix)), initial=0.))


if __name__=='__main__':
    original.maximum = maximum
    original.EvidenceRun = lambda label, source: EvidenceRun('annular-boundary-dynamic-response-attempt02', __file__)
    original.main()
