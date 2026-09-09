# O4 coupled reference and weak kinetic overlap

Date: 2026-09-07. Private continuation; no GitHub action.

**Latest executed status (09:50 BST):** the endpoint-matched full O4
reference has passed ten coarse/fine cases and the refined signed-response
analysis passes **103/103** checks. The earlier collocation failure and
larger-step 102/103 analysis are preserved below. This is a finite-reference
coupling response, not a physical preparation or all-operator local-GR result.

**Status at implementation:** derived equations and runnable implementation,
compiled and dry-run provenance verified. The coupled numerical cases have
NOT yet run: checkpoint 5513 record 45 owns the single numerical core.
Do not substitute compilation, a finite Galerkin spectrum, or a numerical
sensitivity parameter for a physical parent/preparation claim.

## 1. Preserved reference and actual new calculation

The validated gamma-two, zero-O4 calculation remains unchanged:
- scripts/parent_radial_overlap_20260906.py
- scripts/parent_coupled_fluid_radiation_20260906.py
- source-intake/local-preparation/20260906/coupled-fluid-radiation-green-validated.json

The 31-check derivation pack remains unchanged:
- DERIVATION-20260907-O4-Hilbert-source-and-responsive-matter.md
- scripts/parent_O4_hilbert_source_20260907.py
- source-intake/local-preparation/20260907/O4-Hilbert-source-initial.json

The new implementation is separate:
- scripts/parent_O4_star_profile_20260907.py: smooth material background and
  the full scalar Hilbert density, radial pressure and energy flux.
- scripts/parent_O4_fluid_response_20260907.py: driven material response,
  Einstein constraints, curvature variation and two metric-overlap forms.
- scripts/parent_radial_O4_overlap_20260907.py: bound and continuum equations
  with K0, contact reduction, correctly weighted norm and outgoing overlap.
- scripts/parent_O4_coupled_radiation_20260907.py: guarded, resumable driver.

This is an auxiliary, same-retained-action stellar response calculation,
not a claim that the chosen EOS is the observed material of any real star.
It retains the full derived O4 source, rather than freezing curvature or
holding the material at rest while imposing a time-dependent gravitational
source.

## 2. Smooth material and regular surface

In raw reference units mb=K=G=1, use
P(Y)=(sqrt(Y)-1)^3/27. With H=log(sqrt(Y)) and q=expm1(H),
n=q^2/9, p=q^3/27, rho=q^2(3+2q)/27, h=rho+p=q^2(1+q)/9,
cs^2=q/[2(1+q)]. This is gamma=3/2, rho=n+2p.

The TOV equations are
mu'=4 pi r^2 rho,
H'=-(mu+4 pi r^3 p)/[r^2(1-2mu/r)].
The surface is H=0, not a rigid wall or a prescribed density step.
A central rest density 0.0009 is a declared reference choice.

After solving in raw units, lengths and geometric masses are scaled
together by s=alpha/raw_mass to set G M m=alpha in scalar-mass units m=1.
Densities scale by s^-2. Consequently the numerical polytropic stiffness
in these rescaled coordinates is s, not the raw-unit value 1.
This is a unit/reference rescaling, not a derived stellar mass or EOS.

Near the surface H~nu'_s(R-r), rho~(R-r)^2 and rho' tends to zero.
Q=-6(mu/r^3-4 pi rho/3), its first derivative, X2 and its first derivative
are continuous. The leading delta-layer identified for the gamma-two
surface is therefore absent; rho'' and the higher-order volume source
may have finite one-sided jumps. Integration must retain those jumps.

At the center, evaluating Q as a subtraction of two O(1) terms loses the
O(r^2) signal and destroys Q''. The implementation instead constructs a
sixth-order series in z=r^2:
mu/r^3=sum v_j z^j, H=sum H_j z^j,
v_j=4 pi rho_j/(2j+3),
H_(j+1)=[-0.5(v+4 pi p)/(1-2zv)]_j/(j+1),
Q_j=16 pi j rho_j/(2j+3).
Q_0 is exactly zero. This is a center regularity derivation, not smoothing
of a singular or failed source.

## 3. Matter response from the same conservation equations

Write sigma=2 omega and use the full derived O4 plus canonical source
(rho_tau,p_tau,j_tau), with j_tau the sine-harmonic mixed T^r_t.
Let f=1/a^2, nu=log N, lambda=log a, h=rho+p, and
B_s=-4 pi G r j_tau/(sigma f),
J_m=4 pi G r h/f,
F_s=(nu'+1/r)B_s+4 pi G r p_tau/f,
V=sigma^2/(f N^2)+nu'^2+4nu'/r-8 pi G p/f.

The regular fluid variables are w=xi/r and y=P/(h cs^2), where P is
Lagrangian pressure, NOT Eulerian pressure. Their equations are
w'=(nu'-3/r)w-y/r-B_s/r,
y'=V r w/cs^2-[nu'+J_m+(log(h cs^2))']y-F_s/cs^2.

At the regular center y+3w=0. Near the free surface,
P'~ -gamma nu'_s h y, so
y_s=-(V_s xi_s-F_s)/(gamma nu'_s).
The old gamma-two factor cannot be reused for gamma=3/2.

The numerical boundary is a small enthalpy cut, not the exact singular
endpoint. The two accuracy settings use H_cut/H_center=1e-5 and 1e-6,
with the derived regular branch extrapolated to the surface. Agreement
between these settings must be checked. An analytic linear Jacobian is
used; the boundary condition alone does not establish convergence.

The matter perturbations are
delta p=h cs^2 y-xi p',
delta rho=h y-xi rho'.
Then
B=B_s-J_m xi,
B'=4 pi G r(delta rho+rho_tau)/f-B(1/r-2lambda'),
C'=(2nu'+1/r)B+4 pi G r(delta p+p_tau)/f.
Differentiate the last constraint using the Euler equation and the
analytically differentiated Hilbert pressure to obtain C''.

## 4. Independent weak fluid response check

Use zeta=r^2 xi/N and define
Pi=a N^3 h cs^2/r^2,
W_f=a^3 N h/r^2,
Q_f=a N^3 h(nu'^2+4nu'/r-8 pi G p/f)/r^2.
The driven equation is
[-(Pi zeta')'-Q_f zeta]-sigma^2 W_f zeta
=(a N^2 h cs^2 B_s)'-a N^2 h F_s.

Its weak load for test function v is
-integral a N^2 h [F_s v+cs^2 B_s v'] dr.
The free-surface boundary term vanishes with h cs^2, and regular trial
functions take the form r^3 times piecewise-linear hats.

The independent finite-element solve compares 96 and 192 cells against
the collocation solution in the W_f mass norm, as well as computing the
finite generalized spectrum. It tests sign, normalization, forcing and
boundary implementation. It is NOT a rigorous enclosure of the infinite
fluid spectrum. An off-resonance finite-matrix test is deliberately not
reported as a continuum stability theorem or as proof of preparation.

## 5. Actual curvature/kinetic variation

For K0=1+2u W with W=4Q^2/3,
delta Q=f[C''+(2nu'-lambda'-1/r)C'+(1/r-nu')B']
        -2B(Q+1/r^2)+sigma^2 B/N^2,
D=delta K/K0=16u Q delta Q/(3K0).

The time-acceleration term sigma^2 B/N^2 is retained. The third harmonic
metric source includes
s_D=(omega^2+N^2/(2K0))D phi + N^2 f D' phi'/2.
Simply setting D=0 while retaining O4 in the bound operator is inconsistent.

However, differentiating D numerically would demand a poorly conditioned
third metric derivative. It is unnecessary. Set
w_rad=K0 a r^2/N, p_rad=K0 N r^2/a, V_rad=N a r^2
and use the exact bound equation
(p_rad phi')'=(V_rad-omega^2 w_rad)phi.
For the regular third-harmonic continuum mode u_reg, integration by parts
gives the exact weak overlap
I_D=integral D[(3/2)omega^2 w_rad u_reg phi
              -(p_rad/2)u_reg' phi'] dr
    +[D p_rad u_reg phi'/2]_boundary.

This follows by expanding the derivative of D p_rad u_reg phi'/2; the
V_rad terms cancel, not the entire D source. The driver contains an exact
rational identity and wrong-sign/omission controls for this transformation.
The identity applies distributionally to finite internal jumps of D:
the weak integral includes their effect rather than silently dropping the
interface delta in D'. Only the finite outer boundary is added explicitly;
the regular-origin contribution tends to zero. The small origin cut is
the same as the existing radial reference.

The non-D geometric source is separately integrated through both the
first-derivative Green form and the reduced C'' form, with its own outer
boundary term. Agreement is measured before adding I_D so a large D term
cannot conceal a failed geometric identity. The naive reconstructed-C
integral is retained as a conditioning diagnostic, not a pass criterion.

## 6. Coupling, units and first-order sensitivity

The numerical scan uses u=eta R_star^4 with signed eta and half-step probes.
Eta is NOT a fitted MTS parameter, nor is 0.01 the sourced physical
coefficient. It magnifies the response sufficiently to resolve it in
floating-point arithmetic. Analytic monotone-density Weyl bounds require
K0>0 before accepting a case.

A finite-eta solve contains powers beyond first Wilson order in the retained
model. The strict first-order response must instead be extracted from the
eta -> 0 derivative, with signed and half-step agreement. No ultraviolet
resummation or omitted-operator control follows from this probe.

For a mode normalized by 4 pi integral w_rad phi^2 dr=1, the independent
Hellmann-Feynman identity gives
d(omega^2)/d eta =
8 pi R_star^4 integral W[N r^2/a phi'^2-omega^2 a r^2/N phi^2] dr.
The implementation divides by the actual central-value-one norm.
It is a check on signed finite differences, not a replacement for them.

The historical 5191 sourced coefficient envelope remains separate.
Converting a physical u in m^4 to these coordinates requires u*m_scalar^4,
then eta=u*m_scalar^4/R_star^4. Evaluating 1+that tiny shift directly and
getting 1 in machine arithmetic would not establish a zero coupling.
No physical damping time, state occupancy or local-GR residual follows
from the unit-coupling spectral density alone.

## 7. Execution and acceptance

Driver example, for the agent after the main numerical worker stops:
.\.venv-score\Scripts\python.exe -B scripts\parent_O4_coupled_radiation_20260907.py --tag reproduce1 --eta-step 0.005 --max-cases 2

The initial bounded run executes only the zero-coupling coarse/fine pair,
preceded by exact algebra and old/new uniform-star regression. Subsequent
invocations resume the same source-hashed manifest, two cases at a time.
Any changed implementation requires a NEW tag; failures and implementation
snapshots remain available. The full candidate matrix has ten cases.

Guards: one logical core, BelowNormal, single BLAS thread, no concurrent
5513 worker, exclusive companion lock, immutable case JSONs, source hashes,
main-state hash and workbench metadata fingerprint. The time guard is
between cases, not a mid-calculation kill. No package install is needed.

Per-case gates cover source conservation, mode matching/Rayleigh identity,
kinetic positivity, contact/geometric Green checks, fluid boundary/ODE
residuals, independent weak response and explicit retention of the O4
terms. Afterward, pairwise resolution, signed coupling, half-step and
Hellmann-Feynman checks remain necessary before a derivative is reported.

**All full-parent preparation, all-operator local-GR and full-MTS claims
remain false.** The selected prepared two-derivative reduction is not
being revoked or re-proved by this companion.

### Queued execution at 08:16 BST

The two-case zero-coupling run is queued behind record 45 with
`scripts/run_O4_coupled_after_5513.ps1`, supervisor PID 38144, run directory
`runs/O4-coupled-pilot1-20260907`. Its initial state is WAITING_FOR_MAIN_45.
It checks the terminal main-state hash, record count and 23 validation rows;
then reserves the main-worker lock until the companion exits. No D4 successor
is started. The waiting supervisor consumes no numerical core workload.
Inspect its terminal marker and immutable case JSONs before advancing.

An initial detached Windows-PowerShell invocation failed before execution
because its inherited module path did not expose Get-FileHash. The successful
supervisor uses the observed bundled pwsh.exe. That launch error is preserved
in runs/O4-pilot1-launch-stderr.txt and is not a failed physics case.

### Executed pilots and endpoint formulation, 09:32 BST

Main record 45 finished at 08:50:48 BST: the active cuboid is completely
certified, 218/0/0, 23/23 checks. Its next target is OUTER_TRANSPLANT, not
another node of the completed cuboid. The companion then owned the safe gap.

Pilot1 failed serializing NumPy comparison booleans before saving preflight.
Pilot2 changes only boolean conversion/output ordering, and its preflight
passes. Its surface collocation solve failed at the unchanged tolerance;
pilot3 preserves diagnostic locations: the largest residual 0.04314 occurs
near r/R=0.99998031, just inside the free-surface enthalpy cut. Neither
failed case is counted as a numerical or physical pass.

The subsequent implementation keeps the same equations, surface condition
and independent finite-element response, but integrates two regular endpoint
bases to R/2 and solves a two-by-two matching system. This avoids propagating
the singular fluid solution toward its divergent endpoint. No extra physical
boundary condition or fluid rigidity is inserted. The matching condition
number, dense-polynomial ODE residual and original boundary conditions are
tested; no failed collocation residual is relabelled as passing.

For the center, write nu'=nu1 r, J=J1 r, log(h cs^2)'=L1 r,
cs^2=c0+O(r^2), B_s=b2 r^2+O(r^4), F_s=f1 r+O(r^3), V=V0+O(r^2).
Set w=w0+w2 r^2+O(r^4), y=-3w0+y2 r^2+O(r^4). The differential equations give
y2=0.5[V0/c0+3(nu1+J1+L1)]w0-f1/(2c0),
w2=(nu1 w0-b2-y2)/5.
These provide separate homogeneous (w0=1, no force) and forced (w0=0)
initial data. The outward integrations start at r/R=1e-5 (coarse) and
1e-6 (fine); the regular series fills the remaining center. At the surface
cut, the two inward bases use (w,y)=(1,-V r/(gamma nu')) and
(0,F_s/(gamma nu')). Their coefficients are fixed by matching both w and y,
not by fitting an observable. The surface cut also tightens by ten between
settings. Existing density/overlap tolerances and independent FE checks
are retained. These changes are in the matched1 test, not the prior pilots.

The DOP853 interpolation-polynomial derivative is differentiated analytically
for the ODE residual, independently of the right-hand-side evaluation. This
uses the installed scipy.integrate._ivp.rk.Dop853DenseOutput recurrence;
simply calling the ODE to define its own derivative would not be a test.

## 8. Completed coupled-response evidence

The immutable matched1 and matched2 directories are under
source-intake/local-preparation/20260907/. Each contains its four executed
implementation snapshots, source-hashed manifest, 10/10 preflight checks
and ten individual case files with 26/26 checks per case. Repeated case
checks are implementation tests, not hundreds of independent theorems.

The zero-coupling pair additionally passes 21/21 cross-resolution checks.
The fine material ODE residual is 1.81e-8, geometric Green relative residual
4.08e-7, and 192-cell independent forced-response difference 4.63e-5 in the
fluid mass norm. Refining from 96 cells reduces that difference from
1.83e-4. The finite eigenvalues remain positive, with the driving frequency
between computed modes and approximately 0.199 relative gap from the nearest;
this remains a finite-matrix check, not a continuum spectral enclosure.

The complete matched1 matrix used eta=0,+/-0.01,+/-0.005. Its analysis
passes 102/103: the spectral-density central derivative changes by 2.34%
on halving the step, exceeding the unchanged 2% gate. It is retained as a
failed step-resolution analysis, not declared a physical failure or pass.

The matched2 matrix uses eta=0,+/-0.005,+/-0.0025 with unchanged equations,
numeric tolerances and acceptance gates. All cases pass, and the matrix
analysis passes **103/103**. Its spectral-density derivative changes by
0.581% under step halving. The frequency derivative independently matches
the Hellmann-Feynman integral to 1.23e-7 relatively. The logarithmic density
identity, including continuum factor and bound-mode norm derivatives,
agrees with the direct response. Noise indicators are not rigorous bounds.

Fine results in this declared alpha_G=0.02 reference:

| eta | Total metric overlap I_g | Explicit delta-K overlap | Unit-coupling D_g |
| ---: | ---: | ---: | ---: |
| -0.005 | 0.00178342284699 | -0.000988250836619 | 2.59425270825e-21 |
| -0.0025 | 0.00230146896916 | -0.000488906447054 | 4.32867964702e-21 |
| 0 | 0.00280761500330 | 0 | 6.45445528995e-21 |
| 0.0025 | 0.00330191302586 | 0.000478518911019 | 8.94443178099e-21 |
| 0.005 | 0.00378441492257 | 0.000946700499776 | 1.17720940354e-20 |

The finite signed probe therefore does NOT support discarding delta K.
Richardson estimates at eta=0 are
d(omega^2)/d eta=-1.03430653671e-6,
dI_g/d eta=0.200085345935,
dI_deltaK/d eta=0.193481717606,
dD_g/d eta=9.24939191487e-19,
d log(D_g)/d eta=143.302439933.
The explicit delta-K term supplies about 96.7% of the derivative of the
unnormalized overlap in THIS reference. This fraction is not a universal
MTS prediction. The resolved first-order response includes bound-mode,
fluid/geometry, continuum normalization and explicit kinetic variation.

The rate convention is inherited from
DERIVATION-20260906-parent-nonlinear-transfer.md: if the stated outgoing-state,
single-mode and nonlinear-remainder hypotheses hold, D_3 gives
P_out=(3 omega/2) A^6 D_3 and A_dot=-3D_3 A^5/(2 omega) at leading order.
The new calculation fills a retained-operator coefficient in that conditional
law. It does NOT prove those hypotheses, zero trapped occupation, or a local
preparation timescale. Actual couplings and dimensions must be restored;
the unit gravitational coupling and magnified eta are not physical values.
Likewise alpha_G=G M m=0.02 is a numerical reference, not a sourced Earth,
Sun or neutron-star parameter. Physical small-alpha control remains necessary.

### Reproducibility and preserved failures

- matched2/analysis-signed-response.json SHA:
  9aa185347075f2af5c2acddee2418bc9192b1723eb1a6e6026d56b0db99dc56c.
- matched1/analysis-signed-response.json (102/103) SHA:
  1fdfe62f9cf4cd8bb55a8906a5412420d811e931d733127726280a8d32e0845d.
- scripts/parent_O4_coupled_radiation_20260907.py SHA:
  6b87ace934c4e117d2e09a60eb877348ba603ba4e4ec6611fc8b41ffef2f6ee6.
- scripts/parent_O4_fluid_response_20260907.py SHA:
  b3f3b187fa3a2f1676d11093912cfb713d8d00477fe59e6b87f7abe9c6e986cb.
- scripts/parent_O4_star_profile_20260907.py SHA:
  85ea845693d07d52369f15f15f95f177cb5817744c878bbb922e06c635747425.
- scripts/parent_radial_O4_overlap_20260907.py SHA:
  b1f6836202fe25264f94a04a5cee3945c5617e8f4a8805e79e943861343bafb9.
- scripts/analyze_O4_coupled_response_20260907.py SHA:
  38328147a8f2db0ff7667789a7ae02f7aa113279e8adfa5cbcda3517d88f66af.

The analysis script checks executed snapshots separately from historical
dependencies, reconstructs the spectral density and its normalization, tests
signed/half-step resolution and the independent frequency derivative. An
initial analysis-only snapshot check incorrectly expected the historical
Hilbert script among the four new snapshots; its correction does not change
any numerical case. An attempt while a numerical worker was still finishing
was rejected by the guard; no competing numerical job was started.

All companion cases preserve main state SHA
7ab2c0b74444f4bfd3d828c0dcf36409fd771d4963ef55012fdbe734e7c2c6e6.
The 8760-file workbench metadata fingerprint is unchanged:
5d2a482310acd9ba509985c584515bfd8525b721a5d5629c900ab055445acf38.
This is a size/mtime/path fingerprint, not a content-hash manifest. All code
and documentation edits are in post-checkpoint-work, no caches or GitHub
actions, and validated historical source hashes still agree.
