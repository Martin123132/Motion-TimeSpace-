# Grid-independent initial data and boundary energy control

2026-09-09. Private continuation. Previous goal turn: progress, verified against
the saved evolution and evidence reports before beginning this step.

## What changes mathematically

The previous grid-specific 3x3 corner repair is replaced by a single continuum
initial-data problem. Its amplitudes have explicit formulas; its radial mass
profiles solve a linear boundary-value equation. The same resulting functions
are sampled on every grid. We then evolve only the remainder about this fixed
lift, so discretizing the lift does not secretly change the initial conditions.

Longer tests expose weaknesses in the earlier strong boundary treatment. An
energy-derived weak boundary enforcement and an energy-negative grid filter
are constructed below. These are numerical methods, not additional terms in
the MTS action. Their consistency and residuals must be checked; a stable-looking
trajectory alone does not establish an accurate solution.

The retained problem is still the common-reference, first-order-u exterior
scalar/Einstein block. Neither a calibrated physical coupling, a complete MTS
action, finite-u stability, nor a black-hole solution follows from this work.

## 1. Sources and fixed problem

Paths are relative to this post-checkpoint-work directory:

- `DERIVATION-20260909-compatible-wave-evolution-and-measured-linear-corrections.md`
- `DERIVATION-20260909-coupled-lapse-current-and-fixed-reference-error-control.md`
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/status.json`
- `scripts/annular_coordinate_evolution_operator_20260909.py`
- `source-intake/navier-stokes/20260909/sbp4-operator-derived/coefficients.json`

Keep the two dimensionless canonical and nonlinear/modulated fixtures, kappa=0.1,
epsilon=0.1, r in [4,8], sigma=0.05 and t=v-sigma(r-4). Both ordinary and u1
correction channels use the same reference operator. The ordinary channel is a
linear Newton step, NOT an updated exact reference for the u1 channel.

Let U=(chi,q=chi_v,mu,delta), and write the reference linearized evolution as
e_t=A e+B e_R+C e_RR-d, with the second spatial derivative acting only on chi.
The matrices and defects are those evaluated from the previous sourced action
block; no observational coefficients are refitted here.

## 2. Solve the continuum initial constraint

Set G=R0+sigma C0, where R0 and C0 are the reference radial/temporal mass
sources. Their coordinate-state dependence is G(chi,q,mu,delta,chi_R).
Write g=G_mu and J_j for the approximate initial mass-constraint residual
in channel j=0,1. Initial q error is zero everywhere. The initial mass obeys

```text
nu'_j-g nu_j=G_chi eta_j+G_delta zeta_j+G_chi_R eta'_j-J_j,
nu_j(8)=0.                                                        (1)
```

For the declared width-one profiles H(d)=d^2(1-d)^4/2 and
Jshape(d)=-d(1-d)^4, both zero outside [0,1], put

```text
hL=H(r-4), hR=H(8-r), jR=Jshape(8-r),
eta_j=aL_j hL+aR_j hR, zeta_j=aD_j jR.
```

These profiles are a numerical data choice, not a derived physical law. Their
endpoint values and first scalar derivatives vanish; hL''(4)=hR''(8)=1 and
jR'(8)=1. They are C3 at the support joins, not infinitely smooth functions.

Define five mass solutions M0,M1,ML,MR,MD of (1), all with zero outer value,
and respective right-hand sides

```text
-J_0, -J_1,
G_chi hL+G_chi_R hL', G_chi hR+G_chi_R hR', G_delta jR.
```

Each has the explicit Green-function representation

```text
M_f(R)=integral_8^R exp(integral_s^R g(x)dx) f(s)ds.                (2)
nu_j=M_j+aL_j ML+aR_j MR+aD_j MD.
```

Thus the mass correction is determined by the constraint, not independently
invented to make the final answer look good.

## 3. Explicit, grid-independent corner amplitudes

At both endpoints eta=eta_R=q=0. At the outer endpoint nu=zeta=0 as well.
The differentiated scalar boundary condition therefore requires q_t=0 initially.
The outer lapse condition requires zeta_t=0. Using the actual reference matrices,

```text
aD_j=sigma d_delta,j(8),
aR_j=[d_q,j(8)-B_q,delta(8) aD_j]/C_q,chi(8),
aL_j={d_q,j(4)-A_q,mu(4)[M_j(4)+aR_j MR(4)+aD_j MD(4)]}
     /{C_q,chi(4)+A_q,mu(4) ML(4)}.                              (3)
```

Only nonzero denominators are needed. A sufficient analytic condition for
the inner one is |A_q,mu ML|<C_q,chi with C_q,chi>0. Equation (2) supplies
the usual finite-interval integrating-factor bound on ML. This is a conditional
criterion, not a certified bound over every MTS background.

The numerical inner denominators are 5.0632927443 and 5.0085988777; the
mass-profile corrections to them are only about 2.72e-9 and 3.32e-9. The
outer denominators are 7.6430029681 and 7.4209867356.

The resulting amplitudes (inner scalar, outer scalar, outer lapse) are:

| Fixture/channel | aL | aR | aD |
| --- | ---: | ---: | ---: |
| Canonical/reference | -6.1198e-9 | 6.5082e-10 | 1.3034e-16 |
| Canonical/u1 | -3.8689e-8 | 9.6327e-11 | -6.4066e-14 |
| Nonlinear/reference | 4.1373e-8 | -6.7422e-9 | 4.9677e-15 |
| Nonlinear/u1 | -3.1215e-9 | 2.4462e-10 | -9.7878e-14 |

The numerical mass functions use four unit-width Chebyshev panels of degrees
32 and 64 as a refinement control. At 266 off-collocation points, their maximum
constraint residuals are 3.15e-19 and 4.84e-19, against source scales around
2.54e-11 and 4.00e-11. Degree-refinement differences in the initial fields are
below 8.5e-21 and their first derivatives below 1.01e-18. Second-derivative
differences are around 1.5e-15, reflecting numerical differentiation sensitivity.
These are sampled numerical checks, not interval-certified continuum bounds.

All initial endpoint/corner equations hold to numerical roundoff. Nested-grid
values and derivatives from the same data file are bitwise identical. This
removes the earlier ambiguity caused by a different initial solve at each grid.
The data owner is `source-intake/navier-stokes/20260909/annular-continuum-data-initial/status.json`,
25/25, completed 02:22:13 UTC.

## 4. Evolve a remainder, not a redifferentiated initial profile

Let L(R) be the fixed initial lift and write e=L+w, with w(0,R)=0. Use

```text
w_t=A(t)w+B(t)D_h w+C(t)D_h^2 w
    +A(t)L+B(t)L'+C(t)L''-d(t).                                  (4)
```

The derivatives of L come from the declared profiles and mass polynomials,
not a different finite-difference approximation at each resolution. The
scalar gradient is reconstructed from L'+D_h w, so chi_t=q is maintained.
The time-independent lift has q=0. Initial radial constraints are checked
including the outer endpoint, not only the rows left after a discrete solve.

All comparisons retain the same incoming scalar data, outer lapse normalization
and evolving outer mass-flux equation. No boundary mass is clamped during evolution.

## 5. Derive a boundary treatment from the wave energy

Let alpha=-A_t>0, beta=b-sigma c and c>0. Freeze these wave coefficients.
For q=eta_t and z=eta_R the principal equations are

```text
q_t=(2beta/alpha) q_R+(c/alpha) z_R, z_t=q_R.
E_wave=1/2 integral [alpha q^2+c z^2]dR,
dE_wave/dt=[beta q^2+c q z]_inner^outer.                           (5)
```

The boundary condition is z=d_B q, d_B=sigma+k. At the inner root,
beta+c d_B=+sqrt(b^2-ac); at the outer root it equals -sqrt(b^2-ac).

With SBP norm h H, add to q_t ONLY the penalties

```text
inner: +(c/alpha)(z-d_B q)/(h H_edge),
outer: -(c/alpha)(z-d_B q)/(h H_edge).                             (6)
```

The respective combined boundary energy contributions become
-(beta+c d_B)q^2 and +(beta+c d_B)q^2, hence both nonpositive. This follows
without replacing the bulk q equation or breaking z_t=D_h q. Add the usual
outer lapse advection penalty -zeta/(sigma h H_edge); its frozen energy
boundary contribution is also nonpositive. The scalar identities are checked
exactly in the runner. Variable-coefficient and metric-coupled energy estimates
still need their own control; this is not a full discrete nonlinear theorem.

Boundary errors are now weakly controlled and must tend to zero with resolution,
not be reported as exactly zero by construction. Their measured errors and
the bulk-versus-boundary RHS difference are saved explicitly.

## 6. Control the observed grid-scale alternating component

The unfiltered fine runs retain an alternating mass component near a boundary:
for example, successive canonical/u1 outer samples at T=0.3 alternate around
the smooth trend even as interior constraints shrink. This is evidence of a
numerical grid-scale component, not proof that every remaining error is numerical.

For a vector y, let Delta3 be the unscaled third forward difference and
W a positive energy weight. Use

```text
Q_h y=-eta_num/(h H W) Delta3^T Delta3 y,
<y,Q_h y>_(h H W)=-eta_num ||Delta3 y||^2 <=0.                     (7)
```

Apply this only to the q,mu,delta remainders, with W=alpha for q and W=1
for the metric variables. No chi dissipation is added, preserving chi_t=q.
The operator annihilates polynomials of degree at most two, is O(h^5) in the
smooth interior and O(h^2) at its truncated boundary. Its coefficient 1/64
normalizes the uniform-grid third-difference Nyquist factor 64; it is a
declared numerical coefficient, not a fitted or parent-derived MTS constant.

The finite-grid mass equation is changed by Q_h nu. That term is saved and
compared with the original temporal mass defect, rather than hidden behind an
improved radial constraint. Dissipation strength and mesh dependence remain
necessary numerical controls; energy negativity alone does not prove accuracy.

## 7. Derive a constraint-compatible numerical source, rather than tune a filter

There is a more structural next method. In the reference continuum system,
let S_q and S_delta be added sources in the q and delta evolution equations,
and C_added the added temporal mass source. Keep chi_t=q exactly. Write
J_err=R_err+sigma C_added for the spacelike radial constraint. The exact
residual transformation from the previous note gives

```text
D=-sigma S_delta,
F_chi=A_t S_q+[j_r+q(a/sigma-b)]D
      +j_mu_v C_added+j_mu_r R_err.                               (8)
```

Substitute (8) into the reference Bianchi identity, remembering
partial_r|v=partial_R-sigma partial_t and mu_v=C0+C_added. The terms containing
partial_t C_added cancel in the equation for J_err. The apparent C_added
S_delta product cancels using delta_r=D0-sigma S_delta. The result is

```text
(J_err)_t-kappa p j_mu_r J_err
 =partial_R C_added+beta_C C_added+f_S,
beta_C=D0+kappa p(j_mu_v-sigma j_mu_r),
f_S=sigma[C0-kappa p(j_r+q(a/sigma-b))] S_delta
    +kappa p A_t S_q.                                            (9)
```

Thus a unique source completion preserving the outer physical mass-flux
equation is obtained from

```text
partial_R C_added+beta_C C_added=-f_S, C_added(8)=0,
C_added(R)=integral_R^8 exp(integral_R^s beta_C(x)dx) f_S(s)ds.     (10)
```

This makes (9) homogeneous. It avoids division by p and therefore does not
break at a scalar turning point. If the numerical sources vanish, C_added
vanishes as well: (10) is not a new constitutive or closure law for MTS.
Its finite-interval norm is bounded by the integrating-factor estimate.

This source-completion identity is derived for the reference continuum
equations. Implementing it on a grid must retain the discrete product-rule
defect. Linearizing around our approximate rather than exact background adds
known background-residual variation terms. Those terms, the first-order-u
restoration/source variations and an energy bound for the induced mass source
must be included before claiming an actual constraint-preserving solver.
The implementation of (10) is the next substantive target; it has not been
executed in the runs below.

## 8. Longer and finer runs: what passes and what does not

All run directories are under `source-intake/navier-stokes/20260909/`.

| Run | Result | What it establishes |
| --- | --- | --- |
| annular-fixed-data-evolution-initial | FAILED 65/67 | Fixed-data, strong boundary method; at T=0.3 two full mass-constraint gates fail |
| annular-fixed-data-sat-final | FAILED 74/77 | Energy-based boundary method alone does not cure those failures; one boundary-accuracy gate also fails |
| annular-fixed-data-dissipation-final | FAILED 82/85 | Filtering reduces grid-scale errors; canonical u1 long-time constraint, one refinement and one boundary gate still fail at N256 |
| annular-fixed-data-refined | FAILED 83/85 | At N512 all eight full mass-constraint and boundary-accuracy gates pass, but two short-time q-dominated refinement gates remain failed |
| annular-fixed-data-half-filter-control | FAILED 83/85 | Same data at N64/128/256 and half the filter coefficient; canonical u1 long-time constraint and short-time boundary-accuracy gates remain failed |

No failed run receives a COMPLETE marker. The status of the finest run is
not promoted to success by counting only its favorable tests. Its remaining
failures are canonical/reference and nonlinear/u1 at T=0.1. Their consecutive
max-norm grid-difference ratios are 0.871 and 0.802, below the fixed 1.3 gate.
The associated fine-grid q differences are 1.89e-12 and 1.27e-12, roughly
0.053% and 0.081% of the final q amplitudes. Small absolute errors do not
turn a failed convergence-pattern check into a proved convergence theorem.

At T=0.3, N512 with refined time step, the full radial constraint is:

| Fixture/channel | Before correction | After correction |
| --- | ---: | ---: |
| Canonical/reference | 2.040e-11 | 3.236e-13 |
| Canonical/u1 | 3.505e-12 | 9.492e-13 |
| Nonlinear/reference | 4.869e-11 | 1.657e-12 |
| Nonlinear/u1 | 2.332e-11 | 1.742e-13 |

These are full-domain values, including both endpoints, in the same
dimensionless fixtures. This extends the earlier time interval by a factor
three and finest grid by a factor eight, without refitting physical parameters
or changing the initial profiles. It does not prove the continuum constraint
vanishes. The artificial temporal mass terms are explicitly stored and are
smaller than the original temporal mass defects at every selected fine output.

The finest run completed at 02:45:23 UTC. Halving the filter coefficient at
N256 changes the field-component maxima by at most about 0.81% of their
full-filter reference amplitudes (largest sensitivity: canonical/u1 mass at
T=0.3). The scalar and q differences are below 0.09% in all these comparisons.
This is a measured finite-grid sensitivity, not a bound on the continuum error
or a reason to select a different physical theory. The current source snapshot
hash is `76ad2afd26c5ea3aa08519320798440ccaab0c16aa3302483fc686b0f2a7d6b3`.

Independent evidence run `annular-fixed-data-evidence-final` completes 65/65
at 02:49:22 UTC. It checks all terminal states including honest failures,
execution and input hashes, finite artifacts, matching initial data, independently
reconstructs the full constraints and filter matrix, checks its negative energy
production, and verifies the three algebraic steps in (8)-(10). These 65 checks
do NOT override the numerical run's 83/85 status. Its source SHA-256 is
`99d5f5c402fb544d94db4c3d916cddade824d3c882775f53eae8790645cf7623`.

Scripts: `scripts/annular_continuum_initial_data_20260909.py`,
`scripts/derive_annular_continuum_data_20260909.py`,
`scripts/annular_fixed_data_evolution_20260909.py`, and
`scripts/annular_fixed_data_evidence_20260909.py`. Prior execution snapshots
remain intact even where the live runner gained new numerical options.

Next implement and test (10) with its linearized background-residual terms,
using the same data and controls. Reference feedback through delta K follows
after that, not by treating the current corrected field as exact. Public repos,
galaxy work and the frozen workbench remain untouched. No extra agents or
interference with other tasks is needed.
