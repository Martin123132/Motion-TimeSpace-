from stage165_common import *
from stable_phase_sources import StablePhaseSources
from diagnose_phase_rounding import compensated_moment
from assemble_repair import decimal_array


class CertifiedPhaseSources(StablePhaseSources):
    def precision(self,values,exact):
        metrics=super().precision(values,exact)
        metrics['naive_dot_moment']=metrics.pop('moment')
        accurate=compensated_moment(self.data['temperature'],values)
        scale=np.maximum(abs(values[0]),1e-300)
        metrics['moment']=float(max(abs(accurate)/scale))
        with localcontext() as context:
            context.prec=80
            rounded=decimal_array(values[[0,1,2,97]])
            temperature=decimal_array(self.data['temperature'][:2])
            residual=temperature@rounded[1:3]-rounded[0]
            metrics['rounded_exact_moment']=float(max(abs(np.asarray(residual,dtype=float))/scale))
            metrics['predicate_agreement']=float(max(abs(np.asarray(residual,dtype=float)-accurate)/scale))
        return metrics


def main():
    modest()
    folder=ROOT/'results/reference-certified'
    folder.mkdir(parents=True,exist_ok=False)
    previous=verify_packet(ROOT/'results/reference-refined')
    diagnostic=verify_packet(ROOT/'results/phase-rounding-diagnosis')
    assert diagnostic['all_checks_passed'] and diagnostic['all_compensated_rounded_checks_pass']
    evaluator=CertifiedPhaseSources()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    checks=[dict(row) for row in previous['checks'] if not row['name'].startswith('Unchanged phase gate:')]
    records={}
    for window in ['earlier','terminal']:
        for route in ['local','cubic']:
            maxima={}
            for phase in np.linspace(0,1,4097):
                candidates=[(label,evaluator.complete(phase,route,window,order)) for label,order in [('old',None),('repaired4',4),('repaired6',6)]]
                candidates.extend((step,evaluator.physical(phase,route,window,step)) for step in ['54','65','64'])
                for label,(values,exact) in candidates:
                    metrics=evaluator.precision(values,exact)
                    metrics['rewrite']=coordinates.source(values)[3]['relative_change']
                    for name,value in metrics.items():
                        maxima[label+'_'+name]=max(maxima.get(label+'_'+name,0.),value)
            for quantity,value in maxima.items():
                if not quantity.endswith('_naive_dot_moment'):
                    test(checks,'Certified phase gate:'+window+':'+route+':'+quantity,value,1e-10)
            records[window+'-'+route]=maxima
            print(json.dumps(dict(window=window,route=route,failed=[row for row in checks if not row['passed']])),flush=True)
    allowed=verify_packet(ROOT/'results/sources-refined')['all_checks_passed'] and all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,phase_records=records,phases_per_route=4097,reference_replay_qualified=allowed,
        same_rounded_source_values=True,mathematical_predicate_changed=False,energy_projection_used=False,temperature_curve_changed=False,
        exact_and_rounded_gates_both_required=True,source_reconciliation_completed=True,saved_history_replayed=False,
        naive_dot_is_diagnostic_not_source_defect=True),__file__,[ROOT/'COMPENSATED-PREDICATE.md',ROOT/'results/reference-refined/status.json',
            ROOT/'results/phase-rounding-diagnosis/status.json',ROOT/'results/sources-refined/status.json',*evaluator.inputs,*ladder.inputs])
    print(json.dumps(dict(qualified=allowed,checks=len(checks),failed=[row for row in checks if not row['passed']],phase_records=records)),flush=True)


if __name__=='__main__':
    main()
