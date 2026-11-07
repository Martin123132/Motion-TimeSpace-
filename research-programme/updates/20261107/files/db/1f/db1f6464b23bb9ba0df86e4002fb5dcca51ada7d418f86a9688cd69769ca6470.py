from __future__ import annotations

import sympy as symbolic
from constraint_common import *


def main():
    modest()
    folder=ROOT/'results/geometry'
    folder.mkdir(parents=True,exist_ok=False)
    time,coord_x,coord_y,coord_z=symbolic.symbols('t x y z',real=True)
    coordinates=[time,coord_x,coord_y,coord_z]
    hp=symbolic.Matrix([[.3,.04,.06],[.04,-.15,.02],[.06,.02,.1]])*(1+.2*time)
    hq=symbolic.Matrix([[-.1,.03,-.02],[.03,.25,.05],[-.02,.05,.12]])*(1-.1*time+.03*time**2)
    first_metric=hp*symbolic.cos(coord_x+coord_z)+hq*symbolic.cos(coord_y+coord_z)
    second_metric=symbolic.Matrix([[.02,.01,0],[.01,-.03,.01],[0,.01,.04]])*(1+time**2)*symbolic.cos(coord_x+coord_y+2*coord_z)+symbolic.eye(3)*.015*time
    expressions=[]
    for matrix in [first_metric,second_metric]:
        expressions+=list(matrix)
        expressions+=[entry for coordinate in coordinates for entry in matrix.diff(coordinate)]
        expressions+=[entry for first in coordinates for second in coordinates for entry in matrix.diff(first,second)]
    evaluate=symbolic.lambdify(coordinates,expressions,'numpy',cse=True)
    amplitudes=np.array([.04,.02,.01,.005,.0025])
    comparisons=[]
    maximum_exact_error=0.
    for index in range(8):
        moment=.1+.09*index
        point=[moment,.17+.19*index,.31+.11*index,.27-.09*index]
        values=np.asarray(evaluate(*point),float).reshape(2,189)
        hmat,lmat=values[:,:9].reshape(2,3,3)
        dh,dl=values[:,9:45].reshape(2,4,3,3)
        ddh,ddl=values[:,45:].reshape(2,4,4,3,3)
        scale=1+.2*moment
        hubble=.2/scale
        hubble_prime=-hubble**2
        ricci1,ricci2,gamma1=ricci_series(hmat,dh[1:],ddh[1:,1:])
        ricci_l,_,_=ricci_series(lmat,dl[1:],ddl[1:,1:])
        expansion1=dh[0]/2
        expansion2=(dl[0]-hmat@dh[0])/2
        expansion2_prime=(ddl[0,0]-dh[0]@dh[0]-hmat@ddh[0,0])/2
        expansion2_space=np.array([(ddl[0,axis]-dh[axis]@dh[0]-hmat@ddh[0,axis])/2 for axis in range(1,4)])
        theta1=np.trace(expansion1)
        theta2=np.trace(expansion2)
        ham2=np.trace(ricci_l+ricci2)+4*hubble*theta2+theta1**2-np.trace(expansion1@expansion1)
        mom2=np.trace(expansion2_space,axis1=1,axis2=2)-np.einsum('jji->i',expansion2_space)
        for component in range(3):
            mom2[component]+=sum(-gamma1[other,other,middle]*expansion1[middle,component]+gamma1[middle,other,component]*expansion1[other,middle] for other in range(3) for middle in range(3))
        spatial2=ricci_l+ricci2+hubble*theta2*np.eye(3)+expansion2_prime+2*hubble*expansion2+theta1*expansion1
        expected=np.r_[ham2,mom2,spatial2.ravel()]

        def exact(epsilon):
            nonlocal maximum_exact_error
            spatial=np.eye(3)+epsilon*hmat+epsilon**2*lmat
            dspace=epsilon*dh+epsilon**2*dl
            ddspace=epsilon*ddh+epsilon**2*ddl
            metric=np.zeros((4,4))
            metric[0,0]=-scale**2
            metric[1:,1:]=scale**2*spatial
            first=np.zeros((4,4,4))
            second=np.zeros((4,4,4,4))
            first[0,0,0]=-2*scale*.2
            second[0,0,0,0]=-2*.2**2
            for left in range(4):
                first[left,1:,1:]=scale**2*dspace[left]+(2*scale*.2*spatial if left==0 else 0)
                for right in range(4):
                    second[left,right,1:,1:]=scale**2*ddspace[left,right]
                    if left==0:
                        second[left,right,1:,1:]+=2*scale*.2*dspace[right]
                    if right==0:
                        second[left,right,1:,1:]+=2*scale*.2*dspace[left]
                    if left==right==0:
                        second[left,right,1:,1:]+=2*.2**2*spatial
            _,ricci4=connection_ricci(metric,first,second)
            ricci_scalar4=np.trace(np.linalg.inv(metric)@ricci4)
            einstein4=ricci4-metric*ricci_scalar4/2
            gamma,ricci3=connection_ricci(spatial,dspace[1:],ddspace[1:,1:])
            inverse=np.linalg.inv(spatial)
            expansion=inverse@dspace[0]/2
            expansion_prime=inverse@ddspace[0,0]/2-inverse@dspace[0]@inverse@dspace[0]/2
            expansion_space=np.array([inverse@ddspace[0,axis]/2-inverse@dspace[axis]@inverse@dspace[0]/2 for axis in range(1,4)])
            theta=np.trace(expansion)
            ham=np.trace(inverse@ricci3)+4*hubble*theta+theta**2-np.trace(expansion@expansion)
            mom=np.trace(expansion_space,axis1=1,axis2=2)-np.einsum('jji->i',expansion_space)
            for component in range(3):
                mom[component]+=sum(-gamma[other,other,middle]*expansion[middle,component]+gamma[middle,other,component]*expansion[other,middle] for other in range(3) for middle in range(3))
            spatial_ricci=inverse@ricci3+(hubble_prime+2*hubble**2+hubble*theta)*np.eye(3)+expansion_prime+(2*hubble+theta)*expansion
            errors=np.r_[ham-(2*einstein4[0,0]-6*hubble**2),mom+einstein4[0,1:],(spatial_ricci-inverse@ricci4[1:,1:]).ravel()]
            maximum_exact_error=max(maximum_exact_error,float(np.max(abs(errors))))
            return np.r_[2*einstein4[0,0]-6*hubble**2,-einstein4[0,1:],(inverse@ricci4[1:,1:]).ravel()]

        coefficients=np.array([(exact(epsilon)+exact(-epsilon)-2*exact(0))/(2*epsilon**2) for epsilon in amplitudes])
        comparisons.append((expected,coefficients))
    expected=np.array([row[0] for row in comparisons])
    coefficients=np.array([row[1] for row in comparisons])
    envelopes=np.maximum(np.max(abs(expected),axis=0),1e-8)
    errors=np.max(abs(coefficients-expected[:,None,:])/envelopes[None,None,:],axis=(0,2))
    checks=[dict(name='Hamiltonian/momentum/spatial Ricci agree with direct4D geometry',passed=maximum_exact_error<2e-13),
        dict(name='All13 quadratic geometric components converge',passed=bool(np.all(np.diff(errors)<0))),
        dict(name='Finest quadratic geometric coefficient error below1e-5',passed=bool(errors[-1]<1e-5))]
    assert all(row['passed'] for row in checks),(checks,errors)
    np.savez_compressed(folder/'coefficients.npz',expected=expected,coefficients=coefficients,errors=errors,amplitudes=amplitudes,envelopes=envelopes)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        maximum_direct_geometry_error=maximum_exact_error,quadratic_envelope_errors=errors.tolist(),
        samples=8,components=13,nonparallel_metric=True),__file__)
    print(json.dumps(dict(direct_error=maximum_exact_error,quadratic_errors=errors.tolist())),flush=True)


if __name__=='__main__':
    main()
