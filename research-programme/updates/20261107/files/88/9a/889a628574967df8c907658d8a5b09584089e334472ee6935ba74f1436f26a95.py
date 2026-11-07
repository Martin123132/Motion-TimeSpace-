from continue199 import *
from assess199 import predict_versions,NAMES,KINDS
from propagate199 import lagrange

def main():
    target=packet(ROOT/'results/target-panel.npz');norm=microscopic.norm_setup()
    data=[packet(saved.ROOT/f'sources/{tag}.npz') for tag in ('minus','minus_half','anchor','plus_half','plus')]
    nodes=[-.01,-.005,0.,.005,.01];checks=[];records=[];vectors={}
    for degree in (2,3,4):
        weights=lagrange(OFFSET,nodes[:degree+1])
        paired=[predict_versions(item) for item in data[:degree+1]]
        forecast=saved.parts_sum(np.stack([weight*pair[0] for weight,pair in zip(weights,paired)]),
            np.stack([weight*pair[1] for weight,pair in zip(weights,paired)]))
        error=saved.parts_sum(np.stack([forecast[0],-target['high']]),np.stack([forecast[1],-target['low']]))
        ratios=norm(error[0]+error[1])/np.maximum(norm(target['high']+target['low']),1e-300)
        gas=abs(error[0][...,-1,:]+error[1][...,-1,:])/np.maximum(abs(target['high'][...,-1,:]+target['low'][...,-1,:]),1e-300)
        records.append(dict(degree=degree,weights=weights,photon_relative=ratios.tolist(),gas_relative=gas.tolist(),
            qualification='original frozen attempt' if degree==2 else 'post-test diagnostic only; no new acceptance'))
        vectors[f'degree{degree}_high']=forecast[0];vectors[f'degree{degree}_low']=forecast[1]
        if degree==2:
            frozen=packet(ROOT/'frozen/panel-prediction.npz');prediction=predict_versions(frozen)
            residual=saved.parts_sum(np.stack([forecast[0],-prediction[0]]),np.stack([forecast[1],-prediction[1]]))
            check(checks,'quadratic frozen forecast independently reproduced',np.max(norm(residual[0]+residual[1])/np.maximum(norm(prediction[0]+prediction[1]),1e-300)),1e-10,'identity')
    absolute=norm(target['high']+target['low'])
    step=saved.parts_sum(np.stack([target['high'][1],-target['high'][2]]),np.stack([target['low'][1],-target['low'][2]]))
    relative_step=norm(step[0]+step[1])/absolute[4]
    ratios=absolute[4]/absolute[2]
    discrepancy=saved.parts_sum(np.stack([target['difference_high'][4],-step[0]]),np.stack([target['difference_low'][4],-step[1]]))
    save(ROOT/'results/post-test-shape-diagnostic.npz',**vectors)
    report=dict(checks=checks,failed_checks=[row for row in checks if not row['passed']],records=records,
        candidate_quarter_correction_relative_to_absolute=ratios.tolist(),history_half_quarter_relative_to_correction=relative_step.tolist(),
        frozen_error_to_history_step=(norm(target['difference_high'][4]+target['difference_low'][4])/np.maximum(norm(step[0]+step[1]),1e-300)).tolist(),
        original_forecast_gate_changed=False,permission_to_propagate=False,
        scope='Uses already observed target; diagnoses model-order sensitivity, cannot validate a new forecast or certify quadrature error')
    write(ROOT/'results/post-test-diagnosis.json',report)
    print(json.dumps(dict(checks=checks,summary=[dict(degree=row['degree'],baseline_photon=max(row['photon_relative'][4][0]),
        MTS_photon=max(row['photon_relative'][4][1]),baseline_gas=max(row['gas_relative'][4][0]),MTS_gas=max(row['gas_relative'][4][1])) for row in records],
        correction_relative_to_absolute=ratios.tolist(),history_step_relative=relative_step.tolist(),error_to_step=report['frozen_error_to_history_step'])),flush=True)

if __name__=='__main__':main()
