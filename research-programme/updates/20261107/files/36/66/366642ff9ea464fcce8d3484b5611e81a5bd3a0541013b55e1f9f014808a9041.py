import argparse
from kinetic_common import *
import integrated_dc
import infrared_ladder
import evolve_emitting_background as engine


class DerivedEmission(integrated_dc.IntegratedDCEmission):
    def __init__(self,basis,background,enabled=True):
        super().__init__(basis,background,900,81)
        self.enabled=enabled
        table=ROOT/'results/derived-gaunt-bank/gaunt.npz'
        assert json.loads((table.parent/'status.json').read_text())['all_checks_passed']
        with np.load(table) as saved:
            self.gaunt_temperature=saved['temperatures'].copy()
            self.gaunt_interpolator=interpolate.CubicSpline(np.log(self.gaunt_temperature),saved['gaunt'],extrapolate=False)
        self.inputs.extend([table,ROOT/'results/derived-gaunt-bank/status.json'])

    def at(self,theta,variant):
        original=super().at(theta,variant)
        if not self.enabled or variant not in ['dc','dcbr','dcbrnr']:
            return original
        coordinate=float(np.clip(math.log(theta),np.log(self.gaunt_temperature[0]),np.log(self.gaunt_temperature[-1])))
        if abs(coordinate-math.log(theta))>1e-12:
            raise ValueError('Derived Gaunt table extrapolation forbidden')
        gaunt=float(self.gaunt_interpolator(coordinate))
        if not np.isfinite(gaunt):
            raise ValueError('Derived Gaunt table extrapolation forbidden')
        return original+integrated_dc.DC_CONSTANT*theta**2*(gaunt-1/(1+14.16*theta))*self.matrices['dc']


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--model',choices=['heavy','cold'],default='heavy')
    parser.add_argument('--control',action='store_true')
    parser.add_argument('--steps',type=int,default=6400)
    arguments=parser.parse_args()
    ladder=infrared_ladder.InfraredLadder(BACKGROUND/'banks/infrared96-q700')
    background=thermal_wave.thermal.ThermalBackground(arguments.model)
    emission=DerivedEmission(ladder.basis,background,not arguments.control)
    engine.ROOT=ROOT
    engine.ConsistentBasis=lambda count:ladder.basis
    engine.ExtendedLadder=lambda folder,basis:ladder
    engine.EmissionMatrices=lambda basis,quadrature:emission
    def local_finish(folder,report,script,extra=()):
        corrected=[BACKGROUND/'emission_rates.py' if Path(path)==ROOT/'emission_rates.py' else Path(path) for path in extra]
        report.update(derived_soft_gaunt=not arguments.control,retained_inverse_control=arguments.control,
                      bremsstrahlung_included=True,kernel='Retained physical finite-shift Compton and H/He free-free; derived soft DC population coefficient with retained Gould frequency shape.',
                      dc_gaunt='Numerically integrated soft-photon population coefficient with derived first-order1+4pi^2/3.' if not arguments.control else 'Inherited1/(1+14.16theta) control.',
                      basis_spec=ladder.specification,full_double_compton_redistribution_included=False,
                      full_virtual_weak_operator_inserted=False,finite_frequency_gould_shape_retained=True,
                      final_photon_number_fraction=report['final_photon_number_moment']*np.pi**4/(30*special.zeta(3)))
        finish(folder,report,__file__,[Path(script),BACKGROUND/'integrated_dc.py',BACKGROUND/'sourced_emission.py',
               BACKGROUND/'infrared_ladder.py',*corrected,*emission.inputs])
    engine.finish=local_finish
    arguments.count=96
    arguments.quadrature=900
    arguments.emission='dcbr'
    engine.main(arguments)


if __name__=='__main__':
    main()
