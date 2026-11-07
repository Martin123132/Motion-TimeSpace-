from stage147_step_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    if folder.exists():
        assert not any(folder.iterdir())
    else:
        folder.mkdir(parents=True)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    parent=chain[PARENT/'results/stage-integrity.json']
    for filename,sha in parent['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    readiness=verify_packet(PARENT/'results/repaired-readiness')
    assert readiness['all_checks_passed'] and readiness['allowed_routes']['cubic']
    inputs=[PARENT/'results/repaired-readiness/status.json',PARENT/'results/repaired-readiness/source.npz']
    for model in ['heavy','cold']:
        for phase in ['active','transfer']:
            location=response_folder(model,1024,phase)
            assert verify_packet(location)['all_checks_passed']
            inputs.extend([location/'status.json',location/'response.npz'])
        for match in [20,40]:
            inputs.append(PARENT/'results/spectral-readout'/f'{model}-m{match}-cubic.npz')
    inputs.append(PARENT/'results/spectral-readout/status.json')
    checks=[dict(name='Stage146 immediate payloads and inherited chain intact',passed=True),
            dict(name='Repaired cubic source and saved1024-step responses qualified',passed=True)]
    write_json(folder/'frozen-method.json',dict(counts=COUNTS,modes=96,threshold=.01,
        numerical_floor=1e-10,source_sha256=digest(inputs[1]),
        acceptance_sha256=digest(ROOT/'ACCEPTANCE.md'),derivation_sha256=digest(ROOT/'DERIVATION.md'),
        baseline_scope='Saved nonzero baseline reused and analysed identically; no baseline inner-history refinement.'))
    finish(folder,dict(checks=checks,immediate_parent_payloads=len(parent['file_hashes']),
        new_event_evaluations=0,new_virtual_loops=0,counts=COUNTS,modes=96),__file__,[*inputs,folder/'frozen-method.json'])
    print(json.dumps(dict(preflight='complete',checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
