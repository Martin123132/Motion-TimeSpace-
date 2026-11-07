import argparse
from types import SimpleNamespace
from emission_angular_common import *
from emission_rates import ALPHA
from integrated_dc import IntegratedDCEmission
from infrared_ladder import InfraredLadder
import evolve_emitting_background as engine


class ReactionEmission(IntegratedDCEmission):
    def __init__(self, basis, background, folder, correction=True):
        super().__init__(basis, background, 900, 81)
        self.reaction_source = folder / 'block-0.npz'
        with np.load(self.reaction_source) as saved:
            self.reaction = saved['stiffness'].copy()
        self.correction = correction

    def at(self, theta, variant):
        assert variant == 'dcbr'
        br = super().at(theta, 'dcbr') - super().at(theta, 'dc')
        rate = 4 * ALPHA / (3 * math.pi) * theta ** 2
        if self.correction:
            rate /= 1 + 14.16 * theta
        return br - rate * self.reaction


def main(arguments):
    modest()
    scatter_folder = PARENT / 'banks/infrared104-q700'
    ladder = InfraredLadder(scatter_folder)
    background = thermal_wave.thermal.ThermalBackground(arguments.model)
    reaction_folder = ROOT / 'banks' / arguments.bank
    packet = json.loads((reaction_folder / 'status.json').read_text())
    assert packet['all_checks_passed'] and packet['basis_spec'] == ladder.specification
    emission = ReactionEmission(ladder.basis, background, reaction_folder, not arguments.pure_gould)
    engine.ROOT = ROOT
    engine.ConsistentBasis = lambda count: ladder.basis
    engine.ExtendedLadder = lambda folder, basis: ladder
    engine.EmissionMatrices = lambda basis, quadrature: emission
    def local_finish(folder, report, script, extra):
        dependencies = [BACKGROUND / 'emission_rates.py' if path == ROOT / 'emission_rates.py' else path for path in extra]
        report.update(basis_spec=ladder.specification, bank=str(reaction_folder),
            bremsstrahlung_included=True, full_gould_photon_energy_redistribution=True,
            dc_gas_energy_source='Zero at retained cold-electron Gould order; Compton and BR still exchange energy with gas.',
            scalar_relativistic_rate_correction=not arguments.pure_gould,
            coefficient_scope='Unpolarized Gould reaction plus inherited finite-shift Compton and tabulated H/He BR; not full thermal-electron DC.',
            kernel='Photon loss at incident frequency, gain at both outgoing frequencies; paired recoil-free Gould event.',
            final_photon_number_fraction=report['final_photon_number_moment'] * math.pi ** 4 / (30 * special.zeta(3)))
        finish(folder, report, __file__, [Path(script), reaction_folder / 'status.json', emission.reaction_source,
                                         BACKGROUND / 'integrated_dc.py', *emission.inputs, *dependencies])
    engine.finish = local_finish
    engine.main(SimpleNamespace(model=arguments.model, count=104, steps=arguments.steps, quadrature=900,
                                emission='dcbr', name=arguments.name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, choices=['heavy', 'cold'])
    parser.add_argument('--name', required=True)
    parser.add_argument('--bank', default='reaction104-q420-240')
    parser.add_argument('--steps', type=int, default=6400)
    parser.add_argument('--pure-gould', action='store_true')
    main(parser.parse_args())
