# Second adiabatic frequency, stress and a solution bound

## 1. Imported method; retained-action specialization

The WKB frequency construction is established mathematics, not an MTS discovery.
For background on its use for scalar fields on FLRW, see section4 of
[Moreno-Pulido and Sola Peracaula, EPJC80 (2020)692](https://link.springer.com/article/10.1140/epjc/s10052-020-8238-6).
Only the mode/WKB method is used here: their vacuum-energy/renormalization
claims and nonminimal couplings are NOT imported into the retained action.

The retained positive canonical scalar gives, in conformal time,

    q=a phi, mu=am, H=a'/a,
    q_k'' + Omega_k^2 q_k=0,
    Omega_k^2=k^2+mu^2-H'-H^2.

For v_W=exp(-i integral W d tau)/sqrt(W), direct differentiation yields

    v_W''+Omega_k^2 v_W = R_W v_W,
    R_W=Omega_k^2-W^2- W''/(2W)+3(W'/W)^2/4.

The zeroth frequency omega=sqrt(k^2+mu^2) leaves the previously measured
second-adiabatic residual. Cancelling it derives

    W2=omega + [-H'-H^2-omega''/(2omega)
                 +3(omega'/omega)^2/4]/(2omega).

This is an asymptotic frequency, not the exact nonlinear frequency equation.
Its positivity must be checked on the domain of use.

For the preserved constant-conformal-H probe,

    W2 = omega - H^2(3mu^4+12mu^2 k^2+4k^4)/(8omega^5),
    W20 = mu-3H^2/(8mu).

No coefficient is fitted. For variable H, retain the explicit H' term and
all derivatives it induces; the constant-H certificate below is not portable
without that work.

## 2. Carry source normalization and background pressure together

Let W0 be the homogeneous carrier frequency, Wk the sideband frequency,
L0=-H-W0'/(2W0), Lk=-H-Wk'/(2Wk). Let the physical homogeneous amplitude be
F proportional to1/(a sqrt(W0)). Then

    R'=gamma R+(Wk-W0) I,
    I'=gamma I-(Wk-W0) R,
    gamma=(W0'/W0-Wk'/Wk)/2.

Project the real-field stress onto the carrier difference-frequency terms.
With D=W0^2+mu^2+L0^2,

    delta=2[(L0 Lk+W0 Wk+mu^2)R+(L0 Wk-W0 Lk)I]/D,
    Pi=2[(L0 Lk+W0 Wk-mu^2)R+(L0 Wk-W0 Lk)I]/D,
    u=2k(L0 R-W0 I)/D,
    S=-mu u/k=2mu(W0 I-L0 R)/D,
    w_background=(W0^2+L0^2-mu^2)/D.

The background is not exactly dust at this order. Here u=q_momentum/rho
uses the retained source convention; it is (1+w_background) times the
velocity potential. Confusing the two would lose another order-dependent
normalization. These formulas define a matrix T mapping(R,I) to(delta,S).

The parent symplectic weight in these physical source coordinates is

    Sigma = (2Wk/W0)/det(T),

relative to the homogeneous canonical occupation normalization. For W=omega,
H->0 it reduces to the earlier1+r. For nonzero H it is computed from the same
source map, not imposed independently. With
A=(T'+T B) T^-1, B=[[gamma,Wk-W0],[-(Wk-W0),gamma]],
trace(A)=-Sigma'/Sigma follows from the Wronskian.

Consequently P=Sigma*S is canonical with coordinate delta. This constructs
the quadratic source-coordinate action from the oscillator map: if C maps
(delta,S) to(delta,P), A_can=(C'+C A)C^-1 has trace zero and
K_can=-J A_can is symmetric for J=[[0,1],[-1,0]].
It is the action of the stated WKB-derived approximation, with its error
controlled separately, not an asserted exact nonlinear parent reduction.

## 3. Avoid subtracting nearly identical carrier frequencies

Set w=sqrt(1+y), y=k^2/mu^2, epsilon=H^2/mu^2. The stable beat expression is

    W2k-W20 = mu*y/(w+1) *
      [1+epsilon*(3w^4-w^3-w^2-5w-5)/(8w^5)].

Do not calculate two nearly equal frequencies and subtract them at small k.
Likewise factor logarithmic-rate differences and mixed source coefficients
before numerical evaluation. Preserve the existing zero/long-wave context.

## 4. Residual-to-solution control includes quadrature mixing

Choose real template columns
u=cos(theta)/sqrt(W), v=sin(theta)/sqrt(W), theta'=W.
Their Wronskian is1. They solve an oscillator with squared frequency
Omega^2-R_W. For the exact oscillator on the same supplied background, write

    [q,q']^T = Y_W(tau) c(tau).

Variation of constants gives a rank-one coefficient generator with Euclidean
operator norm |R_W|/W. Therefore, for the SAME initial q and q',

    ||c(tau)-c(tau0)|| <= (exp(B)-1)||c(tau0)||,
    B=integral |R_W|/W d tau.

This controls arbitrary real initial quadratures, including their mixing.
It is not an assumption that the negative-frequency part stays identically
zero. The norm is the declared oscillator-coefficient norm, not an
unqualified relative error in every near-zero pressure or density component.

For 0<=B<1, exp(B)-1<=B/(1-B), giving a completely rational upper certificate.
It does not control floating-point implementation errors or uncertainty in
the supplied background.

## 5. Exact rational enclosure for the preserved probe

Use s=ln(a/a0), y=k^2/mu^2, epsilon=H^2/mu^2 and define

    P(y)=3+12y+4y^2,
    D(y,epsilon)=8(1+y)^3-epsilon P(y),
    f=W2/mu=D/[8(1+y)^(5/2)],
    L=W2'/(H W2)
      =1+5y/(1+y)-2(y D_y+epsilon D_epsilon)/D.

Direct substitution gives

    R2/mu^2=1+y-epsilon-f^2
             +epsilon[L^2/4+y L_y+epsilon L_epsilon]
           =epsilon^2 Q(y,epsilon)/[64(1+y)^5 D^2].

The script derives the exact integer-coefficient polynomial Q, then bounds
its absolute value by the sum of absolute monomials on the frozen rational
rectangle. D>=8-E P(Y)>0 and (1+y)^5>=1 provide an elementary denominator
lower bound; no sampled maximum is treated as a supremum.

With the verified physical box, use
Delta tau<=.001/.0012, mu<=1510 and
W2>=1490[1-E P(Y)/8].
These produce a common bound on B for the background and every saved mode.
The old W=omega template receives its own bound using the same domain,
initial-data rule and coefficient norm.

This certificate concerns the controlled unforced constant-H oscillator.
Projecting stress, choosing an actual nonlinear realization, imposing the
full metric constraints and evolving a galaxy are separate steps. Bounds on
projected near-cancelling observables must propagate their condition numbers.
