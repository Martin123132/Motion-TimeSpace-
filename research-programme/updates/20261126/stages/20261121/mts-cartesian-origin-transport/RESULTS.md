> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Can the archived central quadrupole be evolved as a smooth Cartesian tensor?

21 November 2026, private. This is a local-GR formation test, separate from the fixed-occupation LMC forces (not bundled here). Outcome: the regular evolution passes a smooth nonzero-shear control, but simply applying it to the saved samples understates the true inner launch acceleration by more than a factor of ten. A specific radial power in the *input representation* explains why. Retain the prior physical trajectories and aperture measurements.

## What the new variables measure

Take s=r², a constant trace-free matrix Q=diag(−1/2,−1/2,1), y=xᵀQx and u=Qx. On the spherical spatial metric γ=g(I+m xxᵀ), g=exp(2b₀), evolve the **covariant** quadrupole metric and extrinsic curvature perturbations divided by g. Each has coefficients (a,b,c,d) in

    a Q + b(xuᵀ+uxᵀ) + c y I + d y xxᵀ.

A smooth field can have nonzero a(0). The radial, tangential-average, mixed and tangential-shear harmonic coefficients are a+s(2b+c+s d), −a/2+s c, (a+s b)/2, a/2. Thus rr−avg−4cross+tf=s²d must be O(r⁴) for bounded d; separate O(r²) differences are insufficient. The mixed angular coefficient here multiplies the polar derivative of the scalar harmonic. The test concerns the signed host-minus-zero response, not a demand that its momentum equal the matter current by construction.

The [curvature generator](evidence-001.zip) (archive member: `cartesian_ricci.py`) has no pole at s=0 for smooth inputs and positive metric. An [independent direct 3D calculation](evidence-001.zip) (archive member: `cartesian_witness.py`) differentiates an explicit curved polynomial metric in Cartesian coordinates. On five sites including the origin, maximum absolute component errors were 2.23e-16 for linear Ricci and 1.22e-17 for the ADM extrinsic-curvature products. This is an operator check, not a spacetime solution.

[Driven evolution](evidence-001.zip) (archive member: `centre_evolution.py`): evolve h'=-2p, p'=R₁(h)+f on flat space at 32 and 64 radial cells. The manufactured metric shape is H=Q+s² y I. Independently, R₁(fI)=−(Hess(f)+I Δf)/2 gives R₁(H) with coefficients (−s²,−4s,−20s,−4). A prescribed force (ω²H/2−R₁(H))cos(ωt) drives the oscillation; the four outer cells have the exact boundary history. In the second evolution add initial momentum T=xuᵀ+uxᵀ. Its unforced increments are h=−2tT+2t³Q/3 and p=T−t²Q, with div(p)−grad(tr p)=u. No current or constraint is inserted into a readout. Central eighth errors fell about 16-fold on each time-step halving. The deliberate momentum defect was recovered to 1.18e-12 absolute coefficient error or better. These are short, dimensionless analytic controls.

## A concrete source of the saved-grid discrepancy

We mapped **30** wave/cold launch and saved states: positive host on grids 320 and 640, negative host on 640, five epochs each. On both positive-host branches doubling resolution grows the first-cell final extrinsic quartic coefficient by about eight rather than converging. It is misleading to quote that coefficient as a divergent physical acceleration: its Cartesian tensor contribution carries four powers of radius.

At launch the verified metric has m=0 and only h=c(s)yI. Write χ₀ and χ₂ for the archived monopole and quadrupole Green potentials. Then g=(1+χ₀)⁴, c=4(χ₂/r²)/(1+χ₀). The exact quartic coefficient of covariant linear Ricci divided by g is (−2c_ss+4z c_s)/g, where z=(log g)_s/2. To avoid estimating c_ss by a smooth extrapolation through a nonsmooth input, [integrate the actual first-element polynomial](evidence-001.zip) (archive member: `green_origin.py`). If the input quadrupole source is S₂=Σ aⱼ rʲ and Δ₂χ₂=−S₂, then for U=χ₂/r²,

    U_s  = −Σ aⱼ r^(j−2) / [2(j+5)],
    U_ss = −Σ (j−2)aⱼ r^(j−4) / [4(j+5)].

Derived by integrating (r⁶ U_r)'=−r⁴ S₂ with no singular homogeneous mode; the exterior homogeneous constant drops out of these derivatives. The monopole derivatives are integrated separately and retained in the quotient. The archive’s twelve tabulated source values were converted to powers at 65 decimal digits for each of the six launches. This is the polynomial defined by the archive, **not** a measurement of the physical source arbitrarily close to r=0. Both first-cell midpoints are inside the first original quadrature node.

The signed linear source coefficient is about +1.58e-17 (wave) or +3.48e-17 (cold) on the positive host; both signs reverse on the negative host. A linear source produces U proportional to r and hence a leading quartic Ricci coefficient approximately −Δa₁/(3r³) in the weak metric. On the actual first cells this simple prediction differs from the exact source-derived Ricci by 0.15% on the coarse grid and 0.038% on the fine grid. It contributes O(r) to the full tensor at these radii, **not** an infinite curvature there. Tiny lower polynomial powers are retained in the calculation; this is not an asymptotic statement all the way to zero.

The complete source-derived first-cell acceleration is 70.19–70.26% of the inherited discrete launch rate with the same sign in all six runs. The order-four/order-six smooth-sample derivative would return only 7.7%/9.2% of the source-derived rate. On the old trajectories a constant launch-rate estimate predicts the measured final first-cell change in p_d within 3.03%; this is a retrospective mechanism check, not a held-out forecast. Results: input powers and signed forces (not bundled here), [operator/launch/endpoint comparison](evidence-001.zip) (archive member: `launch-source-comparison.csv`), untouched-history coefficients (not bundled here).

**Next experiment:** evaluate the upstream quadrupole source terms themselves near the origin (including how the matter and spatial interpolants are prepared), not just the archived polynomial extrapolated below its first node. Determine whether the O(r) term belongs to the physical preparation or its radial representation. If the actual source is smooth, derive its regular first element from those inputs and compare to original nodes and the prior proper-aperture tides; if not, use a sourced nonsmooth particular solution plus a regular remainder. Do not set a₁ or the central shear to zero to manufacture agreement. No new self-consistent curved trajectory or improved proper-ruler score is inferred here.
