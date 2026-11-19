# Relative-phase envelope and a controlled pressure reconstruction

Use only the retained equations, with conformal-time primes:

    Phi'=V+F,  V'=-2HV-mu^2 Phi+G,
    f'=g,     g'=-2Hg-(mu^2+k^2)f-kVz,
    mu=am>0, mu'=r mu, r=a'/a, beta=a/rho0.

F and G are the original representation contacts, or actual interpolation
contacts when a saved coherent background is reconstructed. They are not new
interactions. H and r need not coincide in a representation. k is fixed.

## Exact rotating variables

Let J=[[0,-1],[1,0]], Z=diag(1,-1), R(theta) the usual rotation,
omega=sqrt(mu^2+k^2), and delta=k^2/(omega+mu)=omega-mu. Define

    b=(sqrt(mu) Phi,-V/sqrt(mu))=A(cos(theta),sin(theta)), A>0,
    y=(sqrt(omega) f,-g/sqrt(omega)), u=R(-theta)y,
    zeta=H+r/2, xi=H+r mu^2/(2omega^2),
    c_b=(sqrt(mu)F,-G/sqrt(mu)),
    c_theta=(c_b[1]cos(theta)-c_b[0]sin(theta))/A.

The exact homogeneous phase law is theta'=mu-zeta sin(2theta)+c_theta.
No unwrapped angle or division by Phi or V is needed: use b/A for sine/cosine.
Direct differentiation gives

    u'=(A_s+C)u+j,
    A_s=-H I+(delta-c_theta)J,
    C=zeta sin(2theta)J+xi R(-theta) Z R(theta),
    j=R(-theta)(0,kVz/sqrt(omega)).

The rapidly rotating mass frequency has cancelled exactly. The remaining
skew frequency is the relative beat, not a fitted sound speed. The expansion
and phase-dependent matrix C has NOT vanished. In a constant background with
H=r=F=G=z=0, C=0 and u'=delta J u exactly, for any k/mu. The leading
k^2/(2mu) is only an expansion of delta, not an exact replacement.

Recover f,g via diag(1/sqrt(omega),-sqrt(omega)) R(theta)u and then the ORIGINAL

    (d,q,p)=beta(Vg+mu^2 Phi f, kVf, Vg-mu^2 Phi f).

This retains the fast stress oscillation and both physical phase coordinates.
The previous d_star,w are recovered by their existing transformation, including
the initial and final pressure endpoint. No pressure averaging is assumed.

## Derived finite memory correction, without adjustable coefficients

Introduce K_0=I and, for n>=1,

    K_n'=[A_s,K_n]+C K_(n-1), K_n(t0)=0.

These are determined by the actual background/phase, not by rotation curves or
the observed future perturbation. For p=0,1,2 define S_p=sum(n=0..p)K_n and

    v_p'=A_s v_p+S_p^-1 j, v_p(t0)=u(t0), u_p=S_p v_p.

All initial states match exactly because S_p(t0)=I. Direct differentiation
proves the omitted term, with its sign:

    u_p'=(A_s+C)u_p+j-C K_p v_p,
    e_p'= (A_s+C)e_p+C K_p v_p, e_p(t0)=0,
    e_p=u-u_p.

Thus an error bound comes from a physical equation, not fitted discrepancies.
The symmetric part of A_s+C has largest eigenvalue gamma=-H+abs(xi).
Let E_p'=gamma E_p+norm(C K_p v_p), E_p(t0)=0. Then

    norm(e_p(t)) <= E_p(t).

If W(t) maps u to the three physical sources, each source error is at most
norm(W_row) E_p. This statement is exact for the declared continuous
coefficients and exact integration. Numerical evaluation, saved-history
interpolation and inherited-model errors require separate allowances.

There is an independent conservative invertibility check. Since the scalar
damping in A_s cancels in its commutator, its interaction-picture transport is
orthogonal. With L(t)=integral(norm(C) dt),

    norm(K_n)<=L^n/n!,
    norm(S_p-I)<=sum(n=1..p)L^n/n!.

Require the last quantity below one. The two-dimensional operator norm here is
norm(C)=abs(zeta sin(2theta))+abs(xi). This is not an assumption of long-time
convergence: if the interval grows too long, the bound must be reconsidered.
The correction matrices retain accumulated endpoints, and are not reset at
each saved epoch. Their coefficient-only construction is distinct from a new
physical degree of freedom. Keeping the full untruncated evolution is always
the reference.

## Scope of the present test

Freeze orders0,1,2 and the residual budgets before comparisons. Reuse both
3038..3039 and3039..3040 saved windows, old/coherent MTS and cold baseline;
32/64 step caps, stride1/2/4 reconstruction controls, original934 norms and
unchanged1e-10 algebra/2e-5 numerical tolerances. Evolve exact envelope and
primitive fields independently beside both truncations. Compare all physical
sources and integrated pressure against saved independent work.

The saved background and metric are future forcing here, so these are
conditional replays, not live forecasts. The derivation itself specifies how
the coefficients would be computed from live fields. No forcing is averaged,
no source-history fit is performed, and passing this test would not itself
close galactic occupation or the quantum measure.
