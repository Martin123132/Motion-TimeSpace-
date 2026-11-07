from __future__ import annotations

from pathlib import Path
import numpy as np
import sympy as sp

from bound_common import ROOT, PARENT, Background, read_json, modest_process, save
from polar_energy import quadrature, basis, tail, even_form


def main():
    modest_process()
    background = Background()
    rows, inputs = [], [background.profile.path]
    for label in ['standard', 'refined-mesh', 'resolved-more', 'resolved-mesh', 'resolved-support', 'support-mesh']:
        status_path = PARENT/'results'/label/'status.json'
        archive_path = PARENT/'results'/label/'forms.npz'
        inputs.extend([status_path, archive_path])
        status = read_json(status_path)
        configuration = status['configuration']
        gravity_count, matter_count = configuration['gravity_count'], configuration['matter_count']
        offset = gravity_count+matter_count
        with np.load(archive_path) as data:
            edges = data['edges']
            conformal = data['conformal_solution'][:, offset:]
            exact_matrix = data['even'][offset:, offset:]
        position, weights, cells, shape_left, shape_right = quadrature(edges, configuration['order'])
        width = np.diff(edges)
        values = background.values(position)
        field, metric, lapse, potential, rotation = [values[key] for key in ['field', 'metric', 'lapse', 'energy', 'rotation2']]
        measure = lapse*position**2/np.sqrt(metric)
        phase = basis(position, background.radius, matter_count, 2)[0]
        angular = shape_left[:, None]*conformal[cells]+shape_right[:, None]*conformal[cells+1]
        angular_prime = (conformal[cells+1]-conformal[cells])/width[cells, None]
        constraint = angular_prime.T@((weights*measure*metric)[:, None]*angular_prime)+angular.T@((weights*measure*(6/position**2+background.alpha*(rotation*field**2-potential)))[:, None]*angular)
        nodes, factors = np.polynomial.legendre.leggauss(96)
        inverse_radius = (nodes+1)/2
        tail_position = edges[-1]/inverse_radius
        tail_weights = edges[-1]*factors/(2*inverse_radius**2)
        tail_value, tail_prime = tail(tail_position, background.mass, edges[-1])
        tail_integral = np.sum(tail_weights*((1-2*background.mass/tail_position)*tail_position**2*tail_prime**2+6*tail_value**2))
        constraint += tail_integral*np.outer(conformal[-1], conformal[-1])
        phase_mass = phase.T@((weights*measure)[:, None]*phase)
        cross = angular.T@((weights*measure*np.sqrt(rotation)*field)[:, None]*phase)
        positive = angular.T@((weights*measure*(7*rotation*field**2+5*potential)/8)[:, None]*angular)
        integrated = phase_mass/2-3*(cross+cross.T)/4-constraint/(8*background.alpha)+positive
        eliminated = phase_mass/2-7*constraint/(8*background.alpha)+positive
        direct = exact_matrix/2
        rows.append(dict(label=label, bulk_integration_identity_relative_error=float(np.linalg.norm(integrated-direct)/np.linalg.norm(direct)),
             phase_source_identity_relative_error=float(np.linalg.norm(eliminated-direct)/np.linalg.norm(direct)),
             weighted_constraint_relative_residual=float(np.linalg.norm(constraint-background.alpha*(cross+cross.T))/np.linalg.norm(constraint))))
    vacuum_path = ROOT/'results/vacuum/status.json'
    inputs.append(vacuum_path)
    vacuum = read_json(vacuum_path)
    radius, mass = sp.symbols('r M', positive=True)
    master = sp.Function('Z')(radius)
    contact = sp.sympify(vacuum['contact_4alpha'], locals={'r':radius, 'M':mass, 'Z':sp.Function('Z')})
    master_value, master_first = sp.symbols('value first')
    contact_numeric = sp.lambdify((radius, mass, master_value, master_first), contact.subs({sp.diff(master, radius):master_first, master:master_value}), 'numpy')
    vacuum_rows = []
    for powers in [[(2, 1.)], [(3, 1.), (4, .2)]]:
        profile = sum(coefficient*(background.radius/radius)**power for power, coefficient in powers)
        metric = 1-2*mass/radius
        denominator = 2+3*mass/radius
        coefficient = sp.sympify(vacuum['metric_angular_coefficient'], locals={'r':radius, 'M':mass})
        angular = metric*sp.diff(profile, radius)+coefficient*profile
        radial = radius*sp.diff(angular, radius)+denominator/metric*(3*profile/radius-angular)
        functions = sp.lambdify((radius, mass), [profile, sp.diff(profile, radius), angular, sp.diff(angular, radius), radial], 'numpy', cse=True)
        nodes, factors = np.polynomial.legendre.leggauss(128)
        inverse_radius = (nodes+1)/2
        position = background.radius/inverse_radius
        weights = background.radius*factors/(2*inverse_radius**2)
        master_values, master_derivatives, angular_values, angular_derivatives, radial_values = functions(position, background.mass)
        zeros = np.zeros((len(position), 1))
        adm = float(even_form(background, position, weights, radial_values[:, None], angular_values[:, None], angular_derivatives[:, None], zeros, zeros, zeros)[0, 0]/2)
        metric_values = 1-2*background.mass/position
        potential = metric_values*(24*position**3+24*background.mass*position**2+36*background.mass**2*position+18*background.mass**3)/(position**3*(2*position+3*background.mass)**2)
        positive = float(3/(4*background.alpha)*np.sum(weights*(metric_values*master_derivatives**2+potential/metric_values*master_values**2)))
        surface_master, surface_first, *_ = functions(background.radius, background.mass)
        surface_contact = float(contact_numeric(background.radius, background.mass, surface_master, surface_first)/(4*background.alpha))
        vacuum_rows.append(dict(powers=powers, original_ADM_energy=adm, positive_master_bulk=positive, inner_contact=surface_contact,
            matched_relative_error=abs(adm-(positive-surface_contact))/max(abs(adm), abs(positive)),
            contact_omission_relative_error=abs(adm-positive)/max(abs(adm), abs(positive))))
    assert all(row['bulk_integration_identity_relative_error'] < 1e-8 for row in rows)
    assert all(row['matched_relative_error'] < 1e-10 and row['contact_omission_relative_error'] > .01 for row in vacuum_rows)
    save('replay', Path(__file__), dict(phase_rows=rows, vacuum_rows=vacuum_rows, new_field_solves=0,
         scope='Read-only saved finite-element conformal responses and arbitrary off-shell vacuum master profiles. Constraint substitution has discretization error; surface contact independently retained.'), inputs)
    print(dict(phase_rows=rows, vacuum_rows=vacuum_rows), flush=True)


if __name__ == '__main__':
    main()
