# Parent action, affine state plane and metric-dependent reduced dynamics

Use the retained real canonical scalar, c=hbar=1, conformal H=a'/a,
mu=am, and the same Newtonian scalar metric potentials. No matter or
gravitational normalization is chosen from a fit in this derivation.

## 1. Restore the metric terms before asking gravity to respond

Write phi=phi0+y, v=phi0', C=Psi+3Phi, Dm=3Phi-Psi. For lapse
N=a sqrt(1+2Psi), spatial metric h_ij=a^2(1-2Phi)delta_ij and independent
ADM shift N^i, the exact parent matter density is

    N sqrt(h)/2 [(phi'-N^i partial_i phi)^2/N^2
                 -h^ij partial_i phi partial_j phi-m^2 phi^2].

Its quadratic perturbation part is

    L2 = a^2/2 [y'^2-(k^2+mu^2)y^2]
         -a^2 C v y' +a^2 mu^2 Dm phi0 y
         +a^2/2 [3/2 (Psi+Phi)^2 v^2
            -mu^2(3/2 Phi^2-3Psi Phi-Psi^2/2)phi0^2]
         -a^2 v N^i partial_i y.

The previously retained forced scalar action is its y-dependent part.
The restored pure-metric terms are fixed by the SAME action, not new
operators. The shift is kept independent until its momentum variation;
fixing it first would discard a constraint source.

Define scaled background B=(v^2+mu^2 phi0^2)/2,
Pb=(v^2-mu^2 phi0^2)/2 and physical linear sources

    E=v y'-v^2 Psi+mu^2 phi0 y,
    Pr=v y'-v^2 Psi-mu^2 phi0 y,
    momentum_i=v partial_i y.

Then the exact quadratic variations obey

    partial L2/partial Psi=-a^2[E-C B],
    partial L2/partial Phi=-3a^2[Pr+(Psi-Phi)Pb],
    partial L2/partial N^i=-a^2 momentum_i.

The background measure terms matter. Varying only the y-dependent forcing
action would give the wrong metric sources. The existing Einstein action
and all other species still need their own variations; these equations
restore this scalar's matter-side sources, not all Einstein constraints.

## 2. Pull back the actual scalar phase-space action

Let the complex carrier B0=A0 exp(-i theta0), A0^2=1/W0, represent the same
two real quadratures. It is a normalization convention, not a halo population.
Write F=B0 Z, Z=R+i I, lambda_j=L_j-i W_j, L_j=-W_j'/(2W_j).
Let D be a complex metric-dependent affine response and impose the state
plane F'=lambda_k F+D B0. The canonical momentum still subtracts
f1=C(B0'-H B0). Define

    Eaff=D-C(lambda0-H),
    Jforce=H C(lambda0-H)+mu^2 Dm,
    Omega_j^2=j^2+mu^2-H'-H^2,
    R_j=lambda_j'+lambda_j^2+Omega_j^2.

For this WKB convention R_j is real. Divide the averaged parent action by
the carried homogeneous normalization nbar=A0^2 W0/2 (1/2 in the unit
template). Its pulled-back wave part is exactly

    Lpull = 1/W0 { Re[(lambda_k Z+Eaff)^*(Z'+lambda0 Z)]
                  -[|lambda_k Z+D|^2+Omega_k^2|Z|^2]/2
                  +Re[Jforce^* Z] }.

This formula is taken from P q'-Hamiltonian, not reverse-engineered from a
desired fluid equation. The omitted-from-this-line metric-only contribution
is restored below, and all boundary terms are explicitly retained.

Let Delta=Wk-W0 (evaluate via the stable beat), gamma=Lk-L0,
Jz=2Wk/W0, S0=C'(lambda0-H)-2mu^2Psi, and

    epsilon=D'+(lambda0+lambda_k)D-S0.

Algebra and one time integration by parts give

    Lpull=Jz[I R'-Kz]+boundary',
    Kz=Delta(R^2+I^2)/2+gamma R I+D_R I-D_I R
       +R_k(R^2+I^2)/(4Wk)
       +[(epsilon_R-C R_0)R+epsilon_I I]/(2Wk)
       +|D|^2/(4Wk),
    boundary=Lk(R^2+I^2)/(2W0)-Wk R I/W0
             +(Re Eaff R+Im Eaff I)/W0.

Because Jz'/Jz=-2gamma, variation produces

    Z'=[gamma-i(Delta+R_k/(2Wk))]Z
        +D-i epsilon/(2Wk)+i C R_0/(2Wk).

The epsilon correction is derived by varying the pulled-back parent action.
It is not a coefficient adjusted to make conservation work. Exact dynamic
invariance of the imposed plane requires epsilon=-R_k Z for the physical
KG equation (and an on-shell background). In the W2 approximation these
defects must be bounded or retained; a restricted variational trajectory is
not automatically the same as the unrestricted four-real-coordinate field.

The free homogeneous solution of D'+(lambda0+lambda_k)D=S0 remains an
independent initial datum. A retarded prescription would need its actual
earlier history. No local truncation proves that datum vanishes.

## 3. The next term is fixed by the same response equation

For A=lambda0+lambda_k,

    D0=S0/A,
    D1=-D0'/A=-S0'/A^2+S0 A'/A^3.

D0 alone has epsilon=D0'. D0+D1 has epsilon=D1', where

    D1'=-S0''/A^2+3S0'A'/A^3+S0 A''/A^3-3S0(A')^2/A^4.

These are local adiabatic approximations to a response with an undetermined
free component. Source/background derivatives must come from their equations.
For the numerical check, local Taylor coefficients follow the retained
background ODE and the original metric cubic, not finite differences of
quantized outputs. Saved interpolation errors remain separate.

## 4. Density/current coordinates inherit a weight and an affine shift

Let a0=L0-H, ak=Lk-H, Db=W0^2+mu^2+a0^2. The exact plane source map is

    x=(delta,S)^T=T(R,I)^T+(b,0)^T,
    T=2/Db [[a0 ak+W0 Wk+mu^2, a0 Wk-W0 ak],
             [-mu a0, mu W0]],
    b=2(a0 D_R-W0 D_I)/Db-(1+wbg)Psi,
    wbg=(W0^2+a0^2-mu^2)/Db.

The pressure row replaces +mu^2 in T00 by -mu^2 and retains the same b.
The determinant is

    det T=4mu[Wk(W0^2+a0^2)+W0 mu^2]/Db^2>0,
    Jx=Jz/det T.

This is the actual parent symplectic normalization. In the flat limit
Jx=2w/(w+1)=1+r, w=omega/mu, r=(w-1)/(w+1), recovering the earlier result.
The parent normalization nbar multiplies Jx; it must not be dropped when
coupling to gravity or used to select a halo occupation.

If z'=Az z+fz is the real form of the action flow, then

    Ax=(T'+T Az)T^-1, fx=T fz+bvec'-Ax bvec,
    trace Ax=-Jx'/Jx.

Up to the explicitly tracked coordinate boundary, the density action is

    Lx=Jx[S delta'-Kx],
    Kx=-Ax10 delta^2/2+Ax00 delta S+Ax01 S^2/2
         -fx1 delta+fx0 S.

It carries the coordinate connection and source shift together, rather than
multiplying an old unforced action by a guessed weight. Metric-only terms
are not supplied by this trajectory-level Kx and must be kept separately.

## 5. What must accompany any later metric variation

The carrier average of the pure-metric parent term, divided by nbar, is

    Lmetric = 1/(2W0) {3/2(Psi+Phi)^2[(L0-H)^2+W0^2]
                  -mu^2[3/2Phi^2-3Psi Phi-Psi^2/2]}.

The shift source is still obtained from the unreduced action before fixing
N^i=0. Also retain the |D|^2 term and coordinate boundaries above. D0 and
D1 depend on the metric and its derivatives; an exact eliminated response
depends on past metric history. Varying gravity while artificially holding
D fixed would omit its response. The uneliminated parent scalar plus these
derived sources is the clean reference for the next coupled metric test.

This derivation uses standard canonical reduction and minimal coupling on
the existing MTS quadratic subfamily. It imports no constructive-QFT theorem,
mass gap, new gravitational normalization, or population closure.
