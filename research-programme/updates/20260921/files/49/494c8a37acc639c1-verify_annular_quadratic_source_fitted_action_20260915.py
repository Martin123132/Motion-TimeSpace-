from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from annular_source_fitted_action_20260915 import SourceFittedAction
from verify_annular_source_fitted_action_20260915 import manufactured, continuum_source_identity
from scipy.linalg import solve_banded
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-quadratic-source-fitted-action-attempt01', __file__)
    try:
        coordinate = sp.symbols('xi')
        basis = [(1-coordinate)*(1-2*coordinate), 4*coordinate*(1-coordinate), coordinate*(2*coordinate-1)]
        evidence.check('quadratic_partition_and_nodal_basis', sp.simplify(sum(basis)-1) == 0
            and sp.Matrix([[entry.subs(coordinate, point) for entry in basis] for point in [0, sp.Rational(1, 2), 1]]) == sp.eye(3))
        for power in [1, 2]:
            evidence.check('polynomial_reproduction_'+str(power), sp.expand(sum(value**power*entry for value, entry in zip([0, sp.Rational(1, 2), 1], basis))-coordinate**power) == 0)
        for count in [17, 33, 65]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                linear = SourceFittedAction(count, gram, order=10, background_mass=.7)
                quadratic = QuadraticSourceFittedAction(count, gram, order=10, background_mass=.7)
                evidence.check(branch+str(count)+'_every_Gram_row_preserved', quadratic.original.shape[0] == linear.original.shape[0]
                    and np.max(abs((quadratic.original @ quadratic.linear_embedding-linear.original).data), initial=0.) < 1e-13)
                for location in [6.03, 6.05, 6.15]:
                    original_coordinates, original_rates = manufactured(linear, .12, location)
                    coordinates = np.append(quadratic.linear_embedding @ original_coordinates[:-1], original_coordinates[-1])
                    rates = np.append(quadratic.linear_embedding @ original_rates[:-1], original_rates[-1])
                    old, new = linear.evaluate(.12, original_coordinates, original_rates), quadratic.evaluate(.12, coordinates, rates)
                    momentum = np.append(quadratic.linear_embedding.T @ new['momenta'][:-1], new['momenta'][-1])
                    covector = quadratic.linear_embedding.T @ new['scalar_covector']
                    error = max(abs(old['action']-new['action']), np.max(abs(old['momenta']-momentum)), np.max(abs(old['scalar_covector']-covector)),
                        abs(linear.source_covector(.12, original_coordinates, original_rates)-quadratic.source_covector(.12, coordinates, rates)))
                    evidence.check(branch+str(count)+str(location)+'_exact_linear_subspace_action_and_momenta', error < 2e-11, float(error))
                coordinates, rates = manufactured(quadratic, .12, 6.05)
                data = quadratic.evaluate(.12, coordinates, rates)
                acceleration = quadratic.acceleration(.12, coordinates, rates)
                moved = quadratic.evaluate(.12+1e-24j, coordinates+1e-24j*rates, rates+1e-24j*acceleration)
                covector = np.append(data['scalar_covector'], quadratic.source_covector(.12, coordinates, rates))
                euler = np.max(abs(moved['momenta'].imag/1e-24-covector))
                energy_rate = quadratic.energy(.12, coordinates+1e-24j*rates, rates+1e-24j*acceleration).imag/1e-24
                schur = data['source_inertia']-data['cross'] @ solve_banded((2, 2), data['mass_bands'], data['cross'])
                lapse, root = quadratic.metric(.12, coordinates[-1])
                proper = quadratic.source_mass*lapse**2/(root**2*data['clock']**3)
                evidence.check(branch+str(count)+'_positive_Schur_and_full_EL_energy', schur >= proper-2e-12 and euler < 2e-10 and abs(energy_rate) < 2e-12,
                    dict(schur=float(schur), proper=float(proper), euler=float(euler), energy_derivative=float(energy_rate)))
                direction = np.sin(np.arange(quadratic.count+1)+.3)
                step = 2e-5
                samples = [quadratic.evaluate(.12, coordinates+multiple*step*direction, rates)['action'] for multiple in [-2, -1, 1, 2]]
                difference = (samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*step)
                evidence.check(branch+str(count)+'_independent_real_action_gradient', abs(difference-covector @ direction) < 2e-9, float(abs(difference-covector @ direction)))
                offset = quadratic.radii-quadratic.anchor
                polynomial = .03*offset+.004*offset**2+.008*np.maximum(offset, 0.)
                factors = quadratic.lifted @ polynomial
                evidence.check(branch+str(count)+'_true_trace_jump_and_quadratic_Gram_annihilator', abs(quadratic.jump @ polynomial-.008) < 2e-12 and np.max(abs(factors), initial=0.) < 2e-12)
        for gram in [False, True]:
            errors = []
            for count in [17, 33, 65, 129]:
                system = QuadraticSourceFittedAction(count, gram)
                coordinates, rates = manufactured(system, .12, 6.05)
                moved_coordinates, moved_rates = manufactured(system, .12+1e-24j, 6.05)
                momentum_rate = system.evaluate(.12+1e-24j, moved_coordinates, moved_rates)['field_momenta'][-1].imag/1e-24
                force = system.source_covector(.12, coordinates, rates, wave=True)-momentum_rate
                target, pressure, bulk = continuum_source_identity(system, .12, 6.05)
                errors.append(float(abs(force-target)))
            evidence.check(('MTS' if gram else 'reference')+'_manufactured_force_converges', errors[-1] < 2e-9 and errors[-1] < errors[-2]/2, errors)
        evidence.report.update(scope='Nested quadratic extension of the source-fitted finite action; prescribed metric only.',
            original_linear_action_exactly_recovered_on_embedded_subspace=True, all_original_vertex_Gram_rows_retained=True,
            true_quadratic_source_gradient_jump_used=True, no_fitted_coefficient_added=True,
            full_source_momentum_retained=True, live_quadratic_geometry_qualified=False,
            contextual_basis_source='https://defelement.org/elements/examples/interval-lagrange-gll-2.html')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
