# Current local resume

Updated: `2026-07-24`
Last checkpoint: `5214-Y5-R2FR-A00-identical-graviton-permutation-control-variate.md`
Marker: `MTS_5214_A00_SOURCE_POLE_CONTROL_VARIATE`
Predecessor marker: `MTS_5213_SOURCE_SEPARATED_ADDITIVE_CLUSTER_CAUCHY_ZERO`

Session runtime boundary: the capped continuation is safely paused. Return to
the approximately four-hour cap unless the user authorizes another long run.
If the cap approaches, finish only the calculation then in flight, write its
outputs and exact resume point, and report back.

The authoritative current handoff is the first checkpoint section in this
file; later sections retain the derivation history.

## Authoritative current handoff - checkpoints 5212 through 5214

Checkpoint 5214 derives the analytic control selected by the completed 5212
pilot.  It is not a fitted regression.  The exact identical-graviton
permutation `g1 <-> g3` maps the dominant direct source family

```text
Y_13 = Y[g1+,g3-]
```

to

```text
Y_31 = Y[g1-,g3+].
```

For the exact soft-sector partition

```text
w_i = E_i^-2 / sum_j E_j^-2,
```

physical phase-space invariance cancels the exchanged sequential-chart
soft-energy Jacobian.  The remaining reweighting is `w1/w3=(E3/E1)^2`, so

```text
C_13 = Y_13 - (w1/w3) Y_31;
E[C_13] = 0.
```

The coefficient is fixed to one by permutation symmetry.  Both families are
direct, reciprocal-safe terms; the soft subtraction does not contaminate the
identity.  Each reciprocal root is weighted by its own analytic
`(E3/E1)^2` ratio before winding-weighted residue summation.  The control is
applied only to the real component; the rejected imaginary-reflection route
is not revived.

All 24 locked `A00` jobs reproduce exactly, with maximum relative residual
zero.  The source-family decomposition contains 26 families and closes
eventwise.  The dominant family carries `0.971889386` of the covariance with
the real `A00` total and remains rank one in all twelve leave-one-event-out
training sets.

On the locked retrospective events:

```text
A00 real SD ratio                    = 0.2171867716;
full z=-0.6 real SD ratio            = 0.2170072259;
topological-local real SD ratio      = 0.3652064133;
topological-local variance reduction = 7.497616267;
control mean / control SE            = 0.286408526.
```

The diagnostic controlled candidate is

```text
K_mu = -15.7083742119 - 54.3540162508 i;
SE_real = 580.609411038.
```

That shift is not a coefficient claim: a zero-mean control can move a small
retrospective sample.  Checkpoint 5214 passes `18/18` validation checks and
authorizes only a frozen, fresh-seed `A00` pilot.

Checkpoint 5212 executes the fresh crossed-`hhh` coefficient pilot selected
after the exact local-GR result.  It is a calculation, not another inventory
of missing inputs.

The estimator was locked before outcomes as

```text
E[H_crossed]
 = E[H_naive, full]
 + E[H_topological, independent].
```

The full stratum used two fresh outer events and retained the paired
`pole_model+smooth` estimator.  The independent topological stratum used
twelve disjoint fresh events, reciprocal reduction for certified safe pole
pairs, and both roots for every unsafe pair.  The complete schedule contained

```text
2 epsilon values x 10 crossed arguments x
(2 full seeds + 12 topological seeds) = 280 jobs.
```

All `280/280` jobs converged under the locked configuration digest

```text
029d1c238303ab54a90b3b523aa360c6e5191bed55cc3411998700e265d371e3.
```

There are no failed, unconverged or missing jobs.

Two fresh numerical failures were not hidden by relaxing tolerances.

First, `E040/A10` failed the original `5085` fixed removable-limit grid just
above the `10^-7` gate.  The accepted repair keeps that gate and collision
scope unchanged, evaluates successively halved symmetric offsets, and applies
the even removable-limit Richardson sequence.  It was invoked four times
across two full-stratum jobs.

Second, topological event `521213/A00` exposed four unstable nested residue
contours.  Checkpoint 5213 proves an exact guarded zero rather than replacing
them with a fitted number.  With

```text
I(z,q)=D(z,q)-S(z,q),
R_X(q)=(1/(2 pi i)) integral_(C_X) X(z,q) dz/z,
```

each selected componentwise Cauchy sum `R_X(q)` is holomorphic while no
same-summand collision, chart origin or kinematic singularity enters its
relative-coordinate disk.  A pole of `D` coinciding with a pole of `S` does
not singularize either additive summand.  Because the guarded centre
`q0 != 0`,

```text
Res_(q=q0) [(R_D(q)-R_S(q))/q] = 0.
```

The strict guard rejects same-summand pairs, the `g3/soft` alias, chart-origin
collisions, missing pair roots, insufficient margins and irregular
kinematics.  The smallest same-summand margin is `4660.958` production
contour radii; the largest grouped-root residual is `1.8229033e-5`, below the
locked `2e-5` transport grouping threshold.  A 601-row historical
stable-nonzero corpus contains zero strict-scope counterexamples.  The
on-demand theorem was used by 20 topological jobs and certified 35 exact-zero
rows.

The completed pilot estimates

```text
K_mu(candidate)
 = 352.21312257110867 - 54.35401625075943 i,

SE[Re K_mu] = 1382.3515514181697,
SE[Im K_mu] = 43.83445426804328.
```

This is explicitly a **non-claim candidate**.  The real component is not
resolved.  The twelve-event topological real distribution has

```text
mean                  = -96.70238436513553;
standard error        = 168.448743136648;
median                = -1.49247;
one-event-trimmed mean= -54.8755;
maximum delete-one shift = 0.777695 SE;
ordered-half difference  = 1.91848 sigma.
```

The largest observed real variance is the `A00`, physical-cosine `z=-0.6`
family.  Its largest individual values are `-8553.95`, `+4967.31`,
`-2432.49` and `-417.684`.  The realized equal-cost speedup is `0.245397`
for the real component and `1.62768` for the imaginary component.  Thus the
independent split helped the imaginary estimator but made the real pilot less
efficient.  Twelve events do not establish a tail law.

Therefore:

```text
fresh pilot matrix complete                    = yes;
source-separated guarded Cauchy zeros          = exact;
blind scaled sampling authorized               = no;
topological tail convergence demonstrated      = no;
canonical numeric K_mu                         = open;
checkpoint-5211 exact local GR+Maxwell branch  = unchanged;
all-operator local GR                          = false;
full MTS                                       = false.
```

The next calculation is narrowly fixed by the data: freeze the checkpoint-5214
source signatures, rootwise partition ratio, coefficient one, real-only
application and acceptance thresholds, then run an `A00`-only pilot on fresh
independent topological seeds.  Scale to the full local projection only if the
fresh control mean remains zero-compatible and the variance reduction
reproduces.

Checkpoint 5212 passes `16/16`, checkpoint 5213 passes `11/11`, and checkpoint
5214 passes `18/18`.  All 25 checkpoint-5214 JSON files parse, all four CSV
tables parse, and a fresh analysis rerun reproduces all seven checkpoint
artifacts byte-for-byte.  `formalization-workbench`, the public worktree and
the galaxy work remain untouched.

Markers:

```text
MTS_5212_FRESH_CROSSED_HHH_TWO_STRATUM_PILOT
MTS_5213_SOURCE_SEPARATED_ADDITIVE_CLUSTER_CAUCHY_ZERO
MTS_5214_A00_SOURCE_POLE_CONTROL_VARIATE
```

## Authoritative current handoff - checkpoint 5211

Checkpoint 5211 makes the local-GR promotion that the previous source,
vacuum and trajectory work had prepared.  It does not merely list the same
missing coupling again.

On the source-selected checkpoint-5208 trajectory,

```text
F_R(chi)=M_R^2;
Z_chi=1;
V(chi)=m_gap^2 chi^2/2;
P=P_ge2(X_chi);
delta S_visible/delta chi=0.
```

The branch

```text
chi=0;
nabla_mu chi=0
```

is an exact classical consistent truncation of the bulk field equations for
arbitrary retained metric, Maxwell and visible-matter configurations:

```text
E_chi|_0=0;
T_chi|_0=0;
Gamma_hchi=Gamma_Achi=Gamma_matter_chi=0.
```

With the declared silent local state `rho_local=rho_0`, and after retaining
the two-derivative part of the same parent action, the restricted nonlinear
action is exactly

```text
Gamma_2der =
 integral d4x e [
  M_R^2(R-2 Lambda_cal)/2
  -F_mu_nu F^mu_nu/4
 ] + S_visible[e,omega_LC[e],A,Phi_SM].
```

This gives an exact selected **GR + Lambda + Standard Model + Maxwell
two-derivative branch**, not just an inverse-square fit.  The state is an
explicit preparation/boundary datum; the current parent does not derive it
as an attractor.

The one-coframe Hilbert source, soft-spin-2 constraints and Bianchi identity
give a rank-four five-species constraint matrix with one all-ones null
vector.  There is one universal source residue:

```text
Gamma_12 =
 i/[M_R^2(q^2+i0)]
 [T1_mu_nu T2^mu_nu-T1 T2/2].
```

Consequently,

```text
G_N=1/(8 pi M_R^2);
nabla^2 Phi=4 pi G_N rho;
Phi=-G_N M/r;
d^2x/dt^2=-grad Phi.
```

Neutral, null and charged worldlines use the same metric.  No
species-dependent gravitational weights or arena calibrations are added.

The transported ten-parameter two-derivative PPN vector is

```text
(gamma,beta,xi,alpha1,alpha2,alpha3,zeta1,zeta2,zeta3,zeta4)
=(1,1,0,0,0,0,0,0,0,0).
```

The standard Maxwell Hilbert stress, conservation law and Poynting vector
are also exact:

```text
T_EM^00=(E^2+B^2)/2;
T_EM^0i=(E cross B)^i;
nabla_mu(T_EM+T_visible)^mu_nu=0.
```

Checkpoint 5211 introduces the fair matched comparator

```text
DeltaGamma_MTS=Gamma_MTS-Gamma_GR+SM
```

at the same subtraction scheme and with the same `G_N`, `Lambda_cal`,
`alpha_EM`, Standard-Model inputs and common GR+SM Wilson coefficients.
Visible QED/QCD photon-curvature thresholds and standard graviton/ghost
loops are therefore baseline physics, not MTS-specific failures.

The resolved MTS excess is small in the locked local arenas:

```text
max one-real-scalar nonlocal logarithmic residual
 =3.046881093102626e-40;

max locked parent-CFF endpoint residual
 =1.1374144856001986e-79;

c_parent/|c_visible_control|
 =8.23411454651178e-42;

max compact-corridor |Delta c_chi^2|
 =1.8116002546570096e-17.
```

The `C3` numbers remain endpoint smoke values because checkpoint 4971
proved that local running has rank zero for the physical absolute on-shell
anchor.  The two-scale helicity projector is already full rank, but the
full-parent finite amplitude and MTS-specific `p8+` coefficients have not
been supplied.

Current exact boundary:

```text
selected chi=0 bulk branch                      = exact;
nonlinear two-derivative GR+Lambda              = exact;
universal Hilbert source and Newton limit       = derived;
all ten two-derivative PPN coefficients         = GR;
Maxwell Hilbert stress and Poynting vector      = exact;
direct classical one-scalar fifth force         = zero;
Lambda_cal                                      = one frozen datum;
local state attractor/preparation theorem       = open;
physical absolute C3 anchor                     = open;
complete MTS-specific p8+ matched excess        = open;
all-operator local GR                           = not claimed;
full MTS                                        = not claimed.
```

The next target is an actual coefficient calculation, not another missing
input inventory:

```text
DERIVE_FIRST_CANONICAL_MTS_SPECIFIC_P8_ONSHELL_COEFFICIENT
FROM_THE_FULL_PARENT_HESSIAN_OR_BOUND_ITS_MATCHED_EXCESS.
```

Do not reopen universal source coupling, Newton, the standard PPN vector,
the classical Poynting vector, or `Lambda_cal=0` as though they were the
current gap.

Machine products:

```text
scripts/Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py
source-intake/functional_rg/5211/
source-intake/mts_residuals/P8_Y5_BRR545_5211_VALIDATION.csv
```

Validation is `43/43 PASS`; all 14 generated checkpoint products are
deterministic across reruns.  The evidence-CSV digest is
`25b894885dc16be11d63cf1a33de77818d925e51c7e86d92f04fb5ea54598942`.
No GitHub/public worktree, galaxy repository or
`formalization-workbench` file was changed.

## Authoritative current handoff - checkpoint 5210

Checkpoint 5210 closes the repeatedly reopened `Lambda_cal=0` fork for the
parent action that has actually been constructed. It attempts the exact-zero
derivation rather than merely listing it as missing, and obtains a definite
negative result for every currently available route.

The canonical vacuum block is

```text
S_vac=-integral d4x e U_Lambda;
U_Lambda=M_R^2 Lambda_cal;
C0_R=-M_R^2 Lambda_cal.
```

The volume operator is allowed by Diff, local Lorentz symmetry, the
relational local-translation gauge symmetry, visible `U(1)` and the motion
`Z2`/constant-shift limits. It is not a boundary term. On compact
boundaryless flat `T4`,

```text
integral_T4 d4x partial_mu J^mu=0;
integral_T4 d4x e=V4>0.
```

It is not topological because `e^A_mu->a e^A_mu` scales the integral as
`a^4 V4`. No selected parent symmetry sets its coefficient to zero.

CTP normalization also fails as a zero-selection mechanism:

```text
Gamma_C0[g,g]=0;

delta Gamma_C0/delta g_a^mn|_(g_a=0)
 =-C0 sqrt(-g_r) g^r_mn/2 !=0.
```

The diagonal value cancels, but the difference-metric variation that enters
the physical equation does not.

The optimized scalar vacuum trace is now explicit:

```text
partial_t C0_E=k^4/[32 pi^2(1+w)];
w=m^2/k^2;
u0=C0_E/k^4;

beta_u0
 =-4u0+W0/[32 pi^2(1+w)].
```

For one massless real scalar,

```text
beta_u0(0)
 =0.0031662869888230555;

u0*
 =0.0007915717472057639;

d beta_u0/d u0=-4;
theta0=+4.
```

The minimal canonical real-scalar plus public-`U(1)` matter block has
`W0=1+2=3`. The locked primitive and imported benchmark rows have
`W0=1`, `3` and `-62`, never zero. Thus `u0=0` is not an invariant surface
of the explicitly resolved matter flow. Gravity/ghost terms may shift the
full coordinate, but an uncomputed contribution cannot be used as a
cancellation.

Checkpoint 4934's source-complete minimal fixed point covers only

```text
(g,g_plus,g_minus,g_CFF,h_C3).
```

Its one-relevant-direction index is correct inside that five-coordinate
truncation, but it does not contain `u0`, `C0` or `Lambda_cal` and therefore
cannot select or count the vacuum direction.

The exact canonical calibration Jacobian over

```text
coordinates:
 (ln M_R^2,ln Z_A,ln M_psi^2,ln Z_psi,ln Lambda_cal);

observables:
 (ln G_N,ln alpha_EM,ln m_pole^2,ln Lambda_cal)
```

has rank four and nullity one. The null direction is elementary field
normalization; `Lambda_cal` is an independent physical coordinate.
Checkpoint 5209 independently rules out hiding it in a `P(X)` state moment:
the homogeneous constraint remains rank one with nonzero nullity.

The current parent result is therefore

```text
Lambda_cal is one universal renormalization/calibration datum;
it is fixed once;
arena-by-arena retuning is forbidden;
exact zero remains an allowed imposed renormalization branch but is not
predicted.
```

This is a resolved parameter boundary rather than another open placeholder.
It does not solve the cosmological-constant problem, and it does not prevent
a future enlarged UV calculation from adding `u0` and deriving a new Ward or
supertrace identity.

The locked checkpoint-5195 internal comparison remains:

```text
ParentScalar_Lambda_free:
 chi2=1473.9782736442494;

ParentScalar_Lambda_zero:
 chi2=1474.0690807198073;

zero minus free:
 Delta chi2=+0.09080707555790468;
 Delta AIC=-1.9091929244420953;
 Delta BIC=-7.315296305679112.
```

Neither branch hits a prior edge. AIC/BIC conditionally prefer the
one-parameter-smaller zero branch, but this is model comparison, not an
action-level zero theorem.

The free branch supplies a numerical single-calibration propagation:

```text
H0=67.49204419441142 km s^-1 Mpc^-1;
Omega_Lambda=0.48876252734622694;
Lambda_cal=7.805160260508188e-53 m^-2.
```

Using the Schwarzschild-de Sitter weak-field terms,

```text
Phi=-GM/r-Lambda_cal c^2 r^2/6;
a_r=-GM/r^2+Lambda_cal c^2 r/3,
```

gives

```text
Lambda L^2 at 50 micrometres
 =1.951290065127047e-61;

a_Lambda/a_Newton at Earth surface
 =1.5170050109870232e-30;

a_Lambda/a_Newton at Saturn
 =5.190517980275124e-20;

Lambda L^2 at 100 kpc
 =7.43161008040344e-10.
```

The same value is used in every row. The direct Maxwell portal remains zero.
These are background residuals, not a substitute for the complete PPN,
clock, orbital or R10 observable projection.

The checkpoint-4876 scalar-only Newton-matched cutoff gives a
scheme-dependent naturalness diagnostic,

```text
Lambda_UV/Mbar=4pi sqrt(6)=30.781195923884734;
C0_loop/rho_crit=1.3555597928614725e123.
```

This is not an observable probability. It does show that checkpoint 5209's
finite-motion threshold below `8.781062042761168e-123` of critical density
cannot select or cancel the independent quartic coordinate.

Validation:

```text
57/57 PASS;
9/9 evidence CSVs parse and are nonempty;
12/12 generated products are byte-for-byte deterministic across reruns;
script compiles;
scripts/__pycache__ absent;
formalization-workbench SHA256
 =b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
public worktree unchanged and clean;
galaxy repository unchanged with its six pre-existing dirty paths.
```

Artifacts:

```text
5210-Y5-R2FR-parent-vacuum-coordinate-local-invariant-CTP-RG-source-and-renormalization-datum-theorem.md
scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py
source-intake/functional_rg/5210/
source-intake/mts_residuals/P8_Y5_BRR545_5210_VALIDATION.csv
```

Hashes:

```text
document
 =5e91f56762147f1922a1e71be619b83ca0b14091e8112efaed5b247e19f2c21b;

script
 =5cf944fa88e17d0dc28e0c5717891966f2f1db5f73639834fdb9287e6abaaa34;

result JSON
 =3d8602208269ad1a0058c2d1feee3fcb057ea29b330260be4aa4173f9851b95c;

validation
 =53faf56534f04f1b31c053f17c3ebd6a90925230735205b231c50951e6287964;

evidence CSV digest
 =b35b0137d25d39e6aa7e9841f098cb7bafcb5b8b1ce4fcf15242b6e0f8f2ab4d;

checkpoint-5210 output-tree digest
 =199cb38a510968569b7126e630da996614b03ec23df56925519f42f34a6d0f33.
```

Selected next route:

```text
RESUME_UNIVERSAL_SOURCE_COUPLING_AND_LOCAL_GR_WITH_ONE_FROZEN_LAMBDA_DATUM
```

The next local-GR work should not reopen this vacuum fork. It should derive
the universal source-coupling Ward identity and residual vector while
carrying the one calibrated `Lambda_cal` through every arena. A separate,
nonblocking UV extension may later add `u0` to the full Hessian if a vacuum
prediction is required.

No GitHub action occurred. No file outside `post-checkpoint-work` was edited.

## Authoritative current handoff - checkpoint 5209

Checkpoint 5209 calculates the finite-motion-mass deformation of the locked
essential `P(X)` trace instead of treating it as an unspecified future
coefficient.

For the optimized regulator, with `w_s=m_gap^2/k^2`,

```text
q_i,n^(p_s,p_g)(w_s,w_g)
 =[1/n!-eta_i/(2(n+1)!)]
  /[(1+w_s)^p_s(1+w_g)^p_g].
```

After the checkpoint-4958 essential metric quotient, the exact weak sources
through `X^3` are

```text
y=1/(1+w);

S2(w)
 =24-(32/3)y-(4/3)y^2+4y^3;

S3(w)/pi
 =-96+144y-96y^2-(224/5)y^3+(256/5)y^4.
```

They recover

```text
S2(0)=16;
S3(0)=-208 pi/5.
```

The new massive Hessian is exactly identical to the locked projector at
`w=0`, and its direct numerical source values reproduce both analytic
functions at all eight nonzero/zero calibration masses.

For `A2=a2/g^2`,

```text
dA2/d ln k=S2(w);
dw/d ln k=-2w;

F2(w)
 =-8 ln w-4 ln(1+w)-(4w+7)/[3(1+w)^2];

-2w dF2/dw=S2(w).
```

The finite-mass correction relative to the massless logarithm begins

```text
Delta A2_mass
 =-(2/3)w-(7/3)w^2+4w^3+O(w^4).
```

The decisive scale-consistency result is a no-overlap theorem. The locked
local polynomial is controlled for

```text
x=Y/k^4<=0.1;
Y=M_R^2 H^2 q^2.
```

The exact checkpoint-5208 fitted history gives

```text
max w inside the controlled P(X) domain
 =1.3507159281008945e-47;

min x if the finite-mass threshold w=1 is imposed
 =5.481153409541768e92.
```

Thus a finite-mass threshold and the controlled local `P(X)` polynomial do
not overlap anywhere on `-18<=N<=0`. Evaluating the entire finite polynomial
at `k~m_gap~H0` would be outside its demonstrated derivative domain by at
least ninety-two orders of magnitude. Inside the controlled domain,

```text
max relative finite-mass change in A2
 =6.61337403504281e-51.
```

The exact Lorentzian stress calculation gives

```text
P(Y)=Y/2+c2 Y^2;
rho_X2/rho_kinetic=6 c2 Y;
c_s^2=(1+4c2Y)/(1+12c2Y).
```

On the exact fitted background,

```text
max |rho_X2/rho_kinetic|
 =6.34459694749058e-121;

max |Omega_X2|
 =1.8330615662257626e-122;

max |c_s^2-1|
 =8.4594625966541e-121.
```

The resolved `N=3..8` local-polynomial partial sum is below `10^-183.7168`
of the canonical kinetic density. The actual checkpoint-4958 `A3` would
need at least `63.5185` additional orders of magnitude to equal even the
already negligible `X2` term. This is not promoted to an all-order nonlocal
effective-action theorem.

The vacuum branch does not close through `P(X)`. The quadratic homogeneous
constraint has Jacobian

```text
[1,K2]
```

over `{Omega_Lambda,sigma2}`, hence rank one and nullity one. Nonlinear state
moments produce

```text
[1,K2,c2 K4,...],
```

which remains rank one and has more null directions. Even imposing an
un-derived Gaussian moment closure leaves one equation for two coordinates.
Three distinct positive state/vacuum witnesses are generated from the
checkpoint-5205 transfer row. Therefore `P(X)` cannot derive
`Lambda_cal=0`.

The finite mass-dependent one-loop vacuum contribution is bounded by

```text
|Delta Omega_vac,mass|
 <=8.781062042761168e-123.
```

It is renormalization-condition dependent and cannot select the observed
vacuum split.

On the common constant-`F_R` branch,

```text
delta S_m/delta chi =0;
delta S_EM/delta chi=0.
```

The standard Maxwell stress and conservation law remain unchanged, Newton
calibration remains `M_R^2=(8 pi G_N)^-1`, and the finite `P(X)` correction
to the already bounded local scalar response is negligible.

The exact checkpoint-5208 likelihood replay remains

```text
chi2_joint=1475.1718548063207.
```

Validation is `54/54 PASS`. The protected public worktree,
`formalization-workbench`, and the pre-existing six-path galaxy worktree
state are unchanged. No GitHub action occurred.

The next route is

```text
DERIVE_PARENT_VACUUM_COORDINATE_OWNERSHIP_OR_PROVE_
RENORMALIZATION_CONDITION_BOUNDARY.
```

This means determining whether the parent theory has a symmetry, constraint
or critical-surface condition that fixes the renormalized vacuum coordinate.
If it does not, `Lambda_cal` must be counted openly as an independent
renormalization datum rather than repeatedly asking the motion polynomial to
select it.

Authoritative files:

```text
5209-Y5-R2FR-finite-mass-essential-PX-threshold-backreaction-vacuum-rank-and-local-GR-Maxwell-gate.md;
scripts/Y5_R2FR_5209_finite_mass_PX_vacuum_branch_gate.py;
source-intake/functional_rg/5209/finite_mass_PX_vacuum_branch_results.json;
source-intake/mts_residuals/P8_Y5_BRR545_5209_VALIDATION.csv.
```

Locked SHA-256 values:

```text
document:
0e23836824de9281d17bbfb47c6c2350bc91e899356796cb640e622e342bc384;

script:
88c48a13192d1c394bfab38b9b0b894e866b9bc1eba403c8d5487a1e5386ca8a;

result JSON:
98dbaacbb1fafe5bb50dcc9999a4d64b0e94cabf5c4ff74f0b5aea2a5f14a598;

validation:
9b0aa85a4ad32bcf9734092247a4860c3550b07b35ef09cf68b74f3b2fbf0460;

5209 output tree:
82f99a33ff57310a1bd59484b3c035c1d9192f391e327f697f6ae33325b9bfe9;

5209 evidence CSV set:
bd7c18f88d15245f58f4ce195563233ea3a7441194b08dac78637d3868e83538;

formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758.
```

## Authoritative current handoff - checkpoint 5208

Checkpoint 5208 tests a cleaner connection between the cosmological motion
state and local GR than the finite-curvature branch.

For a single scalar with `Z(psi)>0`, the exact field coordinate

```text
chi(psi)=integral_0^psi sqrt(Z(u)) du
```

canonicalizes the kinetic term. Around the reflection-symmetric origin,

```text
m_can^2     =m2/Z0;
lambda_can  =lambda4/Z0^2-2m2 z2/Z0^3;
xi_can      =xi2/Z0;
zeta_c      =xi2/(2Z0);
c_X2,can    =c_X2/Z0^2.
```

Thus `Z`, `F_R`, `V` and `c_X2` are not four independent germs. The positive
`Z` function is an inessential field coordinate, while the displayed
canonical combinations are physical.

The locked Gaussian-matter source surface has

```text
lambda4=xi=z2=0,
```

the exact source-comparator mass eigenvector has no linear `xi` component,
the MTS regular quartic is irrelevant, and the essential functional `X^2`
trajectory has only the already known GR-connected relevant direction.
Therefore the leading common trajectory at the currently calculated order is

```text
F_R(chi)=M_R^2;
V(chi)=m_gap^2 chi^2/2;
Z_can=1;
P_ge2(X)=the locked GR-connected essential P(X) trajectory;
Lambda_cal=0 as an explicit branch hypothesis.
```

This is a two-scale theory. `G_N` and one universal
`J_gap=G_N m_gap^2` remain the two essential data; neither may be retuned by
arena.

The exact autonomous-flow covariance is

```text
u_delta(k)=u(exp(-delta)k);
G_N -> exp(-2delta)G_N;
m_gap -> exp(delta)m_gap;
G_N m_gap^2 -> G_N m_gap^2.
```

Consequently no autonomous dimensionless beta-function system can select an
absolute SI scale. Measured `G_N` is a legitimate dimensional integration
constant, not an unfinished dimensionless RG calculation. The parent can
still predict dimensionless ratios if its relevant trajectory locks them.

The direct `zeta_c=0` refit gives

```text
Omega_m              =0.311668148681;
mu=m_gap/H0          =0.764819326846;
H0                   =67.2431118289 km/s/Mpc;
Omega_b h^2          =0.0225663102893;
phi0                 =2.60060760456;
q0                   =-0.416353415857;
M_R^2/M_N^2          =1;
present source ratio =1;
gamma-1              =0;
Gdot/G               =0;
chi2_cosmology       =1474.066939052;
chi2_local           =1.104915754;
chi2_joint           =1475.171854806;
AIC_joint            =1489.171854806;
BIC_joint            =1527.023078780.
```

Relative to the fitted finite-`zeta_c` checkpoint-5207 branch:

```text
Delta chi2=+0.205226;
Delta AIC =-1.794774;
Delta BIC =-7.202091.
```

AIC is draw-scale but numerically favors the minimal branch; BIC clearly
favors it. The finite curvature coordinate is therefore not selected as the
parent default.

The current fitted scales are

```text
H0       =1.43437605062e-33 eV;
m_gap    =1.09703852548e-33 eV;
J_gap    =8.07403437276e-123.
```

The analytic perturbative mass-gravity size
`J_gap ln(M_N/H0)=1.11974e-120` would require an amplification of
`1.77944e115` to reproduce the fitted finite `zeta_c`; this is a
power-counting result, not a nonperturbative zero theorem.

On the selected constant-`F_R` branch, the direct material scalar charge is
exactly zero. A time-dependent homogeneous field can still respond indirectly
to a local metric perturbation. Including both the static potential term and
the causal `dot(Phi)` envelope gives

```text
max |delta chi/chi| <=6.87376e-24.
```

The largest homogeneous cosmological tidal-to-Newton ratio in the selected
local rows is `1.05415e-19`. Thus local GR does not require a dynamical
`phi_cosmology -> 0` transition on this branch, although the bounded
cosmological residual is not called identically zero.

The locked essential weak flow

```text
beta_g=2g;
beta_c=4c+16g^2;
c=A_X2 g^2;
beta_A_X2=16
```

was extrapolated from both checkpoint-4958 schemes over
`0.01<=k/H<=100`. On the exact refitted background,

```text
max |rho_X2/rho_kinetic|=7.86941e-120;
max |Omega_X2|          =1.36416e-120.
```

The generated `X^2` interaction remains in the action but is not a viable
cosmological fit coordinate.

Validation is `66/66 PASS`, including a fresh saved-output replay. The runner
now disables Python bytecode emission before importing checkpoint 5207, so its
own no-cache cleanliness gate is reproducible without a hidden environment
setting.

Authoritative files:

```text
5208-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-absolute-scale-covariance-and-local-GR-selection.md;
scripts/Y5_R2FR_5208_common_motion_trajectory_scale_covariance.py;
source-intake/functional_rg/5208/common_minimal_motion_trajectory_results.json;
source-intake/mts_residuals/P8_Y5_BRR545_5208_VALIDATION.csv.
```

Locked SHA-256 values:

```text
document:
95f49142309bcc8b438c864d170134b9952086ca6b23322960f8eec29edad8c8;

script:
e7a64067eb5ae71db6064c814f195a96a7ff25243827aa02ac719bc4adf07107;

result JSON:
fbda1e61e5eec0aed77f411fa6309b4e97c87b61e06b007684e9065af2ca70df;

validation:
78c9139c0dc4ac3b4bd58c80fceebcc01cc8b9a27a04836c41df24f81bc39015;

5208 output tree:
2e9a7a355e5d55b13c1258be9e4e677c4d948b5c0406b9ad9297a8fe76934160;

5208 evidence CSV set:
f34e01d85c80fc7a67ee0700f8b812602ac1f5b84e711bc8c36a5151ccf35b36;

formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758.
```

No GitHub action occurred. The public worktree stayed clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`. The galaxy repository remained
read-only at `f850e4997657f457dddc05cbe50f21186588dcc7` with its six pre-existing
dirty paths unchanged. No script `__pycache__` remains.

Selected next route:

```text
DERIVE_FINITE_MASS_ESSENTIAL_PX_BACKREACTION_AND_VACUUM_BRANCH_SELECTION.
```

The immediate target is to include the universal mass deformation in the
essential functional `P(X)` flow and test whether it changes the source-fixed
trajectory beyond the tiny analytic `J_gap` estimate. The independent
vacuum-energy question remains: checkpoint 5205 fixes the homogeneous state
only after `Lambda_cal=0` is declared, so a parent vacuum-branch selection
theorem is still required or the zero-`Lambda` label must remain conditional.

## Authoritative current handoff - checkpoint 5207

Checkpoint 5207 removes the remaining measured-source convention from the
finite-`zeta_c` background tested in checkpoint 5206.

Define the measured reduced Newton scale by

```text
M_N^2=1/(8 pi G_N).
```

For the parent Jordan action, the present Cavendish coupling is

```text
G_cav,0
 =1/(8 pi M_R^2)
  [(2f0+4f_phi0^2)/(2f0+3f_phi0^2)]/f0
 =g0/(8 pi M_R^2).
```

Equating the predicted and measured couplings derives

```text
s=M_R^2/M_N^2=g0;
Omega_i,bare=Omega_i,observed/s.
```

At every likelihood evaluation the runner now solves the two simultaneous
boundary conditions

```text
ln E(0)^2=0;
ln[s/g(phi0)]=0
```

for the regular-mode amplitude and `s`. The growth source then contains
`Omega_m,bare G_eff/G_bare`, which exactly reduces at the present epoch to
the measured source `Omega_m,observed`. No source-normalization coefficient
is fitted.

The self-consistent signed fit is

```text
zeta_c                    =-1.99251066833e-5;
Omega_m,observed          = 0.311668148681;
Omega_m,bare              = 0.311626152088;
mu=m_gap/H0               = 0.764819326846;
H0                        =67.2431118289 km/s/Mpc;
phi0                      = 2.60046992189;
q0                        =-0.416499237103;
M_R^2/M_N^2               = 1.00013476594;
M_R/M_N                   = 1.00006738070;
G_bare/G_N                = 0.999865252216;
gamma-1                   =-1.07404748973e-8;
Gdot/G                    =-2.96875085343e-15 yr^-1;
chi2_cosmology            =1474.087357302;
chi2_local                =   0.879271026;
chi2_joint                =1474.966628328.
```

The present Poisson-source residual is `2.22045e-16`. The optimum is
interior, both conservative local two-sigma envelopes pass, and the full
regular/numerical ledger passes.

Relative to the uncalibrated checkpoint-5206 signed fit:

```text
Delta chi2_joint=-0.106703;
Delta AIC_joint =-0.106703;
Delta BIC_joint =-0.106703.
```

The source correction therefore moves the score slightly in the favorable
direction but is too small to change model selection. Relative to fitted
`LCDM`, the calibrated branch has `Delta chi2=-3.35353`,
`Delta AIC=+0.64647` and `Delta BIC=+11.46111`. Relative to fitted `wCDM`,
it has `Delta AIC=-0.09393` and `Delta BIC=+5.31338`. This is an allowed
near-GR corridor, not evidence for a nonzero coupling.

The exact local branch `phi_local=q_local=0` still gives
`M_R=M_N` conditionally, but no dynamical transition from the cosmological
field state to that local branch has been derived. The absolute numerical
magnitude of `G_N` also remains a measured input: only the dimensionless
parent-to-measured scale ratio is derived here.

Validation is `54/54 PASS`, including a fresh saved-output replay.

Authoritative files:

```text
5207-Y5-R2FR-Cavendish-normalized-parent-scale-observed-density-map-and-self-consistent-source-calibrated-refit.md;
scripts/Y5_R2FR_5207_Cavendish_source_calibrated_refit.py;
source-intake/functional_rg/5207/Cavendish_source_calibrated_results.json;
source-intake/mts_residuals/P8_Y5_BRR545_5207_VALIDATION.csv.
```

Locked SHA-256 values:

```text
document:
8d0b856b7d53bc6b762ff8278eed98999e80079c948d47436db92bfd84bdfb32;

script:
9a130cb1f1fbb7c7188c5e73aeffe9e36eca6f4f6409db02abf9299b492f8e61;

result JSON:
a322ddacd011a47cfa288bf832ff953ab8a4c349d24bf2e03066b9ebfa1e24d8;

validation:
24998ad798103351d38071920cd8ba4a47c22ae635f9264e0636b861fb117d6d;

5207 output tree:
2103eb667ac80716c3ddb884fd7157111c0e8de1cbc0abaa308d6c946d906788;

formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758.
```

No GitHub action occurred. The public worktree stayed clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`. The galaxy repository remained
read-only at `f850e4997657f457dddc05cbe50f21186588dcc7` with its six pre-existing
dirty paths unchanged. No script `__pycache__` remains.

Selected next route:

```text
DERIVE_COMMON_F_R_V_Z_X2_RUNNING_AND_ABSOLUTE_PARENT_SCALE_SELECTION.
```

The source-normalization gap is now closed. The next finite derivation must
ask whether one common parent trajectory selects the curvature coupling,
potential, kinetic normalization and higher-derivative coefficient rather
than fitting them independently. Absolute `G_N` may remain a boundary datum
unless a genuine dimensional-transmutation or parent scale-selection
mechanism can be constructed.

## Authoritative current handoff - checkpoint 5206

Checkpoint 5206 executes the constraint-reduced scalar-tensor refit selected
by checkpoint 5205. It does not reuse the minimal background at finite
coupling.

The tested Jordan truncation is

```text
F/M_R^2=1+zeta_c phi^2;
Z=1;
V=M_R^2 m_gap^2 phi^2/2;
Lambda_cal=0.
```

With `q=dphi/dN`, the exact solved background system is

```text
E^2[f+f_N-q^2/6]
 =Omega_m exp(-3N)+Omega_r exp(-4N)+mu^2 phi^2/6;

q_N=-(3+h)q-mu^2 phi/E^2+6 zeta_c phi(2+h);
```

and the independent spatial metric equation is solved algebraically for
`h=d ln H/dN`. SymPy returns exact zero after substitution into both the
Raychaudhuri and scalar equations.

The regular Frobenius branch is imposed at `N=-18`:

```text
q_i/phi_i
 =(3/2)zeta_c(Omega_m/Omega_r)a_i
  -mu^2 a_i^4/(5 Omega_r)
  +O(r_i^2,a_i^5).
```

The singular mode is excluded. The only homogeneous amplitude is shot until
the Hamiltonian constraint gives `E(0)=1`. Thus neither a present phase nor a
scalar fraction is fitted.

The exact `zeta_c=0` implementation reproduces the locked checkpoint-5195
zero-Lambda total cosmology score with

```text
Delta chi2=-2.74531e-9.
```

The matched primary calculation retains the 1624 Pantheon+ noncalibrator
rows, 13 DESI DR2 BAO rows, five primary `f sigma8` rows and four
compressed-CMB rows. At finite coupling:

* the scalar-tensor `E(N)` is used in the sound-horizon response;
* subhorizon growth uses the derived long-range `G_eff/G_bare`;
* the maximum omitted Yukawa correction at `k=0.01 h/Mpc` is `6.50e-4`;
* Cassini `gamma-1` and LLR `Gdot/G` are scored directly at every likelihood
  evaluation rather than converted into a frozen prior ceiling.

The signed fit is

```text
zeta_c                    =-1.99251066833e-5;
Omega_m                   = 0.311668148681;
mu=m_gap/H0               = 0.764819326846;
H0                        =67.2431118289 km/s/Mpc;
phi0                      = 2.60039240629;
q0                        =-0.416479785119;
gamma-1                   =-1.07398345098e-8;
Gdot/G                    =-2.96852368915e-15 yr^-1;
G_cav/G_bare              = 1.00013475791;
chi2_cosmology            =1474.194050659;
chi2_local                =   0.879280989;
chi2_joint                =1475.073331648.
```

The signed optimum is interior and passes both conservative local
two-sigma envelopes. Relative to the locked minimal zero-Lambda parent:

```text
Delta chi2_joint=-0.100665;
Delta AIC_joint =+1.899335;
Delta BIC_joint =+7.306653.
```

Therefore the local rows weakly prefer a tiny negative coupling, but the
improvement does not pay for the extra action coefficient. This is an
allowed near-GR corridor, not evidence for nonzero `zeta_c`.

The positive-only fit returns to

```text
zeta_c=0
```

and is correctly marked as edge-hitting. Positive curvature coupling is not
selected by the joint data.

Validation is `83/83 PASS`. The constraint is evaluated as a relative
dimensionless residual so the early radiation subtraction is not falsely
judged in absolute units. The finite-`zeta_c` `d ln E/dN` residual,
initial-surface sensitivity, positive-`F`, Einstein-frame kinetic sign,
source-normalization growth sensitivity and range approximation all pass.

Authoritative files:

```text
5206-Y5-R2FR-constraint-reduced-zero-Lambda-Jordan-scalar-tensor-refit-local-Gdot-and-competitive-model-gate.md;
scripts/Y5_R2FR_5206_constraint_reduced_scalar_tensor_refit.py;
source-intake/functional_rg/5206/constraint_reduced_scalar_tensor_results.json;
source-intake/mts_residuals/P8_Y5_BRR545_5206_VALIDATION.csv.
```

Locked SHA-256 values:

```text
document:
2e573b6e7027840b6289b647fc27c966caf39f507fe20bd3422e3f3ab810258e;

script:
da79179a8ad55644cc952ca29972e6d3b44f8e8f08e6586675a3170c971ceedc;

result JSON:
aa09f6859f23954551e44b81e672500099649493964fa7cc9b02a27584d8ddd4;

validation:
e46b85c24f42415363f1781306c8541a34c2b02d2f9ce4876d40d4f30ab8ff55;

5206 output tree:
65cf9be0a79fc358252a9f997c620329fe708c017b159194f21086d20b604b01;

formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758.
```

No GitHub action occurred. The public worktree stayed clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`. The galaxy repository remained
read-only at `f850e4997657f457dddc05cbe50f21186588dcc7` with its six pre-existing
dirty paths unchanged. No script `__pycache__` remains.

Selected next route:

```text
DERIVE_COMMON_F_R_V_Z_X2_TRAJECTORY_AND_PRESENT_G_SOURCE_NORMALIZATION.
```

The immediate finite target is the second clause. Calibrate the action scale
to measured Cavendish gravity self-consistently:

```text
G_N=G_cav,0
   ={1/(8 pi M_R^2)}
     [(2f0+4f_phi0^2)/(2f0+3f_phi0^2)]/f0;

M_R^2/M_N^2=G_cav,0/G_bare.
```

Then rerun or perturbatively bound the background with
`Omega_i,bare=Omega_i,observed/(M_R^2/M_N^2)` and growth source
`Omega_m,observed G_eff/G_cav,0`. This must determine whether the tiny signed
optimum survives exact source calibration. It cannot derive the absolute
dimensionful value of `G_N`; that still requires a parent scale-selection
mechanism.

## Authoritative current handoff - checkpoint 5205

Checkpoint 5205 fills the homogeneous part of the checkpoint-5203
`Gamma_rho_i` slot with a positive normalized CTP state class rather than
leaving the amplitude as an unnamed boundary number.

For one finite regulated homogeneous cell,

```text
rho_i
 =int dA P(A)
   D(A v_reg) rho_0 D(A v_reg)^dagger,

int dA P(A)=1;
P(A)=P(-A).
```

Here `rho_0` is centered and parity even, while `v_reg` is the phase-space
direction fixed by radiation regularity. Therefore `rho_i` is positive and
trace one, and

```text
<chi>=<chi_N>=0;
<A^2>=sigma_A^2.
```

For Gaussian `P`, the exact covariance is

```text
V_i=V_0+sigma_A^2 v_reg v_reg^T.
```

With `V_0=diag(Q_0,1/(4Q_0))`,

```text
det V_i
 =1/4
  +sigma_A^2[
    Q_0 v_p^2+v_q^2/(4Q_0)
   ]
 >=1/4.
```

The exact density kernel has unit trace and zero Hermiticity residual. The
implementation also passes 256 deterministic covariance-positivity trials.

Every source-free regular homogeneous history is

```text
chi_A(N)=A u_reg(N).
```

At minimal canonical quadratic order,

```text
<chi^2>=sigma_A^2 u_reg^2;
<chi_N^2>=sigma_A^2 u_reg,N^2;

rho_chi
 =3M_R^2H0^2 sigma_A^2
  (E^2u_N^2+mu^2u^2);

p_chi
 =3M_R^2H0^2 sigma_A^2
  (E^2u_N^2-mu^2u^2).
```

The equation of state is independent of the detailed amplitude distribution.
Higher moments remain physical for interactions and perturbations but do not
enter this background truncation.

Direct differentiation with the unit-mode equation returns

```text
rho_chi,N+3(rho_chi+p_chi)=0.
```

No externally time-dependent state weight is inserted.

The flat Hamiltonian constraint is

```text
Omega_Lambda+K_0 sigma_A^2
 =1-Omega_m-Omega_r;

K_0=u_N0^2+mu^2u_0^2.
```

Its matrix `[1,K_0]` has rank one over the two coordinates
`{Omega_Lambda,sigma_A^2}`. Therefore:

```text
free Lambda:
  one joint vacuum/state degeneracy remains;

declared Lambda=0:
  sigma_A^2=(1-Omega_m-Omega_r)/K_0
  is unique and positive.
```

The locked target reconstruction is

```text
free Lambda:
 A_reg(-12)=0.4267395644;
 K_0=1.1080370029;
 sigma_A^2=0.1821066558;
 residual=0;

Lambda=0:
 A_reg(-12)=1.1524890880;
 K_0=0.5181888856;
 sigma_A^2=1.3282310980;
 residual=-6.66e-16.
```

The raw checkpoint-5195 flatness and present-state coordinates also match the
independently rebuilt checkpoint-5196 transfer to validation tolerance.

Thus the zero-`Lambda` quadratic background has:

```text
regular phase:
  derived;

homogeneous state second moment:
  fixed by the Hamiltonian constraint;

independent homogeneous amplitude fit coordinate:
  none.
```

This does not derive the absolute statement `Lambda_cal=0`; that remains a
tested minimal-branch hypothesis. It also does not select higher state moments
or the primordial inhomogeneous covariance.

The CTP functional is supported on the initial Cauchy surface, so its direct
functional derivative vanishes in a later disjoint compact domain. The even
mixture removes odd one-point charge but does not cancel quadratic stress,
`alpha_0^2` or `Gdot/G`. The checkpoint-5204 local ceilings remain mandatory.

Validation:

```text
81/81 PASS;
9 evidence files;
5205 output tree:
a8fd68722c7d95fe2a88a043a62f10fb3c33ebfc5f6492adb99bb44c529e23b4;
formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5204 output:
311d5947bed4a1faf354108823ac19a5bdb93ed4dfc181c95a95f8ab530c7108.
```

No GitHub action occurred. The public worktree and galaxy repository were not
modified.

The selected next route is

```text
RUN_CONSTRAINT_REDUCED_ZERO_LAMBDA_SCALAR_TENSOR_REFIT_
WITH_GDOT_BOUNDED_ZETA.
```

That fit must use the full checkpoint-5203 Jordan-frame equations, derive the
state variance from flatness at every evaluation, shoot the regular phase,
retain the checkpoint-5204 local `zeta_c` bound, and compare against fitted
`Lambda`CDM, `wCDM`, CPL and the locked minimal scalar without adding a state
parameter.

## Previous handoff - checkpoint 5204

Checkpoint 5204 attempts the concrete curvature-trigger route for preparing
the fitted homogeneous motion state. It derives and rejects that mechanism
rather than writing another coefficient-gap ledger.

The canonical convention is now fixed:

```text
chi=sqrt(Z0) psi;
zeta_c=F_R''(0)/(2 Z0);
F_R=M_R^2+zeta_c chi^2+O(chi^4);

xi_4951=zeta_c=xi2_5203/(2 Z0).
```

This removes the factor-of-two ambiguity between the 4951 Euclidean
`V-FR+ZX` convention and the 5203 Lorentzian `F_R R/2` convention.

The exact homogeneous fixed-curvature functional is

```text
V_eff
 =(m_pole^2-zeta_c R)chi^2/2
  +lambda4 chi^4/24.
```

For `lambda4>0`, the nonzero extrema obey

```text
chi_*^2=6(zeta_c R-m_pole^2)/lambda4;
V_eff''(chi_*)=2(zeta_c R-m_pole^2);
Delta V_eff=-3(zeta_c R-m_pole^2)^2/(2lambda4).
```

Thus the pitchfork exists, but `chi=0` remains an exact homogeneous solution
and the nonzero minima return continuously to zero at curvature restoration.

The checkpoint-5195 fitted targets reconstruct to

```text
Lambda free:
 chi0/M_R=0.8413859236;
 d(chi/M_R)/dN=-0.3687804316;
 R0/H0^2=8.806623944.

Lambda zero:
 chi0/M_R=2.604048209;
 d(chi/M_R)/dN=-0.4158524805;
 R0/H0^2=8.675401477.
```

Jordan-minimal matter maps exactly to

```text
A_E^2=M_R^2/F_R=(1+zeta_c phi^2)^-1;

alpha0^2
 =F_R,chi^2/(2F_R+3F_R,chi^2);

gamma-1=-2alpha0^2/(1+alpha0^2);

G_cav
 =1/(8pi F_R)
  (2F_R+4F_R,chi^2)/(2F_R+3F_R,chi^2).
```

Using deliberately conservative absolute two-sigma envelopes gives

```text
Cassini |gamma-1| <6.7e-5:
 zeta_c<4.87292e-3 or 1.58016e-3.

LLR |Gdot/G| <2.42e-14 yr^-1:
 zeta_c<5.65824e-4 or 1.62711e-4.
```

The LLR bound is stronger because the fitted states are moving.

Remaining curvature-broken today requires

```text
zeta_c>m_pole^2/R0
      =0.1723780035 or 0.06725848292.
```

These floors are respectively `304.65` and `413.36` times above the LLR
ceilings. The present broken-state/local-bound intersection is empty.

Deep in matter domination,

```text
m_rad^2/H^2 ->6 zeta_c.
```

Even the deliberately weak tracking requirement `m_rad>=H` needs
`zeta_c>=1/6`, which is `294.56` or `1024.31` times above the LLR ceilings.
The curvature minima cannot adiabatically select and normalize the state.

The exact matter-era growing index is

```text
s_+
 =[-3/2+sqrt(9/4+12zeta_c)]/2.
```

At the LLR ceilings, the deliberately extended equality-to-today growth
factors are only `1.00925` and `1.00266`. The actual tachyonic intervals end
near `z=13.25` and `14.65`, giving `1.00622` and `1.00176`. Any surviving
amplitude remains initial-state data.

The scalar is solar-system long ranged:

```text
m_pole AU=1.34478e-15 or 8.30650e-16.
```

The allowed couplings are also factors `4218.68` and `14670.34` below the
checkpoint-4950 neutron-star top-hat threshold. Compact stability passes;
the route fails specifically as a cosmological state selector.

The fixed-background flow has the exact first integral

```text
(zeta_c-1/6)/lambda4^(1/3)=constant.
```

It transports rather than predicts the physical trajectory. Preserving the
5195 quadratic targets to ten percent requires

```text
lambda4<8.99e-121 or 3.58e-122,
```

so this displayed infrared running is ineffective as a cosmological
selector.

The decision is

```text
curvature-triggered 5195 state preparation = rejected;
near-minimal F_R EFT coordinate            = retained;
common F_R,V,Z,X2 packet rejected          = no;
5203 local GR/Newton/Maxwell branch         = retained;
5195 scalar likelihood promoted            = no.
```

Validation:

```text
78/78 PASS;
7 evidence files;
5204 output tree:
311d5947bed4a1faf354108823ac19a5bdb93ed4dfc181c95a95f8ab530c7108;
formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5203 output:
acb402fb2b8b9b5add00884ade75a720675b3f62fc3bf45a5de86038b00e9eeb.
```

No GitHub action occurred. The galaxy repository and public worktree remain
untouched.

The selected next route is

```text
DERIVE_CTP_HOMOGENEOUS_STATE_PREPARATION_OR_DEMOTE_PARENT_SCALAR_COSMOLOGY.
```

It must start from the already required `Gamma_rho_i[Sigma_i]`, produce a
normalized regular radiation-era state, conserve bulk-plus-state stress,
remain silent on the local stationary branch, and determine the 5195
amplitude and phase without fitting new parent constants. If that cannot be
derived, the likelihood branch is retained as phenomenology but demoted to
fitted closure.

## Previous handoff - checkpoint 5203

Checkpoint 5203 assembles one CTP/translation-gauge parent rather than
treating the local, FLRW and collective sectors as unrelated actions:

```text
Gamma_CTP
 =S_can[+]-S_can[-]+Gamma_IF+Gamma_rho_i,

e^A_mu=D_mu X^A+mathcalB^A_mu.
```

The displayed single-copy action contains

```text
-F_R(psi)T_TEGR/2
-T^mu partial_mu F_R(psi)
-U_Lambda
-Z(psi)X_psi/2
-V_even(psi)
+P_ge_2(X_psi)
-Z_A F^2/4
+c_IR CFF
+G_C3 Tr(C^3)
-u_O4 C^2 X_psi
+S_visible
+Gamma_contact+Gamma_nonlocal+Gamma_p8plus
+matched boundary.
```

The scalar-curvature conversion is exact:

```text
F_R R_LC/2
 =-F_R T_TEGR/2
  -T^mu partial_mu F_R
  +boundary.
```

The generator returns zero product-rule residual. The derivative
torsion-vector term is compulsory; `-F_R T/2` alone is a different
scalar-torsion theory whenever `F_R` varies.

The independent variation chain is

```text
delta Gamma/delta mathcalB^A_mu=E_A^mu[e],

delta Gamma/delta X^A=-D_mu E_A^mu.
```

An exact finite adjoint test gives a zero residual matrix. The relational
labels add no independent equations.

For analytic `Z2`-even functions,

```text
F_R'(0)=Z_A'(0)=A_matter'(0)=V_even'(0)=0.
```

Therefore at `psi=0`:

```text
combined additive scalar source=0;
Gamma_hpsi=0;
Gamma_Apsi=0;
Gamma_matter,psi=0.
```

This proves stationarity and quadratic block diagonality, not automatic
stability. The second derivatives remain in `K_psi_psi`; the local physical
branch requires a positive scalar spectrum and separate state selection.

The motion functional cannot be silently reduced to the old minimal block.
The executed curved-scalar comparator gives

```text
beta_lambda=3lambda_4^2/(16pi^2),

beta_xi=lambda_4(xi-1/6)/(16pi^2),

beta_xi|xi=0=-lambda_4/(96pi^2).
```

Thus `xi=0` is not invariant in that comparator when the quartic is nonzero.
The common bulk packet

```text
F_R(psi),V_even(psi),Z(psi),c_X2
```

must be solved on one trajectory. `R psi^2` is retained for RG closure but
is not reopened as a galaxy trigger; checkpoint 4950 already rejects its
galaxy/local activation window.

The branch-relevant parity-even operator basis through dimension eight has

```text
19 classified rows;
14 symmetry-allowed rows;
14/14 allowed rows assigned to a parent block, a locked forbid theorem,
a correlated basis coefficient, or a separate-theory rejection.
```

Direct fixed-metric hidden-visible portals remain absent by checkpoint 4919.
Ordinary `R Hdagger H` remains in the visible EFT. Incomplete scalar-torsion
and independent torsion-current matter couplings are not smuggled into the
GR-connected parent.

Branch reductions:

```text
local leading GR/Newton/PPN/Maxwell:
  derived from the same action, conditional on psi=0, positive K_psi_psi,
  rho_i=rho_0 and one coframe;

flat FLRW:
  equations derived from the same action;
  C3,CFF,O4 background blocks vanish because Weyl=0;
  functional trajectory and homogeneous state remain open;

galaxy collective CTP:
  compatible with the same bulk action and state slot;
  Gamma_rho_i preparation, |k|^(1+q), q, s=4, B=8 and stress projection
  remain underived.
```

No branch-specific bulk value of `G_N`, `alpha_EM` or `m_pole` is allowed.

The state Ward gate is

```text
DeltaT_state[n]=n(T_1-T_0),

nabla_mu DeltaT_state^mu_nu
 =(partial_mu n)DeltaT_10^mu_nu
  +n nabla_mu DeltaT_10^mu_nu.
```

The product-rule residual is zero. A prescribed logistic profile is not
automatically conserved; it must solve the state equation from
`Gamma_rho_i`. Exact local silence requires `n=0` and `partial n=0` on an
open domain.

Validation:

```text
125/125 PASS;
12 evidence files;
5203 output tree:
acb402fb2b8b9b5add00884ade75a720675b3f62fc3bf45a5de86038b00e9eeb;
formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5202 output:
56ed69780a647a3cb65da2943e274f717a2ab532d4641e17251f0e0dadd1d8bb.
```

The selected next route is

```text
SOLVE_OR_REJECT_COMMON_F_R_V_Z_X2_MOTION_TRAJECTORY.
```

It must establish one GR-connected functional trajectory with
`F_R(0)>0`, `Z(0)>0`, positive local `K_psi_psi`, one universal pole,
stable FLRW evolution, no direct visible portal, no reopened galaxy/local
scalarization window and no arena retuning.

## Previous handoff - checkpoint 5202

Checkpoint 5202 attempts the missing non-scalar ancestry rather than merely
listing it as a target.

The scalar-only route is now closed:

```text
N scalar gradients -> rank(g)<=N;
N<4 -> degenerate;
N=4 with fixed eta_AB -> coordinate pullback of flat spacetime;
one extra conformal scalar -> Weyl[g]=0;
arbitrary G_AB(X) -> reintroduced ten-component metric content.
```

Therefore the old single motion scalar cannot generate a curved local-GR
coframe. It remains a clock/matter excitation rather than the spatial
geometry ancestor.

The constructive replacement is

```text
e^A = D_omega X^A + mathcalB^A,

X^A=(one relational clock, three relational rods),
mathcalB^A_mu=translation/motion connection,
R^A_B[omega_inertial]=0.
```

Under

```text
X'^A=X^A+epsilon^A,
mathcalB'^A=mathcalB^A-D_omega epsilon^A,
```

the coframe is exactly invariant. An exact rational test returns a zero
residual matrix and a nondegenerate sample determinant `-3`. Local Lorentz
rotation changes the frame but leaves

```text
g_mu_nu=eta_AB e^A_mu e^B_nu
```

exactly invariant.

For a flat inertial Lorentz connection,

```text
T^A=D_omega e^A=D_omega mathcalB^A.
```

Thus `mathcalB^A` supplies the nonholonomy that exact scalar gradients
cannot. It is a new minimum non-scalar parent field, not a relabeling of the
old scalar and not the galaxy exponent `B=8`.

For the parity-even quadratic torsion family

```text
L=c1 I1+c2 I2+c3 I3,
```

the pure-tetrad frame-null coefficient matrix has rank two and nullity one.
The unique ray is

```text
(c1,c2,c3)=(-1/4,-1/2,+1),
L=-T_TEGR.
```

Necessity is obtained from exact rational momentum constraints. Sufficiency
is verified for arbitrary symbolic `k_mu`: all six pure-tetrad frame
directions and four linearized diffeomorphism directions are exact Hessian
nulls. A generic `I1` action fails the frame-null test.

The selected generic-momentum Hessian has

```text
rank=6,
nullity=10,
combined gauge-null rank=10.
```

This rank is not miscounted as six propagating modes. The nonlinear
two-tensor-mode statement follows from the exact action identity

```text
R_LC=-T_TEGR+2e^-1 partial_mu(e T^mu).
```

The exact symbolic witnesses are

```text
flat FLRW:                    R+T-B=0;
spatial conformal coframe:    R+T-B=0;
anholonomic shear:
  T=0, R=-2 kappa_s^2, B=-2 kappa_s^2, R+T-B=0.
```

The last witness is explicitly boundary-sensitive. EH/TEGR equality
requires matched boundary data rather than silent deletion of the
divergence term.

For transverse-traceless modes,

```text
L_TT=(h_plus^2+h_cross^2)(omega^2-k^2)/2,
```

so the kinetic residue is positive for `M_R^2>0`. Generic NGR coefficients,
`f(T)`, separate `X` kinetic terms, mass/reference-metric potentials and an
independent curved Lorentz connection are not admitted into this minimum
parent without separate mode analysis.

The source chain is exact:

```text
delta S/delta mathcalB^A_mu=delta S/delta e^A_mu,

delta S/delta X^A
 =-D_mu(delta S/delta e^A_mu).
```

The `X^A` equation is a Ward consequence, not an extra scalar mode. With all
matter coupled to the same coframe, checkpoint 5201 is inherited exactly:

```text
M_R^2(G_mu_nu+Lambda_cal g_mu_nu)=T_total_mu_nu;

nabla^2 Phi=4pi G_N rho;
G_N=1/(8pi M_R^2);

(gamma,beta,xi,alpha1,alpha2,alpha3,
 zeta1,zeta2,zeta3,zeta4)
=(1,1,0,0,0,0,0,0,0,0);

T_00^EM=(E^2+B^2)/2;
T_0i^EM=(E cross B)_i.
```

The current claim boundary is:

```text
constructed:
  minimum translation-gauge TEGR parent candidate;
derived:
  scalar no-go, gauge factorization, TEGR coefficient ray,
  exact local Einstein equivalence, two tensor modes and source inheritance;
not derived:
  mathcalB from the old scalar, its microscopic origin, absolute G_N,
  dynamic local-state selection, galaxy phase parameters or full unification.
```

Validation:

```text
107/107 PASS;
11 evidence files;
5202 output tree:
56ed69780a647a3cb65da2943e274f717a2ab532d4641e17251f0e0dadd1d8bb;
formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5201 output:
310a38df16ccf617e6a28124afa717bac1aa2802fc9202853e8a3613d8c583b0.
```

The selected next route is

```text
ASSEMBLE_ONE_CANONICAL_TRANSLATION_GAUGE_MTS_PARENT_ACTION.
```

That action must contain the relational packet, translation connection,
TEGR local block, one universal matter/Maxwell coframe, old motion scalar,
controlled metric-EFT corridor and CTP state sector. Its cross-couplings
must be symmetry-classified so the local, galactic and cosmological branches
become limits of one action rather than separately tuned models.

## Previous handoff - checkpoint 5201

Checkpoint 5201 returns to the primary local-GR/source-coupling spine and
executes the complete current-parent variation.

The parent under test is

```text
S_parent
 =(M_R^2/2) int e(R-2 Lambda_cal)
 -(Z_A/4) int e F^2
 +S_visible[e,omega_LC[e],A,Phi_visible]
 +S_motion[e,psi]
 +Gamma_controlled_EFT
 +Gamma_rho0.
```

The coframe-to-metric source Jacobian was built explicitly:

```text
coframe components                  =16;
metric source components            =10;
rank(delta g/delta e)               =10;
nullity                             =6;
rank(local Lorentz generators)      =6;
maximum Lorentz-null residual       =0.
```

Thus one coframe variation retains every symmetric Hilbert source component
and its only null directions are the six local-Lorentz gauge directions.

The matter variation and Ward chain is

```text
T_a^m=-(1/e) delta S_visible/delta e^a_m,
J^m=-(1/e) delta S_visible/delta A_m,

T_[ab]+(1/2)nabla_m S^m_ab=0,

nabla_m T_visible^m_n
 =F_nm J^m+sum_i E_i nabla_n Phi_i,

nabla_m J^m=0
```

and, on all field equations,

```text
nabla_m(
 T_visible^m_n+T_EM^m_n+T_psi^m_n
 +DeltaT_EFT^m_n+DeltaT_state^m_n
)=0.
```

The direct symbolic weak-field calculation gives

```text
ds^2=-(1+2 Phi)dt^2+(1-2 Psi)delta_ij dx^i dx^j,

G00^(1)=2 nabla^2 Psi,
G12^(1)=partial_x partial_y(Psi-Phi).
```

On the local zero-anisotropic-stress branch,

```text
Phi=Psi,
nabla^2 Phi=rho/(2M_R^2)=4pi G_N rho,
G_N=1/(8pi M_R^2),
Phi=-G_N M/r,
a=-grad Phi.
```

The isotropic Schwarzschild expansion was executed:

```text
g00=-1+2U-2U^2+O(U^3),
gij=[1+2U+(3/2)U^2+O(U^3)]delta_ij,
```

so `beta=gamma=1`.

The complete constant PPN vector is

```text
(gamma,beta,xi,alpha_1,alpha_2,alpha_3,
 zeta_1,zeta_2,zeta_3,zeta_4)

=(1,1,0,0,0,0,0,0,0,0)
```

on the declared one-coframe, `psi=0`, open-domain boundary-vacuum branch.
The preferred-frame entries vanish because there is no local preferred
tensor or extra pole; the `zeta` entries vanish from the conserved
action-based Hilbert source; `xi` vanishes because the local Einstein branch
contains no preferred-location/Whitehead term.

The direct Maxwell contraction gives

```text
F_mn F^mn=2(B^2-E^2),
T_EM^00=(E^2+B^2)/2,
T_EM^0i=(E cross B)^i,
T_EM^m_m=0.
```

The same coframe therefore carries Maxwell energy and Poynting momentum into
the Einstein source. Poynting is not an independent background coupling.

The ten-observable normalization matrix has

```text
gravity block rank        =1;
electromagnetic block rank=1;
combined rank             =2;
arena-dependent gravity calibrations=0.
```

The physical leading normalizations are exactly

```text
G_N <-> M_R,
alpha_EM <-> e^2/Z_A.
```

For six source classes, the soft/Bianchi difference matrix has rank five and
nullity one, with nullspace `(1,1,1,1,1,1)`. Ordinary mass, binding energy,
electromagnetic stress, motion stress, clock energy and radiation therefore
share one spin-two residue.

The locked calibration gives

```text
G_N=6.708832120298927e-57 eV^-2,
M_R=[8pi G_N]^-1/2=2.435323210689248e27 eV.
```

The relation and cross-arena universality are derived. The absolute value of
`G_N` remains one measured scale, not a prediction of the current
dimensionless parent.

The boundary-state local-silence theorem is

```text
rho(n)=(1-n)rho_0+n rho_1,

DeltaT_mn[n]
 =Tr[(rho(n)-rho_0)T_mn]
 =n(T1_mn-T0_mn).
```

Therefore `DeltaT[0]=0`, but its Ward source is

```text
nabla_m DeltaT^m_n
 =(partial_m n)DeltaT10^m_n
 +n nabla_m DeltaT10^m_n.
```

Exact local silence requires `n=0` and `partial n=0` on an open domain.
Pointwise zero is insufficient. A finite logistic profile obeys strictly
`0<n<1`, so it cannot be relabelled an exact local vacuum.

The correct current state contract is

```text
rho_local=rho_0,
rho_collective=rho[n_environment].
```

This route separation is mathematically consistent. Dynamic preparation of
the local vacuum is not yet derived.

The locked higher-gradient corridor remains quarantined:

```text
maximum O4 local scalar-cone shift          =0;
maximum O4 tree metric stress at psi=0      =0;
maximum standard Delta gamma                =0;
maximum standard Delta beta                 =0;
maximum sourced C3 acceleration fraction    =1.512455748599783e-158;
maximum parent-only CFF speed fraction      =1.1374144856001986e-79;
physical total c_IR                         =open.
```

The decision is:

```text
one source-complete local coframe variation:
  derived;

Einstein -> Poisson -> Newton:
  executed;

full constant PPN vector:
  GR on the declared local-vacuum branch;

Maxwell -> stress -> Poynting:
  executed;

leading local source calibration rank:
  two with no arena retuning;

absolute G_N:
  one empirical scale;

exact local boundary-state silence:
  proved for an open P0-vacuum domain;

dynamic local-vacuum selection:
  open;

non-scalar coframe derived from old one-scalar MTS:
  no;

full MTS:
  not claimed.
```

The next calculation should not re-derive Poisson or repeat PPN. It must
derive or reject the smallest non-scalar ancestry candidate for the coframe:
four relational clock/rod fields plus the minimal internal distortion, with
rank, Diff/local-Lorentz identities, constraint count, two tensor modes and
ghost gates. If that route fails, the coframe must be declared fundamental
MTS field content rather than attributed to the old scalar.

Executable:

```text
scripts/Y5_R2FR_5201_source_complete_coframe_PPN_local_silence_gate.py
```

Evidence:

```text
source-intake/functional_rg/5201/
```

Validation:

```text
source-intake/mts_residuals/P8_Y5_BRR545_5201_VALIDATION.csv
117/117 PASS.
```

Locks:

```text
checkpoint-5201 output tree:
  310a38df16ccf617e6a28124afa717bac1aa2802fc9202853e8a3613d8c583b0

formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758

checkpoint-5200 output:
  acc19e684b35c7aff65923713812b6416e8cb5ea5212ddc5645f3802c37f4075

public worktree:
  8913c00b77d98e457ddb0c48e9aeec9cc5f309fd, clean

galaxy repository:
  f850e4997657f457dddc05cbe50f21186588dcc7, unchanged pre-existing dirty state
```

No GitHub action occurred. The protected `formalization-workbench` and galaxy
repository were not modified.

## Previous authoritative handoff - checkpoint 5200

Checkpoint 5200 executes the parent-ownership calculation requested by 5199.
It closes the existing bulk 2PI/projective loop rather than opening another
source inventory.

For one finite regulated `(k,-k)` pair cell,

```text
P0=|0,0><0,0|,
P1=I-P0
```

are exact positive orthogonal projectors. For any positive trace-one density
matrix,

```text
W0=Tr(rho P0)>=0,
W1=Tr(rho P1)>=0,
W0+W1=1.
```

A normalized two-mode squeezed pair state gives exactly

```text
Nbar=r/(1-r),
W0=1-r=1/(1+Nbar),
W1=r=Nbar/(1+Nbar).
```

Consequently, if the odds satisfy

```text
Nbar=exp[q(u-u0)],
```

then

```text
n=W1=Nbar/(1+Nbar),
dn/du=q n(1-n).
```

This proves a lawful positive state-space realization of the projective
logistic map. The current parent action does not select that squeezed-state
family or its scale law.

The metric calculation is decisive. The binary orthogonal-block boundary
metric is

```text
g_F=1/[n(1-n)].
```

The full geometric Fock distribution instead has

```text
g_Fock=1/[n(1-n)^2],
```

and the sourced Gaussian bulk 2PI log-determinant gives

```text
g_2PI=1/2[n^-2+(1-n)^-2].
```

The ratio

```text
g_2PI/g_F
 =[n^2+(1-n)^2]/[2n(1-n)]
```

equals one only at `n=1/2`. Therefore the checkpoint-5199 Fisher geometry
requires a binary boundary reduction/coarse-graining in `Gamma_rho0`; it is
not the functional metric of the known bulk Gaussian 2PI Hessian.

The exact kernel decomposition is

```text
x=|k|/mu,
C_q=1/[x(1+x^q)],
K_q=x+x^(1+q),
n=x/K_q=1/(1+x^q).
```

Checkpoint 5181 owns the infrared `x` term through
`B0(k)=1/(8|k|)`. The parent does not own

```text
x^(1+q)=x^1.7698811733853892.
```

The available local analytic and derivative-pair terms imply `q=1` and
`q=2`, respectively.

The source-locked exponent scan records the real near hit

```text
theta_GR,dynamic,N8 =1.8926421323602347,
8/3-theta_GR        =0.7740245343064318,
q_target            =0.7698811733853892,
relative difference =0.005381818732913113.
```

It is not a derivation: the fractional family is nonclosed, the formal
fractional direction is nonregular, it has no same-kernel CTP projection and
it has no positive `P0/P1` overlap.

The structurally admissible same-Gaussian-pair power count gives

```text
D(p)~p^(-2+eta)
  => K_pair(k)~k^(1-2eta)
  => q_pair=-2eta.
```

With the sourced dynamic

```text
eta_psi=-0.06532510306084385,
```

this predicts

```text
q_pair=0.1306502061216877,
```

not the target. The required value in this convention is
`eta_pair=-0.3849405866926946`. No sourced composite/Bethe--Salpeter block
provides that correction.

The ownership decision is:

```text
positive vacuum/nonvacuum projectors:
  derived kinematically;

squeezed-state projective map:
  exact for an allowed state family;

parent state selection:
  not derived;

binary Fisher metric:
  exact after boundary reduction;

bulk Gaussian Fisher match:
  rejected except at n=1/2;

critical infrared |k| carrier:
  parent-owned;

q-dependent |k|^(1+q) term:
  not parent-owned;

q=0.7698811733853892:
  explicit reduced-state closure;

outer s=4 and B=8:
  explicit boundary closure;

local GR/Newton/Maxwell branch:
  unchanged.
```

The next route is not another galaxy exponent scan. Return to the stated
priority local spine and derive in one parent variation:

```text
metric/coframe matter response;
covariant stress conservation;
Newtonian Poisson normalization;
status of G_N as derived ratio or renormalization input;
first PPN residual vector;
local silence of any retained boundary state sector.
```

Executable:

```text
scripts/Y5_R2FR_5200_CTP_projector_metric_exponent_ownership_gate.py
```

Evidence:

```text
source-intake/functional_rg/5200/
```

Validation:

```text
source-intake/mts_residuals/P8_Y5_BRR545_5200_VALIDATION.csv
98/98 PASS.
```

Locks:

```text
checkpoint-5200 output tree:
  acc19e684b35c7aff65923713812b6416e8cb5ea5212ddc5645f3802c37f4075

formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758

checkpoint-5199 output:
  eab39ad4e57a762fef35e264933e962eacc103b8c4f374e3911946cc35b08411

public worktree:
  8913c00b77d98e457ddb0c48e9aeec9cc5f309fd, clean

galaxy repository:
  f850e4997657f457dddc05cbe50f21186588dcc7, unchanged pre-existing dirty state
```

No GitHub action occurred. The protected `formalization-workbench` and galaxy
repository were not modified.

## Previous authoritative handoff - checkpoint 5199

Checkpoint 5199 executes the nonlinear composite calculation demanded by
5198. It does not open another source inventory.

For the exact ultralocal fractional measure

```text
Z(K)=integral dpsi
 exp[-(3/4)|psi|^(4/3)-K psi^2/2],
Y=psi^2,
```

the exact composite Legendre vertices have stable logistic signs but the
canonical-linear invariant is

```text
I=U'''^2/(U'' U'''')
 =0.7794368858172214,
```

not `I_logistic=3`. In addition, `K=0` is the edge of the source domain:
any `K<0` makes the fractional measure divergent.

The actual kinetic zero mode was then solved nonperturbatively:

```text
H(K)
 =-1/2 d^2/dpsi^2
  +(3/4)|psi|^(4/3)
  +K psi^2/2.
```

Fourth-order Rayleigh--Schrodinger response, with grid, box and spectral
convergence, gives

```text
I_quantum,continuum=0.8298513092338069.
```

The rescue tests also fail:

```text
positive mass:
  moves I monotonically toward the harmonic limit 3/4;

first twelve converged eigenstates:
  0.7992200728 <= I <= 0.8298513505;

converged thermal scan:
  beta_peak=5.079502521963518,
  I_peak=0.871915721557117;

quantum Gaussian 2PI:
  3/4 <= I <= 25/31;

classical Gaussian 2PI:
  2/3 <= I <= 49/67.
```

The known checkpoint-5185 parent interactions cannot produce an order-one
repair:

```text
maximum sourced interaction norm =3.492540005516476e-116;
maximum coherent phase            =5.306102337726383e-101;
minimum unknown-O2 enhancement    =4.689488579429405e28.
```

Therefore the sourced minimal **flat-occupation-metric canonical kink**
realization is rejected. This is not a universal no-go for every nonlocal or
nonequilibrium 2PI state.

The important constructive result is that the logistic law itself survives
without those Landau vertices. For two positive scale-covariant weights,

```text
n=W1/(W0+W1),
d ln W_a/du=Delta_a,
q=Delta1-Delta0,
```

one has identically

```text
dn/du=q n(1-n),
n=(R/L)^q/[1+(R/L)^q].
```

This is exactly the checkpoint-5148/5151 projective occupation. Its stable
binary entropy is

```text
F=n ln n+(1-n)ln(1-n)-q(u-u0)n,
```

and its natural metric is

```text
g_nn=1/[n(1-n)].
```

With

```text
theta=2 asin(sqrt(n)),
```

the metric is canonical and the flow/potential are

```text
dtheta/du=(q/2)sin(theta),
V_theta=q^2 sin^2(theta)/8.
```

Thus the checkpoint-5198 quartic `1:-6:12` contract was sufficient for a
flat `n` metric, not necessary for a projective occupation. The current
conditional scale closure remains

```text
q_scale=0.7698811733853892.
```

It is not yet the parent-signed composite eigenvalue. The outer anti-wall
has the same exact projective form, but `s=4`, `B=8` and the exterior weight
remain open.

The next constructive calculation is checkpoint 5200:

```text
1. project the source-locked parent CTP/2PI covariance into actual positive
   occupied and reference sectors;
2. calculate their radial scaling-generator eigenvalues;
3. test Delta1-Delta0=0.7698811733853892;
4. pull back the parent 2PI metric to n=W1/(W0+W1) and test the Fisher form;
5. derive or reject the exterior projector that owns s and B.
```

Do not repeat cubic/quartic vertex scans without a new parent operator. If
the two-sector projection or metric cannot be obtained from the parent, the
logistic profile is explicitly a reduced-state closure.

Checkpoint artifacts:

```text
document sha256:
  57154bb09b8584b7fb360c9e5f94edf9b43aac3e99426e210d6308d81fbe1891

script sha256:
  2cf8aaf3ab801bd7c87334f7c208c24c3a3a49a9a4eb122155f74d9d19575d33

result sha256:
  b582904c80f8e0e25a463bc0a40a3cea69268ab0f9b7e725ddc592bdf092e042

validation sha256:
  135e9be755b089c9bfcbcfaa32278b88f443e091c23e2f4a5f88fe72aa17acf6

output tree sha256:
  eab39ad4e57a762fef35e264933e962eacc103b8c4f374e3911946cc35b08411
```

All `61/61` validations pass. There are `13` generated evidence files with
`204056` bytes. The protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`;
the checkpoint-5198 output digest remains
`bfbb66e0c37e6995ae888ed21d56a41e8245c4c4ebbb731bb5192159c0044510`.
The public worktree is clean, the pre-existing galaxy-repository status is
unchanged, no scripts `__pycache__` exists and no GitHub action occurred.

## Derivation history - checkpoint 5198

Checkpoint 5198 takes the route separation from 5197 forward rather than
opening another inventory. The galaxy scale is tested as an occupied
collective surface-stress scale, not an elementary Compton length.

For a conserved axisymmetric phase surface stress with the selected Plummer
vertical kernel, continuity, radial/azimuthal Euler equations and the metric
constraint give

```text
omega^2=lambda(k)
 =kappa^2+c_R^2 k^2
  -2 pi G Sigma_chi |k| exp(-|k|H_chi).
```

The outer phase is a finite Mestel-like disk:

```text
Sigma_chi=Gamma0/(2 pi G y),
V_chi^2=Gamma0 L_eff,
kappa_chi^2=2 Gamma0/(L_eff y^2).
```

Its marginal outer branch therefore fixes the radial amplitude

```text
c_R^2=Gamma0 L_eff/8.
```

This is the first derived axisymmetric radial stress amplitude for the
current phase route. It is a state law, not a new vacuum coupling.

At `R=L_eff`, using the already selected

```text
q=0.77,
c_q=4.640081689829917,
H_chi/L_eff=0.02,
B=8,
s=4,
```

the Plummer stationary equation gives

```text
k_star L_eff=2.9218908789809075.
```

The checkpoint-5148 spectral/real scale is

```text
mu_spectral L_eff=2.921396974200681,
```

so the fractional internal residual is
`1.6906458950560754e-4`. Equating the two scale constructions as functions
of `q` gives

```text
q_self-consistent=0.7698811733853892.
```

Holding `q=0.77` instead predicts

```text
H_chi/L_eff=0.02003144295023986.
```

This is a conditional internal closure, not independent evidence: both
routes share the phase shape and the 5148 scale optimizer is broad.

The universal selected phase profile has

```text
0.5<=R/L_eff<=2:
  Q_phase min/median/max
   =1.0310543423768779
    /1.035047406061021
    /1.0461419549668172;
  median Plummer response enhancement
   =6.080455978037317.
```

The full stored Plummer profile has positive `lambda_min`. The simple
constant-dispersion rotating background has a central streaming-speed zero
near `R/L_eff=0.03445`, so its core continuation is not claimed.

The read-only clean replay gives

```text
160 galaxies,
11606 active-annulus points,
median collective Q=1.2318967151151314,
median spherical-EOS Q=2.5469398905272422,
median c_EOS^2/(Gamma0 L_eff/8)=4.344143528923965,
median positive enhancement=2.3779259682473963,
phase-fraction/log-enhancement correlation=0.8017090476912597.
```

The spherical reconstructed EOS is therefore rejected as the disk radial
pressure. It was already labelled a spherical-equivalent diagnostic, so
this does not erase it; the marginal-Mestel law fills the anisotropic radial
component it left open.

Four active points in `NGC6015` and `NGC6946` have negative interpolated
`lambda_min`. They remain explicit countercases for a native two-dimensional
stability replay.

The exact inner logistic potential requires

```text
V_n=q^2 n^2(1-n)^2/2,
m2=q^2,
g3=-6q^2,
g4=12q^2.
```

For `q=0.77` this is

```text
m2=0.5929,
g3=-3.5574,
g4=7.1148.
```

The canonical-linear vertex invariant is

```text
I_logistic=g3^2/(m2 g4)=3,
I_parent_fractional=2/5.
```

Thus the bare `|psi|^(4/3)` potential cannot directly be the logistic order
parameter. The surviving nonlinear route is a reflection-even 2PI
occupation/covariance composite. Its cubic and quartic vertices must be
calculated rather than inserted.

Route decision:

```text
elementary pole owns galaxy scale             = rejected by 5197;
occupied phase collective Hessian             = retained;
c_R^2=Gamma0 L_eff/8                          = derived asymptotically;
spectral/collective scale bridge               = conditional internal closure;
spherical EOS as radial disk pressure          = rejected;
bare fractional scalar as logistic field       = rejected;
local GR/Newton/Maxwell vacuum branch           = unchanged;
full MTS or galaxy claim                        = false.
```

Validation:

```text
45/45 PASS;
5198 output tree
 =bfbb66e0c37e6995ae888ed21d56a41e8245c4c4ebbb731bb5192159c0044510;
document
 =e1bd7de17399f54d4069d9577750010d8329a81397a35a8bf0719eda9edec2be;
script
 =ce71c7a1a43a04653d1c60427bf1392f7dbf05b41adab21edba4010e4fff05cc;
result
 =9ed92451c782c760cb6767f0e53217a972711489c3aaf5258a04ae2d441bf469;
validation
 =0386afb97f3ab218cbc4d1794e0dd2f5088c631cfc6bd5645319a410288a06ad;
formalization-workbench
 =b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5197 output
 =6c6f76b0fe366fe5b5435d2d6bcfe4b982212bf1606769928cf1559ccb2692e9.
```

There was no GitHub action, no galaxy-repository edit, no
`formalization-workbench` edit and no scripts `__pycache__`.

The next calculation is not another missing-input sweep. Calculate the
occupied composite 2PI third and fourth vertices and test whether they
produce

```text
m2:g3:g4=q^2:-6q^2:12q^2.
```

If they do not, the exact logistic `n,b` flows must be labelled as a reduced
state closure while the derived collective Hessian and marginal-Mestel
amplitude remain intact.

## Retained handoff - checkpoint 5197

Checkpoint 5197 enforces the checkpoint-5196 invariant pole across all live,
conditional and historical mass uses. Its exact premise is

```text
m_pole^2=V_eff''(0)/Z_psi,
J_gap=G_N m_pole^2.
```

For one elementary field in one fixed local action, `m_pole` is one universal
number. The matched checkpoint-5195 cosmology targets are

```text
Lambda free:
  m_pole=1.773835953883273e-33 eV,
  J_gap=2.110929995508709e-122,
  reduced Compton scale=3605.143 Mpc;

Lambda=0:
  m_pole=1.095668516985692e-33 eV,
  J_gap=8.053882511735061e-123,
  reduced Compton scale=5836.557 Mpc.
```

The reconstructed natural-unit Newton constant is

```text
G_N=6.708832120298927e-57 eV^-2
```

with branch spread `3.375e-16`.

The weakest particle-population floor used by the galaxy calculations is
`8.882479043701029e-23 eV`. The stricter engineering floors are
`2.8166916621557602e-21 eV` and
`4.8323634180988915e-21 eV`; the locked checkpoint-5176 comparator is
`1e-20 eV`.

For that locked comparator:

```text
relative to Lambda-free cosmology:
  mass separation=12.7510865466 decades,
  J_gap separation=25.5021730933 decades;

relative to Lambda=0 cosmology:
  mass separation=12.9603208172 decades,
  J_gap separation=25.9206416344 decades.
```

The identity

```text
J_galaxy/J_cosmology=(m_galaxy/m_cosmology)^2
```

holds below `5e-16` fractional residual, so the mismatch is not a field
normalization or units artefact.

The epoch gate is independently decisive. The source rows give

```text
H_eq=2.3629115213047323e-28 eV.
```

The two cosmology poles have `m/H_eq=7.506993e-6` and `4.636943e-6`, so they
are not rapidly oscillating dust at equality; they instead have present
`m/H0=1.232099124744752` and `0.7638680134687456`, which permits late thawing.
The galaxy particle values have `m/H_eq` of order `10^7` and `m/H0` of order
`10^12--10^13`. One quadratic elementary mode cannot satisfy both roles.

Therefore:

```text
same constant elementary pole for 5195 cosmology and 5152-5176 massive dust
  = rejected;

old occupied-particle calculations
  = retained as a conditional separate-component comparator;

10^-20 eV as the mass of the 5195 scalar
  = rejected.
```

This does not reject the current galaxy route. The read-only current v19 phase
scripts contain zero `m_gap`, `J_gap`, Compton, pole-mass or particle-mass
tokens. They define

```text
u=ln(R/L_eff),
dn/du=q n(1-n),
db/du=-s b(1-b),
Sigma_chi=(Gamma0/G) n b/(2 pi R/L_eff).
```

They explicitly describe a collective environmental phase, not a particle
dark disk, and retain:

```text
covariantFourDimensionalActionDerived=false,
environmentalBoundaryDerived=false,
stressTensorDerived=false,
phaseActivationDerived=false,
phaseBoundaryDerived=false,
phaseStressTensorDerivedFromAction=false.
```

`L_eff` is therefore not translated into `J_gap`. Setting
`m_pole=hbar/(c L_eff)` without a parent dispersion relation would be hidden
arena-dependent mass retuning.

The selected route is:

```text
one universal elementary cosmological pole
plus
a parent-derived composite/environmental Hessian eigenvalue.
```

This route adds no second elementary pole at this stage. It must derive the
collective state rather than insert it.

Next target:

```text
checkpoint 5198 must construct or reject the parent-owned composite
environmental Hessian and scale map.
```

It should:

```text
define a reflection-even composite chi;
derive Gamma_chi_chi^(2) from the parent 2PI/CTP action;
prove chi=0 with a positive gap on the local invariant vacuum;
test environmental softening without changing m_pole or G_N;
derive or reject n, b, L_eff, the finite wall and the Hilbert stress;
enforce positivity, Ward conservation and local silence.
```

Do not run another elementary-mass scan and do not revive the `10^-20 eV`
particle route as the one-pole unification owner.

Artifacts:

```text
document:
  5197-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-separation-theorem.md
script:
  scripts/Y5_R2FR_5197_universal_gap_cross_arena_compatibility.py
outputs:
  source-intake/functional_rg/5197/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5197_VALIDATION.csv
```

Validation is `28/28 PASS`. The output directory contains 9 files and
`107241` bytes.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5195 output tree:
  7aa855d3f75b9d2eb52fdc73f903c77a2e8e8b9e3be0f9496c4f9e15c5d6a810
checkpoint 5196 output tree:
  fc16f376470ac834daa8c89abe930254a456d67bd677d4c0290ebe8719b62c28
checkpoint 5197 output tree:
  6c6f76b0fe366fe5b5435d2d6bcfe4b982212bf1606769928cf1559ccb2692e9
document:
  f01f94465168758886800556f345e370910f6913e80f1a4a0c646bbe7abe0c0a
script:
  fe4e7c92cb929ac0226dae239e50bd637ecf29be388cb57a14f01abf91e74694
result:
  e42f0be823acd57eed630cca62b1e84a66e85cc81ba4354a24a0dcb93d1d0c0e
validation:
  73b169e5309cc06bd3096f931fb8190e0c8ae5dbb7fba5d988ebf75a5de2b9f7
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`. The galaxy repository remained
read-only at `f850e4997657f457dddc05cbe50f21186588dcc7` with its pre-existing
uncommitted phase scripts unchanged. The protected `formalization-workbench`
was not modified.

## Historical handoff - checkpoint 5196

Checkpoint 5196 attacks the finite mass-gap and homogeneous-state derivation
left by 5195. Its first exact correction is:

```text
J_gap=m_gap^2 G_N
```

is the dimensionless invariant pole-mass coordinate, not an additive scalar
source. In a noncanonical field coordinate the exact relation is

```text
m_pole^2=V_eff''(0)/Z_psi,
J_gap=G_N V_eff''(0)/Z_psi.
```

The symbolic field-rescaling residual is exactly zero. In four dimensions
`J_gap` is dimensionless while an additive scalar source has mass dimension
three, and no dimension-three source operator is present in the current
reflection-even action.

The parent fixed-functional spectrum retains the regular mass eigenoperator

```text
delta u=C_2 varphi^2,
theta_mass=1.84666104495 to 1.85881728347 >0.
```

Its scaling exponent is derived, but its trajectory amplitude is not. The
already-derived GR transfer

```text
J_gap,IR=K R_UV+O(R_UV^2),
K=0.262094420818 or 0.261707706805
```

therefore transports a continuum of values rather than selecting one.

The existing source routes were rechecked term by term:

```text
P(X)                  = derivative-only;
ordinary matter       = delta S_matter/delta psi=0;
quadratic potential   = restoring term proportional to psi;
O4=C^2 X on flat FLRW = zero because C=0;
C3/CFF                = no scalar variation;
X^2                   = zero quadratic Hessian at psi=0;
direct T psi^2        = excluded as independent parent operator;
R psi^2               = current operational xi=0 and multiplicative if added;
Gaussian/alpha4 CTP   = state functional, not action-selected amplitude;
free Bogoliubov route = zero mean and not an abundance owner.
```

The exact homogeneous equation is

```text
chi''+(3+h)chi'+(m_gap^2/H^2)chi=S_psi/H^2,
S_psi=0.
```

During radiation domination the regular series is

```text
chi=A[1-mu^2 e^(4N)/(20 Omega_r)+O(e^(8N))],
chi'=-A mu^2 e^(4N)/(5 Omega_r)+O(e^(8N)).
```

The second solution is `B e^(-N)`. Regularity removes `B` but leaves `A`.
Matter domination gives the same parameter count,
`chi=A+B e^(-3N/2)`. A retarded/no-incoming rule removes the remaining
homogeneous amplitude only by selecting `chi=0`, because the current additive
source is zero.

Thus:

```text
regular phase/velocity relation = derived;
nonzero homogeneous amplitude   = one state datum;
numerical J_gap                  = one universal action calibration.
```

The exact 5195 primary branches were rebuilt from `N=-12`:

```text
free Lambda:
  mu=1.23209912474,
  m_gap=1.77383595388e-33 eV,
  J_gap=2.11092999551e-122,
  chi(-12)=0.426739564394,
  chi(0)=0.343494364916,
  amplitude retained=0.804927393;

Lambda=0:
  mu=0.763868013469,
  m_gap=1.09566851699e-33 eV,
  J_gap=8.05388251174e-123,
  chi(-12)=1.15248908803,
  chi(0)=1.06309822948,
  amplitude retained=0.922436699.
```

Both mass reconstructions match 5195 to machine precision. The corresponding
4938 UV coordinates are finite:

```text
free Lambda R_UV=8.05408e-122 to 8.06598e-122;
Lambda=0 R_UV=3.07289e-122 to 3.07743e-122.
```

The field retains 80--92 percent of its early regular amplitude, so Hubble
friction has not erased the state datum. An explicit four-amplitude regular
counterfamily confirms that early regularity alone cannot choose it.

The minimum honest contract is now:

```text
G_N                         = one gravitational scale calibration;
J_gap                       = one universal motion-gap action calibration;
Lambda_cal                  = one background calibration unless set to zero;
A_reg or Omega_scalar       = one global state datum;
theta_regular               = derived, not fitted;
primordial covariance       = separate state data if predicted.
```

For the `Lambda=0` branch, flatness fixes the scalar amplitude after
`Omega_m`, `H0`, and `m_gap` are given. This removes an independent fit
coordinate and leaves one extra shape coordinate versus flat LCDM. It does
not make the amplitude action-derived.

Next target:

```text
checkpoint 5197 must enforce the same universal J_gap across every still-live
cosmology, galaxy, formation, local, and occupied-state use of m_gap.
```

Historical or rejected mass rows must be separated from live requirements.
If the cosmological `~10^-33 eV` target and a live galactic
`~10^-21--10^-20 eV` requirement refer to the same canonical pole, the
unification route has a decisive conflict. If the galaxy scale is instead a
collective Hessian eigenvalue, its map to `J_gap` must be derived. No
arena-specific mass retuning is allowed.

Artifacts:

```text
document:
  5196-Y5-R2FR-invariant-mass-gap-Hessian-and-homogeneous-state-selection-theorem.md
script:
  scripts/Y5_R2FR_5196_invariant_mass_gap_and_homogeneous_state_selection_theorem.py
outputs:
  source-intake/functional_rg/5196/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5196_VALIDATION.csv
```

Validation is `42/42 PASS`. The output directory contains 10 files and
`72186` bytes. Symbolic identities, locked source hashes, branch
reconstruction, regular counterfamilies, source exhaustion, nonclaim guards,
protected-tree locks, and public-worktree locks all pass.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5195 output tree:
  7aa855d3f75b9d2eb52fdc73f903c77a2e8e8b9e3be0f9496c4f9e15c5d6a810
checkpoint 5196 output tree:
  fc16f376470ac834daa8c89abe930254a456d67bd677d4c0290ebe8719b62c28
document:
  a3495f713d22fea38ebd010a1d0f14d2ff266180fa358ee8a89492a55ea57974
script:
  1739be7cef6d30a7dc103d9ac4f75b57c76a0e360c4ea501188857d059c59234
result:
  aecba0a57eaf557b6fddd18948c0d74e00a2e68e1d892516e10d2d0763fe0f04
validation:
  f937a1491dab2926521a8c28c8fd2ada9cf2f1868d7b24dd143e90c6141af533
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`; the protected
`formalization-workbench` was not modified.

## Historical handoff - checkpoint 5195

Checkpoint 5195 executes the matched refit demanded by 5194. It removes the
independently profiled BAO scale and computes one physical distance
calibration from the fitted `H0` and CAMB sound horizon:

```text
alpha_phys=c/(H0 r_drag).
```

Every baseline and parent branch is refitted under the same Pantheon+, DESI,
growth, and compressed-CMB information. This is an actual calculation, not a
new target ledger.

The primary matched likelihood uses

```text
Pantheon+ noncalibrator rows    = 1624, full STAT+SYS covariance;
DESI DR2 BAO rows               = 13, full covariance;
SDSS/eBOSS f sigma8 rows        = 5, marginal covariance;
compressed CMB rows             = 4, full covariance;
total rows                      = 1646;
local-H0/SH0ES calibration      = absent;
independent BAO alpha           = absent.
```

Only three nuisance coordinates are profiled: one Pantheon+ additive offset,
`sigma8_0`, and `n_s` inside the full compressed-CMB covariance. `H0`,
`Omega_b h^2`, and the model shape are fitted directly.

The primary scores are

```text
model                         chi2          k   AIC           BIC
LCDM                          1477.215242   6   1489.215242   1521.651862
wCDM                          1475.955647   7   1489.955647   1527.798371
CPL                           1470.710226   8   1486.710226   1529.959054
parent scalar, Lambda free    1473.978274   8   1489.978274   1533.227101
parent scalar, Lambda=0       1474.069081   7   1488.069081   1525.911804
```

The exact primary comparisons are

```text
free parent minus CPL, equal k:
  Delta chi2=Delta AIC=Delta BIC=+3.268047;

Lambda=0 parent minus wCDM, equal k:
  Delta chi2=Delta AIC=Delta BIC=-1.886566;

Lambda=0 parent minus CPL:
  Delta chi2=+3.358854,
  Delta AIC=+1.358854,
  Delta BIC=-4.047249;

Lambda=0 parent minus LCDM:
  Delta chi2=-3.146161,
  Delta AIC=-1.146161,
  Delta BIC=+4.259942.
```

CPL has the lowest AIC and LCDM has the lowest BIC. The zero-Lambda parent is
within `1.359` AIC units of CPL and has a `4.260` BIC penalty relative to
LCDM. At the same parameter count it improves on wCDM by `1.887`. The honest
interpretation is competitive/draw-scale under AIC and moderate LCDM
preference under BIC, not a universal model-selection victory.

The frozen-parameter compressed-CMB pressure from 5194 is substantially
reduced:

```text
free parent CMB chi2:
  5194 frozen late fit = 42.5497,
  5195 joint refit     = 3.70371;

Lambda=0 parent CMB chi2:
  5194 frozen late fit = 37.2861,
  5195 joint refit     = 3.68458.
```

This does not rely on a prior edge. The primary parent coordinates are

```text
free Lambda:
  Omega_m=0.309366560,
  H0=67.4920442 km/s/Mpc,
  Omega_b h^2=0.0225732374,
  mu=m_gap/H0=1.23209912,
  f_scalar=0.292205966,
  Omega_scalar,0=0.201780913,
  Omega_Lambda,0=0.488762527,
  theta_0=0.341775064,
  w_dark,0=-0.934351701,
  fitted m_gap=1.77384e-33 eV;

Lambda=0:
  Omega_m=0.311635407,
  H0=67.2427763 km/s/Mpc,
  Omega_b h^2=0.0225638256,
  mu=m_gap/H0=0.763868013,
  Omega_scalar,0=0.688274593,
  Omega_Lambda,0=0,
  theta_0=0.206092191,
  w_dark,0=-0.916247920,
  fitted m_gap=1.09567e-33 eV.
```

These mass and state values are empirically fitted coordinates. They are not
yet derived constants of the MTS parent action.

The prior-edge audit passes for all five primary fits. Extending the parent
mass prior from `log10(mu)=-2` to `-4` reproduces both finite optima:

```text
free parent:
  primary log10(mu)=+0.0906456491,
  wide    log10(mu)=+0.0906456491;

Lambda=0 parent:
  primary log10(mu)=-0.116981675,
  wide    log10(mu)=-0.116953438.
```

The solution is therefore not a disguised `mu -> 0` LambdaCDM boundary.

The local Hessian in prior-normalized coordinates is positive for both
parents:

```text
free parent:
  minimum eigenvalue=29.9254,
  condition number=1.02590e5,
  sigma_local(log10 mu)=0.207972,
  sigma_local(f_scalar)=0.249593,
  corr(log10 mu,f_scalar)=-0.862012,
  status=positive but weak;

Lambda=0 parent:
  minimum eigenvalue=925.351,
  condition number=3333.23,
  sigma_local(log10 mu)=0.109530,
  status=positive local curvature.
```

These are finite-difference local Gaussian diagnostics, not posterior
intervals. They show that the zero-Lambda branch is the cleaner predictive
parent and that the free-Lambda mass/state split remains weak.

The robustness matrix includes

```text
full 14-row SDSS BAO-plus refit with physical alpha;
alternative LCDM compressed-prior table;
no-growth refit;
parent mass prior extended to log10(mu)=-4.
```

Both parent branches remain interior in every branch. The full-SDSS result is
kept nonclaim because no DESI/SDSS cross-survey covariance is available; the
primary fit uses only marginal `f sigma8` rows rather than fabricating
independence for overlapping BAO distance information.

The optimizer uses the fast regular phase shoot at `N=-7`. Rebuilding each
parent optimum from the `N=-12` radiation-era regular series changes

```text
max relative E(z), 0<=z<=2.5       < 6.95e-6;
total chi2                          < 1.32e-3;
compressed-CMB chi2                < 2.0e-7;
maximum Friedmann residual         < 2.3e-15.
```

The fixed-grid RK4 growth evaluator is compared directly with the
checkpoint-5194 DOP853 solution at every observed growth redshift. Its
largest fractional difference is `3.14e-6`.

The route decision is

```text
5194 CMB discrepancy survives matched refit       = no;
parent branch collapses to LambdaCDM prior edge    = no;
zero-Lambda parent remains competitive             = yes;
free-Lambda mass/state split fully identified      = no;
official Planck/ACT/SPT likelihood run             = no;
cosmology-support claim                            = false;
full MTS unification claim                         = false.
```

The next cosmology gate is an official-likelihood-ready implementation. The
higher-priority field-theory target is checkpoint 5196:

```text
derive m_gap^2=V_eff''/Z_psi and the homogeneous-state selection from the
parent J_gap/source-coupling structure, or prove that a local covariant action
leaves the state as explicit initial data.
```

This is the correct next derivation because 5195 now supplies a finite,
interior empirical target rather than an unconstrained placeholder.

Checkpoint artifacts:

```text
document:
  5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md
script:
  scripts/Y5_R2FR_5195_joint_CMB_informed_parent_refit.py
outputs:
  source-intake/functional_rg/5195/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5195_VALIDATION.csv
```

Validation is `32/32 PASS`. The output directory contains 14 files and
`305085` bytes. Predecessor locks, source files, covariance shapes, physical
sound-horizon reconstruction, all primary fits, robustness rows,
forward-parent agreement, growth-integrator agreement, positive local
Hessians, nonclaim guards, protected-tree lock, and public-worktree lock all
pass.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5195 output tree:
  7aa855d3f75b9d2eb52fdc73f903c77a2e8e8b9e3be0f9496c4f9e15c5d6a810
document:
  217fdc07f94e18a21fe996f7592930f69c21ba16b3fe44b1fd1a2518d9d54737
script:
  c379ecbc04bd94fc469281ab3a3a99f103c304a209bd8ea33db4a10785129cb8
result:
  538078e466c2ee9f02e5204090b9e1c87c8c56b5680c366289336dda4abdf3ad
validation:
  9bd11c9d45a76ae25999c155c5f77949221c53421fe80dc466c98416554481c5
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`; the protected
`formalization-workbench` was not modified.

## Historical handoff - checkpoint 5194

Checkpoint 5194 closes the perturbation-owner gap for the surviving
low-energy parent scalar and subjects it to matched growth and first CMB
pressure tests. It does not use the rejected M6 memory closure.

The short result is:

```text
canonical scalar perturbation equations         = derived from parent O2 action;
no-ghost principal sign                         = passed;
rest-frame scalar sound speed                    = c_s^2=1 exactly;
intrinsic scalar anisotropic stress              = zero exactly;
direct fifth force on minimally coupled matter   = absent;
forward regular CMB-time background              = constructed;
SDSS/eBOSS full-covariance growth score           = competitive/draw-scale;
matched baseline jackknifes                       = passed without nuisance edges;
CAMB fluid-versus-PPF convergence                 = passed;
compressed Planck distance diagnostic             = adverse to frozen late fits;
official CMB likelihood                           = not run;
cosmology-support claim                           = false;
full MTS unification claim                        = false.
```

The retained O2 action is

```text
S_O2 = integral sqrt(-g) [
  Mpl^2 (R - 2 Lambda)/2
  - (partial psi)^2/2
  - m_gap^2 psi^2/2
] + S_m[g,Psi].
```

In conformal Newtonian gauge its scalar perturbation equation is

```text
delta_psi'' + 2 Hc delta_psi'
+ (k^2+a^2 m_gap^2) delta_psi
- psi_bar'(Psi'+3 Phi')
+ 2 a^2 m_gap^2 psi_bar Psi = 0.
```

Direct variation also gives

```text
delta rho_psi =
  (psi_bar' delta_psi' - psi_bar'^2 Psi)/a^2
  + m_gap^2 psi_bar delta_psi,

delta p_psi =
  (psi_bar' delta_psi' - psi_bar'^2 Psi)/a^2
  - m_gap^2 psi_bar delta_psi,

delta q_psi = -psi_bar' delta_psi/a^2,
Pi_psi = 0.
```

This fixes the principal propagation rather than fitting it:

```text
c_s,rf^2=1;
Pi_psi=0;
nabla_mu T_m^{mu nu}=0.
```

Matter remains metric-geodesic, and the parent scalar creates neither an
intrinsic linear slip nor a direct fifth force at O2. Standard radiation and
neutrino anisotropic stress is retained rather than relabelled as MTS.

The stable early-time background starts at `N=-12` on the regular
radiation-era series

```text
x_i=-(mu/E_i)^2 chi_i/5
```

and is integrated forward while solving `E(0)=1`. It reproduces the 5193
present branch:

```text
free-Lambda:
  mu=1.79759020906334,
  chi(-12)=0.293207517124,
  theta(0)=0.523064034594,
  max Friedmann residual=2.220e-15;

Lambda=0:
  mu=0.880675983364213,
  chi(-12)=1.02643171042,
  theta(0)=0.238814110897,
  max Friedmann residual=2.109e-15.
```

The growth gate uses 14 source-locked SDSS/eBOSS DR16 BAO-plus rows with full
per-sample covariance. The same generalized least-squares nuisance pair,
`alpha_RSD` and `sigma8_0`, is profiled for every model. The derived smooth
subhorizon limit is

```text
D_NN+[2+dlnH/dN]D_N-3 Omega_m D/2=O[(aH/k)^2].
```

Adding the primary growth score to the checkpoint-5193 Pantheon+ and DESI DR2
score gives

```text
model                        chi2 growth   AIC combined   BIC combined
LCDM                         14.2525133    1494.81527     1521.86095
wCDM                         11.6284895    1489.05191     1521.50672
CPL                          12.3051954    1491.39790     1529.26186
parent, Lambda free          11.8910230    1490.99352     1528.85747
parent, Lambda=0             12.0904028    1489.22111     1521.67593
```

At equal parameter count, the free parent versus CPL differs by
`Delta AIC=Delta BIC=-0.404383`; the zero-Lambda parent versus wCDM differs by
`+0.169208`. Both are draw-scale. The zero-Lambda parent versus LCDM gives
`Delta AIC=-5.59416` and `Delta BIC=-0.185021`.

All models receive the same leave-one-sample-out stress test. The free parent
minus wCDM stays in `[+0.126907,+0.250053]` chi-squared, while the free parent
minus LCDM stays in `[-2.02189,-0.603925]`. All four exclusions leave both
nuisances interior. No jackknife rule is applied only to MTS.

CAMB `1.6.6` evolves the parent table with `c_s^2=1`. The largest normalized
fluid-versus-PPF `f sigma8` difference is `3.285962e-7`; the largest
CAMB-versus-derived-smooth parent response mismatch is `5.436604e-5`; and the
largest dark-energy clustering contribution on `k>=0.01 h/Mpc` is
`3.094851e-4`. Transfer functions and lensed spectra are finite through
`ell=800`.

The source-locked compressed Planck-2018 distance diagnostic is adverse:

```text
model                        profiled H0   compressed chi2
LCDM                         68.226921     3.8895001
wCDM                         67.532519     86.502287
CPL                          67.513722     20.636317
parent, Lambda free          67.518538     42.549720
parent, Lambda=0             67.505584     37.286130
```

This is not an official rejection: all 5193 late parameters are frozen,
`Omega_b h^2` and `n_s` are fixed, and only `H0` is profiled. It is nonetheless
real pressure and must not be explained away. The next calculation must refit
every baseline and parent model under the same CMB information.

The conservative O4 envelope remains negligible on the tested low-energy
branch:

```text
max|delta_F|[(k c)/H0]^4 at k=0.3 Mpc^-1 = 2.667100e-230.
```

The route decision is:

```text
return to phenomenological memory closure             = no;
promote growth result as decisive support              = no;
declare CMB failure from frozen-parameter diagnostic   = no;
ignore compressed-CMB pressure                         = no;
next decisive calculation                              = matched CMB-informed refit.
```

Checkpoint 5195 should jointly refit `LCDM`, `wCDM`, `CPL`, and both parent
branches to Pantheon+, DESI DR2, SDSS/eBOSS growth, and the compressed CMB
vector. It must replace independently profiled BAO scales with one physical
`H0-r_d` calibration, vary the CMB-owned coordinates consistently, and retain
the same priors and convergence rules for every model. If the parent remains
under severe CMB pressure after that refit, the cosmological branch must be
revised or demoted before any official-likelihood expense. If it survives,
the following gate is an official Planck/ACT/SPT likelihood-ready module.

Checkpoint artifacts:

```text
document:
  5194-Y5-R2FR-parent-canonical-scalar-perturbation-growth-and-compressed-CMB-gate.md
script:
  scripts/Y5_R2FR_5194_parent_scalar_perturbation_growth_CMB_gate.py
outputs:
  source-intake/functional_rg/5194/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5194_VALIDATION.csv
```

Validation is `34/34 PASS`. The output directory contains 18 files and
`308199` bytes. The final script compiles and reruns without integration
warnings. All source/provenance, finite-value, nuisance-edge, background,
growth, CAMB convergence, no-claim, protected-tree, and public-worktree gates
pass.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5194 output tree:
  42a8b36602d2666b5be7b0c91c24cc14c12d1ff328aa628408743e872b571ab3
document:
  1478db5333863753c00371b2e8c5ad8d7dc5250a40dd3a1f870de4e8ad25eb5d
script:
  f696e14285549efa7435a3e02b01becb73833998adbd37a60ad49fa779db6bb8
result:
  c77810bd81115c174514b21df7f08ba4e947ba2d56fcbed4602c805536df71f9
validation:
  675e753e270bc85cf1eb032d71c1924969f39b75696fd07617e7199ec95ff5c0
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`; the protected
`formalization-workbench` was not modified.

## Historical handoff - checkpoint 5193

Checkpoint 5193 performs the empirical calculation required by 5192. The
actual parent mass-gap scalar is integrated on its regular homogeneous FLRW
mode inside the likelihood. It is not replaced by, fitted through, or renamed
as the rejected `p=3,u=1/4` memory closure.

The short result is:

```text
direct parent scalar reaches the CPL likelihood basin = yes;
free-Lambda parent versus CPL at equal k               = statistical tie;
Lambda=0 parent versus wCDM at equal k                 = parent lower chi2;
prior-edge dependence                                  = no;
N=-5 versus N=-7 regular-surface dependence            = negligible;
separate mass/state identification from background     = weak;
background cosmology support claim                     = not yet promoted.
```

The matched likelihood uses

```text
Pantheon+ rows                 = 1624 non-calibrators;
Pantheon+ covariance           = full STAT+SYS;
SN nuisance                    = one analytic additive offset;
DESI DR2 BAO rows              = 13;
DESI DR2 covariance            = full Gaussian covariance;
BAO nuisance                   = one analytic common scale alpha;
local-H0/SH0ES calibration     = absent;
fixed radiation density        = Omega_r=9e-5;
total scored points            = 1637.
```

The four data hashes match the previous full-covariance no-SH0ES run. Every
model uses the same rows, covariance matrices, integration grid, fixed
radiation density, and two profiled nuisance coordinates.

The parent model is parameterized without hiding its state freedom. Define

```text
x=dot(psi_c)/(sqrt(6)M_R H),
y=m_gap psi_c/(sqrt(6)M_R H),
mu=m_gap/H0.
```

At the present surface,

```text
Omega_psi,0=f_scalar(1-Omega_m-Omega_r),
Omega_Lambda=(1-f_scalar)(1-Omega_m-Omega_r),
x_0=-sqrt(Omega_psi,0)sin(theta),
y_0= sqrt(Omega_psi,0)cos(theta).
```

Flatness is therefore exact. The backward autonomous system is

```text
x'=-(3+h)x-(mu/E)y,
y'=(mu/E)x-hy,
(ln E)'=h,
h=-3Omega_m(N)/2-2Omega_r(N)-3x^2.
```

`theta` is not fitted. At every likelihood evaluation it is shot onto the
regular frozen mode

```text
x(N_regular)=0.
```

The free-`Lambda` parent model consequently has three shape coordinates:

```text
Omega_m,
log10(mu),
f_scalar.
```

The `Lambda=0` ablation fixes `f_scalar=1` and has two. The SN offset and BAO
scale are counted in every information criterion, giving `k=5` and `k=4`
respectively.

The matched scores are

```text
model                           chi2             k   AIC               BIC
LCDM                            1470.562757549   3   1476.562757549   1492.764619281
wCDM                            1465.423415643   4   1473.423415643   1495.025897952
CPL                             1465.092704776   5   1475.092704776   1502.095807663
M6 fixed 2/27                   1465.259900462   3   1471.259900462   1487.461762194
M6 fitted amplitude             1465.259376497   4   1473.259376497   1494.861858807
parent scalar, Lambda free      1465.102494153   5   1475.102494153   1502.105597040
parent scalar, Lambda=0         1465.130710710   4   1473.130710710   1494.733193019
```

The exact direct comparisons are

```text
free parent minus LCDM:
  Delta chi2=-5.460263395,
  Delta AIC=-1.460263395,
  Delta BIC=+9.340977759;

free parent minus wCDM:
  Delta chi2=-0.320921490,
  Delta AIC=+1.679078510,
  Delta BIC=+7.079699088;

free parent minus CPL:
  Delta chi2=+0.009789377,
  Delta AIC=+0.009789377,
  Delta BIC=+0.009789377;

Lambda=0 parent minus LCDM:
  Delta chi2=-5.432046839,
  Delta AIC=-3.432046839,
  Delta BIC=+1.968573738;

Lambda=0 parent minus wCDM:
  Delta chi2=-0.292704933,
  Delta AIC=-0.292704933,
  Delta BIC=-0.292704933;

Lambda=0 parent minus CPL:
  Delta chi2=+0.038005933,
  Delta AIC=-1.961994067,
  Delta BIC=-7.362614644.
```

The free parent and CPL are indistinguishable in this background likelihood
at the same parameter count. The `Lambda=0` parent has a slightly lower
chi-squared than wCDM at the same count, and trades only `0.038` chi-squared
against CPL while using one fewer parameter.

`M6_fixed` has the lowest raw AIC and BIC because its closure amplitude and
shape were fixed while only `Omega_m` was fitted. It remains a historical
empirical comparator: 5192 proves it is not the source-free analytic parent
scalar. It cannot be promoted as the field-theory result. Restricting the
table to standard baselines and direct parent-owned models,

```text
lowest AIC = parent scalar, Lambda=0;
lowest BIC = LCDM.
```

That disagreement is the honest model-selection result. It is not averaged
into a fabricated winner.

The broad free-`Lambda` best fit is

```text
Omega_m       = 0.302295098208018,
mu=m_gap/H0   = 1.79759020906334,
f_scalar      = 0.200600672417876,
Omega_Lambda  = 0.557672883403780,
Omega_psi,0   = 0.139942018388202,
theta         = 0.523064034367258,
chi_initial   = 0.293207312395323,
early x       = 3.4558607588095e-9,
max Friedmann-constraint residual
              = 1.11022302462516e-15.
```

The `Lambda=0` best fit is

```text
Omega_m       = 0.303173108591393,
mu=m_gap/H0   = 0.880675983364213,
f_scalar      = 1,
Omega_Lambda  = 0,
Omega_psi,0   = 0.696736891408607,
theta         = 0.238814110831892,
chi_initial   = 1.02643154086158.
```

These are fitted coordinates inside a parent-owned model family. They are
not a derivation of `J_gap`, `m_gap`, or the cosmological state.

The robustness matrix gives

```text
broad parent prior:
  chi2=1465.102494153,
  edge=false;

narrow parent prior:
  chi2=1465.102490821,
  Delta chi2=-3.33e-6,
  edge=false;

regular surface N=-7:
  chi2=1465.102490735,
  Delta chi2=-3.42e-6,
  edge=false;

Lambda=0:
  chi2=1465.130710710,
  Delta chi2=+0.028216556,
  edge=false.
```

All branches are nodeless, solve the frozen-mode condition, and preserve the
Friedmann constraint below `1.6e-15`.

An interior best fit does not by itself prove identifiability. The local
finite-difference Hessian of the free parent branch has

```text
minimum eigenvalue              = 0.571453041489006,
maximum eigenvalue              = 31463.2644234443,
condition number                = 55058.3549987975,
corr(log10(mu),f_scalar)        = -0.997948547124753,
status                          = WEAK_MASS_STATE_SPLIT.
```

Local Gaussian curvature diagnostics are

```text
sigma(Omega_m)  = 0.0107691115267379,
sigma(log10_mu) = 1.22188187627554,
sigma(f_scalar) = 1.41785672463727.
```

They are not posterior intervals. They prove that this background constrains
a combined thaw history much more strongly than it separately determines the
universal mass and state share. This is why the `Lambda=0` branch is the
cleaner predictive result.

At the free-`Lambda` optimum,

```text
Omega_scalar,kinetic,0   = 0.0349207175400662,
Omega_scalar,potential,0 = 0.105021300848136,
w_dark,effective,0       = -0.899885402532645.
```

The parent scalar is therefore reproducing a wCDM-like late expansion through
derived Klein-Gordon dynamics, not through the discarded memory activation
function.

The branch-specific O4 prediction remains negligible:

```text
max|delta_F| at H0=70
  =9.787317791686963e-243.
```

The 5191 tensor-safety conclusion survives on the data-fitted branch.

The route decision is

```text
old M6 equals direct parent scalar             = false;
parent scalar background in scorer             = direct ODE;
regular homogeneous mode                       = solved, not fitted;
flatness                                       = exact;
SN/BAO nuisance freedom                        = matched;
historical baselines                           = reproduced;
free parent versus CPL                         = tied at equal k;
Lambda=0 parent versus wCDM                    = competitive at equal k;
separate free mass/state split                  = weakly identified;
background viability                           = survived this gate;
cosmology-support claim                         = false;
full MTS unification claim                      = false.
```

The next target is checkpoint 5194. The background has survived strongly
enough that the work should not return to another closure search. Derive and
execute the perturbation equations of this exact parent branch:

```text
scalar sound speed and no-ghost conditions;
metric-scalar constraint system;
effective Newton coupling and slip;
growth f sigma_8;
CMB background and perturbation handoff;
O4 order-reduced tensor correction.
```

Only after that independent growth/CMB gate can the background result be
considered for promotion.

Checkpoint artifacts:

```text
document:
  5193-Y5-R2FR-direct-parent-scalar-Pantheon-DESI-likelihood-and-model-selection-gate.md
script:
  scripts/Y5_R2FR_5193_direct_parent_scalar_SN_BAO_likelihood.py
outputs:
  source-intake/functional_rg/5193/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5193_VALIDATION.csv
```

Validation is `26/26 PASS`. Nine CSVs parse without malformed or non-finite
cells. All 11 provenance sources exist and match their hashes. The 5193
output tree contains ten files and `120464` bytes.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5193 output tree:
  e9a2d3c5f9e283e68acd326745ac4b6665157817cdcfa93cf644e0b0b6713505
document:
  277a74bf5d75238831d87a5c778a7ac8da2c226d2eafb5ec30203b6fda067dd9
script:
  8ae6018f911667c04b2780ff5247786e3c192f58397148b6ba07cebccc0ddb21
result:
  3fc4dbf416cd1b4ce5b5a921d4dd792abb98bd9d3897ba18d570688e7c4e1a6d
validation:
  26de30e6eca3123fe45731622e50ee7cfc8e20b3ef4a3c60cf6783f1975d8f87
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`; the protected
`formalization-workbench` was not modified.

## Historical handoff - checkpoint 5192

Checkpoint 5192 executes the actual homogeneous motion-sector calculation
requested by 5191. It replaces an ambiguous identification with a sharp
three-way result:

```text
infrared functional P(X) germ             = locally canonical and healthy;
old M6 closure as source-free massless P(X)= rejected exactly;
parent-owned massive scalar FLRW route     = constructed and retained.
```

This is a real change in the cosmology spine. The old fitted memory closure
may remain an empirical comparator, but it is no longer permitted to stand in
for a derived parent solution. The next likelihood must integrate the parent
scalar equation directly.

The 4957 convention is

```text
P_k(X_c)=k^4 p_k(x),
x=X_c/k^4,
p_k(x)=x/2+sum_(n>=2) a_n(k)x^n.
```

With the physical Lorentzian convention `L=-P(X)-V(psi)`,

```text
rho_psi=P+V-2XP_X,
p_psi=-(P+V),
rho_psi+p_psi=-2XP_X,

(P_X+2XP_XX)ddot(psi)
 +3HP_Xdot(psi)+V_psi/2=0.
```

For the shift-symmetric subbranch,

```text
a^3 P_X dot(psi)=Q,
c_s^2=P_X/(P_X+2XP_XX),
dln|X|/dlna=-6c_s^2.
```

The symbolic continuity residual vanishes exactly. The order-eight
`g=1e-10` endpoints were evaluated with 80-digit arithmetic on the local
timelike chart `-0.1<=x<=0`. Both dynamic and reference flows obey

```text
min P_X > 0.5,
min(P_X+2xP_XX) > 0.5,
max|w-1| < 8.1e-19,
max|c_s^2-1| < 1.7e-18.
```

Thus the sourced infrared germ is effectively canonical there. A populated
nonzero massless state is stiff and contains one conserved state constant;
it does not generate a late vacuum-like plateau.

The tested old closure is

```text
F(n)=1-exp[-(n/u)^3],
rho_mem=B_mem F(n),
n=ln(1+z).
```

It satisfies

```text
F(0)=0,
F'(0)=0,
F(infinity)=1.
```

Conservation requires

```text
rho+p=(1/3)d rho/dn.
```

At `n=0`, the enthalpy therefore vanishes. On the connected healthy analytic
branch with `P_X>0`,

```text
rho+p=-2XP_X=0  =>  X=0,
Q=a^3P_Xsqrt(-X)=0.
```

Since `Q` is conserved, `X=0` throughout that source-free branch and a
nonzero varying `B_mem F(n)` is impossible. The independent parametric
reconstruction gives, for finite nonzero `Q`,

```text
X Q^2=-a^6(rho+p)^2/4,
P=-p=rho-(1/3)d rho/dn.
```

The closure returns to `X=0` at both endpoints while requiring `P=0` at one
and `P=B_mem` at the other. It is not a single-valued analytic `P(X)`.
Source/exchange dynamics or another field could evade this theorem, but the
old closure cannot be silently relabelled as the massless parent clock.

The constructive route is already present in the parent. Checkpoints
4935-4939 own the regular low-energy 1PI coordinate

```text
V_1PI=m_gap^2 psi_c^2/2,
J_gap=m_gap^2 G_N.
```

`J_gap` is one universal essential action parameter, but its numerical value
is not selected. Defining

```text
chi=psi_c/(sqrt(6)M_R),
mu=m_gap/H0,
N=ln a,
```

the leading canonical flat-FLRW system is

```text
E^2=[Omega_m e^(-3N)+Omega_r e^(-4N)+Omega_Lambda
     +mu^2 chi^2]/[1-(chi')^2],

chi''+[3+dlnH/dN]chi'+mu^2 chi/E^2=0,

dlnH/dN=[
 -3Omega_m e^(-3N)/2
 -2Omega_r e^(-4N)
 -3E^2(chi')^2]/E^2.
```

No memory shape is inserted. A finite-start frozen-mode condition removes
the decaying mode; one homogeneous amplitude remains a state datum. Using
`Omega_m=0.3`, `Omega_r=9e-5`, and the nonclaim comparator step
`Delta Omega_psi=2/27`, the zero-`Lambda` physical boundary is

```text
mu=m_gap/H0                 = 0.695241020621410,
chi_initial                 = 1.26540813993480,
Omega_psi,0                 = 0.699910000000001,
Omega_psi,early             = 0.773984074074074,
Delta Omega_psi             = 0.0740740740740734,
flatness/step residual      = 6.67e-16.
```

The trajectory is monotone and regular over `0<=ln(1+z)<=2`:

```text
0 <= normalized shape <= 0.995906740224206,
min forward increment       = 1.2463388582339974e-4,
max|chi'|                   = 0.156577463918320,
min E                       = 1.0000000000000002.
```

Moving the frozen initial surface from `N=-5` to `N=-6` and `N=-7` changes
`mu` by at most `7.25649e-7` and the normalized shape by RMS at most
`1.79214e-6`. The finite-start result is converged at the precision relevant
to this checkpoint.

For the illustrative calibration `H0=70 km/s/Mpc`, the boundary translates
conditionally to

```text
m_gap=1.0381226114215e-33 eV,
J_gap=7.23009869080443e-123.
```

These values are not parent predictions. They are the scale required by this
executed comparator transition.

The direct scalar does not derive the old fixed shape:

```text
RMS versus fixed p=3,u=1/4 = 0.161633102799274,
maximum absolute residual  = 0.399259850058825.
```

Its compact stretched-exponential diagnostic is instead

```text
p_eff=1.10597003979209,
u_eff=0.436156123659685,
diagnostic RMS=0.00319571763170777.
```

This diagnostic is not a replacement model. It quantifies why the direct ODE
must be scored rather than renamed as M6.

The O4 prediction is also propagated on this massive branch. For
`B=-c_O4 dot(psi_c)^2`, differentiating the massive Klein-Gordon equation
gives

```text
psi'''=-3dot(H)dot(psi)-3Hddot(psi)-m_gap^2dot(psi),

[ddot(B)+Hdot(B)]/(-2c_O4)
 =ddot(psi)^2-3dot(H)dot(psi)^2
  -2Hdot(psi)ddot(psi)-m_gap^2dot(psi)^2.
```

The symbolic reduction residual is zero. The branch-specific controls are

```text
max|delta_Q/(H0t_P)^4| = 7.81984228041762,
max|delta_F/(H0t_P)^4| = 21.9316804206443,

max|delta_Q| at H0=70   = 1.74962465879476e-243,
max|delta_F| at H0=70   = 4.90703104957204e-243.
```

The massive thaw route therefore preserves the 5191 low-energy tensor-safety
result. The all-scale UV-completion boundary remains unchanged.

The route decision is

```text
parent FLRW stress and scalar equation          = derived;
massless shift-current branch                   = derived;
massless nonzero state selection                = not supplied;
M6 equals source-free analytic P(X)              = rejected exactly;
universal massive parent-scalar route            = retained;
J_gap numerical value                            = not selected;
homogeneous amplitude                            = state datum;
fixed p=3,u=1/4 parent identity                  = rejected numerically;
direct parent-scalar likelihood                  = next calculation;
O4 massive-branch tensor safety                  = passed conditionally;
cosmology-support and full-unification claims    = false.
```

The next target is checkpoint 5193: add the direct parent-scalar ODE to the
existing Pantheon+/DESI-DR2 likelihood machinery and score

```text
LambdaCDM,
wCDM,
CPL,
old fixed M6 comparator,
parent scalar with Lambda_cal free,
parent scalar with Lambda_cal=0 ablation.
```

The comparison must use the same data/covariance treatment, explicit
parameter penalties, prior-edge diagnostics, and no-SH0ES branch. A fit may
estimate the universal mass and state amplitude; it may not be described as
deriving their numerical values.

Checkpoint artifacts:

```text
document:
  5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-mass-gap-cosmology-gate.md
script:
  scripts/Y5_R2FR_5192_parent_motion_FLRW_branch_and_memory_separation.py
outputs:
  source-intake/functional_rg/5192/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5192_VALIDATION.csv
```

Validation is `37/37 PASS`. All eight CSVs parse without malformed or
non-finite cells. All 17 local provenance sources exist and match their
locked hashes. The 5192 output tree contains nine files and `74715` bytes.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5192 output tree:
  03cabc0c1e245ad03b204a60cfe85c2366a5a2c49c79d804da614c8f02bfd7b5
document:
  e171efb8d498df44b535f6c25517c86a0cd5e8b993a67bfb8a9e3b74301eecc3
script:
  f46ba60d65fbe57434a906e01bfdf2055dea33590b5cd3dc891f453812858a77
result:
  b05068d679118084d07d1b9420603d9bd231369ef1e5889d2ab5c3fa0171df32
validation:
  7bd72e8546dbaa85670d4e33004481c11aa5eca2faf6faab155c5d94cfe00012
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`; the protected
`formalization-workbench` was not modified.

## Historical handoff - checkpoint 5191

Checkpoint 5191 resolves the independent `O4=C^2 X` tensor gate exposed by
5189. The answer is neither "delete the operator" nor "accept a fundamental
ghost." The parent predicts a nonzero, on-shell-independent operator whose
finite fourth-order tensor polynomial is not a healthy exact all-scale
theory, but whose low-energy effect is order-reducible and extraordinarily
suppressed on the explicitly bounded canonical branch.

The assembled parent convention is

```text
Gamma contains -u_O4 C_abcd C^abcd X,
c_O4=-u_O4,
B(eta)=c_O4 Xbar(eta).
```

The completed fixed point and four converged infrared endpoints give

```text
u_O4*=-0.0018050754086485139,
u_O4=0 invariant=False,
O4 adds a relevant UV direction=False,

-3.3225249561681114 <= W_O4=u_O4/g^2
                             <= -3.3224177636400554.
```

In the canonical scalar coordinate,

```text
c_O4=-u_O4/Z=-W_O4 l_P^4>0,
|c_O4|<=2.2672938165363195e-139 m^4.
```

For a homogeneous timelike canonical clock, `X_c<0`, so `B<0`.

The full interaction is not redundant. The 4930 integration-by-parts/EOM
quotient retains

```text
O4=C_abcd C^abcd (nabla phi)^2
```

as an independent six-derivative scalar-gravity operator. The 4959
gauge-complete five-projector on-shell Gram matrix is positive definite,
with minimum eigenvalue

```text
1.683210889814806e-05.
```

A field redefinition can move the operator among equivalent basis elements,
but cannot erase its full on-shell amplitude. This is distinct from reducing
its free tensor `q^4` two-point term at a fixed EFT order.

For either real TT polarization `gamma(eta) cos(kz)`, the executed full
linearized Riemann/Ricci/Weyl contraction gives, with
`D gamma=gamma''+k^2 gamma`,

```text
C_1^2
 =1/2(D gamma)^2-2k^2(gamma gamma')'.
```

For time-dependent `B`, the exact weighted identity is

```text
B C_1^2
 =B(D gamma)^2/2-k^2 B'' gamma^2+J',

J=k^2[B' gamma^2-2B gamma gamma'].
```

Both symbolic residuals vanish exactly. The `B''` term is therefore required
and cannot be lost by treating the total derivative as though `B` were
constant.

In the inherited tensor normalization,

```text
A=M_R^2/4,
K_TT(q^2)=q^2(A+Bq^2),
q^2=omega^2-k_phys^2.
```

The two-polarization highest-acceleration Hessian is

```text
H_AB=B delta_AB,
rank=2 and det=B^2 when B!=0.
```

The isolated finite `O4` tensor truncation is therefore not degenerate. The
TT block is an independent FLRW irrep; `P(X)` contributes no cancelling TT
acceleration Hessian, `C^3` begins cubically on `Cbar=0`, and `CFF` has no
pure-TT quadratic term on `Fbar=0`. An unresolved higher-order or nonlocal
tower may alter the full spectrum, but it cannot be assumed as a
cancellation.

If the finite polynomial is incorrectly resummed as exact, then

```text
q_extra^2=-A/B,

1/[q^2(A+Bq^2)]
 =1/A[1/q^2-1/(q^2-q_extra^2)].
```

The GR and extra-pole residues are respectively `+1/A` and `-1/A`. The
predicted timelike branch `B<0` gives a positive `q_extra^2` but a
negative-residue heavy mode. For `B>0`, the root also has tachyonic sign.
The finite truncation is not an exact healthy two-mode fundamental theory.

The low-energy EFT nevertheless survives. For constant `B`,

```text
gamma=[1-B D/(2A)] gamma_R
```

removes the complete linear-`B` `q^4` two-point term. On FLRW, using

```text
E0=gamma''+2 Hc gamma'+k^2 gamma=0,
Hc=a'/a,
D gamma=E0-2Hc gamma',
```

and retaining the exact `B''` contribution gives the order-reduced action

```text
S_T,red=1/2 int d eta [
  Q_T gamma'^2-F_T k^2 gamma^2
]+O(B^2),

Q_T=Aa^2+4B Hc^2,
F_T=Aa^2+2B''.
```

It is second order. In cosmic time,

```text
delta_Q=4BH^2/A,
delta_F=2[ddot(B)+H dot(B)]/A,
c_T^2=(1+delta_F)/(1+delta_Q)+O(B^2).
```

The field redefinition must also be applied consistently to source and
readout maps. It cannot be used to change frames selectively.

For a homogeneous shift-symmetric `P(X)` clock, current conservation further
gives

```text
a^3 P_X dot(psi)=constant,
c_s^2=P_X/(P_X+2X P_XX),
d ln|B|/d ln a=-6c_s^2.
```

Defining

```text
s_B=[ddot(B)+H dot(B)]/(BH^2),
```

one obtains the exact shape law

```text
s_B=36c_s^4-6c_s^2(1+dot(H)/H^2)
    -6 d(c_s^2)/d ln a.
```

For a canonical clock, `c_s^2=1`. On a constant-`w` background,

```text
s_B=39+9w,
30<=s_B<=48 for -1<=w<=1.
```

The numerical envelope deliberately uses the wider `|s_B|<=100`.

Define

```text
Omega_kin=-X_c/(2rho_total),
rho_total=3M_R^2H^2,
M_R^2=1/(8pi l_P^2).
```

On the healthy canonical branch, assuming `0<=Omega_kin<=1` without a large
positive kinetic density hidden by a cancelling negative component,

```text
epsilon_bg=|B|H^2/A
          =24|W_O4|Omega_kin(Ht_P)^4,

|delta_Q|=4epsilon_bg,
|delta_F|=2|s_B|epsilon_bg,

|q_extra|/H
 =1/[sqrt(24|W_O4|Omega_kin)(Ht_P)^2].
```

At `Omega_kin=1`, `|delta_Q|=1` only at

```text
H=4.389104729428941e42 s^-1,
```

and the heavy pole reaches `H` only at

```text
H=6.207131435034301e42 s^-1.
```

At the already extreme illustrative value `H=1e40 s^-1`,

```text
|delta_Q|<=2.694611909530889e-11,
|delta_F|<=1.347305954765445e-09
```

with `|s_B|<=100`. Thus `O4` does not obstruct local GR or low-energy
cosmological tensors when treated as the irrelevant EFT operator the parent
flow makes it. This is a conditional canonical-background theorem, not a
selection of the actual MTS cosmological state.

The route decision is

```text
O4 parent ownership                         = derived;
u_O4=0 invariant surface                    = false;
full O4 operator redundant                  = false;
isolated finite O4 TT truncation degenerate = false;
resummed extra-pole residue                 = opposite to GR;
first-EFT-order q4 two-point term reducible = true;
time-dependent FLRW reduced action          = derived;
local psi=0 tensor protection               = exact;
canonical sub-Planck cosmology              = conditionally controlled;
general P(X) cosmological X(t)              = still required;
all-scale UV completion                     = not established.
```

The next target is no longer another abstract tensor gate. Insert the actual
functional MTS `P(X)` into the homogeneous current/Friedmann system and
select the cosmological branch

```text
Xbar(t), B(t), s_B(t), Omega_kin(t)
```

used by the likelihood work. That converts the conditional envelope into a
branch-specific CMB/GW propagation prediction without introducing a new
coefficient.

Checkpoint artifacts:

```text
document:
  5191-Y5-R2FR-O4-FLRW-tensor-nondegeneracy-order-reduction-and-cosmological-safety-theorem.md
script:
  scripts/Y5_R2FR_5191_O4_FLRW_tensor_nondegeneracy_and_order_reduction.py
outputs:
  source-intake/functional_rg/5191/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5191_VALIDATION.csv
```

Validation is `45/45 PASS`. All 16 local provenance sources exist and match
their locked hashes. The 5191 output tree contains eight files and `31609`
bytes.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5191 output tree:
  71abd12cfb55e20e49fe2e66fb1269442ecbb3b46d95bf01038a37021e08833b
document:
  4568e2ac3fe467b2fa1e2c294058692a0c62994e53e703405b2b18864742b6fa
script:
  36984e867b0f6e115a4637be4012e5019a024e68b9317637472e325e0ea4907c
result:
  e8c3d48469a0e47a5629d30dd43992e1193f20f064f6c582db496514ac08712d
validation:
  82985fdb42002ca783dc444e69d6dbdb3f21582cd686df158e0866111908ab38
```

No GitHub action occurred. The public worktree remains clean at
`8913c00b77d98e457ddb0c48e9aeec9cc5f309fd`; the protected
`formalization-workbench` was not modified.

## Historical handoff - checkpoint 5190

Checkpoint 5190 does not repeat the earlier occupied-state bubble searches.
It closes the unresolved ownership question behind the healthy abstract 5181
Schur completion.

The theorem is deliberately scoped to nonzero spatial momentum, zero
frequency, a regular DC limit, local contact subtraction, and the
homogeneous/isotropic, parity-even, local diffeomorphism-invariant scalar
sector. It does not reject a parent-derived direct state, an independent
vector background, or genuinely active/nonlocal dynamics.

For static Fourier momentum along `z`, conservation gives the exact
nonanalytic connected-stress constraints

```text
k_mu=(0,0,0,k), k!=0,
T03=T13=T23=T33=0.
```

The Ward matrix has rank four and nullity six. The surviving stress basis is

```text
helicity 0: rho=T00, tau=(T11+T22)/2;
helicity 1: P_x=T01, P_y=T02;
helicity 2: T_plus=(T11-T22)/2, T_cross=T12.
```

Solving `[G_SO(2),C]=0` for the complete symmetric six-component covariance
uses 21 variables, has constraint rank 16, and leaves exactly five invariant
functions:

```text
C=diag-block(C_scalar[2x2], C_vector I_2, C_tensor I_2).
```

Every cross-helicity block vanishes. A transverse Poynting fluctuation is
therefore not a hidden Newtonian scalar response.

The missing parent-mixing problem is now an exact power-counting result. If

```text
G_chi(k)~|k|^-alpha,
B_hchi(k)~|k|^d,
K_GR~M_R^2 k^2,
```

then the Schur correction relative to Einstein scales as

```text
(B_hchi G_chi B_chih)/K_GR~|k|^(2d-alpha-2).
```

The 5148 target exponent is `-1`. The massless pair has `alpha=1`, so it
requires `d=1`. The current zero-background scalar parent instead has

```text
kinetic Hilbert vertex h(partial psi)^2: d=2;
curvature improvement R psi^2:           d=2.
```

The zero-derivative mass vertex vanishes at the massless point; retaining it
restores a gap and an analytic bubble. Thus the owned pair produces
`x n_q(x)` relative response while the target requires `n_q(x)/x`, with the
exact ratio

```text
pair/target=x^2.
```

The abstract 5181 completion uses `u=sqrt(K_h)h` and constant normalized
mixing. In unnormalized variables this is

```text
B_hchi=sqrt(A K_h)~sqrt(A) M_R |k|,
```

which is precisely the absent one-spatial-derivative scalar cross block. A
local equilibrium three-dimensional unitary scalar with `Delta>=1/2` has
singularity no stronger than `alpha=2`; a `d=2` escape would require
`alpha=3`. Active, nonlocal, anisotropic, or independent-vector parents lie
outside this no-go and would have to be derived as new dynamics.

Poynting was tested rather than dismissed. At finite frequency,

```text
T_L^0=(omega/k)T00.
```

It vanishes in a regular DC limit. The remaining Maxwell Poynting vector is
transverse, so

```text
k_i P_T^i=0,
a_i P_T^i proportional k_i P_T^i=0.
```

Maxwell `T_EM^0i=(E cross B)^i` remains a valid same-coframe
vector/gravitomagnetic source. It simply cannot supply the stationary common
scalar galaxy kernel. A singular noncommuting DC limit must retain its
conserved density and Ward partners; that is a full hydrodynamic/Vlasov or
new active-state problem, not a Poynting-only patch. An independent
longitudinal unit-flow vector could realize `d=1`, but it adds new modes and
requires parent ownership, Kubo coefficients, PPN and stability gates.

The route arbitration is now:

```text
current local scalar propagator enhancement = rejected;
5181 abstract completion                    = healthy target contract only;
stationary Poynting scalar escape           = rejected;
direct conserved motion-state stress        = conditional survivor;
new active/nonlocal or vector parent         = not ruled out, not derived.
```

The direct-state equation

```text
K_GR h=J_visible+J_state
```

is not the same mechanism as the Schur equation

```text
(K_GR-Sigma)h=J_visible.
```

The 5151 positive conserved state can source rotation and lensing through one
Einstein metric while leaving the local unoccupied branch intact. It remains
conditional because the parent has not selected its occupation, transition,
core, edge, or nonlinear formation law. It is matter-like until that missing
derivation is supplied and cannot by itself complete MTS unification.

Because the separate galaxy programme already owns nonlinear formation, the
next unified-framework target is the independent root gate exposed by 5189:

```text
determine whether c_O4 C^2 X is degenerate/redundant,
or only a controlled order-reduced EFT correction;
derive the tensor pole/residue and cosmological claim band accordingly.
```

Checkpoint artifacts:

```text
document:
  5190-Y5-R2FR-static-Ward-helicity-one-derivative-mixing-no-go-and-direct-state-route-freeze.md
script:
  scripts/Y5_R2FR_5190_static_Ward_helicity_and_mixing_no_go.py
outputs:
  source-intake/functional_rg/5190/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5190_VALIDATION.csv
```

Validation is `44/44 PASS`. The 5190 output tree contains eight files and
`37938` bytes.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5190 output tree:
  8658f7f6f8a9e72e81e8fbd46cbf84ff9d5281caf9656fc19567f14bff18221c
document:
  4f3d83db550d5eed2bea3fc8f6d6542807ec610a152abd2146a39ede6bdf6d55
script:
  03cbeb66f2792a2161c51f0f5c8dc1ea0bb8f47a8190626632bd6211bf2fef2a
result:
  305157492ebc5d064f7ba38d9a83508e7bcb089529b0c7dbec58a66432519ab7
validation:
  c99dd782309139b52ed6aad96d577ac8487835227b6efd682ec956ce11f0e8b9
```

No GitHub action occurred. The public worktree and
`formalization-workbench` were not modified.

## Historical handoff - checkpoint 5189

Checkpoint 5189 maps the surviving MTS motion sector into the 5188
coframe/ADM parent instead of treating “motion” as an untyped extra field.
The exact result is partial ancestry:

```text
old motion scalar psi -> hypersurface-orthogonal clock/time-flow;
non-scalar E/e        -> spatial geometry;
K_ij=(1/2)L_u h_ij   -> motion of already existing space.
```

For `X<0`,

```text
u_mu=-nabla_mu psi/sqrt(-X).
```

Because `u=f dpsi`, `u wedge du=0` identically. The old scalar can own a
clock congruence but not an independently vortical spin-one field. Fixing
that clock leaves an executed rank-six family of spatial metrics. Thus it
does not determine `h_ij` or the three spatial coframe legs. The older 2048
spherical coframe remains a useful special construction, but it supplied an
independent radial function `S(r)` and did not derive `T^2 S=1`; it is not a
general scalar origin of curved spatial geometry.

With signature `(-,+,+,+)`,

```text
nabla_mu psi=-Pi n_mu+s_mu,  n.s=0,  X=-Pi^2+s^2,
J^mu=2 P_X nabla^mu psi,
T^mu_nu=2 P_X nabla^mu psi nabla_nu psi-delta^mu_nu P.
```

The exact ADM projection is

```text
rho=2 P_X Pi^2+P,
j_i=-2 P_X Pi s_i,
S_ij=2 P_X s_i s_j-P h_ij,
p_iso=(2/3)P_X s^2-P,
pi_ij=2 P_X(s_i s_j-s^2 h_ij/3).
```

The anisotropic-stress trace vanishes identically. A homogeneous timelike
clock has `j_i=pi_ij=0`; a spacelike gradient is anisotropic. Stress
conservation closes through

```text
nabla_mu T^mu_nu=(nabla_mu J^mu-P_psi)nabla_nu psi.
```

Minimal `P(X,psi)` preserves the ADM constraint architecture. In velocity
order `(dot N,dot N^1,dot N^2,dot N^3,dot psi)`, its matter Hessian is

```text
diag(0,0,0,0,
     -2 sqrt(h)[P_X-2 Pi^2 P_XX]/N).
```

The lapse/shift block has four exact null directions; a regular scalar adds
one physical configuration degree of freedom. Hence

```text
metric only:        (12-2*4)/2=2;
metric plus scalar: (14-2*4)/2=3.
```

The full regular two-derivative parent contains two tensors plus one scalar.
On the unoccupied local branch below `m_gap`, only two gravitational modes
are resolved; this is scalar decoupling, not scalar field removal.

For a homogeneous clock and a trace-free tensor perturbation,

```text
h_ij=a^2 exp(gamma)_ij,  tr(gamma)=0,
det(h)=a^6,              X=-dot(psi)^2/N^2.
```

Therefore the pure `P(X)` action is independent of `gamma` at all orders,
and its first and second TT variations vanish exactly. The local
`psi=0`, `X=0` branch also retains the 5187 block-diagonal Hessian.

The important correction is the retained six-derivative portal. Use
`c_O4` for the signed coefficient actually multiplying `+C^2 X`, because
4935 displayed `+u_O4` while 5187 displayed `-u_O4`. Although FLRW has
`Cbar=0`, this kills only the background term and first variation. The
executed off-shell TT calculation gives

```text
C1_abcd C1^abcd
 =(gamma_plus^2+gamma_cross^2)(omega^2-k^2)^2.
```

Writing `q2=omega^2-k^2`, the EH plus O4 principal kernel is

```text
K_TT=q2[M_R^2/4+c_O4 X q2].
```

The massless GR pole and its low-energy speed remain exact. If
`c_O4 X!=0`, a second nonperturbative pole occurs at

```text
q2=-M_R^2/(4 c_O4 X).
```

Consequently:

```text
local psi=0:
  O4 pure-metric and mixed Hessians vanish exactly;
  two local tensor modes are protected.

homogeneous cosmological clock:
  minimal P(X) is TT-safe;
  O4 is not Hessian-silent;
  require |4 c_O4 X q2/M_R^2|<<1 throughout an EFT claim band,
  or derive a degeneracy/cancellation/c_O4 X=0 theorem.
```

An independently varied Einstein-aether/unit-flow field remains a
correspondence extension, not the primitive local parent. Its 4857
PPN-safe surface and `G_cos=G_N` lock reproduce exactly, but it carries two
tensor, two vector and one scalar gravitational/aether modes. Its `p->0`
chart is singular. A composite Landau/state flow adds no independent mode
if it is not varied.

The branch decision is now:

```text
local vacuum/compact exterior = leading quadratic GR protected;
homogeneous FLRW clock        = O4 tensor EFT gate open;
classical stationary galaxy   = healthy P(X) no-lump route rejected;
occupied isotropic galaxy     = retained response route;
unit-flow/aether              = correspondence backstop only.
```

The occupied-state target is sharper. With

```text
c=(Phi+Psi)/sqrt(2), s=(Phi-Psi)/sqrt(2),
K_eff=K_GR-Sigma,
C_q=y^(1+q)/(1+y^q), y=mu/|k|, q=0.77,
Sigma_cc/K_GR,cc=A C_q/(1+A C_q),
```

`A>=0` gives a positive static kernel. Exact no-slip for arbitrary ordinary
scalar sources requires `Sigma_cs=Sigma_sc=0` with an invertible slip block.
Tensor protection independently requires `Pi_TT Sigma Pi_TT=0` or a
frequency-dependent bound. The CTP kernel must also satisfy its Diff Ward
identity and retarded/noise positivity.

A real origin no-go is proved under explicit assumptions. After matching
the local Einstein residue, a local gapped vacuum polarization is analytic
in `k^2`; the target has

```text
C_q~mu/|k|,
K_eff/K_GR~|k|/(A mu)
```

in the deep infrared and therefore an absolute nonanalytic `|k|^3` inverse
kernel. The gapped local vacuum cannot generate it. The viable origin class
is narrowed to a gapless continuum or occupied-state retarded stress
spectral density.

The next constructive target is therefore not another coefficient hunt:

```text
derive the occupied-state rho_cc(omega,k);
prove the Ward identity;
project rho_cs and rho_TT;
recover or reject C_q and its mu law with one cross-arena parameter set.
```

Poynting remains the same-coframe `T_EM^0i` momentum source. A stationary
Poynting vector does not by itself provide the missing common scalar
susceptibility; any transfer must be derived dynamically in that same CTP
kernel.

Checkpoint artifacts:

```text
document:
  5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-and-local-tensor-protection-theorem.md
script:
  scripts/Y5_R2FR_5189_motion_ADM_projection_and_tensor_protection.py
outputs:
  source-intake/functional_rg/5189/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5189_VALIDATION.csv
```

Validation is `46/46 PASS`. The 5189 output tree contains ten files and
`41700` bytes.

Integrity:

```text
formalization-workbench:
  b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758
checkpoint 5176:
  254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b
checkpoint 5189 output tree:
  26ce93a44a67f002e088327ab7b46578c26a843ecb7bae8431709b413eba5326
document:
  4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266
script:
  7d7e4be61ddb7cb504a71b8f03049d12058ac5df2961bcab8005be7ca1e09a0b
result:
  6418ffc826ed2068b1f4df46d56423fe3f866c0e9bfa363098f4e849174fcfc2
validation:
  511a92a92551a07f7f175028ff81f376b8f40d2130f33e887d4eb1414c6ef933
```

No GitHub action occurred. The public worktree and
`formalization-workbench` were not modified.

## Authoritative current handoff - checkpoint 5188

Checkpoint 5188 executes the foundational target selected by 5187. It does
not add another coupling ledger. It proves which relational parent route is
mathematically possible, constructs the minimal surviving route, derives its
spin-two kinetic ratios and mode count, and verifies that the existing
Einstein/Newton and Maxwell/Poynting chains survive.

The first exact result is the four-clock/rod scalar dichotomy. For

```text
J^A_m=partial_m X^A,
g_mn=eta_AB J^A_m J^B_n,
det(g)=-(det J)^2,
```

the two branches are

```text
det(J)!=0 -> X^A are local coordinates and g=X^*eta is exactly flat;
det(J)=0  -> g is degenerate.
```

Four scalar first jets do span ten metric variations at one point, so the
old rank-only test was necessary but not sufficient. The executed nonlinear
witness `X=(t,exp(x),y,z)` gives
`g=diag(-1,exp(2x),1,1)` and exactly `R=0`. Generic curved local GR
therefore cannot come from scalar clocks/rods with only a constant internal
Lorentz metric.

The minimal surviving parent is the multiplicative relational coframe

```text
e^a_m=E^a_A(x) partial_m X^A,
g_mn=eta_ab e^a_m e^b_n,
H^mn=sqrt(-g)g^mn.
```

For any nondegenerate coframe and invertible `J`, `E=e J^-1`; the map is
exactly surjective. `E` is a genuinely non-scalar coframe distortion. It is
not derived from the old motion scalar and is not presented as though it
were.

The exact linear ranks at `E=J=I` are

```text
(deltaE,deltaJ)->deltae: rank=16, nullity=16;
deltae->deltag:          rank=10, nullity=6;
(deltaE,deltaJ)->deltag: rank=10, nullity=22;
deltae->deltaH:          rank=10, nullity=6.
```

The six coframe null directions are local Lorentz rotations. Exact rational
trials verify

```text
J->S J, E->E S^-1 leaves e invariant;
E->Lambda E, Lambda^T eta Lambda=eta leaves g and H invariant;
det(g)=-(det E det J)^2.
```

This gives a precise MTS dictionary:

```text
time:   tau=e^0/c_*;
space:  h_mn=sum_i e^i_m e^i_n;
motion: u and K_ij=(1/2)L_u h_ij;
metric: g_mn=h_mn-c_*^2 tau_m tau_n.
```

On a local foliation, Einstein-Hilbert is exactly

```text
S_EH=(M_R^2/2) int N sqrt(h)
     [R3+K_ij K^ij-K^2-2 Lambda_cal]+boundary.
```

The executed DeWitt kinetic form has rank six and inertia
`(5+,1-,0 zero)`. One Hamiltonian plus three momentum first-class
constraints give

```text
(12-2*4)/2=2
```

physical spin-two configuration degrees of freedom. If the action depends on
`E,X` only through `e`,

```text
deltaS/deltaE^a_A=E_e,a^m J^A_m,
deltaS/deltaX^A=-partial_m(E_e,a^m E^a_A),
```

so the `X` equation is dependent on the coframe equation and the split adds
no physical pole. Any direct split-breaking `E` or `X` operator is outside
this theorem and must be analyzed separately.

The leading spin-two kinetic operator is no longer inserted by coefficient.
For the four Lorentz-invariant two-derivative quadratic structures, an exact
Lorentzian `120 x 4` gauge-constraint matrix has

```text
rank=3,
nullity=1,
kernel=(1,-2,2,-1).
```

This is the unique Fierz-Pauli ratio up to overall scale. The
positive-residue convention is

```text
L_FP=-1/2 L1+L2-L3+1/2 L4.
```

With the explicit local-consistency premises already source-locked by 4960,
its nonlinear two-derivative completion is Einstein-Hilbert plus
`Lambda_cal`, modulo field redefinitions, boundary and topological terms.
The 5187 higher-derivative/nonlocal EFT corridor remains explicit.

Curved and weak-field witnesses execute successfully:

```text
FLRW R=6(a a_ddot+a_dot^2)/a^2;
de Sitter a=exp(Ht) -> R=12 H^2;
weak e^0_0=1+Phi, e^i_j=(1-Phi)delta^i_j
  -> g00=-(1+2Phi), gij=(1-2Phi)deltaij, gamma=1;
linearized G00=2 nabla^2 Phi.
```

Thus

```text
M_R^2 G00=rho
-> nabla^2 Phi=4 pi G_N rho,
G_N=1/(8 pi M_R^2),
```

and the same coframe gives the slow geodesic and null/lensing branch.

The Maxwell stress calculation is also executed directly in the local
orthonormal frame:

```text
F^2=2(B^2-E^2),
T^00=(E^2+B^2)/2,
T^0i=(E cross B)^i,
trace(T)=0
```

for canonical fields, or `T^0i=Z_A(E cross B)^i` before canonical
normalization. The Poynting vector is therefore the electromagnetic energy
flux measured by, and sourcing, the same coframe; it is not a separate
background flow.

What is established:

```text
scalar-clock-only curved GR              =exactly rejected;
minimal relational coframe map           =exact and surjective;
integrated H inside this candidate       =rank-ten coframe composite;
relational/Lorentz redundancies          =exact;
e-only split extra physical mode         =absent;
massless spin-two kinetic ratios         =unique;
ADM physical gravity modes               =2;
leading local GR/Newton inside parent    =retained;
flat Maxwell/Lorentz/stress/Poynting     =retained.
```

What remains:

```text
E or tau,h,u/K from old scalar MTS       =not derived;
Diff generated by one old scalar         =false;
visible U(1) representations/charges     =parent data;
absolute G_N value                       =one calibration;
global chart caustics/topology/edges      =open;
split-breaking direct E/X operators      =outside no-mode theorem;
physical total c_IR/nonlocal/p8plus       =open;
full MTS unification                     =not claimed.
```

The next target is not another scalar rank audit. Checkpoint 5189 should map
the surviving MTS motion variables into the exact coframe/ADM invariants
`tau,h_ij,u,K,sigma_ij` and test whether one motion Hessian preserves the
four ADM constraints and two local spin-two modes while supplying the
cosmology/galaxy response without arena-dependent changes to `G_N` or
`gamma=1`. If that map fails, the coframe remains fundamental and the old
motion field remains a controlled stress/exchange sector.

Generated evidence:

- `5188-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-parent-and-Fierz-Pauli-selection-theorem.md`
- `scripts/Y5_R2FR_5188_relational_coframe_parent_and_Fierz_Pauli_gate.py`
- `source-intake/functional_rg/5188/prior_relational_parent_supersession.csv`
- `source-intake/functional_rg/5188/scalar_clock_pullback_no_go.csv`
- `source-intake/functional_rg/5188/minimal_relational_coframe_factorization.csv`
- `source-intake/functional_rg/5188/coframe_H_rank_and_invariance.csv`
- `source-intake/functional_rg/5188/Fierz_Pauli_gauge_nullspace.csv`
- `source-intake/functional_rg/5188/MTS_ADM_dictionary_and_mode_count.csv`
- `source-intake/functional_rg/5188/curved_and_weak_field_witnesses.csv`
- `source-intake/functional_rg/5188/same_coframe_GR_Newton_Maxwell_chain.csv`
- `source-intake/functional_rg/5188/parent_upgrade_claim_boundary.csv`
- `source-intake/functional_rg/5188/source_provenance.csv`
- `source-intake/functional_rg/5188/relational_coframe_parent_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5188_VALIDATION.csv`

Validation and integrity:

```text
validation                                  =48/48 PASS;
formalization-workbench SHA-256             =b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5176 tree SHA-256                =254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b;
checkpoint-5188 output tree SHA-256         =a0d7245f1929707e8e13292edaf2c0f6b5e6a3d2cee0458c55a456d6ec8f4a77;
checkpoint-5188 output files/bytes          =11/40410;
document SHA-256                            =06f376fbab1a07312ae6993f1ea2a2e2f276a2438d7a2c15daf7993a17f6fb7a;
script SHA-256                              =536aa471e58279e0935f55be6f01d07f2a1bee4b72dddb181bb5eb9924c9b6cb;
result JSON SHA-256                         =9160b84ad6cbb9de7cda7df53b4d5a0c35f24b0b2c2795ff529bc94a3c12a30b;
validation CSV SHA-256                      =fbd8fb2b225363f10a74b7707bf90d8f99697fc067ec3849db3060f646837e08;
scripts/__pycache__                         =absent;
GitHub action                               =none.
```

## Historical handoff - checkpoint 5187

Checkpoint 5187 stops the repeated search for another local source
coefficient. Checkpoint 4960 had already proved one universal leading
spin-two residue inside the explicit integrated-`H`, exact-Diff/BRST parent.
The new checkpoint assembles the surviving local sectors into one canonical
action, derives its zero-field Hessian and source vertices, proves the
Einstein/Newton and Maxwell/Poynting chains, and separates derived relations
from unavoidable scale calibrations.

The canonical displayed action is

```text
Gamma_loc=int sqrt(-g){
 M_R^2(R-2Lambda_cal)/2
 -Z_A F^2/4
 -Z_psi(nabla psi)^2/2
 -m_gap^2 psi^2/2
 +c_IR CFF
 +G_C3 I_C3
 -u_O4 C^2(nabla psi)^2
 +P_ge_2(X)}
 +S_matter[g,A,Phi_SM]
 +Gamma_contact+Gamma_nonlocal+Gamma_p8plus,

G_C3=M_R^2 a_plus/2=A_C3^S l_P^2.
```

On an on-shell background with `bar A=bar psi=0`, the local Hessian is
exactly block diagonal:

```text
delta^2 Gamma/(delta h delta A)   =0,
delta^2 Gamma/(delta h delta psi) =0,
delta^2 Gamma/(delta A delta psi) =0.
```

Gauge invariance makes every photon term at least quadratic in `A`;
reflection parity makes every motion term at least quadratic in `psi`.
Curvature-photon `CFF` modifies only the photon block on a curved zero-field
background, `O4` modifies only the motion block, and `C3` modifies only the
metric block. The executed flat field-degree mixed-derivative sum is exactly
zero.

The four-dimensional Hilbert trace-reversal map has

```text
rank        =10,
nullity     =0,
determinant =-1,
R4^2        =identity.
```

The five-source soft/Bianchi system has rank four, nullity one and sole null
direction `(1,1,1,1,1)`. Graviton coordinate normalization cancels exactly
from source exchange. Photon wavefunction normalization leaves only the
physical combination `e^2/Z_A`, with maximum numerical cancellation residual
`2.220e-16`.

The same canonical action now carries the complete leading local chains:

```text
M_R^2(G_mn+Lambda_cal g_mn)=T_total,mn,
G_N=1/(8 pi M_R^2),
Box hbar_mn=-16 pi G_N T_mn,
nabla^2 Phi=4 pi G_N rho-Lambda_cal c^2,
Phi=-G_N M/r-Lambda_cal c^2 r^2/6,
a_r=-G_N M/r^2+Lambda_cal c^2 r/3;

nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n,
u.nabla u^m=(q/m)F^m_n u^n,
T_EM,mn=F_maF_n^a-g_mnF^2/4+c_IR H_CFF,mn,
T_EM^0i=(E cross B)^i.
```

Thus no separate Newton, inertial, orbital, lensing, leading-wave,
photon-stress or Poynting coupling remains to be derived. There are two
leading local force normalizations, `G_N` and `alpha_EM`, each fixed once and
never by arena. The motion coordinate `J_gap=m_gap^2 G_N` is universal but
does not create a classical one-scalar local source on the reflection-even
branch.

The new scale-setting theorem is constructive rather than verbal. The
explicit autonomous family

```text
g_hat(x)=g_star x^2/(1+x^2),
beta_g=2g(1-g/g_star),
g(k)=g_hat(k/Lambda_g)
```

has identical dimensionless fixed-point data for every `Lambda_g`, while

```text
G_N=lim(k->0)g(k)/k^2=C_g/Lambda_g^2.
```

The transformation `Lambda_g -> s Lambda_g` sends
`G_N -> G_N/s^2`. At fixed `J_gap`, it sends
`m_gap -> s m_gap`; therefore `J_gap` does not select the absolute scale.
The current autonomous GR-motion trajectory requires one absolute
gravitational scale calibration unless a future parent supplies a genuine
dimensionful anchor. This does not include the separately counted
`Lambda_cal`, `c_IR`, contact or initial-state data.

The corrected residual and parameter boundary is:

```text
leading local force normalizations                  =2;
neutral-vacuum p4 long-range input count            =0;
p6 empirical inputs                                 =0;
classical one-scalar fifth force                    =exact zero;
standard constant Delta gamma and Delta beta       =exact zero;
max selected C3 exterior |Delta a/a_N|              =3.6208461805802824e-124;
max massless-endpoint determinant |Delta a/a_N|     =1.3684320168245822e-61;
max compact finite C3 |Delta a/a_N|                 =7.415086500522157e-158;
max known nonQCD c_IR / one-ppm arena budget        =1.3813540140137983e-32;
physical total c_IR                                 =open;
p8-plus parent projection/convergence radius        =open;
complete physical thresholded/nonlocal amplitude    =open;
all-operator compact equality to GR                 =not claimed;
full MTS unification                                =not claimed.
```

The leading two-derivative local GR/Newton branch and flat
Maxwell/Lorentz/stress/Poynting chain are established **inside the explicit
parent premises**. `H`, Diff/BRST and visible field representations are not
derived from one motion scalar; checkpoint 4961 already rejects that
scalar-only rank bootstrap.

The next foundational target is therefore not another coupling audit. Test a
minimal genuinely non-scalar relational coframe/tensor parent that could own
integrated `H`, Diff and the visible-field functor. If that construction
fails, retain those objects honestly as fundamental parent data. Independent
finite-EFT work may proceed through the physical `c_IR` match and the minimal
Ricci-flat p8 projection.

Generated evidence:

- `5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md`
- `scripts/Y5_R2FR_5187_canonical_local_parent_action_and_scale_setting_theorem.py`
- `source-intake/functional_rg/5187/canonical_local_parent_action.csv`
- `source-intake/functional_rg/5187/vacuum_quadratic_Hessian_and_source_vertices.csv`
- `source-intake/functional_rg/5187/universal_residue_and_limit_chain.csv`
- `source-intake/functional_rg/5187/RG_scale_setting_no_go.csv`
- `source-intake/functional_rg/5187/canonical_parameter_and_state_count.csv`
- `source-intake/functional_rg/5187/higher_derivative_local_corridor.csv`
- `source-intake/functional_rg/5187/cross_arena_no_retuning.csv`
- `source-intake/functional_rg/5187/source_provenance.csv`
- `source-intake/functional_rg/5187/canonical_local_parent_action_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5187_VALIDATION.csv`

Validation and integrity:

```text
validation                                  =61/61 PASS;
formalization-workbench SHA-256             =b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5176 tree SHA-256                =254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b;
checkpoint-5187 output tree SHA-256         =ca285ab2dd527b1e93b798401260b8ffbe2a5c7ddef641f6694e6f0aa7fef8c8;
checkpoint-5187 output files/bytes          =9/66352;
document SHA-256                            =4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674;
script SHA-256                              =b1d89953e3ef21d4c4be13b31c90efd794947a9385d04530b7e678b4e8620355;
result JSON SHA-256                         =05d9e06edf88c219a6d21f49303b7e98dd82f3d1ecee5c9d445da385d4fa4e6d;
validation CSV SHA-256                      =01fb80fe411f43e64786695c93c713e64b277c2085d28bc4580a7b2033d01f40;
scripts/__pycache__                         =absent;
GitHub action                               =none.
```

## Historical handoff - checkpoint 5186

Checkpoint 5186 executes the neutral-state source-selection route selected at
checkpoint 5185. It reconstructs the checkpoint-5156 FLRW Hessian, derives the
Bogoliubov transfer problem and integrates the abundance for all three locked
masses. It does not merely record that a vacuum prescription is missing.

On the neutral branch `bar(psi)=0`, the mixed metric-motion Hessian vanishes:

```text
delta^2 S/(delta g_mn delta psi)|_bar(psi)=0.
```

The scalar Hilbert stress begins at quadratic order in `delta psi`, so the
linear metric-constraint source is zero for the free production mode. Metric
response re-enters through the parent `h psi psi` vertex derived at checkpoint
4952.

The canonical mode equation is

```text
v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=0.
```

All three locked masses begin oscillation in controlled radiation domination.
The largest checkpoint-5152 transition shift is
`9.301896904756468e-05` in `H`, and the largest non-radiation fraction at
`H=m_gap` is `2.435547348408605e-04`.

With

```text
a(eta)=s eta,
s=H0 sqrt(Omega_r),
a_osc=sqrt(s/m),
y=a/a_osc,
kappa=k/sqrt(m s),
```

the three physical problems reduce exactly to one universal oscillator:

```text
u_kappa,yy+(kappa^2+y^2)u_kappa=0.
```

The half-line radiation-boundary prescription

```text
u_kappa(0)=1/sqrt(2 kappa),
u_kappa,y(0)=-i kappa u_kappa(0)
```

gives

```text
n_kappa=|beta_kappa|^2,
|c_kappa|^2=n_kappa(n_kappa+1),

I_half=integral dkappa kappa^2 n_kappa
      =0.029513535747314544,

C_half=I_half/(2 pi^2)
      =0.0014951731876941788.
```

The numerical Wronskian residual is
`4.989941160271627e-08`. The spectrum has integrable asymptotics

```text
kappa -> 0:
n_kappa approximately 0.23894406462864104/kappa;

kappa -> infinity:
n_kappa approximately 1/(64 kappa^8).
```

The exact symmetric adiabatic crossing provides an independent comparator:

```text
n_kappa=exp(-pi kappa^2),
I_sym=1/(4 pi),
C_sym=1/(8 pi^3)
     =0.004031441804149937.
```

That comparator requires a smooth negative-to-positive `y` extension not
owned by the MTS parent. The half-line prescription is also a boundary choice,
not a derived cosmogenesis law.

Finite-start WKB prescriptions and a second-order ultraviolet state were
executed. They establish:

```text
late projection stability              = better than 2e-5;
coarse/fine phase-space agreement       = better than 2e-4;
ultraviolet order sensitivity           = convergent and suppressed;
infrared state normalization            = boundary dependent;
parent-selected density matrix          = absent.
```

The physical scale is

```text
k_star=sqrt(m s)=m a_osc,
n_0=C_n k_star^3,
rho_0=m n_0,
rho_osc=C_n m^4.
```

Against the locked `Omega_X=0.2657568086361595` target:

```text
m=2.8166916621557602e-21 eV:
largest vacuum fraction = 8.748508719860617e-96;

m=1e-20 eV:
largest vacuum fraction = 2.0777139635569732e-94;

m=1e-18 eV:
largest vacuum fraction = 2.0777139635569732e-89.
```

Even the most favorable locked mass needs

```text
4.8129820444005446e88
```

times more occupation than the largest declared vacuum-production
comparator. The result is therefore not repairable by an order-one
normalization correction.

The source-selection decision is:

```text
free FLRW vacuum production:
  valid neutral squeezed state;
  rejected as Omega_X abundance owner;

arbitrary finite IR squeezing:
  can supply abundance;
  explicit initial-state data, not parent derived;

checkpoint-5152 misalignment:
  can supply abundance and exact dust transfer;
  psi_i remains one global initial datum;

separate nonadiabatic cosmogenesis event:
  only route back to a derived abundance;
  no such event is present in the current locked parent action.
```

This does not invalidate the conditional galaxy occupied-state branch. Its
transfer, conserved stress and local vacuum subtraction remain derived. It
does impose a strict claim ceiling: the present parent action does not derive
the dark-sector abundance or primordial covariance.

The next constructive route is not another undefined vacuum hunt. Freeze the
galaxy state as an explicit conditional cosmological input, preserve its
derived transfer/stress results, and return to the universal-source/local-GR,
Newton and Maxwell spine. Reopen cosmogenesis only if a real parent-owned
time-dependent transition sector is identified.

Checkpoint files:

- `5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-production-and-abundance-no-go.md`
- `scripts/Y5_R2FR_5186_FLRW_Bogoliubov_neutral_vacuum_production_and_abundance_gate.py`
- `source-intake/functional_rg/5186/FLRW_Bogoliubov_neutral_production_results.json`
- `source-intake/functional_rg/5186/universal_radiation_Bogoliubov_spectrum.csv`
- `source-intake/functional_rg/5186/three_mass_Bogoliubov_spectra.csv`
- `source-intake/functional_rg/5186/three_mass_vacuum_abundance_gate.csv`
- `source-intake/functional_rg/5186/vacuum_prescription_and_start_time_sensitivity.csv`
- `source-intake/functional_rg/5186/adiabatic_UV_and_background_robustness.csv`
- `source-intake/functional_rg/5186/neutral_Gaussian_covariance_gate.csv`
- `source-intake/functional_rg/5186/neutral_source_selection_route_decision.csv`
- `source-intake/functional_rg/5186/source_provenance.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5186_VALIDATION.csv`

Validation:

```text
35/35 checks pass;
5186 evidence files = 9;
5186 evidence bytes = 165770;
5186 evidence tree SHA256
 =752630c554b3f1c647f5a27d02d5abb9011162941748f9ae0656146c96e7b83c;

formalization-workbench SHA256
 =b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;

checkpoint-5176 tree SHA256
 =254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b;

scripts/__pycache__ absent;
GitHub action = false.
```

## Historical handoff - checkpoint 5185

Checkpoint 5185 follows the surviving route from checkpoint 5184 and derives
the occupied-state interaction stress from the parent-owned essential
`X^2/X^3` vertices. It does not posit a response kernel and it does not count
the checkpoint-5171 classical Vlasov response twice.

Let the finite vacuum-subtracted state covariance be

```text
C_mn(x)
 =[nabla_m nabla_n' F_state(x,x')]_(x'=x),

A^m_n=g^ma C_an,
t_n=Tr(A^n).
```

For a Gaussian reflection-even state, exact cumulant identities give

```text
<X^2>=M2=t1^2+2t2,

<X^3>=M3=t1^3+6t1t2+8t3.
```

With source-locked physical coefficients

```text
c2=A2 G_N^2,
c3=A3 G_N^4,
```

the first 2PI/Hartree interaction density is

```text
L_H
 =c2(t1^2+2t2)
  +c3(t1^3+6t1t2+8t3).
```

Define

```text
C1_mn=C_mn,
C2_mn=C_ma g^ab C_bn,
C3_mn=C_ma g^ab C_bc g^cd C_dn.
```

The exact explicit metric variation at a stationary 2PI propagator gives

```text
Theta2_mn
 =c2[
    4t1 C1_mn
   +8C2_mn
   -g_mn(t1^2+2t2)
   ],

Theta3_mn
 =c3[
    (6t1^2+12t2)C1_mn
   +24t1C2_mn
   +48C3_mn
   -g_mn(t1^3+6t1t2+8t3)
   ].
```

In four dimensions,

```text
Theta2^m_m=0,
Theta3^m_m=2c3M3.
```

The same functional gives the exact Hartree gap tensor

```text
Z_H^mn
 =g^mn
  +4c2[t1g^mn+2C^mn]
  +6c3[
      (t1^2+2t2)g^mn
     +4t1C^mn
     +8(C2)^mn
     ].
```

Stress and propagation are therefore not separately tunable. A
`5000`-sample complex-step metric variation verifies the closed form with
maximum relative residual `2.27595720048157e-14`.

The first genuinely nonlocal `X^2-X^2` 2PI topology is also derived. Define

```text
D_mn'(x,y)=nabla_m^x nabla_n'^y G(x,y),

I2=Tr[g_x^-1 D g_y^-1 D^T],

I4=Tr[(g_x^-1 D g_y^-1 D^T)^2].
```

The complete 24-contraction all-cross Wick sum is

```text
8I2^2+16I4,
```

so the Euclidean basketball cumulant is

```text
Gamma_2,basketball
 =-4c2^2 integral_(x,y)[I2^2+2I4].
```

CTP continuation produces the nonlocal self-energy and `2<->2` collision
kernel. An independent explicit pairing test over 128 random cross
covariances has maximum relative residual
`4.13298764724799e-14`.

The 2PI Ward chain is

```text
delta Gamma/delta G=0,
delta Gamma/delta <psi>=0

 => nabla_mu T^mu_nu=0.
```

The `2<->2` collision integral contains

```text
delta^4(p1+p2-p3-p4).
```

Therefore

```text
integral dPi_1 p1^nu C_22[f1]=0.
```

The `2<->4` channel does not conserve particle number but does conserve total
four-momentum. The new interaction kernel consequently has the correct
compensated energy-momentum zero mode.

Vacuum silence is exact at the state-functional level:

```text
Delta Gamma_2[F]
 =Gamma_2[G_vac+F]-Gamma_2[G_vac]-local counterterms,

F=0
 => Delta Gamma_2=Delta T_int=Delta Pi_int=0.
```

The free/classical state response is separated as

```text
Pi_total
 =Pi_free/Vlasov
  +Pi_Hartree
  +Pi_basketball
  +Pi_collision,

Pi_new=Pi_total-Pi_free/Vlasov.
```

`Pi_free/Vlasov` was already evolved in checkpoints 5164--5169 and derived
explicitly at checkpoint 5171. It may not be added again.

The source-locked physical coefficients at the transition are

```text
dynamic eta_N:
c2=-7.283939259579509e-111 eV^-4,
c3= 1.323733110599660e-223 eV^-8;

reference eta_N=0:
c2=-7.207628856092619e-111 eV^-4,
c3= 1.323733096741495e-223 eV^-8.
```

Conservative four-dimensional covariance-norm bounds give

```text
||delta Z_X2|| <=24|c2|rho,
||delta Z_X3|| <=288|c3|rho^2,

||Theta_X2||/rho <=48|c2|rho,
||Theta_X3||/rho <=480|c3|rho^2.
```

The executed maxima are

```text
interaction kinetic norm ceiling = 3.492540005516476e-116;
Hartree stress fraction ceiling   = 6.985080011032952e-116;
required transition correction    = 1.644003838438572;
```

and the `X^2` expression independently reproduces the checkpoint-5163
source envelope exactly.

The Hartree response obeys the exact resolvent identity

```text
chi_H=(1-chi0 f_H)^-1 chi0,

Delta chi
 =chi0 f_H(1-chi0 f_H)^-1 chi0,
```

so its relative change is bounded by
`epsilon_H/(1-epsilon_H)`.

Long-time accumulation does not repair the magnitude. Using the deliberately
generous ceiling

```text
T=1e18 s,
omega_max=m_gap/hbar,
```

gives

```text
epsilon_H omega_max T
 <=5.306102337726383e-101.
```

An independent nonrelativistic derivative-amplitude ceiling,

```text
|M_2to2|<=64|c2|m^4,

sigma_2to2<=(256/pi)c2^2m^6,
```

gives

```text
maximum log10(collisions per particle)
 =-281.881979211639532
```

even with `v=1` and the same oversized exposure. The known interaction has
the right Ward, compensation and vacuum structure but is dynamically inert
for the required galaxy redistribution.

Checkpoint 4959's open `O2` coefficient is not a controlled rescue. The
measured `O2` projector Gram norm requires

```text
W_O2/g^2=1.335831664599493e29
```

for a unit O2-only integrated kernel. This is
`4.689488579429405e28` above the natural co-leading reference. Such a value
would destroy the perturbative derivative hierarchy. The exact `O2` flow is
still useful for completeness, but it cannot be invoked as a galaxy patch.

Route disposition:

```text
Gaussian Hartree moments and Hilbert stress      = derived;
Hartree gap tensor                               = derived;
X2 nonlocal basketball topology                  = derived;
Ward conservation and compensated zero mode      = retained;
vacuum silence                                   = exact;
free Vlasov susceptibility                       = subtracted;
known X2/X3 interaction profile repair            = rejected by magnitude;
unknown O2 controlled rescue                      = rejected;
local GR/Newton/Maxwell zero state                = retained;
galaxy or full-MTS claim                          = false.
```

The next target is checkpoint 5186: derive neutral occupied-state
normalization and primordial covariance from the parent's time-dependent
CTP/Bogoliubov kernel. Checkpoint 5158 already proves that neutral
gravitational production may create total occupation while signed `U(1)`
charge remains zero. Checkpoint 5186 must calculate `beta_k`, abundance and
covariance for the three locked masses without fitting `Y_X`, `C_n` or a
galaxy profile.

Checkpoint 5185 audit:

```text
validations                         = 34/34 pass;
metric-variation samples            = 5000;
metric-variation maximum residual   = 2.27595720048157e-14;
basketball pairing samples          = 128;
basketball maximum residual         = 4.13298764724799e-14;
formalization-workbench digest      = b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5176 tree digest         = 254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b;
checkpoint-5185 evidence tree       = 756f0bace9502776c325e8bbef747e4cb3a4ecce0321da2e79afdae8beae4ee1;
checkpoint-5185 evidence files      = 8;
checkpoint-5185 evidence bytes      = 47368;
GitHub action                       = none.
```

Primary files:

- `5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md`
- `scripts/Y5_R2FR_5185_occupied_state_2PI_interaction_stress_and_collision_gate.py`
- `source-intake/functional_rg/5185/occupied_state_2PI_interaction_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5185_VALIDATION.csv`

## Historical handoff - checkpoint 5184

Checkpoint 5184 derives rather than assumes the parent stationary nonzero
motion background requested at checkpoint 5183. The result rejects the
classical stationary-background route inside the certified healthy local EFT,
while leaving the distinct occupied two-point state route open.

For

```text
S_P=integral sqrt(-g) P(X),
X=g^munu nabla_mu psi nabla_nu psi,
P(0)=0,
P_X(0)=1/2,
```

the shift current and Hilbert source are

```text
J^mu=2 P_X nabla^mu psi,
nabla_mu J^mu=0,

T^mu_nu=2 P_X v^mu v_nu-delta^mu_nu P.
```

On a connected horizon-free static galaxy slice,

```text
ds^2=-N^2dt^2+gamma_ij dx^i dx^j,
N>0,
partial_t psi=0,
```

the motion equation is

```text
D_i[2 N P_X D^i psi]=0.
```

Multiplication by `psi-psi_inf` and integration by parts gives

```text
integral 2 N sqrt(gamma) P_X |D psi|^2

 = boundary_integral
   2 N P_X (psi-psi_inf) n^i D_i psi.
```

Checkpoint 4943 fixes

```text
delta S_SM/delta psi=0,
Q_psi=0,
```

through ordinary-matter interiors and nonsingular junctions. With constant
asymptotic data or zero scalar boundary flux and

```text
P_X>=epsilon>0,
```

the right side vanishes and positivity forces

```text
D_i psi=0.
```

Thus a regular localized source-free classical galaxy background is not
available in the healthy parent corridor. This is an existence theorem, not a
profile closure.

The spherical stationary extension is equally restrictive. For

```text
psi=q_clock t+phi(r),
ds^2=-N(r)^2dt^2+A(r)^2dr^2+r^2dOmega^2,
```

the exact radial first integral and off-diagonal stress are

```text
Q=2 N r^2 P_X phi'(r)/A=constant,
T_tr=2 P_X q_clock phi'(r).
```

Regularity and the parent `Q_psi=0` theorem give `phi'=0` when `P_X>0`.
A diagonal static metric independently requires
`q_clock phi'=0`. The stationary branch therefore reduces to a homogeneous
clock, a forbidden nonzero-flux profile, or a degenerate `P_X=0` phase.

The exact checkpoint-4982 mixed variation is

```text
delta_h delta_chi L
 =P_X[tr(h)(v.w)-2v.h.w]
  -2P_XX(v.h.v)(v.w).
```

For Newtonian perturbations and a timelike clock,

```text
B_(Phi,Psi)
 =2 q_clock omega
  [P_X-2q_clock^2 P_XX,3P_X],

K_chichi
 =2P_X k^2
  -2(P_X-2q_clock^2P_XX)omega^2.
```

Hence

```text
omega=0 => B_(Phi,Psi)=(0,0).
```

The clock can affect time-dependent/cosmological response, but its Schur
correction vanishes as `omega^2/k^2` in the quasistatic limit. Its amplitude
also remains global state data rather than a baryon-selected galaxy profile.

For a homogeneous spacelike gradient,

```text
X=V^2,
k_parallel=k cos(theta),
U=[P_X,-P_X+2XP_XX],

B_(Phi,Psi)=2V k_parallel U,

K_chichi
 =2k^2[P_X+2XP_XX cos(theta)^2],

B K_chichi^-1 B^T
 =2X cos(theta)^2 U U^T
  /[P_X+2XP_XX cos(theta)^2].
```

This Schur kernel is anisotropic and homogeneous of degree zero in `k`. It is
carried by a nonlocalized stressed background whose amplitude and direction
are unsourced boundary data. It does not reproduce the checkpoint-5183
required kernel

```text
d_required proportional k n_q(k/mu).
```

For the locked `q=0.77`, the low/high kernel slopes are

```text
required:                 +0.999944863714249,
                           +0.230055136285751;

constant-gradient Schur:   0,
                            0.
```

Relative to the Einstein `k^2` kernel, the required slopes are approximately
`-1` and `-1.77`, while the constant-gradient branch has `-2` at both ends.
No constant normalization repairs both asymptotics.

The `P_X=0` stealth escape also fails the present gate. Exact zero stress for a
nonnull gradient requires both `P_X=0` and `P=0`; absorbing only a cosmological
term still requires `P_X=0`. The source-locked order-eight UV germs give

```text
dynamic eta_N:
first lambda_L zero = 0.158098249516021,
first P_X zero      = 0.236527539730595;

reference eta_N=0:
first lambda_L zero = 0.175979291246878,
first P_X zero      = 0.262824710655261.
```

Both `P_X` roots lie outside the certified `x<=0.1` chart, and the
longitudinal principal eigenvalue crosses zero first. At `P_X=0` the
transverse kinetic eigenvalue itself vanishes. This is an
unstable/strong-coupling escape, not a derived healthy background phase. All
`242` order-eight trajectory rows remain positive in the certified chart.

Route disposition:

```text
regular localized classical P(X) background = rejected in certified EFT;
homogeneous timelike clock static response   = exact zero;
spacelike/null constant gradient             = nonlocalized/stressed/anisotropic;
P_X=0 stealth                                = unhealthy and uncertified;
zero-gradient GR/Newton/Maxwell branch       = retained;
occupied state with <psi>=0 and F_X!=0       = distinct surviving route;
local-GR, galaxy or full-MTS claim           = false.
```

The next target is checkpoint 5185: derive the first parent-owned interacting
occupied-state stress from the existing essential `X^2/X^3` vertices in the
CTP/2PI hierarchy. It must satisfy the metric Ward identity, subtract the
classical Vlasov density already counted at checkpoint 5171, test for a
compensated scale-dependent local-vacuum-silent static kernel, and derive its
state normalization or reject the route. Do not return to an arbitrary
classical profile.

Checkpoint 5184 audit:

```text
validations                         = 35/35 pass;
independent Hessian samples         = 40000;
maximum mixed residual              = 1.23521289129664e-15;
maximum Schur residual              = 2.77555756156289e-16;
formalization-workbench digest      = b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758;
checkpoint-5176 tree digest         = 254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b;
checkpoint-5184 evidence tree       = df41b11e6d09db413e6c3ec2d040361cddddf49df0c459253f274280dad7f134;
checkpoint-5184 evidence files      = 8;
checkpoint-5184 evidence bytes      = 39059;
GitHub action                       = none.
```

Primary files:

- `5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-Hessian-gate.md`
- `scripts/Y5_R2FR_5184_stationary_PX_background_no_lump_and_mixed_Hessian_gate.py`
- `source-intake/functional_rg/5184/stationary_PX_background_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5184_VALIDATION.csv`

## Historical handoff - checkpoint 5183

Checkpoint 5183 corrects a signature inconsistency found while beginning the
stationary-background calculation. Checkpoint 5182 combined the Euclidean
matter-determinant sign with the Lorentzian static Einstein constraint
kernel. Its broad all-`eta` screening theorem is retracted. The current
parent conclusion survives, but for a narrower and sign-consistent reason.

Let

```text
x=(Phi,Psi),

S_L,EH^(2)=+1/2 x^T K_L x,
S_L,src=-J^T x.
```

Static Wick rotation gives

```text
S_E,EH^(2)=-1/2 x^T K_L x,
S_E,src=+J^T x.
```

The bosonic determinant has

```text
Gamma_E,pair
 =+1/2 Tr log(A_0+V[x]),

Gamma_E,pair^(2)
 =-1/2 x^T C x,
C>=0.
```

Therefore Euclidean stationarity is

```text
(-K_L-C)x+J=0,
```

or equivalently the physical static source equation

```text
(K_L+C)x=J.
```

Checkpoint 5182 instead inverted `K_L-C`. That is the exact superseded step.

For the two-sign audit define

```text
K_sigma=K_L+sigma d w w^T,
K_L=a[[0,-1],[-1,1]],
a=2M_R^2 k^2,
d>=0,
w=(u,v).
```

Exact inversion for a dust source gives

```text
Delta_sigma=a-sigma d u(u+2v),

Phi/Phi_GR
 =1+sigma d(u+v)^2/Delta_sigma,

Psi/Psi_GR
 =(a-sigma d u v)/Delta_sigma,

(Phi-Psi)/Phi_GR
 =sigma d v(u+v)/Delta_sigma.
```

The old mixed-sign calculation used `sigma=-1`. The consistent result is
`sigma=+1`. On the GR-connected side `Delta_+>0`,

```text
Phi/Phi_GR>=1.
```

Thus a nonminimal positive pair projector can enhance rather than screen.
The checkpoint-5182 all-`eta` inequality and its special screening formulas
must not be reused.

For the operational pair vector

```text
w(eta)=(4eta-1,1-8eta),
F(eta)=48eta^2-16eta+1,
Delta_+=a+dF(eta).
```

The parent-owned value remains `eta=0`, because the exact shift-symmetric
parent has no `R chi^2` vertex. At `eta=0`,

```text
w=(-1,1),
u+v=0,
Phi=Psi=Phi_GR.
```

This exact dust invisibility is sign independent and is retained.

At the nontrivial no-slip value `eta=1/8`, the corrected formula is

```text
Phi/Phi_GR=Psi/Psi_GR=4a/(4a-d)>1
```

before its pole, not the screening formula reported at 5182. At the
operational pure-common value `eta=1/6`,

```text
Phi/Phi_GR=(9a+d)/(9a-3d),
Psi/Psi_GR=(9a-d)/(9a-3d),
lensing/GR=3a/(3a-d)>1.
```

This possible enhancement is not parent-owned and cannot be inserted as a
fitted curvature coupling.

The zero-background local pair route still fails, now by an independent
momentum-scaling theorem. With `x=k/mu`,

```text
n_q(x)=1/(1+x^q),

required checkpoint-5148 response:
C_q(x)=n_q(x)/x,

local two-derivative Hilbert pair correction:
d/a proportional x n_q(x).
```

Their exact ratio is

```text
[x n_q]/[n_q/x]=x^2.
```

For the locked `q=0.77`, the executed slopes are

```text
local pair low/high = +0.9999984002514203,
                       +0.23000159974857923;

required low/high   = -1.0000015997485794,
                       -1.7699984002514217;

shape-ratio slope   = +1.9999999999999996.
```

No constant normalization can repair two missing inverse powers of momentum
over the full scale corridor. A finite-`k` zero of `Delta_+` is a constraint
pole, not an asymptotic `1/k` response.

Checkpoint-5182 disposition:

```text
static metric expansion and rank-one covariance = retained;
eta=0 pure slip                                  = retained;
eta=0 exact dust invisibility                    = retained;
all-eta screening theorem                        = retracted;
eta=1/8 screening formula                        = retracted;
eta=1/6 screening/lensing formulas               = retracted;
gap collapse as standalone current-parent rescue = still rejected;
zero-background pair as the 5148 bridge          = rejected by eta=0 and scaling.
```

The next checkpoint is 5184, not another pair-loop normalization pass:

```text
derive or reject a parent-owned stationary nonzero motion background and
its exact linear h-delta-chi Hessian;

test the shift-current equation, regular boundary conditions, background
Hilbert stress, static versus finite-frequency mixing and the local-GR limit.
```

Checkpoint 5151's direct conserved state stress remains a separate
conditional route.

Validation and integrity:

- dry run passed `27/27`;
- full runner passed `35/35`;
- independent verifier passed `40,000` random two-sign constraint samples;
- maximum independent response residual:
  `3.61524143954739e-11`;
- internal maximum response residual:
  `2.7426949600339867e-12`;
- exact shape identity residual:
  `2.220446049250313e-16`;
- evidence tree: `7` files, `26045` bytes,
  SHA-256 `db11acfe8a2c989352417aec6ae683f10e58323dde4306f926dab830b8fbf105`;
- protected formalization tree remains
  `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`;
- checkpoint-5176 tree remains
  `254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`.

No local-GR, galaxy, cosmology or full-MTS claim is made. No GitHub action
occurred.

## Historical handoff - checkpoint 5182 (partially superseded by 5183)

The checkpoint-5182 derivation below remains useful for its vertex and
projector calculation. Its all-`eta` screening conclusion and the
`eta=1/8`, `eta=1/6` response formulas are superseded by checkpoint 5183.

Checkpoint 5182 performs the parent-specific calculation left open at 5181:
the actual static Hilbert `h chi chi` pair vertex is projected through the
Newtonian-gauge scalar constraints rather than compared only by dimensional
normalization.

Use

```text
ds^2=-(1+2Phi)dt^2+(1-2Psi)delta_ij dx^i dx^j.
```

For the canonical static zero mode,

```text
N sqrt(gamma) gamma^ij
 =sqrt[(1+2Phi)(1-2Psi)] delta^ij
 ={1+(Phi-Psi)-1/2(Phi+Psi)^2+O(h^3)}delta^ij.
```

Therefore the minimal linear pair vertex is

```text
V_min=(Phi-Psi)[p.(p+k)]/2.
```

The quadratic seagull is proportional to
`-(Phi+Psi)^2(grad chi)^2/4`. It contains only a one-propagator tadpole:
scaleless at the critical point and analytic in external momentum when a
mass or state scale is present. It cannot change the nonanalytic pair term.

To audit the strongest local curvature improvement without importing an
incompatible source sign convention, define `eta` operationally by

```text
V_eta=eta k^2(Phi-2Psi)chi^2.
```

The result holds for every real `eta`, so translating a source coefficient
written with the opposite `R chi^2` sign cannot change the route decision.

Using

```text
B_0(k)=1/(8|k|),
I_MM/|k|^3=1/32,
k^2 I_M0/|k|^3=-1/16,
```

the exact connected critical-pair covariance is

```text
C_ab(k)=W|k|^3 w_a w_b/64,
w(eta)=(4eta-1,1-8eta),
Delta K_ab=-C_ab.
```

It is rank one and positive semidefinite before the passive cumulant sign:

```text
det C=0,
tr[C/(W|k|^3)]=(40eta^2-12eta+1)/32>0.
```

At the parent-owned value `eta=0`, `w=(-1,1)` is pure gravitational
slip. The scalar-slip coefficient is exactly 32 times the independent TT
coefficient from checkpoint 5150.

After analytic local renormalizations define

```text
a=2M_R^2 k^2>0,
d=W|k|^3/64>=0,

K_GR=a[[0,-1],[-1,1]],
K=K_GR-d w w^T.
```

The determinant is

```text
det K=-a Delta,
Delta=a-d(48eta^2-16eta+1).
```

The branch continuously connected to the Einstein scalar constraints has
`Delta>0`. Exact inversion for a dust source gives

```text
Phi/Phi_GR
 =1-16d eta^2/Delta,

Psi/Psi_GR
 =1+4d eta(4eta-1)/Delta,

(Phi+Psi)/(Phi+Psi)_GR
 =1-2d eta/Delta,

(Phi-Psi)/Phi_GR
 =-4d eta(8eta-1)/Delta.
```

This proves the decisive theorem

```text
Phi/Phi_GR<=1
```

for every positive scalar dressing of this derived pair projector on the
GR-connected branch. Equality requires `d=0` or `eta=0`. The checkpoint-5148
galaxy target instead requires an enhanced common response
`Phi/Phi_GR=1+A C_q>1`.

The two exact no-slip values are

```text
eta=0,
eta=1/8.
```

The first is exactly invisible to dust. The second is nontrivial but screens:

```text
Phi/Phi_GR=Psi/Psi_GR=4a/(4a+d)<1.
```

The operational pure-common value `eta=1/6` gives

```text
w=(-1/3,-1/3),
Phi/Phi_GR=(9a-d)/(9a+3d),
Psi/Psi_GR=(9a+d)/(9a+3d),
lensing/GR=3a/(3a+d).
```

It rotates the pair covariance into the common projector, but screens both
the circular potential and total lensing and generates slip. A zero of
`Delta` is loss of scalar-constraint rank, not the positive critical Schur
residual constructed abstractly at 5181.

Checkpoint 4951 proves that the exact shift-symmetric parent has no
`R chi^2` vertex, hence parent-owned `eta=0`. Allowing every real `eta`
already fails, so ownership cannot rescue this mechanism inside the audited
vertex class.

The gap question is also closed for this route:

```text
B_m(k)
 =atan(|k|/(2m))/(4pi|k|)
 =1/(8pi m)-k^2/(96pi m^3)+O(k^4),  |k|<<m.
```

A finite gap is analytic and cannot own the required infrared `1/|k|`
carrier. Exact gap collapse reaches `B_0`, whose constrained projector has
just been rejected. More gap work cannot rescue the passive zero-background
pair mechanism without a new parent vertex.

The resulting route boundary is:

```text
passive zero-background Hilbert pair dressing = rejected as the 5148 bridge;
local GR/Newton/Maxwell                       = retained unchanged;
direct conserved state stress from 5151      = survives conditionally;
nonzero background linear h-delta-chi mixing = selected next calculation.
```

Checkpoint 5183 must derive or reject a parent-owned stationary motion
background and its actual linear metric-motion Hessian block `B`. If no such
background exists, return to deriving the source-selected conserved
occupation for the checkpoint-5151 direct-state-stress route. Do not return
to gap tuning or the zero-background pair loop without a genuinely new
operator.

Validation and integrity:

- dry run passed `35/35`;
- full runner passed `43/43`;
- independent verifier passed a dense constrained-matrix scan;
- maximum direct-loop/outer-product residual:
  `8.881784197001252e-16`;
- maximum symbolic/numerical inverse residual:
  `2.4868995751603507e-12`;
- maximum sampled `Phi/Phi_GR-1`: `0.0`;
- finite-gap low-`k` log slope:
  `-1.6431300764452317e-11`;
- near-massless `B_m/B_0`: `0.9999999987267605`;
- evidence tree: `8` files, `39430` bytes,
  SHA-256 `43a8b6fc5f1196c96d2098b26ee12008fbb1abf206b0a42f5d89fd25a18d9a3e`;
- protected formalization tree remains
  `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`;
- checkpoint-5176 tree remains
  `254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`.

No local-GR, galaxy, cosmology or full-MTS claim is made. No GitHub action
occurred.

## Authoritative current handoff - checkpoint 5181

Checkpoint 5181 takes the only mechanism left open at 5180 and derives its
critical carrier rather than recording it as another missing input. In three
spatial dimensions the equal-mass static pair bubble is exactly

```text
B_m(k)
 = integral d^3q/(2pi)^3
   1/[(q^2+m^2)((q+k)^2+m^2)]

 = 1/(8pi) integral_0^1 dx
   [m^2+x(1-x)k^2]^-1/2

 = atan(|k|/(2m))/(4pi |k|).
```

Its critical and regular limits are

```text
B_0(k)=1/(8|k|),

B_m(k)
 =1/(8pi m)-k^2/(96pi m^3)+O(k^4),
 |k|<<m.
```

This closes the origin of checkpoint 5149's infrared nonanalytic power. The
checkpoint-5148 response factorizes identically:

```text
n_q(mu/k)=mu^q/(k^q+mu^q),

C_q(k^2)
 =mu^(1+q)/[|k|(|k|^q+mu^q)]
 =8mu n_q(mu/k) B_0(k).
```

The maximum independent Feynman-parameter error is
`1.3027012555245862e-15`; the maximum factorization error over 24 momentum
decades is `2.836128479528997e-16`.

The minimal full-crossover operator contract is consequently

```text
F_q(k)=sqrt[n_q(mu/k)],

C_q=8mu F_q^2 B_0,

d n_q/d ln k=-q n_q(1-n_q).
```

The massless pair owns the infrared power, but the parent still has to derive
this running external composite form factor inside the occupied loop.

Checkpoint 5181 also proves a new restriction. One ordinary massive pair has

```text
rho_Bm(t)=theta(t-4m^2)/(8pi sqrt(t)).
```

If the full `C_q` were a positive mixture of such bubbles, its cumulative
pair weight would be

```text
W(m)=16pi m rho_C(4m^2).
```

Writing `x=(2m/mu)^q` and `c=cos(pi q/2)` gives

```text
W(m)=8mu(1+c x)/(1+2c x+x^2),

dW/dm
 =-8mu q x(c+2x+c x^2)/
   [m(1+2c x+x^2)^2] <0.
```

It decreases from `8mu` to zero. Therefore the complete `q=0.77` crossover
cannot be obtained from a positive average of ordinary massive pair
thresholds. A parent-derived occupied-state kernel, running pair vertex or
equivalent composite dynamics is mandatory.

For the ordered derivative composite `O=(grad psi)^2`, contact subtraction
gives

```text
D_0,nonlocal
 =(k^4/4)B_0
 =|k|^3/32.
```

This is precisely the residual power required after critical cancellation:

```text
K_h=M_R^2 k^2,

K_eff~M_R^2 |k|^3/(A mu).
```

In this convention the parent constraint-dressed Hilbert projection must
return

```text
g_proj=32 M_R^2/(A mu)
```

with the stabilizing sign. Across the checkpoint-5148 corridor the
reduced-Planck benchmark is

```text
6.6379761156449585e81
 <= g_proj/eV <=
5.975728610780566e83.
```

Relative to one `mu`-normalized ordered pair this is an enhancement of
`2.4829218581865097e107` to `2.012210506360269e111`. This is a hard
normalization gate, not yet a strict exclusion, because the geometric-motion
field normalization and constraint projector have not been calculated.

A positive full scalar Hessian completion now exists explicitly. With
`u=sqrt(K_h)h`,

```text
H =
 [[1,       sqrt(A)],
  [sqrt(A), C_q^-1+A]].
```

Its quadratic form, determinant and Schur complement are

```text
(u+sqrt(A)chi)^2+C_q^-1 chi^2,

det H=C_q^-1>0,

K_eff
 =K_h-A K_h/(C_q^-1+A)
 =K_h/(1+A C_q),

zeta=A C_q/(1+A C_q).
```

The minimum sampled normalized eigenvalue is
`4.833011663096798e-7`. The measured infrared slopes are

```text
1-zeta : 1.0000358754968344,
K_eff  : 3.0000358754968346.
```

The checkpoint-5149 positive Stieltjes density gives a causal generalized
oscillator continuum. Dressing preserves passivity exactly:

```text
Im[C_R/(1+A C_R)]
 =Im(C_R)/|1+A C_R|^2 >=0.
```

The numerical identity residual is `2.220446049250313e-16`. This proves
static scalar positivity and retarded passivity compatibility; it does not
replace the full constrained scalar/vector/tensor Hessian.

The finite-local obstruction is now a theorem:

1. a finite regular local Hessian is analytic in `s=k^2`;
2. a gapped eliminated block has an analytic inverse and Schur complement;
3. a finite number of local massless fields gives a rational/Laurent
   function with integer powers of `s`;
4. neither class can generate the branch point `s^(1/2)=|k|`.

A gapless continuum, infinite threshold accumulation, critical state or
explicitly nonlocal parent is therefore necessary.

The exact finite-gap suppression is

```text
B_m/B_0=(2/pi)atan(k/(2m)).
```

Retaining 90 or 99 percent of the critical bubble requires

```text
m/k <=0.07919222016226816  (90 percent),
m/k <=0.007854627661832444 (99 percent).
```

At the largest fitted `L_eff=62.908458962933175 kpc`,

```text
m_eff <=7.984587435411873e-31 eV
```

is required for the 99-percent corridor. The current `1e-20 eV` benchmark is
larger by `12524128617.6537` and retains only
`3.235765242114026e-9` to `2.9129443369788347e-7` of the massless bubble
across the fitted scale range. Checkpoint 5180 already proves that controlled
`X2-X3` interactions do not collapse this gap.

The current parent match is:

```text
minimal motion kinetic pair carrier             = parent owned;
connected Hilbert stress-pair entry form         = parent owned;
massless pair 1/|k| and derivative |k|^3 powers  = derived;
positive static/causal scalar completion         = proved compatible;
full n_q running composite vertex                = open;
q, mu and A                                      = not parent derived;
environmental gap collapse                       = open;
B^2=A K_h cross-block normalization              = open;
unit local-stiffness cancellation                 = open;
constraint-dressed tensor/seagull sign            = open.
```

Conditional on a Lorentz-invariant generalized-field continuation, the
required scaling is

```text
eta_IR=1,
Delta_IR=3/2,
eta_UV=1-q=0.23,
Delta_UV=1.115.
```

The current elementary motion scalar instead has

```text
eta_psi,UV=-0.06532510306084385,
eta_psi,IR=-4.2441318203201676e-11.
```

That rejects an elementary-`psi` identification, not the reflection-even
pair channel: the bilocal/composite Bethe-Salpeter eigenproblem has not yet
been solved. Likewise, `q=0.77` is not the current sole GR-connected relevant
exponent `1.8926421323602347`.

The exact contact-subtracted equal-time tails are

```text
C_q(r)~mu/(2pi^2 r^2),

1-zeta(r)~-1/(A mu pi^2 r^4),

D_0(r)~3/(8pi^2 r^6).
```

The checkpoint passes `49/49` generator validations. An independent verifier
recomputed the loop, factorization, Schur identity and pair-weight sign;
parsed all emitted tables; checked all `15` source hashes; and passed. The
checkpoint-5181 evidence tree contains `8` files and `41709` bytes with
digest

```text
60e1906071baf7913f71b20ee5ff1d2b4d8dba319a89479ea429ba8eea44b811.
```

The protected locks remain

```text
formalization-workbench:
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758

checkpoint 5176:
254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b.
```

No local-GR, Newton, Maxwell, PPN, galaxy, cosmology or full-MTS claim is
promoted. No public repository action belongs to checkpoint 5181.

The next target is checkpoint 5182:

```text
derive the constraint-dressed Hilbert stress-to-bilocal pair vertex from the
existing parent 2PI Hessian, including contact and seagull terms; calculate
the scalar projector sign and normalization; test against
g_proj=32 M_R^2/(A mu); then derive or reject the environment-dependent
critical-gap and logistic composite flow.
```

This is now the narrowest derivation that can decide whether the critical-pair
mechanism is parent physics or merely a mathematically admissible closure.

## Previous handoff - checkpoint 5180

Checkpoint 5180 performs the interacting spectral calculation selected at
5179. It does not introduce another unspecified state coefficient. The
trajectory-normalized `X2-X3` CTP kernel is explicit, the collisionless
response is subtracted algebraically, and the remaining kernel is tested
against checkpoint 5149's non-negotiable infrared condition

```text
1-zeta(k) proportional |k|.
```

For

```text
L_int=(c_ess/4)(partial psi.partial psi)^2
     +(e_ess/8)(partial psi.partial psi)^3,
```

the symmetric derivative vertices are

```text
V4=2 c_ess sum_(3 pairings)(p_i.p_j)(p_k.p_l),

V6=6 e_ess sum_(15 pairings)
          (p_i.p_j)(p_k.p_l)(p_m.p_n).
```

The factors are exact:

```text
2^2 2! (c_ess/4)=2c_ess,
2^3 3! (e_ess/8)=6e_ess.
```

The 2PI hierarchy through its first nonlocal terms is

```text
Gamma2_X2,H=(1/8) integral_C V4 G G,
Gamma2_X2,B=(1/48) integral_C V4(x) G(x,y)^4 V4(y),

Gamma2_X3,H=(1/48) integral_C V6 G G G,
Gamma2_X3,B=(1/1440) integral_C V6(x) G(x,y)^6 V6(y).
```

Opening a line gives exact self-energy factors `1/6` and `1/120`.
Decomposing `G` into statistical and spectral parts gives

```text
Sigma_F,4
 =-(V4 V4/6)[F^3-(3/4)F rho^2],

Sigma_rho,4
 =-(V4 V4/6)[3 rho F^2-(1/4)rho^3],

Sigma_F,6
 =-(V6 V6/120)
   [F^5-(5/2)F^3 rho^2+(5/16)F rho^4],

Sigma_rho,6
 =-(V6 V6/120)
   [5 rho F^4-(5/2)rho^3 F^2+(1/16)rho^5],

Sigma_R=theta(x0-y0) Sigma_rho.
```

These coefficients are generated exactly from the two CTP branches
`(F-i rho/2)^n` and `(F+i rho/2)^n`. The full momentum form retains the
derivative vertices and all distinct `F/rho` placements. The first `X3`
four-leg contribution remains the local contraction

```text
V4_bar=V4+(1/2)Tr_G V6+...,
```

with `choose(6,2)4!/6!=1/2`. The mixed `c_ess e_ess` basketball is contained
in `V4_bar^2`; the first direct nonlocal `X3` self-energy has five internal
lines.

The vacuum `X2` and `X3` cuts begin at `3m_gap` and `5m_gap`. An occupied
medium can have low-frequency scattering cuts, but their collisionless part
is not new. With

```text
R0=[-i omega+L_Vlasov]^-1,
RC=[-i omega+L_Vlasov+C22]^-1,
```

the exact new remainder is

```text
RC-R0=-RC C22 R0.
```

A rational finite-kernel audit verifies this identity with exact zero
residual. It also verifies `C22 1=0` exactly. The continuum checkpoint-4953
invariants remain

```text
integral dPi C22=0,
integral dPi p^nu C22=0.
```

Bose detailed balance was checked independently with exact zero energy,
particle-number and exponent residuals. Collisions damp nonconserved
distortions and produce a finite-frequency width. They cannot manufacture
missing static source stress or select a new equilibrium state. The
checkpoint-5171 UGC09133 static Vlasov eigenvalue remains
`0.5522232579424047`, so that fixed radial state has no static Vlasov pole.

The key new result is an exact shift-Ward/infrared theorem. Since every field
in `X2` and `X3` is differentiated,

```text
V4(0,p2,p3,p4)=0,
V6(0,p2,...,p6)=0.
```

Therefore every two-point graph built from these interactions has

```text
Sigma_X2-X3(p)=p_mu p_nu Pi^mu_nu(p).
```

For a regular occupied state with exponential connected clustering,

```text
|C_TT(r)|<=C0 exp(-r/xi),
```

all Fourier moments exist. Reflection and rotational symmetry then give

```text
chi(k)=chi0+chi2 k^2+chi4 k^4+... .
```

The exact benchmark

```text
C(r)=C0 exp(-r/xi)
```

has

```text
chi(k)=8 pi C0 xi^3/(1+k^2 xi^2)^2
      =chi0[1-2(k xi)^2+3(k xi)^4-...].
```

The executed low-`k` departure slope is `1.9999832907953505`, converging to
the analytic value `2`; checkpoint 5149 requires `1`. Even an exact local
coefficient cancellation leaves `k^4`, not `|k|`. Thus a regular clustering
`X2-X3` state can renormalize kinetic coefficients but cannot additively erase
a gap or generate the required determinant nonanalyticity.

The surviving state target is now precise rather than verbal. In three
spatial dimensions:

```text
determinant correction |k|
 <-> equal-time r^-4 kernel after contact subtraction;

susceptibility C_q~mu/|k|
 <-> equal-time r^-2 tail.
```

A future state must derive these power laws, not merely provide a large local
coefficient.

The quantitative interaction bound was recomputed for every one of the `173`
positive-target SPARC rows. The dynamic-`N=8` trajectory gives

```text
c_ess=-7.287811982461907e-111 eV^-4,
r3=e_ess/(2 c_ess^2)=12474921.033335365.
```

The extrema are

```text
max |c_ess|rho
 =2.558501308462119e-115;

minimum local enhancement needed for the locked fraction
 =3.9942868661138966e114;

max |e_ess rho^2|/|c_ess rho|
 =2 r3 |c_ess rho|
 =6.383420357350028e-108.
```

For a narrow high-occupancy shell,

```text
sigma22=7 c_ess^2 E^6/(5 pi),
rho~f E^4,
Gamma22/E~[7/(5 pi)](c_ess rho)^2.
```

Granting the much larger microscopic rate `E=m` and replacing the exact
finite angular factor `7/(5pi)=0.44563384065730693` by a unit-prefactor
comparator gives

```text
max Gamma_coll/omega_profile
 =7.267645087104551e-224.
```

Closing the locked deficit would require

```text
C_coll>=1.4061484911334452e223.
```

That is not a finite perturbative phase-space coefficient. If correlations
make it effectively divergent, the state has left the controlled
quasiparticle branch and entered the critical route identified above.

The checkpoint decision is:

```text
first nonlocal X2 retarded kernel                 = derived;
first direct nonlocal X3 retarded kernel          = derived;
CTP F/rho coefficients                            = derived exactly;
collisionless Vlasov response                     = subtracted exactly;
collision number and four-momentum zero modes     = retained exactly;
regular clustering X2-X3 gap closure              = rejected;
regular clustering |k| determinant                = rejected;
controlled collision/static repair                = rejected quantitatively;
parent-derived critical occupied state             = open, not claimed;
local GR/Newton/Maxwell branch                     = unchanged;
galaxy bridge or full MTS                          = not claimed.
```

Route decision:
`THE_TRAJECTORY_NORMALIZED_X2_X3_CTP_KERNEL_HAS_NOW_BEEN_WRITTEN_EXPLICITLY_THE_X2_BASKETBALL_AND_X3_FIVE_LINE_GRAPHS_ARE_THE_FIRST_NONLOCAL_SELF_ENERGIES_AND_THEIR_STATISTICAL_SPECTRAL_POLYNOMIALS_ARE_FIXED_BY_CTP_COMBINATORICS_AFTER_SUBTRACTING_THE_ALREADY_COUNTED_VLASOV_RESOLVENT_THE_REMAINING_COLLISION_OPERATOR_ANNIHILATES_NUMBER_AND_MOMENTUM_MODES_AND_IS_PARAMETRICALLY_TOO_SMALL_MORE_STRONGLY_SHIFT_SYMMETRY_FORCES_AN_EXTERNAL_MOMENTUM_ON_EACH_SELF_ENERGY_LEG_SO_ANY_REGULAR_EXPONENTIALLY_CLUSTERING_OCCUPIED_STATE_PRODUCES_ONLY_AN_ANALYTIC_K_SQUARED_SERIES_AND_CANNOT_ERASE_A_GAP_OR_GENERATE_THE_REQUIRED_ABSOLUTE_K_DETERMINANT_THE_PERTURBATIVE_INTERACTION_REPAIR_IS_THEREFORE_CLOSED_WHILE_A_PARENT_DERIVED_CRITICAL_STATE_WITH_THE_REQUIRED_POWER_LAW_TAIL_REMAINS_OPEN_AND_NOT_CLAIMED`.

The exact next calculation is checkpoint 5181. Do not run another weak loop,
fit a boundary coefficient, add a second source coupling or reuse the Vlasov
response. Construct the smallest positive parent-derived critical occupied
state allowed by the complete even boundary hierarchy. Calculate its
equal-time and retarded stress kernels and test:

1. the `r^-4` determinant-tail and `r^-2` susceptibility coefficients;
2. the checkpoint-5149 unit-mixing normalization;
3. the full metric-motion spectral and gradient eigenvalues;
4. formation from the parent without an inserted occupation law.

If no positive state can satisfy these simultaneously, the galaxy bridge
cannot come from the present single shift-symmetric motion-scalar
realization.

Artifacts:

- `5180-Y5-R2FR-interacting-retarded-2PI-kernel-Vlasov-subtraction-and-infrared-gap-closure-gate.md`;
- `scripts/Y5_R2FR_5180_interacting_retarded_2PI_Vlasov_subtraction_and_gap_closure_gate.py`;
- `source-intake/functional_rg/5180/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5180_VALIDATION.csv`.

The strict dry-run, full run, Python compilation and independent verifier
pass. All `36/36` validations and `17/17` read-only provenance hashes pass.
The 5180 evidence tree contains `7` files, totals `110780` bytes and has
digest
`da086fe81ef70f151cb9de2ead48257c6c79614f33efdf578604c0603fdd17be`.
The immutable checkpoint-5176 tree remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`;
the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No project cache remains, the public worktree is clean and no GitHub action
occurred.

## Historical handoff - checkpoint 5179

Checkpoint 5179 carries out checkpoint 5178's non-Gaussian calculation rather
than introducing another unspecified state coefficient. For a general initial
CTP density matrix,

```text
<phi_+|rho|phi_->=exp(i F[phi]),
F=sum_(n>=0) alpha_n phi^n/n!.
```

Every `alpha_n` is supported on the initial surface and Hermiticity requires

```text
i alpha_n^(a_1...a_n)
 =[i alpha_n^(-a_1...-a_n)]*.
```

The selected parent and state are reflection even. Hence all odd kernels
vanish, `alpha_2` is the independent Gaussian covariance proved nonunique at
5156, and the first non-Gaussian datum is exactly

```text
F_4=(1/4!) integral_(Sigma_0^4) alpha_4 psi^4.
```

The functional form of `alpha_4` is now derived from the bulk parent. On flat
FLRW,

```text
S_X2
 =(c_ess/4) integral d_eta d3x
   [-(psi')^2+(grad psi)^2]^2,
```

because the `a^4` measure cancels the two inverse metrics. Its symmetric
vertex is

```text
V_X2=2c_ess sum_pairings(p_i.p_j)(p_k.p_l),
```

which exactly reproduces

```text
M_22=(c_ess/2)(s^2+t^2+u^2).
```

For any specified Gaussian preparation history,

```text
C4_c(eta_0)
 =i integral_(eta_i)^eta_0 d_eta
   <[H_X2,I(eta),psi_1 psi_2 psi_3 psi_4(eta_0)]>_G
  +O(c_ess^2),
```

and integrating the preparation contour into its endpoint gives

```text
alpha_4,X2(z_i)
 =-i integral_P d4v
   V_X2[nabla Delta_P(v,z_1),...,nabla Delta_P(v,z_4)]
  +O(c_ess^2).
```

This is the derivative-interaction extension of the source-signed
Garny--Muller initial-correlation construction. It derives the kernel but also
proves what remains state data: the parent has not selected `P`, `eta_i`,
temperature or the initial Gaussian density matrix.

The canonical massless Euclidean half-space can be completed explicitly:

```text
A_4,E(k_i)
 =[2c_ess/k_t]
  sum_pairings
   [k_i k_j-k_i_vec.k_j_vec]
   [k_k k_l-k_k_vec.k_l_vec].
```

For a regular momentum tetrahedron,

```text
A_4,E=(8/3)c_ess k^3.
```

That is interacting-vacuum wavefunctional dressing, not galaxy occupation.
The dynamic-`N=8` trajectory gives

```text
c_ess=-7.287811982461907e-111 eV^-4,
```

so its standalone Euclidean quartic has the destabilizing sign. This does not
reject the functional `P(X)` trajectory; it proves that its higher even tower
or a UV completion is mandatory for a global positive preparation.

`X3` supplies no independent leading four-point shape. Contracting two of six
legs gives

```text
delta V_4,X3=(1/2)Tr_G V_6,X3,
```

where `C(6,2)4!/6!=1/2`; this is a local tadpole renormalization. Two `X2`
preparation vertices generate `alpha_6=O(c_ess^2)`. A strong state therefore
cannot consistently stop at `alpha_4`.

An exact positivity test closes the simplest amplitude escape. For

```text
p_lambda(q)
 proportional exp[-q^2/(2C)-lambda q^4/(24C^2)],
```

the enumerated Wick contractions give

```text
<q^2>/C=1-lambda/2+O(lambda^2),
kappa_4/C^2=-lambda+O(lambda^2).
```

The exact pairing counts are `15`, `105`, `12` and `24`. More strongly,

```text
d<q^2>/d lambda=-Cov(q^2,q^4)/(24C^2)<0,
2Cov(Y,Y^2)=E[(Y-Y')^2(Y+Y')]>=0, Y=q^2.
```

Every normalizable positive quartic damping suppresses the covariance. The
minimum locked transition correction `1.021938817332546` would require

```text
lambda=-2.043877634665092,
```

which is both nonperturbative and nonnormalizable as a quartic-only diagonal
weight. A general unitary quantum state can evade the diagonal theorem, but
then its full preparation history and even hierarchy must be constructed.

The post-4951 parent is interacting, so the old displayed
`Gamma_2^scalar=0` is not reused outside its quadratic scope. The weak `X2`
2PI hierarchy begins with

```text
Gamma_2,double-bubble proportional (1/8) integral_C V4 G G,
Gamma_2,basketball   proportional (1/48) integral_C V4 G^4 V4.
```

The first term is local Hartree order `c_ess`; the first nonlocal self-energy
is order `c_ess^2`. The initial kernel enters the statistical propagator
through the sourced surface term

```text
S_alpha
 =Pi_(lambda alpha),F F(eta_0,eta')
  +(1/4)Pi_(lambda alpha),rho rho(eta_0,eta').
```

At late times,

```text
delta T_mn^(2)=D_mn^(2) delta F,
delta T_mn^X2=c_ess D_mn^(4)[G G+C4_c].
```

Thus a bulk-induced connected four-point contributes at `O(c_ess^2)`.
Vacuum preparation remains in the vacuum sector; arbitrary covariance
retuning remains state data; the leading occupied Wigner response remains the
already-evolved Vlasov term and cannot be added again.

The quantitative stress gate is now explicit. Define

```text
|Delta T_X2|=|c_ess|rho^2 K_T.
```

Then `K_T=f/(|c_ess|rho)` identically. Using the deliberately generous
`Mbar_Pl^-4` coefficient, even the densest of all `173` positive-target
checkpoint-4953 rows requires

```text
K_T>=1.0233690404038258e114.
```

For `UGC09133`,

```text
K_T,generous  =1.7961810156526596e117,
K_T,trajectory=7.010630531829909e117.
```

The independent formation calculation remains decisive:

```text
maximum finite-preparation probability =3.1256442447836532e-58;
maximum generous controlled log gain   =0.038692310770790016;
minimum required log multiplicity      =14.911693718845843;
minimum completed six-point kernel     =1.281894157582452e-61;
controlled high-frequency failures     =692/692.
```

The weak gapped vacuum cut also cannot make the checkpoint-5149 critical
nonanalyticity. At the reference transition,

```text
hbar c/R_n=1.7549606539036143e-28 eV,
(hbar c/R_n)/m_gap=1.7549606539036146e-8.
```

It lies far below the three-particle threshold. A finite-density low-frequency
cut can exist, but its leading collisionless response is precisely the
subtracted Vlasov term; weak collision corrections remain inside the rejected
4954--4959 envelope.

Planck 2018 source files are now local and hashed. Its trispectrum constraints
are recorded:

```text
g_NL^local          =(-5.8 +/- 6.5)e4;
g_NL^dot-pi^4       =(-0.8 +/- 1.9)e6;
g_NL^(partial pi)^4 =(-3.9 +/- 3.9)e5.
```

They are not falsely applied directly to a hidden motion `alpha_4`. A numeric
MTS test first requires

```text
T_zeta^MTS
 =product_i T_(zeta X)(k_i) C4_X,c
  +metric-constraint terms
```

and a sourced Planck-template overlap. The parent does not yet derive that
transfer. Checkpoint 5156 remains an empirical Gaussian nonclaim baseline.

The checkpoint decision is:

```text
lowest reflection-even non-Gaussian kernel       = alpha_4, derived;
covariant X2 preparation functional form         = derived;
explicit Euclidean vacuum alpha_4                = derived;
X3 independent lowest four-point source          = rejected;
standalone positive diagonal quartic repair      = rejected exactly;
adiabatic-vacuum alpha_4 as galaxy occupation    = rejected;
controlled weak X2-X3 prepared stress            = rejected quantitatively;
direct Planck g_NL bound on hidden alpha_4        = forbidden without transfer;
strong full even hierarchy                       = open, not claimed;
gapless occupied continuum                       = open, not claimed;
local GR/Newton/Maxwell branch                    = unchanged.
```

Route decision:
`THE_LOWEST_REFLECTION_EVEN_NON_GAUSSIAN_STATE_VERTEX_IS_THE_SURFACE_SUPPORTED_ALPHA4_AND_A_COVARIANT_PREPARATION_CONTOUR_DERIVES_ITS_LEADING_X2_KERNEL_BUT_NOT_A_FREE_GALAXY_STRESS_THE_STANDALONE_POSITIVE_DIAGONAL_QUARTIC_STATE_CAN_ONLY_SUPPRESS_VARIANCE_THE_BULK_INDUCED_WEAK_KERNEL_IS_VACUUM_LOCAL_OR_ORDER_CESS_SQUARED_AFTER_VLASOV_SUBTRACTION_AND_THE_EXISTING_CONTROLLED_FORMATION_BOUNDS_ARE_FAR_TOO_SMALL_SO_AN_ORDER_ONE_REPAIR_REQUIRES_A_PARENT_DERIVED_STRONG_FULL_EVEN_BOUNDARY_HIERARCHY_OR_GAPLESS_OCCUPIED_CONTINUUM_AND_CANNOT_BE_CLAIMED_FROM_ALPHA4_ALONE`.

The exact next calculation is checkpoint 5180. Construct the
trajectory-normalized `X2-X3` retarded 2PI spectral kernel on an occupied
branch, isolate and subtract its Vlasov limit analytically, and test whether
the remaining spectral density can remove the infrared gap or generate
`1-zeta proportional |k|`. Do not rerun weak finite-time cascades, fit an
`alpha_4`, add another `G_N`, or reopen `O4`. If the residual kernel remains
gapped and perturbative, close this interaction/state repair and leave a
strong boundary hierarchy as an explicit cosmogenesis postulate.

Artifacts:

- `5179-Y5-R2FR-lowest-reflection-even-CTP-boundary-kernel-FLRW-preparation-and-perturbative-extra-stress-no-go.md`;
- `scripts/Y5_R2FR_5179_lowest_even_CTP_boundary_kernel_and_perturbative_state_preparation_no_go.py`;
- `source-intake/functional_rg/5179/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5179_VALIDATION.csv`.

The strict dry-run, full run, Python compilation and independent verifier
pass. All `35/35` generated validations and `22/22` read-only provenance
hashes pass. The 5179 evidence tree contains `252` files, totals `17333795`
bytes and has digest
`e7dd43280c937d485b20dfde99470b2d90bd7214676dcf42f3a3fc420715f76c`.
The immutable checkpoint-5176 tree remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`;
the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No project cache remains, the public worktree is clean and no GitHub action
occurred.

## Historical handoff - checkpoint 5178

Checkpoint 5178 performs the parent-Hessian calculation requested by
checkpoint 5177 rather than recording another missing operator. For the
renormalized CTP-2PI functional at zero motion one-point,

```text
Gamma[g,G]
 =S_g+(i/2)Tr ln G^-1+(i/2)Tr(D^-1[g]G-1)
  +Gamma_2[g,G]+Gamma_ct+Gamma_rho0,

Gamma_,G[g,G_star[g]]=0.
```

Writing

```text
A=Gamma_gg,
B=Gamma_gG,
C=Gamma_GG,
```

stationarity gives the exact implicit response and reduced Hessian

```text
dG_star/dg=-C^-1 B_dagger,
Gammabar_gg=A-B C^-1 B_dagger.
```

This is the exact connected stress-response Schur complement. Twelve
independent rational-arithmetic block systems verify with zero residual:

```text
Schur identity;
full versus reduced source response;
quadratic completion;
gauge-fixed determinant factorization;
one full Hessian gauge null direction.
```

The full on-shell Ward system

```text
[[A,B],[B_dagger,C]] (R_g,R_G)^T=0
```

implies

```text
R_G=-C^-1 B_dagger R_g,
(A-B C^-1 B_dagger)R_g=0.
```

Thus diffeomorphism conservation descends through the same physical inverse
used in the response. The theorem is stated only on the complete background
equations; away from them the standard contact/EOM terms are retained.

The scientific correction is that the whole Schur term is not an independent
new galaxy stress. In the checkpoint-4949 displayed quadratic truncation,

```text
Gamma_2=0,
C_0=(i/2)G^-1 tensor_s G^-1,
B_0=(i/2)delta D^-1/delta g + contacts.
```

Its occupied-state leading Wigner projection is the collisionless Vlasov
response. Checkpoints 5164-5169 already evolved that response nonlinearly and
checkpoint 5171 constructed its Frechet kernel. Adding it to the scored
profile again is therefore forbidden double counting.

The complete subtraction is now explicit:

```text
vacuum local determinant terms
 -> already matched into Lambda, M_R^2, a_R, a_C and Gamma_higher;

finite nonlocal vacuum terms
 -> calculable quantum corrections, not adjustable occupation;

Gaussian occupied classical response
 -> already evolved Vlasov response;

Maxwell/Poynting stress
 -> already part of the universal Hilbert source and assembly history;

Gaussian wave gradients and O4
 -> genuinely distinct but quantitatively bounded;

Gamma_rho0 or nonzero strong Gamma_2
 -> genuinely uncounted route.
```

For the locked `UGC09133`, `m_gap=1e-20 eV` reference,

```text
R_n=36.43917542575495 kpc;
v_infinity=225.72789767279875 km/s;
|u_O4/Z|=2.265012477923484e-139 m^4.
```

The spherical curvature envelope gives

```text
|Delta Z_O4/Z|
 =96 |u_O4/Z| (v/c)^4/R_n^4
 =4.372437627335837e-234.
```

The twelve locked MTS profiles require at least
`1.021938817332546` additional fractional `V^2` at the transition, so the
fixed `O4` coefficient would need an impossible controlled enhancement of
`2.3372290343115127e233`.

The selected wave/Wigner expansion gives

```text
epsilon_Rn^2=1.0865149241629725e-9;
max_observed (epsilon_Rn/x)^2=1.4088761625565654e-5.
```

Even the largest observed proxy needs a coefficient
`72535.74476539672` to equal the minimum transition deficit. This rejects an
order-one repair within the controlled reference expansion, while not
claiming a theorem against every nonperturbative wave core.

The exact criticality result is also sharper. Checkpoint 5149 requires

```text
1-zeta(k) proportional |k|
```

in the infrared. A regular local gapped Gaussian Hessian has analytic
`A(k^2)`, `B(k^2)` and `C(k^2)^-1` whenever `det C(0)` is nonzero. Its Schur
complement is therefore analytic in `k^2` and cannot produce `|k|`. A zero
mode, continuum threshold, occupied critical state or non-Gaussian kernel is
mandatory.

The existing interaction hierarchy supplies no hidden easy source:

```text
X2 2<->2 number invariant                    = exact;
X2 2<->2 stress invariant                    = exact;
stationary Bose collision source             = zero by detailed balance;
controlled six-point minimum kernel          = 1.281894157582452e-61;
controlled formation route                   = rejected at 4954-4959;
strong nonquasiparticle X2-X3 CTP kernel      = open;
Gaussian covariance selected by Hessian      = rejected at 5156.
```

Checkpoint 5177's no-retuning theorem remains intact, but its surviving route
is narrowed. No second `G_N`, additive Vlasov replay, fitted `O4` or relabelled
Poynting stress may repair the profile. The only uncounted route is a
parent-derived non-Gaussian initial-boundary functional, strong interacting
`Gamma_2`, or derived occupied critical continuum. The checkpoint-4960
local GR/Newton/Maxwell branch remains unchanged.

Route decision:
`THE_STATIONARY_2PI_REDUCTION_GIVES_AN_EXACT_ON_SHELL_TRANSVERSE_SCHUR_COMPLEMENT_BUT_AFTER_VACUUM_MATCHING_AND_THE_ALREADY_EVOLVED_VLASOV_RESPONSE_ARE_SUBTRACTED_THE_CURRENT_GAPPED_GAUSSIAN_HESSIAN_SUPPLIES_NO_INDEPENDENT_ORDER_ONE_GALAXY_STRESS_THE_O4_AND_CONTROLLED_WAVE_RESIDUALS_ARE_TOO_SMALL_AND_ONLY_A_PARENT_DERIVED_NON_GAUSSIAN_INITIAL_OR_STRONG_INTERACTING_CTP_KERNEL_CAN_REOPEN_THE_ROUTE`.

The exact next calculation is checkpoint 5179: derive the lowest
reflection-even non-Gaussian CTP state-preparation kernel rather than
postulating it. Use the checkpoint-5156 empirical adiabatic Gaussian
covariance only as a declared nonclaim baseline, evolve the first connected
four-point function generated by the checkpoint-4953/4959 `X2-X3` bulk
vertices on FLRW, contract it into the checkpoint-5178 stress kernel, and
enforce positivity, Ward conservation and CMB covariance/trispectrum bounds.
Do not reopen the Gaussian/Vlasov, constant-coupling or `O4` routes. If the
controlled induced kernel vanishes or is parametrically incapable, close the
perturbative extra-stress repair and leave any strong initial state as an
explicit boundary postulate rather than calling it derived.

Artifacts:

- `5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md`;
- `scripts/Y5_R2FR_5178_2PI_Schur_Ward_Vlasov_subtraction_and_Gaussian_residual_no_go.py`;
- `source-intake/functional_rg/5178/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5178_VALIDATION.csv`.

The strict dry-run, full run, Python compilation and independent verifier
pass. All `29/29` generated validations, `12/12` exact Schur/Ward trials and
`36/36` provenance hashes pass. The eight-file 5178 evidence tree totals
`50505` bytes and has digest
`abbe170591aa64127a8bcec03df814ea995693bdb6a7f3b8182f9e2e01ca800d`.
The immutable checkpoint-5176 tree remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`;
the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No project cache remains, the public worktree is clean and no GitHub action
occurred.

## Authoritative current handoff - checkpoint 5177

Checkpoint 5177 turns checkpoint 5176's final metric split into an exact
profile-level result without rerunning a trajectory, changing a score or
retuning either model. It reconstructs all 24 MTS/CDM profiles from the twelve
frozen phase and evolution caches and reproduces every recorded q and RMSE
with maximum errors `0` and `0`.

The two locked estimands measure different things. The q statistic is the
five-point local logarithmic slope

```text
q[V^2] = 2 d ln(V^2)/d ln R
```

on the exact stencil
`[33.689357475553784, 42.522489842557555] kpc` around
`R_tr=36.43917542575495 kpc`. RMSE uses 42 scored radii and contains both
multiplicative amplitude and centered-shape error. Checkpoint 5176's immutable
confirmatory result remains

```text
mean D_q = -0.0392272547258426;
bootstrap95 D_q = [-0.06256573517896083,
                    -0.01672942342481484];
exact sign-flip p(D_q) = 0.01171875;

mean D_RMSE = +0.0006039774233205624 dex;
bootstrap95 D_RMSE = [-0.0012737960786308275,
                       +0.002521414183604568] dex;
exact sign-flip p(D_RMSE) = 0.560546875;
MTS joint wins = 3;
CDM joint wins = 0;
joint sign p = 0.25.
```

The locked overall verdict therefore remains
`STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE`.

Checkpoint 5177 derives the exact constant-normalization identities

```text
e_i(A)=e_i+log10(A);
q[A V^2]=q[V^2];
A_best=10^(-mean e);
min_A RMSE^2=Var(e).
```

All 24 reconstructed profiles verify q invariance to maximum numerical error
`5.81756864903582e-14`. The twelve-seed paired mean MSE difference decomposes
without residual:

```text
Delta MSE(MTS-CDM)       = +0.00029622652052732683 dex^2;
Delta amplitude bias^2   = +0.00019599784333573038 dex^2;
Delta centered variance  = +0.00010022867719160092 dex^2.
```

Amplitude bias supplies `0.6616485350022859` of the mean difference and
centered shape supplies `0.33835146499772917`. After granting each profile its
own prohibited post-hoc best normalization, the mean centered-shape RMSE is
still `0.11944836417592654 dex` for MTS versus
`0.11899649748138023 dex` for CDM. Thus the q result is a reproducible local
transition-slope effect; it is not yet a global amplitude or shape solution.

The radial MSE identity gives

```text
inner-of-q-stencil contribution = +0.0001483585718298592;
q-stencil contribution          = +0.00013516699608762489;
outer contribution              = +0.000012700952609843115;
sum                             = +0.00029622652052732683 dex^2.
```

The completed ensemble also supplies a strict constant-coupling no-go. Across
all 24 profiles, matching the transition requires

```text
A_transition in [1.996571072859183, 2.4329313339375127],
```

whereas matching the edge requires

```text
A_edge in [0.8319960735500093, 0.8433622899779304].
```

The ranges are disjoint. Even the exact log-minimax compromise
`A=1/sqrt(T E)` leaves an unavoidable multiplicative mismatch in
`[1.545843908012368, 1.7025847793359408]`. A universal amplitude therefore
cannot match both anchors and cannot change q in the first place.

This matters for the full theory route. Checkpoint 4960 already fixes one
universal `G_N=1/(8 pi M_R^2)` across Einstein, Poisson, Newton, lensing and
matter-source residues and forbids arena retuning. Checkpoint 5170 rejected a
constant multiplier for the earlier formation state. The stochastic
checkpoint-5176 ensemble now confirms that no galaxy-only coupling
normalization may be used to manufacture a win. The calibrated local
GR/Newton/Maxwell branch remains untouched.

The surviving mechanism must be nonmultiplicative and parent-derived: a
conserved, compensated, scale-dependent occupied-state or motion-sector stress
that changes radial structure while remaining silent locally. The classical
Vlasov density response rejected at checkpoint 5171 may not be added again.
That operator has not yet been derived.

Route decision:
`THE_LOCKED_MTS_Q_ADVANTAGE_IS_A_LOCAL_TRANSITION_SLOPE_EFFECT_WHILE_GLOBAL_AMPLITUDE_AND_CENTERED_SHAPE_REMAIN_UNRESOLVED_AND_NO_CONSTANT_SOURCE_NORMALIZATION_CAN_MATCH_TRANSITION_AND_EDGE_OR_REPLACE_THE_CALIBRATED_GN_RETURN_TO_A_PARENT_DERIVED_NONMULTIPLICATIVE_CONSERVED_STATE_STRESS_BEFORE_A_NEW_PREREGISTERED_GATE`.

The next calculation must return to the parent motion-sector Hessian/current
and derive or reject the nonmultiplicative occupied-state stress under
conservation, compensation and local-vacuum-silence constraints. Only a
derived operator may be propagated into a separately preregistered
cross-galaxy gate; no parameter may be fitted to the UGC09133 residual.
The exact entry point is checkpoint 4935's renormalized
`Gamma_psi,k^(2)=Z_psi,k[-Box_g+m_psi,k^2]+...` and unique `O4` Hessian
portal, joined to checkpoint 4960's universal Hilbert source. Do not reopen
the divergent bare fractional-potential vacuum Hessian, and explicitly
subtract the classical Vlasov density response already evolved in
checkpoints 5164 through 5171.

Artifacts:

- `5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-theorem.md`;
- `scripts/Y5_R2FR_5177_locked_ensemble_metric_split_and_no_retuning_theorem.py`;
- `source-intake/functional_rg/5177/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5177_VALIDATION.csv`.

The script dry-run and full run pass. Independent validation confirms `22/22`
generated checks, `18/18` provenance hashes, `12/12` bias-variance and radial
identities, and the no-go for all `24/24` profiles. The 5176 tree remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`;
the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
The nine checkpoint-5177 output files total `833078` bytes. No project cache
remains, no public worktree changed and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5176

Checkpoint 5176 converts checkpoint 5175's realization sensitivity into a
genuinely predeclared paired experiment. Before any new outcome was inspected,
it froze twelve confirmatory high-mode seeds, all checkpoint-5175 physics and
numerics, two paired estimands, inherited numerical envelopes, a symmetric
preference rule and a no-early-preference stopping rule. The protocol hash is

```text
64529978cc452b302a5f09f52fff4be7af2ae8ef5cd64f29a8352005925fb7e7.
```

The already observed checkpoint-5175 seed `517500409` is retained only as a
pilot and is excluded from confirmatory inference. The six-seed point is
descriptive only; the locked model-preference gate is evaluated once at all
twelve seeds. Each invocation executes only the next scheduled seed and writes
`log.txt`, `status.json` and `COMPLETE.marker`, so it is resumable and remains
inside the standing four-hour cap.

Confirmatory seed `01/12`, value `3240854344`, completed in
`8660.622554000001 s = 2.405728 h`. It gives

```text
MTS forward q = 1.6661100236781148;
CDM forward q = 1.8121303291091404;
MTS q-band distance = 0;
CDM q-band distance = 0;

MTS RMSE = 0.26493073339481193 dex;
CDM RMSE = 0.27031896138684475 dex;
D_RMSE(MTS-CDM) = -0.0053882279920328124 dex.
```

Both models enter the parent q band, while MTS has the lower RMSE. The locked
seed classification is therefore `MIXED_OR_SINGLE_METRIC`, not an MTS win or a
CDM win. This contrasts with the excluded pilot, which favored CDM on both
metrics, and directly confirms that one realization was not interpretable.

Confirmatory seed `02/12`, value `2557716234`, completed in
`11277.178004199988 s = 3.132549 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.9055214552086714;
CDM forward q = 1.6985663646708449;
MTS q-band distance = 0;
CDM q-band distance = 0;

MTS RMSE = 0.2579403375424721 dex;
CDM RMSE = 0.25276619674592515 dex;
D_RMSE(MTS-CDM) = +0.005174140796546933 dex.
```

Both models again enter the parent q band, while this realization gives CDM
the lower RMSE. It is also `MIXED_OR_SINGLE_METRIC`, not a joint win.

Confirmatory seed `03/12`, value `2077240922`, completed in
`11513.725992299966 s = 3.198257 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.3778998208438649;
CDM forward q = 1.3762430791118931;
MTS q-band distance = 0.13407781583615308;
CDM q-band distance = 0.1357345575681248;
D_q(MTS-CDM) = -0.0016567417319717226;

MTS RMSE = 0.23870894144848137 dex;
CDM RMSE = 0.23872306539511515 dex;
D_RMSE(MTS-CDM) = -0.000014123946633776141 dex.
```

Both models lie below the parent q interval, with MTS slightly closer and with
slightly lower RMSE. However, `|D_q|=0.0016567417319717226` is below the frozen
q envelope `0.0041618798307934135`, and
`|D_RMSE|=0.000014123946633776141` is below the frozen RMSE envelope
`0.000037956742793165965`. The locked classification is therefore
`NUMERICAL_TIE`, not an MTS win.

Confirmatory seed `04/12`, value `3997337815`, completed in
`7805.266651500016 s = 2.168130 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.350700543069131;
CDM forward q = 1.2367488578094947;
MTS q-band distance = 0.16127709361088693;
CDM q-band distance = 0.2752287788705232;
D_q(MTS-CDM) = -0.11395168525963628;

MTS RMSE = 0.2502030303178072 dex;
CDM RMSE = 0.24582494827433982 dex;
D_RMSE(MTS-CDM) = +0.004378082043467402 dex.
```

Both models lie below the parent q interval. MTS is materially closer on the
q-band-distance statistic, while CDM has materially lower RMSE; both differences
exceed their respective frozen numerical envelopes in opposite directions. The
locked classification is therefore `MIXED_OR_SINGLE_METRIC`, not a joint win
for either branch.

Confirmatory seed `05/12`, value `1601888544`, completed in
`8547.912162500026 s = 2.374420 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.147173922573155;
CDM forward q = 1.075197334064474;
MTS q-band distance = 0.36480371410686296;
CDM q-band distance = 0.4367803026155439;
D_q(MTS-CDM) = -0.07197658850868094;

MTS RMSE = 0.24037615685505082 dex;
CDM RMSE = 0.2389572514940265 dex;
D_RMSE(MTS-CDM) = +0.0014189053610243196 dex.
```

This is a second resolved metric split: MTS is closer to the inherited q band,
while CDM has lower RMSE, and both differences exceed their frozen numerical
envelopes. The locked classification is `MIXED_OR_SINGLE_METRIC`; neither
branch receives a joint win.

Confirmatory seed `06/12`, value `1077884374`, completed in
`7433.874670499994 s = 2.064965 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.5394361998700428;
CDM forward q = 1.460760201533313;
MTS q-band distance = 0;
CDM q-band distance = 0.05121743514670496;
D_q(MTS-CDM) = -0.05121743514670496;

MTS RMSE = 0.2580331892184844 dex;
CDM RMSE = 0.2610722215483044 dex;
D_RMSE(MTS-CDM) = -0.0030390323298200017 dex.
```

MTS enters the inherited q band while CDM remains below it, and MTS also has
the lower RMSE. Both advantages exceed their frozen numerical envelopes in the
same direction, so the locked seed classification is `MTS_JOINT_WIN`. This is
the first confirmatory joint win, but one seed is not an ensemble preference.

Confirmatory seed `07/12`, value `3363819115`, completed in
`8259.141000700009 s = 2.294206 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.35140634597034;
CDM forward q = 1.3233328626701182;
MTS q-band distance = 0.1605712907096779;
CDM q-band distance = 0.18864477400989976;
D_q(MTS-CDM) = -0.028073483300221858;

MTS RMSE = 0.24593528441584778 dex;
CDM RMSE = 0.24776838355367337 dex;
D_RMSE(MTS-CDM) = -0.001833099137825589 dex.
```

Both models lie below the inherited q band, but MTS is closer and also has
lower RMSE. Both advantages clear their frozen numerical envelopes in the same
direction. Seed 7 is therefore a second consecutive `MTS_JOINT_WIN`, while the
ensemble remains incomplete and nonclaim.

Confirmatory seed `08/12`, value `3861952803`, completed in
`9639.743068599957 s = 2.677706 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.3624988165788856;
CDM forward q = 1.2933484233895756;
MTS q-band distance = 0.14947882010113234;
CDM q-band distance = 0.21862921329044238;
D_q(MTS-CDM) = -0.06915039318931004;

MTS RMSE = 0.2631192449864078 dex;
CDM RMSE = 0.2571894506651439 dex;
D_RMSE(MTS-CDM) = +0.005929794321263893 dex.
```

MTS is again closer to the inherited q band, while CDM has lower RMSE; both
differences clear their frozen numerical envelopes in opposite directions.
The locked classification is `MIXED_OR_SINGLE_METRIC`, not a joint win.

Confirmatory seed `09/12`, value `2049864674`, completed in
`10659.290117199998 s = 2.960914 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.3919551152951986;
CDM forward q = 1.3199169670855937;
MTS q-band distance = 0.12002252138481939;
CDM q-band distance = 0.19206066959442425;
D_q(MTS-CDM) = -0.07203814820960486;

MTS RMSE = 0.2543788356133927 dex;
CDM RMSE = 0.25087466465736746 dex;
D_RMSE(MTS-CDM) = +0.003504170956025232 dex.
```

MTS is closer to the inherited q band while CDM has lower RMSE, with both
differences above their frozen numerical envelopes in opposite directions.
The locked classification is another `MIXED_OR_SINGLE_METRIC` result.

Confirmatory seed `10/12`, value `2453975482`, completed in
`10330.918570900045 s = 2.869700 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.709665216213733;
CDM forward q = 1.807205326564159;
MTS q-band distance = 0;
CDM q-band distance = 0;
D_q(MTS-CDM) = 0;

MTS RMSE = 0.24357305795120351 dex;
CDM RMSE = 0.24540754207087037 dex;
D_RMSE(MTS-CDM) = -0.001834484119666857 dex.
```

Both models enter the inherited q band, while MTS has lower RMSE. Because the
q statistic is tied, the locked classification is `MIXED_OR_SINGLE_METRIC`,
not a joint win.

Confirmatory seed `11/12`, value `2202452999`, completed in
`7852.93685659999 s = 2.181371 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.4959537527942506;
CDM forward q = 1.6070796228110562;
MTS q-band distance = 0.016023883885767365;
CDM q-band distance = 0;
D_q(MTS-CDM) = +0.016023883885767365;

MTS RMSE = 0.2615616472725181 dex;
CDM RMSE = 0.26171652676596324 dex;
D_RMSE(MTS-CDM) = -0.00015487949344511476 dex.
```

CDM enters the inherited q band while MTS remains just below it, whereas MTS
has slightly lower RMSE. The two metrics point in opposite directions and both
clear their numerical envelopes, so the locked classification is
`MIXED_OR_SINGLE_METRIC`.

Confirmatory seed `12/12`, value `1993157507`, completed in
`8709.048773100018 s = 2.419180 h`, inside the four-hour cap. It gives

```text
MTS forward q = 1.3782483860083448;
CDM forward q = 1.299561920758597;
MTS q-band distance = 0.13372925067167318;
CDM q-band distance = 0.21241571592142106;
D_q(MTS-CDM) = -0.07868646524974787;

MTS RMSE = 0.247952817293614 dex;
CDM RMSE = 0.24884633467267087 dex;
D_RMSE(MTS-CDM) = -0.0008935173790568796 dex.
```

MTS is closer to the inherited q band and has lower RMSE. Both differences
clear their inherited numerical envelopes, so the locked classification is
`MTS_JOINT_WIN`. The result file SHA-256 is
`2b266738b22cddbc6f4a9fa8c5f78833cb8a2aea4152049e5f8520ab045a6427`.

Across all twelve confirmatory seeds,

```text
mean D_q = -0.0392272547258426;
median D_q = -0.03964545922346341;
bootstrap95 D_q = [-0.06256573517896083,
                    -0.01672942342481484];
exact sign-flip p(D_q) = 0.01171875;

mean D_RMSE(MTS-CDM) = +0.0006039774233205624 dex;
median D_RMSE = -0.00008450172003944545 dex;
bootstrap95 D_RMSE = [-0.0012737960786308275,
                       +0.002521414183604568] dex;
exact sign-flip p(D_RMSE) = 0.560546875;
MTS joint wins = 3;
CDM joint wins = 0;
ties/metric splits = 9.
joint-win sign p = 0.25.
```

The q component passes its frozen component test in the MTS direction: its
mean is negative, its bootstrap interval excludes zero and its exact
sign-flip value is `p=0.01171875`. The RMSE component does not pass: its mean
is slightly positive, its bootstrap interval crosses zero and
`p=0.560546875`. Three seeds are MTS joint wins and none are CDM joint wins,
but only three seeds are jointly decisive, so the exact joint-win sign test is
`p=0.25`. The preregistered rule is conjunctive; therefore neither MTS nor CDM
is preferred overall in this locked formation gate.

Current verdict:
`STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE`.
Current route:
`STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE`.

The exact runner used for seeds 1 through 12 is frozen at SHA-256
`c15616bf4eedd9fae55c11c67a5f9064c88f6af0321ec89697f167d228ac8303`.
All twelve scheduled confirmatory seeds are complete. There is no next seed
and no rerun is allowed inside this ensemble. Preserve the runner, protocol,
schedule, score, grids, source history and inference rule as the frozen audit
record.

The next valid route is checkpoint 5177: interpret the locked q/RMSE split
without retuning, identify which fixed observable contribution creates the
split, and use that diagnosis to preregister a separate discrimination gate.
Any exploratory diagnostic must remain explicitly post hoc and must not be
reported as part of checkpoint 5176's confirmatory inference.

Artifacts:

- `5176-Y5-R2FR-predeclared-paired-high-mode-seed-ensemble.md`;
- `scripts/Y5_R2FR_5176_predeclared_paired_high_mode_seed_ensemble.py`;
- `scripts/Y5_R2FR_5176_runner_freeze_verifier.py`;
- `source-intake/functional_rg/5176/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5176_VALIDATION.csv`.

All `12/12` internal validations pass, all five freeze hashes reproduce, all
seven frozen source rows still exist and hash-match, and the protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.

Checkpoint 5176's frozen public `1/12` snapshot is published as checkpoint
`1192`. PR `#9` merged to `main` at commit
`deabe06a958343f19299684da28900ff0494c1e8` on 2026-07-22; its source branch
`agent/publish-checkpoint-1192-preregistration-v2` remains retained at commit
`8913c00`.
The 26-file delta includes the byte-preserved protocol, schedule, freeze
record, compact seed-1 outputs, runner, validation table and a portable public
snapshot verifier. It excludes approximately 73 MiB of seed-1 logs, arrays and
phase caches. PR `#8` was closed unmerged after its stale base repeated the
previous publication; no force-push, branch deletion or direct push to `main`
occurred.

PR `#9` intentionally remains the public `1/12` preregistration snapshot and
was not rewritten after seeds 2 through 12. Those eleven seeds are the
subsequent private delta. The final private checkpoint-5176 output is `393`
files / `874.641 MiB`; its caches remain excluded. No GitHub action occurred
during the seed-12 run or final audit.

## Authoritative current handoff - checkpoint 5175

Checkpoint 5175 restores rather than deletes the physical transfer band that
checkpoint 5174 found in under-resolved cube corners. It embeds every old
non-Nyquist integer mode with component `|n_i|<32` into a `96^3` standardized
Gaussian basis, adds one common high-mode realization, samples the field with
`144^3` particles and uses the same `192^3` global and `160^3` local force
meshes for MTS and CDM.

The exact-low-mode contract is satisfied:

```text
shared standardized modes = 250047;
maximum copied-mode error = 0;
inverse Hermitian error = 1.5398946627761043e-18;
conditioned constraint error <= 6.661338147750939e-16.
```

The isotropic source axis Nyquist is `30.238281627956656 Mpc^-1`, above
checkpoint 5174's density-deficit `k90=29.08088339694904 Mpc^-1`. The shortest
retained source wavelength has exactly three particle cells and four global
force cells. Measured peak working memory was about `2.29 GB`, below the
predeclared conservative `4.96 GiB` gate.

After the same pair-consistent visible history,

```text
MTS preassembly q = 3.0003735677908807;
CDM preassembly q = 3.0779955071456984;

MTS forward q = 1.3163215218202087;
CDM forward q = 1.4120505307635705;
Delta q(CDM-MTS) = +0.09572900894336178;

MTS RMSE = 0.24952409629621566 dex;
CDM RMSE = 0.24860397698800685 dex;
Delta RMSE(CDM-MTS) = -0.0009201193082088166 dex.
```

Both slopes lie below the parent interval. Their distances to its lower edge
are `0.19565611485980927` for MTS and `0.09992710591644749` for CDM. The q and
RMSE differences exceed the inherited numerical envelopes; CDM is closer on
both metrics in this one resolved high-mode realization.

This does not reinstate checkpoint 5173's full-cube verdict and does not prove
a CDM preference. Checkpoint 5174 and checkpoint 5175 together show that the
formation score is sensitive to the newly resolved stochastic high-mode
realization: deleting the band made the branches indistinguishable, while one
resolved realization separates them. A paired seed ensemble is therefore
mandatory before changing the parent mass or state-preparation law.

Route decision:
`THE_ISOTROPICALLY_RESOLVED_TRANSFER_BAND_FAVORS_CDM_IN_THIS_ONE_SHARED_REALIZATION_REQUIRE_A_PREDECLARED_MULTI_SEED_ENSEMBLE_BEFORE_REVISING_THE_PARENT_STATE_LAW`.

The next calculation must freeze a deterministic high-mode seed schedule and
paired stopping/statistical rule before another trajectory is evaluated. Keep
the low modes, grids, spectra, spherical taper, `G_N`, visible history and score
fixed. Run bounded seed pairs under the four-hour cap and compare paired
`Delta q`, q-band distance and `Delta RMSE`; do not inspect one seed and choose
the next seed or alter the parent law mid-ensemble.

Artifacts:

- `5175-Y5-R2FR-exact-low-mode-shared-isotropic-resolution-discrimination-gate.md`;
- `scripts/Y5_R2FR_5175_exact_low_mode_shared_isotropic_resolution_gate.py`;
- `source-intake/functional_rg/5175/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5175_VALIDATION.csv`.

All `16/16` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5174

Checkpoint 5174 tests whether checkpoint 5173's apparent CDM advantage is a
resolved physical consequence of the parent mass transfer. It executes seven
new nonlinear antithetic pairs with the same nested force, calibrated `G_N`,
visible history and score: the two other locked checkpoint-5156 masses, two
predeclared logarithmic masses, one geometric crossing diagnostic, and matched
MTS/CDM spherical-cutoff controls.

The calculation first corrects the relevant scale hierarchy. The seed is a
`64^3` Fourier cube resampled onto `96^3` particles. Its axis Nyquist is
`20.15885441863777 Mpc^-1`, whereas cube-corner modes extend to
`34.91616007546498 Mpc^-1`. For the `1e-20 eV` transfer, `81.4585%` of the
discrete CDM-minus-MTS density deficit and `67.0390%` of the displacement
deficit lie above the axis Nyquist. Their median wavenumbers are respectively
`24.14497544643008` and `22.272597906829947 Mpc^-1`. The large 5173 contrast
was therefore dominated by directionally under-resolved cube-corner modes.

Applying the same spherical cosine cutoff at the axis Nyquist to both spectra
gives

```text
MTS: q=1.7545171766343097, RMSE=0.25087250734395466 dex;
CDM: q=1.7542603049540266, RMSE=0.2524699415280995 dex.
```

Both slopes lie in the parent interval
`[1.511977636680018,2.20499007120595]`. The full-cube difference
`Delta q(CDM-MTS)=-0.40447031113307363` collapses to
`-0.0002568716802830995`, only `0.063508%` of its former magnitude and below
the `0.0041618798307934135` q envelope. The RMSE difference reverses sign:
the conservative cutoff favors MTS by `0.0015974341841448192 dex`. Therefore
checkpoint 5173's CDM advantage does not survive the matched resolution gate.

The full-cube mass continuation is also nonmonotone:

```text
2.81669e-21 eV: q=1.3352583760;
1.00000e-20 eV: q=2.2340071399;
1.77828e-20 eV: q=1.8261831992;
3.16228e-20 eV: q=1.8111795224;
1.00000e-19 eV: q=1.8703640312;
1.00000e-18 eV: q=1.8232146180;
CDM:             q=1.8295368288.
```

Consequently the numerical crossing between `1e-20` and
`1.7782794100389228e-20 eV` is not a stable mass bound. It is retained only as
evidence of UV/realization sensitivity; the parent mass or state law must not
be revised from it.

Route decision:
`THE_5173_CDM_ADVANTAGE_DOES_NOT_SURVIVE_THE_SHARED_SPHERICAL_NYQUIST_CONTROL_THE_Q_SEPARATION_COLLAPSES_AND_THE_RMSE_SIGN_REVERSES_SO_DO_NOT_REVISE_THE_PARENT_STATE_LAW_FROM_THE_CUBE_CORNER_RESULT_REQUIRE_HIGHER_RESOLUTION_ISOTROPIC_SHARED_MODES`.

The next calculation is an isotropic shared-phase resolution ladder. Preflight
the memory and runtime first, then raise the source grid so its axis Nyquist
contains the measured deficit band; compare MTS and CDM with the same spherical
cutoff and no target feedback. Do not infer a mass bound or state-law failure
until that comparison is stable across resolution and seeds.

Artifacts:

- `5174-Y5-R2FR-mass-gap-continuation-and-spherical-cutoff-discrimination-gate.md`;
- `scripts/Y5_R2FR_5174_mass_gap_continuation_and_spherical_cutoff_gate.py`;
- `source-intake/functional_rg/5174/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5174_VALIDATION.csv`.

All `14/14` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5173

Checkpoint 5173 subjects the checkpoint-5169 formation result to the matched
baseline required before interpreting its miss as MTS-specific. It regenerates
the same constrained antithetic realization with the same phases, one-sigma
constraint prescription, nested particle force, calibrated `G_N`, visible
source history, cooling/transport construction, time step and score. The only
changed physics input is

```text
P_MTS(k)=P_CDM(k) T_FDM(k)^2  ->  P_CDM(k).
```

For the UGC09133 patch the source-backed variances are almost identical:

```text
sigma_CDM=1.9544359736828194,
sigma_MTS=1.954435819834488,
sigma_MTS/sigma_CDM=0.9999999212824909.
```

The MTS/CDM power ratio is `0.999999999999383` at `1/R_L`,
`0.9999999617892193` at `2pi/R_L`, but `0.8006483134230982` at the particle
Nyquist scale. The matched experiment therefore isolates the resolved
small-scale covariance tail rather than changing the halo-scale peak.

The full forward result is

```text
preassembly: MTS q=3.688824512640322, CDM q=3.2803593820913157;
forward:     MTS q=2.234007139940017, CDM q=1.8295368288069433;
forward:     MTS RMSE=0.27740773926786666 dex,
             CDM RMSE=0.2767978774229841 dex.
```

Thus `Delta q=-0.40447031113307363` and
`Delta RMSE=-0.0006098618448825421 dex` in the CDM-minus-MTS direction. These
exceed the inherited selected-branch numerical envelopes of
`0.0041618798307934135` and `3.7956742793165965e-05 dex`. The CDM slope lies
inside the parent interval `[1.511977636680018,2.20499007120595]`; the current
MTS slope lies just above it.

Route decision:
`THE_MATCHED_CDM_COVARIANCE_OUTPERFORMS_THE_CURRENT_MTS_STATE_IN_THIS_SHARED_PHASE_PATCH_SO_THE_MTS_STATE_SELECTION_ROUTE_REQUIRES_REVISION_BEFORE_PROMOTION`.

This is real adverse evidence for the current empirical `m=1e-20 eV`
covariance/state-selection branch, not a rejection of the parent field theory
and not a cosmological validation of CDM. It is one constrained patch, not an
ensemble. No coupling, target feedback or arena switch can be used to repair
it. Before changing the parent state law, localize the effect in `k`, prove it
survives exact shared-mode resolution/cutoff controls, and determine whether
the responsible modes lie inside the source-backed and force-resolved domain.

Artifacts:

- `5173-Y5-R2FR-matched-CDM-formation-baseline-discrimination-gate.md`;
- `scripts/Y5_R2FR_5173_matched_CDM_formation_baseline_gate.py`;
- `source-intake/functional_rg/5173/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5173_VALIDATION.csv`.

All `13/13` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5172

Checkpoint 5172 removes the spherical visible-source approximation without
changing the parent state, source history, force normalization or calibrated
`G_N`. The measured UGC09133 gas and disk components define

```text
v_flat^2(R)=v_gas(R)|v_gas(R)|+0.5 v_disk^2(R),
H(k)=k integral dR v_flat^2(R) J1(kR).
```

The Plummer-softened axisymmetric Green function then gives

```text
zeta=sqrt(z^2+epsilon^2),
g_R=-integral dk H(k)J1(kR)exp(-k zeta),
g_z=-(z/zeta)integral dk H(k)J0(kR)exp(-k zeta).
```

The measured `0.7 v_bulge^2` component remains spherical. This operator
contains no response coefficient and reads no galaxy target. Its FFTLog
reconstruction has RMS relative error `1.9446289569274164e-05` and maximum
error `0.00012738032875273282`. The inferred thin-source surface density is
nonnegative over `0.05--500 kpc`; the component outer masses close exactly to
`225804813799.87292 Msun`.

The checkpoint-5169 isobaric `Z=0.3` transport, arrival clock and full
antithetic particle states were replayed about three orthogonal disk axes:

```text
axis z primary: q=2.360216786674679,  RMSE=0.2907262635454763 dex;
axis x control: q=2.376265465075138,  RMSE=0.2917243445466116 dex;
axis y control: q=2.3564847213863844, RMSE=0.2900817181037569 dex;
128-step z:     q=2.365336461267273,  RMSE=0.2906952329051777 dex.
```

The parent interval remains `[1.511977636680018, 2.20499007120595]`.
Relative to the checkpoint-5169 spherical result `q=2.234007139940017`, the
source-backed flattened geometry moves in the wrong direction by
`Delta q=+0.12620964673466206` and worsens RMSE by
`0.013318524277609656 dex`. This is not numerical orientation noise: the
maximum orthogonal-axis displacement is `0.016048678400458982`, the doubled
time-resolution displacement is `0.005119674592593881`, phase transfer closes
to `2.8381553512539006e-14`, and the symmetry-protected axial angular momentum
closes to `5.5473051038371345e-15`.

Route decision:
`SOURCE_BACKED_AXISYMMETRIC_GEOMETRY_DOES_NOT_IMPROVE_THE_PARENT_Q_GATE_SO_THE_CURRENT_OCCUPIED_STATE_SOURCE_BRIDGE_REQUIRES_NEW_PARENT_PHYSICS_NOT_A_GEOMETRY_OR_COUPLING_PATCH`.

The result rejects spherical projection as the explanation for the remaining
gap. It does not reject every time-dependent or non-axisymmetric baryon
history, but such a history may not be invented from the rotation target.
The next least-assumptive route is the parent state-selection/interaction
gate: identify a parent-owned stress or state law beyond the already-evolved
classical Vlasov response, prove its local-vacuum silence, and calculate its
forward radial response. Do not add checkpoint 5171 to checkpoint 5169, tune
another coupling, or fit a disk thickness to `q`.

Artifacts:

- `5172-Y5-R2FR-source-backed-axisymmetric-baryon-geometry-forward-response-gate.md`;
- `scripts/Y5_R2FR_5172_axisymmetric_source_geometry_forward_response_gate.py`;
- `source-intake/functional_rg/5172/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5172_VALIDATION.csv`.

All `15/15` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5171

Checkpoint 5171 calculates the classical occupied-state response requested by
checkpoint 5170. For the positive, energy-monotone checkpoint-5154 `p=2`
Eddington state, the retarded action-angle Vlasov equation gives

```text
delta f_n=[n.partial_J f_0/(n.Omega-omega-i0)] delta Phi_n,
delta f(omega->0)=f_Epsilon[delta Psi-<delta Psi>_(Epsilon,L)].
```

Each orbit therefore contributes the positive variance operator

```text
B=sum_a C_a[diag(p_a)-p_a p_a^T],
B 1=0,
1^T B=0,
u^T B u=sum_a C_a Var_(p_a)(u)>=0.
```

Thus the constant-potential zero mode, occupied-mass compensation and kinetic
Ward identity are derived rather than imposed. The self-consistent static
response uses the same calibrated `G_N`,

```text
delta Psi=(I-kappa K B)^(-1) delta Psi_b,
```

and introduces no response coefficient. In the primary 1536-orbit execution,
the phase mass closes to `-1.872257101487307e-05`, the kernel mass mode to
`2.388465384022028e-15`, and the predicted response mass to
`3.2951935733112233e-16` relative residual. The maximum static radial
dielectric eigenvalue is `0.5522232579424047`, so this benchmark has no static
radial pole. Fine-versus-primary changes are `0.003883609442384084` in that
eigenvalue and `0.008435864706112017` in peak cumulative response.

The response has 30 positive and 66 negative density shells. Its cumulative
mass peaks at `3.223732392293224e11 Msun` near `77.94611143262613 kpc`. The
independently reconstructed checkpoint-5170 requirement peaks at
`5.874817564917664e11 Msun` near `166.08144847903398 kpc`. Their score-window
cosine is `0.9202693383295976`, but the predicted/required ratio spans
`[0.23408343819975605, 2.6511207080165695]` and is
`1.917559127085508` at the transition. No constant multiplier repairs this
shape, and none was used.

Two fail-closed facts prevent promotion. First, the global perturbing-potential
ratio reaches `4.2643327730030665`, so the linear hierarchy fails. Second, the
same classical collisionless response is already evolved nonlinearly by the
checkpoint-5164 through checkpoint-5169 particle characteristics. Adding the
5171 kernel to the 5169 profile would double-count the same Vlasov response.
Checkpoint 5170 is therefore refined: any genuinely new stress must lie beyond
the already-evolved classical Vlasov density response, or the parent must
select a different occupied state/source geometry.

Route decision:
`THE_PARENT_EDDINGTON_STATE_DERIVES_A_COMPENSATED_STATIC_VLASOV_RESPONSE_BUT_THE_LINEAR_HIERARCHY_FAILS_AND_THE_SAME_COLLISIONLESS_RESPONSE_IS_ALREADY_PRESENT_IN_5164_5169_SO_IT_CANNOT_BE_ADDED_AS_A_NEW_STRESS_MOVE_TO_THE_SOURCE_GEOMETRY_GATE_BEFORE_NEW_PARENT_PHYSICS`.

The next least-assumptive calculation is the source-geometry gate: retain the
same state, same `G_N` and frozen source history, but replace the spherical
baryon projection with the source-backed axisymmetric disk/gas force. Do not
invent another coupling or add the 5171 response to the 5169 score.

Artifacts:

- `5171-Y5-R2FR-action-angle-retarded-vlasov-polarization-static-response-and-double-counting-gate.md`;
- `scripts/Y5_R2FR_5171_action_angle_retarded_vlasov_polarization_gate.py`;
- `source-intake/functional_rg/5171/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5171_VALIDATION.csv`.

All `27/27` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5170

Checkpoint 5170 returns from baryon bookkeeping to the parent coupling and
motion-state stress. Checkpoint 4960 already proves one rank-one Hilbert source
direction and one locally calibrated `G_N`. A second constant response
coefficient cannot repair checkpoint 5169 because its transition score is

```text
q[V^2]=2 d ln(V^2)/d ln r,
q[A V^2]=q[V^2]
```

for every positive constant `A`. The selected branch therefore remains at
`q=2.234007139940017`, outside the parent upper edge
`2.20499007120595`, under any constant rescaling. Its best scoring-window
amplitude is `1.7324401962430662`, which would duplicate the calibrated
Newton residue by `Delta G/G=0.7324401962430662` and still leaves the
transition at `0.6552336161759004` of target while overshooting the edge by
factor `2.052939757104537`.

The inverse residual is now quantified without promoting it to a predictive
operator:

```text
required gain at R_n    =2.6440038384385716;
required gain at R_edge =0.84388262746029;
residual sign crossing  =283.8481283505484 kpc;
edge mass expulsion     =0.15611737253971003 of corrected edge mass.
```

After edge normalization separates total amplitude from shape, the unique
one-dimensional monotone-transport lower bound moves every internal quantile
inward. Its selected mean displacement is `60.38564635937875 kpc`, RMS
`64.35901954609716 kpc`, corresponding to at least
`22.144458933210117 km/s` across the sourced clock. All four thermal branches
give mean bounds in `[60.38564635937875, 61.55519642473791] kpc`.

This proves that the missing effect is a compensated, sign-changing collective
redistribution, not a larger positive source or a fitted coupling. At the
transition, canonical wave stress is too small by factor
`59630.650686393856`; the derived `X^2` and `O4` envelopes are too small by
`1.4121560547697633e116` and `3.749634411983126e233`.

The surviving parent target is consequently the occupied-state retarded
polarization

```text
delta T_X^munu(x)=int d4y Pi_R^munu,ab(x,y;F_X) delta g^ab(y).
```

It must satisfy the frozen Ward, compensated-zero-mode, radial-sign-change,
causal-stability, no-retuning and local-vacuum-silence clauses in the 5170
contract. The positive occupied-state existence branch retains maximum
embedded Mercury tidal ratio `6.614360568718464e-19`, but no full PPN or
galaxy claim is inferred.

Route decision:
`ONE_UNIVERSAL_HILBERT_SOURCE_COUPLING_IS_ALREADY_FIXED_AND_CANNOT_CHANGE_Q_THE_5169_RESIDUAL_REQUIRES_A_COMPENSATED_OCCUPIED_STATE_POLARIZATION_WITH_INWARD_MASS_TRANSPORT_AND_LOCAL_VACUUM_SILENCE`.

The next derivation is no longer “find the coupling.” It is to calculate the
retarded Vlasov/CTP stress polarization from the parent occupied state and
test whether it can satisfy the eight 5170 clauses without fitting its radial
shape. Failure demotes the current occupied-state galaxy bridge; success must
retain checkpoint-4960 local GR/Newton/Maxwell automatically.

Artifacts:

- `5170-Y5-R2FR-collective-stress-residual-single-coupling-no-go-and-conserved-kernel-target.md`;
- `scripts/Y5_R2FR_5170_collective_stress_residual_and_single_coupling_no_go.py`;
- `source-intake/functional_rg/5170/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5170_VALIDATION.csv`.

All `20/20` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5169

Checkpoint 5169 performs the forward calculation deferred by checkpoint 5168.
The frozen capacity-bounded flow is replayed as a Lagrangian source operator on
the original full antithetic particle states:

```text
Delta M_sj(t)=sum_i f_isj M_i,arrived(t)/M_i,endpoint,
lambda_s(t)=sum_j Delta M_sj(t)/M_c,
Delta M_visible,s(t)=lambda_s(t) M_c,
a=-G_N M_enclosed(t) r/(r^2+epsilon^2)^(3/2).
```

Every phase deposits exactly the baryon mass removed from it. The operator is
fixed before the response, uses no `q`, has no fitted efficiency, and preserves
the inherited calibrated `G_N` central force. The four full-particle primary
results are

```text
isochoric Z=0.1: q=2.2468474728387435, RMSE=0.2850806581897878 dex;
isochoric Z=0.3: q=2.26699412921067,   RMSE=0.2822731967466959 dex;
isobaric  Z=0.1: q=2.269361831204709,  RMSE=0.282861104216976 dex;
isobaric  Z=0.3: q=2.234007139940017,  RMSE=0.27740773926786666 dex.
```

All improve the free baseline `0.42140386547507747 dex`, but none enters the
parent interval `[1.511977636680018, 2.20499007120595]`. The closest primary
gap is `0.029017068734066953`. The selected isobaric `Z=0.3` branch has a
matched checkpoint-5167 full-particle homologous baseline: transport changes
`q` by `+0.01720705206218609` and RMSE by
`+0.018081789772517787 dex`, so the degradation is not a compressed-particle
comparison artifact.

The previous nearest branch was selected using checkpoint-5167 `q` only for
predeclared numerical controls, never to define the operator or a primary
physics branch. Those controls give

```text
time refinement: q=2.2358570186820326;
p=2 norm:         q=2.2338814558909474;
13 radial bins:   q=2.236200096911821;
52 radial bins:   q=2.2298452601092236.
```

Their maximum displacement from the primary is only
`0.0041618798307934135`. Phase transfer closes to
`1.58396098650932e-13` relative error and angular momentum to
`9.645765841927827e-15`.

Route decision:
`FROZEN_PAIR_CONSISTENT_TRANSPORT_DOES_NOT_CLOSE_THE_PARENT_RESPONSE_GATE_SO_VISIBLE_ASSEMBLY_IS_RETAINED_AS_A_BOUNDED_SOURCE_HISTORY_AND_PARENT_COLLECTIVE_STRESS_TAKES_PRIORITY`.

This rejects the idea that the remaining galaxy slope can be repaired merely
by making radial baryon bookkeeping admissible. It does not reject the parent
MTS field route. The next target must return to the parent motion-sector
Hessian/current: derive the collective stress/source coupling that can generate
a nonlocal response while leaving the inherited local GR/Newton/Maxwell branch
unchanged. Visible assembly remains a measured source-history input and bound,
not a tunable replacement coupling.

Artifacts:

- `5169-Y5-R2FR-pair-consistent-capacity-bounded-transport-forward-response-gate.md`;
- `scripts/Y5_R2FR_5169_pair_consistent_transport_forward_response_gate.py`;
- `source-intake/functional_rg/5169/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5169_VALIDATION.csv`.

All `20/20` generated validations pass. Every output remains nonclaim, source
hashes are unchanged, the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5168

Checkpoint 5168 attacks the remaining homologous donor approximation rather
than tuning the narrow checkpoint-5167 slope miss. A direct resolved assignment
of the pair-mean cooled-shell source to the two antithetic phases is proved
infeasible. With pair source `rbar_i`, phase capacities `a_si`, and
`x_-i=rbar_i+delta_i`, `x_+i=rbar_i-delta_i`, feasibility requires

```text
max(-rbar_i,rbar_i-a_+i) <= delta_i
                         <= min(a_-i-rbar_i,rbar_i),
sum_i delta_i=0.
```

Only the one-bin homologous limit satisfies these constraints; every tested
resolved partition with two or more bins fails. The earlier `25 versus 4 Gyr`
phase endpoints were therefore not physical alternatives but the result of an
inadmissible source map.

The derived repair is a capacity-bounded one-dimensional optimal-transport
operator `f_isj`:

```text
min sum_i,s,j f_isj |r_i-r_j|^p/R_edge^p,
sum_s,j f_isj=2 rbar_i,
sum_i,j f_i,-,j=sum_i,j f_i,+,j=M_c,
sum_i f_isj <= a_sj,
f_isj >= 0.
```

The primary `p=1`, 26-bin solution transports mass by mean absolute distance
`22.110619352735302 kpc` (RMS `48.54166468669157 kpc`) and changes the pair
radial profile by L1 fraction `0.48996626692208395`. Across 13, 20, 26 and 52
bins the mean displacement stays within
`[21.58391328746118, 22.20984793120233] kpc`; `p=2` is retained as a frozen
closure-norm comparator.

Lifting the endpoint flow through each sourced shell-arrival history proves,
for all four thermal branches and all 41 sampled times,

```text
x_sj(t)>=0,
x_sj(t)<=a_sj,
Delta M_s,edge(t)=0,
[lambda_-(t)+lambda_+(t)]/2=lambda_bar(t).
```

The maximum pair-history residual is `2.220446049250313e-16`; edge and capacity
residuals are floating-point mass errors only. The operator never reads `q`,
does not alter the local GR/Newton/Maxwell branch, and remains a reduced
variational matter closure rather than a radiation-hydrodynamic derivation.

Route decision:
`RAW_PAIR_RADIAL_REMOVAL_IS_CAPACITY_INFEASIBLE_FOR_SEPARATE_ANTITHETIC_PHASES_BUT_A_MINIMUM_RADIAL_TRANSPORT_OPERATOR_NOW_SATISFIES_BOTH_PHASE_CAPACITIES_BOTH_ENDPOINTS_AND_THE_PAIR_TIME_IDENTITY_WITHOUT_READING_Q`.

The next gate is now constructive: run the forward dynamics with the frozen
`p=1` operator for all four checkpoint-5167 clocks, repeat the selected branch
with `p=2` and resolution controls, and compare the slope/amplitude response
without refitting the operator to the target.

Artifacts:

- `5168-Y5-R2FR-pair-consistent-capacity-bounded-optimal-transport-radial-source-operator-gate.md`;
- `scripts/Y5_R2FR_5168_pair_consistent_optimal_transport_source_operator_gate.py`;
- `source-intake/functional_rg/5168/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5168_VALIDATION.csv`.

All `16/16` generated validations pass. Every output remains nonclaim, all
source hashes are unchanged, the protected `formalization-workbench` digest
remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5167

Checkpoint 5167 removes the specific one-zone temporal approximation rejected
by checkpoint 5166. Each inherited hot-baryon shell is cooled through the real
Cloudy/Grackle table from the derived fixed-edge virial temperature to the
predeclared atomic floor, using both controlled thermodynamic brackets:

```text
rho de_th/dt=-C n_H^2 Lambda(n_H,T,Z),
t_cool,V=integral rho d[3kT/(2 mu m_p)]/[C n_H^2 Lambda],
t_cool,P=integral rho(T) d[5kT/(2 mu m_p)]/[C n_H(T)^2 Lambda],
t_arr(r)=t_cool(r)+pi sqrt[r^3/(G_N M_tot(<r))]/(2 sqrt(2)).
```

The isochoric/isobaric pair and `Z={0.1,0.3} Zsun` Cartesian product was fixed
before the response was read. The shell mass is ranked by `t_arr` until it
equals the measured condensed endpoint. Its pair-mean cumulative distribution
defines `lambda_arr(t)` and drives the checkpoint-5164 exact identity

```text
m_gi(t)=m_pi-lambda_arr(t) Delta m_phase d_i,
N_d Delta m_phase=M_c(R_edge),
M_cond(<r,t)=lambda_arr(t) M_c,obs(<r).
```

A direct shell-rank assignment to each antithetic particle phase was audited
and rejected before evolution: the deliberately unequal antithetic halo masses
would force approximately 90 percent of one phase but 33 percent of the other
to condense and create artificial `25 versus 4 Gyr` endpoints. The radial clock
is therefore pair-mean, while donor removal retains the already-proved
phase-by-phase homologous mass identity. No favorable invalid map was run.

The converged radial clock endpoints are

```text
isochoric Z=0.1: 6.168757986717486 Gyr;
isochoric Z=0.3: 3.6215880802906995 Gyr;
isobaric  Z=0.1: 4.852653732169424 Gyr;
isobaric  Z=0.3: 2.6663381340430043 Gyr.
```

Radial-shell refinement changes each endpoint by only
`0.001756..0.001760` fraction. The four primary forward results are

```text
isochoric Z=0.1: q=2.261310803962612,  RMSE=0.2671620600590398 dex;
isochoric Z=0.3: q=2.2325996564659354, RMSE=0.2643584119327723 dex;
isobaric  Z=0.1: q=2.293025495707922,  RMSE=0.2634024092506205 dex;
isobaric  Z=0.3: q=2.2173885341915036, RMSE=0.2595842073314631 dex.
```

Every branch improves the free baseline `0.42140386547507747 dex`. The parent
interval is `[1.511977636680018, 2.20499007120595]`; no primary point lies
inside it. All four branches were repeated at doubled time resolution:

```text
isochoric Z=0.1: q=2.261121428524268;
isochoric Z=0.3: q=2.24551025779569;
isobaric  Z=0.1: q=2.2947321954941886;
isobaric  Z=0.3: q=2.210775108908433.
```

The closest branch was additionally repeated with every inherited particle,
giving `q=2.216800087877831`; its particle shift is only
`0.0005884463136727192`. The closest controlled value remains the doubled-time
isobaric `Z=0.3` result, `0.0057850377024828425` above the parent upper edge.
Thus radial entropy/freefall removes most of the checkpoint-5166 global-clock
error but does not yet pass the slope gate.

Route decision:
`RADIAL_ENTROPY_COOLING_AND_FREEFALL_REMOVES_MOST_OF_THE_GLOBAL_CLOCK_SLOPE_ERROR_BUT_ALL_REFINED_POINT_ESTIMATES_REMAIN_NARROWLY_ABOVE_THE_PARENT_Q_BAND`.

This is neither a success claim nor a reason to retune metallicity. The next
physical target is the remaining homologous source approximation: derive a
pair-consistent radial donor-removal/deposition operator, including pressure,
angular-momentum transport and feedback bounds, without mapping the pair mean
onto either antithetic phase as though it were a separate observed halo. If
that controlled source correction cannot close the `0.0058` gap while retaining
the amplitude improvement, visible assembly becomes a quantified source-history
bound and the collective-stress route takes priority.

Artifacts:

- `5167-Y5-R2FR-radial-entropy-cooling-freefall-mass-transfer-and-forward-response-gate.md`;
- `scripts/Y5_R2FR_5167_radial_entropy_cooling_freefall_transfer_gate.py`;
- `source-intake/functional_rg/5167/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5167_VALIDATION.csv`.

All `21/21` generated validations pass. Every generated row remains nonclaim,
all source hashes are unchanged, the protected `formalization-workbench`
digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5166

Checkpoint 5166 closes the immediate checkpoint-5165 clock question by doing
the constructive calculation. The baryon-current, Maxwell-exchange and first-
law projection gives

```text
nabla_mu(n_b u^mu)=0,
nabla_mu T_EM^{mu nu}=-F^nu_lambda J^lambda,
nabla_mu T_b^{mu nu}=F^nu_lambda J^lambda-G_rad^nu,
n_b T u^mu nabla_mu s=j_cond^mu E_mu-Q_rad.
```

The minimal neutral, optically thin CIE branch uses

```text
Q_rad=n_H^2[Lambda_prim(n_H,T)+(Z/Zsun)Lambda_metal(n_H,T)],
M_hot(<r,lambda)=[b-mu lambda]M_X(<r),
K(lambda) dot(lambda)=L_CIE(lambda),
t(lambda)=integral_0^lambda K(x)/L_CIE(x) dx.
```

The cooling coefficients come from the immutable Grackle
`CloudyData_noUVB.h5` file at commit
`928696482fbe15d9bac4382de6134d95568f099c`, local SHA-256
`0abe25cceeb5c0825381c5f17059982a9a2cdd27ce369a475c559fba6a8fa106`.
No duration or response efficiency is fitted to `q`.

For the inherited UGC09133 mass profile, the fixed-edge virial state is

```text
T_vir                         = 1314274.0487669532 K;
mean molecular weight         = 0.61226;
n_H shell range               = 9.758469145473242e-6 .. 2.952095954325897e-3 cm^-3;
tau_e(lambda=0)               = 2.8960082791591003e-4;
tau_e(lambda=1)               = 1.492436225264951e-4.
```

The electron-scattering depth is safely within the sourced XSTAR thin
reference envelope, although line/photoelectric transfer remains unsolved.
The actual antithetic NESTED160 snapshots give the Poisson-self-pair-subtracted
clumping factors

```text
pair N13 = 1.5167698711776387;
pair N20 = 1.497631108966023;
pair N26 = 1.5385341412037419.
```

Using the predeclared N26 pair value, the sourced clocks are

```text
Z=0.1 Zsun: 4.302288610288357 Gyr = 3.2142398640115175 transition orbits;
Z=0.3 Zsun: 1.826692151371429 Gyr = 1.3647217246593508 transition orbits.
```

Both durations lie in the inherited one-to-four-orbit window, but the exact
inverse-integral histories are strongly front-loaded. They were inserted
directly into the checkpoint-5164 particle evolution rather than replaced by
a duration-matched C2 ramp. The result is

```text
parent q interval              = [1.511977636680018, 2.20499007120595];
Z=0.1 forward q                = 2.376080267862411;
Z=0.1 RMSE                     = 0.2791849168854609 dex;
Z=0.3 forward q                = 2.426883714866849;
Z=0.3 RMSE                     = 0.2911000922263307 dex;
Z=0.3 doubled-time-step q      = 2.4231802176392696;
Z=0.3 refinement |Delta q|     = 0.0037034972275793443.
```

The sourced clocks improve the free baseline RMSE `0.42140386547507747 dex`,
but miss the parent upper `q` edge by `0.17109019665646086` and
`0.22189364366089892`. This is a stable scientific rejection of the one-zone
homologous CIE clock as the completed parent mechanism, not a code failure and
not a reason to discard the sourced entropy route.

Route decision:
`SOURCED_CIE_CLOCK_IMPROVES_THE_BASELINE_RMSE_BUT_BOTH_PREDECLARED_FORWARD_BRANCHES_MISS_THE_PARENT_Q_BAND_SO_ONE_ZONE_HOMOLOGOUS_COOLING_IS_REJECTED_AS_THE_COMPLETED_PARENT_CLOCK`.

The next derivation must remove the approximation that produced the failure:
solve a radial entropy/cooling-flow ordering so dense shells cool and transfer
mass on their own sourced times instead of applying one global homologous
`lambda(t)`. The donor-removal and condensed-source deposition must remain
exactly mass-conserving. UGC09133 hot-phase metallicity and line-transfer
uncertainty should be bounded only after the radial forward map exists.

Artifacts:

- `5166-Y5-R2FR-sourced-CIE-cooling-clumping-derived-clock-and-forward-response-gate.md`;
- `scripts/Y5_R2FR_5166_sourced_CIE_cooling_assembly_clock_gate.py`;
- `source-intake/functional_rg/5166/`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5166_VALIDATION.csv`.

All `22/22` generated validations pass. Every generated row remains nonclaim,
all source hashes are unchanged, the protected `formalization-workbench`
digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5165

Checkpoint 5165 asks whether the baryon plus Maxwell/Poynting energy equation
actually selects the checkpoint-5164 near-successful source duration. The
answer is now proved rather than recorded as a vague missing input.

The existing parent action gives the same-action exchange and worldtube law

```text
nabla_mu T_EM^{mu nu}=-F^nu_lambda J^lambda,
nabla_mu T_matter^{mu nu}=+F^nu_lambda J^lambda,
Delta E_total+integral_boundary J_E.n dSigma=0.
```

For a closed-baryon one-coordinate assembly branch this reduces to

```text
L_out(t)=K(lambda) dot(lambda),
K(lambda)=-dE_mech/dlambda.
```

This supplies a clock only after a constitutive
`L_out[lambda,baryon state]` is known. For every positive duration `T`, a
monotone endpoint-preserving `lambda_T` and
`L_T=K(lambda_T)dot(lambda_T)` obey the same integrated energy identity.
Checkpoint 5165 constructs that family explicitly. Maxwell plus total-energy
conservation therefore cannot secretly select one orbit; the matter current,
emissivity/opacity or boundary flux law must do so.

The exact checkpoint-5164 mass-transfer coordinate was projected through the
spherical frozen-motion endpoint energy. Since

```text
M_b(r,lambda)=(b-lambda mu)M_X(r)+lambda M_c(r),
W(lambda)=W0+W1 lambda+W2 lambda^2,
K(lambda)=-(W1+2W2 lambda)/2,
```

the edge baryon mass is constant and the energy barrier is analytic. For the
primary resolved pair,

```text
M_X(R_edge)                 = 2.514412294695019e12 Msun;
M_c(R_edge)                 = 2.2580481379987292e11 Msun;
full binding release        = 3.578693974236985e52 J;
virial radiative release    = 1.7893469871184925e52 J;
minimum K(lambda)           = 7.410020069160251e51 J;
quadrature relative change  = 1.0662775091098126e-7.
```

`K` is positive on the full assembly interval. Finite outgoing flux can
therefore power every tested monotone history. The fixed-edge causal crossing
time is `0.0011797696063842644 Gyr`, so the impulsive history is rejected.
Four distinct positive durations remain admissible under the causal and
diagnostic Eddington-scale screens.

The one-orbit `C2` branch requires average power
`4.236130605845907e35 W = 1.1066171906598504e9 Lsun` and peak power
`8.885675232120723e35 W`, only `3.1303025149258354e-7` of the condensed-
baryon Eddington scale. This proves energetic feasibility, not duration
selection. The SPARC surface-light integral is explicitly retained only as a
3.6-micron luminosity-scale comparator, never as bolometric cooling power.

The important robustness result is that the predeclared one- and four-orbit
primary responses differ by only `0.004884644110929592` in `q`; the one-orbit
refinement interval still intersects the parent band. The useful response is
therefore a broad factor-four clock region rather than a single tuned instant.

Route decision:
`POYNTING_ENERGY_BALANCE_EXCLUDES_IMPULSIVE_ASSEMBLY_AND_PROVES_A_BROAD_ONE_TO_FOUR_ORBIT_RESPONSE_ENERGETICALLY_ADMISSIBLE_BUT_CANNOT_SELECT_A_CLOCK_WITHOUT_A_PARENT_CONSTITUTIVE_EMISSIVITY`.

The next target is concrete: derive the charged-baryon continuity, Euler and
entropy/radiative-transfer projection that supplies
`L_out[lambda,state]`, with plasma/cooling inputs sourced and frozen before
the response is inspected. If that law cannot place assembly in the broad
one-to-four-orbit window, demote visible-source timing to closure-only and
move to the collective density-matrix stress alternative.

Artifacts:

- `5165-Y5-R2FR-baryon-Maxwell-Poynting-assembly-clock-identifiability-and-energy-bound-gate.md`;
- `scripts/Y5_R2FR_5165_baryon_Maxwell_Poynting_assembly_clock_gate.py`;
- `source-intake/functional_rg/5165/covariant_energy_exchange_contract.csv`;
- `source-intake/functional_rg/5165/assembly_mass_profile_samples.csv`;
- `source-intake/functional_rg/5165/binding_energy_polynomial.csv`;
- `source-intake/functional_rg/5165/photometric_luminosity_scale.csv`;
- `source-intake/functional_rg/5165/assembly_clock_luminosity_bounds.csv`;
- `source-intake/functional_rg/5165/assembly_clock_family_samples.csv`;
- `source-intake/functional_rg/5165/clock_response_joint_gate.csv`;
- `source-intake/functional_rg/5165/clock_identifiability_gate.csv`;
- `source-intake/functional_rg/5165/route_decision.csv`;
- `source-intake/functional_rg/5165/source_provenance.csv`;
- `source-intake/functional_rg/5165/baryon_Maxwell_Poynting_assembly_clock_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5165_VALIDATION.csv`.

All `21/21` generated validations pass. Every row remains nonclaim, all
source hashes are unchanged, the protected `formalization-workbench` digest
remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`,
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5164

Checkpoint 5164 replaces the checkpoint-5163 scalar adiabatic-response
efficiency with a forward two-component initial-value calculation. It exactly
regenerates both checkpoint-5162 antithetic `NESTED160` end states and retains
their actual three-dimensional positions, physical velocities and angular
momenta. The regenerated phase values differ from the stored values by at
most `6.22e-14`; the pair value is
`q=3.688824512640322` versus stored `3.688824512640355`.

The condensed and diffuse visible sources are now separated without deleting
baryon mass. For donor indicator `d_i`, source-transfer coordinate `lambda`
and measured condensed source `M_b,obs`,

```text
m_g,i(lambda)=m_p-lambda Delta_m d_i,
Delta_m=M_b,obs(R_edge)/N_d,
M_g(<r,lambda)=sum_(i<r)m_g,i-M_background(<r)
              +lambda M_b,obs(<r).
```

Thus `N_d Delta_m=M_b,obs(R_edge)` exactly for every `lambda`; outside the
edge the removed particle-tied mass and added condensed mass cancel. Across
the paired realization, UGC09133's measured condensed source is
`0.48348752008544155` of the donor particles' cosmic baryon allotment. The
remaining baryons stay diffuse and particle-tied. The force is the spherical
Newtonian projection of the same checkpoint-4947 Einstein/Hilbert source and
the same calibrated `G_N`; no response efficiency, galaxy force or local
coefficient was introduced.

Six source histories were frozen before scoring: impulsive, two
Newton-freefall ramps, one transition orbit, and four/eight-orbit adiabatic
ramps. Every source run has a same-state `lambda=0` control. The primary matrix
uses exact-mass radial compression; the near-boundary branch was repeated at
doubled timesteps and with every original particle.

The important numerical result is:

```text
parent q band                     = [1.511977636680018, 2.20499007120595]
free checkpoint-5162 q            = 3.688824512640322
one-orbit primary q                = 2.2069358661442315
one-orbit doubled-timestep q       = 2.196497562958223
one-orbit full-particle q          = 2.2235536913099607
one-orbit timestep |Delta q|       = 0.010438303186008469
one-orbit particle |Delta q|       = 0.016617825165729183
```

The primary value misses the inherited band by `0.00194579493828151`, while
the refinement interval intersects it. This is therefore a real numerical
compatibility result, not a claimed parent prediction: the one-orbit clock was
predeclared but is not yet selected by the parent field equations.

The source improves but does not finish the amplitude problem. The baseline
velocity-squared RMSE and transition ratio are `0.42140386547507747 dex` and
`0.20525141123436702`; the one-orbit values are
`0.27569297375275253 dex` and `0.3841731626520422`. The mass-conserving
circular adiabatic limit reaches `0.116709324250618 dex` but overshoots the
slope to `q=0.23704123622245601`. Source history therefore controls a genuine
slope/amplitude tradeoff rather than acting as an arbitrary multiplicative
coupling.

Numerical controls are clean. The adiabatic four/eight-orbit difference is
`0.05747733879589889`; doubled-timestep adiabatic `|Delta q|` is
`0.003481376334322217`; maximum angular-momentum residual is
`1.051941315326681e-13`; and the maximum source-minus-control outer-boundary
ingress difference is `0.006648404627445054`. All `23/23` generated checks and
the independent strict audit pass.

The next derivation target is not another response scan. Derive the visible
source assembly clock from the integrated baryon plus Maxwell/Poynting energy
equation, rather than selecting one orbit because it nearly works. Insert that
derived clock into the mass-conserving cosmological two-component source and
retest both `q` and the remaining amplitude deficit. If the parent EM/baryon
energy flow cannot select the required clock or amplitude, move to the
collective density-matrix stress route already left open by checkpoint 5163.

Artifacts:

- `5164-Y5-R2FR-mass-conserving-visible-motion-initial-value-response-gate.md`;
- `scripts/Y5_R2FR_5164_mass_conserving_two_component_initial_value_gate.py`;
- `source-intake/functional_rg/5164/mass_conserving_two_component_force_contract.csv`;
- `source-intake/functional_rg/5164/snapshot_reproduction_gate.csv`;
- `source-intake/functional_rg/5164/baryon_mass_conservation_gate.csv`;
- `source-intake/functional_rg/5164/source_history_contract.csv`;
- `source-intake/functional_rg/5164/two_component_response_scores.csv`;
- `source-intake/functional_rg/5164/two_component_response_profile_samples.csv`;
- `source-intake/functional_rg/5164/two_component_numerical_controls.csv`;
- `source-intake/functional_rg/5164/route_decision.csv`;
- `source-intake/functional_rg/5164/source_provenance.csv`;
- `source-intake/functional_rg/5164/mass_conserving_two_component_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5164_VALIDATION.csv`.

The two compressed snapshot files are reproducibility caches, not claim data.
All current rows remain nonclaim; source hashes are unchanged; the protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`;
and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5163

Checkpoint 5163 follows the resolved checkpoint-5162 collisionless failure
into terms that the existing parent actually owns. The canonical
Klein--Gordon/Schrodinger Madelung stress was derived at the target transition.
For `n_q=x^q/(1+x^q)`,

```text
eta_Q(R_n)=C_q [hbar/(m v_infinity R_n)]^2,
C_q=q(2q^4+6q^3+9q^2+12q+8)/[2(q+2)^3].
```

For UGC09133 at the frozen `m=1e-20 eV`,
`eta_Q=2.1752123578548805e-9`. Requiring every current halo mapping to
remain above the instantaneous equality Jeans mass gives the weaker universal
floor `m=8.882479043701029e-23 eV`, where the UGC09133 value is still only
`2.7569778620807335e-5`. Making wave stress order one at this transition
instead raises the equality Jeans mass above every one of the 350 current
halo/mapping rows. Canonical wave pressure is therefore rejected as the sole
order-one repair on the universal population branch, unless a distinct
parent critical amplifier is derived.

The known parent gradient interactions are even smaller. Transporting the
checkpoint-4958 essential coefficients gives conservative transition
envelopes

```text
essential X^2 fractional Hessian shift <=1.1641800018388254e-116;
Weyl-squared kinetic shift             <=4.3844376752694736e-234.
```

No free coefficient was used in either result.

The important positive finding is that checkpoint 5162 omitted the condensed
visible source. It evolved a cosmic total-matter particle field and then
projected its motion fraction, but did not apply UGC09133's measured baryonic
acceleration. The checkpoint-4947 parent already owns that coupling through
the same Einstein/Hilbert source and calibrated `G_N`; no new galaxy force is
needed. With the locked `ML_disk=0.5`, `ML_bulge=0.7` source convention, the
baryonic acceleration at `R_n` is `0.9031622469349835` times the target motion
acceleration.

A spherical circular-orbit adiabatic response bracket was executed as a
diagnostic, not adopted as closure:

```text
r_i M_X,i(r_i)/f_X
 =r_f[M_X,i(r_i)+epsilon_ad M_b,eq(r_f)].
```

The zero-response fine profile exactly reproduces `q=3.688824512640322`.
Full response gives `q=0.122574399396473` and improves the no-refit
velocity-squared log RMSE from `0.42140386547507747` to
`0.145472021520355 dex`. Thus the ordinary visible source has enough leverage
to cross `q_parent=1.858483853942984`. The inverse crossing is near
`epsilon_ad=0.051006101448935366`, but it is explicitly not a prediction:
solving for it uses the target exponent and it worsens the amplitude score at
the nearest predeclared response row.

The next target is an actual two-component visible-plus-motion initial-value
calculation under the one Poisson/Einstein source. Freeze the cosmic baryon
fraction, the checkpoint-5156 covariance, the UGC09133 source data and the
assembly comparators before reading the output. Evolve the same antithetic
phases and resolved nested grids, score `q`, profile amplitude and the edge
together, and do not promote a response-efficiency fit. If controlled source
histories cannot jointly improve the transition and profile, move to a
genuinely collective density-matrix stress rather than inflating the already
bounded canonical gradient terms.

Artifacts:

- `5163-Y5-R2FR-parent-wave-stress-and-visible-source-response-gate.md`;
- `scripts/Y5_R2FR_5163_parent_wave_and_visible_source_response_gate.py`;
- `source-intake/functional_rg/5163/parent_wave_and_source_operator_contract.csv`;
- `source-intake/functional_rg/5163/canonical_wave_transition_magnitude.csv`;
- `source-intake/functional_rg/5163/universal_wave_mass_overlap_gate.csv`;
- `source-intake/functional_rg/5163/essential_gradient_stress_envelope.csv`;
- `source-intake/functional_rg/5163/visible_baryon_source_profile.csv`;
- `source-intake/functional_rg/5163/adiabatic_visible_source_response_matrix.csv`;
- `source-intake/functional_rg/5163/visible_source_inverse_requirement.csv`;
- `source-intake/functional_rg/5163/route_decision.csv`;
- `source-intake/functional_rg/5163/source_provenance.csv`;
- `source-intake/functional_rg/5163/parent_wave_and_visible_source_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5163_VALIDATION.csv`.

All `24/24` generated validations and the independent strict revalidation
pass. The maximum shell-invariant residual is
`1.27971934931738e-12`; every output remains nonclaim; all source hashes are
unchanged; no `__pycache__` is kept; and the protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
The galaxy source was read-only and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5162

Checkpoint 5162 performs the first calculation that actually resolves the
frozen UGC09133 transition rather than extrapolating below a force floor. It
retains the global `192^3` periodic Vlasov--Poisson force and adds a numerical
nested correction sourced by the tapered difference between fine and
prolongated-coarse Lagrangian density contrasts. The correction is a
zero-Dirichlet solve of the same Poisson operator, not a galactic force or new
physical coupling. A sampling factor `N_cell/(1+N_cell)` prevents unresolved
particle shot noise from becoming a source, and the weighted correction has
zero net momentum.

The analytic controls pass before the physics output is read. The largest
Gaussian-force error is `0.014083024791743393`; a homogeneous particle lattice
has exactly zero nested force. The largest source-boundary ratio is
`0.004129904468415234`. The first full run correctly failed because the
unconstrained shrinking centre jumped between early diffuse structures. The
repair limits each tracked-centre step to `0.125` local boxes while requiring
agreement with the independently measured final halo. The rerun has maximum
step `0.18085950283162297 Mpc`, at most nine limited steps, and zero final
tracking residual in all four runs.

The 128 and 160 local grids have three-cell resolved radii
`33.9111567809293` and `27.128925424743443 kpc`, both below the frozen
`R_n=36.43917542575495 kpc`. Four paired runs execute `424673280`
particle-step updates. Their full resolved profiles converge:

```text
fixed-edge mass fractional difference = 0.0022556677490277455;
velocity-squared log-RMSE              = 0.01272512465013473 dex;
density log-RMSE                       = 0.020617152235922285 dex;
profile convergence gate               = PASS.
```

The resolved transition gives the decisive conditional result:

```text
q_parent                         = 1.858483853942984;
q_nested_128                     = 3.342318295377389;
q_nested_160                     = 3.688824512640355;
resolution relative difference  = 0.0939340475741273;
fine-grid phase relative spread = 0.09258508958212712;
parent difference               = 1.830340658697371;
numerical envelope              = 0.34650621726296604;
q selection                     = NOT_SELECTED.
```

Thus resolution and phase controls both close, but the parent exponent lies
far outside their numerical envelope. The free collisionless occupied state
does **not** derive the checkpoint-5154 phase flow in this controlled branch.
This is not a rejection of the full MTS programme and remains one antithetic
pair rather than an ensemble; it is a clean rejection of using ordinary free
Vlasov collapse as the missing derivation. Fixed-edge mass remains only about
`15%` high, but the newly resolved target velocity-profile RMSE rises to
`0.38--0.42 dex`, and the compact edge remains absent.

The next theory target is therefore no longer another collisionless rerun. It
must derive an actual term already permitted by the parent action: either the
finite-gradient/wave stress of the complex motion field, or a regular
source-coupling interaction whose exact local zero preserves the
GR/Newton/Mercury and Maxwell/Poynting cog. The new term must generate the
required transition slope and stress dynamically; importing
`dn/dlnR=q n(1-n)` as closure remains forbidden.

Artifacts:

- `5162-Y5-R2FR-shared-mode-nested-transition-zoom-and-resolved-q-gate.md`;
- `scripts/Y5_R2FR_5162_shared_mode_nested_transition_zoom_q_gate.py`;
- `source-intake/functional_rg/5162/nested_force_operator_contract.csv`;
- `source-intake/functional_rg/5162/nested_force_analytic_controls.csv`;
- `source-intake/functional_rg/5162/nested_zoom_initial_diagnostics.csv`;
- `source-intake/functional_rg/5162/nested_zoom_run_summary.csv`;
- `source-intake/functional_rg/5162/nested_zoom_profile_samples.csv`;
- `source-intake/functional_rg/5162/nested_zoom_no_refit_scores.csv`;
- `source-intake/functional_rg/5162/resolved_q_selection_gate.csv`;
- `source-intake/functional_rg/5162/nested_grid_convergence_gate.csv`;
- `source-intake/functional_rg/5162/nested_boundary_silence_diagnostics.csv`;
- `source-intake/functional_rg/5162/machine_cog_inheritance.csv`;
- `source-intake/functional_rg/5162/source_provenance.csv`;
- `source-intake/functional_rg/5162/nested_transition_zoom_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5162_VALIDATION.csv`.

All `29/29` generated validations and the independent strict revalidation
pass. CSVs are structurally clean; JSON is strict; all source paths exist and
remain hash-identical; every row remains nonclaim; no `__pycache__` is kept;
and the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
Galaxy inputs were read-only and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5161

Checkpoint 5161 closes checkpoint 5160's non-phase-matched particle-resolution
loophole. The exact `64^3` periodic constrained pair is Fourier-resampled to
`96^3`, including correct even-grid Nyquist handling. Resampling the fine field
back to the coarse grid has maximum pointwise error
`3.552713678800501e-14`; the largest peak-constraint error is
`1.1102230246251565e-15`, and the fine power above the coarse Nyquist surface
is only `9.64402999770094e-32`. No short modes are added, so both runs represent
the same continuous initial universe rather than merely reusing a seed.

Both particle samplings use the identical `192^3` force mesh, 120 KDK steps,
box, target, signs and parent equations. Four nonlinear runs execute
`275251200` particle-step updates. The strict fine-versus-coarse comparison at
the common `155.841824557513 kpc` resolved radius gives:

```text
fixed-edge mass fractional difference = 0.015487167413585357;
velocity-squared log-RMSE              = 0.004321914431131502 dex;
density log-RMSE                       = 0.01797143585763045 dex;
outer-ratio absolute difference        = 0.02011875380712097;
particle-resolution gate               = PASS.
```

Thus the conditional outer result is not a particle-sampling artefact within
the shared coarse-mode branch. It is not yet universal: one antithetic pair is
not an ensemble and this gate deliberately excludes physical modes above the
coarse Nyquist scale. The frozen no-refit target scores remain conditional;
fixed-edge target mass ratios are `1.168--1.187` and velocity-squared target
log-RMSE values are `0.09198--0.09476` dex at the finer common force mesh.

The compact-edge failure also survives. None of four scores passes the
`p=2` edge gate; the smallest exterior/interior excess-density ratio is
`0.3349058700395164`, versus `<1e-3`. The target transition remains
`36.43917542575495 kpc`, below the current resolved radius, so `q_parent`
remains unscored.

The next resolution requirement is now quantitative. Three-cell resolution
of `R_n` requires force cells no larger than `12.146391808584983 kpc`. The
`9.973876771680832 Mpc` global box needs at least grid 822, hence a practical
`1024^3` force mesh. The current float64 PM layout has an estimated lower-bound
peak of `44.0390625 GiB`, making a uniform run unsafe on 32 GiB. A local box of
four edge radii needs only minimum grid 120, hence `128^3`. The next numerical
route is therefore an actual shared-mode nested force/particle zoom, with the
coarse field supplying exterior tides and the local correction resolving
`R_n`.

The machine-cog contract remains untouched. The local GR/Newton/Mercury zero
state, Maxwell stress and Poynting source are inherited from the same parent
law; only particle sampling of its occupied cosmological state changed. No
arena-dependent force or coupling was introduced.

Artifacts:

- `5161-Y5-R2FR-exact-shared-mode-particle-resolution-convergence-gate.md`;
- `scripts/Y5_R2FR_5161_exact_shared_mode_particle_convergence_gate.py`;
- `source-intake/functional_rg/5161/shared_mode_refinement_contract.csv`;
- `source-intake/functional_rg/5161/exact_phase_matching_audit.csv`;
- `source-intake/functional_rg/5161/shared_mode_initial_diagnostics.csv`;
- `source-intake/functional_rg/5161/shared_mode_PM_run_summary.csv`;
- `source-intake/functional_rg/5161/shared_mode_profile_samples.csv`;
- `source-intake/functional_rg/5161/shared_mode_no_refit_scores.csv`;
- `source-intake/functional_rg/5161/particle_resolution_convergence_gate.csv`;
- `source-intake/functional_rg/5161/transition_zoom_resolution_requirement.csv`;
- `source-intake/functional_rg/5161/inherited_PM_equation_controls.csv`;
- `source-intake/functional_rg/5161/machine_cog_inheritance.csv`;
- `source-intake/functional_rg/5161/source_provenance.csv`;
- `source-intake/functional_rg/5161/shared_mode_particle_convergence_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5161_VALIDATION.csv`.

All `35/35` generated validations and the independent strict revalidation
pass. CSVs are structurally clean; JSON is strict; all source paths exist and
remain hash-identical; every row remains nonclaim; no `__pycache__` is kept;
and the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
Galaxy inputs were read-only and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5160

Checkpoint 5160 replaces the rejected radial-only formation route with a
genuine periodic three-dimensional Vlasov--Poisson particle-mesh calculation.
It preserves the checkpoint-5156 CAMB plus Hu-FDM covariance, imposes the same
one-sigma UGC09133 top-hat constraint by an exact Hoffman--Ribak projection,
and evolves antithetic residual signs around one common conditional mean. No
profile or edge parameter is fitted after evolution.

The first execution correctly failed three controls. Rather than relaxing
them, the repaired run moves the start from `a=0.02` to `a=0.01`, preserving
the old logarithmic time resolution with 120 base and 240 doubled steps. The
largest initial density magnitude is `0.40797131771263784` and the largest
Zel'dovich displacement is `0.8919300470615931` particle cells. The old
single linear test had also confused finite CIC/central-difference attenuation
with a force-law error. The replacement controls separately show:

```text
homogeneous force                              = 0;
long-mode continuum-growth relative error     = 0.012598070153085006;
mode-2 finite-mesh response mu                 = 0.9496412035509973;
mode-2 error against independent mesh ODE      = 0.0013624899655244604;
mode-2 attenuation relative to continuum       = 0.04863231844988414.
```

The complete matrix contains 14 nonlinear runs and `652738560`
particle-step updates. At fixed `64^3` particle phases, the force/time gate
passes: fixed-edge mass-ratio span `0.08275028605275514` and exterior-ratio
span `0.03606682726265903`. The base three-mass runs place about
`1.203` times the frozen target motion mass inside the fixed edge and achieve
velocity-squared log-RMSE `0.03193--0.03252` dex without refitting. This is a
real conditional outer-halo result, not a universal halo claim.

The negative result is equally sharp. No run generates the checkpoint-5154
compact `p=2` edge: the smallest exterior/interior excess-density ratio is
`0.3094561286744944`, versus the declared `<1e-3` gate. Every target
transition radius is about `36.4 kpc`, while the present resolved radii are
`155.8--267.2 kpc`; `q_parent` therefore remains unscored rather than being
declared wrong. The `96^3` run adds short modes and is not phase-matched, so
full particle/ensemble convergence also remains open.

The machine-cog contract is unchanged. The same parent action, metric,
`G_N`, matter coupling and Maxwell/Poynting Hilbert source leave the local
GR/Newton/Mercury zero state untouched; only the occupied cosmological state
is evolved. The next defensible numerical leap is a nested shared-mode zoom
that resolves `R_n` while retaining an identical large-scale realization.
Only after that can `q_parent` be tested or a wave/density-matrix core route be
distinguished from a missing parent interaction.

Artifacts:

- `5160-Y5-R2FR-paired-3D-constrained-realization-particle-mesh-collapse-and-tidal-profile-gate.md`;
- `scripts/Y5_R2FR_5160_paired_3D_constrained_PM_collapse_gate.py`;
- `source-intake/functional_rg/5160/paired_3D_frozen_contract.csv`;
- `source-intake/functional_rg/5160/paired_realization_initial_diagnostics.csv`;
- `source-intake/functional_rg/5160/particle_mesh_run_summary.csv`;
- `source-intake/functional_rg/5160/paired_3D_profile_samples.csv`;
- `source-intake/functional_rg/5160/paired_mean_no_refit_scores.csv`;
- `source-intake/functional_rg/5160/particle_mesh_convergence_matrix.csv`;
- `source-intake/functional_rg/5160/particle_mesh_equation_controls.csv`;
- `source-intake/functional_rg/5160/machine_cog_inheritance.csv`;
- `source-intake/functional_rg/5160/source_provenance.csv`;
- `source-intake/functional_rg/5160/paired_3D_constrained_PM_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5160_VALIDATION.csv`.

All `31/31` generated validations and the independent strict revalidation
pass. Every generated row remains nonclaim; all CSVs are structurally clean;
JSON is strict; source hashes are unchanged; the galaxy input was read-only;
and the protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

## Authoritative current handoff - checkpoint 5159

Checkpoint 5159 stops treating nonlinear formation as a future label and
executes the first source-backed shell-crossing calculation. It freezes the
checkpoint-5156 Planck-normalized CAMB plus Hu-FDM covariance, conditions an
exact one-sigma top-hat peak, and evolves the cold spherical Vlasov sheet from
`a=0.02` to `a=1` without fitting `q_parent`, `R_n`, `R_edge`, `p`, mass or
profile amplitude after evolution.

The Gaussian conditional mean is

```text
sigma_R^2=integral dlnk Delta_X^2 W^2(kR),
delta_bar(q)=sigma_R Cov(delta_q,delta_R)/sigma_R^2.
```

The nonlinear KDK runner evolves

```text
dx/da=P/(a^3 E),
dP/da=F_delta/(a^2 E),
F_delta=-G[M(<|x|)-M_background(<|x|)]/H0^2
```

with a controlled Plummer denominator and enclosed mass re-sorted after every
shell crossing. The base execution contains six runs, 48,000 evolved shells
and 18,000 KDK steps over CamB, the deterministic maximum-`R_n/R_L` reference
UGC09133, and all three locked masses. Both parent mappings are scored against
the unchanged checkpoint-5154 profiles.

The strongest result is exact rather than numerical. In the spherical
conditional-mean branch,

```text
dL/dt=r cross (-grad Phi)=0,
L_initial=0  =>  L=0.
```

Radial shell crossing therefore cannot produce the positive isotropic
Eddington `f(E)` state constructed at checkpoint 5154. This rejects the radial
conditional mean as a full formation proof independently of resolution.

The numerical output is kept fail-closed. Homogeneous evolution has zero
measured drift and the early growing-mode control agrees with its independent
Zel'dovich prediction to `0.0032607463063611952`. However, the nonlinear
fixed-edge mass ratio spans `0.4667440830072318` and velocity log-RMSE spans
`0.5990970882923841` across the shell/time/softening ladder. The quantitative
`q` diagnostics are therefore **inconclusive** and are not used to reject
`q_parent`. All seven base/convergence controls do robustly fail the compact
`p=2` edge criterion: the smallest exterior/interior density ratio is
`0.20465370939473415`, versus the declared `<1e-3` compact-edge gate. Halo
support and edge density are scored after subtracting the homogeneous
cosmological background.

The machine-cog contract remains intact. No action coefficient, `G_N`, metric,
matter charge, Maxwell source or local parameter changed. The Cartesian zero
state remains the same GR/Newton/Maxwell branch, including Poynting momentum in
the common Hilbert source. Galactic occupation is tested only as another state
of that same law.

The next calculation is not another radial rerun. It must retain the residual
Gaussian covariance in paired constrained realizations and evolve a genuinely
three-dimensional tidal field. Only converged radii may be scored. A passing
3-D outer profile would still require a separate wave/density-matrix zoom for
core selection.

Artifacts:

- `5159-Y5-R2FR-source-backed-constrained-peak-spherical-Vlasov-collapse-and-profile-selection-gate.md`;
- `scripts/Y5_R2FR_5159_constrained_peak_spherical_Vlasov_collapse_gate.py`;
- `source-intake/functional_rg/5159/frozen_initial_value_contract.csv`;
- `source-intake/functional_rg/5159/spherical_Vlasov_run_summary.csv`;
- `source-intake/functional_rg/5159/nonlinear_profile_samples.csv`;
- `source-intake/functional_rg/5159/no_refit_profile_selection_scores.csv`;
- `source-intake/functional_rg/5159/collapse_convergence_controls.csv`;
- `source-intake/functional_rg/5159/radial_sheet_phase_space_theorem.csv`;
- `source-intake/functional_rg/5159/machine_cog_inheritance.csv`;
- `source-intake/functional_rg/5159/source_provenance.csv`;
- `source-intake/functional_rg/5159/constrained_peak_spherical_collapse_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5159_VALIDATION.csv`.

All `33/33` generated validations and an independent strict revalidation pass.
Every generated row remains nonclaim; CSVs are clean; JSON is strict; both
primary method archives are local and hashed; no `__pycache__` exists; and the
protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

## Authoritative current handoff - checkpoint 5158

Checkpoint 5158 applies the single-machine criterion directly: the parent law
must preserve the local GR/Newton/Maxwell and Mercury cog while allowing its
occupied motion state to activate the galactic cog. It therefore searches the
existing parent vertices for a regular clock-charge source instead of adding an
arena-dependent switch.

The search gives a sharp current-corpus no-go. For the checkpoint-4890 pair,

```text
L=-[(grad A)^2+A^2((grad theta)^2+m_X^2)]/2
  +kappa_mix grad(phi).grad(theta),
j_theta=-A^2 grad(theta)+kappa_mix grad(phi).
```

There is no undifferentiated `theta`, so phase-shift symmetry and conservation
of the closed total current are exact. The old clock-memory mix has
`dL_mix/dA=0`; the amplitude equation is homogeneous and its `A=0` residual is
zero. In Cartesian variables the displayed mix divides by `X_1^2+X_2^2` at the
origin. A regular completion therefore preserves the no-source result, while a
singular completion is inadmissible at the exact local vacuum.

The full source audit covers ten existing operator classes. Universal gravity
can create neutral `X+anti-X` pairs, but their signed charge sums to zero. The
Schwinger--Keldysh route can transfer a charge only from a parent-specified
oppositely charged bath, which is absent and whose full cosmological branch was
already retired. The real-scalar `X^2/X^3` hierarchy changes neutral occupation,
not signed `O(2)_X` charge. A tadpole would source the field only by breaking the
protective symmetry and reopening the local scalar source.

The resulting branch decision is:

```text
precharged complex clock = consistent global boundary/superselection sector,
                           not dynamically prepared;
neutral real motion state = least-additive active route;
next execution            = frozen, no-refit nonlinear collapse gate.
```

This is not a claim that the galactic cog is derived. It does establish that no
unsafe charge source has been smuggled in to obtain it. The exact Cartesian
vacuum, universal metric residue, Maxwell source and Poynting momentum remain
unchanged. The missing result is whether nonlinear evolution of one globally
fixed neutral state produces the parent activation, finite wave core and
`p=2` edge while inheriting the already locked local and linear-cosmology
limits.

Artifacts:

- `5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-state-pivot.md`;
- `scripts/Y5_R2FR_5158_clock_charge_source_symmetry_no_go.py`;
- `source-intake/functional_rg/5158/clock_charge_source_operator_audit.csv`;
- `source-intake/functional_rg/5158/clock_memory_modified_current.csv`;
- `source-intake/functional_rg/5158/neutral_pair_vs_signed_charge.csv`;
- `source-intake/functional_rg/5158/state_preparation_branch_decision.csv`;
- `source-intake/functional_rg/5158/source_provenance.csv`;
- `source-intake/functional_rg/5158/clock_charge_source_symmetry_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5158_VALIDATION.csv`.

All `25/25` checkpoint validations and an independent strict revalidation pass.
Every generated row remains nonclaim, every provenance path exists, no
placeholder or non-finite value is present, no `__pycache__` exists, and the
protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

## Authoritative current handoff - checkpoint 5157

Checkpoint 5157 attacks checkpoint 5156's state-preparation obstruction rather
than running a nonlinear collapse from a covariance already known to be
external. The corpus contains a source-derived checkpoint-4890 Cartesian pair

```text
Z=X_1+iX_2=A exp(-i m_X U).
```

Its polar decomposition has now been independently rederived. The exact
identities are

```text
(grad X_1)^2+(grad X_2)^2
 =(grad A)^2+m_X^2 A^2(grad U)^2,
J_X^mu=m_X A^2 u^mu,
u_mu=-grad_mu U,
div J_X=0,
(grad U)^2+1=Box A/(m_X^2 A).
```

Thus one occupied neutral pair can carry both a motion density and a WKB
proper-time flow. In its controlled branch `rho_X=m_X n_X`, `n_X a^3` is
constant and `p_X/rho_X=O(H^2/m_X^2)`. The largest executed equality pressure
proxy over the three locked masses is only `7.91715e-15`. Its nonrelativistic
envelope is the same checkpoint-5155 Schrodinger--Poisson field, not a new
galaxy force.

The local machine cog remains structurally intact. At `X_1=X_2=0` the
Cartesian action and pair stress vanish exactly; only the polar chart becomes
undefined. The internal `U(1)_X` is neutral and distinct from electromagnetic
`U(1)`, so Maxwell and Poynting momentum remain in the checkpoint-4947 Hilbert
source. The pair is only a re-entry candidate: checkpoint 4896 retired the
full bath cosmology and checkpoint 4897 remains the active metric-only
baseline. No retired diagonal bath continuum was restored.

The central new theorem is the charge-to-entropy adiabatic law. If a
post-inflation one-clock production surface supplies aligned separately
conserved currents

```text
J_X^mu=n_X u^mu,
s^mu=s u^mu,
```

then exactly

```text
u.grad ln(n_X/s)=0.
```

If the production yield `Y_X=n_X/s` is spatially uniform on that surface,
then

```text
S_Xgamma=delta ln(n_X/s)=delta_X-3 delta_gamma/4=0,
P_SS=P_RS=0.
```

This conditionally reduces the arbitrary Gaussian functions `n_k,c_k` to one
common curvature covariance, one global yield and bounded production noise.
For the three locked masses the required yield is
`4.39966e17 ... 1.56200e20`. The Planck 2018 scale-invariant uncorrelated CDI
bound `beta_iso(k=0.05/Mpc)<0.038` requires any independent fractional yield
noise to have rms below `9.10081e-6` for the checkpoint-5156 curvature
amplitude. The alternative real-misalignment spectator branch conditionally
requires `H_inf < 3.89344e11 ... 1.69005e12 GeV`.

There is also an exact obstruction. The isolated quadratic `U(1)_X` pair
cannot evolve `Q_X=0` into nonzero `Q_X`; a charge existing before 60
inflationary e-folds is density-diluted by `exp(-180)=6.71418e-79`. Therefore
the current active parent still does not own the state. It must derive either
a post-inflation boundary charge or a charge-asymmetric one-clock production
operator with sufficiently small noise. Symmetric gravitational pair
production cannot be relabelled as net charge. If no such source exists, this
clock-charge re-entry is to be rejected rather than completed by closure.

With the same `m_X`, `Omega_X` and a genuinely adiabatic production state, the
checkpoint-5156 transfer and patch results are inherited without refitting:
all `1050/1050` frozen-covariance patches retain the one-sigma linear mass
supply. The nonlinear `q_parent` profile, finite wave core and `p=2` edge are
not inherited and remain unproved.

All `28/28` validation gates pass. Source hashes are unchanged, all generated
rows remain nonclaim, no placeholder markers occur, and the protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

The next derivation target is concrete: search existing parent vertices for a
post-inflation charge-asymmetric source whose rate depends only on the same
clock and whose stationary/local residue vanishes. If that source closes,
execute the frozen no-refit Vlasov-volume plus wave/density-matrix zoom and
score `q_parent`, core and edge directly. If it does not, reject the
clock-charge branch and return to the real-scalar state boundary explicitly.

## Authoritative current handoff - checkpoint 5156

Checkpoint 5156 goes after checkpoint 5155's initial-state obstruction rather
than merely relabelling it. The machine-cog criterion is retained: one
checkpoint-4947 Einstein metric and Hilbert source governs local
GR/Newton/Maxwell and the cosmological/galactic motion state. No galaxy-only
force, second metric or arena switch was introduced; Poynting momentum remains
inside the same electromagnetic stress tensor.

On spatially flat FLRW, conformal flatness gives `C_mnrs=0`. The retained
`u_O4 C^2 (nabla psi)^2` portal therefore drops out of the homogeneous
quadratic motion operator, leaving the ordinary massive scalar plus the same
Einstein constraints. For `v=a sqrt(Z_psi) delta psi`, the free mode operator
is

```text
v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=metric-constraint source.
```

During radiation domination `a''=0`; after coherent oscillation the same
Hessian gives the scale-dependent WKB sound speed

```text
c_X^2=[k^2/(4m_gap^2 a^2)]/[1+k^2/(4m_gap^2 a^2)].
```

The action-versus-state boundary is now an exact theorem. Canonical dynamics
fixes the mode basis and Wronskian, but a homogeneous positive Gaussian CTP
state retains independent occupation and squeezing functions `n_k,c_k`, with

```text
n_k>=0,
|c_k|^2<=n_k(n_k+1).
```

The same Hessian therefore admits infinitely many statistical covariances.
The reflection-even `+/-psi_i` mixture removes odd scalar charge but cannot
select `P_delta(k)`. A parent density-matrix or cosmogenesis boundary law is
mathematically required to predict amplitude, tilt and motion isocurvature.

One exact economical branch is identified. If every component descends from
one physical clock perturbation, then

```text
delta rho_i/rho_i'=delta rho_j/rho_j',
S_Xgamma=delta_X-3 delta_gamma/4=0.
```

Before motion oscillation, `w_X -> -1` and the source-derived adiabatic mode
has `delta_X=u_X=0` at leading superhorizon order. The present corpus does not
yet derive the single-clock cosmogenesis premise, so `P_S=P_RS=0` is not
promoted to an MTS prediction.

Concrete formation evidence was nevertheless calculated with one global,
source-backed, explicitly nonclaim adiabatic covariance. CAMB 1.6.6 supplies
4096 full photon/baryon/neutrino/metric baseline modes normalized to
`n_s=0.965`, `sigma8=0.811`. The top-hat reconstruction gives
`sigma8=0.811101`. The Hu--Barkana--Gruzinov full radiation-era FDM transfer
was then applied at all three locked masses. Parent and published equality
Jeans scales agree within `0.4286%`; numerical and published half-power scales
agree within `2.3081%`.

All 1050 checkpoint-5155 Lagrangian patches were integrated against the full
linear spectrum. Their minimum sigma is `1.95443`, exceeding the spherical
collapse threshold `1.686`; the largest peak height is only `0.862654`.
Every row is therefore inside the one-sigma collapse threshold by `z=0` under
this single empirical covariance. Even the strict mass has no patch below its
half-mode radius. Linear wave suppression does not erase the required mass
supply. This does not prove a particular patch occurred or that nonlinear
evolution selects the MTS projective profile.

All `26/26` validation gates pass. High-k truncation changes patch sigma by at
most `1.38e-6`. The protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

The next decisive numerical target is a no-refit hybrid formation run seeded
by this one frozen global covariance: a Vlasov cosmological volume plus
wave-resolved zoom/core regions, scored against the parent `q`, finite core,
`p=2` edge and conserved rotation/lensing stress. In parallel, the derivation
target is a parent state-preparation law that predicts the curvature/entropy
covariance rather than borrowing it. The actual infrared `c_ess` and the
nonlinear projective-profile attractor remain open.

## Prior authoritative handoff - checkpoint 5155

Checkpoint 5155 turns the checkpoint-5154 equilibrium into a genuine
initial-value question under the user's machine-cog criterion. The same
rank-one metric source that preserves local GR/Newton/Maxwell gives the
weak-field Schrodinger--Poisson equations and their smooth-scale
Wigner--Vlasov limit. No galaxy-only force, second metric, direct scalar charge
or arena switch was introduced. Electromagnetic energy and Poynting momentum
remain in the same Hilbert stress tensor.

The controlled parent limit is

```text
i hbar partial_t Psi_c
 =-hbar^2 nabla_x^2 Psi_c/(2m a^2)+m Phi Psi_c,
nabla_x^2 Phi
 =4pi G_N a^2(delta rho_b+delta rho_EM+delta rho_X),
```

with linear density equation

```text
ddot delta+2H dot delta
 +[hbar^2 k^4/(4m^2a^4)-4piG rho_m]delta=0.
```

The Wigner equation approaches Vlasov--Poisson with correction
`O[(hbar/(m v L))^2]`. The checkpoint-5154 `p=2` isotropic state is exactly
stationary under that Vlasov flow because `f=f(E)` gives
`{f,H}=f'(E){H,H}=0`. This establishes an equilibrium candidate, not its
cosmological formation.

An exact obstruction is now proved rather than recorded as a missing input.
An exactly homogeneous reflection-even `+/-psi_i` mixture, evolved under
deterministic translation-invariant parent equations with a unique solution,
remains homogeneous. Its mean abundance cannot manufacture a nonzero spatial
two-point function. Halo formation therefore mathematically requires one
global primordial covariance `P_delta(k)>0` (or equivalent parent 2PI initial
kernel); inserting arbitrary numerical noise would be a hidden closure.

The executable post-equality transfer gate covers all three locked masses, 320
scaled modes per mass and all 1050 finite halo patches. RK4 refinement changes
power by at most `1.07e-10`; the three curves agree as functions of
`k/k_J,eq` to `1.67e-15`. Their half-power crossing is
`k/k_J,eq=0.898453`. The conservative patch mode has maximum
`k/k_J,eq=0.486514` and minimum present power ratio `0.944916`; all patch
modes therefore survive this late gate. This is post-equality dynamics, not a
radiation-era Boltzmann or primordial-amplitude claim.

A real 3D periodic Strang split-step runner was executed at
`k/k_J,eq=0.7,1.3` for all three masses. The six physical runs match the
independent linear ODE to at worst `1.5732e-6`; base-run norm drift is at most
`7.77e-15`. The strict-mass 24/32/40 grid-time comparison has relative spread
`1.7906e-6`. This validates the wave-equation plumbing in the linear regime,
not the nonlinear profile attractor.

The multiscale route is now fixed by calculation. At the strict mass,
`316/350` rows are below a one-percent Wigner correction at every observed
radius, while the maximum observed proxy is `0.255782`; the core cannot be
silently deleted. A full-edge wave box would require at least `15445^3` cells
and approximately `214 TiB` working memory. The target coherent scaling
invariant spans `9.02e9`, excluding one universal rescaled isolated soliton.
The honest candidate is therefore a cosmological Vlasov volume with
wave-resolved zoom/core regions.

All `24/24` checkpoint validations pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

The next decisive calculation is not another equilibrium rewrite. Derive the
gauge-invariant quadratic scalar perturbation/2PI initial kernel from the same
parent FLRW Hessian, determine whether it supplies one normalized adiabatic or
isocurvature covariance without per-galaxy freedom, propagate that covariance
through the radiation-era transfer, and only then seed the hybrid
Vlasov-plus-wave collapse test. The actual parent `c_ess` coefficient and the
nonlinear projective-profile attractor remain open and must not be claimed.

## Prior authoritative handoff - checkpoint 5154

Checkpoint 5154 applies the user's machine-cog criterion directly: one parent
metric source must preserve the local GR/Newton/Mercury limit while the same
source remains active on galactic scales. No arena switch, galaxy-only
coupling or per-galaxy outer-edge parameter was introduced.

The checkpoint-5153 sharp isotropic edge is now rejected exactly. For relative
potential `Psi` and any locally integrable nonnegative isotropic distribution,

```text
rho(Psi)=4pi sqrt(2) integral_0^Psi f(E)sqrt(Psi-E)dE,
0<=rho(Psi)<=4pi sqrt(2Psi) integral_0^Psi f(E)dE ->0.
```

Therefore a finite nonzero interior density step at the escape boundary cannot
come from a regular isotropic `f(E)`. The circular `p_r=0` Einstein-cluster
comparison remains mathematically separate; it may not be relabelled as an
isotropic phase-space state.

For the universal edge family

```text
E_p(y)=(1-y^2)^p_+,  y=r/R_t,
rho~Psi^p,
f(E)~E^(p-3/2),
```

bounded escape-energy phase density requires exactly `p>=3/2`. The `p=3/2`
member is the least-suppressed bounded comparator. Adding the declared
requirements of an even polynomial in `y`, a regular centre and a `C1` vacuum
join selects the first candidate `p=2`, with `f~sqrt(E)` at escape. This is a
minimal regularity selection inside that class, not yet a coefficient produced
by parent collapse.

The unchanged metric-only spherical-collapse condition gives

```text
X^3=2[v_infinity/(H0 R_n)]^2 I_p(X)/(f_X Delta_vir,c),
I_p(X)=integral_0^X [S+xS'](1-x^2/X^2)^p dx.
```

All 350 parent/galaxy rows at the three locked masses were executed for both
`p=3/2` and `p=2`: 2100 phase-space states. A new exact-CDF spectral quantile
quadrature removes the broad-log normalization loss; its maximum independent
support disagreement against the checkpoint-5153 order-1536 integration is
`6.90e-7`.

The Eddington/Abel equation was inverted rather than circularization being
assumed. Every one of the 1050 `p=3/2` distributions is positive, but none
passes the global monotone-relative-energy sufficient stability sign. Every
one of the 1050 universal `p=2` distributions is positive and monotone. The
worst independent midpoint reconstruction error below normalized energy
`0.999` is `0.00181764`; worst-case profiles retain both signs at energy orders
64, 128 and 256. This is a discrete existence/stability-sign certificate, not
a nonlinear stability theorem or a relativistic Einstein-Vlasov solve.

The selected finite radii span `R_t/R_n=9.92665--96.52895`. The virial identity
closes to `1.42e-13`, edge density, density slope and isotropic pressure vanish,
and maximum boundary compactness is `2.88e-7`. The revised primordial patches
remain above the instantaneous equality Jeans gates by at least factors
`69.47` in mass and `2.055` in radius.

The no-refit radial smoke again covers both mappings, three masses, all 175
galaxies and 3391 radii: 20346 point evaluations. Every point lies inside the
smooth edge; the maximum `r_obs/R_t` is `0.29952`, maximum support displacement
from the unregularized parent is `0.06237`, and the largest pooled RMSE change
is `+0.16485 km/s`. The largest individual-galaxy absolute RMSE change is
`1.11457 km/s`. Thus smoothing costs a small amount at this unweighted
interface but does not jam the galaxy cog or obtain regularity by refitting it.

Because `0<=E_2<=1`, the smooth density and enclosed motion source cannot
exceed the untapered local source. The inherited embedded-halo tide ceiling is
`6.61e-19` at Mercury and `3.10e-13` over the checked Solar-System orbits;
direct scalar fifth force remains zero on the same reflection-even
universal-metric branch. This is conditional local-cog compatibility, not a
replacement for the full PPN and pulsar likelihoods.

The route decision is
`POSITIVE_UNIVERSAL_ISOTROPIC_STATE_EXISTS_ADVANCE_TO_FIXED_COLLAPSE_ATTRACTOR_RUN`.
The next calculation is not another source ledger. Derive and dry-run the
fixed checkpoint-5152 primordial Schrodinger--Poisson/Vlasov initial-value
problem at the three locked masses, with no fitted `q`, edge or core. Measure
whether coarse-graining approaches the projective `p=2` family. Failure makes
the smooth edge an explicit closure; success supplies the missing formation
mechanism. A fully relativistic Einstein-Vlasov continuation, flattened
rotating state, lensing likelihood and primordial perturbation probability
remain open. All 25 validations pass. The protected `formalization-workbench`
hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
The galaxy corpus was read-only and no GitHub action occurred.

## Authoritative current handoff - checkpoint 5153

Checkpoint 5153 closes the finite-core and finite-mass *existence* problems
conditionally without changing the parent `q` profile or inserting a fitted
halo function. It starts from the exact positive Stieltjes mixture at 5151,
uses the 5152 mass/WKB hierarchy for its inner cutoff, and uses the unchanged
metric-only cosmological baseline for its outer virial boundary.

For `alpha=q/2`, the lower-cut mixture is

```text
S_q,c(x)=N_q(t_min)^(-1)
 integral_tmin^infinity dt [x^2/(x^2+t)]rho_q(t),

t_min=(r_c/R_n)^2=(m_WKB,row/m_gap)^2,
N_q=1-F_q(t_min).
```

Every retained kernel is positive and cored. The construction proves
`S(0)=0`, `S(infinity)=1`, `S'>0`, positive density, positive circular
epicyclic factor and finite
`rho(0)=3v_infinity^2<1/t>/(4piG R_n^2)`. It is parameter-free within this
declared lower-cut prescription after `m_gap` is fixed, but nonlinear wave
dynamics has not yet selected the hard cutoff or its coefficient.

All 350 parent/galaxy rows were executed at the strict WKB mass,
`1e-20 eV` and `1e-18 eV`, giving 1050 finite states. At least
`0.9988461464454078` of the positive spectral weight is retained. The maximum
`r_c/R_n` is `0.1`; central densities are
`0.007606819858269044--0.6496827104087403 Msun/pc^3`. The independent
adaptive-integral disagreement is `1.21e-12`.

The flat baseline spherical-collapse value is

```text
Delta_vir,c(z=0)=103.18310421960845,
f_X=Omega_X/Omega_m=0.8436724083687603.
```

Combining it with the exact circular-state relation
`w=GM_X/(c^2r)=beta/(1+2beta)` gives the unique positive virial root

```text
r_vir^2=2v_infinity^2 S_q,c(r_vir/R_n)
 /[f_X Delta_vir,c H_0^2(1+2beta_vir)].
```

Cutting the zero-radial-pressure circular state at this orbit and continuing
with Schwarzschild mass gives a finite compact-support equilibrium. The
metric/compactness junction residual is `5.29e-23`; the virial-density
identity residual is `4.22e-15`. The smallest `r_vir/R_n` is `13.8788`, all
measured radii are below `0.2142 r_vir`, and finite motion masses span
`7.0396e9--5.9466e12 Msun`. The sharp edge is permitted for this circular
state but its smooth formation profile remains unproved.

Each halo now maps to a finite primordial supply patch

```text
R_L=[3M_X/(4pi rho_X,0)]^(1/3),
N_X=M_X/m_gap.
```

The patches span `0.368789--3.486197 Mpc` and contain
`7.8523e93--2.35494e99` quanta. Every patch exceeds the instantaneous
equality Jeans gate: minimum `M_total/M_Jeans=178.57` and minimum
`R_L/lambda_Jeans=2.8156`. This bypasses the rejected local multiplicity
cascade by primordial inventory; it does not derive the primordial power or
collapse probability.

The no-refit radial execution covers three masses, both parent mappings, all
175 galaxies and all 3391 radii: 20346 point evaluations. The largest support
change is `9.77893e-4`, the largest per-galaxy RMSE change is
`0.00814 km/s`, and no point reaches the outer boundary. Thus physical
regularization does not break the existing galaxy cog.

The route decision is
`FINITE_STATE_FAMILY_CONSTRUCTED_ADVANCE_TO_PHASE_SPACE_AND_COLLAPSE_ATTRACTOR_GATE`.
The next calculation is not another source ledger: invert the finite density
and metric to a nonnegative isotropic Eddington/Vlasov distribution, compare
it continuously with the known circular anisotropic limit, and test
radial-orbit stability. If a positive finite distribution exists, proceed to
the three-mass nonlinear collapse run; if not, demote this route. Parent
selection of `C_n,n_q`, the primordial perturbation spectrum, smooth edge,
flattened state and lensing likelihood remain open. All 24 validations pass.
The protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
The galaxy sample was read-only; no GitHub action occurred.

## Authoritative current handoff - checkpoint 5152

Checkpoint 5152 applies the user's one-machine/two-cog criterion directly.
It retains the same metric-plus-motion parent action for local GR and galaxy
states, with all ordinary, electromagnetic (including Poynting momentum) and
motion stresses entering one Hilbert tensor. No galaxy-only coupling or arena
switch is introduced.

The already-executed 4949 and 4953--4959 calculations reject static local
population and the controlled high-frequency formation/cascade routes. The
new calculation therefore tests the distinct primordial-state route. An
even CTP mixture of the `+psi_i` and `-psi_i` homogeneous representatives has
`<psi>=0` and all odd correlators zero while retaining their positive
quadratic stress. It bypasses local particle manufacture without undoing the
reflection-even no-direct-fifth-force branch.

In exact radiation domination the regular massive solution is

```text
psi/psi_i=2^(1/4) Gamma(5/4) (m t)^(-1/4) J_(1/4)(m t).
```

Its late stress has `<p>=0`, `rho proportional a^-3` and exact matching
coefficient `C_RD=4 Gamma(5/4)^2/pi=1.0460496200531022`. The executed
Klein--Gordon residual is `4.44e-16`, late-cycle averaged `w=1.47e-3`, and
the comoving-energy asymptotic error at `mt=1e6` is `5.27e-8`.

The motion component replaces conventional CDM rather than being added to
it: `Omega_X=Omega_m-Omega_b=0.2657568086361595`. At the checkpoint-5151
all-galaxy WKB floor `m=2.81669166215576e-22 eV`, oscillations begin at
`z=4.5443458e6`, the exact radiation matching requires
`psi_i=0.0431687721 Mbar_Pl`, motion is only `6.50e-4` of radiation at onset,
and the largest transition-era background shift is `2.94e-4` in `H`.

The nonrelativistic perturbation equation and Jeans scale are now explicit:

```text
ddot(delta)+2H dot(delta)
 +[hbar^2 k^4/(4m^2a^4)-4piG rho]delta=0,
k_phys,J^4=16piG rho m^2/hbar^2.
```

At the marginal WKB mass the equality comoving Jeans wavelength is
`0.4142000432 Mpc` and its Jeans-sphere mass is `1.477632934e9 Msun`. The
strict all-350-row collisionless requirement is
`m>=2.8166916621557602e-21 eV`. Requiring additionally an instantaneous
equality Jeans wavelength below `100 kpc` gives the joint internal lower
benchmark `m>=4.8323634180988915e-21 eV`. The chosen next-run benchmark
`1e-20 eV` has `lambda_J,com(eq)=0.0695152 Mpc`,
`M_J(eq)=6.9851466e6 Msun`, and maximum `lambda_db/R_n=0.0281669` over all
350 parent/galaxy rows.

For the parent `c_ess X^2` term, quadratic control is no longer merely named:
`|c_ess|X_osc<epsilon`, with `X_osc approximately (m psi_i)^2/2`. Across the
mass grid, one-percent control needs an equivalent suppression scale above at
most `9.813 keV`; a Planck-natural comparator has maximum
`|c_ess|X=2.64e-96`. The actual infrared parent coefficient remains to be
transported.

The local cog remains suppressed under the same law: no direct scalar fifth
force, maximum inherited halo-tide/solar ratio `3.10045e-13`, homogeneous
motion-density Mercury ratio `9.28e-25`, and maximum diagnostic oscillating
metric potential `6.12e-19` for `0.3 GeV/cm^3`. These are not a replacement
for a full PPN or pulsar-timing likelihood.

The route decision is
`PRIMORDIAL_REFLECTION_EVEN_STATE_SURVIVES_CONDITIONALLY_ADVANCE_TO_NONLINEAR_COLLAPSE`.
This is a genuine source-route advance, but not a full MTS claim. The one
global initial abundance, primordial perturbation/isocurvature spectrum,
infrared higher-operator coefficients, nonlinear production of `C_n` and
`n_q`, finite core/outer boundary, flattened state and lensing likelihood are
not derived. Until nonlinear collapse selects the checkpoint-5151 profile,
the background branch remains indistinguishable from ordinary ultralight
scalar dark matter.

The next calculation is therefore fixed rather than another source ledger:
derive the Schrodinger--Poisson/Vlasov initial-value problem at the strict WKB
floor, `1e-20 eV` and `1e-18 eV`, then test whether one global primordial
spectrum and the parent interaction generate the `q_parent` phase profile,
`C_n` scaling, finite core and finite outer boundary without per-galaxy shape
fits. If not, demote the galaxy state route to scalar-halo closure. All 23
validations pass; the protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub or galaxy-repository write occurred.

## Authoritative current handoff - checkpoint 5151

Checkpoint 5151 takes the direct conserved-state route selected after the
minimal common-propagator rejection and constructs an actual stationary
stress realization. In the collisionless WKB limit, a reflection-even CTP
two-point occupation has positive kinetic stress
`Delta T^munu=integral dPi p^mu p^nu f`, obeying
`p^mu nabla_mu f=0` while `<psi>=0`. A stationary axisymmetric distribution
may be a function of orbit integrals; the explicit spherical circular-orbit
member is a nontrivial axisymmetric existence solution, not yet the selected
flattened galaxy state.

For every `0<q<2`, the projective phase is proved to have the exact positive
cored-profile representation

```text
n_q(x)=x^q/(1+x^q)
      =integral_0^infinity dt [x^2/(x^2+t)] rho_q(t),

rho_q(t)=sin(pi q/2) t^(q/2-1)
 /{pi[1+2t^(q/2)cos(pi q/2)+t^q]}.
```

Both parent Hessian exponents `1.8496934455116607` and
`1.858483853942984` lie in this positivity window. The numerical mixture
reconstruction has maximum relative error `2.70e-15`. Every component is a
regular cored flat-rotation density. Their unique continuum has only a mild
integrable `rho proportional r^(q-2)` central cusp for the parent values and
a force that vanishes as `r^(q-1)`.

One global conversion from phase radius to the existing empirical support,
with no per-galaxy shape fit, gives the best parent branch

```text
q_parent=1.8496934455116607,
a=1.7271465744325227,
R_n/L_eff=0.578989655425489,
shape RMSE=0.06514699919477658.
```

This is comparable to the now-rejected 5148 propagator shape RMSE
`0.0616004223044119` while retaining the parent exponent near `1.85` rather
than relabelling it as the empirical `0.77`. It fixes the source-scaling
target `C_n=(xi ell_gap a/L_eff)^q_parent`. Transport of that critical
exponent down the occupied infrared trajectory remains to be derived.

The isolated circular state has exact conserved stress and two metric
functions

```text
p_r=0,
w=Gm/(c^2r)=beta/(1+2beta),
B=1+2beta,
d ln A/d ln r=2beta,
p_t=rho c^2 beta/2,

A(r)/A(L_eff)
 =[(1+(a r/L_eff)^q)/(1+a^q)]^(2 beta_infinity/q).
```

Density positivity, weak circular stability, dominant energy and all exact
mass/metric/conservation identities pass. In a baryonic galaxy the motion
state orbits in the total metric, so the exact isolated formulas are used as
an existence theorem and the full ROTMOD pass uses the total weak velocity
for its pressure scale rather than pretending to be an exact disk solution.

The read-only execution covers all 175 galaxies and 3391 radii. The best
parent phase support has mean unweighted RMSE `21.024301108192173 km/s`
versus `21.889021670909763 km/s` for the locked exponential baseline, pooled
RMSE `33.48575685418064` versus `33.75732021897959 km/s`, and wins `121/175`.
This is a promising interface smoke, not an uncertainty-weighted galaxy
claim. Maximum total `v^2/c^2=1.2191437962544262e-6`, so the motion tangential
stress and leading pressure-sensitive lensing order are tiny.

The universal WKB requirement is now bounded: resolving every transition
radius needs `m_gap>=2.81669166215576e-22 eV`, or ten times that for
`lambda_db<=0.1 R_n`. At the declared embedded location `R_host=L_eff`, the
worst Mercury halo-tide/solar ratio is `6.614360568718464e-19`; the classical
scalar fifth force remains zero. This is not a full Solar-System PPN bound.

The remaining decisive work is dynamical rather than another stress ansatz:
derive the source-selected `C_n` and total occupation from the galaxy-formation
CTP kernel with one `J_gap`, carry the parent exponent to the infrared, and
derive finite central and outer boundaries. Without those results the route
is only collisionless scalar halo matter under another name. A full flattened
axisymmetric solution and projected lensing likelihood follow only after that
source step. All 21 validations pass. The protected `formalization-workbench`
hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub or galaxy-repository write occurred.

## Prior handoff - checkpoint 5150

Checkpoint 5150 performs the first explicit occupied-state calculation against
the checkpoint-5148 machine/cog response target. It grants the minimal
homogeneous `P(X)` route its most favorable gapless limit. The current parent
motion vacuum has positive `m_gap^2`; retaining that gap would only strengthen
the analytic/gapped obstruction found here.

For a timelike homogeneous state, the quadratic scalar coefficients are

```text
Z_t=P_X+2 Xbar P_XX > 0,
Z_s=P_X > 0,
c_s^2=Z_s/Z_t > 0.
```

Isotropy and the TT projection make the tree-level scalar--TT mixing vanish.
The remaining tree Hessian is rational and analytic in `k^2`, so it cannot
produce the required nonanalytic `|k|` response by itself.

The exact static zero-mode calculation uses
`T_xy=partial_x(phi) partial_y(phi)`. Dimensional regularization gives one
contraction coefficient `|k|^3/1024`, connected TT correlator
`W_state |k|^3/512`, and, from the metric vertex
`S_int=(1/2) h_xy T_xy`, the effective metric-Hessian contribution

```text
Delta K_TT = -W_state |k|^3/2048.
```

After any analytic `k^2` term is tuned to criticality, this sign is opposite
to the positive `+M_R^2 |k|^3/(A mu)` coefficient required by the stable 5148
common-propagator kernel. Therefore the minimal homogeneous passive `P(X)`
realization of that common no-slip/TT dressing is rejected. This is a scoped
result: it does not reject all motion-state stress responses or the exact
local `psi=0` branch.

As a magnitude-only diagnostic, the 175-galaxy interface median
`L_eff=9.29254645998695 kpc` gives `mu=2.0104429740702643e-27 eV`; matching the
kernel coefficient would require
`N_eff W_state=5.649324663894458e84 eV`. The sign already fails, so this number
is not evidence for a fit or a physical inferred population.

The selected next route is now a direct conserved motion-state Hilbert stress,
not another universal propagator dressing. The next calculation must derive a
stationary axisymmetric CTP state stress and solve for both metric potentials,
testing rotation and lensing together while the unoccupied local branch remains
exactly GR. Occupation, anisotropic stress and any Poynting/wave contribution
must arise from the same parent state and conservation equations; none may be
inserted as an arena switch. All 12 validations pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub or galaxy-repository write occurred.

## Prior handoff - checkpoint 5149

Checkpoint 5149 tests whether the constructive 5148 kernel can be a healthy
parent response. For `s=k^2`,

```text
C_q(s)=mu^(1+q)/[sqrt(s)(s^(q/2)+mu^q)]
```

has the exact Stieltjes density

```text
rho_C(t)=mu^(1+q)[mu^q+t^(q/2)cos(pi q/2)]
         /{pi sqrt(t)[mu^(2q)+2mu^q t^(q/2)cos(pi q/2)+t^q]}.
```

For `0<q<=1`, including the locked `q=0.77`, this density is positive. A
numerical integral reconstructs `C_q` over twelve decades in `s/mu^2` with
maximum relative error `5.98642246885106e-11`. The candidate kernel therefore
admits a causal retarded oscillator-continuum response in principle; it is
not merely a shape written in momentum space.

The physical transverse vacuum-propagator interpretation fails cleanly. If
`D_vac=[1+A C_q]/(M_R^2 s)`, its continuum Kallen--Lehmann density away from
the massless pole is `rho_D=-A rho_C/(M_R^2 t)<0`. The 5148 form is therefore
rejected as a fundamental Lorentz-invariant vacuum modification. It may only
survive as a state-dependent motion-medium susceptibility for which the full
metric-plus-medium system owns positivity.

The exact Schur-complement mixing fraction

```text
zeta=A C_q/(1+A C_q)
```

has measured ultraviolet slope `-1.7696613135637107`, matching
`-(1+q)=-1.77`, and `1-zeta` has infrared slope
`1.0002827701968626`, matching the required `+1`. At the lowest executed
momentum `zeta=0.9999999064675871`. Thus flat rotation is not obtainable from
a small loop correction: the occupied galaxy state must approach a critical
unit-mixing determinant, `det Gamma2 proportional to |k| K_h K_chi`, while
the local `psi=0` branch remains at `zeta=0`.

The current stationary checkpoint-4949 motion vacuum is gapped, positive and
has `B=0`. More generally, a finite local gapped Hessian is analytic in `k^2`
and cannot generate the required `|k|` term. That route is now rejected. The
only surviving realization is an occupied gapless/critical CTP collective
state with a transverse nonanalytic stress response; its full spectral and
gradient matrix must remain positive and free of Jeans instability.

The next calculation is the actual smallest occupied-state `P(X)` Hessian
and retarded stress polarization. It must derive, not assume, the critical
unit-mixing limit and the `|k|` correction. Time-dependent Poynting or
gravitational flux may enter only through this same correlator; stationary/DC
activation remains excluded. All 13 validations pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub or galaxy-repository write occurred.

## Prior handoff - checkpoint 5148

Checkpoint 5148 returns from coefficient-pipeline work to the physical
machine/cog problem. Checkpoints 4942-4943 already give an exact
reflection-even `psi=0` local branch, while 4960 gives one universal public
metric source. The physical metric-motion Hessian can therefore be organized
as a single parent block matrix with effective metric kernel
`K_eff=K_h-B K_chi^-1 B_dagger`. On the certified local branch `B=0`, so the
Einstein/Newton/Mercury response is unchanged. A nonzero motion state can
activate the same Schur complement without adding a second gravitational
coupling, but the state itself must still be derived.

The two required radial limits now determine a concrete response target.
With `y=mu/k` and the exact projective occupation
`n_q=y^q/(1+y^q)`, the no-new-scale monomial class `y^a n_q^b` has a unique
minimal member that gives both inner `Delta V^2 proportional to r^q` and an
outer flat plateau: `C_q=y n_q=y^(1+q)/(1+y^q)`. The candidate static
propagator and equivalent self-energy are

```text
D_h=D_GR[1+A C_q],
Sigma/K_h=A C_q/(1+A C_q),
K_eff=K_h/(1+A C_q).
```

For `A>=0` and Euclidean `k>0`, the static kernel is positive and has no new
zero. Its high-frequency correction falls as `(mu/k)^(1+q)`, while the
low-frequency correction is `mu/k` and therefore generates a `1/k^3`
static Green function. The exact Fourier transform gives
`Delta V^2=(2 A G M mu/pi) S_q(mu r)`, with
`S_q(x)=0.7907858771245267 x^q+...` locally and `S_q->1` at large radius.
Thus one response can leave Mercury alone and produce a flat galactic
plateau; it is not a hand-selected change of force law by arena.

For the galaxy-locked `q=0.77`, one global spectral/real conversion
`mu L_eff=2.921396974200681` maps the derived support to the current canonical
`1-exp[-(r/L_eff)^q]` shape with RMSE `0.0616004223044119`. A read-only smoke
over all 175 LTGs uses the galaxy lab's exact `L_eff` construction and the
outer proxy `GM_proxy=Vbar_out^2 r_out`. The implied dimensionless response
amplitude has geometric mean `1.0691523388681814`, median
`1.109102407624266`, 16--84 percent range
`[0.5320173994224269,2.171141304980281]`, and `116/175` rows lie within a
factor two of unity. The source/scale log relation has Pearson
`r=0.9308544875726481`, but slope `0.8009552174166118 +/-
0.023903426418726347` and material scatter, so this is promising interface
evidence rather than a galaxy pass.

Using the largest inferred `A` and smallest `L_eff` together gives a
conservative Mercury static-kernel force correction
`2.1134587844508184e-14`. Poynting stress continues to enter the same Hilbert
source, but checkpoint 4952's exact stationary/DC no-pair-source result is
retained; electromagnetic flux is not inserted as an activation switch.

The sole next derivation is now sharply defined: calculate the retarded
state-dependent motion polarization `B K_ret^-1 B_dagger` from the actual
parent CTP Hessian and test whether it yields the required transverse
`A C_q/(1+A C_q)` self-energy. That calculation must also derive the state
laws for `A` and `mu`, explain the numeric `q=0.77`, and pass causal spectral,
lensing/slip and PPN gates. If it fails, this route is rejected rather than
kept as closure. All 15 checkpoint validations pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub or galaxy-repository write occurred.

## Prior handoff - checkpoint 5147

Checkpoint 5147 applies the checkpoint-5146 conditioned finite-annulus
global-cycle rule to the remaining unconverged E020/A10 row while retaining
its argument-local chart construction and the checkpoint-5142 KLT
simple-pole proof. All four charts now pass the numeric Laurent-order checks,
so the exact certificate is a verified backstop but is not invoked. This is
the zero-certificate case explicitly allowed by the parent checkpoint-5143
semantics; every non-order root, reciprocal-root, residue and regular-part
check remains mandatory.

The first fail-closed pass exposed an error in checkpoint 5147's wrapper: it
required exactly one certificate even when every chart passed numerically.
The numerical ladder itself had passed. The wrapper now mirrors the parent
rule: at most one exact certificate is allowed, and zero is valid only when
all charts were numerically accepted. No tolerance, interval cap, physics
parameter or numerical threshold was changed.

The locked 96/192 inner-node ladder passes both strict outer gates using 67
composite intervals. The maximum adaptive relative errors are
`2.5704974972112284e-05` and `2.570495337356024e-05`, both below the unchanged
`5e-5` tolerance. The corrected values agree to relative difference
`7.386270871118726e-12`; the selected value is
`2.7045874510128503-0.9217389861269736i`. No removable-extension or annulus
fallback is used, residues remain stable and all selected annuli satisfy the
derived clearance budget. All 19 checkpoint validations pass.

Both A10 false-positive labels are therefore closed under one common
Cauchy-conditioning derivation. Current durable schedule count is `52`
converged, zero unconverged, zero failed and `508` missing. The next locked
coefficient row is `E020__S512503_N0000__A00__primary24`, but bulk schedule
continuation is not the project priority.

The next project-level target is constructive: derive the one-parent-law
coupling spine that suppresses non-GR corrections in local/PPN/Mercury
conditions while activating the same motion sector in the galactic regime.
This coefficient-pipeline result is supporting infrastructure, not evidence
for local GR, galaxies or the full MTS theory. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

## Prior handoff - checkpoint 5146

Checkpoint 5144 compared every existing full-remainder row under the locked
adaptive criterion rather than treating an MTS row in isolation. Forty-nine
of 51 rows were strict passes. Both A10 rows—older
`E040__S512503_N0000__A10__primary24` and repaired
`E020__S512503_N0000__A10__primary24`—had reached the same 4096-interval
ceiling while being incorrectly labelled converged. Checkpoint 5145 repairs
the root status semantics, preserves byte-identical pre-repair witnesses and
demotes only those two rows to `COMPLETED_UNCONVERGED`.

The shared failure was then pursued rather than logged as another missing
input. The outer adaptive estimator was accumulating error from an
ill-conditioned inner global Cauchy average. The old representative contour
could sit too close to the Laurent origin; choosing the first finite annulus
alone also fails when its two bounding pole moduli nearly coincide.

Checkpoint 5146 derives the conditioned finite-annulus rule. For every
adjacent pair `rho_i < rho_(i+1)`, the radius
`R_i=sqrt(rho_i rho_(i+1))` uniquely maximizes
`min(log(R/rho_i),log(rho_(i+1)/R))`, with maximum
`0.5 log(rho_(i+1)/rho_i)`. Signed Cauchy residues preserve the same fixed
pole ownership as the representative contour moves. Annuli must satisfy the
predeclared inner-error clearance budget; among those, the center nearest the
unit circle is selected to suppress avoidable small/large-radius Laurent
conditioning. No physical pole ownership, physics parameter, outer tolerance
or outer interval cap changes.

The locked E040/A10 replay passes at both 96 and 192 inner nodes. Each run uses
59 composite intervals and has maximum outer adaptive error about
`3.4203e-05`, below the unchanged `5e-5` tolerance. The two corrected values
agree to relative difference `1.8245861794256666e-11`; the selected value is
`2.629523668093365-0.7498785367793288i`. No removable-collision fallback is
used, all residues remain stable, and every selected annulus satisfies the
clearance rule.

Current durable schedule count is `51` converged, `1` unconverged, zero
failed and `508` missing. The next locked row is now
`E020__S512503_N0000__A10__primary24`. Reuse the same conditioned-annulus
derivation only after preserving its argument-local Laurent certificate and
run a 96/192 cross-node replay; do not bulk-resume the schedule.

This is a real coefficient-pipeline advance and validates the user's demand
for baseline comparison: the apparent MTS failure was a shared numerical
representation fault. It is not yet the physical local-GR-to-galaxy
derivation. The governing machine/cog criterion remains mandatory: one parent
law must preserve local GR/Newton/Mercury behaviour while activating the
galactic sector without a manual switch. Source coupling, the exact local
GR/Newton limit, the physical transition law and the full MTS theory remain
open and unclaimed. The protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

## Prior handoff - checkpoint 5140

Checkpoint 5134 runs the next locked row,
`E040__S512503_N0000__A14__primary24`, only after its default argument-local
gate passes. A14 reaches `COMPLETED_CONVERGED` with `49` composite intervals
and maximum adaptive relative error `2.5344072795132247e-05`, below the
unchanged `5e-5` tolerance. Its normalized coefficient is
`1076.1926986349474-1558.2157293640844i`. The pilot advances from `49` to `50`
converged without a failed or unconverged row.

The final E040 row, `E040__S512503_N0000__A04__primary24`, exposes a real
certificate issue rather than being forced through. Its default small
beam-spinor chart rejects both residue agreement
`5.53993845058186e-05 > 5e-5` and the second-to-first Laurent-mode ratio
`0.0011372594836585406 > 2e-4`. The predeclared nested route is not used
because Laurent order had not passed. Checkpoints 5136 and 5137 test radius,
precision and symmetric `+/-t` extraction; they remain inconclusive because
the global-cycle evaluator loses stable digits close enough to the pole.

Checkpoint 5138 then resolves the order algebraically in the implemented KLT
integrand. Only the left-cut angle bracket `b=<1 0>` vanishes, and its zero is
simple. The sole permutation overlap with two Parke-Taylor factors `b^-2`
also carries the momentum-kernel factor `s21 proportional to b`, leaving a
simple `b^-1` pole. Other permutations are finite; the `special=1` numerator
supplies `b^4`, while only `special=2,3` retain the simple pole. The opposite
chirality and both right-cut chiralities are nonzero, so the cut product does
not square it. The implemented-integrand double pole is therefore excluded by
source algebra rather than by numerical threshold adjustment.

At the proof-authorized deep boundary profile, A04's residue disagreement
falls to `4.0817817955696196e-05` and regular-part uncertainty to
`1.4142793200102986e-05`; both pass unchanged limits. The noisy second Fourier
mode remains `0.000274383036206232`, so checkpoint 5140 accepts exactly one
chart through the exact 5138 Laurent-order certificate while retaining that
numeric value in the gate. No numeric threshold, seed, argument, profile
tolerance, interval cap, principal value or half residue is changed.

The locked A04 replay reaches `COMPLETED_CONVERGED` with `147` composite
intervals and maximum adaptive relative error `3.27252422208022e-05`. The
chart route is exercised `720` times in `5292` target-profile calls. The
causally corrected value is `80.3570715629863+27.796538995332977i`, and the
normalized coefficient is `-51.15690060655379-17.695826327815478i`.

Current durable pilot count is `51/560` converged, zero unconverged, zero
failed and `509` missing. All ten locked arguments of the
`E040/S512503_N0000` full-remainder block have now converged under the same
event-level pole equations: `A10,A00,A11,A01,A12,A02,A13,A03,A14,A04`.
Argument geometry selects chart activation; there is no hand-set argument
switch. The next locked missing row is
`E020__S512503_N0000__A10__primary24`; certify that row before executing it
alone, and do not bulk-resume the schedule.

This closes a coefficient-pipeline block and demonstrates the required
machine/cog discipline inside that pipeline. It does not yet derive the
physical local-GR-to-galaxy transition or establish a UV coefficient. The
source coupling, exact local GR/Newton limit and full MTS remain open and
unclaimed. The protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

## Prior handoff - checkpoint 5133

Checkpoint 5133 reuses the locked-next runner unchanged. Current schedule
state selects `E040__S512503_N0000__A03__primary24` and fixes the only allowed
count transition at `48 -> 49` converged with `512 -> 511` missing. No
argument-specific wrapper or manual schedule choice is introduced.

A03 passes its default gate directly. Chamber 0 activates no chart and
chamber 1 activates the same four event-derived poles. The small beam residue
disagreement is `3.4471838685426354e-05`, below the unchanged `5e-5` gate, so
the nested precision route is not used. This confirms that refinement remains
conditional on certificate failure rather than becoming a hidden new default.

The locked A03 replay reaches `COMPLETED_CONVERGED` with `117` composite
intervals and maximum adaptive relative error `4.6004993118058265e-05`, below
but close to the unchanged `5e-5` tolerance. The chart route is exercised
`936` times in `4356` target-profile calls. The causally corrected value is
`154.99664028824793+14.964922718214375i`.

Current durable pilot count is `49/560` converged, zero unconverged, zero
failed and `511` missing. The next locked missing row is
`E040__S512503_N0000__A14__primary24`. Certify A14 first and execute it alone
only if accepted. A03's near-tolerance convergence should remain visible in
later aggregate diagnostics; it is accepted, not promoted to a precision
claim.

Across seven transported arguments, the event-level pole law remains fixed
while argument geometry alone selects activation. This is still numerical
coefficient-pipeline evidence, not the missing physical derivation from local
GR to galactic activation. The protected `formalization-workbench` hash
remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5132

Checkpoint 5132 replaces per-argument wrapper duplication with a reusable
locked-next runner. It reads the authoritative schedule and run state,
selects the first incomplete row, derives the exact one-job count transition,
configures checkpoint-specific outputs and refuses any non-next row unless it
is explicitly finalizing an existing result. Gate, execute and finalize
remain separate phases; bulk continuation is never authorized.

The runner selects `E040__S512503_N0000__A13__primary24`. Its default gate
activates no chart in chamber 0 and all four event-derived poles in chamber 1,
but correctly rejects the small beam residue disagreement
`0.0001063916104268314`. Isolation, Laurent order and regular-part uncertainty
pass. The rejected gate is preserved before the predeclared nested precision
pair is tried. With unchanged chart radii and thresholds, refined disagreement
is `1.9012579862580397e-05`; all four charts pass.

The locked A13 replay reaches `COMPLETED_CONVERGED` with `52` composite
intervals and maximum adaptive relative error `3.120351934123457e-05`, below
the unchanged `5e-5` tolerance. The chart route is exercised `864` times in
`1908` target-profile calls. The causally corrected value is
`-99.34336960930257+292.4189481762057i`.

Current durable pilot count is `48/560` converged, zero unconverged, zero
failed and `512` missing. The next locked missing row is
`E040__S512503_N0000__A03__primary24`. Invoke the locked-next runner with a
new checkpoint id, certify A03 first and execute that row only if accepted.

Across six transported arguments, one event-level pole law survives while
geometry alone selects its active chamber. This continues to satisfy the
machine/cog implementation discipline without converting a numerical result
into a physical claim. The local-GR-to-galaxy mechanism itself remains to be
derived. The protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5131

Checkpoint 5131 separates chart certification from integral execution. The
reusable runner now has a `gate` phase that derives the transported contour,
constructs all Cauchy charts, writes a complete accepted or rejected gate and
returns without creating a job or kernel. A separate `finalize-existing`
phase validates an authoritative completed row without rerunning or replacing
its cached integral.

The next locked row, `E040__S512503_N0000__A02__primary24`, passes the default
gate directly. Chamber 0 activates no chart and chamber 1 activates the same
four event-derived poles. The beam pair lies `0.0015985077057241075` from the
contour and the hard-soft pair lies `0.0008531907823727436` away. Unlike A01
and A12, no nested precision refinement is needed: the small beam residue
disagreement is `1.0999469300999489e-05` at the default boundary levels,
below the unchanged `5e-5` gate.

The locked A02 replay reaches `COMPLETED_CONVERGED` with `91` composite
intervals and maximum adaptive relative error `3.657403050600277e-05`, below
the unchanged `5e-5` tolerance. The chart route is exercised `864` times in
`3276` target-profile calls. The causally corrected value is
`378.2569567405178-53.46821170932667i`.

Current durable pilot count is `47/560` converged, zero unconverged, zero
failed and `513` missing. The next locked missing row is
`E040__S512503_N0000__A13__primary24`. Certify A13 with the non-mutating gate
phase, then run it alone only if accepted; no bulk continuation is authorized.

Across five transported arguments, the event-level pole equations remain
fixed while argument geometry selects their active chamber. This is useful
evidence that the numerical mechanism has the no-manual-switch architecture
required by the machine/cog criterion. It remains a coefficient-pipeline
result, not yet the physical local-GR-to-galaxy derivation. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5130

Checkpoint 5130 applies the now-parameterized argument-local pole mechanism
to the next locked missing row, `E040__S512503_N0000__A12__primary24`.
Before integration, chamber 0 activates no chart and chamber 1 activates the
same four event-derived beam-spinor and hard-soft poles. The beam pair lies
`0.00183592644022141` from the A12 contour and the hard-soft pair lies
`0.000979911144814956` away.

The default boundary certificate again fails closed only for the small beam
root: residue disagreement is `0.00010681874127781828`, while isolation,
simple-pole order and regular-part uncertainty already pass. Because this is
the same diagnosed asymmetry as A01, the predeclared nested precision pair
`48/64/96` versus `64/96/128` is reused with unchanged chart radii and
acceptance thresholds. The rejected gate is preserved. Refined disagreement
is `3.594992526749294e-05`, below `5e-5`; all four charts pass.

The locked A12 replay reaches `COMPLETED_CONVERGED` with `59` composite
intervals and maximum adaptive relative error `3.590841949633697e-05`, below
the unchanged `5e-5` tolerance. The chart route is exercised `864` times in
`2196` target-profile calls. The causally corrected value is
`4.895039509856131+51.685835901633666i`.

Current durable pilot count is `46/560` converged, zero unconverged, zero
failed and `514` missing. The next locked missing row is
`E040__S512503_N0000__A02__primary24`. Apply the same preflight and run A02
alone; no full-pilot continuation is authorized.

Across A00, A11, A01 and A12, the same event-level pole equations now survive
four distinct transported contours while geometry alone selects their active
chamber. This is concrete support for the machine/cog implementation
discipline, but it is still a coefficient-pipeline result rather than the
physical local-GR-to-galaxy transition. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5129

Checkpoint 5129 follows the locked interleaved schedule rather than choosing
the next numerical label: after A11, the next missing row was A01. The 5128
preflight was parameterized so the event-level beam-spinor and hard-soft pole
laws are retained while each transported argument independently determines
which chamber, if any, enters their isolation disks.

For `E040__S512503_N0000__A01__primary24`, chamber 0 activates no chart and
chamber 1 activates all four derived poles before integration. Its beam pair
lies `0.0006604994898023685` from the contour and its hard-soft pair lies
`0.00035253635277639` away. The default Cauchy pair correctly failed closed:
the small beam root had residue disagreement `0.000140766885436162`, above
the unchanged `5e-5` gate.

That failure was not hidden or solved by loosening acceptance. The rejected
gate is preserved. A nested precision sequence, with the same chart radii and
thresholds, reaches low/high levels `48/64/96` and `64/96/128`; disagreement
falls to `1.5599298158747994e-05`, the double-to-simple ratio is
`3.058545905504786e-05`, and regular-integral uncertainty is
`1.7152035847382755e-05`. All four charts then pass.

The locked A01 replay reaches `COMPLETED_CONVERGED` with `83` composite
intervals and maximum adaptive relative error `1.7658876241031874e-05`, below
the unchanged `5e-5` tolerance. The chart route is exercised `864` times in
`2988` target-profile calls. The causally corrected value is
`896.7568399400188-310.68180156622657i`.

Current durable pilot count is `45/560` converged, zero unconverged, zero
failed and `515` missing. The next locked missing row is
`E040__S512503_N0000__A12__primary24`. Apply the same preflight to A12 and
run it alone; no full-pilot continuation is authorized.

The governing machine/cog criterion remains mandatory: the eventual parent
law must preserve successful local GR/Newton behavior while deriving galaxy
activation from the same dynamics without a manual switch. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5128

Checkpoint 5128 generalizes the 5127 pole repair from one hard-coded argument
to a pre-integration geometric selection rule. The beam-spinor and hard-soft
pole equations remain event-level laws. For each transported argument, a
chart activates only when that argument's chamber segment enters the guarded
isolation disk fixed by the nearest known singularity. No integral result is
used to choose the active chamber or poles.

For locked job `E040__S512503_N0000__A11__primary24`, chamber 0 activates no
pole chart. Chamber 1 activates exactly the same four derived roots as A00.
Their contour distances are `0.003989887137241419` for the beam-spinor pair
and `0.002129570546338084` for the hard-soft pair, inside independently
constructed chart radii `0.020148741219346` and `0.075145115431803`.

All four Cauchy gates pass before replay. The locked A11 row then reaches
`COMPLETED_CONVERGED` with `72` composite intervals and maximum adaptive
relative error `4.5036049193367614e-05`, below the unchanged `5e-5`
tolerance. The chart route was genuinely exercised `936` times in `2772`
target-profile calls. Its causally corrected value is
`7.5040633139199056+7.147796267695423i`.

Current durable pilot count is `44/560` converged, zero unconverged, zero
failed and `516` missing. No full-pilot continuation is authorized. Next,
apply the same preflight to the next untouched transported argument and run
that row alone; do not assume it shares A11's active chamber and do not
bulk-resume the schedule.

The governing machine/cog criterion remains mandatory: the eventual parent
law must leave the successful Mercury, clocks, local lensing and laboratory
GR/Newton cogs turning while deriving galactic activation from the same
dynamics without a manual switch or regime retuning. Checkpoint 5128 is a
clean numerical example of that discipline, not yet the physical local-to-
galaxy proof. The protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5127

Checkpoint 5127 resolves the exact A00 obstruction rather than loosening its
locked numerical profile. The endpoint-adjacent direct-g1 double zeros are
removable, but they were not the dominant source of the adaptive error. The
missing singular strata were four same-sheet outer collinear simple poles
that checkpoint 5030's opposite-ownership collision catalog could not
contain.

Two reciprocal pole families are now derived from the parent kinematics. The
beam-spinor family obeys `p_1^- = E_1-p_{1z}=0`, at
`q=0.12666165152262066` and `q=7.895049432711758`. The hard-soft family
obeys `s_13=2 e A(1+beta)(1-C)=0`, hence `C=1`, at
`q=0.33192806900481986` and `q=3.0127009234204865`. Reciprocal closure is
`6.66e-16` and the maximum defining-kinematic residual is `3.33e-16`.

The implemented log-Cauchy chart writes `F(z)=R/(z-z0)+H(z)`. It derives `R`
from an isolated high-precision boundary, independently checks the residue
and second principal coefficient, reconstructs only regular `H` inside a
guarded 65-percent boundary disk, and integrates the subtracted pole
analytically. It introduces neither a principal-value prescription nor a
half residue.

The unchanged A00 replay is now `COMPLETED_CONVERGED`. Adaptive intervals
fell from `4112` to `69`, maximum relative error fell from
`0.003319880181794845` to `1.8630336285107402e-05`, below the locked `5e-5`
tolerance, and the causally corrected value moved only from
`4759.040097130271-2596.845904847965i` to
`4759.048142980555-2596.8478131853926i`. All four derived pole rows were
exercised; validation passes `16/16`.

Current durable pilot count is `43/560` converged, zero unconverged, zero
failed and `517` missing. No 5127 Python process or `__pycache__` remains.
Do not blind-resume the full pilot. The next row is
`E040__S512503_N0000__A11__primary24`: generalize the 5127 chart into an
argument-local preflight, run A11 alone, and fail closed if its pole-chart
gate does not pass before allowing any broader continuation.

The governing machine/cog criterion remains mandatory: one parent mechanism
must preserve Mercury, clocks, local lensing and laboratory GR/Newton while
deriving any galactic activation from the same dynamics without a manual
switch or regime retuning. The protected `formalization-workbench` hash
remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoints 5125-5126

Checkpoint 5125 locks and starts the first genuinely fresh test of the 5124
variance route. Before any fresh output was read it fixed 28 unused Sobol
seeds, disjoint 4-event full-remainder and 24-event reciprocal-topological
strata, ratio six, both E040/E020 rows, ten crossed arguments, the Richardson
rule, stop conditions and the 560-job schedule. The source design predicts
cost-normalized speedups `1.1007115833572758/1.2056537703007533`, but the
fresh result—not that prediction—will decide the route.

The first fresh obstruction was not hidden. Job
`E040__S512502_N0000__A10__primary24` had one unstable isolated
`direct:g1/subtraction:decay` residue. Checkpoint 5126 derives and guards the
repair from the 5124 involution: `I:xi->1/xi` gives `I*omega=-omega`, hence
`Res_(1/r)=-Res_r`. Substitution is allowed only for one-to-one isolated
roots with reciprocal residual below `2e-8`, exact `u/v` label involution and
a stable partner. Multi-pair, mixed `g2/decay`, missing-partner and
unstable-partner cases still fail closed.

The witness root residual is `1.6270411272829336e-17`; its stable reciprocal
partner has zero residue. The repaired replay converges under the unchanged
profile. The same guarded theorem was then used 16 more times across the
remaining S512502 rows. There are 17 cumulative certified repairs; no
tolerance, seed, allocation or field equation changed.

Historical count at checkpoint 5126 was `42/560` converged, `1` unconverged,
zero failed and `517` missing. No Python process remains. The next row is the
existing unconverged
`E040__S512503_N0000__A00__primary24`; do not simply rerun it.

That second obstruction is now localized to adaptive integration, not
residues: all residue rows are stable, but the calculation used 4112
intervals and 294588 relative-integrand evaluations, ending at maximum
relative error `0.003319880181794845`. It ran for `6417.849976199999 s`.
Chamber 1 contains endpoint-adjacent zero-residue direct-g1 collision groups
at log distances `0.00022818379047273926` and
`0.0004574902398047273`; these are the leading suspects for unresolved
removable/double-pole cancellation.

Next calculation: derive an endpoint-local removable/double-zero extension or
an algebraically combined chamber integrand for that exact family, then replay
A00. Do not raise the interval cap, loosen `5e-5`, delete the event, change the
locked seeds, or use the huge unconverged value. Only after that replay passes
should the unchanged 5126 overlay resume the 560-job pilot.

The governing machine/cog criterion remains mandatory: one parent mechanism
must preserve Mercury, clocks, local lensing and laboratory GR/Newton while
deriving any galactic activation from the same dynamics without a manual
switch. At checkpoint 5126 the protected `formalization-workbench` hash was
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The UV coefficient, source coupling, exact local
GR/Newton limit and full MTS remain open and unclaimed.

## Prior handoff - checkpoint 5124

Checkpoint 5124 advances the crossed `hhh` bottleneck rather than adding a
new missing-input ledger. The existing code already combines `s/t/u` target
values per outer event, so superficial cyclic precombination is proved unable
to reduce variance.

The exact fixed-event decomposition is

```text
R = R_topological + R_naive,
R_naive = R_pole_model + R_smooth.
```

Richardson extrapolation, cyclic crossing and local projection preserve this
identity to maximum closure residual `2.4783339495784277e-11`. The pole and
smooth pieces are almost perfectly anticorrelated (`-0.999978344080608` real,
`-0.9999987790273194` imaginary), so they must remain paired. The plain
topological split was actually benchmarked and rejected: cost fraction
`0.789823215091073`, projected speedups `0.8513369707062017/0.9191694655160288`.

A new reciprocal-root reduction is supported across all 540 completed
kernels. Every one of 8038 crossing rows pairs under `r -> 1/r`. For 3222
isolated safe pairs, `Res(1/r)=-Res(r)` closes with zero failures and maximum
residual `1.9157276434582633e-09`. The 797 clustered or mixed `g2/decay`
pairs are not assumed safe; both residues are evaluated fail-closed. The
reconstructed stored topological sums close to maximum relative residual
`1.0814879829950791e-08`.

The exact production replay evaluates 11 rather than 18 crossing rows,
reproduces the stored topological value to relative residual
`2.0856023705233558e-13`, and costs `0.5622287687622782` of the full gate.
The resulting design-conditioned speedups are `1.1038901349061654` real and
`1.215206368122875` imaginary. These are useful design results, not an
independent coefficient measurement.

Next: build a restartable reciprocal-reduced topological outer-event runner,
lock fresh seeds and allocation before seeing outcomes, and measure realized
cost-variance against the paired high estimator. Never separate
`pole_model+smooth`; never shortcut the 797 unsafe reciprocal families.

The governing machine/cog criterion is mandatory: the eventual single parent
theory must preserve the tested local GR/Newton responses (Mercury, clocks,
local lensing and laboratory gravity) while deriving any galactic activation
from the same dynamics without a manual scale switch or sector retuning.

All `21/21` checkpoint-5124 validations pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred. The numeric UV coefficient, parent source coupling,
exact local GR/Newton limit and full MTS theory remain open and unclaimed.

## Prior handoff - checkpoint 5123

Checkpoint 5123 replaces the unstable physical-argument `epsilon -> 0`
extrapolation with the derived angular-first physical `hhh` cut. At each fixed
physical scattering angle it averages the internal directions at fixed soft
energy, subtracts the exact checkpoint-5019 endpoint only after that average,
and then evaluates the soft-energy plus integral. It does not use the rejected
pointwise endpoint subtraction.

The five controlled physical values `D_hhh/G^3` are

```text
z=-0.6: -0.03557017332 +/- 0.000207
z=-0.3: -0.0005238131103 +/- 0.0000834
z= 0.0:  0.02285665832 +/- 0.000141
z=+0.3: -0.0005238131103 +/- 0.0000834
z=+0.6: -0.03557017332 +/- 0.000207
```

The real-sheet, angular-resolution, Gauss-order and identical-scalar-evenness
gates all pass. The physical contribution to the local-shape coefficient has
standard error `7.327856002402613e-05`.

Replacing only the physical rows while retaining every crossed high-only row
does not close the UV coefficient. The hybrid `a_hhh` is
`-173.32927977131123 + 16.05311369367297 i`, with real/imaginary standard
errors `102.9515216455813/32.82837179404016`. The entire real local-shape
uncertainty is crossed: its standard error is `102.95152164555522`.

This is a forward localization, not another broad missing-input statement:
the ordinary physical branch is now controlled, and the unresolved object is
only the crossed finite-`x` upper-boundary continuation. The next calculation
must combine the `s/t/u` finite-`x` integrands and residues before outer
sampling so cancellations occur before variance is generated. Do not add
another independent control bank, delete the large events, or retune the field
equations.

The governing cog criterion is explicit: preserve the successful local
GR/Newton responses while deriving any galactic-scale activation from the
same parent dynamics, without a manual regime switch.

All `22/22` checkpoint-5123 validations pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub action occurred.

The complete crossed `hhh` cut, numeric UV coefficient, parent source
coupling, exact local GR/Newton limit, and full MTS theory remain open and
unclaimed.

## Prior handoff - checkpoints 5109-5122

Checkpoint 5109 closes the proposed imaginary-zero shortcut. The event and
integrand conjugation map is exact, and the target roots transform exactly,
but the locked upper-Feynman contour is not the reflection image because it
reanchors at `+0.3` rather than the reflected `-0.3`. There are 408 ownership
mismatches in the locked event/chamber audit. The true image cycle obeys the
reflection relation to `5.9215582170490347e-14`; the prescribed cycle misses
it by `1.3467511476339342`. Therefore no zero imaginary mean may be imposed.

Checkpoint 5110 replaces that failed route with an exact complex telescoping
identity. Writing `A=R_primary(E020)`, `B=R_primary(E040)`, `H=2A-B`, and
`C=A`, fixed `beta=1` gives `E[H-C]+E[C]=E[H]` in every real and imaginary
channel without any symmetry assumption. The identity residual is
`7.105427357601002e-15`.

The ratio-three design estimate is `0.7462906810169911 < 0.8` with projected
total cost `9.94395049986113 h`; twelve new controls project to
`5.021066679416702 h`. It is borderline under leave-one-high-out
(`0.8000294913775439`) and uses v12 high data to choose the route, so it is a
design-conditioned continuation, not independent evidence.

Checkpoint 5111 implements that runner and passes `19/19` dry-run checks. Its
scope is exactly 180 `E020/primary24` jobs over seeds `507611..507622`; all 120
high-source jobs converge and none of the new targets overlaps v12. It reuses
179 verified E040 topologies and deliberately reconstructs one non-reusable
source through the ordinary fail-closed path. Resume accepts only exact-digest
`COMPLETED_CONVERGED` rows, each invocation is capped at four hours, and the
new run is isolated from both v12 and `formalization-workbench` by hashes.

The first collision exposed a genuine error in the generalized 5084 recoil
zero theorem. Checkpoint 5112 proves the conditional Cauchy identity remains
valid but its assumed direct-residue holomorphy is not established: one outer
root is a stable nonzero `31.01294678732344 - 0.254009009904149 i`. Eight
historical zero rows and the paired inner row survive only as individually
recomputed event-local arbitrary-precision zeros.

Checkpoints 5113-5115 replace repeated manual collision handling with a
fail-closed source-separated classifier. Cross-additive rows with one owned
direct `g1/g2` pole and same-source direct `g1/g2` opposite-ownership pairs
can be classified as event-local zero or stable nonzero at 60 decimal digits;
unknown or unstable rows still fail closed. The first same-source witness is
retained as `-19.942056041962328 + 0.4064000175315503 i`. No contour or
convergence tolerance has been relaxed.

Checkpoint 5116 recovers the external timeout at a durable `74/180`. The next
row, `E020__S507615_N0000__A14__primary24`, then exposes an integration rather
than residue failure: all residues are stable, but the unclustered calculation
exhausts 4108 intervals with relative error `2.1895202689681583`.

Checkpoint 5117 derives the applicable same-orientation Cauchy cluster cycle
from the parent 5095 identity and certifies it at E020 with 24 and 48
global-residue nodes. Both calculations pass the unchanged `5e-5` gate, and
their values agree to `2.9371898151125674e-12` relative. Maximum cluster
isolation ratio is `0.010846102551545899 < 0.1`; no exact-collision fallback is
used. Production replay converges in `93.17 s` without changing the profile,
tolerance, interval cap or topology.

Checkpoint 5118 records the clean second wall-cap pause at `126/180`.
Checkpoint 5119 resolves the only later failure by proving the S507622
projective collision roots are homogeneous momentum ratios independent of
all fifteen finite E020 external arguments. The maximum factor-root mismatch
is `2.1965717747241423e-13`; minimum same-source separation is
`0.003127198980147923`. This is one guarded family derivation, not fifteen
row-specific zero assumptions.

The 5111 control matrix is complete: `180/180` exact-digest jobs converge,
with zero failed, unconverged or missing rows. The final row is
`E020__S507622_N0000__A14__primary24`; status is `COMPLETE`.

Checkpoint 5120 executes the locked beta-one analysis without fitting the new
controls. The exact paired identity closes with zero numerical residual, but
the realized cost-normalized score is `1.5148246022524876 > 0.8`. Accepted
final-job runtime is `9.860421870944458 h <= 10 h`, so the score rather than
runtime fails. The bottleneck is `real_z-0.3`.

Checkpoint 5121 shows why. At the bottleneck, independent-control variance is
`4.8092264142119125` times the four-high design proxy. The best score within
the original runtime cap is `1.5045429011673104`; no single low deletion
passes, and even the diagnostic ratio-20 scan bottoms at
`1.1723088359800824`. Therefore the beta-one variance-reduction route is
rejected rather than retuned post hoc.

Checkpoint 5122 reconciles the completed matrix, locked result and failure
mechanism. Retain all numerical evidence. Next: return to the high-only `hhh`
cut/UV-coefficient route, then map that coefficient into the parent source
coupling and local-GR/Newton limit. Do not alter the field equations to rescue
a failed estimator.

The complete `hhh` cut, UV coefficient, exact local GR/Newton limit, and full
MTS theory remain open and unclaimed.

## Prior handoff - checkpoints 5101-5108 and pilot v12

The locked central-anchor numerical matrix is complete. The authoritative v12
run has `360/360` converged jobs, zero unconverged jobs, zero failures, and zero
missing rows. Its config digest is
`bb930b0d2c11cd1bf4644b05db976f548e256d10add888144b98cfab95aa7a69`; the
locked schedule digest remains
`da19db9b4d7f5c1ca41babe2f1fcfafc2f9ed92a043cc4298f1fb5c4bee3f956`.

Checkpoint 5101 proves the S507622 projective cluster identity is independent
of the external scattering argument. Under `p'=lambda p`, all four factor roots
are homogeneous degree-zero momentum ratios, so the common `lambda` cancels.
Both reciprocal roots pass all fifteen locked E040 arguments with maximum
mismatch `2.1763879942877348e-13`; unrelated same-source roots remain separate.

Checkpoint 5102 carries only the 359 previously converged rows into v12 and
leaves A14 fresh. The exact A14 replay then converges in `94.15743670001393 s`,
with the unchanged adaptive residual `0.0003562977572416951 < 0.0005`, one
exactly scoped 5101 certificate, and all residues stable. Checkpoint 5103
validates every job and linked kernel/topology record, all digests and upstream
ledgers, no Python cache, and the unchanged formalization hash.

The unchanged predeclared 5080 estimator has now been executed. Checkpoints
5104 and 5106 prove that the v12 run binding and the missing precision-budget
schema adapter preserve the original seeds, controls, covariance estimator,
score, threshold, and runtime cap. The five injected margins rederive exactly
from the 5018 source and match the historical 5040 rows. The first execution
attempt wrote no output; the repaired one-shot execution passes all checks.

The locked decision is `LOCKED_FRESH_PILOT_DOES_NOT_PASS`. Its score ratio is
`1.3474894142500562` versus the predeclared `0.8`; runtime passes at
`8.938616622583346 h`. The matrix itself remains complete and valid.

Checkpoint 5108 isolates the failure mechanism. The high-only precision
bottleneck is `imag_z-0.3`, where the locked control is zero. Positive low-bank
cost with unchanged variance imposes

    sqrt((C_correction+3 C_low)/C_high)=1.3474894142500562,

exactly the observed score. This rejects the locked multifidelity estimator,
not the MTS kernel or theory. Next: prove or reject an exact
conjugation/reflection-symmetric imaginary control before authorizing more
kernels; if no such control exists, retain high-only sampling and reject the
low-only bank route.

The complete `hhh` cut, UV coefficient, exact local GR/Newton limit, and full
MTS theory remain open and unclaimed.

## Prior handoff — checkpoints 5083-5086 and pilot v6

The central-anchor pilot runner now excludes the quarantined broad 5041 zero
theorem. Checkpoint 5083 proves one owned-`g2` cross-source zero locally.
Checkpoint 5084 derives the corrected guarded theorem for isolated owned
`direct:g1/direct:g2` recoil poles and finds no counterexample among 601 stable
nonzero historical rows. `direct:g3` remains explicitly excluded because it
aliases the subtraction source.

Checkpoint 5085 derives the same-source `u/v` coalescence identity
`plus_u=plus_v iff e^2=h hbar iff n_z=z` and constructs a guarded
multidirection removable extension. Checkpoint 5086 derives an outward-contour
gate for isolated same-source minus/plus collisions when shrinking contours
are numerically pathological. Both policies are row-local and fail closed.

The v6 locked pilot has `112/360` converged jobs, zero accepted-unconverged
jobs, one failed job, and 247 unrun jobs. It stops at
`E020__S507603_N0000__A07__primary24`: the 5085 extension gives convergence
`1.9066396040169262e-7` and direction spread `1.0202079759829128e-7`, just
above the unchanged `1e-7` gate. The pilot and 5080 statistical analysis remain
incomplete and unclaimed.

Next: checkpoint 5087 must add the approach level `3.90625e-6` for this exact
row and rerun the three-direction Richardson limit. Resume the cached v6 matrix
only if the original `1e-7` gates pass; otherwise reject this extension route.
Do not relax tolerances, rerun completed jobs, or infer an MTS result from the
partial matrix.

The complete `hhh` cut, UV coefficient, exact local GR/Newton limit, and full
MTS theory remain open and unclaimed.

## Prior superseded handoff - checkpoint 5031

The complete off-unit relative collision set is now transported by an
integer causal homotopy rather than the rejected endpoint-joined spiral. In
the log-relative-azimuth plane, collision worldlines crossing each chamber's
reference surface generate explicit winding corrections. The four chambers
have invariant crossing counts `(7,6,7,8)` under raised/direct upper-half-plane
paths, regulators `0.003/0.001`, and `96/192` tracking steps.

Relative local residues and exact pole subtraction produce the first converged
crossed finite-`x` two-azimuth event. The global-node-32, relative-order-192
value is `11.4896509-13.3716999i`; global-node refinement changes it by
`0.00954` (`5.41e-4` relative). The topological correction is
`-0.00202321-0.08611732i` and is stable to `9.06e-11`.

This closes only the event kernel at `x=0.37`, `s_z=0.23`, `d_z=-0.31`.
The next non-optional calculation is a small multi-event topology grid before
any bounded outer integration over `x`, `s_z`, and `d_z`. The complete `hhh`
cut, UV coefficient, local GR, and full MTS remain open and unclaimed.

## Prior authoritative handoff - checkpoint 5029

The finite-`x` `hhh` plus integrand now has an explicit global-azimuth
physical-pole contour. Its physical pointwise residual is `1.2805e-7`,
the direct/endpoint subtraction remains finite through `x=0.001`, and
the physical phase-space smoke is consistent with checkpoint 5017.

The exact complex sequential boost has also been derived. For hard-leg
sign `sigma=+/-1`,

    c_sigma=[sigma d_z+(sigma(gamma-1)mu-B)s_z]
            /[gamma(1-sigma beta mu)],

so every finite-`x` hard polar pinch `c_sigma=+/-z` reduces to a reciprocal
quadratic pair in the relative azimuth. The analytic boost, mass shells,
and pinch roots close below `5.6e-14`.

At one finite-`x` event, the exact physical relative chambers reproduce
the raw two-azimuth integral to `1.523e-4`. A crossed contour made only by
joining transported boundary roots with logarithmic spirals fails order
convergence and is rejected. The rational collision map shows why: the
physical boundary list is complete, but many off-unit opposite-ownership
collision poles must be carried by the homotopy too.

Current decision:

    covariant finite-x KLT integrand          = exact pointwise;
    global finite-x physical-pole transport  = constructed;
    soft-plus subtraction                    = finite;
    boosted polar and pinch laws             = exact;
    one physical relative chamber            = controlled;
    naive crossed logarithmic spiral         = rejected;
    full off-unit collision homotopy          = next derivation;
    crossing-complete hhh nonlocal vector     = open;
    full coupled cut and numeric UV invariant = open;
    exact all-operator local GR               = false;
    full MTS                                  = false.

Next: introduce a small upper-half-plane start regulator to split the
coincident physical collision roots, transport the entire off-unit
collision set and contour by one causal homotopy, and require fixed-event
order convergence before integrating the remaining three variables.

## Prior authoritative handoff - checkpoint 4994

The mixed `h phi` `u` cut has now been reduced beyond its boxes and
triangles. An exact null-numerator IBP system gives

    J_AC= u^3(11t^2-9tu+6u^2)/(6t^3),
    J_AD=0,
    J_BC=0,
    J_BD=-u^3(11t^2+15tu+6u^2)/(6t^3).

Hence

    C_u^(strict 4D)=-t^2u^4/4,
    C_t^(strict 4D)=-u^2t^4/4.

The reducer independently reproduces all four 4992 scalar-box leading
singularities. Six exact rational kinematic points reconstruct the result
and two held-out points pass.

The generic-dimensional check reveals a required evanescent cancellation.
On `t=1,u=2`,

    C_u(D)=-(27D^3+532D^2-6036D+8720)
           /[40(D-4)(D-2)(D-1)]
          =108/[5(D-4)]-959/60+O(D-4).

The strict-4D value on that slice is `-4`, so neither `-4` nor `-959/60`
may be inserted as the physical rational completion alone. The generic-D
box, triangle and bubble coefficients must be expanded together and their
`1/(D-4)` scalar-basis poles canceled before the finite hard kernel is
defined.

Current decision:

    complete four-dimensional scalar-box sector    = exact;
    complete one-mass triangle sector               = exact from IR;
    strict-4D mixed I2(u) and crossed I2(t)         = exact;
    evanescent generic-D basis pole                 = exact on one slice;
    generic-D all-master cancellation               = next derivation;
    scalar-intermediate I2(s)                       = open;
    full dimensionally regulated one-loop amplitude = open;
    crossing-complete outer hh cut                  = open;
    numeric full K_mu K_ang and finite C_w          = open;
    exact all-operator local GR                     = false;
    full MTS                                        = false.

The generator closes `11/21` gates and the independent validator passes
`198/198`. The next target is the generic-D mixed-family expansion through
the finite term, with evanescent box-triangle-bubble cancellation proved
before the identical-scalar `s`-cut bubble is reduced.

## Prior authoritative handoff - checkpoint 4993

The universal one-loop gravitational soft operator now fixes every
one-mass triangle coefficient after the 4992 boxes:

    T_s=(t+u)[t^6+t^5u+2t^4u^2+2t^2u^4+tu^5+u^6]/8,
    T_t=-t^5(t^2+tu+2u^2)/8,
    T_u=-u^5(2t^2+tu+u^2)/8.

The source pair sum gives no `1/epsilon^2` term because `s+t+u=0`. Its
first epsilon derivative gives the universal
`sL_s+tL_t+uL_u` simple pole. In the common helicity phase, the reduced
tree is `t^3u^3/(4s)`, so the three logarithmic targets are fixed without
a fit.

Each reconstructed box-plus-triangle logarithmic pole matches its target
exactly, `T_t` and `T_u` cross correctly, and the full double-pole
coefficient is zero.

Current decision:

    complete four-dimensional scalar-box sector    = exact;
    complete one-mass triangle sector               = exact from IR;
    all channel log/epsilon soft poles              = exact;
    full double-pole cancellation                   = exact;
    bubble and UV simple-pole sector                = open;
    D-dimensional rational completion               = open;
    full one-loop phi phi h h amplitude             = open;
    crossing-complete outer hh cut                  = open;
    numeric full K_mu K_ang and finite C_w          = open;
    exact all-operator local GR                     = false;
    full MTS                                        = false.

The generator closes `16/25` gates and the independent validator passes
`404/404`. The next target is the all-channel `D`-dimensional cut/IBP
reduction onto the three bubble masters, with UV and rational remainders
kept separate.

## Prior authoritative handoff - checkpoint 4992

The complete four-dimensional scalar-box sector of the one-loop
opposite-helicity `h h phi phi` amplitude has now been obtained from actual
unitarity cuts. In the convention

    M1=kappa^4 F/<1|3|2]^4,

the three box coefficients are

    B_st=t^4(s^4+t^4+u^4)/32,
    B_su=u^4(s^4+t^4+u^4)/32,
    B_tu=t^4u^4/16.

The 4991 `hh` `s`-cut boxes were supplemented by the missing identical
scalar state,

    B_st^(phiphi)=s^4t^4/32,
    B_su^(phiphi)=s^4u^4/32.

An independently sewn distinguishable `h phi` `u` cut gives

    B_su^(mixed)=u^4(s^4+t^4+u^4)/32,
    B_tu^(mixed)=t^4u^4/16,

and its crossing image gives `B_st`. All shared-box residuals vanish
exactly. The scalar `1/2` state factor removes paired routing duplication;
the mixed cut has no identical-state factor. Projective quadruple-cut roots
at chart infinity are included.

This completes the four-dimensional box sector, not the full one-loop
amplitude. Triangles, bubbles, `D`-dimensional `mu^2`/rational terms and the
common soft subtraction remain before the outer crossed `hh` cut can be
integrated.

Current decision:

    sourced hh s-channel box component             = exact;
    scalar-intermediate s-channel boxes             = exact;
    mixed h phi t/u-channel boxes                   = exact;
    three-channel scalar-box consistency            = exact;
    complete four-dimensional box sector            = true;
    full one-loop phi phi h h amplitude              = open;
    crossing-complete outer hh cut                   = open;
    numeric full K_mu K_ang and finite C_w           = open;
    exact all-operator local GR                      = false;
    full MTS                                         = false.

The generator closes `20/29` gates and the independent validator passes
`351/351`. The next target is the universal one-loop gravity soft operator
in the same integral normalization, used to solve or bound the complete
triangle sector before the `D`-dimensional bubble reduction.

## Prior authoritative handoff - checkpoint 4991

The first non-scalar amplitude needed by the corrected 4990 master has been
recovered from Chi's exact `D`-dimensional ancillary coefficients. For the
opposite-helicity two-graviton `s`-channel component,

    M1_hh,s=kappa^4 F_hh,s/<1|3|2]^4,

with

    b_I2(4)=tu[2(t^4+u^4)-3tu(t^2+u^2)]/32,
    b_I2^(epsilon)=-tu[180(t^4+u^4)-333tu(t^2+u^2)
                       +605t^2u^2]/2880,
    b_I3=-(t^7+u^7)/16,
    b_I4(s,t)=t^4(t^4+u^4)/32,
    b_I4(s,u)=u^4(t^4+u^4)/32.

The source tree phase cancels exactly in the physical interference:

    M1_hh,s M0*=kappa^6 F_hh,s/(4stu).

The retained component's exact double-pole checksum is

    -(3t^6-3t^5u+3t^4u^2-t^3u^3
      +3t^2u^4-3tu^5+3u^6)/16.

This is source-complete for the declared `hh` `s`-channel component, not for
the full one-loop `phi phi h h` amplitude. The scalar-intermediate and mixed
`h phi` crossed cuts remain and must determine the missing `I4(t,u)`,
`I3(t/u)` and `I2(t/u)` information before full infrared subtraction or the
outer two-loop `hh` integration.

Current decision:

    sourced massless hh s-channel kernel           = exact;
    epsilon-times-bubble-pole contribution          = retained exactly;
    t-u crossing and physical phase cancellation    = exact;
    full one-loop phi phi h h amplitude              = open;
    mixed h phi crossed cuts                         = next derivation;
    crossing-complete outer hh cut                   = open;
    numeric full K_mu K_ang and finite C_w           = open;
    exact all-operator local GR                      = false;
    full MTS                                         = false.

The generator closes `9/16` gates and the independent validator passes
`301/301`. The next target is an explicit mixed `h phi` unitarity cut, not a
new missing-input inventory.

## Prior authoritative handoff - checkpoint 4990

Checkpoint 4990 repairs a direct-channel/crossing mismatch in 4989. For
cyclic channels and `s+t+u=0`,

    q^3 P2((p-r)/q)=q^3-6stu,
    sum q^3=3stu,
    sum q^3 P2=-15stu.

The exact 4988 scalar slopes then give

    D_phi,crossed,log=-(203/20)F1_log.

With Bern's `2 Im F=U` master normalization,

    R_master=2 sum_cuts D_cut-D1 ReF1,
    beta_C^S-matrix=203/10,
    D C^S-matrix=-203/10,
    2D_phi,crossed,log-D1 ReF1=0.

The matching double logarithm is

    F2_double=(203/(20pi))[(23/15)Q_A-(1/30)Q_B],
    dF2_double/dlnmu=-(203/10)F1_log,

and its direct discontinuity reproduces both 4988 scale slopes exactly.
Tree-times-tree three-particle cuts are therefore not assigned artificial
`mu` slopes.

The `16` coefficient remains valid only in its declared Type-I/Litim FRG
coordinate. The finite map from that Wilsonian coordinate to the on-shell
amplitude coordinate is open.

The corrected coefficient has also been propagated through the inherited
4985-4987 amplitude orbit:

    C(t)=C_c+(203/10)t,
    W(t)=C_w+(S-6C_c/pi)t-[609/(10pi)]t^2,
    I=3S-(203/10)rho,
    K_mu=3S-(203/10)rho+(18/pi)r4,
    K_ang=A-B-[47/(15pi)]r4.

Both full invariants remain exact under the simultaneous finite orbit, and
the rational-free reduction remains `K_mu=3S_rf`, `K_ang=A_rf-B_rf`.

The 4988 values are restored as additive scalar-cut subtotals:

    Delta K_mu_phi=(-135061+1500pi^2)/(450pi),
    Delta K_ang_phi=(13357+24075pi^2)/(3375pi).

They are not full invariants and must not be multiplied by two again.

The `hh` helicity theorem proves direct-channel `J=0,2` silence only. A
crossed `P4` counterexample has `T0=252/5` and `T2=144/7`, so full crossed
`hh`, mixed `hhh`, and `phiphih` finite cuts all remain required.

Current decision:

    crossing-complete scalar/D1 nested log       = exact zero;
    on-shell beta_C and D C                       = 203/10 and -203/10;
    Type-I/Litim FRG coefficient                  = 16 in a distinct coordinate;
    finite FRG/on-shell bridge                    = open;
    inherited 4985-4987 amplitude orbit           = corrected exactly;
    scalar Delta K subtotals                      = exact;
    hh direct J0 J2                               = exact zero;
    hh crossing-summed Delta K                    = open;
    mixed hhh and phiphih finite cuts             = open;
    numeric full K_mu K_ang and finite C_w        = open;
    exact all-operator local GR                   = false;
    full MTS                                      = false.

The generator closes `12/20` gates and the independent validator passes
`263/263`. The next target is one crossing-complete finite cut calculation,
not another scale-slope inventory.

## Superseded handoff history - checkpoint 4989

The 4989 section below is retained for audit only. Its factor-two
interpretation, `G=16ReF1` on-shell identification, remaining scale-slope
targets, global `hh` low-spin zero, and two-number affine reduction are
superseded by checkpoint 4990.

Checkpoint 4989 derives the once-global anomalous-action subtraction and
corrects the interpretation of the 4988 scalar-cut projection. Bern's
optical-theorem normalization gives

    D_cut=-U/(2pi s^3),
    R_master=2 sum_cuts D_cut-G,
    G=D1 ReF1=16 ReF1.

The exact physical-channel kernel is

    G(x,L)=G0(x)+(144/pi)x(1-x)L,
    coefficient_L[G]=(24/pi)(P0-P2),

with low-spin constant coefficients

    G_0=868/(135pi),
    G_2=-3716/(675pi).

Scale independence then forces

    sum_cuts d0_L= 12/pi,
    sum_cuts d2_L=-12/pi.

After subtracting the exact scalar cut, the missing low-spin targets are

    d0_hhh,L+d0_phiphih,L= 3097/(72pi),
    d2_hhh,L+d2_phiphih,L=-21397/(1800pi).

The opposite-helicity `hh` cut has helicity difference four, so its Wigner
support starts at `J=4`. The same-helicity tree is exactly zero. Therefore
the `hh` cut contributes exactly zero to `J=0,2` and cannot directly alter
`K_mu` or `K_ang`. Only the two three-particle cuts own the missing low-spin
numbers.

Writing their `L=0` coefficients as `r0,r2`,

    K_mu=(-89221+1500pi^2)/(225pi)-12(r0-5r2),
    K_ang=2(67537+24075pi^2)/(3375pi)+2(r0+7r2).

Current decision:

    global D1 ReF1 normalization              = derived exactly;
    4988 master factor-two correction          = applied and validated;
    remaining low-spin scale sum rules         = derived exactly;
    opposite-helicity hh J0 J2 support          = exact zero;
    low-spin unknown cut classes                = two three-particle cuts;
    higher-J locality tower                     = exact target, numeric open;
    numeric full K_mu K_ang and finite C_w      = open;
    exact all-operator local GR                 = false;
    full MTS                                    = false.

The generator closes `9/17` gates and the independent validator passes
`231/231`. The next target is the actual low-spin evaluation of the mixed
`hhh` and `phiphih` three-particle cuts, not another inventory pass.

## Authoritative current handoff - checkpoint 4988

Checkpoint 4988 evaluates the first of the four irreducible two-loop cut
classes. In the 4987 rational-free convention, the complete physical-channel
one-loop four-scalar hard kernel has universal endpoint residues

    lim[x h_raw]_(x->0)=lim[(1-x)h_raw]_(x->1)=-pi^2/16.

The crossing-even singular subtraction

    h_reg=h_raw+pi^2/[16x(1-x)]

removes both nonintegrable poles. The regular kernel is linear in
`L=ln(s/mu^2)`:

    h_reg=C0(x)-(203/320)(x^2-x+1)L,
    coefficient[L^2]=0.

Exact angular integration gives

    h0=18161/34560+13pi^2/288-(203/384)L,
    h2=-621877/864000+173pi^2/1440-(203/9600)L.

The scalar-cut reduced discontinuity is

    d0_phi=(176/3pi)h0,
    d2_phi=(16/3pi)h2,

    and its exact additive invariant subtotals are

    Delta K_mu_phi
      =(-135061+1500pi^2)/(450pi)+[1827/(10pi)]L,

    Delta K_ang_phi
      =(13357+24075pi^2)/(3375pi)-[9541/(300pi)]L.

At `L=0` these additive scalar-cut terms are `-85.0641390166317` and
`23.6697802325722`. They are not full `K_mu/K_ang` invariants: Bern's
master weights `D=-U/(2pi)` by two, and the inverse map already combines
that factor with cyclic crossing. Multiplying them by two again would double
count. The global `D1 ReF1` subtraction is applied once after all cuts. The
other cut classes remain open. The
`zeta(3)` moments cancel exactly; the independent validator passes `443/443`
with maximum direct-kernel residual `2.20e-79`.

Current decision:

    scalar two-particle cut hard kernel       = derived exactly;
    universal singular soft subtraction      = derived exactly;
    scalar-cut h0 h2 d0 d2                   = derived exactly;
    scalar-cut Delta K_mu Delta K_ang subtotals = derived exactly;
    global D1 ReF1 subtraction                = open;
    remaining cut classes                     = three;
    numeric full K_mu K_ang and C_w           = open;
    exact all-operator local GR               = false;
    full MTS                                  = false.

The next target is checkpoint 4989: derive the `D1 ReF1` contribution in
the same reduced convention, convert total scale cancellation into exact
sum rules, and then evaluate the opposite-helicity `hh` two-particle cut.

## Authoritative current handoff - checkpoint 4987

Checkpoint 4987 enlarges the fixed-p4 finite orbit used in 4986. Crossing
symmetry and `s+t+u=0` leave one local rational polynomial at p4 and one at
p6. With `C'=C+beta` and `W'=W+alpha C+delta`, exact amplitude and flow
invariance give

    r4'=r4-beta,
    rho'=rho+3alpha,
    S'=S+16alpha-B_gc beta,
    A'=A-beta f_A,
    B'=B-beta f_B.

The full invariants are therefore

    K_mu=3S-16rho-3B_gc r4,
    K_ang=A-B-(f_A-f_B)r4,

where `B_gc=-6/pi`, `f_A=46/(15pi)` and `f_B=-1/(15pi)`. The declared
rational-free choice `beta=r4`, `alpha=-rho/3` gives

    r4_rf=rho_rf=0,
    K_mu=3S_rf=-6(A_rf+B_rf),
    K_ang=A_rf-B_rf.

Reflection parity, the same-helicity `2phi2h` tree zero, and the massless
all-equal-helicity KLT zero reduce the complete cut state sum to

    C2_ren=C2_phiphi+C2_hh(+-)+C3_hhh(mixed)+C3_phiphih-C_IR.

The exact projections are

    Pi_stu[-C2_ren/pi-D1 ReF1]=-K_mu stu,

    D(z)=Disc_s/(-2pi i s^3)=d0+d2P2(z),
    K_mu=-6(d0-5d2),
    K_ang=d0+7d2.

Current decision:

    full finite X2/O2 scheme orbit           = derived exactly;
    fully invariant K_mu and K_ang           = derived exactly;
    double rational-free scheme              = constructed;
    eliminated cut classes                   = exact zeros;
    surviving cut classes                    = four;
    numeric K_mu and K_ang                    = open;
    finite C_w                               = open;
    exact all-operator local GR              = false;
    full MTS                                 = false.

The live runner records 13 closed and four explicit open/nonclaim gates; the
independent validator passes `233/233`. No GitHub action.

The next target is checkpoint 4988: evaluate the source-complete
rational-free `phiphi` two-particle cut from the archived Dunbar-Norridge
one-loop amplitude, perform the universal soft subtraction, and project its
exact `d0,d2` contribution before attacking the other three classes.

## Authoritative current handoff - checkpoint 4986

Checkpoint 4986 reconstructs the complete nonlocal logarithmic shape behind
the 4985 local beta projection. With

    L_A=sum s^3 ln(-s/mu^2),
    L_B=stu sum ln(-s/mu^2),
    Q_A=sum s^3 ln^2(-s/mu^2),
    Q_B=stu sum ln^2(-s/mu^2),

the exact channel reduction and crossing sum give

    P_s=-(23/15)s^3+(1/30)stu,
    sum P_s=-(9/2)stu,

    F_1,log=(2/pi)[(23/15)L_A-(1/30)L_B],
    F_2,double=(8/pi)[(23/15)Q_A-(1/30)Q_B].

Their scale derivatives are

    dF_1,log/dlnmu=-(18/pi)stu,
    dF_2,double/dlnmu=-16F_1,log.

The finite one-loop rational coordinate must be retained as
`F_1=F_1,log+rho_mix stu`. Under `w'=w+alpha gc`, both the local
two-loop source and rational coordinate move:

    S_2L'=S_2L+16alpha,
    rho_mix'=rho_mix+3alpha.

Therefore the actual scheme-invariant scale target is

    I_2L=3S_2L-16rho_mix.

For `F_2,single=A_2L_A+B_2L_B`, RG invariance fixes

    A_2+B_2=-I_2L/6,
    J_2L=A_2-B_2.

The unresolved two-loop primitive is now precisely numeric `I_2L` plus the
scale-invariant angular coefficient `J_2L`; raw `S_2L` is rejected as a
standalone physical target. `C_w` remains finite UV trajectory data.

The retained pure-metric terms are also converted into exterior results.
For the selected C3 coordinate and every `r>=2M`,

    |Delta Phi/Phi_N|<=5|a_+|/r^4,
    |Delta a/a_N|<=35|a_+|/r^4.

At `52 micrometres`, the selected acceleration bound is
`3.62084618058e-124`; the raw-running guard is `4.24865650783e-122` and is
not called a complete amplitude. The determinant separates a gravity-only
`a+b=43/120` contribution from the parent massless-log endpoint
`a+b=89/240`. The latter gives

    delta A/A=-[89/(120pi)]l_P^2q^2ln(q^2/mu^2),
    |Delta Phi/Phi_N|=[89/(60pi)]l_P^2/r^2,
    |Delta a/a_N|=[89/(20pi)]l_P^2/r^2.

The gravity-only and parent-endpoint acceleration fractions at
`52 micrometres` are `1.32230509491e-61` and `1.36843201682e-61`. The
parent value is valid only for `m_gap r << 1`; the physical motion-sector
threshold form factor remains unsourced.
Finite local `R^2/Ricci^2` terms are source contacts at first EFT order and
vanish for separated exterior points. The determinant result is the
two-point subset, not the complete one-loop source-source potential.

Current decision:

    one-loop mixed nonlocal logarithm             = derived;
    two-loop double-log kernel                    = derived;
    scheme-invariant I_2L definition              = derived;
    numeric I_2L and angular J_2L                 = open;
    finite trajectory datum C_w                   = open;
    finite p4 separated-source exterior response = contact zero;
    gravity determinant two-point tail             = derived and bounded;
    parent massless-log determinant endpoint       = derived and bounded;
    physical motion m_gap threshold form factor    = open;
    selected C3 exterior contribution             = derived and bounded;
    complete C3 and quantum source amplitudes      = open;
    exact all-operator local GR                    = false;
    full MTS                                       = false.

The live runner records 13 closed and six intended open/nonclaim gates; the
independent validator passes `109/109`. No GitHub action.

The next target is checkpoint 4987: calculate `I_2L` and `J_2L` directly
from the renormalized two-loop scalar discontinuities, including the common-
scheme `4phi` and `2phi2h` one-loop amplitudes, `X^2` counterterm insertion,
two- and three-particle cuts, and universal soft subtraction.

## Authoritative current handoff - checkpoint 4985

Checkpoint 4985 closes the metric part of the running essential-frame
connection. Linearizing the exact finite map at `ctilde=d=0` gives

    delta g_mn=kappa[(beta_d+beta_ctilde/2)Xg_mn
                     -beta_ctilde v_m v_n]dt.

The EH first variation contains only the two redundant Ricci coordinates and
a Palatini divergence. Thirty-two Euclidean/Lorentzian jets reproduce its
bulk and boundary reductions at `4.89e-15` and `4.04e-16`. Finite
Hessian-squared spillover starts quadratically off the zero surface, so

    delta beta_wO2|metric frame=0.

Together with 4984, both scalar- and metric-frame connection contaminations
of the physical `O2` coordinate are now exactly zero.

The genuine flow calculation also moved forward. Gravity EFT counting proves
that a pure-minimal one-loop graph is four derivative, not six derivative.
The complete one-loop contribution linear in `X^2` has only scalar-scalar
cuts. Exact soft-subtracted `J=0,2` partial waves and crossing give

    mu d wbar_O2/dmu|X2=-3 ubar_X2/(16pi^2 M_P^2),
    beta_w=6w-(3/(2pi))g u_X2+S_2L g^3+...
          =6w-(6/pi)g c_ess+S_2L g^3+... .

Thus the 4959 `g^2` source ansatz is superseded. With
`beta_c=4c+16g^2`, the corrected weak trajectory is

    w/g^3=C_w+(S_2L-6C_c/pi)t-(48/pi)t^2.

The mixed coefficient and `-48/pi` double logarithm are invariant under the
resonant finite redefinition `w'=w+alpha gc`; the isolated `S_2L` shifts by
`16alpha`. The remaining physical calculation is a fixed-common-scheme
renormalized two-loop single-log amplitude plus finite matching, not a
scheme-free raw pole.

Current decision:

    metric-frame O2 connection                       = exactly zero;
    pure-minimal one-loop p6 source                  = exactly zero;
    one-loop X2-to-O2 mixing                         = derived;
    B_gc                                             = -6/pi;
    invariant double-log coefficient                = -48/pi;
    fixed-common-scheme two-loop single logarithm    = open;
    finite trajectory datum C_w                      = open;
    arbitrary-O2 positive six-point lower bound     = retained;
    selected local scalar packet                     = source silent;
    pure-metric C3 and determinant response          = open;
    exact all-operator local GR                      = false;
    full MTS                                         = false.

The live runner closes 14 derived gates and records four intended open
nonclaim gates; the independent validator passes `98/98`. No GitHub action.

The next target is checkpoint 4986: calculate the fixed-common-scheme
renormalized two-loop four-scalar `stu log(mu)` coefficient with all p4,
evanescent and soft subdivergences included, while converting the isolated
pure-metric `C^3` and determinant kernels into explicit local bounds.

## Authoritative current handoff - checkpoint 4984

Checkpoint 4984 propagates the 4983 running scalar coordinate
`partial_t psi=gamma_Box Box psi` through six derivative order. The exact
spillover of `cX^2` is

    beta_A6|frame=-4c gamma_Box,  A6=X(Box psi)^2,
    beta_B6|frame=-8c gamma_Box,  B6=(Box psi)v^m v^n H_mn.

Both coordinates contain the leading scalar EOM explicitly. Twenty-four
Euclidean/Lorentzian local-jet controls reproduce the direct variation from
the reduced bulk plus boundary divergence at `3.73e-15`. Fourteen massless
events show that their on-shell projector is zero at maximum
induced-to-`O2` ratio `3.25e-16`, while the independently derived
`P_O2=-3stu` remains nonzero. Therefore

    delta beta_wO2|gamma_Box=0.

The unknown numeric `beta_bBox` no longer contaminates the physical `O2`
coordinate. The genuine parent `O2` loop source and derivative spillover of
the running metric frame are still separate open calculations.

The same checkpoint proves a stronger branch theorem. For any covariant
self-adjoint analytic or nonanalytic two-point kernel

    Gamma2=(1/2)<psi,F_H(-Box)psi>,

the selected `J_psi=0`, zero-boundary profile `psi=0` has zero classical
scalar EOM, explicit scalar stress, charge, and one-scalar force. The result
proves existence and source silence, not uniqueness or stability. The
field-coordinate Jacobian and fluctuation determinant are pure-metric
quantum responses and remain explicit.

Current decision:

    scalar running-frame p6 map                         = derived;
    raw connection vector (A6,B6)                      =(-4c,-8c)gamma_Box;
    essential O2 shift from beta_bBox                  = exactly zero;
    numeric beta_bBox needed for that result           = false;
    selected nonlocal two-point source silence         = proved;
    leading flat Newton p2 Hessian from p6 packet      = zero;
    genuine parent beta_wO2                            = open;
    metric-frame p6 spillover                          = open;
    quantum Jacobian and determinant                   = open;
    exact all-operator local GR                        = false;
    full MTS                                           = false.

The next target is checkpoint 4985: calculate the genuine parent `O2`
momentum-flow source and metric-frame derivative spillover in one common
measure scheme, while retaining the pure-metric `C^3` and determinant
bounds. The live runner passes `32/32`; the independent validator passes
`98/98`. No GitHub action.

## Authoritative current handoff - checkpoint 4983

Checkpoint 4983 resolves the nonconstant-gradient ambiguity left by 4982.
The omitted four-derivative scalar bilinear

    S_Box2=(b_Box/2) int sqrt(g)(Box psi)^2

is not the corpus's six-derivative operator
`O2=X(nabla_rho nabla_sigma psi)^2`. Its exact covariant scalar Hessian is
`b_Box Box^2`; the complete connection-dependent metric-motion block is
derived and vanishes at `psi=0`. Thirty-two local-jet controls reproduce
the analytic blocks at maximum relative residual `2.81e-15`.

At four derivatives,

    I_Box-I_Hessian-I_RicciX=boundary,
    psi_old=chi+[b_Box/(2Z)]Box chi,
    b_Box,new=b_Box-2Zs=0.

Together with the already derived conformal/disformal metric map, five raw
directions minus one IBP identity and three independent field-redefinition
directions leave one essential coordinate, `c_ess`, with the unchanged
source `beta_c,ess=16g^2`. This does not assert a numeric raw `b_Box` or
`beta_bBox`. A running essential frame instead obeys
`gamma_Box=beta_bBox/(2Z)`.

The local response expansion gives

    1/(Zp^2+b_Box p^4)=1/(Zp^2)-b_Box/Z^2+O(b_Box^2p^2).

The first correction has source support and vanishes outside any smooth
compact source. More strongly, the selected integrated-`H` parent has
`J_psi=0`, zero scalar boundary data, and `Q_psi=0`; hence `psi=0`,
`T_Box2=0`, and the one-scalar fifth force vanish for all eight imported
Earth, Sun, white-dwarf, and neutron-star density controls for arbitrary
local `b_Box`.

Current decision:

    four- versus six-derivative operator identity          = resolved;
    covariant Box2 Hessian and flat p4 projector           = derived;
    local four-derivative essential quotient               = dimension one;
    essential source beta_c,ess                            = 16g^2;
    selected source-zero Box2 local branch                 = exact;
    numeric beta_bBox and nonlocal form factor             = open;
    nonperturbative heavy fourth-order mode                = not promoted;
    six-derivative running-frame spillover                 = open;
    finite parent metric TTT                               = open;
    exact all-operator local GR                            = false;
    full MTS                                               = false.

The next target is checkpoint 4984: derive the running-frame connection's
six-derivative spillover and determine whether the nonanalytic two-point
tail is also source-silent on the selected branch. The runner passes
`27/27`; the independent validator passes `105/105`. No GitHub action.

## Authoritative current handoff - checkpoint 4982

Checkpoint 4982 closes the constant-gradient order-`X` motion-metric packet
left by checkpoint 4981. The complete covariant second variation of
`sqrt(g)P(X)` is derived and independently checked by differentiating the
original density with a second-order jet engine. Twenty-four controls agree
at maximum relative residual `4.89e-15`, and the checkpoint-4956 flat
functional Hessian is recovered at `2.78e-17`.

The exact mixed vertex obeys

    B_mn=(1/2)g_mn(v.D)-v_(m D_n),
    B^dagger K B=(1/2)X(-Box).

Consequently the flat principal Schur insertion is `X/2`, local, and adds no
new pole. On constant-gradient backgrounds, the four-derivative packet closes
modulo the scalar EOM, integration by parts, and boundary terms into
`X^2`, `R_mn X^mn`, and `RX`. The source-owned standard-frame flows and the
already derived exact Einstein-frame quotient give

    beta_c=20g^2,
    8pi g(beta_ctilde+beta_d)=-4g^2,
    beta_c,ess=16g^2.

No finite coefficient is fitted. The full essential `N=8` germ is strictly
elliptic on `x<=0.1`, with minimum transverse and longitudinal eigenvalues
`0.957920827810` and `0.846546731674`; this is not promoted to a Lorentzian
causality claim.

At `X=0`, this complete `P(X)` packet, its stress, and its curvature-dressed
four-derivative terms vanish exactly. It therefore preserves the selected
leading Einstein/Newton/metric-Maxwell branch. This is a packet-level result,
not an all-operator local-GR proof.

Current decision:

    covariant order-X parent Hessian                    = derived;
    principal mixed Schur operator                      = reduced;
    constant-gradient essential subtraction             = derived;
    essential source beta_c,ess                         = 16g^2;
    P(X)-packet local-GR silence at X=0                 = derived;
    nonconstant-gradient O2/(Box psi)^2 sector          = open;
    Lorentzian causal cone                              = open;
    finite parent metric TTT                            = open;
    exact all-operator local GR                         = false;
    full MTS                                            = false.

The next target is checkpoint 4983: derive the nonconstant-gradient
`O2/(Box psi)^2` projector and test its Ward-reduced invariant remainder on
sourced local profiles. The runner passes `19/19`; the independent validator
passes `79/79`. No GitHub action.

## Authoritative current handoff - checkpoint 4981

Checkpoint 4981 transfers the calculation from the free-scalar control to
the declared integrated-metric MTS parent. In source-locked de Donder gauge,
all metric and ghost nonminimal derivative coefficients vanish. The parent
quadratic operators are a Laplace-type Einstein tensor block, a minimal
vector ghost, and the renormalized motion scalar block.

The checkpoint-4956 functional Hessian proves exact factorization at zero
motion gradient: `p(0)=0`, `p'(0)=1/2`, and the mixed block is proportional
to `sqrt(x)`. The signed determinant count is

    (1/2)(9+1)-4+1/2=3/2,

corresponding to two graviton helicities plus one real motion scalar. The
single negative DeWitt trace eigenvalue is retained as the Euclidean
conformal-sign issue rather than hidden.

The apparent factor two between checkpoints 4979 and 4980 is resolved:
4979 records a mixed two-point response, which is twice the action
coefficient written in 4980. The source-locked Einstein-ghost result and one
real minimally coupled motion scalar then give the parent ultraviolet log

    Gamma_log=(4pi)^-2 int sqrt(g)[
      (43/120) Ricci log(-Box/mu^2) Ricci
      +(1/80) R log(-Box/mu^2) R].

For nonzero motion background, the first Schur-complement correction is
derived explicitly. It contains
`-C0^-1 B_half^T A0^-1 B_half` at order `x`, proving that separate scalar
and metric determinants cannot be reused away from `x=0`.

Current decision:

    parent gauge-fixed quadratic Hessian at x=0          = derived;
    signed Einstein-ghost-motion supertrace              = derived;
    universal parent quadratic-curvature logs            = derived;
    leading nonzero-motion Schur correction              = derived;
    physical m_gap finite threshold                      = open;
    finite parent metric TTT                             = open;
    full quantum BRST restoration                        = not proven;
    exact all-operator local GR                          = false;
    full MTS                                             = false.

The next target is checkpoint 4982: covariantize and project the order-`x`
motion-metric Schur kernel and fix its two-point subtraction before any
finite parent TTT claim. The runner passes `18/18`; the independent
validator passes `68/68`. No GitHub action.

## Authoritative current handoff - checkpoint 4980

Checkpoint 4980 closes the generic traceful finite contact for the complete
one-loop free minimal-scalar determinant. A covariant four-dimensional
Pauli--Villars multiplet with coefficients `(1,-3,3,-1)` and mass-squared
ratios `(0,1,2,3)` supplies the determinant-volume first, pair, and triple
contacts from the parent massive scalar action. Its first three regulator
moments vanish exactly.

The `q^4` response is extracted analytically before large `q^0/q^2`
cancellations and agrees with an unexpanded massive determinant fit at
`8.54e-9`. Forty-eight independent two-point controls fix the exact common
scheme

    Delta W_ct=1/[2(4pi)^2] log(3M^2/8)
               int sqrt(g)[Ricci^2/60+R^2/120].

The two-point covariance residual is `1.20e-14`. With no three-point fit,
the rule matches old traceful controls G03/G04 and fresh G05/G06 over six
regulator masses. Maximum relative and absolute residuals are `1.33e-8` and
`2.07e-13`; regulator-mass spread is `1.20e-13`.

Current decision:

    complete free-scalar TT finite determinant             = matched;
    complete free-scalar generic traceful determinant       = matched;
    covariant regulator/contact rule                        = derived;
    interacting motion/graviton/ghost Hessian               = open;
    exact all-operator compact GR                           = false;
    full MTS                                                 = false.

The next target is to transfer the same regulator/contact architecture to
the parent motion--graviton--ghost Hessian, fixing its two-point scheme
before evaluating any parent three-point kernel. The runner passes `16/16`;
the independent validator passes `60/60`. No GitHub action.

## Authoritative current handoff - checkpoint 4979

Checkpoint 4979 independently renormalizes the exact direct massless scalar
determinant. Its exact triangle integrand agrees with the checkpoint-4912
Taylor engine at `3.57e-16`. The universal MS-bar finite moments and pole
residues are derived analytically, and an independent two-point projection
fixes the source convention

    (-W)_source = UV_shell - W_MSbar

with fit residual `9.49e-12` and exact rational coefficients at
`1.36e-10` relative precision.

Four new transverse-traceless metric triples then match the complete finite
source response without fitted constants. The maximum absolute discrepancy
is `1.4066710036370056e-15`; the maximum relative discrepancy is
`5.4373545944886145e-11`. UV-shell, mu-rescaling and common-scale identities
hold at `2.40e-15`, `7.37e-15`, and `2.31e-15`.

Current decision:

    exact massless determinant integrand                 = derived;
    source/MS-bar finite scheme map                      = derived;
    complete TT scalar finite determinant                = independently matched;
    generic traceful finite contact                      = open;
    G03/G04 product-continuation mismatch                = 0.1343 / 0.03645;
    interacting motion/graviton/ghost kernels            = open;
    exact all-operator compact GR                        = false;
    full MTS                                             = false.

The remaining traceful discrepancy is continuation dependent and absent on
all four TT controls. The next calculation is the trace-Ward and evanescent
Gauss--Bonnet contact completion, not another refit of the nonlocal kernel.
The runner passes `16/16`; the independent validator passes `63/63`. No
GitHub action.

## Authoritative current handoff - checkpoint 4978

Checkpoint 4978 assembles the complete source-side free minimal-scalar
massless metric third response. The exact first Frechet variation of
`log(-Box/mu^2)` is evaluated for both scalar and Ricci-tensor Laplacians,
including connection and inverse-metric variations, and added to all eighteen
cubic source form factors.

On G03 and G04, `N=6` and `N=8` agree to `7.35e-15`; cyclic source
relabeling agrees to `4.74e-16`. The source braces are

    G03 = +0.003264605722251795,
    G04 = -0.03279909335440577.

The direct scalar determinant UV q4 shell independently matches the
logarithmic residue to `4.46e-11` on G03 and `2.26e-11` on G04.

Current decision:

    free-scalar local q6 and q8/a8                  = exact;
    massless scalar cubic form factors              = source-complete;
    quadratic nonlocal metric third variation       = derived;
    complete source-side free-scalar metric TTT      = derived;
    direct determinant logarithmic residue           = matched;
    scheme-dependent finite determinant comparator   = next target;
    interacting motion/graviton/ghost kernels         = open;
    exact all-operator compact GR                     = false;
    full MTS                                          = false.

The runner passes `14/14` internal gates and the independent validator passes
`51/51`. No GitHub action.

## Authoritative current handoff - checkpoint 4977

Checkpoint 4977 leaves the local Taylor ladder and evaluates the exact
massless finite-momentum scalar form factors. With `P=R/6`, eighteen source
form factors consolidate into eleven minimal-scalar cubic-curvature
channels. The independent alpha-simplex and explicit triangle/log-ratio
representations agree across 54 evaluations to `8.640926257429126e-13`; the
reduced channels agree to `5.1542112619360135e-12`.

The potential channel independently matches the direct determinant triangle
to `2.1842604679129222e-16`. The massless logarithm is now located exactly:

    -W_log^(2)=1/[2(4pi)^2] integral sqrt(g)[
      -(1/60) Ricci log(-Box/mu^2) Ricci
      -(1/120) R log(-Box/mu^2) R].

The cubic Gamma_i have no independent absolute mu-log; the full third metric
response inherits that log from the third variation of the quadratic
nonlocal action.

Current decision:

    free-scalar local q6 and q8/a8             = exact;
    massless scalar cubic-curvature form factors = source-complete;
    minimal-scalar reduced channels              = 11;
    source two-representation identity            = validated;
    direct potential determinant normalization    = exact;
    quadratic massless logarithm                  = exact;
    full scalar third metric response              = next target;
    interacting motion/graviton/ghost kernels      = open;
    exact all-operator compact GR                  = false;
    full MTS                                       = false.

The runner passes `11/11` internal gates and the independent validator passes
`45/45`. No GitHub action.

## Authoritative current handoff - checkpoint 4976

Checkpoint 4976 closes the free-scalar local `q^8/a8` third response rather
than fitting the checkpoint-4975 leakage. The restored-Riemann local `a4`
source, specialized with `P=R/6` and zero internal curvature, fixes two
quadratic four-derivative and fifteen consolidated cubic two-derivative
operators from twenty-five source terms.

The unfitted source vector reproduces the twelve-geometry determinant target

    a8,target=-2(4pi)^2 W_123,8

with relative residual `1.7200056164357514e-15`. The local response matrix
agrees between N6 and N8 to `3.879527387949945e-15`. Eight fresh geometries
give out-of-sample relative residual `2.8706094306143018e-15`.

The extended `20 x 17` matrix has rank 15 and nullity 2. The two null
directions are exhausted by the closed-manifold IBP/contracted-Bianchi
identity and the four-dimensional Gauss--Bonnet descendant. They are
geometric identities, not fitted parameters.

Current decision:

    free-scalar q6 quotient control             = exact;
    complete local free-scalar q8/a8 response   = source-derived and exact;
    dimension-eight integrated quotient         = rank 15, nullity 2;
    checkpoint-4975 restricted q8 image         = superseded as incomplete;
    unique basis-independent C3 derivative      = not promoted;
    full nonlocal scalar third response          = next target;
    controlled massless logarithm               = open;
    interacting motion/graviton/ghost kernels   = open;
    leading local GR/Newton/Maxwell branch      = retained;
    exact all-operator compact GR               = false;
    full MTS                                    = false.

The runner passes `8/8` internal gates and the independent validator passes
`31/31`. No GitHub action.

## Authoritative current handoff - checkpoint 4975

Checkpoint 4975 evaluates the complete free-scalar determinant third-response
Taylor germ through `q^8`. The identical pipeline recovers the known `q^6`
coefficient with `9.07e-16` image residual and `2.47e-12` relative
coefficient error, providing a strict baseline.

The unique first symmetric scalar dressing of the `q^6` quotient is

    M8,C3=diag(q1^2+q2^2+q3^2) M6.

The measured `q^8` response has converged relative leakage
`0.030214084796217903` outside this image. Angular-order eight and ten rows
agree to `4.45e-15`, so this is not quadrature error. Leave-one projected
coefficients range from `-2.2660e-6` to `+1.3422e-6`; the apparent
`5.3764e-7` coefficient is therefore diagnostic only.

The full `q^8` vector scales exactly as `m^-4`. The proper-time `m=3` operator
is consequently exact component by component:

    K8/a8=-24x^3/(1+x)^5,
    F8=x^3(x+4)/(1+x)^4,
    x=3k^2/m^2.

Its UV-to-IR weight integrates to one. This is a calculated finite-momentum
germ and a constructive basis rejection, not another placeholder ledger.

Current decision:

    free-scalar q6 quotient control             = exact;
    free-scalar q8 response                     = calculated and converged;
    q8 mass scaling and PT profile              = exact;
    restricted sigma1-dressed q6 image          = rejected;
    unique C3 form-factor derivative            = not identified;
    complete dimension-eight third-response     = next target;
    massless physical logarithm                 = open;
    leading local GR/Newton/Maxwell branch      = retained;
    exact all-operator compact GR               = false;
    full MTS                                    = false.

The runner passes `8/8` internal gates. The independent validator passes
`22/22`; validation CSV SHA256 is
`defa054feb409c92caf7157adb070895a32bce12ff848af9afa06be95e10d6e1`.
No GitHub action.

## Authoritative current handoff - checkpoint 4974

Checkpoint 4974 corrects the kernel order before any further integration.
The `Gamma4 + Gamma3-Gamma3` topology used as the 4973 next target is the
second metric response displayed by the acquired source for
curvature-squared form factors. Since `C^3` begins at `h^3`, the correct
kernel is the third metric response.

The exact one-loop determinant contains

    1 Gamma5 contact
    - 3 Gamma3/Gamma4 mixed terms
    + 2 Gamma3-cubed triangle orientations.

The exact Wetterich response with a field-independent regulator insertion
contains the corresponding ordered `1+6+6` terms. The executable derives
these noncommuting trace words and passes every topology check.

The validated 4912 scalar determinant then supplies the first actual
regulator-resolved kernel row. In the source-locked proper-time `m=3`, free
real-scalar `eta_psi=0` benchmark,

    C0=1/[30240(4pi)^2],
    x=3k^2/m^2,

    d_t zeta_scalar=-162 C0 k^6/(m^2+3k^2)^4,
    (m^2/C0)d_t zeta_scalar=-6x^3/(1+x)^4.

The profile vanishes at both RG endpoints but has exact positive integration
weight `3x^2/(1+x)^4` and cumulative fraction `[x/(1+x)]^3`. Therefore

    integral_(k=infinity)^(k=0) d_t zeta_scalar dlnk=C0/m^2.

This explicitly fills one endpoint-silent direction from the 4973 theorem;
the Hessian and regulator determine its finite interior. Both local helicity
projectors preserve the exact factor-ten identity.

The result is deliberately bounded. It is the free scalar local threshold,
not the interacting motion, graviton, ghost, finite-external-momentum, or
complete four-graviton kernel. In particular, the local massive limit cannot
test the 4972 massless logarithm; momentum projection must precede the
massless limit.

Current decision:

    prior two-response C3 topology             = superseded;
    correct third-response topology            = exact;
    free-scalar PT-m3 local C3 kernel           = calculated;
    free-scalar finite threshold                = integrated exactly;
    local helicity factor-ten gate              = pass;
    interacting motion contacts                 = open;
    graviton/ghost Gamma3 Gamma4 Gamma5         = open;
    finite momentum and physical log test       = open;
    full delta_c_fin                            = open;
    leading local GR/Newton/Maxwell branch      = retained;
    exact all-operator compact GR               = false;
    full MTS                                    = false.

The runner passes `28/28` internal checks. The independent validator passes
`22/22`; validation CSV SHA256 is
`7b612b3cbf282c092060cc47f51c42bfcfc6524c6c2e0954ed552c4cd318064f`.
No GitHub action.

## Authoritative current handoff - checkpoint 4973

Checkpoint 4973 derives the actual momentum-dependent equation for the
dimension-minus-two Weyl-cubic form factor:

    F_k(x,y)=k^2 f_C3,k(k^2x,k^2y),
    partial_lnk F_k=2F_k+2xF_x+2yF_y+H_C3,k,
    (1+x partial_x+y partial_y)F_*=-H_*/2.

Along a fixed-angle ray `x=rho`, `y=zrho`, the exact solution is

    F_*(rho,zrho)=C(z)/rho-[1/(2rho)] integral_0^rho H_*(v,zv)dv.

The homogeneous mode is `C(t/s)/s`. Quasi-local UV regularity therefore sets
`C(z)=0`, making the form factor unique conditional on knowing the full
momentum kernel.

The current local and endpoint data do not know that kernel. The executable
family

    Delta K_a(x)=a x/(1+x)^2,
    x=Q^2/k^2,

vanishes at both endpoints, preserves the 4972 local beta, physical log, and
factor-ten helicity identity, yet shifts the finite conversion by `-a/2`.
This constructively rejects extraction of `delta_c_fin` from the retained
endpoint data.

The exact two-loop finite remainders were also projected directly at
`s=1,t=u=-1/2`. Their apparent shifts differ:

    ++++: -0.088250826539336+0.001745329251994 i,
    -+++: -0.082010427087366+0.057404503362590 i.

Thus the raw finite loop remainder is not one universal local C3 conversion.
The exact finite-scheme orbit

    c -> c+zeta,
    L_h -> L_h-P_h zeta

leaves both amplitudes invariant and proves why one common-scheme match is
required.

The acquired primary sources identify the next calculation but do not contain
a ready-made parent C3 kernel. Checkpoint 4974 must assemble the dressed
parent `Gamma_k^(2)`, `Gamma_k^(3)`, and `Gamma_k^(4)` in one gauge, regulator,
and field split, then project the tadpole and two-vertex topologies onto both
C3 helicities. If the parent cannot supply that construction, retain one
explicit `lambda` rather than setting `delta_c_fin=0` by fiat.

Current decision:

    C3 form-factor PDE                       = derived;
    fixed-angle characteristic               = exact;
    quasi-local uniqueness                   = conditional on full kernel;
    endpoint-silent finite null family       = exact;
    direct two-loop finite fill              = tested and rejected;
    delta_c_fin from current endpoint data   = not identifiable;
    leading local GR/Newton/Maxwell branch   = retained;
    exact all-operator compact GR            = false;
    full MTS                                 = false.

The runner passes `23/23` internal checks and the independent validator passes
`21/21`; validation CSV SHA256 is
`174f0a8964f211825da2bf6a78d25d74b85a6f1996deffb3f90373f7e6bf4d3c`.
No GitHub action.

## Authoritative current handoff - checkpoint 4972

Checkpoint 4972 closes the exact normalization between the selected parent
EAA coefficient and the finite four-graviton amplitude basis:

    r_C3=G_C3/G_N,
    c_tree=32 pi^3 r_C3,
    A_Bern,tree=-r_C3.

The current selected local parent interval therefore gives

    -0.021879913239298467 <= c_tree <= -0.021701239349867996,
     2.1871820879230358e-5 <= A_Bern,tree <= 2.2051899226020373e-5.

With the explicit published local-EFT prescription `delta_c_fin=0` at the
matching scale, the resulting anchor estimates are

    SM45:        lambda/mu_m=1.09068 to 1.09146,
    SM45+motion: lambda/mu_m=1.09229 to 1.09308.

These are calculated conditional estimates, not complete amplitude claims.
The exact physical relation is

    c_phys(mu_m)=32 pi^3 r_C3^S+delta_c_fin(mu_m).

The missing nonlocal object is now partly derived rather than merely named.
The local infrared slope and the physical state-count slope require

    d(delta_c_NL)/dlnmu=-N/240-64 pi^3 B_C3.

This equals `0.2864969117` for SM45 and `0.2823302450` for SM45 plus one
active motion scalar, up to the locked tiny endpoint spread. All four closure
rows reproduce the physical beta exactly.

The two-helicity matrix for `(r_C3^S,delta_c_fin)` has rank one and nullity
one, with exact null direction `(1,-32 pi^3)`. Hence the tree normalization,
factor-ten identity and complete logarithmic form factor are fixed, while one
additive finite conversion remains. Re-running the zero-momentum local flow
cannot determine it.
Validation passes `20/20` checks; validation CSV SHA256 is
`47230465dc6ce29d0806bd6f75144505bd6392dad02d1a06d1c2d3efb1d77f70`.

Current decision:

    EAA-to-amplitude tree map                 = exact;
    current local parent amplitude insertion = calculated;
    nonlocal logarithmic slope               = derived;
    finite matching obstruction              = one additive constant;
    source-prescription lambda estimate      = calculated conditional;
    full delta_c_fin                         = open;
    leading local GR/Newton/Maxwell branch   = retained;
    exact all-operator compact GR            = false;
    full MTS                                 = false.

Next: construct and integrate the momentum-dependent C3 form-factor flow
`F_C3,k(s,t,u)` from the UV fixed-point boundary to `k=0`, enforce the 4972
logarithmic slope and 4971 factor-ten identity, and extract `delta_c_fin` at
one declared subtraction point. Do not repeat the local Wilson fit or perform
GitHub action.

## Authoritative current handoff - checkpoint 4971

Checkpoint 4971 replaces the checkpoint-4970 pure-Einstein comparator by the
active parent state-count bracket. At the tested high matching scales,

    N=2+N_s+2N_V-4N_D+N_motion,
    SM45:             N=-60,
    SM45 plus motion: N=-59.

The current functional slope corresponds to `N_eff=-8.75925881086`; it is
not the completed GR plus Standard Model on-shell flow. Forty full-parent
C3-induced splices retain matching-surface invariance to
`3.70703467922e-11`. Direct full-SM/motion p8 thresholds remain separate.

The exact current v2 two-loop four-graviton ancillary files now close the E6
projector itself:

    c(mu)=c_R3(mu)-c_GB(mu)/2,
    A_Bern=-c(mu)/(32pi^3),

    Delta R_pppp=-60cstu,
    Delta R_mppp=-6cstu,

    A_Bern=Delta R_pppp/(1920pi^3stu)
          =Delta R_mppp/(192pi^3stu).

The factor-ten relation between the two helicities is an independent future
matching check. The integration constant is equivalently one physical scale,

    lambda/mu=exp[-A_Bern/beta_A].

Running alone cannot assign `lambda`, and the current local derivative
truncation does not contain the finite momentum-dependent parent remainder.
The local-running-only route is therefore rejected, while the direct
amplitude route is now exact rather than schematic.

The E8 transfer at two endpoint scales has full rank four in the p8 subspace
and rank five after the E6 anchor. Its minimum channel determinant is
`0.00180620959558`.
Validation passes `24/24` checks; the validation CSV SHA256 is
`6a16885d61f34c2ea57ee29db096bc22abe68cd9d5cc78e5fa9fe3051e9ebd31`.

Current decision:

    full-parent state-count beta             = derived;
    SM45/SM45-plus-motion C3 splice           = calculated;
    finite all-plus E6 projector              = derived;
    finite single-minus cross-check           = derived;
    anchor free object                        = one physical scale lambda;
    numeric lambda from current local running = not derivable;
    direct parent finite amplitude            = open;
    two-scale p8 matching route               = full rank;
    direct full-SM/motion p8 thresholds       = open;
    leading local GR/Newton/Maxwell branch     = retained;
    exact all-operator compact GR             = false;
    full MTS                                  = false.

Next: checkpoint 4972 must calculate the finite Wilsonian-to-amplitude
conversion by constructing the momentum-dependent parent C3 three-/four-
graviton vertex or equivalent nonlocal form factor in the selected functional
scheme. Project both `++++` and `-+++` and require the factor-ten identity. If
the parent action cannot supply this calculation, retain `lambda` as one
explicit EFT input rather than imposing zero. Do not repeat the field-count
audit, reopen p8 scaling, or perform GitHub action.

## Authoritative current handoff - checkpoint 4970

Checkpoint 4970 advances the unmatched C3 boundary into an explicit
piecewise matching theorem for the `N_b-N_f=2` pure-Einstein vacuum branch.
A constant finite shift is impossible because

    dA_F/dt approximately -3.67837938995e-5,
    dA_OS/dt=1/(3840pi^3)=8.39883709198e-6.

The weak branch therefore replaces, rather than adds to, the functional C3
source below `t_m`:

    A_OS(t)=A_F(t_m)+delta_A_m+beta_A^OS(t-t_m),

    d delta_Bminus/dt
      =H_B delta_Bminus-12(A_OS-A_F)+xi_minus/(32pi^3),

    d delta_Bplus/dt
      =H_B delta_Bplus+xi_plus/(32pi^3).

The five-coordinate vector
`(delta_A_m,delta_Bminus_m,delta_Bplus_m,xi_minus,xi_plus)` maps to
`(A_C3,B_minus,B_plus)_end` with rank three and nullity two. One endpoint
cannot separate a primitive three-loop slope from a finite same-helicity
boundary.

Setting every finite offset to zero at every candidate matching point is
rejected as a physical prescription: the resulting endpoint has maximum
relative spread `1.06288909237`. Requiring one physical endpoint instead
derives the matching-coordinate flow

    d delta_A_m/dt_m
      =beta_A^OS-dA_F/dt_m,

    d delta_Bminus_m/dt_m
      =H_B delta_Bminus_m-12 delta_A_m,

    d delta_Bplus_m/dt_m
      =H_B delta_Bplus_m.

Across all twenty scheme/order/scale representations this transport restores
endpoint invariance to `1.1533436098526417e-11`. It removes arbitrary
matching-surface dependence but does not determine the absolute anchor.

Current decision:

    constant finite C3 map                  = rejected;
    piecewise source replacement            = derived;
    no-double-counting p8 correction        = derived;
    matching-coordinate RG transport        = derived;
    transported endpoint invariance         = pass;
    absolute finite anchor                  = open;
    primitive xi_minus and xi_plus          = open;
    complete pure-Einstein four-graviton match = open;
    full-parent matter/photon threshold beta    = open;
    exact all-operator compact GR           = false;
    full MTS                                = false.

Next: checkpoint 4971 must first add the Bern field-content and threshold
law, then calculate the pure-Einstein anchor from finite helicity-amplitude
remainders at a common subtraction scale. Use the six-derivative all-plus
coefficient for `delta_A_m` and the independent p8 same/mixed-helicity
remainders for `delta_Bminus_m,delta_Bplus_m`. Separate
`xi_minus,xi_plus` through scale dependence or a direct primitive
three-loop calculation. Do not set the anchor to zero, reopen the repaired
p8 scaling, or perform GitHub action.

Validation: `P8_Y5_BRR545_4970_VALIDATION.csv` passes `30/30`, SHA256
`fc06ce49ae48127ef407638a762aa8944028d15b365da71c5533e426b7d8ba1f`.

## Authoritative current handoff - checkpoint 4969

Checkpoint 4969 catches and repairs a real normalization error in the p8
trajectory. Since `v=k^6b` and `B=b/G^3=v/g^3`, the exact chain rule is

    beta_B=[6-3beta_g/g]B+source,
    M_p8=diag(6,6),
    B*=-source*/6.

The C3, O4 and CFF source calculations from 4967-4968 remain retained, but
their `diag(4,4)` propagation and endpoint values are superseded. All four
canonical-repaired trajectories integrate successfully. The N8 bracket is

    0.0137843312491 <= B_C <= 0.0137851876261,
   -0.0121806559340 <= B_t <= -0.0121803370306.

Primary on-shell amplitudes and the gravity pole recurrence derive the exact
pure-Einstein split

    B_minus(L)=B_minus(0)-12A_C3(0)L
               -L^2/(640pi^3)+xi_minus L/(32pi^3),
    B_plus(L)=B_plus(0)+xi_plus L/(32pi^3).

The coefficient follows the direct Bern action/log-amplitude equation,
`dA_C3/dL=1/(3840pi^3)`. Baratella's tenfold larger amplitude-coordinate
number and the published FRG factor-two discrepancy are quarantined as
normalization diagnostics, not averaged or added as another beta term.

The double logarithm is fixed by the two-loop R3 source and one-loop R3-to-R4
mixing. `xi_minus,xi_plus` are the genuinely primitive three-loop single-pole
vector and are not set to zero. At `g_match=10^-2`, the exact response is

    iterated Delta B_minus            = -0.0043074735,
    primitive Delta B/xi              = -0.0092035633,
    unmatched-boundary transfer       =  0.77827655.

The existing functional `A_C3` slope is not yet finite-matched to the on-shell
pure-GR slope, so the exact response is not double counted in the primary
candidate. The known-source compact response remains below
`9.75814718068e-234`.

Current decision:

    p8 canonical scaling                       = repaired;
    p8 relevant-parameter count                = unchanged at zero new;
    pure-Einstein iterated double log           = derived;
    primitive three-loop rank-two vector        = explicit and open;
    canonical-repaired known-source trajectory  = integrated;
    functional/on-shell C3 matching             = open;
    full finite parent p8 vector                 = open;
    exact all-operator compact GR               = false;
    full MTS                                     = false.

Next: perform the weak-scale Wilsonian-to-on-shell C3 matching and retain two
explicit four-graviton matching coordinates unless the primitive three-loop
amplitude is actually calculated. Do not restore the old p8 canonical factor,
set `xi_minus` or `xi_plus` to zero, or perform GitHub action.

Validation: `P8_Y5_BRR545_4969_VALIDATION.csv` passes `26/26`, SHA256
`3fb709b4a3771f1dd6d22fb22d8711c04e59648de1d224d59f0ff907c5ee43bc`.

## Authoritative current handoff - checkpoint 4968

Checkpoint 4968 closes the lowest-loop omitted photon/`CFF` p8 source from
4967. Starting from

    S=int sqrt(-g)[2R/kappa^2-F^2/4+c CFF],

an exact covariant field expansion gives the complete tree amplitudes

    M(h+ h+ -> gamma- gamma-)=kappa^2 c s^2/2,
    M(h+ h- -> gamma+ gamma+)=kappa^2 c t u/2,

with parity partners. Eight photon/graviton Ward replacements pass with
maximum residual `1.42492443457e-15`. Comparison with the independent
all-plus factorization result fixes `Lambda^-2=2c`.

For `q=M_P^2c=2W_C`, the direct `J=0` and crossed `J=4` identical-photon
cuts give

    dC_R4/dlnmu=0,
    dC_R4prime/dlnmu=-79q^2/(280pi^2),

    source(beta_Bminus)=0,
    source(beta_Bplus)=-79g_CFF^2/(140pi g^2).

Adding this source to all four N6/N8 GR-connected trajectories preserves
the `diag(4,4)` p8 stability block and adds zero relevant parameters. The
completed calculated N8 bracket is

    0.0138769287424 <= B_C <= 0.0138777960481,
   -0.0122356429173 <= B_t <= -0.0122353157427.

The maximum N6/N8 movement is `4.77600528411e-8`. The exact static response
on all eleven compact rows is at most `9.82370208177e-234`.

Current decision:

    complete CFF hhAA amplitude                 = derived;
    photon and graviton Ward identities         = pass;
    CFF-squared same-helicity p8 source          = exact zero;
    CFF-squared mixed-helicity p8 source         = derived;
    CFF-completed GR-connected trajectories      = integrated;
    new relevant p8 parameters                   = zero;
    source-truncated compact correction          = bounded;
    three-loop pure-Einstein p8 source            = open;
    unselected parent thresholds                 = open;
    full finite parent p8 vector                  = open;
    exact all-operator compact GR                 = false;
    full MTS                                      = false.

Next: calculate or sharply bound the three-loop pure-Einstein p8 source in
the same helicity normalization. Do not remove the derived CFF source,
reopen the complete rank-two p8 basis, identify local Wilson coordinates
with complete amplitudes, or perform any GitHub action.

Validation: `P8_Y5_BRR545_4968_VALIDATION.csv` passes `23/23`, SHA256
`80549949db0e5f8263c1e1a3741d04b3dd1a98a1d11fed593ebc53fe69362d44`.

## Authoritative current handoff - checkpoint 4967

Checkpoint 4967 extends the converged GR-connected functional trajectory by
the complete two-coordinate Ricci-flat p8 target. Primary on-shell
normalization gives

    C_R3=(3/(4pi))A_C3,
    C_R4=B_minus/(128pi^3),
    C_R4prime=B_plus/(128pi^3),

    dB_minus/dlnk=-12A_C3,
    dB_plus/dlnk=0.

The optimized natural Type-II O4 calculation independently gives

    d c_Q2/dt
      =w_O4^2 k^4(1-eta_psi/10)
       /[16pi^2(1+m_psi^2/k^2)^3].

For B_i=v_i/g^3, the p8 stability subblock at the fixed point is
`diag(4,4)`. Both directions are irrelevant, so the C3+O4 source-truncated
extension adds zero relevant parameters and UV regularity fixes both finite
coordinates.

All four N6/N8 trajectories integrate successfully. The N8 combined bracket
is

    0.0130494838053 <= B_C <= 0.0130500685321,
   -0.0130633704013 <= B_t <= -0.0130627606655.

The largest N6-to-N8 relative shift is `4.44154420413e-8`. Applying the exact
4966 Schwarzschild response to all eleven compact rows gives a maximum
source-truncated metric correction `9.23777701892e-234`.

The massive-spin threshold transfer is now exact:

    B_i^threshold=sum_s n_s c_i^(s)/(8pi mu_s^4).

For the minimal massive motion scalar, setting `rho=J_gap/chi` gives
`Delta g proportional chi/rho^2`; at the strict `rho>=10` locality gate the
largest compact row is `8.57656495653e-83`.

Current decision:

    C3 one-loop p8 map                         = derived;
    O4-squared optimized p8 source             = derived;
    source-truncated p8 UV boundary            = derived;
    new relevant p8 parameters                 = zero;
    four p8 GR-connected trajectories          = integrated;
    exact source-truncated compact correction  = bounded;
    massive-spin threshold transfer            = derived;
    photon/CFF p8 source                       = open;
    three-loop pure-Einstein p8 source          = open;
    full finite parent [B_C,B_t]                = open;
    selected static compact GR through p6       = retained;
    exact all-operator compact GR               = false;
    full MTS                                    = false.

Next: checkpoint 4968 should derive the four-graviton photon/CFF p8 helicity
projector, the lowest-loop omitted parent source. Do not identify running
`h_C3/g` with a complete physical amplitude, set omitted sources to zero,
reopen the p8 basis, or perform any GitHub action.

Validation: `P8_Y5_BRR545_4967_VALIDATION.csv` passes `22/22`, SHA256
`5261c9e6d087d6114e012da9b5b6afc677b9226e7272c9edd5e6d5c46745f273`.

## Authoritative current handoff - checkpoint 4966

Checkpoint 4966 source-locks the physical O4 normalization as

    U4=(u_O4/Z_psi)/l_P^4=utilde_O4/g^2=W_O4,

not the small UV fixed-point coordinate. Both converged N8 GR-connected
trajectories give a finite nonzero value near `-3.32247`.

The constant-z heat kernel proves that one O4 insertion has zero
derivative-free p8 source. At quadratic order the determinant gives

    Delta B_C^log
      =(3/pi)U4^2 mu_psi^4 ln(m_psi^2/mu_R^2),
    Delta B_t^log=0.

Its helicity direction `[1,1]` is independent of the 4965 minimal motion
direction `[1,6/5]`. Their direction determinant is `-1/5`; retaining all
residues gives `-U4^2/(100800pi^2)`. The known motion-sector p8 source map
therefore has rank two throughout both N8 trajectories. This is structural
rank closure, not a finite total prediction.

The static spherical response is also exact. Parity gives `Y=C.Ctilde=0`, so
`delta(Y^2)=0`, while direct symbolic variation of `K^2` gives

    Delta A=128 B_C chi^3(8-11M/r),
    Delta B=128 B_C chi^3(36-67M/r),
    chi=l_P^2 M/r^3.

The field-equation source is conserved and the tt, rr and angular equations
all close. Hence

    P_static^[B_C,B_t]=[1,0],
    P_static^[B_minus,B_plus]=[1/2,1/2].

Current decision:

    canonical O4 IR normalization                 = derived;
    linear O4 derivative-free p8 source            = exact zero;
    quadratic O4 pole/log source                   = derived;
    known motion p8 source-direction rank          = two;
    static spherical response rank                 = one;
    exact Schwarzschild B_C response               = derived;
    finite total [B_C,B_t]                         = open;
    selected static compact GR through p6          = retained;
    exact all-operator compact GR                  = false;
    full MTS                                       = false.

Next: checkpoint 4967 should calculate the motion, photon/CFF and
pure-gravity p8 thresholds in one subtraction convention and derive the
finite parent boundary or retain one bounded physical B_C LEC. Do not call a
zero logarithm at `mu_R=m_psi` a zero finite boundary, infer `B_t=0` from
static silence, reopen the p8 basis count, or perform any GitHub action.

Validation: `P8_Y5_BRR545_4966_VALIDATION.csv` passes `31/31`, SHA256
`a7963f8a10b4ab9d564da5d10d0acd2029fbbef60dcceb4b12e98f4b610cc759`.

## Authoritative current handoff - checkpoint 4965

Checkpoint 4965 proves that the selected four-dimensional Ricci-flat,
parity-even local `p8` pure-gravity target has exactly two coordinates. The
source-locked chiral count is

    C_L4+C_L2 C_R2+C_R4,

and reality plus parity leave the same-chirality sum and the mixed-chirality
operator. No derivative pure-gravity coordinate occurs until dimension ten.

The two reduced four-graviton amplitudes give

    [beta_minus]   [1 -1][beta_C]
    [beta_plus ] = [1  1][beta_t],

with determinant two and an exact inverse. The target is therefore fully
projectable with `++++` and `+--+` helicity data.

More importantly, the 4935 minimal renormalized motion Hessian now supplies
the first calculated p8 source. For `mu_psi=m_psi l_P`,

    B_minus^psi=1/(60480 pi mu_psi^4),
    B_plus^psi =1/(50400 pi mu_psi^4),
    B_C^psi    =11/(604800 pi mu_psi^4),
    B_t^psi    = 1/(604800 pi mu_psi^4).

Thus the source ray has `B_plus/B_minus=6/5` and `B_C/B_t=11`. Its stripped
C3 prefactor exactly matches the independent 4935 coefficient
`1/(483840 pi^2)`. This raises the known parent-related p8 source rank from
zero to one, but does not determine the total rank-two vector: `O4`, pure
gravity, photons and the independent p8 boundary remain to be combined.

Current decision:

    complete selected p8 basis rank               = 2;
    helicity projector rank                       = 2;
    minimal motion-scalar p8 source rank           = 1;
    current 4935 total p8 projection rank          = 0;
    total parent p8 vector                         = open;
    static compact p8 response weights             = open;
    selected static compact GR through p6          = retained;
    exact all-operator compact GR                  = false;
    full MTS                                       = false.

Next: checkpoint 4966 should derive the `O4` contribution to the same two
helicity channels and the two static compact response weights. Do not identify
the minimal scalar ray with the total parent vector, use local `A_C3^S` as a
scheme-independent dispersive input, or perform any GitHub action.

## Authoritative current handoff - checkpoint 4964

Checkpoint 4964 proves that finite local `a_R,a_C` were over-counted as two
neutral-vacuum matching inputs. In four dimensions,

    C2=E4+2 Ricci2-(2/3)R2,

and

    delta g^mn=(2/M_R2)[-2a_C R^mn+(a_R+a_C/3)R g^mn]

cancels the complete non-topological `p4` gravity bulk density at first
strict-EFT order. On matter support it gives the exact packet

    Delta L_contact
      =[2a_C T_mnT^mn+(a_R-2a_C/3)T2]/M_R4.

Therefore the independent neutral-vacuum `p4` parameter count is zero, while
full EOS/worldline contact matching remains open. The 4935 `W_plus,W_minus`
coordinates are confirmed to be photon `F4`, not gravitational `R2/C2`.

The curvature-photon sector retains one universal coefficient

    c_IR=c_nonQCD+c_QCD^r(mu).

Its action, field equation, stress, conservation and exact flat-Maxwell limit
are derived. The finite QCD value is not calibrated; 4946 proves it cannot be
obtained from lower flat or trace data alone.

For the first omitted on-shell compact tower,

    chi=l_P2 M/r3,
    epsilon_p8plus<=C8 chi3/(1-R chi).

Eleven coefficient-budget rows pass. The tightest unit-growth one-percent
budget is `C8<3.027551244686395e232` at the near-turning SLY4 star. This is
not a parent bound: neither `C8` nor `R` has been projected, and finite p6
data cannot identify an independently addable p8 operator.

Current decision:

    independent R2/C2 neutral-vacuum p4 obstruction = removed;
    full matter contact matching                    = open;
    CFF physical coefficient count                  = one;
    numeric physical c_IR                           = open;
    p8 conditional norm theorem                     = derived;
    parent p8 norm and convergence radius           = open;
    selected static compact GR through p6           = retained;
    exact all-operator compact GR                   = false;
    full MTS                                        = false.

Next: checkpoint 4965 should construct the minimal Ricci-flat p8 on-shell
basis and project its functional flow. Do not reopen the universal weak source
residue, refit C3, set `a_R/a_C` to zero, infer QCD CFF from lower data, or
promote a coefficient budget to a Wilson prediction. No GitHub action is
authorized.

## Authoritative current handoff - checkpoint 4963

Checkpoint 4963 closes the declared CP-even `p6` zero-state C3 source audit.
Four scheme/order trajectories, an independently derived logarithmic source,
and the complete inherited finite-gap displacement select

    -2.2051899226020373e-5
      <=A_C3^S<=
    -2.1871820879230358e-5,

    |a_+|<=7.564067676419907e-143 m^4.

Across nine EOS stars, a canonical 1.4-solar-mass/12-km benchmark and a
10-solar-mass Schwarzschild proxy, the largest finite residual is
7.415086500522157e-158. A deliberately conservative raw-running envelope is
1.106517857252991e-155. The running quantity is not a standalone observable;
a future physical amplitude must include the nonlocal logarithm.

The exact static multiplier identity

    integral N sqrt(gamma)
      [D_i psi J^i+psi V_eff'(psi)]=0

uses 4943 junction cancellation, 4956/4957 functional convexity and 4962 EOS
positivity. It excludes every regular disconnected scalar branch that stays
inside the certified healthy x<=0.1 chart. It does not prove all-X,
dynamical or rotating uniqueness.

Current decision:

    declared p6 C3 compact residual               = safe;
    healthy static scalar branch inside x<=0.1    = unique psi=0;
    p>=8 and nonlocal C3 completion               = open;
    finite R2/C2 and physical CFF matching        = open;
    exact all-operator compact GR                 = false;
    full MTS                                      = false.

Next: checkpoint 4964 should derive or source-match finite R2/C2/CFF
coefficients in the same normalization and bound the p>=8 compact tail. Do
not refit C3, reopen the weak source residue, or export the scalar theorem
beyond its certified domain. No GitHub action is authorized.

## Authoritative current handoff - checkpoint 4962

Checkpoint 4962 extends the selected integrated-H, exact-Diff,
reflection-even metric branch from weak test bodies to compact objects at
leading two-derivative point-particle and tensor-radiation order.

    m_A(-x_inf)=m_A(x_inf)
      -> alpha_A=0
      -> Q_A=0
      -> (alpha_A-alpha_B)^2=0.

The 4943 junction flux independently gives Q_A=0. No vector sensitivity
exists because the selected branch has no independent vector pole. A positive
integrated scalar quadratic form excludes a perturbative zero mode. Re-reading
the locked BSK24, SLY4 and DD2 tables gives nine passing stable models and a
worst central-density ratio 5.3697748471940454e-18, 17.2700 orders below the
sufficient instability threshold.

The compact matching and binary-flux chain is

    [K_ab]-h_ab[K]=-S_ab/M_R^2,
    [psi]=[n.K_eff.grad psi]=0,
    C_cons=1/M_R^2,
    C_rad=M_R^2(1/M_R^2)^2=1/M_R^2.

Thus one M_R residue controls compact conservative dynamics, wave generation
and tensor-wave stress. No second radiation G is available.

Current decision:

    selected two-derivative compact point-particle GR = true conditionally;
    first compact scalar sensitivity and dipole       = zero;
    realistic-EOS perturbative scalar zero mode       = excluded;
    all-operator compact GR                            = false;
    full MTS                                           = false.

The finite remaining compact set is C3 Wilson selection, finite R2/C2 and CFF
matching, and disconnected nonlinear scalar branches. Next: checkpoint 4963
should attack those two verdict-changing routes rather than reopen weak source
coupling or the old aether sensitivity ladder. No GitHub action is
authorized.

## Authoritative current handoff - checkpoint 4961

Checkpoint 4961 attempts the remaining integrated-`H` origin step and decides
the fork rather than returning another unsigned target.

```text
one-scalar gradient metric Jacobian rank       = 4 of 10;
one-scalar first-jet rank cap                  = 5 of 10;
connected covariance tangent rank             = 10 of 10;
spin-two gauge-map rank for every nonzero q    = 4;
regular HS inverse-kernel nullity              = 0;
Ward-compatible ungauge-fixed Hessian nullity  = 4;
4956 H_hh at g=0                              = I10;
4956 H_hpsi at g=0                            = 0.
```

The connected covariance can therefore carry a full state-dependent tensor,
but neither it nor an exact regular Hubbard-Stratonovich/composite-delta
rewrite creates an independent field with Diff redundancy. Releasing the
composite constraint and quotienting by Diff is the 4875 parent-field upgrade,
not a derivation from the scalar. The 4956 motion Hessian is also an expansion
around inherited gravity data, not a bootstrap of them.

The induced residue is

```text
M_R^2=M_0^2+W1 Lambda_UV^2/(96 pi^2)+delta M_threshold^2.
```

For a minimal real scalar and zero bare/threshold terms, matching requires
`Lambda_UV=30.7812 Mbar_Pl=6.13996 m_Pl`; one Newton measurement leaves a
rank-one matching equation with nullity two.

Current decision:

```text
integrated H and exact Diff/BRST             = explicit parent data;
current scalar/HS origin route               = rejected;
positive induced Einstein contribution       = conditional on W1>0;
absolute G prediction                        = false;
4960 weak local GR/Newton/Maxwell theorem     = retained;
strong compact-body equivalence              = open;
full MTS                                     = false.
```

Next: checkpoint 4962 must derive compact-body sensitivities, junction
matching and binary flux in this explicit parent, or produce finite strong-GR
residuals. Do not reopen the scalar-origin loop without genuinely new
microscopic tensor-gauge data. No GitHub action is authorized.

## Authoritative current handoff - checkpoint 4960

Checkpoint 4960 returns from the scattering calculation to the local coupling
throat and closes the leading coefficient problem inside the declared
integrated-`H`, exact-Diff/BRST parent.

```text
deltaS_m/deltaH^munu=-(T_mn-g_mnT/2)/2,
rank(R4)=10,
R4^2=I,

ker(C_soft)=ker(C_Bianchi,connected)
 =span{(1,1,1,1,1)},

(a/2)^2[4K^-1/(M_R^2a^2q^2)]
 =K^-1/(M_R^2q^2).
```

Thus the leading gravitational coefficient is universal rather than a
primitive species/material/arena vector. The complete retained 4947 chain is
re-executed: 14 source rows, 10 limits, 9 calibrations and 5 no-retuning arena
rows pass. Einstein, Newton, geodesic, weak PPN, Maxwell, Lorentz and Poynting
all use the same declared parent residues.

Current decision:

```text
leading local source coupling in integrated-H parent = derived;
weak local GR/Newton/Maxwell ladder                  = promoted conditionally;
integrated H and Diff from motion scalar             = false;
visible matter and U1 ontology from motion           = false;
strong compact-body equivalence                      = open;
full MTS                                             = false.
```

Next: attempt the integrated-`H`/Diff origin and induced positive EH residue
from the motion Hessian without re-entering Weinberg-Witten. If that origin
cannot be derived, retain the field and symmetry as fundamental parent data
rather than hiding them as emergence. No GitHub action is authorized.

## Authoritative current handoff - checkpoint 4959

The essential gravity-motion trajectory at 4958 retained one relevant
direction and reached the Gaussian GR regime, but its physical six-scalar
amplitude lacked the independent `O2`, `O3` and `O4` projectors. Checkpoint
4959 now derives all three.

```text
M6=u_X2^2P_X2+v_X3P_X3+kappa w_O2P_O2
   +kappa^3h_C3P_O3+kappa^2u_O4P_O4.
```

The `O2` contact requires four scalar-leg attachments; their sum passes the
Ward identity. `O3/O4` are obtained from pair-sourced linear Weyl tensors.
Two rational events give exact `X3/O2` determinant `175/41472`, so no value
of the open coefficient `w_O2` can erase the forced `X3` channel. Four
`32768`-event replicas leave about `86.1%` of the leading rate after the best
possible `O2` cancellation.

The old absolute scalar kernel was low by exactly `256` because
`u_X2=4a2`; ratios, fixed points and trajectory shapes are unchanged.

Current decision:

```text
essential combined fixed point and trajectory = retained;
complete p6 projector amplitude form           = derived;
arbitrary-O2 positive rate floor               = derived;
unique w_O2 coefficient and rate               = open;
4947 local GR/Newton/Maxwell branch             = retained;
universal parent matter/source map              = priority open;
galaxy rate and full MTS                        = false.
```

The next work returns to the universal local source-coupling derivation. The
`O2` momentum flow remains a parallel precision-coefficient task and must not
replace the GR/Newton/Maxwell priority. No GitHub action is authorized.

## Where we are

Checkpoint 4932 finds and hash-locks a real essential photon-gravity
functional flow in the exact canonical `CFF` normalization. Its closed
four-derivative coordinate set is

```text
{g,g_plus,g_minus,g_CFF},

g=k^2G_N,
g_plus =(g_F2sq+g_F4)/2,
g_minus=(g_F2sq-g_F4)/2,
g_CFF=k^2G_CFF.
```

This corrects the previous reduced portal slice: both independent `F4`
directions are required in the nonperturbative `CFF` flow.

The published most predictive interacting fixed point is

```text
FP1=(0.131,0.351,3.327,0.00375),
theta={1.845,-0.239+/-0.0155i,-0.291}.
```

It has one relevant direction and is connected to the Gaussian/GR infrared
regime. It proves that an interacting photon-gravity fixed point need not have
`g_CFF*=0`. It is an external comparator, not yet the MTS point.

The MTS normalization map is exact:

```text
c_gamma=G_CFF,
u_gamma=k^2c_gamma=g_CFF.
```

The unique external FP1 infrared endpoint gives

```text
W_C=lim G_CFF/(16piG_N)=0.000550.
```

Conditional on full MTS inheritance,

```text
c_gamma^parent,FP1,IR
 =16pi ell_P^2W_C
 =7.221914138634598e-72 m^2.
```

The known electron threshold is `1.332274019549677e41` times larger. The
conditional ultraviolet parent term would therefore be negligible in the
low-energy EM ledger, but it is not the total coefficient and does not replace
QED/QCD/EW matching.

The FP1 beta-spectrum gap is

```text
delta_FP1=0.239.
```

The sufficient enlarged modal stability condition is now

```text
||E_modal||_2<0.239,
```

which is `7.866` times tighter than the pre-photon comparator. The exact full
matrix remains preferable.

The primary paper, source archive and official Mendeley notebook are hash
locked. The notebook contains the trace inputs but no stored output cells; it
was not locally re-executed with Wolfram/xAct. No independent execution is
claimed.

Full MTS inheritance is still open because the source truncation omits `C3`,
the MTS motion block and full visible matter. The next calculation is the
smallest combined block capable of deciding the issue:

```text
4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md
```

It must include both `F4` directions, construct or bound the `C3-CFF-F4`
mixing matrix, and either solve the enlarged common zero or fail the `0.239`
inheritance gate. No GitHub action has been taken.

## Previous checkpoint 4931

Checkpoint 4931 resolves the first gauge-curvature portal fork. For

```text
u_X=k^2c_X,

beta_uX=(2+gamma_X)u_X+b_X+O(u_X^2).
```

The source-locked minimal massless Einstein-Maxwell and Einstein-Yang-Mills
systems have

```text
b_X^(1)|u_X=0=0
```

in the on-shell one-loop basis. Thus `u_X=0` is a perturbative additive-zero
manifold. The strict canonical comparator gives

```text
beta_u=2u,
u*=0,
theta=-2.
```

This is not the full MTS fixed point: `gamma_X`, higher loops and the mixed MTS
functional trace remain open.

Massive charged matter generates a finite threshold,

```text
Delta c_gamma
 =-Q^2alpha_EM/(360pi)(hbar/(mc))^2.
```

The calculated free-particle baseline is

```text
c_gamma,e       =-9.621568578321357e-31 m^2,
c_gamma,e+mu+tau=-9.621794423569482e-31 m^2.
```

This is a free-lepton subtotal, not the full Standard-Model threshold. The
correct infrared decomposition is

```text
c_gamma^IR
 =c_gamma^parent+c_gamma^free-leptons
  +c_gamma^QCD+c_gamma^EW+... .
```

Electroweak rotation gives

```text
c_gamma=c_B cos^2(theta_W)+c_W sin^2(theta_W),
c_Z=c_B sin^2(theta_W)+c_W cos^2(theta_W),
c_AZ=2sin(theta_W)cos(theta_W)(c_W-c_B).
```

Photon data therefore constrain one `c_B,c_W` strip. The full retained
electromagnetic variation and characteristic are

```text
H=F-4c_gamma C.F,
nabla.H=J,
nabla.J=0,
nabla.T_EM,total=-F.J,

[k^2I-8c_gamma k.C.k]a=0.
```

The local dimension-six effect is polarization birefringence without leading
frequency dispersion. In Schwarzschild,

```text
abs(Delta v_pol)/c
 =12abs(c_gamma)M_geom/r^3+O(c_gamma^2).
```

Real source acquisition gives

```text
PSR B1534+12 original positive side:
  c_gamma<6.0e6 m^2;

M87* thin-ring case:
  abs(c_gamma)<2.85156e25 m^2.
```

The pulsar result is legacy, one-sided and model conditional. The M87 result
is two-sided but explicitly a case study. The old radar source has internally
inconsistent numbers and is quarantined. Known QED is over `6.23e36` below the
pulsar scale, but this does not predict the MTS parent residual.

Current decision:

```text
massless one-loop additive portal source  -> zero derived;
strict-canonical portal point             -> u*=0 theta=-2 comparator;
finite charged-Dirac threshold            -> derived and numeric;
photon/stress characteristic              -> derived;
legacy PSR and modern M87 scales          -> sourced conditional;
known QED baseline                        -> overwhelmingly safe;
full MTS portal fixed point               -> open;
nonleptonic threshold matching            -> open;
robust joint polarization likelihood      -> open;
weak GR/Newton                            -> retained;
compact and full MTS-to-GR                -> not promoted.
```

Direct next target:

`4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md`

No GitHub action or public claim is authorized.

## Previous checkpoint 4930

Checkpoint 4930 closed the complete CP-even six-derivative motion-scalar
quotient and the complete dimension-six gravity-SM quotient:

```text
motion scalar plus gravity: 5 operators O1-O5;
gravity plus Standard Model: 10 operators in 5 parity pairs.
```

With scalar anomalous dimension it derived

```text
Q_-1=-eta_s/k^2,
Delta beta_h=eta_s/[30240(4pi)^2]
```

and retained the inherited topology in `9801/9801` direct-leak rows. It
rejected generic exact block triangularity through

```text
(1/2)Tr log(I-4u_XC)
  contains -(32/3)d_Xu_X^3TrC^3,
```

then replaced it with the sufficient signed stability contract

```text
||E_modal||_2<1.88.
```

The vacuum/full parity-even Wilson count was separated as `1/9`; weak
GR/Newton was retained and the electromagnetic portal became checkpoint 4931.

## Previous checkpoint 4929

Checkpoint 4929 added visible matter, electromagnetism and one conditional
ultraviolet motion scalar to the `C^3` fixed-point question at leading
free-spectator order. It derived

```text
W3=N_s-4N_D+2N_V=W0,

Q_-1[W]=-W'(0)=0,

beta_g=beta_g^(grav)+W1g^2/(6pi),
beta_h=beta_h^(grav)
```

for the complete natural Laplace operator with the optimized regulator and
zero matter anomalous dimension. All 18 benchmark rows and all 6,642 wide-scan
rows retained the tested two-coordinate fixed-point topology. The optimized
conditional separatrices gave

```text
A_C3=2.9979025e-6 to 3.0396516e-6,
ell_+=1.7907367e-36 to 1.7969389e-36 m.
```

The proper-time source was quarantined as a shifted-Gaussian diagnostic. Full
interacting operator closure, anomalous dimensions and the enlarged stability
matrix remained open and became checkpoint 4930.

No GitHub action or public claim is authorized.

## Previous checkpoint 4928

Checkpoint 4928 has now executed the ultraviolet mechanism that was previously
only a possibility. The primary 2026 source includes an attached notebook with
the natural-regulator pure-gravity beta functions. Independent integration
gives

```text
g_*      =0.5890486225480862,
g_C3,*   =-3.242484275319408e-7,
theta    =(+2.78260869565,-7.75000535537),
G_C3/G_N =3.024098389340624e-6
```

on the unique separatrix after fixing the unit scale. The exact infrared
logarithmic coefficient is

```text
c_log
 =69/(725760pi^3)
 =3.066242112944727e-6.
```

The article prose prints the opposite sign, but the attached beta notebook,
the independently reproduced positive limit and the article's own
`k0/M_Pl approximately 0.37` sign crossing all require the positive sign. The
discrepancy is recorded rather than silently ignored.

The exact MTS operator map is

```text
zeta_+=G_C3,
a_+=16pi G_N G_C3.
```

Thus the conditional natural pure-gravity branch has

```text
a_+/l_P^4 =1.520077645389635e-4,
ell_+     =1.794635816842645e-36 m.
```

It is safely below compact bounds by over 150 coefficient orders. The
four-dimensional constant `H`-to-`g` Jacobian and common `I1=C3` basis prove
kinematic compatibility with integrated `H`. Full dynamic inheritance is not
yet established because the current parent does not select the natural
gravity/ghost regulator, a zero-cosmological ultraviolet trajectory, the full
matter/EM/motion beta functions, their fixed point and stability matrix, or
the `k0=M_Pl` transition scale.

Current decision:

```text
pure-gravity C3 functional flow          -> calculated;
unique separatrix and IR coefficient     -> independently reproduced;
source log-sign discrepancy              -> found and quarantined;
integrated-H kinematic inheritance       -> derived;
full MTS dynamic flow inheritance        -> open;
conditional fixed-point compact safety   -> overwhelming but nonclaim;
observational low-energy I1 parameters   -> exactly one A_+(Q_GW);
weak invariant-vacuum GR/Newton/Maxwell  -> retained;
compact vacuum/matter and full MTS       -> not promoted.
```

Direct next target:

`4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md`

Calculate the leading visible-matter, EM and motion-sector deformation of the
natural essential flow. Test whether the non-Gaussian fixed point and its
one-relevant-direction critical surface survive. If a controlled
matter-completed projection cannot be constructed, retain the one
observational Wilson coefficient without reopening the closed normalization,
measure or all-mass loop questions.

No GitHub action or public claim is authorized.

## Previous checkpoint 4927

Checkpoint 4927 resolves the apparent motion-normalization parameter without
choosing an arbitrary value. The old covariance map requires

```text
[B_old]=-5,
B_psi=B_old M_N,
[B_psi]=-4,
```

so both the original coefficient-one map and the later `ell_*^2` map are
dimensionally superseded. Under the exact old-field coordinate change

```text
phi_old'=s phi_old,
M_N'=s^2 M_N,
lambda_old'=s^(2/3)lambda_old,
B_old'=s^-2 B_old,
```

the physical combinations

```text
g_psi=lambda_old M_N^(-1/3),
B_psi=B_old M_N
```

remain invariant. Hence `C_N=M_N/M_Pl` is a redundant field coordinate, not
an undetermined physical coupling. Closed stress correlators independently
confirm this: each old-coordinate stress vertex contributes `M_N^-1` and each
propagator contributes `M_N`, so every `n`-stress loop is independent of
`M_N`. The measured Einstein residue cannot select a coordinate convention.

The exact massive-scalar Weyl form factor also gives the global theorem

```text
-1/60 <= d k_W/d ln(q^2/m^2) <= 0,
abs Delta k_W <= ln(q_h/q_l)/30.
```

A 405-row scan spanning `m/q_h=1e-20` through `1e20` closes heavy, crossover
and nonlocal regimes against this bound. The largest deliberately conservative
one-real-scalar transfer displayed from AU to nuclear scales is
`2.5057690980704453e-39`. Thus uncertainty in the invariant motion gap no
longer blocks local GR through finite-multiplicity scalar loops.

Current decision:

```text
C_N old-field normalization             -> redundant coordinate, removed;
g_psi, mu and B_psi                     -> invariant physical quantities;
coefficient-one and ell_*^2 maps        -> dimensionally superseded;
Einstein residue determination of C_N   -> impossible by exact cancellation;
all-mass finite scalar-loop transfer    -> bounded and locally negligible;
weak invariant-vacuum GR/Newton/Maxwell -> retained;
finite integrated-H/QCD a_IR            -> unresolved single Wilson input;
compact vacuum/matter and full MTS      -> not promoted.
```

Direct next target:

`4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-observational-Wilson-freeze.md`

Return to the actual compact-GR obstruction: derive the integrated-`H`
functional-flow boundary for the parity-even Weyl-cubic coefficient. If the
parent supplies no fixed-point or boundary condition, retain exactly one
explicit observational Wilson coefficient rather than reopening motion-field
normalization.

No GitHub action or public claim is authorized.

## Previous checkpoint 4926

Checkpoint 4926 has replaced the unspecified threshold spectrum with a
source-locked calculation and repaired the old motion-scale dimensions.
For every colorless massive free field satisfying the local expansion,

```text
a_i=r_i l_P^2(hbar c/m_i)^2/(30240pi).
```

PDG 2026 masses and four NuFIT 6.0 neutrino benchmarks give

```text
max abs(a_visible)^(1/4)=1.557659434600340e-21 m,
max abs(a_visible)/ell_NS^4=4.044516337887705e-98.
```

The exactly massless benchmark state, photon and gluon remain nonlocal. No
free-quark infrared sum is made; all colored dynamics form one interacting QCD
matching block. Normalizing that block with the neutral-pion scale shows that
compact saturation would need `abs(C_QCD)=2.4767e118`, but this is a
naturalness firewall rather than a three-stress spectral theorem.

The printed motion coupling has mass dimension three and cannot equal the
canonical fractional-potential coefficient of dimension `8/3`. Dimensional
homogeneity derives

```text
[phi_old]=3/2,
S_old=M_N^(-1) integral d4x [kinetic+potential],
psi=phi_old/sqrt(M_N),
g_psi=lambda_old M_N^(-1/3),
mu=lambda_old^(3/8)M_N^(-1/8).
```

Writing `M_N=C_N M_Pl` and using the old `Phi_G` formulas gives

```text
mu=Phi_G^(3/2)C_N^(-1/8)M_Pl.
```

The conditional minimal benchmark `C_N=1` has

```text
mu=2.512800690133141e28 eV,
ell_motion=6.349828232642897e-37 m per central-pilot real pole.
```

It is not promoted. For one pole the compact floor only requires
`C_N<4.2739934e634`, so the normalization dependence is exactly known and
extremely weak without being derived.

The active matching equation is

```text
a_IR
 =a_unresolved^R+a_visible+a_motion+Delta a_GS,

a_unresolved^R
 =a_UV,H^R+a_QCD^R+a_MTS,res^R.
```

The provenance labels inside `a_unresolved^R` do not add fit dimensions. Local
tests still have one signed `a_IR`. Known thresholds are compact-safe, but the
finite UV/QCD remainder is not derived, so compact GR remains unpromoted.

Current decision:

```text
known colorless thresholds             -> calculated and compact-safe;
massless local-threshold misuse        -> removed;
free-quark infrared sum                -> removed;
motion dimensional repair              -> derived;
motion C_N normalization               -> open;
QCD and finite UV matching             -> one unresolved IR remainder;
independent parity-even I1 test inputs  -> one;
weak invariant-vacuum GR               -> retained;
compact vacuum/matter and full MTS     -> not promoted.
```

Direct next target:

`4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md`

Try to determine `C_N` from the normalization of the old gradient-covariance
metric map, the canonical motion stress residue and the selected Einstein
residue. If that coefficient is a pure field convention, prove the redundancy
and retain one empirical `a_IR` rather than creating another closure.

No GitHub action or public claim is authorized.

## Previous checkpoint 4925

Checkpoint 4925 removed a false multiplicity in the finite Weyl-cubic problem.
For

```text
H^{mu nu}=sqrt(abs(g))g^{mu nu},
```

the exact pointwise Jacobian is

```text
abs det[dH/dg]
  =abs(d-2)/2 abs(g)^[(d+1)(d-4)/4]
  =1 in four dimensions.
```

The displayed `D H` coordinate measure therefore creates no hidden local
`C^3` term. The bare coefficient and scheme-dependent metric/ghost finite
piece collapse into one renormalized coefficient,

```text
a_eff(Q)
 =a_UV^R(mu_U)
  +sum_i Delta a_i^threshold
  +[209/(1440pi^2)]l_P^4 ln(Q/mu_U).
```

At one reference scale this is one signed `a_IR=s_plus ell_IR^4`. The free
threshold ratios are `r_scalar=+1`, `r_Dirac=-4`, `r_Proca=+3`. The current
conservative GW250114 envelope is `abs(ell_IR)<=49.228989 km`, a private
nonclaim that remains above the compact target.

## Previous checkpoint 4924

Checkpoint 4924 returns from the observational bound to the finite parent
coefficient. The motion-scalar determinant now gives, per healthy real pole,

```text
zeta_plus_scalar
  =F/[30240(4pi)^2m_gap^2],

a_plus_scalar
  =G F/[30240pi m_gap^2],

sign(zeta_plus_scalar)=positive,
zeta_minus_scalar=0.
```

With `m_gap=c_m lambda^(3/8)`, the nonpromoted 4909 mass-gap pilot maps to

```text
c6_central=2.0077121007e-7,
c6 union=[1.4801479971e-7,3.9533795366e-7]
```

per real pole. This is an exact transform of a pilot, not a promoted
continuum coefficient.

The pure-gravity running is now in the corrected canonical I1 coordinate:

```text
Delta a_plus
  =[209/(1440pi^2)]l_P^4 ln(mu/mu0),

ell_plus_GS=0.3482338723l_P per unit logarithm.
```

The scalar threshold alone reaches the selected one-percent neutron-star
domain if a one-real-pole motion scale obeys

```text
mu>1.17843e-51 eV
```

after conservative c_m propagation. The parent still does not fix mu or the
physical pole multiplicity.

The total coefficient cannot be obtained from the scalar determinant alone.
I1 is symmetry allowed, and the quantum public metric has a nonzero two-loop
I1 pole. A counterterm-complete parent therefore requires an independent
finite boundary `a_plus,b(mu0)`. Measured G fixes the Einstein residue, not
that boundary.

Current decision:

```text
motion-scalar finite threshold       -> derived per real pole;
motion-scalar sign                   -> positive;
universal I1 running                 -> derived and negligible;
interacting scalar residual          -> no nonzero value promoted;
finite I1 renormalization boundary   -> required but unowned;
total zeta_plus magnitude and sign   -> not derived;
weak invariant-vacuum GR             -> retained;
compact vacuum/matter and full MTS   -> not promoted.
```

Direct next target:

`4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md`

Search the integrated-H UV measure for a real boundary condition. If none
exists, freeze one explicitly bounded Wilson input instead of presenting the
positive scalar threshold as the total.

No GitHub action or public claim is authorized.

## Previous checkpoint 4923

Checkpoint 4923 acquired and checksum-verified the complete official
GW250114 companion release, extracted the pSEOB posterior, and performed the
coefficient-level gravitational-QNM recast that checkpoint 4922 required.

The active coefficient and observable map are

```text
alpha_ev=alpha_bar1=s_+(ell_+/M)^4,
omega=omega_Kerr+[alpha_ev/M]deltaomega_branch(chi),
deltahat_f=alpha_ev Re(deltaomega)/Re(Momega_Kerr),
deltahat_tau=-alpha_ev Im(deltaomega)/Im(Momega_Kerr).
```

The paper's 440 reporting cut retains `17,742` pSEOB samples. Enforcing the
source-backed gravitational-QNM endpoint `chi_f<=0.7` retains `17,719`,
or `99.8704 percent` of that set.

The two parity-even branches give

```text
polar plus:  -0.01687 < alpha_ev < 0.03195 at 90 percent,
axial minus: -0.04306 < alpha_ev < 0.02104 at 90 percent.
```

Both include GR and have Delta-chi-square proxies below `0.54`. They are not
combined: the parent does not yet predict the polar/axial excitation weights.
The measured 440 deviations are not converted because the theory source has
no cubic 440 coefficients.

Bandwidth, spin and five-percent theory-coefficient variations give
`max abs(alpha_ev) approximately 0.054`. The inherited compact proxy is

```text
epsilon_h=(3/4)abs(alpha_ev) approximately 0.040
```

on that robust envelope. This is far tighter than the old positive GW170608
endpoint but still about four times above the selected one-percent compact
certificate.

Current decision:

```text
official GW250114 release and 220 map -> closed;
nonzero cubic signal                    -> not supported;
weak invariant-vacuum GR                -> retained;
compact vacuum/matter GR                -> not promoted;
parent finite zeta_+ and sign           -> not derived;
polarization excitation                 -> not derived;
MTS-to-Maxwell and full MTS-to-GR       -> open.
```

Direct next target:

`4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md`

Return to the selected parent determinant and calculate the finite
renormalized `zeta_+` and its sign, or prove that an independent finite
counterterm is part of the theory definition. The GW intervals are now a
clean target for that calculation, not a substitute for it.

No GitHub action or public claim is authorized.

## Previous checkpoint 4922

Checkpoint 4922 corrects the coefficient-coordinate error discovered in the
4921 cubic route. The active corpus packet is

```text
O_+=I1=C7,
a_+=16 pi G_N zeta_+=s_+ell_+^4,
ell_+=abs(16 pi G_N zeta_+)^(1/4).
```

Burger's displayed `r^-6` potential depends on `lambda beta1`, while the
smooth Ricci-flat quotient gives

```text
zeta_+=lambda(beta2+beta1/2).
```

The counterexample `beta1=0`, `beta2!=0` proves that old `L3` is not
invertible to `zeta_+`. The 4921 Galileo, Cassini and Mercury bounds are now
historical Burger-`beta1` benchmarks only. Do not use them in the active GR
certificate.

The sourced pure-`I1` metric instead gives

```text
N^2f=1-2M/r+40s_+ell_+^4M^3/r^7,
delta Phi=-20s_+ell_+^4M^3/r^7,
abs(delta a/a_N)=140ell_+^4M^2/r^6.
```

The exact GW170608 coefficient map and published 90-percent result are

```text
alpha_bar1=s_+(ell_+/M_geo)^4,
-0.16<alpha_bar1<2.82,
-3.27<alpha_bar2<3.77,
log B_EFT/GR=-2.81.
```

Thus

```text
s_+=-1: ell_+/M_geo<0.6324555,
s_+=+1: ell_+/M_geo<1.2958725.
```

Using the paper's approximate `12+7 solar mass` description gives illustrative
limits `17.7446 km` and `36.3579 km`. The dimensionless interval is the
authoritative result because mass-coupling posterior samples are not local.

The corrected positive-endpoint weak projections are

```text
Galileo alpha_clock            = 1.3098771e-26,
Earth abs(delta a/a_N)         = 7.1957602e-26,
Earth ell_+^4K                 = 2.4671178e-26,
Sun ell_+^4K                   = 1.6131431e-27.
```

The active strong-domain variable is

```text
epsilon_K=ell_+^4K,
epsilon_h=(3/4)abs(alpha_bar1).
```

GW170608 permits `epsilon_h=0.12` or `2.115`, exceeding the one-percent
horizon target by factors `12` and `211.5`. The bound therefore protects the
weak branch but does not certify compact curvature. It also does not derive
the finite MTS `zeta_+`.

Current decision:

```text
4921 L3 total-C3 interpretation -> superseded;
invariant zeta_+ waveform map   -> closed;
direct GW170608 bound           -> closed;
weak invariant-vacuum GR       -> retained after corrected transfer;
compact vacuum/matter GR       -> not promoted;
parent finite zeta_+            -> not derived;
direct pure-I1 Maxwell shift    -> zero at fixed metric;
full MTS-to-GR/Maxwell          -> open.
```

Direct next target:

`4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md`

Attempt an exact coefficient-level recast of the GW250114 ringdown information
with the finite-spin gravitational QNM series in arXiv:2307.07431, after
checking the remnant spin and posterior products. Do not use arXiv:2604.11755:
it computes scalar perturbation modes, not the gravitational modes in the
data. If the compatible products are insufficient, record the precise
acquisition blocker rather than converting a generic QNM deviation into
`ell_+`. Do not confuse a tighter observational upper limit with a parent
derivation.

No GitHub action or public claim is authorized.

## Previous checkpoint 4918

Checkpoint 4918 resolves the hidden-state profile without pretending that a
microscopic bath and the active low-energy action are the same layer.

The microscopic parent contains `psi,X`, but the active Wilsonian action
integrates them once into renormalized metric coefficients and uses

```text
Gamma_MTS,res = 0.
```

It therefore has no independent bath source:

```text
T_X = h_X = tau_X = 0;
p_mix = sigma_mix = kappa_clock = 0.
```

This is a field-content theorem for the declared active action, not an
assertion that a retained physical bath has zero stress. A nonvacuum bath is
an explicit extension. An invariant hidden vacuum independently obeys

```text
<T_X^mn> = -rho_v g^mn;
p_X      = -rho_v;
h_X      = 0.
```

The exact 4896 closed-parent sources are

```text
rho_B/M_R^2 = D+(K_chi+I_m)/2-phi Y
              +C_phiphi phi^2/2-C_thetatheta theta^2/2;
h_B/M_R^2   = D+K_chi-qJ-bdot;
tau_B       = 3h_B-4rho_B.
```

Eight archived profile rows reconstruct Raychaudhuri below `4.45e-16`, but
the generating bath cosmology remains retired. At `z=0` it has

```text
rho_B/(3M_R^2H^2) = 0.0490000;
h_B/(3M_R^2H^2)   = 0.3989649;
tau_B/(3M_R^2H^2) = 1.0008947.
```

The selected minimal matter-loop ray is

```text
a_C,loop = L/(128 pi^2);
a_R,loop = L/(384 pi^2);
a_R/a_C  = 1/3.
```

The complete renormalized coefficients retain finite, threshold and
integrated-H/ghost pieces. On the retired present profile the loop shifts are
only `p_mix/L=-2.64164e-123` and
`kappa_clock/L=-7.14483e-124`.

The correct clock combination is

```text
kappa_clock = p_mix/2-sigma_mix
            = [-4a_C rho_X
               +2(a_R-2a_C/3)tau_X]/M_R^4.
```

Galileo gives `abs(Delta kappa_clock)<=1.35481e-14` for the adopted
Earth-to-satellite geometry. A constant common shift calibrates out. The
universal contact gives `eta_AB=0` at test-body order because every ordinary
body follows the same matter metric.

Decision:

```text
active state-flow contact             -> exact zero by IR field content
invariant-vacuum enthalpy             -> exact zero by state symmetry
nonvacuum rho/h/tau profile           -> derived retired diagnostic
selected matter-loop curvature ray    -> derived
total a_C/a_R                         -> open matching sums
clock profile-difference bound        -> sourced
universal-contact test-body WEP       -> exact zero
full vacuum mixed 1PI basis           -> open
local GR/Newton/Maxwell baseline       -> retained
```

Direct next target:

`4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md`

Calculate the surviving mixed operators in the invariant vacuum after the
flow-spurion basis is removed. Begin with `R H_SM^dagger H_SM` and any hidden
scalar vacuum expectation value, separate field-basis redundancies from
physical terms, and project the irreducible remainder into Higgs, clock, WEP
and local-gravity bounds.

No GitHub action or public claim is authorized.

Checkpoint 4893 directly solves the missing parent response from `k=0` to
CAMB's minimum mode. The infrared limit agrees to `1.52e-7`, the momentum
residual stays below `2.86e-6`, and low-ell TT now has more than `99.999%`
power coverage. The revised shifts are `+1.081%` at `ell=2` and `+1.219%` at
`ell=4`.

The high-k point branch is rejected rather than hidden. Raw evolution loses
the momentum constraint; a momentum-projected branch violates the clock
equation by at most `2.77%`. Their Weyl difference is bounded by `1.216e-4`,
which makes the full-k linear lensing envelope narrow (`3.66e-5` maximum
angular width) and suppressive through `L=400`.

The exact adjoint FDT filter matches the four forward impulses to `8.69e-6`
and rejects checkpoint 4892's `Lambda=0.3` bath point by a factor `1.72066`.
At normalized `Theta=0.1`, today requires `Lambda<=0.2517166`, but no parent
damping, memory, or carrier scale selects it.

Direct next target:

`4894-Y5-R2FR-parent-nonlocal-bath-kernel-self-consistent-Einstein-Boltzmann-or-cosmology-source-demotion-gate.md`

This is a decisive route: compile the full retarded nonlocal bath kernel into
the perturbation system and test momentum, clock, and FDT covariance together.
If it cannot close them, demote the cosmological bath-source branch. No GitHub
action or public claim is authorized.

Checkpoint 4892 fixes the CAMB transfer normalization and inserts the solved
parent Weyl response into the exact non-Limber late-ISW and lens-potential
sources. The central fixed-background result gives `+1.02--1.24%` low-ell TT,
`-1.25--1.35%` low-ell lens potential, and a positive `T-phi` cross shift. The
non-Limber lens result independently agrees with checkpoint 4891's Limber
route to `8.84e-5` absolute fractional shift.

A positive normalized super-Drude KMS state is now constructive:

```text
(Lambda_bar,Theta_B,DeltaN)=(0.3,0.1,1)
Var I=0.0210361 < 0.0282438
```

The vacuum bound `Lambda_bar DeltaN<=0.434222` means the admissible state is
non-Markovian; it cannot be used to justify a broad local damping closure.
The parent still must select its cutoff, temperature, and physical cell
measure.

No CMB claim is made. Low-ell TT needs `R_W` below `0.001 h/Mpc`, high-ell
lensing needs it above `0.1 h/Mpc`, and the fixed-background insertion must
eventually become one self-consistent parent Einstein--Boltzmann run.

Direct next target:

`4893-Y5-R2FR-infrared-Weyl-response-full-CMB-transfer-and-parent-bath-cutoff-selection-or-CMB-likelihood-demotion-gate.md`

Checkpoint 4879 promotes a private conditional classical local-GR certificate through 1PN for the selected metric-only strict-EFT branch.

The finite local curvature-squared terms are explicitly field-redefined into

```text
DeltaS_contact = Mbar^-4 int sqrt(-g)
  [2 aC T_mn T^mn + (aR-2aC/3) T^2].
```

For two finite sources with a positive separation, every `AB` cross product vanishes. Self terms renormalize measured body/worldline coefficients but do not create an extra force across the vacuum gap. This closes the finite-source R10 contact route rather than merely bounding it.

The two-heavy-source/any-graviton theorem then gives the operational classical values

```text
gamma = 1;
beta  = 1;
delta gamma_R2C2 = delta beta_R2C2 = 0.
```

The MESSENGER central value is `0.692 sigma` from `beta-1=0`.

The physical minimal point-clock monopole gives

```text
etaClock = 8.73090378e-70 m^2;
alphaClock = 2.71364489e-83.
```

The on-shell photon eikonal reproduces the GR one- and two-PM angles. Retaining the detector-resolution logarithm and imposing the deliberately broad `|log|<=100` envelope gives

```text
abs(delta theta total) < 4.30928e-91 rad;
abs(gamma-1)_equivalent < 1.62418e-85.
```

The certificate covers weak four-dimensional fields, minimally coupled positively separated sources, the selected metric-only branch and momenta below the EFT cutoff. It does not cover strong-field GR, primitive `H`/Diff ownership, nonminimal flow, curvature-cubed operators or composite-clock finite-size response.

Checkpoint 4878 selects the strict renormalized-EFT local branch and removes a category error. The exact scalar/spin-2 transfer is

```text
Phi/PhiN = 4/(3 A2) - 1/(3 A0);
Psi/PsiN = 2/(3 A2) + 1/(3 A0);
gamma    = (2 d0+d2+3)/(4 d0-d2+3).
```

For finite local curvature-squared terms,

```text
d0_local = 12 aR lbarP^2 q^2;
d2_local = -4 aC lbarP^2 q^2.
```

At first strict-EFT order, `q^2` cancels the Newton propagator and leaves contact distributions. Hence local `R2/C2` operators do not generate an exterior Yukawa force between separated source supports. The R10 Yukawa curve now belongs only to a separately labelled resummed diagnostic.

The universal matter logs have position-space coefficients

```text
etaPhi = 5.32169373e-70 m^2;
etaPsi = 2.70704212e-70 m^2;
etaSlip = 2.79943264e-70 m^2.
```

The physical pure-gravity Newton tail supplies

```text
etaGrav = (41/(10 pi)) lP^2 = 3.40921005e-70 m^2;
etaN_total = 8.73090378e-70 m^2.
```

Derived arena envelopes are `9.69e-61` for R10 acceleration, `1.30e-87` for the matter-loop Cassini deflection-equivalent gamma residual, `1.65e-83` for Galileo redshift and `4.58e-82 arcsec/century` for Mercury. Minimal Maxwell remains exact at this order.

This is not yet a full local-GR claim. The direct next work is finite-source contact matching, nonlinear PPN beta, and gauge-invariant pure-gravity clock/light response. The R10 power-law tail also needs apparatus convolution before any likelihood claim.

Checkpoint 4877 decides the signed-spectrum fork. The primitive corpus is bosonic as written and contains no Grassmann measure, Dirac kinetic operator, Clifford module or spin-statistics derivation. Its healthy one-loop matter spectrum therefore obeys

```text
W0 = Ns + 2 Nv > 0,
```

and cannot cancel the quartic vacuum term. The imported Standard Model benchmark has positive Einstein weight but nonzero vacuum weight. The four-scalar/one-Dirac example is proven threshold-rigid, so it remains an existence proof rather than an MTS mechanism.

The ordinary scalar/Dirac/Maxwell weights are now

```text
W0 = Ns + 2 Nv - 4 ND;
W1 = Sh + 2 ND - 4 Nv;
WC = Ns + 6 ND + 12 Nv.
```

The universal matter-induced nonlocal completion is explicit:

```text
Gamma_nl = -int sqrt(-g)[WC C log(-Box/LambdaUV^2) C/(3840 pi^2)
                         +Sh2 R log(-Box/LambdaUV^2) R/(2304 pi^2)].
```

Because `x^2 ln(1/x)->0`, these terms decouple relative to EH in the infrared. After Newton matching, the imported-SM matter benchmark is at most `1.73e-38` on the R10-to-nuclear scale grid; a deliberately large `10^6` coefficient envelope remains below `3.05e-34`. This is a hierarchy smoke, not an arena likelihood or a bound on omitted H/ghost loops.

Since no parent-owned vacuum cancellation exists in the current corpus, freeze one declared renormalization condition:

```text
C0_R(mu0) = -M_R^2 Lambda_cal;
Lambda_cal = 1.09091e-52 m^-2.
```

It is fixed once and is not a prediction, a radiative-stability solution, or an arena-dependent fit. The local integrated-H GR branch remains viable as an infrared EFT; finite local R2/C2 coefficients, H/ghost form factors and actual source-to-observable projections remain open.

Checkpoint 4876 supplies the normalized one-loop layer of the integrated-H parent.

The counterterm-complete local action, scalar proper-time regulator, Diff Ward step, saddle equation, induced `C0/Mstar2/R2/C2/E4` coefficients and both extra-pole scales are explicit. For `h=1-6xi>0`,

```text
Lambda_bg_scalar_only = -3 Lambda_UV^2/(2h);
m0^2                  =  Lambda_UV^2/(Lh);
m2^2                  = -5h Lambda_UV^2/L;
epsilon0               = Lh(qmax/Lambda_UV)^2;
epsilon2               = L(qmax/Lambda_UV)^2/(5h).
```

Therefore the massless scalar-only parent cannot naturally own the flat saddle used by the local graviton expansion. SK diagonal normalization does not remove the vacuum stress. The branch now forks cleanly between a parent-derived signed-spectrum cancellation and an explicit renormalized vacuum condition.

A constructive free-field example exists: four real scalars plus one Dirac field, equal masses and `xi_s=0`, cancel the quartic, quadratic and logarithmic one-loop vacuum weights while retaining a positive Einstein coefficient. This proves compatibility, not MTS ownership.

Newton matching fixes

```text
N_s(1-6xi)Lambda_UV^2 = 12 pi/GN,
```

but does not predict `GN` until the three microscopic factors are independently fixed.

Checkpoint 4875 decides the primitive parent fork.

The strict fixed-background scalar-only route is rejected: treating the graviton as a massless composite of that ordinary scalar QFT triggers Weinberg-Witten. Its induced `RHat` term can only be an external response on that branch.

The selected viable parent integrates the principal density modulo diffeomorphisms:

```text
Z=int DH Dpsi_r Dpsi_a DX Dmatter / Vol(Diff)
    exp i[S0[g(H),...]+S_gf+S_gh].
```

`H` and Diff are primitive field/symmetry data; a bare EH stiffness may vanish at the UV boundary while microscopic loops induce it.

On a flat `Lambda_eff=0` saddle, the induced EH Hessian and propagator are

```text
Gamma2=Mstar^2 q^2(P2-2 P0s);
D=i(P2-P0s/2)/[Mstar^2(q^2+i0)]+gauge;
Res_spin2=1/Mstar^2>0.
```

The projector inversion passes exactly. Diff/BRST invariance gives

```text
Gamma2 P_L=0;
q_mu Gamma2^munu,rhosigma=0;
nabla_mu[2/sqrt(-g) delta Gamma/delta g_munu]=0.
```

Only helicities `+2,-2` are physical in the EH local sector. For conserved sources,

```text
A=i(T_mn T^mn-T^2/2)/(Mstar^2 q^2);
nonrelativistic numerator=rho^2/2>0;
GN=1/(8 pi Mstar^2).
```

The spin-2 pole and Ward identity activate the checkpoint-4874 soft theorem, so universal coupling and the common Maxwell/Hilbert/Poynting source follow conditionally on this parent.

Weinberg-Witten is not triggered because the integrated gauge theory has no gauge-invariant local Lorentz-covariant total gravitational stress tensor. This evasion relies on an exact Diff/BRST-preserving measure and regulator.

Checkpoint 4874 removes the additive reference metric from the lead primitive definition. The exact legacy split test is

```text
W_split Gamma=(delta/delta g_ref-delta/delta C)Gamma=0.
```

The new public metric is reconstructed directly from the densitized infrared principal symbol:

```text
H^munu=sqrt(-gHat) gHat^munu;
sqrt(-gHat)=sqrt(-det H);
gHat^munu=H^munu/sqrt(-det H).
```

This closes the kinematic reference-background problem. The Hadamard covariance and self-energy now feed `H`; they no longer define `gHat` by adding to a hidden metric.

Universal source coupling has a derivation route rather than an arbitrary axiom. For one physical massless spin-2 pole, soft gauge consistency gives

```text
sum eta_i kappa_i p_i=0;
sum eta_i p_i=0;
therefore kappa_i=kappa for every species.
```

The same route gives equality of inertial and gravitational mass and a common leading local metric cone, conditional on Lorentz invariance, soft factorization and emergent spin-2 gauge symmetry.

The decisive correction is that the 4873 heat-kernel `RHat` coefficient does not prove a graviton. Required next evidence is

```text
<hh>(q)=i Pi_spin2/[Mstar^2(q^2+i0)]+...;
positive residue; helicities +/-2; q_mu Gamma2^munu,rhosigma=0;
no unsuppressed scalar or ghost.
```

The fixed-background scalar parent also risks the Weinberg-Witten no-go for a composite massless spin-2 state. MTS must derive emergent diffeomorphism redundancy or prove another theorem premise fails.

Checkpoint 4873 supplies a valid covariant open variational owner for damping:

```text
S_SK=int sqrt(-gHat)[psi_a(E_psi+gamma u.d psi_r)+i N psi_a^2/2];
delta S_SK/delta psi_a at psi_a=0 = E_psi+gamma u.d psi_r.
```

It passes the SK normalization, reality and positive-noise identities. In an Ohmic thermal Markov limit, `Sigma_R=-i gamma omega` and `N=2 gamma T`; the bath-state Landau vector supplies time orientation.

The connected covariance is now defined by the renormalized Hadamard kernel:

```text
C^munu=ell_star^2[nabla_x^mu nabla_y^nu G_H(x,y)]_y=x^ren;
gHat^munu=g_ref^munu+C^munu.
```

The Gaussian heat-kernel anchor gives

```text
Mstar^2=N_s(1-6 xi)Lambda_UV^2/(96 pi^2);
GN_metric=12 pi/[N_s(1-6 xi)Lambda_UV^2].
```

This is non-circular if `Lambda_UV`, `N_s` and `xi` are derived without input `G`, but it is regulator dependent and brings an induced vacuum term of order `N_s Lambda_UV^4/(64 pi^2)`.

An exact positive spectral counterexample has equal normalization and covariance moments but response moments `1` and `11/4`. Therefore the covariance metric alone cannot determine the four unit-flow Kubo coefficients.

The lead primitive local branch is now the metric-only quotient:

```text
Gamma_IR=Gamma_IR[gHat,scalar state variables,Psi,A];
delta Gamma_IR/delta u=0;
c1=c2=c3=c4=0 because u is not an independent field.
```

This reaches exact GR outside the singular unit-flow chart. The nonzero unit-flow branch remains a tested state-flow extension, not discarded.

Checkpoint 4872 has returned from the correspondence ladder to the primitive corpus and produced three exact corrections plus one constructive existence result.

The printed damping term satisfies

```text
-gamma psi partial_t psi = -(gamma/2) partial_t(psi^2);
delta S_gamma/delta psi = 0.
```

It does not generate the advertised bulk damping equation. A doubled/open or nonlocal parent is required.

For a positive rank-one covariance, the printed covariant metric ansatz gives

```text
p_core = -q/(1-q) <= 0,
```

opposite to the retained healthy `p>0` branch. The minimal sign-corrected candidate is

```text
C^munu = ell_star^2[bar(d^mu psi d^nu psi)-bar(d^mu psi)bar(d^nu psi)];
gHat^munu = eta^munu + C^munu;
p=q>=0 on the rank-one timelike branch.
```

Its inverse, determinant and Lorentzian `0<=q<1` gate are exact. Every Lorentzian `gHat` supplies a coframe with local Lorentz redundancy, so the old affine-translation compensator is not needed for the metric branch.

A flow of the form `u=N dpsi` has `u wedge du=0` and cannot own the selected `c_omega>0` vector sector. An explicit two-realization positive-weight covariance has nonzero eigenflow curl, so a genuinely multimode smoothing state can. The physical flow is therefore a composite timelike Landau/eigenvector, not a normalized single gradient.

The four-operator unit-flow architecture and analytic decoupling law

```text
c_i = p cbar_i + O(p^2)
```

are now structurally derived under the corrected quotient assumptions. The exact `r`-dependent ratios, induced `Mstar` and universal matter quotient remain EFT matching data. The 4857-4871 calculations are retained as correspondence results rather than discarded.

The shared characteristic metric remains the lead private public metric. The genuine quartic compact-body response remains parent-derived through leading compactness:

```text
kappa4_weak = -C*r*(27*r^2+57*r+98)/(21*(1+r)) + O(C^2);
g_weak      = -2*C*r*(108*r^2+183*r+227)/(21*(1+r)) + O(C^2).
```

The checkpoint-4867 on-shell calculation continues to pass its weak-field regression:

```text
-2*a_v2 = alpha1 - 2*alpha2/3;
sigma_weak = (alpha1-2*alpha2/3)*Omega/M.
```

Checkpoint 4868 has now lifted the leading unit-flow subproblem onto the exact GR Tolman VII background at first order in `p`. The exact angularly reduced `L2/L4` functionals, two-field Euler system, regular-center/asymptotic BVP, and aether Noether surface charge through `v4` are executable.

The finite-background BVP is numerically regular in both collocation and finite-basis variational smoke solves. At `r=1/3,C=0.3`, Richardson extrapolation gives:

```text
f_bulk      = 0.27696368;
kappa4_bulk = -0.15842314;
A_inf       = -0.35073278;
B_inf       = -0.30918749.
```

Checkpoint 4869 corrects the interpretation of that comparison. The complete GR plus comoving-matter `l=1` shift action and exact aether source reduce to the gauge invariant

```text
Z = k-R*s'-s+2*R*(N'/N)*s;
E_k^(GR+m) = -8*pi*Z/(3*A*N);
Z = -3*A*N*S_k/(8*pi).
```

The asymptotic Yagi-Foster map and exterior aether equation then prove

```text
f_metric = f_bulk.
```

Therefore the nonzero `D2/M=0.3071` value introduced in checkpoint 4868 is withdrawn. It came from forcing a `C3`-truncated external value at `C=0.3`, not from the parent equations.

The external discrepancy is nevertheless real and is now localized. A symmetric `+C/-C` derivative solve gives

```text
a1_parent = 10/7                  = a1_Gupta;
a2_parent is consistent with     -2.6825951826;
4.94 < a3_parent < 5.00;
a3_Gupta = 10.8375176022.
```

Thus the branches agree through `C2` and disagree at `C3`. Checkpoint 4871 has now replaced the equal quarantine: the action-derived branch is selected for internal correspondence work, while the printed external coefficient is retained as an unresolved literature-source discrepancy and not used as a closure condition.

Checkpoint 4870 closes the quartic mass accounting inside the selected correspondence action. The stationary total-mass envelope theorem gives

```text
f_parent      = -I2/(8*pi*C);
kappa4_parent =  I4/(16*pi*C);
g_parent      = 3*f_parent + 8*kappa4_parent.
```

The `q3` correction contributes only the first variation `delta I2[q1;q3]`, which vanishes by the `q1` Euler equation, center regularity and the zero residual boundary condition after the exact `gamma*v` asymptotic factor is removed. At `r=1/3,C=0.3`,

```text
f_parent      =  0.27696368;
kappa4_parent = -0.15842314;
g_parent      = -0.43649409.
```

The 26-row finite-C scan gives the conservative sampled envelopes `|kappa4|<0.159` and `|g|<0.47`. The conserved-charge split is also fixed: `Q4=B4`, `D4=-E_aether4`, so `D4` is derived bookkeeping rather than a free completion.

Checkpoint 4871 derives the previously missing third-order profile from the parent action:

```text
H2[q1] q3 = -E4[q1].
```

The independently derived asymptotic current gives `kappa4_surface(A1,B1,A3,B3)`. Five finite-C rows reproduce the on-shell action value with maximum absolute difference `1.83e-8`; at `r=1/3,C=0.3`, the values are `-0.15842312565` and `-0.15842313376`. The extrapolated `delta I2[q1;q3]` residual remains below `5.6e-8`.

The refined small-compactness extraction gives

```text
a2_parent = -2.6825953696;
a3_parent =  4.9573884008;
4.95 < a3_parent < 4.97.
```

Both arXiv v1 and v2 carry the same syntactically incomplete final `C3` term. Its ambiguity vanishes at `r=1/3`, and omission or sign reversal of the surviving blocks does not recover the parent interval. The parent branch is therefore the internal MTS correspondence branch; no correction to the external paper is claimed.

The 4864 compact-body results remain

```text
p_J0337 < 8.54609e-6;
p_J1738,dipole < 2.23676e-6;
p_uniform = 1.3928203230e-6.
```

The 2025 direct radiation-reaction calculation reports disagreement with older far-zone flux formulas, so the dipole result remains a smoke gate pending reconciliation.

The current `MTS-Galaxy-Lab-` snapshot is now explicitly counted as an empirical pillar: 175 LTGs, 16 ETGs, locked-candidate metrics, holdout/null/jackknife and QA machinery. Its exact response cache is not yet a compact parent-derived transport law.

## Current branch status

- The integrated-H parent is now counterterm-complete at one loop and has an explicit local saddle equation.
- A public-metric proper-time scalar determinant preserves the Diff Ward identity by trace cyclicity; the complete H measure remains to be closed.
- The massless scalar-only naturally flat saddle is rejected by an exact cutoff-scale curvature result.
- SK normalization is proved not to cancel the vacuum stress entering the metric response equation.
- A signed scalar-Dirac spectrum can cancel one-loop vacuum moments while retaining positive induced gravity; actual MTS spectrum ownership remains open.
- The scalar-anchor R2 scalar pole and problematic C2 spin-2 scale are derived, with exact epsilon0/epsilon2 IR gates.
- Measured GN fixes one microscopic combination rather than supplying a prediction of its factors.
- The strict fixed-background scalar composite-graviton branch is rejected.
- The integrated diffeomorphic principal-density parent is selected privately as the only viable local-GR route.
- `H` and Diff are primitive; their Einstein-Hilbert stiffness and higher operators are induced.
- The standard positive massless spin-2 pole and linear/nonlinear Ward identities are derived on this parent.
- Universal soft coupling, Newtonian equivalence and common Maxwell/Hilbert/Poynting sourcing are activated conditionally.
- The remaining local work is normalized parent action, saddle, covariant regulator, induced Lambda/R2 coefficients and empirical hierarchy—not another graviton-existence audit.
- The public metric and volume are reconstructed from `H^munu` without a reference metric.
- The additive `g_ref+C` representation is retained only as a split-Ward regression, not the primitive definition.
- Universal gravitational coupling is derived algebraically from the soft theorem conditional on a physical MTS massless spin-2 gauge pole.
- The induced Einstein-Hilbert coefficient remains a response anchor, not yet a collective graviton propagator.
- The collective metric measure, spin-2 projector, diffeomorphism Ward identity and Weinberg-Witten evasion are the single decisive local-GR gate.
- If that gate closes, GR/PPN, Newtonian equivalence and Maxwell/Hilbert/Poynting coupling follow at leading two derivatives.
- A covariant doubled/open action now generates damping; a closed bath spectrum and state remain to derive.
- The Hadamard point-split kernel replaces informal smoothing and makes covariance a calculable state object.
- A one-loop induced Einstein-Hilbert/Newton normalization is derived as a regulator-dependent microscopic anchor.
- Covariance-to-flow-coefficient underdetermination is proved by an exact positive spectral counterexample.
- The metric-only induced-GR quotient is selected as the lead primitive local branch; no zero-kinetic aether field is retained.
- The nonzero public unit-flow action remains a tested extension and preferred-frame leakage envelope.
- Background independence, universal matter/Maxwell principal symbols, microscopic cutoff origin and vacuum subtraction are the remaining local-root gates.
- The printed one-field damping action remains rejected; its role is superseded by the valid doubled open response action.
- The legacy covariant covariance metric is rejected for the retained rank-one sign; the inverse connected-covariance public metric is the lead primitive candidate.
- Local Lorentz coframe redundancy is derived from metric factorization; local translations are no longer required on the torsion-free metric route.
- A single-gradient flow is ruled out for the spin-1 branch; a multimode composite eigenflow route exists explicitly.
- The complete unit-flow operator basis and `c_i=O(p)` decoupling are derived conditionally; exact coefficient ratios remain Kubo matching data.
- Universal Poynting/source chain rules remain valid downstream of same-public-metric descent, whose microscopic premise is still open.
- `gHat` remains the lead public metric; the same-`g`, `beta_u=0` branch remains fallback only.
- Absolute `p` now has BBN anchors and an `r`-independent weak-PPN-safe sufficient corridor.
- Complete local `K2/K3/K4`, scalar/vector projection and operator norms are derived.
- Metric-flow mixing and mixed graviton-flow scales are explicitly bounded.
- Weak-field strong coupling no longer appears to be the limiting threat.
- The Gupta compact-body sensitivity series remains recorded as external provenance, but its printed cubic coefficient is no longer used as an exact parent-action calibration.
- `sigma'=O(p)` and corrected binary `hat alpha1/hat alpha2` transfer are derived.
- The genuine quartic coefficient `kappa4=(g-3f)/8` is parent-derived and independently v3-surface-crosschecked at finite sampled `C` inside the selected correspondence action.
- The finite-C fixed-background `L2/L4` flow functional and two-field BVP are derived and numerically regular.
- The exact aether surface charge through `v4` is derived and passes its aligned static regression.
- The full first-response metric Ward completion is derived and exactly equals the on-shell bulk boundary functional.
- The prior forced nonzero `D2` completion is withdrawn; the stationary mass identity fixes `D4=-E_aether4`, so it is a derived charge partition rather than an independent response.
- The parent and Gupta sensitivity expansions agree through `C2`; the refined parent `C3=4.95738840` is selected internally and the disjoint printed value is demoted to an external-source discrepancy.
- The finite-C `v3,l=1` profile and exact asymptotic current are derived; their quartic response agrees with the bulk action to `1.83e-8`.
- Across the sampled public corridor, `|kappa4|<0.159` and `|g|<0.47`, comfortably inside inherited binary sufficient windows.
- Direct binary preferred-frame data leave substantial completion headroom around the derived leading value.
- Solitary spin precession, tabulated-EoS repetition, endpoint gauge restoration and primitive MTS ownership remain open.
- Galaxy work is a substantial empirical pillar; its parent-action derivation remains open.

Checkpoint 4880 now proves the exact strong-field vacuum continuation of the finite local classical sector:

```text
R_mn=Lambda_cal g_mn
=> H_mn^(R2)=0, B_mn=0
=> E_mn^(EH+R2+C2)=0.
```

Thus Schwarzschild, Kerr and every matched four-dimensional Einstein vacuum background remain exact on the selected EH-connected analytic metric branch. Strong compactness is a calculation-method handoff, not by itself a theory failure. Nonlocal quantum terms remain bounded residuals rather than exact zeros.

The declared one-percent gate is `u^2<0.01`, so Earth, Sun and a white dwarf stay in the 1PN certificate. A benchmark neutron star requires a full matter-interior/EOS/contact solve. A ten-solar-mass horizon uses the exact Einstein vacuum branch. The first nonredundant vacuum operator is controlled by `epsilon6=|c6|(qK ellStar)^4`.

Marker: `PPC4161_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880`.

Checkpoint 4881 now closes the compact perfect-fluid algebra:

```text
F = a_R(rho-3p)^2 + 4a_C rho(rho/3+p);
rho_eff = rho-F/Mbar^4;
p_eff = p-[(rho+p)(F_rho+cs2 F_p)-F]/Mbar^4.
```

The interior is standard GR TOV with the effective EOS; no extra fourth-order stellar operator remains. The exterior field redefinition vanishes. Causal local coefficient envelopes are exact, but the neutron-star mean-density numbers are benchmarks rather than profile bounds. The direct mass bound depends on `int rho^2/int rho`.

The scalar determinant now owns the exact Ricci-flat `a6` tensor and massive `exp(-m^2/LambdaUV^2)/m^2` spectral moment. Including the checkpoint-4876 finite-mass Einstein-anchor factor, under `h>=0.1`, both local hierarchy ratios below `0.1` and `delta_EH<=0.01`, its full raw operator-norm envelope is `4.18204e-5`. A massless scalar remains nonlocal. Bare dimension-six matching and the complete signed mass/spin spectrum are not set to zero.

Marker: `PPC4161_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881`.

Checkpoint 4882 now differentiates the coupled TOV plus relativistic Love system:

```text
Z_A' = J_Y Z_A + s_A;
R_A = -(Z_A)_n/n'_surface;
M_A = (Z_A)_m;
(y_R)_A = (Z_A)_y + y'_surface R_A;
O_A|M = O_A - O_c M_A/M_c.
```

The turning condition `kappa_turn=|d ln M/d ln nc|^-1` prevents fixed-mass overreach at maximum mass. Sixteen nonlinear checks validate both contact directions at fixed central density and fixed mass with maximum relative error `1.15423e-6`.

For the causal analytic `Gamma=2`, `K=100L_sun^2` benchmark, fixed-mass tidal envelopes remain below `5.034e-17` through `0.99Mmax`. The engine is valid, but the EOS has `Mmax=1.637M_sun` and fails the two-solar-mass requirement, so no microphysical strong-matter promotion is made.

Marker: `PPC4161_TOV_LOVE_RESPONSE_JACOBIAN_4882`.

## Next theorem/test

- Acquire tabulated or source-backed piecewise-polytropic EOS families that support two-solar-mass stars.
- Add monotone thermodynamically consistent interpolation and any surface-density jump rule.
- Rerun the validated fixed-mass mass-radius-Love response across EOS families and compare contact envelopes with EOS spread.
- Retain the turning-point condition and reject ill-conditioned sequence rows.

## Next target

`4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md`

## Checkpoint 4883 handoff

Checkpoint 4883 replaces the under-massive analytic polytrope with source-backed BSK24, SLY4 and DD2 tables locked to LALSuite commit `a43ed75d9785b825d33b63072e1812f83efae36a`.

All three EOS families support `2M_sun` and reproduce CompOSE `Mmax` and `R1.4` anchors to sub-percent accuracy. The general cold-barotrope contact law is now derived:

```text
q = p^(2/5)
D_A = (rho+p) f_A,q/rho_q - f_A
rho_eff = rho-lambda_R f_R-lambda_C f_C
p_eff = p-lambda_R D_R-lambda_C D_C.
```

Nine response rows cover `1.4M_sun`, `2M_sun` and `0.99Mmax` for each EOS. All `48` nonlinear derivative comparisons pass with maximum relative error `6.007e-3`. Surface-threshold variation is below `1.22e-12` fractionally in radius.

At canonical mass, realistic EOS spread exceeds the inherited MTS contact caps by approximately `1e17`. This supports strong-matter GR correspondence for the selected strict-EFT metric branch under its caps. It does not derive or measure `a_R,a_C` and does not promote the full MTS parent.

Marker: `PPC4161_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883`.

## Next theorem/test

- Attempt to derive `a_R,a_C` from the adopted MTS parent spectrum and matching conditions.
- If parent ownership does not close, use the validated multi-EOS Jacobian to construct explicit EOS-marginalized observational bounds on both coefficients.
- Preserve independent signs, turning-point conditioning, source hashes and the no-cancellation envelope.
- Do not mistake derivative-control caps for measured Wilson coefficients.

## Next target

`4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md`

## Checkpoint 4884 handoff

Checkpoint 4884 corrects the ownership diagnosis. The universal matter-loop
pieces are already derived:

```text
a_R,loop = L S_h2/(1152 pi^2)
a_C,loop = L W_C/(1920 pi^2).
```

For the maximal explicit `complex psi + Gamma + U(1)` reading,
`W1=3h-4`, so positive induced Einstein stiffness requires `h>4/3`
(`xi<-1/18`). At `W1=1`, the candidate gives `h=5/3`, `xi=-1/9`,
`a_R/a_C=25/27` and the same cutoff ratio `4pi sqrt(6)` as the five-minimal-
scalar completion. This avoids inventing two additional modes, but `Gamma`
and the common nonminimal weight are not yet primitive-owned.

The sampled compact-star stability law is
`m_s>=8.02675e-12 sqrt(h-1) eV`. Every tested parent loop ray shifts the
multi-EOS radius/tidal observables by more than `65` orders below source-
backed widths. Source-backed GW170817/NICER interval inversions are full-rank
but over `17` orders weaker than the strict-EFT control scale, and broad
vertices exceed linear contact control. Twelve nonlinear fixed-mass solves
validate the one-percent corridor only.

Finite renormalized, integrated-`H`/ghost and threshold terms remain the
total-coefficient gate. No observational posterior bound or full parent claim
is made.

Marker: `PPC4161_CONTACT_COEFFICIENT_OWNERSHIP_4884`.

## Next theorem/test

- Derive a second-order UV operator and functional measure for `Gamma`.
- Derive its nonminimal weight from the closed-bath/Hadamard parent, or demote
  the three-boson route.
- Decide explicitly whether `a_R,fin(LambdaUV)=a_C,fin(LambdaUV)=0` is a
  minimal Wilsonian theory boundary or whether independent finite terms stay.
- Preserve the negative-`xi` stability and nonlinear stellar scope gates.

## Next target

`4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md`

## Checkpoint 4885 handoff

Checkpoint 4885 finds the canonical curvature-memory scalar `M` already
present in the cosmology corpus and derives its quadratic operator:

```text
D_M = -Box + m0^2 + 3 a Mbar^2 - 2 b T + xi_M R.
```

The particle-sector first-order `Gamma` variable is not another UV species.
It follows as the controlled overdamped limit of `M` plus the 4873 bath under

```text
Gamma = g_M M;
J_K = (gamma_M/g_M) S[K];
mu = Omega_M^2/gamma_M.
```

The bath Schur complement proves a sign obstruction:

```text
xi_eff = (xi_M + integral w_X xi_X)/(1 + integral w_X),
w_X = g_X^2/Omega_X^4 >= 0.
```

A passive bath with nonnegative microscopic curvature weights cannot derive
the negative `xi` needed by the 4884 pure-induced branch. The `bTM^2` term
provides only an IR trace-curvature relation after an Einstein branch exists.

At the prior `xi=-1/9` anchor, the printed massless `M=0` branch has
`m_eff^2=-R/9` in positive compact-star curvature and a sampled tachyon
length of `30.109 km`. The density-supported minimum is locally stable, but
its scalar charge and exterior force are unsolved.

The pure-induced three-boson route is demoted. The retained branch is a
once-calibrated renormalized-EH `complex psi + M + U(1)` EFT with

```text
W1 = -1;
a_R/a_C = 1/3;
M0^2 = Mbar_Pl^2 + LambdaUV^2/(96 pi^2).
```

This does not predict Newton's constant. It puts `G_N` in the same one-input
status as GR, with no arena retuning, while preserving the derived universal
loop residuals.

Marker: `PPC4161_GAMMA_MEMORY_UV_OPERATOR_4885`.

## Next theorem/test

- Derive and solve the static spherical `M(r)` equation on BSK24, SLY4 and
  DD2 matter traces.
- Extract asymptotic scalar charge, fifth-force strength and compact-body
  sensitivity rather than inferring screening from the local Hessian.
- Evolve the same `a,b,m0,xi_M` branch on FLRW and reject any local/cosmology
  parameter switching.
- If no shared viable region exists, retain the renormalized-EH local branch
  and demote active memory to an explicit phenomenological closure.

## Next target

`4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md`

## Checkpoint 4886 handoff

Checkpoint 4886 gives the direct trace interaction its minimal covariant
universal matter owner:

```text
phi=M/Mbar_Pl;
beta=b Mbar_Pl^2;
A(phi)=exp(beta phi^2).
```

The full static spherical zero-mode equation was solved on the nine existing
BSK24, SLY4 and DD2 TOV backgrounds with regular centers and exact
Schwarzschild exterior matching. At `beta=-1/18`, charge ratios span
`0.3233--0.7493`. First global zero modes occur only at
`beta=-1.0870--1.4311`, at least `19.566` times farther into negative
coupling. The 4885 pointwise tachyon warning therefore does not become a
global neutron-star instability at the anchor.

Weak sources are not screened. The solar charge ratio is `1.000000566`; the
ambient Compton range is `2.461e4 Mpc`.

The cosmological minimum and PPN coupling obey

```text
phi_inf^2=B0/abs(beta);
alpha_DEF^2=8 abs(beta) B0;
gamma-1=-2 alpha_DEF^2/(1+alpha_DEF^2).
```

Using the conservative absolute two-sigma Cassini envelope gives
`B0<7.53775e-5`. The printed large-scale growth correction is approximately
`-B0`, so a one-percent target exceeds the envelope by `132.08`.

Minimum tracking back to recombination makes the trace completion
nonperturbative; remaining near the small-field branch invalidates the
minimum-branch growth formula. Significant direct-trace active-memory
cosmology is therefore rejected under this owner. Canonical `M`, the
overdamped `Gamma` map and the renormalized-EH local branch remain retained.

Marker: `PPC4161_MEMORY_SCALAR_COMPATIBILITY_4886`.

## Next theorem/test

- Construct a variationally closed derivative or curvature memory source.
- Prove its stationary weak local PPN projection vanishes or is boundary
  suppressed.
- Prove the same source remains nonzero on FLRW without an arena switch.
- Preserve common-metric matter conservation and avoid a preferred frame.
- If this cannot be done, demote active-M cosmology while retaining canonical
  M as the UV memory determinant.

## Next target

`4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md`

## Checkpoint 4887 handoff

Checkpoint 4887 constructs a replacement for the rejected direct trace
cosmology:

```text
S_theta=-Mbar_Pl^2 sigma_theta int sqrt(-g) u.grad phi.
```

Here `u` is the composite Landau flow of the already required closed bath.
Integration by parts gives `sigma_theta phi div(u)`. For a normalized
stationary Killing flow, `div(u)=0` exactly, so the source is a boundary and
the stationary metric-only PPN values remain `gamma=beta=1`. On FLRW,
`div(u)=3H`, and the same operator gives

```text
phi_ddot+(3H+gamma_M)phi_dot+kappa phi^3=3 sigma_theta H+noise.
```

A covariant bath clock supplies a closed flow owner and the stability gate

```text
sigma_theta^2 < (rho_X+p_X)/Mbar_Pl^2.
```

The benchmark `sigma_theta/H0=0.3` requires
`Omega_X(1+w_X)>0.03`; a baryon-enthalpy-scale state passes. The scalar
principal cone is unchanged.

Three fixed-background integrations from zero memory at `N=-7`, with
`gamma_M/H0=1`, reach present memory fractions `10^-4`, `10^-3` and `10^-2`.
All remain below `0.01406`; the percent branch half-activates at `z=0.99`.
The activation follows from the covariant `3 sigma_theta H` drive and does not
use a redshift switch.

This is a constructed conditional mechanism. `sigma_theta` is not yet a
microscopic prediction, and the scalar-only response does not own the full
bath-memory stress or a cosmological likelihood.

Marker: `PPC4161_EXPANSION_MEMORY_SOURCE_4887`.

## Next theorem/test

- Derive the bath compression-memory Kubo coefficient `sigma_theta` from the
  explicit closed `X_Omega` spectrum or freeze it as a Wilson coefficient.
- Evolve bath memory and Friedmann equations with total stress conservation.
- Derive linear perturbations and growth from the same action.
- Run the existing cosmology comparator without local parameter retuning.
- Test dynamical binary and preferred-frame leakage.

## Next target

`4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md`

## Checkpoint 4888 handoff

Checkpoint 4888 derives the exact compression-memory matching equation

```text
Mbar_Pl^2 sigma_theta=K_phi_theta^R(0,0)
                     =sum_a c_a d_a/Omega_a^2.
```

The cross kernel necessarily comes with diagonal `phi^2` and `theta^2`
susceptibilities obeying Cauchy--Schwarz. `gamma_M` does not numerically fix
`sigma_theta`; the cross spectrum remains independent parent data.

The exact interaction stress and clock current are now varied. On FLRW,
`rho_sigma=0` but `p_sigma=-Mbar_Pl^2 sigma_theta phi_dot`. Damping energy is
deposited into the bath, closing total conservation.

The three predeclared branches pass fully backreacted Friedmann,
Raychaudhuri, memory and bath evolution. The percent row has
`kappa/H0^2=985.3921`, maximum memory fraction `0.01398`, and requires a
`1.815%` initial bath-normalization compensation.

Real Pantheon+/DESI DR2 fixed-row scores were executed. The percent row has
`Delta chi2=-0.627` and `-3.264` relative to fitted LambdaCDM on the
no-SH0ES and SH0ES-column branches. It is worse in chi2 than fitted
`wCDM/CPL`, and conservative parameter counting does not support an evidence
claim.

The key correction is

```text
(c^2-1)(c^2-c_X^2)-R_mix c_X^2=0.
```

The benchmark is gradient-stable but the upper low-energy mode exceeds the
public cone for finite positive `c_X^2`. The bare `phi` block remains metric;
the coupled cone does not. The full nonlocal retarded kernel must determine
the UV front before causal or local-GR promotion.

Marker: `PPC4161_BATH_KUBO_BACKREACTED_COSMOLOGY_4888`.

## Next theorem/test

- Construct one positive frequency-dependent spectral matrix matching
  `gamma_M`, `sigma_theta`, and both diagonal moments.
- Calculate its poles, branch cuts and high-frequency front velocity.
- Derive the full metric--clock--memory scalar perturbation equations.
- Run growth/CMB only if the kernel remains stable and causal.
- Calculate dynamical-binary sourcing and radiation leakage.

## Next target

`4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md`

## Checkpoint 4889 handoff

The generic finite-sound `P(X)` bath clock is demoted as the selected local
parent. The replacement is the explicit fixed-norm action

```text
S_Uphi=int sqrt(-g)[-varrho((grad U)^2+1)/2
        +Mbar_Pl^2 sigma_theta grad(phi).grad(U)].
```

It produces the same `sigma_theta theta` memory equation and the same three
backreacted backgrounds. The clock multiplier stays positive; the minimum
effective inertia factors are `0.3849`, `0.3641`, and `0.2181`.

The exact symbolic local determinant is

```text
omega^2(omega^2-k^2).
```

The memory wave is luminal and the clock is a constrained dust zero mode.
There is no upper superluminal clock-memory wave on this parent.

The derived subhorizon two-component growth kernel predicts up to `11.1%`
suppression in `f` today. Real BAO-plus and full-shape-only SDSS/eBOSS scores
were run separately. Every fixed MTS ray modestly improves matched LambdaCDM
chi-square; the `10^-3` ray gives `-0.980` and `-1.040`. This is not evidence
because `sigma8_today` is profiled and CMB amplitude is not imposed.

On the stationary background-subtracted branch, extra stress vanishes and
the field equation reduces to EH plus universal matter and Maxwell Hilbert
stress. Newton and PPN have their GR values up to `H0^2L^2`; Poynting flux
gravitates through `T_EM`. The largest sampled finite-frequency metric
envelope is `2.853e-23`.

The remaining decisive work is the full Einstein--Boltzmann plus SK-noise
kernel, a microscopic identity for `U,varrho`, and the zero-density/caustic
test.

Marker: `PPC4161_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889`.

## Next theorem/test

- Derive all finite-k Einstein, memory, clock, matter and radiation equations.
- Include `delta Q_SK`, fluctuation noise and conservation identities.
- Identify the clock with existing parent bath variables or reject it as an
  extra dust component.
- Test the zero-density local patch and nonlinear caustics.
- Impose CMB amplitude without retuning the local parent.

## Next target

`4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md`

## Checkpoint 4890 handoff

The 4889 fixed-norm clock now has a controlled microscopic identity. For two
degenerate Cartesian modes in the existing closed bath,

```text
X1+iX2=A exp(i m_c U);
varrho=m_c^2 A^2.
```

Their canonical action reduces exactly to an amplitude kinetic term plus
`-varrho[(grad U)^2+1]/2`. The leading WKB limit is the selected clock; the
radial correction is `(grad U)^2+1=Box A/(m_c^2 A)`. The map is singular at
`A=0`, where the Cartesian fields rather than the dust chart must be used.

The three backgrounds were reshot from `N=-14` so every sampled mode starts
superhorizon. The maximum late overlap shift from the 4888 histories is
`4.88e-7`.

The finite-k Einstein--memory--clock--matter--perfect-radiation equations are
implemented with both constraints and `delta Q_SK`. Three wavenumbers on
each of the three memory rays remain finite. Maximum relative Hamiltonian
and momentum residuals are `2.215e-16` and `1.721e-3`; the code-level
linearity residual is zero.

The FDT shape and retarded noise response are explicit. Four normalized
noise impulses preserve the Hamiltonian constraint and give a finite
`G_Phi_xi`. A stochastic power and CMB likelihood remain blocked because
the bath state, carrier preparation, photon--baryon/recombination equations,
neutrino hierarchy and primordial cross-covariance are not yet fixed.

The 4889 stationary EH/Newton/PPN/Maxwell correspondence is retained.

Marker: `PPC4161_COMPOSITE_CLOCK_FINITE_K_FDT_4890`.

## Next theorem/test

- Wire photons, baryons and neutrinos to the unchanged finite-k parent.
- Restore `Psi` distinct from `Phi` through anisotropic stress.
- Derive or bound the bath density matrix and coherent carrier occupation.
- Propagate the resulting FDT covariance into metric transfer functions.
- Run a CMB likelihood only if the permission gate closes.
- Treat the `A=0` Cartesian patch and nonlinear caustics separately.

## Next target

`4891-Y5-R2FR-composite-clock-neutrino-photon-baryon-hierarchy-and-FDT-state-normalization-or-CMB-source-demotion-gate.md`

## Checkpoint 4891 handoff

The standard photon--baryon--neutrino hierarchy is no longer a placeholder.
CAMB `1.6.6` supplies the collision, recombination, polarization, massless-
neutrino and compiled massive-neutrino operators. The 4890 parent supplies
explicit density, momentum and pressure source slots and has zero linear
anisotropic stress.

The early matter density is lower than today's value by the amount of later
bath heating. Using this early normalization keeps the parent residual
background positive. All three rays run through matched CAMB geometry and
standard-species spectra. The worst shifts through `ell=400` are

```text
abs(Delta thetaStar/thetaStar) = 6.833e-4;
max abs(Delta TT/TT)           = 4.423e-3;
max abs(Delta EE/EE)           = 5.836e-3.
```

For the central ray, the parent-to-GR Weyl ratio is silent to `2.67e-7` at
`z>=30` and reaches at most `1.921%` late. Reweighting CAMB's linear Weyl
power gives `0.21--1.24%` lensing suppression over `L=10--200`.

The FDT state now has an empirical covariance ceiling. With one percent of
primordial metric power reserved for noise,

```text
Var I_k < 0.0282438;
I_rms   < 0.168059;
Theta_k DeltaN < 0.0141219.
```

These are normalized Fourier-cell bounds, not a physical temperature. A
spectral measure and microscopic state still have to realize them.

The current CAMB PPF branch is a background geometry/standard-hierarchy
comparator, not the parent perturbation owner. The parent Weyl response is an
operator split and the lensing result is linear Limber, so no official CMB
support claim is made.

Marker: `PPC4161_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891`.

## Next theorem/test

- Calculate the non-Limber late ISW source from the parent Weyl response.
- Calculate the full linear lensing line of sight and coverage error.
- Attempt a coherent/vacuum/KMS bath state with a derived spectral measure.
- Reject any state violating the normalized covariance bound.
- Run an official fixed-row likelihood only if those gates close.
- Preserve the 4889 stationary local correspondence unchanged.

## Next target

`4892-Y5-R2FR-parent-late-ISW-lensing-line-of-sight-and-FDT-state-realization-or-CMB-source-demotion-gate.md`

## Checkpoint 4906 handoff

The actual MTS-Galaxy-Lab artifacts have now been imported read-only. The
canonical support fails fixed-kernel source homogeneity exactly, and the active
v18.21 response is a 175-curve exact support cache rather than a native
source operator. Eighty-seven curves match the canonical support exactly;
eighty-eight contain noncanonical radial redistribution.

The direct checkpoint-4905 no-slip import is therefore rejected for the
current artifacts. This does not reject a universal nonlinear action. It
requires the galaxy scale and response to arise from an environmental
background generated by the parent.

The spherical-equivalent response profile is

```text
rho_X = a Gamma0 [1-exp(-x^q)+q x^q exp(-x^q)]
        /(4 pi G L x^2),  x=r/L,
```

with slopes `-1.23` and `-2` for canonical `q=0.77`.

The v19 conformal candidate instead predicts the leading relation

```text
mu_dyn=1+epsilon; mu_lens=1; eta=(1-epsilon)/(1+epsilon),
```

and reaches no-slip only at zero response. Its current disk implementation is
rejected: sink-target mean gain `-1.173 km/s`, zero negative target profiles,
failed boundary direction, and protected maximum regression `88.621 km/s`.

The exact future two-response inverse is

```text
A2=1/mu_lens;
A0=1/(4 mu_lens-3 mu_dyn).
```

No lensing likelihood was run because no claim-safe kernel exists. The active
residual remains zero.

Marker: `PPC4161_GALAXY_KERNEL_NO_SLIP_ARBITRATION_4906`.

## Next target

`4907-Y5-R2FR-parent-derived-environmental-bi-response-action-or-galaxy-residual-freeze.md`

## Checkpoint 4907 handoff

The final current-parent galaxy action-entry routes have been calculated.

An analytic metric residual connected to calibrated GR has only positive
powers of source normalization and cannot reproduce the canonical nonzero
`lambda^0` support. The only explicit memory-scalar re-entry is constrained by
Cassini to `alpha_DEF^2<3.3501123e-5`. Even doubling this as a force envelope
leaves the weakest p16 galaxy requirement larger by factor `5805.98`.

Neither negative-beta branch screens the Sun:

```text
beta=-1/18 -> charge ratio 1.000000566;
beta=-0.2  -> charge ratio 1.000002038.
```

The shortest empirical response length is `0.6988 kpc`, giving one-AU
attenuation `0.9999999931`, so Yukawa hiding is unavailable. Pure conformal
lensing remains `mu_lens=1`.

The derivative bath source obeys `theta=0` for a stationary axisymmetric
circular disk. Four-dimensional Maxwell conformal invariance and `T_EM=0`
leave the Poynting vector as ordinary Einstein Hilbert stress, not a
trace-memory source.

The galaxy empirical pillar is retained, but its residual is frozen outside
the active action. `Gamma_MTS,res=0`; no new field or coefficient was added.

Marker: `PPC4161_ENVIRONMENTAL_BIRESPONSE_GALAXY_FREEZE_4907`.

## Next target

`4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md`

## Checkpoint 4909 handoff

The printed motion scalar now has a positive finite lattice measure and an
executed nonperturbative pilot. The constant cutoff fit gives
`c_m=1.02129+/-0.02408`, while alternative intercepts and a two-sigma model
union keep the value private and unpromoted. One finite-volume comparison is
null at `0.203 sigma`; the replicated cutoff differs by `2.003 sigma`.

The exact connected response is

```text
W123=<S123>-Cov(S1,S23)-Cov(S2,S13)-Cov(S3,S12)
     +<deltaS1 deltaS2 deltaS3>.
```

It passes a distinct-source Gaussian test at `0.662 sigma`. Densitized metric
seagulls are exact, and the selected TT triplet has nonzero Weyl template
`0.1138547018` with ratios `1,64,729,4096`.

Marker: `PPC4161_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909`.

## Next target

`4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md`

## Checkpoint 4910 handoff

The exact free TTT calculation validates the numerical response but rejects
the single-triplet coefficient map. Six `q6/Weyl` fits have the wrong sign and
miss the known scalar coefficient by factors `134.9--164.4`.

The flat-torus theorem shows why: a real periodic Euclidean Ricci-flat mode is
constant and has zero Weyl curvature. A nonzero real TT source is off shell,
so the full derivative/Ricci/Riemann `a6` basis contributes at `q6`.

The selected replacement is a full-rank geometric template matrix with
correlated inverse and a separately proved Ricci-flat map. No interacting
long run is authorized before this recovers the free coefficient.

Marker: `PPC4161_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910`.

## Next target

`4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md`

## Current checkpoint 4933 handoff

Last checkpoint:
`4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md`.

The intervening 4911-4932 chain acquired, normalized and source-locked the
natural-essential Weyl-cubic and photon-gravity flows. Checkpoint 4933 now
executes them in one shared `20 x 20` projection rather than comparing two
independent endpoint tables.

The partial common zero is

```text
(g,g_plus,g_minus,g_CFF,h_C3)
  =(0.130560452615,
    0.347004250660,
    3.244436423674,
    0.003729942576,
    4.27303833729e-6),

||beta||_infinity=1.44518e-13.
```

Its partial beta spectrum has one relevant direction and signed gap
`0.242075164606`. The conservative coordinate-basis derivative gate is
`||DeltaJ||_2<0.00160840422841`.

The minimal Maxwell `a6` term and principal `CFF^3` chain are derived. Two
source blocks remain open inside the minimal five-coordinate truncation:

1. linear and quadratic `CFF`-curvature `a6` terms in `beta_h`;
2. direct `C3` Hessian terms in the seven photon-background rows.

Their complete first-order source-to-fixed-point response is stored in
`source-intake/functional_rg/4933/combined_c3_photon_stability_results.json`.
The tightest isolated one-percent target is `4.67446e-8` in the portal `a6`
row. This is a diagnostic threshold, not a coefficient bound.

The current point is not the full MTS point. Motion, full visible matter and
the enlarged GR-connected trajectory remain open after the two minimal-flow
terms close.

Marker: `PPC4161_C3_CFF_F4_COMBINED_NATURAL_FLOW_4933`.

## Next target

`4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-gate.md`

## Current checkpoint 4934 handoff

Last checkpoint:
`4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-gate.md`.

Both exact cross-source blocks left open by 4933 have been derived. The
linear `g_CFF` contribution to the C3 row is an exact zero, while

```text
Delta RHS_C3|g_CFF^2
 =g_CFF^2(5gamma_a-3gamma_DF+20)/(80pi^2).
```

The direct C3 metric Hessian vanishes in six photon rows by curvature-irrep
selection. The unique surviving `CFF` coefficient is derived including the
retained metric/mixed Hessian and RG-kernel blocks.

The source-complete point of the declared minimal selected-row system is

```text
(g,g_plus,g_minus,g_CFF,h_C3)
  =(0.1305603732179711,
    0.3470041701608080,
    3.244460421436017,
    0.0037300003823489045,
    3.947320506281829e-6),

||beta||_infinity=1.43268557658e-14.
```

Its beta matrix has one negative and four positive real parts, with signed
gap `0.242082333593261`. No exact source block remains absent from the
declared minimal `C3-CFF-F4` system.

Five duplicate lower-curvature photon rows have residual infinity norm
`2.33688716e-4`. They are retained as a truncation diagnostic because they
omit the C3 vacuum Hessian; they are not additional canonical equations.

This is not the full MTS fixed point. The completed point still needs a
GR-connected infrared trajectory, basis-enlargement stability, the MTS
motion/time/source Hessian and visible-matter completion before any local-GR,
Newton or Maxwell promotion.

Marker: `PPC4161_SOURCE_COMPLETE_C3_CFF_F4_FLOW_4934`.

## Next target

`4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md`

Integrate the completed point along its single relevant direction, test the
regular Gaussian/GR infrared branch and all five essential coordinates, then
append the parent motion-sector Hessian rather than another missing-source
ledger.

## Current checkpoint 4935 handoff

Last checkpoint:
`4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md`.

The completed minimal `C3-CFF-F4` point now has an explicitly integrated
Gaussian/GR infrared separatrix. Five negative-direction seeds from `1e-4` to
`1e-6` all reach `g=1e-10`; the positive direction runs away.

The minimal infrared endpoint is

```text
W_plus            =0.00791633789162,
W_minus(c_l=16pi) =0.0947256563061,
W_C               =0.000550951486901,
A_C3              =-2.17009107830e-5.
```

Gaussian powers and the exact photon logarithm are recovered. The raw deep-IR
projection condition is large from canonical scaling, but the maximum
equilibrated condition is `210.5102` and the maximum backward relative solve
residual is `1.3233e-16`.

The actual motion action has also been varied. For

```text
V=(3/4)g_psi|psi|^(4/3),
```

the only classical vacuum is `psi=0` and `V''->+infinity`. The motion field
must enter through its renormalized 1PI mass gap, not a guessed bare mass.

Its invariant dimensionless coordinates obey, before mixing,

```text
beta_gtilde=-(8/3)gtilde_psi,
beta_w=-2w_psi.
```

Thus the motion sector introduces a second canonically relevant physical
scale unless the coupled flow fixes it or a parent identity relates it to
Newton's scale. The unique six-derivative quadratic motion portal is
`O4=C^2(nabla psi)^2`.

This is not yet the full MTS trajectory. The next calculation must project
`beta_w`, `eta_psi` and `beta_uO4`, solve the enlarged point and index, and
then re-integrate the surviving GR branch.

Marker: `PPC4161_GR_CONNECTED_MINIMAL_TRAJECTORY_MOTION_ENTRY_4935`.

## Next target

`4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md`

## Current checkpoint 4936 handoff

Last checkpoint:
`4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md`.

The exact optimized LPA-prime flow of

```text
u=(3/4)gtilde|varphi|^(4/3)
```

generates the lower `|varphi|^(2/3)` interaction. The one-coupling
fractional family is therefore not closed. `eta_psi=4` makes the retained
interaction marginal but leaves the lower trace term nonzero; `eta_psi=6`
silences the optimized scalar trace but leaves canonical running. There is no
nonzero scalar-only fixed point inside this one-coupling truncation.

The official `arXiv:2204.08564` scalar-gravity notebook has now been acquired,
hash locked and independently executed. Its A and B fixed points, exponents
and `gamma_phi` are reproduced. The exact source beta function gives

```text
beta_Dphi4(g,0)=(406/5)g^2+O(g^3),
```

so gravity additively sourcing scalar interactions is proved. Those
coefficients belong to the external shift-symmetric source theory and are not
MTS coefficients.

The normalized motion-Weyl projector is

```text
P_O4=(1/2)partial_C2 partial_p2 Gamma_psipsi^(2).
```

The isolated free scalar trace has exact zero additive O4 source. The
fractional diagonal trace is nonzero but its bare-vacuum projection is
singular. The mixed six-derivative coefficient remains open.

Route arbitration selects the full functional potential `u_k(varphi)`. The
one-coupling route is rejected, the exact mixed-cancellation route is
unsatisfied, the current-parent `psi=chi^3` shortcut is inequivalent and
phenomenological closure is demoted.

The sibling galaxy logistic equations now have an exact conditional
interface: a positive ratio `r proportional to R^q` mapped by
`n=r/(1+r)` obeys `dn/dlnR=q n(1-n)`. With a derived `k proportional to 1/R`,
`q` and `s` can be critical exponents of parent Hessian amplitude ratios.
Their physical identity and numerical MTS values remain open.

This is not yet the enlarged MTS fixed function or trajectory, and it does not
promote local GR, Newton or Maxwell.

Marker: `PPC4161_MOTION_FUNCTIONAL_COMPLETION_AND_PREDICTIVITY_GATE_4936`.

## Next target

`4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md`

Derive the constant-background gravity-motion block Hessian of the unchanged
parent, calculate its functional potential and O4 traces, solve the regular
fixed-functional boundary-value/eigenoperator problem, count the total
relevant directions and connect every viable branch to the 4935 Gaussian/GR
separatrix.

## Current checkpoint 4937 handoff

Last checkpoint:
`4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md`.

Direct off-shell variation gives the physical trace-motion Hessian

```text
H=[[-K_sigma/3,U'/2],
   [U'/2,p^2+U'']],

K_sigma=(F/2)p^2-U/4.
```

The optimized canonical block has

```text
a=1-u/(4w),
b=1+u'',
mu^2=3(u')^2/(4w),

T_pair=(a+r_sigma b)/[32pi^2(a b+mu^2)].
```

For the fractional parent, off-diagonal mixing starts at `q^2` and cannot
cancel the scalar `3q/(32pi^2gtilde)` source. The exact-cancellation route is
closed inside the unchanged minimal block.

At the 4934/4935 Newton coordinate, both source-normalization variants of the
MES-compatible low root have a relevant motion mass,
`theta_mass=1.8467--1.8490`. Both action-sign maps of
`lambda=3g/(16pi)` give `theta_mass=1.8501--1.8588`. The scalar-irrelevant
high root is at `v about 0.964`, near the TT pole and not the source MES
branch. No generic nonconstant row in the declared seventy-two-shot scan
reaches `varphi=3`; this is not promoted to a universal no-go theorem.

The exact next relation is

```text
I_M=gtilde_psi g^(4/3)=g_psi G_N^(4/3),

beta_I/I=beta_gtilde_psi/gtilde_psi+(4/3)beta_g/g,

m_gap sqrt(G_N)=c_m I_M^(3/8).
```

Canonical Gaussian scaling preserves `I_M` but fixes neither `I_M` nor
`c_m`. The unchanged-parent one-scale branch is therefore false at this
checkpoint, while a precise scale-lock derivation route remains.

Marker: `PPC4161_GRAVITY_MOTION_FUNCTIONAL_HESSIAN_ONE_SCALE_GATE_4937`.

## Next target

`4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md`

Calculate the coupled beta of `I_M`, determine whether the enlarged UV
critical surface fixes `I_M` and `c_m`, and propagate every surviving value
down the 4935 GR separatrix. If no parent-owned fixed value exists, retain the
motion gap as an explicit second essential scale rather than a closure.

## Current checkpoint 4938 handoff

Last checkpoint:
`4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md`.

Every current scale owner has been tested. The fixed golden-ratio old-coupling
formula is not invariant under the exact old-field coordinate orbit. The
constant-gamma term is a boundary, covariance coefficients transform
inversely, closed stress residues cancel the normalization, and the minimal
UV surface retains a second relevant mass direction.

The physical scale coordinate is

```text
J_gap=w_psi g=m_gap^2G_N=c_m^2 I_M^(3/4),

beta_J/J=beta_w/w+beta_g/g.
```

The augmented stability matrix is block triangular,

```text
B_aug=[[B_g,c],[0,-theta_mass]],
```

and has two relevant eigenvalues for all three source/sign variants. The
known Newton threshold derivative is

```text
c_g=-g_*^2/(6pi)=-0.000904318973124.
```

It rotates the motion eigenvector but cannot remove its eigenvalue.

The independent UV coordinate

```text
R_UV=delta w/epsilon^(theta_mass/theta_g)
```

was propagated down all five 4935 GR seeds. The endpoint Jacobians are

```text
K_plus=0.262094420818,

K_minus=0.261707706805,
```

with less than `4.94e-5` seed drift. This is a stable transfer of an arbitrary
second datum, not a value selection.

The unchanged parent is therefore explicitly two-scale: `G_N` and one shared
`J_gap`. Do not fit `g_psi`, `c_m` and `J_gap` independently and do not retune
the gap by arena.

Marker: `PPC4161_MOTION_NEWTON_SCALE_IDENTITY_OR_TWO_SCALE_GATE_4938`.

## Next target

`4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md`

Derive the curved O4 flow, include complete mass-threshold backreaction,
integrate the universal `J_gap` family to the GR endpoint, and calculate local
Newton/Maxwell residuals with the same scale value everywhere.

## Current checkpoint 4939 handoff

Last checkpoint:
`4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md`.

Checkpoint 4939 repairs the 4938 spectator approximation by including the
massless neutral motion scalar before solving the ultraviolet point:

```text
beta_x=beta_x^4934
 +(g^2/[6pi(1+w)],0,0,0,0).
```

The shifted point is

```text
x_*=(0.130890578648,
     0.371493332004,
     3.450502470197,
     0.004095125661,
     3.916215903e-6),
```

with residual `4.68e-14`. The gravity block retains one relevant
direction. Both regular-mass sign maps have two enlarged relevant directions,
with `theta_mass=1.84968` or `1.85847`.

The finite family includes three gravity seeds, seven positive
`R_UV` values and both sign maps. All 42 positive-mass runs plus
three massless controls reach `g=1e-10`. The small-amplitude
transfer is about `J_gap=0.262 R_UV`, while at `R_UV=1`
finite feedback gives `J_gap=0.2006` or `0.1885`.

The O4 source is now sharply split:

```text
beta_utilde_O4
 =(4+eta_psi)utilde_O4
  +S_O4^(gravity-mixed).
```

The quadratic scalar trace and neutral photon trace give exact zero additive
O4 sources. The remaining off-shell curved gravity-motion mixed trace is not
calculated. Therefore the finite `u_O4=0` family is a known-source
diagnostic, not yet the full parent trajectory.

Marker:
`PPC4161_TWO_SCALE_O4_KNOWN_SOURCE_BACKREACTED_GR_FAMILY_GATE_4939`.

## Next target

`4940-Y5-R2FR-curved-gravity-motion-O4-additive-source-and-full-invariant-submanifold-gate.md`

Calculate the off-shell metric-scalar and mixed Hessian trace projected at
`C^2p^2`. Derive the remaining O4 source or prove its zero, append
`utilde_O4` to the fixed point and finite family if necessary, and
keep physical PPN/Maxwell claims blocked until that enlarged trajectory is
projected into the local source problem.

## Current checkpoint 4940 handoff

Last checkpoint:
`4940-Y5-R2FR-metric-kernel-O4-nonzero-source-self-backreacted-fixed-point-and-direct-trace-cancellation-gate.md`.

The parent essential metric kernel contains

```text
Psi^g_mn contains gamma_C2 C^2 g_mn
```

on the Ricci-flat projection. Its contraction with the canonical motion
kinetic action is `gamma_C2 O4/2` in four dimensions. The known source beta is
therefore

```text
beta_uO4=4u_O4-gamma_C2/2+S_O4,direct.
```

The scalar O4 Hessian feedback into the C2 and RC2 rows has also been derived
and inserted before every source solve. With the explicit direct RHS trace
left open, the six-coordinate point is

```text
(g,g_plus,g_minus,g_CFF,h_C3,u_O4)_*
 =(0.130878136125,
   0.371466079910,
   3.453208488035,
   0.00409533354414,
   3.91680160559e-6,
  -0.00180507540865).
```

Its residual is `1.43e-13`; it has one relevant direction. Both
mass-augmented blocks have two relevant directions, while the O4 eigenvalue
is `+3.99603`. All 45 trajectories reach `g=1e-10`, and the Gaussian Wilson
ratio approaches `W_O4=-3.31918`.

The known-source zero surface is now rejected. Exact restoration of
`u_O4=0` requires

```text
S_O4,direct,*=-0.00721281432165
```

in the identical source scheme. This is the one remaining O4 source
calculation, not a free fitting parameter.

Marker:
`PPC4161_METRIC_KERNEL_O4_SOURCE_SELF_BACKREACTED_GATE_4940`.

## Next target

`4941-Y5-R2FR-direct-metric-scalar-C2p2-trace-and-O4-cancellation-or-shift-gate.md`

Calculate the explicit right-hand-side metric-scalar and mixed Hessian trace
at `C^2p^2`, test the signed cancellation value above, and insert the result
into the same fixed point and finite family. Keep full MTS and local
GR/Newton/Maxwell claims false until this direct trace and the later local
observable projection close.

## Current checkpoint 4941 handoff

Last checkpoint:
`4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-minimal-O4-parent-completion-gate.md`.

The explicit right-hand-side metric-scalar O4 trace is now calculated in the
unchanged parent's natural Type-II/Litim source scheme. Generic symbolic
four-dimensional Weyl contraction proves the pure `hh` source channels zero,
while

```text
B^dagger K B=(1/2)X(-nabla^2)
```

makes the no-residual mixed density proportional to `Q0[zW]=0`. The only
nonzero Type-I principal channel is

```text
S_direct(beta_endo,D)
 =(1-beta_endo)^2 g(D+3)/(8piD^4).
```

Since the parent owns `beta_endo=1`,

```text
S_O4,direct=0.
```

This does not cancel the nonzero metric-kernel source. The completed minimal
O4 point is therefore the unchanged 4940 point,

```text
(g,g_plus,g_minus,g_CFF,h_C3,u_O4)_*
 =(0.130878136125,
   0.371466079910,
   3.453208488035,
   0.00409533354414,
   3.91680160559e-6,
  -0.00180507540865),
```

with one relevant six-coordinate direction, two after adding the universal
motion gap, and 45 completed IR trajectories.

The lower four-derivative quotient is

```text
c_ess=c+8pi g(ctilde+d),
beta_c,ess|0=16g^2.
```

Its retained `X^2` representative has no additive two-scalar Hessian at
`psi=0`. This completes the declared minimal O4 parent, not all five scalar
six-derivative beta functions or full visible matter.

Marker:
`PPC4161_NATURAL_TYPEII_DIRECT_O4_ZERO_MINIMAL_PARENT_4941`.

## Next target

`4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md`

Derive the homogeneous `psi=0` local branch and scalar characteristic from the
completed O4 endpoint action. Combine the same endpoint's C3, CFF, scalar
threshold and O4 coefficients into one weak-field PPN/Newton/Maxwell residual
vector. Keep one universal `J_gap`, and keep full local promotion false unless
the source equations and bounds close without arena retuning.
## Current checkpoint 4942 handoff

Last checkpoint:
`4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md`.

The completed local motion equation is

```text
nabla_m[(Z_psi+2u_O4 C^2)nabla^m psi]-m_psi^2 psi=0.
```

Thus `psi=0` is exact for every `J_gap`; its canonical and O4 stresses
vanish. The principal symbol is `Z_eff g^mn`, so the scalar cone is the
metric cone when `Z_eff>0`. The worst correction on five local benchmarks
is `|Delta Z/Z|=3.12e-155`.

All 45 O4-completed trajectories were re-integrated. The same-family
envelopes are

```text
W_C=0.000600014865..0.000603365146,
A_C3=-2.20044196e-5..-2.19231661e-5,
W_O4=-3.31918185..-3.31843918.
```

They give `|a_+|=7.55e-143 m^4` and
`|c_gamma^parent|=7.92e-72 m^2`. Standard constant PPN `gamma` and
`beta` are unchanged on `psi=F=0`, but the distinct pure-C3 `r^-7`
metric residual and CFF polarization split are calculated and retained.

Marker:
`PPC4161_COMPLETED_O4_LOCAL_BRANCH_C3_CFF_RESIDUAL_4942`.

## Next target

`4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md`

Vary the unchanged matter action with respect to `psi`, derive the interior
equation and junction conditions, and prove or reject continuation of the
zero branch through ordinary sources. If a source survives, calculate its
fifth-force profile with the fixed 4942 coefficients. Do not retune
`J_gap`, and keep full local promotion false until this source theorem and
visible threshold matching close.

## Current checkpoint 4943 handoff

Last checkpoint:
`4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md`.

The selected integrated-`H` parent has

```text
Args(S_SM)={H,Phi_SM,theta_SM},
delta S_SM/delta psi=0,
Gamma_eff[H,psi,Phi_SM]=Gamma_eff[H,-psi,Phi_SM].
```

Therefore ordinary matter has no one-scalar tadpole. The inherited
gravity-mediated stress contact has been expanded exactly into `A_time`,
`B_space` and `m_eff^2`. Under the conservative strict-EFT caps, all eight
Earth/Sun/white-dwarf/neutron-star density rows remain positive; the worst
kinetic correction is `9.06e-18`.

The homogeneous bulk equation has junctions

```text
[psi]_Sigma=0,
[n_mu K_eff^munu nabla_nu psi]_Sigma=0.
```

Hence `psi=0` continues through ordinary matter with

```text
Q_psi=0,
a_psi/a_N=0
```

at classical one-scalar order. This closes the source and junction gate on
the selected reflection-even parent. It does not derive the visible matter
functor from `psi`, test a reflection-breaking state, or erase C3/CFF and
higher-order residuals.

Marker:
`PPC4161_MATTER_SOURCE_INTERIOR_JUNCTION_NO_FIFTH_FORCE_4943`.

## Next target

`4944-Y5-R2FR-complete-electroweak-spin1-and-hadronic-CFF-matching-or-total-photon-residual-bound.md`

Complete the physical CFF photon coefficient by matching every charged
visible threshold in one operator convention, then project the total bounded
coefficient onto the fixed 4942 local systems. Keep the 4943 matter-source
theorem and universal `J_gap` unchanged. Do not call a parent-only or
free-lepton-only coefficient the physical Maxwell residual.

## Current checkpoint 4944 handoff

Last checkpoint:
`4944-Y5-R2FR-complete-electroweak-spin1-and-hadronic-CFF-matching-or-total-photon-residual-bound.md`.

The visible `CFF` hierarchy now has source-executed numbers:

```text
c_leptons=-9.6217944e-31 m^2,
c_pi,anchor=+6.44866e-36 m^2,
c_K,anchor =+5.15430e-37 m^2,
|c_W|<=3.50065e-38 m^2.
```

The `W` row is a complete-dimension-six magnitude envelope, not an exact
signed match. Current quarks were not inserted below confinement and the
hadronic local remainder was not set to zero.

The calculable control interval is

```text
c_control
 in [-9.6217251328e-31,-9.6217244326e-31] m^2.
```

The secondary two-sided PSR recast gives the conditional complete-total and
unmatched bounds

```text
|c_IR|<=6.0025e6 m^2,
|c_unmatched|<=6.0025e6 m^2+|c_control|.
```

Projected onto the five fixed local systems, the maximum conditional split is
`0.08617496` at the neutron-star benchmark. This is a real bound rather than a
missing-input placeholder, but it remains secondary and model conditional, so
local Maxwell promotion stays false.

Marker: `PPC4161_VISIBLE_CFF_THRESHOLD_TOTAL_BOUND_4944`.

## Next target

`4945-Y5-R2FR-primary-two-sided-CFF-likelihood-or-QCD-TJJ-dispersion-bound-and-local-Maxwell-certificate.md`

First try to reconstruct a primary two-sign PSR polarization likelihood with
competing operators. If the data are unavailable, derive a dispersive or
chiral bound on the hadronic `TJJ` coefficient from measured electromagnetic
and gravitational form factors. Do not weaken the 4944 conditionality label or
retune the universal coefficient between systems.

## Current checkpoint 4945 handoff

Last checkpoint:
`4945-Y5-R2FR-primary-two-sided-CFF-likelihood-or-QCD-TJJ-dispersion-bound-and-local-Maxwell-certificate.md`.

The primary mode formula proves

```text
T_+(-c_gamma)=T_-(c_gamma),
Delta T_split=24|c_gamma|A,
```

so the physical split covers both signs. The numeric legacy pulsar bound does
not survive source execution: its printed `6.0e6 m^2` value implies a geometry
factor `0.106`, below the allowed far-observer minimum one. The measured
PSR B1534+12 conjunction has `b=6.11e8 m`, not the companion's `10 km`
radius. Under the historical one-microsecond allowance the central and
conservative bounds are

```text
|c_gamma|_central<=1.18743e15 m^2,
|c_gamma|_2sigma <=1.35442e15 m^2.
```

The corrected transfer leaves conditional CFF residuals `2.79e-7` at Earth
and `7.13e-8` at the Sun, but the neutron-star and horizon rows are outside
linear control. The source packages contain no polarization-resolved TOA
likelihood, and plasma, intrinsic mode phase and jitter remain nuisance terms.
The 4942-4943 GR/Newton/no-fifth-force branch is unchanged; only the previous
photon bound is superseded.

Marker:
`PPC4161_PRIMARY_CFF_SIGN_GEOMETRY_LOCAL_CERTIFICATE_4945`.

## Next target

`4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md`

Derive or rigorously bound the confined-QCD `TJJ` contribution in the same
Ricci-flat CFF convention. Combine it with the parent, lepton, scalar and
charged-vector packet. Promote a predictive weak-local Maxwell action only if
the physical coefficient closes without the rejected pulsar number, a zero
hadronic remainder or an arena-dependent cancellation.

## Current checkpoint 4946 handoff

Last checkpoint:
`4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md`.

The finite local shift

```text
delta W=delta c integral sqrt(-g) CFF
```

leaves flat HVP, one-current electromagnetic form factors and one-stress
gravitational form factors unchanged but shifts electromagnetic `TJJ`. This
proves that no precision increase in those lower data can derive or bound the
QCD `CFF` coefficient. Its dispersive form necessarily retains `c_QCD^r` as a
subtraction constant unless an additional UV theorem is supplied.

The identifying first-principles estimator is now defined:

```text
c_QCD^r
 =lim_(epsilon->0) epsilon^-4
  P_C[Gamma_TJJ(epsilon momenta)-Gamma_Maxwell],
```

with gradient-flow EMT, two conserved currents, contact, Ward, Bose,
continuum, volume, flow-time and physical-mass gates. No lattice number is
invented.

The non-QCD coefficient is already

```text
c_nonQCD
 in [-9.621794773635e-31,
     -9.621794073504e-31] m^2,

c_IR=c_nonQCD+c_QCD^r.
```

The local Maxwell action, current, field equation, stress and combined
conservation identity are derived. Flat spacetime is exact Maxwell for every
`c_IR`. The coefficient may be computed from TJJ or calibrated once from a
robust curved-photon experiment and then transferred through the five fixed
slopes without retuning.

Marker:
`PPC4161_QCD_TJJ_NO_GO_LATTICE_MAXWELL_CONTRACT_4946`.

## Next target

`4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md`

Combine the metric pole residue `G_N`, photon normalization, motion gap and
curvature-photon coefficient into one parent calibration ledger. Derive the
Poisson, geodesic and Lorentz-force source residues from the unchanged action,
count genuinely independent empirical inputs and reject any local arena that
needs an extra source normalization.

## Current checkpoint 4947 handoff

Last checkpoint:
`4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md`.

The unchanged parent now derives

```text
M_R^2 G_mn=T_mn
 -> Box hbar_mn=-16piG_N T_mn
 -> nabla2Phi=4piG_N rho
 -> Phi=-G_NM/r
 -> a=-gradPhi,
```

with one source residue `G_N=(8piM_R^2)^-1` shared by Einstein gravity,
exchange, Newtonian force, orbits and leading lensing. Neutral matter follows
the same metric geodesic and the selected `psi=0` branch retains zero
classical one-scalar fifth force.

The unchanged EM action also derives Maxwell-CFF propagation, Lorentz force,
EM stress, Poynting flux and total conservation with one `alpha_EM` convention
and one universal `c_IR`. No arena receives a separate force or stress
normalization.

The displayed truncation contains seven nonduplicate scalar coordinates:

```text
G_N, Lambda_cal, alpha_EM, J_gap, c_IR, a_R^r, a_C^r.
```

Only `G_N` and `alpha_EM` normalize leading local source laws. `J_gap`,
`c_IR`, `a_R^r` and `a_C^r` remain unselected or incompletely matched. The
count is not promoted to the untruncated EFT and `theta_SM` remains an
inherited parameter set.

Five fixed systems reuse identical `G_N`, `alpha_EM`, `J_gap` and `c_IR`
tokens. Earth, Sun and the white dwarf pass the weak-Newton gate. The neutron-
star and horizon rows retain the GR source chain but are not called
Newtonian.

Marker: `PPC4161_LOCAL_CALIBRATION_COUNT_SOURCE_RESIDUE_4947`.

## Next target

`4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md`

Read the galaxy work without modifying its repository. Map the completed
parent motion Hessian to the proposed phase occupation and boundary equations,
including stress and boundary conditions. Derive the flow with one universal
`J_gap` or reject that exact map; do not import `dn/dlnR=q n(1-n)` or
`db/dlnR=-s b(1-b)` as closures.

## Current checkpoint 4948 handoff

Last checkpoint:
`4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md`.

For the natural shell `k=xi/R`, positive relevant and irrelevant parent
Hessian weights generate exact projective flows

```text
dn/dlnR=theta n(1-n),
db/dlnR=-lambda b(1-b).
```

The completed parent gives `theta_mass=1.8496934455--1.8584838539` and
`lambda_O4=3.9960254523`. The locked public galaxy support exponent `0.77` is
not proved to be the phase exponent and is not matched if that identification
is imposed. The canonical exponential support is also not algebraically the
logistic occupation.

One universal gap still permits source-dependent transition radii through
`R_n=xi sqrt(G_N/J_gap) C_n^(-1/theta)` and the corresponding `R_b` law. The
current one-point branch cannot calculate `C_n` or `C_b`: visible matter has
no linear `psi` source, `psi=0` is exact under the declared boundaries and
`O4` stress vanishes there. The direct one-point galaxy map is rejected.

The selected next route is a reflection-even state `G=<psi psi>` governed by
a covariant 2PI Dyson equation. Its metric variation can supply a conserved
occupation stress while preserving zero one-point scalar charge, and its
vacuum-subtracted local limit must return the 4947 GR/Newton/Maxwell branch.
This is a defined calculation, not yet a solved disk model.

Marker: `PPC4161_PARENT_HESSIAN_GALAXY_PHASE_2PI_4948`.

## Next target

`4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md`

Construct the renormalized axisymmetric 2PI truncation from the completed
parent. Derive the state-dependent source amplitudes and metric stress with
one `J_gap`, prove positivity, Ward conservation and local-GR recovery, or
reject the composite route before fitting SPARC.

## Current checkpoint 4949 handoff

Last checkpoint:
`4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md`.

The physical CTP statistical and spectral equations and the exact static
axisymmetric parent operator are now derived. At fixed mean metric, the
completed displayed scalar action is quadratic:

```text
Gamma_2^scalar=Sigma_F^scalar=Sigma_rho^scalar=0.
```

Because its quadratic form is positive and time independent, a stationary
baryonic metric has zero Bogoliubov pair production. It changes mode shapes
but does not select a populated state. Any nonzero occupation is initial
density-matrix data unless a new parent-owned source kernel or environmental
bifurcation is derived.

A nonvacuum state nevertheless has a valid variational metric stress and Ward
identity. Subtracting `F_vac[g]` cleanly separates it from vacuum Wilson
matching; `Delta F_state=0` returns the 4947 GR/Newton/Maxwell branch.

The read-only 175-LTG sample gives 173 positive outer residual rows. The
one-correlation-cell scaling requires `log10 N_R=99.08--105.29`, median
`102.51`. This is an amplitude diagnostic, not a fit. The current minimal
scalar 2PI galaxy route is rejected because no equation selects that state.

Marker: `PPC4161_CTP_2PI_STATIC_SOURCE_NO_GO_4949`.

## Next target

`4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md`

Derive whether the completed parent RG generates `R psi^2`, `T psi^2` and a
positive stabilizer or an equivalent CTP influence kernel. Calculate the
universal galaxy-versus-local lowest-eigenvalue window and reject the static
pair route if it cannot activate galaxies while preserving every local-GR
arena without retuning.

## Current checkpoint 4950 handoff

Last checkpoint:
`4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md`.

The pair-source hunt found a larger parent closure requirement rather than a
missing scalar number. A regular interacting curved motion sector must solve

```text
V_k(psi), F_k(psi)R, Z_k(psi), c_ess X^2
```

together. The primary one-loop comparator gives

```text
beta_lambda=3lambda^2/(4pi)^2,
beta_xi=lambda(xi-1/6)/(4pi)^2,
```

so `xi=0` is not generally invariant. The conformal value is not adopted as
an MTS prediction. Direct `Tpsi^2` is excluded by fixed-metric factorization;
on the leading GR trace branch only `B=-(xi_R-xi_T)` survives.

The exact spherical zero-mode law

```text
x cot x=-mL,
Bcrit=[(mL)^2+x^2]/(6C)
```

was applied to 175 public galaxies at four Compton ranges. Every one of the
700 rows has no activation interval below the Sun, white-dwarf or neutron-
star stability ceiling. The potential-depth proxy remains at least 73.46
times above the white-dwarf ceiling. The minimal universal local pair route
is rejected; no full disk theorem is claimed.

Checkpoint 4949 is refined accordingly: `Gamma2_scalar=0` is exact only in
its displayed quadratic truncation. The generated `X2` interaction supplies
occupied-state scattering once its parent-scheme coefficient is solved, but
still has zero quadratic source at `psi=0`.

Marker: `PPC4161_PAIR_OPERATOR_RG_BIFURCATION_4950`.

## Next target

`4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md`

Build one parent-scheme `V-F-Z-X2` flow, append it to the current
gravity-motion stability block, count its relevant directions and test
whether a GR-connected trajectory predicts finite `xi`, `lambda` and
`c_ess` while keeping the local spectrum positive. Do not return to galaxy
fitting until this parent block closes.

## Current checkpoint 4951 handoff

Last checkpoint:
`4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md`.

The coupled functional source hunt now has an exact result. At the
Gaussian-matter pair surface, constant-shift symmetry is preserved by the
declared parent regulator, so

```text
beta_m2|0=beta_lambda4|0=beta_xi|0=beta_z2|0=0.
```

Gravity-generated `c_ess X2` survives but is shift invariant. Expanding the
full `V-F-Z-X2` action about `psi=0` gives

```text
Gamma_psi_psi=-Z0 box+m2-xi R;
```

the quartic, field-dependent wave function and `X2` terms are all fourth
order and cannot move the first environmental instability.

The MTS parent low branch has `theta_mass=1.8466610` and
`theta_quartic=-0.1533390`. External physical-gauge fixed points were solved
exactly but kept behind a scheme firewall; their `xi` values and indices are
not inserted into MTS.

The universal stable infrared trajectory obeys

```text
delta_xi(k2)/delta_xi(k1)=[lambda4(k2)/lambda4(k1)]^(1/3),
delta_xi=xi-1/6.
```

It suppresses the pair coefficient toward galaxy scales. The easiest
spherical galaxy instead requires growth by `467.019` relative to a white
dwarf and `3.81399e5` relative to a neutron star. The current static
`V-F-Z-X2` galaxy bridge is rejected as a derived route. No complete disk
no-go is claimed, and the 4947 local GR/Newton/Maxwell branch is retained.

Marker: `PPC4161_VFZX2_SHIFT_SOURCE_STATIC_PAIR_DECISION_4951`.

## Next target

`4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md`

Derive the parent `h psi psi` vertex and the visible-matter stress noise
kernel, propagate it through the graviton Hadamard/spectral function into the
scalar CTP source, and test spectral support above the pair threshold. Keep
the stress Ward identity and the 4947 zero-state local limit exact. Do not
insert an occupation or galaxy profile as initial data.

## Current checkpoint 4952 handoff

Last checkpoint:
`4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md`.

The selected non-equilibrium source has now been constructed. The unchanged
metric coupling gives a conserved `h psi psi` vertex and

```text
N_h^ind=(kappa^2/4)D_R N_m D_A,
Im S_IF^psi=(kappa^4/32)T_psi^-D_R N_m D_A T_psi^-.
```

The real-pair kernel is order `kappa^4/16` and uses the unsymmetrized
positive-energy matter emission spectrum. Symmetrized vacuum noise is not an
occupation source. Exact ground states, stationary stress and DC Poynting
flow have zero positive-energy emission.

For two motion modes each resolving radius `R`,

```text
n>=2(c/v)sqrt[1+(R/lambda_c)^2].
```

All 175 public massless galaxy rows fail at smooth `n<=4`; their minimum,
median and maximum thresholds are `1801`, `6014` and `33685`. The sourced
white-dwarf comparator requires `2093`, while the conservative 716-Hz,
16-km neutron-star row requires `9`. Frequency support is therefore not a
galaxy-only selector. The smooth late-time direct CTP route is rejected, but
formation transients and a derived `X2` redistribution cascade remain open.
The 4947 stationary local GR/Newton/Maxwell branch is retained.

Marker: `PPC4161_VISIBLE_MATTER_GRAVITON_CTP_PAIR_SOURCE_4952`.

## Next target

`4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md`

Derive a bounded galaxy-formation stress-emission spectrum, insert it into the
4952 pair kernel, and derive the `X2` collision integral and redistribution
time. Require one universal parent coefficient to build the macroscopic
galaxy occupation within a formation time while respecting white-dwarf,
neutron-star and local energy-injection bounds. Do not supply the initial
occupation, cascade or environmental switch by hand.

## Current checkpoint 4953 handoff

Last checkpoint:
`4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md`.

The proposed leading `X2` cascade has now been calculated rather than left as
an open word. For `L_int=c_ess X^2`,

```text
M_22=(c_ess/2)(s^2+t^2+u^2),
sigma_22=7c_ess^2 s^3/(320pi),
a0=5c_ess s^2/(96pi).
```

The covariant on-shell collision integral obeys

```text
int dPi C_22=0,
int dPi p^nu C_22=0.
```

It can redistribute momentum but cannot multiply the injected population for
any `c_ess`. Combining this exact invariant with the 4952 source gives

```text
F_N<=min(1,E_R/E_inj),
F_N,redshift<=min(1,1090.92 E_R/E_inj).
```

All `692` positive-target high-frequency public rows fail even under the full
recombination redshift grant. Direct profile-frequency injection survives
only as an unsolved high-harmonic formation-stress amplitude. A natural
`1/Mbar_Pl^4` comparator is negligible, and the maximal compact challenge
quantifies the source-efficiency suppression that any universal continuation
must derive. The 4947 local GR/Newton/Maxwell branch remains intact.

Marker: `PPC4161_FORMATION_X2_CASCADE_LOCAL_INJECTION_4953`.

## Next target

`4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md`

Derive the finite-time/off-shell `1<->3` memory kernel and first on-shell
`2<->4` number-changing contribution from the parent `X2` vertex, contract
them with the 4952 source, and enforce the 4953 galaxy/local efficiency
ceilings. Do not revive the rejected `2<->2` cascade or insert a source switch.

## Current checkpoint 4954 handoff

Last checkpoint:
`4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md`.

The remaining controlled number-changing routes from 4953 have now been
calculated. The finite-time 2PI reduction contains four channels, but a sharp
source switch is UV-sensitive. A smooth Gaussian preparation instead gives

```text
P_13=6.06609438657e-6(c_ess E^4)^2/(E tau)^4.
```

At the 4953 perturbative-unitarity ceiling, all `692` positive-target
high-frequency rows fail. The first generic on-shell multiplier was also
constructed. Its complete leading tree amplitude is

```text
sigma_24=c_ess^4E^14(C0+C1r_3+C2r_3^2),
r_3=d_3/c_ess^2,
```

because the independent `d_3 X^3` contact enters at the same order as the ten
two-`X2` exchange diagrams. A deliberately generous controlled six-point
envelope also fails all `692` rows. The controlled high-frequency composite
route is rejected. A parent-derived broad nonquasiparticle state and direct
profile-frequency formation amplitude remain open. The 4947 stationary local
GR/Newton/Maxwell branch is retained.

Marker: `PPC4161_FINITE_TIME_X2_X3_NUMBER_CHANGE_4954`.

## Next target

`4955-Y5-R2FR-six-derivative-shift-sector-X3-parent-flow-and-number-changing-fixed-ratio-or-strong-2PI-route-rejection.md`

Derive the complete parent six-derivative shift-symmetric scalar flow,
including `d_3`, and determine whether a GR-connected trajectory fixes or
bounds `r_3=d_3/c_ess^2`. Only a parent-predicted route to broad spectral
support warrants the expensive full unequal-time 2PI solve. Do not fit `d_3`,
insert `Gamma/E`, or revive either closed finite-time route.

## Current checkpoint 4955 handoff

Last checkpoint:
`4955-Y5-R2FR-six-derivative-shift-sector-X3-parent-flow-and-number-changing-fixed-ratio-or-strong-2PI-route-rejection.md`.

The missing minimal-gravity `X3` source has now been derived exactly. The
ten-component harmonic-gauge projector reproduces the published
`beta_c|0=20g^2` and gives

```text
beta_e|0=-(208pi/5)g^3.
```

Hence `X3=0` is not invariant. The same checkpoint derives the exact flat
functional hierarchy

```text
partial beta_a_n/partial a_(n+1)=-(n+1)(n+2)/(48pi^2),
```

so every finite polynomial `P(X)` truncation is nonclosed. The leading
Gaussian-GR solution forces `e=(104pi/5)g^3+C_e g^4`, but `r3` is scale
dependent. Its contact comparator fails all `692` positive high-frequency
rows. This does not reject an uncomputed functional trajectory or direct
profile-frequency source. The 4947 local GR/Newton/Maxwell branch is retained.

Marker: `PPC4161_X3_PARENT_FLOW_FUNCTIONAL_HIERARCHY_4955`.

## Next target

`4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md`

Construct and solve the gravity-coupled constant-gradient fixed-function
equation for `P_k(X)`. Enforce regularity, convexity and increasing-order
convergence rather than setting the next coefficient to zero. Only a stable
functional trajectory may supply `r3` to the 4954 amplitude or warrant the
full unequal-time 2PI solve. Keep `O2`, `O4`, `O5` and curved-projection
residuals explicit.

## Current checkpoint 4956 handoff

Last checkpoint:
`4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md`.

The finite-polynomial nonclosure identified at 4955 has been addressed by
constructing the full local `P_k(X)` functional projector. Its arbitrary
`p,p',p''` metric-motion Hessian and normalized Wetterich trace reproduce the
independent scalar hierarchy and both gravity source coefficients

```text
beta_c|0=20g^2,
beta_e|0=-(208pi/5)g^3
```

to maximum relative error `3.05e-15`.

The Gaussian matter root was continued to the source-locked 4935 gravity
fixed point, raised through polynomial projections `N=2,...,12`, and
continued back to the Gaussian endpoint. Every step passes for both
`eta_N=0` and `eta_N=-2`. The low functional coordinates converge with
relative spread below `7.99e-9`, selecting the ultraviolet germ bracket

```text
3.84413576778<=r3_UV,germ<=4.35063788925.
```

Both `N=12` branches are scalar-convex and full-Hessian regular on
`0<=x<=0.1`, with minimum singular value above `0.337`. Both lose scalar
convexity before `x=0.25`; a global fixed function is not established. The
bracket is ultraviolet, not the infrared coefficient entering the 4954 rate.
`O2`, `O4`, `O5` and curved projectors remain explicit residuals. The 4947
local GR/Newton/Maxwell branch is retained, and full MTS remains false.

Marker: `PPC4161_FUNCTIONAL_PX_FIXED_FUNCTION_4956`.

## Next target

`4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md`

Integrate the converged functional coordinates down the source-locked 4935
GR-connected trajectory, propagate the two regulator insertions as a scheme
band, and require the physical trajectory to remain inside the proven
`x<=0.1` regular domain. Derive or bound the omitted `O2`, `O4`, `O5` and
curved-projector residuals. Only a resulting infrared `r3` may be supplied to
the 4954 number-changing kernel or used to justify a full unequal-time 2PI
calculation.

## Current checkpoint 4957 handoff

Last checkpoint:
`4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md`.

The 4956 functional motion germ has now been joined self-consistently to the
scalar-backreacted `C3-CFF-F4-O4` gravity parent. Combined roots exist through
`N=8` in both declared regulator schemes. Their ratio-coordinate stability
matrices retain exactly one GR-connected relevant direction.

All four `N=6/N=8` trajectories reach `g=10^-10`. The low infrared
coordinates are order converged, and every direct full-Hessian sample remains
regular on `x<=0.1`, with minimum singular value `0.336372084499`. `O2` is
locally silent by field degree, `O4` is included with its anomalous-dimension
weights and is locally source/stress silent, and `O5` is forbidden by the
selected reflection. The 4947 local GR/Newton/Maxwell chain is retained.

The raw trajectory ratio obeys

```text
r3_raw=[A3/(2A2^2)]/g,
g r3_raw in [8.003921167e-4,8.152905004e-4],
K24_raw(g=1e-10) approximately 5.8118225e-64.
```

The raw ratio is not the physical 4954 amplitude coefficient. The
six-derivative essential quotient and direct on-shell amplitude map remain
open. No global fixed function, complete nonzero-background motion sector,
observational rate or full-MTS result is claimed.

Marker: `PPC4161_FUNCTIONAL_PX_O4_GR_TRAJECTORY_4957`.

## Next target

`4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md`

Derive the redundant-operator quotient at six derivatives and map the
running raw `X2/X3` coordinates to an essential coefficient. Prefer direct
on-shell `2->4` projection if it removes basis ambiguity. Only that invariant
result may be supplied to the 4954 formation kernel. Do not fit the map,
equate it to raw `r3`, or disturb the retained local GR branch.

## Current checkpoint 4958 handoff

Last checkpoint:
`4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md`.

The five-element CP-even shift-symmetric six-derivative basis is now
source-locked. A finite disformal-conformal Einstein-frame map removes the
redundant `R X` and Ricci-gradient coordinates and yields

```text
c_ess=c+8pi g(ctilde+d),
e_ess=e+24pi g c ctilde+128pi^2g^2ctilde^2+64pi^2g^2ctilde d.
```

Maintaining `ctilde=d=0` along the flow gives the derived functional kernel

```text
Delta beta_a_m=16pi g a_(m-1)
 [(3-m)beta_d+(m/2)beta_ctilde].
```

It exactly reproduces the independent essential source `beta_c=16g^2`.
The corrected combined roots persist through `N=8`; `N=6/N=8` in both
schemes retain one GR-connected relevant direction and all four trajectories
reach `g=10^-10`. The infrared coordinates pass the order gate by at least
three orders of magnitude. The 4947 local GR/Newton/Maxwell branch remains
retained.

The flat-scalar `X2/X3` tree `2->4` subamplitude is now basis independent in
the declared minimal-essential frame. The complete gravity-motion
six-scalar amplitude remains open because `O2`, `O3=C^3` and `O4=C^2X` have
allowed external-scalar graviton projectors at the same derivative order.
No galaxy rate or full-MTS result is claimed.

Marker: `PPC4161_ESSENTIAL_PX_SIXPOINT_TRAJECTORY_4958`.

## Next target

`4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md`

Derive the canonical, amputated and gauge-independent on-shell six-scalar
projectors generated by `O2`, `O3` and `O4`, including all attachment
permutations and interference with the essential scalar amplitude. Evaluate
them along both scheme brackets and both trajectory orders. Do not set the
curvature projectors to zero by flat-background counting or supply the 4954
formation kernel before the full amplitude closes.

## Current checkpoint 5019 handoff

Latest completed checkpoint:
`5019-Y5-R2FR-hhh-exact-soft-endpoint-and-crossed-pole-theorem.md`.

The coupled outer-cut route has advanced beyond the earlier numerical smoke.
Checkpoint 5018 completed the crossed `hh` contribution with an exact
Legendre resolvent and an explicit Hadamard finite part. Its remaining
crossing-complete `hhh` target is fixed modulo local `stu`.

Checkpoint 5019 then reduced the full `hhh` soft endpoint analytically. For
even `J>=4`,

```text
a_J = 12 sqrt((J-4)!/(J+4)!),
b_J = a_J [2 log(2)-R_J],
R_J = 8(lambda_J^3-5lambda_J^2+18lambda_J+36)
      /[lambda_J(lambda_J-2)(lambda_J-6)(lambda_J-12)].
```

The physical endpoint is

```text
G0_hhh(z)=2[(S(z)-2 log(2)) A_4(z)+2 C_4(z)],
```

and its direct series agrees with the independent resolvent to
`5.69e-17`. All tested physical soft, collinear, recoil and simultaneous
boundaries are integrable.

The crossed obstruction is now identified exactly. For `z>1`, the helicity
factors have real-sphere simple poles at

```text
q_-=0: A=+-1/z, phi=pi/2,
q_+=0: A=+-1/z, phi=3pi/2,
Res_phi=-i sigma (z^2-1)^2/(2z).
```

These poles cross the unit azimuth contour. Therefore checkpoint 5017's raw
crossed real-sphere QMC values are rejected as an analytic continuation, not
merely labelled noisy. No theory verdict follows from their mismatch.

Marker: `MTS_5019_HHH_EXACT_SOFT_ENDPOINT_AND_CROSSED_POLE_THEOREM`.

## Next target

`5020-Y5-R2FR-finite-x-hhh-azimuth-pole-sectorization-and-residue-sum.md`

Complexify the finite-`x` three-body phase-space azimuth with
`t=exp(i phi)`, factor every surviving five-point KLT pole, track which roots
cross the unit contour, and add their residues before integrating over
`x` and the remaining angles. Compare the corrected cyclic `hhh` vector
directly with the checkpoint-5018 nonlocal target. Do not fit the five target
values and do not use a local scheme change to erase a nonlocal mismatch.

## Current checkpoint 5023 handoff

Latest completed checkpoint:
`5023-Y5-R2FR-causal-covariant-KLT-endpoint-gate.md`.

The sourced covariant scalar-gluon four- and five-point amplitudes are now
implemented with explicit Mandelstam propagators and generic color ordering.
They reproduce the independent spinor-helicity implementation with maximum
pointwise residuals

```text
four-point KLT             1.264e-15
five-point gauge trees     1.244e-13
five-point KLT trees       2.047e-12
finite-x summed hhh cut    1.058e-14
```

The physical `z=0.3` endpoint approaches the exact 5019 resolvent as
`epsilon -> 0`. The crossed `z=1.5+0.08i` endpoint does not: all four left/right
`i0` sign assignments retain relative residuals above `0.50` at
`epsilon=0.01`. Therefore explicit causal denominators on the undeformed real
sphere are not the crossed analytic continuation. This supersedes 5021's
`q+i epsilon` interpretation but retains its useful global-azimuth coordinate.

The finite-x covariant cut is a real forward step because every candidate pole
can now be assigned to a physical propagator rather than a spinor-gauge bracket.
No coupled-cut, UV, local-GR or full-MTS pass is claimed.

Marker: `MTS_5023_CAUSAL_COVARIANT_KLT_ENDPOINT_GATE`.

## Next target

`5024-Y5-R2FR-physical-propagator-pole-classification-and-coupled-cycle-transport.md`

At fixed soft energy and remaining angles, factor the global-azimuth Laurent
polynomials of every explicit four-/five-point propagator. Evaluate the actual
full-integrand local residue at each coincident root, remove canceled roots,
and track the surviving roots continuously from the physical sheet. Then
derive the accompanying hard-polar detour at the `A=+-1/z` pinch and require
the transported endpoint to reproduce 5019 before applying it at finite `x`.

## Current checkpoint 5033 handoff

Latest completed checkpoint:
`5033-Y5-R2FR-representative-topology-class-kernel-matrix.md`.

The projective causal topology from 5032 is retained. One corrected inner
kernel has now been evaluated for each of its eight topology classes at global
node tiers 24 and 32. All eight pass the unchanged class gates:

```text
max global-tier residual       7.265818964e-5
max adaptive-relative residual 3.785322969e-5
max correction-tier scale      below serialized precision
```

All 190 high-tier collision residues are stable. The whole-cycle cancellation
estimator has been replaced by a pair-local double residue on the causally
owned branch. The global base contour now retains the sub-minimum circle when
well conditioned and moves to the widest logarithmic pole-free annulus only
near chart-origin collapse. These are contour-equivalent numerical repairs,
not fitted physics.

Checkpoint 5032's topology remains authoritative, but its baseline numerical
kernel is superseded by

```text
K_C1 = 11.4923618585 - 13.2844664533 i.
```

The outer phase-space integral, crossing-complete `hhh` cut, UV coefficient,
local GR and full MTS remain open. No GitHub action was taken.

Marker: `MTS_5033_REPRESENTATIVE_CLASS_KERNEL_MATRIX_GATE`.

## Next target

`5034-Y5-R2FR-bounded-adaptive-outer-phase-space-smoke-and-cyclic-hhh-vector.md`

Build a restartable, time-bounded outer `(x,s_z,d_z)` integrator. Every sampled
event must be assigned to the projectively transported Feynman sheet; use
independent scrambles and global-node tiers, persist partial sums and error
estimates, and compare the resulting cyclic `hhh` vector with the fixed 5018
target without fitting it. Stop and checkpoint after at most four wall-clock
hours rather than allowing another unbounded run.

## Current checkpoint 5034 handoff

Latest completed checkpoint:
`5034-Y5-R2FR-bounded-adaptive-outer-phase-space-smoke-and-cyclic-hhh-vector.md`.

The remaining five-angle measure has been reduced exactly to the unit-cube
outer integral

```text
integral_[0,1]^3 du_x du_s du_d K(x,s_z,d_z),
D_hhh/G^3 = (-2/pi) E[K].
```

Every Sobol event and every direct/crossed argument now receives its own
projectively tracked canonical Feynman homotopy. No nearest topology class and
no representative-kernel interpolation is used. The restartable runner writes
immutable config, status, per-topology, per-kernel and partial-result files and
stops only between complete kernels at its wall/job boundary.

The exact-real-endpoint pilot is rejected as a numerical contour evaluation:
it left collision poles on the terminal relative path and produced 12 topology
failures plus three unconverged kernels. On the common upper regulator surface
`Im(z)=0.08`, the global-24 matrix plus a global-32 central audit closes after
one isolated same-path refinement of the `z=-9+0.08i` tracker from 12288 to
24576 steps. All 36 merged jobs are numeric and converged. The central cyclic
global-tier difference is `2.20504e-10` relative.

The two-scramble cyclic vector is

```text
z=-0.6 : 187.2005921 -  8.5522348 i
z=-0.3 :  73.6311740 -  4.5728718 i
z= 0.0 :  51.5881065 -  4.0362784 i
z= 0.3 :  65.5089510 + 15.0376575 i
z= 0.6 :  55.7820112 +  0.8399377 i.
```

After projecting only the predicted vector onto the local `1-z^2` direction,
the nonlocal RMS difference from the untouched 5018 target is `47.6801`.
Outer standard errors are large and only two scrambles were used. Together
with the finite regulator and visible imaginary/asymmetric components, this is
not a target match and not a rejection. It is a concrete convergence target.
A raised-path shortcut is forbidden: at `z=-3+0.08i` it gives a different net
winding signature from the canonical near-boundary Feynman path.

No GitHub action was taken. Local GR, Newton, Maxwell, the epsilon-zero `hhh`
cut, its UV coefficient and full MTS remain unclaimed.

Marker: `MTS_5034_BOUNDED_ADAPTIVE_OUTER_PHASE_SPACE_SMOKE`.

## Next target

`5035-Y5-R2FR-paired-epsilon-zero-and-outer-scramble-convergence-ladder.md`

Keep the same canonical Feynman path, fixed normalization and paired Sobol
events. First run a bounded central-component ladder at decreasing positive
epsilon and increased independent scrambles, testing extrapolation form and
variance. Only after that gate stabilizes should the full five-component
vector be extended. Do not use the raised path, fit the 5018 target, interpret
the two-point outer errors as significances, or promote the `epsilon=0.08`
smoke to a crossing-complete coefficient.

## Current checkpoint 5035 handoff

Latest completed checkpoint:
`5035-Y5-R2FR-paired-epsilon-zero-and-outer-scramble-convergence-ladder.md`.

The exact central crossing combination is

```text
C_epsilon = D(0+i epsilon)
          - [D(3+i epsilon)+D(-3+i epsilon)]/8.
```

The same four independent one-point scrambled Sobol events are paired across
`epsilon=(0.08,0.04,0.02)`. The restartable global-24 run plus a first-event
global-32 audit has `45/45` terminal jobs. Six first-pass kernels exposed a
specific numerical defect: the inherited pair-local residue fallback enlarged
an unstable contour from `0.1` to `0.2` times its safe scale. The audited repair
shrinks nested contours instead. All six close at fraction `0.05`; original and
repaired jobs and hashes remain in the 5035 repair ledger. Final state is
`COMPLETE_WITH_RESIDUE_RADIUS_REPAIR`, with zero failed or unconverged jobs.

The primary cyclic means are

```text
epsilon=0.08 : -65.94550 - 16.31238 i
epsilon=0.04 : -76.81181 - 11.59450 i
epsilon=0.02 : -80.53964 -  6.54195 i.
```

Unpaired real outer standard errors remain large (`72.30`, `81.52`, `84.77`),
but paired regulator-step norms contract from `11.8463` to `6.27893`, giving
diagnostic `p_eff=0.915846`. The unassumed linear Richardson diagnostic is
`-84.2675-1.48940i` with standard errors `88.0595` and `1.49532`. First-event
global-24/global-32 relative differences are below `2e-14` at every epsilon.

The central ladder therefore authorizes a bounded full-vector convergence
smoke. It does not complete the epsilon-zero limit, production precision,
crossing-complete `hhh`, local GR or full MTS. The fixed 5018 target was not
fitted. No GitHub action was taken.

Marker: `MTS_5035_PAIRED_EPSILON_ZERO_OUTER_SCRAMBLE_LADDER`.

## Next target

`5036-Y5-R2FR-paired-epsilon-full-cyclic-vector-and-local-nonlocal-decomposition.md`

Carry the shrinking-radius residue rule into a restartable full-vector runner.
Reuse locked `epsilon=0.08` work and calculate the missing arguments at
`epsilon=0.04` and `0.02` for the first two paired scrambles within a four-hour
boundary. Test convergence of the predicted local `1-z^2` projection and all
five untouched nonlocal components before comparing with the fixed 5018 target.
Do not fit that target or promote two scrambles to production precision.

## Current checkpoint 5036 handoff

Latest completed checkpoint:
`5036-Y5-R2FR-paired-epsilon-full-cyclic-vector-and-local-nonlocal-decomposition.md`.

The immutable run
`source-intake/functional_rg/5036/runs/paired_full_vector_s2_v1` is now
`COMPLETE`: `99/99` jobs, `51` exact source-locked imports, `48` newly
converged kernels, and zero failed or unconverged jobs. The v4 shrinking-radius
rule was active on all 48 new kernels and none required a radius adjustment.

The paired mean-step norms contract across `epsilon=0.08,0.04,0.02`:

```text
full cyclic vector : 11.494850 -> 6.838742
local coefficient  :  2.853803 -> 1.144789
```

Every one of the five eventwise nonlocal components also contracts. Central
global-24/global-32 relative differences stay below `2e-14`, and the maximum
local/nonlocal projection residual is below `7e-14`. The bounded paired
full-vector numerical smoke gate therefore passes.

The linear diagnostic gives local coefficient
`100.874739+0.391444i`. Its untouched nonlocal comparison with the fixed 5018
target has RMS `47.3152`. This is neither a match nor a rejection: only two
one-point outer scrambles exist, their extrapolated local coefficients are
`116.7801` and `84.9694`, and reflection imbalance remains large. The target
was loaded after decomposition and was never fitted.

No epsilon-zero, production-precision, crossing-complete `hhh`, local-GR or
full-MTS claim is made. No GitHub action was taken.

Marker: `MTS_5036_PAIRED_EPSILON_FULL_CYCLIC_VECTOR`.

## Next target

`5037-Y5-R2FR-paired-outer-precision-and-z-reflection-control.md`

Add independent paired outer scrambles in restartable four-hour batches while
retaining the exact cyclic estimator, canonical Feynman transport and v4
residue rule. Track the even/odd `z<->-z` decomposition as a diagnostic without
imposing symmetry, require sensible error scaling, and repeat the untouched
5018 comparison only after the outer variance gate closes. Do not fit the
target or promote a linear two-epsilon diagnostic to a proved limit.

## Checkpoint 5037 in-progress handoff

The locked four-scramble run is
`source-intake/functional_rg/5037/runs/paired_outer_precision_s4_v1`, config
digest `86e46b1d2663217182a1bd246c1367e6dfd1eca61694ec86c388d3182e502c49`.
Its strict matrix is 189 jobs: 117 exact imports and 72 required new kernels.

The first bounded batch and a targeted chart-origin repair leave `131/189`
terminal jobs: 117 imported, 13 newly converged, one failed, zero unconverged,
and 58 not yet attempted. The two-scramble baseline remains the only complete
full-vector population.

Two unstable residue rows at `z=+-4.7142857+0.04i` were derived to arise from
stereographic chart-origin collisions. The v5 audit identifies four distinct
same-source chart roots per kernel across 12 chamber sightings; every
represented global factor root vanishes below `3.8e-15` and none carries a
transported winding. Filtering only those non-required coordinate
degenerations closes both kernels without changing their direct values. The
hash-linked v5 repair is
`scripts/Y5_R2FR_5037_chart_origin_collision_repair.py`.

One honest obstruction survives at `z=9+0.04i`:
`direct:g1:minus_u/direct:g1:minus_v` is a finite, nonzero transported endpoint
collision, not a chart root. It must be sectorized; it is forbidden to filter
or interpolate it. No four-scramble, fixed-target, epsilon-zero, production,
local-GR or full-MTS claim is made. No GitHub action was taken.

Marker: `MTS_5037_PAIRED_OUTER_PRECISION_REFLECTION_CONTROL_IN_PROGRESS`.

## Immediate next calculation

Derive a target-relative chamber split at the finite A14 endpoint collision.
Carry inherited global-cycle ownership on each side, include the boundary
detour explicitly, and require agreement with the unsplit chamber wherever the
pinch is moved off the integration path. Only after A14 closes should the same
immutable 5037 run resume its remaining canonical kernels.

## Checkpoint 5038 handoff

Latest completed local geometry checkpoint:
`5038-Y5-R2FR-finite-endpoint-removable-sector-lemma-and-bounded-resume.md`.

The A14 failure was localized to adaptive quadrature entering the numerical
root-coincidence tube at sector parameter `O(1e-13)`. It was not an ordinary
chamber failure. All eight sides of the four transported endpoints have local
double residues below `3.57e-15`; one-sided quadratic limits converge within
`9.29e-9`, and adjacent sectors agree within `7.03e-9`. The conditional contour
lemma therefore makes these endpoints removable for this event: the boundary
detour vanishes and no half-residue is inserted.

The hash-linked primary/audit repair uses extension floors `1e-9` and `2e-9`.
Both return

```text
D/G^3 = 833.9779876731545 + 261.7261506446660 i,
residual = 3.6128138543e-5.
```

Only five evaluations inside the numerical tube use the common sector limit;
all off-pinch evaluations are unchanged. This is a certified A14 numerical
result, not yet a symbolic all-event endpoint theorem.

The immutable 5037 matrix then advanced by eight jobs. Six converged directly;
two chart-origin-only rows closed under the existing v5 proof. Current state is
`139/189` numeric: 117 imports, 22 computed kernels, zero failed, zero
unconverged, and 50 remaining. The active four-scramble statistics correctly
remain blocked because only two complete paired vectors exist.

No GitHub action was taken. No epsilon-zero, production-precision,
crossing-complete `hhh`, local-GR or full-MTS claim is made.

Marker: `MTS_5038_FINITE_ENDPOINT_REMOVABLE_SECTOR_AND_BOUNDED_RESUME`.

## Immediate next calculation

Resume `paired_outer_precision_s4_v1` in a bounded batch. Do not alter its
locked config or estimator. Any new chart-origin row must meet v5; any new
finite endpoint extension must receive its own zero-residue and two-sided-limit
certificate. Once all 189 jobs are numeric, calculate the four-scramble outer
precision, reflection control, and untouched fixed-target verdict.

## Checkpoint 5039 handoff

Latest completed checkpoint:
`5039-Y5-R2FR-completed-four-scramble-uncertainty-and-target-audit.md`.

The immutable 5037 matrix is complete: `189/189`, with 117 exact imports, 72
computed-converged kernels, and zero failed or unconverged rows. The finite A14
endpoint at each of `epsilon=(0.08,0.04,0.02)` has its own zero-double-residue,
two-sided-limit, and two-floor certificate. Six chart-origin-only rows close
under v5. No finite collision was filtered as a chart artefact.

The full-vector and local mean steps contract, but raw nonlocal components at
`z=-0.6` and `z=+0.3` do not. The paired uncertainty audit shows that neither
increase establishes noncontraction at 95%; four of five component contraction
tests remain unresolved and `z=+0.6` supports contraction. Every first-order
complex defect retains zero in its Hotelling 95% region.

The untouched fixed target is not excluded by any component, but it is also
not matched: all confidence intervals are broad, with normal-approximate
planning counts `(48,14,40,33,10)`. Neither measured odd component excludes the
fixed target. The numerical bottleneck is now outer sampling variance rather
than topology or inner quadrature.

No GitHub action was taken. No epsilon-zero, production `hhh`, local-GR,
Newton, Maxwell or full-MTS claim is made.

Marker: `MTS_5039_COMPLETED_MATRIX_UNCERTAINTY_AUDIT`.

## Immediate next calculation

Design the next outer-sampling ladder with a sequential stopping contract.
Compare adding independent one-point scrambles against increasing paired points
within each scramble. Stop only when the paired contraction intervals, all five
fixed-target residual intervals, and both odd-component intervals meet declared
precision gates; do not assume eight scrambles will be sufficient.

## Checkpoint 5040 in-progress handoff

Latest local calculation:
`5040-Y5-R2FR-nested-Sobol-variance-reduction-and-sequential-stopping.md`.

The 5018 source errors imply strict hhh-target margins
`(0.264,0.0365,0.310,0.0490,0.264)`. At the observed one-point variances, a
brute independent route would require normal-planning counts from `2.31e6` to
`3.22e7` replicates, so merely adding one-point scrambles is not the primary
route.

The locked 5040 run compares equal-cost designs: four more independent points
against one nested second Sobol point in each existing Owen scramble. The
nested design must reduce scramble-level standard deviation below `0.525395`
of the one-point value to beat the eight-independent-point 95% halfwidth after
the small-sample t penalty.

Current state is `333/378` terminal: 189 exact sample-0 imports, 136 converged
sample-1 kernels, and eight bounded-unconverged rows. `S503401_N0001` and
`S503402_N0001` are production-clean. The third sample closes 37/45 rows; its
eight obstructions each reduce to one required owned-`direct:g1` versus
unowned-`subtraction:decay` collision. There are no topology or adaptive
quadrature failures.

High-node multi-radius probes make the two A13 rows zero candidates, but the
six A00/A14 rows require an analytic or arbitrary-precision iterated residue.
No row was promoted. Their largest measured cyclic impact is `8.26e-9`; a
tenfold envelope remains below `2.27e-6` of every target margin, so the third
scramble is used only for variance-design diagnosis. Its three-replicate SD
ratios are `(0.986,0.426,0.606,0.835,0.614)`: only one component currently
beats the predeclared nested threshold, provisionally favoring independent
scrambles, but no design verdict is made before exact closure and replicate 4.

Marker: `MTS_5040_NESTED_SOBOL_VARIANCE_REDUCTION`.

## Immediate next calculation

Checkpoint 5041 completes that derivation. Because the finite-plus integrand is
an additive direct/subtraction sum, the unowned component is holomorphic on the
owned local global contour and the owned direct residue remains holomorphic at
a cross-source-only relative collision. The causal global-first, relative-second
iterated residue is therefore exactly zero. This is not a tolerance zero.

Both `plus_v/plus_u` and `minus_v/minus_u` branches pass independent 70-digit,
16-by-16 Cauchy checks: halving the relative radius suppresses the alias remainder
by `2^16`, from about `1.24e-19` to `1.89e-24`. All eight rows were recomputed
from backed-up originals and converge. Current state remains `333/378`, now with
189 imports, 144 computed-converged kernels, zero failed/unconverged rows, and
three production-clean nested scrambles. Updated nested/sample-0 SD ratios are
`(1.009,0.415,0.615,0.849,0.616)`; the fourth replicate is still required.

Marker: `MTS_5041_CROSS_SOURCE_ADDITIVE_ZERO_REPAIR`.

## Immediate next calculation

The theorem-guarded continuation has now completed all 45 `S503404_N0001` jobs.
The locked matrix is `378/378`: 189 exact imports, 189 computed-converged jobs,
zero failed and zero unconverged. The fourth block carries 372 recertified
cross-source additive-zero rows with original contracts retained.

Completed nested/sample-0 SD ratios are `(0.873,0.490,0.545,0.706,0.528)`;
nested/equal-cost-independent halfwidth ratios are
`(1.662,0.933,1.037,1.344,1.005)`. The predeclared worst-component decision is
`SWITCH_TO_ADDITIONAL_INDEPENDENT_SCRAMBLES`. This does not pass the stopping
gates: target and imaginary-zero equivalence each fail 5/5 components, while
contraction is supported for 3/5.

Marker: `MTS_5041_THEOREM_GUARDED_5040_RESUME`.

## Immediate next calculation

Do not brute-force the million-scale one-point planning estimate. First derive
an unbiased control variate or stratification for independent scrambles from the
known endpoint/soft decomposition, lock it before seeing new target comparisons,
and run a small equal-cost pilot against this completed matrix. Preserve all
claim boundaries: no production `hhh`, local-GR, Newton, Maxwell or full-MTS
claim yet.

## Checkpoint 5042 handoff

Shifted-Legendre `L1/L2` controls of the three outer Sobol coordinates were
constructed with exact zero uniform expectation and leave-one-scramble-out
coefficients. All three models fail: their worst target-normalized SD ratios are
`1.128`, `1.242`, and `1.113`. No polynomial-control pilot is authorized.

The same audit identifies a physically correlated candidate: the lower
regulator `E040` nonlocal vector. Its unbiased use does not require a known
mean: `mean_H(Y-beta X)+beta mean_L(X)` is exact for fixed coefficients and
independent future high/low samples.

Marker: `MTS_5042_UNBIASED_OUTER_CONTROL_VARIATE_GATE`.

## Checkpoint 5043 handoff

A theorem-first coarse `E040` evaluator now applies the 5041 cross-source zero
before numerical residue work, preserves shrinking-radius same-source rows,
filters certified chart origins, and reuses the promoted 5037 finite-endpoint
continuous extension. Its fixed `coarse12` matrix is `120/120` converged with
zero failed rows, `1299` theorem-zero residues, `1960` numerical residues, and
`300` chart-origin exclusions. The full matrix took `5352.99 s`.

Uniformly coarse `E040` is rejected: only `3/10` real/imaginary channels improve
cross-fitted, the worst SD ratio is `1.884`, and the equal-cost
target-normalized score ratio is `1.370`. No fresh pilot is authorized.

Marker: `MTS_5043_THEOREM_FIRST_COARSE_E040_MULTILEVEL_GATE`.

## Checkpoint 5044 handoff

The loss of correlation is localized. Across nine nested reflection-symmetric
fidelity thresholds, the best fixed split uses `primary24` for exterior crossed
arguments `|z|>=1.5` (`A00-A04`, `A10-A14`) and `coarse12` for the physical band
`|z|<=0.6` (`A05-A09`). It gives an equal-cost score ratio `0.735`, improves
`7/10` channels cross-fitted, and has worst cross-fitted SD ratio `1.492`.
Adjacent thresholds also remain below `0.8`.

This design is locked only as a reserve. Its minimum defensible four-high-unit
pilot needs `45` low units and is projected to take `46.29 h`, so execution is
not authorized under the four-hour cap. It is retrospective estimator design,
not amplitude evidence.

Marker: `MTS_5044_SYMMETRIC_HYBRID_FIDELITY_GATE`.

## Immediate next calculation

Do not run the 46-hour reserve pilot. Derive a cheaper exterior-only control by
conditioning on the exact causal-topology/collision data already produced for
`A00-A04` and `A10-A14`, or analytically integrate the exterior crossed sector.
The next gate must reduce the low-event cost or correction variance enough to
put a fresh four-scramble pilot below the four-hour execution cap before any new
production kernels are authorized.

## Checkpoints 5045-5050 theorem-scope repair handoff

The preceding 5040-5044 handoff is superseded where it relies on the broad 5041
guard. Checkpoint 5045 proves that the exact-zero result was independently
witnessed only for two owned `direct:g1` families. The original eight
third-scramble repairs remain valid; all 372 fourth-scramble theorem zeros were
outside that proved scope and were quarantined.

Checkpoint 5047 recomputed the complete 45-job fourth block under the restricted
guard: all jobs converge, with 684 stable numerical residue rows and zero
theorem substitutions. Checkpoint 5048 backed up and hash-verified the old live
block, installed the replacements, and regenerated the 5040 statistics. The
corrected nested/sample-0 SD ratios are `(0.935,0.657,0.632,0.759,0.673)` and
the design still selects independent scrambles. The corrected 5042 polynomial
controls remain rejected, with score ratios `1.261`, `1.374`, and `1.295`.

Checkpoint 5049 rebuilt the full 120-job coarse `E040` matrix. All jobs converge
and all 97 theorem-zero rows are inside the restricted witnessed scope. Unlike
the quarantined 5043 result, the aggregate multilevel score now passes at
`0.674`; all five real channels improve strongly. A fresh pilot remains blocked
because three imaginary channels are unstable and the worst cross-fitted ratio
is `1.581`.

Checkpoint 5050 reruns the old exterior hybrid family and selects no promoted
arguments. The previous 5044 exterior split was an artefact of contaminated
inputs. Uniform `coarse12` remains best, but is not statistically locked and a
minimum pilot is projected at `31.58 h`.

Markers: `MTS_5045_THEOREM_SCOPE_FALSIFICATION_AND_QUARANTINE`,
`MTS_5048_INTEGRATE_RESTRICTED_FOURTH_SCRAMBLE_AND_REAUDIT`,
`MTS_5049_RESTRICTED_COARSE_E040_MULTILEVEL_REAUDIT`,
`MTS_5050_RESTRICTED_SYMMETRIC_HYBRID_FIDELITY_REAUDIT`.

## Immediate next calculation

Do not revive the exterior split and do not launch a 31-hour pilot. Derive and
cross-fit a phase-covariant complex control coefficient, together with a
predeclared real-only fallback (`beta=0` on unstable imaginary channels), using
the existing corrected 5049 matrix. Compare those unbiased estimators against
the scalar-channel control. Authorize fresh kernels only if every selected
channel is stable and the equal-cost score stays below `0.8` without fitting the
fixed target.

## Checkpoints 5051-5052 exact Richardson-control handoff

The corrected 5049 data suggest five real control coefficients close to one.
Checkpoint 5051 converts that observation into an exact parameter-free
identity. With `H=2R(E020)-R(E040)` and `L=R(E040)`, choosing `B=1` gives
`H-L=2[R(E020)-R(E040)]`. The selected matrix applies this unit coefficient to
the five real channels and fixes all five imaginary coefficients to zero.

The resulting equal-cost score ratio is `0.6663`; all active real correction
ratios are below `0.17`, and inactive imaginary corrections are unchanged.
Complex phase-covariant alternatives are rejected because they amplify at least
one imaginary correction by factors above 15. The exact unit-real design also
beats the fitted real-only design (`0.666` versus `0.681`) while removing all
coefficient estimation.

Checkpoint 5052 deletes each independent scramble in turn without refitting.
Every panel passes: score ratios range from `0.553` to `0.652`, and the worst
active-real correction ratio ranges from `0.140` to `0.297`. The gain is not
carried by one seed. The design is statistically locked but not executed: its
minimum fresh run remains about `32.10 h`, above the current 10-hour cap.

Markers: `MTS_5051_PHASE_COVARIANT_COMPLEX_CONTROL_GATE`,
`MTS_5052_UNIT_RICHARDSON_SEED_JACKKNIFE`.

## Immediate next calculation

Keep the exact unit-real control fixed. Do not refit a phase coefficient and do
not launch the 32-hour pilot. Audit the low-event cost by topology and argument,
then derive a real-projected or reuse-safe low evaluator that preserves
`H-L=2[R(E020)-R(E040)]`. The next execution gate is a measured projected pilot
below 10 hours with the same delete-one-seed robustness; otherwise retain the
32-hour design as a deferred reserve.

## Checkpoints 5053-5055 cost and sample-unit repair handoff

Checkpoint 5053 traces all 120 rows to measured source jobs and topologies. A
one-event high primary costs `6492.92 s`; a high correction including its coarse
kernel costs `6861.22 s`; and a fresh low-only event costs `1866.46 s`. The
coarse high-side kernel reuses the exact `E040` topology, but fresh low events
cannot. `E020` and `E040` topologies are distinct in all 120 rows and no high
topology charge is duplicated.

Checkpoint 5054 exploits the exact linear projector and all 52 partitions of
the five disjoint raw cyclic components. Splitting low streams never helps. At
10 hours the best full-vector allocation has score ratio `1.128`; the first
apparently efficient allocation uses 12 low units.

Checkpoint 5055 then identifies and repairs a sample-unit defect: the variances
are variances of two-event scramble means, while earlier runtimes charged one
event. The unit-consistent paired threshold is `27.69 h`, not `13.85 h` or the
earlier 32-hour estimate. A conservative one-event design reduces the threshold
to `14.88 h`, but at 10 hours its score ratio is `1.129`. The attractive
sample-index-1 result is retained as a diagnostic and is not selected post hoc.

Markers: `MTS_5053_HIGH_LOW_COST_PROVENANCE_AND_REUSE_AUDIT`,
`MTS_5054_PROJECTOR_STRATIFIED_LOW_STREAM_ALLOCATION_GATE`,
`MTS_5055_VARIANCE_COST_SAMPLE_UNIT_REPAIR`.

## Immediate next calculation

Keep the exact unit-real Richardson control, but do not launch a fresh run under
the current cap. The only honest routes are to derive a lower-cost topology
construction, derive a known-expectation low observable, or explicitly design a
non-claim smoke that reuses the existing low bank and reports its selection
dependence. Do not lower the number of high units merely to fit the clock and do
not use a two-event variance at one-event cost again.

## Checkpoints 5056-5064 certified topology-transport handoff

Checkpoint 5056 finds that 119/120 saved `E040/E020` pairs preserve their full
discrete crossing structure even though only 29 numerical root signatures are
equal. The sole structural transition is `S503402_N0000/A06`.

Checkpoint 5057 transports the labelled `E040` collision branches directly to
the exact `E020` target roots. All 119 permitted numerical signatures are
reproduced exactly, with maximum target-root error `1.32e-16`; the structural
exception remains a full-homotopy fallback. Checkpoint 5058 shows that this
reduces mean high-primary cost by `21.2%`, from `6492.92 s` to `5118.31 s`, but
does not make the multifidelity estimator preferable under 10 hours because it
also cheapens the high-only comparator.

Checkpoint 5059 supplies the missing a-priori decision rule. An 8/16 short
epsilon-segment certificate detects exactly the one transition across all 120
`E040 -> E020` cases at mean cost `0.277 s` per argument. Checkpoint 5060 tests
the same rule on 84 held-out `E080 -> E040` cases: it independently catches
`S503403_N0000/A06` and transports the other 83 signatures exactly, with no
false negatives.

Checkpoint 5061 writes complete transported topology documents. Across 204
combined cases, all 202 certified transports match the full target's numerical
signature, class, endpoints, and kernel-consumed contract; the two transitions
remain unwritten fallbacks. Checkpoint 5062 then replays a nonzero eight-crossing
kernel. Full and transported topologies give exactly the same topological
correction and final complex kernel and reproduce the saved job.

Checkpoints 5063-5064 integrate the rule as a default-off, explicit opt-in
prefill. Disabled mode writes nothing; enabled mode writes only certified safe
targets, never overwrites an existing target, leaves transitions for full
homotopy, and is accepted by the existing 5034 cache path at zero homotopy
runtime.

Markers: `MTS_5056_TOPOLOGY_COMBINATORICS_INVARIANCE_SWEEP`,
`MTS_5057_DIRECT_TARGET_ROOT_TOPOLOGY_TRANSPORT_BENCHMARK`,
`MTS_5059_SHORT_EPSILON_SEGMENT_TRANSITION_CERTIFICATE`,
`MTS_5060_HELDOUT_E080_TO_E040_TRANSPORT_CERTIFICATE`,
`MTS_5061_SERIALIZED_TRANSPORT_TOPOLOGY_CONSTRUCTOR_DRY_RUN`,
`MTS_5062_NONZERO_KERNEL_TRANSPORT_REPLAY`,
`MTS_5064_OPT_IN_PREFILL_INTEGRATION_SMOKE`.

## Immediate next calculation

The epsilon transport route is accepted and operationally complete. Do not
repeat its proof or launch a fresh estimator merely because high-event topology
is cheaper. The remaining cost bottleneck is the fresh low-only `E040` topology.
Benchmark the same certified continuation idea across the ordered argument
ladder: compute full homotopy only at class anchors, certify each adjacent
argument segment, transport when its transition signature is zero, and fall
back otherwise. Require held-out exact signatures and measured low-event cost
reduction before revisiting the 10-hour estimator gate.

## Checkpoints 5087-5090 exact double-zero repair and v7 resume handoff

Checkpoint 5087 rejected the extra numerical removable-limit level for
`E020/S507603/A07`; neither the `1e-7` tolerance nor the Richardson acceptance
rule was relaxed.

Checkpoint 5088 derives the local collision instead. For
`G=I/w` and `H=(w-u)(w-v)G`, the regularized constant and linear terms vanish,
the root split derivative is nonzero, and both adjacent chambers' owned
residues are linear in `q-q0`. Their exact collision limits are zero. The
blocked fixed event then converges with all residues stable and no principal
value or half-residue insertion.

Checkpoint 5089 integrates that rule only for
`E020__S507603_N0000__A07__primary24`; a fresh run and cache resume pass, and
the old numerical removable extension is not invoked.

Checkpoint 5090 preserves v6, creates a hash-locked v7 carry-forward, and
stages 113 converged rows. The first genuinely new post-repair row, `A08`, also
converges. Current v7 state is `114/360` converged, zero failed, 246 missing,
and `PAUSED_JOB_CAP`.

Markers: `MTS_5087_FINER_REMOVABLE_LIMIT_CERTIFICATE`,
`MTS_5088_EXACT_SAME_SOURCE_DOUBLE_ZERO_COLLISION_CERTIFICATE`,
`MTS_5089_EXACT_DOUBLE_ZERO_RUNNER_INTEGRATION_SMOKE`,
`MTS_5090_V7_PILOT_CERTIFIED_CARRY_FORWARD`.

## Immediate next calculation

Resume the v7 pilot at `E020__S507603_N0000__A09__primary24` under the
four-hour cap and stop on the first failed or unconverged row. Do not revive the
5087 numerical ladder. Do not run aggregate 5080 statistics before the full
360-row matrix is complete.

## Checkpoints 5091-5092 coarse multi-root repair and v8 handoff

The v7 pilot advanced to 131 converged rows and then stopped at
`E040__S507603_N0000__A11__coarse12`. The 5085 numerical removable extension
missed its strict `1e-7` criterion; that criterion was not relaxed.

Checkpoint 5091 finds both exact `direct:g2:plus_u/plus_v` collision roots.
At each root the pair-regularized numerator has a double zero, the root split
is nonzero, and both possible owned residues are linear in displacement from
the root. A refined-distance, higher-node audit passes without changing any
acceptance threshold. The formerly blocked event converges with six exact
calls and no numerical fallback.

Checkpoint 5092 preserves v7 and creates a source-hashed v8 carry-forward.
After correcting and rejecting a constructor-wiring failure before numerical
evaluation, the actual v8 runner replay converges. The matrix then advances
through coarse A12-A14 and primary A00-A01 of `S507604_N0000`.

Current state: `bounded_central_anchor_pilot_v8` has `137/360` converged,
zero failed, 223 missing, and is paused at the job cap. The formalization tree
hash remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.

## Immediate next calculation

Resume at `E040__S507604_N0000__A02__primary24` under the four-hour cap and
stop on the first failed or unconverged row. Do not loosen a contour or
convergence threshold if another collision appears; derive its local form
first. Do not run aggregate 5080 statistics before the 360-row matrix closes.
