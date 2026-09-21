from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, MaterialState, LiveGeometry, DensityTable, material_weight
from annular_repaired_live_current_20260915 import LiveTangent
import numpy as np


class VariedGeometry:
    def __init__(self, geometry, amplitude, sector):
        self.geometry, self.amplitude, self.sector = geometry, amplitude, sector
        self.edges = geometry.edges

    def metric(self, radius):
        lapse, root = self.geometry.metric(radius)
        direction = .02*(1+.3*np.sin(np.asarray(radius)))
        if self.sector == 'lapse':
            lapse = lapse+self.amplitude*direction
        else:
            root = np.sqrt(root**2-2*self.amplitude*direction/np.asarray(radius))
        return lapse, root


def deformed_preparation(system):
    coordinates, unused, rates, unused2 = system.initial()
    coordinates[:, -1] += .003*system.labels**2
    coordinates[:, :-1] *= (1+.15*system.labels)[:, None]
    rates[:, -1] += .003*system.labels+.004*system.labels**2
    material = MaterialState(system, coordinates)
    geometry = LiveGeometry(system, material, rates)
    momenta = np.array([system.layer(offset, geometry).evaluate(0., position, velocity)['momenta']
                        for offset, position, velocity in zip(system.labels, coordinates, rates)])
    return coordinates, momenta, rates, geometry


def action_variation(system, coordinates, rates, geometry, sector):
    points, weights = np.polynomial.legendre.leggauss(48)
    labels, weights = points/2, weights/2*material_weight(points/2)
    material = MaterialState(system, coordinates)
    interpolation = material.interpolation(labels)
    amplitude = 1j*1e-24
    varied = VariedGeometry(geometry, amplitude, sector)
    value = 0.
    for offset, weight, position, velocity in zip(labels, weights, interpolation @ coordinates, interpolation @ rates):
        value += weight*system.layer(offset, varied).evaluate(0., position, velocity)['action'].imag/amplitude.imag
    radial_points, radial_weights = np.polynomial.legendre.leggauss(14)
    radius = (geometry.centers[:, None]+geometry.lengths[:, None]/2*radial_points).ravel()
    radial_weights = (geometry.lengths[:, None]/2*radial_weights).ravel()
    density = DensityTable(material, radius)
    density.update(rates)
    lapse, root = geometry.metric(radius)
    dual = -.5*(density.temporal_square/(lapse**2*root**2)+density.gradient_square)-density.gram
    clock = np.sqrt(lapse**2-density.velocity**2/root**2)
    if sector == 'lapse':
        covector = radius**2*root*dual-system.source_mass*lapse/clock*density.source_density
    else:
        covector = -radius*lapse/root*dual+system.source_mass*density.velocity**2/(radius*root**4*clock)*density.source_density
    expected = radial_weights @ (covector*.02*(1+.3*np.sin(radius)))
    normalization = radial_weights @ density.source_density
    return dict(action_derivative=float(value), averaged_density_derivative=float(expected),
                difference=float(abs(value-expected)), material_normalization_error=float(abs(normalization-1)))


def main():
    evidence = EvidenceRun('annular-repaired-live-controls-attempt01', __file__)
    try:
        for count in [17, 65]:
            for gram in [False, True]:
                system = RepairedLiveSystem(count, gram, 8, 10, action_order=10, label_order=12)
                coordinates, momenta, rates, geometry = deformed_preparation(system)
                row = dict(branch='MTS' if gram else 'reference', count=count, preparation='Nonaffine ordered moving layer map and label-dependent nonzero field.')
                for sector in ['lapse', 'mass']:
                    row[sector] = action_variation(system, coordinates, rates, geometry, sector)
                if count == 17:
                    tangent = LiveTangent(system, coordinates, momenta)
                    balances = [tangent.noether(offset) for offset in [-.4, -.25, .25, .4]]
                    row['noether_error'] = max(item['noether'] for item in balances)
                    row['omitted_interface_error'] = max(item['omitted_interface'] for item in balances)
                    targets = [5.993, 6.023, 6.03, 6.037, 6.105, 6.41]
                    comparison = tangent.compare(targets, label_order=12)
                    row['temporal_current_error'] = comparison['on_shell_error']
                    current_path = evidence.output/(row['branch']+'-deformed-current.npz')
                    np.savez_compressed(current_path, **comparison)
                    evidence.own(current_path, 'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                for sector in ['lapse', 'mass']:
                    evidence.check(row['branch']+str(count)+sector+'_independent_averaged_action_covector', row[sector]['difference'] < 2e-9, row)
                    evidence.check(row['branch']+str(count)+sector+'_source_measure_normalized', row[sector]['material_normalization_error'] < 2e-10, row)
                if count == 17:
                    evidence.check(row['branch']+'_deformed_moving_Noether_requires_jump', row['noether_error'] < 2e-9 and row['omitted_interface_error'] > 1e-7, row)
                    evidence.check(row['branch']+'_deformed_live_temporal_current', row['temporal_current_error'] < 2e-8, row)
        evidence.report.update(independent_average_before_metric_variation_checked=True,
                               nonaffine_source_and_overlapping_supports_tested=True,
                               moving_interface_omission_negative_control=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
