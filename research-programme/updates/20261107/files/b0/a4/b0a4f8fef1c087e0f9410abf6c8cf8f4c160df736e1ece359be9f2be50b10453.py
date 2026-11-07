from __future__ import annotations

from scipy.special import eval_legendre
from constraint_common import *


def angular_grid(polar,azimuthal):
    cosine,weights=np.polynomial.legendre.leggauss(polar)
    angle=2*np.pi*np.arange(azimuthal)/azimuthal
    directions=np.stack([np.repeat(np.sqrt(1-cosine**2),azimuthal)*np.tile(np.cos(angle),polar),
        np.repeat(np.sqrt(1-cosine**2),azimuthal)*np.tile(np.sin(angle),polar),
        np.repeat(cosine,azimuthal)],axis=1)
    return directions,np.repeat(weights/(2*azimuthal),azimuthal)


def angular_source(directions,pvector,qvector,hp,hq,fp,fq,dfp,dfq):
    pnorm=np.linalg.norm(pvector)
    qnorm=np.linalg.norm(qvector)
    pn=directions@pvector
    qn=directions@qvector
    hp_n=directions@hp
    hq_n=directions@hq
    projected_p=np.sum(hp_n*directions,axis=1)
    projected_q=np.sum(hq_n*directions,axis=1)
    ep=-projected_p/2
    eq=-projected_q/2
    e2=np.sum(hp_n*hq_n,axis=1)/2-projected_p*projected_q/8
    jp=fp+2*projected_p
    jq=fq+2*projected_q
    grad_p=dfp[:,None]*(pvector/pnorm)+4*hp_n
    grad_q=dfq[:,None]*(qvector/qnorm)+4*hq_n
    vp=-hp_n+projected_p[:,None]*directions/2
    vq=-hq_n+projected_q[:,None]*directions/2
    pp=pvector-directions*pn[:,None]
    pq=qvector-directions*qn[:,None]
    source=-4j*(pn+qn)*e2-.5j*((vp@qvector+4*pn*ep)*jq-ep*np.sum(pp*grad_q,axis=1)+
        (vq@pvector+4*qn*eq)*jp-eq*np.sum(pq*grad_p,axis=1))
    return source,(ep,eq,e2,jp,jq,hp_n,hq_n)


def stress_part(directions,weights,hp,hq,parts,driven):
    ep,eq,e2,jp,jq,hp_n,hq_n=parts
    volume_p=np.trace(hp)/2
    volume_q=np.trace(hq)/2
    determinant2=volume_p*volume_q/2+np.trace(hp@hq)/4
    energy=driven+(ep*jq+eq*jp)/2+e2-(volume_p*(jq+eq)+volume_q*(jp+ep))/2+determinant2
    current=directions*(driven-(volume_p*jq+volume_q*jp)/2+determinant2)[:,None]
    base=np.einsum('ni,nj->nij',directions,directions)
    first_p=-np.einsum('ni,nj->nij',hp_n,directions)-ep[:,None,None]*base
    first_q=-np.einsum('ni,nj->nij',hq_n,directions)-eq[:,None,None]*base
    second=np.einsum('ni,nj->nij',directions@((hp@hq+hq@hp)/2),directions)
    second+=np.einsum('ni,nj->nij',(hp_n*eq[:,None]+hq_n*ep[:,None])/2,directions)
    second+=(ep*eq-e2)[:,None,None]*base
    stress=base*driven[:,None,None]+(first_p*jq[:,None,None]+first_q*jp[:,None,None])/2+second
    stress-=(volume_p*(base*jq[:,None,None]+first_q)+volume_q*(base*jp[:,None,None]+first_p))/2
    stress+=determinant2*base
    return np.r_[weights@energy,weights@current,np.einsum('n,nij->ij',weights,stress).ravel()]


def solve_response(packet,polar,azimuthal,thin=1):
    times=packet['conformal_time']
    names=list(packet['names'])
    values=packet['values'][1]
    mode=float(packet['modes'][1])
    assert abs(mode-.1)<1e-14
    _,volume_rate,_,_=inherited.metric(mode,np.array([1.,0.,0.]),names,values,float(packet['baryon_fraction']))
    shear=-values[:,names.index('H')]*values[:,names.index('v_newtonian_cdm')]
    trace=-2*values[:,names.index('delta_cdm')]
    eta=values[:,names.index('etak')]/mode
    selected=np.unique(np.r_[np.arange(0,len(times),thin),len(times)-1])
    table=np.column_stack([trace,eta,volume_rate,shear])
    spline=interpolate.CubicSpline(times[selected],table[selected])
    directions,weights=angular_grid(polar,azimuthal)
    pvector=np.array([mode,0.,0.])
    qvector=np.array([0.,mode,0.])
    mu_p=directions[:,0]
    mu_q=directions[:,1]
    k_dot=directions@(pvector+qvector)
    ratio=(7/8)*(4/11)**(4/3)*float(packet['effective_neutrino_number'])
    fraction=ratio/(1+ratio)
    initial=[values[0,names.index('delta_neutrino')],values[0,names.index('v_neutrino')],
        eta[0]*(4/3)*(mode*times[0])**2/(15+4*fraction),eta[0]*(4/21)*(mode*times[0])**3/(15+4*fraction)]
    def initial_angular(mu):
        field=sum(((-1j)**order)*(2*order+1)*initial[order]*eval_legendre(order,mu) for order in range(4))
        derivative=-3j*initial[1]-15*initial[2]*mu+7j*initial[3]*(15*mu**2-3)/2
        return field,derivative
    fp,dfp=initial_angular(mu_p)
    fq,dfq=initial_angular(mu_q)
    start=np.r_[fp,dfp,fq,dfq,np.zeros(len(directions),complex)]
    identity=np.eye(3)
    projector_p=np.diag([2/3,-1/3,-1/3])
    projector_q=np.diag([-1/3,2/3,-1/3])
    def metric_at(moment):
        scalar_trace,eta_value,volume,shear_value=spline(moment)
        hp=scalar_trace*identity/3+(scalar_trace+6*eta_value)*projector_p
        hq=scalar_trace*identity/3+(scalar_trace+6*eta_value)*projector_q
        return hp,hq,volume,shear_value
    def derivative(moment,state):
        fp,dfp,fq,dfq,driven=state.reshape(5,-1)
        hp,hq,volume,shear_value=metric_at(moment)
        source,_=angular_source(directions,pvector,qvector,hp,hq,fp,fq,dfp,dfq)
        return np.r_[-1j*mode*mu_p*fp-4*volume/3-4*shear_value*(mu_p**2-1/3),
            -1j*mode*mu_p*dfp-1j*mode*fp-8*shear_value*mu_p,
            -1j*mode*mu_q*fq-4*volume/3-4*shear_value*(mu_q**2-1/3),
            -1j*mode*mu_q*dfq-1j*mode*fq-8*shear_value*mu_q,
            -1j*k_dot*driven+source]
    samples=np.linspace(times[0],times[-1],121)
    solution=integrate.solve_ivp(derivative,(times[0],times[-1]),start,method='DOP853',
        rtol=1e-8,atol=1e-10,t_eval=samples,max_step=.5)
    assert solution.success,solution.message
    stresses=[]
    monopoles=[]
    for index,moment in enumerate(samples):
        fp,dfp,fq,dfq,driven=solution.y[:,index].reshape(5,-1)
        hp,hq,_,_=metric_at(moment)
        _,parts=angular_source(directions,pvector,qvector,hp,hq,fp,fq,dfp,dfq)
        stresses.append(stress_part(directions,weights,hp,hq,parts,driven))
        monopoles.append(weights@driven)
    return samples,np.array(stresses),np.array(monopoles),solution.nfev


def main():
    modest()
    folder=ROOT/'results/quadratic-neutrinos'
    folder.mkdir(parents=True,exist_ok=False)
    report=dict(state='running',pid=os.getpid(),completed=0,total=6)
    write_json(folder/'status.json',report)
    checks=[]
    inputs=[ROOT/'QUADRATIC-RESPONSE-CONTRACT.md']
    directions,weights=angular_grid(16,32)
    hp=np.array([[.3,.04,.06],[.04,-.15,.02],[.06,.02,.1]])
    hq=np.array([[-.1,.03,-.02],[.03,.25,.05],[-.02,.05,.12]])
    pvector=np.array([.1,0.,0.])
    qvector=np.array([0.,.1,0.])
    empty=np.zeros(len(directions),complex)
    source,parts=angular_source(directions,pvector,qvector,hp,hq,empty,empty,empty,empty)
    ep,eq,e2,*_=parts
    equilibrium=10*ep*eq-4*e2
    residual=source-1j*(directions@(pvector+qvector))*equilibrium
    checks.append(dict(name='Static equilibrium annihilates full quadratic angular source',passed=bool(np.max(abs(residual))<1e-13),max_error=float(np.max(abs(residual)))))
    rows=[]
    for label in ['heavy','cold']:
        source=ROOT/'runs/native'/(label+'.npz')
        inputs.append(source)
        packet=np.load(source)
        results=[]
        for polar,azimuthal,thin in [(24,48,1),(32,64,1),(32,64,2)]:
            started=time.monotonic()
            times,stress,driven,nfev=solve_response(packet,polar,azimuthal,thin)
            results.append(stress)
            np.savez_compressed(folder/(label+'-'+str(polar)+'x'+str(azimuthal)+'-thin'+str(thin)+'.npz'),
                times=times,stress_source_part=stress,driven_canonical_monopole=driven)
            row=dict(model=label,quadrature=[polar,azimuthal],time_thin=thin,nfev=nfev,seconds=time.monotonic()-started)
            rows.append(row)
            report.update(completed=report['completed']+1,last=row)
            write_json(folder/'status.json',report)
            print(json.dumps(row),flush=True)
        envelope=max(float(np.max(abs(results[1]))),1e-10)
        angular_error=float(np.max(abs(results[0]-results[1])))/envelope
        time_error=float(np.max(abs(results[2]-results[1])))/envelope
        checks.extend([dict(name=label+': quadratic angular convergence',passed=angular_error<1e-5,envelope_error=angular_error),
            dict(name=label+': quadratic source-time refinement',passed=time_error<.001,envelope_error=time_error)])
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,rows=rows,
        pair=dict(p=[.1,0,0],q=[0,.1,0]),normalization='symmetric ordered quadratic kernel; energy/stress divided by rho_nu0, covariant current by a*rho_nu0',
        computed_component='retarded quadratic drive plus instantaneous first-metric products',
        retained_separate_components=['retarded linear response to l_ij','propagated second-order primordial boundary distribution'],
        full_nonlinear_cosmological_solution=False,no_amplitude_fit=True,same_operations_on_heavy_and_cold=True,
        acceptance_sampling_times=121),__file__,inputs)
    assert passed,checks


if __name__=='__main__':
    main()
