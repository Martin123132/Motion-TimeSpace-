from __future__ import annotations

import subprocess
from matching_common import *


def child(case):
    source = ROOT/'runs/matching-inputs/a225-w6-d8.npz'
    if case=='unmatched_exact':
        source=BACKGROUND
    params = params_for(source)
    native=camb.get_background(params)
    times=native.conformal_time(np.array([1/.0003-1]),tol=1e-10)
    native.Params.Accuracy.IntTolBoost=6
    native.get_time_evolution([.04],times,vars=['delta_cdm'])
    raise RuntimeError('Expected native refusal did not happen')


def main():
    modest()
    if len(sys.argv)>1:
        child(sys.argv[1])
        return
    folder=ROOT/'results/input-guards'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    for case, message in [('unknown_mode','no sourced phase projection'),('unmatched_exact','exact domain exceeded')]:
        result=subprocess.run([sys.executable,'-B',__file__,case],stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,text=True,timeout=90)
        (folder/(case+'.log')).write_text(result.stdout,encoding='utf-8')
        checks.append(dict(name=case,passed=result.returncode!=0 and message in result.stdout,exit_code=result.returncode))
    from camb.mts import MTSTwoField
    for case,nodes,first,second in [('unordered',[.03,1.,.1,5.],[1.]*4,[0.]*4),
        ('nonfinite',[.03,.1,1.,5.],[1.,np.nan,1.,1.],[0.]*4),
        ('mismatched_lengths',[.03,.1,1.,5.],[1.]*3,[0.]*4)]:
        try:
            MTSTwoField().set_table('SetMatching',nodes,first,second)
            passed=False
        except ValueError:
            passed=True
        checks.append(dict(name=case,passed=passed))
    finish(folder,dict(checks=checks,all_checks_passed=all(row['passed'] for row in checks)),__file__,
        [*native_hashes(),*folder.glob('*.log')])
    print(json.dumps(checks,indent=2))
    assert all(row['passed'] for row in checks)


if __name__ == '__main__':
    main()
