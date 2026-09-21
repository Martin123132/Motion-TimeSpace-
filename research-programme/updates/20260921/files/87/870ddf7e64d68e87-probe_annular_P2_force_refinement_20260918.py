from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_live_P2_current_20260918 import LiveP2Tangent
from derive_annular_P2_conforming_force_lift_20260918 import conforming_force_lift
from budget_annular_P2_saved_force_20260918 import checked_json
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


class SourceRefinedSystem(PrimitiveP2System):
    def __init__(self, gram, source_splits):
        super().__init__(65, gram, layer_degree=14, radial_degree=18, action_order=32, label_order=20)
        self.model = LocallyRefinedSourceAction(65, gram, order=32, background_mass=.7, source_splits=source_splits)
        self.count = self.model.count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configuration', choices=['uniform129', 'source16'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-initial-force-refinement-'+args.configuration+'-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            only_initial_data_not_an_evolved_accuracy_test=True, same_analytic_initial_preparation=True,
            distinct_discrete_states_not_a_saved_state_transfer=True, finite_Gram_retained=True,
            no_force_correction_applied=True, full_live_P2_force_convergence_proven=False,
            uniform_refinement_changes_Gram_spacing=True,
            source_only_refinement_keeps_Gram_base_grid=True)
        for branch in ['reference', 'MTS']:
            started = perf_counter()
            comparison = checked_json(evidence, 'annular-P2-continuum-comparison-65-attempt01', branch+'-65.json')
            if args.configuration == 'uniform129':
                system = PrimitiveP2System(129, branch == 'MTS', layer_degree=14,
                    radial_degree=18, action_order=32, label_order=20)
            else:
                system = SourceRefinedSystem(branch == 'MTS', 16)
            coordinates, momenta, prepared_rates, unused = system.initial()
            tangent = LiveP2Tangent(system, coordinates, momenta)
            row = conforming_force_lift(tangent)
            current = tangent.layer_data(0.)
            canonical = float(system.canonical_residual(coordinates, momenta, tangent.rates, tangent.geometry))
            radial = [float(value) for value in tangent.geometry.off_grid_residual(tangent.rates)]
            target = comparison['times'][0]
            baseline_error = target['force']['reduced_wave_force']-target['continuum_wave_force']
            error = row['force']-target['continuum_wave_force']
            row.update(configuration=args.configuration, branch=branch, base_count=system.base_count,
                scalar_nodes=system.count, source_splits=system.model.source_splits, time=0.,
                Gram_spacing=float(system.model.gram_spacing),
                continuum_force=float(target['continuum_wave_force']), force_error_from_continuum=float(error),
                old65_initial_force_error=float(baseline_error), absolute_error_ratio=float(abs(error/baseline_error)),
                canonical_residual=canonical, radial_residual=radial,
                prepared_rate_recovery_error=float(max(abs(prepared_rates-tangent.rates).ravel())),
                source_Euler_residual=float(abs(current.source_euler)),
                scalar_Euler_residual=float(max(abs(current.euler))), seconds=perf_counter()-started)
            evidence.report['cases'].append(row)
            evidence.save()
            evidence.check(branch+'_prepared_canonical_state', canonical < 2e-10 and row['prepared_rate_recovery_error'] < 2e-10)
            evidence.check(branch+'_radial_constraints', max(radial) < 2e-9, radial)
            evidence.check(branch+'_force_lift_identity', row['identity_error'] < 2e-9, row['identity_error'])
            evidence.check(branch+'_local_cauchy_bound', all(abs(part['signed_lifting_work']) <= part['cauchy_bound']+2e-14
                for part in row['elements']))
            print(json.dumps({name:value for name,value in row.items() if name != 'elements'}), flush=True)
        log = evidence.output/'completion-log.txt'
        with log.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(log, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
