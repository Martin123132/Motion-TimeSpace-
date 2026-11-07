from hybrid_reference_common import *
from test_temperature_forecast import weighted_norm, compare
from decimal import Decimal, localcontext


def spectrum_metrics(reader, predicted, actual):
    result = {}
    for label, mask in [("full", np.ones(len(reader.frequency), dtype=bool)),
                        ("low", reader.frequency < 1.),
                        ("core", (reader.frequency >= .001) & (reader.frequency < .01))]:
        for quantity in ["potential", "residual"]:
            result[label + "_" + quantity] = weighted_norm(predicted[quantity][mask] - actual[quantity][mask], reader.measure[mask]) / np.maximum(weighted_norm(actual[quantity][mask], reader.measure[mask]), 1e-300)
    for index, quantity in enumerate(["mu", "y"]):
        result[quantity] = abs(predicted["amplitudes"][index] - actual["amplitudes"][index]) / np.maximum(abs(actual["amplitudes"][index]), 1e-300)
    return result


def paired_error(values):
    maximum = Decimal(0)
    with localcontext() as context:
        context.prec = 80
        for row in np.atleast_2d(values):
            baseline = Decimal.from_float(float(row[0]))
            for value in row[1:3]:
                increment = Decimal.from_float(float(value))
                recovered = (baseline + increment) - baseline
                maximum = max(maximum, abs(recovered - increment) / max(abs(increment), Decimal("1e-300")))
    return float(maximum)


def main():
    modest()
    folder = ROOT / "results/comparison-hybrid"
    folder.mkdir(parents=True, exist_ok=False)
    frozen = {f"{model}-m{match}": verify_packet(ROOT / "results/frozen-hybrid" / f"{model}-m{match}")
              for model in ["heavy", "cold"] for match in [20, 40]}
    assert all(packet["all_checks_passed"] for packet in frozen.values())
    checks, inputs, records = [], [], {}
    for model in ["heavy", "cold"]:
        for match in [20, 40]:
            label = f"{model}-m{match}"
            equation = HybridEquation(model, match)
            reader = ShapeReadout(equation.basis, canonical=True)
            reference, paths = corrected_state_at(model, FRACTION_TARGET, equation.basis, match)
            carrier, carrier_energy, carrier_paths = unresolved_carrier(model, FRACTION_TARGET, match, reader)
            actual = reader.split_values(reader.values @ reference["photon"] + carrier, reference["energy"] + carrier_energy)
            endpoint, endpoint_paths = corrected_state_at(model, 1., equation.basis, match)
            final_carrier, final_energy, final_paths = unresolved_carrier(model, 1., match, reader)
            readout_path = SOURCE166 / "results/comparison" / f"{model}-{ROUTE}-4096-m{match}.npz"
            readout = read_npz(readout_path)
            final = reader.split_values(reader.values @ endpoint["photon"] + final_carrier, endpoint["energy"] + final_energy)
            for quantity in ["potential", "residual"]:
                close(checks, "Full saved hybrid baseline:" + label + ":" + quantity,
                      final[quantity][:, :1], readout[quantity][:, :1], 1e-10)
                close(checks, "Full saved hybrid MTS:" + label + ":" + quantity,
                      final[quantity][:, 1:3], readout[quantity][:, 3:5], 1e-10)
            origin = ROOT / "results/frozen-hybrid" / label
            inputs.extend([*equation.inputs, *paths, *carrier_paths, *endpoint_paths, *final_paths, readout_path, origin / "status.json"])
            predictions = {}
            for count in [*map(str, STEP_COUNTS), "constant_control"]:
                path = origin / ("constant-initial-control.npz" if count == "constant_control" else f"prediction-{count}.npz")
                assert digest(path) == frozen[label]["predictions_sha256"][count]
                predicted_state = read_npz(path)
                predictions[count] = predicted_state
                represented, represented_split, unused = compare(reader, predicted_state, reference)
                predicted = reader.split_values(reader.values @ predicted_state["photon"] + carrier,
                                                predicted_state["energy"] + carrier_energy)
                hybrid = spectrum_metrics(reader, predicted, actual)
                record = dict(represented={key: value.tolist() for key, value in represented.items()},
                              hybrid={key: value.tolist() for key, value in hybrid.items()},
                              actual_amplitudes=actual["amplitudes"][:, :3].tolist(),
                              predicted_amplitudes=predicted["amplitudes"][:, :3].tolist())
                records[label + "-" + count] = record
                output = folder / f"{label}-{count}.npz"
                np.savez_compressed(output, frequency=reader.frequency, measure=reader.measure,
                                    conditional_carrier=carrier, conditional_carrier_energy=carrier_energy,
                                    predicted_potential=predicted["potential"], actual_potential=actual["potential"],
                                    predicted_residual=predicted["residual"], actual_residual=actual["residual"],
                                    represented_predicted_residual=represented_split["residual"],
                                    predicted_amplitudes=predicted["amplitudes"], actual_amplitudes=actual["amplitudes"],
                                    predicted_gas=predicted_state["gas"], actual_gas=reference["gas"])
                inputs.extend([path, output])
                if count == str(STEP_COUNTS[-1]):
                    for scope, result in [("represented", represented), ("hybrid", hybrid)]:
                        for quantity in ["low_residual", "full_potential", "mu", "y"]:
                            for index, name in enumerate(COLUMNS[:3]):
                                test(checks, "FORECAST:" + label + ":" + scope + ":" + quantity + ":" + name, result[quantity][index], .01)
                    for index, name in enumerate(COLUMNS[:3]):
                        test(checks, "FORECAST:" + label + ":gas:" + name, represented["gas"][index], .01)
                    for quantity in ["photon", "energy", "gas"]:
                        test(checks, "80digit paired component arithmetic:" + label + ":" + quantity, paired_error(predicted_state[quantity]), 1e-10)
                    test(checks, "80digit paired hybrid spectrum:" + label, paired_error(predicted["potential"]), 1e-10)
            refinement, unused, unused_actual = compare(reader, predictions[str(STEP_COUNTS[0])], predictions[str(STEP_COUNTS[-1])])
            records[label + "-refinement"] = {key: value.tolist() for key, value in refinement.items()}
            for quantity in ["low_residual", "full_potential", "mu", "y", "gas"]:
                for index, name in enumerate(COLUMNS[:3]):
                    test(checks, "REFINEMENT:" + label + ":" + quantity + ":" + name, refinement[quantity][index], .01)
            record = read_npz(trace_path(model, match))
            inputs.extend([trace_path(model, match), trace_path(model, match).parent / "status.json"])
    summary = dict(records=records, start=FRACTION_START, target=FRACTION_TARGET,
                   column_order=COLUMNS, forecast_passed=all(row["passed"] for row in checks if row["name"].startswith("FORECAST:")),
                   numerical_checks_passed=all(row["passed"] for row in checks if not row["name"].startswith("FORECAST:")),
                   source_curve_changed=False, tolerances_changed=False,
                   unresolved_carrier_forecast=False, conditional_resolved_temperature_forecast=True,
                   independent_microscopic_source_prediction=False,
                   retained_initial_failures=[row for row in verify_packet(ROOT / "results/comparison")["checks"] if not row["passed"]])
    write_json(ROOT / "HYBRID-SUMMARY.json", summary)
    report = finish(folder, checks, [*inputs, ROOT / "HYBRID-SUMMARY.json"], forecast_passed=summary["forecast_passed"],
                    numerical_checks_passed=summary["numerical_checks_passed"],
                    conditioned_carrier_not_predicted=True, legacy_representation_preserved=True)
    print(json.dumps(dict(count=report["count"], failures=[row for row in checks if not row["passed"]],
                          low_errors={label: result["hybrid"]["low_residual"][:3]
                                      for label, result in records.items() if label.endswith("-256")})), flush=True)


if __name__ == "__main__":
    main()
