# Common-metric constraint and spatial-pressure test

Private stage, 2026-11-17. No new theory parameter, fit, scattering bank, grid, epoch, tolerance or quantum measure. The previous stage is preserved under `../mts-coupled-preparation-response-20261116`. Its full preparation-pressure budget, not just the small later increment, remains the source-budget authority.

## Exact retained conventions

Use conformal time and the saved flat scalar mode k=5 Mpc^-1. With the existing gravitational normalization kappa, define B=kappa a^2 rho, P=kappa a^2 p, D=kappa a^2 delta-rho, T=kappa a^2 delta-p, Q=the native rescaled heat flux and Pi=the native anisotropic stress. These rescaled stresses have dimensions Mpc^-2. H=a'/a has dimension Mpc^-1 for a coherent background; distinguish the old interpolation rate r from the native Friedmann H. The native eta_k, z and sigma have dimension Mpc^-1 in these equations.

The retained solver uses
```
3H^2=B,       Hz=D/(2k)+eta_k,
eta_k'=Q/2,   sigma=z+3Q/(2k^2).
```
The metric readout takes the actual species right-hand sides, differentiates their stresses, sets H'=B'/(6H), and differentiates the density constraint to obtain z'. It does not finite-difference saved samples, and it does not use the spatial Einstein equation to define the derivative being tested.

Define actual residuals
```
E_B=B'+H(B+3P)
E_D=D'+H(D+3T)+kQ+kz(B+P)
E_Q=Q'+2HQ-k(T-2Pi/3)
E_eta=eta_k'-Q/2
C00=Hz-D/(2k)-eta_k
F=3H^2-B.
```
Their exact compatibility identities are
```
R_trace=z'+2Hz-eta_k+3T/(2k)
       =E_D/(2kH)-z E_B/(6H^2)+E_eta/H+C00+z F/(3H)
R_shear=sigma'+2H sigma-eta_k+Pi/k
       =R_trace+3 E_Q/(2k^2).
```
The native spatial-equation sigma derivative is independently exposed. Its difference from the differentiated-constraint derivative equals R_shear. These are familiar Einstein/conservation compatibility relations, not a new physical law; this stage's work is the explicit derivation and test for all species and approximations in the retained MTS implementation.

## Independent approximation/contact predictions

Subtracting a residual defined from the same failed equation would be tautological. Instead predict contacts from each species' implemented equations, and separately test the RAW residuals at the unchanged numerical tolerance.

For pressureless cold matter:
```
E_B=(H-r)B, E_D=(H-r)D, E_Q=0.
```

The retained baryon background is pressureless, but its Euler equation contains the thermal pressure T_b=B_b cs2 delta_b. Its continuity equation does not contain the corresponding relativistic pressure correction. Therefore
```
E_D,b=(H-r)D_b+3H T_b
E_Q,b=(H-r)Q_b-J
E_D,gamma=2(H-r)D_gamma
E_Q,gamma=2(H-r)Q_gamma+J
J=B_gamma opacity (4v_b/3-q_gamma).
```
Internal Thomson drag cancels. The 3H T_b contact is a retained thermo approximation, not newly imposed exchange. Massless neutrinos have the same factor-two expansion contacts without drag. The saved high-ktau closure changes higher multipoles but not the low-moment equations used here.

For either quadratic scalar, write M=(am)^2, homogeneous b,v and perturbation u,w. Then
```
B=(v^2+Mb^2)/2, P=(v^2-Mb^2)/2, B+P=v^2
D=vw+Mbu, T=vw-Mbu, Q=kvu
fb=b'-v, fv=v'+2Hv+Mb
E_B=(r-H)Mb^2+v fv+Mb fb
E_D=2(r-H)Mbu+fv w+M fb u
E_Q=k fv u.
```
The perturbation equation is u'=w, w'=-2Hw-(k^2+M)u-kzv. In the coherent background r=H and fb=fv=0. No Euler contact is silently discarded in the old interpolated control.

### Scalar rounding repair

The first native readout tests failed only the tiny slow-scalar density contact. Forming B+P from two nearly opposite stored energies lost its kinetic part. Evaluate it from the primitive v^2 identity instead. The failure receipts, native packet bytes, frozen norms and 1e-10 tolerance are preserved. This affects the component audit representation, not the evolution or physical parameters. The original velocity comes from the saved field packet; the corrected velocity is the simultaneously evolved background.

### Massive-neutrino implementation

Retain its actual momentum kernel W, vq=1/sqrt(1+(am/q)^2), full momentum modes and represented relativistic tail. With f=grhormass/a^2,
```
D=f sum(W F0/vq), T=f sum(W vq F0/3)
Q=f sum(W F1), Pi=f sum(W vq F2)
D'=f[sum(W F0'/vq)-r(density+3pressure)]
Q'=f sum(W F1')-2rQ.
```
Background rho,p use the retained small-am formula in massive_neutrinos.f90. Differentiate that formula itself to get rho_n=d rho/d ln(a), rather than imposing rho_n=rho-3p. The difference is retained explicitly:
```
E_B=f[(H-r)(rho+3p)+r(rho_n-rho+3p)]
E_D=(H-r)(D+3T)+fkz[rho+p-(4/3)sum(W/vq)]+tail_D
E_Q=2(H-r)Q+tail_Q.
```
The finite-kernel background/source mismatch is not set to zero. For each tail mode with s=m^2/(2q^2) and represented F=Fr+s Ft,
```
tail_D=f sum_tail W k/vq[(vq-1+s a^2) Fr1+s(vq-1) Ft1]
tail_Q=f sum_tail W[(1-s a^2-vq) Sr+s(1-vq) St]
Sr=k Fr0/3-2k Fr2/3, St=k Ft0/3-2k Ft2/3.
```
The code uses the native denlk coefficients. Unsupported curvature, matching branch, thermal branch or massive-neutrino regime fails rather than silently generalizing.

## Frozen test design and reuse

1. Independently capture all 934 original states and verify byte equality with previous packets.
2. Freeze per-equation and per-species norms as the maximum absolute constituent-term sum over those original states BEFORE corrected-state testing. Both baseline and MTS use this same rule, not the same cosmological density.
3. Check exact contact identities at 1e-10 and raw physical residuals at 2e-5. Record old-control failures rather than requiring them to pass as a precondition to checking the proposed repair.
4. Reuse the previous Coupled solver unchanged. The full corrected states were not saved at query points, so bounded readout restarts recover them using the exact original initial state, 33x902 query grid, interpolation breakpoints, rtol=1e-10, normalized atol=1e-12 and 32/64 maximum-step settings. Extra diagnostics are only evaluated at saved queries, not every adaptive RHS call.
5. Require every original accepted output array to reproduce byte-for-byte. Capture full component diagnostics and primitive scalar velocities; check both old and coherent states and coarse/fine stability.
6. Test raw R_trace/R_shear, conservation and constraints independently of contact-accounting identities. Measured refinements are numerical uncertainty estimates, not rigorous global bounds.

Sources are the frozen previous run_coupled.py, native_context.py, background defect-response Model, retained native equations.f90, MTSTwoField.f90 and massive_neutrinos.f90. The input manifests record absolute paths and SHA256. New code is the private diagnostic mts_metric_hook.inc, metric_stable.py, prove_metric.py and run_metric.py. Original evolution equations are not edited. Interpretation is limited to this mode, interval and retained approximations. The earlier tiny baseline correction-relative failures remain separate and unresolved.

