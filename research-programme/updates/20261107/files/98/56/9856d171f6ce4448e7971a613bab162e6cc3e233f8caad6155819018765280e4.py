from azimuth_common import *


def main():
    modest()
    folder = ROOT / 'results/combined-source'
    folder.mkdir(parents=True, exist_ok=False)
    locations = [ROOT / 'runs' / f'{part}-h5-az8' for part in ['expensive', 'control']]
    reports = [json.loads((location / 'status.json').read_text()) for location in locations]
    assert all(report['all_checks_passed'] for report in reports)
    expensive, control = [dict(np.load(location / 'source.npz')) for location in locations]
    reference_path = PARENT / 'results/combined-source/source.npz'
    reference = dict(np.load(reference_path))
    remainder = control['kinematic_remainder'] + sum(expensive[key] for key in ['difference', 'virtual', 'state'])
    complete = reference['accurate_leading'] + remainder
    assert np.array_equal(reference['sampled_leading'], control['sampled_leading'])
    pair = float(np.max(abs(complete[0] + complete[-1])))
    energy = float(np.max(abs(reference['temperature'] @ complete[1:-1] - complete[0])))
    scale = max(float(np.max(abs(complete[0]))), 1e-30)
    checks = [
        dict(name='Whole96-mode four-profile source assembled without omitted terms', passed=bool(np.isfinite(complete).all() and complete.shape == (98, 4))),
        dict(name='Integrated independent photon/gas exchange retained', value=pair, passed=pair < 1e-6 * scale),
        dict(name='Original temperature test matches independent energy row', value=energy, passed=energy < 1e-6 * scale),
    ]
    np.savez(folder / 'source.npz', total=complete, remainder=remainder,
        **{key:expensive[key] for key in ['difference', 'virtual', 'state']},
        **{key:control[key] for key in ['control', 'sampled_leading', 'kinematic_remainder']},
        **{key:reference[key] for key in ['accurate_leading', 'mass', 'temperature', 'chemical']})
    finish(folder, dict(checks=checks, hard_order=5, electron_azimuth=8, electron_count=32, control_incoming_order=128, expensive_incoming_order=4,
        new_parent_history=False, full_parent_feedback_applied=False, source_smallness_used_to_waive_gate=False),
        __file__, [reference_path, *[location / name for location in locations for name in ['source.npz', 'status.json']]])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
