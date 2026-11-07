from common import ROOT, SECOND, ALGEBRA, modest, guard, digest, read, write, require
from derive_and_test import matrices, JFULL, load, sup, norm
import numpy as np
from scipy.linalg import expm, expm_frechet


def main():
    modest()
    output = ROOT / "canonical"
    output.mkdir(exist_ok=False)
    frozen = {str(path): digest(path) for path in (ROOT / "CANONICAL-PROTOCOL.md", ROOT / "canonical_generator.py",
              ROOT / "derive_and_test.py", ROOT / "result.json")}
    write(output / "frozen-inputs.json", dict(sources=frozen, harmonics=[2, 4], phases=[16, 32], probes=33))
    parent = read(SECOND / "prediction-result.json")
    reports = []
    for family in parent["reports"]:
        guard()
        case = next(row for row in family["cases"] if row["tag"] == "G192-full-fine")
        path = SECOND / "runs-second" / (family["model"] + "-" + family["label"]) / case["file"]
        require(digest(path) == case["sha256"], "frozen source")
        if family["model"] == "cold":
            reports.append(dict(family="cold-" + family["label"], identity_control=True, passed=True,
                                scope="no heavy carrier and therefore no new micromotion map", packet=str(path), sha256=case["sha256"]))
            continue
        packet = load(path)
        probes = np.unique(np.linspace(0, len(packet["a"]) - 1, 33, dtype=int))
        maximum = dict(fourier_reconstruction=0., coefficient_refinement=0., symplectic=0., inverse=0.,
                       transformed_symmetry=0., full_chain=0., metric_mixing=0., generator_norm=0., near_identity=0.)
        raw_variation, transformed_variation, mean_shifts = [], [], []
        for index in probes:
            guard()
            scale, hubble, wave = float(packet["a"][index]), float(packet["H"][index]), family["wave"]
            meta, observed, terms = packet["metadata"][index], packet["observer"][index], packet["terms"][index]
            omega_s, omega_h = scale * meta[8], scale * meta[18]
            phase, mu = float(packet["carrier_phase"][index]), float(packet["carrier_derivative"][index])
            background = scale * (np.sqrt(omega_h) * meta[14] + 1j * meta[15] / np.sqrt(omega_h)) * np.exp(1j * phase)
            slow_scale, metric_scale = scale * (wave**2 + omega_s**2)**.25, scale * np.sqrt(wave)
            balance = np.diag([1 / slow_scale, slow_scale, 1., 1., 1 / metric_scale, metric_scale, 1 / metric_scale, metric_scale])
            inverse_balance = np.diag(1 / np.diag(balance))
            def evaluate(angles):
                count = len(angles)
                repeat = lambda value: np.full(count, value)
                exact, mean = matrices(repeat(scale), repeat(hubble), repeat(omega_s), repeat(meta[5]),
                                       repeat(omega_h), repeat(background), repeat(mu), np.array(angles), wave)[:2]
                return np.einsum("ij,njk,kl->nil", balance, exact, balance), balance @ mean[0] @ balance
            coefficients = []
            for count in (16, 32):
                angles = 2 * np.pi * np.arange(count) / count
                full, average = evaluate(angles)
                coefficients.append({harmonic: (2 * np.mean(full * np.cos(harmonic * angles)[:, None, None], axis=0),
                                                2 * np.mean(full * np.sin(harmonic * angles)[:, None, None], axis=0))
                                     for harmonic in (2, 4)})
            size = max(norm(full), 1.)
            maximum["coefficient_refinement"] = max(maximum["coefficient_refinement"],
                max(sup(coefficients[0][harmonic][part] - coefficients[1][harmonic][part]) / size
                    for harmonic in (2, 4) for part in (0, 1)))
            coefficients = coefficients[1]
            other_pressure, shear = float(terms[:5, 2].sum()), float(observed[4])
            linear = np.zeros(8)
            linear[4] = -scale**2 / hubble * (other_pressure / 2 - shear / 3)
            linear[6] = 2 * scale**2 * shear / hubble
            balanced_linear = balance @ linear
            seed = np.sin(np.arange(1., 9.))
            transformed_samples, exact_samples = [], []
            for angle in np.r_[phase, 2 * np.pi * np.arange(16) / 16]:
                exact, average = evaluate([angle])
                exact = exact[0]
                oscillating = sum(np.cos(harmonic * angle) * values[0] + np.sin(harmonic * angle) * values[1]
                                  for harmonic, values in coefficients.items())
                generating = sum((np.sin(harmonic * angle) * values[0] - np.cos(harmonic * angle) * values[1]) /
                                 (harmonic * mu) for harmonic, values in coefficients.items())
                generator_matrix = JFULL @ generating
                transform, fast_derivative = expm_frechet(generator_matrix, JFULL @ oscillating)
                new_hessian = transform.T @ exact @ transform + transform.T @ JFULL @ fast_derivative
                new_linear = transform.T @ balanced_linear
                original_rate = JFULL @ (exact @ transform @ seed + balanced_linear)
                replay_rate = transform @ JFULL @ (new_hessian @ seed + new_linear) + fast_derivative @ seed
                maximum["fourier_reconstruction"] = max(maximum["fourier_reconstruction"], sup(exact - average - oscillating) / size)
                maximum["symplectic"] = max(maximum["symplectic"], sup(transform.T @ JFULL @ transform - JFULL))
                maximum["inverse"] = max(maximum["inverse"], sup(expm(-generator_matrix) @ transform - np.eye(8)))
                maximum["transformed_symmetry"] = max(maximum["transformed_symmetry"], sup(new_hessian - new_hessian.T) / max(norm(new_hessian), 1.))
                maximum["full_chain"] = max(maximum["full_chain"], sup(original_rate - replay_rate) / norm(original_rate))
                maximum["metric_mixing"] = max(maximum["metric_mixing"], sup(transform[4:, :4]), sup(transform[:4, 4:]))
                maximum["generator_norm"] = max(maximum["generator_norm"], float(np.linalg.norm(generator_matrix, np.inf)))
                maximum["near_identity"] = max(maximum["near_identity"], float(np.linalg.norm(transform - np.eye(8), np.inf)))
                if len(transformed_samples) < 16:
                    transformed_samples.append(new_hessian)
                    exact_samples.append(exact)
            sampled = np.array(transformed_samples[1:] + [new_hessian])
            old = np.array(exact_samples[1:] + [exact])
            raw_variation.append(norm(old - average) / size)
            transformed_variation.append(norm(sampled - sampled.mean(axis=0)) / size)
            mean_shifts.append(norm(sampled.mean(axis=0) - average) / size)
        required = ("fourier_reconstruction", "coefficient_refinement", "symplectic", "inverse", "transformed_symmetry", "full_chain")
        require(all(maximum[name] < ALGEBRA for name in required), "canonical frozen identity")
        report = dict(family=family["model"] + "-" + family["label"], packet=str(path), sha256=case["sha256"],
                      passed=True, probes=len(probes), maxima=maximum, raw_harmonic_variation=max(raw_variation),
                      transformed_harmonic_variation=max(transformed_variation), transformed_mean_shift=max(mean_shifts),
                      worst_local_variation_ratio=max(new / max(old, 1e-80) for old, new in zip(raw_variation, transformed_variation)),
                      full_time_derivative_included=False, forward_qualified=False)
        write(output / (report["family"] + ".json"), report)
        reports.append(report)
        print(report["family"], maximum, "variation_ratio", report["worst_local_variation_ratio"], flush=True)
        del packet
    write(output / "result.json", dict(passed=True, reports=reports, source_hashes=frozen,
          exact_frozen_canonical_map=True, actual_background_derivative_pending=True,
          no_future_perturbation_states_used_in_coefficients=True, new_evolutions=0))
    print("Canonical coefficient tests complete", flush=True)


if __name__ == "__main__":
    main()

