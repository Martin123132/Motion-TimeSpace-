from emission_common import *
sys.path.insert(0, str(THERMAL_STAGE))
from background_geometry import ConservedThermalBackground, state_at_scale


class EmittingGeometry(ConservedThermalBackground):
    def __init__(self, model, name, amplitude=None):
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
        self.amplitude = self.heat if amplitude is None else amplitude
        self.initial = state_at_scale(self.thermal, self.thermal.start_scale)
        self.mass2 = self.parent.masses ** 2
        start = np.r_[self.initial['fields'], self.initial['prime'], 0., 0.]
        self.solution = integrate.solve_ivp(self.rhs, (0., self.thermal.end), start, method='DOP853',
                                            rtol=2e-12, atol=1e-28, max_step=.008, dense_output=True)
        assert self.solution.success
