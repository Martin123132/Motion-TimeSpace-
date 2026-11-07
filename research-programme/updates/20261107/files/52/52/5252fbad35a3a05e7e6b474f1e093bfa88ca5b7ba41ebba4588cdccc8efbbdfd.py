from __future__ import annotations

from datetime import datetime, timezone
import csv
import sys

import numpy as np
import sympy as sp
from numpy.polynomial import Chebyshev
from scipy.integrate import quad, solve_ivp

from carrier import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process, orbit_series, imported_hashes

sys.path.insert(0,str(PARENT))
from analyze_inspiral import Curve


class ClockCurve:
    def __init__(self, source, base_curve):
        self.base = base_curve
        self.mass, self.radius = base_curve.mass, base_curve.radius
        self.nodes = sorted(source, key=lambda row:row['separation'])
        coordinates = [row['separation'] for row in self.nodes]
        self.polynomials = {}
        for channel in ['BH','difference']:
            selected = [row for row in self.nodes if row['channel'] == channel]
            coordinate = [row['separation'] for row in selected]
            normalization = []
            for row in selected:
                semilatus = row['semilatus']
                value = -64/(5*self.mass**2*semilatus**3)
                if channel == 'difference':
                    value *= base_curve.tidal_lambda/(self.mass*semilatus)**5
                normalization.append(value)
            self.polynomials[channel] = Chebyshev.fit(coordinate, [row['P2']/normal for row,normal in zip(selected,normalization)],
                                                      len(selected)-1, domain=[5.,10.])
        def log_rhs(separation, state):
            values = base_curve.integrand(separation)
            return [values[2],values[5]*1e4]
        self.log_solution = solve_ivp(log_rhs,(10.,5.),[0.,0.],method='DOP853',rtol=2e-12,atol=2e-13,dense_output=True)
        assert self.log_solution.success

    def second(self, separation):
        semilatus = separation*self.radius/self.mass
        normal = -64/(5*self.mass**2*semilatus**3)
        return (float(self.polynomials['BH'](separation))*normal,
                float(self.polynomials['difference'](separation))*normal*self.base.tidal_lambda/(self.mass*semilatus)**5)

    def integrand(self, separation):
        semilatus = separation*self.radius/self.mass
        values = self.base.rates(separation)
        shrink, difference = values['P_BH'],values['P_out']-values['P_H']
        body_shrink = shrink+difference
        second, second_difference = self.second(separation)
        reference_ratio = second/shrink
        ratio_difference = (second_difference*shrink-second*difference)/(shrink*body_shrink)
        body_ratio = reference_ratio+ratio_difference
        alpha = orbit_series(semilatus)['angular_frequency_fraction']
        logs = self.log_solution.sol(separation)
        reference_z = np.exp(logs[0])
        relative_z_change = np.expm1(logs[1]/1e4)
        inverse_reference = 1/(self.mass**2*shrink)
        inverse_body = 1/(self.mass**2*body_shrink)
        inverse_difference = -difference/(self.mass**2*shrink*body_shrink)
        omega_scaled = semilatus**-1.5
        reference_clock = -inverse_reference*reference_z*reference_ratio
        clock_difference = -reference_z*(inverse_difference*body_ratio+inverse_reference*ratio_difference+
                                         inverse_body*body_ratio*relative_z_change)
        reference_phase = omega_scaled*inverse_reference*reference_z*(alpha-reference_ratio)
        phase_difference = omega_scaled*reference_z*(inverse_difference*(alpha-body_ratio)-inverse_reference*ratio_difference+
                                                      inverse_body*(alpha-body_ratio)*relative_z_change)
        return np.array([reference_clock,reference_phase,clock_difference,phase_difference])*self.radius/self.mass

    def integral(self, separation=5.):
        if separation == 10.:
            return np.zeros(4)
        return np.array([quad(lambda distance:self.integrand(distance)[index],10.,separation,
                              epsrel=2e-11,epsabs=1e-10,limit=150)[0] for index in range(4)])


def main():
    modest_process()
    inputs = {}
    def load(path):
        value = read_json(path)
        assert value['state'] == 'complete'
        inputs[str(path)] = digest(path)
        return value
    parent = load(PARENT/'results/analysis/status.json')
    full = {label:load(ROOT/'results'/('analysis-full-'+label)/'status.json') for label in ['fine','coarse']}
    weak = load(ROOT/'results/weak-field/status.json')
    exact = load(ROOT/'results/derivation/status.json')
    summary = parent['summary']
    mass,radius,tidal_lambda = summary['central_mass'],summary['central_radius'],summary['tidal_lambda']
    base = {label:Curve(parent['raw_nodes']['nodes-'+label],mass,radius,tidal_lambda) for label in ['fine','coarse']}
    curves = {}
    for label in ['fine','coarse']:
        selected = [row for row in full[label]['shrinkage_laws'] if row['component']=='combined_ell2' and row['channel'] in ['BH','difference']]
        curves[label] = ClockCurve(selected,base[label])
        if label=='fine':
            ordered = sorted({row['separation'] for row in selected})
            for stride in [2,4]:
                positions = ordered[::stride]
                curves['nested'+str(len(positions))] = ClockCurve([row for row in selected if row['separation'] in positions],base[label])
    endpoints = {label:curve.integral().tolist() for label,curve in curves.items()}
    reference = np.array(endpoints['fine'])
    comparisons = {label:(abs((np.array(value)-reference)/reference)).tolist() for label,value in endpoints.items()}
    ode = solve_ivp(lambda separation,state:curves['fine'].integrand(separation)/abs(reference),(10.,5.),np.zeros(4),
                    method='DOP853',rtol=2e-12,atol=2e-13)
    assert ode.success
    ode_error = abs((ode.y[:,-1]*abs(reference)-reference)/reference).tolist()
    pi,pf=10*radius/mass,5*radius/mass
    p_symbol, initial_symbol, tidal_symbol = sp.symbols('p pi Lambda',positive=True)
    local = {'p':p_symbol,'pi':initial_symbol,'Lambda':tidal_symbol}
    weak_values = []
    for report,keys in [(exact,['newtonian_clock_coefficient','newtonian_phase_coefficient']),
                         (weak,['differential_clock_primitive','differential_phase_primitive'])]:
        for key in keys:
            expression = sp.sympify(report[key],locals=local)
            function = sp.lambdify((p_symbol,initial_symbol,tidal_symbol),expression,'numpy')
            value = function(pf,pi,tidal_lambda/mass**5)
            if report is weak:
                value -= function(pi,pi,tidal_lambda/mass**5)
            weak_values.append(float(value))
    leading = np.array(parent['endpoint_integrals']['nodes-fine'])
    initial_e = .01
    squared = initial_e**2
    endpoint = dict(
        initial_eccentricity=initial_e, initial_separation=10.,final_separation=5.,
        clock_correction_per_initial_e_squared_BH=reference[0],
        orbital_phase_correction_per_initial_e_squared_BH=reference[1],
        clock_correction_per_initial_e_squared_difference=reference[2],
        orbital_phase_correction_per_initial_e_squared_difference=reference[3],
        corrected_scaled_time_BH=leading[0]+squared*reference[0],
        corrected_scaled_phase_BH=leading[1]+squared*reference[1],
        corrected_scaled_time_difference=leading[3]+squared*reference[2],
        corrected_scaled_phase_difference=leading[4]+squared*reference[3],
        eccentricity_clock_fraction_BH=squared*reference[0]/leading[0],
        eccentricity_phase_fraction_BH=squared*reference[1]/leading[1],
        corrected_candidate_time_fraction=(leading[3]+squared*reference[2])/(leading[0]+squared*reference[0]),
        corrected_candidate_phase_fraction=(leading[4]+squared*reference[3])/(leading[1]+squared*reference[1]))
    order_controls = []
    for channel in ['BH','body']:
        endpoint0 = leading[:2] if channel=='BH' else leading[:2]+leading[3:5]
        correction = reference[:2] if channel=='BH' else reference[:2]+reference[2:]
        for initial_squared in [.001,.002]:
            def rhs(separation,state):
                semilatus=separation*radius/mass
                values=base['fine'].rates(separation)
                second,second_difference=curves['fine'].second(separation)
                shrink,gamma=values['P_BH'],values['G_BH']
                if channel=='body':
                    shrink+=values['P_out']-values['P_H']
                    gamma+=values['G_out']-values['G_H']
                    second+=second_difference
                squared_eccentricity=initial_squared*state[2]
                total=shrink+second*squared_eccentricity
                scale=radius/mass
                return [scale/(mass**2*total*endpoint0[0]),
                        scale*semilatus**-1.5*(1+orbit_series(semilatus)['angular_frequency_fraction']*squared_eccentricity)/(mass**2*total*endpoint0[1]),
                        scale*gamma/total*state[2]]
            nonlinear=solve_ivp(rhs,(10.,5.),[0.,0.,1.],method='DOP853',rtol=2e-12,atol=2e-13)
            assert nonlinear.success
            value=nonlinear.y[:2,-1]*endpoint0
            remainder=value-endpoint0-initial_squared*correction
            order_controls.append(dict(channel=channel,initial_squared=initial_squared,
                 resummed_endpoint=value.tolist(),remainder=remainder.tolist(),remainder_over_z_initial_squared=(remainder/initial_squared**2).tolist()))
    trajectory=[]
    for separation in np.linspace(10.,5.,41):
        correction=curves['fine'].integral(float(separation))
        trajectory.append(dict(separation=float(separation),clock_BH_per_initial_z=float(correction[0]),
             phase_BH_per_initial_z=float(correction[1]),clock_difference_per_initial_z=float(correction[2]),
             phase_difference_per_initial_z=float(correction[3])))
    directory=ROOT/'results/clock'
    directory.mkdir(parents=True,exist_ok=False)
    result=dict(state='complete',script_sha256=digest(__file__),time_utc=datetime.now(timezone.utc).isoformat(),
         input_hashes={**inputs,**imported_hashes()},endpoint=endpoint,endpoints=endpoints,comparisons=comparisons,
         ode_relative_errors=ode_error,weak_field_predictions=weak_values,
         finite_radius_corrections_to_weak=(reference/np.array(weak_values)-1).tolist(),trajectory=trajectory,
         order_controls=order_controls,normalization='T=eta*t/M;Phi=eta*orbital_phase;correction coefficients per initial e^2.',
         approximation='Strict first order in initial z=e^2 for clocks/phase; resummed equations are order controls, not higher-order solutions.')
    write_json(directory/'status.json',result,exclusive=True)
    with (directory/'trajectory-coefficients.csv').open('x',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(trajectory[0]))
        writer.writeheader()
        writer.writerows(trajectory)
    print(dict(endpoint=endpoint,comparisons=comparisons,ode=ode_error,
               finite_radius_corrections=result['finite_radius_corrections_to_weak'],order_controls=order_controls),flush=True)


if __name__=='__main__':
    main()

