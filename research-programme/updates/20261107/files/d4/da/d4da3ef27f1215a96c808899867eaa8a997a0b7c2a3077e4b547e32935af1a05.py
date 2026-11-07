from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp

from pn_algebra import Jet, gr_matching, derive_circular_model


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/pn-derivation'
    output.mkdir(parents=True, exist_ok=False)
    central_fraction = sp.symbols('chi', positive=True)
    companion_fraction = 1-central_fraction
    eta = central_fraction*companion_fraction
    model = derive_circular_model(central_fraction)
    checks = []

    def exact(name, expression):
        reduced = sp.factor(expression)
        assert reduced == 0, (name, reduced)
        checks.append({'name': name, 'passed': True})

    for index, value in enumerate(model['radial_residual'].values):
        exact('stationary_circular_action_'+str(index), value)
    exact('circular_radius_point_PN', model['radius'].values[1]-(eta-3)/3)
    exact('circular_radius_tide', model['radius'].values[2]-3*companion_fraction/central_fraction)
    exact('circular_radius_mixed', model['radius'].values[3]-companion_fraction*(-6+26*central_fraction-central_fraction**2)/(2*central_fraction))
    energy = model['energy'].values
    exact('point_Newton_energy', energy[0]+sp.Rational(1, 2))
    exact('same_source_energy_point_PN', energy[1]-(9+eta)/24)
    exact('previous_leading_tidal_energy', energy[2]-9*companion_fraction/(2*central_fraction))
    exact('same_source_energy_mixed', energy[3]-11*companion_fraction*(3+2*central_fraction+3*central_fraction**2)/(4*central_fraction))
    exact('independent_parent_energy_44_over_9', sp.limit(energy[3]/energy[2], central_fraction, 1)-sp.Rational(44, 9))
    normal, tangent = model['normal_moment'].values, model['tangent_moment'].values
    exact('circular_quadrupole_normal_PN', normal[1]+(85+11*eta)/42)
    exact('circular_quadrupole_tide', normal[2]-3*(3-2*central_fraction)/central_fraction)
    exact('circular_quadrupole_normal_mixed', normal[3]-(4+56*central_fraction+264*central_fraction**2-219*central_fraction**3)/(14*central_fraction))
    exact('circular_quadrupole_tangent_PN', tangent[1]-sp.Rational(11, 21)*(1-3*eta))
    exact('circular_quadrupole_tangent_mixed', tangent[3]-(103-252*central_fraction+302*central_fraction**2-132*central_fraction**3)/(7*central_fraction))
    flux = model['flux'].values
    exact('point_Newton_flux', flux[0]-1)
    exact('point_PN_flux', flux[1]+sp.Rational(1247, 336)+35*eta/12)
    exact('previous_leading_tidal_flux', flux[2]-6*(3-2*central_fraction)/central_fraction)
    expected_flux_mixed = (-704-1803*central_fraction+4501*central_fraction**2-2170*central_fraction**3)/(28*central_fraction)
    exact('same_source_mixed_flux', flux[3]-expected_flux_mixed)
    exact('source_owned_quadrupole_wave_bridge', (flux[3]/flux[2]-model['electric_flux'].values[1]).subs(central_fraction, 1)-sp.Rational(85, 21))
    exact('test_companion_point_quadrupole_PN', model['electric_flux'].values[1].subs(central_fraction, 1)+sp.Rational(107, 21))
    for key in ['octupole_flux', 'current_flux']:
        exact('no_leading_test_mass_transported_tide_'+key, model[key].values[3].subs(central_fraction, 1))
    chirp = model['chirp'].values
    exact('point_PN_chirp', chirp[1]+sp.Rational(743, 336)+11*eta/4)
    exact('previous_leading_chirp', chirp[2]-6*(12-11*central_fraction)/central_fraction)
    expected_chirp_mixed = (4421-12263*central_fraction+26502*central_fraction**2-18508*central_fraction**3)/(56*central_fraction)
    exact('same_source_PN_chirp', chirp[3]-expected_chirp_mixed)
    exact('test_mass_mixed_chirp', chirp[3].subs(central_fraction, 1)-sp.Rational(19, 7))
    exact('same_source_Fourier_phase_leading', model['fourier_phase_tide']+24*(1+11*companion_fraction)/central_fraction)
    exact('same_source_Fourier_phase_mixed', model['fourier_phase_mixed']+5*(3179-919*central_fraction-2286*central_fraction**2+260*central_fraction**3)/(28*central_fraction))
    inverse = model['inverse_chirp'].values
    exact('mixed_cross_term_preserved', inverse[3]-(2*chirp[1]*chirp[2]-chirp[3]))
    pn = sp.symbols('x', positive=True)
    tidal_scale = sp.symbols('lambda_over_Mtotal_fifth', positive=True)
    frequency_phase = sp.Rational(3, 128)/eta*tidal_scale*(model['fourier_phase_tide']*pn**sp.Rational(5, 2)+model['fourier_phase_mixed']*pn**sp.Rational(7, 2))
    second_frequency_derivative = 4/(9*pn)*(sp.diff(frequency_phase, pn, 2)-sp.diff(frequency_phase, pn)/(2*pn))
    inverse_tidal = tidal_scale*(inverse[2]*pn**5+inverse[3]*pn**6)
    exact('SPA_second_frequency_derivative', second_frequency_derivative-sp.Rational(5, 48)/eta*pn**sp.Rational(-11, 2)*inverse_tidal)
    time_phase = tidal_scale/(16*eta)*(-chirp[2]*pn**sp.Rational(5, 2)+sp.Rational(5, 7)*inverse[3]*pn**sp.Rational(7, 2))
    exact('time_domain_phase_derivative', sp.diff(time_phase, pn)-sp.Rational(5, 32)/eta*pn**sp.Rational(-7, 2)*inverse_tidal)
    electric_only_point = model['electric_flux'].values[1]
    exact('omitted_multipoles_leave_point_baseline_defect', flux[1]-electric_only_point-sp.Rational(155, 112)*(1-2*central_fraction)**2)
    tide_symbol = sp.symbols('tide')
    derived = {name: [str(value) for value in item.simplified().values] if isinstance(item, Jet) else str(item)
               for name, item in model.items()}
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'algebra_sha256': hashlib.sha256((ROOT/'pn_algebra.py').read_bytes()).hexdigest(), 'checks': checks,
              'coefficient_order': ['1', 'x', 'lambda_over_d0_fifth', 'x_times_lambda_over_d0_fifth'],
              'central_fraction_definition': 'chi=M_body/(M_body+mu_companion); only body2 deforms electrically',
              'derived': derived, 'GR_matching_input': {key: str(value) for key, value in gr_matching(central_fraction).items()},
              'time_domain_phase_primitive': str(sp.factor(time_phase)),
              'input_attribution': 'Universal retained-GR 1PN reduced action and uncontracted mass quadrupole: Vines-Flanagan-Hinderer2011 Eqs2.2-2.4 and3.2-3.3. Not newly derived microscopic MTS coefficients.',
              'independent_checks': ['Parent direct-field energy44/9', 'Parent source-normalized wave85/21', 'Conserved-current translated moments in separate script'],
              'same_source_checks': 'Circular GR coefficients used only after reduction, but share the universal matching source and are not an independent experimental validation.',
              'new_body_coefficient_fitted': False, 'axial_Love_assumed_zero': False,
              'scope': 'Adiabatic electric-quadrupole sector through first relative PN, linear in lambda. Does not include an independent magnetic Love response.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'energy': derived['energy'], 'flux': derived['flux'],
                      'chirp': derived['chirp'], 'fourier_phase_mixed': derived['fourier_phase_mixed']}))


if __name__ == '__main__':
    main()
