import argparse
from mixed_common import *
from mixed_wave_system import MixedSystem


def main(arguments):
    modest()
    folder = ROOT / 'backgrounds' / arguments.model
    folder.mkdir(parents=True, exist_ok=False)
    system = MixedSystem(arguments.model, 24, 8, 'event8')
    count, heat = system.count, system.background(0.)['heat']
    step = system.geometry.thermal.end / arguments.steps
    state = np.zeros(count + 2)
    previous = state.copy()
    moments, histories, residuals, charges = [], [], [], []
    for index in range(arguments.steps + 1):
        expansion = index * step
        if index:
            reduced_mass, reduced_operator, source = system.background_correction_operator(expansion)
            mass = linalg.block_diag(reduced_mass, np.ones((1, 1)))
            operator = np.zeros_like(mass)
            operator[:-1, :-1] = reduced_operator
            operator[-1, -2] = 1.
            forcing = np.r_[source, 0.]
            if index == 1:
                alpha, history = 1 / step, state / step
            else:
                alpha, history = 1.5 / step, (2 * state - .5 * previous) / step
            right = mass @ history + forcing
            new = linalg.solve(alpha * mass - operator, right)
            residuals.append(float(linalg.norm((alpha * mass - operator) @ new - right) / max(linalg.norm(right), 1e-100)))
            previous, state = state, new
        moments.append(expansion)
        histories.append(state.copy())
        charges.append(float(abs(system.basis.energy @ state[:count] + heat * (state[-2] + state[-1]))))
    histories = np.asarray(histories)
    np.savez_compressed(folder / 'history.npz', expansion=moments, profiles=histories[:, :count],
                        temperature=histories[:, -2], temperature_integral=histories[:, -1], heat=heat)
    checks = [dict(name='Forced background solve finite', passed=bool(np.isfinite(histories).all())),
              dict(name='Forced background implicit equation residual', passed=max(residuals) < 1e-9, value=max(residuals)),
              dict(name='Background photon-plus-gas-plus-expansion-work charge',
                   passed=max(charges) < 1e-10, value=max(charges))]
    finish(folder, dict(checks=checks, all_checks_passed=all(row['passed'] for row in checks), count=len(checks),
                        steps=arguments.steps, model=arguments.model, physical_correction_scale='heat^2',
                        exact_charge='E p + chi (t + integral t ds)=0',
                        relaxed_collision_energy='E p_prime = -chi (t+t_prime)',
                        source_only_is_not_the_background_collision_correction=True), __file__,
           [ROOT / 'mixed_wave_system.py', *system.bank.inputs, system.geometry.source])
    print(json.dumps(dict(model=arguments.model, checks=checks)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--steps', type=int, default=3200)
    main(parser.parse_args())
