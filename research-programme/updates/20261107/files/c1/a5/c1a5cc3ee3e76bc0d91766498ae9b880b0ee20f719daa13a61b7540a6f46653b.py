from weak_common import *
import mpmath as mp


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/elastic-counting'
    folder.mkdir(parents=True, exist_ok=False)
    temperature = mp.mpf('.00045962015785263325')
    energy = temperature
    hard = energy / (1 + energy * mp.mpf('.9'))
    incoming_frequency, outgoing_frequency = energy / temperature, hard / temperature
    occupation_in = 1 / mp.expm1(incoming_frequency)
    occupation_out = 1 / mp.expm1(outgoing_frequency)
    electron_change = (energy - hard) / temperature
    electron_reverse = mp.exp(-electron_change)
    equilibrium = occupation_in * (1 + occupation_out)
    incoming_phi = mp.mpf('.31')
    outgoing_phi = mp.mpf('-.23')
    electron_phi = mp.mpf('.19')
    final_electron_phi = mp.mpf('.19') + mp.mpf('.7') * electron_change
    departure = outgoing_phi + final_electron_phi - incoming_phi - electron_phi
    test_difference = mp.mpf('.47')
    def net_flux(epsilon, rate_change):
        left = occupation_in + epsilon * occupation_in * (1 + occupation_in) * incoming_phi
        right = occupation_out + epsilon * occupation_out * (1 + occupation_out) * outgoing_phi
        initial_electron = 1 + epsilon * electron_phi
        final_electron = electron_reverse * (1 + epsilon * final_electron_phi)
        rate = 1 + epsilon * rate_change
        return rate * (initial_electron * left * (1 + right)
                       - final_electron * right * (1 + left)) * test_difference
    direct = mp.diff(lambda epsilon: net_flux(epsilon, 0), mp.mpf(0))
    two_orientations = -equilibrium * departure * test_difference * 2
    checks = [
        check('Elastic forward and reverse equilibrium weights agree',
              abs(equilibrium - electron_reverse * occupation_out * (1 + occupation_in)), 1e-60),
        check('Nonlinear elastic source derivative equals half the two-orientation Dirichlet sum',
              abs(direct - two_orientations / 2), 1e-60),
        dict(name='Omitting the elastic half factor doubles the actual gain-loss derivative',
             passed=bool(abs(two_orientations / direct - 2) < mp.mpf('1e-60'))),
        check('Distribution dependence of scalar rate multiplies vanishing equilibrium bracket',
              abs(mp.diff(lambda epsilon: net_flux(epsilon, mp.mpf('17')), mp.mpf(0)) - direct), 1e-60)]
    finish(folder, dict(checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks),
           source_derivative=str(direct), doubled_unweighted_sum=str(two_orientations),
           meaning='The elastic integral covers both initial-final orientations; ordered 2-to-3 reaction and its paired representation have separately derived factors.'),
           __file__)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']], count=len(checks))), flush=True)


if __name__ == '__main__':
    main()
