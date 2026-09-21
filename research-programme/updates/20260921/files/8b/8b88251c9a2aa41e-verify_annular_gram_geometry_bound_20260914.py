import hashlib
import json
import traceback
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as symbolic
    from annular_gram_geometry_bound_20260914 import MatchedConstraintSystem, IndependentRadialPair, analytic_constants
    from annular_horizontal_clock_evolution_20260913 import PolarGeometry

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    main_dir = intake/'annular-gram-geometry-bound-attempt01'
    output = intake/'annular-gram-geometry-bound-independent-attempt01'
    output.mkdir(exist_ok=False)
    report = {'state':'running', 'checks':[], 'inputs':{}, 'outputs':{}, 'cases':[],
              'full_GR_limit_proven':False, 'dynamical_h_family_evolved':False,
              'uniform_H3_solution_bound_proven':False, 'valid_for_physics_claim':False}

    def save():
        (output/'status.json').write_text(json.dumps(report, indent=2)+'\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name':name, 'passed':bool(passed), 'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    class ExplicitDensityFamily(MatchedConstraintSystem):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            size = len(self.radii)-3
            diagonal = np.full(size, 5/72)
            diagonal[:3] = [59097/573104, 1825/25284, 491/7056]
            diagonal[-3:] = diagonal[:3][::-1]
            self.adjacent = np.full(size-1, -1/144)
            self.adjacent[:2] = [253/50568, -3/392]
            self.adjacent[-2:] = self.adjacent[:2][::-1]
            self.margins = diagonal.copy()
            self.margins[:-1] -= abs(self.adjacent)
            self.margins[1:] -= abs(self.adjacent)
            self.extra_edges = [(0,2,-1/392), (size-3,size-1,-1/392)]
            for first, second, weight in self.extra_edges:
                self.margins[first] -= abs(weight)
                self.margins[second] -= abs(weight)

        def density_parts(self, offsets):
            offsets = np.asarray(offsets).reshape(-1)
            radius = self.radii[None,:]+self.width*offsets[:,None]
            coordinate = radius-5.
            if self.profile == 'smooth':
                scalar = .04*np.sin(2*np.pi*coordinate)+.005*coordinate**3
            else:
                scalar = np.broadcast_to(.04*self.spacing*(-1.)**np.arange(len(self.radii)), radius.shape)
            velocity = .012*(1+.2*np.cos(np.pi*coordinate))
            base_nodal = np.zeros_like(radius)
            differences = scalar[:,1:]-scalar[:,:-1]
            base_nodal[:,:-1] += differences**2/2
            base_nodal[:,1:] += differences**2/2
            third = scalar[:,3:]-3*scalar[:,2:-1]+3*scalar[:,1:-2]-scalar[:,:-3]
            extra_nodal = np.zeros_like(radius)
            size = len(self.radii)-3
            diagonal_energy = self.margins[None,:]*third**2
            extra_nodal[:,1:size+1] += diagonal_energy/2
            extra_nodal[:,2:size+2] += diagonal_energy/2
            edge_energy = abs(self.adjacent)[None,:]*(third[:,:-1]+np.sign(self.adjacent)[None,:]*third[:,1:])**2
            extra_nodal[:,2:size+1] += edge_energy
            for first, second, weight in self.extra_edges:
                position = (first+second)/2+1.5
                left = int(np.floor(position))
                fraction = position-left
                energy = abs(weight)*(third[:,first]+np.sign(weight)*third[:,second])**2
                extra_nodal[:,left] += (1-fraction)*energy
                extra_nodal[:,left+1] += fraction*energy
            base = radius**2*base_nodal/(2*self.spacing)
            free_kinetic = self.node_weights[None,:]*radius**2*velocity**2/2
            base[:,:-1] += free_kinetic[:,:-1]
            kinetic = np.zeros_like(radius)
            kinetic[:,-1] = free_kinetic[:,-1]
            reservoir = np.zeros_like(radius)
            reservoir[:,-1] = self.reservoir_scale*.003*(1+.1*np.cos(2*np.pi*offsets))
            measure = (1.5-6*offsets**2)[:,None]/self.width
            return {key:measure*value for key,value in {'base':base, 'extra':radius**2*extra_nodal/(2*self.spacing),
                                                       'kinetic':kinetic, 'reservoir':reservoir}.items()}

    save()
    try:
        main = json.loads((main_dir/'status.json').read_text())
        check('main_complete', main['state']=='complete' and len(main['cases'])==8 and all(row['passed'] for row in main['checks']))
        for table in ['inputs','outputs']:
            for filename, expected in main[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed evidence: '+filename)
                report['inputs'][filename] = expected
        own(main_dir/'status.json')
        check('all_main_and_inherited_hashes_match', True)
        own(Path(__file__))
        snapshot = output/('executed-'+Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
        check('verifier_compiles_without_bytecode', True)
        radius, root_base, root_extra, coupling, base, extra, kinetic, reservoir = symbolic.symbols('R U0 U1 kappa e0 eG k sigma', positive=True)
        mass_base = radius*(1-root_base**2)/2
        mass_extra = radius*(1-root_extra**2)/2
        difference = mass_extra-mass_base
        first = coupling*(root_base**2*base+kinetic+root_base*reservoir)
        second = coupling*(root_extra**2*(base+extra)+kinetic+root_extra*reservoir)
        coefficient = coupling*(2*base/radius+2*reservoir/(radius*(root_base+root_extra)))
        check('exact_finite_nonlinear_mass_subtraction_identity', symbolic.simplify(second-first+coefficient*difference-coupling*root_extra**2*extra)==0)
        log_first = mass_base/(radius**2*root_base**2)+coupling*(base+kinetic/root_base**2)/radius
        log_second = mass_extra/(radius**2*root_extra**2)+coupling*(base+extra+kinetic/root_extra**2)/radius
        expected = difference*(1+2*coupling*kinetic)/(radius**2*root_base**2*root_extra**2)+coupling*extra/radius
        check('exact_finite_lapse_subtraction_identity', symbolic.simplify(log_second-log_first-expected)==0)
        check('source_reservoir_term_is_not_algebraically_optional', symbolic.simplify(coefficient-2*coupling*base/radius)!=0)
        margins = [Fraction(3821,39984), Fraction(5,84), Fraction(185,3528), Fraction(1,18)]
        check('exact_Gram_margin_lower_bound_one_twentieth', all(value>=Fraction(1,20) for value in margins), [str(value) for value in margins])
        smooth_constants = analytic_constants(1/16)
        rough_extra_upper = 4*.04**2*6.1**2
        rough_base_upper = 2*.04**2*6.1**2+6.1**2*.0144**2/2
        rough_extra_lower = 8/5*.04**2*4.9**2*7/8
        rough_mass_upper = .8+.1*(rough_base_upper+rough_extra_upper+.0033)
        rough_F_floor = 1-2*rough_mass_upper/4.9
        rough_Aint = .1*(2*rough_base_upper/4.9+.0033/(4.9*np.sqrt(.5)))
        rough_mass_lower = .1*.5*np.exp(-rough_Aint)*rough_extra_lower
        report['uniform_rough_bounds'] = {'extra_lower':rough_extra_lower, 'extra_upper':rough_extra_upper,
                                        'base_plus_kinetic_upper':rough_base_upper, 'mass_upper':rough_mass_upper,
                                        'proven_F_lower':rough_F_floor, 'outer_mass_difference_lower':rough_mass_lower}
        check('smooth_and_rough_regular_charts_have_analytic_energy_barriers', smooth_constants['proven_uniform_F_lower']>.5 and rough_F_floor>.5)
        check('rough_family_has_positive_uniform_mass_gap', rough_mass_lower>0, report['uniform_rough_bounds'])
        radii = np.linspace(5.,6.,513)
        offsets = np.array([-.49,-.3,-.1,0.,.17,.41,.49])
        for record in main['cases']:
            label = record['label']
            report['active_case'] = label
            save()
            system = ExplicitDensityFamily(record['count'],1.,profile=record['profile'])
            original = MatchedConstraintSystem(record['count'],1.,profile=record['profile'])
            actual_parts = system.density_parts(offsets)
            old_parts = original.density_parts(offsets)
            density_errors = {key:float(abs(actual_parts[key]-old_parts[key]).max()) for key in actual_parts}
            check(label+'_explicit_local_factors_match_original_matrices', max(density_errors.values())<1e-10, density_errors)
            check(label+'_extra_support_inside_normalization_radius', np.all(actual_parts['extra'][:,[0,-1]]==0))
            with np.load(main_dir/(label+'.npz'),allow_pickle=False) as archive:
                saved = {key:archive[key].copy() for key in archive.files}
            check(label+'_saved_arrays_finite', all(np.isfinite(value).all() for value in saved.values()))
            pair = IndependentRadialPair(system)
            independent = pair.metric(radii)
            errors = {'base_mass':float(abs(independent['base_mass']-saved['masses'][0]).max()),
                      'base_log_lapse':float(abs(independent['base_log_N']-saved['log_lapses'][0]).max()),
                      'mass_difference':float(abs(independent['mass_difference']-saved['mass_difference']).max()),
                      'log_lapse_difference':float(abs(independent['log_lapse_difference']-saved['log_lapse_difference']).max())}
            check(label+'_finite_difference_ODE_matches_original_nonlinear_pair', max(errors.values())<2e-10, errors)
            signal = max(record['max_mass_difference'],record['max_log_lapse_difference'])
            check(label+'_correction_resolved_above_independent_error', max(errors['mass_difference'],errors['log_lapse_difference'])<max(2e-12,.0001*signal))
            integrals = record['integrals']
            attenuation = .1*(2*integrals['base']/4.9+integrals['reservoir']/(4.9*np.sqrt(.5)))
            lower = .1*.5*np.exp(-attenuation)*integrals['extra']
            check(label+'_two_sided_mass_bound', lower<=independent['mass_difference'][-1]<=.1*integrals['extra'],
                  {'lower':lower, 'outer_difference':float(independent['mass_difference'][-1]), 'upper':.1*integrals['extra']})
            check(label+'_extra_integral_independently_recovered', abs(independent['extra_cumulative'][-1]-integrals['extra'])<2e-12)
            if record['profile']=='bounded_energy_rough':
                check(label+'_analytic_uniform_rough_bounds_respected', integrals['extra']>=rough_extra_lower and integrals['extra']<=rough_extra_upper
                      and integrals['base']+integrals['kinetic']<=rough_base_upper and independent['mass_difference'][-1]>=rough_mass_lower)
            independent_record = {'label':label, 'errors':errors, 'rhs_calls':pair.calls,
                                  'outer_mass_difference':float(independent['mass_difference'][-1]),
                                  'source_peak_density':float(system.density_parts([0.])['reservoir'][0,-1])}
            if record['count'] in [17,129]:
                refined_pair = IndependentRadialPair(system,rtol=5e-13,atol=2e-15,divisor=8)
                refined = refined_pair.metric(radii)
                refinement = {key:float(abs(refined[key]-independent[key]).max()) for key in independent}
                check(label+'_adaptive_radial_refinement', max(refinement.values())<2e-10, refinement)
                independent_record['adaptive_refinement'] = refinement
                spectral_errors = []
                for index,gamma in enumerate([0.,1.]):
                    fine = MatchedConstraintSystem(record['count'],gamma,degree=48,profile=record['profile']).geometry().metric(radii)
                    spectral_errors.append(max(float(abs(fine['mu']-saved['masses'][2*index]).max()),float(abs(fine['log_N']-saved['log_lapses'][2*index]).max())))
                check(label+'_radial_degree32_vs48', max(spectral_errors)<2e-10, spectral_errors)
                independent_record['spectral_refinement'] = spectral_errors
            if record['count']==17:
                initial_system = MatchedConstraintSystem(17,1.,profile=record['profile'])
                interpolated = PolarGeometry(initial_system,0.,initial_system.initial_state).metric(radii)
                interpolation_error = max(float(abs(interpolated['mu']-saved['masses'][2]).max()),float(abs(interpolated['log_N']-saved['log_lapses'][2]).max()))
                check(label+'_original_state_interpolating_geometry_matches_analytic_profile', interpolation_error<2e-10, interpolation_error)
                outer_mass = independent['base_mass'][-1]
                delta_mass = independent['mass_difference'][-1]
                base_F = 1-2*outer_mass/6
                extra_F = base_F-2*delta_mass/6
                source_sigma = system.density_parts([0.])['reservoir'][0,-1]
                omitted_damping_residual = 2*.1*source_sigma*delta_mass/(6*(np.sqrt(base_F)+np.sqrt(extra_F)))
                check(label+'_omitted_source_damping_negative_control_resolved', abs(omitted_damping_residual)>1e-10, float(omitted_damping_residual))
                missing_clock_error = abs(.5*np.log1p(-2*delta_mass/(6*base_F)))
                check(label+'_omitted_outer_clock_normalization_resolved', missing_clock_error>1e-8, float(missing_clock_error))
            archive_path = output/(label+'.npz')
            np.savez_compressed(archive_path,radii=radii,**independent)
            own(archive_path,'outputs')
            report['cases'].append(independent_record)
            save()
            print(json.dumps(independent_record),flush=True)
        for profile in ['smooth','bounded_energy_rough']:
            rows = [row for row in main['cases'] if row['profile']==profile]
            check(profile+'_source_integral_fixed_while_peak_grows', max(row['integrals']['reservoir'] for row in rows)-min(row['integrals']['reservoir'] for row in rows)<1e-14)
            peaks = [row['source_peak_density'] for row in report['cases'] if row['label'].startswith(profile+'_')]
            check(profile+'_source_peak_scales_inverse_width', abs(peaks[-1]/peaks[0]-8)<1e-12,peaks)
        check('no_python_cache',not (root/'scripts/__pycache__').exists())
        report['state']='complete'
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'cases':len(report['cases'])}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()
