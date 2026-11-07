from stage163_common import *
from stable_moments import StableMoments,components


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=True)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    seal=chain[PARENT/'results/stage-integrity.json']
    paths=[PARENT/filename for filename in seal['file_hashes']]
    proof=verify_packet(PARENT/'results/preflight')
    inputs=list(paths)
    checks=[]
    records={}
    diagnosis=json.loads((PARENT/'PRECISION-DIAGNOSIS.json').read_text())
    for endpoint,fraction in ENDPOINTS.items():
        bundle=EpochBundle(fraction)
        model=StableMoments(bundle)
        theta=epoch_context(bundle)[0][0]['theta']
        assert theta==proof['contexts'][endpoint][0]['theta']
        inputs.extend(bundle.inputs)
        for case in diagnosis['top_events'][endpoint+'-65'][:2]:
            order,index=case['order'],case['index']
            node=list(integration_nodes(theta,order))[index]
            old,weight,path,loop_path=parent162.load_node162(endpoint,order,node,theta)
            parameters,unused=parameters_and_weight(theta,node)
            started=time.monotonic()
            values,energy_null=components(parameters,model,float(old['loop_scalar']))
            elapsed=time.monotonic()-started
            tag=endpoint+f'-order{order}-node{index}'
            reference=PARENT/'results/stable-jump-probe'/(tag+'.npz')
            probe=read_npz(reference)
            restored=low_rows(values['difference'],bundle.basis)
            close(checks,'Primitive/full stable probe agreement:'+tag,restored,probe['new'][[0,1,2,97]],1e-10)
            for component in COMPONENTS:
                close(checks,'Independent gas evaluator retained:'+tag+':'+component,values[component][-1],old[component][-1],1e-10)
                checks.append(dict(name='Finite primitive values:'+tag+':'+component,passed=bool(np.isfinite(values[component]).all())))
            test(checks,'Real-event absolute photon/gas:'+tag,energy_null,1e-10)
            save=moment_path(endpoint,order,index)
            save.parent.mkdir(parents=True,exist_ok=True)
            np.savez(save,**values,identity=json.dumps(node,sort_keys=True),weight=weight,
                old_path=str(path),old_sha256=digest(path),loop_path=str(loop_path),loop_sha256=digest(loop_path),
                event_energy_null=energy_null,seconds=elapsed)
            inputs.extend([path,loop_path,reference])
            records[tag]=dict(seconds=elapsed,energy_null=energy_null,path=str(save))
            print(json.dumps(dict(case=tag,seconds=elapsed,failed=[row for row in checks if not row['passed']])),flush=True)
    hashes=authenticate(inputs,chain)
    finish(folder,dict(checks=checks,contexts=proof['contexts'],prior_hashes=hashes,records=records,
        expected_events=7560,reused_virtual_coefficients=True,temperature_curve_changed=False,
        interior_orders=[6,6,6,8,7,7,6],parent_precision_failed_checks_retained=39),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
