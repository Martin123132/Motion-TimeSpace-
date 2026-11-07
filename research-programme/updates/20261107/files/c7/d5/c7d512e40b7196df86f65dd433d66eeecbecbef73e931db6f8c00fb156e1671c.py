from grid_common import *
from compare_responses import load_run
sys.path.insert(0, str(WAVES))
from coupled_system import CoupledSystem


class FrozenReference:
    def __init__(self, heat, inertia):
        self.masses = np.zeros(2)
        self.values = dict(scale=1e-5, fields=np.zeros(2), prime=np.zeros(2), hubble=1.,
                           cold=0., baryon=inertia - 5 * heat / 3, photon=1., neutrino=0.)

    def at(self, moment):
        return self.values


class ThermalStress(CoupledSystem):
    def __init__(self, reference, heat):
        super().__init__(reference, 8)
        self.heat = heat
        self.temperatures = np.zeros(4, complex)

    def stress(self, moment, states):
        original = super().stress(moment, states)
        scale = self.background.at(moment)['scale']
        result = []
        for index, (energy, current, spatial) in enumerate(original):
            velocity = self.unpack(states[index])['velocity']
            internal = self.heat * self.temperatures[index]
            result.append((energy + internal, current + scale * (5 * self.heat / 3) * velocity,
                           spatial + (2 * internal / 3) * np.eye(3)))
        return result


def state_from_spectral(system, blocks, values):
    output = np.zeros((4, system.size), complex)
    axis = np.array([1., 0., 0.])
    photon = np.zeros((system.count, 3, 3), complex)
    for degree, (block, state) in enumerate(zip(blocks, values)):
        tensors, _ = modal_tensors(system.directions, axis, degree)
        points = len(block['nodes'])
        for mode in range(len(block['names'])):
            component = state[mode * points:(mode + 1) * points]
            amplitude = (2 * degree + 1) / 2 * (block['nodes'] @ block['mass'] @ component)
            photon += amplitude * tensors[mode]
    output[0, 23] = values[1][-1]
    output[0, 26:26 + 9 * system.count] = photon.ravel()
    system.temperatures[:] = 0
    system.temperatures[0] = values[0][-1]
    return output


def main():
    modest()
    folder = ROOT / 'results/stress-interface'
    assert not folder.exists()
    labels = ['synthetic-192-refined', 'synthetic-224-band']
    checks, rows, inputs = [], [], []
    for label in labels:
        blocks = load_run(label)
        heat, inertia = float(blocks[0]['capacity']), float(blocks[1]['capacity'])
        reference = FrozenReference(heat, inertia)
        thermal = ThermalStress(reference, heat)
        for kind in ['instantaneous-source', 'integrated-exchange']:
            if kind == 'instantaneous-source':
                values = [linalg.cho_solve(linalg.cho_factor(block['metric'], lower=True),
                                          block['initial_collision_covector']) for block in blocks]
            else:
                values = [block['defects'][-1] - block['defects'][0] for block in blocks]
            state = state_from_spectral(thermal, blocks, values)
            temperature, velocity = values[0][-1], values[1][-1]
            heat_exchange = heat * temperature
            momentum_exchange = inertia * velocity
            direct_energy = blocks[0]['invariants'][-1, :-1] @ values[0][:-1]
            direct_flux = blocks[1]['invariants'][-1, :-1] @ values[1][:-1]
            radiation = thermal.moments(state[0])[0]
            energy_match = float(abs(radiation[0] - direct_energy) / abs(heat_exchange))
            flux_match = float(abs(radiation[1][0] - direct_flux) / abs(momentum_exchange))
            full = thermal.constraints(0., state)[0]
            old = CoupledSystem(reference, 8).constraints(0., state)[0]
            scale = reference.values['scale']
            heat_constraint_scale = 2 * scale ** 2 * abs(heat_exchange)
            momentum_constraint_scale = scale ** 2 * abs(momentum_exchange)
            hamiltonian_error = float(abs(full[0]) / heat_constraint_scale)
            momentum_error = float(np.linalg.norm(full[1:]) / momentum_constraint_scale)
            pressure = thermal.stress(0., state)[0][2] - radiation[2]
            pressure_error = float(np.linalg.norm(pressure - (2 * heat_exchange / 3) * np.eye(3)) / abs(heat_exchange))
            old_heat_error = float(abs(old[0]) / heat_constraint_scale)
            omitted_enthalpy = scale ** 2 * abs((5 * heat / 3) * velocity)
            old_momentum_error = float(abs(old[1]) / omitted_enthalpy)
            checks.extend([
                dict(name=label + ':' + kind + ': independent tensor-to-energy source map', passed=energy_match < .002, value=energy_match),
                dict(name=label + ':' + kind + ': independent tensor-to-momentum source map', passed=flux_match < 1e-9, value=flux_match),
                dict(name=label + ':' + kind + ': collision tangent preserves inherited Hamiltonian constraint',
                     passed=hamiltonian_error < .002, value=hamiltonian_error),
                dict(name=label + ':' + kind + ': collision tangent preserves inherited momentum constraint',
                     passed=momentum_error < 1e-9, value=momentum_error),
                dict(name=label + ':' + kind + ': ideal-gas spatial stress accompanies internal energy',
                     passed=pressure_error < .002, value=pressure_error),
                dict(name=label + ':' + kind + ': removing heat correctly fails at the heat-transfer scale',
                     passed=.998 < old_heat_error < 1.002, value=old_heat_error),
                dict(name=label + ':' + kind + ': removing thermal enthalpy correctly fails at its own scale',
                     passed=.98 < old_momentum_error < 1.02, value=old_momentum_error)])
            rows.append(dict(fixture=label, probe=kind, heat_exchange_magnitude=float(abs(heat_exchange)),
                             momentum_exchange_magnitude=float(abs(momentum_exchange)),
                             normalized_hamiltonian_residual=hamiltonian_error,
                             normalized_momentum_residual=momentum_error,
                             heat_omission_control=old_heat_error, enthalpy_omission_control=old_momentum_error))
        inputs.append(ROOT / 'runs' / label / 'status.json')
        inputs.extend((ROOT / 'runs' / label).glob('*.npz'))
    inputs += [WAVES / 'coupled_system.py', WAVES / 'evolution_common.py', ROOT / 'compare_responses.py']
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, existing_parent_constraint_methods_called_read_only=True,
                        finite_thermal_energy_and_enthalpy_required_by_source_balance=True,
                        frozen_reference_photon_units=True, background_is_normalized_test_snapshot_not_refit=True,
                        scope='Linear fixed-metric collision tangent and integrated local exchange; density perturbation fixed to zero.',
                        full_streaming_expansion_and_metric_propagation=False), __file__, sorted(set(inputs)))
    print(json.dumps(dict(count=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
