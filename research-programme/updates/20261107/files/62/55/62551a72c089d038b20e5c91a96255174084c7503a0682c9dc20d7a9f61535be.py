import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import psutil
import run_final_real_directions as original
import run_stable_absorption_pair as stable


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'real-pair007-008-preflight.json'
EXPECTED = {
    'verify_stable_real_pair_005_006.py': 'c1b2fbcdb7a12b13f16d75a31397d59f92b2affd047f6502f0aada508dc35893',
    'run_stable_absorption_pair.py': 'c8a7b53df118e23fcae5c74ab6346869a16bfec2e1125b9ac0a813a71dfd6d3a',
    'stable_absorption_panel.py': '8b0d7a28e511b266ffcec9a03cbed6ada54a062ec9941fc92c7520d44fa2728f',
    'verify_stable_real_pair_003_004.py': '249942eec79ad3828d9ab9141f621a40dc277d785f2a9a4cd4397d6398b994ef',
    'final-stable-real-batch-rays005-006/integrity.json': '105e3be8779773529a531b01c5855a77d7ae9326a4b45968e5510bb25c058214',
    'final-stable-real-batch-rays003-004/integrity.json': '00b03fbe99725a77a490fdfc2bc16f329dcdac762cf0644542e34c01163d5f75',
}
read, digest, verify = original.read, original.digest, original.verify


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def prepare():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    verify({ROOT / name: value for name, value in EXPECTED.items()})
    from verify_stable_real_pair_005_006 import adapted_check
    prior_verification = adapted_check()
    require(prior_verification['passed'] and set(map(int,prior_verification['coverage'])) == set(range(7)), 'Prior coverage audit')
    verify({ROOT / name: value for name, value in stable.FROZEN.items()})
    verify({ROOT / name: value for name, value in original.PARENTS.items()})
    prior = ROOT / 'final-stable-real-batch-rays005-006'
    integrity = read(prior / 'integrity.json')
    require(integrity['passed'] and integrity['task_workers_remaining'] == 0, 'Prior acceptance required')
    require(read(prior / 'end.json')['completed_rays'] == [5,6], 'Wrong prior pair')
    protected = dict(read(prior / 'protocol.json')['protected'])
    protected.update({str(prior / name):digest(prior / name) for name in ('protocol.json','end.json','integrity.json')})
    for ray in (5,6):
        directory = Path(integrity['coverage'][str(ray)])
        require(directory == ROOT / f'final-epoch-real-v2-ray{ray:03d}', 'Authoritative prior location')
        for name in ('protocol.json','order18-vs26.json','order18-vs26.csv'):
            protected[str(directory / name)] = digest(directory / name)
        for order in (18,26):
            for name in ('complete.json','complete.npz','independent.json'):
                protected[str(directory / f'order-{order}' / name)] = digest(directory / f'order-{order}' / name)
    verify(protected)
    inputs = {**{str(ROOT / name):value for name,value in EXPECTED.items()},str(Path(__file__)):digest(__file__)}
    compiled = []
    require(not (ROOT / 'final-stable-real-batch-rays007-008').exists(), 'Campaign exists: inspect instead of restarting')
    cache_protocol = ROOT / 'final-epoch-kinematic-bank/protocol.json'
    for ray in (7,8):
        for prefix in ('compensated-epoch-source-final450-ray','final-absorption-native-v2-ray','final-epoch-real-v2-ray'):
            require(not (ROOT / f'{prefix}{ray:03d}').exists(), 'Existing result requires review')
        cache_path = ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}.json'
        cache = read(cache_path)
        require(cache['passed'] and cache['ray'] == ray and all(row['passed'] for row in cache['checks'])
                and cache['protocol_sha256'] == digest(cache_protocol), 'Matching saved cache required')
        kernel = ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}-kernel.json'
        require(digest(kernel) == cache['kernel_sha256'], 'Cache fingerprint')
        inputs.update({str(cache_path):digest(cache_path),str(kernel):cache['kernel_sha256'],str(cache_protocol):digest(cache_protocol)})
        for stage in ('native','freeze','run','check','compare'):
            source, metadata = stable.render(stage,ray)
            compile(source, str(ROOT / metadata['original_program']['parent']), 'exec')
            compiled.append(dict(ray=ray,stage=stage,sha256=hashlib.sha256(source.encode()).hexdigest()))
        source, metadata = original.render('precise',ray)
        compile(source, str(ROOT / metadata['parent']), 'exec')
        compiled.append(dict(ray=ray,stage='precise',sha256=hashlib.sha256(source.encode()).hexdigest()))
    for name in ('run_stable_real_pair_007_008.py','verify_stable_real_pair_007_008.py'):
        compile((ROOT / name).read_text(),str(ROOT / name),'exec')
        inputs[str(ROOT / name)] = digest(ROOT / name)
    record = dict(passed=True,prepared=datetime.now(timezone.utc).isoformat(),rays=[7,8],preserved_inputs=protected,
                  prior_readonly_verification=prior_verification,
                  inputs=inputs,compiled=compiled,numerical_work_started=False,original_inputs_changed=False,
                  process=dict(pid=psutil.Process().pid,created_time=psutil.Process().create_time()))
    with OUTPUT.open('x',encoding='utf-8') as stream:
        json.dump(record,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(passed=True,preserved_files=len(protected),compiled_stages=len(compiled),output=str(OUTPUT))))


if __name__ == '__main__':
    prepare()
