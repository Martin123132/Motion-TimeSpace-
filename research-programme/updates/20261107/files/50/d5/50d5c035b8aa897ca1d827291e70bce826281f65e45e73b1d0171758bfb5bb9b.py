from source_tangent import *
from scipy.special import roots_genlaguerre
finite_check = check


def check(rows, name, value, tolerance):
    finite_check(rows, name, float(value), tolerance)


def main():
    modest()
    folder = ROOT / "results/closed-factor-identities"
    assert not (folder / "COMPLETE").exists()
    folder.mkdir(parents=True, exist_ok=True)
    configuration = json.loads((ROOT / "configuration.json").read_text())
    nodes, quadrature = roots_genlaguerre(2, .5)
    checks = []
    with mp.workdps(90):
        theta = mp.mpf(configuration["theta0"])
        radial = list(map(lambda value: mp.mpf(float(value)), nodes))
        weights = list(map(lambda value: mp.mpf(float(value)), quadrature))
        def population(xi):
            value = [weight*(1+mp.exp(xi)*node)*mp.sqrt(2+mp.exp(xi)*node)
                     for node, weight in zip(radial, weights)]
            return [entry/sum(value) for entry in value]
        coordinate = mp.log(theta)
        probability = population(coordinate)
        gamma = [1+theta*node for node in radial]
        score = [theta*node/energy+theta*node/(2*(energy+1)) for node, energy in zip(radial, gamma)]
        score_prime = [theta*node/energy**2+theta*node/(energy+1)**2 for node, energy in zip(radial, gamma)]
        mean = sum(weight*value for weight, value in zip(probability, score))
        mean_prime = sum(weight*value for weight, value in zip(probability, score_prime))
        variance = sum(weight*(value-mean)**2 for weight, value in zip(probability, score))
        first, second = [], []
        for index, (node, energy, weight) in enumerate(zip(radial, gamma, probability)):
            beta = mp.sqrt(theta*node*(2+theta*node))/energy
            tangent = 1/(energy*(energy+1))
            curvature = -theta*node*(2*energy+1)/(energy**2*(energy+1)**2)
            function = lambda xi: mp.sqrt(mp.exp(xi)*node*(2+mp.exp(xi)*node))/(1+mp.exp(xi)*node)
            for order, exact in [(1, beta*tangent), (2, beta*(tangent*tangent+curvature))]:
                direct = mp.diff(function, coordinate, order)
                check(checks, f"Velocity derivative {index}/{order}", abs(direct-exact)/abs(direct), 1e-60)
            first.append(weight*(score[index]-mean))
            second.append(weight*((score[index]-mean)**2+score_prime[index]-mean_prime-variance))
            for order, exact in [(1, first[-1]), (2, second[-1])]:
                direct = mp.diff(lambda xi: population(xi)[index], coordinate, order)
                check(checks, f"Normalized population derivative {index}/{order}", abs(direct-exact)/abs(direct), 1e-60)
        check(checks, "First population derivative sums to zero", abs(sum(first)), 1e-60)
        check(checks, "Second population derivative sums to zero", abs(sum(second)), 1e-60)
        for value in ["0.0001", "0.1", "1", "10"]:
            argument = mp.mpf(value)
            occupation = 1/mp.expm1(argument)
            direct_first = mp.diff(lambda xi: 1/mp.expm1(argument*mp.exp(xi)), mp.mpf(0), 1)
            direct_second = mp.diff(lambda xi: 1/mp.expm1(argument*mp.exp(xi)), mp.mpf(0), 2)
            first = -occupation*(1+occupation)*argument
            second = occupation*(1+occupation)*((1+2*occupation)*argument**2-argument)
            check(checks, f"Bose first derivative {value}", abs(first-direct_first)/abs(direct_first), 1e-60)
            check(checks, f"Bose second derivative {value}", abs(second-direct_second)/abs(direct_second), 1e-60)
    report = finish(folder, checks, [ROOT / "configuration.json", ROOT / "SECOND-DERIVATIVE.md"],
                    target_source_evaluated=False, source_curve_used=False, analytic_factor_check_only=True)
    print(json.dumps(dict(count=report["count"], passed=report["all_checks_passed"])), flush=True)


if __name__ == "__main__":
    main()
