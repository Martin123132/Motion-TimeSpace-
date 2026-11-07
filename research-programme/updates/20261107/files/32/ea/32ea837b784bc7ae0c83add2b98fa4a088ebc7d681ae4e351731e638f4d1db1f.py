from common import *
from rest_operator_v2 import JFULL, norm, sup
from coefficients import metric_polynomial
from mean_math import *
import numpy as np


def main():
    modest()
    check_parent()
    forward = read(ROOT / "forward-result.json")
    require(forward["state"] == "complete", "forward completion")
    mean_packet = load(ROOT / "forward/heavy-mean.npz")
    full_packet = load(ROOT / "forward/heavy-full.npz")
    operators = load(TIMECHAIN / "operators/balanced.npz")
    candidate = load(ROOT / "heavy-balanced-coefficients.npz")
    require(np.array_equal(mean_packet["efold"], operators["efold"]), "same physical grid")
    units = operators["balance"]
    matrix = operators["transform"] * units[:, :, None] / units[:, None, :]
    rate = operators["rate"] * units[:, :, None] / units[:, None, :]
    hessian = operators["hessian"]
    state, normal = mean_packet["canonical_state"], mean_packet["evolved_state"][:, :8]
    scale_value, hubble, terms = mean_packet["a"], mean_packet["H"], mean_packet["terms"]
    source = np.zeros_like(state)
    source[:, 4] = -scale_value**2 / hubble * (terms[:, :5, 2].sum(axis=1) / 2 - mean_packet["observer"][:, 4] / 3)
    source[:, 6] = 2 * scale_value**2 / hubble * mean_packet["observer"][:, 4]
    new_hessian = transpose(matrix) @ hessian @ matrix + transpose(matrix) @ JFULL @ rate
    action_part = multiply(matrix @ JFULL, multiply(candidate["hessian"] - new_hessian, normal))
    source_part = multiply(matrix @ JFULL, multiply(candidate["source"] - transpose(matrix), source))
    parent_rate = multiply(JFULL, multiply(hessian, state) + source)
    measured = mean_packet["canonical_state_rate"] - parent_rate
    total = action_part + source_part
    rate_scale = np.maximum(np.maximum(np.max(abs(parent_rate), axis=0), np.max(abs(mean_packet["canonical_state_rate"]), axis=0)), 1e-80)
    checks = dict(full_rate_split=float(np.max(np.max(abs(measured - total), axis=0) / rate_scale)))
    wave = float(candidate["wave"])
    momentum = hubble * mean_packet["canonical_state_rate"][:, 6] - terms[:, :, 1].sum(axis=1) / (2 * wave)
    residual = hubble * parent_rate[:, 6] - terms[:, :, 1].sum(axis=1) / (2 * wave)
    momentum_scale = max(norm(hubble * mean_packet["canonical_state_rate"][:, 6]), norm(terms[:, :, 1].sum(axis=1) / (2 * wave)))
    checks["momentum_split"] = sup(momentum - hubble * total[:, 6] - residual) / momentum_scale
    peak = int(np.argmax(abs(momentum)))
    report = dict(peak_index=peak, peak_efold=float(mean_packet["efold"][peak]),
                  measured_momentum_residual=sup(momentum) / momentum_scale,
                  action_part=sup(hubble * action_part[:, 6]) / momentum_scale,
                  source_part=sup(hubble * source_part[:, 6]) / momentum_scale,
                  inherited_canonical_part=sup(residual) / momentum_scale,
                  signed_parts_at_peak=(np.array([momentum[peak], hubble[peak] * action_part[peak, 6],
                                                   hubble[peak] * source_part[peak, 6], residual[peak]]) / momentum_scale).tolist(),
                  diagnostic_not_a_repaired_trajectory=True)
    provider = Background("heavy")
    indices = np.unique(np.linspace(0, len(provider.efold) - 1, 65, dtype=int))
    original, mean, cosine, sine = phase_background(provider, provider.efold[indices])
    hessian_poly, exponent, exponent_rate, balancing = polynomials(mean, cosine, sine, wave)
    order = action_orders(hessian_poly, exponent, exponent_rate)[2]
    feedback_poly = product(metric_polynomial(mean, wave, balancing), order["coordinate_map"])
    primitives = []
    bounds = {}
    for name, polynomial, left_j in (("core", order["hessian"], True), ("source", order["source_map"], True), ("feedback", feedback_poly, False)):
        oscillating = {key: JFULL @ value if left_j else value for key, value in polynomial.items() if key != 0}
        primitive = {key: value / (1j * key * mean["mu"][:, None, None]) for key, value in oscillating.items()}
        derivative = {key: 1j * key * mean["mu"][:, None, None] * value for key, value in primitive.items()}
        checks[name + "_primitive_identity"] = max(sup(derivative[key] - value) for key, value in oscillating.items()) / max(max(norm(value) for value in oscillating.values()), 1e-80)
        bound = sum(np.linalg.norm(value, axis=(-2, -1)) for value in primitive.values())
        bounds[name] = float(np.max(bound))
        primitives.append((name, evaluate(primitive, original["phase"]).real))
    np.savez_compressed(ROOT / "projection-diagnostic.npz", efold=mean_packet["efold"], action_part=action_part,
                        source_part=source_part, measured_rate_difference=measured, momentum=momentum, canonical_residual=residual)
    np.savez_compressed(ROOT / "next-coupled-corrector-native-phase.npz", efold=provider.efold[indices], indices=indices,
                        balance=balancing, **dict(primitives))
    passed = all(np.isfinite(value) and 0 <= value < ALGEBRA for value in checks.values())
    write(ROOT / "projection-diagnostic.json", dict(passed=passed, checks=checks, momentum=report, primitive_coefficient_norms=bounds,
          diagnosis="omitted phase-dependent coupled operator, not a failed native baseline or changed pressure law",
          corrective_rates_overwritten=False, new_trajectory_claimed=False,
          next_corrector="For full coupled M(theta), U_n=M_n/(i*n*mu), n!=0. Use X=(I+U)V; derive the FULL U_N and transformed rest/source equations before a prospective rerun.",
          source_hashes={str(path): digest(path) for path in (ROOT / "diagnose_projection.py", ROOT / "forward-result.json",
              ROOT / "heavy-balanced-coefficients.npz", ROOT / "forward/heavy-mean.npz", TIMECHAIN / "operators/balanced.npz")}))
    print("Projection diagnosis", passed, checks, report, bounds, flush=True)
    require(passed, "projection identity failed; inspect")


if __name__ == "__main__":
    main()
