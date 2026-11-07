from pathlib import Path
import csv

import numpy as np
import sympy as sp

from interior_energy import ROOT, PARENT, TANGENT, Interior, dependencies, digest, read_json, save, modest_process


def main():
    modest_process()
    checks, inputs = [], dependencies()

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
        assert passed, (name, detail)

    reports = {}
    scripts = {'probe':'probe_interior.py', 'vacuum-canonical':'derive_vacuum_contact.py',
               'match':'match_interior.py', 'action-derivation':'derive_action.py',
               'nonlinear-action-check':'nonlinear_density_check.py'}
    for label, script in scripts.items():
        path = ROOT/'results'/label/'status.json'
        report = read_json(path)
        reports[label] = report
        inputs[str(path)] = digest(path)
        check(label+' completion and script', report['state'] == 'complete' and report['script_sha256'] == digest(ROOT/script))
        check(label+' source hashes', all(digest(source) == expected for source, expected in report['input_hashes'].items()))
    exact = reports['action-derivation']
    check('19 action identities', len(exact['checks']) == exact['exact_checks'] == 19 and
          all(row['passed'] and row['residual'] == '0' for row in exact['checks']))
    vacuum = reports['vacuum-canonical']
    check('off-shell vacuum contact identity', vacuum['residual'] == '0' and vacuum['canonical_normalization_times_alpha'] == '3/2')
    namespace = {name:sp.Symbol(name, positive=True) for name in ['r', 'M']}
    namespace.update({name:sp.Symbol(name, real=True) for name in ['Z', 'V']})
    contact_expression = sp.sympify(vacuum['boundary_contact_times_alpha'], locals=namespace)
    contact = sp.lambdify(list(namespace.values()), contact_expression, 'numpy')
    radius, mass, master, slope = list(namespace.values())
    flat_expected = (5*radius*master**2+2*radius**2*master*slope-radius**3*slope**2)/4
    check('independent flat vacuum contact limit', sp.factor(contact_expression.subs(mass, 0)-flat_expected) == 0)
    rows, refinements = [], []
    for label in ['coarse', 'fine', 'refined', 'edge_check']:
        interior = Interior(label)
        inputs[str(interior.archive_path)] = digest(interior.archive_path)
        inputs[str(interior.profile.path)] = digest(interior.profile.path)
        baseline = interior.integral(order=48, cells=80)
        lower_order = interior.integral(order=24, cells=80)
        doubled_cells = interior.integral(order=32, cells=160)
        scale = abs(sum(baseline))
        order_error = float(max(abs(baseline-lower_order))/scale)
        cell_error = float(max(abs(baseline-doubled_cells))/scale)
        check(label+' quadrature order', order_error < 2e-8, order_error)
        check(label+' quadrature cells', cell_error < 2e-8, cell_error)
        refinements.append(dict(label=label, order_error=order_error, cell_error=cell_error))
        surface = interior.row['static_master']
        normalization = 1.5/interior.alpha
        conversion = normalization*surface[0]**2
        terms = baseline/conversion
        contact_A = float(contact(interior.radius, interior.mass, *surface)/(1.5*surface[0]**2))
        predicted = float(sum(terms)-contact_A)
        target = -interior.row['coefficient_s2']
        relative_error = predicted/target-1
        check(label+' independently action-derived storage matches response',
              abs(relative_error) < 1e-6, relative_error)
        check(label+' positive matched coefficient', predicted > 0 and target > 0)
        match = next(row for row in reports['match']['rows'] if row['label'] == label)
        check(label+' replay of saved match', abs(predicted/match['predicted_A']-1) < 1e-12)
        omitted_contact = float(sum(terms))
        omitted_gravity = predicted-float(terms[0])
        omitted_phase = predicted-float(sum(terms[2:]))
        check(label+' omitting canonical surface conversion fails', abs(omitted_contact/target-1) > .1)
        check(label+' omitting gravitational kinetic term fails', abs(omitted_gravity/target-1) > .05)
        check(label+' omitting phase terms fails', abs(omitted_phase/target-1) > .5)
        center = interior.problem.lower*interior.radius
        center_estimate = float(sum(interior.density(np.array([center]))[:, 0])*center/7/conversion)
        check(label+' center-cutoff power-counting estimate negligible', abs(center_estimate/target) < 1e-18, center_estimate)
        rows.append(dict(label=label, distance=interior.row['distance'],
            gravity=float(terms[0]), amplitude=float(terms[1]), rotating_phase=float(terms[2]),
            shift_phase=float(terms[3]), phase_gradient=float(terms[4]), surface_conversion=-contact_A,
            derived_A=predicted, response_A=target, relative_error=relative_error,
            omitted_contact_A=omitted_contact, omitted_gravity_A=omitted_gravity,
            omitted_phase_A=omitted_phase, center_cutoff_estimate=center_estimate))
    lookup = {row['label']:row for row in rows}
    ratio = abs(lookup['refined']['relative_error']/lookup['coarse']['relative_error'])
    check('edge-distance halving has observed cubic mismatch scaling', 7.5 < ratio < 8.5, ratio)
    edge_constants = [abs(lookup[label]['relative_error'])/lookup[label]['distance']**3
                      for label in ['coarse', 'refined', 'edge_check']]
    check('three distinct edge joins share cubic scaling', max(edge_constants)/min(edge_constants)-1 < .02,
          edge_constants)
    nonlinear = reports['nonlinear-action-check']['rows']
    for fraction in [.15, .4, .7, .9, .97]:
        subset = [row for row in nonlinear if row['radius_fraction'] == fraction]
        errors = [abs(row['relative_error']) for row in subset]
        check('nonlinear action density '+str(fraction), errors[-1] < 1e-7, errors[-1])
        check('finite variation converges '+str(fraction),
              all(following < previous/3+5e-12 for previous, following in zip(errors[:-1], errors[1:])), errors)
        check('finite variation stays on positive-amplitude branch '+str(fraction),
              max(row['largest_fractional_amplitude_change'] for row in subset) < .2)
    check('signed local gravity density not mislabeled positive',
          any(row['expected_mass_density'] < 0 for row in nonlinear) and any(row['expected_mass_density'] > 0 for row in nonlinear))
    check('no bytecode cache', not list(ROOT.rglob('__pycache__')))
    parent = read_json(PARENT/'results/stage-integrity.json')
    check('stage43 sealed payloads unchanged',
          all(digest(PARENT/source) == expected for source, expected in parent['file_hashes'].items()))
    directory = ROOT/'results/validation'
    directory.mkdir(parents=True, exist_ok=False)
    table = directory/'canonical-components.csv'
    with table.open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with table.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        parsed = list(reader)
        check('component CSV rectangular and complete',
              len(parsed) == 4 and len(reader.fieldnames) == len(set(reader.fieldnames)) and
              all(None not in row and None not in row.values() for row in parsed))
    report = dict(state='complete', script_sha256=digest(__file__),
        input_hashes=inputs, output_hashes={table.name:digest(table)}, checks=checks,
        exact_action_checks=19, exact_vacuum_conversion_checks=1, validation_checks=len(checks),
        rows=rows, quadrature_refinements=refinements, edge_halving_mismatch_ratio=ratio,
        largest_action_response_mismatch=max(abs(row['relative_error']) for row in rows),
        largest_finest_nonlinear_density_error=max(abs(row['relative_error']) for row in nonlinear if row['epsilon'] == .0005),
        csv_rows=4, canonical_normalization=1.5/Interior('refined').alpha,
        new_interior_or_background_solves=0, new_wave_solves=0, fitted_coefficients=0,
        source_of_action_match='Only the saved static block and divided phase/shift are integrated; the saved s2 is a held-aside comparison target.',
        energy_convention='Rotating-frame canonical energy / fixed-charge Routhian E-wQ.',
        positive_claim='Positive matched coefficient on this driven branch; local ADM density is signed; full polar Hamiltonian not diagonalized.',
        primary_pdfs=parent['primary_pdfs'], source_urls=parent['source_urls'])
    from datetime import datetime, timezone
    report['time_utc'] = datetime.now(timezone.utc).isoformat()
    from interior_energy import write_json
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    print(dict(state='complete', validation_checks=len(checks),
               largest_action_response_mismatch=report['largest_action_response_mismatch'],
               largest_finest_nonlinear_density_error=report['largest_finest_nonlinear_density_error'],
               edge_ratio=ratio, components=lookup['refined']), flush=True)


if __name__ == '__main__':
    main()

