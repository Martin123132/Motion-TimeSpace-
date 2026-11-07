from response_cold199 import *
DESTINATION=QUALIFIED/'endpoint-matched'
ORIGINAL_ADVANCE=match.System.advance

def corrected_advance(self,current,older,step,source=None,diagnostics=False):
    config=response_protocol()
    cutoff=math.floor((config['target_fraction']-.75)*self.count/.25)
    cutoff-=cutoff%(self.count//2048)
    if step['index']==cutoff:
        assert source is not None
        self.endpoint_source={name:value.copy() for name,value in source.items()}
        self.endpoint_rate=step['rate']
    if step['index']==cutoff+1:
        assert source is None and hasattr(self,'endpoint_source')
        coefficient=-.5*self.endpoint_rate/step['rate']
        source={name:coefficient*value for name,value in self.endpoint_source.items()}
    return ORIGINAL_ADVANCE(self,current,older,step,source,diagnostics)

def prepare():
    if (DESTINATION/'results/source-assessment.json').exists():return
    qualification=read(QUALIFIED/'results/source-assessment.json')
    assert qualification['permission_to_propagate']
    save(DESTINATION/'results/target-panel.npz',**packet(QUALIFIED/'results/target-panel.npz'))
    qualification=dict(qualification,target_sha256=digest(DESTINATION/'results/target-panel.npz'),
        endpoint_method='one-sided BDF2 derivative-jump correction; physical source unchanged')
    write(DESTINATION/'results/source-assessment.json',qualification)
    write(DESTINATION/'inputs.json',read(QUALIFIED/'inputs.json'))
    manifest={str(MAIN/name):digest(MAIN/name) for name in ('continue199.py','propagate199.py','response_cold199.py','endpoint199.py','ENDPOINT-MATCHING.md')}
    write(DESTINATION/'frozen/evaluation-protocol.json',manifest)
    raw=read(MAIN/'results/validation.json')
    assert len(raw['failed_checks'])==48
    write(MAIN/'results/unmatched-response-validation.json',raw)
    rows=[];records=[]
    for count in (18,36):
        step=1/count;current=float(count)*step;older=(count-1)*step
        plain,plain_old=current,older;fixed,fixed_old=current,older
        for index in range(40):
            updated=(2*plain-.5*plain_old)/1.5;plain_old,plain=plain,updated
            updated=(2*fixed-.5*fixed_old+step*(-.5 if index==0 else 0.))/1.5;fixed_old,fixed=fixed,updated
        check(rows,f'{count}:uncorrected extra half-step',plain-1-.5*step,1e-14)
        check(rows,f'{count}:corrected source cutoff',fixed-1,1e-14)
        records.append(dict(count=count,uncorrected=plain,corrected=fixed,exact=1.))
    write(DESTINATION/'results/scalar-control.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],records=records))

def run(model,count):
    prepare();engine.ROOT=DESTINATION;engine.checked_protocol=response_protocol;engine.ExtensionSource=ColdSideSource
    match.System.advance=corrected_advance
    try:engine.run(model,count)
    finally:match.System.advance=ORIGINAL_ADVANCE

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--count',type=int,choices=[2048,4096],required=True);args=parser.parse_args()
    run(args.model,args.count)
