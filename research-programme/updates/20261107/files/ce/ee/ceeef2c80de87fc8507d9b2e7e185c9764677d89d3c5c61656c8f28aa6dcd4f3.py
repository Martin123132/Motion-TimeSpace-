from stage169_common import *
from tail_common import FreeFree


def gaunt_derivative(table, gamma_squared, frequency):
    coordinate = (np.log10(gamma_squared) - table.gamma_start) / table.step
    lower = int(np.clip(np.floor(coordinate) - 1, 0, table.columns - 4))
    frequency_coordinate = (np.log10(frequency) - table.u_start) / table.step
    frequency_lower = np.clip(np.floor(frequency_coordinate).astype(int) - 1, 0, table.rows - 4)
    value = np.zeros_like(frequency)
    for column in range(4):
        derivative = 0.
        for omitted in range(4):
            if omitted == column:
                continue
            term = 1. / (column - omitted)
            for other in range(4):
                if other not in [column, omitted]:
                    term *= (coordinate - lower - other) / (column - other)
            derivative += term
        derivative *= -1. / (math.log(10.) * table.step)
        for row in range(4):
            weight = np.ones_like(frequency)
            for other in range(4):
                if other != row:
                    weight *= (frequency_coordinate - frequency_lower - other) / (row - other)
            value += derivative * weight * table.values[frequency_lower + row, lower + column]
    return value


def main():
    modest()
    folder = ROOT / "results/rate-derivation"
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, records = [], [], {}
    for model in ["heavy", "cold"]:
        equation = TemperatureEquation(model)
        reader = ShapeReadout(equation.basis, canonical=True)
        frequencies = np.array([.001, .01, .1, 1.])
        free = FreeFree(equation.background, frequencies)
        inputs.extend([*equation.inputs, *free.inputs])
        helium = equation.background.helium_fraction / (1 - equation.background.helium_fraction)
        helium *= equation.background.constants["m_H"] / equation.background.constants["m_He4"]
        for label, coordinate in [("start", equation.begin), ("target", equation.end)]:
            theta = equation.background.at(coordinate)["thermal_parameter"]
            rates = free.br_rates(theta)
            gamma = integrated_dc.ALPHA**2 / (2 * theta)
            gaunt = free.tables[0](gamma, frequencies) + 4 * helium * free.tables[1](4 * gamma, frequencies)
            derivative = gaunt_derivative(free.tables[0], gamma, frequencies) + 4 * helium * gaunt_derivative(free.tables[1], 4 * gamma, frequencies)
            slope = -.5 + derivative / gaunt
            step = 1e-4
            numerical = (np.log(free.br_rates(theta * np.exp(step))) - np.log(free.br_rates(theta * np.exp(-step)))) / (2 * step)
            test(checks, "BR analytic temperature derivative:" + model + ":" + label, float(max(abs(numerical - slope))), 1e-7)
            test(checks, "DC exact theta-squared rate:" + model + ":" + label,
                 float(np.linalg.norm(equation.emission.at(theta * 1.001, "dc") / 1.001**2 - equation.emission.at(theta, "dc")) /
                       np.linalg.norm(equation.emission.at(theta, "dc"))), 1e-10)
            generator, forcing, info = equation.at(coordinate)
            thermal_photon = equation.basis.temperature[:, None]
            thermal = reader.apply(thermal_photon, np.array([equation.basis.energy @ equation.basis.temperature]))
            test(checks, "Resolved thermal change has no residual:" + model + ":" + label,
                 float(weighted(thermal["residual"], reader.measure) / weighted(thermal["potential"], reader.measure)), 1e-10)
            drive = linalg.solve(equation.basis.mass, info["rate"] * info["stiffness"] @ equation.basis.temperature)
            shape = reader.apply(drive[:, None], np.array([equation.basis.energy @ drive]))
            derivative_size = float(weighted(shape["residual"], reader.measure))
            checks.append(dict(name="Same residual does not fix its temperature derivative:" + model + ":" + label,
                               value=derivative_size, passed=bool(derivative_size > 1e-10)))
            records[model + "-" + label] = dict(theta=theta, frequencies=frequencies.tolist(),
                                               br_rates=rates.tolist(), br_log_temperature_slope=slope.tolist(),
                                               residual_drive_from_resolved_temperature=derivative_size)
    write_json(folder / "rates.json", records)
    report = finish(folder, checks, [*inputs, folder / "rates.json"], exact_rates_not_fitted=True,
                    emission_bank_replaced=False, residual_autonomous_scalar_law=False)
    print(json.dumps(dict(count=report["count"], failures=[row for row in checks if not row["passed"]], records=records)), flush=True)


def weighted(values, measure):
    return np.sqrt(np.sum(measure[:, None] * values**2))


if __name__ == "__main__":
    main()
