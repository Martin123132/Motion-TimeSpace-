import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'final-spectrum-uncertainty-20261019'))
from stage167_common import *
import stage167_common as parent167
from twofold_sources import TwofoldSources,SourcePacket,split_decimal,LOW_INDICES
from assemble_repair import decimal_array
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'final-spectrum-uncertainty-20261019'
PARENT_SEAL='efa0ad1749b2a2687298a6ee1853644f04e8fb635e1147521332da62396e3a2f'
INHERITED_PAYLOADS=332755
STARTED=datetime(2026,10,19,16,50,41,tzinfo=timezone.utc)
DEADLINE='2026-10-19T20:10:00+00:00'
GROUPS=['old_defect','current_defect','endpoint_update','zero','raw_minus_reference','raw_defect',
    'endpoint65','incoming13','incoming38','incoming820','direct_current','zero_duplicate']


def ancestors():
    chain=parent167.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,inputs):
    paths={*ROOT.glob('*.py'),ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in inputs)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).resolve().is_relative_to(BRANCH):
            paths.add(Path(filename).resolve())
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        input_hashes={str(path):digest(path) for path in sorted(paths)},count=len(report['checks']),
        all_checks_passed=all(bool(row['passed']) for row in report['checks']))
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


class HeldoutSources(TwofoldSources):
    def __init__(self):
        super().__init__()
        self.groups={}
        self.raw_metrics={}
        self.source_records={}
        self.raw_packets={}
        for route in ['local','cubic']:
            warm=bubble(.75,route)
            predictor=np.array([-.125-.375*warm,warm,.75-.75*warm,0.,.375+.125*warm])
            weights=-predictor
            weights[3]=1.
            old=self.references['terminal_anchors'].copy()
            old_lower=decimal_array(old[:,LOW_INDICES])
            current=old.copy()
            current_lower=old_lower.copy()
            current[0]=self.data['soft_start_source6']
            current[4]=self.data['soft_end_source6']
            current_lower[0]=self.full[('start',6)]
            current_lower[4]=self.full[('end',6)]
            old_values,old_exact=self.combine(weights,old,old_lower)
            current_values,current_exact=self.combine(weights,current,current_lower)
            raw_old=SourcePacket(old_values,old_exact)
            raw_current=SourcePacket(current_values,current_exact)
            physical,physical_low=self.combine(-predictor[[0,4]],
                np.stack([self.data['soft_'+endpoint+'_total65'] for endpoint in ENDPOINTS]),
                np.stack([self.low[(endpoint,'65')] for endpoint in ENDPOINTS]))
            raw_steps=[SourcePacket(physical,physical_low)]
            for prefix in ['order8','band4','band820']:
                arrays=np.stack([self.data[prefix+'_'+site+'_total'] for site in ['cold','warm','centre']])
                values,exact=self.combine(np.array([1.,-predictor[1],-predictor[2]]),arrays,decimal_array(arrays[:,LOW_INDICES]))
                raw_steps.append(SourcePacket(values,exact))
            self.raw_packets[route]=[raw_old,raw_current,*raw_steps]
            self.raw_metrics[route]={name:self.metrics(packet) for name,packet in zip(
                ['old_defect','current_defect','endpoint65','incoming13','incoming38','incoming820'],self.raw_packets[route])}
            old_packet=self.reference_coordinates(raw_old)
            current_packet=self.reference_coordinates(raw_current)
            endpoint_change=self.subtract(current_packet,old_packet)
            raw_audit=self.independent_raw_coordinates(raw_current)
            raw_difference=self.subtract(raw_audit,current_packet)
            zero=SourcePacket(np.zeros_like(current_values),np.zeros_like(current_exact))
            self.groups[route]=[old_packet,current_packet,endpoint_change,zero,raw_difference,raw_audit,
                *[self.reference_coordinates(packet) for packet in raw_steps],current_packet,zero]
            source_norm=SourceNorm(self.data['mass'])
            self.source_records[route]=dict(predictor_weights=predictor.tolist(),
                raw_relative_miss=(source_norm(current_values)/source_norm(current[3])).tolist(),
                previous_relative_miss=(source_norm(old_values)/source_norm(old[3])).tolist(),
                cold_profile_at_nodes=[cold_bubble(phase,route) for phase in [0,.25,.5,.75,1.]])

    def subtract(self,first,second):
        with localcontext() as context:
            context.prec=80
            return SourcePacket(first.high-second.high,first.exact-second.exact)

    def reference_coordinates(self,raw):
        with localcontext() as context:
            context.prec=80
            exact=self.coordinate_low(raw.exact)
        return SourcePacket(raw.high,exact)

    def independent_raw_coordinates(self,raw):
        with localcontext() as context:
            context.prec=80
            exact=raw.exact.copy()
            exact[0]=self.stored_temperature@exact[1:3]
        return SourcePacket(raw.high,exact)

    def forcing(self,phase,route,selection,closed=False):
        factor=Decimal.from_float(float(cold_bubble(phase,route)))
        with localcontext() as context:
            context.prec=80
            groups=list(self.groups[route])
            if closed:
                groups[4]=groups[3]
                groups[5]=groups[1]
            packets=[SourcePacket(float(factor)*packet.high[:,selection],factor*packet.exact[:,selection]) for packet in groups]
            high=np.column_stack([packet.high for packet in packets])
            low=np.column_stack([packet.low for packet in packets])
            represented=np.column_stack([packet.represented for packet in packets])
            mapped=self.coordinate_low(represented)
            mapped_high,mapped_low=high[1:-1].copy(),low[1:-1].copy()
            mapped_high[1],mapped_low[1]=split_decimal(mapped[2])
            change=np.asarray(mapped[2]-represented[2],dtype=float)
        others=np.r_[0,np.arange(2,96)]
        force_high=np.vstack([high[0],high[1:-1][others]])
        force_low=np.vstack([low[0],low[1:-1][others]])
        denominator=np.linalg.norm(linalg.solve_triangular(self.factor,high[1:-1],lower=True),axis=0)
        rewrite=float(max(abs(change)*self.pivot_norm/np.maximum(denominator,1e-300)))
        assert rewrite<1e-10,(phase,route,rewrite)
        return dict(high=high,low=low,force_high=force_high,force_low=force_low,
            spectral_high=mapped_high,spectral_low=mapped_low,rewrite=rewrite)
