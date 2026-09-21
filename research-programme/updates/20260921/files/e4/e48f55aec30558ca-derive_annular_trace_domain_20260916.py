from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_boundary_response_20260916 import field_matrices, nested_coordinates
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from scipy.linalg import eigh
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-trace-domain-and-inertia-attempt01', __file__)
    try:
        coordinate = sp.symbols('s', real=True)
        width, radius, stiffness = sp.symbols('epsilon b D', positive=True)
        smooth = coordinate*(1-coordinate)**2
        kinetic = width**3*sp.integrate((radius+width*coordinate)**2*smooth**2, (coordinate, 0, 1))
        bulk = width*sp.integrate((radius+width*coordinate)**2*sp.diff(smooth, coordinate)**2, (coordinate, 0, 1))
        evidence.check('smooth_layer_has_fixed_source_trace_and_C1_outer_cutoff', smooth.subs(coordinate, 0)==0
                       and sp.diff(smooth, coordinate).subs(coordinate, 0)==1 and smooth.subs(coordinate, 1)==0
                       and sp.diff(smooth, coordinate).subs(coordinate, 1)==0)
        evidence.check('smooth_layer_kinetic_norm_vanishes', sp.limit(kinetic, width, 0)==0)
        evidence.check('smooth_layer_bulk_energy_vanishes', sp.limit(bulk, width, 0)==0)
        evidence.check('fixed_stencil_Gram_energy_survives', sp.limit(bulk+stiffness, width, 0)==stiffness)
        difference = width*sp.integrate((radius+width*coordinate)**2*(sp.diff(smooth, coordinate)-sp.diff(smooth, coordinate).subs(coordinate, 2*coordinate))**2, (coordinate, 0, sp.Rational(1, 2)))
        difference += width*sp.integrate((radius+width*coordinate)**2*sp.diff(smooth, coordinate)**2, (coordinate, sp.Rational(1, 2), 1))
        evidence.check('adjacent_layers_have_zero_jump_difference_and_vanishing_bulk_distance', sp.limit(difference, width, 0)==0)
        evidence.check('cubic_layer_constants', sp.integrate(smooth**2, (coordinate, 0, 1))==sp.Rational(1, 105)
                       and sp.integrate(sp.diff(smooth, coordinate)**2, (coordinate, 0, 1))==sp.Rational(2, 15))
        quadratic = coordinate*(1-coordinate)
        mass = width**3*(radius**2/30+radius*width/30+width**2/105)
        spring = width*(radius**2/3+radius*width/3+2*width**2/15)
        evidence.check('exact_variable_weight_P2_layer_mass', sp.expand(mass-width**3*sp.integrate((radius+width*coordinate)**2*quadratic**2, (coordinate, 0, 1)))==0)
        evidence.check('exact_variable_weight_P2_layer_bulk_stiffness', sp.expand(spring-width*sp.integrate((radius+width*coordinate)**2*sp.diff(quadratic, coordinate)**2, (coordinate, 0, 1)))==0)
        evidence.check('reference_inverse_width_frequency_scaling', sp.limit(width**2*spring/mass, width, 0)==10)
        evidence.check('Gram_inverse_width_cubed_frequency_squared_scaling', sp.limit(width**3*(spring+stiffness)/mass, width, 0)==30*stiffness/radius**2)
        for count in [257, 513]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                for splits in [2, 4, 8, 16, 32, 64]:
                    coarse = QuadraticSourceFittedAction(count, gram, background_mass=0.)
                    system = LocallyRefinedSourceAction(count, gram, background_mass=0., source_splits=splits)
                    matrices = field_matrices(system, system.anchor)
                    embedding, bubbles, retained, new = nested_coordinates(coarse, system)
                    source_edge = int(np.searchsorted(system.edges, system.anchor))
                    cell_width = system.edges[source_edge+1]-system.anchor
                    layer = np.zeros(system.count)
                    layer[system.element_indices[source_edge, 1]] = cell_width/4
                    measured_mass = float(layer @ (matrices['mass'] @ layer))
                    measured_bulk = float(layer @ (matrices['bulk'] @ layer))
                    measured_gram = float(layer @ (matrices['gram'] @ layer))
                    denominator = float(system.lifted_hinge @ (matrices['gram_weights']*system.lifted_hinge))
                    exact_mass = float(mass.subs({width:cell_width, radius:system.anchor}))
                    exact_bulk = float(spring.subs({width:cell_width, radius:system.anchor}))
                    prefix = branch+str(count)+'split'+str(splits)
                    evidence.check(prefix+'_trace_normalized_and_samples_fixed', abs(system.jump @ layer-1)<2e-13
                                   and np.max(abs(system.original @ layer), initial=0.)==0 and np.max(abs(layer[retained]))==0)
                    evidence.check(prefix+'_exact_mass_and_stiffness', abs(measured_mass/exact_mass-1)<2e-11
                                   and abs(measured_bulk/exact_bulk-1)<2e-11 and abs(measured_gram-denominator)<2e-13)
                    local_mass = (bubbles.T @ matrices['mass'] @ bubbles).toarray()
                    local_stiffness = (bubbles.T @ matrices['stiffness'] @ bubbles).toarray()
                    eigenvalue = float(eigh(local_stiffness, local_mass, subset_by_index=[len(new)-1, len(new)-1], eigvals_only=True)[0])
                    quotient = (measured_bulk+measured_gram)/measured_mass
                    evidence.check(prefix+'_Rayleigh_lower_bound_on_maximum_frequency', quotient <= eigenvalue*(1+2e-11))
                    evidence.report['cases'].append(dict(branch=branch, count=count, source_splits=splits, width=float(cell_width),
                        trace_mass=measured_mass, trace_bulk_stiffness=measured_bulk, trace_Gram_stiffness=measured_gram,
                        trace_trial_frequency=float(np.sqrt(quotient)), maximum_local_frequency=float(np.sqrt(eigenvalue))))
                    evidence.save()
        evidence.report.update(scope='Conditional fixed-original-stencil trace-domain lemma and frozen stationary-source layer spectra, not the full parent action or a converged moving-source evolution.',
            bare_bulk_L2_form_closable=False, bare_bulk_nonclosability_requires_fixed_nonzero_Gram_stiffness=True,
            natural_trace_condition_requires_admissible_arbitrary_narrow_layer_variations=True,
            admissible_completion_in_augmented_domain_not_ruled_out=True,
            static_condition_imposed_on_finite_trajectories=False, simultaneous_base_grid_limit_proven=False,
            dynamic_relaxation_or_well_preparedness_proven=False, full_parent_theory_rejected=False,
            scalar_form_convention='Q=2*potential, so the layer Gram limit is D, not D/2',
            source_urls=['https://www.math.vanderbilt.edu/peters10/teaching/spring2020/OperatorAlgebras.pdf',
                         'https://www.ma.huji.ac.il/~razk/Publications/PDF/CHK00.pdf'],
            source_access='Search excerpts available; direct PDF opens timed out. Proofs and tests here are explicit and do not assume either source proves the MTS-specific statements.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
