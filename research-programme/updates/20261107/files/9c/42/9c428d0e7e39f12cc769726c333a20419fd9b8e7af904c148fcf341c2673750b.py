from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.interpolate import PPoly


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'quadrupole-response-20261004'))
from solve_static_bvp import integration_mesh, edge_values
from solve_tides import Profile, TidalProblem, potential, exterior_basis


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def spline_for(path):
    with np.load(path) as stored:
        return PPoly.construct_fast(stored['spline_coefficients'], stored['spline_knots'], axis=1)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/limits'
    output.mkdir(exist_ok=False)
    fine_path = ROOT/'results/fine/status.json'
    coarse_path = ROOT/'results/coarse/status.json'
    parent_path = BRANCH/'quadrupole-response-20261004/results/static-bvp/status.json'
    fine = json.loads(fine_path.read_text(encoding='utf-8'))
    coarse = json.loads(coarse_path.read_text(encoding='utf-8'))
    flat_report = json.loads(parent_path.read_text(encoding='utf-8'))
    flat_row = next(row for row in flat_report['rows'] if abs(row['radius']-20) < 1e-7 and row['cutoff_distance'] == .005)
    profile = Profile(20., 0.)
    position, weights = integration_mesh(profile.radius)
    field, gradient = profile.values(position)[:2]
    direct = float(weights@(position**6*(18*profile.frequency**2*field**2+2*gradient**2-12*potential(field))))
    predicted = (2*flat_row['susceptibility']+direct)/30
    positive = [row for row in fine['rows'] if row['alpha'] > 0]
    first, second = positive[:2]
    extrapolated = (second['alpha']*first['lambda_over_alpha']-first['alpha']*second['lambda_over_alpha'])/(second['alpha']-first['alpha'])
    weak_check = {'flat_chi_relax': flat_row['susceptibility'], 'direct_metric_moment': direct,
                  'predicted_lambda_over_alpha': predicted, 'extrapolated_lambda_over_alpha': extrapolated,
                  'relative_extrapolation_difference': abs(extrapolated/predicted-1),
                  'metric_contribution_fraction_of_total': direct/(2*flat_row['susceptibility']+direct),
                  'relative_error_if_only_previous_relaxation_is_used': abs((flat_row['susceptibility']/15)/predicted-1),
                  'two_nonzero_couplings_used_for_extrapolation': [first['alpha'], second['alpha']]}
    parent_archive = parent_path.parent/flat_row['archive']
    flat_spline = spline_for(parent_archive)
    current_flat = next(row for row in fine['rows'] if row['alpha'] == 0)
    current_archive = fine_path.parent/current_flat['archive']
    current_spline = spline_for(current_archive)
    coordinate = np.linspace(.001, min(flat_spline.x[-1], current_spline.x[-1]), 700)
    old_value = flat_spline(coordinate)[0]*profile.radius**4
    new_value = current_spline(coordinate)[2]*profile.radius**4
    flat_check = {'relative_scalar_profile_l2_difference': float(np.linalg.norm(new_value-old_value)/np.linalg.norm(old_value)),
                  'relative_edge_amplitude_difference': abs(current_flat['edge_amplitude']/flat_row['edge_amplitude']-1),
                  'maximum_normalized_metric_difference': float(max(abs(current_spline(coordinate)[0]+2*coordinate**2))),
                  'residual_decaying_coefficient_over_radius_fifth': abs(current_flat['decaying_coefficient'])/profile.radius**5}
    mesh_rows = []
    for row in fine['rows']:
        previous = next(entry for entry in coarse['rows'] if entry['alpha'] == row['alpha'])
        mesh_rows.append({'alpha': row['alpha'], 'nominal': row['nominal_flat_compactness'],
                          'relative_lambda_change': abs(previous['geometric_tidal_lambda']/row['geometric_tidal_lambda']-1) if row['alpha'] > 0 else None,
                          'relative_edge_change': abs(previous['edge_amplitude']/row['edge_amplitude']-1)})
    wronskians = []
    for compactness in [0., .01, .03, .2, .5]:
        for position in [20., 30., 60.]:
            mass = 10*compactness
            growing, growing_prime, decaying, decaying_prime = exterior_basis(position, mass)
            wronskians.append(abs((growing*decaying_prime-growing_prime*decaying)/(-5/growing)-1))
    report = {'state': 'complete', 'script_sha256': digest(__file__),
              'input_hashes': {str(path): digest(path) for path in [fine_path, coarse_path, parent_path, parent_archive, current_archive]},
              'weak_limit': weak_check, 'flat_limit': flat_check, 'mesh_rows': mesh_rows,
              'exterior_basis_checks': len(wronskians), 'maximum_wronskian_relative_error': max(wronskians),
              'scope': 'Same background family and fixed charge, varied coupling for weak-limit controls; not a fixed-theory astrophysical sequence.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
