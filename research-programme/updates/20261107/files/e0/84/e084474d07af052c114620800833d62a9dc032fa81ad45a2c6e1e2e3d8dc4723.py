import os
for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[name] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'local-quarter-step-gas-curvature-20261020'
sys.path.insert(0, str(PARENT))
import quarter_step_stage183 as prior
np, linear, native = prior.np, prior.linear, prior.native


def main():
    prior.source.modest()
    ladder = native.infrared_ladder.InfraredLadder(native.BACKGROUND / 'banks/infrared96-q700')
    basis = ladder.basis
    index = 1
    slope_low = (ladder.blocks[index] - ladder.blocks[index - 1]) / (ladder.temperatures[index] - ladder.temperatures[index - 1])
    slope_high = (ladder.blocks[index + 1] - ladder.blocks[index]) / (ladder.temperatures[index + 1] - ladder.temperatures[index])
    rows = []
    for model in ['heavy', 'cold']:
        background = native.thermal_wave.thermal.ThermalBackground(model)
        emission = native.NonlocalEmission(basis, background, 'nonlocal-leading', native.ROOT / 'banks/s960-i256')
        with np.load(PARENT / 'histories' / model / 'quarter/history.npz') as packet:
            anchor = float(packet['coordinates'][0])
            ordinal = int(np.argmin(abs(packet['expansion'] - anchor)))
            profile = packet['profiles'][ordinal]
            gas = float(packet['temperature_scaled'][ordinal])
            step = float(packet['step'])
        local = background.at(anchor)
        rate = local['coefficient'] / local['thermal_parameter']
        stiffness = rate * (ladder.at(local['thermal_parameter'], 0) - emission.at(local['thermal_parameter'], 'dcbr'))
        jump = rate * local['thermal_parameter'] * (slope_high - slope_low)
        dual = linear.solve(basis.mass.T, basis.energy, assume_a='pos')
        capacity = background.chi - dual @ stiffness @ basis.temperature
        derivative_jump = -dual @ jump @ (profile - basis.temperature * gas) / capacity
        rows.append(dict(model=model, anchor=anchor, step=step, gas=gas, heat=background.chi,
            effective_capacity=float(capacity), relaxation_width=float(background.chi / capacity),
            slaved_slope_jump=float(derivative_jump), predicted_width_difference=float(-derivative_jump / .01),
            continuous_curvature_jump=float(-dual @ jump @ (profile - basis.temperature * gas) / background.chi)))
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
