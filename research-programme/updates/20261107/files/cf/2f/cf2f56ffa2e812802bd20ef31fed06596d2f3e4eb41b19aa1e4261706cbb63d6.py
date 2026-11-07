from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_moving_Legendre_current_20260921 import samples
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def assemble(action, edge_vertices, field_vertices, order, correction=None):
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    shape = field_vertices.shape[0], field_vertices.shape[1] + 1
    coupling = np.zeros(shape)
    mass, wave_norm, dust_norm, maximum_source_response = 0., 0., 0., 0.
    for label, weight in zip(labels, weights):
        row = samples(action, label, 12)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        cells, local = quad['cells'], quad['local']
        indices = np.array(action.mesh['elements'])[cells]
        reference_edges = np.array([float(value) for value in action.edges])
        widths = np.diff(reference_edges)[cells] * geometry['jacobian']
        field_values = cardinal @ field_vertices
        edge_values = cardinal @ edge_vertices
        field, unused = interpolate_nodal(field_values, indices, local, widths)
        eta = (1 - local) * edge_values[cells] + local * edge_values[cells + 1]
        gradient = row['gradient'] / geometry['jacobian']
        defect = field - eta * gradient
        measure = quad['measure'] * geometry['kinetic']
        mass += weight * (measure @ defect**2)
        response = np.zeros_like(defect)
        source_response = 0.
        if correction is not None:
            response, unused = interpolate_nodal(cardinal @ correction[:, :-1], indices, local, widths)
            source_response = float(cardinal @ correction[:, -1])
            response += row['motion'] * source_response
        remainder = defect - response
        field_covector = np.zeros(shape[1] - 1)
        selected = indices >= 0
        contributions = (measure * remainder)[:, None] * row['shape']
        np.add.at(field_covector, indices[selected], contributions[selected])
        source_covector = measure @ (row['motion'] * remainder)
        source = row['source']
        values = action.solver.values(action.solution, np.array([source]))[0]
        lapse, metric = np.exp(values[1, 0]), 1 - 2 * values[0, 0] / source
        clock = np.sqrt(lapse**2 - row['velocity']**2 / metric)
        inertia = action.owner.source_mass * lapse**2 / (metric * clock**3)
        source_covector -= inertia * source_response
        coupling += weight * np.outer(cardinal, np.r_[field_covector, source_covector])
        wave_norm += weight * (measure @ remainder**2)
        dust_norm += weight * inertia * source_response**2
        maximum_source_response = max(maximum_source_response, abs(source_response))
    return dict(coupling=coupling, mass=mass, direct_norm=wave_norm + dust_norm,
        wave_norm=wave_norm, dust_norm=dust_norm, maximum_source_response=maximum_source_response)


def main():
    evidence = EvidenceRun('annular-support-Schur-conditioning-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 5400
    try:
        evidence.own(evidence.root / 'DERIVATION-20260928-support-Schur-conditioning.md')
        authority_path = evidence.output.parent / 'annular-directional-coupled-Euler-attempt02/status.json'
        parent = json.loads(authority_path.read_text())
        evidence.own(authority_path)
        evidence.check('directional_main_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, digest in parent[category].items():
                path = evidence.root / relative
                key = str(path.relative_to(evidence.root))
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    bad.append(relative)
                else:
                    digests[key] = digest
                    evidence.own(path)
        evidence.check('directional_inputs_rehashed', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        rows = []
        with localcontext() as context:
            context.prec = 64
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                if perf_counter() > deadline:
                    raise RuntimeError('Safe completed-case runtime boundary')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                owner = read(sources['parent'])
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                if level == 'fine':
                    owner = read(str((evidence.output.parent / 'annular-matched-seed-flow-attempt01/status.json').relative_to(evidence.root)))
                final = max((row for row in owner['iterations'] if row['case'] == centre['case'] and row['estimate'] == 1), key=lambda row: row['iteration'])
                solved_residual = read(final['output'])['residual']
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                directions = read(case['direction_path'])
                raw = assemble(action, directions['edge_vertices'], directions['field_vertices'], 48)
                correction = inverse.solve(raw['coupling'].ravel()).reshape(loads.rates.shape)
                mass_eliminated = float(raw['coupling'].ravel() @ correction.ravel())
                schur = raw['mass'] - mass_eliminated
                residual = matrix @ correction.ravel() - raw['coupling'].ravel()
                relative_residual = float(np.max(abs(residual)) / max(np.max(abs(raw['coupling'])), 1e-300))
                evidence.check(name + ':linear_solve', relative_residual <= 2e-10, relative_residual)
                direct = assemble(action, directions['edge_vertices'], directions['field_vertices'], 48, correction)
                refined = assemble(action, directions['edge_vertices'], directions['field_vertices'], 64, correction)
                scale = max(raw['mass'], 1e-300)
                evidence.check(name + ':positive_schur', schur > 0 and direct['direct_norm'] > 0)
                evidence.check(name + ':independent_Schur_norm', abs(schur - direct['direct_norm']) <= 2e-9 * scale,
                    dict(schur=schur, direct=direct['direct_norm'], absolute_error=abs(schur - direct['direct_norm'])))
                orthogonality = float(np.max(abs(direct['coupling'])) / max(np.max(abs(raw['coupling'])), 1e-300))
                evidence.check(name + ':independent_orthogonality', orthogonality <= 2e-8, orthogonality)
                evidence.check(name + ':norm_quadrature', abs(refined['direct_norm'] - direct['direct_norm']) <= 2e-8 * scale)
                base = read(case['material_paths'][0])
                channels = list(base['channels'])
                expected_mass = float(base['average'][channels.index('kinetic_defect')])
                evidence.check(name + ':same_direction_mass', abs(expected_mass - raw['mass']) <= 2e-9 * scale)
                force = float(base['average'][channels.index('coupled_direct')])
                old_euler_work = float(correction.ravel() @ solved_residual.ravel())
                corrected_force = force - old_euler_work
                response = -corrected_force / schur
                path = evidence.output / (name + '-projection.npz')
                np.savez_compressed(path, coupling=raw['coupling'], correction=correction,
                    linear_residual=residual, independent_orthogonality=direct['coupling'], solved_Euler_residual=solved_residual,
                    raw_mass=raw['mass'], effective_mass=schur, direct_norm=direct['direct_norm'], refined_norm=refined['direct_norm'])
                evidence.own(path, 'outputs')
                rows.append(dict(branch=branch, level=level, raw_kinetic_mass=raw['mass'], eliminated_mass=mass_eliminated,
                    effective_mass=schur, independent_norm=direct['direct_norm'], wave_norm=direct['wave_norm'], dust_norm=direct['dust_norm'],
                    directional_force=force, removed_old_Euler_work=old_euler_work, corrected_force=corrected_force,
                    frozen_metric_amplitude_acceleration=response, mass_norm_required=abs(corrected_force) / np.sqrt(schur),
                    linear_relative_residual=relative_residual, direct_orthogonality=orthogonality,
                    condition_scope='fixed metric; no new support-to-metric response; not an evolved physical solution'))
                evidence.report['cases'].append(dict(branch=branch, level=level, output=str(path.relative_to(evidence.root))))
                evidence.save()
                del inverse, matrix
        path = evidence.output / 'support-Schur-conditioning.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=rows, new_nonlinear_solves=0,
            new_trajectories=0, full_metric_response_for_independent_support_included=False, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
