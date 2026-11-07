from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy.interpolate import PPoly

from susceptibility import ROOT, BRANCH, PARENT, read_json, digest, save, dependencies, modest_process, Profile, TangentProblem, operator_tangent


def main():
    modest_process()
    checks, inputs = [], {}

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))

    def load(path):
        inputs[str(path)] = digest(path)
        report = read_json(path)
        assert report['state'] == 'complete'
        return report

    solved = load(ROOT/'results/tangent/status.json')
    derived = load(ROOT/'results/derivation/status.json')
    predicted = load(ROOT/'results/prediction/status.json')
    previous = load(PARENT/'results/nodes/status.json')
    check('19 exact identities', derived['exact_checks'] == 19 and all(row['passed'] and row['residual']=='0' for row in derived['checks']))
    for name, script in [('tangent', 'solve_susceptibility.py'), ('derivation', 'derive_susceptibility.py'), ('prediction', 'predict_response.py')]:
        report = read_json(ROOT/'results'/name/'status.json')
        check(name+' script hash', report['script_sha256'] == digest(ROOT/script))
        check(name+' dependencies unchanged', all(Path(path).is_file() and digest(path)==expected for path, expected in report['input_hashes'].items()))
        check(name+' payload hashes', all(digest(ROOT/'results'/name/path)==expected for path, expected in report.get('output_hashes', {}).items()))
    reference = next(row for row in solved['rows'] if row['label']=='refined')
    numerical_refinements = {}
    for row in solved['rows']:
        check(row['label']+' solver residual', row['maximum_rms_residual'] <= 1.001*row['tolerance'], row['maximum_rms_residual'])
        check(row['label']+' boundary residual', row['maximum_boundary_residual'] < 1e-11, row['maximum_boundary_residual'])
        check(row['label']+' center normalization derivative', abs(row['normalization_derivative']) < 1e-12)
        numerical_refinements[row['label']] = abs(row['coefficient_s2']/reference['coefficient_s2']-1)
        check(row['label']+' tangent convergence', numerical_refinements[row['label']] < 1e-6, numerical_refinements[row['label']])
    for label in ['fine','coarse']:
        actual = next(row for row in solved['rows'] if row['label']==label)
        inherited = next(row for row in previous['static_boundaries'] if row['settings']==label)
        error = abs(actual['static_slope']/inherited['slope']-1)
        check(label+' static slope regression', error < 1e-9, error)
    check('positive local boundary storage coefficients', reference['static_slope'] > 0 and reference['coefficient_s2'] < 0,
        dict(stiffness=reference['static_slope'], kinetic_coefficient=-reference['coefficient_s2']))
    profile = Profile(20.,.03)
    problem = TangentProblem(profile,.04,1e-9)
    coordinates = np.linspace(.002, problem.base.upper-.001, 31)
    random = np.random.default_rng(4206)
    state = random.normal(size=(6,len(coordinates)))
    parameters = random.normal(size=4)
    left, right = random.normal(size=(2,6))
    expected_operator = operator_tangent(problem.base, coordinates, state)
    expected_boundary = problem.tangent_parameter@parameters
    operator_controls, boundary_controls = [], []
    for step in [1e-8, 1e-12]:
        problem.base.square = 1j*step/problem.base.radius**2
        independent_operator = problem.base.equation(coordinates,state,parameters).imag/step
        independent_boundary = problem.base.boundary(left,right,parameters).imag/step
        operator_error = float(np.max(abs(independent_operator-expected_operator)/(1+abs(expected_operator))))
        boundary_error = float(np.max(abs(independent_boundary-expected_boundary)/(1+abs(expected_boundary))))
        operator_controls.append(operator_error)
        boundary_controls.append(boundary_error)
        check('parent operator derivative control '+str(step), operator_error < 1e-10, operator_error)
        check('parent boundary derivative control '+str(step), boundary_error < 1e-10, boundary_error)
    problem.base.square = 0.
    with np.load(ROOT/'results/tangent/refined.npz', allow_pickle=False) as archive:
        spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        parameters = archive['parameters']
    residual = spline(coordinates,1)-problem.equation(coordinates,spline(coordinates),parameters)
    independent_residual = float(np.max(abs(residual)/(1+abs(problem.equation(coordinates,spline(coordinates),parameters)))))
    check('off-grid augmented differential equation', independent_residual < 2e-8, independent_residual)
    slope_error = predicted['maximum_fractional_slope_change_error']
    check('observed boundary-change prediction within one percent', slope_error < .01, slope_error)
    fine_nodes = [row for row in predicted['node_predictions'] if row['settings']=='fine']
    local_rate_error = max(abs(value) for row in fine_nodes for value in row['rate_errors'].values())
    action_error = max(abs(value) for row in fine_nodes for value in row['action_errors'].values())
    check('observed dynamic rate prediction within one percent', local_rate_error < .01, local_rate_error)
    check('observed dynamic action prediction within one percent', action_error < .01, action_error)
    integral_error = max(abs(value) for value in predicted['fractional_dynamic_integral_errors']['fine'])
    check('observed dynamic integrated prediction within one percent', integral_error < .01, integral_error)
    fine_integrals = np.array(predicted['integrated']['fine']['endpoint']['dynamic_polar'])
    coarse_integrals = np.array(predicted['integrated']['coarse']['endpoint']['dynamic_polar'])
    prediction_refinement = float(np.max(abs(coarse_integrals/fine_integrals-1)))
    check('predicted dynamic integral refinement', prediction_refinement < 1e-6, prediction_refinement)
    check('predicted boundary optical identities', max(row['maximum_optical_error'] for row in predicted['controls']) < 1e-8)
    check('predicted node energy/angular balance', max(row['balance_error'] for row in predicted['node_predictions']) < 1e-9)
    check('predicted carrier derivative stencil', max(row['frequency_stencil_error'] for row in predicted['node_predictions']) < 1e-7)
    slopes = [row for row in predicted['slope_predictions'] if row['settings']=='fine']
    frequency_min, frequency_max = min(row['frequency'] for row in slopes), max(row['frequency'] for row in slopes)
    scaled_remainders = [row['remainder_over_omega4'] for row in slopes]
    check('unfitted remainder has consistent quartic sign', max(scaled_remainders)<0)
    remainder_spread = max(scaled_remainders)/min(scaled_remainders)
    check('quartic remainder diagnostic across archived band', remainder_spread > .97, dict(min=min(scaled_remainders), max=max(scaled_remainders)))
    heldout = []
    directory = BRANCH/'near-circular-inspiral-20261005/results/gauss-fine'
    report = load(directory/'status.json')
    static = next(row['slope'] for row in previous['static_boundaries'] if row['settings']=='fine')
    for row in report['rows']:
        if row['sector'] != 'polar':
            continue
        path = directory/row['archive']
        inputs[str(path)] = digest(path)
        with np.load(path, allow_pickle=False) as archive:
            actual = float(archive['direct_body'][0,1])-static
        prediction = reference['coefficient_s2']*row['frequency']**2
        heldout.append(dict(frequency=row['frequency'], separation=row['separation_over_radius'],
            fractional_change_error=prediction/actual-1))
    heldout_error = max(abs(row['fractional_change_error']) for row in heldout)
    check('independent Gauss frequencies within one percent', heldout_error < .01 and len(heldout)==32, heldout_error)
    with (ROOT/'results/prediction/slope-predictions.csv').open(newline='',encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        check('rectangular slope CSV', len(rows)==340 and all(None not in row and None not in row.values() for row in rows))
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    check('no bytecode cache', not list(ROOT.rglob('__pycache__')))
    previous_seal = load(PARENT/'results/stage-integrity.json')
    check('all stage41 payloads unchanged', all(digest(PARENT/path)==expected for path, expected in previous_seal['file_hashes'].items()))
    failed = [row for row in checks if not row['passed']]
    if failed:
        print(dict(state='failed', failures=failed), flush=True)
        raise SystemExit(1)
    save('validation', __file__, dict(checks=checks, input_hashes={**inputs, **dependencies()}, exact_checks=19,
        coefficient_s2=reference['coefficient_s2'], numerical_refinements=numerical_refinements,
        operator_derivative_controls=operator_controls, boundary_derivative_controls=boundary_controls,
        off_grid_equation_residual=independent_residual, prediction_refinement=prediction_refinement,
        maximum_dynamic_slope_prediction_error=slope_error, maximum_dynamic_rate_prediction_error=local_rate_error,
        maximum_dynamic_action_prediction_error=action_error, maximum_dynamic_integral_prediction_error=integral_error,
        frequency_range=[frequency_min, frequency_max], omega_R_range=[frequency_min*profile.radius,frequency_max*profile.radius],
        unfitted_quartic_remainder_range=[min(scaled_remainders),max(scaled_remainders)],
        heldout=heldout, maximum_heldout_error=heldout_error,
        primary_pdfs=previous_seal['primary_pdfs'], source_urls=previous_seal['source_urls'],
        scope='Derived branch-local surface susceptibility, with numerical regularity controls; not a global uniqueness or spectral stability theorem.'))
    print(dict(state='complete', checks=len(checks), coefficient_s2=reference['coefficient_s2'],
        maximum_slope_prediction_error=slope_error, maximum_integral_prediction_error=integral_error,
        independent_heldout_error=heldout_error, remainder_range=[min(scaled_remainders),max(scaled_remainders)]), flush=True)


if __name__=='__main__':
    main()
