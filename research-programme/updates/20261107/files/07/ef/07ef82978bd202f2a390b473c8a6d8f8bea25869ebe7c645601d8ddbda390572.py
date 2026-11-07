from common import ROOT, WAVE, ALGEBRA, modest, read, write, digest, load, require
import sympy as sy
import numpy as np

def main():
    modest()
    wave, density, flux, shear, hubble, phi, psi = sy.symbols("k D Q Pi H Phi Psi", nonzero=True)
    solution=sy.solve([2*wave**2*phi+density+3*hubble*flux/wave,phi-psi-shear/wave**2],(phi,psi))
    identity=sy.simplify(solution[psi]+density/(2*wave**2)+3*hubble*flux/(2*wave**3)+shear/wave**2)
    tau=sy.symbols("tau",real=True)
    scale=sy.Function("a")(tau)
    theta=sy.Function("theta")(tau)
    factor=sy.simplify(sy.diff(scale*theta,tau)-scale*wave**2*psi-scale*(sy.diff(theta,tau)+hubble*theta-wave**2*psi))
    factor=sy.simplify(factor.subs(sy.diff(scale,tau),hubble*scale))
    Hmax,ammin=sy.symbols("Hmax ammin",positive=True)
    star=sy.sqrt(Hmax*ammin)
    balance=sy.simplify(Hmax/star-star/ammin)
    identities={"Einstein_force_split":str(identity),"velocity_integrating_factor":str(factor),"balanced_scale_parameters":str(balance)}
    require(all(value=="0" for value in identities.values()),"limit identities")
    owner=read(ROOT/"newton-limit-budget.json")
    require(owner["source_sha256"]==digest(ROOT/"derive_limit_budget.py"),"derived owner")
    require(owner["comparison_sha256"]==digest(ROOT/"comparison-algebra-result.json"),"accepted comparison owner")
    rows=[]
    for row in owner["reports"]:
        model=row["model"]
        packet=load(ROOT/"runs-configured"/model/"G192-fine.npz")
        require(digest(ROOT/"runs-configured"/model/"G192-fine.npz")==row["source_sha256"],"trajectory owner")
        expected=3*row["H_over_k"][1]*row["flux_over_density_norm"]+2*row["shear_over_density_norm"]
        require(expected==row["triangle_bound"] and row["poisson_normalized_error"]<=expected+ALGEBRA,"numerical triangle inequality")
        maximum_H=float(np.max(packet["H"]))
        mass=packet["metadata"][:,18]
        minimum_am=float(np.min(packet["a"]*mass))
        selected=None
        if minimum_am>0:
            selected=float(np.sqrt(maximum_H*minimum_am))
            epsilon=float(np.sqrt(maximum_H/minimum_am))
            require(abs(maximum_H/selected-epsilon)<ALGEBRA and abs(selected/minimum_am-epsilon)<ALGEBRA,"balanced physical wave")
            require(maximum_H < selected < minimum_am,"nonempty nonrelativistic subhorizon interval")
        rows.append(dict(model=model,maximum_H=maximum_H,minimum_am=minimum_am,
                         balanced_wave_mpc_inverse=selected,maximum_balanced_epsilon=epsilon if selected else None,
                         original_wave_mpc_inverse=WAVE,source_sha256=row["source_sha256"]))
    report=dict(passed=True,identities=identities,rows=rows,source_sha256=digest(__file__),
                derivation_sha256=digest(ROOT/"newton-limit-budget.json"),
                scope="Balanced scale minimizes max(Hmax/k,k/ammin); it does not establish small radiation anisotropic stress or dust averaging.")
    write(ROOT/"limit-budget-validation.json",report)
    print(report,flush=True)

if __name__=="__main__":
    main()

