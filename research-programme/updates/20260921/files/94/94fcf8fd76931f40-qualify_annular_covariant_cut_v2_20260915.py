from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction
import qualify_annular_covariant_cut_20260915 as qualification
import warnings
import json
import numpy as np


class CorrectedEvidence(EvidenceRun):
    def __init__(self, unused_label, unused_source):
        super().__init__('annular-covariant-cut-canonical-qualification-attempt02', __file__)
        path = self.root/'source-intake/navier-stokes/20260914/annular-covariant-cut-canonical-qualification-attempt01/status.json'
        self.previous = json.loads(path.read_text())
        self.own(path)
        self.check('original_warning_qualification_preserved', self.previous['state'] == 'complete'
                   and len(self.previous['checks']) == 27)
        self.report.update(original_complex_Hessian_dtype_warning_preserved=True,
                           repair='Promote coordinate storage to the common coordinate/rate/time dtype before assembling the Hessian.',
                           equation_or_gate_changes=False, complex_cast_warnings_are_errors=True)

    def complete(self):
        fields = ['coordinate_variation_error', 'velocity_variation_error', 'minimum_inertia', 'source_schur', 'noether_error']
        error = max(abs(new[field]-old[field]) for new, old in zip(self.report['cases'], self.previous['cases']) for field in fields)
        self.check('same_physical_results_after_dtype_repair', len(self.report['cases']) == len(self.previous['cases']) and error < 2e-11, error)
        super().complete()


if __name__ == '__main__':
    warnings.simplefilter('error', np.exceptions.ComplexWarning)
    qualification.CurvedCutAction = CurvedCutAction
    qualification.EvidenceRun = CorrectedEvidence
    qualification.main()
