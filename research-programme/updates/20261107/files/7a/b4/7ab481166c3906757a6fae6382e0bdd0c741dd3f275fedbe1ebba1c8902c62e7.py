import sympy as sp
from mixed_nodes import *


def main():
    modest()
    folder=ROOT/'results/mixed-proof'
    folder.mkdir(parents=True,exist_ok=False)
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SEAL
    seal=json.loads(seal_path.read_text())
    assert seal['state']=='complete' and len(seal['file_hashes'])==41453
    for name,expected in seal['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    checks=[dict(name='All41453 sealed Stage100 payloads unchanged',passed=True)]
    old_seal_path=OUTER/'results/stage-integrity.json'
    assert digest(old_seal_path)=='92f16eb08d78ec2a6f17e0242b2d00122af0ca67480ee652a1a0000ca0b65f87'
    old_seal=json.loads(old_seal_path.read_text())
    parent_config=json.loads((PARENT/'runs/expensive-r3-shard0/status.json').read_text())['configuration']
    theta=parent_config['temperature']
    old=[]
    inputs=[seal_path,old_seal_path,PARENT/'runs/expensive-r3-shard0/status.json',ROOT/'mixed_nodes.py',ROOT/'DERIVATION.md']
    for order in [3,4]:
        location=OUTER/'runs'/f's{order}-h3-g2-2-4'
        for filename in ['source.npz','status.json']:
            path=location/filename
            assert digest(path)==old_seal['file_hashes'][path.relative_to(OUTER).as_posix()]
            inputs.append(path)
        report=json.loads((location/'status.json').read_text())
        assert report['all_checks_passed']
        config=report['configuration']
        assert config['temperature']==theta and config['seed_order']==order and config['hard_order']==3
        assert (config['gas_radial'],config['gas_polar'],config['gas_azimuth'])==(2,2,4)
        assert (config['soft_angular'],config['panel_order'],config['panel_width'],config['virtual_order'])==(4,18,.5,2)
        old.append(dict(np.load(location/'source.npz')))
    fine_path=PARENT/'results/combined-source/source.npz'
    ledger_path=PARENT/'results/radial-budget/responses.npz'
    fine,ledger=dict(np.load(fine_path)),dict(np.load(ledger_path))
    for values in old:
        assert np.array_equal(values['mass'],fine['mass'])
    checks.append(dict(name='Both original frequency corners own the same temperature,basis,profiles and internal rules',passed=True))
    for component in ['difference','virtual','state']:
        expected=old[1][component]-old[0][component]
        assert expected.shape==(98,4) and np.array_equal(expected,ledger['delta-incoming-'+component])
        checks.append(dict(name='Inherited incoming difference exactly replays original seed3/4:'+component,passed=True))
    parent_nodes=list(physical_nodes(theta,4))
    from radial_nodes import physical_nodes as prior_nodes
    assert parent_nodes==list(prior_nodes(theta,'expensive'))
    current_nodes=list(physical_nodes(theta,3))
    old_keys={node_key(identity) for identity in parent_nodes}
    overlap=sum(node_key(identity) in old_keys for identity in current_nodes)
    assert len(parent_nodes)==6300 and len(current_nodes)==4725 and overlap==0
    assert [sum(node['index']%2==shard for node in current_nodes) for shard in [0,1]]==[2363,2362]
    checks.append(dict(name='Unchanged fine-grid generator and disjoint4725-point missing coarse corner',passed=True))
    full,folded=list(electron_nodes(theta,3,False)),list(electron_nodes(theta,3,True))
    assert len(full)==72 and len(folded)==45
    assert abs(sum(node['electron_weight']*node['reflection_multiplicity'] for node in folded)-1)<2e-14
    assert seal['scalar_reflection_reduction_derived'] and seal['conditional_gas_moment_identities_derived']
    checks.append(dict(name='Inherited positive gas measure and unitary scalar reflection unchanged',passed=True))
    coarse_old,fine_old,coarse_new,fine_new=sp.symbols('coarse_old fine_old coarse_new fine_new')
    expression=(fine_new-coarse_new)-(fine_old-coarse_old)-((fine_new-fine_old)-(coarse_new-coarse_old))
    assert sp.expand(expression)==0
    checks.append(dict(name='Exact four-corner composite-grid identity',passed=True))
    previous={'incoming-'+component:np.full((2,1),index+1.) for index,component in enumerate(['difference','virtual','state'])}
    previous['retained-other']=np.full((2,1),7.)
    replacement={component:np.full((2,1),index+.25) for index,component in enumerate(['difference','virtual','state'])}
    updated,mixed=replace_incoming(previous,replacement)
    assert len(updated)==4 and np.array_equal(updated['retained-other'],previous['retained-other'])
    for component in replacement:
        assert np.array_equal(updated['incoming-'+component],replacement[component])
        assert np.array_equal(mixed[component],replacement[component]-previous['incoming-'+component])
    checks.append(dict(name='Replacement keeps one contribution per incoming component,no double counting',passed=True))
    finish(folder,dict(checks=checks,temperature=theta,source_shape=[98,4],missing_coarse_points=4725,
        saved_fine_points=6300,exact_physical_node_overlap=overlap,shard_sizes=[2363,2362],
        composite_grid_change=True,fine_source_unchanged=True,actual_mixed_increment_computed=False,
        rigorous_continuum_error_bound=False),__file__,[*inputs,fine_path,ledger_path])
    print(json.dumps(dict(checks=checks,all_passed=all(row['passed'] for row in checks),temperature=theta,points=4725)),flush=True)


if __name__=='__main__':
    main()
