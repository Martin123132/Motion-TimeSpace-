from outer_common import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/multirate-budget'
    folder.mkdir(parents=True, exist_ok=False)
    paths = [ROOT / 'runs' / f's{order}-h3-g2-2-4/source.npz' for order in [3, 4]]
    coarse, fine = [dict(np.load(path)) for path in paths]
    norm = lambda value: dual_norm(value[1:-1], fine['mass'])
    denominator = norm(fine['remainder'])
    pieces = {key: norm(fine[key] - coarse[key]) / denominator for key in ['difference', 'virtual', 'state']}
    triangle = sum(pieces.values())
    joint = sum(fine[key] - coarse[key] for key in pieces)
    coherent = norm(joint) / denominator
    full_change = fine['remainder'] - coarse['remainder']
    control_change = fine['kinematic_remainder'] - coarse['kinematic_remainder']
    reconstruction = float(np.max(abs(full_change - control_change - joint)))
    control_share = norm(control_change) / norm(full_change)
    checks = [
        dict(name='Exact separation of computed control and remaining source changes', value=reconstruction,
            passed=bool(reconstruction < 1e-12 * np.max(abs(fine['remainder'])))),
        dict(name='Triangle inequality for observed expensive-piece differences', passed=bool(np.all(coherent <= triangle * (1 + 1e-12)))),
    ]
    finish(folder, dict(checks=checks, original_remainder_norm=denominator.tolist(),
        component_observed_budget={key: value.tolist() for key, value in pieces.items()},
        triangle_observed_budget=triangle.tolist(), coherent_observed_budget=coherent.tolist(),
        control_change_to_full_change_norm=control_share.tolist(),
        scope='Differences between computed seed3/4 rules, normalized by the still-unresolved seed4 remainder; not continuum error bounds.',
        proposed_estimator='R_mixed=K_fine+D_seed4+V_seed4+S_seed4 with separately evidenced integration errors.',
        mixed_estimator_computed=False, candidate_denominator_must_be_recomputed=True,
        incoming_frequency_gate_closed=False, all_dimension_remainder_gate_closed=False), __file__, paths)
    print(json.dumps(dict(component_max={key:float(value.max()) for key,value in pieces.items()},
        triangle_max=float(triangle.max()), coherent_max=float(coherent.max()),
        control_change_share=control_share.tolist())), flush=True)


if __name__ == '__main__':
    main()
