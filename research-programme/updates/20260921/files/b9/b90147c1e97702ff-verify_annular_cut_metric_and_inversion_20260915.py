from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction, history_state
from scipy.optimize import brentq
import numpy as np


def inverse_momenta(system, time, coordinates, momenta, pulled=None):
    data = system.evaluate(time, coordinates, np.zeros_like(coordinates), pulled)
    lapse, root = system.metric(time, coordinates[-1]) if pulled is None else pulled[2:4]
    if pulled is not None and pulled[4] != 0:
        raise ValueError('This canonical inversion is derived only at P=0.')
    mass_matrix = data['inertia'][:-1, :-1]
    cross = data['inertia'][:-1, -1]
    free_velocity = np.linalg.solve(mass_matrix, momenta[:-1])
    cross_velocity = np.linalg.solve(mass_matrix, cross)
    field_inertia = data['inertia'][-1, -1]-system.source_mass/(root**2*lapse)
    remainder_inertia = field_inertia-cross @ cross_velocity
    if remainder_inertia < -2e-12:
        raise ValueError('Negative field Schur complement beyond rounding tolerance.')
    target = momenta[-1]-cross @ free_velocity
    def residual(velocity):
        clock = np.sqrt(lapse**2-velocity**2/root**2)
        return system.source_mass*velocity/(root**2*clock)+remainder_inertia*velocity-target
    limit = lapse*root*(1-1e-12)
    velocity = brentq(residual, -limit, limit, xtol=5e-15, rtol=2e-14)
    rates = np.append(free_velocity-cross_velocity*velocity, velocity)
    return rates, float(remainder_inertia)


def metric_pull(system, time, coordinates, amplitude, sector):
    radius, unused = system.mesh(coordinates[-1])
    targets = np.concatenate([radius, system.radii, [coordinates[-1]]])
    lapse, root = system.metric(time, targets)
    lapse_direction = .013*(1+.2*np.sin(targets)) if sector == 'lapse' else 0*targets
    mass_direction = .009*(1+.3*np.cos(targets)) if sector == 'mass' else 0*targets
    varied_lapse = lapse+amplitude*lapse_direction
    varied_root = np.sqrt(root**2-2*amplitude*mass_direction/targets)
    coefficient = targets**2*varied_lapse*varied_root
    coefficient_direction = targets**2*root*lapse_direction-targets*lapse*mass_direction/root
    count = len(radius)
    pulled = (coefficient[:count], coefficient[count:-1], varied_lapse[-1], varied_root[-1], 0.)
    return pulled, coefficient_direction, lapse_direction[-1], mass_direction[-1]


def main():
    evidence = EvidenceRun('annular-cut-metric-and-canonical-inversion-attempt01', __file__)
    try:
        for gram in [False, True]:
            system = CurvedCutAction(17, gram, order=10)
            branch = 'MTS' if gram else 'reference'
            for time in [-.15, 0., .15]:
                coordinates, rates, unused = history_state(system, time)
                data = system.evaluate(time, coordinates, rates)
                recovered, field_schur = inverse_momenta(system, time, coordinates, data['momenta'])
                roundtrip = float(np.max(abs(recovered-rates)))
                evidence.check(branch+str(time)+'_unique_canonical_roundtrip', roundtrip < 2e-11 and field_schur >= -2e-12)
                for sector in ['lapse', 'mass']:
                    unused, coefficient_direction, lapse_direction, mass_direction = metric_pull(system, time, coordinates, 0., sector)
                    lapse, root = system.metric(time, coordinates[-1])
                    source_covector = -system.source_mass*lapse/data['clock']*lapse_direction
                    source_covector += system.source_mass*rates[-1]**2/(coordinates[-1]*root**4*data['clock'])*mass_direction
                    count = len(data['radius'])
                    derivative = np.dot(data['weight']*data['density_dual'], coefficient_direction[:count])
                    derivative += data['nodal_dual'] @ coefficient_direction[count:-1]+source_covector
                    step = 2e-4
                    actions, hamiltonians = {}, {}
                    for amplitude in [-2*step, -step, step, 2*step]:
                        pulled = metric_pull(system, time, coordinates, amplitude, sector)[0]
                        actions[amplitude] = system.evaluate(time, coordinates, rates, pulled)['action']
                        changed_rates, unused = inverse_momenta(system, time, coordinates, data['momenta'], pulled)
                        hamiltonians[amplitude] = data['momenta'] @ changed_rates-system.evaluate(time, coordinates, changed_rates, pulled)['action']
                    action_difference = (-actions[2*step]+8*actions[step]-8*actions[-step]+actions[-2*step])/(12*step)
                    hamiltonian_difference = (-hamiltonians[2*step]+8*hamiltonians[step]-8*hamiltonians[-step]+hamiltonians[-2*step])/(12*step)
                    error = float(abs(action_difference-derivative))
                    canonical_error = float(abs(hamiltonian_difference+derivative))
                    evidence.check(branch+str(time)+sector+'_independent_metric_and_fixed_momentum_variations',
                                   max(error, canonical_error) < 2e-9)
                    evidence.report['cases'].append(dict(branch=branch, time=time, sector=sector,
                                                         action_metric_error=error, fixed_momentum_metric_error=canonical_error,
                                                         velocity_roundtrip_error=roundtrip, field_schur_complement=field_schur))
        evidence.report.update(scope='P=0 lapse/mass covectors and invertible coupled field/source Legendre map at fixed regular metric.',
                               inverse_equation='P_b-d^T M^-1 pi = S V/(U_b^2 sqrt(N_b^2-V^2/U_b^2)) + (I-d^T M^-1 d)V',
                               canonical_inversion_derived=True,
                               field_Schur_nonnegative_by_Gram_integral=True,
                               fixed_momentum_metric_variation_checks_pass=True,
                               coupled_radial_metric_solution_completed=False,
                               unique_parent_boundary_selection_proven=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
