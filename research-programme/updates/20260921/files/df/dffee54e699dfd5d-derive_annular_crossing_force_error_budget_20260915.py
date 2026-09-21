from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
import json
import numpy as np
import sympy as sp


def source_traces(system, state, quadratic):
    coordinates, rates = np.split(state[:-1], 2)
    position, velocity = coordinates[-1], rates[-1]
    if quadratic:
        source_edge = np.searchsorted(system.edges, system.anchor)
        indices = system.element_indices[source_edge-1:source_edge+1]
        values = coordinates[:-1][np.maximum(indices,0)]*(indices >= 0)
        unused, jacobian, unused2 = system.mapping((system.edges[:-1]+system.edges[1:])/2, position)
        lengths = (np.diff(system.edges)*jacobian)[source_edge-1:source_edge+1]
        left = values[0] @ np.array([1.,-4.,3.])/lengths[0]
        right = values[1] @ np.array([-3.,4.,-1.])/lengths[1]
    else:
        source_edge = np.searchsorted(system.radii, system.anchor)
        left_length = (system.anchor-system.radii[source_edge-1])*(position-system.radii[0])/(system.anchor-system.radii[0])
        right_length = (system.radii[source_edge]-system.anchor)*(system.radii[-1]-position)/(system.radii[-1]-system.anchor)
        left, right = -coordinates[source_edge-1]/left_length, coordinates[source_edge]/right_length
    return float(left), float(right), float(position**2*(1-velocity**2)/2)


def main():
    evidence = EvidenceRun('annular-crossing-force-error-budget-attempt01', __file__)
    try:
        coefficient, exact_coefficient, left, right, exact_left, exact_right, remainder = sp.symbols('c cstar Hleft Hright Lstar Rstar residual', real=True)
        force_error = coefficient*(left**2-right**2)+remainder-exact_coefficient*(exact_left**2-exact_right**2)
        derived = (coefficient-exact_coefficient)*(exact_left**2-exact_right**2)+coefficient*((left-exact_left)*(left+exact_left)-(right-exact_right)*(right+exact_right))+remainder
        evidence.check('exact_trace_geometry_mesh_force_error_identity', sp.expand(force_error-derived) == 0)
        moment = sp.Matrix([[1,sp.Rational(1,2)],[sp.Rational(1,2),sp.Rational(1,3)]])
        endpoint = sp.Matrix([1,1])
        defect = 4*moment-endpoint*endpoint.T
        evidence.check('sharp_linear_derivative_endpoint_inverse_inequality', (endpoint.T*moment.inv()*endpoint)[0] == 4
            and defect.det() == 0 and defect.trace() > 0 and defect[0,0] > 0)
        coordinate, width, radius = sp.symbols('s epsilon b', positive=True)
        layer = coordinate*(1-coordinate)**2
        squared_gradient = sp.integrate(sp.diff(layer,coordinate)**2,(coordinate,0,1))
        weighted = width*sp.integrate((radius+width*coordinate)**2*sp.diff(layer,coordinate)**2,(coordinate,0,1))
        evidence.check('vanishing_bulk_energy_does_not_control_source_gradient_trace', layer.subs(coordinate,0) == 0
            and sp.diff(layer,coordinate).subs(coordinate,0) == 1 and squared_gradient == sp.Rational(2,15)
            and sp.limit(weighted,width,0,dir='+') == 0)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        precision_path = intake/'annular-quadratic-crossing-precision-attempt02/status.json'
        precision = json.loads(precision_path.read_text())
        evidence.check('independent_force_and_quadrature_qualified', precision['state'] == 'complete' and all(row['passed'] for row in precision['checks']))
        evidence.own(precision_path)
        oracle_path = intake/'annular-source-fitted-fine-crossing-attempt01/oracle-512.npz'
        evidence.own(oracle_path)
        saved = np.load(oracle_path)
        times, exact_states = saved['times'], saved['states']
        oracle = TwoSidedGRCharacteristics(512,mass=0.)
        reference = []
        for state in exact_states:
            fields, position, momentum, velocity = oracle.unpack(state)
            left = (fields[0,0,-1]-fields[0,1,-1])/2
            right = (fields[1,0,0]-fields[1,1,0])/2
            reference.append((left,right,position**2*(1-velocity**2)/2,oracle.source_force(fields,position,velocity)))
        for quadratic, rows in [(True,precision['cases']),(False,precision['linear_cases'])]:
            for row in rows:
                count, branch = row['base_count'] if quadratic else row['count'], row['branch']
                if quadratic:
                    folder = 'annular-quadratic-crossing-attempt01' if count <= 257 else 'annular-quadratic-fine-crossing-attempt01'
                    system = QuadraticSourceFittedAction(count,branch == 'MTS',background_mass=0.)
                else:
                    folder = 'annular-source-fitted-force2049-attempt01'
                    system = SourceFittedAction(count,branch == 'MTS',background_mass=0.)
                state_path = intake/folder/(branch+'-'+str(count)+'.npz')
                evidence.own(state_path)
                history = np.load(state_path)['states']
                budgets, trace_residuals, identity_residuals = [], [], []
                for instant, state, exact, decomposition in zip(times,history,reference,row['full_force_decompositions']):
                    left, right, coefficient = source_traces(system,state,quadratic)
                    exact_left, exact_right, exact_coefficient, exact_force = exact
                    geometry = (coefficient-exact_coefficient)*(exact_left**2-exact_right**2)
                    left_error = coefficient*(left-exact_left)*(left+exact_left)
                    right_error = -coefficient*(right-exact_right)*(right+exact_right)
                    mesh = decomposition['interior_mesh_pressure']-decomposition['smooth_bulk_euler_projection']
                    gram = decomposition['Gram_shape_force']
                    total = geometry+left_error+right_error+mesh+gram
                    observed = decomposition['canonical_force']-exact_force
                    triangle = abs(geometry)+abs(left_error)+abs(right_error)+abs(mesh)+abs(gram)
                    trace_residuals.append(abs(coefficient*(left**2-right**2)-decomposition['physical_source_pressure']))
                    identity_residuals.append(abs(total-observed))
                    budgets.append(dict(time=float(instant),left_trace=left,right_trace=right,
                        left_trace_error=float(left-exact_left),right_trace_error=float(right-exact_right),
                        geometry_error=float(geometry),left_trace_force_error=float(left_error),right_trace_force_error=float(right_error),
                        signed_mesh_bulk_error=float(mesh),direct_Gram_shape_force=float(gram),
                        reconstructed_force_error=float(total),observed_force_error=float(observed),
                        observed_triangle_envelope=float(triangle),
                        triangle_envelope_below_absolute_gate=bool(triangle < 2e-7)))
                label = ('quadratic' if quadratic else 'linear')+branch+str(count)
                evidence.check(label+'_independent_source_trace_pressure', max(trace_residuals) < 2e-11, float(max(trace_residuals)))
                evidence.check(label+'_force_error_identity_and_triangle_bound', max(identity_residuals) < 2e-11
                    and all(abs(item['observed_force_error']) <= item['observed_triangle_envelope']+2e-11 for item in budgets),float(max(identity_residuals)))
                evidence.report['cases'].append(dict(branch=branch,degree=2 if quadratic else 1,count=count,budgets=budgets))
                evidence.save()
        evidence.report.update(scope='Exact conditional force-error decomposition and kinematic trace counterexample, not a new physical solution or a certified continuum reference bound.',
            derivative_endpoint_constant_squared=4,compact_layer_gradient_norm_squared=str(squared_gradient),
            compact_layer_weighted_gradient_norm_squared=str(weighted),
            no_fitted_coefficient_added=True,all_force_terms_retained=True,
            continuum_reference_degree=512,uniform_all_time_force_bound_proven=False,
            live_quadratic_geometry_qualified=False,kinematic_counterexample_not_claimed_as_on_shell_evolution=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
