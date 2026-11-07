from pathlib import Path

import sympy as sp

from interior_energy import ROOT, Interior, dependencies, read_json, digest, save, modest_process


def main():
    modest_process()
    vacuum_path = ROOT/'results/vacuum-canonical/status.json'
    vacuum = read_json(vacuum_path)
    namespace = {name:sp.Symbol(name, positive=True) for name in ['r', 'M']}
    namespace.update({name:sp.Symbol(name, real=True) for name in ['Z', 'V']})
    contact = sp.lambdify(list(namespace.values()), sp.sympify(vacuum['boundary_contact_times_alpha'], locals=namespace), 'numpy')
    rows, inputs = [], dependencies()
    inputs[str(vacuum_path)] = digest(vacuum_path)
    for label in ['coarse', 'fine', 'refined', 'edge_check']:
        interior = Interior(label)
        integral = interior.integral()
        surface = interior.row['static_master']
        value = float(contact(interior.radius, interior.mass, *surface))
        predicted = (interior.alpha*sum(integral)-value)/(1.5*surface[0]**2)
        target = -interior.row['coefficient_s2']
        row = dict(label=label, bulk_mass=float(sum(integral)), contact_times_alpha=value,
            canonical_normalization=1.5/interior.alpha, amplitude=surface[0],
            predicted_A=float(predicted), response_A=target, relative_error=float(predicted/target-1))
        rows.append(row)
        inputs[str(interior.archive_path)] = digest(interior.archive_path)
        inputs[str(interior.profile.path)] = digest(interior.profile.path)
        print(row, flush=True)
    save('match', Path(__file__), dict(input_hashes=inputs, rows=rows,
         formula='A=(alpha*integral(M_ADM)-C_surface)/(1.5*Z_surface^2)'))


if __name__ == '__main__':
    main()

