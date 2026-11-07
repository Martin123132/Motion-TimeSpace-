from stage148_terminal_common import *
from repair_saved_sources import compensated_leading
import ast


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    assert not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    parent=chain[PARENT/'results/stage-integrity.json']
    for filename,sha in parent['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    start_path=REPAIRED/'results/reaggregation/end/source.npz'
    old_path=REPAIRED/'results/repaired-readiness/source.npz'
    old=read_npz(old_path)
    start=read_npz(start_path)
    assert np.array_equal(start['remainder'],old['end'])
    inputs=[start_path,old_path]
    arrays={'start_source':start['remainder']}
    for key in COMPONENTS:
        arrays['start_'+key]=start[key]
    checks=[dict(name='Immediate parent seal and payloads intact',passed=True)]
    source_tree=ast.parse((BRANCH/'colder-half-source-prediction-test-20261016/colder_common.py').read_text())
    target_tree=ast.parse((ROOT/'stage148_terminal_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        original=next(node for node in source_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        current=next(node for node in target_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        assert ast.dump(original)==ast.dump(current),name
        checks.append(dict(name='Unchanged event physics AST:'+name,passed=True))
    contexts={}
    background=thermal_wave.thermal.ThermalBackground('heavy')
    reference_theta=background.at(.75*background.end)['thermal_parameter']
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        contexts[epoch]=epoch_context(bundle)[0]
        theta=contexts[epoch][0]['theta']
        test(checks,'Independent exponential temperature:'+epoch,
             abs(theta/(reference_theta*math.exp(-(fraction-.75)*background.end))-1),1e-14)
        assert np.array_equal(bundle.basis.mass,start['mass'])
        assert bundle.epochs[0].values.shape==(24001,4)
        phase=(fraction-.5)/.25
        quadratic_old=quadratic(old,phase)
        quartic_old=quadratic_old+bubble(phase,'cubic')*old['warm_defect']+cold_bubble(phase,'cubic')*old['cubic_defect']
        arrays[epoch+'_quadratic_extrapolation']=quadratic_old
        arrays[epoch+'_quartic_extrapolation']=quartic_old
        leading_folder=folder/epoch
        leading_folder.mkdir()
        arrays[epoch+'_sampled_leading'],metadata=compensated_leading(bundle.epochs[0],theta,leading_folder)
        write_json(leading_folder/'leading-metadata.json',metadata)
        arrays[epoch+'_raw_sampled_leading']=sampled_leading(bundle,theta)
        arrays[epoch+'_profiles']=bundle.epochs[0].values
        arrays[epoch+'_profile_frequency']=bundle.epochs[0].frequency
        arrays[epoch+'_gas']=np.asarray(bundle.gas)
        inputs.extend(bundle.inputs)
        inputs.extend([leading_folder/'leading-terms.npz',leading_folder/'leading-metadata.json'])
        for item in contexts[epoch]:
            inputs.extend(Path(path) for path in item['inputs'])
        for part,expected in [('expensive',1008),('control',4608)]:
            assert len(list(physical_nodes(theta,part)))==expected
        checks.append(dict(name='Saved history and full four-profile coverage:'+epoch,passed=True))
        print(json.dumps(dict(epoch=epoch,theta=theta,fraction=fraction)),flush=True)
    for model in ['heavy','cold']:
        for phase in ['active','transfer']:
            location=PARENT/'results/response'/f'{model}-4096'/phase
            assert verify_packet(location)['all_checks_passed']
            inputs.extend([location/'status.json',location/'response.npz'])
        for match in [20,40]:
            inputs.append(PARENT/'results/comparison'/f'{model}-m{match}-4096.npz')
    for path in set(inputs):
        if not path.is_relative_to(ROOT):
            inherited.inherited.verify_source(path,chain)
    np.savez_compressed(folder/'frozen-inputs.npz',**arrays,
                        **{key:start[key] for key in ['mass','temperature','chemical']})
    finish(folder,dict(checks=checks,epoch_contexts=contexts,fractions=FRACTIONS,
        source_interval=[.75,1.],column_order=COLUMN_NAMES,immediate_payloads=len(parent['file_hashes']),
        frozen_inputs_sha256=digest(folder/'frozen-inputs.npz'),
        predictions_precede_production=True,source_forecast_gate=.01,modes=96,steps=COUNTS),
        __file__,[*inputs,folder/'frozen-inputs.npz'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(preflight='complete',checks=len(checks))),flush=True)


if __name__=='__main__':
    main()

