# Conjugate partners and the matter-current identity

16 November 2026. This is a bounded completion of the previous synthetic
fixed-flat interface, not new cosmological evolution. Reuse its three saved
fixtures, coefficients, engineering guards and 1e-10 identity tolerance.

## 1. Complete the ordered conjugate tensors

For each pair of distinct all-left fermion multiplets, write the already
tested local tensor as psi_L^T B(H) psi_R. B contains the spin charge-conjugation
matrix C, the color contraction and the appropriate weak/Higgs contraction.
The three pairs are (Q,uc), (Q,dc), (L,ec). Their independent barred partner is

    Y = y psi_L^T B(H) psi_R,
    Ybar = y* bar_psi_R B(H)^dagger bar_psi_L^T.

Thus the ordering is REVERSED for the partner. For example,

    Ybar_up = y_up* sum H_j* epsilon_ij* bar_uc_(b,c)
                       (C^dagger)_ba bar_Q_(a,c,i).

The down/lepton partners instead contain H_i. The bars are independent
Euclidean Grassmann rows, not the complex conjugates of the projected
columns. This prescription conjugates the coefficient tensor and reverses
Grassmann order; it does not assert reflection positivity or that the
Euclidean probe action is real. We use commuting witnesses for the ordered
multilinear coefficients, not a simulation of fermion expectation values.

Under a site transformation G, columns transform by G_R and rows by G_R^-1.
The conjugate tensors are invariant because the already verified tensor
intertwiner is conjugated and its factor order reversed. Merely using y
instead of y* would still preserve gauge symmetry, so coefficient-conjugacy
must be checked separately from the Ward identity.

Let P=P_hat_minus[U] and Pplus=(1+gamma5)/2, with the retained overlap D.
Use redundant ambient coordinates

    psi=P eta,  bar_psi=zeta Pplus,

where eta and zeta are independent. They are a convenient way to evaluate
the constrained-field action, NOT a chosen integration basis or measure.
Gauge transformations act on eta,zeta by the same representations.

The matter action is S_fermion+Y+Ybar+S_Higgs. The pure gauge action, separately
gauge invariant, is excluded when defining the MATTER source current.
Adding the retained synthetic neutral bath gives the second comparison case.

## 2. Derive the local off-shell Ward identity

Use anti-Hermitian generators T_a. For each oriented link from x to x+mu,
define the LEFT-trivialized matter response

    J_act(x,mu,a) = d/dt S_matter(exp(t T_a)U_mu(x); eta,zeta,H) at t=0.

A site gauge variation omega(x) induces

    delta U_mu(x) = omega(x)U_mu(x)-U_mu(x)omega(x+mu).

It follows, by collecting incoming and outgoing coefficients, that

    (D^- J_act)^a(x) =
      sum_mu [J_act^a(x,mu)
        - sum_b Ad[U_mu(x-mu)]_(b,a) J_act^b(x-mu,mu)].

Define E_gauge^a(x) by varying only the fields at that site at fixed links:

    delta eta = T_a eta, delta zeta = -zeta T_a,
    delta H = T_H,a H, delta H* = T_H,a* H*.

The action is invariant under the combined variation, hence coefficient by
coefficient in omega,

    BOXED: (D^- J_act)^a(x) + E_gauge^a(x) = 0.

E_gauge is a sum of Euler-Lagrange expressions multiplied by the corresponding
field variation. Therefore on a stationary charged-field configuration it
vanishes, and covariant current conservation D^-J_act=0 follows. On arbitrary
saved probes neither term need vanish: test their cancellation, not the false
off-shell assertion that the divergence is zero.

This argument uses even gauge variations and preserves the order of each
Grassmann monomial, avoiding an implicit choice of left/right odd derivative.
In code, gradients of commuting coefficient witnesses evaluate those ordered
directional variations. They are not an on-shell quantum state.

The neutral bath has no gauge link or charged-field argument at this fixed
metric. Its J_act and E_gauge contributions are both zero. The SAME identity
therefore holds with the bath added. This says nothing about removing its
metric stress or its gravitational interaction.

## 3. The link derivative must include projector motion

Set K=H_W=gamma5(D_W-I), S=sign(K), so D=I+gamma5 S and P=(I+S)/2.
For K=V diag(lambda) V^dagger with a nonzero kernel gap,

    delta S = V [F elementwise (V^dagger delta K V)] V^dagger,
    F_ij=(sign(lambda_i)-sign(lambda_j))/(lambda_i-lambda_j).

F is zero for equal-sign pairs, including coincident eigenvalues. No arbitrary
denominator clipping is needed across opposite signs because of the gap.
This is the Frechet derivative, obtained by differentiating the spectral
functional calculus; it is not a fit to numerical link changes.

At fixed eta,zeta,H, for each multiplet,

    delta S_matter =
      bar_psi gamma5 (delta S) psi
      + (bar_psi D + Y_psi) (delta S) eta / 2.

Only the holomorphic Yukawa terms contribute Y_psi here; the barred fields
use the fixed projector Pplus. Form the matrix

    W = psi (bar_psi gamma5) + eta (bar_psi D + Y_psi)/2.

The Frechet map is symmetric under the bilinear trace pairing, so

    delta S_matter = Tr[L_sign(W) gamma5 delta D_W].

This makes an efficient independent link-current construction: compute the
matrix sensitivity once per multiplet, then contract its small endpoint
blocks with each Wilson-link derivative. Current is not manufactured by
setting it equal to minus the Euler contact term.

The Higgs current is the derivative of its forward-link kinetic norm.
Its potential contributes to the field gradient but is gauge invariant.
The code assembles current divergence and Euler contacts by separate routes
at every site and all 12 gauge generators. It also evaluates current without
the delta P term as a deliberately broken control.

## 4. What is kept separate

J_act above is a CLASSICAL ACTION derivative. It is not the fermion measure
current in [Craig's construction](https://arxiv.org/html/2610.09093v1).
For a quantum functional integral the variation includes delta log(dmu)
as well as -delta S. Establishing the required measure phase/global-loop
conditions is a distinct task. Passing this identity does not set that
Jacobian to zero or independently replay the external theorem.

The existing global-group choice, finite flat geometry and engineering
plaquette guard are unchanged. No continuum mass, coupling, charged
population or new cosmological score is derived here.

## 5. Frozen test procedure

- Load the three original fixtures read-only and verify the previous seal.
- Check the three barred partners, their conjugate coefficient/order relation
  and full matter-action covariance under the saved strong gauge transforms.
- Build J_act by the spectral derivative and explicit Wilson/Higgs link
  contractions; form D^-J independently of the field-contact expression.
- Check all16 sites x12 generators, for matter and matter-plus-bath, before
  and after the saved gauge transformations.
- Independently compare three representative link currents with symmetric
  eighth-order finite differences at the two steps frozen in protocol.json.
  Both matter and bath-added actions must use the same1e-10 gate.
- Omit projector motion, or give barred rows the wrong transformation sign:
  require detectable failure above the existing1e-6 floor.
- Keep a zero-charged-field control explicitly labelled trivial; arbitrary
  neutral fields alone must not manufacture a gauge current.
- Preserve any failure; never reroll fixtures or relax a tolerance.
- One worker/thread, CPU4 below-normal, ten-minute guard. No active goal,
  GitHub, handoff, new fitting, parallel subagents or unbounded lattice run.
