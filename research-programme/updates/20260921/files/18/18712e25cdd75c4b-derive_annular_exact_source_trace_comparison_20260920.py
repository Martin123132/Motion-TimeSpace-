from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_P2_overlay_20260919 import compose_rows
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from derive_annular_common_weak_action_20260920 import factor_mapping
from annular_decimal_transport_v2_20260919 import decimal_array
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
import contextlib
import json
import numpy as np


def rational_rows(rows):
    return [{int(column):Fraction(value) for column, value in row.items()} for row in rows]


def jump_row(mesh):
    edges = list(map(Fraction, mesh['edges']))
    source = edges.index(Fraction(mesh['anchor']))
    row = {}
    for element, factors in [(source-1, [-1, 4, -3]), (source, [-3, 4, -1])]:
        width = edges[element+1]-edges[element]
        for index, factor in zip(mesh['elements'][element], factors):
            if index >= 0:
                row[index] = row.get(index, Fraction(0))+Fraction(factor)/width
    return {index:value for index, value in row.items() if value}


def difference(first, last):
    return {index:first.get(index, Fraction(0))-last.get(index, Fraction(0))
        for index in sorted(set(first) | set(last)) if first.get(index, Fraction(0)) != last.get(index, Fraction(0))}


def main():
    evidence = EvidenceRun('annular-exact-source-trace-comparison-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            physical_force_mismatch_fixed=False, trace_witness_not_integrated_force_attribution=True)
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                embeddings = [rational_rows(rows) for rows in packet['embeddings']]
                restrictions = [rational_rows(rows) for rows in packet['left_inverses']]
                coarse_test = compose_rows(restrictions[0], embeddings[1])
                fine_trial = compose_rows(restrictions[1], embeddings[0])
                common_jump = jump_row(packet['overlay'])
                coarse_jump, fine_jump = [jump_row(mesh) for mesh in packet['native']]
                evidence.check(branch+'_common_coarse_jump_exact', compose_rows([common_jump], embeddings[0])[0] == coarse_jump)
                evidence.check(branch+'_common_fine_jump_exact', compose_rows([common_jump], embeddings[1])[0] == fine_jump)
                trial_defect = difference(compose_rows([fine_jump], fine_trial)[0], coarse_jump)
                test_defect = difference(compose_rows([coarse_jump], coarse_test)[0], fine_jump)
                represented_columns = set().union(*(row.keys() for row in coarse_test))
                candidates = sorted(index for index in fine_jump if index not in represented_columns)
                row = dict(branch=branch, trial_jump_commutes_exactly=not trial_defect,
                    test_jump_commutes_exactly=not test_defect, trial_defect_entries=len(trial_defect),
                    test_defect_entries=len(test_defect), exact_coarse_invisible_jump_candidates=candidates,
                    valid_for_claim=False)
                if candidates:
                    index = candidates[0]
                    evidence.check(branch+'_witness_coarse_projection_exact_zero', all(index not in item for item in coarse_test))
                    evidence.check(branch+'_witness_fine_source_jump_nonzero', fine_jump[index] != 0)
                    data = checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-fine-action.npz')
                    witness = np.full((packet['native'][1]['count'], 1), Decimal(0), dtype=object)
                    witness[index, 0] = Decimal(1)
                    values = factor_mapping(data, 'gram').apply(witness)
                    gram_form = sum((decimal_array(data['gram_weights'])[:, None]*values**2).flat, Decimal(0))
                    evidence.check(branch+'_witness_original_Gram_form', gram_form > 0 if branch == 'MTS' else gram_form == 0)
                    row.update(witness_fine_index=index, witness_exact_source_jump=str(fine_jump[index]),
                        witness_native_Gram_form=str(gram_form), projected_coarse_Gram_form='0')
                evidence.report['cases'].append(row)
                output = evidence.output/(branch+'-exact-trace-comparison.json')
                output.write_text(json.dumps(dict(trial_defect={str(index):str(value) for index, value in trial_defect.items()},
                    test_defect={str(index):str(value) for index, value in test_defect.items()},
                    fine_jump={str(index):str(value) for index, value in fine_jump.items()},
                    coarse_jump={str(index):str(value) for index, value in coarse_jump.items()}))+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
