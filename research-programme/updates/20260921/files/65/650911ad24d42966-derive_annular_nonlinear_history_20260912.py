import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_nonlinear_history_20260912 import ManufacturedHistory, HistoryAction

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Fresh alphanumeric attempt required.')
    root = Path(__file__).resolve().parents[1]
    destination = root / 'source-intake/navier-stokes/20260912' / ('annular-nonlinear-history-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'inputs': {}, 'outputs': {}, 'cases': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'manufactured_histories_only': True}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        for name in [Path(__file__).name, 'annular_nonlinear_history_20260912.py']:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        for name in ['DERIVATION-20260911-canonical-action-and-boundary-consistent-initial-data.md', 'DERIVATION-20260911-coupled-initial-jet-and-exact-time-link-adjoint.md', 'DERIVATION-20260909-covariant-time-links-and-mixed-gravity-basis.md']:
            own(root / name)
        radius, mass, lapse, momentum, scalar_momentum, gradient, mass_r, lapse_r, momentum_r, scalar_momentum_r, gradient_r, kappa = symbolic.symbols('R mu N P pi w mu_R N_R P_R pi_R w_R kappa', positive=True)
        geometry = 1 - 2 * mass / radius
        geometry_r = -2 * mass_r / radius + 2 * mass / radius**2
        energy = scalar_momentum**2 / (2 * radius**2) + radius**2 * gradient**2 / 2
        cross = kappa * lapse * geometry**symbolic.Rational(3, 2) * momentum * scalar_momentum * gradient
        quadratic = kappa * radius * geometry**3 * (-lapse * geometry_r / (2 * geometry**symbolic.Rational(3, 2)) + lapse_r / symbolic.sqrt(geometry)) * momentum**2 / 2
        hamiltonian = -lapse * mass_r / (kappa * symbolic.sqrt(geometry)) + lapse * symbolic.sqrt(geometry) * energy + cross + quadratic

        def radial_derivative(expression):
            return symbolic.diff(expression, radius) + sum(symbolic.diff(expression, field) * derivative for field, derivative in [(mass, mass_r), (lapse, lapse_r), (momentum, momentum_r), (scalar_momentum, scalar_momentum_r), (gradient, gradient_r)])

        mass_rate = kappa * lapse * geometry**symbolic.Rational(3, 2) * scalar_momentum * gradient + kappa * radius * geometry**symbolic.Rational(3, 2) * (geometry * lapse_r - lapse * geometry_r / 2) * momentum
        scalar_rate = lapse * symbolic.sqrt(geometry) * scalar_momentum / radius**2 + kappa * lapse * geometry**symbolic.Rational(3, 2) * momentum * gradient
        momentum_rate = lapse * energy / (radius * symbolic.sqrt(geometry)) - lapse_r / (kappa * symbolic.sqrt(geometry)) + lapse * mass / (kappa * radius**2 * geometry**symbolic.Rational(3, 2))
        momentum_rate += 3 * kappa * lapse * symbolic.sqrt(geometry) * momentum * scalar_momentum * gradient / radius
        momentum_rate += kappa * geometry**symbolic.Rational(3, 2) * ((lapse / (2 * radius) + 3 * lapse_r) * momentum**2 + lapse * momentum * momentum_r)
        scalar_flux = lapse * symbolic.sqrt(geometry) * radius**2 * gradient + kappa * lapse * geometry**symbolic.Rational(3, 2) * momentum * scalar_momentum
        constraint = mass_r / (kappa * symbolic.sqrt(geometry)) - symbolic.sqrt(geometry) * energy - kappa * geometry**symbolic.Rational(3, 2) * momentum * scalar_momentum * gradient
        constraint += kappa * geometry**symbolic.Rational(3, 2) * ((geometry / 2 - 3 * mass_r + 3 * mass / radius) * momentum**2 + radius * geometry * momentum * momentum_r)
        checks = {
            'full_GR_mass_rate': symbolic.diff(hamiltonian, momentum) - mass_rate,
            'full_GR_scalar_rate': symbolic.diff(hamiltonian, scalar_momentum) - scalar_rate,
            'full_GR_P_rate': -symbolic.diff(hamiltonian, mass) + radial_derivative(symbolic.diff(hamiltonian, mass_r)) - momentum_rate,
            'full_GR_scalar_flux': symbolic.diff(hamiltonian, gradient) - scalar_flux,
            'full_GR_lapse_constraint': -symbolic.diff(hamiltonian, lapse) + radial_derivative(symbolic.diff(hamiltonian, lapse_r)) - constraint,
            'bulk_linear_lapse': symbolic.diff(hamiltonian, lapse, 2) + symbolic.diff(hamiltonian, lapse_r, 2),
        }
        velocity, mass_velocity = symbolic.symbols('q mu_t', real=True)
        shift = kappa * lapse * geometry**symbolic.Rational(3, 2) * momentum
        weak_lagrangian = lapse * mass_r / (kappa * symbolic.sqrt(geometry)) + shift * mass_velocity / (kappa * lapse * geometry**symbolic.Rational(3, 2))
        weak_lagrangian -= radius * (lapse_r / symbolic.sqrt(geometry) - lapse * geometry_r / (2 * geometry**symbolic.Rational(3, 2))) * shift**2 / (2 * kappa * lapse**2)
        weak_lagrangian += radius**2 * (velocity - shift * gradient)**2 / (2 * lapse * symbolic.sqrt(geometry)) - radius**2 * lapse * symbolic.sqrt(geometry) * gradient**2 / 2
        first_order = momentum * mass_velocity + scalar_momentum * velocity - hamiltonian
        checks['nonzero_P_bulk_auxiliary_elimination'] = first_order.subs(scalar_momentum, radius**2 * (velocity - shift * gradient) / (lapse * symbolic.sqrt(geometry))) - weak_lagrangian
        chart_parameter = kappa**2 * geometry**2 * momentum**2
        chart = 1 - chart_parameter
        connection = kappa * symbolic.sqrt(geometry) * momentum / (lapse * chart)
        coefficient = radius**2 * lapse * symbolic.sqrt(geometry) * chart
        checks.update({
            'c_P': symbolic.diff(connection, momentum) - kappa * symbolic.sqrt(geometry) * (1 + chart_parameter) / (lapse * chart**2),
            'c_mu': symbolic.diff(connection, mass) + kappa * momentum * (1 + 3 * chart_parameter) / (radius * lapse * symbolic.sqrt(geometry) * chart**2),
            'c_N': symbolic.diff(connection, lapse) + connection / lapse,
            'C_P': symbolic.diff(coefficient, momentum) + 2 * kappa**2 * radius**2 * lapse * geometry**symbolic.Rational(5, 2) * momentum,
            'C_mu': symbolic.diff(coefficient, mass) + radius * lapse * (1 - 5 * chart_parameter) / symbolic.sqrt(geometry),
            'C_N': symbolic.diff(coefficient, lapse) - radius**2 * symbolic.sqrt(geometry) * chart,
            'P0_connection': connection.subs(momentum, 0),
            'P0_direct_P_coefficient': symbolic.diff(coefficient, momentum).subs(momentum, 0),
            'P0_transport_mu': symbolic.diff(connection, mass).subs(momentum, 0),
            'P0_transport_N': symbolic.diff(connection, lapse).subs(momentum, 0),
            'P0_P_coupling': symbolic.diff(connection, momentum).subs(momentum, 0) - kappa * symbolic.sqrt(geometry) / lapse,
        })
        for name, expression in checks.items():
            check(name, symbolic.simplify(expression) == 0)
        print('Exact nonlinear bulk and connection identities passed.', flush=True)
        for soluble in [False, True]:
            action = HistoryAction(ManufacturedHistory(soluble))
            masks = [('mu', [1, 0, 0, 0]), ('N', [0, 1, 0, 0]), ('P', [0, 0, 1, 0]), ('chi', [0, 0, 0, 1]), ('mixed', [1, 1, 1, 1])]
            if soluble:
                masks = [masks[2], masks[-1]]
            for name, mask in masks:
                label = ('affine_clock_' if soluble else 'nonlinear_clock_') + name
                row = {'label': label, 'primary': action.integrated(mask, order=20), 'higher': action.integrated(mask, order=28)}
                report['cases'].append(row)
                primary = row['primary']
                scale = max(abs(primary['raw']), 1e-12)
                row['raw_adjoint_error'] = abs(primary['raw'] - primary['adjoint'])
                check(label + '_time_IBP_with_boundary', row['raw_adjoint_error'] < 2e-10 * scale + 2e-14, row['raw_adjoint_error'])
                check(label + '_temporal_quadrature_control', max(abs(primary[key] - row['higher'][key]) for key in ['raw', 'adjoint', 'action']) < 2e-10 * scale + 2e-14)
                check(label + '_weighted_anchor_identity', primary['weighted_current_error'] < 2e-12, primary['weighted_current_error'])
                check(label + '_genuinely_off_zero_P_slice', primary['P_max'] > .1 and primary['maximum_time_displacement'] > 1e-5 and primary['minimum_J'] > 0)
                row['finite_differences'] = []
                for step in [1e-3, 5e-4]:
                    plus = action.integrated(mask, amplitude=step, order=20)['action']
                    minus = action.integrated(mask, amplitude=-step, order=20)['action']
                    derivative = (plus - minus) / (2 * step)
                    error = abs(derivative - primary['raw'])
                    row['finite_differences'].append({'step': step, 'derivative': derivative, 'error': error})
                    check(label + '_actual_perturbed_action_' + str(step), error < 2e-5 * scale + 2e-12, error)
                if soluble:
                    pullback = action.physical_time_pullback(mask)
                    row['physical_time_pullback'] = pullback
                    check(label + '_analytic_transport', primary['analytic_transport_error'] < 2e-12, primary['analytic_transport_error'])
                    check(label + '_inverse_time_double_J_adjoint', abs(pullback['transport'] - primary['transport']) < 2e-10 * max(abs(primary['transport']), 1e-12) + 2e-14, pullback)
                    check(label + '_wrong_single_J_rejected', abs(pullback['wrong_single_J'] - primary['transport']) > 100 * max(abs(pullback['transport'] - primary['transport']), 1e-14), pullback)
                    check(label + '_wrong_same_time_rejected', abs(pullback['wrong_unpulled_anchor_time'] - primary['transport']) > 100 * max(abs(pullback['transport'] - primary['transport']), 1e-14), pullback)
                print(json.dumps({'case': label, 'raw_adjoint_error': row['raw_adjoint_error'], 'variation': primary['raw'], 'boundary': primary['boundary']}), flush=True)
                save()
        boundary_cases = [row for row in report['cases'] if 'mixed' in row['label']]
        check('omitted_time_boundary_rejected', all(abs(row['primary']['boundary']) > 1e-10 for row in boundary_cases))
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'cases': len(report['cases'])}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
