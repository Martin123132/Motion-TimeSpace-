from annular_high_order_native_v2_20261003 import HighLoads, HighAction, PolynomialBasis
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_product_basis_20261003 import product_basis_values


class ProductBasis(PolynomialBasis):
    def values(self, coordinate, derivative=0):
        return product_basis_values(coordinate, self.degree, derivative)


def install_product_basis(loads):
    basis = ProductBasis(loads.basis.degree)
    loads.basis = basis
    loads.native_engine.basis = basis
    loads.material.basis = basis


def live_product(owner, coordinates, rates, mesh, branch, deadline):
    loads = HighLoads(owner, coordinates, rates, mesh, branch, deadline)
    install_product_basis(loads)
    solver = CandidateRadialSolve(loads, 22, 28, [branch])
    solution = solver.solve(branch)
    return loads, HighAction(loads, mesh, solver, solution)
