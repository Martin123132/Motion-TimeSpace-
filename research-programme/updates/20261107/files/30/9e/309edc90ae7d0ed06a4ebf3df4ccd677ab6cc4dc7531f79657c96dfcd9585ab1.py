from common import *
from evolve import NAMES, BRANCHES, identity, relative, compare
from forward import retained_observables
import numpy as np

def main():
    modest()
    check_parent()
    result = read(ROOT / "evolution-result.json")
    require(result["passed"], "completed independent evolution")
    checks = []
    def check(name, condition, detail=None):
        checks.append(dict(name=name, passed=bool(condition), detail=detail))
    for path, expected in read(ROOT / "evolution-inputs.json")["sources"].items():
        check("frozen:" + path, digest(path) == expected)
    for report in read(ROOT / "preflight-v2/preflight-result.json")["reports"]:
        check(report["model"] + ":preflight", report["passed"])
        for name, value in report["numerical"].items():
            check(report["model"] + ":preflight:" + name, np.isfinite(value) and value < GATE, value)
        for name, value in report["algebra"].items():
            check(report["model"] + ":preflight:" + name, np.isfinite(value) and value < ALGEBRA, value)
    for name, value in read(ROOT / "preflight-v2/symbolic-identities.json").items():
        check("symbolic:" + name, value == "0")
    physical, errors = retained_observables()
    for model in ("heavy", "cold"):
        model_result = read(ROOT / "evolution" / (model + "-result.json"))
        check(model + ":branch-coverage", [row["branch"] for row in model_result["rows"]] == list(BRANCHES))
        control = load(ROOT / "evolution" / (model + "-gr.npz"))
        for row in model_result["rows"]:
            prefix = model + ":" + row["branch"]
            packet = load(row["packet"])
            wave = float(packet["wave"])
            check(prefix + ":hash", digest(row["packet"]) == row["sha256"])
            check(prefix + ":success", row["status"]["success"] and row["status"]["points"] == len(packet["efold"]))
            check(prefix + ":original-grid", np.array_equal(packet["efold"], control["efold"]) and np.array_equal(packet["times"], control["times"]))
            check(prefix + ":names", tuple(packet["value_names"].tolist()) == NAMES)
            for name, array in packet.items():
                if array.dtype.kind in "fci":
                    check(prefix + ":finite:" + name, np.isfinite(array).all())
            values = {name: packet["values"][:, index] for index, name in enumerate(NAMES)}
            rates, diagnostics, terms = packet["rates"], packet["diagnostics"], packet["terms"]
            hubble, enthalpy, alpha = diagnostics[:, 0], diagnostics[:, 2], diagnostics[:, 6]
            expressions = dict(density_projection=identity(values["D"], -terms[:, :, 0].sum(axis=1), 3 * hubble * enthalpy * alpha),
                               current_projection=identity(values["Q"], -terms[:, :, 1].sum(axis=1), -enthalpy * wave * alpha),
                               velocity_projection=identity(values["theta_c"], -wave**2 * alpha),
                               continuity=identity(rates[:, 1], values["theta_c"], -3 * rates[:, 4]),
                               euler=identity(rates[:, 2], hubble * values["theta_c"], -wave**2 * values["Psi"]))
            if row["branch"] == "gr":
                expressions["Hamiltonian"] = identity(2 * wave**2 * values["Phi"], values["D"], 3 * hubble * values["Q"] / wave)
                expressions["slip"] = identity(values["Phi"], -values["Psi"], -values["Pi"] / wave**2)
                momentum = identity(rates[:, 4], hubble * values["Psi"], -values["Q"] / (2 * wave))
                check(prefix + ":actual-momentum", momentum < GATE, momentum)
                check(prefix + ":control-hash", digest(row["control"]["path"]) == row["control"]["sha256"])
                old = load(row["control"]["path"])
                expected = physical(old, wave)
                state_error = float(np.max(errors(packet["projected_state"], old["projected_state"])))
                check(prefix + ":independent-state-reproduction", state_error < GATE, state_error)
                for name in NAMES:
                    error = relative(values[name] - expected[name], expected[name])
                    check(prefix + ":independent-observable:" + name, error < GATE, error)
            else:
                expressions["Poisson"] = identity(2 * wave**2 * values["Psi"], values["D"])
                if row["branch"] == "newton-dust-force":
                    expressions["dust-continuity"] = identity(rates[:, 1], values["theta_c"])
                    check(prefix + ":spatial-driver-zero", np.count_nonzero(values["Phi"]) == 0 and np.count_nonzero(rates[:, 4]) == 0)
                else:
                    expressions["spatial-driver"] = identity(values["Phi"], -values["Psi"])
                calculated = compare(packet, control, wave)
                check(prefix + ":force-split", calculated["force_decomposition"] < ALGEBRA, calculated["force_decomposition"])
                for name in NAMES:
                    error = calculated["physical_errors"][name]
                    check(prefix + ":reported-difference:" + name, error == row["comparison"]["physical_errors"][name], error)
                for index, integrals in enumerate(calculated["live_evolution_integral_checks"]):
                    for name in ("velocity", "density"):
                        check(prefix + ":integral:" + str(index) + ":" + name, integrals[name] < GATE, integrals[name])
                for name in NAMES:
                    if name not in ("Phi", "Psi"):
                        check(prefix + ":initial-matter:" + name, packet["values"][0, NAMES.index(name)] == control["values"][0, NAMES.index(name)])
            for name, value in expressions.items():
                check(prefix + ":algebra:" + name, value < ALGEBRA, value)
    check_parent()
    passed = all(item["passed"] for item in checks)
    write(ROOT / "evolution-validation.json", dict(passed=passed, count=len(checks), checks=checks,
          scope="numerical implementation and explicit truncation accounting, not a physical small-error assertion"))
    print("validation", len(checks), "passed", passed, flush=True)
    for item in checks:
        if not item["passed"]:
            print(item, flush=True)
    require(passed, "validation failures; preserve and inspect")

if __name__ == "__main__":
    main()
