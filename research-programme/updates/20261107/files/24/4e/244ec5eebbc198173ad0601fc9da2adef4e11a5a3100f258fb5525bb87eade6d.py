from __future__ import annotations

import re
import psutil
from boundary_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    expected={'regular-seed':15,'boundary-geometry':16,'screen-transport':14,
        'native-boundary':8,'matter-correction':8,'corrected-boundary':6,'seed-constraints':8}
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
    for label in ['heavy','cold']:
        for category in ['native-boundary','corrected-boundary']:
            path=ROOT/'results'/category/(label+'-orthogonal-seed.npz')
            with np.load(path) as packet:
                for name in packet.files:
                    if packet[name].dtype.kind in 'fc':
                        assert np.isfinite(packet[name]).all(),(path,name)
                assert packet['metric2'].shape==packet['mixed_rate2'].shape==(3,3)
                assert packet['field2'].shape==packet['field_prime2'].shape==(2,)
                assert not packet['primordial_zeta2_value_assigned']
                assert packet['primordial_metric2_per_zeta2'].shape==(3,3)
            inputs.append(path)
        check(label+': both original and improved boundary arrays finite and unassigned primordial state retained',True)
        native_path=ROOT/'results/native-boundary'/(label+'-comparison.json')
        native=json.loads(native_path.read_text())
        check(label+': all comparison rows have actual positive scale and no fitted normalization',all(row['scale']>0 for row in native['rows']) and native['normalization_from_native_chi_minus_one_not_fitted'])
        corrected_path=ROOT/'results/corrected-boundary'/(label+'-comparison.json')
        corrected=json.loads(corrected_path.read_text())
        check(label+': high-k finite-gradient residual is explicitly retained',max([max(row['relative_errors_corrected']) for row in corrected['rows'] if np.isclose(row['mode'],1.) and row['requested_scale']==1e-6])>.005)
        inputs.extend([native_path,corrected_path])
    scripts=list(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    check('All scripts compile',True,script_count=len(scripts))
    citations=set()
    pending={ROOT/'results/stage-integrity.json',folder/'status.json'}
    for path in ROOT.rglob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.html','.f90','.dll','.txt')):
                target=(path.parent/reference).resolve()
                assert target in pending or target.is_file(),(path,reference)
                if target not in pending:
                    citations.add(str(target))
        inputs.append(path)
    check('Every cited local source exists or is the pending seal',True)
    process=psutil.Process()
    check('Single worker resource settings intact',process.cpu_affinity()==[2] and process.nice()==psutil.BELOW_NORMAL_PRIORITY_CLASS and all(os.environ[key]=='1' for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']))
    other_workers=[]
    for candidate in psutil.process_iter(['pid','name','cmdline','cwd']):
        if candidate.info['pid']==os.getpid() or 'python' not in (candidate.info['name'] or '').lower():
            continue
        command=' '.join(candidate.info['cmdline'] or []).replace('\\','/').lower()
        directory=(candidate.info['cwd'] or '').replace('\\','/').lower()
        if str(ROOT).replace('\\','/').lower() in command or directory==str(ROOT).replace('\\','/').lower():
            other_workers.append(candidate.info['pid'])
    check('No other stage worker remains active',not other_workers,other_stage_pids=other_workers)
    check('No bytecode cache introduced',not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    finish(folder,dict(checks=checks,count=len(checks),all_current_acceptance_checks_passed=True,
        mathematical_numerical_checks=75,local_citations=sorted(citations),new_primary_source_urls=[
            'https://arxiv.org/abs/astro-ph/9506072','https://arxiv.org/abs/gr-qc/0612191',
            'https://arxiv.org/abs/1803.08939','https://arxiv.org/abs/0809.3036','https://arxiv.org/html/0809.3036v2'],
        full_second_order_cosmological_prediction=False,new_survey_fit=False),__file__,inputs)
    print(json.dumps(dict(accepted_checks=len(checks),mathematical_numerical_checks=75)),flush=True)


if __name__=='__main__':
    main()
