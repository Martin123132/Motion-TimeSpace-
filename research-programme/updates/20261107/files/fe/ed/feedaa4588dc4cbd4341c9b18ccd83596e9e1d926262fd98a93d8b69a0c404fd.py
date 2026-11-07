from common236 import *
import itertools


class Direction:
    def __init__(self, parameters, direction):
        self.parameters = parameters
        self.spin = angular.inherited.source.exact
        self.energy = scalar(parameters['energy'])
        self.cosine = scalar(parameters['cosine'])
        self.temperature = scalar(parameters['temperature'])
        self.hard_direction = mp.matrix([mp.sqrt(1 - self.cosine**2), 0, self.cosine])
        self.direction = self.spin.unit(direction)
        self.directions = [mp.matrix([0, 0, 1]), self.hard_direction, self.direction]
        self.frames = [self.spin.frame(value) for value in self.directions]
        self.vertices = [[self.spin.slash(value) for value in frame] for frame in self.frames]
        self.rays = [self.spin.photon(mp.mpf(1), value) for value in self.directions]
        self.initial = mp.matrix([1, 0, 0, 0])
        self.initial_states = self.spin.spinors(self.initial)
        self.left_initial = self.initial_states.transpose_conj() * self.spin.gamma_matrices()[0]
        right = [[self.spin.slash(self.rays[leg]) * self.vertices[leg][polarization] * self.initial_states / 2 for polarization in range(2)] for leg in range(3)]
        self.blocks = []
        self.leading_coefficients = []
        constant_recoil = self.directions[0] - self.directions[1]
        linear_recoil = self.directions[1] - self.directions[2]
        for polarization in itertools.product(range(2), repeat=3):
            blocks = []
            leading = [mp.zeros(4, 2) for unused in range(4)]
            for last in range(3):
                other = [leg for leg in range(3) if leg != last]
                reduced = sum((self.vertices[middle][polarization[middle]] * right[first][polarization[first]] for first, middle in (other, other[::-1])), mp.zeros(4, 2))
                matrix = self.vertices[last][polarization[last]] * self.spin.slash(self.rays[last]) * reduced
                blocks.append((matrix, reduced))
                leading[0] += matrix / 2
                constant = mp.fsum(constant_recoil[axis] * self.frames[last][polarization[last]][axis + 1] for axis in range(3))
                linear = mp.fsum(linear_recoil[axis] * self.frames[last][polarization[last]][axis + 1] for axis in range(3))
                if last == 0:
                    leading[0] += constant * reduced
                    leading[1] += linear * reduced
                elif last == 1:
                    leading[0] += linear * reduced
                    leading[3] -= (constant + linear) * reduced
                else:
                    leading[0] -= linear * reduced
                    leading[2] -= constant * reduced
            self.blocks.append((polarization, blocks))
            self.leading_coefficients.append([self.left_initial * coefficient for coefficient in leading])
        self.gram = mp.matrix(4)
        for first in range(4):
            for second in range(4):
                self.gram[first, second] = mp.re(mp.fsum(mp.conj(coefficient[first][row, column]) * coefficient[second][row, column]
                    for coefficient in self.leading_coefficients for row in range(2) for column in range(2))) / 4
        self.hard0 = self.energy / (1 + self.energy * (1 - self.cosine))
        self.recoil0 = mp.matrix([0, 0, self.energy]) - self.hard0 * self.hard_direction
        self.final0 = mp.sqrt(1 + mp.fsum(value**2 for value in self.recoil0))
        self.transform = mp.matrix(parameters['transform'].tolist())
        self.bath = mp.matrix(parameters['bath'].tolist())
        self.doppler = self.spin.dot(self.bath, self.rays[2])
        self.hard_doppler = self.spin.dot(self.bath, self.rays[1])
        self.alpha_factor = mp.mpf(str(angular.inherited.source.ALPHA)) / (4 * mp.pi**2)
        self.tree = 2 * (1 + self.cosine**2 + self.energy**2 * (1 - self.cosine)**2 / (1 + self.energy * (1 - self.cosine)))
        self.pole = {}
        self.pole['full'] = self.alpha_factor * mp.fsum(value**2 for value in self.spin.cross(self.recoil0, self.direction)) / (self.final0 - mp.fsum(self.recoil0[axis] * self.direction[axis] for axis in range(3)))**2
        self.pole['control'] = self.alpha_factor * self.energy**2 * 2 * (1 + self.cosine**2) / self.tree * mp.fsum(value**2 for value in self.spin.cross(constant_recoil, self.direction))
        self.pole['difference'] = self.pole['full'] - self.pole['control']

    def event(self, signed_soft):
        signed_soft = scalar(signed_soft)
        denominator0 = 1 + self.energy * (1 - self.cosine)
        mixed_angle = 1 - mp.fsum(self.hard_direction[axis] * self.direction[axis] for axis in range(3))
        incident_angle = 1 - self.direction[2]
        denominator = denominator0 - signed_soft * mixed_angle
        hard_shift = -signed_soft * ((1 + self.energy * incident_angle) * denominator0 - self.energy * mixed_angle) / (denominator0 * denominator)
        hard = self.hard0 + hard_shift
        assert hard > 0 and denominator > 0
        recoil_shift = -hard_shift * self.hard_direction - signed_soft * self.direction
        recoil = self.recoil0 + recoil_shift
        final_energy = mp.sqrt(1 + mp.fsum(value**2 for value in recoil))
        kinetic = mp.fsum(value**2 for value in recoil) / (final_energy + 1)
        kinetic_shift = (2 * mp.fsum(before * change for before, change in zip(self.recoil0, recoil_shift)) + mp.fsum(value**2 for value in recoil_shift)) / (final_energy + self.final0)
        final = mp.matrix([final_energy, *recoil])
        return dict(soft=signed_soft, hard=hard, hard_shift=hard_shift, denominator=denominator,
            recoil=recoil, recoil_shift=recoil_shift, final=final, kinetic=kinetic, kinetic_shift=kinetic_shift)

    def amplitude(self, event):
        final = event['final']
        left = self.spin.spinors(final).transpose_conj() * self.spin.gamma_matrices()[0]
        energies = [self.energy, -event['hard'], -event['soft']]
        projections = [self.spin.dot(final, ray) for ray in self.rays]
        values = []
        for polarization, blocks in self.blocks:
            combined = mp.zeros(4, 2)
            for last, (matrix, reduced) in enumerate(blocks):
                combined += matrix / (2 * projections[last]) - self.spin.dot(final, self.frames[last][polarization[last]]) * reduced / (energies[last] * projections[last])
            values.append(left * combined)
        return values

    def densities(self, signed_soft):
        event = self.event(signed_soft)
        tensors = self.amplitude(event)
        intensity = mp.fsum(abs(value)**2 for matrix in tensors for value in matrix) / 4
        fraction = event['soft'] / self.energy
        rational = mp.matrix([1, fraction, 1 / fraction, 1 / (1 - fraction)])
        leading = (rational.transpose() * self.gram * rational)[0]
        outgoing_x = event['hard'] * self.hard_doppler / self.temperature
        original_x = self.hard0 * self.hard_doppler / self.temperature
        stimulation = (1 + 1 / mp.expm1(outgoing_x)) / (1 + 1 / mp.expm1(original_x))
        prefactor = self.alpha_factor * event['hard'] * abs(event['soft']) * stimulation / (self.energy * event['denominator'] * (self.hard0 / self.energy)**2 * self.tree)
        full, control = prefactor * intensity, prefactor * leading
        return dict(full=full, control=control, difference=full-control), event


def pilot():
    modest()
    config = protocol()
    target = ROOT / 'results/density-pilot.json'
    assert not target.exists()
    write(ROOT / 'density-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        ray_indices=[0, 11, 23], soft_frequencies=[1.2e-6, 1e-4, .01, 1., 3.], digits=[60, 80],
        tolerance=1e-10, direct_dirac_cases='warm ray0 x1 emission and absorption', comparison='full, leading and subtracted densities'))
    checks, records = [], []
    started = time.monotonic()
    nodes = list(angular.inherited.source.angular_nodes(4))
    for row in config['events']:
        parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
        for ray_index in (0, 11, 23):
            direction = nodes[ray_index][0]
            results = {}
            for digits in (60, 80):
                with mp.workdps(digits):
                    owner = Direction(parameters, direction)
                    for frequency in (1.2e-6, 1e-4, .01, 1., 3.):
                        for sign in (1, -1):
                            signed = sign * scalar(frequency) * owner.temperature / owner.doppler
                            began = time.monotonic()
                            density, event = owner.densities(signed)
                            elapsed = time.monotonic() - began
                            values = {**density, **{name + '_minus_pole': value - owner.pole[name] / abs(signed) for name, value in density.items()}}
                            if digits == 60:
                                results[frequency, sign] = values
                            else:
                                for name, value in values.items():
                                    error = abs(results[frequency, sign][name] - value) / max(abs(value), mp.mpf('1e-300'))
                                    check(checks, f'{row["label"]}:ray{ray_index}:x{frequency}:sign{sign}:{name}:60to80', error)
                                if row['label'] == 'warm' and ray_index == 0 and frequency == 1.:
                                    photons = [owner.spin.photon(owner.energy, owner.directions[0]), owner.spin.photon(event['hard'], owner.directions[1]), owner.spin.photon(signed, owner.direction)]
                                    reference = []
                                    for polarization in itertools.product(range(2), repeat=3):
                                        reference.append(owner.spin.electron_amplitude(owner.initial, [photons[0], -photons[1], -photons[2]],
                                            [owner.frames[index][state] for index, state in enumerate(polarization)]))
                                    reconstructed = owner.amplitude(event)
                                    error = mp.sqrt(mp.fsum(mp.norm(value - before)**2 for value, before in zip(reconstructed, reference)) / mp.fsum(mp.norm(value)**2 for value in reference))
                                    check(checks, f'original six-propagator Dirac replay sign{sign}', error)
                                records.append(dict(anchor=row['label'], ray=ray_index, frequency=frequency, sign=sign, seconds=elapsed,
                                    full=float(density['full']), control=float(density['control']), difference=float(density['difference']),
                                    difference_minus_pole=float(values['difference_minus_pole'])))
        print(json.dumps(dict(anchor=row['label'], checks=len(checks), failed=sum(not entry['passed'] for entry in checks))), flush=True)
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        elapsed_seconds=time.monotonic()-started, finished_at=now()))
    print(json.dumps(dict(checks=len(checks), failed=failed, seconds=time.monotonic()-started, mean_event_seconds=np.mean([row['seconds'] for row in records]))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    pilot()
