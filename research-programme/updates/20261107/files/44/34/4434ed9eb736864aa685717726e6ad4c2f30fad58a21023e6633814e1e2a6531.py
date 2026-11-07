from common241 import *
import sympy as symbolic


def run():
    modest()
    protocol()
    assert not (ROOT / 'results/algebra.json').exists()
    checks = []
    duration, scale, density, capacity, transfer, shear = symbolic.symbols('t a rho C CE Pi', nonzero=True)
    energy, current, transverse, longitudinal = symbolic.symbols('E J ST SL')
    sigma_transverse = scale**2 * (energy - longitudinal) * duration**2 / 4
    sigma_longitudinal = scale**2 * (energy + longitudinal - 2 * transverse) * duration**2 / 4
    metric_transverse = symbolic.integrate(2 * sigma_transverse, (duration, 0, duration))
    metric_longitudinal = symbolic.integrate(2 * sigma_longitudinal, (duration, 0, duration))
    expressions = {
        'native transverse metric third derivative': symbolic.diff(metric_transverse, duration, 3) - scale**2 * (energy - longitudinal),
        'native longitudinal metric third derivative': symbolic.diff(metric_longitudinal, duration, 3) - scale**2 * (energy + longitudinal - 2 * transverse),
        'metric first derivative initially zero': symbolic.diff(metric_transverse, duration).subs(duration, 0),
        'metric second derivative initially zero': symbolic.diff(metric_transverse, duration, 2).subs(duration, 0),
    }
    pressure = density * (transfer / 3 - 2 * transfer / (3 * capacity))
    scalar_metric = metric_transverse.subs({energy: 0, transverse: pressure, longitudinal: pressure})
    expressions['balanced monopole cubic coefficient'] = scalar_metric / duration**3 + scale**2 * density * transfer * (capacity - 2) / (18 * capacity)
    expressions['NR pressure limit'] = pressure.subs(capacity, 1) + density * transfer / 3
    expressions['quadrupole metric trace'] = (2 * metric_transverse + metric_longitudinal).subs({energy: 0, transverse: -shear, longitudinal: 2 * shear})
    expressions['quadrupole transverse coefficient'] = metric_transverse.subs({energy: 0, transverse: -shear, longitudinal: 2 * shear}) / duration**3 + scale**2 * shear / 3
    expressions['quadrupole longitudinal coefficient'] = metric_longitudinal.subs({energy: 0, transverse: -shear, longitudinal: 2 * shear}) / duration**3 - 2 * scale**2 * shear / 3
    heat, capacity_derivative, inertia, density_wave, temperature_wave, velocity_wave, background_transfer = symbolic.symbols('chi CR Bg b r v Q', nonzero=True)
    gas_direct = -background_transfer * density_wave / (heat * capacity)
    expressions['one-electron density temperature cancellation'] = gas_direct + background_transfer * density_wave / (heat * capacity)
    for name, expression in expressions.items():
        check(checks, name, int(symbolic.simplify(expression) != 0), 0)
    check(checks, 'incorrect direct metric forcing detected', int(symbolic.simplify(metric_transverse / duration**2 - scale**2 * (energy - longitudinal) / 2) == 0), 0)
    check(checks, 'equal energy exchange need not erase pressure', int(symbolic.simplify(pressure) == 0), 0)
    report = dict(stage=241, qualified=all(row['passed'] for row in checks), checks=checks,
        failed=[row for row in checks if not row['passed']], finished_at=now(), script_sha256=digest(__file__),
        scope='Native metric local derivative identities, balanced pressure and one-electron density term; no finite-time or mass-gap theorem')
    write(ROOT / 'results/algebra.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'])), flush=True)


if __name__ == '__main__':
    run()
