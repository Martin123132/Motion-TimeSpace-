from common import *
from native_context import factory
from rest_operator import NativeRest, norm, sup
import numpy as np


def error(left, right, units):
    return sup((left - right) / np.maximum(np.asarray(units), 1e-80))


def main():
    modest()
    check_parent()
    (ROOT / "native-contexts").mkdir(exist_ok=False)
    frozen = {str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")}
    sources = [SECOND / "run_second.py", WAVELENGTH / "build-full-momentum/camb_python.f90",
               POST / "mts-background-operator-bridge-20261107/build/equations.f90",
               WAVELENGTH / "build-full-momentum/native/camb/cambdll.dll"]
    frozen.update({str(path): digest(path) for path in sources})
    write(ROOT / "preflight-inputs.json", dict(sources=frozen, algebra=ALGEBRA, numerical=GATE))
    open_context = factory()
    waves = read(WAVELENGTH / "inventory-config.json")["waves"]
    reports = []
    for model in ("heavy", "cold"):
        for label, wave in waves:
            guard()
            print("Opening", model, label, flush=True)
            context = open_context(model, label, wave)
            system = NativeRest(context, model, wave)
            efolds = system.background["efold"]
            indices = np.unique(np.linspace(0, len(efolds) - 1, 17, dtype=int))
            units = context["normalization"]
            checks = dict(roundtrip=0., geometry_expansion=0., geometry_shear=0., kernel_columns=0.,
                          rest_core_rhs=0., pressure_source=0., zero=0., linearity=0., extended_hierarchy=0.)
            untouched = np.array([index for index in range(system.native_rest_size) if index not in set(system.tail_indices.ravel())])
            extension_units, initial, project, physical_rhs = context["extension"](192, True)
            for index in indices:
                guard()
                efold = float(efolds[index])
                point = context["point"](efold)
                stamp, hubble = point[11:13]
                vector = np.sin(np.arange(1, system.dimension + 1)) * units
                state, rest, observed, terms, meta = system.encode(efold, vector)
                decoded = system.decode(efold, state, rest)
                checks["roundtrip"] = max(checks["roundtrip"], error(decoded, vector, units))
                expansion, shear = system.geometry(efold, state)
                checks["geometry_expansion"] = max(checks["geometry_expansion"], abs(expansion - meta[2]) / max(abs(expansion), abs(meta[2]), 1e-80))
                checks["geometry_shear"] = max(checks["geometry_shear"], abs(shear - observed[5]) / max(abs(shear), abs(observed[5]), 1e-80))
                native = context["original_rhs"](stamp, vector)
                scalar_columns = [system.position(1), system.position(2)] + system.scalar_positions
                for column in scalar_columns:
                    basis = np.zeros(system.dimension)
                    basis[column] = units[column]
                    output = context["observe"](stamp, basis)
                    rate = context["original_rhs"](stamp, basis)
                    native_shear = output[5]
                    native_expansion = native_shear - 1.5 * output[3] / wave**2
                    expected = system.expansion * native_expansion + system.shear * native_shear
                    discrepancy = sup(rate[system.rest_positions] - expected[system.rest_positions]) / max(norm(rate[system.rest_positions]), norm(expected[system.rest_positions]))
                    checks["kernel_columns"] = max(checks["kernel_columns"], discrepancy)
                state_rate, rest_rate = system.full_rhs(efold, state, rest)
                reference = native[system.rest_positions] / hubble
                difference = error(rest_rate[:system.native_rest_size][untouched], reference[untouched], system.rest_units[:system.native_rest_size][untouched])
                checks["rest_core_rhs"] = max(checks["rest_core_rhs"], difference / max(1., sup(reference[untouched] / system.rest_units[untouched])))
                _, linear, source_observed, source_terms = system.source_only(efold, rest)
                pressure_scale = max(norm(terms[:5, 2]), norm(source_terms[:5, 2]))
                checks["pressure_source"] = max(checks["pressure_source"], sup(terms[:5, 2] - source_terms[:5, 2]) / pressure_scale,
                                               abs(source_observed[4] - observed[4]) / max(abs(observed[4]), 1e-80))
                negative_state, negative_rest = system.full_rhs(efold, -state, -rest)
                checks["linearity"] = max(checks["linearity"], sup(negative_state + state_rate), sup(negative_rest + rest_rate))
                zero_state, zero_rest = system.full_rhs(efold, np.zeros(8), np.zeros(system.rest_size))
                checks["zero"] = max(checks["zero"], sup(zero_state), sup(zero_rest))
                extended = np.cos(np.arange(1, len(extension_units) + 1)) * extension_units
                physical = project(extended)
                extended_rate, _ = physical_rhs(efold, extended)
                expected_native_rate = project(extended_rate) / hubble
                state_ext, rest_ext, _, _, _ = system.encode(efold, physical)
                tail = extended[len(context["core"]):].reshape(190, 5)
                rest_ext[system.native_rest_size:] = tail[system.native_order - 2:].ravel()
                _, calculated = system.full_rhs(efold, state_ext, rest_ext)
                expected_rest = np.r_[expected_native_rate[system.rest_positions],
                                      extended_rate[len(context["core"]):].reshape(190, 5)[system.native_order - 2:].ravel() / hubble]
                scaled_error = sup((calculated - expected_rest) / system.rest_units) / max(1., sup(expected_rest / system.rest_units))
                checks["extended_hierarchy"] = max(checks["extended_hierarchy"], scaled_error)
            passed = all(np.isfinite(value) and 0 <= value < ALGEBRA for value in checks.values())
            report = dict(model=model, label=label, wave=wave, passed=bool(passed), checks=checks, probes=len(indices),
                          native_dimension=system.dimension, rest_dimension=system.rest_size, canonical_dimension=len(system.active),
                          native_order=system.native_order, retained_order=192, source_scope="current states only")
            write(ROOT / "native-contexts" / (model + "-" + label) / "feedback-check.json", report)
            reports.append(report)
            print(report, flush=True)
            require(passed, "feedback preflight failed; preserve and inspect")
            del system, context
    check_parent()
    write(ROOT / "preflight-result.json", dict(state="complete", passed=True, reports=reports, compiled_native_code=False, future_sources_used=False))
    print("Native feedback preflight complete", flush=True)


if __name__ == "__main__":
    main()
