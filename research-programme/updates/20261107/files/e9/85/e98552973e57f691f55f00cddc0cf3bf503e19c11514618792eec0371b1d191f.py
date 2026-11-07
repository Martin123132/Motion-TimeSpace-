from initial_state import *
from diagnostics import *


def main():
    modest()
    folder=ROOT/'results/kernels'
    folder.mkdir(parents=True,exist_ok=False)
    system=CoupledSystem(Background('heavy'),8)
    moment,state,projection=initial_state(system,1e-6)
    generator=np.random.default_rng(69007)
    direction,screen=system.directions,system.screen
    checks=[]
    def check(name,value,gate):
        checks.append(dict(name=name,value=float(value),gate=gate,passed=bool(value<gate)))
    for component in range(3):
        expected=np.eye(3)[component]-direction[:,component,None]*direction
        check('Surface gradient of Cartesian direction '+str(component),np.max(abs(system.angular.gradient(direction[:,component])-expected)),1e-12)
    for trial in range(4):
        tensor=generator.normal(size=(3,3))*.01
        tensor=(tensor+tensor.T)/2
        photon=screen@tensor@screen+(direction@generator.normal(size=3)*.005)[:,None,None]*screen
        velocity=generator.normal(size=3)*.02
        density=float(generator.normal()*.02)
        source=system.collision_quadratic(photon,velocity,density)
        energy,flux,stress=system.angular.moments(photon)
        output=system.angular.moments(source)
        expected_energy=-velocity@flux+4*velocity@velocity/3
        expected_flux=density*(-flux+4*velocity/3)+energy*velocity+stress@velocity
        check('Collision energy/work identity '+str(trial),abs(output[0]-expected_energy),1e-13)
        check('Collision momentum/force identity '+str(trial),np.max(abs(output[1]-expected_flux)),1e-13)
        amplitude=.001
        zeroth=screen/2
        positive=collision.exact_collision(direction,system.weights,zeroth+amplitude*photon,amplitude*velocity,1+amplitude*density)
        negative=collision.exact_collision(direction,system.weights,zeroth-amplitude*photon,-amplitude*velocity,1-amplitude*density)
        baseline=collision.exact_collision(direction,system.weights,zeroth,np.zeros(3))
        finite=(positive+negative-2*baseline)/(2*amplitude**2)
        check('Independent exact boosted collision expansion '+str(trial),np.max(abs(source-finite))/max(np.max(abs(source)),1e-30),1e-5)
    check('Initial Einstein constraint projection',np.max(abs(system.constraints(moment,state))),1e-12)
    wards=[]
    for step in [1e-4,1e-5,1e-6]:
        result=ward_identity(system,moment,state,step)
        wards.append(dict(step=step,**result))
        check('Initial matter-radiation Ward identity step '+str(step),np.max(result['residuals']),2e-7)
    derivative=system.slow_rhs(moment,state)+system.collision_rhs(moment,state)
    constraint_derivatives=[]
    for fraction in [1e-4,1e-5,1e-6]:
        step=fraction*moment
        slope=(system.constraints(moment+step,state+step*derivative)-system.constraints(moment-step,state-step*derivative))/(2*step)
        constraint_derivatives.append(dict(relative_step=fraction,absolute_values=abs(slope).tolist()))
    check('Constraint tangent Hamiltonian',np.max(np.array(constraint_derivatives[-1]['absolute_values'])[:,0]),1e-7)
    check('Constraint tangent momentum',np.max(np.array(constraint_derivatives[-1]['absolute_values'])[:,1:]),1e-7)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        wards=wards,projection=projection,constraint_derivatives=constraint_derivatives),__file__,[ROOT/'coupled_system.py',ROOT/'initial_state.py',ROOT/'diagnostics.py'])
    print(json.dumps(dict(checks=len(checks),failures=[row for row in checks if not row['passed']],constraint_derivatives=constraint_derivatives)),flush=True)


if __name__=='__main__':
    main()
