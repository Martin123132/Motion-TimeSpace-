from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    output = ROOT/'results/convention-crosswalk'
    output.mkdir(parents=True, exist_ok=False)
    degree, mass, moment, tide = sp.symbols('ell M S_l B_l', positive=True)
    normalization = sp.sqrt(4*sp.pi/(2*degree+1))
    growing = 2*tide/(3*degree*(degree-1))
    decaying = 2*normalization*moment/degree
    published = -sp.Rational(3, 2)*degree*(degree-1)/(degree+1)*normalization*moment/tide/mass**(2*degree+1)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('Cardoso_B10_and_definition3_general', published+degree/(2*(degree+1))*decaying/growing/mass**(2*degree+1))
    ratio, sigma_bar = sp.symbols('response sigma_bar', real=True)
    quadrupole_k = -ratio/(3*mass**5)
    exact('Cartesian_sigma_to_Cardoso_k2B', quadrupole_k.subs(ratio, -6*sigma_bar)-2*sigma_bar/mass**5)
    exact('BV_sigma_halves_barred_sigma', (sigma_bar/2)*4/mass**5-2*sigma_bar/mass**5)
    landry_k = -ratio/(3*(2*mass)**5)
    exact('Landry_K2mag_to_Cardoso_k2B', 32*landry_k-quadrupole_k)
    (output/'status.json').write_text(json.dumps({'state': 'complete',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checks': checks, 'definitions': {
            'metric_response': 'response=b/a',
            'Cartesian_geometric_sigma_bar': '-response/6',
            'BV_geometric_sigma': '-response/12',
            'Cardoso_k2B': '-response/(3*M^5)=2*geometric_sigma_bar/M^5',
            'Landry_K2mag': '-response/(96*M^5)'},
        'source': 'Cardoso2017 Eqs3,B10,C16; LandryPoisson2015 Eq5.8; BanihashemiVines2020 Eqs20,25,33.'}, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks)}))


if __name__ == '__main__':
    main()
