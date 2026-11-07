from common243 import *
import argparse


def local_law(equation, inverse, coordinate, profile):
    stiffness = equation.stiffness(coordinate)
    energy_map = equation.energy * inverse * stiffness
    gamma = 1 - (energy_map * equation.template)[0] / equation.heat
    equilibrium = -((energy_map * profile)[0] + 1) / (equation.heat * gamma)
    return gamma, equilibrium


def run_relaxation(model):
    modest()
    frozen = read(ROOT / 'relaxation-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['corner_hashes'][model] == digest(DATA / f'corner/{model}.json')
    inputs, checks = {}, []
    half = read(register(inputs, DATA / f'drives/{model}-half.json'))
    quarter = read(register(inputs, DATA / f'drives/{model}-quarter.json'))
    first, last = half['points'][:2]
    middle_coordinate = quarter['points'][1]['coordinate']
    with mp.workdps(80):
        equation = history.previous.ProbeEquation(model, 'candidate')
        inverse = equation.mass ** -1
        before, after = history.parse_state(first['state']), history.parse_state(last['state'])
        start, stop, middle = map(mp.mpf, (first['coordinate'], last['coordinate'], middle_coordinate))
        width, fraction = stop - start, (middle - start) / (stop - start)
        predicted_profile = before['profile'] + fraction * (after['profile'] - before['profile'])
        gamma0, equilibrium0 = local_law(equation, inverse, start, before['profile'])
        gamma1, equilibrium1 = local_law(equation, inverse, stop, after['profile'])
        gamma_middle, equilibrium_middle = local_law(equation, inverse, middle, predicted_profile)
        profile_rate, unused = prior.rhs(equation, before, start, inverse)
        check(checks, model + ':gas relaxation identity',
            (profile_rate['gas'] + gamma0 * (before['gas'] - equilibrium0)) / max(abs(profile_rate['gas']), mp.mpf('1e-300')))
        check(checks, model + ':positive local relaxation', int(min(gamma0, gamma_middle, gamma1) <= 0), 0)
        linear = before['gas'] + fraction * (after['gas'] - before['gas'])
        slow_slope = (equilibrium1 - equilibrium0) / width
        memory_factor_log = -gamma0 * (middle - start)
        memory = (before['gas'] - equilibrium0) * mp.exp(memory_factor_log)
        leading = equilibrium_middle + memory
        lagged = leading - slow_slope / gamma_middle
        numerical_prediction = dict(linear=mp.nstr(linear, 85), slow_equilibrium=mp.nstr(leading, 85),
            first_lag=mp.nstr(lagged, 85), gamma_start=mp.nstr(gamma0, 85),
            gamma_middle=mp.nstr(gamma_middle, 85), equilibrium_start=mp.nstr(equilibrium0, 85),
            initial_fast_amplitude=mp.nstr(before['gas'] - equilibrium0, 85))
        write(DATA / f'relaxation/{model}-prediction.json', dict(prediction=numerical_prediction,
            built_at=now(), coefficient_rule='Parent gas energy equation; coarse photon interpolation; no coefficient fit',
            scope='Post-diagnostic numerical audit, not a fresh held-out test; frozen-start exponential is only a local approximation'))
        observed = history.parse_state(quarter['points'][1]['state'])
        gamma_observed, equilibrium_observed = local_law(equation, inverse, middle, observed['profile'])
        observed_rate, unused = prior.rhs(equation, observed, middle, inverse)
        observed_identity = observed_rate['gas'] + gamma_observed * (observed['gas'] - equilibrium_observed)
        check(checks, model + ':saved probe gas relaxation identity',
            observed_identity / max(abs(observed_rate['gas']), mp.mpf('1e-300')))
        with mp.workdps(100):
            audit_equation = history.previous.ProbeEquation(model, 'candidate')
            audit_inverse = audit_equation.mass ** -1
            audit_gamma, audit_equilibrium = local_law(audit_equation, audit_inverse, middle, predicted_profile)
            check(checks, model + ':80/100 relaxation rate', gamma_middle / audit_gamma - 1)
            check(checks, model + ':80/100 equilibrium', equilibrium_middle - audit_equilibrium)
        linear_error = linear - observed['gas']
        report = dict(model=model, qualified=all(row['passed'] for row in checks), checks=checks,
            start=float(start), middle=float(middle), stop=float(stop), width=float(width), fraction=float(fraction),
            gamma_per_log_scale=[float(gamma0), float(gamma_middle), float(gamma1)],
            relaxation_width= float(1 / gamma0), relaxation_width_over_half_step=float(1 / gamma0 / width),
            initial_fast_amplitude=float(before['gas'] - equilibrium0), frozen_start_log_memory_factor=float(memory_factor_log),
            source_driven_start_rhs=float(profile_rate['gas']), linear_error=float(linear_error),
            leading_equilibrium_error=float(leading - observed['gas']),
            first_lag_error=float(lagged - observed['gas']),
            first_lag_error_over_linear_error=float(abs((lagged - observed['gas']) / linear_error)),
            true_equilibrium_lag=float(observed['gas'] - equilibrium_observed),
            coarse_photon_interpolation_equilibrium_error=float(equilibrium_middle - equilibrium_observed),
            prediction=numerical_prediction, script_sha256=digest(__file__), finished_at=now(),
            adopted_as_dense_output=False, original_failed_gates_remain=True,
            limitation='Exact relaxation identity; local frozen-start and slow-lag approximations tested only at first midpoint, not an interval bound')
    modules(inputs)
    for path, checksum in inputs.items():
        assert digest(path) == checksum
    report['consumed_inputs'] = inputs
    write(DATA / f'relaxation/{model}.json', report)
    print({key: value for key, value in report.items() if key not in ('consumed_inputs','prediction')}, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model', choices=['heavy', 'cold'])
    run_relaxation(parser.parse_args().model)

