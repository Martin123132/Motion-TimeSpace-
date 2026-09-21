from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_compatible_current_restoring_20260909 import unit_gram_template
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from scipy.linalg import solve_banded
from fractions import Fraction
import argparse
import hashlib
import json
import numpy as np
import sympy as sp


def source_rows(system):
    selected = []
    matrix = system.original.tocsr()
    for index in range(matrix.shape[0]):
        columns = matrix.indices[matrix.indptr[index]:matrix.indptr[index+1]]
        radii = system.radii[columns]
        selected.append(bool(len(radii) and min(radii)<system.anchor<max(radii)))
    return np.asarray(selected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(finite_future_trajectories_read=False,force_fit=False,force_correction=False,
            original_action_unchanged=True,prescribed_flat_background_only=True,
            local_trace_identity_not_global_force_convergence=True,interval_arithmetic=False,
            conditional_smoothness_not_assumed_for_continuum=True)
        phase_cycle = [Fraction(3,5),Fraction(1,5),Fraction(2,5),Fraction(4,5)]
        for exponent in range(5,31):
            coordinate = Fraction(83,160)*2**exponent
            phase = coordinate-coordinate.numerator//coordinate.denominator
            if phase!=phase_cycle[(exponent-5)%4]:
                raise RuntimeError('Incorrect exact dyadic phase.')
        evidence.check('exact_dyadic_phase_cycle',True,[str(value) for value in phase_cycle])
        diagonal = [Fraction(59097,573104),Fraction(1825,25284),Fraction(491,7056),Fraction(5,72)]
        radii = [Fraction(253,50568)+Fraction(1,392),Fraction(253,50568)+Fraction(3,392),
            Fraction(3,392)+Fraction(1,144)+Fraction(1,392),Fraction(1,72)]
        evidence.check('uniform_Gram_coefficient_bounds',all(center-radius>Fraction(1,20)
            and center+radius<Fraction(1,8) for center,radius in zip(diagonal,radii)),
            dict(lower=[str(center-radius) for center,radius in zip(diagonal,radii)],
                upper=[str(center+radius) for center,radius in zip(diagonal,radii)]))
        variable,width = sp.symbols('variable width',real=True)
        for power in range(1,6):
            right = (4*(width/2)**power-width**power)/width
            left = ((-width)**power-4*(-width/2)**power)/width
            expected_right = {1:1,2:0,3:-width**2/2,4:-3*width**3/4,5:-7*width**4/8}[power]
            expected_left = {1:1,2:0,3:-width**2/2,4:3*width**3/4,5:-7*width**4/8}[power]
            evidence.check('P2_endpoint_monomial_'+str(power),
                sp.simplify(right-expected_right)==0 and sp.simplify(left-expected_left)==0)
        phase = sp.symbols('phase',real=True)
        hinge_stencil = sp.Matrix([1-phase,2*phase-1,-phase])
        quadratic_stencil = sp.Matrix([(1-phase)**2,1+2*phase-2*phase**2,phase**2])
        evidence.check('hinge_stencil_norm',sp.simplify((hinge_stencil.T*hinge_stencil)[0]-(6*phase**2-6*phase+2))==0)
        speed,acceleration,gradient,gradient_rate,curvature,radius = sp.symbols('speed acceleration gradient gradient_rate curvature radius')
        mixed = gradient_rate-speed*curvature
        moving_boundary_second = curvature+2*gradient/radius+2*speed*mixed+speed**2*curvature+acceleration*gradient
        evidence.check('moving_Dirichlet_curvature_law',
            sp.simplify(moving_boundary_second-((1-speed**2)*curvature+2*speed*gradient_rate+(acceleration+2/radius)*gradient))==0)
        reference_mass = sp.Matrix([[4,2,-1],[2,16,2],[-1,2,4]])/30
        mass_eigenvalues = list(reference_mass.eigenvals())
        expected_eigenvalues = [sp.Rational(1,6),(19-sp.sqrt(201))/60,(19+sp.sqrt(201))/60]
        evidence.check('P2_mass_coercivity_constant',all(any(sp.simplify(actual-expected)==0 for actual in mass_eigenvalues)
            for expected in expected_eigenvalues))
        kernel = (5*sum(value**2 for value in quadratic_stencil)
            -quadratic_stencil[0]*quadratic_stencil[1]-quadratic_stencil[1]*quadratic_stencil[2])/72
        evidence.report['quadratic_source_kernel_squared'] = str(sp.expand(kernel))
        evidence.report['mesh_cases'] = []
        systems = {}
        for count in [33,65,129,257,513,1025,2049]:
            system = LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=8)
            spacing = 1.6/(count-1)
            exponent = (count-1).bit_length()-1
            phase_value = phase_cycle[(exponent-5)%4]
            left_length,right_length = spacing*float(phase_value)/8,spacing*(1-float(phase_value))/8
            source_edge = np.searchsorted(system.edges,system.anchor)
            observed_left = system.anchor-system.edges[source_edge-1]
            observed_right = system.edges[source_edge+1]-system.anchor
            evidence.check(str(count)+'_actual_mesh_phase',max(abs(observed_left-left_length),abs(observed_right-right_length))<2e-14
                and min(observed_left,observed_right)>=spacing/40-2e-14)
            jump_squared = float(system.jump @ system.jump)
            expected = 17*(observed_left**-2+observed_right**-2)
            evidence.check(str(count)+'_exact_jump_inverse_norm',abs(jump_squared/expected-1)<2e-12
                and spacing*np.sqrt(jump_squared)<=170+2e-7)
            offset = system.radii-system.anchor
            hinge = np.maximum(offset,0.)
            selected = np.flatnonzero(system.jump)
            ideal_offsets = np.array([-observed_left,-observed_left/2,observed_right/2,observed_right])
            hinge_roundoff = float(system.jump[selected] @ (hinge[selected]-np.maximum(ideal_offsets,0.)))
            hinge_raw_error = float(system.jump @ hinge-1)
            evidence.check(str(count)+'_unit_hinge_jump',abs(hinge_raw_error-hinge_roundoff)<2e-13,
                dict(raw_error=hinge_raw_error,explicit_coordinate_roundoff=hinge_roundoff,
                    corrected_identity_error=hinge_raw_error-hinge_roundoff))
            margin,adjacent,extras = unit_gram_template(count)
            upper = margin.copy()
            upper[:-1] += 2*abs(adjacent)
            upper[1:] += 2*abs(adjacent)
            for first,second,weight in extras:
                upper[[first,second]] += 2*abs(weight)
            evidence.check(str(count)+'_implemented_Gram_coefficient_bounds',min(margin)>1/20 and max(upper)<1/8)
            factor = system.original @ hinge**2
            mask = source_rows(system)
            expected_norm = spacing**4*float(kernel.subs(phase,sp.Rational(phase_value.numerator,phase_value.denominator)))
            observed_norm = float(factor[mask] @ factor[mask])
            evidence.check(str(count)+'_phase_dependent_quadratic_factor',abs(observed_norm/expected_norm-1)<2e-8)
            coefficients = np.array([[.7,-.2,.4,-.3,.1],[1.1,.3,-.6,.2,-.15]])
            values = np.zeros_like(offset)
            for side,selected in enumerate([offset<0,offset>0]):
                for power in range(1,6):
                    values[selected] += coefficients[side,power-1]*offset[selected]**power
            expected_jump = coefficients[1,0]-coefficients[0,0]
            expected_jump += (observed_left**2*6*coefficients[0,2]-observed_right**2*6*coefficients[1,2])/12
            expected_jump -= (observed_left**3*24*coefficients[0,3]+observed_right**3*24*coefficients[1,3])/32
            expected_jump += 7*(observed_left**4*120*coefficients[0,4]-observed_right**4*120*coefficients[1,4])/960
            selected = np.flatnonzero(system.jump)
            ideal_offsets = np.array([-observed_left,-observed_left/2,observed_right/2,observed_right])
            ideal_values = np.zeros(4)
            for side,selection in enumerate([ideal_offsets<0,ideal_offsets>0]):
                for power in range(1,6):
                    ideal_values[selection] += coefficients[side,power-1]*ideal_offsets[selection]**power
            coordinate_roundoff = float(system.jump[selected] @ (values[selected]-ideal_values))
            raw_error = float(system.jump @ values)-expected_jump
            evidence.check(str(count)+'_piecewise_quintic_jump',abs(raw_error-coordinate_roundoff)<2e-13,
                dict(raw_error=raw_error,explicit_coordinate_roundoff=coordinate_roundoff,
                    corrected_identity_error=raw_error-coordinate_roundoff))
            evidence.report['mesh_cases'].append(dict(count=count,phase=str(phase_value),spacing=spacing,
                left_length=observed_left,right_length=observed_right,scaled_jump_norm=spacing*np.sqrt(jump_squared),
                source_rows=int(sum(mask)),quadratic_factor_norm=float(np.sqrt(observed_norm)),
                normalized_quadratic_factor_squared=observed_norm/spacing**4,
                manufactured_raw_trace_error=raw_error,manufactured_coordinate_roundoff=coordinate_roundoff,
                manufactured_identity_error=raw_error-coordinate_roundoff,
                hinge_raw_error=hinge_raw_error,hinge_coordinate_roundoff=hinge_roundoff))
            if count in [257,513,1025]:
                systems[count] = system
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        status_path = intake/'annular-dense-GR-references-attempt01/status.json'
        projection_path = intake/'annular-GR-projection-residual-attempt02/status.json'
        evidence.own(status_path)
        evidence.own(projection_path)
        oracle_status,projection_status = [json.loads(path.read_text()) for path in [status_path,projection_path]]
        evidence.check('GR_only_sources_complete',oracle_status['state']=='complete' and projection_status['state']=='complete'
            and not projection_status['finite_future_trajectories_read'])
        for degree in [512,768]:
            oracle = TwoSidedGRCharacteristics(degree,mass=0.,source=.03)
            path = intake/'annular-dense-GR-references-attempt01'/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            evidence.check(str(degree)+'_GR_hash',hashlib.sha256(path.read_bytes()).hexdigest()==oracle_status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path,allow_pickle=False) as saved:
                times,oracle_states = saved['times'].copy(),saved['states'].copy()
            jets,third_bounds,fifth_bounds,boundary_curvatures = [],[],[],[]
            for instant,state in zip(times,oracle_states):
                fields,position,momentum,speed = oracle.unpack(state)
                coefficients = ((fields[:,0]-fields[:,1])/2) @ oracle.inverse.T
                tangent = oracle.rhs(instant,state)
                moved_fields,unused,unused2,moved_speed = oracle.unpack(state.astype(complex)+1e-25j*tangent)
                acceleration = moved_speed.imag/1e-25
                boundary_gradient = np.array([(fields[0,0,-1]-fields[0,1,-1])/2,(fields[1,0,0]-fields[1,1,0])/2])
                boundary_rate = np.array([(moved_fields[0,0,-1]-moved_fields[0,1,-1]).imag/2,
                    (moved_fields[1,0,0]-moved_fields[1,1,0]).imag/2])/1e-25
                jacobians = np.array([(position-oracle.inner)/.83,(oracle.outer-position)/.77])
                boundary_curvatures.append(-jacobians**2*(2*speed*boundary_rate+(acceleration+2/position)*boundary_gradient)/(1-speed**2))
                sides,third,fifth = [],[],[]
                for side in range(2):
                    length = [.83,.77][side]
                    jacobian = [(position-oracle.inner)/length,(oracle.outer-position)/length][side]
                    endpoint = 1. if side==0 else -1.
                    derivatives = [np.polynomial.chebyshev.chebder(coefficients[side],m=order) for order in range(5)]
                    sides.append([float(jacobian*(2/length)**order*np.polynomial.chebyshev.chebval(endpoint,values))
                        for order,values in enumerate(derivatives)])
                    third.append(float(jacobian*(2/length)**2*sum(abs(derivatives[2]))))
                    fifth.append(float(jacobian*(2/length)**4*sum(abs(derivatives[4]))))
                jets.append(sides)
                third_bounds.append(third)
                fifth_bounds.append(fifth)
            jets,third_bounds,fifth_bounds = np.array(jets),np.array(third_bounds),np.array(fifth_bounds)
            boundary_curvatures = np.array(boundary_curvatures)
            for count,system in systems.items():
                path = intake/'annular-GR-projection-residual-attempt02'/('projection-'+str(degree)+'-'+str(count)+'.npz')
                evidence.own(path)
                evidence.check(str(degree)+'_'+str(count)+'_projection_hash',
                    hashlib.sha256(path.read_bytes()).hexdigest()==projection_status['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path,allow_pickle=False) as saved:
                    projected = saved['states'].copy()
                    if not np.array_equal(times,saved['times']):
                        raise ValueError('Mismatched GR projection times.')
                edge = np.searchsorted(system.edges,system.anchor)
                left_length,right_length = system.anchor-system.edges[edge-1],system.edges[edge+1]-system.anchor
                exact_jump = jets[:,1,0]-jets[:,0,0]
                observed_jump = projected[:,:system.count] @ system.jump
                jump_error = observed_jump-exact_jump
                leading = (left_length**2*jets[:,0,2]-right_length**2*jets[:,1,2])/12
                fourth = -(left_length**3*jets[:,0,3]+right_length**3*jets[:,1,3])/32
                basic_bound = (left_length**2*third_bounds[:,0]+right_length**2*third_bounds[:,1])/12
                higher_bound = 7*(left_length**4*fifth_bounds[:,0]+right_length**4*fifth_bounds[:,1])/960
                evidence.check(str(degree)+'_'+str(count)+'_finite_polynomial_trace_bounds',
                    np.all(abs(jump_error)<=basic_bound+2e-11) and np.all(abs(jump_error-leading-fourth)<=higher_bound+2e-11))
                offset = system.radii-system.anchor
                hinge = np.maximum(offset,0.)
                quadratic = system.original @ hinge**2
                cubic = system.original @ offset**3
                cubic_hinge = system.original @ hinge**3
                mask = source_rows(system)
                actual_factor = np.asarray(system.lifted @ projected[:,:system.count].T).T[:,mask]
                curvature_jump = jets[:,1,1]-jets[:,0,1]
                quadratic_factor = curvature_jump[:,None]*quadratic[None,mask]/2
                nodal_remainder_bound = np.where(offset[None,:]<0,third_bounds[:,0,None],third_bounds[:,1,None])*abs(offset[None,:])**3/6
                local_factor_bound = np.linalg.norm(np.asarray(abs(system.original[mask]) @ nodal_remainder_bound.T).T,axis=1)
                local_factor_bound += np.linalg.norm(system.lifted_hinge[mask])*basic_bound
                evidence.check(str(degree)+'_'+str(count)+'_local_curvature_factor_bound',
                    np.all(np.linalg.norm(actual_factor-quadratic_factor,axis=1)<=local_factor_bound+2e-11))
                bulk_offset = system.base_radii-system.anchor
                raw_bounds = np.empty((len(times),count-3))
                stencil_weights = np.array([1.,3.,3.,1.])
                for stencil in range(count-3):
                    locations = bulk_offset[stencil:stencil+4]
                    if locations[-1]<0:
                        raw_bounds[:,stencil] = system.gram_spacing**3*third_bounds[:,0]
                    elif locations[0]>0:
                        raw_bounds[:,stencil] = system.gram_spacing**3*third_bounds[:,1]
                    else:
                        quadratic_difference = np.diff(np.maximum(locations,0.)**2,n=3)[0]
                        local_bounds = np.where(locations[None,:]<0,third_bounds[:,0,None],third_bounds[:,1,None])
                        raw_bounds[:,stencil] = abs(curvature_jump*quadratic_difference)/2
                        raw_bounds[:,stencil] += np.sum(stencil_weights[None,:]*local_bounds*abs(locations[None,:])**3/6,axis=1)
                full_factor_bound = np.linalg.norm(raw_bounds,axis=1)/np.sqrt(8)+np.linalg.norm(system.lifted_hinge)*basic_bound
                full_factors = np.asarray(system.lifted @ projected[:,:system.count].T).T
                evidence.check(str(degree)+'_'+str(count)+'_global_Gram_factor_bound',
                    np.all(np.linalg.norm(full_factors,axis=1)<=full_factor_bound+2e-11))
                cubic_factor = quadratic_factor+jets[:,0,2,None]*cubic[None,mask]/6
                cubic_factor += (jets[:,1,2]-jets[:,0,2])[:,None]*cubic_hinge[None,mask]/6
                cubic_factor -= leading[:,None]*system.lifted_hinge[None,mask]
                model = FlatPreassembledFlow(system)
                reference_model = FlatPreassembledFlow(LocallyRefinedSourceAction(count,False,background_mass=0.,source_splits=8))
                gram_forces,source_forces,quadratic_forces,cubic_forces,force_bounds,force_identity_errors = [],[],[],[],[],[]
                full_force_bounds = []
                for index,state in enumerate(projected):
                    field,position,speed = state[:system.count],state[system.count],state[-2]
                    matrices = model.matrices(position)
                    cross = band_product(matrices['transport'],field)
                    inverse_cross = solve_banded((2,2),matrices['mass'],cross,check_finite=False)
                    inertia = system.source_mass/(1-speed**2)**1.5
                    schur = inertia+field @ band_product(matrices['square'],field)-cross @ inverse_cross
                    if schur<=0:
                        raise ValueError('Nonpositive coupled inertia.')
                    weight = system.lifted @ inverse_cross
                    actual = system.lifted @ field
                    diagonal,diagonal_b = matrices['gram'],matrices['gram_b']
                    complete_force = inertia/schur*(weight @ (diagonal*actual)-actual @ (diagonal_b*actual)/2)
                    gram_forces.append(float(complete_force))
                    transport_energy = float(field @ band_product(matrices['square'],field))
                    if transport_energy<0:
                        raise ValueError('Negative transport kinetic form.')
                    jacobians = 1+model.jacobian_slopes*(position-system.anchor)
                    mass_lower = system.radii[0]**2*min(jacobians)*min(np.diff(system.edges))*(19-np.sqrt(201))/60
                    lift_norm_bound = 8/np.sqrt(8)+np.linalg.norm(system.lifted_hinge)*np.linalg.norm(system.jump)
                    weight_bound = lift_norm_bound*np.sqrt(transport_energy/mass_lower)
                    full_force_bounds.append(float(inertia/schur*(weight_bound*max(abs(diagonal))*full_factor_bound[index]
                        +max(abs(diagonal_b))*full_factor_bound[index]**2/2)))
                    for factors,collector in [(actual[mask],source_forces),(quadratic_factor[index],quadratic_forces),(cubic_factor[index],cubic_forces)]:
                        collector.append(float(inertia/schur*(weight[mask] @ (diagonal[mask]*factors)-factors @ (diagonal_b[mask]*factors)/2)))
                    factor_bound = local_factor_bound[index]
                    force_bounds.append(float(inertia/schur*(np.linalg.norm(diagonal[mask]*weight[mask]-diagonal_b[mask]*quadratic_factor[index])*factor_bound
                        +max(abs(diagonal_b[mask]))*factor_bound**2/2)))
                    if index in [0,37,42,80]:
                        force_identity_errors.append(float(abs(complete_force-(model.evaluate(state)['force']-reference_model.evaluate(state)['force']))))
                gram_forces,source_forces,quadratic_forces,cubic_forces,force_bounds = map(np.array,
                    [gram_forces,source_forces,quadratic_forces,cubic_forces,force_bounds])
                evidence.check(str(degree)+'_'+str(count)+'_exact_Gram_material_force_identity',max(force_identity_errors)<2e-11,max(force_identity_errors))
                evidence.check(str(degree)+'_'+str(count)+'_source_force_factor_remainder_bound',
                    np.all(abs(source_forces-quadratic_forces)<=force_bounds+2e-11))
                full_force_bounds = np.array(full_force_bounds)
                evidence.check(str(degree)+'_'+str(count)+'_global_Gram_force_energy_bound',
                    np.all(abs(gram_forces)<=full_force_bounds+2e-11))
                norms = np.linalg.norm(actual_factor,axis=1)
                row = dict(degree=degree,count=count,source_splits=8,phase=evidence.report['mesh_cases'][[entry['count'] for entry in evidence.report['mesh_cases']].index(count)]['phase'],
                    maximum_trace_error=float(max(abs(jump_error))),maximum_cubic_trace_residual=float(max(abs(jump_error-leading))),
                    maximum_quartic_trace_residual=float(max(abs(jump_error-leading-fourth))),
                    maximum_global_polynomial_third_bound=float(max(basic_bound)),
                    maximum_global_polynomial_fifth_bound=float(max(higher_bound)),
                    maximum_curvature_jump=float(max(abs(curvature_jump))),maximum_source_factor_norm=float(max(norms)),
                    maximum_boundary_curvature_compatibility_residual=float(np.max(abs(jets[:,:,1]-boundary_curvatures))),
                    boundary_curvature_jump_at_021=float(boundary_curvatures[42,1]-boundary_curvatures[42,0]),
                    projected_curvature_jump_at_021=float(curvature_jump[42]),
                    maximum_quadratic_factor_residual=float(max(np.linalg.norm(actual_factor-quadratic_factor,axis=1))),
                    maximum_local_curvature_factor_bound=float(max(local_factor_bound)),
                    maximum_cubic_factor_residual=float(max(np.linalg.norm(actual_factor-cubic_factor,axis=1))),
                    trace_at_021=float(jump_error[42]),cubic_trace_at_021=float(leading[42]),quartic_trace_at_021=float((leading+fourth)[42]),
                    source_factor_at_021=float(norms[42]),quadratic_factor_at_021=float(np.linalg.norm(quadratic_factor[42])),
                    maximum_Gram_force=float(max(abs(gram_forces))),maximum_source_row_Gram_force=float(max(abs(source_forces))),
                    maximum_quadratic_source_force_residual=float(max(abs(source_forces-quadratic_forces))),
                    maximum_cubic_source_force_residual=float(max(abs(source_forces-cubic_forces))),
                    maximum_source_force_bound=float(max(force_bounds)),Gram_force_at_021=float(gram_forces[42]),
                    maximum_global_Gram_factor_bound=float(max(full_factor_bound)),
                    maximum_global_Gram_force_energy_bound=float(max(full_force_bounds)),
                    source_Gram_force_at_021=float(source_forces[42]),quadratic_Gram_force_at_021=float(quadratic_forces[42]),
                    cubic_Gram_force_at_021=float(cubic_forces[42]),
                    continuum_jet_bounds_established=False)
                evidence.report['cases'].append(row)
                destination = evidence.output/('trace-'+str(degree)+'-'+str(count)+'.npz')
                np.savez_compressed(destination,times=times,jets=jets,jump_error=jump_error,leading_trace=leading,
                    quartic_trace=leading+fourth,third_bound=basic_bound,fifth_bound=higher_bound,
                    boundary_curvatures=boundary_curvatures,
                    actual_source_factor=actual_factor,quadratic_factor=quadratic_factor,cubic_factor=cubic_factor,
                    local_curvature_factor_bound=local_factor_bound,
                    Gram_force=gram_forces,source_Gram_force=source_forces,quadratic_Gram_force=quadratic_forces,
                    cubic_Gram_force=cubic_forces,source_force_bound=force_bounds,
                    global_Gram_factor_bound=full_factor_bound,global_Gram_force_energy_bound=full_force_bounds,
                    source_rows=np.flatnonzero(mask))
                evidence.own(destination,'outputs')
                evidence.save()
                print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
