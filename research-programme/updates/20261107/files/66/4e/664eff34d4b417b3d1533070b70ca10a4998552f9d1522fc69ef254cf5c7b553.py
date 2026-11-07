from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_boundary_integral_20260930 import density_rows
from annular_C0_decimal_transport_20260930 import eulerian_density
from annular_compact_baseline_current_v2_20261001 import compact_rows
from probe_annular_C0_precise_transport_20260930 import converted
from decimal import localcontext
from mpmath import mp
from time import perf_counter
import ctypes
import json
import numpy as np
import sympy as sp


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 16):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun('annular-coefficient-baseline-probe-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter()+1800
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-compact-baseline-current.md')
        evidence.own(evidence.root/'DERIVATION-20261001-coefficient-weighted-current.md')
        local = sp.Symbol('x')
        for power in range(1, 6):
            interpolated = sp.interpolate([(sp.Integer(0), sp.Integer(0)), (sp.Rational(1, 2), sp.Rational(1, 2)**power), (sp.Integer(1), sp.Integer(1))], local)
            formula = (2**sp.Integer(2-power)-1)*local+(2-2**sp.Integer(2-power))*local**2
            evidence.check('P2_monomial_'+str(power), sp.expand(interpolated-formula)==0)
        for power, quotient in [(3, 1), (4, local+sp.Rational(3, 2)), (5, local**2+sp.Rational(3, 2)*local+sp.Rational(7, 4))]:
            interpolated = (2**sp.Integer(2-power)-1)*local+(2-2**sp.Integer(2-power))*local**2
            evidence.check('factored_interpolation_remainder_'+str(power), sp.expand(local**power-interpolated-local*(local-sp.Rational(1, 2))*(local-1)*quotient)==0)
        alpha, beta, alpha_r, beta_r, alpha_t, temporal, gradient, speed, speed_r, rate_r, acceleration, map_acceleration = sp.symbols(
            'alpha beta alpha_R beta_R alpha_t T g W W_R v_R q_ddot W_dot', nonzero=True)
        integral, weighted, weighted_r, profile = sp.symbols('I V V_R h')
        gradient_rate = rate_r-speed_r*gradient
        temporal_rate = acceleration-map_acceleration*gradient-speed*gradient_rate
        alpha_dot, beta_dot = alpha_t+speed*alpha_r, -beta*alpha_t/alpha+speed*beta_r
        momentum_rate = (alpha_dot+speed_r*alpha)*temporal+alpha*temporal_rate
        energy = (alpha*temporal**2+beta*gradient**2)/2
        energy_dot = (alpha_dot*temporal**2+beta_dot*gradient**2)/2+alpha*temporal*temporal_rate+beta*gradient*gradient_rate
        compact_energy = speed*(beta_r*gradient**2-alpha_r*temporal**2)/2+beta*gradient*rate_r-speed_r*energy
        evidence.check('exact_energy_reduction', sp.expand(energy_dot+(speed_r+alpha_t/alpha)*energy-temporal*momentum_rate-compact_energy)==0)
        flux = alpha*speed*temporal+beta*gradient
        original = -momentum_rate*weighted-flux*weighted_r+(energy_dot+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*profile
        compact = momentum_rate*(temporal*integral-weighted)-flux*weighted_r+compact_energy*integral+energy*speed*profile
        evidence.check('exact_compact_current', sp.expand(original-compact)==0)
        variables = [alpha, beta, alpha_r, beta_r, alpha_t, temporal, speed, speed_r, rate_r, acceleration, map_acceleration, weighted, weighted_r]
        derivative = sum(sp.diff(original-compact, variable)*sp.Symbol('delta_'+str(variable)) for variable in variables)
        evidence.check('exact_general_velocity_derivative', sp.expand(derivative)==0)
        mp.dps = 90
        with localcontext() as context:
            context.prec = 80
            for branch in ['reference-reference', 'MTS-primary']:
                if perf_counter()>deadline:
                    raise RuntimeError('Safe compact probe boundary')
                restored = restore(evidence, branch, 'third', deadline)
                evaluator = restored['evaluator']
                cells = np.linspace(0, len(evaluator.widths)-1, 96).astype(int)
                labels = np.tile([-.47, -.33, -.11, .03, .17, .29, .37, .47], 12)
                local = np.tile([.13, .47, .83], 32)
                lower = evaluator.geometry.geometry(evaluator.edges[cells], labels)[0]
                upper = evaluator.geometry.geometry(evaluator.edges[cells+1], labels)[0]
                offsets = lower+(upper-lower)*local
                packet, active = evaluator.packet(labels, offsets)
                values, unused, radial, unused2 = evaluator.metric.evaluate(offsets, evaluator.metric.cells(offsets))
                time = sum(item.evaluate(offsets, item.cells(offsets))[0] for item in evaluator.time_traces)
                radius = evaluator.anchor+offsets
                historical = density_rows(packet, radius, values, radial, time)
                rewritten = compact_rows(packet, radius, values, radial, time)
                exact_packet = {name:converted(value) for name, value in packet.items()}
                exact_args = [converted(value) for value in [radius, values, radial, time]]
                exact_old = eulerian_density(exact_packet, *exact_args)
                exact_new = compact_rows(exact_packet, *exact_args, precise=True)
                scale = np.maximum(np.maximum(abs(exact_old), abs(exact_new)), mp.mpf('1e-100'))
                relative = float(np.max(abs(exact_new-exact_old)/scale))
                evidence.check(branch+':active', active.all())
                evidence.check(branch+':90digit_original_current_identity', relative<1e-60, relative)
                target = np.asarray(exact_old, float)
                evidence.check(branch+':finite_binary_results', np.isfinite(historical).all() and np.isfinite(rewritten).all())
                path = evidence.output/(branch+'-compact-baseline.npz')
                np.savez_compressed(path, offsets=offsets, labels=labels, cells=cells, local=packet['local'],
                    old=historical, compact=rewritten, exact=target, old_error=historical-target, compact_error=rewritten-target)
                evidence.own(path, 'outputs')
                summary = dict(branch=branch, points=len(labels), high_precision_relative_identity=relative,
                    old_max_abs_error=np.max(abs(historical-target), axis=1).tolist(),
                    compact_max_abs_error=np.max(abs(rewritten-target), axis=1).tolist(),
                    integrated_baseline_replaced=False, C1_integral_replaced=False, valid_for_claim=False)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary), flush=True)
        evidence.report.update(seconds=perf_counter()-started, github_action=False, subagents_used=False,
            compact_current_derived=True, velocity_derivative_identity_proven=True, integrated_improvement_established=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
