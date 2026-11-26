> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Why a projected gravity result can fail far outside the origin

## Identify the growing mode without fitting the history

The old, unregularized centre already had a diagnosed instability; see the [q=32 tests](../mts-late-tide-refinement/RESULTS.md). That is not a new finding here. The new question is whether its tested **trace-preserving six-cell replacement**, used for the present q=1024 evolution, removes it over the longer light path. Form the frozen angular-order-two geometry block on the *actual* zero-host launch with coordinate vector (δg,hδK), cell time t/h, and the eight retained metric/curvature entries; h is the central mesh spacing. Apply each basis perturbation to the production equations (not a regression on the history). Use two independent patch radii and a random superposition to check extraction. The zero extension at the far side of this small spectral patch is for the tangent test only; the actual trajectories retain the full domain.

The dominant original rate is **0.748514/h** on two grids and on both 24- and 40-cell patches. More than 99% of its squared right-eigenvector norm lies within six cells. On the 320-cell/Mpc evolution the left-eigenvector projection grows by about 1.196 million in the final quarter, on both the measured wave and cold trajectories; the launch operator predicts the amplification within 0.0124%. ADM has a smaller positive rate **0.382746/h**, concentrated within nine cells: its clean fine-grid detector result at this clock does not remove that mode. These two tangent rates are not a property of astronomical wave densities. An independent application of the Hamiltonian and both momentum constraints rejects the growing directions, whereas a regular homogeneous static shear has zero or negligible response. See mechanism code and packets named origin_mode, mode-*, and centre-mode-constraints.

The proper detector integrates radial length from the centre. Decompose its *same full reading*, not a substitute observer, into (i) the changing local field on the starting ruler, (ii) the local metric weight change, and (iii) the remaining movement of the proper distance. For positive original host, 320 cells/Mpc, full time, 0.15 window, the last term is −2.578135832629 × 10¹² ppm while the first minus prediction and the local weight are +138234 and −79533 ppm (Ricci). These large cancellations are why freezing the ruler is not a legitimate cure. Meanwhile the maximum signed metric quadrupole increment at radii 0.65–1.6 Mpc is only 1.56 × 10⁻¹⁵ even as the first grid cell reaches 0.207 on the wave branch and 0.456 on cold. Such late central fields are outside a small-perturbation interpretation. Report the failure, not a physical growing halo.

## Can better initial data alone fix it?

Let A be the scaled frozen geometry block, C the derivative of the three constraints, and l the left eigenvector of the growing mode. Find the unit radial-mass-norm vector in ker(C) maximizing |l*x| with support in cells 8–31 of the 40-cell patch. The vector is zero around the origin and outside the patch; include all the constraint stencils that can see it. In these scaled units the resulting initial constraint norm is 9.22 × 10⁻¹⁵ or smaller but the derivative norm is **0.01514**. The full matter-plus-geometry RHS gives the same rate to about 1.1 × 10⁻¹² relative using independent symmetric evaluations of the constraints at the launch. This is an explicit semidiscrete witness, not a claim that an arbitrary eigenvector represents valid initial data. It locates an error in *transport* of constraints, not merely preparation. The global Hamiltonian need not be projected out of the detector.

## An identity which specifies a repair, not a fitted damping rate

For the flat geodesic principal equations, H=∂ᵢ∂ⱼgᵢⱼ−Δ tr(g), Mᵢ=∂ʲKᵢⱼ−∂ᵢK, and ġ=−2K in Cartesian components. Commuting the derivatives gives **Ḣ=−2 div M**. In the retained spherical quadrupole variables the kinematic map V from (K,s,c,t) to (ℓ̇,ḃ,v̇,ḋ) is (−K/3−s,−K/3+s/2,−2c,−2t). Invert it on any test geometry. The radial and polar momentum operators then give, in the continuum,
```
M_r(V⁻¹g) = 2 b' + [2(b−ℓ)+3v]/r ,
M_θ(V⁻¹g) = −v'/2 + [ℓ+b+d−3v/2]/r .
R₂[g] = −2 [ (r² M_r)'/r² − 6 M_θ/r ]
       = −4 b''+(4ℓ'−12b'−12v')/r+(16ℓ+8b+12d−24v)/r² .
```
Separately discretizing the expanded expressions need not preserve this identity. In flat vacuum take **zero metric perturbation** and a compactly supported extrinsic-curvature perturbation satisfying both discrete momentum constraints to 9.1 × 10⁻¹⁶. The current discrete H has dimensionless time derivative 2.204 on this unit witness (at linear order), verified against the independent Decimal constraint evaluator. Since flat H is independent of K at linear order, altering **only K̇** cannot fix Ḣ at this initial state.

Construct instead H* = −2 Div_h M_h V⁻¹. The identity is then exact for the linear flat equations. A collocated construction passes the identity but is nearly blind to an alternating two-cell perturbation. A staggered construction uses the radial face flux
```
Q_f = r_f² D_f(s−2K/3) + r_f I_f(3s−6c) ,
H* = −2 [D_b Q_f / r² − 6 M_θ / r] , applied to V⁻¹g .
```
The zero-radius flux is exactly zero with no division by r_f. On its own constrained vacuum witness the rate drops from 0.02014 (expanded curvature) to 3.50 × 10⁻¹⁵ or smaller. The lowest-spacing manufactured smooth test has relative radial-weighted error 9.48 × 10⁻¹²; the checkerboard response retains 1.00004 of the archived second derivative, versus 0.000012 for the collocated construction. These are two distinct witnesses because the momentum layouts differ. Kernels and norms are not observational error bars.

**Not yet used to alter the measured trajectories.** H* is a constructive flat scalar/kinematic identity. It is not enough to recalculate H at readout or to remove the fitted eigenmode. Next derive the companion spatial-Ricci/extrinsic-rate and compatible matter-flux identities, so both H and M propagate together on the actual curved launch; preserve the tensor-wave principal speed, check the centre spectrum and repeat the same full proper-ruler experiment before the higher-q run.
