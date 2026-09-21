from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import symbolic_checks, reconstructed_solver, excess_mass, richardson, build_base, wave_dust_current, gram_cut_current, gram_power_probes
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from time import perf_counter
import argparse
import contextlib
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds',type=float,default=9000)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-candidate-energy-current-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        helper = evidence.root/'scripts/annular_candidate_energy_current_20260921.py'
        evidence.own(helper)
        snapshot = evidence.output/('executed-'+helper.name)
        snapshot.write_bytes(helper.read_bytes())
        evidence.own(snapshot,'outputs')
        prior_path = evidence.output.parent/'annular-candidate-reaction-balance-final-integrity.json'
        evidence.own(prior_path)
        prior = json.loads(prior_path.read_text())
        evidence.check('prior_complete',prior['state']=='complete')
        evidence.report.update(full_components=16425,action_unchanged=True,new_trajectory=False,github_action=False,
            subagents_used=False,scientific_checks=[],summaries=[],wave_orders=[28,48],gram_degrees=[32,64],
            mass_absolute_tolerance=1e-10,mass_relative_tolerance=1e-3,
            gram_mass_current_is_conditional=True,maximum_seconds=args.max_seconds)
        def owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key,prior['outputs'].get(key))
            evidence.check(path.name+'_sealed_input',expected is not None and hashlib.sha256(path.read_bytes()).hexdigest()==expected)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe saved-work boundary during energy-current experiment.')
        symbolic_checks(evidence)
        previous = owned(evidence.output.parent/'annular-candidate-reaction-balance-attempt02/status.json')
        main_run = owned(evidence.output.parent/'annular-candidate-source-acceleration-attempt01/status.json')
        wide_run = owned(evidence.output.parent/'annular-candidate-source-acceleration-wide-probes-attempt01/status.json')
        grids = {}
        for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            case = branch+'-'+extension
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            initial = owned(evidence.output.parent/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(evidence.output.parent/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(evidence.output.parent/'annular-complete-frozen-candidate-attempt01'/(case+'-action.json'))
            owner,unused,unused_rates = common_material(native,initial,overlay)
            for label,run in [('initial',main_run),('endpoint-wide',wide_run)]:
                name = case+'-'+label
                progress(name+'-begin')
                selected = [row for row in previous['replays'] if row['branch']==branch and row['extension']==extension and row['label']==label]
                states = {(row['index'],row['sign']):owned(evidence.root/row['source_path']) for row in selected}
                archives = {(row['index'],row['sign']):owned(evidence.root/row['replay_path']) for row in selected}
                steps = run['derivative_steps']
                saved = states[-1,0]
                loads,action = build_base(owner,overlay['overlay'],packet,extension,saved,archives[-1,0],deadline)
                if label not in grids:
                    inner,outer = action.solver.edges[[0,-1]]
                    source = np.asarray(saved['coordinates'][:,-1],float)
                    grids[label] = np.unique(np.r_[np.linspace(inner+.02,outer-.02,129),
                        np.linspace(min(source)-owner.width,max(source)+owner.width,129)])
                radius = grids[label]
                mass_values,ordinary_mass = [],[]
                for index in range(3):
                    masses,ordinary = [],[]
                    for sign in [-1,1]:
                        solver,solution = reconstructed_solver(archives[index,sign])
                        masses.append(excess_mass(solver,solution,radius))
                        ordinary.append(solver.values(solution,radius)[0][0])
                    mass_values.append(masses)
                    ordinary_mass.append(ordinary)
                mass_values,ordinary_mass = np.asarray(mass_values),np.asarray(ordinary_mass)
                mass_differences,mass_rate = richardson(mass_values,steps)
                unused,ordinary_rate = richardson(ordinary_mass,steps)
                base_excess = excess_mass(action.solver,action.solution,radius)
                replay_mass = action.solver.values(action.solution,radius)[0][0]
                evidence.check(name+'_central_mass_removed_without_changing_geometry',
                    np.max(abs(base_excess+owner.central_mass-replay_mass))<5e-15)
                waves = [wave_dust_current(loads,action,radius,order) for order in [28,48]]
                currents,nodes = [],[]
                for degree in [32,64]:
                    progress(name+'-Gram-degree'+str(degree))
                    current,node = gram_cut_current(loads,action,radius,degree)
                    currents.append(current)
                    nodes.append(node)
                probes = gram_power_probes(loads,action,nodes[-1],states,archives,steps)
                nodes_high = nodes[-1]
                signal = max(float(np.max(abs(mass_rate[-1]))),float(np.max(abs(waves[-1]['wave_mass_current']+waves[-1]['dust_mass_current']))),1e-30)
                tolerance = 1e-10+1e-3*signal
                bare = mass_rate[-1]+waves[-1]['wave_mass_current']+waves[-1]['dust_mass_current']
                conditional = bare+waves[-1]['conversion']*currents[-1]['total']
                derivative_change = float(np.max(abs(mass_rate[-1]-mass_rate[0])))
                quadrature_change = float(np.max(abs(waves[0]['wave_mass_current']+waves[0]['dust_mass_current']-
                    waves[1]['wave_mass_current']-waves[1]['dust_mass_current'])))
                gram_change = float(np.max(abs(waves[-1]['conversion']*(currents[0]['total']-currents[1]['total']))))
                power_scale = max(float(np.max(np.sum(abs(nodes_high['field_power'])+abs(nodes_high['internal_rate']),axis=1))),1e-30)
                power_error = float(np.max(abs(np.sum(nodes_high['outward_increment'],axis=1))))
                checks = [('mass_derivative_scale_change',derivative_change,tolerance),
                    ('wave_label_quadrature_change',quadrature_change,tolerance),
                    ('Gram_cut_degree_change',gram_change,tolerance),
                    ('mass_current_wave_dust_only',float(np.max(abs(bare))),tolerance),
                    ('mass_current_conditional_Gram_conversion',float(np.max(abs(conditional))),tolerance),
                    ('Gram_node_global_power_cancellation',power_error,1e-22+5e-11*power_scale)]
                for quantity,error,limit in checks:
                    evidence.report['scientific_checks'].append(dict(branch=branch,extension=extension,label=label,
                        quantity=quantity,error=error,tolerance=limit,passed=bool(error<=limit),valid_for_claim=False))
                evidence.check(name+'_finite_outputs',all(np.all(np.isfinite(value)) for value in
                    [mass_rate,conditional,probes['energy_balance'],nodes_high['force']]))
                if extension=='reference':
                    evidence.check(name+'_reference_Gram_identically_zero',np.all(currents[-1]['total']==0)
                        and np.all(nodes_high['force']==0) and np.all(probes['energy_balance']==0))
                path = evidence.output/(name+'-currents.npz')
                np.savez_compressed(path,radius=radius,steps=steps,mass_values=mass_values,ordinary_mass=ordinary_mass,
                    mass_differences=mass_differences,mass_rate=mass_rate,ordinary_rate=ordinary_rate,
                    bare_residual=bare,conditional_residual=conditional,
                    **{'wave'+str(order)+'_'+key:value for order,row in zip([28,48],waves) for key,value in row.items()},
                    **{'gram'+str(degree)+'_'+key:value for degree,row in zip([32,64],currents) for key,value in row.items()},
                    **{'node_'+key:value for key,value in nodes_high.items()},**probes)
                evidence.own(path,'outputs')
                summary = dict(branch=branch,extension=extension,label=label,points=len(radius),signal=signal,
                    bare_residual_max=float(np.max(abs(bare))),bare_relative=float(np.max(abs(bare)))/signal,
                    conditional_residual_max=float(np.max(abs(conditional))),conditional_relative=float(np.max(abs(conditional)))/signal,
                    mass_derivative_change=derivative_change,ordinary_subtraction_change=float(np.max(abs(ordinary_rate[-1]-mass_rate[-1]))),
                    wave_quadrature_change=quadrature_change,Gram_quadrature_change=gram_change,
                    Gram_energy_current_max=float(np.max(abs(currents[-1]['total']))),
                    Gram_graph_max=float(np.max(abs(currents[-1]['graph']))),Gram_advection_max=float(np.max(abs(currents[-1]['advection']))),
                    Gram_global_power_error=power_error,Gram_power_scale=power_scale,
                    Gram_energy_finite_difference_error=float(np.max(abs(probes['energy_rate'][-1]-probes['analytic_energy_rate'][-1]))),
                    Gram_metric_exchange_balance_error=float(np.max(abs(probes['energy_balance'][-1]))),
                    source_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
                evidence.report['summaries'].append(summary)
                evidence.report['cases'].append(dict(branch=branch,extension=extension,label=label,path=str(path.relative_to(evidence.root))))
                progress(name+'-complete')
                print(json.dumps(summary),flush=True)
        evidence.check('same_six_phase_points_and_all_comparisons',len(evidence.report['cases'])==6
            and len(evidence.report['scientific_checks'])==36)
        evidence.report.update(seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],
            scientific_passed=sum(row['passed'] for row in evidence.report['scientific_checks']),scientific_total=36)),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
