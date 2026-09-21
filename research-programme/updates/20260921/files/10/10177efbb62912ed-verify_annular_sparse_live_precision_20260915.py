from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_live_repaired_20260915 import SparseRepairedLiveSystem
from annular_sparse_live_tangent_20260915 import SparseLiveTangent
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from run_annular_sparse_live_refinement_20260915 import compare
from functools import lru_cache
import numpy as np
import json
import time


class CachedTangent(SparseLiveTangent):
    @lru_cache(maxsize=32)
    def layer_data(self, offset):
        return super().layer_data(offset)

    @lru_cache(maxsize=1024)
    def current_parts(self, offset, target):
        full = super().wave_current(offset, target, True)
        layer, coordinates, rates, unused, data, euler, unused2, unused3, unused4 = self.layer_data(offset)
        selected = layer.radii < target if target < coordinates[-1] else layer.radii > target
        correction = np.sum((euler*rates[:-1])[selected])
        if target >= coordinates[-1]:
            correction = -correction
        return full, full-correction

    def wave_current(self, offset, target, retain_euler=True):
        if not self.system.base[0]+self.system.width*offset < target < self.system.base[-1]+self.system.width*offset:
            return super().wave_current(offset, target, retain_euler)
        return self.current_parts(float(offset), float(target))[0 if retain_euler else 1]


def main():
    evidence = EvidenceRun('annular-sparse-live-precision-controls-attempt01', __file__)
    try:
        phase = evidence.output.parent/'annular-sparse-live-phase-refinement-attempt01'
        half = evidence.output.parent/'annular-sparse-live-halfstep-controls-attempt01'
        fine = evidence.output.parent/'annular-sparse-live-fine-refinement-attempt01'
        for folder in [phase, half, fine]:
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(folder.name+'_completed_before_controls', status['state'] == 'complete')
        for branch in ['reference', 'MTS']:
            paths = [folder/(branch+'-129.npz') for folder in [phase, half]]
            for path in paths:
                evidence.own(path)
            error = float(np.max(abs(np.load(paths[0])['state']-np.load(paths[1])['state'])))
            evidence.check(branch+'_whole_129_trajectory_halfstep', error < 2e-9, error)
        oracle_path = evidence.output.parent/'annular-live-continuum-refinement-attempt02/degree384.npz'
        evidence.own(oracle_path)
        saved_oracle = np.load(oracle_path)
        oracle = BarycentricLiveContinuum(384, 8, 18, radial_spacing=.025, label_order=12)
        oracle_geometries = [oracle.solve(state) for state in saved_oracle['states']]
        for branch in ['reference', 'MTS']:
            gram = branch == 'MTS'
            control_path = phase/(branch+'-129.npz')
            saved = np.load(control_path)
            system = SparseRepairedLiveSystem(129, gram, 8, 10)
            coordinates, momenta = saved['state'][:2*9*130, -1].reshape(2, 9, 130)
            tangent = CachedTangent(system, coordinates, momenta)
            target = 6.03
            for retain in [True, False]:
                cached = tangent.wave_current(.07, target, retain)
                original = SparseLiveTangent.wave_current(tangent, .07, target, retain)
                evidence.check(branch+'_current_cache_equivalence_'+str(retain), abs(cached-original) < 2e-12, float(abs(cached-original)))
            for count in [513, 1025]:
                key = branch+'-'+str(count)
                path = fine/(key+'.npz')
                evidence.own(path)
                saved = np.load(path)
                diagnostic_path = fine/(key+'-diagnostics.json')
                evidence.own(diagnostic_path)
                previous = json.loads(diagnostic_path.read_text())
                system = SparseRepairedLiveSystem(count, gram, 8, 10)
                size = 2*9*(count+1)
                started = time.perf_counter()
                changes, errors = [], []
                for state, geometry, row in zip(saved['state'].T, oracle_geometries, previous['times']):
                    coordinates, momenta = state[:size].reshape(2, 9, count+1)
                    rates, actual_geometry = system.solve(coordinates, momenta)
                    control = compare(system, coordinates, rates, state[size:], actual_geometry, oracle, geometry)
                    changes.append(abs(control['field_error']-row['field_error']))
                    errors.append(control['field_error'])
                summary = dict(branch=branch, count=count, maximum_384_field_error=float(max(errors)),
                    maximum_change_from_512=float(max(changes)),
                    finest_margin_exceeds_oracle_change=bool(previous['summary']['maximum_field_error']+max(changes) < .005),
                    uncertainty_estimate_not_rigorous_error_bound=True, valid_for_physics_claim=False)
                evidence.check(key+'_oracle_refinement_small_against_field_gate', max(changes) < 5e-5, summary)
                tangent = CachedTangent(system, coordinates, momenta)
                noether = tangent.noether(0.)
                summary['noether'] = noether
                evidence.check(key+'_fine_moving_interface_Noether', noether['noether'] < 2e-10, summary)
                current = tangent.compare(np.array([5.90, 6.03, 6.15]), label_order=10)
                path = evidence.output/(key+'-current.npz')
                np.savez_compressed(path, **current)
                evidence.own(path, 'outputs')
                summary.update(current_error=current['error'], on_shell_current_error=current['on_shell_error'],
                    seconds=time.perf_counter()-started)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(summary, flush=True)
                evidence.check(key+'_independent_temporal_mass_equation', current['on_shell_error'] < 2e-8, summary)
                tangent.layer_data.cache_clear()
                tangent.current_parts.cache_clear()
        evidence.report.update(time_step_control_129_not_all_grids=True,
            independent_oracle_changed_without_changing_finite_data=True,
            source_cell_crossing_qualified=False, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
