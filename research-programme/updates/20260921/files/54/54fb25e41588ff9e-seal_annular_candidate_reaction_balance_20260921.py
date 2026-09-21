from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime,timezone
import csv
import hashlib
import json
import re
import traceback
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-reaction-balance'
    destination = intake/(prefix+'-final-integrity.json')
    if destination.exists():
        raise FileExistsError(str(destination))
    report = dict(state='running',inputs={},outputs={},checks=[],reconstructed=[],summaries=[],scientific_checks=[],
        analytic_controls=[],projection_summaries=[],github_action=False,subagents_used=False,valid_for_physics_claim=False,
        full_GR_limit_proven=False,protected_scan_scope='mtime since2026-09-21T16:47:30Z, not a pre-turn whole-tree hash')
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
        if not passed or len(report['checks']) % 25 == 0:
            save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs','outputs']:
            for name,expected in data[category].items():
                source = (root/name).resolve()
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed owned file: '+name)
                report['inputs'][str(source.relative_to(root))] = expected
        own(path)
        return data

    def loaded(path):
        own(path)
        with np.load(path,allow_pickle=False) as archive:
            return {key:archive[key].copy() for key in archive.files}

    def close(actual,expected):
        actual,expected = np.asarray(actual),np.asarray(expected)
        return bool(np.all(np.isfinite(actual)) and np.all(np.isfinite(expected))
            and np.max(abs(actual-expected)) <= 1e-18+5e-13*max(float(np.max(abs(expected))),1e-30))

    def integrated(measure,values):
        return float(np.sum(np.longdouble(measure)*np.longdouble(values),dtype=np.longdouble))

    def table(label,rows):
        path = intake/(prefix+'-'+label+'.csv')
        if path.exists():
            raise FileExistsError(str(path))
        sourced = [dict(row,record_source=str(destination.relative_to(root))) for row in rows]
        columns = list(dict.fromkeys(key for row in sourced for key in row))
        with path.open('w',encoding='utf-8',newline='') as stream:
            writer = csv.DictWriter(stream,fieldnames=columns)
            writer.writeheader()
            writer.writerows(sourced)
        with path.open(encoding='utf-8',newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(label+'_CSV_parses_with_sources',len(parsed) == len(rows) and all(None not in row
            and None not in row.values() and row['valid_for_claim'] == 'False'
            and (root/row['record_source']).is_file() for row in parsed))
        own(path,'outputs')
        return len(rows)

    save()
    try:
        prior = inherit(intake/'annular-candidate-source-acceleration-v3-final-integrity.json')
        failed = inherit(intake/'annular-candidate-reaction-balance-attempt01/status.json')
        run_path = intake/'annular-candidate-reaction-balance-attempt02/status.json'
        run = inherit(run_path)
        check('input_lineage_and_immutable_save_failure_preserved',prior['state'] == 'complete'
            and failed['state'] == 'failed' and 'multiple values' in failed['error']
            and run['state'] == 'complete' and all(row['passed'] for row in run['checks'])
            and run['inherited_failed_executions'] == prior['total_failed_attempts_preserved']+1)
        check('all_modes_equal_branches_and_original_action',run['full_components'] == 16425
            and not run['modes_deleted'] and run['original_action_unchanged'] and run['replay_not_new_trajectory']
            and run['reference_orders'] == [16,32] and run['material_order'] == 48
            and len(run['cases']) == 6 and len(run['replays']) == 42 and len(run['summaries']) == 12)
        import sympy as sp
        alpha,beta,speed,slope,jacobian,displacement,jacobian_source = sp.symbols('alpha beta V a J d J_b')
        temporal = -slope*speed
        momentum_time = jacobian_source*speed*alpha*temporal
        flux_space = -alpha*temporal*jacobian_source*speed
        check('manufactured_constant_speed_pinned_wave_solves_bulk_EL',sp.expand(momentum_time+flux_space) == 0)
        energy = (alpha*temporal**2+beta*slope**2)/2
        energy_flux = -beta*temporal*slope
        traction = (beta-alpha*speed**2)*slope**2/2
        check('moving_interface_energy_flux_equals_traction_power',sp.expand(energy_flux-speed*energy-speed*traction) == 0)
        field_time,field_radial,field_tt,field_rr,field_tr,alpha_time,beta_time,beta_radial = sp.symbols(
            'field_time field_radial field_tt field_rr field_tr alpha_time beta_time beta_radial')
        field_EL = -alpha_time*field_time-alpha*field_tt+beta_radial*field_radial+beta*field_rr
        energy_time = alpha_time*field_time**2/2+alpha*field_time*field_tt+beta_time*field_radial**2/2+beta*field_radial*field_tr
        energy_flux_radial = -beta_radial*field_time*field_radial-beta*field_tr*field_radial-beta*field_time*field_rr
        check('off_shell_wave_energy_exchange_identity',sp.expand(energy_time+energy_flux_radial
            +field_time*field_EL+alpha_time*field_time**2/2-beta_time*field_radial**2/2) == 0)
        report['energy_identity'] = dict(wave_energy='(alpha phi_t^2+beta phi_r^2)/2',
            wave_flux='-beta phi_t phi_r',wave_EL='-partial_t(alpha phi_t)+partial_r(beta phi_r)',
            local_identity='partial_t e+partial_r j=-phi_t E-0.5 alpha_t phi_t^2+0.5 beta_t phi_r^2',
            moving_pinned_interface='j-V e=V T',Gram_and_gravity_current_not_added_by_assumption=True)
        for left_slope,right_slope in [(2.,1.),(1.,1.),(0.,0.)]:
            kinetic,spatial,speed_value = 1.3,2.1,.2
            expected = .5*(spatial-kinetic*speed_value**2)*(left_slope**2-right_slope**2)
            boundary_values = []
            for gradient in [left_slope,right_slope]:
                temporal_value = -speed_value*gradient
                density = .5*(kinetic*temporal_value**2-spatial*gradient**2)
                flux = -kinetic*temporal_value*speed_value-spatial*gradient
                boundary_values.append(density-gradient*flux)
            measured = boundary_values[0]-boundary_values[1]
            check('manufactured_interface_force_'+str(left_slope)+'_'+str(right_slope),abs(measured-expected) < 2e-15)
            report['analytic_controls'].append(dict(left_slope=left_slope,right_slope=right_slope,
                measured=measured,expected=expected,zero_force=bool(expected == 0),
                constant_coefficient_control_not_spherical_gravity=True,valid_for_claim=False))
        mesh_data = {}
        for branch in ['reference','MTS']:
            mesh_path = intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json')
            own(mesh_path)
            mesh_data[branch] = json.loads(mesh_path.read_text())['overlay']
        case_orders = {}
        for summary in run['summaries']:
            branch,extension,label,order = [summary[key] for key in ['branch','extension','label','order']]
            name = '-'.join([branch,extension,label,str(order)])
            raw = loaded(root/summary['source_path'])
            check(name+'_finite_arrays_and_shapes',all(np.all(np.isfinite(raw[key])) for key in raw if raw[key].dtype.kind in 'fci')
                and raw['cardinal'].shape == (48,15) and raw['canonical_force'].shape == (15,1095)
                and len(raw['offsets']) == 49 and raw['offsets'][-1] == len(raw['reference']))
            points,weights = np.polynomial.legendre.leggauss(48)
            weights = weights/2*6*(points/2+.5)*(.5-points/2)
            check(name+'_material_measure',close(raw['labels'],points/2) and close(raw['weights'],weights))
            elements = np.array(mesh_data[branch]['elements'])
            hinges = np.flatnonzero((elements[:-1,-1] == -1)&(elements[1:,0] == -1))
            check(name+'_one_pinned_anchor',len(hinges) == 1)
            hinge = int(hinges[0])
            reconstructed = []
            for material_index in range(48):
                section = slice(int(raw['offsets'][material_index]),int(raw['offsets'][material_index+1]))
                measure = raw['measure'][section]
                momentum_rates,source_rates = [],[]
                for index,step in enumerate(raw['derivative_steps']):
                    momentum_rates.append((np.longdouble(raw['probe_momentum'][2*index,section])
                        -np.longdouble(raw['probe_momentum'][2*index+1,section]))/(2*np.longdouble(step)))
                    source_rates.append((np.longdouble(raw['probe_source_momentum'][2*index,section])
                        -np.longdouble(raw['probe_source_momentum'][2*index+1,section]))/(2*np.longdouble(step)))
                row = {}
                for index in range(2):
                    momentum_rate = (4*momentum_rates[index+1]-momentum_rates[index])/3
                    source_rate = (4*source_rates[index+1]-source_rates[index])/3
                    eta,eta_dot,momentum,force,flux_x,boundary_x = [raw[key][section] for key in
                        ['eta','eta_dot','momentum','force','flux_x','boundary_x']]
                    volume = -eta*(momentum_rate+flux_x)
                    direct = force-eta_dot*momentum-eta*momentum_rate
                    channels = dict(volume=integrated(measure,volume),direct_product=integrated(measure,direct),
                        direct_difference=integrated(measure,force-source_rate),
                        pointwise_identity_error=float(np.max(abs(direct-volume-boundary_x))),
                        source_momentum_rate=integrated(measure,source_rate))
                    row.update({key+'_'+str(index):value for key,value in channels.items()})
                jumps = raw['edge_right'][material_index,:-1]-raw['edge_left'][material_index,1:]
                check(name+'_label'+str(material_index)+'_raw_face_jumps_and_source_momentum',
                    close(jumps,raw['jump_density'][material_index])
                    and close(raw['source_momentum'][section],raw['eta'][section]*raw['momentum'][section]))
                row.update(anchor=float(jumps[hinge]),internal=float(np.sum(np.delete(jumps,hinge),dtype=np.longdouble)),
                    exterior=float(raw['edge_right'][material_index,-1]-raw['edge_left'][material_index,0]),
                    boundary_integral=integrated(measure,raw['boundary_x'][section]),
                    bulk_force=integrated(measure,raw['force'][section]))
                original = dict(zip(raw['columns'],raw['label_channels'][material_index]))
                check(name+'_label'+str(material_index)+'_independent_cell_integrals',all(close(value,original[key]) for key,value in row.items()))
                row['gram'] = original['gram']
                reconstructed.append(row)
            projected = {key:raw['cardinal'].T @ (weights*np.array([row[key] for row in reconstructed])) for key in reconstructed[0]}
            check(name+'_material_projection_and_Gram_action',all(close(value,raw['projected_'+key]) for key,value in projected.items())
                and np.max(abs(projected['gram']-raw['canonical_gram'][:,-1])) < 1e-14)
            anchor_path = intake/('annular-candidate-source-acceleration-v3-'+branch+'-'+extension+'-'+label+'-traction.npz')
            anchor = loaded(anchor_path)['projected_traction']
            check(name+'_independent_preceding_anchor_matches',np.linalg.norm(projected['anchor']-anchor) < 1e-14)
            base_rows = [row for row in prior['dust_reaction_components'] if row['branch'] == branch
                and row['extension'] == extension and row['label'] == label]
            base_rows.sort(key=lambda row:row['index'])
            reaction = np.array([row['reaction'] for row in base_rows])
            check(name+'_original_raw_reaction_and_root_error_preserved',np.array_equal(reaction,raw['raw_reaction'])
                and np.array_equal(raw['root_residual_derivative'],np.array([row['root_residual_derivative'] for row in base_rows])))
            boundary = projected['anchor']+projected['internal']+projected['exterior']
            total = boundary+projected['volume_1']+projected['gram']
            lower = boundary+projected['volume_0']+projected['gram']
            direct_product = projected['direct_product_1']+projected['gram']
            direct_difference = projected['direct_difference_1']+projected['gram']
            check(name+'_complete_vector_balance_reconstructed',close(total,raw['decomposed'])
                and close(lower,raw['lower_estimate']) and close(direct_product,raw['direct_product'])
                and close(direct_difference,raw['direct_difference']))
            norm = max(float(np.linalg.norm(reaction)),1e-30)
            tolerance = 1e-13+1e-3*norm
            quantities = dict(full_reaction_decomposition=np.linalg.norm(total-reaction),
                integrated_cell_identity=np.linalg.norm(total-direct_product),
                source_momentum_product_rule=np.linalg.norm(direct_product-direct_difference),
                matched_moving_quadrature=np.linalg.norm(direct_difference-reaction),
                derivative_estimate_change=np.linalg.norm(total-lower))
            for quantity,error in quantities.items():
                recorded = next(row for row in run['scientific_checks'] if row['branch'] == branch and row['extension'] == extension
                    and row['label'] == label and row['order'] == order and row['quantity'] == quantity)
                check(name+'_'+quantity+'_unchanged_scientific_gate',close(error,recorded['error'])
                    and recorded['tolerance'] == tolerance and recorded['passed'] == bool(error <= tolerance))
            check(name+'_reported_reaction_remainder',close(np.linalg.norm(total-reaction),summary['full_remainder'])
                and close(np.linalg.norm(total-reaction)/norm,summary['full_remainder_relative_to_reaction']))
            case_orders.setdefault((branch,extension,label),{})[order] = total
            if order == 32:
                old_folder = 'annular-candidate-source-acceleration-attempt01' if label == 'initial' else 'annular-candidate-source-acceleration-wide-probes-attempt01'
                old_name = branch+'-'+extension+'-'+label
                base = loaded(intake/old_folder/(old_name+'-base.npz'))
                physical = loaded(intake/old_folder/(old_name+'-acceleration.npz'))
                mass_row = next(row for row in prior['dust_reaction_summaries'] if row['branch'] == branch
                    and row['extension'] == extension and row['label'] == label)
                coefficient = mass_row['source_mass']*base['clock'][:48]/base['metric'][:48]
                interpolation = base['cardinal'][:48]
                metric_weights = weights*coefficient
                gram_metric = interpolation.T @ (metric_weights[:,None]*interpolation)
                eigenvalues = np.linalg.eigvalsh(gram_metric)
                residual_profile = physical['proper_acceleration'][:48]-physical['geodesic_acceleration'][:48]
                observed_covector = interpolation.T @ (metric_weights*residual_profile)
                projected_coefficients = np.linalg.solve(gram_metric,observed_covector)
                projected_profile = interpolation @ projected_coefficients
                complement = residual_profile-projected_profile
                corrected_covector = total+raw['root_residual_derivative']
                predicted_coefficients = np.linalg.solve(gram_metric,corrected_covector)
                predicted_profile = interpolation @ predicted_coefficients
                covector_error = corrected_covector-observed_covector
                coefficient_error = np.linalg.solve(gram_metric,covector_error)
                weighted_error = float(np.sqrt(max(covector_error @ coefficient_error,0.)))
                uniform_eigenvalue_bound = float(np.linalg.norm(covector_error)/np.sqrt(eigenvalues[0]))
                profile_norm = float(np.sqrt(metric_weights @ residual_profile**2))
                complement_norm = float(np.sqrt(metric_weights @ complement**2))
                dual_norm = float(np.sqrt(max(observed_covector @ projected_coefficients,0.)))
                orthogonality = np.linalg.norm(interpolation.T @ (metric_weights*complement))
                check(name+'_positive_material_acceleration_metric',min(coefficient) > 0 and eigenvalues[0] > 0
                    and orthogonality < 1e-20+1e-12*np.linalg.norm(observed_covector),
                    dict(minimum_coefficient=float(min(coefficient)),minimum_eigenvalue=float(eigenvalues[0]),orthogonality=float(orthogonality)))
                check(name+'_derived_projection_norm_and_error_bound',
                    abs(profile_norm**2-dual_norm**2-complement_norm**2) < 1e-30+1e-12*profile_norm**2
                    and weighted_error <= uniform_eigenvalue_bound*(1+1e-12)
                    and abs(float(np.sqrt(metric_weights @ (predicted_profile-projected_profile)**2))-weighted_error) < 1e-20+1e-10*weighted_error)
                projection_path = intake/(prefix+'-'+old_name+'-acceleration-projection.npz')
                if projection_path.exists():
                    raise FileExistsError(str(projection_path))
                np.savez_compressed(projection_path,labels=base['labels'][:48],weights=weights,coefficient=coefficient,
                    cardinal=interpolation,gram_metric=gram_metric,eigenvalues=eigenvalues,
                    observed_covector=observed_covector,corrected_covector=corrected_covector,
                    residual_profile=residual_profile,projected_profile=projected_profile,
                    predicted_profile=predicted_profile,complement=complement,covector_error=covector_error)
                own(projection_path,'outputs')
                report['projection_summaries'].append(dict(branch=branch,extension=extension,label=label,
                    minimum_metric_eigenvalue=float(eigenvalues[0]),metric_condition=float(eigenvalues[-1]/eigenvalues[0]),
                    actual_residual_weighted_norm=profile_norm,projected_residual_weighted_norm=dual_norm,
                    unresolved_material_projection_norm=complement_norm,corrected_reconstruction_error_norm=weighted_error,
                    covector_error_eigenvalue_bound=uniform_eigenvalue_bound,
                    corrected_error_relative_to_residual=weighted_error/max(profile_norm,1e-30),
                    projection_complement_relative_to_residual=complement_norm/max(profile_norm,1e-30),
                    anchor_power=float(base['rates'][:,-1] @ projected['anchor']),
                    raw_non_dust_power=float(base['rates'][:,-1] @ reaction),
                    decomposed_non_dust_power=float(base['rates'][:,-1] @ total),
                    includes_explicit_inverse_root_correction=True,
                    finite_quadrature_linear_algebra_bound_not_continuum_error_bound=True,
                    source_path=str(projection_path.relative_to(root)),valid_for_claim=False))
            report['reconstructed'].append(dict(branch=branch,extension=extension,label=label,order=order,
                material_samples=48,reference_samples=len(raw['reference']),source_path=summary['source_path'],valid_for_claim=False))
            save()
        for (branch,extension,label),orders in case_orders.items():
            recorded = next(row for row in run['scientific_checks'] if row['branch'] == branch and row['extension'] == extension
                and row['label'] == label and row['quantity'] == 'reference_quadrature_16_32')
            error = float(np.linalg.norm(orders[32]-orders[16]))
            check(branch+'-'+extension+'-'+label+'_16_32_gate_reconstructed',close(error,recorded['error'])
                and recorded['passed'] == bool(error <= recorded['tolerance']))
        report['summaries'] = run['summaries']
        report['scientific_checks'] = run['scientific_checks']
        qualified = all(row['passed'] for row in report['scientific_checks'])
        check('qualification_matches_all_original_science_gates',qualified == run['reaction_decomposition_qualified'])
        report['table_rows'] = {key:table(key,report[key]) for key in ['summaries','scientific_checks','reconstructed','analytic_controls','projection_summaries']}
        report['table_rows']['replays'] = table('replays',run['replays'])
        result_path = intake/(prefix+'-computed-results.md')
        if result_path.exists():
            raise FileExistsError(str(result_path))
        lines = ['# Full source-reaction decomposition','',
            'All values use the inherited normalization and the same15-component material covector basis.',
            'Norms of separate contributions do not add; the vector sum is evaluated before its norm.',
            'Initial small reactions remain derivative-sensitive. Endpoint rows use wider probes.','',
            '| Branch | Phase | Order | Boundary-only remainder / reaction | Full remainder / reaction |',
            '| --- | --- | ---: | ---: | ---: |']
        for row in run['summaries']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['order']} | "
                f"{row['boundary_only_remainder']/row['reaction_norm']:.7g} | {row['full_remainder_relative_to_reaction']:.7g} |")
        lines.extend(['','## Contributions at reference order32','',
            '| Branch | Phase | Anchor norm | Internal jump norm | Cell field EL norm | Gram source norm | Full remainder |',
            '| --- | --- | ---: | ---: | ---: | ---: | ---: |'])
        for row in run['summaries']:
            if row['order'] == 32:
                lines.append(f"| {row['extension']} | {row['label']} | {row['anchor_norm']:.7g} | "
                    f"{row['internal_jump_norm']:.7g} | {row['cell_field_EL_norm']:.7g} | {row['Gram_source_norm']:.7g} | {row['full_remainder']:.7g} |")
        lines.extend(['','Scientific gates passed: '+str(sum(row['passed'] for row in run['scientific_checks']))+'/'+str(len(run['scientific_checks']))+'.',
            'The exact identity and finite-grid numerical validation are distinct from a continuum convergence or parent-action existence theorem.',''])
        lines.extend(['## Derived force-to-acceleration projection','',
            'The positive material metric G integrates m*s/F times the cardinal basis products.',
            'The reconstructed covector includes the separately recorded inverse-root derivative correction.',
            'The last two columns are measured finite-quadrature errors relative to the weighted acceleration-residual norm.','',
            '| Branch | Phase | Corrected reconstruction error / residual | Unresolved material projection / residual |',
            '| --- | --- | ---: | ---: |'])
        for row in report['projection_summaries']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['corrected_error_relative_to_residual']:.7g} | "
                f"{row['projection_complement_relative_to_residual']:.7g} |")
        lines.append('')
        result_path.write_text('\n'.join(lines),encoding='utf-8')
        own(result_path,'outputs')
        note = root/'DERIVATION-20260921-cell-flux-and-Gram-reaction-balance.md'
        content = note.read_text(encoding='utf-8')
        citations = re.findall(r'`([^`\r\n]+\.(?:md|py|json|csv|npz))`',content)
        check('report_complete_and_cited_sources_exist','RESULTS_PENDING' not in content
            and bool(citations) and all((root/name).is_file() for name in citations))
        for name in citations:
            if (root/name).resolve() != destination.resolve():
                own(root/name)
        own(note)
        for name in ['annular_candidate_reaction_balance_20260921.py','run_annular_candidate_reaction_balance_20260921.py',
            'run_annular_candidate_reaction_balance_v2_20260921.py','seal_annular_candidate_reaction_balance_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('compile_no_bytecode_cache',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,21,16,47,30,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged',not changed,changed)
        for filename,source in [(prefix+'-resume-snapshot.md',root/'CURRENT_LOCAL_RESUME.md'),
            (prefix+'-executed-sealer.py',Path(__file__))]:
            path = intake/filename
            if path.exists():
                raise FileExistsError(str(path))
            path.write_bytes(source.read_bytes())
            own(path,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),
            reaction_decomposition_qualified=qualified,distinct_files_rehashed=len(hashes),
            total_failed_attempts_preserved=run['inherited_failed_executions'],
            implementation_checks=len(run['checks']),next_target='Derive and evaluate the same-action radial mass-current balance, using the established source reaction and moving-interface power identity; include the Gram energy flux and explicit metric exchange rather than assuming matter energy is separately constant. Keep the derived weighted force-to-acceleration bound for the geodesic limit.')
        save()
        print(json.dumps({key:report[key] for key in ['state','reaction_decomposition_qualified','distinct_files_rehashed','table_rows']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
