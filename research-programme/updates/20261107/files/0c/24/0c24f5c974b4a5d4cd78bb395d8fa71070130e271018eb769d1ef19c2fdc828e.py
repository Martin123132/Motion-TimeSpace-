import numpy as np
from annular_covariant_cut_action_20260915 import CurvedCutAction as OriginalCutAction
from annular_covariant_cut_action_20260915 import history, source_history, history_state


class CurvedCutAction(OriginalCutAction):
    def evaluate(self, time, coordinates, rates, pulled=None):
        dtype = np.result_type(coordinates, rates, time)
        coordinates = np.asarray(coordinates, dtype=dtype)
        return super().evaluate(time, coordinates, rates, pulled)
