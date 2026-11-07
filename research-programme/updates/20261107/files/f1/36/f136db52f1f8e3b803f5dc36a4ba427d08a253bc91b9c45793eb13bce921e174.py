import argparse
from nonlocal_dc import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--soft', type=int, required=True)
    parser.add_argument('--seed', type=int, required=True)
    arguments = parser.parse_args()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    basis, specification = current_basis()
    full, local, diagnostics = build_matrix(basis, arguments.soft, arguments.seed)
    frequency, measure = thermal_wave.frequency_quadrature(arguments.soft, basis.minimum, basis.maximum / 2)
    shape = integrated_dc.integrated_dc_absorption_shape(frequency, arguments.seed)
    values = basis.evaluate(frequency)
    imported = (values.T * (measure * shape)) @ values
    slope = soft_slope_row(basis)
    scale = np.linalg.norm(full) * np.linalg.norm(basis.temperature)
    checks = [
        check('Three-photon energy identity is exact before quadrature', diagnostics['maximum_event_temperature_null'], 1e-13),
        check('Full matrix retains photon-energy null', np.linalg.norm(full @ basis.temperature) / scale, 1e-12),
        check('Restricted soft readout reproduces imported integrated absorption', relative(local, imported), 1e-10),
        check('Positive weak measure gives nonnegative finite matrix', max(0., -float(np.linalg.eigvalsh(full).min())) / np.linalg.norm(full), 1e-12),
        check('Derived hard-slope row recognizes the photon temperature mode', abs(slope @ basis.temperature - 1), 1e-10),
        dict(name='Photon chemical mode retains production', passed=bool(basis.chemical @ full @ basis.chemical > 0))]
    np.savez(folder / 'matrix.npz', nonlocal_matrix=full, local_soft_matrix=local, slope_row=slope)
    finish(folder, dict(arguments=vars(arguments), basis_spec=specification, checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), elapsed_seconds=time.monotonic() - started,
           diagnostics=diagnostics, matrix_norm=float(np.linalg.norm(full)),
           photon_temperature_relaxation_local=float(basis.temperature @ local @ basis.temperature),
           photon_temperature_relaxation_nonlocal=float(basis.temperature @ full @ basis.temperature),
           leading_Gould_no_recoil=True, exact_relativistic_finite_frequency_kernel=False),
           __file__, [KINETIC / 'backgrounds/heavy-derived-gaunt/status.json'])
    print(json.dumps(dict(name=arguments.name, seconds=time.monotonic() - started,
                         failed=[row for row in checks if not row['passed']],
                         diagnostics=diagnostics)), flush=True)


if __name__ == '__main__':
    main()
