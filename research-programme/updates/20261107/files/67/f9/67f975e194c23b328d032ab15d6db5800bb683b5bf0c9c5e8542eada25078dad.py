from common197 import *
from propagate197 import weights

def validate():
    frozen();checks=[]
    for profile in ('quadratic','linear'):
        for index,offset in enumerate(OFFSETS):
            check(checks,f'{profile}:cardinal node{index}',np.max(abs(weights(offset,profile)-np.eye(5)[index])),1e-10,'identity')
        for offset in np.linspace(-.01,.01,101):
            coefficients=weights(offset,profile)
            for degree in range(3 if profile=='quadratic' else 2):
                check(checks,f'{profile}:polynomial reproduction:{offset}:{degree}',abs(coefficients@OFFSETS**degree-offset**degree),1e-10,'identity')
    upper,lower=parts_sum(np.array([[1e16],[1.],[-1e16]]),np.zeros((3,1)))
    check(checks,'compensated catastrophic cancellation control',abs(upper[0]+lower[0]-1),0,'identity')
    stiffness=np.array([[-1.,.2],[.2,-2.]])
    temperature=np.array([1.,0.]);heat=3.;rate=.7
    history=np.array([.4,-.3]);gas_history=.1;force=np.array([.2,.5])
    for alpha in (80.,120.):
        for gas_source in (-.2,.13):
            coupling=-rate*stiffness@temperature
            free=(history[0]+heat*gas_history+rate*(force[0]+gas_source))/(heat*(alpha+1))
            coefficient=alpha/(heat*(alpha+1))
            reduced=alpha*np.eye(2)-rate*stiffness
            reduced[:,0]+=coupling*coefficient
            photons=linalg.solve(reduced,history+rate*force+coupling*free)
            gas=free-coefficient*photons[0]
            full=np.block([[alpha*np.eye(2)-rate*stiffness,-coupling[:,None]],
                           [(rate*temperature@stiffness)[None,:],np.array([[heat*(alpha+1)-rate*temperature@stiffness@temperature]])]])
            independent=linalg.solve(full,np.r_[history+rate*force,heat*gas_history+rate*gas_source])
            check(checks,f'independent unreduced photon-gas solve:{alpha}:{gas_source}',np.max(abs(np.r_[photons,gas]-independent))/np.max(abs(independent)),1e-10,'identity')
    known=packet(PARENT/'results/seven-node-curvature.npz')
    sites={tag:packet(ROOT/f'sources/{tag}.npz') for tag in TAGS}
    for version,group in [(0,None),(5,3)]:
        for kind,component in [(0,0),(1,4),(2,5)]:
            differences=[];scales=[]
            with localcontext() as context:
                context.prec=100
                for row,column in np.ndindex(98,4):
                    source={tag:Decimal.from_float(float(data['high'][version,kind,row,column]))+
                            Decimal.from_float(float(data['low'][version,kind,row,column])) for tag,data in sites.items()}
                    derivative=(source['plus_half']-2*source['anchor']+source['minus_half'])/Decimal('.005')**2
                    expected=float(known['old_vectors'][1,0,component,row,column] if group is None else known['vectors'][1,group,component,row,column])
                    differences.append(abs(float(derivative)-expected));scales.append(abs(expected))
            check(checks,f'Stage196 curvature recovered:{VERSIONS[version]}:{KINDS[kind]}',max(differences)/max(max(scales),1e-300),1e-10,'identity')
    write(ROOT/'results/independent-validation.json',dict(checks=checks,failed_checks=[row for row in checks if not row['passed']]))
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(independent_checks=len(checks),failed=0)),flush=True)

if __name__=='__main__':
    validate()
