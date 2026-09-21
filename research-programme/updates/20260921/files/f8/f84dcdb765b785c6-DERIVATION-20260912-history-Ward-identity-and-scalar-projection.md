# History Ward identity: the missing propagation term is identified

Private/local, 12 September 2026. This continues
`DERIVATION-20260912-full-second-jet-and-constraint-propagation.md`.
No GitHub action, physical-input refit, evolution, black-hole solution,
interval certificate, or full physical GR-limit claim.

## 1. Result and working-branch decision

The nonlinear history action has an interior time-coordinate Ward identity.
Its connection current, nodal coefficient work, and inverse-time factors
cancel as required; the time derivative contains **3 c_t K_t**, not 2.
The complete GR-plus-scalar canonical identity is independently verified
symbolically at nonzero P, off shell. Combining the two gives the conditional
continuum constraint-propagation identity for this particular action sector.

The previously unexplained finite MTS second-constraint residual is not a
demonstrated failure of that identity. On 17 independent zero-endpoint lapse
tests it is accounted for by transported initial-constraint moments,
unresolved Euler work in the finite phase spaces, and explicit radial-action
work. The reconstruction error is below 3.73e-13 at both quadratures.
The dominant unresolved Euler work is scalar, not a new unsourced coupling.

An actual frozen scalar gauge-family enlargement was also constructed and
the coupled equations were recomputed. It worsens the full 19-row Cddot
residual, in both MTS and matched GR. It is **rejected as a repair**. The
working branch remains the preceding joint acceleration-trace attempt02;
none of its fields, maps, scripts, or certificates was overwritten.

The new result is a propagation derivation and source identification, not
the missing on-shell solution. In particular, finite weak equations do not
allow us to set their distributional residuals to zero on arbitrary tests.

## 2. Exact history identity before imposing field equations

Use the definitions and temporal-window contract in
`DERIVATION-20260912-nonlinear-history-Euler-equations.md`. Write

    delta S_G = integral dt [integral dR K delta c
                 - sum_i d_i delta C_i + sum_i G_chi,i delta chi_i]
                 + retained temporal-window work.

Here C_i is the principal coefficient R_i^2 N_i sqrt(F_i)(1-u_i),
not the lapse constraint; d_i is the inverse-time nodal density. The K
kernel includes oriented links and inverse physical-time evaluation.

Under an active time relabelling H(t,R)=t+epsilon(t,R), R fixed, the
previous exact conjugacy construction gives

    delta c   = epsilon c_t - epsilon_R - c epsilon_t,
    delta C   = epsilon C_t + C epsilon_t,
    delta chi = epsilon chi_t.

Inserting these variations and integrating their derivatives yields

    K_R + c K_t + 2 c_t K
        + sum_i delta(R-R_i) [C_i (d_i)_t + G_chi,i (chi_i)_t] = 0.   (W)

This is an interior physical-time distributional identity, with endpoint
node distributions retained. The temporal boundary must instead be kept
explicit if the variation reaches the transported time-window edges. The
known action transformation there is -[sum_f epsilon_f A_f^2 D_f/(2h)];
the general variation also carries the previously derived Y=delta T work.
No causal initial-value interpretation follows from this covariance result.

On P=0, let a=c_t and b=c_tt. Differentiate W before restricting:

    (K_t)_R + 3 a K_t + 2 b K
      + sum_i delta_i [C_i,t d_i,t + C_i d_i,tt
                       + G_chi,i,t chi_i,t + G_chi,i chi_i,tt] = 0.  (W1)

The extra a K_t comes from differentiating c K_t even though c itself
vanishes on the initial slice. Dropping it is detectably wrong.

### Exact endpoint and anchor checks

For one link, using its existing I, J=T_s and L=T_ss,

    jump_node K   = -I/J,
    jump_node K_t = -I_s/J^2 + I L/J^3.

The nodal sources in W and W1 are respectively I/J and
I_s/J^2-I L/J^3. These equalities are checked symbolically with independent
A,A_s,A_ss,D,D_s,C,C_t,J,L,chi_t,chi_tt. Shared-anchor jumps cancel using
sum_i J_i I_i=0 and its time derivative; they are not discarded individually.

On the actual N16 data, all 19 original lapse tests give

| Check | Primary maximum | Higher maximum |
|---|---:|---:|
| W, including endpoint distributions | 2.75e-16 | 2.70e-16 |
| W1, including inverse-time factors | 2.95e-13 | 2.92e-13 |
| Wrong coefficient 2 instead of 3 | 2.38e-6 | 2.38e-6 |

## 3. Pullback to the canonical variables

Let beta=kappa N F^(3/2)P and u=kappa^2 F^2 P^2. The metric
ds^2=-N^2 dt^2+F^(-1)(dR+beta dt)^2 fixes the transformations

    delta mu = epsilon mu_t + R F beta epsilon_R,
    delta N  = epsilon N_t + N epsilon_t - N beta epsilon_R,
    delta P  = epsilon P_t - N(1-3u)/(kappa sqrtF) epsilon_R,
    delta chi= epsilon chi_t,
    delta pi = epsilon pi_t + T epsilon_R,
    T = N sqrtF R^2 chi_R + beta pi.

The auxiliary pi transformation is the first-order action transformation;
one must not freeze beta, use a fixed-beta lapse derivative, or infer it from
a zero-shift-only kinetic term. The full local action identity is checked
off shell, so no scalar auxiliary equation is used to force the proof.

Let E_mu,E_P,E_chi,E_pi be Euler covectors of the full action, with signs

    E_mu = -P_t - H_mu + G_mu,
    E_P  = mu_t - H_P + G_P,
    E_chi= -pi_t - H_chi + G_chi,
    E_pi = chi_t - H_pi,
    Ccal = C_bulk + G_N.

H derivatives here are variational derivatives, not partial derivatives
with radial work omitted. Define

    V = E_mu R F beta - E_P N(1-3u)/(kappa sqrtF)
          + E_pi T - N beta Ccal.

The interior identity is

    N (Ccal)_t = E_mu mu_t + E_P P_t + E_chi chi_t + E_pi pi_t - V_R. (CW)

The history contribution to V simplifies exactly to -K: the coefficient of
epsilon_R in delta c is -1, and that in delta C is zero. Its coefficient of
epsilon_t is N G_N=-c K-sum_i delta_i d_i C_i. Thus W is precisely the
missing history part of CW, not a guessed extension of the GR bracket.

On a genuine sufficiently regular history solution of all four evolution
equations, CW reduces to

    N (Ccal)_t = partial_R(N beta Ccal).

At P=0, smooth compact tests eta consequently give

    (Ccal)_tt[eta] = Ccal_0[zeta_eta],
    zeta_eta = kappa F^(3/2) P_t (eta N_R - N eta_R),

with actual radial/interface/time-window conditions still required. The
old failed nodal-bracket shortcut was applying this **on-shell** conclusion
to a finite Galerkin state, whose off-space Euler work is not zero.

## 4. Evaluate the missing Euler work instead of declaring it zero

Set f=eta/N. Smearing CW and retaining the boundary work gives

    (Ccal)_t[eta] = Ccal[beta (eta N_R/N-eta_R)]
      + E_mu[f mu_t + f_R R F beta]
      + E_P[f P_t - f_R N(1-3u)/(kappa sqrtF)]
      + E_chi[f chi_t] + E_pi[f pi_t+f_R T] + boundary work.

Denote these four generated tests by v_mu,v_P,v_chi,v_pi. At P=0 the
second derivative therefore contains

    Ccal_0[zeta_eta] + sum_a { (E_a)_t[v_a] + E_a[(v_a)_t] }
        + differentiated boundary work.                              (D)

All tests and their needed scalar radial derivatives were constructed from
the actual first and second jets, not fitted to Cddot. The new evaluations
use the full nodal G_mu,G_chi,G_P terms and differentiated inverse-time K.

The weak operator includes the physical P^2 radial action. Its explicit
symmetry work must accompany its contribution to E_P. For compact eta the
extra term in D, in the sign convention of the code, is

    B_sym = [v_P kappa R N F^(5/2) P_t]_in^out.

Leaving it out produces a few-e-9 discrepancy. Including it closes the
identity below; it is derived radial-action work, not a free counterterm.

### Exact scope of the numerical comparison

Use the 15 interior P1 tests plus both global cubic tests with their endpoint
values subtracted using the two endpoint P1 functions. This is a rank-17
zero-endpoint family obtained from the original 19 tests by a saved linear
map. The two independent nonzero-endpoint lapse rows remain separately
subject to the existing port/trace conditions; they are NOT certified here.
The changed test normalization explains why the compact maximum .0064413
differs from the previous full 19-row maximum .0061681.

| Working branch, primary | Matched GR | MTS |
|---|---:|---:|
| Compact Cddot maximum | 5.7102391e-6 | .00644128430 |
| Transported Ccal_0 moment maximum | 5.7124367e-6 | 5.7488073e-6 |
| Total Euler work maximum | 2.21e-12 | .00643554003 |
| Mass-configuration work maximum | 5.79e-16 | 1.35e-8 |
| Mass-momentum work maximum | 4.02e-15 | 2.13e-9 |
| Scalar-configuration work maximum | 2.21e-12 | .00626241306 |
| Scalar-momentum work maximum | 1.24e-14 | .000294902443 |
| D reconstruction error including B_sym | 2.20e-15 | 3.67e-13 |

Component maxima are NOT additive: their maxima need not be in the same
row. Higher-quadrature reconstruction errors are 6.27e-15 for GR and
3.73e-13 for MTS. These are floating-point checks of this finite fixture,
not certified intervals or a statement about arbitrary histories.

The dominant scalar terms are specifically

    E_chi[(v_chi)_t],       (E_pi)_t[v_pi],
    (v_chi)_t = eta chi_tt/N - eta N_t chi_t/N^2,
    v_pi = eta pi_t/N + (eta/N)_R T.

E_chi,t[v_chi] is already roundoff-small on this fixture. Saying simply
that the time-link identity is missing, or that another lapse fit is needed,
would now misidentify the problem.

## 5. An attempted repair, not just another missing-input ledger

Construct a scalar phase extension containing all 17 v_chi and their time
derivatives, and all 17 v_pi and their time derivatives, evaluated on the
working jet. The inherited canonical completion provides continuous
configuration dual lifts. Every old scalar function and derivative is
retained in span; coordinates are renormalized, so this is not an exact
old-column-prefix claim. The mass maps and all initial physical fields stay
unchanged. The source-backed amplitudes and couplings are not adjusted.

The new scalar dimensions are 124 (GR) and 125 (MTS), from 74; pairing
conditions are about 2.45 and 2.52. The entire requested frozen test family
is represented to the recorded numerical tolerances. Then ALL first rates,
time-link factors, all four accelerations and constraints are recomputed.
Only the two Pddot endpoints and clock-rate row determine the small lapse
correction. No Cddot row is fitted.

| Full 19-row Cddot maximum | Matched GR | MTS |
|---|---:|---:|
| Working branch before extension | 5.9037271e-6 | .00616809811 |
| Frozen gauge-family trial, primary | .000157131780 | .580008685569 |
| Same trial, higher quadrature | .000157163311 | .580008691721 |

The first-jet gates still pass. Primary Pddot endpoints and clock rate pass,
but the higher-quadrature second traces do not uniformly pass 1e-10.
This trial is not adopted. Worsening also occurs in GR, so it is not
legitimate to advertise it as a selective no-go for MTS.

The regenerated compact tests still obey D: MTS compact Cddot is now
.01026974209, with scalar-configuration work .00733772048 and
scalar-momentum work .00292628965. Its reconstruction error is below
3.49e-13. The large .5800 full maximum also contains boundary-row effects;
do not equate it with the compact interior norm. The old frozen family is
represented, but it is no longer the complete family generated by the new
coupled jet. Good pairing condition numbers do not make this feedback vanish.

## 6. Constructive next target: kinetic and Ward-compatible scalar action

For fixed canonical maps Q and P_s, let M_s=P_s^T W Q and define the
canonical projection Pi_Q=Q M_s^(-1) P_s^T W. At the initial P=0 slice,
the scalar acceleration equation reads

    chi_tt = Pi_Q [A pi_t + D],
    A = N sqrtF/R^2,
    D = (N_t sqrtF/R^2 - N mu_t/(R^3 sqrtF)) pi
          + kappa N F^(3/2) P_t chi_R.

Consequently the exact regular acceleration projection defect is

    (E_pi)_t = -(1-Pi_Q)[A pi_t+D].

Since pi_t belongs to P_s, sufficient conditions eliminating this defect
for the whole momentum-rate space and the allowed lapse-rate family are

    (1-Pi_Q) A P_s = 0,
    (1-Pi_Q) D_family = 0.

The other scalar condition is that the **current regenerated** (v_chi)_t
be represented in the configuration test space, or that its unresolved
Euler work be explicitly controlled. Representing yesterday's tests is not
the same condition. These are finite numerical compatibility requirements,
not additional physical axioms or new free MTS coefficients.

Next construct or revise the scalar variational approximation around these
kinetic conditions, with matched GR and unchanged physical initial inputs,
and reevaluate the full current Ward tests. Check continuity, interface work,
pairing rank and boundary compatibility before claiming a space is valid.
In particular, do not simply promote A times a broken momentum function to
a continuous configuration function without addressing its interfaces.

If exact finite-space closure is unattainable, the alternative is a justified
structure-preserving weak discretization and controlled convergence of these
identified defects, not endless zero-forcing or lowering the acceptance
threshold. A new finite action must be labelled and independently checked;
no inherited certificate transfers automatically.

Still needed even after a scalar repair: transported initial-constraint
moments (already visible in GR), both nonzero-endpoint lapse rows, robust
second traces, genuinely supplied boundary acceleration histories and an
appropriate history/causal evolution contract. No trajectory was launched.

## 7. Evidence and reproducibility

All new run folders are below source-intake/navier-stokes/20260912.

- `source-intake/navier-stokes/20260912/annular-history-ward-attempt01/status.json`: first 15-test source derivation; radial symmetry term not yet added.
- `source-intake/navier-stokes/20260912/annular-history-ward-attempt02/status.json`: full 17-test compact derivation, component split and saved generated families.
- `source-intake/navier-stokes/20260912/annular-history-ward-symbolic-attempt01/status.json`: six symbolic positive/negative checks.
- `source-intake/navier-stokes/20260912/annular-scalar-ward-completion-attempt01/status.json`: actual enlarged-space trial, paired outcomes and retained-space checks.
- `source-intake/navier-stokes/20260912/annular-canonical-ward-control-attempt01/status.json`: working-branch identity including radial-action symmetry work.
- `source-intake/navier-stokes/20260912/annular-canonical-ward-enlarged-control-attempt01/status.json`: regenerated enlarged-space identity, not a scientific pass.
- `scripts/derive_annular_history_ward_20260912.py`.
- `scripts/derive_annular_history_ward_compact_20260912.py`.
- `scripts/verify_annular_history_ward_symbolic_20260912.py`.
- `scripts/derive_annular_scalar_ward_completion_20260912.py`.
- `scripts/verify_annular_canonical_ward_source_work_20260912.py`.

All runs are bounded N16 calculations, one BelowNormal single-core Python
worker at a time. Failed mathematical repair and successful identity
verification are deliberately reported as different outcomes.
