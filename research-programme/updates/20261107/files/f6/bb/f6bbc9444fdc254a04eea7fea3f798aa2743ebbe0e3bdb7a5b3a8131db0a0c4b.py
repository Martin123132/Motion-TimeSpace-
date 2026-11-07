from stage165_common import *
from reconcile_reference import cardinal_weights
from assemble_repair import decimal_array


def main():
    modest()
    folder=ROOT/'results/phase-diagnosis-refined'
    folder.mkdir(parents=True,exist_ok=False)
    reference=verify_packet(ROOT/'results/reference-refined')
    sources=read_npz(ROOT/'results/sources-refined/source.npz')
    data=read_npz(ROOT/'results/reference-refined/reference.npz')
    inputs=[ROOT/'results/reference-refined/status.json',ROOT/'results/reference-refined/reference.npz',ROOT/'results/sources-refined/source.npz']
    checks,records=[],{}
    with localcontext() as context:
        context.prec=80
        exact={}
        for endpoint in ENDPOINTS:
            for order in [4,5,6]:
                path=ROOT/'results/sources-refined'/f'{endpoint}-order{order}-moments.json'
                packet=json.loads(path.read_text())
                exact[(endpoint,order)]=np.array([Decimal(value) for value in packet['values']],dtype=object).reshape(packet['shape'])
                inputs.append(path)
        temperature=decimal_array(sources['temperature'][:2])
        for window in ['earlier','terminal']:
            for route in ['local','cubic']:
                for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                    worst_pair=(-1,None)
                    worst_moment=(-1,None)
                    for phase in np.linspace(0,1,2049):
                        weights=cardinal_weights(phase,route)
                        values=stable_sum(weights[:,None,None]*data[window+'_'+step])
                        for diagnostic,residual in [('pair',values[0]+values[-1]),('moment',sources['temperature']@values[1:-1]-values[0])]:
                            ratio=abs(residual)/np.maximum(abs(values[0]),1e-300)
                            column=int(np.argmax(ratio))
                            entry=(float(ratio[column]),dict(phase=float(phase),column=column,energy=float(values[0,column]),residual=float(residual[column])))
                            if diagnostic=='pair' and entry[0]>worst_pair[0]:
                                worst_pair=entry
                            if diagnostic=='moment' and entry[0]>worst_moment[0]:
                                worst_moment=entry
                    key=window+'-'+route+'-'+step
                    records[key]={}
                    for diagnostic,worst in [('pair',worst_pair),('moment',worst_moment)]:
                        value,record=worst
                        weights=cardinal_weights(record['phase'],route)
                        terms={}
                        for endpoint,index in ([('start',4)] if window=='earlier' else [('start',0),('end',4)]):
                            terms[endpoint]=Decimal.from_float(float(weights[index]))*(exact[(endpoint,high)]-exact[(endpoint,low)])
                        combined=sum(terms.values())
                        total=combined.sum(axis=(0,1))[:,record['column']]
                        pair=total[0]+total[-1]
                        moment=temperature[0]*total[1]+temperature[1]*total[2]-total[0]
                        record.update(float_relative=value,exact_energy=str(total[0]),exact_pair=str(pair),exact_moment=str(moment),
                            exact_pair_relative=float(abs(pair/total[0])) if total[0] else None,
                            exact_moment_relative=float(abs(moment/total[0])) if total[0] else None,
                            energy_condition=float(sum(abs(term.sum(axis=(0,1))[0,record['column']]) for term in terms.values())/abs(total[0])) if total[0] else None,
                            weights=weights.tolist())
                        contributions={}
                        for endpoint,terms_by_panel in terms.items():
                            for component_index,component in enumerate(COMPONENTS):
                                component_values=terms_by_panel[:,component_index].sum(axis=0)[:,record['column']]
                                contributions[endpoint+'-'+component]=dict(energy=str(component_values[0]),pair=str(component_values[0]+component_values[-1]),
                                    moment=str(temperature[0]*component_values[1]+temperature[1]*component_values[2]-component_values[0]))
                        record['components']=contributions
                        records[key][diagnostic]=record
                fullmax={'pair':0.,'moment':0.}
                for phase in np.linspace(0,1,2049):
                    weights=cardinal_weights(phase,route)
                    full=stable_sum(weights[:,None,None]*(data[window+'_anchors']+data[window+'_raw_reference']+data[window+'_64']))
                    fullmax['pair']=max(fullmax['pair'],float(max(abs(full[0]+full[-1])/np.maximum(abs(full[0]),1e-300))))
                    fullmax['moment']=max(fullmax['moment'],float(max(abs(sources['temperature']@full[1:-1]-full[0])/np.maximum(abs(full[0]),1e-300))))
                for diagnostic,value in fullmax.items():
                    test(checks,'Full repaired6 phase gate:'+window+':'+route+':'+diagnostic,value,1e-10)
        for diagnostic in ['pair','moment']:
            reproduced=max(record[diagnostic]['float_relative'] for key,record in records.items() if key.startswith('terminal-cubic'))
            close(checks,'Reproduce failed phase maximum:'+diagnostic,np.array([reproduced]),np.array([reference['phase_records']['terminal-cubic']['physical_'+diagnostic]]),1e-10)
    finish(folder,dict(checks=checks,records=records,precision=80,temperature_curve_changed=False,propagation_allowed=False),__file__,inputs)
    print(json.dumps(dict(checks=checks,terminal_cubic={key:value for key,value in records.items() if key.startswith('terminal-cubic')})),flush=True)


if __name__=='__main__':
    main()
