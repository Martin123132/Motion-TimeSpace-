from overlap_common import *
import ast


def main():
    modest()
    folder=ROOT/'results/identities'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    generator=np.array([[-3.,.8,0.],[.2,-1.5,.4],[0.,.9,-2.]])
    step=.125
    matrix=np.eye(3)-step*generator
    checks.append(dict(name='Manufactured M-matrix inverse positive',
        passed=bool(np.linalg.inv(matrix).min()>=0)))
    initial=np.array([.4,-.2,.5])
    state=initial.copy()
    error=np.zeros(3)
    envelope=np.zeros(3)
    outer_previous=initial.copy()
    worst_identity,worst_envelope=0.,0.
    for index in range(1,17):
        coordinate=index*step
        outer=initial+np.array([math.sin(coordinate),coordinate**2,-coordinate])
        forcing=np.array([coordinate,-.1,.3])
        residual=(outer-outer_previous)/step-generator@outer-forcing
        state=np.linalg.solve(matrix,state+step*forcing)
        error=np.linalg.solve(matrix,error-step*residual)
        envelope=np.linalg.solve(matrix,envelope+step*abs(residual))
        worst_identity=max(worst_identity,float(np.max(abs(state-outer-error))))
        worst_envelope=max(worst_envelope,float(np.max(np.maximum(abs(error)-envelope,0))))
        outer_previous=outer
    checks.extend([check('Manufactured defect forcing sign',worst_identity,1e-13),
                   check('Manufactured comparison envelope',worst_envelope,1e-13)])
    frequency=np.geomspace(1e-4,.04,101)
    ratio=np.array([.85,1.,1.18])[:,None]
    exact=(frequency/np.expm1(frequency))*(ratio*frequency/(-np.expm1(-ratio*frequency)))
    expansion=1+(ratio-1)*frequency/2+((1+ratio**2)/12-ratio/4)*frequency**2
    checks.append(check('Planck expansion absolute remainder over x cubed',
        np.max(abs(exact-expansion)/frequency**3),.02))
    identity=(frequency/(2*np.sinh(frequency/2)))**2
    checks.append(check('Equal-frequency Planck measure identity',np.max(abs(exact[1]-identity)),1e-14))
    correction_at_half=[]
    for factor in [1,.5]:
        scaled=frequency*factor
        value=(scaled/np.expm1(scaled))*(scaled/(-np.expm1(-scaled)))
        correction_at_half.append(abs(value[-1]-1))
    checks.append(check('Equal-frequency remainder quadratic soft limit',
        abs(correction_at_half[0]/correction_at_half[1]-4),.002))
    tree=ast.parse((ROOT/'solve_overlap.py').read_text(encoding='utf-8'))
    keys=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='prediction':
            if isinstance(node.slice,ast.Constant):
                keys.append(node.slice.value)
    assert set(keys)=={'frequency','offsets','coefficient_bank','coefficient_knots','coordinate'},keys
    checks.append(dict(name='Prediction reads only geometry,clock and physical coefficient cache;no target slopes',
        accessed_keys=sorted(set(keys)),passed=True))
    finish(folder,dict(checks=checks,manufactured_dynamics=True,actual_scientific_predictions=False),
           __file__,[ROOT/'solve_overlap.py',ROOT/'PLANCK-BOUND-SCOPE.md'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
