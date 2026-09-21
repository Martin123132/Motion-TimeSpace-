from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
from datetime import datetime, timezone
from pathlib import Path
from fractions import Fraction
import csv
import hashlib
import json
import re
import traceback
import numpy as np


def stored(values):
    return np.array([Decimal(value) for value in values.ravel()]).reshape(values.shape)


def exact(values):
    return np.array([Decimal.from_float(float(value)) for value in np.asarray(values).ravel()]).reshape(np.shape(values))


def difference(positive, negative, step):
    with localcontext() as context:
        context.prec = 64
        return np.asarray((exact(positive)-exact(negative))/(2*Decimal.from_float(step)),float)


def decimal_difference(positive, negative, step):
    with localcontext() as context:
        context.prec = 64
        return np.asarray((positive-negative)/(2*Decimal.from_float(step)),float)


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-source-acceleration-v3'
    destination = intake/(prefix+'-final-integrity.json')
    if destination.exists():
        raise FileExistsError('Immutable seal already exists.')
    report = dict(state='running',inputs={},outputs={},checks=[],candidate_only=True,github_action=False,
        subagents_used=False,valid_for_physics_claim=False,full_GR_limit_proven=False,
        independent_cases=[],independent_probes=[],physical_summaries=[],analytic_controls=[],tangent_block_diagnostics=[],
        probe_scale_comparisons=[],dust_reaction_summaries=[],dust_reaction_components=[],traction_summaries=[],
        paired_branch_contrasts=[],paired_contrast_sensitivity=[],
        protected_scan_scope='mtime since2026-09-21T14:47:07Z; not a pre-turn whole-tree hash baseline')
    hashes = {}

    def digest(path):
        path = path.resolve()
        if path not in hashes:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            hashes[path] = hasher.hexdigest()
        return hashes[path]

    def own(path,category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs','outputs']:
            for name,expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed owned input: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting owned input: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    def loaded(path):
        own(path)
        with np.load(path,allow_pickle=False) as data:
            return {key:data[key].copy() for key in data.files}

    def agree(actual,expected):
        return bool(np.all(np.isfinite(actual)) and np.all(np.isfinite(expected))
            and np.max(abs(actual-expected)) <= 2e-12*max(float(np.max(abs(expected))),1e-20))

    def table(label,rows,source):
        path = intake/(prefix+'-'+label+'.csv')
        if path.exists():
            raise FileExistsError(str(path))
        flat = [dict(row,record_source=str(source.relative_to(root))) for row in rows]
        fields = list(dict.fromkeys(key for row in flat for key in row))
        with path.open('w',encoding='utf-8',newline='') as stream:
            writer = csv.DictWriter(stream,fieldnames=fields)
            writer.writeheader()
            writer.writerows(flat)
        with path.open(encoding='utf-8',newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(label+'_sourced_rows_parse',len(parsed) == len(rows) and all(None not in row
            and None not in row.values() and row['valid_for_claim'] == 'False'
            and (root/row['record_source']).is_file() for row in parsed))
        own(path,'outputs')
        return len(parsed)

    def samples_check(name,values):
        radius = values['cardinal'] @ np.asarray(stored(values['coordinates'])[:,-1],float)
        velocity = values['cardinal'] @ values['rates'][:,-1]
        metric = 1-2*values['mass']/radius
        clock = np.sqrt(values['lapse']**2-velocity**2/metric)
        check(name+'_physical_sampling_and_timelike_clock',agree(radius,values['radius'])
            and agree(velocity,values['velocity']) and agree(metric,values['metric']) and agree(clock,values['clock'])
            and agree(velocity/clock,values['proper_velocity']) and min(metric) > 0 and min(clock) > 0)

    save()
    try:
        prior = inherit(intake/'annular-candidate-finer-time-final-integrity.json')
        check('previous_seal_complete_unchanged',prior['state'] == 'complete' and all(row['passed'] for row in prior['checks']))
        failed = inherit(intake/'annular-candidate-source-acceleration-final-integrity.json')
        own(root/'scripts/seal_annular_candidate_source_acceleration_20260921.py')
        check('failed_first_postflight_preserved',failed['state'] == 'failed'
            and failed['checks'][-1]['name'] == 'reference-reference-endpoint_dust_EL_geodesic_identity_and_field_reaction'
            and not failed['checks'][-1]['passed'])
        failed_v2 = inherit(intake/'annular-candidate-source-acceleration-v2-final-integrity.json')
        own(root/'scripts/seal_annular_candidate_source_acceleration_v2_20260921.py')
        check('failed_second_postflight_preserved',failed_v2['state'] == 'failed'
            and 'not subscriptable' in failed_v2['error'] and len(failed_v2['independent_cases']) == 9)
        report['failed_postflight_v2_source'] = 'source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-v2-final-integrity.json'
        report['failed_postflight_source'] = 'source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-final-integrity.json'
        report['reaction_gate_policy'] = dict(original_raw_closure_relative_tolerance=2e-6,
            corrected_accounting_tolerance=1e-9,corrected_accounting_is_not_physical_validation=True,
            raw_scientific_failures_retained=True)
        energy_run = inherit(intake/'annular-candidate-fine16-quadrature-attempt01/status.json')
        source_masses = {}
        for row in energy_run['endpoints']:
            if row['label'] == 'fine':
                source_masses[row['branch'],row['extension']] = float(loaded(root/row['path'])['source_mass'])
        meshes,models = {},{}
        for branch in ['reference','MTS']:
            path = intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json')
            own(path)
            meshes[branch] = json.loads(path.read_text())['overlay']
            models[branch] = IndexedGradedP2System(257,branch == 'MTS',2e-5)
        import sympy as sp
        alpha,beta,field_t,gradient,speed = sp.symbols('alpha beta field_t gradient speed',real=True)
        density = alpha*field_t**2/2-beta*gradient**2/2
        boundary = density-gradient*(sp.diff(density,gradient)-speed*sp.diff(density,field_t))
        check('moving_Dirichlet_boundary_traction_algebra',sp.simplify(boundary.subs(field_t,-speed*gradient)-
            (beta-alpha*speed**2)*gradient**2/2) == 0)
        material_mass,radial_speed,radial_acceleration,metric_value,clock_rate,lapse_value = sp.symbols(
            'material_mass radial_speed radial_acceleration metric_value clock_rate lapse_value',nonzero=True)
        metric_dot,metric_r,lapse_r,clock_dot = sp.symbols('metric_dot metric_r lapse_r clock_dot')
        dust_momentum_rate = material_mass*(radial_acceleration/(metric_value*clock_rate)
            -radial_speed*metric_dot/(metric_value**2*clock_rate)
            -radial_speed*clock_dot/(metric_value*clock_rate**2))
        dust_coordinate_force = -material_mass*(lapse_value*lapse_r
            +radial_speed**2*metric_r/(2*metric_value**2))/clock_rate
        proper_radial = radial_acceleration/clock_rate**2-radial_speed*clock_dot/clock_rate**3
        geodesic_radial = (-metric_value*lapse_value*lapse_r
            +radial_speed*(metric_dot-radial_speed*metric_r)/metric_value
            +radial_speed**2*metric_r/(2*metric_value))/clock_rate**2
        check('exact_dust_EL_equals_weighted_geodesic_residual',sp.simplify(dust_momentum_rate
            -dust_coordinate_force-material_mass*clock_rate/metric_value*(proper_radial-geodesic_radial)) == 0)
        runs = []
        for folder,expected_cases,expected_steps in [
            ('annular-candidate-source-acceleration-attempt01',6,[1e-5,5e-6,2.5e-6]),
            ('annular-candidate-source-acceleration-wide-probes-attempt01',3,[1e-4,5e-5,2.5e-5])]:
            run_path = intake/folder/'status.json'
            run = inherit(run_path)
            runs.append((run_path,run))
            check('run_complete_equal_branches',run['state'] == 'complete' and all(row['passed'] for row in run['checks'])
                and len(run['cases']) == expected_cases and len(run['probes']) == expected_cases*6 and len(run['samples']) == expected_cases*64)
            check('full_inverse_and_same_action',run['full_components'] == 16425 and not run['modes_deleted']
                and run['original_action_unchanged'] and run['reference_order'] == 16 and run['material_order'] == 48
                and run['derivative_steps'] == expected_steps and not run['geodesic_match_claimed'])
            inverses = {}
            for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
                path = intake/'annular-candidate-full-canonical-inverse-attempt01'/(branch+'-'+extension+'-22-fixed-metric-mass.npz')
                own(path)
                inverses[branch,extension] = BandedSourceInverse(load_npz(path),(15,1095))
            for case in run['cases']:
                branch,extension,label = [case[key] for key in ['branch','extension','label']]
                name = branch+'-'+extension+'-'+label
                case_home = (root/case['path']).parent
                base = loaded(root/case['path'])
                source = loaded(root/case['source_path'])
                position,momentum,force = [stored(base[key]) for key in ['coordinates','momenta','force_decimal']]
                source_p = source['momenta'] if label == 'initial' else source['target_momenta']
                source_v = source['midpoint_rates'] if label == 'initial' else source['endpoint_rates']
                check(name+'_original_phase_point_preserved',np.array_equal(position,stored(source['coordinates']))
                    and np.array_equal(momentum,stored(source_p)) and np.array_equal(base['rates'],source_v))
                nodes = base['labels'][48:63]
                cardinal = (np.polynomial.chebyshev.chebvander(2*base['labels'],14) @
                    np.linalg.inv(np.polynomial.chebyshev.chebvander(2*nodes,14)))
                check(name+'_independent_material_interpolation',np.max(abs(cardinal-base['cardinal'])) < 2e-12)
                samples_check(name,base)
                inverse = inverses[branch,extension]
                probes = {}
                for row in [item for item in run['probes'] if all(item[key] == case[key] for key in ['branch','extension','label'])]:
                    raw = loaded(root/row['path'])
                    with localcontext() as context:
                        context.prec = 64
                        parameter = Decimal.from_float(row['sign']*row['step'])
                        q_match = np.array_equal(stored(raw['coordinates']),position+parameter*exact(base['rates']))
                        p_match = np.array_equal(stored(raw['momenta']),momentum+parameter*force)
                        residual = np.asarray(exact(raw['computed_momentum'])-stored(raw['momenta']),float)
                    relative = inverse.residual_norm(residual)/inverse.residual_norm(np.asarray(stored(raw['momenta']),float))
                    correction = inverse.solve(residual.ravel()).reshape(base['rates'].shape)
                    check(name+'_'+str(row['index'])+'_'+str(row['sign'])+'_exact_phase_probe_and_inverse',
                        q_match and p_match and relative < 5e-12 and np.max(abs(correction)) < 2e-12
                        and agree(correction,raw['preconditioned_residual']))
                    samples_check(name+'_'+str(row['index'])+'_'+str(row['sign']),raw)
                    probes[row['index'],row['sign']] = raw
                    report['independent_probes'].append(dict(branch=branch,extension=extension,label=label,index=row['index'],
                        sign=row['sign'],relative_residual=relative,maximum_correction=float(np.max(abs(correction))),
                        source_correction_derivative_scale=float(np.max(abs(correction[:,-1]))/row['step']),
                        correction_scale_is_not_error_bound=True,valid_for_claim=False))
                direct = []
                for index,step in enumerate(run['derivative_steps']):
                    plus,minus = probes[index,1],probes[index,-1]
                    values = dict(acceleration=difference(plus['rates'],minus['rates'],step))
                    values.update({key+'_dot':difference(plus[key],minus[key],step)
                        for key in ['lapse','metric','clock','proper_velocity']})
                    direct.append(values)
                refined = [{key:(4*direct[index+1][key]-direct[index][key])/3 for key in direct[0]} for index in range(2)]
                result = loaded(case_home/(name+'-acceleration.npz'))
                check(name+'_all_derivatives_reconstructed',all(agree(value,result['richardson_'+str(index)+'_'+key])
                    for index,row in enumerate(refined) for key,value in row.items()) and
                    all(agree(value,result['direct'+str(index)+'_'+key]) for index,row in enumerate(direct) for key,value in row.items()))
                physical = []
                for row in refined:
                    acceleration = base['cardinal'] @ row['acceleration'][:,-1]
                    velocity,lapse,metric,clock = [base[key] for key in ['velocity','lapse','metric','clock']]
                    clock_dot = (2*lapse*row['lapse_dot']-2*velocity*acceleration/metric+
                        velocity**2*row['metric_dot']/metric**2)/(2*clock)
                    proper = acceleration/clock**2-velocity*clock_dot/clock**3
                    metric_t = row['metric_dot']-velocity*base['metric_radial']
                    connection_tt = metric*lapse*base['lapse_radial']
                    connection_tr = -metric_t/(2*metric)
                    connection_rr = -base['metric_radial']/(2*metric)
                    geodesic = -(connection_tt+2*connection_tr*velocity+connection_rr*velocity**2)/clock**2
                    physical.append(dict(proper_acceleration=proper,geodesic_acceleration=geodesic,
                        direct_proper_acceleration=row['proper_velocity_dot']/clock,clock_chain=clock_dot,
                        source_acceleration=acceleration,geodesic_residual=proper-geodesic,
                        newton_proxy=-base['mass']/base['radius']**2,metric_partial_time=metric_t))
                physical_scale = max(float(np.max(abs(physical[-1]['proper_acceleration']))),
                    float(np.max(abs(physical[-1]['geodesic_acceleration']))),1e-20)
                check(name+'_proper_clock_and_independent_Christoffel_conversion',all(
                    np.max(abs(value-result[key])) <= 2e-12*max(float(np.max(abs(value))),physical_scale)
                    for key,value in physical[-1].items()))
                for row in [item for item in run['derivative_checks'] if all(item[key] == case[key] for key in ['branch','extension','label'])]:
                    key = row['quantity']
                    if key.startswith('coordinate_acceleration_'):
                        section = slice(None,-1) if key.endswith('field') else slice(-1,None)
                        first,second = [value['acceleration'][:,section] for value in refined]
                    elif key == 'proper_chain_versus_direct_velocity_derivative':
                        first,second = physical[-1]['direct_proper_acceleration'],physical[-1]['proper_acceleration']
                    else:
                        first,second = [value[key] for value in physical]
                    discrepancy = float(np.max(abs(first-second)))
                    signal = max(float(np.max(abs(second))),1e-30)
                    tolerance = 1e-8+2e-3*signal
                    check(name+'_'+key+'_scientific_gate_reconstructed',abs(discrepancy-row['discrepancy']) < 2e-12*signal
                        and row['passed'] == (discrepancy <= tolerance))
                tangent_step = run['derivative_steps'][-1]/2
                tangents = {}
                for tangent_label in ['coordinate','velocity','joint']:
                    records = [loaded(case_home/(name+'-'+tangent_label+str(sign)+'-tangent.npz')) for sign in [1,-1]]
                    for sign,raw in zip([1,-1],records):
                        direction_q = base['rates'] if tangent_label != 'velocity' else np.zeros_like(base['rates'])
                        direction_v = refined[-1]['acceleration'] if tangent_label != 'coordinate' else np.zeros_like(base['rates'])
                        with localcontext() as context:
                            context.prec = 64
                            expected_q = position+Decimal.from_float(sign*tangent_step)*exact(direction_q)
                        check(name+'_'+tangent_label+str(sign)+'_independent_tangent_inputs',
                            np.array_equal(stored(raw['coordinates']),expected_q)
                            and np.array_equal(raw['rates'],base['rates']+sign*tangent_step*direction_v))
                    tangents[tangent_label] = difference(records[0]['momentum'],records[1]['momentum'],tangent_step)
                raw_force = np.asarray(force,float)
                scale = max(inverse.residual_norm(raw_force),1e-30)
                defects = dict(full_chain_residual=tangents['coordinate']+tangents['velocity']-raw_force,
                    joint_chain_residual=tangents['joint']-raw_force,
                    split_versus_joint=tangents['coordinate']+tangents['velocity']-tangents['joint'])
                for row in [item for item in run['tangent_checks'] if all(item[key] == case[key] for key in ['branch','extension','label'])]:
                    measured = inverse.residual_norm(defects[row['quantity']])/scale
                    check(name+'_'+row['quantity']+'_gate_reconstructed',measured == row['relative_residual']
                        and row['passed'] == (measured < 2e-3))
                    for block,section in [('field',slice(None,-1)),('source',slice(-1,None))]:
                        scaling = inverse.original_scale.reshape(raw_force.shape)[:,section]
                        numerator = np.linalg.norm(defects[row['quantity']][:,section]/scaling)
                        denominator = np.linalg.norm(raw_force[:,section]/scaling)
                        report['tangent_block_diagnostics'].append(dict(branch=branch,extension=extension,label=label,
                            quantity=row['quantity'],block=block,relative_residual=float(numerator/max(denominator,1e-30)),
                            diagnostic_only=True,valid_for_claim=False))
                for row in [item for item in run['samples'] if all(item[key] == case[key] for key in ['branch','extension','label'])]:
                    index = row['sample_index']
                    check(name+'_sample'+str(index)+'_physical_row_matches',all(abs(row[key]-value[index]) <
                        2e-12*max(abs(value[index]),physical_scale) for key,value in physical[-1].items()))
                weight = base['weights']
                source_mass = source_masses[branch,extension]
                cardinal = base['cardinal'][:48]
                velocity,lapse,metric,clock = [base[key][:48] for key in ['velocity','lapse','metric','clock']]
                dust_force_density = -source_mass*(lapse*base['lapse_radial'][:48]+
                    velocity**2*base['metric_radial'][:48]/(2*metric**2))/clock
                dust_force = cardinal.T @ (weight*dust_force_density)
                dust_derivatives,field_derivatives,root_derivatives,target_field_derivatives = [],[],[],[]
                target_total_derivatives = []
                for index,step in enumerate(run['derivative_steps']):
                    dust_momenta,field_momenta,root_errors,target_field_momenta,target_total_momenta = [],[],[],[],[]
                    for sign in [1,-1]:
                        sample = probes[index,sign]
                        density = source_mass*sample['velocity'][:48]/(sample['metric'][:48]*sample['clock'][:48])
                        dust_momentum = cardinal.T @ (weight*density)
                        dust_momenta.append(dust_momentum)
                        field_momenta.append(sample['computed_momentum'][:,-1]-dust_momentum)
                        with localcontext() as context:
                            context.prec = 64
                            target = stored(sample['momenta'])[:,-1]
                            target_total_momenta.append(target)
                            root_errors.append(exact(sample['computed_momentum'][:,-1])-target)
                            target_field_momenta.append(target-exact(dust_momentum))
                    dust_derivatives.append(difference(dust_momenta[0],dust_momenta[1],step))
                    field_derivatives.append(difference(field_momenta[0],field_momenta[1],step))
                    root_derivatives.append(decimal_difference(root_errors[0],root_errors[1],step))
                    target_field_derivatives.append(decimal_difference(target_field_momenta[0],target_field_momenta[1],step))
                    target_total_derivatives.append(decimal_difference(target_total_momenta[0],target_total_momenta[1],step))
                dust_rate = (4*dust_derivatives[2]-dust_derivatives[1])/3
                field_rate = (4*field_derivatives[2]-field_derivatives[1])/3
                root_rate = (4*root_derivatives[2]-root_derivatives[1])/3
                target_field_rate = (4*target_field_derivatives[2]-target_field_derivatives[1])/3
                target_total_rate = (4*target_total_derivatives[2]-target_total_derivatives[1])/3
                field_force = np.asarray(force[:,-1],float)-dust_force
                reaction = field_force-field_rate
                target_reaction = field_force-target_field_rate
                corrected_reaction = reaction+root_rate
                dust_euler = dust_rate-dust_force
                projected = cardinal.T @ (weight*source_mass*clock/metric*
                    (physical[-1]['proper_acceleration'][:48]-physical[-1]['geodesic_acceleration'][:48]))
                reference_scale = max(float(np.linalg.norm(dust_force)),1e-30)
                identity_error = float(np.linalg.norm(dust_euler-projected)/reference_scale)
                action_closure = float(np.linalg.norm(reaction-dust_euler)/reference_scale)
                corrected_closure = float(np.linalg.norm(corrected_reaction-dust_euler)/reference_scale)
                target_closure = float(np.linalg.norm(target_reaction-dust_euler)/reference_scale)
                target_total_error = float(np.linalg.norm(target_total_rate-np.asarray(force[:,-1],float))/reference_scale)
                check(name+'_dust_EL_geodesic_identity',identity_error < 2e-6,identity_error)
                check(name+'_inverse_residual_derivative_accounts_for_raw_mismatch',
                    corrected_closure < 1e-9 and target_closure < 1e-9 and target_total_error < 1e-9,
                    dict(raw_closure=action_closure,corrected_closure=corrected_closure,
                        target_closure=target_closure,target_total_derivative_error=target_total_error))
                report['dust_reaction_summaries'].append(dict(branch=branch,extension=extension,label=label,
                    source_mass=source_mass,dust_force_norm=reference_scale,field_force_norm=float(np.linalg.norm(field_force)),
                    field_momentum_rate_norm=float(np.linalg.norm(field_rate)),reaction_norm=float(np.linalg.norm(reaction)),
                    reaction_to_dust_force=float(np.linalg.norm(reaction)/reference_scale),
                    cancellation_ratio=float(np.linalg.norm(reaction)/max(np.linalg.norm(field_force)+np.linalg.norm(field_rate),1e-30)),
                    dust_identity_relative_error=identity_error,full_action_closure_relative_error=action_closure,
                    original_raw_closure_tolerance=2e-6,original_raw_closure_passed=action_closure < 2e-6,
                    root_residual_derivative_norm=float(np.linalg.norm(root_rate)),
                    root_derivative_relative_to_dust_force=float(np.linalg.norm(root_rate)/reference_scale),
                    root_derivative_relative_to_raw_reaction=float(np.linalg.norm(root_rate)/max(np.linalg.norm(reaction),1e-30)),
                    target_owned_reaction_norm=float(np.linalg.norm(target_reaction)),
                    projected_geodesic_residual_norm=float(np.linalg.norm(projected)),
                    corrected_accounting_relative_error=corrected_closure,target_accounting_relative_error=target_closure,
                    corrected_accounting_is_not_independent_physics_evidence=True,
                    weak_material_projection_only=True,valid_for_claim=False))
                for index in range(15):
                    report['dust_reaction_components'].append(dict(branch=branch,extension=extension,label=label,index=index,
                        dust_force=float(dust_force[index]),dust_momentum_rate=float(dust_rate[index]),
                        non_dust_force=float(field_force[index]),non_dust_momentum_rate=float(field_rate[index]),
                        reaction=float(reaction[index]),root_residual_derivative=float(root_rate[index]),
                        target_owned_reaction=float(target_reaction[index]),corrected_reaction=float(corrected_reaction[index]),
                        projected_geodesic_residual=float(projected[index]),valid_for_claim=False))
                mesh,model = meshes[branch],models[branch]
                edges = list(map(Fraction,mesh['edges']))
                hinge = edges.index(Fraction.from_float(float(model.model.anchor)))
                check(name+'_moving_zero_field_anchor_is_in_saved_space',mesh['elements'][hinge-1][-1] == -1
                    and mesh['elements'][hinge][0] == -1)
                with localcontext() as context:
                    context.prec = 64
                    slopes = []
                    for cell,coefficients in [(hinge-1,[1,-4,3]),(hinge,[-3,4,-1])]:
                        derivative = np.full(15,Decimal(0),dtype=object)
                        for index,coefficient in zip(mesh['elements'][cell],coefficients):
                            if index >= 0:
                                derivative += coefficient*position[:,index]
                        width = edges[cell+1]-edges[cell]
                        slopes.append(np.asarray(derivative/(Decimal(width.numerator)/Decimal(width.denominator)),float))
                source_radius = base['radius'][:48]
                lower = model.model.radii[0]+model.width*base['labels'][:48]
                upper = model.model.radii[-1]+model.width*base['labels'][:48]
                jacobian_left = (source_radius-lower)/(model.model.anchor-model.model.radii[0])
                jacobian_right = (upper-source_radius)/(model.model.radii[-1]-model.model.anchor)
                left_gradient = (cardinal @ slopes[0])/jacobian_left
                right_gradient = (cardinal @ slopes[1])/jacobian_right
                traction_density = (source_radius**2*np.sqrt(metric)*clock**2/(2*lapse)*
                    (left_gradient**2-right_gradient**2))
                traction = cardinal.T @ (weight*traction_density)
                traction_defect = reaction-traction
                traction_path = intake/(prefix+'-'+name+'-traction.npz')
                if traction_path.exists():
                    raise FileExistsError(str(traction_path))
                np.savez_compressed(traction_path,left_gradient=left_gradient,right_gradient=right_gradient,
                    traction_density=traction_density,projected_traction=traction,measured_reaction=reaction,
                    residual=traction_defect,labels=base['labels'][:48],weights=weight)
                own(traction_path,'outputs')
                report['traction_summaries'].append(dict(branch=branch,extension=extension,label=label,
                    traction_norm=float(np.linalg.norm(traction)),reaction_norm=float(np.linalg.norm(reaction)),
                    reaction_minus_traction_norm=float(np.linalg.norm(traction_defect)),
                    discrepancy_relative_to_dust_force=float(np.linalg.norm(traction_defect)/reference_scale),
                    discrepancy_relative_to_raw_reaction=float(np.linalg.norm(traction_defect)/max(np.linalg.norm(reaction),1e-30)),
                    includes_unseparated_Gram_and_Galerkin_remainders=True,
                    physical_interpretation_of_anchor_not_assumed=True,valid_for_claim=False))
                proper,geodesic = physical[-1]['proper_acceleration'],physical[-1]['geodesic_acceleration']
                rms = float(np.sqrt(weight @ ((proper[:48]-geodesic[:48])**2)))
                scale = float(np.sqrt(weight @ geodesic[:48]**2))
                derivative_shift = proper-physical[0]['proper_acceleration']
                weighted_shift = float(np.sqrt(weight @ derivative_shift[:48]**2))
                report['physical_summaries'].append(dict(branch=branch,extension=extension,label=label,
                    center_proper_acceleration=float(proper[-1]),center_geodesic_acceleration=float(geodesic[-1]),
                    center_newton_proxy=float(physical[-1]['newton_proxy'][-1]),
                    center_geodesic_relative_difference=float((proper[-1]-geodesic[-1])/abs(geodesic[-1])),
                    weighted_geodesic_residual=rms,weighted_relative_geodesic_residual=rms/max(scale,1e-30),
                    maximum_geodesic_residual=float(np.max(abs(proper-geodesic))),
                    center_derivative_shift=float(abs(derivative_shift[-1])),weighted_derivative_shift=weighted_shift,
                    residual_to_observed_derivative_shift=rms/max(weighted_shift,1e-30),
                    derivative_shift_is_not_error_bound=True,
                    clock_omission_shift=float(np.max(abs(result['omit_clock_response']-proper))),
                    metric_time_omission_shift=float(np.max(abs(result['omit_metric_time']-geodesic))),
                    derivative_qualified=all(row['passed'] for row in run['derivative_checks'] if all(row[key] == case[key]
                        for key in ['branch','extension','label'])),valid_for_claim=False))
                report['independent_cases'].append(dict(branch=branch,extension=extension,label=label,
                    reconstructed_components=16425,reconstructed_source_samples=64,valid_for_claim=False))
                save()
        for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            main_case = next(row for row in runs[0][1]['cases'] if row['branch'] == branch
                and row['extension'] == extension and row['label'] == 'endpoint')
            wide_case = next(row for row in runs[1][1]['cases'] if row['branch'] == branch and row['extension'] == extension)
            main_base,wide_base = [loaded(root/row['path']) for row in [main_case,wide_case]]
            check(branch+'-'+extension+'_scale_control_same_phase_point',all(np.array_equal(main_base[key],wide_base[key])
                for key in ['coordinates','momenta','rates','force_decimal']))
            first = loaded((root/main_case['path']).parent/(branch+'-'+extension+'-endpoint-acceleration.npz'))
            second = loaded((root/wide_case['path']).parent/(branch+'-'+extension+'-endpoint-wide-acceleration.npz'))
            shift = second['proper_acceleration']-first['proper_acceleration']
            maximum = float(np.max(abs(shift)))
            signal = max(float(np.max(abs(second['proper_acceleration']))),1e-30)
            report['probe_scale_comparisons'].append(dict(branch=branch,extension=extension,
                maximum_proper_acceleration_change=maximum,relative_change=maximum/signal,
                weighted_change=float(np.sqrt(main_base['weights'] @ shift[:48]**2)),
                center_change=float(shift[-1]),tolerance=1e-8+2e-3*signal,
                passed=bool(maximum < 1e-8+2e-3*signal),valid_for_claim=False))
        branch_contrasts = {}
        for label in ['initial','endpoint','endpoint-wide']:
            source_path,run = runs[1] if label == 'endpoint-wide' else runs[0]
            reference = loaded(source_path.parent/('reference-reference-'+label+'-acceleration.npz'))
            reference_base = loaded(source_path.parent/('reference-reference-'+label+'-base.npz'))
            for extension in ['primary','alternative']:
                candidate = loaded(source_path.parent/('MTS-'+extension+'-'+label+'-acceleration.npz'))
                candidate_base = loaded(source_path.parent/('MTS-'+extension+'-'+label+'-base.npz'))
                check(label+'-'+extension+'_paired_material_samples_match',np.array_equal(reference_base['labels'],candidate_base['labels'])
                    and np.array_equal(reference_base['weights'],candidate_base['weights']))
                contrast = candidate['proper_acceleration']-reference['proper_acceleration']
                branch_contrasts[label,extension] = contrast
                report['paired_branch_contrasts'].append(dict(extension=extension,label=label,
                    center_contrast=float(contrast[-1]),weighted_contrast=float(np.sqrt(reference_base['weights'] @ contrast[:48]**2)),
                    maximum_contrast=float(np.max(abs(contrast))),same_material_label_and_model_time=True,
                    branch_specific_geometry_retained=True,spatial_error_bound=False,valid_for_claim=False))
        for extension in ['primary','alternative']:
            first,second = branch_contrasts['endpoint',extension],branch_contrasts['endpoint-wide',extension]
            report['paired_contrast_sensitivity'].append(dict(extension=extension,
                center_contrast_change=float(second[-1]-first[-1]),maximum_contrast_change=float(np.max(abs(second-first))),
                differential_numerical_control_not_physical_significance=True,valid_for_claim=False))
        check('original_endpoint_raw_reaction_failures_retained',
            all(not row['original_raw_closure_passed'] for row in report['dust_reaction_summaries'] if row['label'] == 'endpoint'))
        check('wider_endpoint_raw_reaction_closes_unchanged_tolerance',
            all(row['original_raw_closure_passed'] for row in report['dust_reaction_summaries'] if row['label'] == 'endpoint-wide'))
        for mass,radius,mu,velocity in [(1.,6.,.8,.03),(.003,6.,.8,-.03),(1.,3.1,1.,.1),(1.,6.,.8,0.)]:
            metric = 1-2*mu/radius
            clock = np.sqrt(metric-velocity**2/metric)
            momentum = mass*velocity/(metric*clock)
            force = -mass*mu/radius**2*(1+velocity**2/metric**2)/clock
            derivatives = []
            for step in [1e-4,5e-5,2.5e-5]:
                samples = []
                for sign in [1,-1]:
                    displaced = radius+sign*step*velocity
                    target = momentum+sign*step*force
                    changed_metric = 1-2*mu/displaced
                    rate = changed_metric**1.5*target/np.sqrt(mass**2+target**2*changed_metric)
                    local_clock = np.sqrt(changed_metric-rate**2/changed_metric)
                    samples.append(rate/local_clock)
                derivatives.append((samples[0]-samples[1])/(2*step*clock))
            measured = (4*derivatives[2]-derivatives[1])/3
            expected = -mu/radius**2
            check('closed_form_test_source_inverse_'+str(len(report['analytic_controls'])),abs(measured-expected) < 1e-8)
            report['analytic_controls'].append(dict(mass=mass,radius=radius,mu=mu,velocity=velocity,
                computed=measured,expected=expected,absolute_error=abs(measured-expected),valid_for_claim=False))
        for source_path,run in runs:
            check(source_path.parent.name+'_qualification_matches_scientific_rows',run['physical_acceleration_qualified'] ==
                all(row['passed'] for key in ['derivative_checks','tangent_checks'] for row in run[key]))
        merged = {key:[dict(row,run_source=str(source_path.relative_to(root)))
            for source_path,run in runs for row in run[key]]
            for key in ['cases','probes','iterations','derivative_checks','tangent_checks','samples']}
        report['table_rows'] = {key:table(key,rows,destination) for key,rows in merged.items()}
        report['table_rows'].update({key:table(key,report[key],destination) for key in
            ['independent_cases','independent_probes','physical_summaries','analytic_controls','tangent_block_diagnostics',
            'probe_scale_comparisons','dust_reaction_summaries','dust_reaction_components','traction_summaries',
            'paired_branch_contrasts','paired_contrast_sensitivity']})
        results_path = intake/(prefix+'-computed-results.md')
        if results_path.exists():
            raise FileExistsError(str(results_path))
        lines = ['# Computed source-acceleration comparisons','',
            'All values retain the candidate normalization. These are not assigned SI accelerations.',
            'The same phase points and action are retained in the wider-probe repeat. Both estimates remain visible.','',
            '| Branch | Phase / probes | Center proper acceleration | Center geodesic comparator | Weighted relative residual |',
            '| --- | --- | ---: | ---: | ---: |']
        for row in report['physical_summaries']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['center_proper_acceleration']:.12g} | "
                f"{row['center_geodesic_acceleration']:.12g} | {row['weighted_relative_geodesic_residual']:.6g} |")
        lines.extend(['','## Derivative sensitivity','',
            '| Branch | Phase / probes | Weighted geodesic residual | Weighted derivative-estimate change |',
            '| --- | --- | ---: | ---: |'])
        for row in report['physical_summaries']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['weighted_geodesic_residual']:.6g} | "
                f"{row['weighted_derivative_shift']:.6g} |")
        lines.extend(['','Derivative-estimate changes are observed numerical diagnostics, not rigorous error bounds.',
            'A numerical residual is not by itself a physical deviation from GR.','',
            '## Source reaction and moving-anchor traction','',
            'Norms below are for the same15-component material covector basis, not invariant physical-force norms.',
            'The bulk traction comparison leaves Gram and finite-element field-equation terms unseparated.','',
            '| Branch | Phase / probes | Non-dust reaction / dust-force norm | Reaction minus bulk traction / dust-force norm | Remainder / raw reaction |',
            '| --- | --- | ---: | ---: | ---: |'])
        for reaction,traction in zip(report['dust_reaction_summaries'],report['traction_summaries']):
            lines.append(f"| {reaction['extension']} | {reaction['label']} | {reaction['reaction_to_dust_force']:.6g} | "
                f"{traction['discrepancy_relative_to_dust_force']:.6g} | {traction['discrepancy_relative_to_raw_reaction']:.6g} |")
        lines.extend(['','## Inverse-root differentiation audit','',
            'The first postflight failed the original raw2e-6 dust-force-normalized closure gate at the reference endpoint.',
            'That failure and the same raw gate are preserved for every branch. The discrepancy is reconstructed from',
            'the derivative of computed minus target canonical momentum, not removed by loosening a threshold.',
            'Root-corrected and target-owned reactions are accounting identities, not independent evidence of physical agreement.',
            'The wider-probe raw comparison passes the original gate for all three endpoint branches.','',
            '| Branch | Phase / probes | Raw closure / dust force | Root derivative / dust force | Original raw gate |',
            '| --- | --- | ---: | ---: | --- |'])
        for row in report['dust_reaction_summaries']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['full_action_closure_relative_error']:.6g} | "
                f"{row['root_derivative_relative_to_dust_force']:.6g} | {row['original_raw_closure_passed']} |")
        lines.extend(['','Source: the final integrity manifest and its source-linked CSV tables. The parent derivation states assumptions and equations.',''])
        results_path.write_text('\n'.join(lines),encoding='utf-8')
        own(results_path,'outputs')
        note = root/'DERIVATION-20260921-physical-source-acceleration.md'
        content = note.read_text(encoding='utf-8')
        citations = re.findall(r'`([^`\r\n]+\.(?:md|py|json|csv|npz))`',content)
        check('report_complete_and_local_sources_exist','RESULTS_PENDING' not in content and bool(citations)
            and all((root/name).is_file() for name in citations))
        for name in citations:
            if (root/name).resolve() != destination.resolve():
                own(root/name)
        own(note)
        for name in ['annular_candidate_source_acceleration_20260921.py','run_annular_candidate_source_acceleration_20260921.py',
            'run_annular_candidate_source_acceleration_wide_probes_20260921.py',
            'seal_annular_candidate_source_acceleration_20260921.py','seal_annular_candidate_source_acceleration_v2_20260921.py',
            'seal_annular_candidate_source_acceleration_v3_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('scripts_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,21,14,47,7,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged',not changed,changed)
        snapshot = intake/(prefix+'-resume-snapshot.md')
        executed = intake/(prefix+'-executed-sealer.py')
        if snapshot.exists() or executed.exists():
            raise FileExistsError('Immutable snapshots already exist.')
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),
            physical_acceleration_qualified=all(run['physical_acceleration_qualified'] for source_path,run in runs)
                and all(row['passed'] for row in report['probe_scale_comparisons']),geodesic_match_claimed=False,
            distinct_files_rehashed=len(hashes),total_failed_attempts_preserved=prior['total_failed_attempts_preserved']+2,
            all_raw_reaction_gates_passed=all(row['original_raw_closure_passed'] for row in report['dust_reaction_summaries']),
            wider_endpoint_raw_reaction_qualified=all(row['original_raw_closure_passed'] for row in report['dust_reaction_summaries'] if row['label'] == 'endpoint-wide'),
            implementation_checks={source_path.parent.name:len(run['checks']) for source_path,run in runs},next_target='Derive the full non-dust reaction balance: account for the moving zero-field anchor traction, the Galerkin field-equation remainder and Gram source terms, then test radial mass-current consistency with the same action.')
        save()
        print(json.dumps({key:report[key] for key in ['state','physical_acceleration_qualified','distinct_files_rehashed','table_rows']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()



