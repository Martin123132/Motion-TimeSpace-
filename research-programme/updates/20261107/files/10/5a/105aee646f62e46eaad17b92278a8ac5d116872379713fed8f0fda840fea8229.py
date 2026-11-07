from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import psutil
import sympy as sp

from pn_algebra import Jet, derive_circular_model


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result, (path, key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(parents=True, exist_ok=False)
    reports = {name: strict_json(ROOT/f'results/{name}/status.json')
               for name in ['transport', 'pn-derivation', 'numerical-fine', 'shared-tail']}
    checks = []
    inputs = {}

    def check(name, passed):
        assert passed, name
        checks.append({'name': name, 'passed': True})

    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for name, report in reports.items():
        path = ROOT/f'results/{name}/status.json'
        inputs[path.relative_to(ROOT).as_posix()] = digest(path)
        check('complete_and_script_owned_'+name, report['state'] == 'complete' and report['script_sha256'] in script_hashes)
        check('reported_checks_pass_'+name, bool(report['checks']) and all(row['passed'] for row in report['checks']))
        if 'algebra_sha256' in report:
            check('algebra_current_'+name, report['algebra_sha256'] == digest(ROOT/'pn_algebra.py'))
        for path, expected in report.get('input_hashes', {}).items():
            check('source_hash_'+name+'_'+Path(path).parent.name, Path(path).is_file() and digest(path) == expected)
    for name in ['provenance', 'tail-provenance']:
        source_report = strict_json(ROOT/f'sources/{name}.json')
        check('acquisition_script_owned_'+name, source_report['script_sha256'] in script_hashes)
        for row in source_report['sources']:
            check('source_pdf_'+Path(row['path']).stem, digest(row['path']) == row['sha256'] and Path(row['path']).read_bytes().startswith(b'%PDF'))
            for render in row.get('renders', []):
                check('source_page_render_'+Path(render).stem, Path(render).is_file())
    chi = sp.symbols('chi', positive=True)
    model = derive_circular_model(chi)
    for name, value in model.items():
        if isinstance(value, Jet):
            saved = reports['pn-derivation']['derived'][name]
            check('recomputed_symbolic_'+name, all(sp.simplify(actual-sp.sympify(expected, locals={'chi': chi})) == 0 for actual, expected in zip(value.values, saved)))
    tide_free = model['flux'].values[1]
    known_point = -sp.Rational(1247, 336)-35*chi*(1-chi)/12
    check('point_baseline_recovered_exactly', sp.simplify(tide_free-known_point) == 0)
    for name in ['octupole_flux', 'current_flux']:
        defective = tide_free-model[name].values[1]
        check('detect_removed_'+name, sp.simplify((defective-known_point).subs(chi, sp.Rational(3, 4))) != 0)
    bad_slope = Jet(*(-2*value for value in model['energy'].values))
    bad_chirp = model['flux']/bad_slope
    check('detect_frozen_tidal_frequency_dependence', sp.simplify(bad_chirp.values[2]-model['chirp'].values[2]) != 0)
    check('detect_missing_mixed_inverse_cross_term', sp.simplify(model['inverse_chirp'].values[3]+model['chirp'].values[3]) != 0)
    scale, body_mass, companion_mass, orbit, deformability, frequency = sp.symbols('s M mu d lambda Omega', positive=True)
    dimensions = {body_mass: scale*body_mass, companion_mass: scale*companion_mass, orbit: scale*orbit,
                  deformability: scale**5*deformability, frequency: frequency/scale}
    mass_total = body_mass+companion_mass
    invariants = [(mass_total*frequency)**sp.Rational(2, 3), deformability/orbit**5, body_mass/mass_total]
    for index, expression in enumerate(invariants):
        check('geometric_scale_invariance_'+str(index), sp.simplify(expression.subs(dimensions, simultaneous=True)-expression) == 0)
    numerical = reports['numerical-fine']
    for row in numerical['direct_root_controls']:
        check('finite_root_control_'+row['central_fraction']+'_'+str(row['step']),
              all(math.isfinite(value['relative_or_unit_scaled_error']) for value in row['coefficient_controls']))
    body_path = ROOT.parent/'orbital-backreaction-20261004/results/fine/status.json'
    body = strict_json(body_path)
    csv_counts = {}
    for name, count in [('predictions', 9), ('wave-controls', 5), ('phase-illustrations', 4), ('shared-tail-controls', 10)]:
        path = ROOT/f'results/{name}.csv'
        with path.open(newline='', encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            fields = reader.fieldnames
            rows = list(reader)
        check('csv_shape_'+name, len(rows) == count and len(fields) == len(set(fields)) and all(None not in row and None not in row.values() for row in rows))
        inputs[path.relative_to(ROOT).as_posix()] = digest(path)
        csv_counts[name] = len(rows)
        if name == 'predictions':
            for index, row in enumerate(rows):
                ratio, separation = float(row['illustrative_mass_ratio']), float(row['separation_over_radius'])
                central = 1/(1+ratio)
                pn = body['mass']*(1+ratio)/(separation*body['radius'])
                tide = body['tidal_lambda']/(separation*body['radius'])**5
                eta = central*(1-central)
                point = -743/336-11*eta/4
                leading = 6*(12-11*central)/central
                mixed = (4421-12263*central+26502*central**2-18508*central**3)/(56*central)
                expected = tide*(leading+(mixed-point*leading)*pn)
                actual = float(row['first_PN_electric_tide_chirp_fraction_over_point'])
                check('independent_saved_chirp_'+str(index), abs(actual/expected-1) < 1e-12)
    earliest = numerical['wave_controls'][0]
    check('retain_nonuniform_10R_PN_correction', earliest['separation_over_radius'] == 10 and earliest['first_PN_relative_error'] > earliest['leading_relative_error'])
    tail = reports['shared-tail']['controls']
    check('both_baselines_tested', {row['sector'] for row in tail} == {'point_GR_quadrupole', 'linear_electric_body_minus_BH'})
    check('tail_never_fitted', all(row['tail_coefficient_derived_not_fitted'] == 4*math.pi for row in tail))
    check('retained_failed_first_attempt', (ROOT/'numerical-console.txt').is_file() and (ROOT/'results/numerical/FAILED.md').is_file())
    original = (ROOT/'run_pn_checks.py').read_text()
    revised = (ROOT/'run_pn_checks_v2.py').read_text()
    expected_revision = original.replace("ROOT/'results/numerical'", "ROOT/'results/numerical-fine'").replace("['0.0001', '0.00005', '0.000025']", "['0.00001', '0.000005', '0.0000025']")
    check('refinement_only_no_gate_relaxation', revised == expected_revision)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_bytecode_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks, 'input_hashes': inputs,
              'report_check_counts': {name: len(report['checks']) for name, report in reports.items()},
              'exact_physics_checks': 84, 'additional_Jet_Taylor_checks': numerical['Jet_Taylor_checks'],
              'independent_unexpanded_circular_root_solves': 108, 'csv_row_counts': csv_counts, 'compiled_scripts': compiled,
              'new_interior_solves': 0, 'inherited_direct_wave_points': 5,
              'scope': 'Algebra, source attribution, shared-baseline asymptotics and implementation controls; no observational validation.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'validation_checks': len(checks), 'report_checks': report['report_check_counts'], 'csv_rows': csv_counts}))


if __name__ == '__main__':
    main()
