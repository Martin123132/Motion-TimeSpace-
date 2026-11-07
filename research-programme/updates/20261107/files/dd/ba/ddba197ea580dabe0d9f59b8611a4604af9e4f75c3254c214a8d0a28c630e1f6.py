from stage166_common import *
from stable_phase_sources import StablePhaseSources
from reconcile_reference import cardinal_weights
from assemble_repair import decimal_array


LOW_INDICES=[0,1,2,97]


def split_decimal(values):
    high=np.asarray(values,dtype=float)
    low=np.asarray(values-decimal_array(high),dtype=float)
    return high,low


class SourcePacket:
    def __init__(self,values,exact):
        self.high=values.copy()
        self.low=np.zeros_like(values)
        with localcontext() as context:
            context.prec=80
            self.high[LOW_INDICES],self.low[LOW_INDICES]=split_decimal(exact)
            self.represented=decimal_array(self.high[LOW_INDICES])+decimal_array(self.low[LOW_INDICES])
        self.exact=exact.copy()

    def select(self,selection):
        return SourcePacket(self.high[:,selection],self.exact[:,selection])


class TwofoldSources(StablePhaseSources):
    def __init__(self):
        super().__init__()
        bundle=EpochBundle(ENDPOINTS['start'])
        self.inputs.extend(bundle.inputs)
        self.factor=np.linalg.cholesky(self.data['mass'])
        self.pivot_norm=float(np.linalg.norm(linalg.solve_triangular(self.factor,np.eye(96)[:,1],lower=True)))
        self.stored_temperature=decimal_array(self.data['temperature'][:2])
        with localcontext() as context:
            context.prec=80
            self.temperature_exact=self.stored_temperature.copy()
            self.temperature_exact[0]=Decimal.from_float(float(bundle.basis.mean))*Decimal.from_float(float(bundle.basis.norms[0]))
            self.temperature_high,self.temperature_low=split_decimal(self.temperature_exact)
            self.temperature=decimal_array(self.temperature_high)+decimal_array(self.temperature_low)
            assert np.array_equal(self.temperature_high,self.data['temperature'][:2])
            self.references_low={}
            for endpoint in ENDPOINTS:
                path=PARENT/'results/sources-refined'/f'{endpoint}-source4-exact.json'
                packet=json.loads(path.read_text())
                lower=np.array([Decimal(value) for value in packet['update']],dtype=object).reshape(4,4)
                self.references_low[endpoint]=self.coordinate_low(lower)
                self.inputs.append(path)

    def coordinate_low(self,lower):
        result=lower.copy()
        result[2]=(lower[0]-self.stored_temperature[0]*lower[1])/self.stored_temperature[1]
        result[3]=-lower[0]
        return result

    def physical_packet(self,phase,route,window,step,only=None):
        values,exact=super().physical(phase,route,window,step,only)
        return SourcePacket(values,exact)

    def complete_packet(self,phase,route,window,order):
        values,exact=super().complete(phase,route,window,order)
        return SourcePacket(values,exact)

    def reference_packet(self,phase,route,window,only=None):
        weights=cardinal_weights(phase,route)
        factors=[weights[4],0.] if window=='earlier' else [weights[0],weights[4]]
        if only is not None:
            factors=[factor if endpoint==only else 0. for endpoint,factor in zip(ENDPOINTS,factors)]
        arrays=np.stack([self.references[endpoint+'_coordinate_reference'] for endpoint in ENDPOINTS])
        values=stable_sum(np.asarray(factors)[:,None,None]*arrays)
        with localcontext() as context:
            context.prec=80
            exact=sum(Decimal.from_float(float(factor))*self.references_low[endpoint] for endpoint,factor in zip(ENDPOINTS,factors))
        return SourcePacket(values,exact)

    def metrics(self,packet):
        with localcontext() as context:
            context.prec=80
            metrics={}
            for prefix,values,temperature in [('exact',packet.exact,self.temperature_exact),('represented',packet.represented,self.temperature)]:
                scale=np.maximum(abs(values[0]),Decimal('1e-300'))
                metrics[prefix+'_pair']=float(max(abs(values[0]+values[-1])/scale))
                metrics[prefix+'_moment']=float(max(abs(temperature@values[1:3]-values[0])/scale))
            scale=np.maximum(np.max(abs(packet.exact),axis=0),Decimal('1e-300'))
            metrics['encoding']=float(max(np.max(abs(packet.represented-packet.exact),axis=0)/scale))
            metrics['legacy_single_float_moment']=float(max(abs(self.stored_temperature@decimal_array(packet.high[[1,2]])-decimal_array(packet.high[0]))/np.maximum(abs(packet.exact[0]),Decimal('1e-300'))))
            mapped=self.coordinate_low(packet.represented)
            correction=np.asarray(mapped[2]-packet.represented[2],dtype=float)
            denominator=np.linalg.norm(linalg.solve_triangular(self.factor,packet.high[1:-1],lower=True),axis=0)
            metrics['coordinate_rewrite']=float(max(abs(correction)*self.pivot_norm/np.maximum(denominator,1e-300)))
        return metrics

    def add(self,first,second):
        with localcontext() as context:
            context.prec=80
            return SourcePacket(first.high+second.high,first.exact+second.exact)

    def forcing(self,phase,route,window,selection):
        maximum={}
        physical={}
        for step in ['54','65','64']:
            packet=self.physical_packet(phase,route,window,step)
            metrics=self.metrics(packet)
            for name,value in metrics.items():
                if name=='legacy_single_float_moment':
                    continue
                maximum[step+':'+name]=value
                assert value<1e-10,(phase,route,window,step,name,value)
            physical[step]=packet
        arithmetic=self.reference_packet(phase,route,window)
        arithmetic_start=self.reference_packet(phase,route,window,'start')
        arithmetic_end=self.reference_packet(phase,route,window,'end')
        zero=SourcePacket(np.zeros_like(arithmetic.high),np.zeros_like(arithmetic.exact))
        physical_start=self.physical_packet(phase,route,window,'64','start')
        physical_end=self.physical_packet(phase,route,window,'64','end')
        groups=[arithmetic_start,arithmetic,arithmetic_end,zero,physical['64'],self.add(arithmetic,physical['64']),
            physical_start,physical_end,physical['54'],physical['65'],self.add(arithmetic,physical['54']),self.add(arithmetic,physical['64'])]
        packets=[packet.select(selection) for packet in groups]
        high=np.column_stack([packet.high for packet in packets])
        low=np.column_stack([packet.low for packet in packets])
        others=np.r_[0,np.arange(2,96)]
        force_high=np.vstack([high[0],high[1:-1][others]])
        force_low=np.vstack([low[0],low[1:-1][others]])
        mapped_high,mapped_low=high[1:-1].copy(),low[1:-1].copy()
        with localcontext() as context:
            context.prec=80
            represented=np.column_stack([packet.represented for packet in packets])
            mapped=self.coordinate_low(represented)
            mapped_high[1],mapped_low[1]=split_decimal(mapped[2])
            change=np.asarray(mapped[2]-represented[2],dtype=float)
        denominator=np.linalg.norm(linalg.solve_triangular(self.factor,high[1:-1],lower=True),axis=0)
        rewrite=float(max(abs(change)*self.pivot_norm/np.maximum(denominator,1e-300)))
        assert rewrite<1e-10,(phase,rewrite)
        return dict(high=high,low=low,force_high=force_high,force_low=force_low,
            spectral_high=mapped_high,spectral_low=mapped_low,metrics=maximum,rewrite=rewrite)
