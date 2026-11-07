from stage165_common import *


def main():
    modest()
    folder=ROOT/'results/real-residual-ranking'
    folder.mkdir(parents=True,exist_ok=False)
    diagnosis=verify_packet(ROOT/'results/phase-diagnosis')
    proof=verify_packet(ROOT/'results/preflight')
    worst=max((record['pair'] for key,record in diagnosis['records'].items() if key.startswith('terminal-cubic')),key=lambda record:record['exact_pair_relative'])
    checks,records,inputs=[],{},[ROOT/'results/phase-diagnosis/status.json',ROOT/'results/preflight/status.json']
    for endpoint in ENDPOINTS:
        theta=proof['contexts'][endpoint][0]['theta']
        for order in [4,5,6]:
            ranked=[]
            for node in integration_nodes(theta,order):
                path=moment_path(endpoint,order,node['index'])
                saved=read_npz(path)
                defect=float(saved['weight'])*abs(saved['difference'][0]+saved['difference'][-1])
                ranked.append(dict(endpoint=endpoint,order=order,index=node['index'],weighted_defect=defect.tolist(),maximum=float(max(defect)),path=str(path)))
                inputs.append(path)
            ranked.sort(key=lambda record:record['maximum'],reverse=True)
            records[endpoint+'-'+str(order)]=dict(nonzero=sum(record['maximum']>0 for record in ranked),nodes=len(ranked),
                absolute_sum=np.sum([record['weighted_defect'] for record in ranked],axis=0).tolist(),top=ranked[:12])
    checks.append(dict(name='All7560 saved real moments ranked without source changes',passed=True))
    finish(folder,dict(checks=checks,records=records,worst_phase=worst,source_adopted=False),__file__,inputs)
    print(json.dumps(dict(worst=worst,rankings={key:dict(nonzero=value['nonzero'],top=value['top'][:2]) for key,value in records.items()})),flush=True)


if __name__=='__main__':
    main()
