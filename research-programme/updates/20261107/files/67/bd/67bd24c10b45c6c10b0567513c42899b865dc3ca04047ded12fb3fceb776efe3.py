from __future__ import annotations

from pathlib import Path
import numpy as np
import sympy as sp

from interior_common import ROOT, PARENT, modest_process, save
from local_system_v2 import LocalSystem, scalar_schur


def main():
    modest_process()
    system = LocalSystem()
    background = system.background
    position = background.radius*np.r_[np.linspace(.005, .995, 199), .999, 1.001, 1.1, 2., 4.]
    values, coefficients, derivatives, local, contact = system.values(position)
    phase, gradient, mixed, potential = scalar_schur(local)
    normalized_gradient = gradient.copy()
    scales = np.stack([np.sqrt(2*background.alpha/3)*position, np.ones_like(position)], axis=1)
    normalized_gradient *= scales[:, :, None]*scales[:, None, :]
    rows = [dict(radius_fraction=float(position[index]/background.radius), beta=float(coefficients['beta'][index]), omega=float(coefficients['omega'][index]),
            phase_coefficient=float(phase[index]), normalized_gradient_min=float(np.linalg.eigvalsh(normalized_gradient[index])[0]),
            normalized_gradient_max=float(np.linalg.eigvalsh(normalized_gradient[index])[1]),
            mixed=mixed[index].tolist(), potential=potential[index].tolist()) for index in range(len(position))]
    save('inspect-v2', Path(__file__), dict(rows=rows, minimum_phase_coefficient=float(min(phase)),
        minimum_normalized_gradient=float(min(np.linalg.eigvalsh(normalized_gradient)[:, 0])),
        negative_phase_samples=int(np.count_nonzero(phase <= 0)),
        negative_gradient_samples=int(np.count_nonzero(np.linalg.eigvalsh(normalized_gradient)[:, 0] <= 0)),
        scope='Local variable-change diagnostics, not canonical mode frequencies or a certified continuum positivity bound.'),
        [ROOT/'results/energy-v2/status.json', background.profile.path])
    print(dict(samples=len(position), phase_min=float(min(phase)), gradient_min=float(min(np.linalg.eigvalsh(normalized_gradient)[:, 0])), first=rows[0], last=rows[-1]), flush=True)


if __name__ == '__main__':
    main()
