from __future__ import annotations

from pathlib import Path
import numpy as np
import sympy as sp

from interior_common import ROOT, PARENT, modest_process, read_json, save
from local_system_v2 import LocalSystem
from polar_energy import quadrature, even_form


def main():
    modest_process()
    system = LocalSystem()
    background = system.background
    radius = background.radius
    coordinate = sp.symbols('x', positive=True)
    master = coordinate**3/(1+coordinate**5)
    matter = coordinate**2*(1-coordinate)**2
    functions = sp.lambdify(coordinate, [master, sp.diff(master, coordinate), sp.diff(master, coordinate, 2), matter, sp.diff(matter, coordinate), sp.diff(matter, coordinate, 2)], 'numpy')
    configurations = [('gravity', [np.sqrt(background.alpha)*radius, 0., 0.]), ('scalar', [0., 1., 0.]), ('phase', [0., 0., 1.]), ('mixed', [np.sqrt(background.alpha)*radius, .3, -.2])]
    rows = []
    for cells in [128, 256]:
        interior_position, interior_weights, *_ = quadrature(np.linspace(0, radius, cells+1), 10)
        tail_nodes, tail_factors = np.polynomial.legendre.leggauss(128)
        tail_coordinate = (tail_nodes+1)/2
        exterior_position = radius/tail_coordinate
        exterior_weights = radius*tail_factors/(2*tail_coordinate**2)
        all_positions = np.r_[interior_position, exterior_position, radius]
        all_weights = np.r_[interior_weights, exterior_weights]
        values, coefficients, derivatives, local, contacts = system.values(all_positions)
        profile = functions(all_positions/radius)
        for name, factors in configurations:
            master_value = factors[0]*profile[0]
            master_first = factors[0]*profile[1]/radius
            master_second = factors[0]*profile[2]/radius**2
            interior = all_positions < radius
            scalar = np.where(interior, factors[1]*profile[3], 0.)
            scalar_first = np.where(interior, factors[1]*profile[4]/radius, 0.)
            scalar_second = np.where(interior, factors[1]*profile[5]/radius**2, 0.)
            phase = np.where(interior, factors[2]*profile[3], 0.)
            phase_first = np.where(interior, factors[2]*profile[4]/radius, 0.)
            vector = np.stack([master_first, master_value, scalar_first, scalar, phase], axis=1)
            vector_first = np.stack([master_second, master_first, scalar_second, scalar_first, phase_first], axis=1)
            names = ['k_Zprime', 'k_Z', 'k_wprime', 'k_w', 'k_pibar']
            angular = sum(coefficients[key]*vector[:, index] for index,key in enumerate(names))
            angular_prime = sum(derivatives[key]*vector[:, index]+coefficients[key]*vector_first[:, index] for index,key in enumerate(names))
            difference = coefficients['beta']/values['metric']*(3*master_value/all_positions-angular)
            difference_prime = (derivatives['beta']/values['metric']-coefficients['beta']*values['metric_prime']/values['metric']**2)*(3*master_value/all_positions-angular)+coefficients['beta']/values['metric']*(3*master_first/all_positions-3*master_value/all_positions**2-angular_prime)
            radial = all_positions*angular_prime+difference
            amplitude = scalar+coefficients['a']*angular
            amplitude_prime = scalar_first+coefficients['a_prime']*angular+coefficients['a']*angular_prime
            momentum = phase+coefficients['c']*angular_prime+coefficients['d']*angular
            curvature = 2*values['metric']/all_positions*difference_prime+((6+2*values['metric'])/all_positions**2+2*values['metric_prime']/all_positions)*difference+((6-2*values['metric'])/all_positions+values['metric_prime'])*angular_prime+4*angular/all_positions**2
            density = background.frequency*values['field']/values['lapse']*momentum-values['rotation2']*values['field']**2*(radial+2*angular)/2-values['rotation2']*values['field']*amplitude-values['metric']*values['gradient']**2*radial/2+values['metric']*values['gradient']*amplitude_prime+values['force']*amplitude
            constraint_error = float(np.max(abs(curvature-4*background.alpha*density))/max(np.max(abs(curvature)), np.max(abs(4*background.alpha*density)), 1e-30))
            measure = values['lapse']*all_positions**2/np.sqrt(values['metric'])
            local_density = measure*np.einsum('qi,qij,qj->q', vector, local, vector)/2
            surface_contact = float((measure*(contacts[0]*angular**2/2+contacts[1]*angular*master_value+contacts[2]*angular*scalar))[-1])
            parts = []
            for selection, weights in [(slice(0,len(interior_position)), interior_weights), (slice(len(interior_position),-1), exterior_weights)]:
                original = float(even_form(background, all_positions[selection], weights, radial[selection,None], angular[selection,None], angular_prime[selection,None], amplitude[selection,None], amplitude_prime[selection,None], momentum[selection,None])[0,0]/2)
                reduced = float(np.sum(weights*local_density[selection]))
                parts.append((original,reduced))
            full_original = sum(pair[0] for pair in parts)
            full_local = sum(pair[1] for pair in parts)
            scale = max(abs(full_original), abs(full_local), 1e-30)
            rows.append(dict(cells=cells, profile=name, original_energy=full_original, local_energy=full_local,
                joined_relative_error=abs(full_original-full_local)/scale,
                interior_contact_relative_error=abs(parts[0][0]-parts[0][1]-surface_contact)/scale,
                exterior_contact_relative_error=abs(parts[1][0]-parts[1][1]+surface_contact)/scale,
                surface_contact=surface_contact, constraint_relative_error=constraint_error))
    assert all(row['joined_relative_error'] < 1e-8 and row['interior_contact_relative_error'] < 1e-8 and row['exterior_contact_relative_error'] < 1e-8 for row in rows), rows
    assert all(row['constraint_relative_error'] < 1e-9 for row in rows), rows
    save('replay-v2', Path(__file__), dict(rows=rows, new_field_solves=0, scope='Arbitrary off-shell regular profiles in new variables; reconstruct old constrained fields and compare complete original/local energies on both sides of surface.'), [ROOT/'results/energy-v2/status.json', background.profile.path])
    print(dict(rows=rows), flush=True)


if __name__ == '__main__':
    main()
