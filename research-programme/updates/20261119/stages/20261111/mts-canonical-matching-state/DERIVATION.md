# Preparation-owned cross moments and the matching connection

Retain the same minimally coupled positive quadratic scalar and the ORIGINAL signed secular extraction L. Units are the existing conformal Mpc convention. At the fixed matching center a0, set mu0=a0*m and beta0=a0/R0. At each saved epoch use mu=a*m, beta=a/R0, B=(b,v), U=(u,w). All source normalization and mode k=5 are inherited.

## A source-complete candidate, not an inverse of two moments

Define the normalized histories

    S(t)=beta B B^T, M(t)=beta B U^T.

Their natural projections are Sbar=L[S], Mbar=L[M]. To retain the ACTUAL mass coefficient in the projected density and pressure, define a source-compatible representative

    Sc00=L[beta*mu^2*b^2]/mu0^2,
    Mc00=L[beta*mu^2*b*u]/mu0^2,

with every other entry equal to its natural projected value. Then

    d=Mc11+mu0^2*Mc00, q=k*Mc10, p=Mc11-mu0^2*Mc00.

These recover all THREE projected native sources. Mc01=L[beta*b*w] is separately determined by the original saved phase history. It is not fixed by d,q,p, and is not chosen to make future dynamics agree.

The inferred homogeneous energy and pressure are

    e=(Sc11+mu0^2*Sc00)/2, pb=(Sc11-mu0^2*Sc00)/2.

Do not rescale e to1 to force agreement with the original matched dust weight. The background-weight and pressure checks must expose that difference.

If Sc is positive definite, a factor Bq with Bq Bq^T=Sc exists. Set Uq^T=Bq^-1 Mc. Then Bq Uq^T=Mc reproduces every retained moment. For stable factorization use diag(mu0,1)*Sc*diag(mu0,1) before undoing the scaling. Common orthogonal rotation of the quadrature columns changes neither moment nor any quadratic source. This constructs a moment representative; it does NOT prove the signed extraction is a probability measure or that the original coherent state became a physical two-quadrature population.

At a specified current metric eta0,alpha0, the retained canonical map acts on each column:

    uN=uS+v*alpha0,
    pN=wS-3eta0*v-mu0^2*b*alpha0.

The same matrix formulation applies without factorization. Products with varying eta,alpha,H and Phi within the extraction have their already-derived covariance corrections. Their measured initial values are saved, not asserted zero or hidden in a new coupling.

## Exact projected-rate residual

Use r=H for the equation-owned clock, with actual tabulated background derivatives b'=H*b_N, v'=H*v_N. Define Eb=v'+2Hv+mu^2*b and Ef=b'-v. The unmodified perturbation equations give u'=w and w'=-2Hw-(k^2+mu^2)u-k*z*v.

Let

    Ab=[[0,1],[-mu^2,-2H]],
    Au=[[0,1],[-(mu^2+k^2),-2H]],
    F=[[0,0],[0,-k*z]],
    eB=(Ef,Eb).

Then, exactly on those source histories,

    S'=H*S+Ab*S+S*Ab^T
          +beta*(eB B^T+B eB^T),
    M'=H*M+Ab*M+M*Au^T+S*F^T
          +beta*eB U^T.

Fix H0=L[H], z0=L[z], and the corresponding center operators. Applying L produces an ordinary local generator plus explicit operator/state and force/state correlations and representation defects. Define DeltaS=Sc-Sbar and DeltaM=Mc-Mbar. The mass-map connection is

    DeltaS00'=L[(mu^2/mu0^2-1)*S00'
                  +2*(H-H0)*(mu^2/mu0^2)*S00],

and the identical formula with M for DeltaM00'. Other connection entries vanish. The candidate rate discrepancy is therefore

    RS=operator_correlations+representation
       +DeltaS'-(H0*DeltaS+Ab0*DeltaS+DeltaS*Ab0^T),

    RM=operator_correlations+force_correlations+representation
       +DeltaM'-(H0*DeltaM+Ab0*DeltaM+DeltaM*Au0^T+DeltaS*F0^T).

Every term is calculated from saved preparation and the same equations, not fitted to a discrepancy. This is the RATE extracted by the fixed functional, not a claim that a new moving average has been defined or that L automatically commutes with evolution. These equalities test whether the bare center generator is already a faithful local handoff; if not, RS/RM identify the initial memory forcing that must be transported rather than discarded.

## Metric-force reconstruction without differencing quantized densities

The original native output stores growth=delta_cb'/(H*delta_cb), and the native synchronous dust equations are delta_c'=-k*z and delta_b'=-k*(z+v_b). Thus

    z=-H*growth*delta_cb/k-f_b*v_b,
    delta_cb=(1-f_b)*delta_c+f_b*delta_b.

f_b is the fixed baryon fraction of the retained baryon+CDM component, read from the already saved same-branch native background. This uses saved derivatives rather than differentiating float-origin transfer columns. Their finite output precision remains a numerical qualification. The code records the exact source paths for these conventions.

For actual cold dust, beta*Rc is constant. The projected density rate is -k*L[beta*Rc*z], identical to the center generator with z0=L[z] and the inherited constant. No scalar phase or pressure is assigned to the cold component.

The local-rate/background gates must pass before this representative is promoted to a late evolving state. Even then a complete current native rest-state handoff is required; output transfer columns alone are not a full restart vector.
