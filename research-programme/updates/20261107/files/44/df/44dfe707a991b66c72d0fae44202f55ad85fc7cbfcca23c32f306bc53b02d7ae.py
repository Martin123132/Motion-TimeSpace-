from __future__ import annotations

import re
import psutil
from collision_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    expected={'collision-operator':11,'relaxation':19,'calibration':3,
        'photon-baryon':8,'photon-reference-refined-fixed':4}
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
    native=ROOT/'runs/backgrounds/status.json'
    packet=json.loads(native.read_text())
    check('Both inherited heavy/cold backgrounds complete',packet['state']=='complete' and packet['all_checks_passed'] and len(packet['rows'])==2)
    assert (native.parent/'COMPLETE').is_file()
    for source,expected_hash in packet['input_hashes'].items():
        assert digest(source)==expected_hash,source
    inputs.append(native)
    failed_path=ROOT/'results/photon-reference-refined/status.json'
    failed=json.loads(failed_path.read_text())
    check('Failed over-tight native tolerance attempt retained as failure',failed['state']=='failed' and failed['completed']==0 and not failed['comparison_results_produced'])
    inputs.append(failed_path)
    for label in ['heavy','cold']:
        path=ROOT/'runs/backgrounds'/(label+'.npz')
        with np.load(path) as packet:
            check(label+': positive opacity and baryon inertia',np.min(packet['opacity'])>0 and np.min(packet['ratio'])>0)
            check(label+': ordered times and finite inherited values',np.all(np.diff(packet['times'])>0) and np.isfinite(packet['values']).all())
        inputs.append(path)
    data_paths=list((ROOT/'results/photon-baryon').glob('*.npz'))+list((ROOT/'results/photon-reference-refined-fixed').glob('*.npz'))
    assert len(data_paths)==12,len(data_paths)
    for path in data_paths:
        with np.load(path) as packet:
            assert packet['independent'].shape==packet['native'].shape==(241,5)
            assert np.isfinite(packet['independent']).all() and np.isfinite(packet['native']).all()
            assert np.all(np.diff(packet['times'])>0) and np.min(packet['envelopes'])>0
            errors=np.max(abs(packet['independent']-packet['native']),axis=0)/packet['envelopes']
            assert np.allclose(errors,packet['errors'],rtol=1e-12,atol=1e-15)
        inputs.append(path)
    check('All12 independent/reference arrays and saved error calculations valid',True)
    calibration=json.loads((ROOT/'results/calibration/status.json').read_text())
    check('Current constants remain calibration, not a derived charge or silent native change',not calibration['new_charge_or_electron_mass_derivation'] and calibration['native_constants_not_changed'] and calibration['recoil_diagnostic_not_full_thermal_Compton_operator'])
    scripts=list(ROOT.glob('*.py'))+list((ROOT/'diagnostics').glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    check('All current and archived attempt scripts compile',True,script_count=len(scripts))
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
        failed_native_attempts_preserved=1,failed_physics_acceptance_checks=0,
        local_citations=sorted(citations),new_primary_source_urls=[
            'https://physics.nist.gov/cuu/Constants/Table/allascii.txt',
            'https://www.physics.nist.gov/cuu/Reference/versioncon.shtml',
            'https://arxiv.org/abs/0809.3036','https://arxiv.org/html/0809.3036v2',
            'https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/electromagnetic/gamma_incident/compton/compton.html'],
        full_second_order_cosmological_prediction=False,new_survey_fit=False),__file__,inputs)
    print(json.dumps(dict(accepted_checks=len(checks),failed_native_attempts_preserved=1)),flush=True)


if __name__=='__main__':
    main()
