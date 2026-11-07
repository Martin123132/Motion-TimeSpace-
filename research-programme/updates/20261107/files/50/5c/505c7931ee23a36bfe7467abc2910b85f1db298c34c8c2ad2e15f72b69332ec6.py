from fractions import Fraction
from curvature_source_common import *


def main():
    modest()
    folder=ROOT/'results/frozen-predictions'
    assert not (ROOT/'runs').exists()
    folder.mkdir(parents=True,exist_ok=False)
    ancestors=sealed_ancestors()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    earlier=BRANCH/'history-dependent-source-20261011/results/anchor-source/source.npz'
    centre=PARENT/'results/anchor-source/source.npz'
    quarter,middle,last=[dict(np.load(path)) for path in [earlier,centre,MID/'source.npz']]
    keys=['control','sampled_leading','kinematic_remainder','difference','virtual','state','remainder']
    nodes={key:np.stack([quarter[key][:,:4],middle[key],last[key]]) for key in keys}
    assert np.array_equal(nodes['remainder'][0],middle['quarter'])
    assert np.array_equal(nodes['remainder'][1],middle['actual'])
    assert np.array_equal(nodes['remainder'][2],middle['midpoint'])
    contexts,predictions,sampled,inputs={},{},{},[earlier,centre,MID/'source.npz']
    checks=[dict(name='Stage103 payloads and three fixed source anchors unchanged',value=len(parent['file_hashes']),passed=True),
        dict(name='Both predictions precede all production',passed=True)]
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        contexts[epoch]=epoch_context(bundle)
        theta=contexts[epoch][0][0]['theta']
        assert np.array_equal(bundle.basis.mass,middle['mass'])
        inputs.extend(bundle.inputs)
        for models in contexts[epoch]:
            for model in models:
                inputs.extend(Path(path) for path in model['inputs'])
        phase=Fraction(1,4) if epoch=='early' else Fraction(3,4)
        weights=[(1-phase)*(1-2*phase),4*phase*(1-phase),phase*(2*phase-1)]
        exact=[Fraction(0),Fraction(1,2),Fraction(1)]
        assert all(sum(weight*location**degree for weight,location in zip(weights,exact))==phase**degree for degree in range(3))
        numerical=np.asarray([float(weight) for weight in weights])
        linear=np.array([.5,.5,0.]) if epoch=='early' else np.array([0.,.5,.5])
        for key in keys:
            predictions[epoch+'_'+key]=np.einsum('i,ijk->jk',numerical,nodes[key])
            predictions[epoch+'_linear_'+key]=np.einsum('i,ijk->jk',linear,nodes[key])
        check=sum(predictions[epoch+'_'+key] for key in ['kinematic_remainder','difference','virtual','state'])-predictions[epoch+'_remainder']
        norm=dual_norm(check[1:-1],middle['mass'])/np.maximum(dual_norm(predictions[epoch+'_remainder'][1:-1],middle['mass']),1e-300)
        sampled[epoch]=sampled_leading(bundle,theta)
        assert sampled[epoch].shape==(98,4) and np.isfinite(sampled[epoch]).all()
        background=thermal_wave.thermal.ThermalBackground('heavy')
        theta_reference=background.at(.375*background.end)['thermal_parameter']
        expected_theta=theta_reference*math.exp((.375-fraction)*background.end)
        checks.extend([
            dict(name='Exact quadratic reproduction through degree2:'+epoch,passed=True,weights=numerical.tolist()),
            dict(name='Combined component forecast:'+epoch,value=float(norm.max()),passed=bool(norm.max()<1e-12)),
            dict(name='Actual new temperature exponential history:'+epoch,value=theta,passed=abs(theta/expected_theta-1)<1e-14),
            dict(name='Expected actual-event counts:'+epoch,passed=all(sum(1 for node in physical_nodes(theta,part))==count for part,count in [('expensive',1008),('control',4608)]))])
    for path in dict.fromkeys(inputs):
        verify_reference(path,ancestors)
    np.savez(folder/'prediction.npz',**predictions,anchors=nodes['remainder'],
        mass=middle['mass'],temperature=middle['temperature'],chemical=middle['chemical'])
    np.savez(folder/'sampled-leading.npz',**sampled)
    finish(folder,dict(checks=checks,epoch_contexts=contexts,fractions=FRACTIONS,
        source_relative_gate=.01,response_relative_gate=.01,
        prior_chain_entries=sum(len(packet['file_hashes']) for packet in ancestors.values()),
        prediction_sha256=digest(folder/'prediction.npz'),
        formula='Three-anchor quadratic from .25,.375,.5;weights3/8,3/4,-1/8 and -1/8,3/4,3/8.',
        both_predictions_precede_production=True,new_sources_evaluated=False,
        source_interpolation_error_bounded=False,new_parent_history=False),__file__,
        [*inputs,ROOT/'DERIVATION.md',folder/'prediction.npz',folder/'sampled-leading.npz'])
    print(json.dumps(dict(checks=len(checks),failed=[row['name'] for row in checks if not row['passed']],
        temperatures={key:value[0][0]['theta'] for key,value in contexts.items()},prediction_sha256=digest(folder/'prediction.npz'))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

