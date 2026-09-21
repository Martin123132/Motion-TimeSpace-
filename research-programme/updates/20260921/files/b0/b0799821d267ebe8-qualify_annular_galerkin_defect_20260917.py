from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_characteristic_galerkin_defect_20260917 import nodal_reference, canonical_defect, mass_dual_norm, weak_defects
import argparse
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--counts', nargs='+', type=int, default=[33, 65, 129, 257, 513, 1025, 2049])
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_finite_trajectory_rerun=True, source_field_momentum_retained=True,
            pointwise_force_convergence_proven=False, all_time_supremum_numerically_certified=False,
            finite_samples_not_asymptotic_proof=True, force_fit=False, force_correction=False)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for label in ['annular-full-characteristic-field-attempt01', 'annular-actual-reference-regularity-attempt01']:
            path = intake/label/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        reference = FullCharacteristicField(tight=True)
        times = np.array([0., .071, .173, .21, .317, .4])
        for count in options.counts:
            base = LocallyRefinedSourceAction(count, False, background_mass=0., source_splits=8)
            mts = LocallyRefinedSourceAction(count, True, background_mass=0., source_splits=8)
            base_model, mts_model = FlatPreassembledFlow(base), FlatPreassembledFlow(mts)
            cases, arrays = [], {}
            for instant in times:
                state, derivative = nodal_reference(base, reference, instant)
                covector, unused, matrices, flow_defect = canonical_defect(base_model, state, derivative)
                full, gram, unused, mts_defect = canonical_defect(mts_model, state, derivative)
                direct = weak_defects(base, reference, instant, state, derivative, order=10)
                control = weak_defects(base, reference, instant, state, derivative, order=14)
                prefix = str(count)+'_'+str(instant)
                identity = mass_dual_norm(covector-direct['interpolated'], matrices)
                continuum = mass_dual_norm(direct['exact'], matrices)
                quadrature = max(mass_dual_norm(direct[name]-control[name], matrices) for name in ['exact', 'interpolated'])
                error_identity = float(max(abs(direct['direct_error_field']-(direct['interpolated']-direct['exact'])[:-1])))
                gram_identity = mass_dual_norm(full-covector-gram, matrices)
                evidence.check(prefix+'_original_flow_vs_independent_weak_EL', identity < 2e-8, identity)
                evidence.check(prefix+'_continuum_field_and_source_weak_balance', continuum < 2e-8, continuum)
                evidence.check(prefix+'_split_quadrature_control', quadrature < 2e-8, quadrature)
                evidence.check(prefix+'_explicit_interpolation_error_identity', error_identity < 2e-11, error_identity)
                evidence.check(prefix+'_canonical_Gram_split', gram_identity < 2e-8, gram_identity)
                evidence.check(prefix+'_pullback_chain_rule', direct['reference_material_derivative_identity'] < 3e-13,
                    direct['reference_material_derivative_identity'])
                evidence.check(prefix+'_position_and_clock_defects_zero', np.max(abs(flow_defect[:base.count+1])) < 1e-15
                    and abs(flow_defect[-1]) < 1e-15 and np.max(abs(mts_defect[:base.count+1])) < 1e-15 and abs(mts_defect[-1]) < 1e-15)
                row = dict(base_count=count, scalar_dofs=base.count, time=float(instant), h=base.gram_spacing,
                    base_canonical_defect=mass_dual_norm(covector, matrices), extra_Gram_canonical_defect=mass_dual_norm(gram, matrices),
                    total_MTS_canonical_defect=mass_dual_norm(full, matrices), base_source_covector=float(covector[-1]),
                    continuum_weak_defect=continuum, independent_EL_identity_error=identity,
                    quadrature_control=quadrature, canonical_Gram_identity_error=gram_identity,
                    interpolation_L2=direct['error_norms'], interpolation_L1=direct['error_L1'])
                cases.append(row)
                arrays[str(instant)+'_base'] = covector
                arrays[str(instant)+'_Gram'] = gram
                arrays[str(instant)+'_MTS'] = full
                evidence.report['progress'] = dict(count=count, accepted_time=float(instant))
                evidence.save()
            destination = evidence.output/('defects-'+str(count)+'.npz')
            np.savez_compressed(destination, times=times, **arrays)
            evidence.own(destination, 'outputs')
            row = dict(base_count=count, h=base.gram_spacing,
                maximum_sampled_base_defect=max(value['base_canonical_defect'] for value in cases),
                maximum_sampled_Gram_defect=max(value['extra_Gram_canonical_defect'] for value in cases),
                maximum_sampled_MTS_defect=max(value['total_MTS_canonical_defect'] for value in cases),
                maximum_sampled_base_source=max(abs(value['base_source_covector']) for value in cases), cases=cases)
            evidence.report['cases'].append(row)
            evidence.save()
            print({name: value for name, value in row.items() if name != 'cases'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
