from common import *
from quadrature_v2 import integrate_budget
from adjoint_operator import relative, sup, BRANCHES
import ast
import numpy as np


def main():
    modest()
    check_parent()
    checks = []
    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
    for path, expected in read(ROOT / "frozen-inputs.json")["sources"].items():
        check("frozen:" + path, digest(path) == expected)
    for path in ROOT.glob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"))
        check("syntax:" + path.name, True)
    for index, value in enumerate(read(ROOT / "symbolic.json")):
        check("symbolic-source-transform:" + str(index), value == "0")
    for index, row in enumerate(read(ROOT / "quadrature-tests.json")):
        check("polynomial-integral:" + str(index), row["passed"])
    result = read(ROOT / "primitive-result.json")
    check("scope:no-new-solve-or-closure", result["new_ode_solves"] == 0 and not result["slow_adjoint_assumed"] and not result["new_physical_parameters"])
    check("scope:terminal-only", result["terminal_only"] and not result["rigorous_continuum_certificate"])
    parent = read(ADJOINT / "response-v2/adjoint-result.json")
    for model_result in result["reports"]:
        model = model_result["model"]
        for name, value in model_result["numerical"].items():
            check(model + ":derivative:" + name, np.isfinite(value) and value < GATE, value)
        for name, value in model_result["algebra"].items():
            check(model + ":identity:" + name, np.isfinite(value) and value < ALGEBRA, value)
        old_model = next(row for row in parent["reports"] if row["model"] == model)
        check(model + ":branch-coverage", [row["branch"] for row in model_result["branches"]] == list(BRANCHES))
        for branch in model_result["branches"]:
            prefix = model + ":" + branch["branch"]
            old_branch = next(row for row in old_model["reports"] if row["branch"] == branch["branch"])
            check(prefix + ":tail-zero", branch["tail_injection"] == 0)
            check(prefix + ":injection", branch["injection_identity"] < ALGEBRA, branch["injection_identity"])
            check(prefix + ":old-budget", np.array_equal(branch["old_bound"], old_branch["absolute_budget"]))
            for case in branch["cases"]:
                tag = prefix + ":" + case["tag"]
                check(tag + ":packet", digest(case["packet"]) == case["sha256"])
                check(tag + ":reused-adjoint", digest(case["original_adjoint"]) == case["original_adjoint_sha256"])
                packet = load(case["packet"])
                saved = load(case["original_adjoint"])
                check(tag + ":same-grid", np.array_equal(packet["efold"], saved["efold"]))
                for name, value in packet.items():
                    if value.dtype.kind in "fci":
                        check(tag + ":finite:" + name, np.isfinite(value).all())
                boundary_terms = packet["response"][[0, -1]] * packet["primitive"][[0, -1], None]
                check(tag + ":both-endpoints", np.array_equal(boundary_terms, packet["boundary_terms"]))
                boundary = boundary_terms[1] - boundary_terms[0]
                check(tag + ":boundary", np.array_equal(boundary, case["boundary"]))
                check(tag + ":conservative-boundary", np.all(abs(boundary) <= case["conservative_boundary"]))
                expected_temporal = -packet["response_rate"] * packet["primitive"][:, None]
                check(tag + ":full-response-derivative", np.array_equal(expected_temporal, packet["transformed"][:, :, 2]))
                check(tag + ":untouched-current-shear", np.array_equal(packet["transformed"][:, :, :2], saved["physical_contributions"][:, :, :2]))
                integrals = [integrate_budget(packet["efold"], packet["transformed"], stride) for stride in (1, 2)]
                check(tag + ":integral-reproduction", integrals == case["integrals"])
                prediction = boundary + np.array(integrals[0]["signed_prediction"])
                bound = abs(boundary) + np.array(integrals[0]["combined_absolute_budget"])
                check(tag + ":prediction-reproduction", np.array_equal(prediction, case["prediction"]))
                check(tag + ":bound-reproduction", np.array_equal(bound, case["bound"]))
                check(tag + ":prediction-inside-bound", np.all(abs(prediction) <= bound + 1e-14))
                check(tag + ":reconstruction", case["replay_error"] < GATE, case["replay_error"])
                for name in ("quadrature_signed", "quadrature_budget"):
                    check(tag + ":" + name, case[name] < GATE, case[name])
            measured = np.array(old_branch["measured"])
            check(prefix + ":measured-unchanged", np.array_equal(measured, branch["measured"]))
            check(prefix + ":prediction-accuracy", sup(np.array(branch["prediction"]) - measured) < GATE, sup(np.array(branch["prediction"]) - measured))
            old_bound, new_bound = np.array(branch["old_bound"]), np.array(branch["transformed_bound"])
            check(prefix + ":both-bounds-cover", np.all(abs(measured) <= old_bound) and np.all(abs(measured) <= new_bound))
            check(prefix + ":predeclared-minimum", np.array_equal(np.minimum(old_bound, new_bound), branch["selected_bound"]))
            check(prefix + ":honest-improvement-factor", np.array_equal(old_bound / new_bound, branch["improvement_factor"]))
            for name, value in branch["step_refinement"].items():
                check(prefix + ":step:" + name, value < GATE, value)
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks,
          scope="exact primitive identity with qualified native/carrier derivatives and reused coupled adjoints; numerical terminal budgets"))
    print("validation", len(checks), "passed", passed, flush=True)
    for row in checks:
        if not row["passed"]:
            print(row, flush=True)
    require(passed, "inspect primitive validation")

if __name__ == "__main__":
    main()

