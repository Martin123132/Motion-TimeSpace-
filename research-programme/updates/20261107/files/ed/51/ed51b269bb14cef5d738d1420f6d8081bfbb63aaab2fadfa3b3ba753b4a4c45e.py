from derive_annular_source_gravity_20260914 import EvidenceRun
from diagnose_annular_wave_flux_form_20260929 import verified_sources
from annular_native_precision_context_20260929 import restore_native
from annular_source_centered_quadrature_20260929 import reference_offsets, CenteredLabelDensity
from decimal import localcontext
from time import perf_counter
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-wave-support-extent-attempt01', __file__)
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, github_action=False, subagents_used=False)
        digests = verified_sources(evidence)
        with localcontext() as context:
            context.prec = 70
            restored = restore_native(evidence, digests, 'reference-reference', 'fine', perf_counter()+600)
            action = restored['action']
            geometry = object.__new__(CenteredLabelDensity)
            geometry.action, geometry.anchor, geometry.references = action, float(action.owner.model.anchor), reference_offsets(action)
            geometry.source_coefficients = action.owner.layer_rule.inverse @ (action.source-geometry.anchor)
            geometry.source_derivative = 2*np.polynomial.chebyshev.chebder(geometry.source_coefficients)
            endpoints = np.concatenate([geometry.geometry(geometry.references, label)[0] for label in [-.5, .5]])
            metric = action.solver.edges-geometry.anchor
            summary = dict(material_min=float(min(endpoints)), material_max=float(max(endpoints)),
                metric_min=float(metric[0]), metric_max=float(metric[-1]),
                inner_extrapolation=float(max(0., metric[0]-min(endpoints))),
                outer_extrapolation=float(max(0., max(endpoints)-metric[-1])),
                labels=action.source.tolist(), layer_width=float(action.owner.width),
                outside_endpoint_count=int(np.count_nonzero((endpoints < metric[0]) | (endpoints > metric[-1]))),
                response_domains=[item.solver.edges[[0, -1]].tolist() for item in restored['precision'].position.responses],
                original_evaluator_rule='Clipped polynomial index with unconstrained polynomial coordinate',
                valid_for_claim=False)
            evidence.report['cases'].append(summary)
            evidence.check('finite_extent', all(np.isfinite(endpoints)))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
