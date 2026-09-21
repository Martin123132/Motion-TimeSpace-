from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_frozen_initial_layer_20260917 import FrozenInitialLayer
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.integrate import solve_ivp
from datetime import datetime, timezone
import argparse
import json
import time
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    started = time.monotonic()
    try:
        protocol = dict(frozen_at=datetime.now(timezone.utc).isoformat(), counts=[513, 1025],
            branches=['reference', 'MTS'], source_splits=8, physical_horizon=.02, scaled_plot_horizon=6.4,
            comparison_times=[0., .005, .01, .015, .02], fit_parameters=[], both_branches_same_protocol=True,
            diagnostic_explanation_fraction=.25, diagnostic_fraction_not_physics_gate=True,
            nonlinear_trajectories_not_read_or_rerun=True)
        path = evidence.output/'prediction-protocol.json'
        path.write_text(json.dumps(protocol, indent=2)+'\n', encoding='utf-8')
        evidence.own(path, 'outputs')
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_nonlinear_forward_trajectory_rerun=True, frozen_linear_response_not_original_nonlinear_trajectory=True,
            uniform_nonlinear_remainder_proven=False, all_source_Gram_terms_retained=True, source_field_inertia_retained=True,
            old_peak_force_gates_unchanged=True, force_fit=False, force_correction=False, protocol=protocol)
        generator = np.random.default_rng(20260917)
        for count in protocol['counts']:
            for branch in protocol['branches']:
                system = LocallyRefinedSourceAction(count, branch == 'MTS', background_mass=0., source_splits=8)
                model = FlatPreassembledFlow(system)
                layer = FrozenInitialLayer(model, initial(system))
                prefix = branch+str(count)
                direction = generator.normal(size=len(layer.state))*layer.scale
                covector = generator.normal(size=len(layer.state))
                actual = layer.multiply(direction)
                complex_check = model.evaluate(layer.state.astype(complex)+1e-25j*direction)['flow'].imag/1e-25
                normalized = float(max(abs(actual-complex_check))/max(1., max(abs(actual))))
                evidence.check(prefix+'_Jacobian_complex_direction', normalized < 2e-11, normalized)
                transpose = layer.adjoint.transpose(layer.state, covector, layer.context)
                duality = float(abs(covector @ actual-transpose @ direction)/max(1., abs(covector @ actual)))
                evidence.check(prefix+'_Jacobian_transpose_duality', duality < 2e-11, duality)
                initial_slope = float(layer.gradient @ layer.base_flow)
                evidence.check(prefix+'_scaled_initial_flow', max(abs(layer.scaled_rhs(0., np.zeros_like(direction))*layer.scale
                    /system.gram_spacing-layer.base_flow)) < 2e-12)
                scaled_times = np.linspace(0., 6.4, 129)
                physical_times = np.linspace(0., .02, 129)
                times = np.unique(np.concatenate([scaled_times*system.gram_spacing, physical_times]))
                tau = times/system.gram_spacing
                controls = []
                settings = [('standard', 2e-10, 2e-12, .04), ('tight', 2e-12, 2e-14, .02)]
                for setting, relative, absolute, maximum_step in settings:
                    def guarded_rhs(instant, state):
                        if time.monotonic()-started > 2400:
                            raise TimeoutError('Bounded frozen-response budget exceeded; no nonlinear job was launched.')
                        return layer.scaled_rhs(instant, state)

                    solution = solve_ivp(guarded_rhs, (0., tau[-1]), np.zeros_like(layer.state), t_eval=tau,
                        method='DOP853', rtol=relative, atol=absolute, max_step=maximum_step)
                    evidence.check(prefix+setting+'_frozen_integration_complete', solution.success and np.isfinite(solution.y).all())
                    displacements, linear_force, evaluated_force, linear_rate = layer.reconstruct(solution.y.T)
                    destination = evidence.output/(prefix+'-'+setting+'-frozen-layer.npz')
                    np.savez_compressed(destination, times=times, tau=tau, displacements=displacements, linear_force=linear_force,
                        evaluated_force=evaluated_force, linear_force_rate=linear_rate, initial_state=layer.state,
                        initial_flow=layer.base_flow, force_gradient=layer.gradient)
                    evidence.own(destination, 'outputs')
                    controls.append(dict(linear_force=linear_force, evaluated_force=evaluated_force, displacements=displacements,
                        linear_force_rate=linear_rate, nfev=solution.nfev))
                    evidence.save()
                    print(dict(case=prefix, setting=setting, nfev=solution.nfev, elapsed_seconds=time.monotonic()-started), flush=True)
                standard, tight = controls
                force_control = float(max(abs(standard['linear_force']-tight['linear_force'])))
                evaluated_control = float(max(abs(standard['evaluated_force']-tight['evaluated_force'])))
                evidence.check(prefix+'_frozen_force_time_control', max(force_control, evaluated_control) < 2e-10,
                    dict(linear=force_control, evaluated=evaluated_control))
                phase = (system.anchor-system.base_radii[0])/system.gram_spacing
                row = dict(branch=branch, base_count=count, scalar_dofs=system.count, h=system.gram_spacing,
                    source_phase=float(phase-np.floor(phase)), initial_force=layer.base_force, initial_force_slope=initial_slope,
                    physical_horizon=float(times[-1]), tau_horizon=float(tau[-1]),
                    force_time_control=force_control, evaluated_force_time_control=evaluated_control,
                    state_time_control=float(np.max(abs(standard['displacements']-tight['displacements']))),
                    rate_time_control=float(max(abs(standard['linear_force_rate']-tight['linear_force_rate']))),
                    maximum_observable_Taylor_remainder=float(max(abs(tight['linear_force']-tight['evaluated_force']))),
                    standard_nfev=standard['nfev'], tight_nfev=tight['nfev'])
                evidence.report['cases'].append(row)
                evidence.save()
        evidence.report['predictions_frozen_at'] = datetime.now(timezone.utc).isoformat()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
