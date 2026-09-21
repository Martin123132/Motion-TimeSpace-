# Source-fitted crossing action and fine-phase robustness

Private continuation of `DERIVATION-20260915-sparse-live-resolution-and-phase-tests.md`.
Turn started 2026-09-15T17:19:05Z; safe check-in due 21:19:05Z.

## What is new, and what is not being claimed

Two separate experiments must not be conflated:

1. The **unchanged live-gravity benchmark** is tested at nearby fine counts 1031 and 1037, against the previously saved 1025 and independent degree-512 continuum solution. This varies source-cell phase and spacing together, not phase at exactly fixed spacing. Counts were selected before their force outcomes. All old accuracy gates and failures remain.
2. A **new source-fitted variational discretization** is constructed to remove the old fixed-grid source-crossing obstruction. Its continuum coordinate transformation, canonical momentum, source force and label-density pushforward are derived below. Its first evolution tests are on a prescribed flat metric, not the coupled live metric. These are additional controls, not replacements for the original live preparation.

This is progress in the conditional spherical GR bridge, not a full GR limit, a unique parent action, a black-hole extension, a fitted observation, or derived physical MTS coefficients. The original finite cut action and every original Gram row remain preserved in immutable evidence. The new finite Gram extension is specified and tested, not claimed to be uniquely mandated by the parent theory.

## 1. Why the old source-cell chart needs replacing

If a fixed-grid value q at distance delta from the zero-trace source is retained while delta tends to zero, the affine cut-cell gradient is q/delta and its spatial energy is asymptotically C_b q^2/(2 delta). Bounded energy only requires q=O(sqrt(delta)); a bounded one-sided gradient requires the stronger q=O(delta). Neither arbitrary coordinate continuation across a node nor deletion of that node is a derived conservative transfer rule.

This is an obstruction of that finite-element chart, not proof of a physical singularity or failure of MTS. Instead of projecting away energy at a crossing, keep the source at a fixed reference anchor and let the mesh move.

## 2. Exact continuum pullback

Let a < b_star < d be fixed, with reference coordinate r. For physical source b(t), use

    R(r,b) = a + (b-a)(r-a)/(b_star-a),          r < b_star,
    R(r,b) = d - (d-b)(d-r)/(d-b_star),          r > b_star.

Write J=R_r and k=R_b. Then J>0 while a<b<d; k=0 at the exterior endpoints and k=1 at the source. The geometric conservation identity is J_t=partial_r(k V), V=dot b. No denominator vanishes when b crosses an OLD grid node. Endpoint collision remains outside this chart.

For phi_tilde(t,r)=phi(t,R(t,r)), define H_ref=partial_r phi_tilde. The physical derivatives are

    H = H_ref/J,
    W = partial_t phi_tilde - k V H_ref/J.

With A=R^2/(N U), C=R^2 N U and ell=sqrt(N_b^2-V^2/U_b^2), the exact pulled action is

    L = (1/2) integral dr [ A J W^2 - (C/J) H_ref^2 ] - S ell.

The wave characteristics in reference coordinates move at (±N U-k V)/J, hence their physical speeds remain ±N U. This is a coordinate change, not a modified light cone.

Moving-reference formulations are established numerical machinery: [Guo and Chan, arXiv:2009.12768](https://arxiv.org/abs/2009.12768) map wave equations to a fixed reference domain. That paper supplies context only; its DG stability theorem is **not** imported as a theorem for this MTS action. The identities here follow directly from the displayed change of variables.

## 3. The canonical shift is global and cannot be discarded

The pulled momentum density is Pi=A J W. Differentiation with respect to V gives

    zeta = - integral dr A k H_ref W
         = - integral dr k H Pi,
    P_b = p_s + zeta,
    p_s = S V/(U_b^2 ell).

The same relation follows from the canonical one-form:

    integral dR pi delta(phi) + p_s delta b
    = integral dr Pi delta(phi_tilde)
      + [p_s - integral dr k H Pi] delta b.

Unlike the old localized cut-cell momentum, this zeta need not be O(h). It must remain in both source acceleration and energy/current accounting. At continuum level the shift p_s=P_b+integral k H Pi is metric-independent at fixed pulled canonical variables. This statement is not an exact formula for inversion of a finite consistent mass matrix; the finite implementation retains its full banded field/source Schur solve.

The physical Hamiltonian on a static prescribed metric is

    H_total = (1/2) integral dr [ A J W^2 + (C/J) H_ref^2 ] + S N_b^2/ell.

Its positivity and the velocity-Hessian Schur lower bound follow from the positive wave kinetic Gram form plus the positive proper-source inertia S N_b^2/(U_b^2 ell^3), when N,U,J,S are positive and the source is timelike. This is not a parent ghost-freedom theorem in arbitrary backgrounds.

## 4. Source pressure follows from the same variation

Define the physical off-shell wave residual E=partial_R(C H)-partial_t(A W). At fixed pulled field a source variation induces delta(phi)=-k H delta b. The source variational identity, including both moving sides and the zero-trace condition W_±+V H_±=0, is

    partial_b L_wave - d_t(partial_V L_wave)
      = (1/2)(C_b-A_b V^2)(H_-^2-H_+^2)
        - integral dR k H E.

The exterior endpoint term vanishes because k=0 there. On the continuum scalar equation E=0 this is the same physical moving-boundary pressure already derived for the fixed-grid route. Off shell, or at finite spatial resolution, the volume term must not be silently dropped.

The reference-coordinate wave equation is

    partial_t(A J W) = partial_r(C H_ref/J + k V A W).

For a static metric the physical wave-energy identity becomes

    partial_t(J epsilon) = partial_r(C W H + k V epsilon),
    epsilon=(A W^2+C H^2)/2.

Summing the two domains gives source exchange dot E_wave = -V F_pressure, apart from exterior flux; the material energy gains V F_pressure. This derives a crossing route without an energy projection, new force coefficient, or plateau axiom.

### Finite-element caveat: the interior mesh also carries shape forces

The continuum formula above assumes ordinary one-sided smooth jets away from the physical source. A piecewise-linear finite-element gradient jumps at every mesh vertex; the product H E for a distributional residual cannot simply be assigned a value there. Varying each element separately resolves the ambiguity. At an internal moving vertex x_i, with speed w_i=k_i V and continuous pulled nodal rate u_i, the shape traction is

    Q_±=(A W_±^2+C H_±^2)/2+w_i A W_± H_±
       =A u_i^2/2+(C-A w_i^2)H_±^2/2.

The u_i term cancels across a vertex of continuous metric. Hence the **exact finite regular-action source force** is

    F_h,regular = sum_internal_vertices k_i (C_i-A_i w_i^2)(H_i,-^2-H_i,+^2)/2
                  - sum_elements integral dR k H E_smooth.

The physical source is included once, with k=1 and u=0. The other terms are mesh-shape stresses, not additional physical matter species. Add the Gram shape force

    F_h,Gram = -sum_i gamma_i [ C_R(R_i) k_i/J_i - C(R_i) partial_b J_i/J_i^2 ].

This decomposition gives an independent check on L_b-dot zeta and explains why a conserved coarse trajectory can still have a wrong instantaneous force. It neither licenses dropping the interior terms nor proves their uniform continuum disappearance. The crossing precision script tests this identity on the actual evolved states, separately for reference and MTS. Physical-pressure convergence remains an independent accuracy gate.

## 5. Finite action actually implemented

`scripts/annular_source_fitted_action_20260915.py` fixes the split zero-trace basis at b_star, maps its quadrature points to R(r,b), and uses the action above. Every original higher-difference Gram row and its sampling row is retained. With the fixed reference hinge lift F=Gq-(G rho_star)(j_star q), the added potential is

    V_Gram = sum_alpha [sampling(C(R_i)/J_i)]_alpha F_alpha^2/(2 h_ref).

This is an explicit new finite extension, not an exact finite-state change of variables from the old moving-cut basis. At b=b_star and V=0, the action value and field blocks match the old action; the full source canonical momentum generally does not. Representative-dependent finite-grid corrections require convergence tests rather than declarations of coordinate invariance.

`scripts/verify_annular_source_fitted_action_20260915.py` tests source positions on both sides of, and exactly at, an old grid node; action gradients, momenta, positive Schur complement and complete Euler-Lagrange/energy identities remain finite. A manufactured off-shell history independently tests the pressure-minus-bulk identity through 1025 nodes. No weak-equation residual is confused with a physical-accuracy gate.

## 6. Derived live-geometry input, not a frozen-metric shortcut

For material label z, width w>0 and ordered source b(z), shift the reference endpoints and anchor by w z. A node with reference value r_i and fixed k_i has physical location

    R_i(z) = r_i + k_i[b(z)-b_star] + (1-k_i)w z,
    partial_z R_i = k_i partial_z b + (1-k_i)w.

Since 0<=k_i<=1, positive source ordering partial_z b>0 implies positive ordering of **every mesh node**. At the boundary the label Jacobian is w; at the source it is partial_z b. The same convex-combination identity holds between nodes. This is an actual no-folding result for this chart, conditional on source ordering, not proof that dynamics preserve that ordering forever.

Let gamma_i=[sampling^T(F^2)]_i/(2h_ref), and let w_mat(z) be the normalized material weight. The Gram metric-dual distribution is the pushforward

    g(R) = sum_i integral dz w_mat(z) gamma_i(z)/J_i(z) delta(R-R_i(z))
         = sum_i w_mat(z_i) gamma_i(z_i) / [J_i(z_i) partial_z R_i(z_i)].

The inverse label z_i exists only on that node's support. The old substitution of constant width w in the denominator is generally wrong after the source-fitted deformation. Variation of the regular action at fixed physical metric gives

    delta_N L_wave = - integral dr J R^2 U D_regular delta N(R),
    delta_U L_wave = - integral dr J R^2 N D_regular delta U(R),
    D_regular=(W^2/(N^2 U^2)+H^2)/2.

Average those physical densities over labels **before** forming the nonlinear radial metric equations. With D=<D_regular>+g and rho_s=w_mat(z_s)/partial_z b(z_s), the inherited conditional spherical constraints therefore have the same form,

    mu_R = kappa R^2 U^2 D + kappa U S N rho_s/ell,
    (ln N)_R = mu/(R^2 U^2) + kappa R D
                 + kappa S V^2 rho_s/(R N U^3 ell).

There is also a new whole-mesh atom current. With c_i=gamma_i/J_i and dot R_i=k_i V(z), distributional differentiation gives

    partial_t g + partial_R(sum_i integral dz w_mat c_i dot R_i delta(R-R_i))
      = sum_i integral dz w_mat dot c_i delta(R-R_i).

`scripts/derive_annular_source_fitted_live_pullback_20260915.py` checks the exact Jacobians and metric variations, independent real finite-difference action derivatives, three weak pushforward moments and the moving-atom transport identity. This supplies the density/current ingredients for the next live implementation. It does **not** yet qualify the full coupled Einstein mass current, a live crossing evolution, or the finite source-fitted radial/canonical fixed point.

## 7. Numerical results

### Unchanged live-gravity phase test

The paired1031/1037 run completes26 checks, with all four cases passing the same physical-accuracy gates used at1025. The source, duration, preparation, width, coupling, material-label degree, radial degree and independent512 oracle remain unchanged.

| Nodes | Initial source-cell phase | Maximum field error, both branches | Reference final force error | MTS final force error | Strict field/force/source-clock |
| --- | ---: | ---: | ---: | ---: | --- |
| 1025, inherited | .2000 | .487830% | .0313221% | .0531727% | Both pass |
| 1031, new | .3125 | .484988% | .219787% | .118576% | Both pass |
| 1037, new | .4250 | .482180% | .190130% | .142534% | Both pass |

The new absolute force errors are6.35765e-8/3.42997e-8 at1031 and5.49979e-8/4.12301e-8 at1037 (reference/MTS), all below2e-7. Maximum new source-position error is1.055e-10, velocity error7.753e-9 and clock error2.634e-11. Radial/canonical residuals stay below1.879e-10; exterior-mass drift is at most1.111e-16. Minimum source-cell margin is.1884359, above the unchanged.15 gate.

Thus the original passing live result is not confined to the single1025 mesh placement. This remains a test of three nearby fine grids: spacings also change slightly, errors are sampled at five times, and the result is not an all-phase or unrestricted convergence theorem. Earlier coarse force failures remain. The independent temporal-current controls from1025 are inherited; this turn does not pretend to have repeated those full controls at every new phase.

### New fixed-background crossing control

Use the original compact-quintic profile shape and amplitude .01, but explicitly ADD the flat-background control with initial source velocity .06, S=.03 and duration .4. This is not the original width-.02 live-gravity experiment. The source travels from 6.03 to about 6.05333665. All quantities below use the benchmark's internal units, not SI observational bounds. Both methods receive the same initial data, oracle and gates.

| Nodes | Reference maximum field error | MTS maximum field error | Reference final force error | MTS final force error |
| --- | ---: | ---: | ---: | ---: |
| 33 | 19.0155% | 26.6111% | 115.720% | 133.168% |
| 65 | 7.77390% | 8.69029% | 7.86275% | 14.9417% |
| 129 | 3.89668% | 3.89668% | 1.19814% | 10.1875% |
| 257 | 1.94958% | 1.94958% | 0.854088% | 1.30667% |
| 513 | 0.974954% | 0.974954% | 0.198933% | 0.252064% |
| 1025 | 0.487498% | 0.487498% | 0.0687073% | 0.0903434% |

These are the revised comparisons to the qualified degree-512 characteristic oracle, not the initially underresolved degree-256 oracle. Each maximum is sampled at nine times, not a certified time supremum. At 1025:

- The source passes the locations of **15 old fixed-grid nodes**, with no reinitialization, node deletion or energy projection. Minimum mapping Jacobian is about .969693; the source remains timelike.
- Both branches pass the unchanged .5% field gate and source/velocity/clock gates. Maximum source-position error is <=1.867e-8, velocity error <=5.894e-7 and proper-clock error <=1.110e-9 against the oracle.
- The final forces are reference -0.001712733925676227 and MTS -0.001712363102469313, against -0.001713911508494131. Absolute errors are **1.17758e-6 and 1.54841e-6**. Both pass the 2% relative-force criterion but **fail the 2e-7 absolute-force criterion**; therefore both strict force flags remain false. No coarse grid is promoted by its excellent energy conservation.
- Energy relative drift is <=4.311e-16 at the saved fine states; this is a floating-point diagnostic, not a rigorous error bound. Coarse MTS drift is larger but still <1.3e-12. Maximum sampled coupled Euler-Lagrange residual across these crossing runs is about1.12e-16.
- The independent degree384/512 field-vector difference is at most2.513e-5 relative; maximum force difference is5.992e-8. Degree192/256 had a5.400e-7 force difference and remains recorded as underresolved. Resolution differences are empirical estimates, not certified continuum-error bounds.
- Halving the 129 time step changes the complete sampled state by at most1.396e-12 reference and6.502e-11 MTS. It does not fix spatial underresolution. Final fine-field quadrature and independent force decomposition checks pass.

The finite force decomposition is particularly informative. At MTS1025 the physical trace pressure is -0.001711117405047039, while the interior mesh-pressure contribution is +0.001604000970529318 and the smooth bulk-residual projection is +0.001605246661652654. Their small difference, plus Gram shape force -6.299e-12, gives the full canonical force. Simply using the trace pressure, or omitting dot zeta, is not the same finite theory: dot zeta is about0.001032800033. The independently derived element-boundary identity reproduces all twelve evolved reference/MTS force cases to the2e-11 check, with actual discrepancies far smaller.

### Derived measures and action checks

The source-fitted action suite passes42 checks. At1025 the manufactured off-shell pressure-minus-bulk error is6.744e-11 reference and6.739e-11 MTS, decreasing roughly quadratically in the tested smooth history. This is not a convergence theorem for all evolving histories.

The live-pullback derivation passes11 checks. Its three weak Gram-density moments agree between label-space and physical-space integration to <3e-15 relative. Reusing the old constant-width denominator gives about **8.36%** error in this deliberately nonuniform-label control. The moving-atom transport identity also passes; omitting the transport term gives a detectable1.340e-9 weak-current error. These results identify the precise live-coupling inputs to implement rather than concealing a Jacobian or current assumption.

Crossing evolution passes31 coarse and31 fine implementation/conservation checks, with all physical-accuracy failures retained. Independent crossing precision adds24 checks, including the exact finite-element force decomposition. These check counts measure reproducibility coverage, not the number of new physics results or proximity to a complete theory.

## 8. Next decisive task

The remaining strict fixed-background force-error gate is now a quantified numerical target, not an unspecified coupling gap. First test one additional paired resolution or a justified higher-order field representation against the unchanged512 oracle, retaining the derived interior-mesh/bulk force decomposition and the original failures. Do not loosen the absolute gate or substitute trace pressure merely to obtain a pass.

Then implement the source-fitted continuously averaged density and radial/canonical fixed point using the derived inverse node-label maps, not a constant-width substitution. Retain the whole-mesh atom current and global field-carried source momentum. First check low-resolution equivalence to the action variation and independent temporal mass current, then evolve an actual crossing against a source-fitted continuum oracle with the same physical preparation. No horizon or full-parent claim follows from that milestone alone.

## Evidence and preservation

Existing seal: `source-intake/navier-stokes/20260914/annular-sparse-live-resolution-final-integrity.json`.
Live phase run: `source-intake/navier-stokes/20260914/annular-sparse-live-nearby-fine-phase-attempt01/status.json`.
Action qualification: `source-intake/navier-stokes/20260914/annular-source-fitted-action-qualification-attempt01/status.json`.
Crossing control: `source-intake/navier-stokes/20260914/annular-source-fitted-crossing-attempt01/status.json`.
Fine crossing: `source-intake/navier-stokes/20260914/annular-source-fitted-fine-crossing-attempt01/status.json`.
Independent crossing precision: `source-intake/navier-stokes/20260914/annular-source-fitted-crossing-precision-attempt01/status.json`.
Precision/decomposition implementation: `scripts/verify_annular_source_fitted_crossing_precision_20260915.py`.
Live pullback: `source-intake/navier-stokes/20260914/annular-source-fitted-live-pullback-attempt01/status.json`.

All work is private inside post-checkpoint-work. No GitHub action, no subagents and no edits to formalization-workbench. At most two own one-core BelowNormal workers. Existing failed accuracy gates and the five inherited failed attempts remain part of the evidence, not deleted by this extension.

All numerical jobs are finished as of2026-09-15T20:10:52Z, within the four-hour window. The combined new suites contain165 successful implementation/derivation/control checks, with the failed crossing accuracy flags expressly retained. Integrity sealing is performed by `scripts/seal_annular_source_fitted_crossing_20260915.py`; its separate result records the actual file/hash and protected-folder checks.
