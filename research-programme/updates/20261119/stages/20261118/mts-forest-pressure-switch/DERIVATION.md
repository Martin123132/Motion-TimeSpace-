# From the retained scalar to a force a particle/field calculation can use

Use conformal time τ, scale factor a, Hc=aH, physical peculiar velocity, c=ℏ=1 and comoving k in Mpc⁻¹. The retained example is the positive quadratic massive mode in the ordinary matter metric; its abundance and state are fixed to the saved cosmological example. Neither a nonlinear force law fitted to a galaxy nor a new gravity coupling is introduced. Parent sources: ../MTS-HEAVY-BATH-COUNTERFLOW-AND-GALACTIC-STRESS.md, ../mts-absolute-matter-preparation-20261118/EQUATIONS.md, and the original native MTSTwoField.f90 (path/hash in build.json). This calculation concerns scalar perturbations and the weak-field approximation on its tested states.

## A matched intervention

D_h,q_h are synchronous, CDM-comoving heavy density contrast and momentum per homogeneous heavy density. After the earlier phase match the background is pressureless. In the native scalar equations

    Π = c_s² (D_h + 3 Hc q_h/k),       u=k/(a m_h)
    c_s²=u²/(sqrt(1+u²)+1)²,
    D_h' = −k Z − k q_h − 3 Hc Π,     q_h' = −Hc q_h + k Π,
    D_c' = −k Z.

Z is the scalar synchronous expansion perturbation in the solver (not redshift). All species contribute to the returned Einstein sources. At the requested full-state output, save the active state, leave it untouched, reset integrator history on *both* arms, and change only the pressure callback on the chosen arm. The output exactly at the switch is left-sided; subsequent outputs use the new stress. The all-cold control has no such callback contribution. This avoids stepping across an unlocated discontinuity or fixing later gravity to the control.

Δ means wave minus identically prepared pressureless. For identical initial data at τ_s,

    Δq_h = k/a ∫ a Π_wave dτ,
    Δ(D_h−D_c) = −k ∫ Δq_h dτ − 3 ∫ Hc Π_wave dτ.

Common metric forcing cancels *in this relative density*, not in baryons, potentials or individual CDM perturbations. Dust current separately obeys aq_h=constant. green-response.csv integrates the source independently using cubic antiderivatives; its errors are normalized to clustered mode scales (not to vanishing differences). Changing the gravity through its density input is essential to the reported result.

## What “force” means here

Let U_c,b=−θ_c,b/Hc in Newtonian gauge, σ=−Hc U_c/k. In the native flat background Φ=etak/k−Hc σ/k and Ψ=2Φ_W−Φ where the native Weyl transfer is k²Φ_W. Our force column is **−k²Ψ**, the scalar driving velocity convergence; its fractional change is also that of the acceleration at fixed k and a. D_b,N=D_b,sync−3Hcσ/k. The independent CDM geodesic check is (aHcU_c)'=a(−k²Ψ). The baryon geodesic-only residual includes non-gravitational forces; we did not force it to vanish.

Writing g_i=4πG a²ρ_i, the flat constraint for Ψ contains density, longitudinal momentum and anisotropic stress. We separately reconstruct the clustered comoving source g_c D_c+g_b D_b+g_h D_h+3Hc(g_b v_b+g_h q_h)/k. geodesic-and-source.csv separates ordinary radiation, massive-neutrino density, rolling scalar and photon shear. The unallocated term includes neutrino momentum/shear not separately present in the saved readouts and numerical residuals; it is not assigned to a new force.

## Independent clustered-sector prediction

The reduced system uses C=D_c, J=C', b=D_b−C, v=v_b,sync, r=D_h−C and q=q_h. Combine the synchronous CDM continuity equation with the Einstein trace (Raychaudhuri):

    C'=J
    J'=−Hc J + (g_c+g_b+g_h) C + g_b b + g_h(r+3Π)
    b'=−kv,                         v'=−Hc v
    r'=−kq−3HcΠ,                    q'=−Hc q+kΠ.

The trace omits the residual radiation, slow field, massive-neutrino perturbations and baryon pressure; the homogeneous expansion remains that of the branch. This is a closed approximation, not a replacement trace identity for the full theory. The seed J follows from the full initial density constraint, not a late growth fit. Its predicted shear and force use σ=−J/k+3(g_b v+g_h q)/k² and −k²Ψ≈(g_c+g_b+g_h)C+g_b b+g_h r+3Hc(g_b v+g_h q)/k. Tests distinguish absolute fields from ratios of two approximate solutions. An alternative correction about a *supplied pressureless evolution* evolves the same differences with zero initial state and adds the pressureless D_h+3Hc q_h/k to the stress argument. It needs that pressureless history, not a future pressure-on field.

The leading dispersion follows by expansion, not a fitted coefficient: c_s²=u²/4+O(u⁴), so the conformal restoring-frequency squared is k⁴/(4a²m_h²). Replacing only c_s² tests the leading coefficient in the complete native hierarchy; it is more restrictive than showing the reduced stand-alone calculation gets the signs right.

## Nonlinear Newtonian carrier, and its limit

For a single coherent, slowly modulated nonrelativistic envelope, remove homogeneous dilution from the retained massive scalar. In conformal coordinates its leading equation is iψ'=−∇²ψ/(2ma)+maΨψ. The potential is sourced by *all* gravitating densities. Put n=|ψ|² and j_i=Im(ψ*∂iψ)/(ma). Direct substitution gives

    n'+∂i j_i=0,
    j_i'+Hc j_i+∂j F_ij=−n ∂iΨ,
    F_ij=[Re((∂iψ)* ∂jψ) − δ_ij ∇²n/4]/(ma)².

For n>0, subtract advection j_i j_j/n: the remaining stress is [(∂i n)(∂j n)/n−δ_ij ∇²n]/(4m²a²). Its linear longitudinal source is +k²δ/(4m²a²). Keeping a rest-frame density when embedding this coefficient in the relativistic calculation is important. The flux in ψ has no division by density and remains finite at interference nodes. An alternative Newtonian stress differing by a divergence-free tensor gives the same bulk force, but is **not** automatically the same relativistic Hilbert stress. No general anisotropic-stress replacement in the Einstein equation, or mixed-state galactic occupation, is inferred.

Periodic 3D controls use an independently differentiated Schrödinger RHS, normalized wave/cold/baryon density sources, an integrated Poisson force and the expanding energy identity (K+W)'=−Hc(2K+W). Smooth and exact-node synthetic heavy cases use the saved expansion, mass and fractions; the cold control has zero wave weight. This is a local-in-time nonlinear balance check on two spatial resolutions, not a long nonlinear hydrodynamical simulation.

