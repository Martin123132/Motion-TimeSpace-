from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from pathlib import Path
from datetime import datetime,timezone
from decimal import localcontext
from fractions import Fraction
import csv
import hashlib
import json
import re
import traceback
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-Ward-source'
    destination = intake/(prefix+'-final-integrity.json')
    if destination.exists():
        raise FileExistsError(str(destination))
    report = dict(state='running',inputs={},outputs={},checks=[],summaries=[],comparisons=[],ablation_controls=[],shape_diagnostics=[],
        source_components=[],scientific_checks=[],github_action=False,subagents_used=False,valid_for_physics_claim=False,
        protected_scan_scope='mtime since2026-09-21T18:25:03Z, not a pre-turn whole-tree hash')
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
                path_input = root/name
                if not path_input.is_file() or digest(path_input)!=expected:
                    raise RuntimeError('Changed immutable evidence: '+name)
                report['inputs'][str(path_input.relative_to(root))] = expected
        own(path)
        return data
    def loaded(path):
        own(path)
        with np.load(path,allow_pickle=False) as archive:
            return {key:archive[key].copy() for key in archive.files}
    def close(first,second,absolute=2e-19,relative=2e-11):
        first,second = np.asarray(first),np.asarray(second)
        return bool(np.all(np.isfinite(first)) and np.all(np.isfinite(second))
            and (not first.size or np.max(abs(first-second))<=absolute+relative*max(float(np.max(abs(second))),1e-30)))
    def derivative(values,steps):
        divisor = 2*np.asarray(steps).reshape((-1,)+(1,)*(values.ndim-2))
        centered = (values[:,1]-values[:,0])/divisor
        return (4*centered[1:]-centered[:-1])/3
    def maximum(values):
        return float(np.max(abs(values)))
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
        check(name+'_CSV_source_and_shape',len(parsed)==len(rows) and all(None not in row and None not in row.values()
            and row['valid_for_claim']=='False' and (root/row['record_source']).is_file() for row in parsed))
        own(path,'outputs')
        return len(rows)
    save()
    try:
        prior = inherit(intake/'annular-candidate-energy-current-final-integrity.json')
        run = inherit(intake/(prefix+'-attempt01/status.json'))
        check('matched_completed_unchanged_action_experiment',prior['state']=='complete' and run['state']=='complete'
            and all(row['passed'] for row in run['checks']) and run['full_components']==16425
            and run['original_action_unchanged'] and not run['new_trajectory'] and len(run['cases'])==6)
        import sympy as sp
        coordinate = sp.Matrix(sp.symbols('u0:2'))
        rate = sp.Matrix(sp.symbols('v0:2'))
        residual = sp.Matrix(sp.symbols('E0:2'))
        mass_matrix = sp.Matrix([[2,sp.Rational(1,2)],[sp.Rational(1,2),3]])
        stiffness = sp.Matrix([[5,-1],[-1,4]])
        def symmetric(prefix):
            diagonal_first,off_diagonal,diagonal_last = sp.symbols(prefix+'0:3')
            return sp.Matrix([[diagonal_first,off_diagonal],[off_diagonal,diagonal_last]])
        cut_mass,cut_stiffness,mass_rate,cut_mass_rate,cut_stiffness_rate = [symmetric(prefix)
            for prefix in ['MR','KR','Mt','MRt','KRt']]
        acceleration = -mass_matrix.inv()*(stiffness*coordinate+mass_rate*rate+residual)
        energy_rate = (rate.T*cut_mass*acceleration+rate.T*cut_stiffness*coordinate
            +rate.T*cut_mass_rate*rate/2+coordinate.T*cut_stiffness_rate*coordinate/2)[0]
        current = (rate.T*(cut_mass*mass_matrix.inv()*stiffness-cut_stiffness)*coordinate
            +rate.T*(cut_mass*mass_matrix.inv()*mass_rate-cut_mass_rate)*rate)[0]
        exchange = (-rate.T*cut_mass_rate*rate/2+coordinate.T*cut_stiffness_rate*coordinate/2
            -rate.T*cut_mass*mass_matrix.inv()*residual)[0]
        check('localized_linear_Galerkin_current_with_metric_exchange',sp.expand(energy_rate+current-exchange)==0)
        whole_current = (rate.T*(mass_matrix*mass_matrix.inv()*stiffness-stiffness)*coordinate
            +rate.T*(mass_matrix*mass_matrix.inv()*mass_rate-mass_rate)*rate)[0]
        check('whole_domain_linear_control_has_zero_cut_current',sp.expand(whole_current)==0)
        report['next_stage_matrix_lemma'] = dict(current='v^T(M_R M^-1 K-K_R)u + v^T(M_R M^-1 Mdot-M_Rdot)v',
            assumptions='Linear quadratic field action; fixed spatial ansatz; time-dependent symmetric coefficients; positive invertible M; actual partial energy matrices.',
            full_moving_source_candidate_not_substituted=True,valid_for_claim=False)
        replay_run = json.loads((intake/'annular-candidate-reaction-balance-attempt02/status.json').read_text())
        by_branch = {}
        for summary in run['summaries']:
            branch,extension,order = [summary[key] for key in ['branch','extension','order']]
            name = branch+'-'+extension+'-order'+str(order)
            raw = loaded(root/summary['source_path'])
            check(name+'_finite_arrays_and_full_face_node_shapes',all(np.all(np.isfinite(value)) for value in raw.values()
                if value.dtype.kind in 'fci') and raw['label_node_radius'].shape==(len(raw['labels']),1094)
                and raw['label_face_radius'].shape==(len(raw['labels']),546))
            points,weights = np.polynomial.legendre.leggauss(order)
            cuts = raw['cuts']
            labels = ((cuts[:-1,None]+cuts[1:,None])/2+np.diff(cuts)[:,None]*points/2).ravel()
            weights = (np.diff(cuts)[:,None]*weights/2).ravel()*6*(labels+.5)*(.5-labels)
            check(name+'_segmented_material_rule',close(labels,raw['labels']) and close(weights,raw['weights'])
                and abs(sum(weights)-1)<1e-12 and min(weights)>0)
            time_from_integrals = np.stack([derivative(values,raw['steps']) for values in raw['label_probe_temporal_momentum']])
            time_difference = maximum(time_from_integrals-raw['label_time_work'])
            check(name+'_independent_integrated_time_work',close(time_from_integrals,raw['label_time_work'],absolute=3e-14),time_difference)
            check(name+'_cell_EL_work_reconstructed',close(raw['label_volume'],-raw['label_time_work']-raw['label_space_work'][:,None,:]))
            target = raw['targets']
            face_mask = raw['label_face_radius'][:,:,None]<target
            reconstructed_faces = raw['label_face_average']*raw['label_face_EL']
            check(name+'_face_average_trace_identity',close(reconstructed_faces,raw['label_face_power'],absolute=1e-16))
            internal = np.einsum('lf,lf,lfk->lk',raw['label_face_power'],raw['label_ordinary_mask'],face_mask)
            anchor = np.einsum('lf,lf,lfk->lk',raw['label_face_power'],~raw['label_ordinary_mask'],face_mask)
            exterior = np.einsum('lf,lfk->lk',raw['label_exterior_power'],raw['label_exterior_radius'][:,:,None]<target)
            check(name+'_ordinary_anchor_exterior_cuts',close(internal,raw['label_internal'])
                and close(anchor,raw['label_anchor']) and close(exterior,raw['label_exterior']))
            dust_rate = np.stack([derivative(values,raw['steps']) for values in raw['label_dust_probe']])
            dust = raw['label_velocity'][:,None,None]*(raw['label_dust_force'][:,None,None]-dust_rate[:,:,None])
            dust *= raw['label_source'][:,None,None]<target
            node_mask = raw['label_node_radius'][:,:,None]<target
            gram_field = np.einsum('ln,lnk->lk',raw['label_node_field_power'],node_mask)
            gram_source = np.einsum('ln,lnk->lk',raw['label_node_source_power'],node_mask)
            check(name+'_dust_and_distributed_Gram_work',close(dust,raw['label_dust']) and close(gram_field,raw['label_gram_field'])
                and close(gram_source,raw['label_gram_source']))
            total = raw['label_volume']+internal[:,None,:]+anchor[:,None,:]+exterior[:,None,:]+dust
            total += gram_field[:,None,:]+gram_source[:,None,:]
            integrated = np.tensordot(weights,total,axes=(0,0))
            predicted = -raw['conversion']*integrated
            check(name+'_full_independent_assembly',close(total,raw['label_total'])
                and close(integrated,raw['sum_total']) and close(predicted,raw['predicted']))
            for component in ['volume','internal','anchor','exterior','dust','gram_field','gram_source']:
                check(name+'_'+component+'_integration',close(np.tensordot(weights,raw['label_'+component],axes=(0,0)),raw['sum_'+component]))
            spot = loaded(intake/(prefix+'-attempt01')/(branch+'-'+extension+'-order'+str(order)+'-spot.npz'))
            spot_index = int(raw['spot_index'])
            spot_momentum_rate = derivative(spot['probe_momentum'],spot['steps'])
            spot_mask = spot['physical_radius'][:,None]<target
            spot_measure = spot['measure'][:,None]*spot_mask
            spot_time = np.array([(spot['temporal']*rate) @ spot_measure for rate in spot_momentum_rate])
            spot_space = (spot['temporal']*spot['flux_x']) @ spot_measure
            check(name+'_full_pointwise_spot_reconstruction',close(spot_time,raw['label_time_work'][spot_index])
                and close(spot_space,raw['label_space_work'][spot_index]) and float(spot['label'])==raw['labels'][spot_index])
            selected = [row for row in replay_run['replays'] if row['branch']==branch and row['extension']==extension and row['label']=='endpoint-wide']
            base_row = next(row for row in selected if row['index']==-1)
            base = loaded(root/base_row['source_path'])
            archive = loaded(root/base_row['replay_path'])
            solver,solution = reconstructed_solver(archive)
            owner = IndexedGradedP2System(257,branch=='MTS',2e-5)
            cardinal = np.polynomial.chebyshev.chebvander(2*labels,14) @ owner.layer_rule.inverse
            source = cardinal @ np.asarray(base['coordinates'][:,-1],float)
            velocity = cardinal @ base['rates'][:,-1]
            geometry,radial = solver.values(solution,source)
            metric,lapse = 1-2*geometry[0]/source,np.exp(geometry[1])
            metric_radial = -2*radial[0]/source+2*geometry[0]/source**2
            clock = np.sqrt(lapse**2-velocity**2/metric)
            force = -owner.source_mass*(lapse**2*radial[1]+velocity**2*metric_radial/(2*metric**2))/clock
            check(name+'_source_and_dust_force_from_original_metric',close(source,raw['label_source'])
                and close(velocity,raw['label_velocity']) and close(force,raw['label_dust_force']))
            for row in selected:
                if row['index']==-1:
                    continue
                state = loaded(root/row['source_path'])
                archived = loaded(root/row['replay_path'])
                probe_solver,probe_solution = reconstructed_solver(archived)
                position = cardinal @ np.asarray(state['coordinates'][:,-1],float)
                speed = cardinal @ state['rates'][:,-1]
                values,unused = probe_solver.values(probe_solution,position)
                geometry_factor,lapse_factor = 1-2*values[0]/position,np.exp(values[1])
                momentum = owner.source_mass*speed/(geometry_factor*np.sqrt(lapse_factor**2-speed**2/geometry_factor))
                check(name+'_dust_probe_'+str(row['index'])+'_'+str(row['sign']),
                    close(momentum,raw['label_dust_probe'][:,row['index'],0 if row['sign']==-1 else 1]))
            mesh_path = intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json')
            own(mesh_path)
            mesh = json.loads(mesh_path.read_text())['overlay']
            edges = np.array([float(Fraction(value)) for value in mesh['edges']])
            knots = np.array([float(Fraction(value)) for value in mesh['nodes']])
            packet_path = intake/'annular-complete-frozen-candidate-attempt01'/(branch+'-'+extension+'-action.json')
            own(packet_path)
            packet = json.loads(packet_path.read_text())
            factor = MixedMap(packet['gram_factor']['rows'],packet['gram_factor']['columns'])
            sampling = template_rows(len(knots))[1].tocsr()
            if extension=='reference':
                from scipy.sparse import csr_matrix
                sampling = csr_matrix((0,len(knots)))
            with localcontext() as context:
                context.prec = 64
                image_vertices = np.asarray(factor.apply(decimals(base['coordinates'][:,:-1]).T),float)
                unused,gradients = local_polynomials(mesh,decimals(base['coordinates'][:,:-1]).T)
            for label_index in [0,spot_index,len(labels)-1]:
                selected_cardinal = cardinal[label_index]
                node_radius,jacobian,displacement = owner.model.mapping(knots,source[label_index]-owner.width*labels[label_index])
                node_radius += owner.width*labels[label_index]
                values,derivatives = solver.values(solution,node_radius)
                factor_metric,node_lapse = 1-2*values[0]/node_radius,np.exp(values[1])
                factor_radial = -2*derivatives[0]/node_radius+2*values[0]/node_radius**2
                gamma = node_radius**2*node_lapse*np.sqrt(factor_metric)/jacobian
                jacobian_source = np.where(knots<owner.model.anchor,1/(owner.model.anchor-owner.model.radii[0]),
                    -1/(owner.model.radii[-1]-owner.model.anchor))
                gamma_source = gamma*(displacement*(2/node_radius+derivatives[1]+factor_radial/(2*factor_metric))-jacobian_source/jacobian)
                image = image_vertices @ selected_cardinal
                with localcontext() as context:
                    context.prec = 64
                    gram_force = -np.asarray(factor.apply(decimal_array(((sampling @ gamma)*image)[:,None]),transpose=True)[:,0],float)
                field_power = (selected_cardinal @ base['rates'][:,:-1])*gram_force
                source_power = -velocity[label_index]*gamma_source*(sampling.T @ (image**2/2))
                check(name+'_Gram_spot_from_parent_'+str(label_index),close(field_power,raw['label_node_field_power'][label_index])
                    and close(source_power,raw['label_node_source_power'][label_index])
                    and close(node_radius,raw['label_node_radius'][label_index]))
                local_gradient = np.einsum('cpl,l->cp',gradients,selected_cardinal)
                interior_edges = edges[1:-1]
                radii,jacobians,displacements = owner.model.mapping(interior_edges,source[label_index]-owner.width*labels[label_index])
                radii += owner.width*labels[label_index]
                left_jacobians = jacobians.copy()
                at_anchor = interior_edges==owner.model.anchor
                left_jacobians[at_anchor] = (source[label_index]-owner.model.radii[0]-owner.width*labels[label_index])/(owner.model.anchor-owner.model.radii[0])
                gradient_left = np.sum(local_gradient[:-1],axis=1)/left_jacobians
                gradient_right = local_gradient[1:,0]/jacobians
                indices = np.array(mesh['elements'])[:-1,-1]
                field_rate = selected_cardinal @ base['rates'][:,:-1]
                common_rate = np.where(indices>=0,field_rate[np.maximum(indices,0)],0.)
                speed = displacements*velocity[label_index]
                time_left,time_right = common_rate-speed*gradient_left,common_rate-speed*gradient_right
                values,unused = solver.values(solution,radii)
                metric_faces,lapse_faces = 1-2*values[0]/radii,np.exp(values[1])
                alpha,beta = radii**2/(lapse_faces*np.sqrt(metric_faces)),radii**2*lapse_faces*np.sqrt(metric_faces)
                energy_left,energy_right = (alpha*time_left**2+beta*gradient_left**2)/2,(alpha*time_right**2+beta*gradient_right**2)/2
                physical_jump = beta*(time_right*gradient_right-time_left*gradient_left)+speed*(energy_right-energy_left)
                check(name+'_independent_energy_jump_'+str(label_index),close(physical_jump,raw['label_face_power'][label_index],absolute=1e-16))
            old = loaded(intake/'annular-candidate-energy-current-attempt01'/(branch+'-'+extension+'-endpoint-wide-currents.npz'))
            indices = np.asarray(run['target_grid_indices'])
            check(name+'_held_fixed_observed_profile',np.array_equal(target,old['radius'][indices])
                and np.array_equal(raw['observed'],old['conditional_residual'][indices])
                and close(raw['conversion'],old['wave48_conversion'][indices]))
            error = maximum(predicted[-1]-raw['observed'])
            sensitivity = maximum(predicted[-1]-predicted[0])
            tolerance = 5e-12+.05*maximum(raw['observed'])
            scaled_observed = raw['observed']/raw['conversion']
            scaled_prediction = predicted[-1]/raw['conversion']
            difference_error = raw['conversion']*((scaled_prediction-scaled_prediction[-1])-(scaled_observed-scaled_observed[-1]))
            post_source = target>max(source)
            pre_source = target<min(source)
            report['shape_diagnostics'].append(dict(branch=branch,extension=extension,order=order,
                post_source_absolute_prediction_error=maximum((predicted[-1]-raw['observed'])[post_source]),
                post_source_outer_referenced_difference_error=maximum(difference_error[post_source]),
                pre_source_absolute_prediction_error=maximum((predicted[-1]-raw['observed'])[pre_source]),
                outer_absolute_error=float(predicted[-1,-1]-raw['observed'][-1]),
                interpretation='Post-run integrating-factor difference diagnostic, not a fitted boundary condition or a corrected physical prediction.',
                source_path=summary['source_path'],valid_for_claim=False))
            for quantity,value in [('independent_Ward_prediction',error),('source_derivative_estimate_change',sensitivity)]:
                recorded = next(row for row in run['scientific_checks'] if row['branch']==branch and row['extension']==extension
                    and row['order']==order and row['quantity']==quantity)
                check(name+'_'+quantity+'_gate',close(value,recorded['error']) and close(tolerance,recorded['tolerance'])
                    and recorded['passed']==bool(value<=tolerance))
            for index,radius in enumerate(target):
                report['comparisons'].append(dict(branch=branch,extension=extension,order=order,radius=float(radius),
                    observed=float(raw['observed'][index]),predicted=float(predicted[-1,index]),
                    error=float(predicted[-1,index]-raw['observed'][index]),
                    prediction_derivative_change=float(predicted[-1,index]-predicted[0,index]),
                    source_path=summary['source_path'],valid_for_claim=False))
            faces = raw['sum_internal']+raw['sum_anchor']+raw['sum_exterior']
            for control,removed in [('omit_faces',faces),('reverse_faces',2*faces),
                ('omit_Gram_field_and_source',raw['sum_gram_field']+raw['sum_gram_source']),('omit_dust_work',raw['sum_dust'][-1])]:
                altered = predicted[-1]+raw['conversion']*removed
                report['ablation_controls'].append(dict(branch=branch,extension=extension,order=order,control=control,
                    altered_error=maximum(altered-raw['observed']),full_error=error,tolerance=tolerance,
                    altered_rejected=bool(maximum(altered-raw['observed'])>tolerance),valid_for_claim=False))
            by_branch.setdefault(extension,{})[order] = predicted[-1]
            save()
        for extension,orders in by_branch.items():
            difference = maximum(orders[12]-orders[8])
            recorded = next(row for row in run['scientific_checks'] if row['extension']==extension and row['quantity']=='paired_quadrature_8_12')
            check(extension+'_paired_quadrature_gate',close(difference,recorded['error']) and recorded['passed']==bool(difference<=1e-12))
        report.update(summaries=run['summaries'],source_components=run['source_components'],scientific_checks=run['scientific_checks'])
        report['table_rows'] = {name:table(name,report[name]) for name in ['summaries','comparisons','source_components','scientific_checks','ablation_controls','shape_diagnostics']}
        result_path = intake/(prefix+'-computed-results.md')
        if result_path.exists():
            raise FileExistsError(str(result_path))
        lines = ['# Independent Ward-source prediction','',
            'The source is evaluated from action cell/face/dust/Gram work, not from the measured mass-current defect.',
            'Metric time responses are shared archived inputs: this is an identity/decomposition test, not statistically independent observational evidence.','',
            '| Branch | Order | Radius | Observed R | Action-source prediction | Difference | Derivative estimate change |',
            '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
        for row in report['comparisons']:
            lines.append(f"| {row['extension']} | {row['order']} | {row['radius']:.9g} | {row['observed']:.9g} | "
                f"{row['predicted']:.9g} | {row['error']:.9g} | {row['prediction_derivative_change']:.9g} |")
        passed = sum(row['passed'] for row in report['scientific_checks'])
        lines.extend(['',f'Predeclared scientific comparisons: {passed}/15 pass. Failed comparisons, if any, remain in the CSV and seal.','',
            'Inspect the separate cell, face, dust and Gram components and the omission controls before interpreting an apparently small total.',''])
        lines.extend(['## Integrating-factor shape diagnostic','',
            'After the source, compare differences of R/a relative to the outer cut. This cancels a common accumulated offset; it is not a fitted replacement for the inner boundary condition.','',
            '| Branch | Order | Post-source absolute error | Post-source outer-referenced difference error | Pre-source error |',
            '| --- | ---: | ---: | ---: | ---: |'])
        for row in report['shape_diagnostics']:
            lines.append(f"| {row['extension']} | {row['order']} | {row['post_source_absolute_prediction_error']:.9g} | "
                f"{row['post_source_outer_referenced_difference_error']:.9g} | {row['pre_source_absolute_prediction_error']:.9g} |")
        lines.append('')
        result_path.write_text('\n'.join(lines),encoding='utf-8')
        own(result_path,'outputs')
        note = root/'DERIVATION-20260921-independent-Ward-source-and-mass-current.md'
        content = note.read_text(encoding='utf-8')
        citations = re.findall(r'`([^`\r\n]+\.(?:md|py|json|csv|npz))`',content)
        check('completed_report_sources_exist','Numerical results pending' not in content
            and bool(citations) and all((root/name).is_file() for name in citations))
        for name in citations:
            if (root/name).resolve()!=destination.resolve():
                own(root/name)
        own(note)
        for name in ['annular_candidate_Ward_source_20260921.py','run_annular_candidate_Ward_source_20260921.py',
            'seal_annular_candidate_Ward_source_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('no_bytecode_cache',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        since = datetime(2026,9,21,18,25,3,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
        check('protected_workbench_mtime_unchanged',not changed,changed)
        for filename,source in [(prefix+'-resume-snapshot.md',root/'CURRENT_LOCAL_RESUME.md'),(prefix+'-executed-sealer.py',Path(__file__))]:
            path = intake/filename
            if path.exists():
                raise FileExistsError(str(path))
            path.write_bytes(source.read_bytes())
            own(path,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),distinct_files_rehashed=len(hashes),
            prediction_qualified=all(row['passed'] for row in report['scientific_checks']),
            implementation_checks=len(run['checks']),total_failed_attempts_preserved=prior['total_failed_attempts_preserved'],
            next_target='Use the independently reconstructed local Ward source to derive a finite-element kinetic/face current or a controlled projection bound, with metric-shift consistency explicit. Resolve any failed prediction before claiming its source is explained; no fitted flux multiplier.')
        save()
        print(json.dumps({key:report[key] for key in ['state','distinct_files_rehashed','prediction_qualified','table_rows']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
