from stage169_common import *


def weighted_norm(values, measure):
    return np.sqrt(np.sum(measure[:, None] * values**2, axis=0))


def compare(reader, prediction, reference):
    predicted = reader.apply(prediction["photon"], prediction["energy"])
    actual = reader.apply(reference["photon"], reference["energy"])
    output = {}
    for label, mask in [("full", np.ones(len(reader.frequency), dtype=bool)),
                        ("low", reader.frequency < 1.),
                        ("core", (reader.frequency >= .001) & (reader.frequency < .01))]:
        for quantity in ["potential", "residual"]:
            denominator = weighted_norm(actual[quantity][mask], reader.measure[mask])
            difference = weighted_norm(predicted[quantity][mask] - actual[quantity][mask], reader.measure[mask])
            output[label + "_" + quantity] = difference / np.maximum(denominator, 1e-300)
    output["mu"] = abs(predicted["amplitudes"][0] - actual["amplitudes"][0]) / np.maximum(abs(actual["amplitudes"][0]), 1e-300)
    output["y"] = abs(predicted["amplitudes"][1] - actual["amplitudes"][1]) / np.maximum(abs(actual["amplitudes"][1]), 1e-300)
    output["gas"] = abs(prediction["gas"] - reference["gas"]) / np.maximum(abs(reference["gas"]), 1e-300)
    return output, predicted, actual


def main():
    modest()
    folder = ROOT / "results/comparison"
    folder.mkdir(parents=True, exist_ok=False)
    frozen = {model: verify_packet(ROOT / "results/frozen" / model) for model in ["heavy", "cold"]}
    assert all(packet["all_checks_passed"] for packet in frozen.values())
    checks, inputs, records = [], [], {}
    for model in ["heavy", "cold"]:
        equation = TemperatureEquation(model)
        reader = ShapeReadout(equation.basis, canonical=True)
        reference, reference_paths = state_at(model, FRACTION_TARGET, equation.basis)
        inputs.extend([*equation.inputs, *reference_paths])
        origin = ROOT / "results/frozen" / model
        inputs.append(origin / "status.json")
        initial = read_npz(origin / "initial.npz")
        endpoint, endpoint_paths = state_at(model, 1., equation.basis)
        endpoint_path = SOURCE166 / "results/comparison" / f"{model}-{ROUTE}-4096-m20.npz"
        endpoint_readout = read_npz(endpoint_path)
        close(checks, "Assembled current MTS final spectrum:" + model,
              reader.values @ endpoint["photon"][:, 1:3], endpoint_readout["potential"][:, 3:5], 1e-10)
        inputs.extend([*endpoint_paths, endpoint_path])
        predictions = {}
        for label in [*map(str, STEP_COUNTS), "constant_control"]:
            path = origin / ("constant-initial-control.npz" if label == "constant_control" else f"prediction-{label}.npz")
            assert digest(path) == frozen[model]["predictions_sha256"][label]
            prediction = read_npz(path)
            predictions[label] = prediction
            result, predicted, actual = compare(reader, prediction, reference)
            records[model + "-" + label] = {key: value.tolist() for key, value in result.items()}
            output_path = folder / f"{model}-{label}.npz"
            np.savez_compressed(output_path, frequency=reader.frequency, measure=reader.measure,
                                predicted_photon=prediction["photon"], actual_photon=reference["photon"],
                                predicted_residual=predicted["residual"], actual_residual=actual["residual"],
                                predicted_amplitudes=predicted["amplitudes"], actual_amplitudes=actual["amplitudes"],
                                predicted_gas=prediction["gas"], actual_gas=reference["gas"])
            inputs.extend([path, output_path])
            if label == str(STEP_COUNTS[-1]):
                for quantity in ["low_residual", "full_potential", "gas", "mu", "y"]:
                    for index, name in enumerate(COLUMNS[:3]):
                        test(checks, "FORECAST:" + model + ":" + quantity + ":" + name, float(result[quantity][index]), .01)
                for quantity in ["photon", "energy", "gas"]:
                    close(checks, "Predicted paired baseline:" + model + ":" + quantity,
                          prediction[quantity][..., 3:5] - prediction[quantity][..., :1],
                          prediction[quantity][..., 1:3], 1e-8)
                    checks.append(dict(name="Exact zero control:" + model + ":" + quantity,
                                       passed=bool(np.count_nonzero(prediction[quantity][..., -1]) == 0)))
        coarse, fine = predictions[str(STEP_COUNTS[0])], predictions[str(STEP_COUNTS[-1])]
        refinement, unused, unused_actual = compare(reader, coarse, fine)
        records[model + "-step_refinement"] = {key: value.tolist() for key, value in refinement.items()}
        for quantity in ["low_residual", "full_potential", "gas", "mu", "y"]:
            for index, name in enumerate(COLUMNS[:3]):
                test(checks, "REFINEMENT:" + model + ":" + quantity + ":" + name, float(refinement[quantity][index]), .01)
        reference_coarse, coarse_paths = state_at(model, FRACTION_TARGET, equation.basis, 2048)
        reference_step, unused, unused_actual = compare(reader, reference_coarse, reference)
        records[model + "-saved_reference_step"] = {key: value.tolist() for key, value in reference_step.items()}
        inputs.extend(coarse_paths)
    summary = dict(records=records, column_order=COLUMNS, start=FRACTION_START, target=FRACTION_TARGET,
                   forecast_passed=all(row["passed"] for row in checks if row["name"].startswith("FORECAST:")),
                   numerical_checks_passed=all(row["passed"] for row in checks if not row["name"].startswith("FORECAST:")),
                   fixed_tolerances=True, conditional_on_saved_source=True,
                   microscopic_source_temperature_law_derived=False, source_curve_changed=False,
                   new_events=0, new_expensive_virtual_integrals=0,
                   target_previously_calculated=True, target_spectrum_not_used_to_predict=True)
    write_json(ROOT / "NUMERICAL-SUMMARY.json", summary)
    report = finish(folder, checks, [*inputs, ROOT / "NUMERICAL-SUMMARY.json"],
                    **{key: value for key, value in summary.items() if key != "records"})
    print(json.dumps(dict(checks=report["count"], failures=[row for row in checks if not row["passed"]],
                          forecast_passed=summary["forecast_passed"],
                          results={key: {name: values[:3] for name, values in record.items()
                                         if name in ["low_residual", "gas", "mu", "y"]}
                                   for key, record in records.items()})), flush=True)


if __name__ == "__main__":
    main()
