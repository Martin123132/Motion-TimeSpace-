from stage162_common import *


def main():
    modest()
    folder=ROOT/'results/moment-repair'
    folder.mkdir(parents=True,exist_ok=False)
    raw=verify_packet(ROOT/'results/sources')
    assert raw['state']=='complete'
    data=read_npz(ROOT/'results/sources/source.npz')
    inputs=[ROOT/'results/sources/source.npz',ROOT/'results/sources/status.json',ROOT/'results/preflight/status.json']
    proof=verify_packet(ROOT/'results/preflight')
    checks,records,arrays=[],{},{}
    with localcontext() as context:
        context.prec=60
        for endpoint in ENDPOINTS:
            theta=proof['contexts'][endpoint][0]['theta']
            exacts={}
            for order in [4,5,6]:
                exact=np.empty((7,3,4,4),dtype=object)
                exact.fill(Decimal(0))
                for node in integration_nodes(theta,order):
                    saved,weight,path,loop_path=load_node162(endpoint,order,node,theta)
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    factor=Decimal.from_float(-weight)
                    for component_index,component in enumerate(COMPONENTS):
                        for position,moment in enumerate([0,1,2,97]):
                            for column in range(4):
                                exact[panel,component_index,position,column]+=factor*Decimal.from_float(float(saved[component][moment,column]))
                    inputs.extend([path,loop_path])
                exacts[order]=exact
                write_json(folder/f'{endpoint}-order{order}-moments.json',dict(shape=list(exact.shape),moments=[0,1,2,97],
                    decimal_precision=60,values=[str(value) for value in exact.flat]))
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                exact_delta=exacts[high]-exacts[low]
                total=exact_delta.sum(axis=(0,1))
                arrays[endpoint+'_panel'+step]=np.asarray(exact_delta,dtype=float)
                arrays[endpoint+'_total'+step]=np.asarray(total,dtype=float)
                for column in range(4):
                    photon,first,second,gas=total[:,column]
                    temperature=Decimal.from_float(float(data['temperature'][0]))*first+Decimal.from_float(float(data['temperature'][1]))*second
                    scale=max(abs(photon),Decimal('1e-300'))
                    pair=float(abs(photon+gas)/scale)
                    moment=float(abs(temperature-photon)/scale)
                    records[endpoint+'-'+step+'-'+str(column)]=dict(pair=pair,moment=moment,
                        photon=str(photon),gas=str(gas),first=str(first),second=str(second))
                    test(checks,'60digit atomic photon/gas:'+endpoint+':'+step+':'+str(column),pair,1e-10)
                    test(checks,'60digit atomic moment:'+endpoint+':'+step+':'+str(column),moment,1e-10)
            print(json.dumps(dict(endpoint=endpoint,failed=[row for row in checks if not row['passed']])),flush=True)
    np.savez_compressed(folder/'moments.npz',**arrays)
    finish(folder,dict(checks=checks,records=records,precision=60,
        no_projection_used=True,raw_failures_preserved=[row for row in raw['checks'] if not row['passed']]),__file__,
        [*inputs,folder/'moments.npz'])
    print(json.dumps(dict(checks=len(checks),passed=all(row['passed'] for row in checks),records=records)),flush=True)


if __name__=='__main__':
    main()
