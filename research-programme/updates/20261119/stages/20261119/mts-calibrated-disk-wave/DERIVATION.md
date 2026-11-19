# One occupation calibration; two independently calculable gravitational observables

Use the retained Newtonian, stationary weak-field sector, not an empirical rotation-curve response. In specific-energy units its same-node, even, axisymmetric wave solves
`[-(ħ/m_h)² ∇²/2 + Φ_w + η Φ_disk+bulge + Φ_compact] f = ε f`,
where `η Φ_disk+bulge` means `η(Φ_disk + Φ_bulge)`, `∇²Φ_w=4πG M|f|²`, and `∫ |f|² d³x=1`. No particle pole or metric coupling was changed. In the numerical basis particle number is carried by the wave norm rather than multiplying a unit-normalized density twice. The same compact source and ordinary field enter both accelerations; the self-consistent shape of the wave feels both. This is a test of this positive quadratic subfamily and state, not a deduction that every galactic environment selects it.

Let the inward force be positive, define `S(R)=R(g_bar + g_X)` in the plane, and put `u=ln M`. The outer constraint fixes `S_*(u,η)=V_*²`. Within the continued stationary branch:
- `du/dη = -(∂η S_*)/(∂u S_*)`, `du/dV_* = 2V_*/(∂u S_*)`. The constrained wave Hessian includes the source `2 f δf` of the perturbed Poisson potential. Just multiplying a frozen force by mass would omit that rearrangement.
- For an observable `O`, `dη O=∂η O + ∂u O du/dη`; analogously for the anchor. In midplane speed units divide the corresponding derivative of S by `2√S`. The primary root has `∂u S_*=46573.35 (km/s)²`, `du/dη=-0.580675`, `du/dV_*=0.00962052 (km/s)⁻¹`. These are local responses, not priors.
- For a halo with unit-amplitude force `g_H`, `A=[V_*²/R_*-g_bar,*]/g_H,*`. No response of the halo shape is assumed: this comparison uses a fixed 16-kpc NFW scale. Thus varying either common input recalibrates the control too. The standard unscaled halo is retained but not used as the scored competitor.
- With shared scalar anchor error `s_*`, the first-order prediction covariance is `s_*² J Jᵀ`, not eleven independent anchor errors. For the *difference* of models use `J_wave-J_NFW`. The optional residual quadratic adds the published per-bin bootstrap diagonal, assuming independent inner bins and anchor; the catalogue's actual systematic/bin covariance is not supplied. These numbers are not model evidence.

**Why similar vertical forces hide different matter distributions.** Write `g_in=∂R Φ`, `K_z=-∂z Φ`. Midplane symmetry and the cylindrical Poisson equation imply, at fixed R and h>0,
`-K_z(h)=2πG Σ(-h,h) - ∫₀ʰ [∂R(R g_in)/R] dz`.
We integrated the actual wave density (and the analytic NFW density separately), differentiated physical off-plane forces, and compared against the direct vertical force. At R=8.3 and h=1.5 kpc the nonordinary true columns are 39.18 and 30.11 solar masses/pc², but the force-equivalent columns are only 18.91 and 19.41. The radial terms are 547.89 and 289.09 (km/s)²/kpc. Neither force-equivalent number is the true mass column.

The same identity without differentiation for an annulus [a,b] gives
`G M_ann = ∫ₐᵇ R[-K_z(R,h)] dR + ∫₀ʰ [b g_in(b,z)-a g_in(a,z)] dz`.
It includes both plane-parallel faces and both cylindrical walls. Independent integration of `4π ∫ₐᵇ R dR ∫₀ʰ ρ dz` checks the Newton source and the sign of the wall term. The finite-radius source observable does not assume spherical enclosed mass or infinite-sheet geometry. Ordinary force flux is computed separately; the independent volume-density check applies to the wave and comparator halo, not to the ordinary component. The remaining model difference has a precise physical location: mostly the *radial* rather than vertical flux.

**What a circular-speed slope measures.** In an axisymmetric circular flow `A=(V/R-V')/2`, `B=-(V/R+V')/2`. They are not these simple functions of the potential in a general sample of stars. TGAS finds nonzero noncircular velocity gradients. A joint test must model tracer phase space/selection or infer azimuthally averaged gravitational forces. Do not score a stellar streaming gradient as a bare force measurement.
