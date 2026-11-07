import argparse
from thermal_wave_common import *
from kernel_ladder import KernelLadder
from thermal_wave_system import ThermalWaveSystem
import run_paired_thermal_waves as paired


class RefinedLadder(KernelLadder):
    def __init__(self, count):
        super().__init__(count)
        folder = ROOT / 'banks' / ('high8-' + str(count) + '-event8')
        packet = json.loads((folder / 'status.json').read_text())
        assert packet['all_checks_passed'] and packet['basis_count'] == count and packet['event_order'] == 8
        self.inputs.append(folder / 'status.json')
        for index, theta in enumerate(self.temperatures):
            path = folder / ('theta-' + str(index) + '.npz')
            with np.load(path) as saved:
                assert abs(float(saved['theta']) / theta - 1) < 1e-14
                self.blocks[index][8] = saved['stiffness'].copy()
            self.inputs.append(path)


class RefinedSystem(ThermalWaveSystem):
    def __init__(self, model, count=24, maximum=8, control='physical'):
        super().__init__(model, count, maximum, control)
        self.ladder = RefinedLadder(count)


def refined_finish(folder, report, script, extra):
    report.update(highest_angular_event_order=8,
                  original_degree8_quadrature_failure_retained=True,
                  physical_change='Only degree8 event quadrature refined; no coefficients fitted and no tolerance relaxed.')
    finish(folder, report, __file__, [Path(script), ROOT / 'thermal_wave_system.py', ROOT / 'kernel_ladder.py', *extra])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--count', type=int, default=24)
    parser.add_argument('--steps', type=int, default=3200)
    parser.add_argument('--maximum', type=int, default=8)
    arguments = parser.parse_args()
    paired.ThermalWaveSystem = RefinedSystem
    paired.finish = refined_finish
    paired.main(arguments)
