import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import psutil
import run_final_real_directions as original
import run_stable_absorption_pair as stable


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'real-pair017-018-preflight.json'
EXPECTED = {
    'verify_stable_real_pair_015_016.py': 'dbcef8a03f729a7ca9ca979c411bda2ba8f0241471dbda09dcc37b96a801c712',
    'final-stable-real-batch-rays015-016/integrity.json': '914c935471b5487d19aa243422dadc4181fc1585f2daea69c90e4691b9ddf856',
    'verify_stable_real_pair_013_014.py': 'a78fbef684d0c2a95c6c72c60150c7b0f281481fde2c8144889f960330e27272',
    'final-stable-real-batch-rays013-014/integrity.json': 'f40056ed6f03f438e7313396baeddf60e87f98868f4df3f757ce54a8cc055069',
    'verify_stable_real_pair_011_012.py': '6ac92d21699c232b0dd002b0f2e1fef03b63e57ba60eaad6f0061836b8aabdfa',
    'final-stable-real-batch-rays011-012/integrity.json': '901dbfd4d65ce75fef6e95ca4bb2b6f7773ab6c0c7b720055fb4ff9116542205',
    'verify_stable_real_pair_009_010.py': '5904d186d2f66795bf0bcb401d21cdc29e400bd1f252ea074753dfcb85f70c89',
    'final-stable-real-batch-rays009-010/integrity.json': '94c4d754cddd71bae66f95082ec36073975255b8f6f1591798cd6a2e02b5c9e5',
    'verify_stable_real_pair_007_008.py': '4768393039f28a3a00b85298c2c4bf28cbc5037d4f0da42a3a6614107ea0ffa5',
    'final-stable-real-batch-rays007-008/integrity.json': '77a89afb38245a352cfc86b5ba028a3d089952d0b4dc4f56db74149b35aeadcc',
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
    from verify_stable_real_pair_015_016 import adapted_check
    prior_verification = adapted_check()
    require(prior_verification['passed'] and set(map(int,prior_verification['coverage'])) == set(range(17)), 'Prior coverage audit')
    verify({ROOT / name: value for name, value in stable.FROZEN.items()})
    verify({ROOT / name: value for name, value in original.PARENTS.items()})
    prior = ROOT / 'final-stable-real-batch-rays015-016'
    integrity = read(prior / 'integrity.json')
    require(integrity['passed'] and integrity['task_workers_remaining'] == 0, 'Prior acceptance required')
    require(read(prior / 'end.json')['completed_rays'] == [15,16], 'Wrong prior pair')
    protected = dict(read(prior / 'protocol.json')['protected'])
    protected.update({str(prior / name):digest(prior / name) for name in ('protocol.json','end.json','integrity.json')})
    for ray in (15,16):
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
    require(not (ROOT / 'final-stable-real-batch-rays017-018').exists(), 'Campaign exists: inspect instead of restarting')
    cache_protocol = ROOT / 'final-epoch-kinematic-bank/protocol.json'
    for ray in (17,18):
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
    for name in ('run_stable_real_pair_017_018.py','verify_stable_real_pair_017_018.py'):
        compile((ROOT / name).read_text(),str(ROOT / name),'exec')
        inputs[str(ROOT / name)] = digest(ROOT / name)
    record = dict(passed=True,prepared=datetime.now(timezone.utc).isoformat(),rays=[17,18],preserved_inputs=protected,
                  prior_readonly_verification=prior_verification,
                  inputs=inputs,compiled=compiled,numerical_work_started=False,original_inputs_changed=False,
                  process=dict(pid=psutil.Process().pid,created_time=psutil.Process().create_time()))
    with OUTPUT.open('x',encoding='utf-8') as stream:
        json.dump(record,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(passed=True,preserved_files=len(protected),compiled_stages=len(compiled),output=str(OUTPUT))))


if __name__ == '__main__':
    prepare()
