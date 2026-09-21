# Bounded N128 check and a constructive nonlinear continuation

Private/local, 12 September 2026. No public update, subagents, new physical
claim or time evolution. N128 was the agreed ceiling; N256 was not run.

## 1. Plain-language result

The paired finer-grid initial check succeeds. The main physical differences
between meshes get smaller, though the radial mass gradient is not yet fully
resolved. The small Gram correction continues to shrink with numerical mesh
spacing; this is NOT a new physical screening mechanism or a measured GR limit.

More importantly, we have moved beyond testing the special initial slice:
the full nonlinear history-force formula is now derived and checked against
direct action variations. An endpoint condition also identifies a concrete
next repair. It affects BOTH the GR comparator and MTS, and we have constructed
an explicit small lapse-profile candidate instead of merely recording a gap.
The candidate is not yet substituted into the coupled calculation.

The detailed nonlinear mathematics is in
`DERIVATION-20260912-nonlinear-history-Euler-equations.md`.

## 2. Fair bounded spatial experiment

Both branches use the same prepared N16 scalar/free auxiliary momentum,
original N16 kinetic map K_seed, annulus [5.875,6.125], inner mass, prescribed
mass/scalar drives, lapse-shape prescription and natural outer clock. The
physical scalar momentum is pi=K_seed*xi at every mesh. The fine mesh does
not import a separately fitted archived root. Only the dependent mass
profile and two whole-annulus endpoint amplitudes are solved.

All original canonical phase directions and all 128 parent-kernel directions
are retained. Time links include inherited scalar/mass-face breakpoints,
including the nonnested coarse SBP boundary faces identified last time.
No filter, pseudoinverse deletion, artificial force or bulk smearing is used.
The GR control includes the matched rough canonical scalar; it is not the
earlier distinct smooth manufactured GR reference or vacuum GR.

| N128 quantity | MTS metric-Gram | Matched GR+scalar |
|---|---:|---:|
| Maximum initial constraint | 1.6941e-15 | 1.5450e-15 |
| Maximum first constraint-rate row | 2.0542e-13 | 4.7367e-17 |
| Higher-quadrature constraint-rate row | 1.4544e-13 | 3.4435e-17 |
| Primary inner mass-drive gap | 1.6684e-14 | 4.3368e-19 |
| Primary outer scalar-drive gap | 6.94e-18 | 8.67e-18 |
| Outer clock-value gap | 0 | 0 |

MTS constraint-rate dual L2 norms are 9.41e-12 and 6.52e-12 for the two
quadratures. All specified numerical gates pass. These finite residuals are
not interval certificates, continuum identities for arbitrary fields, or
proof that a trajectory preserves the constraints.

The independent check rebuilds physical fields and all initial C rows,
recontracts the full saved Cdot with its saved Gram-rate component, recomputes
the Gram scalar covector from J and node data, and tests the complete physical
boundary flux. It does not mislabel recontraction of saved rates as an
independent new evolution or a full recomputation of every kernel integral.

## 3. What the extra mesh actually tells us

Same-survey N64-to-N128 L2 differences:

| Quantity | MTS | Matched GR+scalar |
|---|---:|---:|
| mu | 2.7047e-8 | 2.3566e-8 |
| mu_R | 5.1357e-5 | 5.1352e-5 |
| pi_t | 4.0338e-2 | 6.9287e-6 |

The relative mass-gradient change drops from about 13.16% to 6.55% in BOTH
branches. MTS's relative pi_t change drops from about 3.75% to 1.29%.
All eleven measured MTS differences decrease; the slowest ratio is about
0.674 for the radial mass-rate gradient. This supports numerical improvement,
not an asymptotic convergence proof or an error bar against the continuum.

For GR, the pi_R difference grows from approximately 1.93e-14 to 3.30e-14:
it is already at relative scale 1.51e-15. The raw report correctly records
`all_measured_differences_decrease=false` for GR rather than suppressing this
roundoff-scale exception. Its other reported differences decrease. This is
not evidence that GR physically loses a test which MTS wins.

The N128 MTS-minus-matched-GR differences include

    mu L2:   4.4167e-9,
    q L2:    3.3136e-7,
    pi_t L2: 1.19695e-2.

No further mesh was launched. The next task concerns nonlinear boundary
compatibility, not an automatic march through more expensive grids.

## 4. Numerical remainder versus physical theory

The untransported base Gram quadratic form is

    N16: 1.690473e-7,
    N32: 1.052335e-8,
    N64: 6.560864e-10,
    N128: 4.098288e-11.

The approximately factor-16 decrease on halving h is consistent with the
declared high-order numerical remainder. h is a computational spacing, NOT
the physical L_cg or a sourced parent coupling. The full transported action
has its own time Jacobians and is not equated numerically with this base form.

The nonlinear P and P-squared bulk terms derived this turn are inherited GR
geometry terms, not new MTS phenomenology. The canonical scalar has genuine
stress energy, but it is shared with this GR control. This restricted fixture
does not demonstrate a surviving, parent-sourced continuum MTS departure from
GR, nor does it replace the separate galaxy/cosmology evidence programme.

## 5. The conditional endpoint bound now has a real fine-grid check

At N128, each endpoint Gram stencil lies wholly within one of the original
N16 cubic scalar cells. Its constant third derivative can therefore be
calculated without assuming unproven global smoothness. Replacing the earlier
exp(5h sup|g|) estimate by the maximum ACTUAL finite endpoint Jacobian ratio,
the bound is

    |G_chi,b| <= (190279/1719312) h^2 M3 C_max max(J_fi/J_fb).

| Endpoint | Actual force magnitude | Finite conditional bound | Ratio |
|---|---:|---:|---:|
| Inner | 3.820815e-5 | 4.017038e-5 | 0.95115 |
| Outer | 4.978500e-5 | 5.225511e-5 | 0.95273 |

Higher quadrature agrees. The sampled finite Jacobian ratios are about
1.000000309 and 1.000000320. This checks the explicit stencil bound for the
computed data; it does not supply an interval enclosure for the Jacobians,
a uniform bound on future histories, or a physical local-suppression law.

## 6. Actual nonlinear derivation and checks

The companion note gives the full GR+scalar bulk equations, all nonlinear
connection/coefficient derivatives, and the physical-time memory kernel

    K(t,R) = sum_fi oriented_indicator_fi(R)
       [I_fi(s) J_fi(s)/J_f(s,R)^2] at s=T_f(.,R)^(-1)(t).

The resulting covectors G_mu,G_N,G_P,G_chi are written explicitly, including
direct nodal terms, and inserted with their correct signs in the action Euler
equations. This is a conditional formula for full nonlinear HISTORIES, not
reuse of a P=0 instantaneous potential. Time-boundary work is kept.

The completed run passes 70 checks, including 18 symbolic identities and seven
manufactured-history directions. Raw and reduced first variations agree to
1.36e-20 maximum; centered differences of the actual action at step 5e-4 agree
within 5.32e-14. Independent inverse-time quadrature detects incorrect
Jacobian and anchor-time substitutions. These histories are intentionally
off shell: this verifies the derivation/implementation, not an MTS solution.

## 7. A derived boundary repair to attempt next

The retained P-squared boundary term yields a natural P_b=0 condition IF
endpoint P variations are independently free in a classical extension and
there is no extra parent P-boundary action. Its initial tangent then requires
P_t,b=0. The current first jets do not satisfy that extra classical condition:

| Projected endpoint P_t | MTS | Matched GR+scalar |
|---|---:|---:|
| Inner | 7.910001e-4 | 7.908565e-4 |
| Outer | -7.189199e-4 | -7.189266e-4 |

This is nearly the same issue in both branches. It does NOT invalidate the
finite initial C/Cdot tests: weak finite boundary covectors are coupled, and
this classical trace compatibility was not one of their certified gates.
It DOES prevent presenting those finite passes as a ready classical evolution.

The action gives a concrete candidate, not an unknown coefficient to hunt:

    (N_R/N)_b = kappa E_b/R_b + mu_b/(R_b^2 F_b).

The companion note constructs an exact global cubic lapse lift which preserves
both endpoint lapse values and supplies these derivatives. At N128 the MTS
required derivative changes are approximately (+6.4222e-5,-5.8976e-5).
The uniform lapse-change bound is only 4.56290e-6; subtracting it from the
original piecewise-linear minimum leaves about 0.81206005. GR is similar.
The corrected strong endpoint P-rate formula is zero to floating precision.

These are UNAPPLIED candidate profiles, saved separately from all tested
initial data. Their P1-plus-global-cubic representation must be retained
exactly; naive interpolation back to P1 loses the asserted derivative law.
They are not a full coupled repair: changing lapse changes P_t/J and memory
fluxes, and any changes to test spaces require their own constraint rows.

**Next bounded task:** put the derived endpoint lapse law into an explicitly
declared boundary/gauge representation on the small owned annulus; replay
every canonical, Gram, clock and physical-drive condition with matched GR.
Use the now-derived nonlinear history covectors for the next time jet and
boundary work. Only then decide whether a short coupled trajectory is
justified. Do not evolve the old jet, append a free source, or delete a trace
equation to make the problem appear closed.

## 8. Preserved implementation failures and provenance

The first N128 run computed both branches but failed when saving its first
array: a local NPZ archive variable shadowed the archive-writing function.
The corrected runner changes ONLY that variable name. The computed primary
outcomes are unchanged and the rerun saves all arrays. The failed attempt
is retained. This was an output-plumbing defect, not a theory failure.

The nonlinear first attempt failed only a poorly scaled boundary negative
control, described in the companion note. Its corrected version changes the
diagnostic's scale, not the histories, formulas or results. Both remain saved.

Paths relative to post-checkpoint-work:

- `DERIVATION-20260912-common-profile-refinement-and-inherited-knot-repair.md`
- `DERIVATION-20260912-nonlinear-history-Euler-equations.md`
- `scripts/annular_canonical_bounded_128_20260912.py`
- `scripts/derive_annular_bounded_128_20260912.py`
- `scripts/derive_annular_bounded_128_fixed_20260912.py`
- `scripts/verify_annular_bounded_128_20260912.py`
- `scripts/seal_annular_bounded_nonlinear_20260912.py`
- `source-intake/navier-stokes/20260912/annular-bounded-N128-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-bounded-N128-attempt02/status.json`
- `source-intake/navier-stokes/20260912/annular-bounded-N128-control-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-bounded-N128-control-attempt01/N128_metric_Gram_unapplied_lapse_boundary_candidate.npz`
- `source-intake/navier-stokes/20260912/annular-bounded-N128-control-attempt01/N128_GR_unapplied_lapse_boundary_candidate.npz`
- `source-intake/navier-stokes/20260912/annular-nonlinear-history-attempt02/status.json`

The combined integrity file and immutable resume snapshot are written by the
seal script after this note and CURRENT_LOCAL_RESUME are saved. The protected
workbench check is an mtime scan since 2026-09-12T10:13:59Z, not a pre-turn
content snapshot. No GitHub, galaxy-work or frozen-workbench edits are made.
