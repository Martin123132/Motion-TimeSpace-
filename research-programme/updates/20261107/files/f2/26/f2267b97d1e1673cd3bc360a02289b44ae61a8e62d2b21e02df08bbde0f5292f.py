from common226 import *
from scipy.linalg import expm
from scipy.integrate import solve_ivp

def run():
    protocol()
    rows=[]
    rng=np.random.default_rng(226)
    for index in range(30):
        current,previous,older=rng.normal(size=(3,4))
        lhs=current@((3*current-4*previous+older)/2)
        rhs=(current@current+(2*current-previous)@(2*current-previous)-previous@previous
            -(2*previous-older)@(2*previous-older)+(current-2*previous+older)@(current-2*previous+older))/4
        check(rows,f'G identity {index}',abs(lhs-rhs)/max(abs(lhs)+abs(rhs),1e-300),1e-10,'identity')
    with mp.workdps(80):
        for size in (4,16,64):
            spacing=mp.mpf(1)/size
            initial=mp.mpf('0.73')
            sequence=[mp.mpf(0),initial]
            forcing=[mp.mpf(0),mp.mpf(0)]+[mp.sin(index) for index in range(2,size+1)]
            for index in range(2,size+1):
                sequence.append((4*sequence[-1]-sequence[-2]+2*spacing*forcing[index])/3)
            for index in range(1,size+1):
                exact=mp.mpf('1.5')*(1-mp.mpf(3)**(-index))*initial
                exact+=spacing*mp.fsum((1-mp.mpf(3)**(-(index-earlier+1)))*forcing[earlier] for earlier in range(2,index+1))
                check(rows,f'positive discrete Green {size}:{index}',abs(exact-sequence[index]),1e-10,'identity')
    heat=.2
    metric=np.diag([1.,heat])
    operator=np.array([[-1.4,1.4],[1.4/heat,-1-1.4/heat]])
    for name in ('balanced','unbalanced','zero'):
        raw=np.array([[.2,-.2],[.5,-.5],[-.3,.3],[.1,-.1],[.4,-.4]])
        if name=='unbalanced':
            raw[:,1]*=.7
        if name=='zero':
            raw[:]=0
        coordinates=np.linspace(0,1,5)
        norms=[mp.mpf(float(np.sqrt(force[0]**2+force[1]**2/heat))) for force in raw]
        pairs=[mp.mpf(float(force.sum())) for force in raw]
        coords=[mp.mpf(float(value)) for value in coordinates]
        density_bound=forced_q(mp.mpf(heat),mp.mpf(0),coords,norms,pairs,mp.mpf('1.3'))
        norm_bound=integrals(coords,norms,pairs,mp.mpf('1.3'))[0]
        state=np.zeros(2)
        maxima=0.;last=0.
        for index in range(5):
            first=coordinates[index] if index<4 else 1.
            second=coordinates[index+1] if index<4 else 1.3
            width=second-first
            left=raw[index]/np.diag(metric) if index<4 else np.zeros(2)
            slope=(raw[index+1]-raw[index])/width/np.diag(metric) if index<4 else np.zeros(2)
            augmented=np.zeros((4,4))
            augmented[:2,:2]=operator
            augmented[:2,2]=slope
            augmented[:2,3]=left
            augmented[2,3]=1
            initial=np.r_[state,0.,1.]
            direct=expm(augmented*width)@initial
            independent=solve_ivp(lambda offset,value:operator@value+left+slope*offset,(0,width),state,
                rtol=3e-12,atol=1e-14,method='DOP853')
            assert independent.success
            check(rows,f'{name}:{index}:exponential versus forward',np.max(abs(direct[:2]-independent.y[:,-1])),1e-10,'independent_evolution')
            for offset in np.linspace(0,width,11):
                current=(expm(augmented*offset)@initial)[:2]
                density=heat*(current[0]+heat*current[1])
                maxima=max(maxima,abs(density))
                check(rows,f'{name}:{index}:{offset}:continuous forced norm',np.sqrt(current@metric@current)/max(float(norm_bound),1e-300),1+1e-10,'bound')
            state=direct[:2]
        check(rows,f'{name}:continuous forced density',maxima/max(float(density_bound),1e-300),1+1e-10,'bound')
        for count in (16,32):
            spacing=1/count
            nodes=np.linspace(0,1,count+1)
            supplied=np.column_stack([np.interp(nodes,coordinates,raw[:,column]) for column in range(2)])
            fnorms=[mp.mpf(float(np.sqrt(force[0]**2+force[1]**2/heat))) for force in supplied]
            injection=[mp.mpf(float(force.sum())) for force in supplied]
            upper,density=discrete_bounds(mp.mpf(heat),mp.mpf(spacing),fnorms,injection,mp.mpf(0))
            older=np.zeros(2)
            current=np.linalg.solve(np.eye(2)-spacing*operator/2,spacing*(supplied[0]+supplied[1])/np.diag(metric)/2)
            for index in range(1,count+1):
                if index>1:
                    updated=np.linalg.solve(1.5*np.eye(2)-spacing*operator,2*current-.5*older+spacing*supplied[index]/np.diag(metric))
                    older,current=current,updated
                two_state=np.sqrt(current@metric@current+(2*current-older)@metric@(2*current-older))
                q=heat*(current[0]+heat*current[1])
                check(rows,f'{name}:{count}:{index}:discrete norm',two_state/max(float(upper[index]),1e-300),1+1e-10,'bound')
                check(rows,f'{name}:{count}:{index}:discrete density',abs(q)/max(float(density[index]),1e-300),1+1e-10,'bound')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/controls.json',dict(checks=rows,failed_checks=failed,qualified=not failed,finished_at=now()))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:10])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    run()

