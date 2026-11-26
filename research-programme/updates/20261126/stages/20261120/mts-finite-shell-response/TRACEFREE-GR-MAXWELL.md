> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A three-radius gravity test that does not need a slip boundary condition

**What is input.** Work on the retained common Einstein metric with minimal quadratic heavy mode and gravity normalized as in the parent stress action (not bundled here). The geometrical starting point is the trace-free spatial Einstein equation, equivalently the trace-free extrinsic-curvature evolution equation in the [3+1 formalism](https://arxiv.org/abs/gr-qc/0703035). This is an imported gravitational limit being *tested and matched*, not an independent derivation of Einstein gravity from nothing. The predicted compensated slip below is calculated from the saved material states; it is not taken from a GR halo fit.

## Exact identity on the specified spherical slicing

Use a zero-shift slice with shear-free normals, isotropic comoving radius r, lapse N=exp(U) and spatial metric γ_ij=a²exp(−2V)δ_ij. This is a restriction on the slicing/metric: spherical symmetry alone must not be invoked to discard a nonzero shear on an arbitrary slice. Log potentials are chosen deliberately; second-order differences change under nonlinear redefinitions of metric variables. On these slices K_ij is pure trace. Taking the trace-free part of its evolution leaves

    [R^(3)_ij − D_i D_j N/N]^TF = 8πG S_ij^TF.

The spatial Ricci tensor contributes [V_,ij + V_,i V_,j]^TF. The lapse contributes [U_,ij + U_,i U_,j + V_,i U_,j + V_,j U_,i]^TF. With Δ=V−U, Π=P_r−P_t the anisotropy measured in the normal orthonormal frame, and prime a radial derivative, their difference gives

    Δ''−Δ'/r = 8πG a² exp(−2V) Π + 2V'² − 4V'Δ' + Δ'².

No small-field or static approximation has been used in this equality. If F=exp(−Δ)=exp(U−V), it becomes

    [ exp(4V) F'/r ]' = −exp(4V) F [8πG a² exp(−2V) Π + 2V'²]/r.

Thus for nonnegative radial anisotropy the positive F is concave in the radial variable defined by dξ=r exp(−4V) dr. The sign restriction holds for radial massive streams and a spherically symmetric minimally coupled scalar, not for arbitrary electromagnetic configurations. Isotropic matter pressure cancels from this particular trace-free source; it need not cancel from other Einstein equations.

## Maxwell is a stringent opposite-sign control

For an exterior spherical electric field the radial pressure is −ρ_EM and tangential pressure +ρ_EM. Use the exact electrovac exterior as a check, not as a source of MTS charge: in geometric mass/charge units and a=1 define w=(M²−Q²)/(4r²), B=1+M/r+w. The area radius is rB, exp(−V)=B, exp(U)=(1−w)/B and F=1−w in the exterior patch. The metric source from Maxwell tension is −2Q²/(r⁴B²), unlike either of the positive terms below. The geometric plus matter source simplifies to **2(M²−Q²)/(r⁴B)**. In the uncharged vacuum it is nonzero; at |Q|=M the two terms cancel pointwise *despite a nonzero electric field and nonconstant lapse*. This would fail if field energy were coupled like positive radial dust or if its radial tension had the wrong factor. The calculation solves symbolically for the relative multiplier of the Maxwell stress with fixed electrovac metric and obtains exactly one. This is a consistency test of the retained minimal normalization, not a determination of G, electric charge, or the electromagnetic action from the formation states. The fields of the spherical formation runs are not electrically charged by this control; a nonminimal curvature–photon interaction is not included in the electrovac check. See [the known electrovac exterior in isotropic coordinates](https://inspirehep.net/files/0ec929e12758f2ed730028c59b9a07c4).

## Leading slip from the actual weak-field matter

Let φ be the common leading Newtonian potential. Under slow-motion weak-gravity counting the trace-free equation to its first nonzero order in Δ gives Q_s(r)=8πG a²Π+2(φ')² and (Δ'/r)'=Q_s/r. The square of the Newtonian gradient must be included at the same order as the matter stress. Adopting Ψ=Φ as an *exact* solution loses this term even in vacuum. This calculation is in the log convention above; at second order it cannot be transferred unchanged to the linear-coordinate potentials.

For a positive radial collisionless label element dM (normalized to homogeneous r²dr) with canonical p, its physical speed in c=1 units is |p|/a. Summing streams, including their bulk motion, gives 8πG a²Π dr/r = Σ(C_s/a³) p² dM / r³, C_s=8πG a³ρ̄_s. No caustic density needs dividing by a vanishing trajectory Jacobian. For the coherent heavy field, averaging the retained real scalar over its fast cycle gives Π_h=ρ̄_h |∂rψ|²/(m²a²) at envelope order. It includes both amplitude gradient and phase current, without assigning an ad hoc wave velocity to a density node. Interactions or additional independently anisotropic fields would add sources, not vanish by definition.

Fix three radii r₁=0.10, r₂=0.20, r₃=0.35 comoving Mpc, A=r₂²−r₁², B=r₃²−r₂². One observable that does **not** require specifying Δ or its gradient outside the shell is

    S₃ = A [(Δ₃−Δ₂)/B − (Δ₂−Δ₁)/A]
       = (A/2) ∫_{r₁}^{r₃} T(r) Q_s(r) dr/r,
    T(r≤r₂)=(r²−r₁²)/A,     T(r≥r₂)=(r₃²−r²)/B.

This follows by twice integrating the differential equation. Both homogeneous solutions 1 and r² cancel. S₃ is dimensionless, independent of exterior slip data at this order, and has a definite positive sign for the present radial preparations unless gradients and stresses vanish on its support. It is **not** an absolute two-clock slip, a gauge-independent claim for arbitrary slicing, or a measured gravitational-lensing signal. Its three-radius Eulerian field combination is a concrete target for an independent relativistic solver. A slip correction to the equal-arm optical observable would also need the lapse and matching data not fixed by S₃ alone.

[Solver and electrovac checks](evidence-001.zip) (archive member: `slip.py`) · direct source contributions (not bundled here) · [electrovac flux differences](evidence-001.zip) (archive member: `tracefree-electrovac-controls.csv`). Each numerical evaluation checks the compact integral against successive potential differences reconstructed with a common integration slope. The two epochs are explicitly the archived start and end of the formed histories, not the much shorter pulse window.

