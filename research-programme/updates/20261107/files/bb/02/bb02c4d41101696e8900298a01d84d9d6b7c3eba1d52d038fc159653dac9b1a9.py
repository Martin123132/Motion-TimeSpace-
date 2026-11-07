from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from decimal import Decimal, localcontext
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-wave-label-monotonicity-attempt01', __file__)
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, github_action=False, subagents_used=False)
        intake = evidence.output.parent
        seal_path = intake/'annular-native-precision-repair-integrity-20260929.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('prior_seal_complete', seal['state'] == 'complete')

        def read(path):
            relative = str(path.relative_to(evidence.root))
            if hashlib.sha256(path.read_bytes()).hexdigest() != seal['hashes'][relative]:
                raise RuntimeError('Changed monotonicity input: '+relative)
            evidence.own(path)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {name: archive[name].copy() for name in archive.files}

        with localcontext() as context:
            context.prec = 70
            for branch in ['reference', 'MTS']:
                original = read(intake/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
                overlay = read(intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
                native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
                owner = common_material(native, original, overlay)[0]
                for level in ['fine', 'third']:
                    short = 'reference' if branch == 'reference' else 'MTS-primary'
                    suffix = '-matched-current-attempt01' if level == 'fine' else '-third-current-attempt02'
                    parent = read(intake/('annular-'+short+suffix)/'status.json')
                    centre = next(row for row in parent['centres'] if row.get('route') == 'resampled') if level == 'fine' else parent['centres'][0]
                    state = read(evidence.root/centre['state_path'])
                    source = np.asarray(state['coordinates'][:, -1], float)
                    coefficients = owner.layer_rule.inverse @ (source-owner.model.anchor)
                    exact = [Decimal.from_float(float(value)) for value in coefficients]
                    tail = sum((2*index**2*abs(value) for index, value in enumerate(exact) if index >= 2), Decimal(0))
                    source_lower, source_upper = 2*exact[1]-tail, 2*exact[1]+tail
                    width = Decimal.from_float(float(owner.width))
                    face_lower, face_upper = min(source_lower, width), max(source_upper, width)
                    max_shift = abs(exact[0])+abs(exact[1]-width/2)+sum(map(abs, exact[2:]), Decimal(0))
                    evidence.check(branch+':'+level+':strict_label_monotonicity', face_lower > 0,
                        dict(lower=str(face_lower), upper=str(face_upper), source_tail=str(tail)))
                    evidence.report['cases'].append(dict(branch=branch, level=level,
                        exact_binary64_coefficient_derivative_lower=str(source_lower),
                        exact_binary64_coefficient_derivative_upper=str(source_upper),
                        all_material_faces_derivative_lower=str(face_lower),
                        all_material_faces_derivative_upper=str(face_upper),
                        source_minus_linear_label_max=str(max_shift), source_coefficients=coefficients.tolist(),
                        proof='|U_(k-1)(x)| <= k on [-1,1]; face derivative is a convex combination with the positive layer width',
                        valid_for_claim=False))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
