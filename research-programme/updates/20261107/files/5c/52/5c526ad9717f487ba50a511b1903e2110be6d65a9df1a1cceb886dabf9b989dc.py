from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import csv
import ctypes
import hashlib
import json


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot pin one CPU')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-repaired-compatibility-stage-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes, mismatches, records, csv_counts = {}, [], {}, {}

    def verify(relative, expected=None):
        path = (root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid seal source '+relative)
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    prior_path = directory/'annular-compensated-polynomial-stage-integrity-20261001.json'
    prior = json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Prior stage incomplete')
    verify(str(prior_path.relative_to(root)))
    for relative, expected in prior['hashes'].items():
        verify(relative, expected)
    names = ['annular-repaired-compatibility-attempt01', 'annular-repaired-compatibility-attempt02',
        'annular-repaired-compatibility-attribution-attempt01', 'annular-compact-baseline-probe-attempt01',
        'annular-coefficient-baseline-probe-attempt01']
    for name in names:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        failed = [row['name'] for row in report['checks'] if not row['passed']]
        if name=='annular-repaired-compatibility-attempt01':
            if report['state']!='failed' or failed!=['manufactured_feasible_orthant_replayed'] or report['cases']:
                raise RuntimeError('Unexpected first-attempt failure')
        elif report['state']!='complete' or failed:
            raise RuntimeError('Incomplete daughter '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                verify(relative, expected)
        for item in path.parent.iterdir():
            if item.is_file():
                verify(str(item.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        records[name] = dict(state=report['state'], checks=len(report['checks']), failed_checks=failed)
        for table in path.parent.glob('*.csv'):
            with table.open(newline='', encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream, strict=True))
            if any(None in row or any(value is None for value in row.values()) or row.get('valid_for_claim')!='False' for row in rows):
                raise RuntimeError('Malformed or promoted CSV')
            csv_counts[str(table.relative_to(root))] = len(rows)
    witness_count = 0
    assembly = json.loads((directory/'annular-repaired-compatibility-attempt02/status.json').read_text())
    for summary in assembly['summaries']:
        data = json.loads((root/summary['path']).read_text())
        rational = lambda value:Fraction.from_float(float(value))
        for orthant in data['envelope_search']['orthants']:
            witness = orthant['exact_witness']
            if witness is None:
                continue
            amplitudes = [orthant['signs'][column]*Fraction(int(witness['numerator'][column]), int(witness['denominator'])) for column in range(3)]
            for row in range(4):
                residual = rational(data['baseline'][row])+sum(rational(data['columns'][row][column])*amplitudes[column] for column in range(3))
                bound = rational(data['baseline_error'][row])+sum(rational(data['column_error'][row][column])*abs(amplitudes[column]) for column in range(3))
                if abs(residual)>bound:
                    raise RuntimeError('Exact original-equation witness does not replay')
            witness_count += 1
    compiled = []
    for name in ['assemble_annular_repaired_compatibility_20261001.py', 'annular_exact_envelope_20261001.py',
            'assemble_annular_repaired_compatibility_v2_20261001.py', 'attribute_annular_repaired_compatibility_20261001.py',
            'annular_compact_baseline_current_20261001.py', 'probe_annular_compact_baseline_20261001.py',
            'annular_weighted_current_polynomial_20261001.py', 'annular_compact_baseline_current_v2_20261001.py',
            'probe_annular_coefficient_baseline_20261001.py', 'seal_annular_repaired_compatibility_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-repaired-coupled-compatibility.md', 'DERIVATION-20261001-exact-envelope-vertices.md',
            'DERIVATION-20261001-compact-baseline-current.md', 'DERIVATION-20261001-coefficient-weighted-current.md',
            'RESULTS-20261001-repaired-coupled-equations.md']:
        verify(name)
    started = datetime(2026, 10, 1, 12, 45, 30, tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=[str(path) for path in bytecode]))
    seal = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes, mismatches=mismatches,
        unique_files_rehashed=len(hashes), authorities=records, scripts_compiled=compiled, csv_rows=csv_counts,
        exact_original_equation_witnesses_replayed=witness_count, assembly_variants=len(assembly['summaries']),
        all_sampled_rank_checks_pass=all(row['rank_resolved'] for row in assembly['summaries']),
        central_C2_replaced=True, genuine_source_sensitivities_retained=True,
        exact_feasibility_scope='independent_componentwise_sampled_envelopes_for_supplied_binary64_inputs',
        baseline_budget_dependence_attributed=True, compact_current_derived=True, weighted_interpolation_cancellation_derived=True,
        baseline_integral_replaced=False, velocity_integral_replaced=False, finite_history_established=False,
        protected_workbench_changed_since_turn_start=len(changed), pending={}, current_resume_excluded=True,
        bytecode_cache_present=False, github_action=False, subagents_used=False, valid_for_physics_claim=False)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(seal, indent=2)+'\n')
    print(json.dumps({key:value for key, value in seal.items() if key!='hashes'}, indent=2), flush=True)


if __name__=='__main__':
    main()
