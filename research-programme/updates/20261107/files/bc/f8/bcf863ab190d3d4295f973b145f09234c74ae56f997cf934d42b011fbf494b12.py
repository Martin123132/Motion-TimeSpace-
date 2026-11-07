from stage164_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    inputs=[PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']]
    proof=verify_packet(PARENT/'results/preflight')
    gold=verify_packet(PARENT/'results/correlated-soft-probe')
    checks,records=[],{}
    for endpoint in ENDPOINTS:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        theta=epoch_context(bundle)[0][0]['theta']
        assert theta==proof['contexts'][endpoint][0]['theta']
        model=CorrelatedSoft(bundle)
        inputs.extend(bundle.inputs)
        for tag in gold['records']:
            if not tag.startswith(endpoint+'-'):
                continue
            path=PARENT/'results/correlated-soft-probe'/(tag+'.npz')
            saved=read_npz(path)
            node=json.loads(str(saved['identity']))
            order=int(tag.split('-order')[1].split('-node')[0])
            original_path=parent163.moment_path(endpoint,order,node['index'])
            original=read_npz(original_path)
            parameters,weight=parameters_and_weight(theta,node)
            started=time.monotonic()
            result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
            close(checks,'Exact repeated correlated-soft probe:'+tag,result['total'],saved['new'],1e-13)
            test(checks,'Independent event energy exchange:'+tag,result['event_energy_null'],1e-10)
            test(checks,'Independent soft-shift energy exchange:'+tag,result['shift_energy_null'],1e-10)
            target=moment_path(endpoint,order,node['index'])
            target.parent.mkdir(parents=True,exist_ok=True)
            np.savez(target,difference=result['total'],virtual=original['virtual'],state=original['state'],
                weight=weight,identity=json.dumps(node,sort_keys=True),parent_path=str(original_path),parent_sha256=digest(original_path),
                event_energy_null=result['event_energy_null'],shift_energy_null=result['shift_energy_null'],seconds=time.monotonic()-started)
            records[tag]=dict(seconds=time.monotonic()-started,path=str(target))
            inputs.extend([path,original_path])
            print(json.dumps(dict(probe=tag,seconds=records[tag]['seconds'])),flush=True)
    hashes=authenticate(inputs,chain)
    finish(folder,dict(checks=checks,contexts=proof['contexts'],prior_hashes=hashes,records=records,
        expected_events=7560,virtual_state_reused=True,temperature_curve_changed=False),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
