# Full characteristic reference and actual piecewise-curvature regularity

2026-09-17. Private continuation of
`DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md`.
Original prescribed flat spherical action, profile, source mass, initial
velocity and both finite branches are unchanged. No GitHub action.

## 1. What this step establishes

The complete flat spherical continuum reference is now constructed and
numerically qualified, including the outer reflections omitted by a
source-only calculation. Its actual two initial curvature fronts have
uniform finite curvature and piecewise third-derivative bounds on [0,.4].
This fills the reference-regularity hypothesis needed for the previous
extra-Gram consistency argument; it does not prove the total Galerkin
residual, nonlinear neighborhood bootstrap or instantaneous force convergence.
This is not the full GR limit or a solution of the full MTS parent theory.

The source-only reference from the previous step was already independent of
the old spectral field calculation. This step implements its full spatial
field and tests the SAME saved MTS and reference trajectories against it.
All 77 current implementation checks pass. Physical acceptance flags remain
separate, including four failed peak-force gates. No large finite trajectory
is re-evolved, force-corrected, fitted or selected to improve these results.

## 2. Complete field construction

Use a=5.2, c=6.8, b0=6.03, V0=.06, m=.03 and T=.4, in the unchanged
benchmark's numerical units. The scalar profile is the original compact
quintic envelope multiplied by .01(r-b0). Put

    chi=r phi=F(t-r)+G(t+r),    chi_tt=chi_rr.

The incoming initial functions, with I(r)=integral_b0^r phi_0(s) ds, are

    F0(-r)=[(1+V0)r phi_0(r)-V0 I(r)]/2,
    G0(r) =[(1-V0)r phi_0(r)+V0 I(r)]/2.                (1)

Their first two argument derivatives are evaluated analytically from the
original piecewise polynomial. The implementation uses local offset r-b0,
not a high-power polynomial in the full radius. Independent quadrature of
the original profile verifies I(r). The integration constants at the outer
boundaries are not arbitrarily set to zero: F0+G0=0 there, but F0 and G0
separately need not vanish.

### Moving-source reflection

On the left, incoming F remains F0 until a boundary return reaches the source;
on the right, incoming G remains G0. The energy gate from the previous step
proves no such return by T=.4. Its three-variable source ODE is unchanged.

For the outgoing function choose sign s=+1 on the left (outgoing G), s=-1
on the right (outgoing F), and let A denote the other, incoming function.
Solve the strictly increasing retarded equation

    w=tau+s b(tau),    k=tau-s b(tau),
    B(w)=-A(k),    D=1+sV,    alpha=(1-sV)/D.

Then

    B'=-A' alpha,
    B''=-A'' alpha^2+2s b'' A'/D^3.                  (2)

The map has D>=1/4 on the analytic energy-gated branch. Its inverse is
computed from the dense source ODE solution, with an explicit retarded
equation residual check. No polynomial fit to a finite MTS trajectory is used.

For left-domain G, select G0 when w<=b0 and (2) otherwise. For right-domain F,
select F0 when w<=-b0 and (2) otherwise. These junctions are precisely the
two initial source-emitted curvature fronts. At a front the first derivatives
are continuous but the second derivative is one-sided, not uniquely defined.
At t=0 the code retains the initial-side second derivative; it does not claim
second boundary compatibility at that incompatible initial corner.

### Outer reflection is Robin, not even reflection of chi

Physical Neumann data phi_r=0 give chi_r=chi/r. For the left boundary define
X(t)=F(t-a); for the right define Y(t)=G(t+c). They solve

    X'=G0'(t+a)-[G0(t+a)+X]/a,    X(0)=F0(-a),
    Y'=F0'(t-c)+[F0(t-c)+Y]/c,    Y(0)=G0(c).          (3)

The initial source fronts r=b0+-t cannot reach either outer boundary by .4,
so the incoming functions in (3) are the initial functions over this horizon.
The full field nevertheless contains reflected radiation from the initial
wave profile: lack of a return to the SOURCE does not mean the outer
boundaries remain causally irrelevant everywhere.

Equation (3) and its differentiated form give the first two derivatives of
the reflected functions. Independent integrating-factor quadrature checks
their values, rather than checking the same ODE formula against itself.

### Physical derivatives and diagnostics

For u=t-r and v=t+r,

    phi=(F+G)/r,
    phi_t=(F'+G')/r,
    phi_r=(-F'+G')/r-(F+G)/r^2,
    phi_tt=(F''+G'')/r,
    phi_tr=(-F''+G'')/r-(F'+G')/r^2,
    phi_rr=(F''+G'')/r-2(-F'+G')/r^2+2(F+G)/r^3.      (4)

Wavefronts and profile-transition characteristics are explicit integration
breakpoints. Source-reflected profile transitions use their own retarded
emission times; outer-reflected transitions are included too. This prevents
a quadrature rule from silently smoothing a curvature front.

## 3. Actual reference regularity, not manufactured smoothness

The previous exact energy argument gives |V|<3/4. Thus

    5.73 <= b <= 6.33,    1+-V >= 1/4,
    5.33 <= b-t <= b+t <= 6.73.

Local source ODE existence and the characteristic construction give the
solution initially. Their conserved positive scalar-plus-source energy
prevents escape from this timelike/domain gate before T=.4. The scalar field
is piecewise classical with continuous first derivatives across each initial
front, so there is no extra shock-energy flux. This is a continuation argument
for THIS flat reference; it does not assert a global existence theorem for
the full parent action.

### Explicit uniform majorants

Write delta=7/20 for the profile transition width, d=11/20 for its support
radius, and A0=1/100 for its amplitude. For the quintic S(z), 0<=z<=1,

    S'=-30 z^2(1-z)^2,    0<=S<=1,
    |S'|<=15/8,    |S''|<=15,    |S'''|<=60.

These follow from 0<=z(1-z)<=1/4; they are analytic inequalities, not sampled
maxima. Define bounds on the original profile and its first three derivatives:

    P0=A0 d,
    P1=A0[1+d(15/8)/delta],
    P2=A0[2(15/8)/delta+15d/delta^2],
    P3=A0[45/delta^2+60d/delta^3].                      (5)

The third derivative is piecewise bounded; the second derivative is continuous
at the envelope joins. Safe common bounds for both incoming functions are

    C0=[(1+V0)c P0+V0(c-a)P0]/2,
    C1=[P0+(1+V0)c P1]/2,
    C2=[(2+V0)P1+(1+V0)c P2]/2,
    C3=[(3+2V0)P2+(1+V0)c P3]/2.                      (6)

Let b_- =5.73, b_+=6.33, v_*=3/4, epsilon=1/4. Bounds for the source
gradient, acceleration and jerk follow directly from the source ODE:

    H*=2C1/(b_- epsilon),
    A*=b_+^2 H*^2/m,
    Hdot*=2C2(1+v_*)/(b_- epsilon)
            +H*[v_*/b_-+A*/epsilon],
    B*=b_+^2/(2m),
    Bdot*=b_+ v_*/m+5 b_+^2 v_* A*/(2m),
    J*=2 Bdot* H*^2+4 B* H* Hdot*.                    (7)

The common reflection-map bounds are

    |alpha|<=7,
    |alpha_w|<=2A*/epsilon^3,
    |alpha_ww|<=2J*/epsilon^4+6A*^2/epsilon^5.

Consequently outgoing source-reflected functions have derivative bounds

    C0,
    7 C1,
    49 C2+C1(2A*/epsilon^3),
    343 C3+21 C2(2A*/epsilon^3)
      +C1(2J*/epsilon^4+6A*^2/epsilon^5).              (8)

Outer reflection follows from its scalar linear ODE. Use
exp(T/a)<=1/(1-T/a)=13/12. Its zeroth-derivative bound is

    O0=[C0+T(C1+C0/a)]/(1-T/a),
    On=Cn+(C(n-1)+O(n-1))/a,    n=1,2,3.             (9)

Take Wn as the maximum of the incoming, source-reflected and outer-reflected
bounds. Equation (4) gives

    M2=2W2/a+4W1/a^2+4W0/a^3,
    M3=2W3/a+6W2/a^2+12W1/a^3+12W0/a^4.              (10)

All constants in (5)-(10) are explicit positive rational majorants. Their
exact fractions are saved in the regularity evidence. Numerically they give
M2 approximately444.5203 and M3 approximately2.3062122e6. The sampled actual
maximum |phi_rr| is only about.21929. These bounds are deliberately loose:
they establish finiteness and mesh independence, not a useful numerical
force-error tolerance at the current grids. Floating trajectory integration
is not interval-certified, and the algebra checker is not a formal proof
assistant; neither limitation is hidden by the analytic inequalities.

### Exactly which fronts are allowed

The initial profile is C2 and piecewise C3. Source reflection preserves this
regularity away from the initial corner because its retarded map is timelike
and has bounded derivatives. The initial corner supplies exactly the two
second-derivative jumps already derived:

    Delta G''=-50/2809 on r=6.03-t,
    Delta F''=-50/2209 on r=6.03+t.

No initial source front reaches an outer boundary by T=.4. Initial data
vanish near the outer boundaries, so no initial outer compatibility front
is introduced. Later profile transitions can produce third-derivative
changes but not extra second-derivative jumps. Apart from the moving source
interface, there are two curvature fronts. Between them, curvature has the
uniform Lipschitz majorant M3 even across the continuous-curvature envelope
joins. This is derived from the characteristic construction, not inferred
from a finite number of graph samples.

## 4. What this closes in the discrete consistency argument

The existing source-fitted affine maps satisfy, uniformly over this reference,

    47/77 <= J_map <= 107/77.

The pulled-back second and piecewise third derivatives are bounded by
(107/77)^2 M2 and (107/77)^3 M3. Subtract the exact source derivative-jump
hinge as in the previous lifted-Gram identity; the remaining function is C1
across the source. Two curvature fronts remain, with bounded curvature and
a uniform modulus omega(h)<=C h between fronts.

Applying the previous finite-width stencil estimate therefore gives, on the
nodal interpolant of THIS constructed reference,

    Q_h=||Gtilde U_ref||
       <=C[h^(3/2) omega(h)+h^2 M2 sqrt(3)]=O(h^2),
    ||R_extra,canonical||_*
       <=C[h^(-3/2)Q_h+h^(-1)Q_h^2]=O(h^(1/2)).       (11)

This uses the previously derived mesh/lift/mass bounds for the fixed local
split family and nondegenerate geometry. It establishes a vanishing
EXTRA-Gram residual on the actual reference family, not the total residual
or a uniform bound on the evolved MTS trajectory. In particular, it does not
turn the failed force-trace estimate into a theorem by renaming it energy.

Remaining mathematical link: derive the base Galerkin residual and the
uniform shifted-energy neighborhood bounds, then close the nonlinear
relative-energy bootstrap. Instantaneous source-force convergence requires
its own trace control even if energy/source-position/clock convergence closes.

## 5. Independent numerical qualification

`scripts/qualify_annular_full_characteristic_field_20260917.py` completes
35 checks before any saved finite trajectory is opened. Highlights:

- Original initial field and Eulerian rates reproduced independently.
- Moving-source value/first-compatibility defect: at most1.59e-16.
- Outer Neumann defect: at most5.29e-19.
- Second source compatibility checked only at positive times, not falsely at0.
- Independent finite-difference first-derivative errors below1.47e-12;
  second-derivative errors below1.99e-9 at the selected off-front probes.
- Original continuum energy absolute error:4.30e-16 over81 samples;
  split16/24-point quadrature control:4.17e-17.
- Tighter time settings change first derivatives below3.66e-14 and second
  derivatives below8.49e-13 on the recorded sample grid.
- Both derived front amplitudes reproduced at three times, with C1 matching.
- Outer-reflection values independently checked using integrating factors.

Small sampled errors are not universal or interval error certificates.
The separate exact-majorant script completes15 checks of the analytic
regularity construction, retaining its loose constants and limited scope.

## 6. Fair comparison against saved finite trajectories

Reference equations, module hashes and the qualified reference pack are fixed
and verified before reading the old finite trajectories. This is a known
benchmark comparison, not a blind empirical prediction. Both branches use
the same81 times, the same full continuum reference, the same split physical
integration rule and unchanged old gates. Both locally split grids have
eight subdivisions at each source-side base element.

Field error means the relative physical energy norm of the differences in
phi_t and phi_r, not pointwise error or a percentage of empirical data.
The physical integration mesh contains the two source positions, finite
element edges and continuum wavefronts. Independent6/10-point quadrature
changes the field-error estimates by at most1.32e-12. Original finite forces
are replayed from the unchanged action at three times and match their saved
values; they are not replaced with continuum source formulas.

|Branch|Base nodes|Maximum relative field error|Maximum force error|Terminal force error|
|---|---:|---:|---:|---:|
|Reference|513|9.53924306e-5|5.48253059e-7|+2.32541946e-7|
|Reference|1025|2.58935224e-5|2.31362091e-7|+1.83823487e-7|
|MTS|513|4.93972061e-4|3.67969181e-6|-2.30145251e-6|
|MTS|1025|1.27551923e-4|9.13531208e-7|-7.04040558e-8|

All four cases pass the old field gate. All four pass source position,
velocity and clock gates. All four FAIL the old2e-7 peak absolute-force
gate. Both finer cases pass the separately recorded terminal absolute-and-
relative force gate. A terminal pass must not be substituted for a peak pass.

On refinement, MTS field and peak-force errors shrink by factors.25822 and
.24826, respectively (roughly fourfold). Reference ratios are.27144 and
.42200. These are two-grid results with different source-cell phases, not
a proof of a uniform convergence order. The reference branch also has a
remaining numerical force error; it must not be described as GR itself
failing a physical test.

The old spectral reference gave MTS peak errors3.67184258e-6 and9.20685959e-7.
The improved characteristic comparison changes them only slightly. The
previous MTS peak discrepancy is NOT explained away by reference inaccuracy.
All inherited failures remain available, rather than being overwritten by
the improved reference.

## 7. Next constructive step

Derive the base reference-action Galerkin defect in a norm compatible with
the nonlinear relative-energy identity, retaining the moving-source momentum
and the two travelling curvature fronts. First use exact moment/pullback
identities and bounded piecewise derivatives; do not assume a strong residual
vanishes just because pointwise wave-equation residuals vanish away from
fronts. If a nodal projection loses a boundary trace, derive and qualify an
appropriate energy projection rather than changing the physical action.

Use the full characteristic reference to check this calculation directly on
existing meshes. No expensive new forward run is needed for that derivation.
No extra audit-only loop is required: the full reference implementation and
its actual regularity are completed outputs, not future tasks.

Sources and evidence:

- `scripts/annular_full_characteristic_field_20260917.py`
- `scripts/qualify_annular_full_characteristic_field_20260917.py`
- `scripts/derive_annular_actual_reference_regularity_20260917.py`
- `scripts/compare_annular_characteristic_saved_trajectories_20260917.py`
- `source-intake/navier-stokes/20260914/annular-full-characteristic-field-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-actual-reference-regularity-attempt01/analytic-regularity-majorants.json`
- `source-intake/navier-stokes/20260914/annular-characteristic-saved-comparison-attempt01/status.json`
- `DERIVATION-20260917-finite-width-curvature-and-coupled-energy.md`
- `DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md`
