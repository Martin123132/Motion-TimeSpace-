from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_frozen_candidate_20260920 import FrozenCandidate, source_force
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_decimal_transport_v2_20260919 import decimal_array, propagate, dot
from annular_common_weighted_moments_20260920 import apply_rational_rows
from derive_annular_common_weak_action_20260920 import dec_saved
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from annular_decimal_transport_v2_20260919 import DecimalAction
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import json
import numpy as np
import sympy as sp
import mpmath as mp


def main():
    evidence = EvidenceRun('annular-complete-candidate-controls-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, physical_force_mismatch_fixed=False,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            self_consistent_candidate_metric_solved=False, full_source_Euler_controls_qualified=False,
            frozen_scalar_propagator_qualified=False)
        evidence.report['pairings'], evidence.report['source_controls'] = [], []
        source, speed, field0, field1, rate0, rate1 = sp.symbols('source speed field0 field1 rate0 rate1', real=True)
        fields, rates = sp.Matrix([field0, field1]), sp.Matrix([rate0, rate1])
        mass = sp.diag(1+source**2, 2+source**2)
        transport = sp.Matrix([[source/10, sp.Rational(1, 20)], [-source/8, source/6]])
        inertia = sp.diag(sp.Rational(1, 5)*(1+source**2), sp.Rational(3, 10)*(1+source**2))
        stiffness = sp.Matrix([[4+source**2, sp.Rational(-1, 3)], [sp.Rational(-1, 3), 5+source]])
        lapse, root, rest_mass = 1+source/10, sp.Rational(4, 5)+3*source/100, sp.Rational(3, 100)
        clock = sp.sqrt(lapse**2-speed**2/root**2)
        dust = -rest_mass*clock
        wave = (rates.T*mass*rates)[0]/2-speed*(rates.T*transport*fields)[0]
        wave += speed**2*(fields.T*inertia*fields)[0]/2-(fields.T*stiffness*fields)[0]/2
        lagrangian = wave+dust
        coordinates = [field0, field1, source]
        velocities = [rate0, rate1, speed]
        momenta = sp.Matrix([sp.diff(lagrangian, item) for item in velocities])
        hessian = momenta.jacobian(velocities)
        rhs = sp.Matrix([sp.diff(lagrangian, item) for item in coordinates])-momenta.jacobian(coordinates)*sp.Matrix(velocities)
        arguments = [source, speed, field0, field1, rate0, rate1]
        hessian_function, rhs_function = [sp.lambdify(arguments, expression, 'numpy') for expression in [hessian, rhs]]
        inertia_dust = sp.diff(dust, speed, 2)
        drive_dust = sp.diff(dust, source)-speed*sp.diff(dust, speed, source)
        dust_function = sp.lambdify([source, speed], [inertia_dust, drive_dust], 'numpy')
        partial_function = sp.lambdify(arguments, sp.diff(wave, source), 'numpy')
        matrix_expressions = dict(mass=mass, mass_X=mass.diff(source), transport=transport,
            transport_X=transport.diff(source), inertia=inertia, inertia_X=inertia.diff(source),
            stiffness=stiffness, stiffness_X=stiffness.diff(source))
        with localcontext() as ctx:
            ctx.prec = 48
            for case, velocity_value in enumerate([0., .07, -.04]):
                location = .2
                arguments_value = [location, velocity_value, .013, -.021, .03, .01]
                maps = {}
                numeric = {}
                for name, expression in matrix_expressions.items():
                    numeric[name] = np.array(expression.subs(source, location), dtype=float)
                    rows = [{column:Decimal.from_float(float(value)) for column, value in enumerate(row) if value}
                        for row in numeric[name]]
                    maps[name] = MixedMap(rows, 2).serialize()
                action = FrozenCandidate(dict(count=2, maps=maps))
                field = decimal_array(np.array(arguments_value[2:4]))
                velocity = decimal_array(np.array(arguments_value[4:6]))
                dust_values = dust_function(location, velocity_value)
                result = source_force(action, field, velocity, Decimal.from_float(velocity_value),
                    Decimal.from_float(float(dust_values[0])), Decimal.from_float(float(dust_values[1])))
                expected_acceleration = np.linalg.solve(hessian_function(*arguments_value),
                    np.asarray(rhs_function(*arguments_value)).ravel())[-1]
                expected_wave = dust_values[0]*expected_acceleration-dust_values[1]
                error = abs(float(result['reduced_wave_force'])-expected_wave)
                evidence.check('symbolic_full_Euler_'+str(case), error < 3e-12, error)
                evidence.check('symbolic_partial_covector_'+str(case),
                    abs(float(result['partial_wave_covector'])-partial_function(*arguments_value)) < 3e-12)
                evidence.check('reject_partial_as_reaction_'+str(case),
                    abs(float(result['partial_wave_covector'])-expected_wave) > 1e-7)
                evidence.report['source_controls'].append(dict(case=case, speed=velocity_value,
                    reduced_force=str(result['reduced_wave_force']), independent_Euler_force=float(expected_wave),
                    error=float(error), partial_covector=str(result['partial_wave_covector']), valid_for_claim=False))
            phase = np.stack([field, velocity])[:, :, None]
            propagated, unused = propagate(action, phase, Decimal('0.07'), 64)
            mp.mp.dps = 75
            matrix_mass = mp.matrix([[mp.mpf(float(value)) for value in row] for row in numeric['mass']])
            matrix_stiffness = mp.matrix([[mp.mpf(float(value)) for value in row] for row in numeric['stiffness']])
            generator = mp.zeros(4)
            acceleration = -(matrix_mass**-1)*matrix_stiffness
            for row in range(2):
                generator[row, row+2] = 1
                for column in range(2):
                    generator[row+2, column] = acceleration[row, column]
            expected = mp.expm(mp.mpf('0.07')*generator)*mp.matrix([mp.mpf(str(value)) for value in phase.flat])
            error = max(abs(value-Decimal(str(expected[index]))) for index, value in enumerate(propagated.flat))
            evidence.check('independent_dense_exponential', error < Decimal('1e-36'), str(error))
        with localcontext() as ctx:
            ctx.prec = 64
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', 'MTS-exact-common-overlay.json')
            reference_path = evidence.output.parent/'annular-nonuniform-Gram-precision-attempt01/status.json'
            previous = json.loads(reference_path.read_text())
            evidence.own(reference_path)
            initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', 'MTS-point032.npz')
            terminal_force = checked_load(evidence, 'annular-full-force-endpoints-attempt01', 'MTS-spatial64-force-covector.npz')
            native = checked_load(evidence, 'annular-action-exponential-response-attempt01', 'MTS-fine-action.npz')
            forward = owned_json(evidence, 'annular-weak-residual-force-attempt01', 'MTS-48-order64-forward.json')
            backward = owned_json(evidence, 'annular-weak-residual-force-attempt01', 'MTS-48-order64-adjoint.json')
            with localcontext() as inner:
                inner.prec = 48
                original = DecimalAction(native)
                profiles = dict(initial=(decimal_array(initial['0_position'])[:, None],
                    original.solve(dec_saved(backward['source_terminal'])[1])),
                    final=(dec_saved(forward['source_terminal'])[0],
                    original.solve(decimal_array(terminal_force['covector'])[1, :, None])))
            for extension in ['primary', 'alternative']:
                data = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', 'MTS-'+extension+'-action.json')
                factor = MixedMap(data['gram_factor']['rows'], data['gram_factor']['columns'])
                weights = np.array(list(map(Decimal, data['gram_weights'])), dtype=object)
                for endpoint, values in profiles.items():
                    common = [apply_rational_rows(embedding, field) for embedding, field in zip(packet['embeddings'], values)]
                    mapped = [factor.apply(field)[:, 0] for field in common]
                    bilinear = sum(weights*mapped[0]*mapped[1], Decimal(0))
                    prior = next(row for row in previous['cases'] if row['digits'] == 72 and row['mesh'] == 'profile0'
                        and row['endpoint'] == endpoint and row['extension'] == ('primary' if extension == 'primary' else 'nonunique_control'))
                    error = abs(bilinear-Decimal(prior['bilinear']))
                    evidence.check(extension+'_'+endpoint+'_previous_atom_pairing', error < Decimal('1e-24'), str(error))
                    evidence.report['pairings'].append(dict(extension=extension, endpoint=endpoint,
                        assembled_bilinear=str(bilinear), previous_bilinear=prior['bilinear'], error=str(error), valid_for_claim=False))
                unused, sampling = template_rows(data['count'])
                from qualify_annular_nonuniform_Gram_precision_20260920 import sparse_apply
                field = dec_saved(data['phase'])[0, :, None]
                image = factor.apply(field)[:, 0]
                dual = -np.asarray(sparse_apply(sampling.T.tocsr(), list(image**2)), dtype=object)/2
                direction = np.array([Decimal((index*3)%13-6)/8 for index in range(data['count'])], dtype=object)
                direct = -sum(np.asarray(sparse_apply(sampling, list(direction)))*image**2, Decimal(0))/2
                evidence.check(extension+'_nodal_coefficient_dual', abs(sum(dual*direction, Decimal(0))-direct) < Decimal('1e-40'))
                output = evidence.output/(extension+'-nodal-q-dual.json')
                output.write_text(json.dumps(dict(dual=list(map(str, dual)), variable='q=c/J at reference knots',
                    physical_c_dual_requires_divide_by_J=True, frozen_state_only=True, valid_for_claim=False))+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
        evidence.report.update(full_source_Euler_controls_qualified=True, frozen_scalar_propagator_qualified=True,
            seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

