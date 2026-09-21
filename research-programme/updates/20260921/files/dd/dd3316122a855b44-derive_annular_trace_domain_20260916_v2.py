from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_boundary_response_20260916 import field_matrices
import derive_annular_trace_domain_20260916 as original
import copy
import numpy as np


diagnostics = []


def analytic_quadrature_matrices(system, position):
    corrected = copy.copy(system)
    fraction = system.fractions
    shapes = np.column_stack([(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)])
    derivatives = np.column_stack([4*fraction-3, 4-8*fraction, 4*fraction-1])
    indices = np.repeat(system.element_indices, len(fraction), axis=0)
    valid = indices >= 0
    corrected.reference_indices = np.maximum(indices, 0)
    corrected.reference_shape = np.tile(shapes, (len(system.edges)-1, 1))*valid
    corrected.reference_radial = np.tile(derivatives, (len(system.edges)-1, 1))*valid/np.repeat(np.diff(system.edges), len(fraction))[:, None]
    measured = field_matrices(system, position)
    analytic = field_matrices(corrected, position)
    source_edge = int(np.searchsorted(system.edges, system.anchor))
    width = system.edges[source_edge+1]-system.anchor
    layer = np.zeros(system.count)
    layer[system.element_indices[source_edge, 1]] = width/4
    diagnostics.append(dict(count=system.base_count, branch='MTS' if system.gram else 'reference', source_splits=system.source_splits,
        mass_relative_coordinate_rounding=float((layer @ (measured['mass'] @ layer))/(layer @ (analytic['mass'] @ layer))-1),
        bulk_relative_coordinate_rounding=float((layer @ (measured['bulk'] @ layer))/(layer @ (analytic['bulk'] @ layer))-1)))
    return analytic


class DomainEvidence(EvidenceRun):
    def __init__(self, label, source):
        super().__init__('annular-trace-domain-and-inertia-attempt02', __file__)
        self.own(self.root/'scripts/derive_annular_trace_domain_20260916.py')
        self.own(self.root/'source-intake/navier-stokes/20260914/annular-trace-domain-and-inertia-attempt01/status.json')

    def complete(self):
        self.report.update(quadrature_coordinate_rounding=diagnostics,
            correction_scope='Diagnostic shape and derivative evaluations use known reference Gauss fractions directly rather than recovering fractions by subtraction of nearby physical coordinates.',
            existing_evolution_action_changed=False, original_analytic_formula_tolerances_preserved=True)
        super().complete()


if __name__=='__main__':
    original.field_matrices = analytic_quadrature_matrices
    original.EvidenceRun = DomainEvidence
    original.main()
