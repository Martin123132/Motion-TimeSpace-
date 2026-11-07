from __future__ import annotations

import csv
from pathlib import Path
import numpy as np
from scipy import linalg

from polar_energy import ROOT, BRANCH, PARENT, read_json, save, dependencies, digest, modest_process, whiten


def main():
    modest_process()
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))
        assert passed, (name, value)

    exact = read_json(ROOT/'results/exact/status.json')
    independent = read_json(ROOT/'results/independent/status.json')
    check('21 action identities', len(exact['checks']) == 21 and all(row['passed'] and row['residual'] == '0' for row in exact['checks']))
    check('5 independent tensor identities', len(independent['exact_checks']) == 5 and all(row['passed'] and row['residual'] == '0' for row in independent['exact_checks']))
    check('nonlinear second variations', independent['largest_finest_error'] < 2e-8, independent['largest_finest_error'])
    constraint = read_json(ROOT/'results/constraint-control/status.json')
    check('manufactured constraint L2 convergence', 3.9 < constraint['last_halving_ratios']['l2'] < 4.1, constraint['last_halving_ratios']['l2'])
    check('manufactured gradient convergence', 1.95 < constraint['last_halving_ratios']['gradient'] < 2.05, constraint['last_halving_ratios']['gradient'])
    check('background ground state numerical identity', all(row['background_ground_state_form_error'] < 1e-8 for row in constraint['rows']))
    flat_reference_path = BRANCH/'dynamical-tides-20261004/results/flat-mode/status.json'
    flat_reference = read_json(flat_reference_path)
    check('independent flat reference complete', flat_reference['state'] == 'complete')
    flats = {label:read_json(ROOT/'results'/label/'status.json') for label in ['flat8', 'flat16', 'flat24', 'flat32', 'flat48']}
    flat_error = abs(flats['flat48']['frequencies'][0]/flat_reference['sigma']-1)
    check('canonical Hamiltonian reproduces independent flat mode', flat_error < 1e-9, flat_error)
    check('flat basis convergence', abs(flats['flat32']['frequencies'][0]/flats['flat48']['frequencies'][0]-1) < 1e-8)
    control_ratio = flats['flat48']['deleted_cross_frequency']/flats['flat48']['frequencies'][0]
    check('omitted phase mixing is detected', control_ratio > 5, control_ratio)
    labels = ['pilot', 'standard', 'refined-mesh', 'enlarged', 'support6', 'support-expanded', 'resolved', 'resolved-more', 'resolved-mesh', 'resolved-support', 'support-mesh']
    results = {label:read_json(ROOT/'results'/label/'status.json') for label in labels}
    for label, result in results.items():
        check(label+' positive discrete even/odd forms', result['even_min'] > 0 and result['odd_min'] > 0)
        check(label+' positive discrete frequency squares', result['negative_squares'] == 0 and result['frequency_squares'][0] > 0)
        check(label+' linear constraint residual', result['constraint_residual'] < 1e-9, result['constraint_residual'])
        check(label+' symmetric matrices', max(result['even_symmetry_error'], result['odd_symmetry_error']) < 1e-12)
    check('label support6 is explicitly a repeat not support control', results['support6']['configuration'] == results['standard']['configuration'])
    check('actual expanded support uses six radii', results['support-expanded']['configuration']['extent'] == 6 and results['support-mesh']['configuration']['extent'] == 6)
    refined_change = abs(results['resolved-more']['frequencies'][0]/results['resolved-mesh']['frequencies'][0]-1)
    support_mesh_change = abs(results['resolved-support']['frequencies'][0]/results['support-mesh']['frequencies'][0]-1)
    check('4R lowest Ritz frequency mesh control', refined_change < 2e-7, refined_change)
    check('6R lowest Ritz frequency mesh control', support_mesh_change < 2e-7, support_mesh_change)
    support_eigenvalue_change = abs(results['resolved-support']['even_min']/results['support-mesh']['even_min']-1)
    check('smallest energy eigenvalue remains explicitly mesh sensitive', support_eigenvalue_change > .1, support_eigenvalue_change)
    with np.load(ROOT/'results/pilot/forms.npz') as arrays:
        cholesky = linalg.cholesky(arrays['gram'], lower=True)
        even, odd = whiten(arrays['even'], cholesky), whiten(arrays['odd'], cholesky)
    size = len(even)
    signs = np.diag(np.r_[np.ones(12), -np.ones(8)])
    evolution = np.block([[np.zeros_like(even), signs@odd], [-signs@even, np.zeros_like(even)]])
    hessian = linalg.block_diag(even, odd)
    conservation = evolution.T@hessian+hessian@evolution
    conservation_error = float(np.linalg.norm(conservation)/(np.linalg.norm(evolution)*np.linalg.norm(hessian)))
    check('canonical evolution conserves quadratic energy', conservation_error < 1e-13, conservation_error)
    eigenvalues = linalg.eigvals(evolution)
    direct_frequencies = np.sort(eigenvalues.imag[eigenvalues.imag > 0])
    direct_error = float(np.max(abs(direct_frequencies/np.array(results['pilot']['frequencies'])-1)))
    check('first order and squared eigenproblems agree', direct_error < 1e-9, direct_error)
    check('projected evolution has imaginary eigenvalues', max(abs(eigenvalues.real)) < 1e-10)
    outgoing_path = BRANCH/'dynamical-tides-20261004/results/mode-edge002/status.json'
    outgoing = read_json(outgoing_path)
    check('comparison uses successful outgoing solve', outgoing['state'] == 'complete')
    outgoing_difference = abs(results['support-mesh']['frequencies'][0]/outgoing['sigma']['real']-1)
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        check(str(path.relative_to(ROOT))+' complete', report['state'] == 'complete')
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
        for relative, expected in report.get('output_hashes', {}).items():
            assert digest(path.parent/relative) == expected, (path, relative)
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    check('no bytecode cache', not list(ROOT.rglob('__pycache__')))
    summary_rows = []
    for label, result in {**flats, **results}.items():
        summary_rows.append(dict(label=label, flat=label.startswith('flat'), matter_count=result['configuration']['matter_count'], gravity_count=result['configuration'].get('gravity_count', 0), body_cells=result['configuration']['body_cells'], outer_cells=result['configuration'].get('outer_cells', 0), extent=result['configuration'].get('extent', 1), even_min=result['even_min'], odd_min=result['odd_min'], lowest_Ritz_frequency=result['frequencies'][0], linear_constraint_residual=result.get('constraint_residual', ''), interpretation='flat mode control' if label.startswith('flat') else 'finite discretized energy test; not outgoing spectrum'))
    parent = read_json(PARENT/'results/validation/status.json')
    for source in parent['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    inputs = dependencies()
    inputs.update({str(path):digest(path) for path in [flat_reference_path, outgoing_path, *sorted(ROOT.glob('results/*/status.json'))]})
    report = save('validation', Path(__file__), dict(input_hashes=inputs, validation_checks=len(checks), checks=checks,
        exact_checks=26, coupled_discrete_runs=len(results), flat_runs=len(flats), manufactured_constraint_runs=4,
        flat_reference_frequency=flat_reference['sigma'], flat_measured_frequency=flats['flat48']['frequencies'][0],
        flat_relative_difference=flat_error, phase_mixing_deletion_frequency=flats['flat48']['deleted_cross_frequency'],
        lowest_Ritz_mesh_relative_change_4R=refined_change, lowest_Ritz_mesh_relative_change_6R=support_mesh_change,
        smallest_even_eigenvalue_mesh_relative_change_6R=support_eigenvalue_change,
        outgoing_reference_real_frequency=outgoing['sigma']['real'], Ritz_outgoing_relative_difference=outgoing_difference,
        Ritz_is_outgoing_resonance=False, continuum_even_positivity_proved=False, continuum_gap_claimed=False,
        odd_block_sum_of_squares_derived=True, positive_ground_state_constraint_identity_derived=True,
        independent_phase_restored=True, csv_rows=len(summary_rows), primary_pdfs=parent['primary_pdfs'], source_urls=parent['source_urls'],
        label_note='support6 accidentally repeats the 4R standard settings; retained as repeat. support-expanded and resolved-support/support-mesh are actual 6R controls.',
        no_new_background_or_outgoing_wave_solves=True))
    with (ROOT/'results/validation/run-summary.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)
    print(dict(state=report['state'], checks=len(checks), flat_error=flat_error, phase_control=control_ratio, outgoing_difference=outgoing_difference, smallest_energy_mesh_change=support_eigenvalue_change), flush=True)


if __name__ == '__main__':
    main()
