from mixed_common import *
from background_geometry import ConservedThermalBackground


class MixedBank:
    def __init__(self, name, model, count, stride=1):
        folder = ROOT / 'banks' / name
        packet = json.loads((folder / 'status.json').read_text())
        assert packet['all_checks_passed']
        self.inputs = [folder / 'status.json']
        knots = np.asarray(packet['knots'])
        uniform = np.linspace(0., knots[-1], (len(knots) - 5) // stride + 1)
        indices = [index for index, point in enumerate(knots)
                   if index < 5 or min(abs(uniform - point)) < 1e-12]
        self.knots = knots[indices]
        values = [[] for degree in range(9)]
        thermal, residual = [], []
        selected = 0 if model == 'heavy' else 1
        for index in indices:
            path = folder / ('knot-' + str(index) + '.npz')
            self.inputs.append(path)
            with np.load(path) as saved:
                for degree in range(9):
                    modes = 2 if degree < 2 else 4
                    retained = np.concatenate([np.arange(mode * 24, mode * 24 + count) for mode in range(modes)])
                    values[degree].append(saved['block_' + str(degree)][selected][np.ix_(retained, retained)])
                thermal.append(saved['temperature'][selected, :count])
                residual.append(saved['residual'][selected, :count])
        self.blocks = [interpolate.CubicSpline(self.knots, value) for value in values]
        self.temperature = interpolate.CubicSpline(self.knots, thermal)
        self.residual = interpolate.CubicSpline(self.knots, residual)


class MixedSystem(RefinedSystem):
    def __init__(self, model, count=24, maximum=8, bank='fine16', stride=1):
        super().__init__(model, count, maximum)
        if count != 24:
            self.geometry = ConservedThermalBackground(model, model + '24-3200')
        self.bank = MixedBank(bank, model, count, stride)
        self.geometry_basis = self.geometry.basis
        vectors = np.column_stack([self.geometry_basis.chemical, self.geometry_basis.temperature])
        moments = np.vstack([self.geometry_basis.number, self.geometry_basis.energy])
        self.moment_lift = vectors @ linalg.inv(moments @ vectors)

    def spectral_background(self, expansion, local):
        coefficients = self.geometry.profiles(expansion).copy()
        derivative = self.geometry.profiles(expansion, 1).copy()
        coefficients += self.moment_lift @ np.array([-self.geometry_basis.number @ coefficients,
                                                    local['photon_energy_scaled'] - self.geometry_basis.energy @ coefficients])
        derivative += self.moment_lift @ np.array([-self.geometry_basis.number @ derivative,
                                                  local['photon_energy_prime'] - self.geometry_basis.energy @ derivative])
        coefficients, derivative = coefficients[:self.count], derivative[:self.count]
        redshift = self.basis.temperature + local['heat'] * self.mass_inverse @ self.redshift_weak @ coefficients
        collision = local['heat'] * local['hubble'] * derivative
        boost = self.mass_inverse @ self.boost_weak @ collision
        return redshift, collision, boost

    def correction(self, expansion, include_residual=False):
        local = self.background(expansion)
        redshift, _, _ = self.spectral_background(expansion, local)
        weak = np.zeros((self.size, self.size), complex)
        for degree, section in enumerate(self.slices):
            block = self.bank.blocks[degree](expansion)
            weak[section, section] = block
            if degree == 0:
                weak[self.mode_slice(0), 10] += self.bank.temperature(expansion)
            if degree == 1:
                equilibrium = np.r_[redshift, np.zeros((len(self.names[degree]) - 1) * self.count)]
                weak[section, 9] -= block @ equilibrium
        if include_residual:
            source = local['heat'] * self.bank.residual(expansion)
            weak[self.mode_slice(0)] += np.outer(source, self.density_row)
            boost = self.boost_weak @ (self.mass_inverse @ source)
            weak[self.mode_slice(1), 9] += boost / 3
        photon_heat = self.basis.energy @ self.mass_inverse @ weak[self.mode_slice(0)]
        photon_momentum = self.basis.energy @ self.mass_inverse @ weak[self.mode_slice(1)]
        weak[10] = -photon_heat
        weak[9] = -photon_momentum
        if include_residual:
            weak[10] += (self.basis.energy @ self.mass_inverse @ source) * self.density_row
        return sparse.csc_matrix(local['opacity'] / local['hubble'] * weak)

    def background_correction_operator(self, expansion):
        local = self.background(expansion)
        count, heat = self.count, local['heat']
        stiffness = self.ladder.at(local['theta'], 0)[:count, :count]
        stiffness = stiffness + heat * self.bank.blocks[0](expansion)[:count, :count]
        thermal = -self.ladder.at(local['theta'], 0)[:count, :count] @ self.basis.temperature
        thermal += heat * self.bank.temperature(expansion)
        weak = np.zeros((count + 1, count + 1))
        weak[:count, :count] = stiffness
        weak[:count, count] = thermal
        weak[count] = -self.basis.energy @ self.mass_inverse @ weak[:count]
        weak *= local['opacity'] / local['hubble']
        weak[count, count] -= heat
        source = self.bank.residual(expansion) * local['opacity'] / local['hubble']
        forcing = np.r_[source, -self.basis.energy @ self.mass_inverse @ source]
        mass = linalg.block_diag(self.basis.mass, np.array([[heat]]))
        return mass, weak, forcing
