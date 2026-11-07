from __future__ import annotations

import sympy as symbolic
from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/finite-amplitude'
    folder.mkdir(parents=True,exist_ok=False)
    time,coord_x,coord_y,coord_z=symbolic.symbols('t x y z',real=True)
    coordinates=[coord_x,coord_y,coord_z]
    phase_p=coord_x+coord_z
    phase_q=coord_y+coord_z
    matrix_p=symbolic.Matrix([[.3,.04,.06],[.04,-.15,.02],[.06,.02,.1]])*(1+.2*time)
    matrix_q=symbolic.Matrix([[-.1,.03,-.02],[.03,.25,.05],[-.02,.05,.12]])*(1-.1*time+time**2*.03)
    metric1=matrix_p*symbolic.cos(phase_p)+matrix_q*symbolic.cos(phase_q)
    metric2=symbolic.Matrix([[.02,.01,0],[.01,-.03,.01],[0,.01,.04]])*(1+time**2)*symbolic.cos(phase_p+phase_q)+symbolic.eye(3)*.015*time
    background=.7+.2*time-.03*time**2+.004*time**3
    field1=(.4+.1*time+.02*time**2)*symbolic.cos(phase_p)+(.3-.07*time+.01*time**3)*symbolic.cos(phase_q)
    field2=(.03+.02*time-.005*time**2)*symbolic.cos(phase_p+phase_q)+.012*time*symbolic.cos(2*phase_p)
    expressions=[background,symbolic.diff(background,time),symbolic.diff(background,time,2),
        field1,symbolic.diff(field1,time),symbolic.diff(field1,time,2),
        field2,symbolic.diff(field2,time),symbolic.diff(field2,time,2)]
    expressions+=list(metric1)+list(metric1.diff(time))+list(metric2)+list(metric2.diff(time))
    expressions+=[entry for coordinate in coordinates for entry in metric1.diff(coordinate)]
    expressions+=[entry for coordinate in coordinates for entry in metric2.diff(coordinate)]
    expressions+=[symbolic.diff(field,coordinate) for field in [field1,field2] for coordinate in coordinates]
    expressions+=[symbolic.diff(field,first,second) for field in [field1,field2] for first in coordinates for second in coordinates]
    evaluate=symbolic.lambdify([time,*coordinates],expressions,'numpy',cse=True)
    mass=.8
    samples=[]
    minimum_eigenvalue=1.
    for index in range(12):
        moment=.1+.07*index
        point=[.17+.19*index,.31+.11*index,.27-.09*index]
        values=np.asarray(evaluate(moment,*point),dtype=float)
        b0,bt,btt,u0,ut,utt,v0,vt,vtt=values[:9]
        hmat,ht,lmat,lt=values[9:45].reshape(4,3,3)
        hx=values[45:72].reshape(3,3,3)
        lx=values[72:99].reshape(3,3,3)
        ug,vg=values[99:105].reshape(2,3)
        uh,vh=values[105:123].reshape(2,3,3)
        scale=1+.2*moment
        hubble=.2/scale
        theta1t=np.trace(ht)/2
        theta2t=np.trace(lt)/2-np.trace(hmat@ht)/2
        theta1g=np.trace(hx,axis1=1,axis2=2)/2
        divergence_h=np.einsum('iij->j',hx)
        spatial=np.sum(hmat*uh)+(divergence_h-theta1g)@ug
        expected_kg=vtt+2*hubble*vt-np.trace(vh)+scale**2*mass**2*v0+theta2t*bt+theta1t*ut+spatial
        expected_energy=(bt*vt+.5*ut**2+.5*ug@ug)/scale**2+mass**2*(b0*v0+.5*u0**2)
        expected_pressure=(bt*vt+.5*ut**2-ug@ug/6)/scale**2-mass**2*(b0*v0+.5*u0**2)
        expected_current=-(bt*vg+ut*ug)/scale
        expected_anisotropy=(np.outer(ug,ug)-np.eye(3)*(ug@ug)/3)/scale**2
        expected=np.r_[expected_kg,expected_energy,expected_pressure,expected_current,expected_anisotropy.ravel()]

        def exact(amplitude):
            nonlocal minimum_eigenvalue
            metric_matrix=np.eye(3)+amplitude*hmat+amplitude**2*lmat
            minimum_eigenvalue=min(minimum_eigenvalue,float(np.linalg.eigvalsh(metric_matrix).min()))
            inverse=np.linalg.inv(metric_matrix)
            metric_time=amplitude*ht+amplitude**2*lt
            metric_space=amplitude*hx+amplitude**2*lx
            theta_time=np.trace(inverse@metric_time)/2
            theta_space=np.array([np.trace(inverse@matrix)/2 for matrix in metric_space])
            inverse_space=np.array([-inverse@matrix@inverse for matrix in metric_space])
            divergence_inverse=np.einsum('iij->j',inverse_space)
            phi=b0+amplitude*u0+amplitude**2*v0
            velocity=bt+amplitude*ut+amplitude**2*vt
            acceleration=btt+amplitude*utt+amplitude**2*vtt
            gradient=amplitude*ug+amplitude**2*vg
            hessian=amplitude*uh+amplitude**2*vh
            laplacian=np.sum(inverse*hessian)+(divergence_inverse+theta_space@inverse)@gradient
            kg=acceleration+2*hubble*velocity+theta_time*velocity-laplacian+scale**2*mass**2*phi
            gradient2=gradient@inverse@gradient
            energy=(velocity**2+gradient2)/(2*scale**2)+mass**2*phi**2/2
            pressure=(velocity**2-gradient2/3)/(2*scale**2)-mass**2*phi**2/2
            current=-velocity*gradient/scale
            anisotropy=(np.outer(inverse@gradient,gradient)-np.eye(3)*gradient2/3)/scale**2
            return np.r_[kg,energy,pressure,current,anisotropy.ravel()]

        amplitudes=np.array([.04,.02,.01,.005,.0025])
        coefficients=np.array([(exact(epsilon)+exact(-epsilon)-2*exact(0))/(2*epsilon**2) for epsilon in amplitudes])
        samples.append((expected,coefficients))
    expected=np.array([sample[0] for sample in samples])
    coefficients=np.array([sample[1] for sample in samples])
    envelopes=np.maximum(np.max(abs(expected),axis=0),1e-8)
    errors=np.max(abs(coefficients-expected[:,None,:])/envelopes[None,None,:],axis=(0,2))
    checks=[dict(name='Positive spatial metric on every probe',passed=bool(minimum_eigenvalue>0)),
        dict(name='Even Taylor extraction converges at every refinement',passed=bool(np.all(np.diff(errors)<0))),
        dict(name='Fine exact-operator coefficient error below precommitted tolerance',passed=bool(errors[-1]<1e-5))]
    assert all(check['passed'] for check in checks),(checks,errors)
    np.savez_compressed(folder/'coefficients.npz',amplitudes=amplitudes,expected=expected,
        exact_even_coefficients=coefficients,envelopes=envelopes,errors=errors)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        amplitudes=amplitudes.tolist(),envelope_errors=errors.tolist(),minimum_spatial_eigenvalue=minimum_eigenvalue,
        samples=12,coefficient_components=15,fields_manufactured_off_shell=True),__file__)
    print(json.dumps(dict(errors=errors.tolist(),checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
