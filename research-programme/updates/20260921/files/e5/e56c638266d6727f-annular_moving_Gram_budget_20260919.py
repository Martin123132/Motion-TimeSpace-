from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded
import numpy as np


def pullback(values, indices, shape, count):
    result = np.zeros(count)
    np.add.at(result, indices.ravel(), (shape*values[:, None]).ravel())
    return result


def adjoint_rate(coarse_mass, fine_mass, coarse_mass_rate, fine_mass_rate,
                 test, test_rate, adjoint, indices, shape):
    loads = dict(
        test_acceleration=pullback(band_action(fine_mass, test_rate), indices, shape, len(adjoint)),
        fine_mass_transport=pullback(band_action(fine_mass_rate, test), indices, shape, len(adjoint)),
        coarse_mass_transport=-band_action(coarse_mass_rate, adjoint))
    channels = {name:solve_banded((2, 2), coarse_mass, load, check_finite=False)
                for name, load in loads.items()}
    return dict(rate=sum(channels.values()), channels=channels, load=sum(loads.values()))


def variation_rate(atoms, atom_rates):
    return dict(variation=float(np.sum(abs(atoms))),
        upper_right_rate=float(np.sum(np.where(atoms == 0., abs(atom_rates), np.sign(atoms)*atom_rates))),
        absolute_rate_budget=float(np.sum(abs(atom_rates))))


def pairing_rate(weights, weight_rate, trial, trial_rate, test, test_rate):
    rows = dict(weight_transport=weight_rate*trial*test,
                trial_transport=weights*trial_rate*test,
                test_transport=weights*trial*test_rate)
    return dict(rate=float(sum(np.sum(value) for value in rows.values())),
                channels={name:float(np.sum(value)) for name, value in rows.items()},
                row_absolute_rate_bound=float(sum(np.sum(abs(value)) for value in rows.values())))
