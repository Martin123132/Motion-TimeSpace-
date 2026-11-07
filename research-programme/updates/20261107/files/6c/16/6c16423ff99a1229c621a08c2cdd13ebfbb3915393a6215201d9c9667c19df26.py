from common import ROOT, EARLY, require
import numpy as np
from scipy.interpolate import CubicSpline


def packet(model, index, tag):
    with np.load(ROOT / f"packets/{model}-{index}-{tag}.npz") as data:
        return {key: data[key].copy() for key in data.files}


def fields(model):
    with np.load(EARLY / f"runs/backgrounds/{model}.npz") as data:
        if model == "heavy":
            return CubicSpline(data["heavy_efold"], data["phi_h"]), CubicSpline(data["heavy_efold"], data["phidot_h"]), float(data["heavy_mass_mpc"])
    return None, None, 0.


def physical(data, model):
    names, standard_names = data["observer_names"].tolist(), data["names"].tolist()
    value = lambda name: data["observer"][:, names.index(name)]
    standard = lambda name: data["standard"][:, standard_names.index(name)]
    wave = float(data["k"])
    scale, hubble = value("a_native"), value("H_native")
    enthalpy = value("R") + value("Pbar")
    alpha = value("sigma") / wave
    curvature = value("eta_sync")
    phi = curvature - hubble * alpha
    psi = 2 * value("Weyl") - phi
    result = dict(Phi=phi, Psi=psi, Dstar=value("D_sync") - 3 * enthalpy * curvature,
        Q=value("Q_sync") + enthalpy * value("sigma"), Pi=value("Pi"),
        d_c=value("delta_cdm64") - 3 * curvature, theta_c=wave**2 * alpha,
        delta_b=value("delta_baryon64") - 3 * hubble * alpha,
        delta_gamma=value("delta_gamma64") - 4 * hubble * alpha,
        delta_neutrino=value("delta_massless64") - 4 * hubble * alpha)
    if model == "heavy":
        background, speed, mass = fields(model)
        field, velocity = background(np.log(scale)), speed(np.log(scale))
        result["u"] = standard("mts_dphi_h") + velocity * alpha
        result["p"] = standard("mts_dphidot_h") - (scale * mass)**2 * field * alpha - 3 * velocity * curvature
        result["Dstar_h"] = velocity * result["p"] + (scale * mass)**2 * field * result["u"]
        result["Q_h"] = wave * velocity * result["u"]
    return result


def norm_error(difference, reference):
    return float(np.max(abs(difference)) / max(float(np.max(abs(reference))), 1e-30))


def algebraic(data):
    names = data["observer_names"].tolist()
    value = lambda name: data["observer"][:, names.index(name)]
    wave = float(data["k"])
    hubble = value("H_native")
    enthalpy = value("R") + value("Pbar")
    alpha = value("sigma") / wave
    phi = value("eta_sync") - hubble * alpha
    psi = 2 * value("Weyl") - phi
    density = value("D_sync") - 3 * hubble * enthalpy * alpha
    momentum = value("Q_sync") + enthalpy * value("sigma")
    star = density - 3 * enthalpy * phi
    recovered = -(star + 3 * hubble * momentum / wave) / (2 * wave**2 + 3 * enthalpy)
    rate = value("Weyl_prime") + value("Pi_prime") / (2 * wave**2)
    checks = []
    for terms in ([2 * wave**2 * phi, density, 3 * hubble * momentum / wave],
                  [phi, -psi, -value("Pi") / wave**2],
                  [rate, hubble * psi, -momentum / (2 * wave)], [phi, -recovered]):
        array = np.array(terms)
        checks.append(float(np.max(abs(np.sum(array, axis=0)) / np.maximum(np.max(abs(array), axis=0), 1e-30))))
    require(np.all(enthalpy > 0), "nonpositive enthalpy")
    return max(checks)
