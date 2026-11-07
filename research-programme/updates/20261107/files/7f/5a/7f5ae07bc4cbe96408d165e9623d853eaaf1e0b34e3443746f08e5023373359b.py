from common import ROOT, COUPLED, WAVE, ALGEBRA, modest, require, read, write, digest, load
from check_evolution_algebra import physical
import numpy as np

def main():
    modest()
    accepted=read(ROOT/"comparison-algebra-result.json")
    require(accepted["passed"],"accepted coupled checks")
    reports=[]
    for model in ("heavy","cold"):
        path=ROOT/"runs-configured"/model/"G192-fine.npz"
        packet=load(path)
        old=load(COUPLED/"runs"/model/"G192-fine.npz")
        values=physical(packet)
        density_norm=float(np.max(abs(values["D"])))
        flux_norm=float(np.max(abs(values["Q"])))
        shear_norm=float(np.max(abs(values["Pi"])))
        poisson=-values["D"]/(2*WAVE**2)
        difference=values["Psi"]-poisson
        exact_correction=-3*values["H"]*values["Q"]/(2*WAVE**3)-values["Pi"]/WAVE**2
        scale=density_norm/(2*WAVE**2)
        discrepancy=float(np.max(abs(difference-exact_correction))/scale)
        epsilon=float(np.max(values["H"])/WAVE)
        flux_ratio=flux_norm/density_norm
        shear_ratio=shear_norm/density_norm
        bound=3*epsilon*flux_ratio+2*shear_ratio
        actual=float(np.max(abs(difference))/scale)
        require(discrepancy<ALGEBRA and actual<=bound+ALGEBRA,"exact limit-budget inequality")
        errors=np.max(abs(old["projected_state"]-packet["projected_state"]),axis=0)/np.maximum(np.max(abs(packet["projected_state"]),axis=0),1e-80)
        position=int(np.argmax(errors))
        metadata=packet["metadata"]
        heavy_mass=metadata[:,18]
        heavy_frequency=packet["a"]*heavy_mass
        frequency_ratios=None
        if np.min(heavy_frequency)>0:
            frequency_ratios=dict(k_over_am=[float(np.min(WAVE/heavy_frequency)),float(np.max(WAVE/heavy_frequency))],
                                  H_over_am=[float(np.min(packet["H"]/heavy_frequency)),float(np.max(packet["H"]/heavy_frequency))])
        report=dict(model=model,source_sha256=digest(path),wave_mpc_inverse=WAVE,
                    scale_interval=[float(packet["a"][0]),float(packet["a"][-1])],
                    conformal_H_interval=[float(np.min(packet["H"])),float(np.max(packet["H"]))],
                    H_over_k=[float(np.min(values["H"])/WAVE),epsilon],flux_over_density_norm=flux_ratio,
                    shear_over_density_norm=shear_ratio,poisson_normalized_error=actual,triangle_bound=bound,
                    bound_slack=bound-actual,identity_error=discrepancy,heavy_ratios=frequency_ratios,
                    largest_state_change=dict(native_index=int(packet["mapping"][position]),relative=float(errors[position]),
                                              old_peak=float(np.max(abs(old["projected_state"][:,position]))),
                                              new_peak=float(np.max(abs(packet["projected_state"][:,position])))),
                    convergence_statement="Requires 3 sup(H/k) ||Q||/||D|| + 2 ||Pi||/||D|| -> 0; H/k -> 0 alone is insufficient.",
                    scope="same relativistic source history, positive conformal H, nonzero density norm; not an independently evolved Poisson system")
        reports.append(report)
        print(report,flush=True)
    write(ROOT/"newton-limit-budget.json",dict(passed=True,reports=reports,source_sha256=digest(__file__),
                                             comparison_sha256=digest(ROOT/"comparison-algebra-result.json"),
                                             norm="time-sup norm on the declared physical interval",no_fitted_coefficients=True))

if __name__=="__main__":
    main()

