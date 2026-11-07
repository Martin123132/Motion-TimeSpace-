import argparse
from nonlocal_dc import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--mode', choices=['local-derived', 'local-leading', 'nonlocal-leading', 'nonlocal-soft-gaunt'], required=True)
    parser.add_argument('--bank', default='s700-i160')
    parser.add_argument('--steps', type=int, default=6400)
    arguments = parser.parse_args()
    ladder = infrared_ladder.InfraredLadder(BACKGROUND / 'banks/infrared96-q700')
    background = thermal_wave.thermal.ThermalBackground(arguments.model)
    emission = NonlocalEmission(ladder.basis, background, arguments.mode, ROOT / 'banks' / arguments.bank)
    engine.ROOT = ROOT
    engine.ConsistentBasis = lambda count: ladder.basis
    engine.ExtendedLadder = lambda folder, basis: ladder
    engine.EmissionMatrices = lambda basis, quadrature: emission
    def local_finish(folder, report, script, extra=()):
        corrected = [BACKGROUND / 'emission_rates.py' if Path(path) == ROOT / 'emission_rates.py' else Path(path) for path in extra]
        report.update(mode=arguments.mode, bank=arguments.bank, basis_spec=ladder.specification,
                      bremsstrahlung_included=True, nonlocal_three_photon_response=arguments.mode.startswith('nonlocal'),
                      exact_relativistic_finite_frequency_kernel=False, full_virtual_correction_inserted=False,
                      dc_energy_conserving_leading_limit=arguments.mode.startswith('nonlocal'),
                      source_scope='Same physical Compton, sourced H/He BR, geometry and gas capacity; staged leading Gould redistribution or explicitly named comparison.',
                      final_photon_number_fraction=report['final_photon_number_moment'] * np.pi**4 / (30 * special.zeta(3)))
        finish(folder, report, __file__, [Path(script), *corrected, *emission.inputs])
    engine.finish = local_finish
    arguments.count = 96
    arguments.quadrature = 900
    arguments.emission = 'dcbr'
    engine.main(arguments)


if __name__ == '__main__':
    main()
