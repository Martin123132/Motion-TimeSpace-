from common import *
from adjoint import integrate_budget
from adjoint_operator import relative, sup, BRANCHES
import numpy as np
import sympy as sp


def main():
    modest()
    check_parent()
    checks = []
    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
    for manifest in ("frozen-inputs.json", "adjoint-inputs.json"):
        for path, expected in read(ROOT / manifest)["sources"].items():
            check("frozen:" + manifest + ":" + path, digest(path) == expected)
    matrix = sp.Matrix(3, 3, sp.symbols("a0:9"))
    dual = sp.Matrix(sp.symbols("lambda0:3"))
    error = sp.Matrix(sp.symbols("error0:3"))
    residual = sp.Matrix(sp.symbols("residual0:3"))
    identity = ((-matrix.T * dual).dot(error) + dual.dot(matrix * error + residual) - dual.dot(residual)).expand()
    check("exact:adjoint-error-identity", sp.simplify(identity) == 0)
    result = read(ROOT / "adjoint-result.json")
    check("all:adjoint-result", result["passed"] and result["new_backward_solves"] == 8)
    check("scope:terminal-reference-conditioned", result["reference_conditioned_terminal_bound"] and not result["unknown_density_difference_input"] and not result["rigorous_continuum_certificate"])
    for build in read(ROOT / "build-result.json")["reports"]:
        check(build["model"] + ":coefficient-hash", digest(build["packet"]) == build["sha256"])
        next_index = 0
        for chunk in build["chunks"]:
            check(build["model"] + ":chunk-hash:" + str(chunk["start"]), digest(chunk["path"]) == chunk["sha256"])
            check(build["model"] + ":chunk-continuity:" + str(chunk["start"]), chunk["start"] == next_index and chunk["stop"] > chunk["start"])
            next_index = chunk["stop"]
        check(build["model"] + ":coefficient-coverage", next_index == build["nodes"])
        for name, value in build["numerical"].items():
            check(build["model"] + ":native-operator:" + name, np.isfinite(value) and value < GATE, value)
        for name, value in build["algebra"].items():
            check(build["model"] + ":transpose:" + name, np.isfinite(value) and value < ALGEBRA, value)
    for model_result in result["reports"]:
        model = model_result["model"]
        for name, value in model_result["algebra"].items():
            check(model + ":physical-source:" + name, value < ALGEBRA, value)
        for name, value in model_result["numerical"].items():
            check(model + ":reference-coefficient:" + name, value < GATE, value)
        check(model + ":branch-coverage", [row["branch"] for row in model_result["reports"]] == list(BRANCHES))
        reference_path = POISSON / "evolution" / (model + "-gr.npz")
        reference_row = read(POISSON / "evolution" / (model + "-gr-result.json"))
        check(model + ":reference-hash", digest(reference_path) == reference_row["sha256"])
        reference = load(reference_path)
        indices = [reference["value_names"].tolist().index(name) for name in ("D", "delta_c")]
        scales = np.max(abs(reference["values"][:, indices]), axis=0)
        for row in model_result["reports"]:
            prefix = model + ":" + row["branch"]
            frozen = read(ROOT / "adjoints" / (model + "-" + row["branch"] + "-frozen-prediction.json"))
            check(prefix + ":no-target-in-prediction", frozen["no_target_history_input"] and not frozen["numerically_certified_continuum_bound"])
            check(prefix + ":output-scales", np.array_equal(scales, frozen["output_scales"]))
            check(prefix + ":terminal-scope", row["terminal_only"] and not row["continuum_certificate"])
            case_packets = []
            for case in row["cases"]:
                tag = prefix + ":" + case["tag"]
                check(tag + ":receipt", case["status"]["success"] and case["status"]["points"] == len(reference["efold"]))
                check(tag + ":hash", digest(case["packet"]) == case["sha256"])
                packet = load(case["packet"])
                check(tag + ":original-grid", np.array_equal(packet["efold"], reference["efold"]))
                for name, value in packet.items():
                    if value.dtype.kind in "fci":
                        check(tag + ":finite:" + name, np.isfinite(value).all())
                core_size = packet["adjoint_core"].shape[1]
                mismatch = relative(packet["adjoint_core"][-1] - packet["terminal_adjoint"][:core_size], packet["terminal_adjoint"])
                check(tag + ":terminal-condition", mismatch < ALGEBRA, mismatch)
                recomputed = [integrate_budget(packet["efold"], packet["contributions"], stride) for stride in (1, 2)]
                check(tag + ":budget-reproduction", recomputed == case["budgets"])
                physical_budgets = [integrate_budget(packet["efold"], packet["physical_contributions"], stride) for stride in (1, 2)]
                check(tag + ":physical-budget-reproduction", physical_budgets == case["physical_budgets"])
                gain_budgets = [integrate_budget(packet["efold"], packet["gain_channels"], stride) for stride in (1, 2)]
                check(tag + ":gain-budget-reproduction", gain_budgets == case["gain_budgets"])
                gains = np.asarray(gain_budgets[0]["channel_absolute_budgets"])
                source = packet["source_envelopes"]
                envelope = gains[:, 0] * (source[0] + source[1]) + gains[:, 1] * source[2]
                check(tag + ":envelope-reproduction", np.array_equal(envelope, case["envelope_budget"]))
                split_error = relative(packet["physical_contributions"].sum(axis=2) - packet["contributions"].sum(axis=2), packet["contributions"])
                check(tag + ":physical-channel-identity", split_error < ALGEBRA, split_error)
                for budget in recomputed:
                    signed = np.asarray(budget["signed_prediction"])
                    bound = np.asarray(budget["combined_absolute_budget"])
                    channel = np.asarray(budget["channel_absolute_budgets"]).sum(axis=1)
                    check(tag + ":signed-inside-polynomial-bound:" + str(budget["stride"]), np.all(abs(signed) <= bound + 1e-14))
                    check(tag + ":combined-inside-channel-bound:" + str(budget["stride"]), np.all(bound <= channel + 1e-14))
                    check(tag + ":positive-bound:" + str(budget["stride"]), np.all(bound >= 0))
                case_packets.append(packet)
            for name, value in row["refinement"].items():
                check(prefix + ":refinement:" + name, np.isfinite(value) and value < GATE, value)
            target_row = read(POISSON / "evolution" / (model + "-" + row["branch"] + "-result.json"))
            check(prefix + ":target-hash", digest(target_row["packet"]) == row["target_sha256"] == target_row["sha256"])
            target = load(target_row["packet"])
            actual = (target["values"][-1, indices] - reference["values"][-1, indices]) / scales
            check(prefix + ":measured-reproduction", np.array_equal(actual, row["measured"]))
            prediction = np.asarray(row["prediction"])
            budget = np.asarray(row["absolute_budget"])
            for index, name in enumerate(("D", "delta_c")):
                check(prefix + ":prediction:" + name, abs(actual[index] - prediction[index]) < GATE, float(abs(actual[index] - prediction[index])))
                check(prefix + ":numerical-budget-covers:" + name, abs(actual[index]) <= budget[index], float(budget[index] - abs(actual[index])))
            del target, case_packets
        del reference
    check_parent()
    passed = all(item["passed"] for item in checks)
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks,
          analytical_identity="exact linear adjoint error identity and absolute-integral bound",
          numerical_scope="qualified original-grid interpolant and step refinements; not interval certification"))
    print("validation", len(checks), "passed", passed, flush=True)
    for item in checks:
        if not item["passed"]:
            print(item, flush=True)
    require(passed, "inspect validation failure")

if __name__ == "__main__":
    main()

