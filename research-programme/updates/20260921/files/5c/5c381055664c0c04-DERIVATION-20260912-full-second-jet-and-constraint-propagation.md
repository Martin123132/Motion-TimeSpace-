# Full second jet: constructive trace repair and the remaining propagation problem

Private/local, 12 September 2026. This is a formal interior-time calculation
on the accepted N16 fixture, not an evolved spacetime or full local-GR claim.
The preceding cubic first-jet evidence is immutable and still valid in its
declared scope. No coupling, physical input field or dataset is fitted here.

## 1. Result in plain language

We derived and implemented the four coupled accelerations, including the
time derivative of the full inverse-time memory force. We did not simply
differentiate the zero-P-only evaluator as though it were a nonlinear theory.
The frozen first-jet spaces initially fail the next compatibility test in
BOTH matched GR+scalar and MTS. Two explicit canonical trace extensions fix
most of that failure without changing the initial physical fields.

| Maximum constraint acceleration | GR+matched scalar | MTS metric-Gram |
|---|---:|---:|
| Original frozen spaces, derived clock-rate candidate | 0.2087995222 | 0.2526939436 |
| Add mass acceleration trace family | 3.3388774e-5 | 0.0160452283 |
| Add mass AND scalar acceleration trace families | 5.9037271e-6 | 0.0061680981 |
| Joint extension, higher quadrature | 5.8952468e-6 | 0.0061680991 |

These are residuals in the existing fixture normalization, not observational
errors, physical parameter measurements, or evidence for a competitive fit.
All original phase directions and all 19 lapse-constraint rows remain.
Both branches retain the complete first-jet gates under higher quadrature.
The full second-jet gate remains FALSE in both branches; no evolution starts.

There is a new exact GR constraint-bracket derivation. It identifies the
small remaining GR residual as essentially a transported initial-constraint
moment, not a clock-rate parameter to fit. MTS has an additional residual
which that GR identity does NOT explain. Its full propagation identity is
the next derivation target, not another blind boundary or clock scan.

## 2. What is held fixed, and what is deliberately extended

The physical input is the final cubic first-jet attempt07: the same annulus,
N16 scalar/free auxiliary profile, original K_seed momentum conversion,
inner mass, boundary velocities, outer clock, kappa=0.1 and zero
Lambda/m_chi/b2/b3. The comparator contains the same rough scalar; it is
not vacuum GR or an unrelated smooth manufactured solution.

The explicitly integrated gravitational finite quadrature and its radial
boundary from the preceding checkpoint are retained. This does not transfer
its results back to the older finite quadrature or to N128.

The original accepted mass and scalar phase maps have 77 and 72 pairs.
The constructive joint extension adds two pairs to EACH: 79 mass and 74
scalar. Old value, gradient and momentum-map columns are retained exactly.
New maps are then frozen for this local time-germ calculation; no moving-map
transport is implicitly neglected.

The saved boundary data owns initial velocities, not a unique acceleration
history. Accordingly we report the compatible accelerations that an eventual
drive history would have to supply. Setting both drive accelerations to zero
was tested ONLY as a labelled affine-drive smoke assumption, not inherited
as a parent prediction. Neither the free-drive nor affine-drive scan passes
all the second-jet rows in the original frozen spaces.

## 3. Derive the second transport jet

Use subscripts 1 and 2 for actual first and second time derivatives, without
factorial normalization. All quantities in this section are evaluated on
P=0. Let

    F=1-2mu/R,   a0=kappa sqrt(F)/N,
    alpha=-mu_1/(R F)-N_1/N,
    a=c_t=a0 P_1,
    b=c_tt=a0(P_2+2 alpha P_1).

For each anchor, write J=T_s and L=T_ss. The flow equations give

    J_R=a J,             J(anchor)=1,
    (L/J)_R=b J,         L(anchor)=0.

Thus

    J=exp(integral a),
    L=J integral b J.

The second equation is used at endpoints and at every oriented link
quadrature point, rather than assuming J=1 or freezing its derivative.

With the inherited factor matrices and endpoint labels, define

    A=sum B_i chi_i,
    A_1=sum B_i J_i chi_1,i,
    A_2=sum B_i (L_i chi_1,i+J_i^2 chi_2,i),
    D=sum S_i J_i C_i,
    D_1=sum S_i (L_i C_i+J_i^2 C_1,i),
    C=R^2 N sqrt(F),
    C_1=R^2(N_1 sqrt(F)-N mu_1/(R sqrt(F))).

The current and its ANCHOR-time derivative are

    I_i=A(S_i C_i A_1-B_i chi_1,i D)/h,
    I'_i=A_1(S_i C_i A_1-B_i chi_1,i D)/h
        +A{S_i[J_i C_1,i A_1+C_i A_2]
             -B_i[J_i chi_2,i D+chi_1,i D_1]}/h.

The identities sum J_i I_i=0 and sum(L_i I_i+J_i I'_i)=0
are tested; the latter is essential to the cancellation of artificial
anchor jumps in the differentiated kernel.

For the physical-time kernel from the preceding nonlinear derivation,

    K_1(t0,R)=sum omega_i [
        (I'_i J_i+I_i L_i)/J_R^3
                   -2 I_i J_i L_R/J_R^4 ].

These are inverse-time powers THREE and FOUR. Differentiating a same-anchor
time expression instead would miss the physical-time measure derivative.

The nodal weights have derivatives

    d_1,i=sum_f S_fi A_f A_1,f/(h J_fi),
    d_2,i=sum_f S_fi/h [
        (A_1,f^2+A_f A_2,f)/J_fi^2
                   -A_f A_1,f L_fi/J_fi^3],
    (G_chi,i)_1=-sum_f B_fi/(h J_fi^2) [
        A_1,f D_f+A_f D_1,f-A_f D_f L_fi/J_fi].

The full coefficient derivatives c_mu, c_N, c_P and C_mu, C_N, C_P
are differentiated from their NONZERO-P formulas before setting P=0.
In particular

    (c_mu)_1=-kappa P_1/(R N sqrt(F)),
    (c_N)_1=-a0 P_1/N,
    (c_N)_2=-a0/N [P_2+2(-mu_1/(R F)-2N_1/N)P_1],
    (c_P)_1=a0 alpha,
    (C_P)_1=-2 kappa^2 R^2 N F^(5/2) P_1.

Neither the last nodal term nor the transport terms are dropped.

## 4. Triangular acceleration solve and full constraints

On a frozen canonical pair, the mass momentum equation first gives P_2
from the time derivative of the local mass Euler covector plus

    (G_mu)_1 = K (c_mu)_1
                  -sum delta_i [(d_i)_1 C_mu,i+d_i(C_mu,i)_1].

There is no K_1*c_mu contribution on P=0 because c_mu=0 there.
The scalar velocity equation similarly determines chi_2 without needing
the other accelerations:

    chi_2,strong = (N_1 sqrt(F) pi
          -N mu_1 pi/(R sqrt(F))+N sqrt(F) pi_1)/R^2
          +kappa N F^(3/2) P_1 chi_R.

These two solutions determine L, A_2, D_1 and the memory-force derivatives.
Then the mass velocity and scalar momentum equations determine mu_2 and
pi_2. Every step contracts the actual weak covectors with the full frozen
maps and solves the same canonical pairing matrices. Natural reaction rates
and the radial P-squared boundary are retained.

For C_2 the code differentiates all P-linear and P-squared terms, the
integrated gravity boundary and

    (G_N)_2=K(c_N)_2+2K_1(c_N)_1
        -sum delta_i [d_2,i C_N,i+2d_1,i(C_N,i)_1+d_i(C_N,i)_2].

The four accelerations are affine functions of the 19 N_1 coefficients.
The compatibility system contains all 19 C_2 rows, both P_2 endpoint rows
and the constant-outer-clock rate: 22 rows. The two drive accelerations
are outputs unless their parent histories are separately specified.

This is a FORMAL INTERIOR-TIME GERM. It assumes sufficient two-sided smooth
time coverage around t0 for the inverse maps. It does not turn the history
action into a causal IVP. The temporal boundary work derived previously is
not set to zero: applying these formulas at a terminal/initial history edge
requires an explicit support or boundary contract. N_2 and higher jets are
not fixed by the tests here, nor needed for these P=0 acceleration formulas.

## 5. Actual constructive repairs, not residual subtraction

The first frozen scan gives approximately 0.21/0.25 residuals. Clock-only
least-squares fitting cannot close them. In GR only three resolved directions
remain in that map; MTS has two additional weak directions. Using the latter
produces clock-rate magnitudes about 9,000-13,000 and still fails the full
gate. These numerical fits are retained as failed diagnostics, not accepted
physics or a reason to loosen the gate.

For every lapse test eta, differentiate the bulk mass velocity family at
fixed eta, using the actual initial field rates:

    M_eta = eta*kappa[
        F^(3/2)(pi_1 w+pi w_1)-3sqrt(F)mu_1 pi w/R]
      +kappa R F^(3/2)(F eta_R-eta F_R/2) P_1.

Take its 19 directions together with ALL 16 inherited first-memory-kernel
directions. A canonical dual-trace extension preserves the endpoint values
of this full 35-direction family while retaining old weak moments.
The scalar counterpart uses all 19 directions

    Q_eta=eta[sqrt(F)pi_1/R^2-mu_1 pi/(R^3 sqrt(F))
                            +kappa F^(3/2)P_1 w].

The N_1-only pieces already lie in the old first-rate families. The new
paired continuous coordinate lifts vanish at interior nodes; dual moment
conditions keep the old equations. The construction acts on the entire
source families, not fitted amplitudes of the two observed endpoint errors.

All 35 mass and 19 scalar directions are resolved and tested here; no
singular direction is discarded from either parent family. The resulting
canonical block pairing errors are below 2.8e-15 and family trace errors
below 3.4e-16. Pair condition numbers remain about 1.664 and 1.001.
All initial physical fields remain unchanged. The first jet is recomputed,
including ALL scalar and mass rates before differentiating it again.

Solving just the two P_2 traces and the clock rate after this extension
requires ordinary lapse-rate amplitudes, with max sampled N_1 about
0.000305 (GR) and 0.000317 (MTS), not the huge failed-fit values.
The primary P_2 endpoint residuals are below 6e-17 in both branches.
Higher quadrature gives up to 1.65e-10 (GR) and 7.79e-10 (MTS): this DOES
NOT pass the declared 1e-10 second-boundary gate at both quadratures.
There is no claim that second boundary compatibility is fully certified.

The joint extension leaves these inferred initial drive accelerations:

| Required derivative of drive | GR+scalar | MTS |
|---|---:|---:|
| Inner mass velocity derivative | 0.0131353136553 | 0.0111078161801 |
| Outer scalar velocity derivative | 0.0560273072643 | 0.0770085889469 |

They are compatibility outputs in fixture units, not inherited parent data
and not predictions in physical units. A future common prescribed drive
history still needs a paired compatibility solve.

## 6. Exact GR constraint-propagation derivation

Before radial boundary/interface terms, write the GR Hamiltonian density as
N A+N_R B. Define

    a=A_mu-partial_R A_muR,     b=B_mu-A_muR,
    c=A_P,                     d=B_P,
    e=A_pi,                    f=A_w.

The canonical bracket of H[eta] and H[N] has coefficient

    a*d-b*c+e*f = -kappa F^(3/2) P C_bulk.

This equality is verified EXACTLY from the full nonlinear action, including
all P-squared terms, using symbolic differentiation and simplification.
It implies, for smooth compactly supported tests with the relevant regularity,

    {H[eta],H[N]} = integral (eta N_R-N eta_R)
                                      [-kappa F^(3/2) P C_bulk],
    C_2[eta]|P=0 = integral zeta_eta C0,
    zeta_eta=kappa F^(3/2) P_1(eta N_R-N eta_R).

Radial boundaries and interfaces must be added for noncompact or broken
tests; they are NOT dropped when comparing the finite result. N_1 does not
appear in the displayed interior second-constraint law at P=0. This is the
reason another lapse-rate fit cannot erase these initial-constraint moments.

The accepted finite mass profile solves the original 19 weak C rows, but
its sampled GR strong C0 has maximum about 0.02067. Vanishing those 19
moments does NOT imply vanishing the newly generated zeta moments.
The largest computed transported moment is about 5.8898763e-6. After the
joint trace repair and explicit remaining boundary-flux subtraction, it
explains the full GR C_2 vector within about 3.13e-9, at both quadratures.

This supplies a precise next GR initial-data requirement: solve C0 in a
constraint-transport-closed test family (including the generated moments),
or use a consistently represented solution of the sourced continuum radial
constraint. Simply declaring the old 19-row solution exact everywhere is
not valid. Repreparation would be a new explicit branch with all first-jet
and common-drive checks repeated, not an overwrite of the current datum.

## 7. What remains in MTS, and what does NOT explain it

The derived endpoint memory identity is K_b=sigma_b chi_t,b G_chi,b,
with sigma=(-1,+1), since the endpoint S weights vanish. Differentiating
the full parent mass flux, using the actual chi_2 and G_chi,1, gives a
remaining mass acceleration trace mismatch below 4.25e-10 after joint
completion. Its lapse-covector contribution is below 3.93e-8.

Subtracting that boundary contribution still leaves about 0.00616806 in
MTS. It is therefore WRONG to describe the remaining discrepancy as the
same large boundary-projection defect we have just repaired.

We explicitly tested the conjecture that the GR bracket could simply use
the full nodal initial constraint C0_bulk-sum delta_i R_i^2 sqrt(F_i)d_i.
Its nodal correction is only about 2.65e-8; the mismatch remains 0.00616217.
That shortcut is rejected for this calculation. The MTS history-sector
constraint-propagation identity has NOT been proven by the GR calculation.
The remaining term must be derived and separated into finite projection,
history/nodal variational contributions and any genuine parent-action issue.

There is nevertheless an explicit new representation useful for that task.
Choose global primitives

    g_R=a0 P_1,
    B_R=b exp(g),
    U_i=I'_i exp(g_i+2g_anchor),
    V_i=I_i exp(g_i+g_anchor).

Let c_cell=sum omega_i V_i and
d_cell=sum omega_i[U_i+V_i(B_i+B_anchor)]. Anchor jumps cancel, so these
coefficients are cellwise constant. The REGULAR part of the differentiated
P-memory force is exactly represented, under the stated transport contract, by

    (G_P)_1,bulk = a0 exp(-3g) d_cell
                 +a0[alpha exp(-2g)-2B exp(-3g)] c_cell.

The separate nodal term -d_i(C_P,i)_1 is still retained. On the actual
repaired fields, this independent global-primitive representation matches
the oriented-link weak force derivative within 1.17e-11 (primary) and
8.42e-12 (higher); anchor cancellation errors are below 1.25e-16.
This is not yet a phase completion for the entire N_1 response family:
B depends on the actual P_2 and must be recomputed if the phase maps change.
Do not fit two carriers to one failed result and call the history problem solved.

## 8. Independent validation and preserved failures

- All four GR acceleration covectors independently follow from derivatives
  of the actual finite action, with coefficient errors at most 2.97e-13.
- For MTS, a separate Taylor inverse-time evaluation of the nonlinear
  metric/scalar covectors verifies all four accelerations to 5.69e-13.
  The G_P and G_chi time derivative checks give 2.17e-18 and 1.60e-14.
- Independent actual-action C_2 time differences with Richardson cancellation
  agree within 8.59e-7 (GR) and 4.86e-7 (MTS) on the original frozen case.
  These checks resolve the large failure, not a 1e-10 second-jet certificate.
- The first operator attempt stops on complex-array in-place casting during
  the derivative audit. The replacement changes that addition only.
- The first independent-control attempt uses an insufficiently small raw
  second-difference step; its errors scale by four when the step is halved.
  The replacement performs explicit Richardson cancellation, not a larger
  acceptance threshold. The original failed control is retained.
- The mass-only trace extension is a diagnostic intermediate. It predates
  refreshing all scalar rates after phase extension. The joint final branch
  refreshes all four rates and is the owner for further work.

Key evidence, relative to post-checkpoint-work:

- `scripts/annular_frozen_second_jet_complex_20260912.py`
- `scripts/derive_annular_frozen_second_jet_complex_20260912.py`
- `scripts/verify_annular_full_second_jet_action_20260912.py`
- `scripts/annular_acceleration_trace_completion_20260912.py`
- `scripts/derive_annular_joint_acceleration_trace_completion_20260912.py`
- `scripts/verify_annular_acceleration_trace_and_memory_carrier_20260912.py`
- `scripts/derive_annular_second_constraint_owner_20260912.py`
- `source-intake/navier-stokes/20260912/annular-frozen-second-jet-attempt02/status.json`
- `source-intake/navier-stokes/20260912/annular-frozen-second-jet-control-attempt03/status.json`
- `source-intake/navier-stokes/20260912/annular-acceleration-trace-completion-attempt02/status.json`
- `source-intake/navier-stokes/20260912/annular-acceleration-memory-control-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-second-constraint-owner-attempt01/status.json`
- `DERIVATION-20260912-full-second-jet-and-constraint-propagation.md`

The final integrity seal also preserves every failed/intermediate attempt,
script snapshot and numerical archive, together with an immutable resume
snapshot. Completion of that seal means the checkpoint is recorded and
validated in its stated scope, NOT that the second jet or the theory passes.

## 9. Next target, narrowly enough to make progress

Derive the MTS second-constraint Ward/propagation identity from the full
nonlinear history action, preserving inverse-time, nodal, radial/interface
and temporal-boundary terms. Use the exact GR bracket as the control and
the constructed two-carrier formula for the memory derivative. Compare that
identity with the repaired frozen weak operator to identify the owner of the
remaining 0.00616 term. Do NOT presume it is another endpoint defect.

Then prepare constraint-transport-compatible initial data and/or the derived
missing phase directions as indicated by that identity, with the same paired
GR and prescribed-drive checks. No automatic finer grid, no old failed
trajectory, no gauge-only retry and no physical-claim promotion.

One BelowNormal single-core worker at a time; no subagents, GitHub, galaxy
or frozen-workbench edits. This turn uses only local post-checkpoint-work.
