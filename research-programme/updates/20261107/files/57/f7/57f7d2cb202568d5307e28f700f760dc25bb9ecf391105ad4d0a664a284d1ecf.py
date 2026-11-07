from emitting_geometry import EmittingGeometry
from increment_emitting_geometry import *


def main():
    modest()
    folder = ROOT / 'results/geometry-coordinate-equivalence'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs = [], []
    for model in ['heavy', 'cold']:
        name = model + '-ir96-integrated-6400'
        old = EmittingGeometry(model, name)
        new = IncrementEmittingGeometry(model, name)
        coordinates = np.linspace(.02, old.thermal.end, 301)
        errors = np.zeros(4)
        for expansion in coordinates:
            first, second = old.at(expansion), new.at(expansion)
            old_state, new_state = old.solution.sol(expansion), new.solution.sol(expansion)
            errors = np.maximum(errors, [abs(first['hubble'] / second['hubble'] - 1),
                abs(first['density'] / second['density'] - 1), abs(old_state[-1] / new_state[-1] - 1),
                linalg.norm(old_state[2:4] - new_state[2:4]) / max(linalg.norm(new_state[2:4]), 1e-30)])
        for label, value in zip(['Hubble history', 'stress density', 'proper-time history', 'scalar momenta'], errors):
            checks.append(dict(name=model + ': affine field-coordinate change preserves ' + label, passed=float(value) < 1e-8, value=float(value)))
        inputs.extend([new.source, new.source.parent / 'status.json', new.parent.source])
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        equations_unchanged=True, new_coordinate='field increment from inherited initial field, not a new physical degree of freedom.',
        repair='DOP853 constructs its dense polynomial using total-field differences. Evolving increments keeps those differences representable.'), __file__,
        [ROOT / 'emitting_geometry.py', ROOT / 'increment_emitting_geometry.py', THERMAL_STAGE / 'background_geometry.py', *inputs])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
