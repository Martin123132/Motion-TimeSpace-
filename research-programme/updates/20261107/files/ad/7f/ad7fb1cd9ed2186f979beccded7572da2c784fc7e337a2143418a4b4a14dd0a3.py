from __future__ import annotations

from pathlib import Path
import csv
import sys

import numpy as np

from budget import (ROOT, BRANCH, PARENT, digest, read_json, save, modest_process, dependencies,
                    RateCurve, frozen_boundary, sideband_response, sideband_flux, project_rates)


def main():
    modest_process()
    checks, inputs = [], {}

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))

    def load(path):
        inputs[str(path)] = digest(path)
        result = read_json(path)
        assert result['state'] == 'complete'
        return result

    nodes = load(ROOT/'results/nodes/status.json')
    integrals = load(ROOT/'results/integrals/status.json')
    derivation = load(ROOT/'results/derivation/status.json')
    check('eight exact algebra identities', len(derivation['checks']) == 8 and
          all(row['passed'] and row['residual'] == '0' for row in derivation['checks']))
    for name, script in [('nodes', 'build_budget.py'), ('integrals', 'integrate_budget.py'), ('derivation', 'derive_budget.py')]:
        report = read_json(ROOT/'results'/name/'status.json')
        check(name+' authoring script unchanged', report['script_sha256'] == digest(ROOT/script))
        check(name+' all hashed inputs unchanged', all(Path(path).is_file() and digest(path) == expected
              for path, expected in report['input_hashes'].items()), len(report['input_hashes']))
    diagnostics = [row for row in nodes['controls'] if row['role'] != 'frequency_stencil']
    maxima = dict(direct=max(row['maximum_direct_error'] for row in diagnostics),
        optical=max(row['maximum_optical_error'] for row in diagnostics),
        recovered_current=max(row['current_beta_relative_error'] or 0. for row in diagnostics),
        small_current_branch=max(row['small_current_branch'] for row in diagnostics),
        stencil=max(row['frozen_power2_error'] for row in nodes['controls'] if row['role'] == 'frequency_stencil'),
        balance=max(row['balance_error'] for row in nodes['nodes']),
        archived_regression=max(value for row in nodes['regressions'] for key, value in row.items() if key.endswith('_error')))
    for name, threshold in [('direct', 2e-12), ('optical', 1e-8), ('recovered_current', 2e-12),
                            ('small_current_branch', 1e-5), ('stencil', 1e-7), ('balance', 2e-9), ('archived_regression', 2e-10)]:
        check(name+' control', maxima[name] < threshold, dict(value=maxima[name], threshold=threshold))
    for label in ['fine', 'coarse']:
        rows = [row for row in nodes['nodes'] if row['settings'] == label]
        check(label+' unique grid/component rows', len(rows) == 102 and
              len({(row['separation'], row['component']) for row in rows}) == 102)
        check(label+' inward baseline and damping', all(row['P0'] < 0 and row['G0'] < 0
              for row in rows if row['component'] == 'point_out'))
    for name, errors in integrals['comparisons']['coarse'].items():
        check(name+' fine/coarse integral refinement', max(errors) < 1e-6, max(errors))
    for name, errors in integrals['comparisons']['nested9'].items():
        if name != 'wave_square':
            check(name+' nested-nine primary-order refinement', max(errors) < 1e-6, max(errors))
    check('quadratic-wave diagnostic not accepted from nine nodes',
        max(integrals['comparisons']['nested9']['wave_square']) > 1e-6)
    check('five nodes not accepted for frequency-response budget',
        max(integrals['comparisons']['nested5']['dynamic_polar']) > 1e-6)
    maximum_quadrature = max(row['quadrature_error'] for row in integrals['runs'].values())
    check('independent clock quadratures', maximum_quadrature < 2e-10, maximum_quadrature)
    sys.path.insert(0, str(PARENT))
    from inspiral import analytic_coefficients
    source_body = nodes['static_boundaries'][0]
    mass, radius, deformability = [source_body[key] for key in ['mass', 'radius', 'tidal_lambda']]
    initial = 10*radius/mass
    initial_tide = deformability/(10*radius)**5
    exact = analytic_coefficients(0., .5)
    time_factor, phase_factor = 5/64*initial**4, 5/64*initial**2.5
    exact_point = np.array([19/6*np.log(.5), exact[2]*time_factor, exact[6]*phase_factor,
                           exact[3]*time_factor, exact[7]*phase_factor])
    exact_tide = initial_tide*np.array([exact[1]/exact[0], exact[4]*time_factor, exact[8]*phase_factor,
                                      exact[5]*time_factor, exact[9]*phase_factor])
    weak_error = max(float(np.max(abs(np.array(integrals['runs']['weak']['endpoint'][name])/expected-1)))
                     for name, expected in [('point_out', exact_point), ('weak_tide', exact_tide)])
    check('stage40 same-action-eccentricity frequency-endpoint limit', weak_error < 2e-10, weak_error)
    budget = integrals['budget']
    closure = np.array(budget['weak_tide'])+budget['frozen_remainder']+budget['dynamic_polar']+budget['odd_response']
    closure_error = float(np.max(abs(closure/np.array(budget['full_outgoing'])-1)))
    check('signed budget adds back to total', closure_error < 1e-13, closure_error)
    directory = BRANCH/'near-circular-inspiral-20261005/results/gauss-fine'
    gauss = load(directory/'status.json')
    fine_nodes = [row for row in nodes['nodes'] if row['settings']=='fine']
    components = ['point_out', 'horizon', 'frozen_polar', 'dynamic_polar', 'odd_response', 'wave_square']
    curves = {name:RateCurve(fine_nodes, name, mass, radius) for name in components}
    heldout, heldout_diagnostics = [], []
    for separation in gauss['requested_separations']:
        circular = {name:[] for name in components}
        sidebands = {name:[] for name in components}
        for row in [row for row in gauss['rows'] if abs(row['separation_over_radius']-separation) < 1e-10]:
            response = sideband_response(row)
            full = sideband_flux(response)
            if row['sector'] == 'polar':
                path = directory/row['archive']
                inputs[str(path)] = digest(path)
                with np.load(path, allow_pickle=False) as archive:
                    frozen_row, diagnostic = frozen_boundary(response, archive, source_body['slope'])
                frozen = sideband_flux(frozen_row)
                heldout_diagnostics.append(diagnostic)
            for name in components:
                value = (0. if name in ['frozen_polar', 'dynamic_polar'] and row['sector'] != 'polar' else
                    full['reference'] if name == 'point_out' else full['horizon'] if name == 'horizon' else
                    full['nonlinear_difference'] if name == 'wave_square' else
                    frozen['difference'] if name == 'frozen_polar' else
                    full['difference']-frozen['difference'] if name == 'dynamic_polar' else
                    full['difference'] if row['sector'] == 'odd' else 0.)
                if row['harmonic'] == 0:
                    circular[name].append(dict(azimuth=row['azimuth'], frequency=row['frequency'],
                        alpha=0., power0=value, power2=0.))
                else:
                    sidebands[name].append(dict(azimuth=row['azimuth'], harmonic=row['harmonic'], frequency=row['frequency'], power=value))
        for name in components:
            direct = project_rates(mass, separation*radius/mass, circular[name], sidebands[name])
            predicted = curves[name].rates(separation)
            heldout.append(dict(separation=separation, component=name,
                P0_error=abs(predicted['P0']/direct['P0']-1), G0_error=abs(predicted['G0']/direct['G0']-1)))
    maximum_heldout = max(max(row['P0_error'], row['G0_error']) for row in heldout)
    check('held-out archived Gauss waves reproduce P0/G0 components', maximum_heldout < 1e-6, maximum_heldout)
    check('held-out frozen optical identities', max(row['maximum_optical_error'] for row in heldout_diagnostics) < 1e-8)
    raw_rows = 0
    for path in ROOT.rglob('*.csv'):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            check('rectangular CSV '+path.name, bool(rows) and len(reader.fieldnames) == len(set(reader.fieldnames))
                and all(None not in row and None not in row.values() for row in rows))
            raw_rows += len(rows)
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    check('no bytecode cache', not list(ROOT.rglob('__pycache__')))
    previous = load(PARENT/'results/stage-integrity.json')
    check('all stage40 files unchanged', all(digest(PARENT/relative) == expected for relative, expected in previous['file_hashes'].items()))
    failed = [row for row in checks if not row['passed']]
    if failed:
        print(dict(state='failed', failed=failed), flush=True)
        raise SystemExit(1)
    save('validation', __file__, dict(checks=checks, input_hashes={**inputs, **dependencies()},
        exact_checks=8, maxima=maxima, maximum_quadrature_error=maximum_quadrature,
        stage40_weak_limit_error=weak_error, maximum_heldout_error=maximum_heldout,
        heldout=heldout, heldout_frozen_controls=heldout_diagnostics, csv_rows=raw_rows,
        primary_pdfs=previous['primary_pdfs'], source_urls=previous['source_urls'],
        approximation='leading test mass, retained ell2 modes; operational surface-response split; not a physical all-orders waveform uncertainty bound.'))
    print(dict(state='complete', checks=len(checks), weak_limit=weak_error, maximum_heldout=maximum_heldout,
        maxima=maxima, csv_rows=raw_rows), flush=True)


if __name__ == '__main__':
    main()
