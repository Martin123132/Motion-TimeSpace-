from observer_common import *


def main():
    modest()
    folder = ROOT / 'results/thermalization-gate'
    folder.mkdir(parents=True, exist_ok=False)
    alpha = 7.2973525643e-3
    emission_integral = 4 * math.pi ** 4 / 15
    prefactor = 4 * alpha * emission_integral / (3 * math.pi)
    inputs, rows, checks = [], [], []
    for model in ['heavy', 'cold']:
        system = MixedSystem(model, 24, 8, 'event8')
        inputs.append(system.geometry.source)
        points = np.linspace(0., system.geometry.thermal.end, 801)
        values = [system.background(point) for point in points]
        rate = np.array([local['opacity'] / local['hubble'] * prefactor * local['theta'] ** 2 for local in values])
        integrated = float(integrate.simpson(rate, x=points))
        frequencies = np.array([.001, .003, .01, .03])
        optical_depth = integrated * (-np.expm1(-frequencies)) / frequencies ** 3
        critical = np.sqrt(prefactor * np.array([values[0]['theta'], values[-1]['theta']]))
        rows.append(dict(model=model, integrated_soft_dc_coefficient=integrated,
                         x=frequencies.tolist(), absorption_optical_depth_estimate=optical_depth.tolist(),
                         critical_frequency_start_end=critical.tolist(), valid_for_observational_claim=False))
        basis = system.basis
        sampled_rate = prefactor * values[0]['theta'] ** 2 * (-np.expm1(-basis.nodes)) / basis.nodes ** 3
        damping = (basis.values.T * (basis.measure * sampled_rate)) @ basis.values
        temperature = basis.temperature
        weak = np.block([[-damping, (damping @ temperature)[:, None]],
                         [(temperature @ damping)[None, :], np.array([[-temperature @ damping @ temperature]])]])
        invariant = np.r_[temperature, 1.]
        charge_error = float(linalg.norm(invariant @ weak) / (linalg.norm(weak) * linalg.norm(invariant)))
        maximum = float(max(linalg.eigvalsh(weak / linalg.norm(weak))))
        chemical = np.r_[basis.chemical, 0.]
        chemical_dissipation = float(chemical @ weak @ chemical)
        checks.extend([
            dict(name=model + ': emission plus gas preserves total energy', passed=charge_error < 1e-12, value=charge_error),
            dict(name=model + ': emission quadratic entropy is non-increasing', passed=maximum < 1e-12, value=maximum),
            dict(name=model + ': chemical null genuinely removed by photon production', passed=chemical_dissipation < 0, value=chemical_dissipation),
            dict(name=model + ': pure temperature remains joint photon-gas equilibrium', passed=float(linalg.norm(weak @ invariant)) < 1e-10 * linalg.norm(weak)),
            dict(name=model + ': low-frequency emission cannot be assumed absent over this epoch', passed=optical_depth[0] > 1)])
        np.savez_compressed(folder / (model + '-emission-template.npz'), weak=weak, damping=damping,
                            photon_temperature=temperature, physical_frequency=basis.nodes,
                            scope_equilibrium_monomode=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        alpha_value=alpha, alpha_source='https://www.physics.nist.gov/cuu/pdf/wallet_2022.pdf',
                        rate_source='https://arxiv.org/html/2602.14963v1', source_equations='43 and84',
                        leading_soft_double_compton_only=True, bremsstrahlung_and_gaunt_corrections_not_included=True,
                        rate_used_at_high_frequencies_only_as_algebraic_template_not_physical_opacity=True,
                        omission_gate='Do not convert the no-emission early spectrum into a sky prediction.',
                        valid_for_observational_claim=False), __file__,
           [ROOT / 'sources/2602.14963v1.html', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
