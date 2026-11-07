from stage164_common import *
from probe_state_roundoff import PreciseBornCorrelated


def main():
    modest()
    folder=ROOT/'results/remaining-real-probe'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    checks,records,inputs=[],{},[ROOT/'results/preflight/status.json',ROOT/'results/state-roundoff-probe/status.json']
    for endpoint in ENDPOINTS:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        model=PreciseBornCorrelated(bundle)
        inputs.extend(bundle.inputs)
        theta=proof['contexts'][endpoint][0]['theta']
        ranked=[]
        for order in [5,6]:
            for node in integration_nodes(theta,order):
                path=moment_path(endpoint,order,node['index'])
                saved=read_npz(path)
                defect=float(saved['weight'])*float(max(abs(saved['difference'][0]+saved['difference'][-1])))
                ranked.append((defect,order,node,path))
        ranked.sort(key=lambda item:item[0],reverse=True)
        for defect,order,node,path in ranked[:4]:
            parameters,weight=parameters_and_weight(theta,node)
            saved=read_npz(path)
            old=saved['difference']
            repaired=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))['total']
            old_defect=abs(old[0]+old[-1])
            new_defect=abs(repaired[0]+repaired[-1])
            tag=f'{endpoint}-order{order}-node{node["index"]}'
            close(checks,'Accurate Born real-source equivalence:'+tag,repaired,old,1e-10)
            test(checks,'Independent accurate Born real-source pair:'+tag,float(max(new_defect/np.maximum(abs(repaired[0]),1e-300))),1e-10)
            records[tag]=dict(old_weighted_defect=defect,new_weighted_defect=weight*float(max(new_defect)),
                old_defect=old_defect.tolist(),new_defect=new_defect.tolist(),
                worst_pair_relative=float(max(new_defect/np.maximum(abs(repaired[0]),1e-300))),
                improved=float(max(new_defect))<float(max(old_defect)),source_adopted=False)
            np.savez_compressed(folder/(tag+'.npz'),old=old,new=repaired,weight=weight,identity=json.dumps(node,sort_keys=True))
            inputs.append(path)
            print(json.dumps(dict(case=tag,record=records[tag])),flush=True)
    finish(folder,dict(checks=checks,records=records,probes=len(records),source_adopted=False,
        improved_events=sum(record['improved'] for record in records.values()),all_events_fixed=all(max(record['new_defect'])==0 for record in records.values())),__file__,inputs)


if __name__=='__main__':
    main()
