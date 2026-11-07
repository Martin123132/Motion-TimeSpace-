from __future__ import annotations

import re
import psutil
from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    expected_counts={'ward':7,'volume-equation':4,'finite-amplitude':3,'fourier':35,'native-sources':15,'local-gravity':30}
    for label,expected in expected_counts.items():
        path=ROOT/'results'/label/'status.json'
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and packet['all_checks_passed']
        assert packet['count']==len(packet['checks'])==expected
        assert (path.parent/'COMPLETE').is_file()
        for entry in packet['checks']:
            checks.append(dict(entry,name=label+': '+entry['name']))
        for source,expected_hash in packet['input_hashes'].items():
            assert digest(source)==expected_hash,(label,source)
        inputs.append(path)
    check('All six completed calculation packets and their inputs match',True)
    scripts=list(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    check('All stage scripts compile without cache generation',True,script_count=len(scripts))
    allowed_pending={ROOT/'results/stage-integrity.json',folder/'status.json'}
    citations=[]
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.html')):
                target=(ROOT/reference).resolve()
                assert target in allowed_pending or target.is_file(),(path,reference)
                if target not in allowed_pending:
                    citations.append(str(target))
        inputs.append(path)
    check('Every cited local source/output path exists or is the pending seal',True,citation_count=len(set(citations)))
    data=np.load(ROOT/'results/native-sources/source-packets.npz')
    check('Native source packet has all20 configurations and4064 times',data['heavy_KG_total'].shape==(20,4064))
    check('Both nonzero cosmological masses retained',np.all(data['masses_mpc_inverse']>0))
    for field in ['heavy','slow']:
        error=float(np.max(abs(data[field+'_KG_total']-data[field+'_KG_temporal']-data[field+'_KG_spatial'])))
        scale=max(float(np.max(abs(data[field+'_KG_total']))),1e-300)
        check(field+': stored temporal/spatial split reconciles',error/scale<1e-13)
    comparison=np.load(ROOT/'results/finite-amplitude/coefficients.npz')
    check('Observed coefficient convergence is second order in probe amplitude',np.all((comparison['errors'][:-1]/comparison['errors'][1:])>3.95))
    native=json.loads((ROOT/'results/native-sources/status.json').read_text())
    check('No absent metric or ordinary-species channels silently set to zero',not native['unspecified_channels_set_to_zero'] and not native['full_nonlinear_solution'])
    local=json.loads((ROOT/'results/local-gravity/status.json').read_text())
    check('Local tests retain inherited G and distinguish Maxwell stress from charge',local['newton_G_inherited_not_derived'] and local['scalar_maxwell_stress_degeneracy_not_charge_derivation'])
    process=psutil.Process()
    check('Resource limits applied to numerical worker',process.cpu_affinity()==[2] and process.nice()==psutil.BELOW_NORMAL_PRIORITY_CLASS and all(os.environ[key]=='1' for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']))
    check('Stage has no bytecode directories',not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    assert all(entry['passed'] for entry in checks)
    inputs.extend([ROOT/'results/native-sources/source-packets.npz',ROOT/'results/finite-amplitude/coefficients.npz'])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        physics_and_numerical_checks=sum(expected_counts.values()),source_and_run_checks=len(checks)-sum(expected_counts.values()),
        local_citations=sorted(set(citations)),new_primary_source_urls=[
            'https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll6.html',
            'https://arxiv.org/abs/gr-qc/9712019'],
        numerical_history_precision_not_overstated=True,new_observational_fit=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),all_passed=True)),flush=True)


if __name__=='__main__':
    main()
