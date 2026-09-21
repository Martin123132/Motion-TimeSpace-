from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_common_P2_overlay_20260919 import evaluation_rows
from derive_annular_exact_source_trace_comparison_20260920 import jump_row
from derive_annular_common_weak_action_20260920 import dec_saved
from annular_decimal_transport_v2_20260919 import DecimalAction, decimal_array
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from qualify_annular_nonuniform_Gram_precision_20260920 import decimal_fraction
from decimal import Decimal, localcontext
from fractions import Fraction
from bisect import bisect_right, bisect_left
from math import fsum, sqrt
from time import perf_counter
import contextlib
import json
import numpy as np


def derivative_atoms(mesh, values, fraction=False):
    convert = (lambda value:value) if fraction else decimal_fraction
    zero = Fraction(0) if fraction else Decimal(0)
    slopes_left, slopes_right, curvatures = [], [], []
    for index, indices in enumerate(mesh['elements']):
        left, middle, right = [values[column] if column >= 0 else zero for column in indices]
        length = convert(mesh['edges'][index+1]-mesh['edges'][index])
        slopes_left.append((-3*left+4*middle-right)/length)
        slopes_right.append((left-4*middle+3*right)/length)
        curvatures.append(4*(left-2*middle+right)/length**2)
    locations, first, second = mesh['edges'][1:-1], [], []
    for index, location in enumerate(locations):
        first.append(zero if location == mesh['anchor'] else slopes_left[index+1]-slopes_right[index])
        second.append(curvatures[index+1]-curvatures[index])
    return locations, first, second


def atom_responses(points, locations):
    width = (points[-1]-points[0])/3
    weights = []
    for local in range(4):
        denominator = Fraction(1)
        for other in range(4):
            if other != local:
                denominator *= points[local]-points[other]
        weights.append(6*width**3/denominator)
    rows = []
    for index in range(bisect_right(locations, points[0]), bisect_left(locations, points[-1])):
        location = locations[index]
        hinge = [max(point-location, Fraction(0)) for point in points]
        first = sum(weight*value for weight, value in zip(weights, hinge))
        second = sum(weight*value**2/2 for weight, value in zip(weights, hinge))
        rows.append((index, first, second))
    return width, rows


def stable_difference(knots, atoms):
    locations, first, second = atoms
    result = []
    for index in range(len(knots)-3):
        width, responses = atom_responses(knots[index:index+4], locations)
        result.append(fsum(float(first[column])*float(weight_first)+float(second[column])*float(weight_second)
            for column, weight_first, weight_second in responses)/sqrt(float(width)))
    return np.asarray(result)


def stable_sparse(mapping, values):
    return np.asarray([fsum(float(mapping.data[position])*float(values[mapping.indices[position]])
        for position in range(mapping.indptr[row], mapping.indptr[row+1])) for row in range(mapping.shape[0])])


def main():
    evidence = EvidenceRun('annular-nonuniform-Gram-atoms-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, nonuniform_parent_uniqueness_proven=False,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, actual_time_integrated_force_test=False,
            stable_fixed_profile_kernel_qualified=False, all_non_source_derivative_atoms_retained=True,
            atom_preparation_digits=72, kernel_arithmetic='binary64 with exact rational geometric weights and compensated sums')
        status_path = evidence.output.parent/'annular-nonuniform-Gram-precision-attempt01/status.json'
        qualified = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('high_precision_profile_reference_complete', qualified['state'] == 'complete'
            and qualified['fixed_profile_arithmetic_qualified'] and all(row['passed'] for row in qualified['checks']))
        packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', 'MTS-exact-common-overlay.json')
        meshes = [dict(item, edges=list(map(Fraction, item['edges'])), nodes=list(map(Fraction, item['nodes'])),
            anchor=Fraction(item['anchor'])) for item in packet['native']]
        anchor = meshes[0]['anchor']
        fixture_values = [Fraction((index*7)%23-11, 16) for index in range(meshes[0]['count'])]
        fixture_atoms = derivative_atoms(meshes[0], fixture_values, True)
        fixture_jump = sum(weight*fixture_values[index] for index, weight in jump_row(meshes[0]).items())
        fixture_knots = sorted(map(Fraction, packet['overlay']['nodes']))
        source_index = bisect_left(fixture_knots, anchor)
        wrong_curvature_rejected = False
        for start in range(source_index-5, source_index+5):
            points = fixture_knots[start:start+4]
            width, responses = atom_responses(points, fixture_atoms[0])
            values = [sum((weight*fixture_values[column] for column, weight in row.items()), Fraction(0))
                -fixture_jump*max(location-anchor, Fraction(0))
                for location, row in zip(points, evaluation_rows(meshes[0], points))]
            direct = Fraction(0)
            for local in range(4):
                denominator = Fraction(1)
                for other in range(4):
                    if local != other:
                        denominator *= points[local]-points[other]
                direct += 6*width**3/denominator*values[local]
            recovered = sum((fixture_atoms[1][column]*first+fixture_atoms[2][column]*second
                for column, first, second in responses), Fraction(0))
            evidence.check('exact_local_atom_identity_'+str(start), direct == recovered)
            wrong = sum((fixture_atoms[1][column]*first for column, first, second in responses), Fraction(0))
            wrong_curvature_rejected |= wrong != direct
        evidence.check('reject_missing_curvature_atoms', wrong_curvature_rejected)
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
        with localcontext() as ctx:
            ctx.prec = 72
            prepared = {label:[derivative_atoms(mesh, values) for mesh, values in zip(meshes, fields)]
                for label, fields in profiles.items()}
        data = checked_load(evidence, 'annular-nonuniform-Gram-parent-probes-attempt02', 'MTS-uniform513-initial-profile.npz')
        sequence = [('uniform513', [Fraction.from_float(float(value)) for value in data['knots']])]
        knots = fixture_knots
        for level in range(3):
            if level:
                knots = sorted(set(knots+[(first+last)/2 for first, last in zip(knots, knots[1:])])-{anchor})
            sequence.append(('profile'+str(level), knots))
        for label, knots in sequence:
            template, sampling = template_rows(len(knots))
            distortions = []
            for index in range(len(knots)-3):
                gaps = [last-first for first, last in zip(knots[index:index+4], knots[index+1:index+4])]
                width = sum(gaps)/3
                distortions.append(float(sum((gap-width)**2 for gap in gaps)/sum(gap**2 for gap in gaps)))
            for endpoint, atoms in prepared.items():
                fields = [stable_difference(knots, item) for item in atoms]
                data = checked_load(evidence, 'annular-nonuniform-Gram-parent-probes-attempt02',
                    'MTS-'+label+'-'+endpoint+'-profile.npz')
                weights = stable_sparse(sampling, data['coefficient'])
                for extension in ['primary', 'nonunique_control']:
                    factors = [stable_sparse(template, field*(1+np.asarray(distortions)) if extension == 'nonunique_control' else field)
                        for field in fields]
                    bilinear = fsum(float(weight)*float(first)*float(last) for weight, first, last in zip(weights, *factors))
                    reference = next(row for row in qualified['cases'] if row['digits'] == 72 and row['mesh'] == label
                        and row['endpoint'] == endpoint and row['extension'] == extension)
                    error = abs(Decimal.from_float(bilinear)-Decimal(reference['bilinear']))
                    gate = Decimal('1e-12')*Decimal(reference['absolute_row_sum'])+Decimal('1e-25')
                    evidence.check(label+'_'+endpoint+'_'+extension+'_stable_kernel_matches_decimal', error <= gate, str(error))
                    evidence.report['cases'].append(dict(mesh=label, endpoint=endpoint, extension=extension,
                        stable_bilinear=str(bilinear), decimal_bilinear=reference['bilinear'], absolute_error=str(error),
                        absolute_row_sum=reference['absolute_row_sum'], arithmetic_gate=str(gate),
                        prepared_native_atoms_require_consistent_precision=True, valid_for_claim=False))
            evidence.report['progress'] = dict(mesh=label, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report.update(stable_fixed_profile_kernel_qualified=True, seconds=perf_counter()-started)
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

