from __future__ import annotations

from boundary_common import *


def local_connection(metric,derivatives,coordinate_velocity):
    eigenvalues,eigenvectors=np.linalg.eigh(metric)
    assert np.min(eigenvalues)>0
    roots=np.sqrt(eigenvalues)
    coframe=(eigenvectors*roots)@eigenvectors.T
    inverse_coframe=(eigenvectors/roots)@eigenvectors.T
    coframe_derivatives=np.array([eigenvectors@((eigenvectors.T@value@eigenvectors)/(roots[:,None]+roots[None,:]))@eigenvectors.T for value in derivatives])
    inverse=inverse_coframe@inverse_coframe
    spatial=np.empty((3,3,3))
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                bracket=derivatives[left+1,:,right]+derivatives[right+1,:,left]-derivatives[1:,left,right]
                spatial[upper,left,right]=inverse[upper]@bracket/2
    extrinsic=.5*inverse_coframe@derivatives[0]@inverse_coframe
    mixed=.5*inverse@derivatives[0]
    along_coframe=coframe_derivatives[0]+np.einsum('i,iab->ab',coordinate_velocity,coframe_derivatives[1:])
    along_connection=mixed+np.einsum('i,aib->ab',coordinate_velocity,spatial)
    rotation=along_coframe@inverse_coframe-coframe@along_connection@inverse_coframe
    return coframe,inverse_coframe,extrinsic,rotation


def manufactured_metric(moment,position,strength):
    matrices=np.array([[[.2,.03,.04],[.03,-.1,.02],[.04,.02,.07]],
        [[-.08,.05,-.02],[.05,.16,.03],[-.02,.03,.04]]])
    waves=np.array([[.7,.2,0.],[0.,.5,.9]])
    frequencies=np.array([.6,-.4])
    phases=waves@position+frequencies*moment
    metric=np.eye(3)+strength*np.einsum('n,nij->ij',np.sin(phases),matrices)
    wave4=np.column_stack([frequencies,waves])
    derivatives=strength*np.einsum('n,na,nij->aij',np.cos(phases),wave4,matrices)
    return metric,derivatives


def four_connection(metric,derivatives):
    full=np.zeros((4,4))
    full[0,0]=-1
    full[1:,1:]=metric
    first=np.zeros((4,4,4))
    first[:,1:,1:]=derivatives
    inverse=np.linalg.inv(full)
    connection=np.empty((4,4,4))
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                connection[upper,left,right]=inverse[upper]@(first[left,:,right]+first[right,:,left]-first[:,left,right])/2
    return full,connection


def main():
    modest()
    folder=ROOT/'results/screen-transport'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    for strength in [0.,.5,1.]:
        initial_position=np.array([.2,-.1,.3])
        initial_direction=np.array([.5,.3,.8])
        initial_direction/=np.linalg.norm(initial_direction)
        basis=linalg.null_space(initial_direction[None,:])
        initial_metric,_=manufactured_metric(.2,initial_position,strength)
        values,vectors=np.linalg.eigh(initial_metric)
        inverse_coframe=(vectors/np.sqrt(values))@vectors.T
        initial_coordinate_velocity=inverse_coframe@initial_direction
        initial_four_polarization=np.vstack([np.zeros((1,2)),inverse_coframe@basis])
        initial_four=np.r_[initial_position,1.,initial_coordinate_velocity,initial_four_polarization.ravel()]
        initial_local=np.r_[initial_position,initial_direction,0.,basis.ravel()]
        def covariant_rhs(moment,state):
            position=state[:3]
            momentum=state[3:7]
            polarization=state[7:].reshape(4,2)
            metric,derivatives=manufactured_metric(moment,position,strength)
            _,connection=four_connection(metric,derivatives)
            momentum_prime=-np.einsum('abc,b,c->a',connection,momentum,momentum)/momentum[0]
            polarization_prime=-np.einsum('abc,b,cd->ad',connection,momentum,polarization)/momentum[0]
            return np.r_[momentum[1:]/momentum[0],momentum_prime,polarization_prime.ravel()]
        def local_rhs(moment,state):
            position=state[:3]
            direction=state[3:6]
            polarization=state[7:].reshape(3,2)
            metric,derivatives=manufactured_metric(moment,position,strength)
            values,vectors=np.linalg.eigh(metric)
            inverse_coframe=(vectors/np.sqrt(values))@vectors.T
            velocity=inverse_coframe@direction
            _,_,extrinsic,rotation=local_connection(metric,derivatives,velocity)
            redshift=direction@extrinsic@direction
            direction_prime=rotation@direction-extrinsic@direction+redshift*direction
            screen_generator=rotation+np.outer(direction,direction)@extrinsic
            return np.r_[velocity,direction_prime,-redshift,(screen_generator@polarization).ravel()]
        times=np.linspace(.2,3.2,81)
        direct=integrate.solve_ivp(covariant_rhs,(times[0],times[-1]),initial_four,method='DOP853',t_eval=times,rtol=2e-11,atol=2e-13,max_step=.05)
        local=integrate.solve_ivp(local_rhs,(times[0],times[-1]),initial_local,method='DOP853',t_eval=times,rtol=2e-11,atol=2e-13,max_step=.05)
        assert direct.success and local.success
        errors=[]
        norm_errors=[]
        rotations=[]
        intensity_errors=[]
        polarization_weight=np.array([[.7,.1+.08j],[.1-.08j,.3]])
        for index,moment in enumerate(times):
            state=direct.y[:,index]
            metric,derivatives=manufactured_metric(moment,state[:3],strength)
            coordinate_velocity=state[4:7]/state[3]
            coframe,_,_,rotation=local_connection(metric,derivatives,coordinate_velocity)
            direct_direction=coframe@coordinate_velocity
            direct_polarization=state[7:].reshape(4,2)
            screen=coframe@(direct_polarization[1:]-coordinate_velocity[:,None]*direct_polarization[0])
            comparison=np.r_[state[:3],direct_direction,np.log(state[3]),screen.ravel()]
            errors.append(float(np.max(abs(comparison-local.y[:,index]))))
            polarization=local.y[7:,index].reshape(3,2)
            direction=local.y[3:6,index]
            norm_errors.append(max(abs(direction@direction-1),float(np.max(abs(direction@polarization))),float(np.max(abs(polarization.T@polarization-np.eye(2))))))
            rotations.append(float(np.max(abs(rotation+rotation.T))))
            direct_intensity=state[3]**4*screen@polarization_weight@screen.T
            local_intensity=math.exp(4*local.y[6,index])*polarization@polarization_weight@polarization.T
            intensity_errors.append(float(np.max(abs(direct_intensity-local_intensity))))
        check('Strength'+str(strength)+': exact local screen agrees with4D parallel transport',max(errors)<2e-8,error=max(errors))
        check('Strength'+str(strength)+': norm and transverse screens conserved',max(norm_errors)<2e-8,error=max(norm_errors))
        check('Strength'+str(strength)+': connection rotation antisymmetric',max(rotations)<2e-12,error=max(rotations))
        check('Strength'+str(strength)+': bolometric polarized intensity agrees',max(intensity_errors)<2e-8,error=max(intensity_errors))
        np.savez_compressed(folder/('ray-strength'+str(strength)+'.npz'),times=times,covariant=direct.y,local=local.y,errors=errors,norm_errors=norm_errors,intensity_errors=intensity_errors)
    hessian=np.array([[.2,.1,-.04],[.1,-.3,.05],[-.04,.05,.1]])
    rate=np.array([[.07,-.02,.03],[-.02,.11,-.04],[.03,-.04,-.08]])
    second=np.array([[.03,0,.01],[0,.02,-.01],[.01,-.01,-.03]])
    second_rate=np.array([[.01,.02,0],[.02,-.01,.01],[0,.01,.02]])
    expected_spin=(hessian@rate-rate@hessian)/8
    expected_shear=second_rate/2-(hessian@rate+rate@hessian)/4
    spin_errors=[]
    shear_errors=[]
    for amplitude in [.08,.04,.02,.01,.005]:
        components=[]
        for sign in [-1,1]:
            argument=sign*amplitude
            metric=np.eye(3)+argument*hessian+argument**2*second
            derivatives=np.zeros((4,3,3))
            derivatives[0]=argument*rate+argument**2*second_rate
            components.append(local_connection(metric,derivatives,np.zeros(3))[2:])
        spin=(components[0][1]+components[1][1])/(2*amplitude**2)
        shear=(components[0][0]+components[1][0])/(2*amplitude**2)
        spin_errors.append(float(np.max(abs(spin-expected_spin)))/float(np.max(abs(expected_spin))))
        shear_errors.append(float(np.max(abs(shear-expected_shear)))/float(np.max(abs(expected_shear))))
    check('Quadratic time-screen rotation is[h,hprime]/8',np.all(np.diff(spin_errors)<0) and spin_errors[-1]<1e-5,errors=spin_errors)
    check('Quadratic tetrad shear retains both matrix orders',np.all(np.diff(shear_errors)<0) and shear_errors[-1]<1e-5,errors=shear_errors)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        exact_finite_metric_transport=True,comparison_with_unfixed_four_polarization=True,
        quadratic_noncommuting_rotation_derived=True,manufactured_metric_not_a_cosmological_solution=True),__file__)
    print(json.dumps(dict(checks=len(checks),largest_ray_error=max(row['error'] for row in checks if 'parallel transport' in row['name']),spin_errors=spin_errors)),flush=True)


if __name__=='__main__':
    main()
