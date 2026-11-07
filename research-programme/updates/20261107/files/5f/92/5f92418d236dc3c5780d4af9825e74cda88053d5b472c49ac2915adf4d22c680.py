from history_frequency_common import *


def main():
    modest()
    folder=ROOT/'results/frequency-preflight'
    assert not (ROOT/'runs').exists()
    folder.mkdir(parents=True,exist_ok=False)
    ancestors=sealed_ancestors()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    baseline_path=PARENT/'results/holdout-sources/source.npz'
    baseline=dict(np.load(baseline_path))
    checks=[dict(name='Stage104 payloads unchanged before new calculations',value=len(parent['file_hashes']),passed=True)]
    inputs=[baseline_path,baseline_path.parent/'status.json']
    contexts,reused={},{}
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        contexts[epoch]=epoch_context(bundle)
        theta=contexts[epoch][0][0]['theta']
        assert np.array_equal(bundle.basis.mass,baseline['mass'])
        inputs+=bundle.inputs
        for models in contexts[epoch]:
            for model in models:
                inputs.extend(Path(path) for path in model['inputs'])
        electrons={}
        for order in [3,4]:
            current={}
            for node in population_nodes(theta,order,3,radial=2,polar=2,azimuthal=4):
                current[tuple(node['velocity'])]=node['electron_weight']
            electrons[order]=current
        assert len(electrons[3])==16 and electrons[3]==electrons[4]
        control_path=PARENT/'runs'/f'control-{epoch}'/'source.npz'
        fine_path=PARENT/'runs'/f'expensive-{epoch}'/'source.npz'
        control,fine=dict(np.load(control_path)),dict(np.load(fine_path))
        assert np.array_equal(control['control'],baseline[epoch+'_control'])
        assert all(np.array_equal(fine[key],baseline[epoch+'_'+key]) for key in ['difference','virtual','state'])
        assert np.array_equal(baseline[epoch+'_control']-baseline[epoch+'_sampled_leading'],baseline[epoch+'_kinematic_remainder'])
        reconstructed=baseline[epoch+'_kinematic_remainder']+sum(fine[key] for key in ['difference','virtual','state'])
        relative=dual_norm((reconstructed-baseline[epoch+'_actual'])[1:-1],baseline['mass'])/dual_norm(baseline[epoch+'_actual'][1:-1],baseline['mass'])
        nodes=list(physical_nodes(theta,'expensive'))
        assert len(nodes)==756 and len({(node['frequency'],node['seed_weight']) for node in nodes})==21
        old_frequencies={node['frequency'] for node in population_nodes(theta,4,3,radial=2,polar=2,azimuthal=4)}
        new_frequencies={node['frequency'] for node in nodes}
        reused[epoch]=dict(control_sha256=digest(control_path),seed4_sha256=digest(fine_path),
            actual_source_norm=dual_norm(baseline[epoch+'_actual'][1:-1],baseline['mass']).tolist(),
            theta=theta,existing_seed4_nodes=1008,new_seed3_nodes=756,
            incoming_frequency_overlap=len(old_frequencies.intersection(new_frequencies)))
        checks.extend([
            dict(name='Unchanged electron measure,hard rule,and96-mode basis:'+epoch,passed=True),
            dict(name='Both saved control and seed4 D/V/S reused exactly:'+epoch,passed=True),
            dict(name='Whole-remainder reconstruction from reused components:'+epoch,value=float(relative.max()),passed=bool(relative.max()<1e-12)),
            dict(name='21 incoming points and756 positive-weight physical representatives:'+epoch,passed=all(node['seed_weight']>0 and node['electron_weight']>0 and node['hard_weight']>0 for node in nodes))])
        inputs.extend([control_path,control_path.parent/'status.json',fine_path,fine_path.parent/'status.json'])
    for path in dict.fromkeys(inputs):
        verify_reference(path,ancestors)
    rejected=False
    try:
        list(physical_nodes(contexts['early'][0][0]['theta'],'control'))
    except ValueError:
        rejected=True
    checks.append(dict(name='Production route rejects control recomputation',passed=rejected))
    finish(folder,dict(checks=checks,fractions=FRACTIONS,epoch_contexts=contexts,reused_inputs=reused,
        baseline_sha256=digest(baseline_path),prior_chain_entries=sum(len(packet['file_hashes']) for packet in ancestors.values()),
        source_component_sum_gate=.01,response_component_sum_gate=.01,all_modes_retained=96,
        scope='Only seed3 versus seed4 D/V/S at two fixed epochs;all controls and old three anchors unchanged.',
        new_parent_history=False),__file__,[*inputs,ROOT/'DERIVATION.md'])
    print(json.dumps(dict(checks=len(checks),failed=[row['name'] for row in checks if not row['passed']],
        reused_inputs=reused,baseline_sha256=digest(baseline_path))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

