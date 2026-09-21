from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from scipy.integrate import solve_ivp
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-oracle-independent-controls-attempt01', __file__)
    try:
        previous = evidence.output.parent/'annular-live-continuum-evolution-attempt01'
        vacuum_path = previous/'degree64-no_backreaction.npz'
        evidence.own(vacuum_path)
        saved = np.load(vacuum_path)
        live = LiveContinuumCharacteristics(64, 4, 14, radial_spacing=.05, coupling=0.)
        initial_geometry = live.solve(saved['states'][0])
        geometries = [live.solve(state) for state in saved['states']]
        for index in [0, 2, 4]:
            source = initial_geometry.material.source[index]
            static = TwoSidedGRCharacteristics(64)
            static.inner += live.width*live.labels[index]
            static.outer += live.width*live.labels[index]
            radii, unused, unused2 = static.mesh(source[0], .03)
            coefficient = 1-2*.7/radii
            fields = initial_geometry.fields[index]*coefficient[:, None, :]
            initial = static.pack(fields, source.copy())
            result = solve_ivp(static.rhs, (0., .02), initial, method='DOP853', rtol=2e-11, atol=2e-13,
                               max_step=.0005, t_eval=saved['times'])
            field_errors, source_errors = [], []
            for state, geometry in zip(result.y.T, geometries):
                fields, position, momentum, velocity = static.unpack(state)
                radius, unused, unused2 = static.mesh(position, velocity)
                scaled = fields/(1-2*.7/radius[:, None, :])
                field_errors.append(float(np.max(abs(scaled-geometry.fields[index]))))
                source_errors.append(float(np.max(abs(state[-3:]-geometry.material.source[index]))))
            raw = evidence.output/('static-layer'+str(index)+'.npz')
            np.savez_compressed(raw, times=result.t, states=result.y.T, field_errors=field_errors, source_errors=source_errors)
            evidence.own(raw, 'outputs')
            row = dict(layer=index, field_error=max(field_errors), source_error=max(source_errors))
            evidence.report['cases'].append(row)
            print(row, flush=True)
            evidence.check(str(index)+'_different_variable_static_GR_solver_agrees', result.success and max(field_errors) < 2e-8
                           and max(source_errors) < 2e-9, row)
        dust_path = previous/'degree64-dust.npz'
        evidence.own(dust_path)
        saved_dust = np.load(dust_path)
        dust = LiveContinuumCharacteristics(64, 4, 14, radial_spacing=.05, wave=False)
        initial_geometry = dust.solve(saved_dust['states'][0])
        final_geometry = dust.solve(saved_dust['states'][-1])
        for index in range(5):
            initial_source = initial_geometry.material.source[index]
            final_source = final_geometry.material.source[index]
            mass = initial_geometry.evaluate(initial_source[0], initial_geometry.mass_coefficients)
            unused, initial_root = initial_geometry.metric(initial_source[0])
            unused, final_root = final_geometry.metric(final_source[0])
            proper_speed = initial_root**2*initial_source[1]/dust.source_mass
            exact = solve_ivp(lambda time, state: [state[1], -mass/state[0]**2], (0., final_source[2]),
                              [initial_source[0], proper_speed], method='DOP853', rtol=2e-12, atol=2e-14)
            error = float(np.max(abs(exact.y[:, -1]-[final_source[0], final_root**2*final_source[1]/dust.source_mass])))
            evidence.check(str(index)+'_independent_dust_proper_clock_orbit', exact.success and error < 2e-10, error)
        evidence.report.update(zero_coupling_compared_to_different_characteristic_variables=True,
                               no_wave_compared_to_independent_proper_time_ODE=True,
                               real_wave_backreaction_still_requires_separate_qualification=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
