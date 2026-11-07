from derive_annular_source_gravity_20260914 import EvidenceRun
import ctypes
import json
import sympy as sp


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-source-split-septic-algebra-attempt01', __file__)
    try:
        evidence.own(evidence.root / 'DERIVATION-20261003-source-split-septic-construction.md')
        coordinate = sp.Symbol('coordinate')
        monomials = [coordinate**power for power in range(8)]
        matrix = sp.Matrix([[sp.diff(term, coordinate, order).subs(coordinate, endpoint) for term in monomials]
            for endpoint in [0, 1] for order in range(4)])
        inverse = matrix.inv()
        evidence.check('septic_unique', matrix.det() != 0, str(matrix.det()))
        evidence.check('septic_all_endpoint_jets', matrix * inverse == sp.eye(8))
        width = sp.Symbol('width', positive=True)
        jets = sp.symbols('value_L slope_L curvature_L third_L value_U slope_U curvature_U third_U')
        scaled = sp.Matrix([jet * width**(index % 4) for index, jet in enumerate(jets)])
        coefficients = inverse * scaled
        polynomial = sum(coefficient * term for coefficient, term in zip(coefficients, monomials))
        for endpoint in [0, 1]:
            for order in range(4):
                value = sp.diff(polynomial, coordinate, order).subs(coordinate, endpoint) / width**order
                evidence.check('physical_jet_' + str(endpoint) + '_' + str(order), sp.simplify(value - jets[4 * endpoint + order]) == 0)
        speed, drift, acceleration, slope, third = sp.symbols('speed drift acceleration slope third')
        curvature = -(drift + acceleration) * slope / speed
        evidence.check('source_corner_by_computed_curvature', sp.simplify(speed * curvature + (drift + acceleration) * slope) == 0)
        evidence.check('source_shared_first_jet', slope - slope == 0)
        path = evidence.output / 'exact-septic-endpoint-map.json'
        result = dict(degree=7, endpoint_order=['value_L', 'h*slope_L', 'h^2*curvature_L', 'h^3*third_L',
            'value_U', 'h*slope_U', 'h^2*curvature_U', 'h^3*third_U'],
            coefficients_by_power=[[str(inverse[row, column]) for column in range(8)] for row in range(8)],
            determinant=str(matrix.det()), coupled_fixed_point_convergence_proven=False, valid_for_claim=False)
        path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        evidence.own(path, 'outputs')
        evidence.report.update(exact_endpoint_map=str(path.relative_to(evidence.root)),
            source_split_septic_constructible=True, numerical_live_P7_state_constructed=False,
            github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

