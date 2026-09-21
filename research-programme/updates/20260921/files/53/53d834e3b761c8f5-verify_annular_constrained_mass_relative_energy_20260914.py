import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def radial_mass_jets(system, geometry, direction):
    import numpy as np
    from scipy.integrate import solve_ivp
    from annular_constrained_mass_relative_energy_20260914 import phase_direction
    from annular_finite_width_bulk_current_20260913 import shape_weight

    seed = np.zeros(4)
    for piece in geometry.pieces:
        lower, upper = piece['lower'], piece['upper']
        if piece['gap']:
            continue
        node = int(np.argmin(abs(system.radii-(lower+upper)/2)))
        rule = system.radial_rule
        radius = (lower+upper)/2+(upper-lower)*rule.points/2
        offsets = (radius-system.radii[node])/system.width
        data = geometry.scalar(offsets)
        scalar, momentum = phase_direction(system,direction,offsets)
        amplitude = scalar @ system.factors.T
        measure = shape_weight(offsets,system.shape)/system.width
        density = measure*data['potential'][:,node]
        linear = measure*radius**2*((data['A']*amplitude) @ system.sampling[:,node])/system.spacing
        quadratic = measure*radius**2*(amplitude**2 @ system.sampling[:,node])/(2*system.spacing)
        if node<len(system.radii)-1:
            density += measure*system.node_weights[node]*data['p'][:,node]**2/(2*radius**2)
            linear += measure*system.node_weights[node]*data['p'][:,node]*momentum[:,node]/radius**2
            quadratic += measure*system.node_weights[node]*momentum[:,node]**2/(2*radius**2)
            reservoir = np.zeros(len(radius))
        else:
            reservoir = measure*data['energy']
        coefficients = rule.inverse @ np.column_stack([density,linear,quadratic,reservoir])

        def equation(location, values):
            density, linear, quadratic, reservoir = np.polynomial.chebyshev.chebval((2*location-lower-upper)/(upper-lower),coefficients)
            root = geometry.metric(np.array([location]))['U'][0]
            first, second, third, unused_clock = values
            coupling = system.coupling
            damping = coupling*(2*density/location+reservoir/(location*root))
            first_rate = -damping*first+coupling*root**2*linear
            second_rate = -damping*second+2*coupling*root**2*quadratic
            second_rate -= 4*coupling*first*linear/location+coupling*reservoir*first**2/(location**2*root**3)
            third_rate = -damping*third-6*coupling*(second*linear+2*first*quadratic)/location
            third_rate -= 3*coupling*reservoir*first*second/(location**2*root**3)
            third_rate -= 3*coupling*reservoir*first**3/(location**3*root**5)
            clock_rate = coupling*(2*linear/location+reservoir*first/(location**2*root**3)) if lower>=system.radii[-1]-1e-12 else 0.
            return np.array([first_rate,second_rate,third_rate,clock_rate])

        solution = solve_ivp(equation,(lower,upper),seed,method='DOP853',rtol=2e-11,atol=2e-14,max_step=(upper-lower)/4)
        if not solution.success:
            raise RuntimeError(solution.message)
        seed = solution.y[:,-1]
    return np.append(seed[:3]/system.coupling,seed[3])


def run():
    limit_process()
    import numpy as np
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution
    from annular_constrained_mass_relative_energy_20260914 import (
        uniform_constants,density_energy,mass_gradient,mass_hessian,outer_data)

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    output = intake/'annular-constrained-mass-relative-energy-independent-attempt01'
    output.mkdir(exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
              'unconditional_uniform_convergence':False,'full_GR_limit_proven':False,'valid_for_physics_claim':False}

    def save():
        (output/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    save()
    try:
        main_path = intake/'annular-constrained-mass-relative-energy-attempt01/status.json'
        main = json.loads(main_path.read_text())
        check('main_complete',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in main[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed evidence: '+filename)
                report['inputs'][filename] = expected
        own(main_path)
        own(Path(__file__))
        compile(Path(__file__).read_bytes(),str(Path(__file__)),'exec')
        snapshot = output/('executed-'+Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        check('inherited_hashes_match_and_verifier_compiles',True)
        constants = uniform_constants()
        for count in [33,65,129]:
            system = CompatibleEvolution(count,False)
            archive_path = intake/'annular-compatible-h-evolution-main-attempt01'/('GR_control_count'+str(count)+'.npz')
            with np.load(archive_path,allow_pickle=False) as archive:
                time = float(archive['times'][-1])
                state = archive['states'][-1].copy()
            velocity = system.rhs(time,state)
            geometry = system.geometry(time,state)
            tangent_energy = float(density_energy(system,velocity))
            first,second,third,clock_rate = radial_mass_jets(system,geometry,velocity)
            step = 1e-20
            moved = system.geometry(time,state+1j*step*velocity)
            complex_first = outer_data(moved)[0].imag/step
            complex_second = mass_hessian(system,time,state,velocity,velocity)
            complex_clock = np.log(outer_data(moved)[1]).imag/step
            label = 'count'+str(count)
            check(label+'_independent_radial_first_variation',abs(first-complex_first)<1e-10,float(abs(first-complex_first)))
            check(label+'_independent_radial_second_variation',abs(second-complex_second)<1e-8,float(abs(second-complex_second)))
            check(label+'_independent_internal_clock_variation',abs(clock_rate-complex_clock)<1e-10,float(abs(clock_rate-complex_clock)))
            check(label+'_third_variation_uniform_energy_bound',abs(third)<=constants['phase_third']*tangent_energy**1.5+1e-8)
            finite_thirds = []
            tangent_rates = []
            acceleration = system.rhs(time,state+1j*step*velocity).imag/step
            for increment in [2e-5,1e-5]:
                plus = mass_hessian(system,time,state+increment*velocity,velocity,velocity)
                minus = mass_hessian(system,time,state-increment*velocity,velocity,velocity)
                finite_thirds.append(float((plus-minus)/(2*increment)))
                plus_velocity = velocity+increment*acceleration
                minus_velocity = velocity-increment*acceleration
                plus_tangent = .5*mass_hessian(system,time,state+increment*velocity,plus_velocity,plus_velocity)
                minus_tangent = .5*mass_hessian(system,time,state-increment*velocity,minus_velocity,minus_velocity)
                tangent_rates.append(float((plus_tangent-minus_tangent)/(2*increment)))
            check(label+'_third_variation_finite_difference',abs(finite_thirds[-1]-third)<2e-6,
                  {'radial':float(third),'finite':finite_thirds})
            tangent = second/2
            tangent_predicted = third/2+2*clock_rate*tangent
            check(label+'_live_tangent_energy_identity',abs(tangent_rates[-1]-tangent_predicted)<2e-6,
                  {'predicted':float(tangent_predicted),'finite':tangent_rates})
            check(label+'_reference_Riccati_bound',abs(tangent_predicted)<=constants['tangent_rate']*max(0.,tangent)**1.5+1e-8)
            gradient32 = mass_gradient(system,geometry,velocity,32)
            gradient48 = mass_gradient(system,geometry,velocity,48)
            check(label+'_independent_layer_quadrature',abs(gradient32-gradient48)<1e-10)
            energy48 = density_energy(system,velocity,order=48)
            check(label+'_reference_rate_energy_quadrature',abs(energy48-tangent_energy)<1e-9)
            row = dict(count=count,time=time,radial_jets=[float(first),float(second),float(third)],
                       first_error=float(abs(first-complex_first)),second_error=float(abs(second-complex_second)),
                       clock_error=float(abs(clock_rate-complex_clock)),finite_thirds=finite_thirds,
                       third_error=float(abs(finite_thirds[-1]-third)),tangent_rates=tangent_rates,
                       tangent_predicted=float(tangent_predicted),tangent_error=float(abs(tangent_rates[-1]-tangent_predicted)))
            report['cases'].append(row)
            save()
            print(json.dumps(row),flush=True)
        check('local_tangent_comparison_not_promoted_to_full_saved_interval',constants['uniform_tangent_comparison_time']<.06)
        report['state'] = 'complete'
        save()
        print(json.dumps({'state':'complete','checks':len(report['checks'])}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

