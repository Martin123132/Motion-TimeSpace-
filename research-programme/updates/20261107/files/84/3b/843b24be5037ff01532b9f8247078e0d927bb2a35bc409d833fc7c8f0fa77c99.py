from common import *
from adjoint_operator import sup, relative
import numpy as np
import sympy as sp


def main():
    modest()
    check_parent()
    require(read(ROOT / "validation.json")["passed"], "completed primitive checks")
    density, phi, theta, hubble, wave, cold_density = sp.symbols("density phi theta hubble wave Rc", nonzero=True)
    count = density - 3 * phi
    source = cold_density * density
    constraint = 2 * wave**2 * phi + source
    transformed = (2 * wave**2 + 3 * cold_density) * phi + cold_density * count
    symbolic = dict(volume_constraint=str(sp.simplify(transformed - constraint)))
    denominator = 2 * wave**2 + 3 * cold_density
    coefficient = wave**2 * cold_density / denominator
    newton = cold_density / 2
    epsilon = 3 * cold_density / (2 * wave**2)
    symbolic["coefficient_relative_error"] = str(sp.simplify((newton - coefficient) / newton - epsilon / (1 + epsilon)))
    require(all(value == "0" for value in symbolic.values()), "volume identities")
    write(ROOT / "volume-symbolic.json", symbolic)
    checks = []
    def check(name, value):
        checks.append(dict(name=name, value=float(value), passed=bool(np.isfinite(value) and value < ALGEBRA)))
    write(ROOT / "volume-inputs.json", dict(source=str(Path(__file__)), sha256=digest(__file__),
          algebra=ALGEBRA, no_ode_solve=True, no_new_model=True, dust_subcase_not_assumed_for_MTS_mixture=True))
    summaries = []
    for model in ("heavy", "cold"):
        for branch in ("gr", "poisson-spatial"):
            guard()
            row = read(POISSON / "evolution" / (model + "-" + branch + "-result.json"))
            require(digest(row["packet"]) == row["sha256"], "retained evolution")
            packet = load(row["packet"])
            names = packet["value_names"].tolist()
            values = {name: packet["values"][:, names.index(name)] for name in ("Phi", "Psi", "D", "Q", "Pi", "delta_c", "theta_c")}
            wave_value = float(packet["wave"])
            hubble_value = packet["H"]
            alpha = packet["diagnostics"][:, 6]
            background_density = packet["terms"][:, 0, 5]
            count_density = values["delta_c"] - 3 * values["Phi"]
            cold_source = background_density * values["delta_c"]
            cold_current = background_density * values["theta_c"] / wave_value
            other_source = values["D"] - cold_source
            other_current = values["Q"] - cold_current
            prefix = model + ":" + branch
            check(prefix + ":cold-density-map", relative(cold_source - packet["terms"][:, 0, 0] + 3 * hubble_value * background_density * alpha, cold_source))
            check(prefix + ":cold-current-map", relative(cold_current - packet["terms"][:, 0, 1] - background_density * wave_value * alpha, cold_current))
            count_rate = packet["rates"][:, 1] - 3 * packet["rates"][:, 4]
            check(prefix + ":number-continuity", relative(count_rate + values["theta_c"], values["theta_c"]))
            coefficients = 2 * wave_value**2 + 3 * background_density
            pieces = np.stack([coefficients * values["Phi"], background_density * count_density, other_source])
            if branch == "gr":
                pieces = np.vstack([pieces, 3 * hubble_value * (cold_current + other_current) / wave_value])
                check(prefix + ":slip-dictionary", relative(values["Phi"] - values["Psi"] - values["Pi"] / wave_value**2, values["Phi"]))
            else:
                check(prefix + ":spatial-potential", relative(values["Phi"] - values["Psi"], values["Phi"]))
            check(prefix + ":constraint-dictionary", relative(pieces.sum(axis=0), pieces))
            check(prefix + ":physical-readout-roundtrip", relative(count_density + 3 * values["Phi"] - values["delta_c"], values["delta_c"]))
            path = ROOT / "results" / (model + "-" + branch + "-volume-dictionary.npz")
            np.savez_compressed(path, efold=packet["efold"], delta_count=count_density, delta_physical=values["delta_c"],
                                Phi=values["Phi"], Rc=background_density, D_other=other_source, Q_other=other_current,
                                constraint_pieces=pieces, count_rate=count_rate)
            summaries.append(dict(model=model, branch=branch, packet=str(path), sha256=digest(path), source=row["packet"], source_sha256=row["sha256"],
                                  Rc_positive=bool(np.min(background_density) > 0), other_source_retained=True))
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(ROOT / "volume-result.json", dict(passed=passed, checks=checks, count=len(checks), summaries=summaries,
          new_model_claimed=False, no_new_ode_solve=True, full_mixture_retained=True,
          next_use="physical-density/coordinate-volume dictionary for the Newtonian limit; preserve initial physical preparation"))
    print("volume dictionary", len(checks), "checks passed", passed, flush=True)
    require(passed, "volume dictionary failure")

if __name__ == "__main__":
    main()

