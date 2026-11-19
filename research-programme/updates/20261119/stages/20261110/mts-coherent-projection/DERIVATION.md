# Coherent source projection, gauge products and pressure memory

Use the retained real-scalar action and the flat native conventions from
`../mts-early-canonical-state-bridge-20261110/DERIVATION.md`. Work at the
existing k=1/Mpc; formulas below show k where helpful. H is conformal Hubble,
mu=a*m, b'=v, and native stresses are8*pi*G*a^2 times physical stresses.
No observation, new coupling, new phase window or population is introduced.

## 1. A fixed linear extraction is not a positive average

Let L[f]=sum_i w_i*f_i use the ORIGINAL902-node a225-w6-d8 weights. These
are frozen before examining the repaired histories. For any two histories,

    C(f,g) = L[fg]-L[f]*L[g],
    L[fg] = L[f]*L[g]+C(f,g),
    L[fgh]-L[f]*L[g]*L[h] = C(fg,h)+L[h]*C(f,g).

These identities hold even for signed weights, without a statistical
interpretation. The bound |L[e]|<=sum|w_i|*max|e_i| controls a KNOWN sample
error only; it is not a bound on unresolved derivatives or a positive
population construction. No Sigma=I/2 substitution is authorized.

Set beta=a/density0, retaining the historical normalization density0, and
write d=L[beta*D], j=L[beta*Q], p=L[beta*P]. A product of projected factors
is not the projection of their product, even though all input scalars are
known. The same operator is applied to the cold control at matching epochs.

## 2. Gauge conversion: the explicit missing product terms

For the real scalar, S=v^2 and V=mu^2*b*v. The retained source map gives

    DN=Ds-3H*S*alpha,
    PN=Ps-(3H*S+2V)*alpha,
    QN=Qs+k*S*alpha.

With Hbar=L[H], Sbar=L[beta*S], Vbar=L[beta*V], alphabar=L[alpha], the
factorized map would predict dN=dS-3Hbar*Sbar*alphabar and analogues. Its
corrections, calculated from the coherent histories rather than fitted, are

    delta_d=-3*(C(beta*S*H,alpha)+alphabar*C(beta*S,H)),
    delta_p=delta_d-2*C(beta*V,alpha),
    delta_j=k*C(beta*S,alpha).

The gauge pressure shift for cold dust is zero, not the scalar formula.
Dust uses S=rho_g, delta_p=0 and the same density/current product audit.
The slow scalar is audited in both cases, but its pressure is NOT compared
against a nonrelativistic heavy-scalar closure outside that closure's domain.

## 3. The corresponding metric-source correction

The instantaneous flat constraint is

    Phi = -(Dsync+3H*Qsync/k)/(2k^2).

Use total native source Dsync,Qsync. Let rho0=density0/a0 and compare the
projected metric rho0*L[beta*Phi] with the frozen-coefficient constraint
-(rho0/(2k^2))*(L[beta*Dsync]+3Hbar*L[beta*Qsync]/k). Their difference is

    delta_Phi = -3rho0/(2k^3)*C(beta*Qsync,H).

This is a projection/representation correction, not an extra gravitational
force. It must be checked in the baseline too. Instantaneous constraint
satisfaction does not guarantee that the factorized projected source has
the same constraint.

## 4. Deriving a pressure prediction without fitting pressure

The synchronous perturbation equations are

    us'=ws,
    ws'=-2H*ws-(k^2+mu^2)*us-k*z*v,
    v'=-2H*v-mu^2*b,
    Ps=v*ws-mu^2*b*us.

For C=b*us, direct differentiation yields

    2Ps=C''+2H*C'+k^2*C+k*z*b*v.

Let Z=a*C=a*b*us. Using a'=aH removes the first-derivative term:

    2a*Ps=Z''+(k^2-H^2-H')*Z+a*k*z*b*v.                (1)

This exposes the missing phase/displacement-curvature information. It does
not require dividing by b or v at a turning point. It is derived from the
retained equations, not imported from a different QFT or asserted as an
algebraic dust closure.

Retain source-table defects rather than declaring them zero. Define

    Ef=b'-v,   Eb=v'+2Hv+mu^2*b.

The RHS of(1) must have the following term SUBTRACTED:

    a*((Eb+Ef'+2H*Ef)*us+2Ef*ws).                     (2)

For evaluation on the equation-owned clock,
Ef=H*b_N-v and Ef'=H'*b_N+H^2*b_NN-H*v_N. Use the retained Friedmann
H'=-(R+3Pbar)/6, where Pbar is BACKGROUND pressure, not the pressure
perturbation being predicted. The prior off-shell clock qualification
remains: this is the equation-owned clock, not proof that interpolation of
the thermal scale factor has exactly that derivative everywhere.

Predict the projected pressure from(1)-(2) by fitting only Z to the SAME
frozen29-column harmonic/polynomial design and differentiating that explicit
curve. No pressure samples enter its coefficients. Use actual Z for the
zeroth-order term and the actual metric/source force for z. Differentiate
the frozen phase labels as a function of each case's saved physical clock,
using the full guarded4253-point clock and an every-other-point control.
The selected window, phase labels, weights and coefficient basis do not
change. Compare against independently retained native pressure afterward.

A small Z reconstruction residual alone does not bound its second derivative;
the derivative-resolution comparison and actual pressure discrepancy must
both be reported. A failure is a diagnosis of this representation/test,
not permission to fit pressure or alter the phase window.

## 5. Separately identify the old averaged-pressure approximation

The retained law is c0^2*(dS+3Hbar*jS/k), with
c0^2=r/(sqrt(1+r)+1)^2, r=(k/(a0*m))^2. Its existing pressure gate is2e-6
relative to the original mode norm, not pressure-relative accuracy.

For diagnostic decomposition only, let cs2(a) have the same formula at a.
The measured projected discrepancy equals the sum of

    L[beta*(Ps-cs2(a)*(Ds+3H*Qs/k))]

and the coefficient/product drift between the projected instantaneous law
and its frozen-coefficient value. That decomposition USES measured pressure
and is not by itself an independent derivation of a pressure correction.
The distinct prediction in(1)-(2) is the derivation-first test.
