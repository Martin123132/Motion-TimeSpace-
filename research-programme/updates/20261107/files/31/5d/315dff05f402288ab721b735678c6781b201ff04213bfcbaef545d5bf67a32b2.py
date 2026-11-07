import mpmath as mp
import sympy as sp
from scipy import integrate
from radial_nodes import *


def continuous(theta):
    inverse = 1 / theta
    ratio = mp.besselk(1, inverse) / mp.besselk(2, inverse)
    return dict(normalization=mp.exp(inverse) * mp.besselk(2, inverse) / mp.sqrt(theta),
        energy=ratio + 3 * theta, energy_squared=1 + 3 * theta * ratio + 12 * theta**2,
        pressure=theta)


def discrete(theta, order):
    nodes, weights = mp.gauss_quadrature(order, 'glaguerre', alpha=mp.mpf('.5'))
    energies = [1 + theta * node for node in nodes]
    measures = [weight * energy * mp.sqrt(2 + theta * node) for node, weight, energy in zip(nodes, weights, energies)]
    normalization = mp.fsum(measures)
    return dict(normalization=normalization,
        energy=mp.fsum(weight * energy for weight, energy in zip(measures, energies)) / normalization,
        energy_squared=mp.fsum(weight * energy**2 for weight, energy in zip(measures, energies)) / normalization,
        pressure=mp.fsum(weight * theta * node * (2 + theta * node) / (3 * energy)
            for weight, node, energy in zip(measures, nodes, energies)) / normalization)


def main():
    modest()
    folder = ROOT / 'results/radial-proof'
    folder.mkdir(parents=True, exist_ok=False)
    seal_path = PARENT / 'results/stage-integrity.json'
    assert digest(seal_path) == PARENT_SEAL
    seal = json.loads(seal_path.read_text())
    assert seal['state'] == 'complete' and len(seal['file_hashes']) == 27666
    for name, expected in seal['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks = [dict(name='All27666 sealed Stage99 payloads verified unchanged', passed=True)]
    theta = json.loads((PARENT / 'runs/expensive-p3-shard0/status.json').read_text())['configuration']['temperature']
    inherited_proof = json.loads((PARENT / 'results/symmetry/status.json').read_text())
    assert inherited_proof['all_checks_passed'] and seal['scalar_reflection_reduction_derived']
    checks.append(dict(name='Unchanged inherited unitary scalar-reflection argument and tests', passed=True))
    variable, thermal = sp.symbols('variable thermal', positive=True)
    momentum = sp.sqrt(thermal * variable * (2 + thermal * variable))
    jacobian = sp.simplify(momentum**2 * sp.diff(momentum, variable)
        / (thermal**sp.Rational(3, 2) * sp.sqrt(variable) * (1 + thermal * variable) * sp.sqrt(2 + thermal * variable)))
    assert jacobian == 1
    series = sp.series((1 + thermal * variable) * sp.sqrt(1 + thermal * variable / 2), thermal, 0, 5).removeO()
    expected_series = 1 + sp.Rational(5, 4) * thermal * variable + sp.Rational(7, 32) * thermal**2 * variable**2 - sp.Rational(3, 128) * thermal**3 * variable**3 + sp.Rational(11, 2048) * thermal**4 * variable**4
    assert sp.expand(series - expected_series) == 0
    checks.extend([dict(name='Exact radial Jacobian from original number-weighted momentum measure', passed=True),
        dict(name='Exact small-temperature expansion coefficients of relativistic weight', passed=True)])
    polynomial_rows = []
    for order, deficit in [(2, sp.Rational(15, 2)), (3, sp.Rational(315, 4))]:
        polynomial = sp.expand((-1)**order * sp.factorial(order) * sp.assoc_laguerre(order, sp.Rational(1, 2), variable))
        coefficients = sp.Poly(polynomial**2, variable)
        norm = sp.simplify(sum(coefficient * sp.gamma(power[0] + sp.Rational(3, 2)) / sp.gamma(sp.Rational(3, 2))
            for power, coefficient in coefficients.terms()))
        assert norm == deficit
        checks.append(dict(name='Exact first-missed base moment from monic Laguerre norm: radial' + str(order), passed=True))
        polynomial_rows.append(dict(order=order, monic_polynomial=str(polynomial), first_missed_degree=2*order, normalized_deficit=str(deficit)))
    mp.mp.dps = 70
    for order in [2, 3]:
        nodes, weights = mp.gauss_quadrature(order, 'glaguerre', alpha=mp.mpf('.5'))
        maximum = max(abs(mp.fsum(weight * node**degree for node, weight in zip(nodes, weights))
            / mp.gamma(degree + mp.mpf('1.5')) - 1) for degree in range(2 * order))
        checks.append(dict(name='High-precision base polynomial exactness through degree' + str(2*order-1),
            value=float(maximum), passed=maximum < mp.mpf('1e-60')))
    rows = []
    for temperature in [mp.mpf(str(theta)), mp.mpf('0.000001'), mp.mpf('.001'), mp.mpf('.01'), mp.mpf('.1')]:
        exact = continuous(temperature)
        errors = {}
        row = dict(theta=str(temperature), continuous={key:mp.nstr(value, 45) for key, value in exact.items()}, orders={})
        for order in [2, 3]:
            values = discrete(temperature, order)
            relative = {key:values[key] / exact[key] - 1 for key in values}
            errors[order] = relative
            row['orders'][str(order)] = dict(values={key:mp.nstr(value, 45) for key, value in values.items()},
                relative_errors={key:mp.nstr(value, 30) for key, value in relative.items()})
        improvement = all(abs(errors[3][key]) < abs(errors[2][key]) for key in exact)
        checks.append(dict(name='Three radial nodes improve all four conditional moments at theta=' + str(temperature), passed=improvement))
        value = float(temperature)
        numerical, estimate = integrate.quad(lambda argument: math.sqrt(argument) * math.exp(-argument)
            * (1+value*argument) * math.sqrt(2+value*argument), 0., np.inf, epsabs=2e-12, epsrel=2e-12)
        agreement = abs(numerical/float(exact['normalization'])-1)
        checks.append(dict(name='Independent continuous normalization integral vs Bessel identity: theta=' + str(temperature),
            value=agreement, passed=agreement < 1e-11))
        row['independent_normalization_relative_difference'] = agreement
        row['integration_absolute_estimate'] = estimate
        rows.append(row)
    small = mp.mpf('0.000001')
    exact, coarse = continuous(small), discrete(small, 2)
    asymptotic = dict(normalization=(coarse['normalization']/exact['normalization']-1)/small**4,
        energy=(coarse['energy']-exact['energy'])/small**4,
        pressure=(coarse['pressure']/small-1)/small**3)
    predicted = dict(normalization=-mp.mpf(165)/4096, energy=mp.mpf(45)/256, pressure=mp.mpf(5)/128)
    for key in predicted:
        residual = float(abs(asymptotic[key]/predicted[key]-1))
        checks.append(dict(name='Derived radial2 leading asymptotic error coefficient: ' + key, value=residual, passed=residual < 1e-4))
    actual_rows = []
    for order in [2, 3]:
        full, folded = list(electron_nodes(theta, order, False)), list(electron_nodes(theta, order, True))
        nodes, weights = special.roots_genlaguerre(order, .5)
        energies = 1 + theta * nodes
        corrected = weights * energies * np.sqrt(2+theta*nodes)
        normalization = float(corrected.sum())
        corrected /= normalization
        speeds = np.sqrt(theta*nodes*(2+theta*nodes))/energies
        maximum_speed_error, group_weights = 0., []
        for radial_index, speed in enumerate(speeds):
            group = full[24*radial_index:24*(radial_index+1)]
            assert len(group) == 24
            maximum_speed_error = max(maximum_speed_error, max(abs(np.linalg.norm(node['velocity'])-speed) for node in group))
            group_weights.append(sum(node['electron_weight'] for node in group))
        measure_error = max(abs(np.array(group_weights)-corrected))
        full_weight = sum(node['electron_weight'] for node in full)
        folded_weight = sum(node['electron_weight']*node['reflection_multiplicity'] for node in folded)
        checks.append(dict(name='Original gas implementation matches derived normalized radial rule: radial' + str(order),
            speed_error=maximum_speed_error, weight_error=float(measure_error),
            passed=bool(maximum_speed_error < 1e-14 and measure_error < 1e-14
                and abs(full_weight-1) < 2e-14 and abs(folded_weight-1) < 2e-14
                and len(full) == 24*order and len(folded) == 15*order)))
        actual_rows.append(dict(order=order, physical_electrons=len(full), scalar_representatives=len(folded),
            u=nodes.tolist(), speeds=speeds.tolist(), weights=corrected.tolist(), unnormalized_integral=normalization))
    reflection = np.diag([1., 1., -1., 1.])
    geometry_error = 0.
    for node in electron_nodes(theta, 3, True):
        velocity = np.array(node['velocity'])
        left = weak.source.context(theta, .3, velocity, theta)
        right = weak.source.context(theta, .3, velocity*np.array([1.,-1.,1.]), theta)
        geometry_error = max(geometry_error, float(np.max(abs(right['transform']-reflection@left['transform']@reflection))),
            float(np.max(abs(right['bath']-reflection@left['bath']))))
    checks.append(dict(name='All45 new representative contexts preserve the inherited reflection geometry',
        value=geometry_error, passed=geometry_error < 1e-12))
    count = {part:sum(1 for node in physical_nodes(theta, part)) for part in ['expensive','control']}
    assert count == dict(expensive=6300, control=28800)
    checks.append(dict(name='Radial3 production grids have6300 expensive and28800 control representatives', passed=True))
    finish(folder, dict(checks=checks, theta=theta, conditional_equilibrium_measure=True,
        exact_continuous_moments_derived=True, parent_equilibrium_assumption_newly_derived=False,
        polynomial_rows=polynomial_rows, moment_comparisons=rows, actual_gas_rules=actual_rows,
        asymptotic_limit_check={key:mp.nstr(value,30) for key,value in asymptotic.items()},
        production_nodes=count, current_source_computed=False, moment_checks_replace_source_comparison=False,
        scalar_reflection_proof_inherited=True, new_full_reflected_virtual_probe=False,
        rigorous_continuum_error_bound=False), __file__,
        [ROOT/'radial_nodes.py',ROOT/'DERIVATION.md',PARENT/'results/symmetry/status.json',
         PARENT/'runs/expensive-p3-shard0/status.json',BRANCH/'kinetic-gain-loss-20261008/kinetic_common.py'])
    print(json.dumps(dict(count=len(checks),all_passed=all(row['passed'] for row in checks),
        theta=theta,actual_moment_errors=rows[0]['orders'],actual_gas_rules=actual_rows,
        failed=[row for row in checks if not row['passed']])),flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
