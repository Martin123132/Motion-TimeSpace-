import hashlib
import itertools
import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import sympy as sp

    root = Path(__file__).resolve().parents[1]
    output = root/'source-intake/navier-stokes/20260914/annular-higher-energy-exact-algebra-attempt01'
    output.mkdir(exist_ok=False)
    source = Path(__file__)
    report = {'state':'running','checks':[],'inputs':{str(source.relative_to(root)):hashlib.sha256(source.read_bytes()).hexdigest()},
              'outputs':{},'generic_algebra_control_not_a_new_MTS_solution':True,'valid_for_physics_claim':False}

    def save():
        (output/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    snapshot = output/('executed-'+source.name)
    snapshot.write_bytes(source.read_bytes())
    report['outputs'][str(snapshot.relative_to(root))] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    coordinates = sp.symbols('position1 position2 momentum1 momentum2')
    position1,position2,momentum1,momentum2 = coordinates
    hamiltonian = sum(value**2 for value in coordinates)/2+position1**2*momentum2**2/10+sum(value**2 for value in coordinates)**2/50
    multiplier = 1+position1/5+momentum2/7
    symplectic = sp.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    gradient = sp.Matrix([sp.diff(hamiltonian,value) for value in coordinates])
    flow = multiplier*symplectic*gradient
    jacobian = flow.jacobian(coordinates)
    point = dict(zip(coordinates,[sp.Rational(1,5),sp.Rational(-1,10),sp.Rational(3,20),sp.Rational(1,4)]))
    velocity = flow.subs(point)
    acceleration = jacobian.subs(point)*velocity
    jerk = jacobian.subs(point)*acceleration+sp.Matrix([
        sum(sp.diff(component,coordinates[first],coordinates[second]).subs(point)*velocity[first]*velocity[second]
            for first in range(4) for second in range(4)) for component in flow])

    def tensor(directions):
        return sum(sp.diff(hamiltonian,*[coordinates[index] for index in indices]).subs(point)*
                   sp.prod(direction[index] for direction,index in zip(directions,indices))
                   for indices in itertools.product(range(4),repeat=len(directions)))

    log_multiplier = sp.log(multiplier)
    clock_first = sum(sp.diff(log_multiplier,coordinate).subs(point)*value for coordinate,value in zip(coordinates,velocity))
    clock_acceleration = sum(sp.diff(log_multiplier,coordinate).subs(point)*value for coordinate,value in zip(coordinates,acceleration))
    clock_second = sum(sp.diff(log_multiplier,coordinates[first],coordinates[second]).subs(point)*velocity[first]*velocity[second]
                       for first in range(4) for second in range(4))
    mixed = clock_second+clock_acceleration-clock_first**2
    tangent = tensor([velocity,velocity])/2
    tangent_rate = tensor([velocity,velocity,velocity])/2+2*clock_first*tangent
    stabilizer = sp.Rational(3)
    direct = sp.Rational(5,2)*tensor([velocity,acceleration,acceleration])+tensor([acceleration,jerk])
    direct += tensor([velocity,velocity,velocity,acceleration])+tensor([velocity,velocity,jerk])
    direct += 2*stabilizer*tangent*(tensor([velocity,velocity,velocity])/2+tensor([velocity,acceleration]))
    predicted = sp.Rational(5,2)*tensor([velocity,acceleration,acceleration])+tensor([velocity,velocity,velocity,acceleration])
    clock_terms = 2*clock_first*tensor([velocity,velocity,acceleration])+mixed*tensor([velocity,velocity,velocity])
    clock_terms += 2*clock_first*tensor([acceleration,acceleration])+mixed*tensor([acceleration,velocity])
    predicted += clock_terms+2*stabilizer*tangent*tangent_rate
    check('nonconstant_multiplier_positive',multiplier.subs(point)>0)
    check('clock_rate_nonzero',clock_first!=0)
    check('first_tangent_identity_exact',sp.cancel(tensor([velocity,acceleration])-2*clock_first*tangent)==0)
    check('higher_energy_identity_exact',sp.cancel(direct-predicted)==0)
    check('dropping_clock_terms_changes_rate',clock_terms!=0,str(clock_terms))
    report.update(state='complete',exact_residual=str(sp.cancel(direct-predicted)),
                  numerical_clock_rate=float(clock_first),numerical_omitted_clock_terms=float(clock_terms))
    save()
    print(json.dumps({'state':'complete','checks':len(report['checks']),'clock_rate':float(clock_first),
                      'omitted_clock_terms':float(clock_terms)}),flush=True)


if __name__=='__main__':
    run()

