from continue199 import *
from decimal import Decimal,localcontext

def lagrange(offset,nodes):
    return [math.prod((offset-other)/(node-other) for other in nodes if other!=node) for node in nodes]

class ExtensionSource:
    def __init__(self,model,system):
        self.system=system;self.basis=system.basis
        self.selection=slice(0,2) if model=='heavy' else slice(2,4)
        self.old=[packet(saved.ROOT/f'sources/{tag}.npz') for tag in ('minus','minus_half','anchor')]
        self.target=packet(ROOT/'results/target-panel.npz')
        self.maximum_rewrite=0.
    def vector(self,offset,profile):
        if profile=='frozen':
            nodes=[-.01,-.005,0.];packets=[(data['high'][4],data['low'][4]) for data in self.old]
        else:
            nodes=[OFFSET,-.01,-.005]
            packets=[(self.target['high'][4],self.target['low'][4]),*[(data['high'][4],data['low'][4]) for data in self.old[:2]]]
        weights=lagrange(offset,nodes)
        high=[];low=[]
        for coefficient,pair in zip(weights,packets):
            upper=np.moveaxis(pair[0][...,self.selection],1,0).reshape(98,6)
            lower=np.moveaxis(pair[1][...,self.selection],1,0).reshape(98,6)
            product=coefficient*upper
            remainder=coefficient*lower
            for index in np.ndindex(product.shape):
                remainder[index]+=math.fma(coefficient,float(upper[index]),-float(product[index]))
            high.append(product);low.append(remainder)
        return saved.parts_sum(np.stack(high),np.stack(low))
    def at(self,fraction):
        offset=(.875-fraction)*checked_protocol()['expansion_span']
        pairs=[self.vector(offset,profile) for profile in ('frozen','tested_interpolant')]
        upper=np.column_stack([pair[0] for pair in pairs]);lower=np.column_stack([pair[1] for pair in pairs])
        original=np.column_stack([upper,lower]);spectral=original[1:-1].copy()
        for column in range(12):
            with localcontext() as context:
                context.prec=80
                values=[Decimal.from_float(float(upper[row,column]))+Decimal.from_float(float(lower[row,column])) for row in (0,1)]
                result=(values[0]-Decimal.from_float(float(self.basis.temperature[0]))*values[1])/Decimal.from_float(float(self.basis.temperature[1]))
                high=float(result);low=float(result-Decimal.from_float(high))
                spectral[1,column]=high;spectral[1,column+12]=low
        others=self.system.coordinates.others
        force=np.vstack([original[0],original[1:-1][others]])
        return dict(original=original,force=force,spectral=spectral)

def run(model,count):
    config=checked_protocol();qualification=read(ROOT/'results/source-assessment.json')
    for name,value in read(ROOT/'frozen/evaluation-protocol.json').items():
        assert digest(ROOT/name)==value,name
    assert qualification['permission_to_propagate'] and not qualification['failed_checks']
    assert digest(ROOT/'results/target-panel.npz')==qualification['target_sha256']
    inputs=read(ROOT/'inputs.json');system=match.System(model,count,inputs)
    source=ExtensionSource(model,system);folder=ROOT/'responses'/f'{model}-{count}'
    if (folder/'status.json').exists():return
    stop=math.floor((config['target_fraction']-.75)*count/.25)
    stop-=stop%(count//2048)
    parent_folder=PARENT/'runs-matched'/f'{model}-{count}'
    interface=packet(parent_folder/f'interfaces/step-{system.stop}.npz')
    selected=np.r_[24:30,98:104]
    seed=interface['current'][:,selected];prior=interface['previous'][:,selected]
    high=seed[:,:6];low=seed[:,6:]
    current=np.column_stack([high,high,np.zeros_like(high),np.zeros_like(high),low,low,np.zeros_like(low),np.zeros_like(low)])
    old_high=prior[:,:6];old_low=prior[:,6:]
    older=np.column_stack([old_high,old_high,np.zeros_like(high),np.zeros_like(high),old_low,old_low,np.zeros_like(low),np.zeros_like(low)])
    ledger_max=0.;number_max=0.;began=time.monotonic()
    for index in range(system.stop+1,count+1):
        step=system.make_step(index);supplied=None
        if index<=stop:
            value=source.at(step['fraction'])
            supplied={name:np.column_stack([array[:,:12],array[:,:12],array[:,12:],array[:,12:]]) for name,array in value.items()}
        updated,unused=system.advance(current,older,step,supplied)
        joined=match.collapsed(updated);photon=system.coordinates.transform@joined[:96]
        energy=joined[0]+system.background.chi*joined[96]+joined[97]-joined[99]
        scale=abs(joined[0])+abs(system.background.chi*joined[96])+abs(joined[97])+abs(joined[99])
        ledger_max=max(ledger_max,float(np.max(abs(energy)/np.maximum(scale,1e-300))))
        number=system.basis.number@photon
        number_max=max(number_max,float(np.max(abs(number-joined[98])/np.maximum(abs(number)+abs(joined[98]),1e-300))))
        older,current=current,updated
        if index==stop:
            save(folder/'exit.npz',current=current,previous=older,index=index,fraction=step['fraction'])
    primary=match.collapsed(current)
    homogeneous=match.collapsed(packet(parent_folder/f'transfer/step-{count}.npz')['current'][:,:148][:,selected])
    checks=[]
    for profile in range(2):
        merged=primary[:,profile*6:(profile+1)*6]
        increment=primary[:,12+profile*6:18+profile*6]
        match.compare(checks,f'profile{profile}:saved boundary plus added source',merged,homogeneous+increment,1e-8)
    check(checks,'energy ledger',ledger_max,1e-7)
    check(checks,'number ledger',number_max,1e-7)
    reader=saved.response.ShapeReadout(system.basis,canonical=True)
    split=reader.apply(system.coordinates.transform@primary[:96],primary[0])
    save(folder/'terminal.npz',current=current,previous=older,**split,gas=primary[96],energy=primary[0],work=primary[97],
        frequency=reader.frequency,measure=reader.measure,heat=system.background.chi)
    reference=split['residual'][:,12:18];alternate=split['residual'][:,18:24]
    errors=saved.response.norm(reference-alternate,reader.measure)/np.maximum(saved.response.norm(reference,reader.measure),1e-300)
    for column,error in enumerate(errors):check(checks,f'{column}:source representation',error,.01)
    write(folder/'status.json',dict(checks=checks,failed_checks=[row for row in checks if not row['passed']],
        metrics=saved.response.metrics(split,system.background.chi,reader.measure).tolist(),
        interval=[.75+system.stop*.25/count,.75+stop*.25/count],seconds=time.monotonic()-began,
        output_hashes={path.name:digest(path) for path in folder.glob('*.npz')}))
    write(ROOT/'inputs.json',{name:value for name,value in inputs.items() if not Path(name).is_relative_to(ROOT)})
    print(json.dumps(dict(model=model,count=count,failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-began)),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model',choices=['heavy','cold'],required=True);parser.add_argument('--count',type=int,choices=[2048,4096],required=True)
    args=parser.parse_args();run(args.model,args.count)
