from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_position_reaction_20260929 import second_radial
from annular_source_centered_quadrature_20260929 import metric_at_offset as recentered_values
from annular_registered_metric_coordinates_20260929 import metric_at_offset as registered_values
from fractions import Fraction
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-registered-metric-center-diagnostic-attempt01', __file__)
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False,
            numerical_acceptance_passed=False, full_force_recomputed=False,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.own(evidence.root/'DERIVATION-20260929-registered-metric-centers.md')
        seal_path = evidence.output.parent/'annular-position-reaction-stage-integrity-20260929.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('prior_reaction_seal_complete', seal['state'] == 'complete')

        def read(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if hashlib.sha256(path.read_bytes()).hexdigest() != seal['hashes'][key]:
                raise RuntimeError('Changed polynomial input: '+key)
            evidence.own(path)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {name: archive[name].copy() for name in archive.files}

        for branch in ['reference-reference', 'MTS-primary']:
            short = 'reference' if branch == 'reference-reference' else branch
            for level in ['fine', 'third']:
                parent_name = 'annular-'+short+('-matched-current-attempt01' if level == 'fine' else '-third-current-attempt02')
                parent = read(str((evidence.output.parent/parent_name/'status.json').relative_to(evidence.root)))
                centre = next(row for row in parent['centres'] if row.get('route') == 'resampled') if level == 'fine' else parent['centres'][0]
                archive = read(centre['state_path'])
                folder = 'annular-nested-refinement-preparation-attempt02' if level == 'fine' else 'annular-resampled-third-grid-preparation-attempt01'
                suffix = '-refined-action.json' if level == 'fine' else '-third-action.json'
                packet = read(str((evidence.output.parent/folder/(branch+suffix)).relative_to(evidence.root)))
                anchor = float(Fraction(packet['mesh']['anchor']))
                solver, solution = reconstructed_solver(archive)
                radii = (solver.centers[:, None]+solver.lengths[:, None]*np.array([-.73, 0., .61])/2).ravel()
                offsets = radii-anchor
                original = solver.values(solution, radii)
                registered = registered_values(solver, solution, offsets, anchor)
                recentered = recentered_values(solver, solution, offsets, anchor)
                original_second = second_radial(solver, solution, radii)
                registered_second = registered_values(solver, solution, offsets, anchor, second=True)
                recentered_second = recentered_values(solver, solution, offsets, anchor, second=True)
                shifted_edges = solver.edges-anchor
                maximum = lambda array: float(np.max(np.abs(array)))
                exact = all(np.array_equal(first, second) for first, second in zip(original, registered))
                exact = exact and np.array_equal(original_second, registered_second)
                evidence.check(branch+'-'+level+':registered_evaluation_exact_replay', exact,
                    dict(value_error=maximum(original[0]-registered[0]), radial_error=maximum(original[1]-registered[1]),
                        second_error=maximum(original_second-registered_second)))
                row = dict(branch=branch, level=level, points=len(radii), registered_exact_replay=exact,
                    old_recentered_value_error=maximum(original[0]-recentered[0]),
                    old_recentered_radial_error=maximum(original[1]-recentered[1]),
                    old_recentered_second_error=maximum(original_second-recentered_second),
                    midpoint_recomputation_shift=maximum((shifted_edges[:-1]+shifted_edges[1:])/2-(solver.centers-anchor)),
                    valid_for_claim=False)
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps(row), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
