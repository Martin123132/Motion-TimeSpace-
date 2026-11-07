from step_common import *


def main():
    modest()
    theta = 4.596201578526332e-4
    chi = 5.755472902372619e-10
    model = CollisionStep(64, 8, theta, chi, .001)
    symmetric = model.symmetric_photon()
    residual = symmetric - symmetric.T
    error = np.max(abs(residual.data)) if residual.nnz else 0.
    norm = max(np.max(abs(symmetric.data)), 1.)
    energy_identity = np.max(abs(model.entropy_metric * model.temperature_equilibrium - model.energy))
    momentum_identity = np.max(abs(model.entropy_metric * model.velocity_equilibrium - model.flux))
    equilibria = [np.max(abs(model.source(model.temperature_equilibrium, 1., 0.))),
                  np.max(abs(model.source(model.velocity_equilibrium, 0., 1.))),
                  np.max(abs(model.source(model.chemical_equilibrium, 0., 0.)))]
    eigenvalues = spla.eigsh(symmetric, k=4, which='LA', return_eigenvectors=False, tol=1e-9)
    print(json.dumps(dict(size=model.size, symmetric_error=float(error / norm), energy_identity=float(energy_identity),
                         momentum_identity=float(momentum_identity), equilibrium=equilibria,
                         largest_eigenvalues=eigenvalues.tolist(), number_source=float(np.max(abs(model.number @ model.photon))))), flush=True)


if __name__ == '__main__':
    main()
