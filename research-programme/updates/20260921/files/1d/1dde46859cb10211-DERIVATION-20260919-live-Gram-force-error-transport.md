# Live transport of the explicit Gram force defect

Private continuation of `DERIVATION-20260919-source-impulse-and-force-energy-control.md`. The previous integrated MTS discrepancy of 12.5718% and instantaneous discrepancy of 13.58% remain unchanged. This stage traces a force-sensitive temporal defect through the actual coupled trajectories; it does not establish the full GR limit or change the target to an averaged-force criterion.

The earlier flat-background adjoint work in `DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md` is not a ready-made adjoint for the present moving-source/live-geometry system. The result here is an exact moving-covector identity, not a completed nonlinear backward-adjoint solve. It provides a checkable error-transport target for that larger task without forming an enormous dense Jacobian.

## 1. Separate field error from moving geometry exactly

Let u_f(t),u_c(t) be the central scalar fields from two actual saved temporal refinements on the SAME spatial mesh. Let theta_f,theta_c contain the corresponding source positions and independently reconstructed live metric providers. The explicit Gram functional is the quadratic functional J(u;theta) defined in the preceding note, with every row retained.

Set e=u_f-u_c and u_bar=(u_f+u_c)/2. Quadraticity at fixed theta_f gives

    D = J(u_f;theta_f)-J(u_c;theta_c)
      = g^T e + d_theta,
    g = partial_u J(u_bar;theta_f),
    d_theta = J(u_c;theta_f)-J(u_c;theta_c).

This is exact, not a first-order Taylor approximation. The cross-geometry expression is an explicitly labeled diagnostic counterfactual, not a separately evolved state. Ignoring d_theta would silently assume identical source positions/geometry. The full field momentum and gravitational feedback remain in the saved trajectories used to construct both theta values.

The same identity applies independently to source-straddling Gram rows and to the remaining rows. Their covectors and geometry terms add to the full result; the source partition does not discard the rest of the action.

## 2. Continuous transport law

Where the paths and geometry are differentiable,

    dD/dt = g^T de/dt + (dg/dt)^T e + d(d_theta)/dt.

The covector rate includes both changing fields and changing geometry:

    dg/dt = J_uu(u_bar;theta_f) du_bar/dt
             + J_u,theta(u_bar;theta_f) dtheta_f/dt.

The second term cannot be omitted merely because the field functional was differentiated at fixed geometry when defining g. Fixed geometry in one partial derivative is not frozen geometry in the evolution.

To expose how the field rate changes, introduce the diagnostic rate v_alt obtained by applying the fine layer's retained Legendre inverse at fine coordinates/geometry but the coarse central canonical momenta. Then define

    a_p = v_f-v_alt,
    a_config = v_alt-v_c,
    de/dt = a_p+a_config

for exact pointwise trajectories. Thus the force defect receives momentum-channel work, configuration/metric-channel work, changing-covector work, and the endpoint geometry correction. The numerical central-label interpolation and momentum inversion have finite reconstruction precision; the two named channels are literal algebraic contrasts, not an assertion of independently isolated physical causes. Their sum is checked against the actual reconstructed rate difference. The counterfactual must remain timelike with positive source inertia.

For any common positive energy matrix K(t), a conditional bound follows directly:

    |D(T)| <= |D(0)| + |d_theta(T)-d_theta(0)|
      + integral [ ||g||_(K^-1) (||a_p||_K+||a_config||_K)
                   + ||dg/dt||_(K^-1) ||e||_K ] dt.

Approximate paths add their rate-defect term. This formula does not claim that its coefficients are uniformly bounded for the nonlinear parent, or that the hierarchical error equals the unknown continuum error. It shows precisely why a small terminal field norm alone is insufficient: accumulated rate work and the evolving force covector both matter.

## 3. An exact discrete identity, not a fitted residual model

At matched times t_n define g_mid=(g_(n+1)+g_n)/2 and e_mid=(e_(n+1)+e_n)/2. The elementary product identity is

    g_(n+1)^T e_(n+1)-g_n^T e_n
      = g_mid^T (e_(n+1)-e_n) + (g_(n+1)-g_n)^T e_mid.

For each channel use a trapezoidal rate increment, for example

    Delta_p = (t_(n+1)-t_n) (a_p,n+a_p,n+1)/2.

Define the explicitly visible path-quadrature defect

    rho_n = e_(n+1)-e_n-Delta_p-Delta_config.

Summing gives the exact finite-data budget

    D_end = D_start + sum g_mid^T Delta_p
              + sum g_mid^T Delta_config
              + sum g_mid^T rho_n
              + sum Delta_g^T e_mid
              + d_theta,end-d_theta,start.

Each sum has a computable absolute nodal bound sum |component_i|. These are bounds for the retained numerical decomposition, not validated continuous-time error enclosures. The identity's reconstruction check alone cannot certify the ODE: rho was defined using the observed path increments. Subsampling the SAME actual trajectory gives a separate quadrature-resolution test without pretending it is a new evolution.

## 4. Independent negative control for the meaning of rho

Use the exact analytic paths on [0,1/3]

    u_c=1+t, u_f=1+t+epsilon t^3,
    a_c=1, a_f=1+t, J(u;a)=a u^2/2,
    p_c=u_c'/a_c, p_f=u_f'/a_f,
    v_alt=a_f p_c, epsilon=1/7.

Both paths solve their stated velocity equations EXACTLY. Nevertheless trapezoidal integration of their rate difference produces a nonzero rho, because e=epsilon t^3. Its signed error contribution refines at second order with the sampling interval. It would therefore be mathematically false to relabel rho as the time integrator's ODE error. Symbolic checks also verify that dropping the moving covector or geometry feedback changes the exact force defect.

## 5. Actual-state test

The live test uses 33 matched saved times on T=4e-5: MTS513 compares64/128 evolved steps, reference513 compares32/64. At every time both metric/canonical inverse problems are solved again from their respective states. No live state is replaced, no source/Gram term is switched off, and no new time evolution is launched. The same retained data provide8/16/32 interval transport budgets for all rows, source rows, and remaining rows.

Both live reconstruction workers finished while the conversation was interrupted; their saved results survived. Each completed 111 implementation checks. The independent analytic validator subsequently completed 14 checks, for 236 successful implementation checks in this stage. There were no new failed executions and no new physical evolution. All results remain non-claim.

### 5.1 What is genuinely localized

At T, the actual MTS 64->128 step change in the explicit Gram drive is 1.7207285842325e-10. The quadratic midpoint-covector expression gives 1.7207287857098e-10, differing by 2.0148e-17. Across all 33 times the largest reconstruction difference is 3.5605e-16. These measured floating-point discrepancies must accompany any precision claim about the much smaller partition remainders.

The source-straddling rows account for the endpoint temporal Gram-force change to this measured accuracy: their directly evaluated change is 1.7207285842187e-10. The computed remaining-row contribution is far below the reconstruction floor; it is not a meaningful 12-digit physical localization claim. The largest nodal field difference in this temporal pair is only 7.67035e-18, showing again how strongly the source force can amplify a very small field difference.

The terminal source positions are equal at stored floating-point precision. The largest separately evaluated cross-geometry/source-position correction among these samples is 9.7607e-23. This supports negligible terminal geometry correction for THIS already-tight temporal pair only, not a theorem that geometry feedback is negligible in spatial refinement or the parent theory. The changing configuration/metric rate channel remains explicitly included in the transport sum.

### 5.2 Which transport contributions are not yet resolved

The exact sum reconstructs the same endpoint at every sampling density, as it must. Its individual signed contributions do NOT yet settle:

| Sampling intervals | Momentum-channel work | Configuration/metric work | Path-quadrature remainder | Moving-covector work |
|---:|---:|---:|---:|---:|
|8| -3.26194e-10 | -7.07025e-14 | +4.98337e-10 | +1.62994e-16 |
|16| +6.06675e-10 | -2.90258e-13 | -4.34312e-10 | +1.64153e-16 |
|32| -1.40897e-10 | -3.45349e-13 | +3.13315e-10 | +1.57462e-16 |

The momentum contribution changes sign under sampling refinement, while the path-quadrature remainder is comparable to or larger than the net1.72073e-10 endpoint change. Therefore this is NOT a resolved attribution of the dynamical cause. The finest absolute nodal budget is1.16438e-8, about68times the endpoint change; it is valid for the numerical identity but not a sharp physical error enclosure. The tiny reconstruction residual of the telescoping sum does not repair that weakness.

The zero-Gram reference has exactly zero for this Gram-functional diagnostic, as expected. That is a useful implementation control, not evidence of exactness of the reference's entire dynamics. Its nonzero ordinary force/impulse errors remain in the preceding checkpoint.

### 5.3 Independent exact solution and negative controls

The analytic control has exactly zero ODE solution error but nonzero path-quadrature work: -5.66928e-5, -1.41708e-5, -3.54256e-6 at8,16,32intervals. The second-order refinement and exact symbolic transport are verified independently. Dropping the evolving covector or geometry feedback fails the exact symbolic identity. Thus neither a vanishing telescoping residual nor a nonzero rho can be used to claim that the actual time integrator has been validated or blamed.

## 6. Decision

This stage derives and verifies an exact live-background error-transport law, identifies the source-straddling rows as the location of the remaining TEMPORAL Gram-force sensitivity, and detects insufficient quadrature resolution in attempts to allocate the accumulated work. It does not explain away or fix the larger SPATIAL/continuum mismatch measured previously. The12.5718%integrated and13.58%instantaneous discrepancies are unchanged.

The next bounded calculation should treat the retained fast linear modes analytically using the already saved frozen canonical basis, and test an exponential/oscillatory transport quadrature for the nonlinear remainder. It must keep the live metric/source remainder and initial-data terms, and be checked against actual saved refinements. Another broad source audit, a full dense Jacobian, or interpreting rho as an integrator failure would not address the identified issue. No next-stage evolution was started during completion of this interrupted checkpoint.

Completed evidence:

- `source-intake/navier-stokes/20260914/annular-live-Gram-defect-transport-MTS-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-Gram-defect-transport-reference-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-Gram-transport-identity-attempt01/status.json`

Implementations:

- `scripts/derive_annular_live_Gram_defect_transport_20260919.py`
- `scripts/validate_annular_Gram_transport_identity_20260919.py`
