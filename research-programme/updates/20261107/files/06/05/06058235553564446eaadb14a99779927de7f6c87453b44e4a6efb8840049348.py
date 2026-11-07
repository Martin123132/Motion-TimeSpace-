from common241 import *


def run():
    modest()
    protocol()
    assert not (ROOT / 'results/precision-diagnosis.json').exists()
    basis = packet(PORTS / 'frozen/basis.npz')
    moment = repair.SameMassMoment(basis)
    temperature = basis['temperature'][:, None]
    rows = []
    for anchor in ('warm', 'middle', 'cold'):
        matrices = packet(PARENT / 'results' / f'{anchor}-three-hard-angle-sum.npz')
        ports = packet(ROOT / 'results' / f'{anchor}-ports-and-jets.npz')
        contexts = read(PORTS / 'results' / f'{anchor}-contexts.json')
        for state, context in zip(read(ROOT / 'configuration.json')['states'], contexts):
            for order in (4, 6):
                for join in (0, 1):
                    for component in COMPONENTS:
                        key = f'angular{order}:join{join}:{state["model"]}:{state["history"]}:l0:{component}'
                        weak = matrices[key]
                        direct = context['opacity'] * weak[0]
                        weak_moment = context['opacity'] * precise.stable_dot(weak[1:-1].T, temperature, np.zeros_like(temperature))[:, 0]
                        solved = ports[key + ':photon_moment']
                        rows.append(dict(anchor=anchor, key=key, weak_error=relative(weak_moment, direct),
                            solved_error=relative(solved, direct), solve_versus_weak=relative(solved, weak_moment),
                            weak_cancellation=float(np.linalg.norm(context['opacity'] * (abs(temperature[:, 0]) @ abs(weak[1:-1]))) /
                                max(np.linalg.norm(direct), 1e-300))))
    result = dict(stage=241, rows=rows, maximums={name: max(row[name] for row in rows)
        for name in ('weak_error', 'solved_error', 'solve_versus_weak', 'weak_cancellation')},
        worst_weak=sorted(rows, key=lambda row: row['weak_error'], reverse=True)[:8],
        worst_solve=sorted(rows, key=lambda row: row['solve_versus_weak'], reverse=True)[:8],
        mass_condition=float(np.linalg.cond(moment.mass)), script_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/precision-diagnosis.json', result)
    print(json.dumps({key: value for key, value in result.items() if key not in ('rows', 'worst_solve', 'worst_weak')}), flush=True)
    print(json.dumps(dict(worst_weak=result['worst_weak'][:2], worst_solve=result['worst_solve'][:2])), flush=True)


if __name__ == '__main__':
    run()
