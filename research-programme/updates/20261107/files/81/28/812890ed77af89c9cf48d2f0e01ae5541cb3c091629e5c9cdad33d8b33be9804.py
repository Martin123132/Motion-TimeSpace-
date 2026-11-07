import argparse
from rectangular_common import *


def dual_norm(vector, mass):
    return np.sqrt(np.maximum(np.sum(vector * linalg.solve(mass, vector, assume_a='pos'), axis=0), 0.))


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--first', required=True)
    parser.add_argument('--second', required=True)
    parser.add_argument('--overlap-first')
    parser.add_argument('--overlap-second')
    arguments = parser.parse_args()
    folder = ROOT / 'comparisons' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    locations = [ROOT / 'runs' / name for name in [arguments.first, arguments.second]]
    packets = [json.loads((path / 'status.json').read_text()) for path in locations]
    assert all(packet['all_checks_passed'] and packet['complete_outer_measure'] for packet in packets)
    arrays = [dict(np.load(path / 'source.npz')) for path in locations]
    mass = arrays[1]['mass']
    change = dual_norm(arrays[0]['total'][1:-1] - arrays[1]['total'][1:-1], mass)
    norms = [dual_norm(saved['total'][1:-1], mass) for saved in arrays]
    relative = change / np.maximum(norms[1], 1e-300)
    energy_difference = abs(arrays[0]['total'][0] - arrays[1]['total'][0])
    number_difference = abs(arrays[0]['number'] - arrays[1]['number'])
    checks = [
        dict(name='Actual96-source-vector refinement within1percent in mass-dual norm', value=float(relative.max()), passed=bool(np.max(relative) < .01)),
        dict(name='Comparison retains all four physical profiles and all96 tests', passed=all(saved['total'][1:-1].shape == (96, 4) for saved in arrays)),
    ]
    report = dict(checks=checks, arguments=vars(arguments), source_norm_before=norms[0].tolist(),
        source_norm_after=norms[1].tolist(), relative_vector_change=relative.tolist(),
        energy_absolute_change=energy_difference.tolist(), number_absolute_change=number_difference.tolist(),
        vector_quadrature_accepted=bool(np.max(relative) < .01),
        source_smallness_used_to_waive_relative_gate=False)
    inputs = [path / filename for path in locations for filename in ['status.json', 'source.npz']]
    if arguments.overlap_first or arguments.overlap_second:
        assert arguments.overlap_first and arguments.overlap_second
        overlap_locations = [ROOT / 'overlaps' / name for name in [arguments.overlap_first, arguments.overlap_second]]
        overlap_arrays = [dict(np.load(path / 'overlap.npz')) for path in overlap_locations]
        overlap_change = dual_norm(overlap_arrays[0]['joined_new_domain'][1:-1] - overlap_arrays[1]['joined_new_domain'][1:-1], mass)
        overlap_norm = dual_norm(overlap_arrays[1]['joined_new_domain'][1:-1], mass)
        relative_overlap = overlap_change / np.maximum(overlap_norm, 1e-300)
        checks.append(dict(name='Same-domain leading overlap quadrature within1percent', value=float(relative_overlap.max()), passed=bool(np.max(relative_overlap) < .01)))
        report['relative_overlap_change'] = relative_overlap.tolist()
        finite = arrays[1]['total'] - overlap_arrays[1]['joined_new_domain']
        replacement = arrays[1]['total'] - overlap_arrays[1]['original_old_overlap']
        domain_state = overlap_arrays[1]['domain_state_increment']
        difference = replacement - finite - domain_state
        scale = max(float(np.max(abs(replacement))), float(np.max(abs(finite))), 1e-300)
        checks.append(dict(name='Source replacement equals finite difference plus tracked domain/state change', value=float(np.max(abs(difference)) / scale), passed=np.max(abs(difference)) < 1e-12 * scale))
        np.savez(folder / 'replacement.npz', full_source=arrays[1]['total'], finite_difference=finite,
            domain_state_increment=domain_state, replacement=replacement, mass=mass,
            temperature=arrays[1]['temperature'], chemical=arrays[1]['chemical'])
        report.update(finite_difference_dual_norm=dual_norm(finite[1:-1], mass).tolist(),
            replacement_dual_norm=dual_norm(replacement[1:-1], mass).tolist(),
            overlap_dual_norm=overlap_norm.tolist(),
            finite_difference_over_leading= (dual_norm(finite[1:-1], mass) / np.maximum(overlap_norm, 1e-300)).tolist(),
            full_parent_feedback_applied=False, companion_tail_sources_required=True)
        inputs += [path / filename for path in overlap_locations for filename in ['status.json', 'overlap.npz']]
    finish(folder, report, __file__, inputs)
    print(json.dumps({key: value for key, value in report.items() if key not in ['input_hashes']}), flush=True)


if __name__ == '__main__':
    main()
