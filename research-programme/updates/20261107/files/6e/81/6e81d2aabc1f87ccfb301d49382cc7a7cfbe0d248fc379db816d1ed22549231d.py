import os
from common import ROOT, modest, require, write, digest
import sympy as sp


def main():
    modest()
    wave, hubble, mass, background, speed, enthalpy, cold = sp.symbols("k H mu phi v S Rc", nonzero=True, real=True)
    field, momentum, density, theta = sp.symbols("u p dc theta", real=True)
    external_density, external_momentum, shear = sp.symbols("De Qe Pi", real=True)
    state = sp.Matrix([field, momentum, density, theta])
    denominator = 2 * wave**2 + 3 * enthalpy
    row = sp.Matrix([[-(mass**2 * background + 3 * hubble * speed), -speed, -cold, -3 * hubble * cold / wave**2]]) / denominator
    offset = -(external_density + 3 * hubble * external_momentum / wave) / denominator
    phi = (row * state)[0] + offset
    psi = phi - shear / wave**2
    primitive = sp.Matrix([[0, 1, 0, 0], [-wave**2 - mass**2, -2 * hubble, 0, 0], [0, 0, 0, -1], [0, 0, 0, -hubble]])
    coupling = sp.Matrix([4 * speed, 2 * mass**2 * background, 0, wave**2])
    slip = sp.Matrix([-speed / wave**2, mass**2 * background / wave**2, 0, -1])
    matrix = primitive + coupling * row
    forcing = coupling * offset + slip * shear
    rhs = sp.Matrix([momentum + speed * (psi + 3 * phi), -2 * hubble * momentum - (wave**2 + mass**2) * field + mass**2 * background * (3 * phi - psi), -theta, -hubble * theta + wave**2 * psi])
    scalar_density = speed * momentum + 3 * speed**2 * phi + mass**2 * background * field
    scalar_pressure = speed * momentum + 3 * speed**2 * phi - mass**2 * background * field
    scalar_current = wave * speed * field
    total_star = speed * momentum + mass**2 * background * field + cold * density + external_density
    total_current = scalar_current + cold * theta / wave + external_momentum
    checks = {}
    for index, item in enumerate(sp.simplify(rhs - matrix * state - forcing)):
        checks["affine_state_component_" + str(index)] = item
    checks["Hamiltonian"] = sp.simplify(denominator * phi + total_star + 3 * hubble * total_current / wave)
    checks["pressure_from_evolved_state"] = sp.simplify(speed * rhs[0] - speed**2 * psi - mass**2 * background * field - scalar_pressure)
    checks["density_from_evolved_state"] = sp.simplify(speed * rhs[0] - speed**2 * psi + mass**2 * background * field - scalar_density)
    poisson = -total_star / denominator
    poisson_density = total_star + 3 * enthalpy * poisson
    checks["self_consistent_poisson_density"] = sp.simplify(2 * wave**2 * poisson + poisson_density)
    full_matrix, approximate_matrix = sp.MatrixSymbol("A", 4, 4), sp.MatrixSymbol("An", 4, 4)
    exact, approximate = sp.MatrixSymbol("y", 4, 1), sp.MatrixSymbol("yn", 4, 1)
    force, approximate_force = sp.MatrixSymbol("f", 4, 1), sp.MatrixSymbol("fn", 4, 1)
    identity = sp.expand((full_matrix * exact + force - approximate_matrix * approximate - approximate_force) - approximate_matrix * (exact - approximate) - ((full_matrix - approximate_matrix) * exact + force - approximate_force))
    require(identity == sp.ZeroMatrix(4, 1), "Duhamel error equation")
    checks["Duhamel_error_equation"] = sp.Integer(0)
    rows = [dict(name=name, residual=str(sp.simplify(value)), passed=sp.simplify(value) == 0) for name, value in checks.items()]
    output = dict(passed=all(row["passed"] for row in rows), pid=os.getpid(), checks=rows, coupling_row=str(row), matrix=str(matrix), forcing=str(forcing), pressure=str(scalar_pressure), source_sha256=digest(__file__), scope="exact selected-state feedback with prescribed external compensated sources, not a closed all-species hierarchy")
    write(ROOT / "derivation-result.json", output)
    require(output["passed"], "symbolic gate")
    print(dict(passed=True, identities=len(rows)), flush=True)


if __name__ == "__main__":
    main()

