# Independent continuum GR evolution versus both annular regulators

2026-09-14. Private numerical continuation. No GitHub action or parameter fitting.
All times, radii and energies below use the existing PILOT normalization.

## 1. Outcome

A separate continuum Einstein–massless-scalar solver now provides a numerical
target for BOTH the nearest-neighbour reference and the MTS regulator.
It does not call the collar geometry engine, layer construction, discrete Gram
factors, or reference evolution operator.

Both regulator branches approach that independently computed target under the
tested 33 -> 65 -> 129 node refinement. This occurs for scalar, momentum,
gradient, radial mass, log lapse and full-support mass under the declared norms.
A second comparison at actual collar positions retains the convergence trend,
rather than relying only on common base-coordinate labels.

This is supporting numerical evidence for the restricted spherical GR-limit
argument, not a new mathematical proof, an observational fit, an unrestricted
parent theory pass, or a black-hole result.

Two intervals are deliberately distinguished:

- t=0.0002 is inside the preceding conservative comparison interval
  T<0.0008345769328864052.
- t=0.03 and 0.06 are longer numerical diagnostics. Success there does not
  extend the analytical time bound.

The source mass and midpoint clock remain present throughout. The compact pulse
has not reached the source over this interval, so this is not a demanding test
of an active wave–source collision or of long-time boundary stability.

## 2. Inputs and provenance

Read:

- `DERIVATION-20260914-layer-locking-and-restricted-evolving-GR-limit.md`
- `DERIVATION-20260914-reference-continuum-and-source-shell.md`
- `source-intake/navier-stokes/20260914/annular-reference-layer-locking-final-integrity.json`
- `scripts/annular_compatible_h_evolution_20260914.py`

The initial preparation is unchanged:

    x=(R-5.5)/0.3,
    b0=exp[1-1/(1-x^2)] for |x|<1, otherwise0,
    chi0=0.02 b0, u0=partial_R chi0, p0=0.004 R^2 b0.

The continuum domain is [5,6], inner geometric mass is0.8, kappa=0.1,
and the stationary reservoir is S=0.003. This calibration is an INPUT, not a
derived SI Newton constant. The continuum field is canonical in the previously
specified angular-reduced normalization.

Old regulator trajectories through t=0.06 are read unchanged from:

- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/GR_control_count33.npz`
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/GR_control_count65.npz`
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/GR_control_count129.npz`
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/metric_Gram_count33.npz`
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/metric_Gram_count65.npz`
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/metric_Gram_count129.npz`

The reference t=0.0002 states come from the preceding layer-locking runs.
Three matching MTS short runs were freshly computed. No old trajectory was
edited, relabelled, or refitted.

## 3. Independent continuum algorithm

New implementation: `scripts/annular_independent_continuum_20260914.py`.

It evolves chi, u=chi_R and p on uniform continuum grids with 513,1025,2049 nodes:

    chi_t = L p/R^2,
    u_t   = partial_R(L p/R^2),
    p_t   = partial_R(R^2 L u),
    e=(R^2 u^2+p^2/R^2)/2,
    F=1-2m/R, L=NU.

The first derivative uses a fourth-order centred stencil in the interior and
fourth-order five-point one-sided stencils at the first/last two nodes.
The boundary values u(5)=0 and p(6)=0 are held fixed; chi(6)=0 follows with
the imposed zero scalar velocity there.

The independent u variable is not silently assumed equal to the numerical
derivative of chi: that differential constraint is monitored. Its initial
fourth-order truncation residual is carried by this discretization and refines
from6.04e-6 to2.52e-8. This residual is NOT a new physical degree of freedom.

### 3.1 A different radial constraint implementation

Rather than the regulator's collar-by-collar collocation, the source-free bulk
mass equation is integrated through its scalar integrating factor:

    I(R)=integral_5^R 2 kappa e(s)/s ds,
    m(R)=exp[-I(R)] [0.8+integral_5^R kappa e(s) exp[I(s)] ds].

The primitives use cumulative Simpson quadrature. The lapse is reconstructed
from the density-cancelled identity

    partial_R log L = 2m/(R^2 F).

At the source,

    Uminus=sqrt(1-2m(6)/6),
    Uplus=Uminus-kappa S/6,
    Nshell=(Uminus+Uplus)/2,
    L(6-)=Nshell Uminus,
    mplus=m(6)+kappa S Uminus-(kappa S)^2/12.

Thus log L is integrated backwards from the correct shell value, and
log N=log L-(1/2)log F. The source is not deleted, and Nshell is not set
equal to Uplus by convenience.

All geometry is recomputed at every time step from the evolving fields.
The main time integrator is DOP853 with a resolution-scaled maximum step.
A separate RK4 calculation checks the short-time evolution.

This solver is algorithmically separate, not written by an independent
research group. A refinement test is not a formal stability proof for its
one-sided boundary stencil under an arbitrary future source interaction.

## 4. Validate the target before comparing theories

Main target run:59 checks pass. Independent verifier:16 checks pass.

### 4.1 Spatial and temporal checks

Across 513 -> 1025 -> 2049 nodes:

- the derivative is exact within floating-point tolerance on degree0..4
  polynomials, including boundary rows;
- scalar-gradient, radial mass, radial lapse and mass-time residuals show the
  tested fourth-order refinement range;
- the minimum F is0.68, safely inside this regular pilot chart;
- scalar boundary values and the midpoint-clock identity pass;
- full-support mass drift is1.17e-11,5.55e-16,1.11e-16 respectively.

Those tiny conserved-mass drifts do NOT mean the whole solution is accurate
to machine precision. In particular, the 1025-versus-2049 maximum differences
over the sampled times are approximately

    chi:8.27e-9, u:3.88e-6, p:1.32e-4,
    m:5.31e-10, log N:1.30e-10.

The field quantities have different normalizations; the comparator measures
target refinement in the SAME norms used for regulator errors.

At2049 nodes, the maximum sampled mass-time residual

    |m_t-kappa F L p u|

is7.84e-10. The scalar-gradient residual is2.53e-8.

### 4.2 Independent radial and negative controls

A fresh adaptive radial IVP is run on the evolved t=0.06 fields, using cubic
interpolation of u,p and the ORIGINAL log-N constraint rather than the
density-cancelled log-L implementation. It agrees to

    max mass difference1.56e-12,
    max log-lapse difference5.39e-13.

Short-time RK4 versus the main continuum evolution differs by2.51e-14 in the
maximum compared state component.

Controls deliberately broken at the same state are detected:

| wrong operation | resolved discrepancy |
|---|---:|
| use outer-shell clock instead of midpoint clock | log lapse2.92238e-5 |
| delete the source reservoir | full mass2.56644e-4 |
| reverse the mass-energy-flux sign | mass-time residual1.79061e-2 |

A vacuum scalar state also retains constant mass, the analytically normalized
Schwarzschild lapse on the annulus, and zero scalar evolution.

There is no time-dependent fit or extra tuning to make these checks pass.

## 5. Same comparator and acceptance criteria for both branches

The main comparison uses common base-node labels R_i, exactly as in the
preceding convergence argument. Define

    Eerr=(1/2) integral W(z) [
        sum_i omega_i (p_h(z,i)-p_cont(R_i))^2/R_i^2
        +sum_edges h Rmid_i^2 (Dchi_h(z,i)-u_cont(Rmid_i))^2 ] dz.

Scalar L2 is measured separately. This norm retains internal-layer spread; it
does not only compare the layer mean.

The mass and log lapse are compared at193 identical PHYSICAL radii in[5,5.95].
The source midpoint, where finite-width mass is not the exterior mass, is not
misused as the exterior comparison point. Full-support mass is checked
separately against the thin-shell exterior mass.

All regulator base nodes and edge midpoints are nested in the continuum grids.
No interpolant is needed for those primary field targets; cubic interpolation
is used for the fixed metric probes.

The 1025-versus-2049 target differences must be below2% of the corresponding
regulator discrepancy in each component norm, with a small numerical floor.
These are empirical refinement estimates, not rigorous error bounds.
The same acceptance gate is applied to reference and MTS.

### 5.1 Main results at t=0.06

| nodes | reference Eerr | MTS Eerr | reference max mass error | MTS max mass error |
|---:|---:|---:|---:|---:|
| 33 | 5.50219e-4 | 4.29151e-4 | 2.22219e-4 | 1.66435e-4 |
| 65 | 1.26998e-4 | 6.93850e-5 | 6.58892e-5 | 5.97912e-5 |
| 129 | 2.20428e-5 | 1.56958e-5 | 3.40318e-5 | 3.37705e-5 |

The129-node log-lapse errors are9.50511e-6 (reference) and9.22163e-6 (MTS).
MTS extra-Gram energy at t=0.06 decreases from3.22360e-4 to5.17464e-6.

All207 main comparison checks pass, including both branches at t=0,.0002,.03,.06.
The node-refinement results are finite-grid observations, not an inferred
universal asymptotic order from only two resolution ratios.

## 6. Coordinate-alignment cross-check

Common base labels differ from actual layer positions by(h/2)z.
This alone contributes some finite-h field error, even at the common smooth
initial preparation. It should not be hidden.

A second comparator therefore evaluates the continuum fields at the ACTUAL
positions of each layer's nodes and edge midpoints. Scalar/momentum are sampled
only at strictly interior nodes; all edge midpoints are inside the domain.
There is no exterior extrapolation, no fit, and no relocation of regulator data.

Its normalization and sampled set differ from the primary norm, so the two
tables should not be combined as though they measure the identical quantity.

At t=0.06:

| nodes | reference physical-position Eerr | MTS physical-position Eerr |
|---:|---:|---:|
| 33 | 3.68300e-4 | 1.85341e-4 |
| 65 | 7.55376e-5 | 1.51173e-5 |
| 129 | 8.53461e-6 | 2.08223e-6 |

The same refinement trend holds at t=0.03. All40 cross-checks pass.
The largest target-refinement difference in the physical-position momentum
and gradient component norms is approximately0.235% of the corresponding
regulator error, below the common2% acceptance gate.

This supports the convergence interpretation beyond a base-coordinate
bookkeeping effect.

## 7. What the smaller MTS errors mean—and do not mean

MTS is closer than the nearest-neighbour reference in several finite-grid
diagnostics here, including both displayed combined-energy comparisons.
That is a useful numerical result and should not be erased.

It is NOT evidence that MTS physically outperforms GR: GR is the target
solution, and the competitors in these plots are two discrete approximations.
Modified dispersion and cancellation of finite-grid error can improve one
approximation without establishing new fundamental physics.

The result supports the previously derived restricted annular limit.
It does not derive all parent couplings, the source's material action,
arbitrary-matter gravity, the complete Newtonian limit, horizons, or black-hole
regularity. No observational dataset or public claim is introduced.

## 8. Figure and evidence

Figure: `source-intake/navier-stokes/20260914/annular-continuum-comparison-figure-attempt02/continuum-comparison.png`

The SVG, exact plotted rows and source hashes are retained with the figure.
It was visually inspected at its native exported size: labels, legends, marks,
time qualification and footnotes are readable without clipping or overlap.
Line style and marker shape distinguish branches in addition to colour.
No claim is made of responsive-layout testing or a colour-vision simulation.

New calculation and validation code:

- `scripts/annular_independent_continuum_20260914.py`
- `scripts/run_annular_independent_continuum_20260914.py`
- `scripts/compare_annular_regulators_to_continuum_20260914.py`
- `scripts/verify_annular_independent_continuum_20260914.py`
- `scripts/check_annular_continuum_physical_sampling_20260914.py`
- `scripts/plot_annular_continuum_comparison_v2_20260914.py`

Evidence:

- `source-intake/navier-stokes/20260914/annular-independent-continuum-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-continuum-regulator-comparison-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-independent-continuum-verification-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-continuum-physical-sampling-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-continuum-comparison-figure-attempt02/status.json`

First figure attempt preserved:
`source-intake/navier-stokes/20260914/annular-continuum-comparison-figure-attempt01/status.json`
and `scripts/plot_annular_continuum_comparison_20260914.py`.
It failed because the optional plotting package was absent, not because a
physics test failed. The replacement uses native SVG and the bundled Sharp
renderer; no packages or shared environments were changed.

Final seal:
`scripts/seal_annular_independent_continuum_20260914.py`.
The original workbench remains untouched. All owned numerical jobs have ended.

## 9. Next substantive step

Test a genuine wave–source interaction rather than another quiet-boundary
interval. First validate the continuum boundary treatment with an appropriate
reflection/energy-balance control, then compare both regulators during the
interaction while monitoring source work and the required surface stress.

The longer numerical test and a derivation of the source-support action remain
distinct tasks. Neither should be declared solved merely because this quiet,
regular annular continuum comparison succeeds.

