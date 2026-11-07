from __future__ import annotations

import math

import mpmath as mp
import numpy as np

from correlated_readout import CorrelatedNodalFeatures
from nodal_readout import coefficient_difference, make_bundle
from profile_preserving_features import ProfilePreservingFeatures


def bind(retained_bundle, retained_features, original, contexts, restart, heats):
    if len(original.epochs) != 1 or original.epochs[0].coordinate != restart['coordinate']:
        raise ValueError('An exact source-owned restart epoch is required')
    if set(contexts) != {'heavy', 'cold'} or set(heats) != set(contexts):
        raise ValueError('Both model-specific thermal contexts and heat sources are required')
    expected = {f'{model}-{kind}-s{subdivision}' for model in contexts
        for kind in ('bank', 'candidate') for subdivision in (1, 2, 4)}
    if set(restart['states']) != expected:
        raise ValueError('All twelve verified cases are required')
    for model, context in contexts.items():
        if context['model'] != model or context['coordinate'] != restart['coordinate']:
            raise ValueError('Thermal model/time differs from the carried state')
        if not all(math.isfinite(context[name]) and context[name] > 0 for name in ('theta', 'heat', 'rate', 'scale')):
            raise ValueError('Finite positive source-owned thermal quantities are required')
        if not math.isfinite(heats[model]) or heats[model] <= 0 or abs(heats[model] / context['heat'] - 1) > 1e-10:
            raise ValueError('Stored history heat and thermal coupling disagree')
    if contexts['heavy']['theta'] != contexts['cold']['theta']:
        raise ValueError('Different model temperatures require separate source operators')
    compact = CorrelatedNodalFeatures(original, restart['frequency'])
    features = ProfilePreservingFeatures(compact, retained_features(original))
    if features.profile_count != 96 or features.spectral_count != 577 or features.coefficient_count != 578:
        raise ValueError('Retain the complete 96-profile, 481-tail and gas state')
    labels, columns, normalized, records = [], [], [], []
    with mp.workdps(80):
        for model in ('heavy', 'cold'):
            heat = mp.mpf(float(heats[model]))
            for subdivision in (1, 2, 4):
                identifiers = [f'{model}-{kind}-s{subdivision}' for kind in ('bank', 'candidate')]
                states = [restart['states'][identifier] for identifier in identifiers]
                if any(state['model'] != model or state['subdivision'] != subdivision for state in states):
                    raise ValueError('Case identity differs from its source label')
                values = [state['coefficients'] for state in states]
                values.append(coefficient_difference(*values))
                names = identifiers + [f'{model}-difference-s{subdivision}']
                for name, state in zip(names, values):
                    if len(state) != 578 or not all(mp.isfinite(value) for value in state):
                        raise ValueError('Invalid full-coordinate carried state')
                    scaled = [heat * value for value in state]
                    labels.append(name)
                    columns.extend([scaled, scaled])
                    normalized.append(state)
                    records.append(dict(label=name, model=model, subdivision=subdivision, heat=float(heat)))
    inputs = list(dict.fromkeys([*map(str, original.inputs), *restart['inputs'],
        *(path for context in contexts.values() for path in context['inputs'])]))
    bundle = make_bundle(retained_bundle, features, columns, inputs)
    bundle.coordinate_convention = 'physical-background'
    bundle.coordinate = restart['coordinate']
    bundle.thermal_contexts = contexts
    bundle.history_scales = dict(heats)
    bundle.labels = labels
    if not np.array_equal(bundle.high[:, ::2], bundle.high[:, 1::2]) or not np.array_equal(bundle.low[:, ::2], bundle.low[:, 1::2]):
        raise ValueError('Physical coefficients must be identical across the two representation joins')
    return dict(bundle=bundle, labels=labels, records=records, normalized=normalized,
        physical_columns=columns, features=features, contexts=contexts)
