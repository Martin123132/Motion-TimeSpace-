from __future__ import annotations

from pathlib import Path
import numpy as np
from scipy import linalg

from bound_common import ROOT, BRANCH, PARENT, Background, modest_process, save, read_json, whiten
from polar_energy import quadrature, basis


def background_controls():
    background = Background()
    rows = []
    form_rows = []
    for cells in [128, 512, 2048]:
        position, weights, *_ = quadrature(np.linspace(0, background.radius, cells+1), 8)
        values = background.values(position)
        field, gradient, second_gradient, metric, lapse, potential, second, rotation2, metric_prime, lapse_gradient = [values[key] for key in ['field', 'gradient', 'second_gradient', 'metric', 'lapse', 'energy', 'second', 'rotation2', 'metric_prime', 'log_lapse_prime']]
        phase_load = 3*background.alpha*position**2*rotation2*field**2
        scalar_load = 2*background.alpha*position**2*(metric*gradient**2+potential)+position**2*metric*lapse_gradient**2
        scalar_margin = (6-2*metric)/position**2-2*background.alpha*(metric*gradient**2+potential)-metric*lapse_gradient**2-2*rotation2*lapse_gradient*field/gradient
        rows.append(dict(cells=cells, sample_count=len(position), max_phase_load=float(max(phase_load)), phase_sufficient_threshold=6., max_scalar_load=float(max(scalar_load)), scalar_sufficient_threshold=4., min_metric=float(min(metric)), max_metric=float(max(metric)), min_lapse_gradient=float(min(lapse_gradient)), max_field_gradient=float(max(gradient)), min_scalar_remainder_times_r2=float(min(position**2*scalar_margin)), numerical_sampling_not_interval_certificate=True))
        trial, trial_prime, _ = basis(position, background.radius, 6, 2)
        seed = np.sqrt(metric)*gradient
        log_seed_prime = metric_prime/(2*metric)+second_gradient/gradient
        transformed_derivative = trial_prime-log_seed_prime[:, None]*trial
        weighted = weights*lapse*position**2/np.sqrt(metric)
        original = trial_prime.T@((weighted*metric)[:, None]*trial_prime)+trial.T@((weighted*(second-rotation2+6/position**2))[:, None]*trial)
        transformed = transformed_derivative.T@((weighted*metric)[:, None]*transformed_derivative)+trial.T@((weighted*scalar_margin)[:, None]*trial)
        error = float(np.linalg.norm(original-transformed)/np.linalg.norm(original))
        phase_test = trial[:, 0]
        phase_test_prime = trial_prime[:, 0]
        original_phase = np.sum(weights*position**2/np.sqrt(metric)*(metric*phase_test_prime**2+(6/position**2-background.alpha*rotation2*field**2-2*background.alpha*potential)*phase_test**2))
        ground_phase = np.sum(weights*position**2/np.sqrt(metric)*(metric*(phase_test_prime-lapse_gradient*phase_test)**2+(6/position**2-3*background.alpha*rotation2*field**2)*phase_test**2))
        form_rows.append(dict(cells=cells, scalar_ground_state_relative_error=error, phase_ground_state_relative_error=float(abs(original_phase/ground_phase-1)), scalar_seed_max=float(max(seed))))
    save('background', Path(__file__), dict(rows=rows, form_rows=form_rows,
         scope='Sampled sufficient-criterion diagnostics and integral identity replays on saved background. These are not interval bounds on the continuum solution.',
         new_background_solves=0), [background.profile.path, BRANCH/'self-gravity-20261003/results/fine/status.json'])
    print(dict(background_rows=rows, form_rows=form_rows), flush=True)


def contraction(left, cross, right):
    left_factor = linalg.cholesky(left, lower=True)
    right_factor = linalg.cholesky(right, lower=True)
    left_solved = linalg.solve_triangular(left_factor, cross, lower=True)
    normalized = linalg.solve_triangular(right_factor, left_solved.T, lower=True).T
    singular = linalg.svdvals(normalized)
    return float(singular[0])


def schur_controls():
    labels = ['pilot', 'standard', 'refined-mesh', 'enlarged', 'resolved', 'resolved-more', 'resolved-mesh', 'resolved-support', 'support-mesh']
    rows, inputs = [], []
    for label in labels:
        status_path = PARENT/'results'/label/'status.json'
        archive_path = PARENT/'results'/label/'forms.npz'
        inputs.extend([status_path, archive_path])
        status = read_json(status_path)
        gravity_count = status['configuration']['gravity_count']
        matter_count = status['configuration']['matter_count']
        with np.load(archive_path) as arrays:
            even = (arrays['even']+arrays['even'].T)/2
            gram = arrays['gram']
        cholesky = linalg.cholesky(gram, lower=True)
        even = whiten(even, cholesky)
        even = (even+even.T)/2
        position_count = gravity_count+matter_count
        spatial = even[:position_count, :position_count]
        mixed = even[:position_count, position_count:]
        charge = even[position_count:, position_count:]
        charge_factor = linalg.cho_factor(charge, lower=True)
        solved = linalg.cho_solve(charge_factor, mixed.T)
        reduced = spatial-mixed@solved
        reduced = (reduced+reduced.T)/2
        gravity = reduced[:gravity_count, :gravity_count]
        coupling = reduced[:gravity_count, gravity_count:]
        scalar = reduced[gravity_count:, gravity_count:]
        gamma = contraction(gravity, coupling, scalar)
        phase_gamma = contraction(spatial, mixed, charge)
        rng = np.random.default_rng(4600+gravity_count)
        coordinates = rng.normal(size=position_count)
        phase_momentum = rng.normal(size=matter_count)
        full = np.r_[coordinates, phase_momentum]
        shifted = phase_momentum+solved@coordinates
        direct = float(full@even@full)
        completed = float(shifted@charge@shifted+coordinates@reduced@coordinates)
        reconstruction_error = abs(direct-completed)/max(abs(direct), 1e-300)
        scalar_effective = scalar-coupling.T@linalg.solve(gravity, coupling, assume_a='pos')
        normalized_scalar = whiten(scalar_effective, linalg.cholesky(scalar, lower=True))
        exact_relative_min = float(linalg.eigvalsh(normalized_scalar)[0])
        rows.append(dict(label=label, gravity_count=gravity_count, matter_count=matter_count,
             phase_block_min=float(linalg.eigvalsh(charge)[0]), phase_square_completion_error=reconstruction_error,
             phase_contraction=phase_gamma, gravity_min=float(linalg.eigvalsh(gravity)[0]),
             scalar_min=float(linalg.eigvalsh(scalar)[0]), gravity_scalar_contraction=gamma,
             relative_energy_bound=1-gamma, scalar_schur_relative_bound=1-gamma**2,
             independent_scalar_schur_relative_min=exact_relative_min,
             is_continuum_bound=False))
    assert all(row['phase_square_completion_error'] < 1e-12 for row in rows)
    assert all(abs(row['independent_scalar_schur_relative_min']-row['scalar_schur_relative_bound']) < 1e-9 for row in rows)
    save('schur', Path(__file__), dict(rows=rows, new_field_solves=0,
         scope='Exact matrix Schur completions of archived full constraint Hessians; relative coupling diagnostics, not a continuum operator-norm bound.'), inputs)
    print(dict(schur_rows=rows), flush=True)


if __name__ == '__main__':
    modest_process()
    background_controls()
    schur_controls()
