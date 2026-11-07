from source_tangent import *
from scipy.special import roots_genlaguerre


def main():
    modest()
    folder = ROOT / "results/preparation"
    assert not (folder / "COMPLETE").exists()
    folder.mkdir(parents=True, exist_ok=True)
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SHA
    bundle, theta = context(START)
    background = physics.thermal_wave.thermal.ThermalBackground("heavy")
    selected = []
    for panel, order, lower, upper in [("1-3", 8, 1., 3.), ("3-8", 6, 3., 8.), ("8-20", 7, 8., 20.)]:
        nodes = list(physics.integration_nodes(theta, order))
        frequencies = sorted({node["frequency"] for node in nodes if lower < node["frequency"] < upper})
        frequency = min(frequencies, key=lambda value: abs(value-(lower+upper)/2))
        for node in nodes:
            if node["frequency"] == frequency and node["electron_index"] in [0, 5, 8, 13] and node["cosine"] == 0.:
                selected.append(dict(panel=panel, order=order, node=node, ordinal=len(selected)))
    assert len(selected) == 12
    config = dict(start_fraction=START, target_fraction=TARGET, theta0=theta,
                  delta_log_temperature=-(TARGET-START)*background.end, expansion_span=background.end,
                  offsets=OFFSETS, selected=selected, source_prediction_tolerance=.01,
                  identity_tolerance=1e-10, current_source_curve_changed=False,
                  full_population_integral=False, source_prediction_not_transport=True,
                  native_history_conditioning_explicit=True)
    write_json(ROOT / "configuration.json", config)
    checks = []
    radial, weights = roots_genlaguerre(2, .5)
    def gas_rule(temp):
        gamma = 1+temp*radial
        beta = np.sqrt(temp*radial*(2+temp*radial))/gamma
        raw = weights*gamma*np.sqrt(2+temp*radial)
        return gamma, beta, raw/raw.sum()
    gamma, beta, population = gas_rule(theta)
    rate = theta*radial/gamma + theta*radial/(2*(2+theta*radial))
    weight_derivative = population*(rate-population@rate)
    increment = 1e-4
    unused, beta_plus, weight_plus = gas_rule(theta*math.exp(increment))
    unused, beta_minus, weight_minus = gas_rule(theta*math.exp(-increment))
    check(checks, "Normalized population derivative sums to zero", abs(weight_derivative.sum()), 1e-14)
    check(checks, "Analytic velocity tangent", max(abs((np.log(beta_plus)-np.log(beta_minus))/(2*increment)-1/(gamma*(gamma+1)))), 1e-8)
    check(checks, "Analytic normalized weight tangent", max(abs((weight_plus-weight_minus)/(2*increment)-weight_derivative)), 1e-8)
    np.savez(folder / "basis.npz", mass=bundle.basis.mass, temperature=bundle.basis.temperature,
             energy=bundle.basis.energy, number=bundle.basis.number, mean=bundle.basis.mean, norms=bundle.basis.norms)
    report = finish(folder, checks, [*bundle.inputs, ROOT / "configuration.json", folder / "basis.npz"],
                    target_source_read=False, target_source_evaluated=False, nodes=12)
    print(json.dumps(dict(count=report["count"], passed=report["all_checks_passed"], nodes=12)), flush=True)


if __name__ == "__main__":
    main()
