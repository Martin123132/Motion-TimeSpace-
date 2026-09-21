import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from scipy.integrate import solve_ivp
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution
    from annular_constrained_mass_relative_energy_20260914 import quadrature,phase_direction
    from annular_reference_wave_decoupling_20260914 import (
        extended_constants,reference_acceleration,MassJet,higher_energy,flux_control)
    from verify_annular_constrained_mass_relative_energy_20260914 import radial_mass_jets
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_reference_wave_quadrature_20260914 import root_split_variation_norm

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    output = intake/'annular-reference-wave-decoupling-independent-attempt02'
    output.mkdir(exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],'boundary_cases':[],
              'full_GR_limit_proven':False,'valid_for_physics_claim':False,'continuum_GR_identified':False}

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
        main_path = intake/'annular-reference-wave-decoupling-attempt01/status.json'
        main = json.loads(main_path.read_text())
        check('main_complete',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in main[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed evidence: '+filename)
                report['inputs'][filename] = expected
        own(main_path)
        own(Path(__file__))
        own(root/'scripts/annular_reference_wave_quadrature_20260914.py')
        compile(Path(__file__).read_bytes(),str(Path(__file__)),'exec')
        snapshot = output/('executed-'+Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        check('all_inherited_hashes_match_and_verifier_compiles',True)
        constants = extended_constants()
        coordinate = sp.symbols('coordinate',real=True)
        reciprocal = 1/(1-coordinate**2)
        bump = sp.exp(1-reciprocal)
        third_formula = bump*(-8*coordinate**3*reciprocal**6+48*coordinate**3*reciprocal**5
            -48*coordinate**3*reciprocal**4+12*coordinate*reciprocal**4-24*coordinate*reciprocal**3)
        check('analytic_bump_third_derivative_identity',sp.simplify(sp.diff(bump,coordinate,3)-third_formula)==0)
        for count in [33,65,129]:
            system = CompatibleEvolution(count,False)
            archive_path = intake/'annular-compatible-h-evolution-main-attempt01'/('GR_control_count'+str(count)+'.npz')
            with np.load(archive_path,allow_pickle=False) as archive:
                time,state = float(archive['times'][-1]),archive['states'][-1].copy()
            velocity,acceleration = reference_acceleration(system,time,state)
            geometry = system.geometry(time,state)
            jet = MassJet(system,geometry,velocity,acceleration)
            higher,terms = higher_energy(jet,constants)
            independent = radial_mass_jets(system,geometry,velocity)
            label = 'count'+str(count)
            check(label+'_independent_second_mass_derivative',abs(jet.derivative(2,0)-independent[1])<1e-8)
            check(label+'_independent_third_mass_derivative',abs(jet.derivative(3,0)-independent[2])<1e-8)
            increment = 1e-5
            plus_third = radial_mass_jets(system,system.geometry(time,state+increment*velocity),velocity)[2]
            minus_third = radial_mass_jets(system,system.geometry(time,state-increment*velocity),velocity)[2]
            fourth_fd = float((plus_third-minus_third)/(2*increment))
            fourth_error = abs(fourth_fd-jet.derivative(4,0))
            check(label+'_independent_fourth_mass_derivative',fourth_error<2e-5,
                {'radial':float(jet.derivative(4,0)),'finite':fourth_fd,'error':float(fourth_error)})
            numerical_rates = []
            for duration in [1e-4,5e-5]:
                values = []
                for sign in [-1,1]:
                    solution = solve_ivp(system.rhs,(time,time+sign*duration),state,method='DOP853',
                        rtol=2e-12,atol=2e-14,max_step=duration/2)
                    if not solution.success:
                        raise RuntimeError(solution.message)
                    moved = solution.y[:,-1]
                    moved_time = time+sign*duration
                    moved_velocity,moved_acceleration = reference_acceleration(system,moved_time,moved)
                    moved_jet = MassJet(system,system.geometry(moved_time,moved),moved_velocity,moved_acceleration)
                    values.append(higher_energy(moved_jet,constants)[0])
                numerical_rates.append(float((values[1]-values[0])/(2*duration)))
            rate_error = abs(numerical_rates[-1]-terms.sum())
            check(label+'_higher_energy_live_time_derivative',rate_error<max(1e-3,1e-5*abs(terms.sum())),
                {'predicted':float(terms.sum()),'finite':numerical_rates,'error':float(rate_error)})
            check(label+'_higher_energy_time_refinement',abs(numerical_rates[-1]-numerical_rates[0])<2e-3)
            first = flux_control(system,time,state,velocity,acceleration,constants,32)
            second = flux_control(system,time,state,velocity,acceleration,constants,48)
            quadrature_error = max(abs(first[name]-second[name]) for name in
                ['velocity_energy','acceleration_energy','Gram_velocity_energy','gradient_variation_norm'])
            coarse_quadrature_error = quadrature_error
            refined,segments = root_split_variation_norm(system,velocity,12)
            confirmation,unused_segments = root_split_variation_norm(system,velocity,16)
            quadrature_error = max(abs(refined-confirmation),max(abs(first[name]-second[name]) for name in
                ['velocity_energy','acceleration_energy','Gram_velocity_energy']))
            check(label+'_root_split_layer_quadrature_refinement',quadrature_error<1e-7,
                {'resolved_error':float(quadrature_error),'coarse32vs48_error':float(coarse_quadrature_error),'segments':segments})
            check(label+'_root_split_BV_Gram_bound',second['Gram_velocity_energy']<=
                constants['radius_upper']**2*system.spacing*confirmation**2/4+1e-10)
            report['cases'].append(dict(count=count,fourth_error=float(fourth_error),
                higher_rate=float(terms.sum()),finite_rates=numerical_rates,rate_error=float(rate_error),
                quadrature_error=float(quadrature_error),coarse_quadrature_error=float(coarse_quadrature_error),
                root_split_variation_norm=confirmation,root_split_segments=segments))
            save()
            print(json.dumps(report['cases'][-1]),flush=True)

        system = CompatibleEvolution(33,False)
        values,inner = system.unpack(system.initial_state)
        values = values.copy()
        fraction = system.radii-5
        radius = system.radii[None,:]+system.width*system.grid.offsets[:,None]
        values[:,:32] = .005*np.cos(np.pi*fraction[:-1]/2)
        values[:,32:64] = .003*radius[:,:-1]**2*np.sin(np.pi*fraction[:-1])
        state = system.pack(values,inner)
        velocity,acceleration = reference_acceleration(system,0.,state)
        control = flux_control(system,0.,state,velocity,acceleration,constants)
        offsets,weights = quadrature(32)
        data = system.geometry(0.,state).layer(offsets)
        unused_scalar,p_rate = phase_direction(system,velocity,offsets)
        coefficient = (data['C'][:,:-1]+data['C'][:,1:])/2
        correct_flux = coefficient*np.diff(data['chi'],axis=1)/system.spacing
        wrong_weights = system.node_weights.copy()
        wrong_weights[0] = system.spacing
        wrong_flux = np.cumsum(wrong_weights[:-1]*p_rate[:,:-1],axis=1)
        wrong_endpoint_error = float(abs(wrong_flux-correct_flux).max())
        check('manufactured_endpoint_correct_flux',control['flux_error']<2e-10)
        check('manufactured_endpoint_wrong_half_weight_rejected',wrong_endpoint_error>1e-7,wrong_endpoint_error)
        report['manufactured_endpoint_wrong_weight_error'] = wrong_endpoint_error

        for count in [33,65,129,257]:
            spacing = 1/(count-1)
            node_coefficient = np.ones(count)
            node_coefficient[-1] = .9
            edge_coefficient = (node_coefficient[:-1]+node_coefficient[1:])/2
            flux = (np.arange(count-1)+.5)*spacing
            scalar = np.zeros(count)
            scalar[:-1] = -spacing*np.cumsum((flux/edge_coefficient)[::-1])[::-1]
            factors,sampling = gram_matrices(count)
            radius = np.linspace(5.,6.,count)
            extra = float(((radius**2 @ sampling.T)*(scalar @ factors.T)**2).sum()/(2*spacing))
            gradient_variation = float(abs(np.diff(flux/edge_coefficient)).sum())
            bound = 6.1**2*spacing*gradient_variation**2/4
            check('BV_corner_count'+str(count)+'_bound',0<extra<=bound)
            report['boundary_cases'].append({'count':count,'spacing':spacing,'extra_energy':extra,'energy_over_h':extra/spacing,'bound':bound})
        orders = [float(np.log(first['extra_energy']/second['extra_energy'])/np.log(2.))
                  for first,second in zip(report['boundary_cases'][:-1],report['boundary_cases'][1:])]
        report['boundary_orders'] = orders
        check('BV_corner_shows_first_order_not_fourth',abs(orders[-1]-1)<.03)
        check('conservative_time_window_not_extended_by_numerics',constants['uniform_tangent_comparison_time']<.06)
        report['state'] = 'complete'
        save()
        print(json.dumps({'state':'complete','checks':len(report['checks']),'boundary_orders':orders}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()



