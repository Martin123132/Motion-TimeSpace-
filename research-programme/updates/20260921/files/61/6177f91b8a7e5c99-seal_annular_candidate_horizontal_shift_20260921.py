from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime,timezone
from math import fsum
import csv
import hashlib
import json
import traceback
import numpy as np


def symbolic_checks(check):
    import sympy as sp
    coefficient,radial,displacement,jacobian,jacobian_b,velocity,load,load_rate = sp.symbols('C Cr d J Jb V load load_t',nonzero=True)
    atom = -load/jacobian
    atom_rate = -load_rate/jacobian+load*jacobian_b*velocity/jacobian**2
    gamma_b = radial*displacement/jacobian-coefficient*jacobian_b/jacobian**2
    raw = coefficient*atom_rate+radial*atom*displacement*velocity
    derived = -coefficient*load_rate/jacobian-velocity*gamma_b*load
    check('exact_moving_Gram_delta_prime_bulk_identity',sp.simplify(raw-derived)==0)
    check('exact_local_moving_atom_advection_sign',sp.simplify(-coefficient*atom*displacement*velocity
        -(coefficient*load/jacobian)*displacement*velocity)==0)
    energy_left,energy_right,speed = sp.symbols('eL eR W')
    check('exact_moving_face_coefficient_work',sp.expand(coefficient*speed*(-energy_left/coefficient+energy_right/coefficient)
        -speed*(energy_right-energy_left))==0)
    energy_rate,exchange,projection,cut_work = sp.symbols('Hdot Q P Ccut')
    horizontal,legendre = exchange-energy_rate-cut_work,exchange-energy_rate-projection
    check('exact_horizontal_Legendre_projection_relation',sp.expand(horizontal-legendre-projection+cut_work)==0)
    old_current,ward,conversion = sp.symbols('Jold Ward a')
    old_residual = -conversion*ward
    new_current = old_current+ward-cut_work
    check('exact_conditional_mass_constraint_residual',sp.expand(old_residual+conversion*(new_current-old_current)+conversion*cut_work)==0)
    connection,lapse,metric = sp.symbols('c N F',positive=True)
    shift = 2*connection*lapse**2*metric/(1+sp.sqrt(1+4*connection**2*lapse**2*metric))
    check('exact_finite_connection_to_shift_root',sp.simplify(connection*shift**2+shift-connection*lapse**2*metric)==0)
    mass,source_velocity,shift_variable = sp.symbols('m V beta',positive=True)
    dust = -mass*sp.sqrt(lapse**2-(source_velocity+shift_variable)**2/metric)
    clock = sp.sqrt(lapse**2-source_velocity**2/metric)
    check('exact_dust_shift_energy_current',sp.simplify(lapse**2*metric*sp.diff(dust,shift_variable).subs(shift_variable,0)
        -mass*lapse**2*source_velocity/clock)==0)
    time,radius,angle,azimuth = sp.symbols('t r theta phi',real=True)
    lapse_field,metric_field = sp.Function('N')(time,radius),sp.Function('F')(time,radius)
    density,pressure,angular_pressure = [sp.Function(name)(time,radius) for name in ['rho','p','pt']]
    mixed = sp.Function('K')(time,radius)
    coordinates = [time,radius,angle,azimuth]
    geometry = sp.diag(-lapse_field**2,1/metric_field,radius**2,radius**2*sp.sin(angle)**2)
    inverse = geometry.inv()
    connection_tensor = [[[sp.simplify(sum(inverse[upper,index]*(sp.diff(geometry[index,last],coordinates[first])
        +sp.diff(geometry[index,first],coordinates[last])-sp.diff(geometry[first,last],coordinates[index]))/2
        for index in range(4))) for last in range(4)] for first in range(4)] for upper in range(4)]
    stress = sp.diag(-density,pressure,angular_pressure,angular_pressure)
    stress[0,1],stress[1,0] = mixed,-lapse_field**2*metric_field*mixed
    def radial_divergence(tensor):
        return sum(sp.diff(tensor[first,1],coordinates[first])+sum(connection_tensor[first][first][last]*tensor[last,1]
            -connection_tensor[last][first][1]*tensor[first,last] for last in range(4)) for first in range(4))
    expected = sp.diff(mixed,time)+(sp.diff(lapse_field,time)/lapse_field-sp.diff(metric_field,time)/(2*metric_field))*mixed
    expected += sp.diff(pressure,radius)+(density+pressure)*sp.diff(lapse_field,radius)/lapse_field+2*(pressure-angular_pressure)/radius
    check('derived_radial_stress_divergence_next_equation',sp.simplify(radial_divergence(stress)-expected)==0)
    angular_residual = sp.Function('A')(time,radius)
    check('derived_angular_Einstein_residual_bridge',sp.simplify(radial_divergence(sp.diag(0,0,angular_residual,angular_residual))
        +2*angular_residual/radius)==0)
    step,parameter = sp.symbols('h epsilon',nonzero=True)
    coefficients = sp.symbols('s0:6')
    series = sum(value*parameter**index for index,value in enumerate(coefficients))
    centered = (series.subs(parameter,step)-series.subs(parameter,-step))/(2*step)
    richardson = (4*centered.subs(step,step/2)-centered)/3
    check('derived_Richardson_fifth_coefficient_error',sp.expand(richardson-coefficients[1]+coefficients[5]*step**4/4)==0)


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-horizontal-shift'
    destination = intake/(prefix+'-final-integrity.json')
    if destination.exists():
        raise FileExistsError(str(destination))
    report = dict(state='running',inputs={},outputs={},checks=[],comparisons=[],controls=[],
        github_action=False,subagents_used=False,valid_for_physics_claim=False,
        protected_scan_scope='mtime since2026-09-21T20:51:04Z, not a whole-tree before/after hash')
    hashes = {}
    def digest(path):
        path = path.resolve()
        if path not in hashes:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk:=stream.read(1024*1024):
                    hasher.update(chunk)
            hashes[path] = hasher.hexdigest()
        return hashes[path]
    def own(path,category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)
    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        if not passed or len(report['checks'])%25==0:
            save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))
    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs','outputs']:
            for name,expected in data[category].items():
                source = root/name
                if not source.is_file() or digest(source)!=expected:
                    raise RuntimeError('Changed immutable evidence: '+name)
                report['inputs'][str(source.relative_to(root))] = expected
        own(path)
        return data
    def loaded(path):
        own(path)
        with np.load(path,allow_pickle=False) as archive:
            return {key:archive[key].copy() for key in archive.files}
    def maximum(value):
        return float(np.max(abs(value)))
    def close(first,second,absolute=5e-18,relative=2e-10):
        first,second = np.asarray(first),np.asarray(second)
        return bool(np.all(np.isfinite(first)) and np.all(np.isfinite(second))
            and maximum(first-second)<=absolute+relative*max(maximum(second),1e-30))
    def table(name,rows):
        path = intake/(prefix+'-'+name+'.csv')
        if path.exists():
            raise FileExistsError(str(path))
        rows = [dict(row,record_source=str(destination.relative_to(root))) for row in rows]
        with path.open('w',newline='',encoding='utf-8') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(dict.fromkeys(key for row in rows for key in row)))
            writer.writeheader()
            writer.writerows(rows)
        with path.open(newline='',encoding='utf-8') as stream:
            parsed = list(csv.DictReader(stream))
        check(name+'_CSV_clean',len(parsed)==len(rows) and all(None not in row and None not in row.values()
            and row['valid_for_claim']=='False' and (root/row['record_source']).is_file() for row in parsed))
        own(path,'outputs')
        return len(rows)
    save()
    try:
        prior = inherit(intake/'annular-moving-Legendre-current-final-integrity.json')
        run = inherit(intake/'annular-candidate-horizontal-shift-attempt01/status.json')
        scan = inherit(intake/'annular-horizontal-shift-step-scan-attempt01/status.json')
        check('complete_input_evidence',prior['state']=='complete' and run['state']=='complete' and scan['state']=='complete')
        failures = [row for row in run['scientific_checks'] if not row['passed']]
        check('all_original_coarse_failures_preserved',scan['original_coarse_failures_preserved']==failures)
        symbolic_checks(check)
        for case in scan['cases']:
            raw = loaded(root/case['source_path'])
            centered = (raw['values'][:,1]-raw['values'][:,0])/(2*raw['steps'][:,None])
            estimates = (4*centered[1:]-centered[:-1])/3
            errors = abs(estimates-raw['raw'])
            check(case['source_path']+'_refinement_recomputed',close(estimates,raw['finite']) and close(errors,raw['error']))
            for index,sector in enumerate(['wave','Gram','dust']):
                rows = [row for row in scan['step_rows'] if row['extension']==case['extension'] and row['label']==case['label'] and row['sector']==sector]
                for level,row in enumerate(rows):
                    tolerance = (2e-18 if sector=='Gram' else 2e-12)+2e-7*abs(raw['raw'][index])
                    check(case['extension']+str(case['label'])+sector+str(level)+'_refinement_gate',
                        close(row['error'],errors[level,index]) and row['passed']==(errors[level,index]<=tolerance))
            if case['branch']=='MTS':
                ratios = errors[:2,1]/errors[1:3,1]
                records = [row for row in scan['scientific_checks'] if row['case']=='MTS-'+case['extension']+'-label'+str(case['label'])
                    and row['quantity'].startswith('Gram_fourth_order_ratio')]
                check(case['extension']+str(case['label'])+'_observed_order_recomputed',len(records)==2
                    and all(close(record['value'],ratio) and record['passed']==(8<ratio<32) for record,ratio in zip(records,ratios)))
        for spot in run['shift_spots']:
            path = root/spot['source_path']
            raw = loaded(path)
            check(path.name+'_zero_shift_same_action',maximum(raw['zero']-raw['baseline'])<2e-13)
            centered = (raw['values'][:,1]-raw['values'][:,0])/(2*raw['steps'][:,None])
            derivative = (4*centered[1]-centered[0])/3
            check(path.name+'_finite_derivative_independent_reconstruction',close(derivative,raw['finite']))
            for index,sector in enumerate(['wave','Gram','dust']):
                error = abs(derivative[index]-raw['raw'][index])
                tolerance = (2e-18 if sector=='Gram' else 2e-12)+2e-7*abs(raw['raw'][index])
                gate = next(row for row in run['scientific_checks'] if row['case']==path.name and row['quantity']==sector+'_finite_shift_derivative')
                check(path.name+'_'+sector+'_gate',close(error,gate['error']) and gate['passed']==(error<=tolerance))
            altered = abs(derivative[0]-(raw['raw'][0]-raw['omitted_moving_clock']))
            tolerance = 2e-12+2e-7*abs(raw['raw'][0])
            report['controls'].append(dict(branch=spot['branch'],extension=spot['extension'],label=spot['label'],profile=spot['profile'],
                control='omit_moving_node_clock_in_raw_shift',error=float(altered),tolerance=float(tolerance),
                rejected=bool(altered>tolerance),valid_for_claim=False))
        by_branch = {}
        for summary in run['summaries']:
            branch,extension,order = summary['branch'],summary['extension'],summary['order']
            name = branch+'-'+extension
            case = name+'-order'+str(order)
            raw = loaded(root/summary['source_path'])
            previous = loaded(intake/'annular-moving-Legendre-current-attempt01'/(case+'-localized.npz'))
            summed = {}
            for key in ['horizontal_without_local_atom','regular','edges','atoms','field_Euler_work',
                'source_wave_work','source_dust_work','localized_Euler_work','whole_layer_Noether','source','velocity']:
                values = raw['label_'+key]
                flat = values.reshape(len(raw['weights']),-1)
                result = np.array([fsum(raw['weights']*column) for column in flat.T]).reshape(values.shape[1:])
                check(case+'_'+key+'_independent_sum',close(result,raw['sum_'+key]))
                summed[key] = result
            source_mask = raw['label_source'][:,None]<raw['targets']
            local_work = raw['label_field_Euler_work']+(raw['label_source_wave_work']+raw['label_source_dust_work'])[:,:,None]*source_mask[:,None,:]
            check(case+'_per_layer_cut_residual_not_assumed_zero',close(local_work,raw['label_localized_Euler_work']))
            primitive = raw['label_regular']+raw['label_edges'][:,None,:]+raw['label_atoms'][:,None,:]-raw['label_field_Euler_work']
            anchored = primitive-primitive[:,:,-1,None]*source_mask[:,None,:]
            check(case+'_direct_source_anchored_current',close(anchored,raw['label_horizontal_without_local_atom']))
            current = summed['horizontal_without_local_atom']+raw['gram_advection']
            expected = previous['exchange'][[0,1,0,1]]-previous['frozen'][[0,1,0,1]]-previous['inertia']-summed['localized_Euler_work']
            check(case+'_direct_current_reconstructed',close(current,raw['current']) and close(expected,raw['expected']))
            gap = np.concatenate([-summed['localized_Euler_work'][:2],previous['projection']-summed['localized_Euler_work'][2:]])
            difference = current-previous['current'][[0,1,0,1]]
            check(case+'_derived_gap_reconstructed',close(gap,raw['predicted_gap']) and close(difference,raw['difference']))
            checks = {'independent_shift_Legendre_projection_identity':maximum(current-expected),
                'whole_layer_Noether_identity':maximum(raw['label_whole_layer_Noether']),
                'archived_horizontal_equals_Legendre':maximum(difference[2:]),
                'action_horizontal_equals_Legendre':maximum(difference[:2])}
            for quantity,error in checks.items():
                gate = next(row for row in run['scientific_checks'] if row['case']==case and row['quantity']==quantity)
                check(case+'_'+quantity+'_gate_recomputed',close(error,gate['error']) and gate['passed']==(error<=2e-11))
            for index,radius in enumerate(raw['targets'][1:-1]):
                report['comparisons'].append(dict(branch=branch,extension=extension,order=order,radius=float(radius),
                    horizontal_archived=float(current[3,index+1]),horizontal_action=float(current[1,index+1]),
                    Legendre=float(previous['current'][1,index+1]),gap_archived=float(difference[3,index+1]),
                    gap_action=float(difference[1,index+1]),predicted_gap_archived=float(gap[3,index+1]),
                    C_R_archived=float(summed['localized_Euler_work'][3,index+1]),
                    C_R_action=float(summed['localized_Euler_work'][1,index+1]),
                    mass_residual_horizontal=float(raw['mass_residual'][index]),
                    mass_residual_Legendre=float(raw['legendre_mass_residual'][index]),valid_for_claim=False))
            for label,component in [('omit_all_moving_faces',summed['edges']),('omit_Gram_atom_bulk',summed['atoms'])]:
                mask_by_label = source_mask
                field = raw['label_edges'] if label=='omit_all_moving_faces' else raw['label_atoms']
                correction = field-field[:,-1,None]*mask_by_label
                averaged = np.tensordot(raw['weights'],correction,axes=(0,0))
                error = maximum(current-averaged-expected)
                report['controls'].append(dict(branch=branch,extension=extension,order=order,control=label,
                    error=error,tolerance=2e-11,rejected=bool(error>2e-11),valid_for_claim=False))
            report['controls'].append(dict(branch=branch,extension=extension,order=order,control='omit_local_Gram_advection',
                error=maximum(current-raw['gram_advection']-expected),tolerance=2e-11,
                rejected=bool(maximum(current-raw['gram_advection']-expected)>2e-11),valid_for_claim=False))
            by_branch.setdefault(name,{})[order] = current
        for name,orders in by_branch.items():
            error = maximum(orders[12]-orders[8])
            gate = next(row for row in run['scientific_checks'] if row['case']==name and row['quantity']=='paired_quadrature_8_12')
            check(name+'_paired_quadrature_recomputed',close(error,gate['error']) and gate['passed']==(error<=2e-11))
        report.update(summaries=run['summaries'],shift_spots=run['shift_spots'],scientific_checks=run['scientific_checks'],
            refined_steps=scan['step_rows'],refinement_checks=scan['scientific_checks'],original_coarse_failures=failures)
        report['table_rows'] = {name:table(name,report[name]) for name in ['summaries','comparisons','shift_spots','controls',
            'scientific_checks','refined_steps','refinement_checks']}
        for filename in ['annular_candidate_horizontal_shift_20260921.py','run_annular_candidate_horizontal_shift_20260921.py',
            'seal_annular_candidate_horizontal_shift_20260921.py','annular_horizontal_shift_step_scan_20260921.py',
            'run_annular_horizontal_shift_step_scan_20260921.py']:
            path = root/'scripts'/filename
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        own(root/'DERIVATION-20260921-candidate-horizontal-shift-and-localized-current.md')
        own(root/'RESULTS-20260921-candidate-horizontal-shift-and-localized-current.md')
        own(root/'DERIVATION-20260921-horizontal-shift-step-size-refinement.md')
        check('no_bytecode_cache',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        since = datetime(2026,9,21,20,51,4,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
        check('protected_workbench_mtime_unchanged',not changed,changed)
        for filename,source in [(prefix+'-resume-snapshot.md',root/'CURRENT_LOCAL_RESUME.md'),(prefix+'-executed-sealer.py',Path(__file__))]:
            path = intake/filename
            if path.exists():
                raise FileExistsError(str(path))
            path.write_bytes(source.read_bytes())
            own(path,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),distinct_files_rehashed=len(hashes),
            comparisons_passed=all(row['passed'] for row in run['scientific_checks']),implementation_checks=len(run['checks']),
            current_comparisons_passed=all(row['passed'] for row in run['scientific_checks'] if not row['quantity'].endswith('finite_shift_derivative')),
            refined_derivatives_passed=scan['refined_passed'],
            total_failed_attempts_preserved=prior['total_failed_attempts_preserved'],
            next_target='Derive radial/areal-radius stress variation and test the radial Ward equation, including source-region terms; its residual controls the remaining angular Einstein equation when the other Einstein components hold. Do not define angular pressure by demanding the result.')
        save()
        print(json.dumps({key:report[key] for key in ['state','distinct_files_rehashed','comparisons_passed','table_rows']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
