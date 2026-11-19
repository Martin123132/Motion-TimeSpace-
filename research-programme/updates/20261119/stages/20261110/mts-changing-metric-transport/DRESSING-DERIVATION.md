# Conditional metric-dressed preparation

Frozen before evaluating the alternative preparation, 2026-11-10. This is a
diagnostic extension, not a replacement for PROTOCOL.md or its primary failed
native comparison. No source, mass, grid, numerical gate or original output
is changed. Reuse the saved full forcing integral for all399modes.

## What the primary experiment actually prepared

The saved density/current specify two averaged quantities, not a unique
microscopic perturbation. The primary preparation chose the free sideband
relation F'=lambda_k F, where F is the complex representative of the two real
carrier quadratures. That is not the derivative of a metric-forced particular
solution. A homogeneous high-frequency component can therefore be introduced
even when density and current match exactly at the initial slice.

## Exact flat, constant-metric calculation

Let B=A exp(-i mu tau), omega=sqrt(mu^2+k^2), and

    F''+omega^2 F=-2 mu^2 Psi B.

Selecting no free negative-frequency homogeneous mode gives

    F'=-i omega F-i c Psi B,  c=2 mu^2/(omega+mu).

This has a regular resonant k=0 limit. It follows by differentiating the
forced particular solution; setting the whole negative-frequency projection
to zero would incorrectly remove its forced contribution as well.

Writing F/B=R+i I, w=omega/mu and r=(w-1)/(w+1), the exact quadrature-averaged
linear sources are

    delta=(1+w)R-r Psi,  S=I,
    Pi=(w-1)R-r Psi=r delta-r(1-r)Psi.
    delta'=k^2 S/mu,
    S'=-mu [r delta+(1-r+r^2)Psi].

Here Pi=delta_p/rho_background, not a relative error in pressure. At k=0,
Pi=0 and S'=-mu Psi. By contrast, the undressed free preparation has
Pi=-Psi at that same slice. Thus a pressure transient can arise from the
microscopic preparation rather than from a wrong gravitational coupling.
Finite-k metric-pressure corrections must not be silently discarded.

## Conditional extension to the actual supplied history

Use the previously derived second-adiabatic rates

    lambda_j=L_j-i W_j,  L_j=-W_j'/(2W_j),
    R_j=lambda_j'+lambda_j^2+Omega_j^2.

With C=Psi+3Phi, the physical source coefficient is

    S0=C'(lambda_0-H)-2 mu^2 Psi.

For r_fast=F'-lambda_k F the exact algebraic identity is

    r_fast'+lambda_k r_fast=S0 B-R_k F,

when B'=lambda_0 B. Setting r_fast=D B gives

    D'+(lambda_0+lambda_k)D=S0-R_k F/B.

The leading slowly changing particular response is therefore

    D0=S0/(lambda_0+lambda_k).

Its remaining defect is D0' B+R_k F. This is a derived approximation, NOT
an exact solution or a theorem selecting a cosmological initial population.
The discarded homogeneous solution is still an independent preparation datum.
We will report the sampled adiabatic indicator and not call it a uniform
bound. The certified W2 transport residual is a separate bound.

Compute conformal source derivatives analytically from the unchanged supplied
cubic: C'=H C_s, C''=H' C_s+H^2 C_ss, Psi'=H Psi_s. In particular

    lambda_j'=-W_j''/(2W_j)+(W_j'/W_j)^2/2-i W_j',
    S0'=C''(lambda_0-H)+C'(lambda_0'-H')
         -4 H mu^2 Psi-2 mu^2 Psi',
    D0'=S0'/(lambda_0+lambda_k)
         -S0(lambda_0'+lambda_k')/(lambda_0+lambda_k)^2.

Do not differentiate raw float32 source samples to obtain physical H jets.

## Frozen test

Add A(Re D0, Im D0) to the initial physical perturbation derivative. Invert
the same source map to keep the original delta and S. With
Db=W0^2+mu^2+(L0-H)^2 the density offset is

    delta_D=2[(L0-H)Re D0-W0 Im D0]/Db.

The map's density target changes by -delta_D; its current target is unchanged.
Convert back using the same canonical shift. Propagate with integral8192;
the exact linear difference between the preparations is homogeneous because
their background and metric forcing are identical. Retain the original error
normalizers. Compare all399native modes; do not fit D0 or relax2e-5.
The physical cold Euler control is unchanged and remains a separate baseline.

This alternate state is explicitly conditional. Passing would identify a
preparation/matching mechanism, not derive formation occupation, validate a
galaxy prediction or authorize replacing the retained native closure.
