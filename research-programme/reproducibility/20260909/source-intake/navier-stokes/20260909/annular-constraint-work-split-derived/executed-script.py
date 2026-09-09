import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_constraint_routhian_20260909 import ConstraintRouthian

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    source = intake / 'annular-constraint-routhian-derived'
    destination = intake / 'annular-constraint-work-split-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Exact additive split of the measured differentiated-constraint forcing at fixed corrected roots. Internal canonical evolution and flux-derived inner mass rate, prescribed lifting rates, outer clock rate, and scalar endpoint accelerations are separate. Removing a component is only an attribution diagnostic, never a changed accepted solution or a derived closure.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def verify(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        prior_path = intake / 'annular-constraint-tangent-verified-full-fixture/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('independent_tangent_owner_complete', prior['state'] == 'complete' and prior['passed'] == prior['total'])
        verify('all_previous_sources_roots_and_negative_controls_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        own(Path(__file__))
        compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
        for sample in prior['samples']:
            case_name, intervals, branch = sample['case'], sample['intervals'], sample['branch']
            tag = case_name + '_N' + str(intervals) + '_' + branch
            case = json.loads((intake / 'annular-constraint-correction-initial' / (case_name + '.json')).read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            with numerical.load(source / (tag + '.npz')) as loaded:
                arrays = {name: loaded[name].copy() for name in loaded.files}
            basis = MixedActionBasis(arrays['radius'])
            system = ConstraintRouthian(basis, arrays['scalar'], arrays['defect'], arrays['defect_time'], constants, kappa, arrays['momentum'], arrays['outer_clock'][0])
            corrected, hessian = arrays['corrected'], arrays['Hessian_final']
            speed_parts, forcing_parts, residual_parts = {}, {}, {}
            for mode in ['internal', 'lifting', 'outer_clock', 'scalar_boundary']:
                step = 1e-25
                changed = ConstraintRouthian(basis, arrays['scalar'] + 1j * step * corrected[system.slices[2]] * (mode == 'internal'), arrays['defect'] + 1j * step * arrays['defect_time'] * (mode == 'lifting'), arrays['defect_time'] + 1j * step * arrays['defect_acceleration'] * (mode == 'lifting'), constants, kappa, arrays['momentum'] + 1j * step * arrays['momentum_speed'] * (mode == 'internal'), arrays['outer_clock'][0] + 1j * step * arrays['outer_clock'][1] * (mode == 'outer_clock'))
                forcing = changed.evaluate(corrected, branch == 'Gram', hessian=False)[1].imag / step
                speed = numerical.zeros_like(corrected)
                if mode == 'internal':
                    speed[0] = arrays['shift_mass_speed'][0]
                if mode == 'scalar_boundary':
                    speed[system.fixed[1:]] = arrays['endpoint_acceleration']
                speed[system.free] = numerical.linalg.solve(hessian[numerical.ix_(system.free, system.free)], -(hessian @ speed + forcing)[system.free])
                speed_parts[mode], forcing_parts[mode] = speed, forcing
                residual_parts[mode] = speed[system.slices[0]] - (arrays['shift_mass_speed'] if mode == 'internal' else 0)
            full_residual = sum(residual_parts.values())
            expected_residual = arrays['packed_speed'][system.slices[0]] - arrays['shift_mass_speed']
            verify(tag + '_parameter_forcing_split_exact', maximum(sum(forcing_parts.values()) - arrays['data_derivative']) < 1e-13)
            verify(tag + '_complete_constraint_tangent_split_exact', maximum(sum(speed_parts.values()) - arrays['packed_speed']) < 1e-12)
            verify(tag + '_mass_flux_compatibility_split_exact', maximum(full_residual - expected_residual) < 1e-14)
            no_lifting = full_residual - residual_parts['lifting']
            no_boundary_rates = residual_parts['internal'] + residual_parts['lifting']
            record = {'case': case_name, 'intervals': intervals, 'branch': branch, 'mass_rate_residual_max_by_component': {name: maximum(value) for name, value in residual_parts.items()}, 'full_mass_rate_residual_max': maximum(full_residual), 'omit_lifting_rates_diagnostic_max': maximum(no_lifting), 'omit_both_boundary_rates_diagnostic_max': maximum(no_boundary_rates), 'boundary_rates_and_lifting_removed_in_actual_result': False, 'components_are_not_individually_physical_solutions': True}
            report['samples'].append(record)
            artifact = destination / (tag + '.npz')
            numerical.savez_compressed(artifact, faces=basis.faces, full_mass_rate_residual=full_residual, **{name + '_speed': value for name, value in speed_parts.items()}, **{name + '_forcing': value for name, value in forcing_parts.items()}, **{name + '_mass_rate_residual': value for name, value in residual_parts.items()})
            report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
            save()
        verify('all_owned_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(check['passed'] for check in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
    except Exception as error:
        report.update(state='failed', failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
    if report['state'] != 'complete':
        raise SystemExit(1)
    (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')


if __name__ == '__main__':
    run()
