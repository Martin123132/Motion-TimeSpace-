from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from pathlib import Path
from datetime import datetime,timezone
from decimal import localcontext
from math import fsum
import csv
import hashlib
import json
import re
import traceback
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-energy-current'
    destination = intake/(prefix+'-final-integrity.json')
    if destination.exists():
        raise FileExistsError(str(destination))
    report = dict(state='running',inputs={},outputs={},checks=[],regions=[],branch_contrasts=[],
        scientific_checks=[],power_checks=[],github_action=False,subagents_used=False,valid_for_physics_claim=False,
        original_action_unchanged=True,Gram_mixed_stress_not_assumed=True,
        protected_scan_scope='mtime since2026-09-21T17:53:01Z, not a pre-turn whole-tree hash')
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
                    raise RuntimeError('Changed owned evidence: '+name)
                report['inputs'][str(source.relative_to(root))] = expected
        own(path)
        return data
    def loaded(path):
        own(path)
        with np.load(path,allow_pickle=False) as archive:
            return {key:archive[key].copy() for key in archive.files}
    def close(first,second,absolute=1e-23,relative=5e-12):
        first,second = np.asarray(first),np.asarray(second)
        return bool(np.all(np.isfinite(first)) and np.all(np.isfinite(second))
            and (first.size==0 or np.max(abs(first-second))<=absolute+relative*max(float(np.max(abs(second))),1e-30)))
    def derivative(values,steps):
        divisors = 2*np.asarray(steps).reshape((-1,)+(1,)*(values.ndim-2))
        centered = (values[:,1]-values[:,0])/divisors
        return centered,(4*centered[1:]-centered[:-1])/3
    def maximum(values):
        return float(np.max(abs(values)))
    def table(label,rows):
        path = intake/(prefix+'-'+label+'.csv')
        if path.exists():
            raise FileExistsError(str(path))
        sourced = [dict(row,record_source=str(destination.relative_to(root))) for row in rows]
        with path.open('w',encoding='utf-8',newline='') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(dict.fromkeys(key for row in sourced for key in row)))
            writer.writeheader()
            writer.writerows(sourced)
        with path.open(encoding='utf-8',newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(label+'_CSV_sources_and_shape',len(parsed)==len(rows) and all(None not in row and None not in row.values()
            and row['valid_for_claim']=='False' and (root/row['record_source']).is_file() for row in parsed))
        own(path,'outputs')
        return len(rows)
    save()
    try:
        prior = inherit(intake/'annular-candidate-reaction-balance-final-integrity.json')
        run = inherit(intake/(prefix+'-attempt01/status.json'))
        check('completed_runs_and_unchanged_modes',prior['state']=='complete' and run['state']=='complete'
            and all(row['passed'] for row in run['checks']) and run['full_components']==16425
            and run['action_unchanged'] and not run['new_trajectory'] and run['gram_mass_current_is_conditional']
            and len(run['cases'])==6 and len(run['scientific_checks'])==36)
        replay_run = json.loads((intake/'annular-candidate-reaction-balance-attempt02/status.json').read_text())
        import sympy as sp
        redshift_first,redshift_second,current,energy,energy_rate,power,exchange,redshift_rate = sp.symbols(
            'a_i a_j J h hdot power Q adot')
        substituted_rate = -power-current+exchange
        mass_identity = redshift_first*substituted_rate+redshift_rate*energy+redshift_first*power
        mass_identity += (redshift_first+redshift_second)*current/2
        mass_identity -= redshift_first*exchange+redshift_rate*energy+(redshift_second-redshift_first)*current/2
        check('independent_bond_redshift_exchange_sign',sp.expand(mass_identity)==0)
        radius,coupling,metric = sp.symbols('r kappa F',positive=True)
        mass,rho,pressure,rho_time,mass_time,flux,flux_radial = sp.symbols('mu rho p rho_t mu_t J J_r')
        radial_metric = 2*mass/radius**2-2*coupling*radius*rho
        radial_lapse_log = mass/(radius**2*metric)+coupling*radius*pressure/metric
        coefficient = sp.simplify(radial_lapse_log-radial_metric/(2*metric))
        check('radial_constraints_derive_positive_integrating_factor_coefficient',
            sp.simplify(coefficient-coupling*radius*(rho+pressure)/metric)==0)
        stress_divergence = -rho_time-(flux_radial+coefficient*flux)/(coupling*radius**2)
        stress_divergence -= (rho+pressure)*mass_time/(radius*metric)
        defect_radial = coupling*radius**2*rho_time+flux_radial
        check('derived_mixed_constraint_defect_propagation',sp.simplify(defect_radial
            +coefficient*(mass_time+flux)+coupling*radius**2*stress_divergence)==0)
        phase_data = {}
        for summary in run['summaries']:
            branch,extension,label = [summary[key] for key in ['branch','extension','label']]
            name = branch+'-'+extension+'-'+label
            raw = loaded(root/summary['source_path'])
            base_row = next(row for row in replay_run['replays'] if row['branch']==branch and row['extension']==extension
                and row['label']==label and row['index']==-1)
            base = loaded(root/base_row['source_path'])
            packet_path = intake/'annular-complete-frozen-candidate-attempt01'/(branch+'-'+extension+'-action.json')
            own(packet_path)
            packet = json.loads(packet_path.read_text())
            factor = MixedMap(packet['gram_factor']['rows'],packet['gram_factor']['columns'])
            sampling = template_rows(1094)[1].tocsr()
            if extension=='reference':
                from scipy.sparse import csr_matrix
                sampling = csr_matrix((0,1094))
            check(name+'_finite_arrays_full_shapes',all(np.all(np.isfinite(value)) for value in raw.values()
                if value.dtype.kind in 'fci') and raw['node_force'].shape==(65,1094)
                and base['rates'].shape==(15,1095) and raw['mass_values'].shape==(3,2,len(raw['radius'])))
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            cardinal = np.polynomial.chebyshev.chebvander(2*raw['node_labels'],14) @ native.layer_rule.inverse
            check(name+'_cardinal_and_full_rate_source',close(cardinal,raw['node_cardinal'])
                and close(cardinal @ base['rates'][:,:-1],raw['node_velocity'])
                and close(cardinal @ base['rates'][:,-1],raw['node_source_velocity']))
            with localcontext() as context:
                context.prec = 64
                image = cardinal @ np.asarray(factor.apply(decimals(base['coordinates'][:,:-1]).T).T,float)
                image_rate = cardinal @ np.asarray(factor.apply(decimal_array(base['rates'][:,:-1].T)).T,float)
                sampled = (sampling @ raw['node_gamma'].T).T
                force = -np.asarray(factor.apply(decimal_array((sampled*image).T),transpose=True).T,float)
            check(name+'_actual_D_images_and_Gram_force',close(image,raw['node_image'])
                and close(image_rate,raw['node_image_rate']) and close(force,raw['node_force'])
                and close(sampled,raw['node_sampled']))
            node_load = (sampling.T @ (image**2/2).T).T
            internal = raw['node_gamma']*(sampling.T @ (image*image_rate).T).T
            power = raw['node_velocity']*force
            increments = -power-internal
            check(name+'_actual_energy_allocation_and_current',close(node_load,raw['node_node_load'])
                and close(internal,raw['node_internal_rate']) and close(power,raw['node_field_power'])
                and close(increments,raw['node_outward_increment'])
                and close(raw['node_gamma']*node_load,raw['node_energy']))
            negative_controls = 0
            for label_index in [0,16,32,48,64]:
                for cut in [1,364,547,1093]:
                    left_velocity = raw['node_velocity'][label_index].copy()
                    left_velocity[cut:] = 0
                    left_gamma = raw['node_gamma'][label_index].copy()
                    left_gamma[cut:] = 0
                    with localcontext() as context:
                        context.prec = 64
                        left_image_rate = np.asarray(factor.apply(decimal_array(left_velocity[:,None]))[:,0],float)
                    left_sampled = sampling @ left_gamma
                    cut_formula = fsum(image[label_index]*(sampled[label_index]*left_image_rate-left_sampled*image_rate[label_index]))
                    cut_prefix = fsum(increments[label_index,:cut])
                    budget = 1e-21+1e-10*fsum(abs(power[label_index])+abs(internal[label_index]))
                    check(name+'_independent_cut_'+str(label_index)+'_'+str(cut),abs(cut_formula-cut_prefix)<=budget,
                        dict(error=abs(cut_formula-cut_prefix),roundoff_budget=budget))
                    if abs(cut_formula+cut_prefix)>budget:
                        negative_controls += 1
            check(name+'_current_orientation_control',extension=='reference' or negative_controls>0,negative_controls)
            unused,gamma_rate = derivative(raw['probe_gamma'],raw['steps'])
            unused,metric_rate = derivative(raw['probe_metric_log'],raw['steps'])
            energies = np.array([[np.sum(gamma*(sampling.T @ (image**2/2).T).T,axis=1)
                for gamma,image in zip(gamma_pair,image_pair)]
                for gamma_pair,image_pair in zip(raw['probe_gamma'],raw['probe_image'])])
            unused,energy_rate = derivative(energies,raw['steps'])
            metric_exchange = np.sum(raw['node_gamma']*metric_rate*node_load,axis=2)
            analytic_rate = np.sum(internal,axis=1)+np.sum(gamma_rate*node_load,axis=2)
            source_power = -raw['node_source_velocity']*np.sum(raw['node_gamma_source']*node_load,axis=1)
            balance = analytic_rate+np.sum(power,axis=1)+source_power-metric_exchange
            check(name+'_metric_exchange_and_direct_Gram_power',close(energies,raw['probe_energy'])
                and close(energy_rate,raw['energy_rate']) and close(gamma_rate,raw['gamma_rate'])
                and close(metric_rate,raw['metric_rate']) and close(source_power,raw['node_source_power'])
                and close(analytic_rate,raw['analytic_energy_rate']) and close(balance,raw['energy_balance']))
            centered,mass_rate = derivative(raw['mass_values'],raw['steps'])
            unused,ordinary_rate = derivative(raw['ordinary_mass'],raw['steps'])
            conversion = .1*np.sqrt(raw['wave48_metric'])/raw['wave48_lapse']
            wave_current = -.1*raw['radius']**2*raw['wave48_metric']*raw['wave48_cross_moment']
            dust_current = raw['wave48_velocity']*raw['wave48_dust_mass_density']
            bare = mass_rate[-1]+wave_current+dust_current
            gram_current = raw['gram64_graph']+raw['gram64_advection']
            conditional = bare+conversion*gram_current
            check(name+'_independent_mass_current_reconstruction',close(centered,raw['mass_differences'])
                and close(mass_rate,raw['mass_rate']) and close(ordinary_rate,raw['ordinary_rate'])
                and close(wave_current,raw['wave48_wave_mass_current'],absolute=1e-19)
                and close(dust_current,raw['wave48_dust_mass_current'],absolute=1e-19)
                and close(bare,raw['bare_residual'],absolute=1e-18)
                and close(conditional,raw['conditional_residual'],absolute=1e-18))
            signal = max(maximum(mass_rate[-1]),maximum(raw['wave48_wave_mass_current']+dust_current),1e-30)
            tolerance = 1e-10+1e-3*signal
            science = dict(mass_derivative_scale_change=maximum(mass_rate[-1]-mass_rate[0]),
                wave_label_quadrature_change=maximum(raw['wave28_wave_mass_current']+raw['wave28_dust_mass_current']-raw['wave48_wave_mass_current']-dust_current),
                Gram_cut_degree_change=maximum(conversion*(raw['gram32_total']-raw['gram64_total'])),
                mass_current_wave_dust_only=maximum(raw['bare_residual']),
                mass_current_conditional_Gram_conversion=maximum(raw['conditional_residual']),
                Gram_node_global_power_cancellation=maximum(np.sum(increments,axis=1)))
            power_scale = maximum(np.sum(abs(power)+abs(internal),axis=1))
            for quantity,error in science.items():
                recorded = next(row for row in run['scientific_checks'] if row['branch']==branch and row['extension']==extension
                    and row['label']==label and row['quantity']==quantity)
                threshold = 1e-22+5e-11*max(power_scale,1e-30) if quantity=='Gram_node_global_power_cancellation' else tolerance
                check(name+'_'+quantity+'_predeclared_gate_rebuilt',close(error,recorded['error']) and close(threshold,recorded['tolerance'])
                    and recorded['passed']==bool(error<=threshold))
            report['power_checks'].append(dict(branch=branch,extension=extension,label=label,
                global_cancellation_error=maximum(np.sum(increments,axis=1)),
                finite_difference_energy_error=maximum(energy_rate[-1]-analytic_rate[-1]),
                explicit_metric_exchange_balance_error=maximum(balance[-1]),
                metric_exchange_max=maximum(metric_exchange[-1]),source_power_max=maximum(source_power),
                energy_rate_scale_change=maximum(energy_rate[-1]-energy_rate[0]),
                balance_estimate_change=maximum(balance[-1]-balance[0]),
                orientation_negative_controls_detected=negative_controls,source_path=summary['source_path'],valid_for_claim=False))
            for region,mask in [('all',np.ones(len(bare),dtype=bool)),('outside_source',raw['wave48_source_density']==0),
                ('source',raw['wave48_source_density']>0)]:
                scale = max(maximum((wave_current+dust_current)[mask]),maximum(mass_rate[-1,mask]),1e-30)
                report['regions'].append(dict(branch=branch,extension=extension,label=label,region=region,points=int(sum(mask)),
                    current_scale=scale,bare_max=maximum(raw['bare_residual'][mask]),conditional_max=maximum(raw['conditional_residual'][mask]),
                    bare_RMS=float(np.sqrt(np.mean(raw['bare_residual'][mask]**2))),
                    conditional_RMS=float(np.sqrt(np.mean(raw['conditional_residual'][mask]**2))),
                    conditional_relative_to_region_current=maximum(raw['conditional_residual'][mask])/scale,
                    derivative_sensitivity=maximum((mass_rate[-1]-mass_rate[0])[mask]),
                    candidate_Gram_mass_current_max=maximum((conversion*gram_current)[mask]),
                    largest_conditional_residual_radius=float(raw['radius'][mask][np.argmax(abs(raw['conditional_residual'][mask]))]),
                    diagnostic_after_initial_run_not_new_predeclared_gate=True,
                    source_path=summary['source_path'],valid_for_claim=False))
            phase_data[extension,label] = raw
            save()
        for label in ['initial','endpoint-wide']:
            reference = phase_data['reference',label]
            for extension in ['primary','alternative']:
                current = phase_data[extension,label]
                check(extension+'-'+label+'_same_physical_grid',np.array_equal(current['radius'],reference['radius']))
                mask = (reference['wave48_source_density']==0)&(current['wave48_source_density']==0)
                contrast_bare = current['bare_residual']-reference['bare_residual']
                contrast_conditional = current['conditional_residual']-reference['conditional_residual']
                report['branch_contrasts'].append(dict(extension=extension,label=label,
                    outside_source_bare_contrast_max=maximum(contrast_bare[mask]),
                    outside_source_conditional_contrast_max=maximum(contrast_conditional[mask]),
                    outside_source_bare_contrast_RMS=float(np.sqrt(np.mean(contrast_bare[mask]**2))),
                    outside_source_conditional_contrast_RMS=float(np.sqrt(np.mean(contrast_conditional[mask]**2))),
                    interpretation='Matched-grid diagnostic; not proof of cancelling numerical errors or identical branch states.',
                    valid_for_claim=False))
        report['scientific_checks'] = run['scientific_checks']
        report['summaries'] = run['summaries']
        report['table_rows'] = {key:table(key,report[key]) for key in ['summaries','scientific_checks','regions','power_checks','branch_contrasts']}
        result_path = intake/(prefix+'-computed-results.md')
        if result_path.exists():
            raise FileExistsError(str(result_path))
        lines = ['# Gram energy transport and radial mass-current results','',
            'Private same-action directional test; inherited coordinate units. Gram-to-mass conversion is a candidate diagnostic.',
            'Global residual ratios use the larger dust-dominated scale; outside-source rows prevent that scale hiding the smaller wave residual.',
            'Observed derivative and quadrature sensitivities are not rigorous error bounds.','',
            '| Branch | Phase | Region | Current scale | Bare residual max | Candidate-corrected max | Relative corrected | Derivative sensitivity |',
            '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |']
        for row in report['regions']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['region']} | {row['current_scale']:.8g} | "
                f"{row['bare_max']:.8g} | {row['conditional_max']:.8g} | {row['conditional_relative_to_region_current']:.8g} | {row['derivative_sensitivity']:.8g} |")
        lines.extend(['','## Same-action Gram power','',
            '| Branch | Phase | Global power cancellation | Direct derivative discrepancy | Metric-exchange balance discrepancy |',
            '| --- | --- | ---: | ---: | ---: |'])
        for row in report['power_checks']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['global_cancellation_error']:.8g} | "
                f"{row['finite_difference_energy_error']:.8g} | {row['explicit_metric_exchange_balance_error']:.8g} |")
        lines.extend(['','## Matched-grid MTS minus reference diagnostic','',
            '| Branch | Phase | Bare contrast max | Candidate-corrected contrast max | Bare RMS | Corrected RMS |',
            '| --- | --- | ---: | ---: | ---: | ---: |'])
        for row in report['branch_contrasts']:
            lines.append(f"| {row['extension']} | {row['label']} | {row['outside_source_bare_contrast_max']:.8g} | "
                f"{row['outside_source_conditional_contrast_max']:.8g} | {row['outside_source_bare_contrast_RMS']:.8g} | {row['outside_source_conditional_contrast_RMS']:.8g} |")
        lines.extend(['','All36 predeclared smoke comparisons pass. Passing these loose absolute/relative smoke gates is distinct from resolving the smaller current defect.',
            'The next derivation should construct the discrete wave-energy current and its weak-EL/interface contributions, and the metric/shift variation of the same Gram action, rather than fit a multiple of its energy flux.',''])
        result_path.write_text('\n'.join(lines),encoding='utf-8')
        own(result_path,'outputs')
        note = root/'DERIVATION-20260921-Gram-energy-and-radial-mass-current.md'
        content = note.read_text(encoding='utf-8')
        citations = re.findall(r'`([^`\r\n]+\.(?:md|py|json|csv|npz))`',content)
        check('report_and_cited_paths_exist','RESULTS_PENDING' not in content and bool(citations)
            and all((root/name).is_file() for name in citations))
        for name in citations:
            if (root/name).resolve()!=destination.resolve():
                own(root/name)
        own(note)
        for name in ['annular_candidate_energy_current_20260921.py','run_annular_candidate_energy_current_20260921.py',
            'seal_annular_candidate_energy_current_20260921.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('compiled_without_bytecode_cache',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        since = datetime(2026,9,21,17,53,1,tzinfo=timezone.utc).timestamp()
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
            total_failed_attempts_preserved=prior['total_failed_attempts_preserved'],implementation_checks=len(run['checks']),
            scientific_smoke_passed=sum(row['passed'] for row in run['scientific_checks']),
            next_target='Use the derived (N R/sqrtF)_r=-kappa r^2 N H/sqrtF propagation law. Derive H independently from same-action wave cell/face work, dust and Gram metric-shift variation, then explain or bound the small wave-region residual with reference retained. Do not fit a Gram multiplier or infer H tautologically from R.')
        save()
        print(json.dumps({key:report[key] for key in ['state','distinct_files_rehashed','scientific_smoke_passed','table_rows']}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
