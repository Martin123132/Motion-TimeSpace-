from __future__ import annotations

import re
import psutil
from constraint_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    expected={'geometry':3,'constraint-propagation':6,'kinetic-operator':2,'neutrino-refined':9,'quadratic-neutrinos':5}
    for label,count in expected.items():
        path=ROOT/'results'/label/'status.json'
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and packet['all_checks_passed'] and packet['count']==count
        assert (path.parent/'COMPLETE').is_file()
        assert all(row['passed'] for row in packet['checks'])
        checks.extend(dict(row,name=label+': '+row['name']) for row in packet['checks'])
        for source,expected_hash in packet['input_hashes'].items():
            assert digest(source)==expected_hash,(label,source)
        inputs.append(path)
    original=ROOT/'results/neutrino-response/status.json'
    packet=json.loads(original.read_text())
    assert packet['state']=='complete' and not packet['all_checks_passed'] and packet['count']==18
    failures=[row for row in packet['checks'] if not row['passed']]
    assert len(failures)==2 and all('k=1.0: native density/momentum' in row['name'] for row in failures)
    checks.extend(dict(row,name='original valid scope: '+row['name']) for row in packet['checks'] if row['passed'])
    for source,expected_hash in packet['input_hashes'].items():
        assert digest(source)==expected_hash,source
    inputs.append(original)
    check('Two original high-k failures preserved and explicitly superseded',True,original_failures=failures)
    native=ROOT/'runs/native/status.json'
    packet=json.loads(native.read_text())
    assert packet['state']=='complete' and packet['all_checks_passed'] and packet['completed']==2
    for source,expected_hash in packet['input_hashes'].items():
        assert digest(source)==expected_hash,source
    inputs.append(native)
    check('Both native controls complete with unchanged input ownership',True)
    for path in sorted((ROOT/'results/quadratic-neutrinos').glob('*.npz')):
        data=np.load(path)
        stress=data['stress_source_part']
        envelope=max(float(np.max(abs(stress))),1e-10)
        tensor=stress[:,4:].reshape(-1,3,3)
        error=float(np.max(abs(np.trace(tensor,axis1=1,axis2=2)-stress[:,0])))/envelope
        check(path.stem+': massless stress trace equals energy',error<1e-10,envelope_error=error)
        parity=max(float(np.max(abs(stress[:,0].imag))),float(np.max(abs(stress[:,1:4].real))),float(np.max(abs(tensor.imag))))/envelope
        check(path.stem+': Fourier reality/parity respected',parity<1e-10,envelope_error=parity)
        check(path.stem+': saved arrays finite and121 times',np.isfinite(stress).all() and len(data['times'])==121)
        inputs.append(path)
    scripts=list(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    check('All scripts compile',True,script_count=len(scripts))
    citations=set()
    pending={ROOT/'results/stage-integrity.json',folder/'status.json'}
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.html')):
                target=(ROOT/reference).resolve()
                assert target in pending or target.is_file(),(path,reference)
                if target not in pending:
                    citations.add(str(target))
        inputs.append(path)
    check('Every cited local source exists or is the pending seal',True)
    process=psutil.Process()
    check('Single worker resource settings intact',process.cpu_affinity()==[2] and process.nice()==psutil.BELOW_NORMAL_PRIORITY_CLASS and all(os.environ[key]=='1' for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']))
    check('No bytecode cache introduced',not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    assert all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_current_acceptance_checks_passed=True,
        superseded_original_failure_count=2,all_original_raw_checks_passed=False,
        local_citations=sorted(citations),new_primary_source_urls=[
            'https://arxiv.org/abs/gr-qc/0103032','https://arxiv.org/abs/1910.12152','https://arxiv.org/abs/1104.2933'],
        full_second_order_cosmological_prediction=False,new_survey_fit=False),__file__,inputs)
    print(json.dumps(dict(accepted_checks=len(checks),original_failures_preserved=2)),flush=True)


if __name__=='__main__':
    main()
