import re
import psutil
from initial_state import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
    packets=list(ROOT.glob('runs/*/status.json'))+list(ROOT.glob('results/*/status.json'))
    assert len(packets)==21,len(packets)
    retained_failures=[]
    for path in packets:
        packet=json.loads(path.read_text())
        check(path.parent.name+': complete saved packet',packet['state']=='complete' and (path.parent/'COMPLETE').is_file())
        if path.parent.name=='refinements':
            retained_failures=[row for row in packet['checks'] if not row['passed']]
            check('Original coarse time-grid failures preserved',len(retained_failures)==4 and not packet['all_checks_passed'])
        else:
            checks.extend(dict(row,name=path.parent.name+': '+row['name']) for row in packet['checks'])
        for source,expected in packet['input_hashes'].items():
            assert digest(source)==expected,(path,source)
        inputs.append(path)
    for label in ['heavy','cold']:
        path=ROOT/'runs'/(label+'-sixteenth')/'evolution.npz'
        saved=np.load(path)
        background=Background(label)
        system=CoupledSystem(background,6)
        moment=float(saved['times'][-1])
        state=saved['final_state']
        system.cold_numbers=saved['cold_numbers']
        baseline=system.slow_rhs(moment,state)+system.collision_rhs(moment,state)
        amplitude=.37+.2j
        combined=state.copy()
        combined[3]+=amplitude*state[2]
        changed=system.slow_rhs(moment,combined)+system.collision_rhs(moment,combined)
        expected=baseline[3]+amplitude*baseline[2]
        residual=np.linalg.norm(changed[3]-expected)/max(np.linalg.norm(expected),1e-100)
        check(label+': independent primordial homogeneous response superposes',residual<1e-8,value=float(residual),gate=1e-8)
        unchanged=np.max(abs(changed[:3]-baseline[:3]))
        check(label+': quadratic sector cannot feed first-order modes',unchanged==0,value=float(unchanged))
        initial=background.time_at(5e-7)
        check(label+': finite history and final restart shape',bool(np.isfinite(state).all() and saved['features'].shape==(41,4,27) and state.shape==(4,system.size)))
        first_order_symmetry=np.max(abs(saved['features'][:,0,:4]-saved['features'][:,1,:4]))
        check(label+': x/y exchange leaves scalar response invariant',first_order_symmetry<1e-11,value=float(first_order_symmetry))
        inputs.append(path)
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    check('All scripts compile without bytecode',True,script_count=len(scripts))
    citations=set()
    pending={ROOT/'results/stage-integrity.json',folder/'status.json'}
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.html','.f90','.dll','.txt')):
                target=(path.parent/reference).resolve()
                assert target in pending or target.is_file(),(path,reference)
                if target not in pending:
                    citations.add(str(target))
        inputs.append(path)
    check('Every cited local source exists or is pending seal',True)
    process=psutil.Process()
    check('One-core below-normal resource settings',process.cpu_affinity()==[2] and process.nice()==psutil.BELOW_NORMAL_PRIORITY_CLASS and all(os.environ[key]=='1' for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']))
    others=[]
    for candidate in psutil.process_iter(['pid','name','cmdline','cwd']):
        if candidate.info['pid']==os.getpid() or 'python' not in (candidate.info['name'] or '').lower():
            continue
        command=' '.join(candidate.info['cmdline'] or []).replace('\\','/').lower()
        directory=(candidate.info['cwd'] or '').replace('\\','/').lower()
        if str(ROOT).replace('\\','/').lower() in command or directory==str(ROOT).replace('\\','/').lower():
            others.append(candidate.info['pid'])
    check('No other stage worker remains active',not others,other_stage_pids=others)
    check('No bytecode cache introduced',not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_current_acceptance_checks_passed=passed,
        retained_coarse_failures=retained_failures,local_citations=sorted(citations),new_primary_source_urls=['https://arxiv.org/abs/astro-ph/9506072','https://arxiv.org/html/0809.3036v2'],
        physical_scope_is_early_UR_cold_Thomson_pressureless_baryons=True,new_observational_fit=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)
    assert passed


if __name__=='__main__':
    main()
