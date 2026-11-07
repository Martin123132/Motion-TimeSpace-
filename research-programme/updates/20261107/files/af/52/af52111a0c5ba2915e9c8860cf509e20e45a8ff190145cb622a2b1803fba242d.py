from __future__ import annotations

import sys
import time
import traceback

from native_common import *


def main():
    modest()
    started = time.monotonic()
    folder = ROOT / 'runs' / sys.argv[1]
    folder.mkdir(parents=True, exist_ok=False)
    try:
        omega_m, slow_mass = previous.inherited_parameters()
        report = dict(branches=[])
        for fraction in [0., .5]:
            print('Preparing canonical fields, F=', fraction, flush=True)
            species = previous.StandardSpecies(omega_m, fraction)
            target = fraction * omega_m
            dust = lambda efold: (target * np.exp(-3 * np.asarray(efold)), -3 * target * np.exp(-3 * np.asarray(efold)))
            initial, reference, flatness = previous.solve_slow(species, dust, slow_mass)
            if fraction:
                heavy_initial, exact, shooting = previous.exact_heavy(species, target, slow_mass**2 * initial**2)
                bridge = custom_bridge(exact, target, slow_mass**2 * initial**2, species)
                heavy_nodes = np.sort(np.concatenate([exact.t, .75 * exact.t[:-1] + .25 * exact.t[1:],
                    .5 * (exact.t[:-1] + exact.t[1:]), .25 * exact.t[:-1] + .75 * exact.t[1:]]))
                field_h, velocity_h, phase = exact.sol(heavy_nodes)
            else:
                exact = None
                bridge = dust
                shooting = []
                heavy_initial = 0.
            initial, slow, flatness = previous.solve_slow(species, bridge, slow_mass)
            nodes = np.linspace(previous.START, 0., 14001)
            if fraction:
                nodes = np.unique(np.concatenate([nodes, heavy_nodes]))
            scale = np.exp(nodes)
            field_s, velocity_s = slow.sol(nodes)
            rho_h, rho_h_n = bridge(nodes)
            expansion2 = (species.values(nodes)[0] + rho_h + slow_mass**2 * field_s**2) / (1 - velocity_s**2)
            unit = previous.H0 / previous.C_LIGHT
            table = dict(efold=nodes, scale=scale, phi_s=math.sqrt(6) * field_s,
                phidot_s=math.sqrt(6) * scale * unit * np.sqrt(expansion2) * velocity_s,
                expansion2=expansion2, fraction=fraction, slow_mass_mpc=slow_mass * unit,
                heavy_mass_mpc=previous.HEAVY_MASS * unit)
            if fraction:
                table.update(heavy_efold=heavy_nodes, phi_h=math.sqrt(6) * field_h,
                    phidot_h=math.sqrt(6) * np.exp(heavy_nodes) * previous.HEAVY_MASS * unit * velocity_h,
                    phase_h=phase, heavy_logrho_mpc=np.log(3 * unit**2 * rho_h),
                    heavy_w=-1-rho_h_n / (3 * rho_h))
            path = folder / ('heavy.npz' if fraction else 'cold.npz')
            np.savez_compressed(path, **table)
            params = params_for(path)
            native = camb.get_background(params)
            query = np.linspace(previous.START, 0., 2501)
            expected = np.sqrt(np.exp(interpolate.CubicSpline(nodes, np.log(expansion2))(query)))
            actual = native.hubble_parameter(np.exp(-query)-1) / previous.H0
            error = float(np.max(abs(actual / expected - 1)))
            print('Background checked', fraction, 'maximum H relative error', error, flush=True)
            report['branches'].append(dict(fraction=fraction, slow_initial=initial, heavy_initial=heavy_initial,
                shooting=shooting, flatness_error=abs(flatness-1), maximum_native_H_relative_error=error,
                nodes=len(nodes), rdrag_Mpc=native.get_derived_params()['rdrag'], table=str(path)))
        report['elapsed_seconds'] = time.monotonic() - started
        finish(folder, report, __file__, list(folder.glob('*.npz')))
    except BaseException as error:
        write_json(folder / 'status.json', dict(state='failed', error=repr(error), traceback=traceback.format_exc()))
        raise


if __name__ == '__main__':
    main()
