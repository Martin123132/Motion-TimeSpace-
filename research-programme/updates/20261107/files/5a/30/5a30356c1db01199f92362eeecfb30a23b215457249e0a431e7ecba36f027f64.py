from response_cold199 import *

def main():
    inputs={};system=match.System('heavy',2048,inputs);source=ColdSideSource.__new__(ColdSideSource)
    source.system=system;source.basis=system.basis;source.selection=slice(0,2)
    source.maximum_rewrite=0.;rows=[]
    seed=np.linspace(.001,.002,96)[:,None]*np.arange(1,5)[None,:]
    seed[5:]*=1e-4
    vector=np.vstack([system.basis.temperature@seed,seed,-system.basis.temperature@seed])
    def value(offset):return (1+offset+2*offset**2+3*offset**3)*vector
    def old(offset):
        high=np.zeros((6,3,98,4));high[4]=np.stack([value(offset)*factor for factor in (1.,.01,1.01)])
        return dict(high=high,low=np.zeros_like(high))
    source.old=[old(offset) for offset in (-.01,-.005,0.)]
    source.edge=old(-.015);source.midpoint=old(-.0125)
    for offset in (-.015,-.0135,-.0125,-.01):
        high,low=source.vector(offset,'frozen')
        expected=np.moveaxis(old(offset)['high'][4,...,:2],1,0).reshape(98,6)
        check(rows,f'cubic polynomial exactness {offset}',np.max(abs(high+low-expected))/np.max(abs(expected)),1e-10)
    step=system.make_step(system.stop+1)
    supplied=source.at(step['fraction']);state=np.zeros((100,24))
    advanced,diagnostic=system.advance(state,state,step,supplied,diagnostics=True)
    for name,tolerance in [('photon',1e-7),('gas',1e-8),('spectral',1.)]:
        check(rows,'synthetic one-step '+name,diagnostic[name],tolerance)
    collapsed=match.collapsed(advanced)
    balance=collapsed[0]+system.background.chi*collapsed[96]+collapsed[97]-collapsed[99]
    scale=abs(collapsed[0])+abs(system.background.chi*collapsed[96])+abs(collapsed[97])+abs(collapsed[99])
    check(rows,'synthetic energy ledger',np.max(abs(balance)/np.maximum(scale,1e-300)),1e-7)
    check(rows,'six physics/join columns plus both profiles',int(advanced.shape!=(100,24)),0)
    report=dict(synthetic=True,physical_source_qualification=False,checks=rows,failed_checks=[row for row in rows if not row['passed']])
    write(MAIN/'results/response-wiring-test.json',report)
    print(json.dumps(report),flush=True)

if __name__=='__main__':main()
