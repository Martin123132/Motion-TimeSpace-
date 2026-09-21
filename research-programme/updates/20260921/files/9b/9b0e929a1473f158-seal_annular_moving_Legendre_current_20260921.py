from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
from scipy.sparse import load_npz
from math import fsum
import csv
import hashlib
import json
import traceback
import numpy as np


def exact_controls(check):
    import sympy as sp
    field, source, time, field_rate, source_rate = sp.symbols('u b t v V',real=True)
    coordinates, rates = sp.Matrix([field,source]), sp.Matrix([field_rate,source_rate])
    lapse = 1+time
    clock = sp.sqrt(lapse**2-source_rate**2)
    wave = (1+source**2)*(field_rate-field*source_rate)**2/2-field**2/(2*(1+source**2))
    dust = -2*clock
    lagrangian = wave+dust
    local = (1+source+time)*wave/4+(2+field)*dust/5
    def parts(expression):
        momentum = sp.Matrix([sp.diff(expression,value) for value in rates])
        hessian = momentum.jacobian(rates)
        force = sp.Matrix([sp.diff(expression,value) for value in coordinates])
        convection = momentum.jacobian(coordinates)*rates+sp.diff(momentum,time)
        energy = (rates.T*momentum)[0]-expression
        return momentum,hessian,force-convection,energy
    unused,matrix,forcing,unused_energy = parts(lagrangian)
    unused,local_matrix,local_forcing,energy = parts(local)
    energy_q = sp.Matrix([sp.diff(energy,value) for value in coordinates])
    energy_v = sp.Matrix([sp.diff(energy,value) for value in rates])
    for index,velocity in enumerate([sp.Rational(0),sp.Rational(3,5),sp.Rational(4,5)]):
        point = {field:sp.Rational(1,3),source:sp.Rational(1,4),time:0,
            field_rate:sp.Rational(2,7),source_rate:velocity}
        hessian,partial = matrix.subs(point),local_matrix.subs(point)
        full_force,partial_force,rate = forcing.subs(point),local_forcing.subs(point),rates.subs(point)
        acceleration = sp.Matrix([sp.Rational(2,9),sp.Rational(-3,8)])
        solution = hessian.inv()*full_force
        euler = full_force-hessian*acceleration
        current = (rate.T*(partial_force-partial*solution))[0]
        derivative = (energy_q.subs(point).T*rate+energy_v.subs(point).T*acceleration)[0]+sp.diff(energy,time).subs(point)
        exchange = -sp.diff(local,time).subs(point)
        residual = sp.simplify(derivative+current-exchange+(rate.T*partial*hessian.inv()*euler)[0])
        check('exact_nonquadratic_coordinate_cut_identity_'+str(index),residual==0)
        check('exact_whole_domain_current_'+str(index),sp.simplify((rate.T*(full_force-hessian*solution))[0])==0)
        check('exact_velocity_energy_gradient_'+str(index),energy_v.subs(point)==partial*rate)
        if velocity:
            check('nonrelativistic_clock_inertia_is_detectably_different_'+str(index),
                sp.diff(dust,source_rate,2).subs(point)!=2)
    count = 2
    full = sp.Matrix([[3,1],[1,2]])
    partial = sp.Matrix([[1,sp.Rational(1,4)],[sp.Rational(1,4),sp.Rational(1,2)]])
    stiffness,partial_stiffness = sp.Matrix([[4,-1],[-1,5]]),sp.Matrix([[2,0],[0,1]])
    mass_time,partial_time = sp.Matrix([[1,0],[0,2]]),sp.Matrix([[0,1],[1,0]])
    coordinate,rate = sp.Matrix([2,3]),sp.Matrix([5,7])
    forcing = -stiffness*coordinate-mass_time*rate
    local_forcing = -partial_stiffness*coordinate-partial_time*rate
    general = (rate.T*(local_forcing-partial*full.inv()*forcing))[0]
    earlier = (rate.T*(partial*full.inv()*stiffness-partial_stiffness)*coordinate
        +rate.T*(partial*full.inv()*mass_time-partial_time)*rate)[0]
    check('exact_reduction_to_previous_quadratic_lemma',general==earlier and count==2)


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-moving-Legendre-current'
    destination = intake/(prefix+'-final-integrity.json')
    if destination.exists():
        raise FileExistsError(str(destination))
    report = dict(state='running',inputs={},outputs={},checks=[],comparisons=[],ablations=[],dual_norm_bounds=[],
        scientific_checks=[],github_action=False,subagents_used=False,valid_for_physics_claim=False,
        protected_scan_scope='mtime since2026-09-21T19:15:16Z, not a pre-turn whole-tree hash')
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
    def maximum(values):
        return float(np.max(abs(values)))
    def close(first,second,absolute=3e-18,relative=3e-10):
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
        prior = inherit(intake/'annular-candidate-Ward-source-v2-final-integrity.json')
        run = inherit(intake/'annular-moving-Legendre-current-attempt01/status.json')
        check('complete_immutable_inputs',prior['state']=='complete' and run['state']=='complete')
        exact_controls(check)
        by_branch = {}
        for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            name = branch+'-'+extension
            system_path = intake/'annular-moving-Legendre-current-attempt01'/(name+'-system.npz')
            system = loaded(system_path)
            matrix_path = intake/'annular-moving-Legendre-current-attempt01'/(name+'-Hessian.npz')
            own(matrix_path)
            matrix = load_npz(matrix_path)
            check(name+'_all_16425_components',matrix.shape==(16425,16425) and system['force'].size==16425)
            difference = matrix-matrix.T
            check(name+'_Hessian_symmetry',max(abs(difference.data),default=0)<2e-12*max(abs(matrix.data)))
            check(name+'_forcing_from_action_and_convection',close(system['forcing'],system['force'][None]-system['convection']))
            analytic = (matrix @ system['acceleration'].reshape(2,-1).T).T.reshape(system['forcing'].shape)
            check(name+'_inverse_independent_sparse_residual',close(analytic,system['forcing'],absolute=3e-16,relative=2e-10))
            archived = (matrix @ system['archived_acceleration'].reshape(2,-1).T).T.reshape(system['forcing'].shape)
            check(name+'_Euler_residual_kept',close(system['euler'],system['forcing']-archived))
            rate = system['rates'].ravel()
            rate_norm_square = float(rate @ (matrix @ rate))
            acceleration_error = (system['acceleration']-system['archived_acceleration']).reshape(2,-1)
            dual_norm_square = np.array([float(values @ (matrix @ values)) for values in acceleration_error])
            check(name+'_positive_dual_error_norm',rate_norm_square>=0 and np.all(dual_norm_square>=0))
            global_bound = np.sqrt(rate_norm_square*dual_norm_square)
            chain_error = maximum(system['convection']+archived-system['archived_momentum_tangent'])
            record = next(row for row in run['scientific_checks'] if row['case']==name and row['quantity']=='archived_momentum_chain_rule')
            check(name+'_momentum_chain_gate_recomputed',close(chain_error,record['error']) and record['passed']==(chain_error<=record['tolerance']))
            ward = loaded(intake/'annular-candidate-Ward-source-attempt01'/(name+'-order12-Ward.npz'))
            for order in [8,12]:
                case = name+'-order'+str(order)
                path = intake/'annular-moving-Legendre-current-attempt01'/(case+'-localized.npz')
                raw = loaded(path)
                check(case+'_positive_material_measure',min(raw['weights'])>0 and abs(fsum(raw['weights'])-1)<1e-12)
                summed = {}
                for key in ['energy','frozen_wave','frozen_dust','frozen_gram','exchange_wave','exchange_dust',
                    'exchange_gram','wave_advection','inertia_wave','inertia_dust']:
                    values = raw['label_'+key]
                    flat = values.reshape(len(raw['weights']),-1)
                    result = np.array([fsum(raw['weights']*column) for column in flat.T]).reshape(values.shape[1:])
                    check(case+'_'+key+'_independent_sum',close(result,raw['sum_'+key]))
                    summed[key] = result
                exchange = summed['exchange_wave']+summed['exchange_dust']+summed['exchange_gram']
                frozen = summed['frozen_wave']+summed['frozen_dust']+summed['frozen_gram']-summed['wave_advection']-raw['gram_advection']
                inertia = summed['inertia_wave']+summed['inertia_dust']
                current = exchange-frozen-inertia[:2]
                projection = inertia[:2]-inertia[2:]
                check(case+'_derived_current_rebuilt',close(current,raw['current']))
                check(case+'_EL_projection_rebuilt',close(projection,raw['projection']))
                projection_max = np.max(abs(projection),axis=1)
                check(case+'_global_dual_norm_controls_projection',np.all(projection_max<=global_bound+3e-18))
                report['dual_norm_bounds'].append(dict(branch=branch,extension=extension,order=order,
                    projected_error_max=float(projection_max[-1]),global_dual_norm_bound=float(global_bound[-1]),
                    velocity_M_norm=float(np.sqrt(rate_norm_square)),EL_dual_norm=float(np.sqrt(dual_norm_square[-1])),
                    note='Numerical diagnostic using assembled full Hessian; analytic inequality assumes matched positive partial/full integrals.',
                    valid_for_claim=False))
                predicted = current[:,1:-1]-raw['old_energy_current']+projection[:,1:-1]
                check(case+'_Ward_source_not_used_in_current',close(predicted,raw['predicted_ward'])
                    and np.array_equal(raw['ward'],ward['sum_total']))
                error = maximum(predicted-ward['sum_total'])
                tolerance = 2e-11+.05*maximum(ward['sum_total'])
                gate = next(row for row in run['scientific_checks'] if row['case']==case and row['quantity']=='independent_Ward_vs_Legendre')
                check(case+'_scientific_gate_recomputed',close(error,gate['error']) and gate['passed']==(error<=tolerance))
                endpoint = maximum(current[:,[0,-1]])
                gate = next(row for row in run['scientific_checks'] if row['case']==case and row['quantity']=='empty_and_whole_domain_current')
                check(case+'_global_gate_recomputed',close(endpoint,gate['error']) and gate['passed']==(endpoint<=2e-11))
                corrected = raw['old_mass_residual']+raw['conversion']*(current[-1,1:-1]-raw['old_energy_current'])
                projected = raw['old_mass_residual']+raw['conversion']*predicted[-1]
                check(case+'_mass_comparison_recomputed',close(corrected,raw['corrected_mass']) and close(projected,raw['projected_mass']))
                for index,radius in enumerate(raw['targets'][1:-1]):
                    report['comparisons'].append(dict(branch=branch,extension=extension,order=order,radius=float(radius),
                        current_old=float(raw['old_energy_current'][index]),current_new=float(current[-1,index+1]),
                        EL_projection=float(projection[-1,index+1]),Ward_source=float(ward['sum_total'][-1,index]),
                        Ward_difference=float(predicted[-1,index]-ward['sum_total'][-1,index]),
                        mass_residual_old=float(raw['old_mass_residual'][index]),mass_residual_new=float(corrected[index]),
                        with_EL_mass_residual=float(projected[index]),source_path=str(path.relative_to(root)),valid_for_claim=False))
                for label,omission in [('omit_moving_cut',summed['wave_advection']+raw['gram_advection']),
                    ('omit_exact_dust_inertia',-summed['inertia_dust'][:2])]:
                    altered = current-omission
                    alternative_error = maximum(altered[:,1:-1]-raw['old_energy_current']+projection[:,1:-1]-ward['sum_total'])
                    report['ablations'].append(dict(branch=branch,extension=extension,order=order,control=label,
                        full_error=error,altered_error=alternative_error,tolerance=tolerance,
                        altered_rejected=bool(alternative_error>tolerance),valid_for_claim=False))
                by_branch.setdefault(extension,{})[order] = current
        for extension,orders in by_branch.items():
            case = ('reference-' if extension=='reference' else 'MTS-')+extension
            error = maximum(orders[12]-orders[8])
            gate = next(row for row in run['scientific_checks'] if row['case']==case and row['quantity']=='local_quadrature_8_12')
            check(case+'_paired_quadrature_gate_recomputed',close(error,gate['error']) and gate['passed']==(error<=2e-11))
        report.update(summaries=run['summaries'],scientific_checks=run['scientific_checks'])
        report['table_rows'] = {name:table(name,report[name]) for name in ['summaries','comparisons','ablations','scientific_checks','dual_norm_bounds']}
        for filename in ['annular_moving_Legendre_current_20260921.py','run_annular_moving_Legendre_current_20260921.py',
            'seal_annular_moving_Legendre_current_20260921.py']:
            path = root/'scripts'/filename
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        own(root/'DERIVATION-20260921-moving-source-localized-Legendre-current.md')
        own(root/'RESULTS-20260921-moving-source-localized-Legendre-current.md')
        check('no_bytecode_cache',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        since = datetime(2026,9,21,19,15,16,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
        check('protected_workbench_mtime_unchanged',not changed,changed)
        for filename,source in [(prefix+'-resume-snapshot.md',root/'CURRENT_LOCAL_RESUME.md'),
            (prefix+'-executed-sealer.py',Path(__file__))]:
            path = intake/filename
            if path.exists():
                raise FileExistsError(str(path))
            path.write_bytes(source.read_bytes())
            own(path,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),distinct_files_rehashed=len(hashes),
            numerical_comparisons_passed=all(row['passed'] for row in report['scientific_checks']),
            implementation_checks=len(run['checks']),total_failed_attempts_preserved=prior['total_failed_attempts_preserved'],
            next_target='Test localized current against shift variation and the continuum limit; retain explicit Euler projection and independently diagnose any common mass-tangent offset.')
        save()
        print(json.dumps({key:report[key] for key in ['state','distinct_files_rehashed','numerical_comparisons_passed','table_rows']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
