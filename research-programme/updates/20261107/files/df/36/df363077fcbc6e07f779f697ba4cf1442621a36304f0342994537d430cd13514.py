from stage165_common import *
from precise_soft_shifts import PreciseSoftShifts


def main():
    modest()
    folder=ROOT/'results/precise-shift-probe'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    ranking=verify_packet(ROOT/'results/real-residual-ranking')
    checks,records,inputs=[],{},[ROOT/'results/preflight/status.json',ROOT/'results/real-residual-ranking/status.json']
    for endpoint in ENDPOINTS:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        inputs.extend(bundle.inputs)
        candidates=[case for key,record in ranking['records'].items() if key.startswith(endpoint+'-') for case in record['top']]
        candidates.sort(key=lambda case:case['maximum'],reverse=True)
        for case in candidates[:1]:
            old=read_npz(case['path'])
            node=json.loads(str(old['identity']))
            parameters,weight=parameters_and_weight(proof['contexts'][endpoint][0]['theta'],node)
            results=[]
            before=time.monotonic()
            for digits in [50,80]:
                model=PreciseSoftShifts(bundle,digits)
                result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
                results.append(result['total'])
                test(checks,f'Independent precise shifts:{endpoint}:{digits}',model.maximum_precise_pair,1e-10)
                test(checks,f'Same unit directions to rounding:{endpoint}:{digits}',model.maximum_direction_repair,1e-14)
            tag=f'{endpoint}-order{case["order"]}-node{case["index"]}'
            close(checks,'50/80digit soft shift agreement:'+tag,results[0],results[1],1e-10)
            close(checks,'Unchanged real-source equivalence:'+tag,results[1],old['difference'],1e-10)
            pair=float(max(abs(results[1][0]+results[1][-1])/np.maximum(abs(results[1][0]),1e-300)))
            test(checks,'Independent repaired real pair:'+tag,pair,1e-10)
            np.savez_compressed(folder/(tag+'.npz'),old=old['difference'],new=results[1],low=results[0],identity=old['identity'],weight=weight)
            records[tag]=dict(case=case,pair=pair,seconds=time.monotonic()-before,source_adopted=False)
            inputs.append(Path(case['path']))
            print(json.dumps(dict(case=tag,record=records[tag])),flush=True)
    finish(folder,dict(checks=checks,records=records,source_adopted=False),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
