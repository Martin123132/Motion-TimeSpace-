from stage165_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    proof=verify_packet(PARENT/'results/preflight')
    state_gold=verify_packet(PARENT/'results/state-roundoff-probe')
    real_gold=verify_packet(PARENT/'results/remaining-real-probe')
    assert state_gold['all_checks_passed'] and real_gold['all_checks_passed']
    checks,records=[],{}
    inputs=[PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']]
    for endpoint in ENDPOINTS:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        real_model,state_model=PreciseBornCorrelated(bundle),StableMoments(bundle)
        inputs.extend(bundle.inputs)
        theta=proof['contexts'][endpoint][0]['theta']
        tags=[tag for tag in state_gold['records'] if tag.startswith(endpoint+'-')]
        for tag in tags:
            gold_path=PARENT/'results/state-roundoff-probe'/(tag+'.npz')
            gold=read_npz(gold_path)
            order=int(tag.split('-order')[1].split('-node')[0])
            node=json.loads(str(gold['identity']))
            before=time.monotonic()
            values=repaired_event(endpoint,order,node,theta,real_model,state_model)
            close(checks,'Repeated80digit state probe:'+tag,values['state'],gold['new'],1e-13)
            close(checks,'Repeated accurate Born real probe:'+tag,values['difference'],gold['new_real'],1e-13)
            test(checks,'Independent80digit virtual energy:'+tag,float(values['virtual_pair_exact']),1e-10)
            test(checks,'Independent80digit state energy:'+tag,float(values['state_pair_exact']),1e-10)
            for component,change in json.loads(str(values['equivalence'])).items():
                test(checks,'Unchanged source equivalence:'+tag+':'+component,change,1e-10)
            path=moment_path(endpoint,order,node['index'])
            path.parent.mkdir(parents=True,exist_ok=True)
            np.savez(path,**values,seconds=time.monotonic()-before)
            inputs.extend([gold_path,Path(str(values['parent_path'])),Path(str(values['raw_path'])),Path(str(values['loop_path']))])
            records[tag]=dict(path=str(path),seconds=time.monotonic()-before)
            print(json.dumps(dict(probe=tag,seconds=records[tag]['seconds'])),flush=True)
    hashes=authenticate(inputs,chain)
    finish(folder,dict(checks=checks,contexts=proof['contexts'],prior_hashes=hashes,records=records,expected_events=7560,
        temperature_curve_changed=False,expensive_virtual_coefficients_reused=True),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
