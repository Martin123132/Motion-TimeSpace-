import argparse
from bose_reaction import *
from reaction_geometry import ReactionGeometry


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [], []
    for model in ['heavy', 'cold']:
        geometry = ReactionGeometry(model, model + '-reaction104-6400')
        inputs.append(geometry.source)
        for expansion in [0., 1., math.log(10)]:
            started = time.perf_counter()
            profile = geometry.profiles(expansion)
            blocks = mixed_blocks(geometry.basis, profile, arguments.total_order, arguments.fraction_order)
            error = linalg.norm(geometry.basis.temperature @ blocks[0]) / max(linalg.norm(blocks[0]), 1e-100)
            checks.append(check(model + ' mixed reaction energy left null s=' + str(expansion), error, 1e-11))
            if expansion == 0.:
                checks.append(check(model + ' mixed reaction vanishes on original Planck state', max(linalg.norm(block) for block in blocks), 1e-20))
            np.savez_compressed(folder / (model + '-' + str(expansion) + '.npz'),
                expansion=expansion, profile=profile, **{'mixed_' + str(degree): block for degree, block in enumerate(blocks)})
            rows.append(dict(model=model, expansion=expansion, elapsed=time.perf_counter() - started))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        total_order=arguments.total_order, fraction_order=arguments.fraction_order, maximum_degree=4,
        scope='Intensity-only resolved Gould Bose Hessian; multiply by chi and the reference scalar DC rate.',
        general_polarized_kernel=False, infrared_cutoff=1e-5, virtual_radiative_corrections_included=False,
        wave_evolution=False), __file__, [*inputs, ROOT / 'bose_reaction.py', ROOT / 'gould_angles.py', ROOT / 'reaction_geometry.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--total-order', type=int, default=300)
    parser.add_argument('--fraction-order', type=int, default=180)
    main(parser.parse_args())
