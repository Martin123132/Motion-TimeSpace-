from stage165_common import *
from reconcile_reference import cardinal_weights
from assemble_repair import decimal_array


class StablePhaseSources:
    def __init__(self):
        self.data=read_npz(ROOT/'results/sources-refined/source.npz')
        self.references=read_npz(ROOT/'results/reference-refined/reference.npz')
        self.inputs=[ROOT/'results/sources-refined/source.npz',ROOT/'results/reference-refined/reference.npz']
        self.low={}
        self.full={}
        self.indices=[0,1,2,97]
        with localcontext() as context:
            context.prec=80
            for endpoint in ENDPOINTS:
                moments={}
                for order in [4,5,6]:
                    path=ROOT/'results/sources-refined'/f'{endpoint}-order{order}-moments.json'
                    packet=json.loads(path.read_text())
                    moments[order]=np.array([Decimal(value) for value in packet['values']],dtype=object).reshape(packet['shape']).sum(axis=(0,1))
                    self.inputs.append(path)
                    path=ROOT/'results/sources-refined'/f'{endpoint}-source{order}-exact.json'
                    packet=json.loads(path.read_text())
                    self.full[(endpoint,order)]=np.array([Decimal(value) for value in packet['full']],dtype=object).reshape(4,4)
                    self.inputs.append(path)
                for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                    self.low[(endpoint,step)]=moments[high]-moments[low]
        assert np.count_nonzero(self.data['temperature'][2:])==0

    def combine(self,weights,arrays,low_arrays):
        result=stable_sum(weights[:,None,None]*arrays)
        with localcontext() as context:
            context.prec=80
            exact=sum(Decimal.from_float(float(weight))*values for weight,values in zip(weights,low_arrays))
        result[self.indices]=np.asarray(exact,dtype=float)
        return result,exact

    def physical(self,phase,route,window,step,only=None):
        weights=cardinal_weights(phase,route)
        factors=[weights[4],0.] if window=='earlier' else [weights[0],weights[4]]
        if only is not None:
            factors=[factor if endpoint==only else 0. for endpoint,factor in zip(ENDPOINTS,factors)]
        arrays=np.stack([self.data[f'soft_{endpoint}_total{step}'] for endpoint in ENDPOINTS])
        lower=np.stack([self.low[(endpoint,step)] for endpoint in ENDPOINTS])
        return self.combine(np.asarray(factors),arrays,lower)

    def complete(self,phase,route,window,order):
        arrays=self.references[window+'_anchors'].copy()
        lower=decimal_array(arrays[:,self.indices])
        if order:
            for endpoint,index in ([('start',4)] if window=='earlier' else [('start',0),('end',4)]):
                arrays[index]=self.data[f'soft_{endpoint}_source{order}']
                lower[index]=self.full[(endpoint,order)]
        return self.combine(cardinal_weights(phase,route),arrays,lower)

    def precision(self,values,exact):
        scale=np.maximum(abs(values[0]),1e-300)
        pair=float(max(abs(values[0]+values[-1])/scale))
        moment=float(max(abs(self.data['temperature']@values[1:-1]-values[0])/scale))
        with localcontext() as context:
            context.prec=80
            temperature=decimal_array(self.data['temperature'][:2])
            exact_pair=max(float(abs(exact[0,column]+exact[-1,column])/max(abs(exact[0,column]),Decimal('1e-300'))) for column in range(4))
            exact_moment=max(float(abs(temperature@exact[1:3,column]-exact[0,column])/max(abs(exact[0,column]),Decimal('1e-300'))) for column in range(4))
        return dict(pair=pair,moment=moment,exact_pair=exact_pair,exact_moment=exact_moment)


def main():
    modest()
    folder=ROOT/'results/reference-stable'
    folder.mkdir(parents=True,exist_ok=False)
    previous=verify_packet(ROOT/'results/reference-refined')
    source=verify_packet(ROOT/'results/sources-refined')
    evaluator=StablePhaseSources()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    checks=[dict(row) for row in previous['checks'] if not row['name'].startswith('Unchanged phase gate:')]
    records={}
    for window in ['earlier','terminal']:
        for route in ['local','cubic']:
            maxima={}
            for phase in np.linspace(0,1,2049):
                for label,order in [('old',None),('repaired4',4),('repaired6',6)]:
                    values,exact=evaluator.complete(phase,route,window,order)
                    metrics=evaluator.precision(values,exact)
                    metrics['rewrite']=coordinates.source(values)[3]['relative_change']
                    for name,value in metrics.items():
                        maxima[label+'_'+name]=max(maxima.get(label+'_'+name,0.),value)
                for step in ['54','65','64']:
                    values,exact=evaluator.physical(phase,route,window,step)
                    metrics=evaluator.precision(values,exact)
                    metrics['rewrite']=coordinates.source(values)[3]['relative_change']
                    for name,value in metrics.items():
                        maxima[step+'_'+name]=max(maxima.get(step+'_'+name,0.),value)
            for quantity,value in maxima.items():
                test(checks,'Stable phase gate:'+window+':'+route+':'+quantity,value,1e-10)
            records[window+'-'+route]=maxima
    allowed=source['all_checks_passed'] and all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,phase_records=records,phases_per_route=2049,reference_replay_qualified=allowed,
        interpolation_weights_changed=False,energy_projection_used=False,temperature_curve_changed=False,
        original_failed_checks=[row for row in previous['checks'] if not row['passed']],
        exact_and_rounded_gates_both_required=True,source_reconciliation_completed=True,saved_history_replayed=False),__file__,
        [ROOT/'STABLE-PHASE-DERIVATION.md',ROOT/'results/reference-refined/status.json',ROOT/'results/sources-refined/status.json',*evaluator.inputs,*ladder.inputs])
    print(json.dumps(dict(qualified=allowed,checks=len(checks),failed=[row for row in checks if not row['passed']],phase_records=records)),flush=True)


if __name__=='__main__':
    main()
