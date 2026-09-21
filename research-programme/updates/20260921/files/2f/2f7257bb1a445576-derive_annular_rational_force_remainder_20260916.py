from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import solve_banded
import argparse
import hashlib
import json
import numpy as np
import sympy as sp


def quadratic_parts(model, position, speed, field, rates):
    matrices = model.matrices(position)
    cross = band_product(matrices['transport'],field)
    square_field = band_product(matrices['square'],field)
    mass_b_rate = band_product(matrices['mass_b'],rates)
    transport_rate = band_product(matrices['transport'],rates)
    drift = mass_b_rate+transport_rate-band_product(matrices['transport'],rates,True)
    factor = model.lifted @ field
    stiffness = band_product(matrices['bulk'],field)+model.lifted_transpose @ (matrices['gram']*factor)
    second = band_product(matrices['transport_b'],field)-square_field
    solved = solve_banded((2,2),matrices['mass'],np.column_stack([cross,drift,stiffness,second]),check_finite=False)
    denominator_quadratic = field @ square_field-cross @ solved[:,0]
    numerator = rates @ (mass_b_rate/2-transport_rate)
    numerator += speed*(cross @ solved[:,1]-2*rates @ square_field)
    numerator += cross @ solved[:,2]+speed**2*cross @ solved[:,3]
    numerator -= speed**2*(field @ band_product(matrices['square_b'],field))/2
    numerator -= (field @ band_product(matrices['bulk_b'],field)+factor @ (matrices['gram_b']*factor))/2
    return numerator,denominator_quadratic


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        inertia,numerator0,numerator1,numerator2,denominator0,denominator1,denominator2 = sp.symbols('mu N0 N1 N2 d0 d1 d2')
        force0 = inertia*numerator0/denominator0
        linear = inertia*(numerator1*denominator0-numerator0*denominator1)/denominator0**2
        full = inertia*(numerator0+numerator1+numerator2)/(denominator0+denominator1+denominator2)
        remainder = (inertia*numerator2-force0*denominator2-linear*(denominator1+denominator2))/(denominator0+denominator1+denominator2)
        evidence.check('exact_quadratic_over_quadratic_remainder_identity',sp.factor(full-force0-linear-remainder)==0)
        evidence.report.update(exact_fixed_geometry_remainder_derived=True,source_position_and_speed_held_fixed_for_bound=True,
            source_geometry_response_separately_retained=True,uniform_trajectory_bound=False,
            retrospective_state_errors_used=True,force_correction=False)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        projection_folder = intake/'annular-GR-projection-residual-attempt02'
        analysis_folder = intake/'annular-GR-projection-analysis-attempt01'
        statuses = {}
        for name,folder in [('projection',projection_folder),('analysis',analysis_folder)]:
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(name+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            statuses[name] = status
        for count in [257,513,1025]:
            path = projection_folder/('projection-768-'+str(count)+'.npz')
            evidence.own(path)
            evidence.check(str(count)+'_projection_hash',hashlib.sha256(path.read_bytes()).hexdigest()==statuses['projection']['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path,allow_pickle=False) as saved:
                times,states = saved['times'].copy(),saved['states'].copy()
            for branch in ['reference','MTS']:
                prefix = branch+str(count)
                path = analysis_folder/(prefix+'-retrospective-attribution.npz')
                evidence.own(path)
                evidence.check(prefix+'_error_hash',hashlib.sha256(path.read_bytes()).hexdigest()==statuses['analysis']['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path,allow_pickle=False) as saved:
                    errors = saved['actual_state_error'].copy()
                system = LocallyRefinedSourceAction(count,branch=='MTS',background_mass=0.,source_splits=8)
                model = FlatPreassembledFlow(system)
                records,force_errors,identity_errors,bound_margins,inertia_margins = [],[],[],[],[]
                for state,error in zip(states,errors):
                    field,rates = state[:system.count],state[system.count+1:-2]
                    field_error,rate_error = error[:system.count],error[system.count+1:-2]
                    position,speed = state[system.count],state[-2]
                    material = system.source_mass/(1-speed**2)**1.5
                    numerator0,quadratic0 = quadratic_parts(model,position,speed,field,rates)
                    numerator1,denominator1 = quadratic_parts(model,position,speed,
                        field.astype(complex)+1e-25j*field_error,rates.astype(complex)+1e-25j*rate_error)
                    numerator1,denominator1 = numerator1.imag/1e-25,denominator1.imag/1e-25
                    numerator2,denominator2 = quadratic_parts(model,position,speed,field_error,rate_error)
                    denominator0 = material+quadratic0
                    base_force = material*numerator0/denominator0
                    linear = material*(numerator1*denominator0-numerator0*denominator1)/denominator0**2
                    denominator = denominator0+denominator1+denominator2
                    predicted_remainder = (material*numerator2-base_force*denominator2-linear*(denominator1+denominator2))/denominator
                    bound = (material*abs(numerator2)+abs(base_force)*abs(denominator2)
                        +abs(linear)*(abs(denominator1)+abs(denominator2)))/material
                    shifted = state.copy()
                    shifted[:system.count] += field_error
                    shifted[system.count+1:-2] += rate_error
                    unchanged = model.evaluate(state)
                    shifted_force = model.evaluate(shifted)['force']
                    actual_force = model.evaluate(state+error)['force']
                    measured_remainder = shifted_force-unchanged['force']-linear
                    source_geometry_part = actual_force-shifted_force
                    force_errors.append(abs(base_force-unchanged['force']))
                    identity_errors.append(abs(measured_remainder-predicted_remainder))
                    bound_margins.append(bound-abs(measured_remainder))
                    inertia_margins.append(denominator-material)
                    records.append([linear,predicted_remainder,measured_remainder,bound,source_geometry_part])
                evidence.check(prefix+'_rational_force_matches_original',max(force_errors)<2e-11,float(max(force_errors)))
                evidence.check(prefix+'_exact_finite_amplitude_remainder',max(identity_errors)<2e-11,float(max(identity_errors)))
                evidence.check(prefix+'_positive_kinetic_residual',min(inertia_margins)>-2e-13,float(min(inertia_margins)))
                evidence.check(prefix+'_derived_remainder_bound',min(bound_margins)>-2e-12,float(min(bound_margins)))
                records = np.array(records)
                destination = evidence.output/(prefix+'-rational-remainder.npz')
                np.savez_compressed(destination,times=times,linear=records[:,0],predicted_remainder=records[:,1],
                    measured_remainder=records[:,2],derived_bound=records[:,3],source_geometry_part=records[:,4])
                evidence.own(destination,'outputs')
                row = dict(branch=branch,count=count,max_remainder=float(np.max(abs(records[:,2]))),
                    max_derived_bound=float(np.max(records[:,3])),max_source_geometry_part=float(np.max(abs(records[:,4]))),
                    remainder_at_021=float(records[42,2]),bound_at_021=float(records[42,3]),
                    force_identity_error=float(max(force_errors)),remainder_identity_error=float(max(identity_errors)),
                    minimum_inertia_above_material=float(min(inertia_margins)))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
