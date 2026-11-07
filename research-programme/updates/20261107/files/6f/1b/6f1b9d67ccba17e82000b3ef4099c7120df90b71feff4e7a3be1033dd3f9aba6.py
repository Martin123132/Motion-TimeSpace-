import math

import numpy as np


def assemble(actions, labels):
    required = {f'{model}-{kind}-s{subdivision}' for model in ('heavy', 'cold')
        for kind in ('bank', 'candidate', 'difference') for subdivision in (1, 2, 4)}
    if len(labels) != 18 or set(labels) != required:
        raise ValueError('All twelve physical states and six differences, once each, are required')
    actions = np.asarray(actions, dtype=float)
    if actions.shape != (19, 98, 18) or not np.isfinite(actions).all():
        raise ValueError('Equilibrium plus all background rows,98 outputs and all18 wave columns required')
    positions = {label: index for index, label in enumerate(labels)}
    result = {}
    for model in ('heavy', 'cold'):
        for subdivision in (1, 2, 4):
            baseline = positions[f'{model}-bank-s{subdivision}']
            candidate = positions[f'{model}-candidate-s{subdivision}']
            change = positions[f'{model}-difference-s{subdivision}']
            terms = [actions[baseline + 1, :, change], actions[change + 1, :, baseline], actions[change + 1, :, change]]
            delta = np.array([math.fsum(values) for values in zip(*terms)])
            result[f'{model}-s{subdivision}'] = dict(bank=actions[baseline + 1, :, baseline].copy(),
                candidate=actions[candidate + 1, :, candidate].copy(), bilinear_delta=delta,
                equilibrium_delta=actions[0, :, change].copy(), background_fixed=terms[0].copy(),
                background_change=terms[1].copy(), quadratic_difference=terms[2].copy())
    return result
