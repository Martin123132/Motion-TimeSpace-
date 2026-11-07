from __future__ import annotations

from datetime import datetime, timezone
import json

import mpmath as mp
import psutil

from acquire_source import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    mp.mp.dps = 80
    rows = []
    inputs = {}
    for label in ['coarse', 'fine']:
        path = ROOT/f'results/current/{label}/status.json'
        inputs[str(path)] = digest(path)
        report = json.loads(path.read_text(encoding='utf-8'))
        for wave in report['all_wave_rows']:
            boundary = {key: mp.mpf(str(value)) for key, value in wave['surface_data'].items()}
            source = {key: mp.mpf(str(value)) for key, value in wave['source_data'].items()}
            frequency = mp.mpf(str(wave['Omega']))
            inside_slope = boundary['body_slope']
            horizon_slope = mp.mpc(boundary['horizon_slope_real'], boundary['horizon_slope_imag'])
            outgoing_slope = mp.mpc(boundary['outgoing_slope_real'], boundary['outgoing_slope_imag'])
            real_outgoing = (source['real_outgoing_value'], source['real_outgoing_slope'])
            quadrature = (source['dirichlet_value'], source['dirichlet_slope'])
            outgoing = tuple(real_outgoing[index]+mp.j*outgoing_slope.imag*quadrature[index] for index in range(2))
            horizon = tuple(real_outgoing[index]+(horizon_slope-outgoing_slope.real)*quadrature[index] for index in range(2))
            inside = tuple(real_outgoing[index]+(inside_slope-outgoing_slope.real)*quadrature[index] for index in range(2))

            def overlap(state):
                return source['K']*state[0]-source['J']*state[1]

            body_out = overlap(inside)/(outgoing_slope-inside_slope)
            reference_out = overlap(horizon)/(outgoing_slope-horizon_slope)
            body_in = overlap(outgoing)/(outgoing_slope-inside_slope)
            reference_in = overlap(outgoing)/(outgoing_slope-horizon_slope)
            difference = body_out-reference_out
            action = -3/(8*mp.pi)*difference*overlap(outgoing)
            power_factor = 3*frequency/(4*mp.pi)
            power_difference = power_factor*outgoing_slope.imag*(abs(body_out)**2-abs(reference_out)**2)
            horizon_power = -power_factor*horizon_slope.imag*abs(reference_in)**2
            optical = 2*frequency*action.imag
            scale = abs(power_difference)+horizon_power
            jump_errors = []
            for outside, inner, inner_state in [(body_out, body_in, inside), (reference_out, reference_in, horizon)]:
                for index, expected in enumerate([source['J'], source['K']]):
                    jump_errors.append(abs((outside*outgoing[index]-inner*inner_state[index])/expected-1))
            stored_real = mp.mpf(str(wave['action_real_per_mu_squared']))
            stored_imag = mp.mpf(str(wave['action_imag_per_mu_squared']))
            expected_power = mp.mpf(str(wave['infinity_power_difference_per_mu_squared']))
            row = {'label': label, 'D_over_R': wave['separation_over_radius'],
                   'real_action_replay_relative_error': float(abs(action.real/stored_real-1)),
                   'imag_action_replay_relative_error': float(abs(action.imag/stored_imag-1)),
                   'infinity_power_replay_error_over_component_sum': float(abs(power_difference-expected_power)/scale),
                   'optical_replay_error_over_component_sum': float(abs(optical-power_difference+horizon_power)/scale),
                   'maximum_reconstructed_jump_error': float(max(jump_errors))}
            assert row['real_action_replay_relative_error'] < 2e-12, row
            assert row['imag_action_replay_relative_error'] < 2e-10, row
            assert row['infinity_power_replay_error_over_component_sum'] < 2e-10, row
            assert row['optical_replay_error_over_component_sum'] < 2e-10, row
            assert row['maximum_reconstructed_jump_error'] < 2e-9, row
            rows.append(row)
    output = ROOT/'results/replay'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': inputs,
              'decimal_precision': mp.mp.dps, 'rows': rows,
              'scope': 'High-precision algebra replay of binary64 wave solutions, not 80-digit ODE accuracy.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'wave_rows_replayed': len(rows),
                      'maximum_jump_error': max(row['maximum_reconstructed_jump_error'] for row in rows),
                      'maximum_optical_replay_error': max(row['optical_replay_error_over_component_sum'] for row in rows)}))


if __name__ == '__main__':
    main()
