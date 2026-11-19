# Quadratic-field normal form, retained pressure coefficient and metric coupling

Private derivation from the retained positive quadratic heavy-field subfamily. It does not replace the action, add a coupling or select a galactic population. Source: `../mts-coupled-phase-stress-20261110/native/fortran/MTSTwoField.f90`, especially AveragedPressure, Stress and Evolve; the background representation defects are defined in `../mts-native-source-conservation-20261110/DERIVATION.md`. Frozen input hashes identify the exact versions.

## 1. Conventions and equations

Use conformal time tau, c=1, fixed comoving k>0, mu=a*m>0, omega=sqrt(mu^2+k^2), Sigma=omega+mu, delta=omega-mu=k^2/Sigma. H is the retained conformal Hubble rate; r is the actual numerical a'/a. Native scalar stresses include 8*pi*G*a^2. With beta=a/R0, normalized density/current/pressure sources are dimensionless. In the native Mpc convention, k,mu,omega,H,r have units Mpc^-1, beta has units Mpc^2, b,u are rescaled dimensionless fields, and v,w have units Mpc^-1. Numerical evaluation below retains k=1/Mpc; algebra shows k explicitly. The k=0 homogeneous mode requires a different current coordinate and is not included in this inverse.

The retained equations and explicit background representation defects are

    b'=v+Ef,   v'=-2H*v-mu^2*b+Eb,
    u'=w,      w'=-2H*w-omega^2*u-k*z*v,
    mu'=r*mu, omega'=r*mu^2/omega, beta'=r*beta.

Ef and Eb are measured properties of the retained tabulated representation, not added physical forces. When evaluating saved data, b'=r*b_N and v'=r*v_N. No assumption r=H is made in those checks.

## 2. Exact two-frequency coordinates

Define

    C=b*u+v*w/(mu*omega),       S=v*u/mu-b*w/omega,
    U=b*u-v*w/(mu*omega),       V=-v*u/mu-b*w/omega.

In the unforced constant-coefficient oscillator limit H=r=Ef=Eb=z=0,

    C'=-delta*S, S'=delta*C, U'=-Sigma*V, V'=Sigma*U.

This is a local oscillator/principal-part control, not a self-consistent expanding universe with a nonzero scalar density and H=0. For arbitrary initial phases it separates the difference and sum frequencies exactly.

There are only TWO physical coordinates, not four. Put A=b^2+(v/mu)^2>0. Then

    u=(b*C+(v/mu)*S)/A,
    w=omega*((v/mu)*C-b*S)/A.

The (u,w)->(C,S) determinant is -A/omega. There is no division by b or v, and no H/mu condition is needed for this coordinate inverse. On (u,w/omega) the map is a scaled orthogonal reflection, with condition number exactly one. The coupled native metric constraint separately retains H>0.

With c2=(b^2-(v/mu)^2)/A and s2=2b*v/(mu*A),

    U=c2*C+s2*S, V=-s2*C+c2*S,
    C^2+S^2=U^2+V^2=A*(u^2+w^2/omega^2).

The fast part is therefore encoded in the same state and background phase, not an additional population or freely chosen component.

## 3. Derive, rather than fit, the retained sound coefficient

Let

    d=beta*mu*Sigma*C/2, q=beta*k*mu*S/2,
    c_s^2=delta/Sigma=k^2/Sigma^2,
    p_s=c_s^2*d.

Direct decomposition of the physical sources gives

    YD=d-beta*mu*delta*U/2,
    YQ=q-beta*k*mu*V/2,
    YP=c_s^2*d-beta*mu*Sigma*U/2.

The frozen slow equations are exactly d'=-k*q, q'=k*c_s^2*d. Hence the retained code's coefficient

    (k/mu)^2/(sqrt(1+(k/mu)^2)+1)^2

equals the quadratic difference-frequency coefficient, without fitting. It has c_s^2 approximately k^2/(4mu^2) for k/mu small. This derives the coefficient in that limit; it does not by itself derive the complete expanding closure c_s^2*(d+3H*q/k).

Equal C/S and U/V envelope norms imply a fast-to-slow density envelope ratio c_s^2. But the fast current envelope is as large as the slow current envelope, and the fast pressure envelope equals the slow DENSITY envelope. Small fast density is therefore insufficient to discard fast pressure/current.

For the preceding boundary-adapted variables, define S_b=beta*(b*w+v*u) and J=beta*b*v. Then

    S_b=-beta*(delta*S+Sigma*V)/2,
    WD=YD+(3H*S_b+k*z*J)/2,
    WQ=beta*k*(Sigma*S+delta*V)/4.

The slow part of WQ is Sigma/(2mu) times q; WQ is not the late current by a change of name. Rescaling WQ by 2mu/Sigma leaves a fast current term whose envelope is c_s^2 times q's envelope. These relations keep every term.

## 4. Restore expansion, metric forcing and representation exactly

Set Gamma=4H+r*(1+mu^2/omega^2), F=-k*z*v. Differentiating the coordinates gives

    C'=-delta*S-Gamma*(C-U)/2+Ef*u+Eb*w/(mu*omega)+v*F/(mu*omega),
    S'=delta*C-Gamma*S/2+r*(1-mu^2/omega^2)*V/2
       +Eb*u/mu-Ef*w/omega-b*F/omega.

Let Ld=beta*mu*Sigma/2, Lq=beta*k*mu/2,

    ad=r*(2+mu/omega)-Gamma/2, aq=2r-Gamma/2.

The exact source evolution is

    d'=-k*q+ad*d+Ld*Gamma*U/2
       -beta*k*Sigma*v^2*z/(2omega)+Ld*(Ef*u+Eb*w/(mu*omega)),
    q'=k*c_s^2*d+aq*q+Lq*r*(1-mu^2/omega^2)*V/2
       +beta*k^2*mu*b*v*z/(2omega)+Lq*(Eb*u/mu-Ef*w/omega).

Neither H' nor z' is required. Thus this exact pair supplies a simpler present-state implementation route than differentiating the earlier WD/WQ metric-dependent map. This stage checks the operator on saved data; it does not claim a newly integrated implementation of this pair.

Subtract the retained late formula d'_L=-3H*p_L-k*q-k*z, q'_L=-H*q+k*p_L, p_L=c_s^2*(d+3H*q/k). The remainder has four explicit groups:

    expansion_D=(ad+3H*c_s^2)*d+9H^2*c_s^2*q/k,
    expansion_Q=(aq+H-3H*c_s^2)*q,
    phase_D=Ld*Gamma*U/2, phase_Q=Lq*r*(1-mu^2/omega^2)*V/2,
    metric_D=k*z*(1-beta*Sigma*v^2/(2omega)),
    metric_Q=beta*k^2*mu*b*v*z/(2omega),
    representation_D=Ld*(Ef*u+Eb*w/(mu*omega)),
    representation_Q=Lq*(Eb*u/mu-Ef*w/omega).

Each is calculated from the retained equations/state, not fitted to the discrepancy. Their sum restores the exact rates. Comparing instantaneous rates alone would not fairly test an averaged late model; the original signed extraction is evaluated separately below.

## 5. Exact metric coupling and a nonzero phase-correlation term

In X=(d,q), the physical normalized source rows are

    YD=(1-c_s^2*c2)*d-(delta/k)*s2*q,
    YQ=(k/Sigma)*s2*d+(1-c2)*q,
    YP=(c_s^2-c2)*d-(Sigma/k)*s2*q.

Call the first row ell. If T maps (u,w) to X, the open operator is

    A_open=(T'+T*A_field)*T^-1,
    A_field=[[0,1],[-omega^2,-2H]],
    G=T*[0,-k*v]^T
     =[-beta*k*Sigma*v^2/(2omega), beta*k^2*mu*b*v/(2omega)]^T.

The actual flat native constraint separates the retained rest/slow source as

    z=z_rest+ell*X/(2kH*beta),
    X'=[A_open+G*ell/(2kH*beta)]X+G*z_rest.

This is inherited metric coupling with no new strength parameter. The saved whole state provides z_rest for diagnostic validation; a future live implementation must obtain it from the current rest state, not from saved future forcing.

For an explicitly limited angular control, hold H,mu,beta and E=beta*(v^2+mu^2*b^2)/2 fixed, set r=H, Ef=Eb=0, and average a uniform background phase while holding X and z_rest fixed. This is an algebraic operator average, not a physical ensemble or a proof that time evolution equals its averaged generator. Then

    <A_open>=[[-H*(1-mu/omega)^2/2, -k],
              [k*c_s^2, -H*(1+mu^2/omega^2)/2]],
    <G>=[-k*E*Sigma/(2omega),0]^T,
    <G*ell>/(2kH*beta)
      =diag(-E*Sigma*(1+c_s^2/2)/(4H*omega*beta),
            -E*delta/(8H*omega*beta)).

In particular,

    (<G*ell>-<G><ell>)/(2kH*beta)
        =-E*delta/(8H*omega*beta)*I.

This nonzero correlation is derived analytically and checked with independent 32/64-phase quadrature controls. It illustrates specifically why averaging the metric coefficient and density separately loses a term. It is not promoted to the actual signed-window correction or asserted to be the complete homogenized operator.

## 6. Original signed source extraction, not a new averaging rule

Use the original fixed L[f]=sum(w_i*f_i), including its negative weights. The pressure identity is

    L[YP]=c0^2*L[d]+L[(c_s^2-c0^2)*d]+L[fast_pressure].

The three terms are evaluated from the saved fields, with c0 the original coefficient. For rates, let A_L(t) denote the retained late operator acting on the candidate slow state. For the original center operator A0,

    L[X']=A0*L[X]+[-k*L[z],0]^T
          +L[(A_L-A0)*X]+L[exact_remainders].

This retains operator-state correlations and uses the original extraction; it does not commute that fixed functional with a new evolving time window. The center/rightmost-time transport and actual late background/selector remain separate contracts. Neither original projected density/current nor the code's matching state is silently replaced by L[d],L[q].

The baseline receives the actual CDM source/control, Yc=beta*Rc*delta_c with constant beta*Rc, Yc'=-beta*Rc*k*z, zero pressure/current. No imaginary scalar phase is assigned to it.
