from common import *
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative
from physical_energy_map import PhysicalEnergyMap
from metric_channels import derive
import numpy as np


def main():
    modest()
    check_parent()
    require(read(ROOT / "result.json")["passed"], "completed channel check")
    (ROOT / "rest-contexts").mkdir(exist_ok=False)
    write(ROOT / "rest-inputs.json", dict(sources=frozen_sources(), numerical=GATE, algebra=ALGEBRA,
                                         note="equation-derived row bounds; sampled qualification, no sampled supremum certificate"))
    reports = []
    for model in ("heavy", "cold"):
        packet_record = read(ROOT / (model + "-channels.json"))["coefficient_input"]
        require(digest(packet_record["path"]) == packet_record["sha256"], "unchanged coefficient packet")
        packet = load(packet_record["path"])
        operator = CompactAdjoint(packet)
        system = open_owned(model, "rest-contexts")
        energy = PhysicalEnergyMap(system)
        errors, checks, rows = {}, [], []
        for index in np.unique(np.linspace(3, len(packet["efold"]) - 5, 49, dtype=int)):
            guard()
            efold = float(packet["efold"][index] + .61 * (packet["efold"][index + 1] - packet["efold"][index]))
            derived = derive(system, energy, efold)
            core = operator.blocks(efold, 0)[0]
            matrix = derived["transform"] @ core @ derived["inverse"] + derived["derivative"]
            metric = np.outer(derived["psi_injection"], derived["psi"]) + np.outer(derived["phi_injection"], derived["phi_rate"])
            free = matrix - metric
            hubble = derived["hubble"]
            point = system.context["point"](efold)
            weights = np.diag(derived["transform"]) / system.units[:energy.size]
            baryon = energy.slot(4)
            pressure = np.zeros(energy.size)
            for column in range(energy.size):
                normalized = np.zeros(len(system.units))
                normalized[:energy.size] = derived["inverse"][:, column]
                raw = system.decode(efold, normalized * system.units)
                observed = system.context["observe"](point[11], system.project(raw))
                pressure[column] = weights[baryon] * system.wave / hubble * observed[18]
            pressure_matrix = np.zeros_like(matrix)
            pressure_matrix[baryon] = pressure
            ufa = np.zeros_like(matrix)
            signature = system.context["signature_values"]
            hubble_slope = system.background_spline(efold, 1)[0] / hubble
            ufa_coefficient = 0.
            if signature[12]:
                quad = energy.slot(int(signature[4]) + 2)
                ufa_coefficient = -4 * weights[quad] * hubble * (hubble_slope - 1) / weights[system.alpha_slot]
                ufa[quad, system.alpha_slot] = ufa_coefficient
            residual = free - pressure_matrix - ufa
            fluid_mu = .5 * (hubble_slope - 2 + np.sqrt((hubble_slope + 1)**2 + 1))
            slow = derived["scalars"][0]
            slow_mu = slow["omega"]**2 / slow["full_frequency"]**2
            base_bound = max(0., fluid_mu, slow_mu)
            rest = energy.rest
            base_rest = residual[np.ix_(rest, rest)]
            actual_base = max(-.5, float(np.linalg.eigvalsh((base_rest + base_rest.T) / 2)[-1]))
            original_rest = matrix[np.ix_(rest, rest)]
            actual_rest = max(-.5, float(np.linalg.eigvalsh((original_rest + original_rest.T) / 2)[-1]))
            scale = max(1., np.linalg.norm(base_rest, ord="fro"))
            error = max(0., actual_base - base_bound) / scale
            errors["pressure_free_log_norm"] = max(errors.get("pressure_free_log_norm", 0.), error)
            free_bound = base_bound + np.linalg.norm(pressure[rest]) + abs(ufa_coefficient) / 2
            metric_rest = np.linalg.norm(derived["psi_injection"][rest]) * np.linalg.norm(derived["psi"][rest])
            metric_rest += np.linalg.norm(derived["phi_injection"][rest]) * np.linalg.norm(derived["phi_rate"][rest])
            rest_bound = free_bound + metric_rest
            checks.append(dict(name="rest-log-norm", passed=bool(actual_rest <= rest_bound + ALGEBRA * scale),
                               actual=actual_rest, bound=rest_bound, efold=efold))
            if model == "heavy":
                heavy = energy.heavy
                scalar = derived["scalars"][1]
                omega_ratio = scalar["omega"]**2 / scalar["full_frequency"]**2
                rescaling = system.wave / scalar["full_frequency"]
                diagonal_bound = np.linalg.norm(derived["psi_injection"][heavy]) * np.linalg.norm(derived["psi"][heavy])
                diagonal_bound += np.linalg.norm(derived["phi_injection"][heavy]) * np.linalg.norm(derived["phi_rate"][heavy])
                to_heavy = np.linalg.norm(derived["psi_injection"][heavy]) * np.linalg.norm(derived["psi"][rest])
                to_heavy += np.linalg.norm(derived["phi_injection"][heavy]) * np.linalg.norm(derived["phi_rate"][rest])
                from_heavy = np.linalg.norm(derived["psi_injection"][rest]) * np.linalg.norm(derived["psi"][heavy])
                from_heavy += np.linalg.norm(derived["phi_injection"][rest]) * np.linalg.norm(derived["phi_rate"][heavy])
                derived_comparison = np.array([[diagonal_bound, rescaling * to_heavy], [from_heavy / rescaling, rest_bound]])
                actual_comparison = energy.comparison(matrix)
                actual_comparison[0, 0] -= omega_ratio
                actual_comparison[0, 1] *= rescaling
                actual_comparison[1, 0] /= rescaling
                excess = float(np.max(actual_comparison - derived_comparison))
                checks.append(dict(name="whole-balanced-comparison", passed=bool(excess <= ALGEBRA * scale), excess=excess, efold=efold))
            else:
                derived_comparison = np.array([[0., 0.], [0., rest_bound]])
                actual_comparison = energy.comparison(matrix)
            rows.append(dict(efold=efold, hubble_log_slope=float(hubble_slope), fluid_log_bound=float(fluid_mu),
                             pressure_norm=float(np.linalg.norm(pressure[rest])), ufa_alpha=float(ufa_coefficient),
                             actual_pressure_free_log_norm=actual_base, pressure_free_bound=base_bound,
                             actual_comparison=actual_comparison.tolist(), derived_comparison=derived_comparison.tolist()))
        passed = max(errors.values()) < GATE and all(check["passed"] for check in checks)
        report = dict(model=model, passed=passed, errors=errors, checks=checks, rows=rows, sampled_qualification_only=True)
        write(ROOT / (model + "-rest-bound.json"), report)
        print(LABEL, model, "explicit rest/scalar bounds", passed, errors, "checks", len(checks), flush=True)
        require(passed, "preserve free-rest discrepancy")
        reports.append(report)
        del system, energy, operator, packet
    for path, expected in read(ROOT / "rest-inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen auxiliary source")
    check_parent()
    write(ROOT / "rest-result.json", dict(passed=True, reports=reports))


if __name__ == "__main__":
    main()
