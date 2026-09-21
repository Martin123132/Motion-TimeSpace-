from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import MetricTangent, full_system, localized
from annular_candidate_energy_current_20260921 import build_base, richardson
from annular_candidate_Ward_source_20260921 import probe_action
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from scipy.sparse import save_npz
from time import perf_counter
import argparse
import contextlib
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds', type=float, default=10000)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-moving-Legendre-current-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter()+args.max_seconds
    try:
        for name in ['scripts/annular_moving_Legendre_current_20260921.py',
            'DERIVATION-20260921-moving-source-localized-Legendre-current.md']:
            path = evidence.root/name
            evidence.own(path)
            snapshot = evidence.output/('executed-'+path.name)
            snapshot.write_bytes(path.read_bytes())
            evidence.own(snapshot, 'outputs')
        prior_path = evidence.output.parent/'annular-candidate-Ward-source-v2-final-integrity.json'
        evidence.own(prior_path)
        prior = json.loads(prior_path.read_text())
        evidence.check('prior_Ward_source_complete', prior['state']=='complete')
        evidence.report.update(scientific_checks=[],summaries=[],full_components=16425,
            original_action_unchanged=True,new_trajectory=False,github_action=False,subagents_used=False,
            phase='endpoint-wide',reference_and_material_local_orders=[8,12],hessian_orders=[12,48],
            Ward_energy_absolute_tolerance=2e-11,Ward_energy_relative_tolerance=.05,
            whole_domain_tolerance=2e-11,quadrature_tolerance=2e-11,
            interpretation='Localized semidiscrete Legendre current at fixed-background partial derivatives; no covariant shift completion assumed.',
            inherited_failed_executions=prior['total_failed_attempts_preserved'])

        def owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key, prior['outputs'].get(key))
            evidence.check(path.name+'_sealed_input', expected is not None and hashlib.sha256(path.read_bytes()).hexdigest()==expected)
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
                raise RuntimeError('Safe saved-work wall boundary reached.')

        def scientific(case, name, value, tolerance):
            evidence.report['scientific_checks'].append(dict(case=case,quantity=name,error=float(value),
                tolerance=float(tolerance),passed=bool(np.isfinite(value) and value<=tolerance),valid_for_claim=False))

        replays = owned(evidence.output.parent/'annular-candidate-reaction-balance-attempt02/status.json')['replays']
        for branch, extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            name = branch+'-'+extension
            progress(name+'-begin')
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            original = owned(evidence.output.parent/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(evidence.output.parent/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(evidence.output.parent/'annular-complete-frozen-candidate-attempt01'/(name+'-action.json'))
            owner,unused,unused_rates = common_material(native,original,overlay)
            selected = [row for row in replays if row['branch']==branch and row['extension']==extension and row['label']=='endpoint-wide']
            states = {(row['index'],row['sign']):owned(evidence.root/row['source_path']) for row in selected}
            archives = {(row['index'],row['sign']):owned(evidence.root/row['replay_path']) for row in selected}
            loads,action = build_base(owner,overlay['overlay'],packet,extension,states[-1,0],archives[-1,0],deadline)
            probes = {key:probe_action(action,states[key],archives[key]) for key in states if key!=(-1,0)}
            old_current = owned(evidence.output.parent/'annular-candidate-energy-current-attempt01'/(name+'-endpoint-wide-currents.npz'))
            old_ward = owned(evidence.output.parent/'annular-candidate-Ward-source-attempt01'/(name+'-order12-Ward.npz'))
            steps = old_current['steps']
            targets = np.r_[owner.model.radii[0]-.1,old_ward['targets'],owner.model.radii[-1]+.1]
            tangent = MetricTangent(probes,steps)
            system = full_system(action,tangent,deadline,lambda stage:progress(name+'-'+stage))
            evidence.check(name+'_all_components',system['matrix'].shape==(16425,16425))
            evidence.check(name+'_positive_full_Hessian',system['inverse'].minimum_field_cholesky_pivot>0
                and system['inverse'].minimum_schur_eigenvalue>0)
            momentum_error = float(np.max(abs(system['momentum']-system['action_momentum'])))
            evidence.check(name+'_independently_assembled_momentum',momentum_error<2e-14,momentum_error)
            residual = system['matrix'] @ system['acceleration'].reshape(2,-1).T-system['forcing'].reshape(2,-1).T
            inverse_error = float(np.max(abs(residual))/max(float(np.max(abs(system['forcing']))),1e-30))
            evidence.check(name+'_Hessian_inverse_residual',inverse_error<2e-10,inverse_error)
            rate_probes = np.array([[states[index,sign]['rates'] for sign in [-1,1]] for index in range(3)])
            unused,archived_acceleration = richardson(rate_probes,steps)
            momentum_probes = np.array([[states[index,sign]['computed_momentum'] for sign in [-1,1]] for index in range(3)])
            unused,momentum_tangent = richardson(momentum_probes,steps)
            inertia_tangent = (system['matrix'] @ archived_acceleration.reshape(2,-1).T).T.reshape(archived_acceleration.shape)
            euler = system['forcing']-inertia_tangent
            chain_error = float(np.max(abs(system['convection']+inertia_tangent-momentum_tangent)))
            scientific(name,'archived_momentum_chain_rule',chain_error,2e-10)
            matrix_path = evidence.output/(name+'-Hessian.npz')
            save_npz(matrix_path,system['matrix'])
            evidence.own(matrix_path,'outputs')
            system_path = evidence.output/(name+'-system.npz')
            np.savez_compressed(system_path,targets=targets,steps=steps,force=system['force'],convection=system['convection'],
                forcing=system['forcing'],acceleration=system['acceleration'],archived_acceleration=archived_acceleration,
                archived_momentum_tangent=momentum_tangent,euler=euler,dust_block=system['dust_block'],
                momentum=system['momentum'],rates=loads.rates)
            evidence.own(system_path,'outputs')
            accelerations = np.concatenate([system['acceleration'],archived_acceleration])
            estimates = []
            for order in [8,12]:
                progress(name+'-localized-order'+str(order))
                result = localized(action,loads,tangent,targets,accelerations,order,deadline,
                    lambda stage:progress(name+'-'+stage))
                indices = np.array([int(np.flatnonzero(old_current['radius']==target)[0]) for target in old_ward['targets']])
                old_energy_current = old_current['conditional_residual'][indices]-old_current['mass_rate'][-1,indices]
                old_energy_current /= old_ward['conversion']
                ward = old_ward['sum_total']
                predicted_ward = result['current'][:,1:-1]-old_energy_current+result['projection'][:,1:-1]
                ward_error = float(np.max(abs(predicted_ward-ward)))
                ward_tolerance = 2e-11+.05*float(np.max(abs(ward)))
                scientific(name+'-order'+str(order),'independent_Ward_vs_Legendre',ward_error,ward_tolerance)
                endpoint_error = float(np.max(abs(result['current'][:,[0,-1]])))
                scientific(name+'-order'+str(order),'empty_and_whole_domain_current',endpoint_error,2e-11)
                corrected_mass = old_ward['observed']+old_ward['conversion']*(result['current'][-1,1:-1]-old_energy_current)
                projected_mass = old_ward['observed']+old_ward['conversion']*predicted_ward[-1]
                no_cut_current = result['current']-result['sum_wave_advection']-result['gram_advection']
                no_dust_inertia = result['current']+result['sum_inertia_dust'][:2]
                evidence.check(name+'-order'+str(order)+'_finite',all(np.all(np.isfinite(value)) for value in result.values()))
                path = evidence.output/(name+'-order'+str(order)+'-localized.npz')
                np.savez_compressed(path,**result,old_energy_current=old_energy_current,ward=ward,
                    predicted_ward=predicted_ward,old_mass_residual=old_ward['observed'],conversion=old_ward['conversion'],
                    corrected_mass=corrected_mass,projected_mass=projected_mass,
                    no_cut_current=no_cut_current,no_dust_inertia_current=no_dust_inertia)
                evidence.own(path,'outputs')
                summary = dict(branch=branch,extension=extension,order=order,labels=len(result['labels']),
                    maximum_Ward_error=ward_error,maximum_Ward_source=float(np.max(abs(ward))),
                    maximum_current_difference=float(np.max(abs(result['current'][-1,1:-1]-old_energy_current))),
                    maximum_EL_projection=float(np.max(abs(result['projection'][-1,1:-1]))),
                    old_mass_residual_max=float(np.max(abs(old_ward['observed']))),
                    new_mass_residual_max=float(np.max(abs(corrected_mass))),
                    with_EL_mass_residual_max=float(np.max(abs(projected_mass))),
                    whole_current=endpoint_error,momentum_chain_error=chain_error,inverse_residual=inverse_error,
                    field_pivot=system['inverse'].minimum_field_cholesky_pivot,
                    source_schur_eigenvalue=system['inverse'].minimum_schur_eigenvalue,
                    source_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
                evidence.report['summaries'].append(summary)
                evidence.report['cases'].append(summary)
                estimates.append(result['current'])
                progress(name+'-order'+str(order)+'-complete')
                print(json.dumps(summary),flush=True)
            scientific(name,'local_quadrature_8_12',float(np.max(abs(estimates[1]-estimates[0]))),2e-11)
        evidence.report.update(seconds=perf_counter()-started,
            numerical_comparisons_passed=all(row['passed'] for row in evidence.report['scientific_checks']))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],
            comparisons_passed=evidence.report['numerical_comparisons_passed'])),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
