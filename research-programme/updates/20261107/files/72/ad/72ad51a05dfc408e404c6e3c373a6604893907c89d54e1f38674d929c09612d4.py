from __future__ import annotations

from boundary_common import *


def main():
    modest()
    folder=ROOT/'results/boundary-geometry'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    pairs=[(np.array([.1,0,0]),np.array([0,.1,0])),
        (np.array([.12,.03,0]),np.array([-.02,.07,.08])),
        (np.array([.1,0,0]),np.array([.1,0,0])),
        (np.array([.1,0,0]),np.array([-.1,0,0]))]
    rows=[]
    for index,(momentum_p,momentum_q) in enumerate(pairs):
        result=seed_geometry(momentum_p,momentum_q,.4089)
        dot=float(momentum_p@momentum_q)
        norm_p=float(momentum_p@momentum_p)
        norm_q=float(momentum_q@momentum_q)
        expected=-4*(norm_p+norm_q)+2*dot-6*dot*(norm_q/norm_p+norm_p/norm_q)
        check('Pair'+str(index)+': independent conformal-pullback scalar curvature',abs(result['scalar2']-expected)<2e-13,scalar2=float(result['scalar2']),expected=expected)
        check('Pair'+str(index)+': covariant metric coefficient symmetric',np.max(abs(result['metric2_time_coefficient']-result['metric2_time_coefficient'].T))<2e-13)
        commutator=(result['seed_p']@result['rate_q']+result['seed_q']@result['rate_p']-result['rate_q']@result['seed_p']-result['rate_p']@result['seed_q'])/2
        check('Pair'+str(index)+': mixed extrinsic-curvature antisymmetry retained',np.max(abs(result['rate2']-result['rate2'].T+commutator))<2e-13)
        total=momentum_p+momentum_q
        tensor_norm=0.
        if total@total>0:
            projector=np.eye(3)-np.outer(total,total)/(total@total)
            covariant=result['ricci2']+(result['seed_p']@result['ricci_q']+result['seed_q']@result['ricci_p'])/2
            transverse=projector@covariant@projector
            tensor_norm=float(np.linalg.norm(transverse-projector*np.trace(transverse)/2))
        rows.append(dict(pair=index,scalar2=float(result['scalar2']),covariant_ricci_TT_norm=tensor_norm))
    check('Nonparallel scalar pair retains nonzero generated tensor',rows[0]['covariant_ricci_TT_norm']>1e-6)
    check('Opposite-wave homogeneous curvature retained without K inverse',abs(rows[-1]['scalar2'])>1e-6)
    momenta=[np.array([.7,.2,0]),np.array([-.1,.5,.4])]
    point=np.array([.21,-.17,.31])
    amplitudes=np.array([.04,.02,.01,.005,.0025])
    metric1=np.zeros((3,3),complex)
    first1=np.zeros((3,3,3),complex)
    second1=np.zeros((3,3,3,3),complex)
    metric2=np.zeros((3,3),complex)
    curvature2_linear=np.zeros((3,3),complex)
    modes=[(sign*momentum,.5) for momentum in momenta for sign in [-1,1]]
    for momentum,weight in modes:
        phase=weight*np.exp(1j*momentum@point)
        linear=seed_linear(momentum)*phase
        metric1+=linear
        first1+=1j*np.einsum('a,ij->aij',momentum,linear)
        second1-=np.einsum('a,b,ij->abij',momentum,momentum,linear)
        for partner,partner_weight in modes:
            total=momentum+partner
            coefficient=seed_pair(momentum,partner)*weight*partner_weight*np.exp(1j*total@point)
            metric2+=coefficient
            curvature2_linear+=linear_ricci(coefficient,total)
    coefficient=inherited.inherited.ricci_series(metric1,first1,second1)[1]+curvature2_linear
    def exact(amplitude):
        phases=np.array([momentum@point for momentum in momenta])
        shift=sum(-3*momentum*np.sin(phase)/(momentum@momentum) for momentum,phase in zip(momenta,phases))
        jacobian=np.eye(3)+amplitude*sum(-3*np.outer(momentum,momentum)*np.cos(phase)/(momentum@momentum) for momentum,phase in zip(momenta,phases))
        mapped=point+amplitude*shift
        mapped_phases=np.array([momentum@mapped for momentum in momenta])
        zeta=amplitude*np.cos(mapped_phases).sum()
        gradient=sum(-amplitude*momentum*np.sin(phase) for momentum,phase in zip(momenta,mapped_phases))
        hessian=sum(-amplitude*np.outer(momentum,momentum)*np.cos(phase) for momentum,phase in zip(momenta,mapped_phases))
        metric=math.exp(2*zeta)*jacobian.T@jacobian
        ricci=-hessian-np.eye(3)*np.trace(hessian)+np.outer(gradient,gradient)-np.eye(3)*(gradient@gradient)
        return metric,np.linalg.solve(metric,jacobian.T@ricci@jacobian)
    errors=[]
    metric_errors=[]
    for amplitude in amplitudes:
        positive_metric,positive=exact(amplitude)
        negative_metric,negative=exact(-amplitude)
        extracted=(positive+negative)/(2*amplitude**2)
        extracted_metric=(positive_metric+negative_metric-2*np.eye(3))/(2*amplitude**2)
        errors.append(float(np.max(abs(extracted-coefficient)))/float(np.max(abs(coefficient))))
        metric_errors.append(float(np.max(abs(extracted_metric-metric2)))/float(np.max(abs(metric2))))
    check('Exact nonlinear pullback Ricci converges to quadratic seed',np.all(np.diff(errors)<0) and errors[-1]<2e-4,errors=errors)
    check('Exact nonlinear pullback metric converges to quadratic seed',np.all(np.diff(metric_errors)<0) and metric_errors[-1]<2e-4,errors=metric_errors)
    np.savez_compressed(folder/'curvature-check.npz',amplitudes=amplitudes,errors=errors,metric_errors=metric_errors,ricci2=coefficient,seed2=metric2)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,rows=rows,
        primordial_second_order_curvature_separate=True,spatial_gauge_map_not_ignored=True),__file__,[GEOMETRY/'constraint_common.py'])
    print(json.dumps(dict(checks=len(checks),curvature_errors=errors,metric_errors=metric_errors)),flush=True)


if __name__=='__main__':
    main()
