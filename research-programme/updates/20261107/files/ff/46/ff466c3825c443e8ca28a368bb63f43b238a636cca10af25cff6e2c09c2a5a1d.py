from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import restore_native
from annular_C0_boundary_integral_20260930 import PositionIntegral
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
import hashlib
import json


def restore(evidence, branch, level, deadline):
    path = evidence.output.parent/'annular-C0-integral-stage-integrity-20260930.json'
    seal = json.loads(path.read_text())
    evidence.own(path)
    evidence.check('C0_parent_seal_complete', seal['state'] == 'complete' and not seal['mismatches'])
    digests = {}
    for relative, expected in seal['hashes'].items():
        source = (evidence.root/relative).resolve()
        if not source.is_relative_to(evidence.root) or not source.is_file():
            raise RuntimeError('Invalid transport input '+relative)
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Changed transport input '+relative)
        digests[str(source.relative_to(evidence.root))] = expected
        evidence.own(source)
    setup = restore_native(evidence, digests, branch, level, deadline)
    action, read = setup['action'], setup['read']
    report = lambda name:read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
    match = lambda status:next(row for row in status['cases'] if row['branch'] == branch and row['level'] == level)
    live = match(report('annular-live-support-acceleration-attempt01'))
    jets = match(report('annular-position-metric-jet-validation-attempt01'))
    flow = match(report('annular-direct-background-coupled-current-attempt01'))

    def response(archive):
        solver, solution = reconstructed_solver(archive)
        return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

    directions = read(live['direction_path'])
    correction = read(live['paths']['projection'])['correction']
    mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
    acceleration = read(flow['paths']['flow'])['acceleration']
    time = ResponseSum(response(read(flow['paths']['background_response'])), response(read(flow['paths']['velocity_response'])))
    owner = report('annular-wave-flux-live-response-'+level+'-attempt01')
    selected = next(row for row in owner['cases'] if row['summary']['branch'] == branch)
    candidate = read(selected['paths']['candidate'])
    evaluator = PositionIntegral(action, directions, correction, mode_rate, acceleration,
        candidate['acceleration_change'], setup['precision'].position, time, response(candidate))
    return dict(evaluator=evaluator, setup=setup, read=read, report=report, candidate=candidate,
        metric_time=time, mixed=response(candidate))
