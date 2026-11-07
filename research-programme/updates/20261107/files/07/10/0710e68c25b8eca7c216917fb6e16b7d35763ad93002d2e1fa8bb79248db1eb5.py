from types import SimpleNamespace
from emission_angular_common import *
from increment_emitting_geometry import IncrementEmittingGeometry, ShiftedDense, state_at_scale


class ReactionGeometry(IncrementEmittingGeometry):
    def __init__(self, model, name):
        self.thermal = thermal_wave.thermal.ThermalBackground(model)
        self.parent = self.thermal.parent
        self.source = ROOT / 'backgrounds' / name / 'history.npz'
        packet = json.loads((self.source.parent / 'status.json').read_text())
        assert packet['all_checks_passed'] and packet['model'] == model
        self.basis = ConsistentBasis(**packet['basis_spec'])
        with np.load(self.source) as saved:
            self.expansion = saved['expansion'].copy()
            self.profiles = interpolate.CubicSpline(self.expansion, saved['profiles'])
            self.temperature = interpolate.CubicSpline(self.expansion, saved['temperature_scaled'])
            self.heat = float(saved['heat'])
            self.discrete_energy = saved['energy_scaled'].copy()
            self.number = interpolate.CubicSpline(self.expansion, saved['number_scaled'])
        self.work_integral = self.temperature.antiderivative()
        self.amplitude = self.heat
        self.initial = state_at_scale(self.thermal, self.thermal.start_scale)
        self.mass2 = self.parent.masses ** 2
        start = np.r_[np.zeros(2), self.initial['prime'], 0., 0.]
        self.increment_solution = integrate.solve_ivp(self.increment_rhs, (0., self.thermal.end), start, method='DOP853',
                                                      rtol=2e-12, atol=1e-28, max_step=.008, dense_output=True)
        assert self.increment_solution.success
        self.solution = SimpleNamespace(success=True, sol=ShiftedDense(self.increment_solution.sol, self.initial['fields']),
                                        nfev=self.increment_solution.nfev, t=self.increment_solution.t)
