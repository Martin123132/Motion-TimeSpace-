from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-Gram-trace-relaxation-attempt01',__file__)
    try:
        jump,linear,denominator,constant = sp.symbols('j L D C',real=True)
        original = (constant-2*linear*jump+denominator*jump**2)/2
        relaxed = (constant-linear**2/denominator)/2
        evidence.check('exact_Gram_trace_completion_of_square',sp.simplify(original-relaxed-denominator*(jump-linear/denominator)**2/2)==0)
        evidence.check('exact_trace_contact_derivative',sp.diff(original,jump)==denominator*jump-linear)
        coordinate,width = sp.symbols('s epsilon',positive=True)
        layer = coordinate*(1-coordinate)**2
        norm = width*sp.integrate(sp.diff(layer,coordinate)**2,(coordinate,0,1))
        evidence.check('fixed_trace_variation_can_have_vanishing_bulk_H1_cost',layer.subs(coordinate,0)==0
            and layer.subs(coordinate,1)==0 and sp.diff(layer,coordinate).subs(coordinate,0)==1
            and sp.limit(norm,width,0,dir='+')==0)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        oracle_path = intake/'annular-source-fitted-fine-crossing-attempt01/oracle-512.npz'
        evidence.own(oracle_path)
        oracle_saved = np.load(oracle_path)
        oracle = TwoSidedGRCharacteristics(512,mass=0.)
        for count,splits,folder,filename,index in [
            (257,1,'annular-quadratic-crossing-attempt01','MTS-257.npz',-1),
            (257,8,'annular-local-refinement-crossing-attempt02','MTS-257.npz',-1),
            (513,1,'annular-quadratic-fine-crossing-attempt01','MTS-513.npz',1),
            (513,4,'annular-local-tight-controls-attempt01','MTS-513-tight-first-twentieth.npz',1)]:
            path = intake/folder/filename
            evidence.own(path)
            saved = np.load(path)
            instant,state = float(saved['times'][index]),saved['states'][index]
            system = LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=splits)
            coordinates,rates = np.split(state[:-1],2)
            radius,jacobian,unused = system.mapping(system.radii,coordinates[-1])
            weights = np.asarray(system.sampling @ (system.coefficient(instant,radius)/jacobian))/system.gram_spacing
            values = system.original @ coordinates[:-1]
            hinge = system.lifted_hinge
            denominator_value = float(hinge @ (weights*hinge))
            linear_value = float(hinge @ (weights*values))
            current_jump = float(system.jump @ coordinates[:-1])
            minimizer = linear_value/denominator_value
            residual = values-hinge*current_jump
            energy = float(residual @ (weights*residual)/2)
            relaxed_energy = float((values @ (weights*values)-linear_value**2/denominator_value)/2)
            square_gap = denominator_value*(current_jump-minimizer)**2/2
            prefix = str(count)+'split'+str(splits)
            evidence.check(prefix+'_positive_Gram_trace_stiffness',denominator_value > 0 and relaxed_energy >= -2e-18)
            evidence.check(prefix+'_measured_square_completion',abs(energy-relaxed_energy-square_gap) < 2e-18)
            oracle_index = int(np.argmin(abs(oracle_saved['times']-instant)))
            fields,position,momentum,velocity = oracle.unpack(oracle_saved['states'][oracle_index])
            left = (fields[0,0,-1]-fields[0,1,-1])/2
            right = (fields[1,0,0]-fields[1,1,0])/2
            left_jacobian = (position-system.radii[0])/(system.anchor-system.radii[0])
            right_jacobian = (system.radii[-1]-position)/(system.radii[-1]-system.anchor)
            reference_jump = right_jacobian*right-left_jacobian*left
            evidence.report['cases'].append(dict(count=count,source_splits=splits,time=instant,
                derivative_jump_chart='reference-coordinate gradient jump; not physical H_right-H_left',
                trace_stiffness=denominator_value,current_jump=current_jump,instantaneous_static_minimizer=minimizer,
                difference_from_static_minimizer=current_jump-minimizer,reference_GR_jump=float(reference_jump),
                difference_from_reference_GR_jump=float(current_jump-reference_jump),
                Gram_energy=energy,relaxed_Gram_energy=relaxed_energy,positive_trace_square_gap=square_gap,
                trace_contact_derivative=denominator_value*(current_jump-minimizer)))
            evidence.save()
        evidence.report.update(scope='Exact conditional Gram trace dependence and static relaxation mechanism; no replacement of the evolving action.',
            bulk_H1_continuity_of_point_derivative_Gram_term=False,
            full_energy_or_augmented_trace_domain_not_ruled_out=True,
            dynamic_relaxation_to_static_minimizer_proven=False,
            permission_to_replace_action_by_static_relaxation=False,
            live_quadratic_geometry_qualified=False,uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
