from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_live_P2_canonical_v2_20260918 import P2Density
from types import SimpleNamespace
import contextlib
import json
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-candidate-radial-derivation-attempt03', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, polar_zero_shift_only=True,
            radial_constraint_derived=False, radial_jacobian_qualified=False,
            self_consistent_candidate_metric_solved=False, physical_force_mismatch_fixed=False,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False)
        radius, mass, lapse, coupling, source_mass = sp.symbols('radius mass lapse coupling source_mass', positive=True)
        temporal, gradient, gram, source_density = sp.symbols('temporal gradient gram source_density', nonnegative=True)
        velocity, mass_radial, lapse_radial = sp.symbols('velocity mass_radial lapse_radial', real=True)
        metric = 1-2*mass/radius
        root = sp.sqrt(metric)
        clock = sp.sqrt(lapse**2-velocity**2/metric)
        gravity = lapse*mass_radial/(coupling*root)
        wave = radius**2*temporal/(2*lapse*root)-lapse*root*radius**2*(gradient/2+gram)
        dust = -source_mass*source_density*clock
        lagrangian = gravity+wave+dust
        lapse_euler = sp.diff(lagrangian, lapse)
        mass_euler = sp.diff(lagrangian, mass)-sp.diff(lapse/(coupling*root), radius)
        mass_euler -= sp.diff(lapse/(coupling*root), mass)*mass_radial+sp.diff(lapse/(coupling*root), lapse)*lapse_radial
        density = temporal/(2*lapse**2*metric)+gradient/2+gram
        expected_mass = coupling*(radius**2*metric*density+root*source_mass*lapse/clock*source_density)
        expected_lapse = mass/(radius**2*metric)+coupling*radius*density
        expected_lapse += coupling*source_mass*velocity**2*source_density/(radius*lapse*root**3*clock)
        evidence.check('full_lapse_variation_mass_constraint', sp.factor(sp.together(lapse_euler-(mass_radial-expected_mass)/(coupling*root))) == 0)
        evidence.check('full_mass_variation_lapse_constraint', sp.factor(sp.together(mass_euler-lapse/(coupling*root)*(expected_lapse-lapse_radial/lapse))) == 0)
        evidence.check('vacuum_mass_equation', sp.simplify(expected_mass.subs({temporal:0, gradient:0, gram:0, source_density:0})) == 0)
        evidence.check('vacuum_lapse_equation', sp.simplify(expected_lapse.subs({temporal:0, gradient:0, gram:0, source_density:0})-mass/(radius**2*metric)) == 0)
        evidence.check('Gram_mass_loading_sign', sp.simplify(sp.diff(expected_mass, gram)-coupling*radius**2*metric) == 0)
        evidence.check('Gram_lapse_loading_sign', sp.simplify(sp.diff(expected_lapse, gram)-coupling*radius) == 0)
        inner_lapse, inner_root, outer_lapse, outer_root, multiplier, inner_delta, outer_delta = sp.symbols(
            'inner_lapse inner_root outer_lapse outer_root multiplier inner_delta outer_delta', positive=True)
        boundary = outer_lapse*outer_delta/(coupling*outer_root)-inner_lapse*inner_delta/(coupling*inner_root)
        boundary += -outer_delta/coupling+multiplier*inner_delta
        evidence.check('sourced_boundary_cancellation', sp.simplify(boundary.subs({outer_lapse:outer_root,
            multiplier:inner_lapse/(coupling*inner_root)})) == 0)
        evidence.check('omitted_gravity_boundary_detected', sp.simplify((-outer_delta/coupling+multiplier*inner_delta).subs(
            {multiplier:inner_lapse/(coupling*inner_root)})) != 0)
        expressions = sp.Matrix([expected_mass, expected_lapse])
        symbolic_jacobian = sp.Matrix.hstack(expressions.diff(mass), lapse*expressions.diff(lapse))
        arguments = [radius, mass, lapse, temporal, gradient, gram, source_density, velocity, coupling, source_mass]
        symbolic_function = sp.lambdify(arguments, symbolic_jacobian, 'numpy')
        evidence.report['jacobians'] = []
        for case, speed in enumerate([0., .04, -.12]):
            radii = np.array([5.3, 6.1, 6.7])
            masses, logs = np.array([.7, .71, .72]), np.log(np.array([.8, .86, .89]))
            temporal_values, gradient_values = np.array([.004, .008, .002]), np.array([.02, .03, .01])
            gram_values, source_values = np.array([.001, 0., .0003]), np.array([0., 3., 1.])
            speeds = np.full(3, speed)
            inputs = [temporal_values, gradient_values, gram_values, source_values, speeds, .1, .03]
            value, jacobian = radial_rhs(radii, masses, logs, *inputs, jacobian=True)
            expected = symbolic_function(radii, masses, np.exp(logs), *inputs)
            error = float(np.max(abs(jacobian-expected)))
            evidence.check('symbolic_local_J_'+str(case), error < 3e-12, error)
            for component in [0, 1]:
                trial = [masses.astype(complex), logs.astype(complex)]
                trial[component] += 1e-25j
                differentiated = radial_rhs(radii, *trial, *inputs).imag/1e-25
                error = float(np.max(abs(differentiated-jacobian[:, component])))
                evidence.check('complex_local_J_'+str(case)+'_'+str(component), error < 3e-12, error)
            holder = SimpleNamespace(radius=radii, temporal_square=temporal_values, gradient_square=gradient_values,
                gram=gram_values, source_density=source_values, velocity=speeds,
                material=SimpleNamespace(owner=SimpleNamespace(coupling=.1, source_mass=.03)))
            original = np.array(P2Density.rhs(holder, masses, logs))
            evidence.check('original_rhs_functional_reduction_'+str(case), np.max(abs(original-value)) < 3e-14)
            zero = radial_rhs(radii, masses, logs, temporal_values, gradient_values, 0*gram_values, source_values, speeds, .1, .03)
            expected_extra = np.array([.1*radii**2*(1-2*masses/radii)*gram_values, .1*radii*gram_values])
            evidence.check('exact_reference_Gram_removal_'+str(case), np.max(abs(value-zero-expected_extra)) < 3e-14)
            evidence.report['jacobians'].append(dict(case=case, source_velocity=speed,
                symbolic_max_error=float(np.max(abs(jacobian-expected))),
                original_rhs_max_error=float(np.max(abs(original-value))), valid_for_claim=False))
        evidence.report['pushforwards'] = []
        points, weights = np.polynomial.legendre.leggauss(40)
        labels, measure = points/2, weights/2
        anchor, inner, outer, width = 6.03, 5.2, 6.8, .02

        def mapping(reference, offsets):
            displacement = (reference-inner)/(anchor-inner) if reference < anchor else (outer-reference)/(outer-anchor)
            slope = 1/(anchor-inner) if reference < anchor else -1/(outer-anchor)
            source = anchor+.07+.022*offsets+.003*offsets**2
            radial = reference+displacement*(source-anchor)+(1-displacement)*width*offsets
            spatial = 1+slope*(source-anchor-width*offsets)
            label = displacement*(.022+.006*offsets)+(1-displacement)*width
            return radial, spatial, label

        for index, reference in enumerate([6.025, 6.035, 6.045, 6.055]):
            mapped, spatial, unused = mapping(reference, labels)
            low, high = mapping(reference, np.array([-.5, .5]))[0]
            physical = (low+high)/2+(high-low)*points/2
            inverse = (physical-low)/(high-low)-.5
            for unused in range(8):
                value, unused, derivative = mapping(reference, inverse)
                inverse -= (value-physical)/derivative
            unused, jacobian, label_jacobian = mapping(reference, inverse)

            def load(offsets):
                return (.01*(index+1)*(1+.2*offsets+.1*offsets**2))**2

            def weight(offsets):
                return 6*(offsets+.5)*(.5-offsets)

            for direction in ['energy', 'lapse', 'mass']:
                def coefficient(radial):
                    base = radial**2*np.exp(.01*(radial-6))*np.sqrt(1-1.4/radial)
                    if direction == 'lapse':
                        return base*np.sin(radial)
                    if direction == 'mass':
                        return -base*(.01+.002*np.cos(radial))/(radial*(1-1.4/radial))
                    return base
                first = sum(measure*weight(labels)*load(labels)*coefficient(mapped)/spatial)
                density = weight(inverse)*load(inverse)/(jacobian*label_jacobian)
                last = sum(weights*(high-low)/2*density*coefficient(physical))
                error = abs(first-last)/max(abs(first), 1e-30)
                evidence.check('Gram_pushforward_'+str(index)+'_'+direction, error < 1e-10, float(error))
                omitted_spatial = sum(weights*(high-low)/2*density*jacobian*coefficient(physical))
                omitted_label = sum(weights*(high-low)/2*density*label_jacobian*coefficient(physical))
                evidence.check('omit_spatial_J_detected_'+str(index)+'_'+direction, abs(omitted_spatial-first)/abs(first) > 1e-3)
                evidence.check('omit_label_J_detected_'+str(index)+'_'+direction, abs(omitted_label-first)/abs(first) > .5)
                evidence.report['pushforwards'].append(dict(node=index, direction=direction, reference=reference,
                    label_integral=float(first), radial_integral=float(last), relative_error=float(error),
                    manufactured_control_not_parent_data=True, valid_for_claim=False))
        for name in ['DERIVATION-20260913-cross-cut-source-action-and-driven-initial-boundaries.md',
                'DERIVATION-20260915-repaired-live-canonical-geometry-and-current.md',
                'DERIVATION-20260920-complete-frozen-candidate-and-source-response.md',
                'scripts/annular_live_P2_canonical_v2_20260918.py']:
            evidence.own(evidence.root/name)
        evidence.report.update(radial_constraint_derived=True, radial_jacobian_qualified=True,
            boundary_action_retained=True, collar_pushforward_qualified=True,
            general_nonzero_shift_or_temporal_current_derived=False)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
