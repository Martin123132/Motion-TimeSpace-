from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, IndexedP2Material
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-local-Gram-bound-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            no_terms_removed=True, no_uniform_smallness_claim=True,
            source_partition_from_stencil_support_not_data_fit=True)
        prior_path = evidence.output.parent/'annular-P2-Gram-projected-drive-attempt01/status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('prior_drive_checkpoint_complete', prior['state'] == 'complete'
            and all(row['passed'] for row in prior['checks']))
        for branch in ['reference', 'MTS']:
            cases = [(257, 2e-5, 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01'),
                    'steps32-accepted032.npz'),
                (513, 1e-5, 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS'
                    else 'annular-P2-bulk513-evolution-reference-attempt01',
                    'steps128-accepted128.npz' if branch == 'MTS' else 'steps64-accepted064.npz')]
            for count, cap, folder, filename in cases:
                saved = checked_load(evidence, folder, filename)
                coordinates, momenta = saved['state']
                system = IndexedGradedP2System(count, branch == 'MTS', cap)
                rates, geometry = system.solve(coordinates, momenta)
                interpolation = IndexedP2Material(system, coordinates).interpolation(np.array([0.]))[0]
                layer = system.layer(0., geometry)
                row, arrays = row_bounds(layer, interpolation @ coordinates, interpolation @ rates)
                previous = next(item for item in prior['cases'] if item['branch'] == branch and item['base_count'] == count)
                key = branch+str(count)
                evidence.check(key+'_same_original_drive', abs(row['explicit_drive']-previous['explicit_Gram_drive']) < 2e-12
                    and abs(row['shape_force']-previous['explicit_Gram_shape_force']) < 2e-12)
                evidence.check(key+'_partition_retains_all_rows', sum(group['rows'] for group in row['groups']) == row['row_count'])
                scale = max(1e-30, row['projected_global_bound'])
                tolerance = 2e-14*scale
                evidence.check(key+'_bound_hierarchy', abs(row['projected_drive']) <= row['projected_absolute_row_bound']+tolerance
                    and row['projected_absolute_row_bound'] <= row['projected_partitioned_bound']+tolerance
                    and row['projected_partitioned_bound'] <= row['projected_global_bound']+tolerance
                    and abs(row['explicit_drive']) <= row['drive_absolute_row_bound']+tolerance)
                if row['diagonal_margin_projection_bound_available']:
                    evidence.check(key+'_finite_mass_projection_bound', row['projection_maximum']
                        <= row['diagonal_margin_projection_bound']*(1+2e-12))
                if branch == 'reference':
                    evidence.check(key+'_zero_Gram_control', row['row_count'] == 0 and row['drive_partitioned_bound'] == 0)
                else:
                    evidence.check(key+'_source_partition_nontrivial', 0 < row['source_rows'] < row['row_count'])
                    evidence.check(key+'_omitted_source_rows_negative_control', abs(row['groups'][0]['projected_sum']) > 1e-10)
                row.update(branch=branch, base_count=count, time=float(saved['time']), valid_for_claim=False,
                    source_path=str((evidence.output.parent/folder/'status.json').relative_to(evidence.root)))
                path = evidence.output/(key+'-row-data.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps(row), flush=True)
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
