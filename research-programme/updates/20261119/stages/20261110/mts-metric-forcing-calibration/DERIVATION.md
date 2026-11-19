# Fixed metric coupling, canonical forcing and its error budget

Units c=hbar=1; conformal time tau, H=a'/a, mu=a m. The metric convention is
ds^2=a^2[-(1+2 Psi)d tau^2+(1-2 Phi)dx^2]. H, mu and k have inverse-Mpc
units; Phi and Psi are dimensionless. Primes mean conformal derivatives.
The retained real scalar has L=-[(partial phi)^2+m^2 phi^2]/2 in this metric.
This is the existing positive quadratic subfamily, not a claim about omitted
interactions. G retains its inherited normalization.

## 1. The action fixes both source coefficients

Write phi=phi0+y, v=phi0', C=Psi+3 Phi, D=3 Phi-Psi. The part of the
expanded action needed to vary the linear scalar perturbation is

    L_y = a^2 [y'^2-(k^2+mu^2)y^2]/2
          -a^2 C v y' + a^2 mu^2 D phi0 y.

Pure metric terms and the gravitational action are not displayed. For an
on-shell background v'=-2Hv-mu^2 phi0 its Euler equation is

    y''+2Hy'+(k^2+mu^2)y = v(Psi'+3Phi')-2mu^2 phi0 Psi.

The rescaled canonical momentum p=y'-Cv gives a derivative-free system:

    y'=p+Cv,
    p'=-2Hp-(k^2+mu^2)y+mu^2 D phi0.

There is no independent force coefficient to choose. Let q0=a phi0,
p0=q0', q=a y, Omega_j^2=j^2+mu^2-H'-H^2. Up to the standard homogeneous
integration by parts, the canonical action and its momentum are

    f1=C(p0-Hq0),             f2=Hf1+mu^2 D q0,
    L_q=q'^2/2-Omega_k^2 q^2/2-f1 q'+f2 q,
    P=q'-f1=a p+Hq,
    Hamilton=(P+f1)^2/2+Omega_k^2 q^2/2-f2 q.

Consequently q'=P+f1 and P'=-Omega_k^2 q+f2. The time-dependent work
identity is Hamilton'=(P+f1)f1'+(Omega_k^2)'q^2/2-f2'q. Do not discard
metric-only terms while claiming a full gravity variation: the displayed
action suffices for supplied-metric matter trajectories, not all constraints.

An approximate background is off shell. Expanding the densitized action
and directly linearizing the undensitized KG equation can then differ by
a metric factor times the background residual. They agree on shell. We use
the action above and bound its approximate-background error; no guessed
residual force is added to disguise that distinction.

## 2. Exact stress and conservation, regular at turning points

Define B=(v^2+mu^2 phi0^2)/2 and

    E=v p+3v^2 Phi+mu^2 phi0 y,
    Pr=v p+3v^2 Phi-mu^2 phi0 y,
    Q=k v y,
    delta=E/B, Pi=Pr/B, u=Q/B,
    w=(v^2-mu^2 phi0^2)/(2B).

These are the physical stress including -v^2 Psi in v y'-v^2 Psi.
Substitution of the exact field equations gives

    delta'+k u-3(1+w)Phi'+3H(Pi-w delta)=0,
    u'+H(1-3w)u-k[Pi+(1+w)Psi]=0.

No division by v occurs. These are matter conservation in the supplied
metric; arbitrary Phi and Psi need not themselves solve Einstein constraints.

## 3. Forced extension of the previous certified template

For z0=(q0,p0) and zk=(q,P), let Aj=[[0,1],[-Omega_j^2,0]]. Then

    z0'=A0 z0,  zk'=Ak zk+F z0,
    F=[[-HC,C],[mu^2 D-H^2 C,HC]].

Use each previously derived unit-Wronskian template Yj, with residual Rj.
In coordinates cj=Yj^-1 zj,

    c0'=E0 c0,  ck'=Ek ck+G c0,  G=Yk^-1 F Y0,
    ||Ej||_2=|Rj|/Wj.

The W2 forced approximation keeps the full G integral, but sets Ej=0.
Let Bj=integral |Rj|/Wj and J=integral ||G||_2. With identical canonical
initial states, variation of constants and triangular coupling yield

    ||ck-ck_bar|| <= (exp(Bk)-1)||ck_initial||
        +[exp(Bk+B0)-1] J ||c0_initial||.

This does not exponentiate J. Source error delta G adds at most
exp(Bk+B0) J_delta ||c0_initial||, with J_delta=integral ||delta G||.
No counter-rotating piece has been set to zero. The previous exact rational
constant-H box supplies Bj; arbitrary H requires its derivatives in W2
and a new enclosure, not substitution into this certificate.

For a computable J bound factor Y=diag(1/sqrt(W),sqrt(W)) S R, where R
is a rotation and the shear S has off-diagonal -W'/(2W^2). If W lies in
[Wmin,Wmax] and |W'/(2W^2)|<=sigma, use

    J <= duration (1+sigma)^2 [AC |C|+AD |D|],
    AC=2 Hmax Wmax/Wmin+Wmax+Hmax^2/Wmin,
    AD=mu_max^2/Wmin.

The entrywise absolute sum bounds the operator norm. Metric rounding radii
give |delta C|,|delta D| <= epsilon_Psi+3epsilon_Phi, hence the same bound
for J_delta. This controls supplied-metric rounding, not missing cosmological
evolution. Exact rational bounds and readable float summaries are separate.

## 4. Newtonian phase calibration is fixed, not fitted

With H=0 and constant potentials, eliminate P using the exact background:

    q''+(k^2+mu^2)q=-2mu^2 Psi q0.

Constant Phi cancels at fixed physical q,q'. For q0=A cos(mu tau) and
zero initial q,q', the response is

    q=-2mu^2 Psi A [cos(mu tau)-cos(sqrt(mu^2+k^2)tau)]/k^2.

At k=0 its continuous limit is -mu Psi A tau sin(mu tau). In the convention
phi proportional to cos(theta-S), this is S'=-mu Psi. Restoring units,
the phase force is m Phi_Newton (Psi=Phi_Newton/c^2), so the leading
nonrelativistic acceleration has coefficient one: -grad Phi_Newton.
This recovers the retained minimal metric coupling; it does not derive G's
numerical value or select a galactic occupation from a rotation curve.

## 5. Controlled late-state preparation and averaging

The saved late density/current is averaged, not a unique microscopic phase.
Use the sealed W2 source map T to solve for R,I from

    T (R,I) = (delta+(1+w)Psi, S),  S=-mu u/k.

Prepare two backgrounds with carrier phase 0 and pi/2, and the corresponding
perturbations q=A(R cos theta+I sin theta),
q'=A[Lk(R cos theta+I sin theta)+Wk(-R sin theta+I cos theta)],
where A=1/sqrt(W0), Lk=-Wk'/(2Wk). P=q'-f1. This is explicit preparation,
not inferred fast phase. Its zero-time phase-averaged stress reproduces the
saved delta,S including the lapse term.

Linearity makes the two-quadrature average of quadratic products equal to
a uniform initial-phase ensemble. Average stress numerators and background
energy first, then divide; do not average ratios or call this time averaging.
Sum-frequency transients remain in the finite-time forced response.

## Source owners and method attribution

- ../MTS-HEAVY-BATH-COUNTERFLOW-AND-GALACTIC-STRESS.md, section1;
  ../condensate-origin-20261003/motion-bath-matching-20261006/49-real-motion-envelope-and-existing-bath-matching.md.
- ../MTS-NATIVE-GAUGE-AND-PHYSICAL-EVOLUTION.md, sections1and4, plus the
  retained MTSTwoField.f90 action/equation implementation.
- ../mts-second-adiabatic-state-20261110/DERIVATION.md, proof.json and
  SOURCE-CONSERVATION.md for W2 and the unforced residual certificate.
- ../mts-formation-state-bundle-20261110/late-heavy.npz and late-cold.npz;
  ../mts-averaged-state-action-20261110 for the saved matched probe.

Minimal scalar coupling, gauge transformations, WKB and variation of constants
are established methods. The work here is their explicit consistent reduction
and bounded/tested interface for this retained MTS subfamily, not a new general
gravity principle or a constructive-QFT existence/mass-gap theorem.
