from polar_nodes import *
from exact_angular_factor import reduced


def main():
    modest()
    folder = ROOT / 'results/symmetry'
    folder.mkdir(parents=True, exist_ok=False)
    seal_path = PARENT / 'results/stage-integrity.json'
    assert digest(seal_path) == PARENT_SEAL
    seal = json.loads(seal_path.read_text())
    assert len(seal['file_hashes']) == 27238 and seal['state'] == 'complete'
    for name, expected in seal['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks = [dict(name='All27238 sealed parent payloads verified', passed=True)]
    gamma = reduced.GAMMA
    spin_reflection = gamma[0] @ gamma[1] @ gamma[3]
    inverse = spin_reflection.conj().T
    reflection = np.diag([1., 1., -1., 1.])
    residual = max(float(np.max(abs(spin_reflection @ gamma[index] @ inverse - reflection[index,index] * gamma[index]))) for index in range(4))
    metric_residual = float(np.max(abs(inverse @ gamma[0] @ spin_reflection - gamma[0])))
    assert residual == 0 and metric_residual == 0
    checks.append(dict(name='Exact Pin reflection of all Dirac generators and Dirac adjoint', passed=True))
    theta = json.loads((PARENT / 'runs/expensive-h5-az8/status.json').read_text())['configuration']['temperature']
    moments = []
    for polar in [2, 3]:
        full, folded = list(electron_nodes(theta, polar, False)), list(electron_nodes(theta, polar, True))
        values = []
        for current in [full, folded]:
            moments_row = np.zeros(6)
            normalization = 0.
            for node in current:
                vector = np.array(node['velocity'])
                direction = vector / np.linalg.norm(vector)
                weight = node['electron_weight'] * node['reflection_multiplicity']
                normalization += weight
                moments_row += weight * np.array([direction[0]**2, direction[2]**2, direction[0]**4, direction[2]**4,
                    direction[0]**2 * direction[1]**2, direction[0]**2 * direction[2]**2])
            assert abs(normalization - 1) < 2e-14
            values.append(moments_row)
        target = np.array([1/3, 1/3, 1/6, 1/9, 1/18, 1/9]) if polar == 2 else np.array([1/3, 1/3, 1/5, 1/5, 1/15, 1/15])
        error = max(float(np.max(abs(value - target))) for value in values)
        checks.append(dict(name='Derived normalized second/fourth moments, full and folded polar' + str(polar),
            value=error, passed=error < 2e-14))
        moments.append(dict(polar=polar, full_nodes=len(full), folded_nodes=len(folded), moments=values[0].tolist()))
    closure_errors = []
    for order in [2, 4]:
        angles = list(weak.source.angular_nodes(order))
        error = max(min(np.max(abs(np.array([direction[0], -direction[1], direction[2]]) - other)) + abs(weight-other_weight)
            for other,other_weight in angles) for direction,weight in angles)
        closure_errors.append(float(error))
    checks.append(dict(name='Virtual and real angular quadratures close under reflection',
        value=max(closure_errors), passed=max(closure_errors) < 2e-14))
    spectra = Spectra(.5)
    difference_model, control_model = FastSplit(spectra, 'difference'), SplitReal(spectra, 'control')
    rule = PanelRule(.5)
    physical = list(physical_nodes(theta, 'expensive'))
    selections = [(group * 5 + 1 + group % 3, [1,13,27,6,20,25][group], [0,2,4,1,3,2][group]) for group in range(6)]
    rows, inputs = [], [seal_path, ROOT / 'polar_nodes.py']
    for case, (electron, frequency, hard) in enumerate(selections):
        identity = physical[electron * 140 + frequency * 5 + hard]
        parameters, weight = parameters_and_weight(theta, identity)
        mirrored_velocity = np.array(identity['velocity']) * np.array([1., -1., 1.])
        mirrored = weak.source.context(theta * identity['frequency'], identity['cosine'], mirrored_velocity, theta)
        geometry_error = max(float(np.max(abs(mirrored['transform'] - reflection @ parameters['transform'] @ reflection))),
            float(np.max(abs(mirrored['bath'] - reflection @ parameters['bath']))))
        scalar_keys = ['energy', 'cosine', 'hard', 'hard_doppler', 'hard_bose', 'relative_flux', 'angular_jacobian', 'born_differential_over_thomson']
        scalar_error = max(abs(mirrored[key] - parameters[key]) / max(abs(parameters[key]), 1e-30) for key in scalar_keys)
        left, loop_left, path_left, null_left = source_components(parameters, difference_model, control_model, rule)
        right, loop_right, path_right, null_right = source_components(mirrored, difference_model, control_model, rule)
        differences = {key:float(np.max(abs(left[key] - right[key]))) / max(float(np.max(abs(left[key]))), 1e-30) for key in left}
        loop_error = abs(loop_left-loop_right) / max(abs(loop_left), 1e-30)
        checks.append(dict(name='Actual reflected scalar source and complex-loop probe' + str(case),
            geometry_relative=scalar_error, geometry_absolute=geometry_error, component_relative=differences,
            loop_relative=loop_error, passed=bool(geometry_error < 1e-12 and scalar_error < 1e-12
                and max(differences.values()) < 1e-6 and loop_error < 1e-9 and max(null_left,null_right) < 1e-10)))
        path = folder / ('probe-' + str(case) + '.npz')
        np.savez(path, **{'original-' + key:value for key,value in left.items()},
            **{'reflected-' + key:value for key,value in right.items()},
            velocity=np.array(identity['velocity']), reflected_velocity=mirrored_velocity)
        inputs += [path, path_left, path_right]
        rows.append(dict(case=case, identity=identity, geometry_error=geometry_error, component_relative=differences, loop_relative=loop_error))
    checks.append(dict(name='Positive folded rule covers48 physical velocities with30 representatives',
        passed=len(list(electron_nodes(theta,3,False))) == 48 and len(list(electron_nodes(theta,3,True))) == 30))
    finish(folder, dict(checks=checks, moments=moments, actual_mirror_probes=rows,
        scalar_unpolarized_scope_only=True, imaginary_loop_coefficients_preserved=True,
        symmetry_derived_from_parent_dirac_structure=True,
        direct_probe_max_component_relative=max(max(row['component_relative'].values()) for row in rows),
        global_floating_error_bound=False), __file__, [*inputs,*spectra.inputs,ROOT / 'DERIVATION.md'])
    print(json.dumps(dict(checks=checks,moments=moments,all_passed=all(row['passed'] for row in checks))), flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
