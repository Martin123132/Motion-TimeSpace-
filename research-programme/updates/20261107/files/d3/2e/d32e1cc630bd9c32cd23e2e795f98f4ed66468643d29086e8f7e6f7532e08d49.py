from __future__ import annotations

from datetime import datetime, timezone
import sympy as sp

from polar_radiation import ROOT, digest, write_json, modest_process


def main():
    modest_process()
    body_real, horizon_real, outgoing_current, horizon_current = sp.symbols('a_body a_horizon beta_out beta_horizon', real=True)
    source_real, source_dirichlet = sp.symbols('I_real I_Dirichlet', real=True)
    body_w = body_real+sp.I*outgoing_current
    horizon_w = horizon_real+sp.I*(outgoing_current-horizon_current)
    outgoing_source = source_real+sp.I*outgoing_current*source_dirichlet
    horizon_source = source_real-horizon_real*source_dirichlet+sp.I*horizon_current*source_dirichlet
    body_source = source_real-body_real*source_dirichlet
    reference = horizon_source/horizon_w
    difference = -(body_real-horizon_real+sp.I*horizon_current)*outgoing_source/(body_w*horizon_w)
    checks = []

    def exact(name, expression):
        residual = sp.cancel(sp.together(sp.expand_complex(expression)))
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'residual': str(residual), 'passed': True})

    exact('stable body minus BH amplitude', body_source/body_w-reference-difference)
    infinity = outgoing_current*(2*sp.re(sp.conjugate(reference)*difference)+sp.expand_complex(difference*sp.conjugate(difference)))
    absorption = -horizon_current*sp.expand_complex(outgoing_source*sp.conjugate(outgoing_source)/(horizon_w*sp.conjugate(horizon_w)))
    exact('retarded work equals infinity difference minus absorption', -sp.im(difference*outgoing_source)-infinity+absorption)
    azimuth, harmonic, radial_frequency, angular_frequency, modal_power = sp.symbols('m n Omega_r Omega_phi P', real=True)
    frequency = azimuth*angular_frequency+harmonic*radial_frequency
    exact('two-action first law per signed harmonic', modal_power-angular_frequency*azimuth*modal_power/frequency-radial_frequency*harmonic*modal_power/frequency)
    exact('axisymmetric radiation carries no angular momentum', (azimuth*modal_power/frequency).subs(azimuth, 0))
    exact('circular carrier has zero radial-action flux', (harmonic*modal_power/frequency).subs(harmonic, 0))
    directory = ROOT/'results/derivation'
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory/'status.json', {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
               'script_sha256': digest(__file__), 'checks': checks}, exclusive=True)
    print(len(checks), 'exact identities passed', flush=True)


if __name__ == '__main__':
    main()
