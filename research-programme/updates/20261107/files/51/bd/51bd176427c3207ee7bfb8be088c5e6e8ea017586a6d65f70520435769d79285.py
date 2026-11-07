from pathlib import Path

from interior_energy import ROOT, Interior, dependencies, digest, save, modest_process


def main():
    modest_process()
    rows = []
    inputs = dependencies()
    for label in ['coarse', 'fine', 'refined', 'edge_check']:
        interior = Interior(label)
        values = interior.integral()
        row = dict(label=label, terms=values.tolist(), total=float(sum(values)),
                   divided_surface_master_squared=float(sum(values)/interior.master_surface**2),
                   scaled_alpha=float(interior.alpha*sum(values)/interior.master_surface**2),
                   target=-interior.row['coefficient_s2'], alpha=interior.alpha,
                   surface_master=interior.master_surface)
        rows.append(row)
        inputs[str(interior.archive_path)] = digest(interior.archive_path)
        inputs[str(interior.profile.path)] = digest(interior.profile.path)
        print(row, flush=True)
    save('probe', Path(__file__), dict(input_hashes=inputs, rows=rows,
        meaning='Unmatched ADM low-frequency kinetic integral; surface canonical conversion has not yet been applied.'))


if __name__ == '__main__':
    main()

