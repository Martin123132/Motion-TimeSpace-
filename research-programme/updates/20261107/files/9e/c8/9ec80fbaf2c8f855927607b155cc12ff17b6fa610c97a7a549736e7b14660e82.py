import argparse
from infrared_ladder import *
from sourced_emission import SourcedEmission
import evolve_emitting_background as engine


def main(arguments):
    modest()
    ladder = InfraredLadder(ROOT / 'banks' / arguments.bank)
    background = thermal_wave.thermal.ThermalBackground(arguments.model)
    emission = SourcedEmission(ladder.basis, background, arguments.quadrature, arguments.temperature_knots,
                              nonrelativistic=arguments.emission == 'dcbrnr')
    arguments.count = ladder.basis.count
    engine.ConsistentBasis = lambda count: ladder.basis
    engine.ExtendedLadder = lambda folder, basis: ladder
    engine.EmissionMatrices = lambda basis, quadrature: emission
    def local_finish(folder, report, script, extra):
        report.update(basis_spec=ladder.specification, bank=arguments.bank, temperature_knots=arguments.temperature_knots,
                      bremsstrahlung_included=arguments.emission in ['dcbr', 'dcbrnr'],
                      br_scope='Fully ionized hydrogen and helium; van Hoof source tables; nonrelativistic prefactor with merged NR/BHE Gaunt corrections, not a full EH collision integral.',
                      kernel='Retained physical finite-shift Compton plus sourced isotropic DC and H/He free-free terms.',
                      final_photon_number_fraction=report['final_photon_number_moment'] * math.pi ** 4 / (30 * special.zeta(3)))
        finish(folder, report, __file__, [Path(script), ROOT / 'sourced_emission.py', ROOT / 'infrared_ladder.py',
              ROOT / 'sources/1109.6552.html', ROOT / 'sources/gauntff-index.html', *emission.inputs, *extra])
    engine.finish = local_finish
    engine.main(arguments)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--quadrature', type=int, default=900)
    parser.add_argument('--temperature-knots', type=int, default=81)
    parser.add_argument('--emission', choices=['none', 'soft', 'dc', 'dcbr', 'dcbrnr'], default='dcbr')
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
