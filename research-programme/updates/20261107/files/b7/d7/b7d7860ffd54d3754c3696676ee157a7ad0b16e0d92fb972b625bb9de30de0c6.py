from derive_annular_source_gravity_20260914 import EvidenceRun
from validate_annular_wave_flux_form_20260929 import fixture, family_force
from annular_wave_flux_events_20260929 import EulerianWaveFlux
from decimal import localcontext
from time import perf_counter
from types import SimpleNamespace
import numpy as np


def main():
    evidence = EvidenceRun('annular-wave-flux-events-manufactured-attempt01', __file__)
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, manufactured_data_only=True,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.own(evidence.root/'scripts/annular_wave_flux_events_20260929.py')
        maximum = lambda values: float(np.max(np.abs(values)))
        with localcontext() as context:
            context.prec = 70
            wave = fixture()
            wave.__class__ = EulerianWaveFlux
            wave.action.owner.layer_degree = 0
            wave.action.owner.layer_rule = SimpleNamespace(inverse=np.ones((1, 1)))
            wave.action.cardinal = lambda labels: np.ones((np.asarray(labels).size, 1))
            results = []
            for order in [16, 24]:
                result, diagnostics = wave.integrate(order, order, (1, 5), perf_counter()+300, lambda stage: None)
                evidence.check('weak_flux_'+str(order), maximum(result['regular_flux']-result['weak']) < 2e-11,
                    maximum(result['regular_flux']-result['weak']))
                evidence.check('base_weak_flux_'+str(order), maximum(result['base_flux']-result['base_weak']) < 2e-11,
                    maximum(result['base_flux']-result['base_weak']))
                evidence.check('oracle_'+str(order), maximum(result['oracle_difference']) < 2e-11,
                    maximum(result['oracle_difference']))
                results.append(result)
            evidence.check('event_split_pair', maximum(results[1]['complete_flux']-results[0]['complete_flux']) < 2e-11,
                maximum(results[1]['complete_flux']-results[0]['complete_flux']))
            labels, weights = np.polynomial.legendre.leggauss(48)
            labels, weights = labels/2, weights/2
            weights *= 6*(labels+.5)*(.5-labels)
            derivatives = []
            for step in [1e-4, 5e-5]:
                derivative = sum(weight*(family_force(wave, label, step)-family_force(wave, label, -step))/(2*step)
                    for label, weight in zip(labels, weights))
                derivatives.append(derivative)
            richardson = (4*derivatives[-1]-derivatives[0])/3
            error = maximum(results[-1]['complete_flux']-richardson)
            evidence.check('independent_label_integrated_moving_family', error < 2e-8, error)
            for name in ['moving_cuts', 'jumps', 'endpoints']:
                error = maximum(richardson-(results[-1]['complete_flux']-results[-1][name]))
                evidence.check('omit_'+name+'_negative_control', error > 1e-6, error)
            path = evidence.output/'manufactured-event-force.npz'
            np.savez_compressed(path, **results[-1], independent_derivative=richardson)
            evidence.own(path, 'outputs')
            evidence.report['cases'].append(dict(derivative_error=maximum(results[-1]['complete_flux']-richardson),
                pair_error=maximum(results[-1]['complete_flux']-results[0]['complete_flux']), valid_for_claim=False))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
