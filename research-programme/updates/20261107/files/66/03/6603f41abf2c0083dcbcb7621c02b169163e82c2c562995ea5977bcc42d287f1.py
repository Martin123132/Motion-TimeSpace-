from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/algebra"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to replace executed evidence.")
    OUTPUT.mkdir(parents=True)
    checks = []

    def check(name, expression):
        difference = sym.simplify(expression)
        assert difference == 0, (name, difference)
        checks.append({"name": name, "passed": True})

    shifted, mass, chemical, frequency, amplitude, radial_cubic = sym.symbols(
        "shifted mass chemical frequency amplitude radial_cubic", positive=True)
    determinant = shifted * (shifted + mass) + 4 * chemical**2 * frequency**2
    inverse = sym.Matrix([[shifted + mass, -2 * chemical * frequency],
                          [2 * chemical * frequency, shifted]])
    propagator = sym.Matrix([[shifted, 2 * chemical * frequency],
                             [-2 * chemical * frequency, shifted + mass]]) / determinant
    for row in range(2):
        for column in range(2):
            check(f"inverse_{row}_{column}", (inverse * propagator)[row, column] - (1 if row == column else 0))
            check(f"spatial_metric_vertex_{row}_{column}",
                  sym.diff(propagator[row, column], shifted) + (propagator * propagator)[row, column])
    mixed = mass / amplitude
    radial_vertex = sym.diag(radial_cubic, mixed)
    phase_vertex = sym.Matrix([[0, mixed], [mixed, 0]])
    quartic_phase = sym.diag((radial_cubic - 2 * mixed) / amplitude, 3 * mixed / amplitude)
    check("pointwise_one_loop_Goldstone_tadpole_Ward",
          sym.trace(quartic_phase * propagator - propagator * phase_vertex * propagator * phase_vertex)
          - sym.trace(radial_vertex * propagator) / amplitude)

    radius, momentum, angle = sym.symbols("radius momentum angle", real=True)
    legendre = (3 * angle**2 - 1) / 2
    first_shear = radius**2 * legendre
    second_shear = momentum**2 - 2 * momentum * radius * angle + radius**2 * legendre
    direct = momentum * (momentum - radius * angle)
    check("pointwise_spatial_divergence_geometry", second_shear - direct - (first_shear - momentum * radius * angle))
    squared, scale = sym.symbols("squared scale", positive=True)
    check("regulator_metric_factor", sym.diff(squared + squared**3 / scale**4, squared) - (1 + 3 * squared**2 / scale**4))
    check("regulator_preserves_homogeneous_background", (squared**3 / scale**4).subs(squared, 0))

    loop_frequency, external_frequency, first_phase, second_phase, alpha = sym.symbols(
        "loop_frequency external_frequency first_phase second_phase alpha", real=True)
    first_soft = sym.Matrix([[1 / mass - alpha**2 * loop_frequency**2 * first_phase,
                              alpha * loop_frequency * first_phase],
                             [-alpha * loop_frequency * first_phase, first_phase]])
    transfer_frequency = external_frequency - loop_frequency
    second_soft = sym.Matrix([[1 / mass - alpha**2 * transfer_frequency**2 * second_phase,
                               alpha * transfer_frequency * second_phase],
                              [-alpha * transfer_frequency * second_phase, second_phase]])
    vertices = [sym.diag(0, mixed), sym.Matrix([[0, mixed], [mixed, 0]])]
    expected_matrix = sym.Matrix([[1, -alpha * external_frequency],
                                  [alpha * external_frequency, -alpha**2 * external_frequency**2]])
    for left in range(2):
        for right in range(2):
            actual = -sum(vertices[left][first, second] * vertices[right][third, fourth]
                          * first_soft[first, third] * second_soft[second, fourth]
                          for first in range(2) for second in range(2)
                          for third in range(2) for fourth in range(2)) / 2
            local_term = -mixed**2 * (first_phase + second_phase) / (2 * mass) if left == 1 and right == 1 else 0
            check(f"leading_nonanalytic_soft_self_energy_{left}_{right}",
                  actual - local_term + mixed**2 * first_phase * second_phase * expected_matrix[left, right] / 2)
    regulator_mass, loop_radius = sym.symbols("regulator_mass loop_radius", positive=True)
    radial_integral = sym.integrate(loop_radius**3 / (loop_radius**2 + regulator_mass)**3, (loop_radius, 0, sym.oo))
    check("four_dimensional_bubble_derivative_radial_integral", radial_integral - 1 / (4 * regulator_mass))
    check("four_dimensional_bubble_log_coefficient", -2 * radial_integral / (8 * sym.pi**2) + 1 / (16 * sym.pi**2 * regulator_mass))
    shift, tadpole = sym.symbols("shift tadpole", real=True)
    check("one_loop_background_shift_cancels_phase_mass", tadpole / amplitude + mixed * (-tadpole / mass))
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "checks": checks, "exact_checks": len(checks),
              "hard_boundary_identity": "p^2 dSigma/dp^2 = I1/2 + I2/2 + B; B=Lambda^3/4 int P2 C G G C",
              "parent_routing_correction": "Ward minus collapsed first rung = (I2-I1)/2 + B",
              "additive_regulator": "r(s)=s^3/Lambda^4 times the identity; source Z(s)=1+3*s^2/Lambda^4",
              "infrared_coefficient": "A_IR=C122^2*c_s/(32*pi^2)",
              "leading_radial_metric_vertex": "dSigma11/dp^2=A_IR/(p^2+xi^2/c_s^2) plus subleading terms",
              "leading_mixed_metric_vertex_ratio": "(dSigma12/dp^2)/(dSigma11/dp^2)=-2*mu*xi/m_squared",
              "scope": "One-loop identities and leading nonanalytic soft term. The soft expansion drops subleading nonanalytic and analytic pieces; it is not the full self energy.",
              "parent_sha256": hashlib.sha256((ROOT.parent / "collective-operator-20261003/results/stage-integrity.json").read_bytes()).hexdigest()}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(checks)}))


if __name__ == "__main__":
    main()
