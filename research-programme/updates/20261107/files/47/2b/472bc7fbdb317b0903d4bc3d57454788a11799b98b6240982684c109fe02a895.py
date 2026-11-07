from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_common_P2_overlay_20260919 import evaluation_rows
from derive_annular_exact_source_trace_comparison_20260920 import jump_row
from derive_annular_common_weak_action_20260920 import dec_saved
from annular_decimal_transport_v2_20260919 import DecimalAction, decimal_array
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import contextlib
import json


def decimal_fraction(value):
    return Decimal(value.numerator)/Decimal(value.denominator)


def sample(mesh, values, knots):
    return [sum((decimal_fraction(weight)*values[index] for index, weight in row.items()), Decimal(0))
        for row in evaluation_rows(mesh, knots)]


def sparse_apply(mapping, values):
    return [sum((Decimal.from_float(float(mapping.data[position]))*values[mapping.indices[position]]
        for position in range(mapping.indptr[row], mapping.indptr[row+1])), Decimal(0)) for row in range(mapping.shape[0])]


def difference_profile(knots, compensated):
    values, distortions = [], []
    for index in range(len(knots)-3):
        points = knots[index:index+4]
        width = (points[-1]-points[0])/3
        total = Decimal(0)
        for local in range(4):
            denominator = Fraction(1)
            for other in range(4):
                if other != local:
                    denominator *= points[local]-points[other]
            weight = 6*width**3/denominator
            total += decimal_fraction(weight)*compensated[index+local]
        values.append(total/decimal_fraction(width).sqrt())
        gaps = [last-first for first, last in zip(points, points[1:])]
        distortions.append(decimal_fraction(sum((gap-width)**2 for gap in gaps)/sum(gap**2 for gap in gaps)))
    return values, distortions


def main():
    evidence = EvidenceRun('annular-nonuniform-Gram-precision-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, nonuniform_parent_uniqueness_proven=False,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, actual_time_integrated_force_test=False,
            evolving_front_resolution_proven=False, parent_inputs_precision='binary64; saved path coefficients held at48digits',
            float_pilot_superseded_for_signed_pairs=True, fixed_profile_arithmetic_qualified=False)
        evidence.report['refinement'], evidence.report['binary64_comparisons'] = [], []
        pilot_path = evidence.output.parent/'annular-nonuniform-Gram-parent-probes-attempt02/status.json'
        pilot = json.loads(pilot_path.read_text())
        evidence.own(pilot_path)
        evidence.check('pilot_complete', pilot['state'] == 'complete' and all(row['passed'] for row in pilot['checks']))
        evidence.check('reference_baseline_exact_zero', all(Decimal(row['bilinear']) == 0 and Decimal(row['trial_energy']) == 0
            and Decimal(row['test_energy']) == 0 for row in pilot['cases'] if row['branch'] == 'reference'))
        packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', 'MTS-exact-common-overlay.json')
        meshes = [dict(item, edges=list(map(Fraction, item['edges'])), nodes=list(map(Fraction, item['nodes'])),
            anchor=Fraction(item['anchor'])) for item in packet['native']]
        anchor = meshes[0]['anchor']
        initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', 'MTS-point032.npz')
        force = checked_load(evidence, 'annular-full-force-endpoints-attempt01', 'MTS-spatial64-force-covector.npz')
        native = checked_load(evidence, 'annular-action-exponential-response-attempt01', 'MTS-fine-action.npz')
        forward = owned_json(evidence, 'annular-weak-residual-force-attempt01', 'MTS-48-order64-forward.json')
        adjoint = owned_json(evidence, 'annular-weak-residual-force-attempt01', 'MTS-48-order64-adjoint.json')
        with localcontext() as ctx:
            ctx.prec = 48
            action = DecimalAction(native)
            profiles = dict(initial=(list(decimal_array(initial['0_position'])),
                list(action.solve(dec_saved(adjoint['source_terminal'])[1])[:, 0])),
                final=(list(dec_saved(forward['source_terminal'])[0, :, 0]),
                list(action.solve(decimal_array(force['covector'])[1, :, None])[:, 0])))
        sequence = [('uniform513', [Fraction.from_float(float(value)) for value in
            checked_load(evidence, 'annular-nonuniform-Gram-parent-probes-attempt02', 'MTS-uniform513-initial-profile.npz')['knots']])]
        knots = sorted(map(Fraction, packet['overlay']['nodes']))
        for level in range(3):
            if level:
                knots = sorted(set(knots+[(first+last)/2 for first, last in zip(knots, knots[1:])])-{anchor})
            sequence.append(('profile'+str(level), knots))
        previous = {}
        for digits in [48, 72]:
            with localcontext() as ctx:
                ctx.prec = digits
                for label, knots in sequence:
                    template, sampling = template_rows(len(knots))
                    for endpoint, (trial, test) in profiles.items():
                        data = checked_load(evidence, 'annular-nonuniform-Gram-parent-probes-attempt02',
                            'MTS-'+label+'-'+endpoint+'-profile.npz')
                        weights = sparse_apply(sampling, [Decimal.from_float(float(value)) for value in data['coefficient']])
                        difference_fields = []
                        for mesh, values in zip(meshes, [trial, test]):
                            jump = sum((decimal_fraction(weight)*values[index] for index, weight in jump_row(mesh).items()), Decimal(0))
                            sampled = sample(mesh, values, knots)
                            compensated = [value-jump*decimal_fraction(max(location-anchor, Fraction(0)))
                                for value, location in zip(sampled, knots)]
                            difference, distortions = difference_profile(knots, compensated)
                            difference_fields.append(difference)
                        for extension in ['primary', 'nonunique_control']:
                            factors = [sparse_apply(template, [value*(1+distortion) if extension == 'nonunique_control' else value
                                for value, distortion in zip(field, distortions)]) for field in difference_fields]
                            summands = [weight*first*last for weight, first, last in zip(weights, *factors)]
                            bilinear = sum(summands, Decimal(0))
                            trial_energy, test_energy = [sum((weight*value**2 for weight, value in zip(weights, field)), Decimal(0))/2
                                for field in factors]
                            absolute_sum = sum(map(abs, summands), Decimal(0))
                            evidence.check(str(digits)+'_'+label+'_'+endpoint+'_'+extension+'_positive_Cauchy',
                                trial_energy >= 0 and test_energy >= 0 and abs(bilinear) <= 2*(trial_energy*test_energy).sqrt())
                            row = dict(branch='MTS', digits=digits, mesh=label, endpoint=endpoint, extension=extension,
                                knot_count=len(knots), bilinear=str(bilinear), trial_energy=str(trial_energy),
                                test_energy=str(test_energy), absolute_row_sum=str(absolute_sum),
                                row_cancellation_ratio=str(absolute_sum/abs(bilinear)) if bilinear else 'infinite',
                                actual_time_integrated_force=False, valid_for_claim=False)
                            evidence.report['cases'].append(row)
                            key = (label, endpoint, extension)
                            if digits == 48:
                                previous[key] = row
                            else:
                                error = abs(bilinear-Decimal(previous[key]['bilinear']))
                                evidence.check('_'.join(key)+'_precision_refinement', error < Decimal('1e-24'), str(error))
                                evidence.report['refinement'].append(dict(mesh=label, endpoint=endpoint, extension=extension,
                                    absolute_bilinear_change=str(error), arithmetic_gate='1e-24',
                                    not_a_physical_force_gate=True, valid_for_claim=False))
                                original = next(item for item in pilot['cases'] if item['branch'] == 'MTS'
                                    and item['mesh'] == label and item['endpoint'] == endpoint and item['extension'] == extension)
                                evidence.report['binary64_comparisons'].append(dict(mesh=label, endpoint=endpoint, extension=extension,
                                    binary64_bilinear=original['bilinear'], qualified_bilinear=str(bilinear),
                                    absolute_change=str(abs(bilinear-Decimal(original['bilinear']))), valid_for_claim=False))
                    evidence.report['progress'] = dict(digits=digits, mesh=label, seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report.update(fixed_profile_arithmetic_qualified=True, seconds=perf_counter()-started)
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

