from common import ROOT, modest, read, write, digest
import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.common import select_initial_step

if __name__ == "__main__":
    modest()
    with np.load(ROOT / "runs/heavy/native-reference.npz") as data:
        initial, normalization = data["initial"], data["normalization"]
        first, last = float(data["times"][0]), float(data["times"][-1])
        mapping, signature = data["mapping"], data["signature"]
    with np.load(ROOT / "runs/heavy/operator-audit.npz") as data:
        matrix = data["matrices"][0]
        linearity = data["linearity"]
    normalized = matrix * normalization[None, :] / normalization[:, None]
    rhs = lambda stamp, value: normalized @ value
    value = initial / normalization
    derivative = rhs(first, value)
    guessed = select_initial_step(rhs, first, value, last, np.inf, derivative, 1, 7, 2e-11, 2e-13)
    spacing = float(np.nextafter(first, np.inf) - first)
    safe_step = min(1e-4, 1e-3 / max(1., float(np.max(np.sum(abs(matrix), axis=1))))))
    reports = []
    for explicit in (None, safe_step):
        solution = solve_ivp(rhs, (first, first + .001), value, method="DOP853", rtol=2e-11, atol=2e-13, first_step=explicit)
        reports.append(dict(first_step=explicit, success=solution.success, message=solution.message, reached=float(solution.t[-1]), evaluations=solution.nfev))
    output = dict(dimension=len(initial), regime=signature.tolist(), selected_nonzero_native=mapping[np.flatnonzero(initial)].tolist(), automatic_first_step=guessed, absolute_time_spacing=spacing, safe_first_step=safe_step, maximum_linearity_error=float(np.max(linearity)), local_constant_operator_trials=reports, evidence_scope="first-point constant-operator diagnostic, not a new full-interval fit or a replacement for the failed native operator trial", source_sha256=digest(__file__))
    write(ROOT / "initial-step-diagnostic.json", output)
    print(output, flush=True)

