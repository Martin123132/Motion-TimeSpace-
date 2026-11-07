from __future__ import annotations

import csv

import numpy as np
from scipy.integrate import solve_ivp, quad

from budget import ROOT, BRANCH, read_json, digest, save, modest_process, dependencies, RateCurve


COMPONENTS = ['frozen_polar', 'dynamic_polar', 'odd_response', 'horizon', 'wave_square']


def integrate(nodes, body, weak=False, stride=1):
    mass, radius, deformability = [body[key] for key in ['mass', 'radius', 'tidal_lambda']]
    positions = sorted({row['separation'] for row in nodes})[::stride]
    selected = [row for row in nodes if row['separation'] in positions]
    names = ['weak_tide'] if weak else COMPONENTS
    curves = {} if weak else {name:RateCurve(selected, name, mass, radius) for name in ['point_out']+names}
    initial, final = 10*radius/mass, 5*radius/mass
    norms = np.array([1., 5*(initial**4-final**4)/256, (initial**2.5-final**2.5)/32,
                     5*(initial**4-final**4)/256, (initial**2.5-final**2.5)/32])
    magnifications = np.array([1.]+[1e5]*len(names))

    def rates(separation):
        semilatus = separation*radius/mass
        if not weak:
            return {name:curve.rates(separation) for name, curve in curves.items()}
        normal = -64/(5*mass**2*semilatus**3)
        gamma = -608/(15*mass**2*semilatus**4)
        tide = deformability/(mass*semilatus)**5
        return dict(point_out=dict(P0=normal, X2=157/24*normal, G_action=gamma),
            weak_tide=dict(P0=6*tide*normal, X2=837/4*tide*normal, G_action=459/19*tide*gamma))

    def physical_derivative(separation, state):
        shaped = state.reshape(-1, 5)/magnifications[:, None]*norms[None, :]
        values = rates(separation)
        baseline = values['point_out']
        shrink, gamma, second = [baseline[key] for key in ['P0', 'G_action', 'X2']]
        semilatus = separation*radius/mass
        transport = np.exp(shaped[0, 0])
        time0 = 1/(mass**2*shrink)
        time2 = -transport*second/(mass**2*shrink**2)
        result = [[gamma/shrink, time0, time0*semilatus**-1.5, time2, time2*semilatus**-1.5]]
        for index, name in enumerate(names, start=1):
            correction = values[name]
            delta_shrink, delta_gamma, delta_second = [correction[key] for key in ['P0', 'G_action', 'X2']]
            log_prime = (delta_gamma*shrink-gamma*delta_shrink)/shrink**2
            time0 = -delta_shrink/(mass**2*shrink**2)
            time2 = -transport/(mass**2*shrink**2)*(delta_second+second*shaped[index, 0]-2*second*delta_shrink/shrink)
            result.append([log_prime, time0, time0*semilatus**-1.5, time2, time2*semilatus**-1.5])
        return np.array(result)*radius/mass

    def derivative(separation, state):
        return (physical_derivative(separation, state)/norms[None, :]*magnifications[:, None]).ravel()

    solution = solve_ivp(derivative, (10., 5.), np.zeros((len(names)+1)*5),
                         method='DOP853', rtol=2e-12, atol=2e-14, dense_output=True)
    assert solution.success
    endpoint = solution.y[:, -1].reshape(-1, 5)/magnifications[:, None]*norms[None, :]
    quadrature = np.zeros_like(endpoint)
    for index in range(len(names)+1):
        for column in range(5):
            quadrature[index, column] = quad(lambda separation:physical_derivative(separation, solution.sol(separation))[index, column],
                10., 5., epsabs=1e-12, epsrel=5e-11, limit=100)[0]
    quad_error = float(np.max(abs(quadrature-endpoint)/np.maximum(abs(endpoint), 1e-15)))
    output = {name:endpoint[index].tolist() for index, name in enumerate(['point_out']+names)}
    samples = []
    for separation in np.linspace(10., 5., 41):
        state = solution.sol(separation).reshape(-1, 5)/magnifications[:, None]*norms[None, :]
        for index, name in enumerate(['point_out']+names):
            samples.append(dict(separation=float(separation), component=name,
                log_transport=float(state[index, 0]), circular_time=float(state[index, 1]),
                circular_phase=float(state[index, 2]), eccentric_time_coefficient=float(state[index, 3]),
                eccentric_phase_coefficient=float(state[index, 4])))
    return dict(endpoint=output, quadrature_error=quad_error, evaluations=solution.nfev, nodes=len(positions)), samples


def main():
    modest_process()
    source = ROOT/'results/nodes/status.json'
    report = read_json(source)
    runs, samples = {}, []
    for settings in ['fine', 'coarse']:
        nodes = [row for row in report['nodes'] if row['settings'] == settings]
        body = next(row for row in report['static_boundaries'] if row['settings'] == settings)
        runs[settings], saved = integrate(nodes, body)
        samples.extend([dict(settings=settings, **row) for row in saved])
        if settings == 'fine':
            runs['weak'], _ = integrate(nodes, body, weak=True)
            for stride in [2, 4]:
                runs['nested'+str(16//stride+1)], _ = integrate(nodes, body, stride=stride)
    reference = runs['fine']['endpoint']
    errors = {}
    for label in ['coarse', 'nested9', 'nested5']:
        errors[label] = {name:(abs(np.array(runs[label]['endpoint'][name])/np.array(reference[name])-1)).tolist()
                         for name in reference}
    weak_reference = np.array(runs['weak']['endpoint']['point_out'])
    weak_tide = np.array(runs['weak']['endpoint']['weak_tide'])
    point = np.array(reference['point_out'])
    parts = {name:np.array(reference[name]) for name in COMPONENTS}
    full_outgoing = parts['frozen_polar']+parts['dynamic_polar']+parts['odd_response']
    budget = dict(weak_point=weak_reference.tolist(), curved_point_outgoing=point.tolist(),
        weak_tide=weak_tide.tolist(), full_outgoing=full_outgoing.tolist(),
        frozen_remainder=(parts['frozen_polar']-weak_tide).tolist(),
        dynamic_polar=parts['dynamic_polar'].tolist(), odd_response=parts['odd_response'].tolist(),
        negative_horizon=(-parts['horizon']).tolist(), outgoing_wave_square=parts['wave_square'].tolist(),
        full_outgoing_relative_to_weak=(full_outgoing/weak_tide-1).tolist(),
        point_relative_to_weak=(point/weak_reference-1).tolist())
    illustrations = []
    for initial_z in [0., .0001]:
        baseline_time, baseline_phase = point[1]+initial_z*point[3], point[2]+initial_z*point[4]
        delta_time = full_outgoing[1]+initial_z*full_outgoing[3]
        delta_phase = full_outgoing[2]+initial_z*full_outgoing[4]
        weak_time, weak_phase = weak_tide[1]+initial_z*weak_tide[3], weak_tide[2]+initial_z*weak_tide[4]
        illustrations.append(dict(initial_action_z=initial_z, outgoing_fraction_time=delta_time/baseline_time,
            outgoing_fraction_phase=delta_phase/baseline_phase,
            outgoing_time_difference=delta_time, outgoing_phase_difference=delta_phase,
            time_difference_relative_to_static_weak=delta_time/weak_time-1,
            phase_difference_relative_to_static_weak=delta_phase/weak_phase-1,
            dynamic_time_fraction_of_weak=(parts['dynamic_polar'][1]+initial_z*parts['dynamic_polar'][3])/weak_time,
            dynamic_phase_fraction_of_weak=(parts['dynamic_polar'][2]+initial_z*parts['dynamic_polar'][4])/weak_phase,
            horizon_time_fraction_of_weak=- (parts['horizon'][1]+initial_z*parts['horizon'][3])/weak_time,
            horizon_phase_fraction_of_weak=- (parts['horizon'][2]+initial_z*parts['horizon'][4])/weak_phase))
    result = save('integrals', __file__, dict(input_hashes={**dependencies(), str(source):digest(source)},
        runs=runs, comparisons=errors, budget=budget, illustrations=illustrations,
        array_order=['log action-z transport difference', 'circular T', 'circular Phi', 'T per initial action-z', 'Phi per initial action-z'],
        normalization='T=mu*t/M^2;Phi=(mu/M)*orbital_phase,leading test-mass limit.',
        approximation='Linear response insertion into the clock and initial action eccentricity; wave fluxes retain their archived squared-response term, separately tracked.',
        matching='Initial/final azimuthal frequencies D/R=10 and5,initial action zeta=2Jr/Jphi.' ))
    with (ROOT/'results/integrals/trajectory-budget.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(samples[0]))
        writer.writeheader()
        writer.writerows(samples)
    print(dict(state='complete', illustrations=illustrations,
        max_errors={label:max(value for values in group.values() for value in values) for label, group in errors.items()},
        max_quadrature_error=max(run['quadrature_error'] for run in runs.values())), flush=True)


if __name__ == '__main__':
    main()
