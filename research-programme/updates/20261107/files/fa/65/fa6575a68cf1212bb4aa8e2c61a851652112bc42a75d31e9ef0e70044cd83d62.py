from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, restore_refined
from annular_moving_Legendre_current_20260921 import samples
from annular_radial_Ward_moments_20260921 import test_functions
from derive_annular_radial_shape_exchange_20260927 import generator, nodal_test
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


BRANCHES = ['reference-reference', 'MTS-primary']
BLOCKS = ['field', 'cross', 'map', 'defect']


def exact_derivation(evidence):
    jac, alpha, beta = sp.symbols('J alpha beta', positive=True)
    speed, spatial, rate = sp.symbols('W q v', real=True)
    jac_x, speed_x, spatial_x, spatial_t = sp.symbols('J_x W_x q_x q_t', real=True)
    alpha_r, beta_r, eta, eta_x, eta_t = sp.symbols('alpha_r beta_r eta eta_x eta_t', real=True)
    gradient = spatial / jac
    temporal = rate - speed * gradient
    density = jac * (alpha * temporal**2 - beta * gradient**2) / 2
    momenta = sp.Matrix([sp.diff(density, rate), sp.diff(density, speed)])
    hessian = sp.hessian(density, (rate, speed))
    evidence.check('exact:primary_Legendre_constraint', sp.simplify(momenta[1] + gradient * momenta[0]) == 0)
    evidence.check('exact:velocity_Hessian_rank_one', hessian.rank() == 1)
    evidence.check('exact:null_vector', hessian * sp.Matrix([gradient, 1]) == sp.zeros(2, 1))
    schur = sp.simplify(hessian[1, 1] - hessian[0, 1]**2 / hessian[0, 0])
    evidence.check('exact:zero_map_Schur_complement', schur == 0)
    gradient_x = (spatial_x - gradient * jac_x) / jac
    gradient_t = (spatial_t - gradient * speed_x) / jac
    temporal_x = spatial_t - speed_x * gradient - speed * gradient_x
    variation = sp.diff(density, spatial) * (gradient_x * eta + gradient * eta_x)
    variation += sp.diff(density, rate) * (gradient_t * eta + gradient * eta_t)
    variation += sp.diff(density, jac) * eta_x + sp.diff(density, speed) * eta_t
    variation += sp.diff(density, alpha) * alpha_r * eta + sp.diff(density, beta) * beta_r * eta
    boundary = eta_x * (alpha * temporal**2 - beta * gradient**2) / 2
    boundary += eta * (jac * alpha_r * temporal**2 / 2 + alpha * temporal * temporal_x
                       - jac * beta_r * gradient**2 / 2 - beta * gradient * gradient_x)
    evidence.check('exact:off_shell_wave_shape_identity', sp.simplify(variation - boundary) == 0)
    velocity_shift = sp.symbols('velocity_shift', real=True)
    moved = density.subs({rate: rate + gradient * velocity_shift, speed: speed + velocity_shift}, simultaneous=True)
    evidence.check('exact:finite_null_velocity_invariance', sp.simplify(moved - density) == 0)
    evidence.report['exact_derivation'] = dict(momenta=list(map(str, momenta)), hessian=str(hessian),
        null_vector=str(sp.Matrix([gradient, 1])), map_schur=str(schur), wave_identity='E_chi + g E_u = 0',
        same_action_compatibility='B_G[eta*g,eta]=0', independent_map_inertia=0,
        assumptions=['J>0, alpha>0', 'J_t=W_x', 'fixed Eulerian metric under shape variation',
                     'compact variations vanish at source anchor and exterior boundaries',
                     'all weak cell-face terms retained', 'zero-shift Gram potential has no map velocity'],
        finite_space_caveat='Projected eta*g need not be an exact null direction in the retained trial space.',
        classification='Primary degeneracy and secondary compatibility derived; full Dirac closure not classified.')


def load_owned(evidence, digests, path):
    key = str(path.relative_to(evidence.root))
    if key not in digests:
        raise RuntimeError('Unowned input: ' + key)
    if path.suffix == '.json':
        return json.loads(path.read_text(encoding='utf-8'))
    with np.load(path, allow_pickle=False) as archive:
        return {key: archive[key].copy() for key in archive.files}


def restore_case(evidence, digests, branch_name, level, deadline):
    intake = evidence.output.parent
    branch, extension = branch_name.split('-')
    short = 'reference' if branch == 'reference' else branch_name
    parent_name = 'annular-' + short + ('-matched-current-attempt01' if level == 'fine' else '-third-current-attempt02')
    parent = load_owned(evidence, digests, intake / parent_name / 'status.json')
    centre = next(row for row in parent['centres'] if row.get('route') == 'resampled') if level == 'fine' else parent['centres'][0]
    folder = 'annular-nested-refinement-preparation-attempt02' if level == 'fine' else 'annular-resampled-third-grid-preparation-attempt01'
    suffix = '-refined-action.json' if level == 'fine' else '-third-action.json'
    packet_path = intake / folder / (branch_name + suffix)
    packet = load_owned(evidence, digests, packet_path)
    original_path = intake / 'annular-candidate-initial-metric-attempt02' / (branch + '-velocity-owned-inputs.npz')
    overlay_path = intake / 'annular-transfer-kernel-overlay-attempt01' / (branch + '-exact-common-overlay.json')
    original = load_owned(evidence, digests, original_path)
    overlay = load_owned(evidence, digests, overlay_path)
    native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
    base, unused, unused2 = common_material(native, original, overlay)
    owner = adapt_owner(base, packet['mesh'])
    state = load_owned(evidence, digests, evidence.root / centre['state_path'])
    loads, action = restore_refined(owner, state, packet['mesh'], packet, extension, deadline)
    paths = dict(parent=str((intake / parent_name / 'status.json').relative_to(evidence.root)),
                 state=centre['state_path'], packet=str(packet_path.relative_to(evidence.root)),
                 original=str(original_path.relative_to(evidence.root)), overlay=str(overlay_path.relative_to(evidence.root)))
    return loads, action, paths


def evaluate_layer(action, vertices, images, label):
    row = samples(action, label, 12)
    quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
    gradient = row['gradient'] / geometry['jacobian']
    eta = test_functions(geometry['radius'])[0] - test_functions(row['source'])[0][:, None] * geometry['displacement']
    actual = eta * gradient
    projected_nodes = np.einsum('tln,l->tn', vertices, cardinal)
    projected = np.einsum('tqv,qv->tq', projected_nodes[:, quad['indices']], row['shape'])
    weight = quad['measure'] * geometry['kinetic']
    defect = projected - actual
    blocks = np.array([(projected * weight) @ projected.T, (projected * weight) @ actual.T,
                       (actual * weight) @ actual.T, (defect * weight) @ defect.T])
    nodal = nodal_test(action, label)
    node_geometry = nodal['geometry']
    image = action.factor_values @ cardinal
    projected_image = np.einsum('atl,l->at', images, cardinal)
    atom = node_geometry['gradient'] * np.asarray(action.sampling.T @ (image**2 / 2)).ravel()
    coefficient = np.asarray(action.sampling @ node_geometry['gradient']).ravel() * image
    strain = 2 / node_geometry['radius'] + node_geometry['lapse_log_radial']
    strain += node_geometry['metric_radial'] / (2 * node_geometry['metric'])
    work = coefficient @ projected_image
    support = np.sum(atom * (strain * nodal['eta'] - nodal['eta_slope']), axis=1)
    speed = geometry['displacement'] * row['velocity']
    controls = []
    for amount in [-.125, .125, 1.]:
        moved = row['rate'] + amount * actual - (speed + amount * eta) * gradient
        shifted_projected = row['rate'] + amount * projected - (speed + amount * eta) * gradient
        scale = max(float(np.max(abs(row['temporal']))), float(np.max(abs(amount * actual))), 1e-300)
        controls.append([amount, np.max(abs(moved - row['temporal'])) / scale,
                         np.max(abs(shifted_projected - row['temporal'] - amount * defect)) / scale])
    raw = dict(weight=weight, projected=projected, actual=actual, eta=eta, gradient=gradient,
               rate=row['rate'], speed=speed, temporal=row['temporal'], kinetic=geometry['kinetic'],
               measure=quad['measure'], image=image, projected_image=projected_image, coefficient=coefficient,
               atom=atom, strain=strain * nodal['eta'] - nodal['eta_slope'], label=np.array(label))
    return blocks, np.array([work, support, work + support]), np.array(controls), raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-support-map-constraints-attempt01')
    parser.add_argument('--max-seconds', type=float, default=3600)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Independent support-map kinetic degeneracy and actual Gram shape compatibility.',
            blocks=BLOCKS, new_nonlinear_solves=0, subagents_used=False, github_action=False,
            regularizers_added=0, support_acceleration_solved=False, protected_since='2026-09-27T21:58:38+00:00')
        evidence.own(evidence.root / 'DERIVATION-20260927-support-map-Euler-and-kinetic-null.md')
        digests = {}
        for authority in ['annular-primary-reference-third-component-comparison-attempt01',
                          'annular-radial-shape-exchange-validation-attempt01']:
            path = evidence.output.parent / authority / 'status.json'
            status = json.loads(path.read_text())
            evidence.check(authority + ':complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            evidence.own(path)
            for table in ['inputs', 'outputs']:
                for relative, digest in status[table].items():
                    if relative in digests and digests[relative] != digest:
                        raise RuntimeError('Conflicting source hash: ' + relative)
                    digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        exact_derivation(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe runtime boundary; saved data retained')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        table = []
        for name in BRANCHES:
            for level in ['fine', 'third']:
                key = name + '-' + level
                progress(key + ':restore')
                loads, action, sources = restore_case(evidence, digests, name, level, deadline)
                vertices, source_vertices, images, error = generator(action)
                evidence.check(key + ':cardinals', error <= 2e-12)
                expected_count = 2188 if level == 'fine' else 4376
                evidence.check(key + ':full_grid', len(action.knots) == expected_count)
                generator_path = save(key + '-generator', vertices=vertices, images=images, source_vertices=source_vertices)
                averages, force_averages, material_paths, probe_paths = [], [], [], []
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    all_blocks, all_forces, all_controls = [], [], []
                    for index, label in enumerate(labels):
                        if index % 16 == 0:
                            progress(key + ':material' + str(order) + ':label' + str(index))
                        blocks, forces, controls, raw = evaluate_layer(action, vertices, images, label)
                        all_blocks.append(blocks)
                        all_forces.append(forces)
                        all_controls.append(controls)
                        if order == 64 and index in [0, 31, 63]:
                            probe_paths.append(save(key + '-probe' + str(index), **raw))
                    values, forces, controls = np.array(all_blocks), np.array(all_forces), np.array(all_controls)
                    average, force = np.tensordot(weights, values, axes=(0, 0)), np.tensordot(weights, forces, axes=(0, 0))
                    field, cross, support, defect = average
                    scale = float(np.max(abs(average[:3])))
                    identity_error = float(np.max(abs(defect - (field - cross - cross.T + support))))
                    hessian = np.block([[field, -cross], [-cross.T, support]])
                    eigenvalues = np.linalg.eigvalsh(hessian)
                    defect_eigenvalues = np.linalg.eigvalsh(defect)
                    evidence.check(key + ':block_identity:' + str(order), identity_error <= 2e-13 * scale, identity_error / scale)
                    evidence.check(key + ':positive_semidefinite:' + str(order), min(eigenvalues) >= -2e-13 * scale,
                                   float(min(eigenvalues) / scale))
                    evidence.check(key + ':positive_defect:' + str(order), min(defect_eigenvalues) >= -2e-13 * scale)
                    evidence.check(key + ':null_control:' + str(order), np.max(controls[:, :, 1:]) <= 2e-13,
                                   float(np.max(controls[:, :, 1:])))
                    evidence.check(key + ':finite:' + str(order), np.all(np.isfinite(values)) and np.all(np.isfinite(forces)))
                    if name == 'reference-reference':
                        evidence.check(key + ':zero_Gram_force:' + str(order), np.max(abs(forces)) == 0.)
                    material_paths.append(save(key + '-material' + str(order), labels=labels, weights=weights,
                        blocks=values, forces=forces, controls=controls, average=average, force_average=force,
                        hessian_eigenvalues=eigenvalues, defect_eigenvalues=defect_eigenvalues))
                    averages.append(average)
                    force_averages.append(force)
                if level == 'third':
                    old = load_owned(evidence, digests, evidence.output.parent / 'annular-radial-shape-exchange-attempt01' / (name + '-material64.npz'))
                    error = float(np.max(abs(force_averages[-1][2] - old['average'][6])))
                    evidence.check(key + ':sealed_shape_work', error <= 2e-18, error)
                for test in range(3):
                    table.append(dict(branch=name, level=level, test=test, shape_work=force_averages[-1][2, test],
                        field_work=force_averages[-1][0, test], support_work=force_averages[-1][1, test],
                        map_mass=averages[-1][2, test, test], projected_null_mass=averages[-1][3, test, test],
                        projected_null_fraction=averages[-1][3, test, test] / averages[-1][2, test, test],
                        mass_quadrature_change=averages[-1][3, test, test] - averages[0][3, test, test],
                        force_quadrature_change=force_averages[-1][2, test] - force_averages[0][2, test]))
                evidence.report['cases'].append(dict(branch=name, level=level, sources=sources,
                    field_count=len(action.knots), canonical_count=len(action.source) * (len(action.knots) + 1),
                    cells=len(action.mesh['elements']), gram_rows=action.factor.shape[0],
                    generator_path=generator_path, material_paths=material_paths, probe_paths=probe_paths,
                    shape_work=force_averages[-1][2].tolist(),
                    projected_null_fraction=(np.diag(averages[-1][3]) / np.diag(averages[-1][2])).tolist()))
                evidence.save()
        path = evidence.output / 'support-map-profiles.csv'
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(table[0]))
            writer.writeheader()
            writer.writerows(table)
        evidence.own(path, 'outputs')
        comparisons = []
        for name in BRANCHES:
            for test in range(3):
                fine = next(row for row in table if row['branch'] == name and row['level'] == 'fine' and row['test'] == test)
                third = next(row for row in table if row['branch'] == name and row['level'] == 'third' and row['test'] == test)
                comparisons.append(dict(branch=name, test=test,
                    projected_null_mass_ratio=third['projected_null_mass'] / fine['projected_null_mass'],
                    shape_fine=fine['shape_work'], shape_third=third['shape_work'],
                    shape_change=third['shape_work'] - fine['shape_work']))
        evidence.report.update(grid_comparison=comparisons, seconds=perf_counter() - started,
            numerical_interpretation='Finite-space projected norms measure representation error, not independent physical inertia.',
            exact_map_acceleration_fix_available=False, constrained_equilibrium_excluded=False)
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                             comparison=comparisons)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
