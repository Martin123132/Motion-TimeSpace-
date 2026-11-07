import argparse
from integrated_dc import *
import evolve_sourced_background as runner


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--quadrature', type=int, default=900)
    parser.add_argument('--temperature-knots', type=int, default=81)
    parser.add_argument('--emission', choices=['none', 'soft', 'dc', 'dcbr', 'dcbrnr'], default='dcbr')
    parser.add_argument('--name', required=True)
    arguments = parser.parse_args()
    runner.SourcedEmission = IntegratedDCEmission
    def local_finish(folder, report, script, extra):
        report.update(dc_gaunt='Planck ambient Gould integral, Chluba-Sunyaev equation12, 96-node Laguerre quadrature; not full relativistic DC redistribution.',
                      coefficient_scope='Leading sourced heat order; no fitted Gaunt or radiation temperature. Full finite-frequency ambient derivative required at mixed wave order.')
        finish(folder, report, __file__, [Path(script), ROOT / 'integrated_dc.py', *extra])
    runner.finish = local_finish
    runner.main(arguments)
