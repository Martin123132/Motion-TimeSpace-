from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sympy as sym
import psutil


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results" / "soft-identities"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite evidence.")
    OUTPUT.mkdir(parents=True)
    amplitude, chemical = sym.symbols("amplitude chemical", positive=True)
    radial, phase = sym.symbols("radial phase", real=True)
    potential = sym.Function("V")
    modulus = sym.sqrt((amplitude + radial)**2 + phase**2)
    grand = potential(modulus) - chemical**2 * modulus**2 / 2
    origin = {radial: 0, phase: 0}
    checks = []

    def check(name, expression):
        residual = sym.simplify(expression)
        assert residual == 0, (name, residual)
        checks.append({"name": name, "passed": True})

    derivative = lambda radial_order, phase_order: sym.simplify(sym.diff(grand, radial, radial_order, phase, phase_order).subs(origin))
    tadpole = derivative(1, 0)
    stiffness = derivative(2, 0)
    check("global_U1_generator", -phase * sym.diff(grand, radial) + (amplitude + radial) * sym.diff(grand, phase))
    check("Goldstone_tadpole_identity", derivative(0, 2) - tadpole / amplitude)
    check("mixed_cubic_identity", derivative(1, 2) - stiffness / amplitude + tadpole / amplitude**2)
    check("phase_quartic_identity", derivative(0, 4) - 3 * stiffness / amplitude**2 + 3 * tadpole / amplitude**3)
    check("mixed_quartic_identity", derivative(2, 2) - derivative(3, 0) / amplitude + 2 * stiffness / amplitude**2 - 2 * tadpole / amplitude**3)
    ratio, epsilon = sym.symbols("ratio epsilon", positive=True)
    dimensionless_mass = (2 * ratio - sym.Rational(2, 3)) / (1 + ratio)
    cubic_ratio = (6 * ratio - sym.Rational(2, 9)) / (2 * ratio - sym.Rational(2, 3))
    check("C111_over_C122_bounded_form", cubic_ratio - 3 - 8 / (3 * (3 * ratio - 1)))
    check("mixed_cubic_exchange_strength", (dimensionless_mass * chemical * sym.sqrt(epsilon))**2 / (dimensionless_mass * chemical**2) - dimensionless_mass * epsilon)
    check("upper_mass_strength_remainder", 2 - dimensionless_mass - 8 / (3 * (1 + ratio)))
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "checks": checks, "exact_checks": len(checks),
              "stationary_identities": ["Gamma_phi_phi(0)=0 when the tadpole vanishes",
                                       "C122=m_squared/varrho0",
                                       "D2222=3*m_squared/varrho0_squared",
                                       "D1122=(C111-2*C122)/varrho0"],
              "preferred_branch_strength": "2*epsilon/3 < C122_squared/m_squared < 2*epsilon; 3<C111/C122<13/3",
              "loop_scope": "The radial effective-potential identities hold where the symmetry-preserving regulated derivatives exist. Tree checks do not establish finite loop derivatives or an infrared-safe dressed truncation.",
              "parent_sha256": hashlib.sha256((ROOT.parent / "tensor-response-20261003/results/stage-integrity.json").read_bytes()).hexdigest()}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(checks)}))


if __name__ == "__main__":
    main()
