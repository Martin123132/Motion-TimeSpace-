from __future__ import annotations

import sympy as symbolic
from constraint_common import *


def main():
    modest()
    folder=ROOT/'results/kinetic-operator'
    folder.mkdir(parents=True,exist_ok=False)
    time,coord_x,coord_y,coord_z,momentum_x,momentum_y,momentum_z=symbolic.symbols('t x y z Qx Qy Qz',real=True)
    spatial_coordinates=[coord_x,coord_y,coord_z]
    momentum_coordinates=[momentum_x,momentum_y,momentum_z]
    coordinates=[time,*spatial_coordinates,*momentum_coordinates]
    hp=symbolic.Matrix([[.3,.04,.06],[.04,-.15,.02],[.06,.02,.1]])*(1+.2*time)
    hq=symbolic.Matrix([[-.1,.03,-.02],[.03,.25,.05],[-.02,.05,.12]])*(1-.1*time+.03*time**2)
    metric1=hp*symbolic.cos(coord_x+coord_z)+hq*symbolic.cos(coord_y+coord_z)
    metric2=symbolic.Matrix([[.02,.01,0],[.01,-.03,.01],[0,.01,.04]])*(1+time**2)*symbolic.cos(coord_x+coord_y+2*coord_z)
    occupation0=symbolic.exp(-sum(momentum**2 for momentum in momentum_coordinates)/2)
    occupation1=occupation0*((.2+.1*time)*(momentum_x+.3*momentum_y)*symbolic.cos(coord_x+coord_z)+.15*momentum_z**2*symbolic.cos(coord_y+coord_z))
    occupation2=occupation0*(.03*time+.04*momentum_x*momentum_y)*symbolic.cos(coord_x+coord_y+2*coord_z)
    expressions=list(metric1)+list(metric2)
    expressions+=[entry for matrix in [metric1,metric2] for coordinate in spatial_coordinates for entry in matrix.diff(coordinate)]
    for occupation in [occupation0,occupation1,occupation2]:
        expressions.append(occupation)
        expressions+=[symbolic.diff(occupation,coordinate) for coordinate in coordinates]
    evaluate=symbolic.lambdify(coordinates,expressions,'numpy',cse=True)
    amplitudes=np.array([.04,.02,.01,.005,.0025])
    samples=[]
    for mass in [0.,.8,3.]:
        for index in range(8):
            moment=.1+.07*index
            momentum=np.array([.6+.04*index,-.3+.06*index,.9-.03*index])
            point=[moment,.17+.19*index,.31+.11*index,.27-.09*index,*momentum]
            values=np.asarray(evaluate(*point),float)
            hmat,lmat=values[:18].reshape(2,3,3)
            hx,lx=values[18:72].reshape(2,3,3,3)
            f0,f1,f2=values[72:].reshape(3,8)
            scale=1+.2*moment
            energy0=math.sqrt(momentum@momentum+(scale*mass)**2)
            projected=momentum@hmat@momentum
            energy1=-projected/(2*energy0)
            energy2=momentum@(hmat@hmat-lmat)@momentum/(2*energy0)-projected**2/(8*energy0**3)
            velocity1=-hmat@momentum/energy0+projected*momentum/(2*energy0**3)
            force1=np.array([-momentum@matrix@momentum/(2*energy0) for matrix in hx])
            force2=np.array([momentum@(hx[axis]@hmat+hmat@hx[axis]-lx[axis])@momentum/(2*energy0)-projected*(momentum@hx[axis]@momentum)/(4*energy0**3) for axis in range(3)])
            liouville2=f2[1]+(momentum/energy0)@f2[2:5]+velocity1@f1[2:5]-force1@f1[5:8]-force2@f0[5:8]
            theta1=np.trace(hmat)/2
            theta2=np.trace(lmat)/2-np.trace(hmat@hmat)/4
            determinant2=theta1**2/2-theta2
            density2=(energy0*f2[0]+energy1*f1[0]+energy2*f0[0]-theta1*(energy0*f1[0]+energy1*f0[0])+determinant2*energy0*f0[0])/scale**4
            current2=momentum*(f2[0]-theta1*f1[0]+determinant2*f0[0])/scale**3
            tensor0=np.outer(momentum,momentum)/energy0
            tensor1=-np.outer(hmat@momentum,momentum)/energy0-np.outer(momentum,momentum)*energy1/energy0**2
            tensor2=np.outer((hmat@hmat-lmat)@momentum,momentum)/energy0+np.outer(hmat@momentum,momentum)*energy1/energy0**2+np.outer(momentum,momentum)*(energy1**2/energy0**3-energy2/energy0**2)
            stress2=(tensor0*f2[0]+tensor1*f1[0]+tensor2*f0[0]-theta1*(tensor0*f1[0]+tensor1*f0[0])+determinant2*tensor0*f0[0])/scale**4
            expected=np.r_[energy2,liouville2,density2,current2,stress2.ravel()]
            def exact(epsilon):
                spatial=np.eye(3)+epsilon*hmat+epsilon**2*lmat
                inverse=np.linalg.inv(spatial)
                inverse_space=np.array([-inverse@(epsilon*hx[axis]+epsilon**2*lx[axis])@inverse for axis in range(3)])
                energy=math.sqrt(momentum@inverse@momentum+(scale*mass)**2)
                velocity=inverse@momentum/energy
                force=np.array([momentum@matrix@momentum/(2*energy) for matrix in inverse_space])
                occupation=f0+epsilon*f1+epsilon**2*f2
                liouville=occupation[1]+velocity@occupation[2:5]-force@occupation[5:8]
                determinant=np.linalg.det(spatial)**-.5
                density=determinant*energy*occupation[0]/scale**4
                current=determinant*momentum*occupation[0]/scale**3
                stress=determinant*np.outer(inverse@momentum,momentum)*occupation[0]/(scale**4*energy)
                return np.r_[energy,liouville,density,current,stress.ravel()]
            coefficients=np.array([(exact(epsilon)+exact(-epsilon)-2*exact(0))/(2*epsilon**2) for epsilon in amplitudes])
            samples.append((expected,coefficients))
    expected=np.array([row[0] for row in samples])
    coefficients=np.array([row[1] for row in samples])
    envelope=np.maximum(np.max(abs(expected),axis=0),1e-8)
    errors=np.max(abs(coefficients-expected[:,None,:])/envelope[None,None,:],axis=(0,2))
    checks=[dict(name='Massless and massive phase-space operators and stresses converge',passed=bool(np.all(np.diff(errors)<0))),
        dict(name='Fine kinetic expansion error below1e-5',passed=bool(errors[-1]<1e-5))]
    assert all(row['passed'] for row in checks),(checks,errors)
    np.savez_compressed(folder/'coefficients.npz',expected=expected,coefficients=coefficients,errors=errors,amplitudes=amplitudes,envelopes=envelope)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,quadratic_envelope_errors=errors.tolist(),
        samples=24,components=15,masses=[0.,.8,3.],manufactured_distribution_off_shell=True,
        determinant_and_momentum_derivative_terms_included=True),__file__)
    print(json.dumps(dict(kinetic_errors=errors.tolist())),flush=True)


if __name__=='__main__':
    main()
