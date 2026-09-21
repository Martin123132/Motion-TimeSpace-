from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_cut_initial_data_20260915 import compatible_initial_state
import run_annular_cut_curved_background_20260915 as evolution
import json
import numpy as np


class CompatibleEvidence(EvidenceRun):
    def __init__(self, unused_label, unused_source):
        super().__init__('annular-cut-curved-background-evolution-attempt02', __file__)
        previous = self.root/'source-intake/navier-stokes/20260914/annular-cut-curved-background-evolution-attempt01/status.json'
        status = json.loads(previous.read_text())
        self.own(previous)
        self.check('original_incompatible_preparation_and_failed_gate_preserved', status['state'] == 'failed'
                   and any(not row['passed'] for row in status['checks']))
        for count in [17, 33, 65]:
            system = evolution.BackgroundCutAction(count, True)
            coordinates, rates, unused = compatible_initial_state(system, 0.)
            position, velocity = coordinates[-1], rates[-1]
            cell = np.searchsorted(system.radii, position)-1
            fraction = (position-system.radii[cell])/system.spacing
            trace = (1-fraction)*coordinates[cell]+fraction*coordinates[cell+1]
            trace_rate = (1-fraction)*rates[cell]+fraction*rates[cell+1]
            trace_rate += velocity*(coordinates[cell+1]-coordinates[cell])/system.spacing
            self.check(str(count)+'_common_smooth_initial_trace_and_rate', max(abs(trace), abs(trace_rate)) < 2e-13)
        self.report.update(initial_data='Common compact smooth field with q=0 and q_t+V*q_R=0 at the source, linear in its neighbourhood.',
                           first_attempt_not_relabelled_as_repaired=True,
                           equations_time_window_and_gates_unchanged=True,
                           initial_state_not_an_exact_solution=True)


if __name__ == '__main__':
    evolution.EvidenceRun = CompatibleEvidence
    evolution.history_state = compatible_initial_state
    evolution.main()
