# Common source two-jet from retained exterior initial data

Private continuation, 2026-09-13. Conditional finite-width candidate calculation, not a physical MTS prediction or an evolved spacetime.

## 1. Question and scope

The preceding source-coupled construction passed the tested C0, C1 and C2 constraints but required different inner mass accelerations in GR and the metric-Gram MTS candidate. Those accelerations cannot silently be called the same prescribed boundary history.

This step asks a narrower, constructive question: can the retained exterior scalar initial data prepare the same inner mass value, rate and acceleration, while keeping the old initial interior fields and the sourced outer data? The two adjustable numbers below are initial-state amplitudes, not additional action coefficients. No constraint residual is used to choose them.

Predecessor: `DERIVATION-20260913-source-coupled-second-jet-and-C2-propagation.md`.

## 2. Do not solve a physical mismatch by changing the clock

Write mu_1 and mu_2 for coordinate-time derivatives at the initial slice, and L=N_1/N. At a fixed-radius cut with initial gravitational momentum P=0, d_tau=N^(-1)d_t initially and

```text
d_tau^2 mu = (mu_2-L mu_1)/N^2.
```

For clarity fix the direction of the relabelling: the old time is T=t+zeta(R)t^2/2+O(t^3), with the fields expressed in the new t coordinate. At the initial slice,

```text
L_new = L+zeta,
mu_2,new = mu_2+zeta mu_1,
K_1,new = K_1+2 zeta K,
P_2,new = P_2+zeta P_1-N zeta_R/(kappa U).
```

Thus the proper mass acceleration does not change. These are local jet transformations, not a global gauge-fixing theorem. The current and mass transformation are checked numerically using the actual second-transport construction in both primary branches; the momentum transformation also follows algebraically from the derived c_tt and P_2 laws. A non-adopted zeta=0.3 h00 control tests this explicitly.

For the accepted preparations, impose the same declared inner clock convention **L_inner=0**, before searching the physical exterior amplitudes. Preserve the inherited outer L value and the derived cut slopes

```text
L_R|cut = mu_1/(R^2 U^4)+kappa epsilon_1/R,
```

which are necessary for P_2=0 at cuts where P_1=0. With x=(R-R_inner)/(R_outer-R_inner), h00=1-3x^2+2x^3, subtract L_outer*h00 from the predecessor's extension. The lift has zero derivative at both cuts; it changes the inner value without changing those slopes or the outer clock value. This is a declared clock extension, not a uniquely derived lapse history.

Now the target mu_2,inner=0 is also zero proper inner mass acceleration. The initial inner lapses remain geometry-derived; they are not asserted identical across theories. Matching the coordinate first rate therefore does not assert an identical proper first rate.

## 3. The common boundary data and their provenance

The old source snapshots and prepared collars own the following values, in the existing pilot's numerical normalization:

| Datum at the initial slice | Value | Ownership |
| --- | ---: | --- |
| Inner mu | 1.0000072347033995 | Inherited source mass |
| Inner mu_1 | 0.00033578281226508903 | Inherited source drive |
| Outer scalar q=chi_1 | 0.015344562303521506 | Inherited scalar drive |
| Outer scalar q_1=chi_2 | 0.05577372038655635 | Inherited driven acceleration |
| Outer C_clock=N/U | 1.0000262973362133 | Inherited affine clock |
| Outer (C_clock)_1 | 0.00025872745044339796 | Inherited affine clock |
| Inner mu_2 | 0 | **New declared trial target**, not an archival measurement |
| Inner L | 0 | **New declared common clock convention** |

Initial P and derived P_1/P_2 vanish at the original physical cuts. The retained source apparatus, its initial energy E0=0.001, whole-factor scalar action, Gram coefficients and spacing are unchanged. The earlier two interior momentum-lift coefficients are held at their saved source-prepared values, not refitted.

The mass data define an affine trial boundary history through second order only. This calculation does not establish that an affine history exists on a finite interval. Similarly, the common outer scalar entries do not assert that the entire proper-clock driving functions or the exterior microscopic states coincide between branches.

The existing affine C_clock history does additionally own (C_clock)_2=0. Since N=C_clock U and P=P_1=0 at the cut,

```text
U_1 = -mu_1/(R U),
U_2 = -mu_2/(R U)-mu_1^2/(R^2 U^3),
N_2,outer = 2 (C_clock)_1 U_1+C_clock U_2.
```

The verifier calculates this outer lapse second derivative for every prepared case and checks that the reconstructed (C_clock)_2 vanishes. It does not fill an interior N_2 profile or establish a complete gravitational clock history. The inherited affine-clock owner is `scripts/derive_annular_parent_root_residence_20260910.py`.

## 4. A physical two-mode preparation, strictly outside the old cut

Let z be the translation coordinate of the finite-width layer. Change only the leftmost scalar momentum at negative translations:

```text
b0(z) = 256^2 z^4(z+1/2)^4,       -1/2 < z < 0,
b1(z) = b0(z)(4z+1),             -1/2 < z < 0,
b0=b1=0 elsewhere,
delta p_left(z) = a0 b0(z)+a1 b1(z).
```

The extended modes and their first three derivatives vanish at both endpoints. They are piecewise C3, not globally analytic or C-infinity. They alter neither the scalar value nor any other node's momentum. In particular they vanish throughout the old physical annulus and at its left cut.

This does change exterior kinetic energy. Re-solve the mass, lapse and transport preparation rather than freezing the metric. In the left exterior half-band the source reservoir density is zero, so

```text
mu_R + (2 kappa epsilon/R) mu = kappa epsilon.
```

For fixed new epsilon, a change in the lower-support mass seed propagates to the old cut by the integrating factor exp[-integral(2 kappa epsilon/R)dR]. Adjust that seed by the exact inverse response to preserve the inherited mu(R_inner). This seed adjustment is part of the preparation and is recorded separately; adding exterior energy is not free. With the old interior scalar data and old inner mass retained, the initial interior mass solution, configured lapse, U, epsilon and P_1 are unchanged to numerical accuracy. The whole first time-derivative profile is **not** claimed unchanged: the crossing currents are precisely what the exterior modes alter.

The changed auxiliary momentum is an actual initial condition. It is not a new fundamental field, an adjustable Newton constant, a fitted local force, or a prescribed C2 cancellation.

## 5. Why there is a useful second response: the flat-link calculation

An explanatory special case is one link on a fixed, constant positive background, with B=(-1,1), S=(1/2,1/2), J=1, C=R^2 N U, and A=chi_right-chi_left. The factor formula gives the oriented crossing current

```text
K = A [C(q_right-q_left)/2-C q_right]/h
  = -C A(q_right+q_left)/(2h).

mu_1 = kappa R^2 U^2 A(q_right+q_left)/(2h).

mu_2 = kappa R^2 U^2/(2h)
       * [q_right^2-q_left^2+A(q_1,right+q_1,left)].
```

The last line freezes background coefficients and differentiates the scalar link only; it is not the full coupled gravity equation. If chi and the initial scalar force are fixed, the sum of velocities controls the first response, while the velocity-square difference gives a distinct second response. For normalized layer averaging and constant baseline q_left, a zero-mean delta q_left preserves the averaged first response and gives

```text
Delta <mu_2> = -kappa R^2 U^2/(2h) * <(delta q_left)^2>.
```

For nonconstant baseline q_left the linear cross term -2<q_left delta q_left> must also be retained. These restrictions matter. The curved, varying-coefficient and Gram cases need not obey this simple variance formula; the actual runner uses the full transported force/current, metric and apparatus derivatives. The verifier derives the flat-link current from its factor weights and checks its differentiated square-difference and cross term symbolically.

## 6. Full matching and independent constraint checks

The full mass-acceleration formula used is the predecessor's action-derived result,

```text
mu_2 = -kappa U/N [K_1-(L+mu_1/(R U^2))K]
       -kappa^2 R U^6 P_1^2.
```

K_1 includes the differentiated inverse-time transport, the second transport primitive, moving anchors and live scalar/source response. The apparently compact formula already uses the initial lapse constraint to combine the gravity, scalar and apparatus Hessian terms; it is not permission to omit the apparatus.

The search has two physical controls and two data to match:

1. For each a1, solve a0 so the inner mu_1 remains the inherited drive.
2. Vary a1 to meet the declared mu_2,inner=0 at the fixed inner L=0.

The positive branch is searched on the declared sequence 0.25, 0.5, 1, 2, 4, 8, 16. Roots outside it are not silently accepted. C0, C1 and C2 are evaluated **after** matching, at the unchanged absolute gate 1e-10 in the pilot's normalization. Passing these dependent constraint identities checks implementation consistency; it is not independent observational evidence for the theory.

Because the exterior profiles are only piecewise C3, current interpolation is split at z=0 rather than globally raising polynomial order across the regularity break. The two halves each use degree 56 for the matching calculation; the second-transport primitive uses degree 36 on the inherited radial partition, which includes both old cuts and all layer centers. C2 uses quadratures 24 and 40. Verification raises the fits to 64/44 with the same saved amplitudes, checks direct crossing-current integration and evaluates primary-case C2 at quadrature 48.

A finite-difference two-by-two response matrix is measured at each primary matched preparation by perturbing each exterior amplitude without rematching. Its numerically resolved rank tests whether the two responses are locally distinct. It is not an interval-certified inverse-function or uniqueness proof.

## 7. Results and interpretation

The main matrix completed all six preparations, with **33 main checks passed**. Here h=1/64 and all rows use the retained right reservoir E0=0.001. The previous E0=0.002 control is not repeated in this matching matrix; no claim of general reservoir-energy robustness follows.

| Branch | Layer | a0 | a1 | Absolute inner mu_2 error | Maximum tested absolute C2 |
| --- | --- | ---: | ---: | ---: | ---: |
| GR | beta22, h/2 | -0.561340135 | 8.650977804 | 3.53e-17 | 5.10e-14 |
| MTS metric-Gram | beta22, h/2 | -0.489585794 | 7.551271863 | 2.01e-12 | 4.59e-14 |
| GR | beta22, h/4 | -0.552724481 | 8.679969775 | 3.21e-18 | 6.10e-14 |
| MTS metric-Gram | beta22, h/4 | -0.482498341 | 7.580189912 | 1.41e-12 | 6.18e-14 |
| GR | beta23, h/2 | -0.292704664 | 7.964898066 | 4.37e-13 | 6.37e-14 |
| MTS metric-Gram | beta23, h/2 | -0.257443232 | 7.015401235 | 7.54e-16 | 6.03e-14 |

Across the matrix, maximum C0=1.958e-13, C1=1.189e-16 and C2=6.372e-14; all are below the unchanged 1e-10 gate. The maximum combined boundary-data error is 2.011e-12 and maximum proper inner mass-acceleration error is 3.049e-12. The tested initial interior field change is at most 1.599e-14. The full-precision saved amplitudes, not the rounded table, are required for replay.

This is not a small perturbation claim: the maximum exterior auxiliary-momentum changes range from 1.624 to 2.165. The increase in the layer-integrated **bare scalar kinetic energy** ranges from 5.373e-5 to 8.704e-5 in the pilot's normalization, accompanied by the lower-support mass-seed adjustment. This is not an ADM energy measurement or a fitted fundamental coupling.

For the primary GR and MTS rows the original mu_2 mismatch, after declaring L_inner=0, was respectively about 0.0166881 and 0.0153455. The physical profile preparation reduces these to the errors shown above. By comparison the non-adopted clock control changes the proper acceleration by at most 8.327e-17, confirming that a clock relabelling does not resolve the physical mismatch.

The unprescribed outer responses still depend on the layer profile. For example, outer mu_2 is 0.00785308 for GR and 0.00587277 for MTS at beta22 h/2, but 0.00489279 and 0.00366950 at beta23 h/2. Matching the inner data has not eliminated regulator dependence. The primary source energy second derivatives remain negative, approximately -0.217051 and -0.173468; no apparatus lifetime or finite-time positivity follows from those Taylor coefficients.

The final integrity record supplies the separate higher-resolution checks, direct-current replay, numerical response matrices, lower-support seed changes, derived outer N_2 values and source-path hashes. Only a record with state **complete** and all checks passed establishes completion of that verification. Its immutable resume snapshot may precede the later completion line in the working resume.

## 8. What this does and does not fix

It supplies a concrete candidate mechanism for the previously mismatched second inner boundary datum: **different exterior initial wave preparations can carry the same specified macroscopic inner mass two-jet**. We no longer need to give GR and MTS different unreported inner mass accelerations in this formal comparison.

That is not a derived universal exterior state or a prediction on identical complete initial data. Matching chosen boundary data is preparation, and the chosen amplitudes must be disclosed. The finite-width regulator and right apparatus are still explicit assumptions. The source Hamiltonian's lower bound, fixed-radius support stresses, physical source realization, full GR reduction and any black-hole/astrophysical conclusion are not established here. Positive initial scalar energy and a positive initial chart do not prove stability or continued positivity.

Nor has this matched complete boundary histories: inner mass order three and higher, the full gravitational clock history, and the compatibility of the transported action on a finite time slab still require work. The outer driving function is specified in proper apparatus time, not replaced by a coordinate-time Taylor polynomial beyond the demonstrated order.

## 9. Next substantive test

Use these saved matched preparations, not another unconstrained series of amplitude fits, to build a small **history-consistent time-slab** calculation. First specify the actual clock and source histories on the slab, include the temporal endpoint work and apparatus energy, and retain the exterior fields as degrees of freedom. Test convergence of the coupled equations and boundary conditions under temporal refinement, with the same treatment for GR and MTS. A frozen scalar oscillator replay or a Taylor polynomial evaluated at nonzero time is not that test.

Do not presume that this spatially transported, history-dependent variational action is already a causal ordinary ODE. If the first slab cannot be constructed, retain this conditional initial two-jet result and report the specific interval obstruction without rebranding it as a full evolution pass. Do not select a regulator or source profile because it gives a preferred phenomenological answer.

## 10. Evidence and preservation

- Predecessor seal: `source-intake/navier-stokes/20260913/annular-source-second-jet-final-integrity.json`.
- Source-prepared coefficients: `source-intake/navier-stokes/20260913/annular-clock-reservoir-coupling-attempt01/status.json`.
- New two-mode preparation and piecewise currents: `scripts/annular_common_source_history_20260913.py`.
- Executed matching and holdout matrix: `scripts/derive_annular_common_source_history_20260913.py`.
- Trials, matched arrays and hashes: `source-intake/navier-stokes/20260913/annular-common-source-history-attempt01/status.json`.
- Independent verification: `scripts/verify_annular_common_source_history_20260913.py`.
- Completion authority: `source-intake/navier-stokes/20260913/annular-common-source-history-final-integrity.json`.

All predecessor evidence and executed source files remain immutable. Private local work only: no GitHub, no subagents, one below-normal-priority single-core worker. The protected original workbench check is an mtime scan since 2026-09-13T18:43:05Z, not a pre-turn content-hash comparison. The final integrity record snapshots the mutable resume before any later completion line.
