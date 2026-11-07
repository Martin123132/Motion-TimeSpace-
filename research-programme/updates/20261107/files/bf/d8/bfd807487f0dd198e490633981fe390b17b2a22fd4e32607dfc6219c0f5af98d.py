from stage146_precision_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    inputs=[PARENT/'results/preflight/frozen-prediction.npz',
            PARENT/'results/preflight/prediction-lock.json',
            PARENT/'results/colder-source/source.npz',PARENT/'results/route-readiness/status.json',
            WARM/'results/preflight/frozen-prediction.npz']
    inputs.extend(spec['raw'] for spec in CASES.values())
    for path in inputs:
        inherited.inherited.verify_source(path,chain)
    checks=[dict(name='Immediate Stage145 payloads and all five raw source owners verified',passed=True),
            dict(name='Literal frozen forecasts retained unchanged,not refitted',passed=True)]
    finish(folder,dict(checks=checks,case_fractions=FRACTIONS,
        frozen_forecast_sha256=digest(inputs[0]),threshold=1e-10,
        sum_strategy='fsum plus60digit exact products for independent moment rows',
        leading_strategy='Constant test rows factored through shared scalar quadrature',
        source_projection_before_gate=False,physical_event_reevaluation=False,
        response_modes=96,response_steps=1024),__file__,inputs)
    print(json.dumps(dict(state='complete',checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
