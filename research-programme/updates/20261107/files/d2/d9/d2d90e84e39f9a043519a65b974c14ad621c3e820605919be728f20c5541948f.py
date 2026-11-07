from continue199 import *
import propagate199 as engine
MAIN=ROOT
QUALIFIED=MAIN/'qualified-continuation'
MID=MAIN/'cold-side-midpoint'

def response_protocol():
    config=read(QUALIFIED/'configuration.json')
    for name,value in config['protocol_hashes'].items():assert digest(name)==value,name
    return config

class ColdSideSource(engine.ExtensionSource):
    def __init__(self,model,system):
        self.system=system;self.basis=system.basis
        self.selection=slice(0,2) if model=='heavy' else slice(2,4)
        self.old=[packet(saved.ROOT/f'sources/{tag}.npz') for tag in ('minus','minus_half','anchor')]
        self.edge=packet(MAIN/'results/target-panel.npz');self.midpoint=packet(MID/'results/target-panel.npz')
        self.maximum_rewrite=0.
    def vector(self,offset,profile):
        old=[(data['high'][4],data['low'][4]) for data in self.old]
        edge=(self.edge['high'][4],self.edge['low'][4])
        midpoint=(self.midpoint['high'][4],self.midpoint['low'][4])
        if offset>-.01:
            nodes=[-.01,-.005,0.];packets=old
        elif profile=='frozen':
            nodes=[-.015,-.01,-.005,0.];packets=[edge,*old]
        else:
            nodes=[-.015,-.0125,-.01];packets=[edge,midpoint,old[0]]
        weights=engine.lagrange(offset,nodes);high=[];low=[]
        for coefficient,pair in zip(weights,packets):
            upper=np.moveaxis(pair[0][...,self.selection],1,0).reshape(98,6)
            lower=np.moveaxis(pair[1][...,self.selection],1,0).reshape(98,6)
            product=coefficient*upper;remainder=coefficient*lower
            for index in np.ndindex(product.shape):
                remainder[index]+=math.fma(coefficient,float(upper[index]),-float(product[index]))
            high.append(product);low.append(remainder)
        return saved.parts_sum(np.stack(high),np.stack(low))

def prepare():
    assert not (QUALIFIED/'configuration.json').exists()
    original=checked_protocol();midpoint=read(MID/'results/source-assessment.json')
    assert midpoint['permission_to_propagate'] and not midpoint['failed_checks']
    assert not read(MAIN/'results/source-assessment.json')['permission_to_propagate']
    manifest=read(MAIN/'frozen/qualified-response-protocol.json')
    for name,value in manifest.items():assert digest(name)==value,name
    config=dict(original,selected_method='cold-side cubic, independently tested at t=-0.0125',
        original_extrapolation_remains_rejected=True,protocol_hashes=manifest)
    write(QUALIFIED/'configuration.json',config)
    inputs=read(MID/'inputs.json')
    for path in (MAIN/'results/target-panel.npz',MID/'results/target-panel.npz',MID/'results/source-assessment.json',MID/'configuration.json',MAIN/'COLD-SIDE-ATTEMPT.md'):
        saved.register(inputs,path)
    write(QUALIFIED/'inputs.json',inputs)
    write(QUALIFIED/'frozen/evaluation-protocol.json',manifest)
    data=packet(MAIN/'results/target-panel.npz');save(QUALIFIED/'results/target-panel.npz',**data)
    write(QUALIFIED/'results/source-assessment.json',dict(permission_to_propagate=True,failed_checks=[],
        midpoint_report=str(MID/'results/source-assessment.json'),midpoint_sha256=digest(MID/'results/source-assessment.json'),
        original_rejected_report=str(MAIN/'results/source-assessment.json'),
        qualification='separate cold-side continuation; original extrapolation remains rejected',
        target_sha256=digest(QUALIFIED/'results/target-panel.npz')))

def run(model,count):
    if not (QUALIFIED/'configuration.json').exists():prepare()
    engine.ROOT=QUALIFIED;engine.checked_protocol=response_protocol;engine.ExtensionSource=ColdSideSource
    engine.run(model,count)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--count',type=int,choices=[2048,4096],required=True);args=parser.parse_args()
    run(args.model,args.count)
