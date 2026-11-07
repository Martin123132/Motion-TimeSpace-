from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_native_position_precision_20260929 import NativePrecision
from scipy.sparse import load_npz
import hashlib
import json
import numpy as np


def inherited_sources(evidence):
    path = evidence.output.parent / 'annular-mts-position-reaction-final-integrity-20260929.json'
    seal = json.loads(path.read_text())
    evidence.own(path)
    evidence.check('prior_seal_complete', seal['state'] == 'complete' and seal['all_four_diagnostics_complete'])
    digests = {}
    for relative, expected in seal['hashes'].items():
        if relative == 'CURRENT_LOCAL_RESUME.md':
            continue
        source = (evidence.root / relative).resolve()
        if not source.is_relative_to(evidence.root) or not source.is_file():
            raise RuntimeError('Missing or out-of-scope parent input: ' + relative)
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Changed parent input: ' + relative)
        digests[relative] = expected
        evidence.own(source)
    evidence.check('inherited_hashes_match', len(digests) == len(seal['hashes']) - 1, len(digests))
    return digests


def restore_native(evidence, digests, branch, level, deadline):
    def read(relative):
        path = (evidence.root / relative).resolve()
        key = str(path.relative_to(evidence.root))
        if hashlib.sha256(path.read_bytes()).hexdigest() != digests[key]:
            raise RuntimeError('Changed native input: ' + key)
        evidence.own(path)
        if path.suffix == '.json':
            return json.loads(path.read_text())
        with np.load(path, allow_pickle=False) as archive:
            return {name: archive[name].copy() for name in archive.files}

    def status(name):
        return read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))

    def match(report):
        return next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)

    loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
    for relative in sources.values():
        evidence.own(evidence.root / relative)
    live = match(status('annular-live-support-acceleration-attempt01'))
    positions = match(status('annular-compensated-position-attempt04'))
    jets = match(status('annular-position-metric-jet-validation-attempt01'))
    directions = read(live['direction_path'])
    correction = read(live['paths']['projection'])['correction']

    def response(archive):
        solver, solution = reconstructed_solver(archive)
        return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

    position = ResponseSum(response(read(positions['paths']['response'])),
        response(read(jets['paths']['transported_old_metric'])))
    packet = read(sources['packet'])
    native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
    owner = read(sources['parent'])
    centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
    matrix_path = evidence.root / centre['matrix_path']
    if hashlib.sha256(matrix_path.read_bytes()).hexdigest() != digests[centre['matrix_path']]:
        raise RuntimeError('Changed inherited mass matrix')
    evidence.own(matrix_path)
    inverse = BandedSourceInverse(load_npz(matrix_path), loads.rates.shape)
    precision = NativePrecision(native, loads, action, directions['field_vertices'] - correction[:, :-1],
        -correction[:, -1], directions['edge_vertices'], position)
    parent = match(status('annular-position-reaction-diagnostic-attempt04'))
    return dict(loads=loads, action=action, native=native, precision=precision, inverse=inverse,
        original={order: read(parent['paths']['material' + str(order)]) for order in [48, 64]}, read=read)
