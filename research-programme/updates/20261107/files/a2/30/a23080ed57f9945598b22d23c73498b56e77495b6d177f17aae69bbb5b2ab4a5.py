from common import *
from coefficient_loader import coefficients
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative, sup
from physical_energy_map import PhysicalEnergyMap
from primitive_math import MetricPrimitive
from comparison_math import controls, comparison_envelope, propagate, unit_checks, NODES
from scipy.interpolate import make_interp_spline
import numpy as np
import time


def retained_coefficients(model):
    if LABEL == "balanced":
        saved = read(ROOT / (model + "-central-packing.json"))
        require(digest(saved["packet"]) == saved["sha256"], "lossless central cache")
        return load(saved["packet"])
    return coefficients(model)


def main():
    modest()
    check_parent()
    require(read(ROOT / "physical-probe-result.json")["passed"], "qualified physical map")
    destination = ROOT / "bound"
    destination.mkdir(exist_ok=False)
    (ROOT / "bound-contexts").mkdir(exist_ok=False)
    write(destination / "inputs.json", dict(sources=frozen_sources(), numerical=GATE, algebra=ALGEBRA,
          bound_model="quintic transformed core and forcing, skew retained massive tail",
          interval_envelope="degree-five Bernstein control norms; floating point with 64eps Frobenius padding",
          actual_native_continuum_certificate=False, new_physical_ode_solves=0))
    write(destination / "unit-tests.json", unit_checks())
    reports = []
    for model in ("heavy", "cold"):
        guard()
        directory = destination / model
        directory.mkdir(exist_ok=False)
        packet = retained_coefficients(model)
        operator = CompactAdjoint(packet)
        system = open_owned(model, "bound-contexts")
        energy = PhysicalEnergyMap(system)
        reference = load(POISSON / "evolution" / (model + "-gr.npz"))
        physical = load(ADJOINT / "response-v2/adjoints" / (model + "-physical-sources.npz"))
        primitive = MetricPrimitive(system, reference)
        grid = packet["efold"]
        require(np.array_equal(grid, reference["efold"]) and np.array_equal(grid, physical["efold"]), "same original nodes")
        size = operator.size
        structural = np.zeros((size, size), dtype=bool)
        chunks = []
        source_parts = []
        started = time.monotonic()
        for begin in range(0, len(grid), 128):
            guard()
            end = min(begin + 128, len(grid))
            matrices, forcing = [], []
            for index in range(begin, end):
                efold = float(grid[index])
                core, _, _, _, injection, _ = operator.blocks(efold, 0)
                matrix, transform, inverse, conditions = energy.generator(efold, core)
                direction, direction_rate, denominator = primitive.vector(efold, 1.)
                require(np.count_nonzero(direction[energy.quadrupoles]) == 0, "no hidden massive-tail forcing")
                gravity_vector = injection[:, 0] + physical["mixing"][index, 0] * injection[:, 1]
                current_vector = gravity_vector + direction_rate - core @ direction
                source = current_vector * physical["momentum"][index] + gravity_vector * physical["shear"][index]
                transformed_source = transform @ source
                matrices.append(matrix)
                forcing.append(transformed_source)
                if index == 0:
                    initial_vector = transform @ (direction * physical["momentum"][index])
                if index == len(grid) - 1:
                    final_direction, final_inverse = direction, inverse
            dense = np.array(matrices)
            structural |= np.any(dense != 0., axis=0)
            chunk_path = directory / ("nodes-" + str(begin).zfill(5) + ".npz")
            np.savez_compressed(chunk_path, efold=grid[begin:end], matrix=dense, forcing=np.array(forcing))
            chunks.append(dict(path=str(chunk_path), sha256=digest(chunk_path), begin=begin, end=end))
            source_parts.append(np.array(forcing))
            if begin % 2048 == 0:
                print(LABEL, model, "transformed nodes", end, "/", len(grid), "seconds", round(time.monotonic() - started, 1), flush=True)
        rows, columns = np.nonzero(structural)
        packed = np.empty((len(grid), len(rows)))
        forcing = np.concatenate(source_parts)
        for chunk in chunks:
            guard()
            data = load(chunk["path"])
            selected = data["matrix"][:, rows, columns]
            restored = np.zeros_like(data["matrix"])
            restored[:, rows, columns] = selected
            require(np.array_equal(restored, data["matrix"]), "exact transformed core packing")
            packed[chunk["begin"]:chunk["end"]] = selected
        core_curve = make_interp_spline(grid, packed, k=5, axis=0)
        source_curve = make_interp_spline(grid, forcing, k=5, axis=0)
        require(np.all(np.isin(np.unique(core_curve.t), grid)), "each original interval is a single polynomial span")
        reference_curve = make_interp_spline(grid, reference["evolved_state"][:, :size] / system.units[:size], k=5, axis=0)
        errors = dict(native_core=0., native_heavy=0., native_rest=0., native_forcing=0., bernstein_reconstruction=0.)
        for count, index in enumerate(np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))):
            guard()
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            matrix = np.zeros((size, size))
            matrix[rows, columns] = core_curve(efold)
            transform, inverse, derivative, _ = energy.blocks(efold)
            physical_vector = np.sin(np.arange(size) + count + .2)
            original = np.zeros(len(system.units))
            original[:size] = inverse @ physical_vector
            native = system.evaluate(efold, original * system.units, "poisson-spatial")[0][:size] / system.units[:size]
            expected = transform @ native + derivative @ physical_vector
            difference = matrix @ physical_vector - expected
            errors["native_core"] = max(errors["native_core"], relative(difference, expected))
            errors["native_rest"] = max(errors["native_rest"], relative(difference[energy.rest], expected[energy.rest]))
            if len(energy.heavy):
                errors["native_heavy"] = max(errors["native_heavy"], relative(difference[energy.heavy], expected[energy.heavy]))
            original[:] = 0.
            original[:size] = reference_curve(efold)
            reference_value = system.evaluate(efold, original * system.units, "gr")
            info, values = reference_value[3], reference_value[1]
            hubble = info["H"]
            momentum = 3 * hubble * values["Q"] / (2 * system.wave**3)
            shear = values["Pi"] / system.wave**2
            direction, direction_rate, denominator = primitive.vector(efold, 1.)
            gravity = 3 * hubble * info["enthalpy"] / (2 * system.wave**2)
            mixing = -3 * (hubble + gravity) / (system.wave * denominator)
            expansion_direction = direction * system.wave * denominator / (3 * hubble)
            gravity_vector = mixing * expansion_direction
            gravity_vector[system.alpha_slot] += 1 / (hubble * system.units[system.alpha_slot])
            original[:] = 0.
            original[:size] = direction
            native_direction = system.evaluate(efold, original * system.units, "poisson-spatial")[0][:size] / system.units[:size]
            current_vector = gravity_vector + direction_rate - native_direction
            source_expected = transform @ (current_vector * momentum + gravity_vector * shear)
            errors["native_forcing"] = max(errors["native_forcing"], relative(source_curve(efold) - source_expected, source_expected))
        require(max(errors.values()) < GATE, "transformed interpolation/native source gate")
        comparison = np.empty((len(grid) - 1, 2, 2))
        source_bounds = np.empty((len(grid) - 1, 2))
        padding_rows = np.empty(len(grid) - 1)
        for begin in range(0, len(grid) - 1, 32):
            guard()
            end = min(begin + 32, len(grid) - 1)
            left, right = grid[begin:end], grid[begin + 1:end + 1]
            matrix_controls = controls(core_curve, left, right)
            force_controls = controls(source_curve, left, right)
            matrices = np.zeros((end - begin, 6, size, size))
            matrices[..., rows, columns] = matrix_controls
            local, source, padding = comparison_envelope(matrices, force_controls, energy.heavy, energy.rest)
            comparison[begin:end], source_bounds[begin:end], padding_rows[begin:end] = local, source, padding
            if begin % 2048 == 0:
                print(LABEL, model, "interval envelopes", end, "/", len(grid) - 1, flush=True)
            if begin % 512 == 0:
                fraction = .371
                weights = np.array([float(__import__("math").comb(5, degree)) * fraction**degree * (1 - fraction)**(5 - degree) for degree in range(6)])
                actual = np.einsum("j,bjk->bk", weights, matrix_controls)
                expected = core_curve(left + fraction * (right - left))
                errors["bernstein_reconstruction"] = max(errors["bernstein_reconstruction"], relative(actual - expected, expected))
        require(errors["bernstein_reconstruction"] < ALGEBRA, "Bernstein polynomial reconstruction")
        initial = np.array([np.linalg.norm(initial_vector[energy.heavy]) if len(energy.heavy) else 0., np.linalg.norm(initial_vector[energy.rest])])
        final, transition = propagate(grid, comparison, source_bounds, initial)
        half, transition_half = propagate(grid, comparison, source_bounds, initial, subdivide=2)
        coarse, _ = propagate(grid, comparison, source_bounds, initial, group=2)
        integration = max(relative(final - half, final), relative(transition - transition_half, transition))
        require(integration < GATE, "comparison exponential step identity")
        require(np.all(coarse + ALGEBRA * max(sup(coarse), 1e-80) >= final), "coarser enclosing rates must not improve bound")
        parent_model = next(item for item in read(PRIMITIVE / "primitive-result.json")["reports"] if item["model"] == model)
        parent_branch = next(item for item in parent_model["branches"] if item["branch"] == "poisson-spatial")
        parent_case = next(item for item in parent_branch["cases"] if item["tag"] == "half-cap")
        saved_adjoint = load(parent_case["original_adjoint"])
        output_scales = saved_adjoint["output_scales"]
        readout = packet["rows"][-1] / output_scales[:, None]
        transformed_readout = readout @ final_inverse
        readout_norm = np.stack([np.linalg.norm(transformed_readout[:, energy.heavy], axis=1) if len(energy.heavy) else np.zeros(2),
                                 np.linalg.norm(transformed_readout[:, energy.rest], axis=1)], axis=1)
        boundary = abs(readout @ final_direction * physical["momentum"][-1])
        final_bound = readout_norm @ final + boundary
        prediction = dict(model=model, bound=final_bound.tolist(), initial_norm=initial.tolist(), final_norm=final.tolist(),
                          readout_norm=readout_norm.tolist(), terminal_boundary=boundary.tolist(), comparison_transition=transition.tolist(),
                          output_scales=output_scales.tolist(), no_unknown_difference_input=True, no_new_physical_ode=True)
        write(directory / "frozen-bound.json", prediction)
        measured = np.asarray(parent_branch["measured"])
        covers = abs(measured) <= final_bound
        require(np.all(covers), "closed comparison covers independently evolved result")
        path = directory / "interval-envelope.npz"
        np.savez_compressed(path, efold=grid, comparison=comparison, forcing=source_bounds, padding=padding_rows,
                            initial=initial, final=final, transition=transition, readout_norm=readout_norm, terminal_boundary=boundary,
                            readout=readout, rows=rows, columns=columns, core=packed, source=forcing)
        report = dict(model=model, passed=True, prediction=prediction, measured=measured.tolist(), covers=covers.tolist(),
                      coarse_final=coarse.tolist(), integration_error=integration, errors=errors,
                      packet=str(path), sha256=digest(path), chunks=chunks, exact_zero_packing=True,
                      maximum_comparison=np.max(comparison, axis=0).tolist(), seconds=time.monotonic() - started,
                      transformed_interpolant_scope=True, native_continuum_certificate=False)
        write(directory / "result.json", report)
        reports.append(report)
        print(LABEL, model, "closed physical bounds", final_bound.tolist(), "comparison", transition.tolist(), "seconds", round(report["seconds"], 1), flush=True)
        del system, operator, packet, reference, physical, primitive, core_curve, source_curve, reference_curve, packed, forcing
    for path, expected in read(destination / "inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen bound source")
    check_parent()
    write(destination / "result.json", dict(passed=True, reports=reports, new_physical_ode_solves=0))


if __name__ == "__main__":
    main()

