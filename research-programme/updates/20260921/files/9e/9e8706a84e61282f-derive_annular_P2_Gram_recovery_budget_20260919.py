from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
import contextlib
import json
import numpy as np
import sympy as symbolic


def read_complete(evidence, folder):
    path = evidence.output.parent/folder/'status.json'
    report = json.loads(path.read_text())
    evidence.own(path)
    evidence.check(folder+'_completed_checks', report['state'] == 'complete' and all(row['passed'] for row in report['checks']))
    return report


def main():
    evidence = EvidenceRun('annular-P2-Gram-recovery-budget-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            full_force_not_replaced_by_Gram_subtraction=True,
            local_mesh_law_not_yet_a_variable_geometry_theorem=True,
            no_large_uniform_run_launched=True)
        mesh_law = read_complete(evidence, 'annular-P2-Gram-force-mesh-law-attempt01')
        front = read_complete(evidence, 'annular-P2-front-projected-Gram-attempt01')
        reaction = read_complete(evidence, 'annular-P2-Gram-source-reaction-attempt01')
        localized = read_complete(evidence, 'annular-P2-local-Gram-bound-attempt01')
        drive = read_complete(evidence, 'annular-P2-Gram-projected-drive-attempt01')
        ratio = (9-symbolic.sqrt(73))/4
        graded_coefficient = symbolic.simplify((7+3/(6-ratio))/2)
        evidence.check('geometric_tail_ratio_equation', symbolic.simplify(2*ratio**2-9*ratio+1) == 0
            and 0 < float(ratio) < 1/3)
        evidence.check('exact_graded_coefficient_bracket', 3.5 < float(graded_coefficient) < 4)
        phase = symbolic.Rational(3, 5)
        cross = -17*phase*(phase-1)*(2*phase-1)/72
        coefficient = symbolic.simplify(-symbolic.Rational(3, 10)/2*graded_coefficient
            *(8*symbolic.Rational(1, 100)/phase+8*symbolic.Rational(3, 250)/(1-phase))*cross)
        finest = [row for row in mesh_law['cases'] if row['spacing'] == 1/512]
        for row in finest:
            if row['source_power'] > 1:
                evidence.check(str(row['source_power'])+'_independent_graded_asymptotic_coefficient',
                    max(abs(value-float(graded_coefficient)) for value in row['trace_coefficients']) < 2e-12
                    and abs(row['reaction_main']/row['spacing']**(2-row['source_power'])-float(coefficient)) < 2e-13)
        evidence.report['exact_graded_asymptote'] = dict(tail_ratio=str(ratio), trace_coefficient=str(graded_coefficient),
            trace_coefficient_numeric=float(graded_coefficient), force_coefficient=str(coefficient),
            force_coefficient_numeric=float(coefficient),
            grading='first two source lengths delta, delta, then 2delta, 4delta, ...',
            fixture_only=True)
        for item in drive['cases']:
            branch, count = item['branch'], item['base_count']
            source_path = evidence.root/item['source_path']
            source = json.loads(source_path.read_text())
            evidence.own(source_path)
            state = source['cases'][-1]
            schur = state['schur']
            ratio_inertia = schur['field_projection_inertia']/schur['dust_inertia']
            pressure = item['continuum_force']
            remaining = item['remaining_drive']
            bounded = next(row for row in localized['cases'] if row['branch'] == branch and row['base_count'] == count)
            source_reaction = next((row for row in reaction['cases'] if row['base_count'] == count), None) if branch == 'MTS' else None
            source_work = source_reaction['rank_one_reaction'] if source_reaction else 0.
            perpendicular = source_reaction['perpendicular_remainder'] if source_reaction else 0.
            perpendicular_bound = source_reaction['perpendicular_bound'] if source_reaction else 0.
            shape = bounded['shape_force']
            remaining_rows = next(row for row in bounded['groups'] if row['name'] == 'remaining')
            far_work = remaining_rows['projected_sum']
            primary_defect = remaining+source_work-pressure
            shape_and_remainder = shape+perpendicular+far_work
            inertia_term = -ratio_inertia*(schur['dust_drive']+pressure)
            error = (primary_defect+shape_and_remainder+inertia_term)/(1+ratio_inertia)
            bound = (abs(primary_defect)+bounded['shape_absolute_row_bound']+perpendicular_bound
                +remaining_rows['projected_absolute_sum']+abs(inertia_term))/(1+ratio_inertia)
            actual = item['force']-pressure
            evidence.check(branch+str(count)+'_full_traction_error_identity', abs(error-actual) < 2e-14)
            evidence.check(branch+str(count)+'_full_traction_error_bound', abs(actual) <= bound+2e-14)
            evidence.report['cases'].append(dict(branch=branch, base_count=count,
                force_error_signed=actual, reconstructed_error=error, absolute_error_bound=bound,
                source_reaction=source_work, remaining_free_drive=remaining,
                primary_traction_defect=primary_defect, explicit_shape_and_remaining_row_work=shape_and_remainder,
                source_inertia_error_term=inertia_term, inertia_ratio=ratio_inertia,
                continuum_force=pressure, valid_for_claim=False,
                source_path=item['source_path']))
        resolution = []
        for count, cap in [(257, 2e-5), (513, 1e-5)]:
            model = GradedSourceAction(count, True, source_cap=cap)
            absolute = abs(model.original)
            mask = (absolute @ (model.radii < model.anchor) > 0) & (absolute @ (model.radii > model.anchor) > 0)
            columns = np.asarray(abs(model.original[mask]).sum(axis=0)).ravel() > 0
            offsets = model.radii[columns]-model.anchor
            spacing = model.gram_spacing
            coordinate = (model.anchor-model.base_radii[0])/spacing
            source_phase = coordinate-np.floor(coordinate)
            predicted = np.array([-(3+source_phase)*spacing, (4-source_phase)*spacing])
            support = np.array([min(offsets), max(offsets)])
            evidence.check(str(count)+'_exact_seven_row_support', np.sum(mask) == 7 and max(abs(predicted-support)) < 2e-12)
            front_lengths = np.array([.8, .74])*4e-5
            spacing_limit = min(front_lengths/np.array([3+source_phase, 4-source_phase]))
            resolution.append(dict(base_count=count, source_phase=float(source_phase), bulk_spacing=float(spacing),
                actual_source_stencil_interval=support.tolist(), fixture_front_lengths=front_lengths.tolist(),
                fixed_phase_spacing_limit=float(spacing_limit), bulk_spacing_over_fixture_limit=float(spacing/spacing_limit),
                actual_parent_front_not_asserted=True, valid_for_claim=False))
        phase_safe_limit = .74*4e-5/4
        exponent = int(np.ceil(np.log2(1.6/phase_safe_limit)))
        evidence.report.update(front_resolution_requirements=resolution,
            fixture_phase_safe_spacing_limit=phase_safe_limit,
            prospective_uniform_base_count=2**exponent+1,
            prospective_count_not_allocated_or_authorized=True,
            current_front_fixture_source_force_h_ratio=[row['source_force_over_h'] for row in front['cases']
                if row['source_stencil_front_resolved']],
            next_requirement='Extend force consistency to positive variable geometry and a cost-qualified front-resolved live discretization; do not delete Gram or equate its reaction to missing GR traction by definition.')
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'],
            graded=evidence.report['exact_graded_asymptote'], resolution=resolution,
            prospective_count=evidence.report['prospective_uniform_base_count'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
