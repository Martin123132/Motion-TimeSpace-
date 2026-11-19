# Wavenumber dependence and the canonical late-source chart

This extends the retained positive quadratic heavy-field subfamily. It does not replace the parent action, choose a galaxy population or refit the source coupling. Owners: `../mts-derived-carrier-normal-form-20261110/DERIVATION.md`, `../mts-phase-corrected-carrier-20261110/DERIVATION.md`, and `../mts-canonical-metric-closure-20261110/DERIVATION.md`.

## 1. Keep k physical

Use conformal time, c=1, mu=a*m>0, omega=sqrt(mu^2+k^2), Sigma=omega+mu, delta=k^2/Sigma, and c_s^2=k^2/Sigma^2. The fixed Fourier wavenumber k>0, mu, omega, H and r=a'/a have units Mpc^-1 in the retained convention. beta=a/R0 has units Mpc^2. Field and perturbation b,u are rescaled dimensionless scalars; v,w have units Mpc^-1. Consequently d,q and the normalized physical sources below are dimensionless. k is fixed when differentiating time-dependent coefficients.

The exact synchronous equations and representation defects are

    b'=v+Ef, v'=-2Hv-mu^2*b+Eb,
    u'=w, w'=-2Hw-(k^2+mu^2)u-k*z*v.

Define C=b*u+v*w/(mu*omega), S=v*u/mu-b*w/omega and

    d=beta*mu*Sigma*C/2, q=beta*k*mu*S/2.

The implemented matrix M maps (u,w) into (d,q). With A=b^2+(v/mu)^2, its determinant is -Ld*Lq*A/omega, where Ld=beta*mu*Sigma/2 and Lq=beta*k*mu/2. It is nonsingular at b=0 OR v=0, provided A>0. The k=0 mode has no such current-coordinate inverse and is rejected, not regularized with a fitted cutoff.

Put c2=(b^2-(v/mu)^2)/A and s2=2*b*v/(mu*A). The physical source rows are

    YD=(1-c_s^2*c2)d-(delta/k)s2*q,
    YQ=(k/Sigma)s2*d+(1-c2)q,
    YP=(c_s^2-c2)d-(Sigma/k)s2*q.

They equal beta*(v*w+mu^2*b*u, k*v*u, v*w-mu^2*b*u). In particular the current contains k. The actual native constraint is

    z=zeta+YD/(2*k*H*beta).

Both that denominator and the force -k*z*v must change consistently when k changes. Multiplying a k=1 sound coefficient alone is not sufficient.

## 2. General harmonic coefficients

In the same explicitly limited physical phase control as the retained derivation, r=H and Ef=Eb=0. Write b=A^0.5*cos(theta), v=-mu*A^0.5*sin(theta), E=beta*(v^2+mu^2*b^2)/2. Let

    t=mu/omega, Gamma=H*(5+t^2), D=1/(2*k*H*beta),
    g0=-k*E*Sigma/(2*omega), gs=-k^2*E/(2*omega).

For x=(d,q,zeta), the upper two rows of its instantaneous operator are

    B(theta)=B0+C2*cos(2theta)+S2*sin(2theta)
                  +C4*cos(4theta)+S4*sin(4theta).

All last rows vanish; zeta' is supplied separately by the current rest equations. Nonzero entries, using one-based indices, are

    B0_11=-H*(1-t)^2/2+D*g0*(1+c_s^2/2)
    B0_12=-k; B0_13=g0
    B0_21=k*c_s^2
    B0_22=-H*(1+t^2)/2+D*gs*delta/(2*k)
    C2_11=Gamma/2-D*g0*(1+c_s^2)
    C2_22=H*(1-t^2)/2; C2_13=-g0
    S2_12=-Gamma*Sigma/(2*k)+D*g0*delta/k
    S2_21=k*H*(1-t^2)/(2*Sigma)+D*gs; S2_23=gs
    C4_11=D*g0*c_s^2/2; C4_22=-D*gs*delta/(2*k)
    S4_12=-D*g0*delta/(2*k); S4_21=-D*gs*c_s^2/2.

These follow by differentiating M and multiplying the primitive force and physical density row BEFORE averaging. This retains the phase correlation in self-gravity. The independent numerical control constructs that primitive operator and its product-rule derivative, without using this harmonic expansion.

The zero-mean primitive K=sum_n(Cn*sin(n*theta)-Sn*cos(n*theta))/(n*mu), n=2,4, gives P=I+K. Its time derivative includes actual phase, mass, energy, H and beta derivatives. At fixed k the first generator correction remains

    Beff=B0+[S2,C2]/(4mu)+[S4,C4]/(8mu)
         +3H*(S2+E*partial_E S2)/(4mu)
         +E*partial_H S2/(8beta*mu).

The last two terms derive from theta'-mu=-3H*sin(2theta)/2, the phase-dependent E'=3HE*cos(2theta), and the oscillatory H'=E*cos(2theta)/(2beta). They are not an additional sound-speed fit. The primitive map derivative in the implementation retains arbitrary r and actual b',v'; this phase-average approximation does not redefine those saved derivatives.

The previously derived live-memory law and its error identity remain applicable to a correctly assembled general-k current-state operator: Z0'=B Z0, Delta'=B Delta+(A-B)Z0 and Zstar'-A Zstar=-(A-B)Delta. This stage checks the general-k coefficient and source-map component; it does not claim a new late evolution.

## 3. Explicit native-to-canonical scalar map

Use native synchronous eta and alpha=sigma/k. The retained observer conventions give

    Phi=eta-H*alpha, Psi=alpha'+H*alpha.

Define the source-compatible scalar map

    uN=uS+v*alpha,
    pN=wS-3*eta*v-mu^2*b*alpha.

Its inverse is uS=uN-v*alpha, wS=pN+3*eta*v+mu^2*b*alpha. On an exact background it is also the canonical transformation pN=uN'-(Psi+3Phi)*v already used in the action. The plus sign in uN is fixed by the saved source conventions; reversing it would reverse the current correction.

Let DhS=v*wS+mu^2*b*uS, PhS=v*wS-mu^2*b*uS and QhS=k*v*uS, with scalar enthalpy Sh=v^2. Direct substitution gives, WITHOUT dividing by b or v,

    Dstar_hN=v*pN+mu^2*b*uN=DhS-3*Sh*eta,
    DhN=Dstar_hN+3*Sh*Phi=DhS-3*H*Sh*alpha,
    QhN=k*v*uN=QhS+k*Sh*alpha,
    PhN=v*pN-mu^2*b*uN+3*Sh*Phi
        =PhS-(3*H*Sh+2*mu^2*b*v)*alpha.

All stresses use the retained 8*pi*G*a^2 convention. For total enthalpy St, the unchanged other species transform too:

    Dstar_total=Dsync_total-3*St*eta,
    QN_total=Qsync_total+k*St*alpha,
    Phi=-(Dstar_total+3*H*QN_total/k)/(2*k^2+3*St).

The alpha terms cancel when the two total rows are combined. This is the same metric constraint already checked in the late hierarchy, not a new force law or adjustable coupling. Other species' anisotropic stress still fixes Psi=Phi-Pi/k^2. The map must be composed with their CURRENT state; holding their transformed metric-dependent sources fixed during scalar variation would be incorrect.

The cold CDM-comoving control has Qsync_c=0, deltaN_c=deltaSync_c-3H*alpha, QN_c=Rc*k*alpha and Dstar_c=Rc*(deltaSync_c-3eta). It is transformed as dust, not assigned a scalar phase.

## 4. Exact defect transport, not an implicit exact-background assumption

Keep r=a'/a distinct from the retained H when diagnosing representation. Define synchronous perturbation defects

    euS=uS'-wS,
    ewS=wS'+2H*wS+(k^2+mu^2)uS+k*z*v,

and metric defects

    eshift=k^2*alpha-k*z-3*eta',
    elapse=alpha'+H*alpha-Psi.

The source-compatible map above then obeys

    euN = uN'-pN-(Psi+3Phi)*v
        = euS+Eb*alpha+v*elapse,

    epN = pN'+2H*pN+(k^2+mu^2)uN-mu^2*(3Phi-Psi)*b
        = ewS+v*eshift+2*(H-r)*mu^2*b*alpha
          -mu^2*Ef*alpha-3*eta*Eb-mu^2*b*elapse.

These follow by the product rule with (mu^2)'=2r*mu^2. They are checked with independent symbolic differentiation, leaving EVERY defect arbitrary. They vanish for exact scalar/metric/background equations, but not merely because the algebraic stress map passes. They identify the terms to carry into the existing continuity/Euler and gravitational-constraint budget instead of silently assuming they are zero.

## 5. What the saved late data do and do not determine

The accepted late capture is k=5, z near10, 93 MTS or91 cold states, heavy selector1. Its ORIGINAL output schedule has61 times; the accepted short interval has ONLY two captured endpoints, at original indices8 and9. Five saved operator evaluations and the earlier integrated controls have their separately documented scope. This stage reuses those endpoint source records; it does not invent intermediate native snapshots.

The late selector's two heavy entries are normalized density/current, not the unaveraged field pair (uS,wS). Therefore the explicit scalar map cannot be applied by simply relabelling those entries. The next implementation must carry the retained homogeneous normalization and an independently specified phase/ensemble/fast-state matching into a native stress replacement. The saved background/averaging defects accompany it. No pointwise equality of an averaged source pair to a unique oscillating field has been inferred here.
