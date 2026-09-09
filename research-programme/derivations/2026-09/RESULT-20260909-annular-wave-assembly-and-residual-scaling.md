# Explicit annular wave fields and matched residual-scaling tests

2026-09-09 BST. Private work; no GitHub action.

## Result

The transport quadratures have been evaluated, the reference and coupled
fields assembled, and their remaining equations evaluated numerically at
finite wavelengths. This is no longer only a register of formally cancelling
coefficients. Both branches show the predicted residual orders in two
specified test cases. Removing the third-order scalar coefficients degrades
both branches by one asymptotic order, as it should.

Actual completed runs:

- Assembly: **49/49 exact symbolic checks**, completed
  `2026-09-09T00:15:15.630321+00:00`.
- Numerical evaluation: **30/30 checks**, completed
  `2026-09-09T00:20:08.207542+00:00`.

This is a finite-annulus consistency test of the retained spherical action.
It is not an empirical comparison, a full numerical evolution, a proof of
well-posedness, a uniform error bound, or regularity of a black-hole centre.

## 1. Sources and implementation

Preserved theoretical owners:

- `DERIVATION-20260909-next-averaged-mass-evolution.md` and its completed
  `source-intake/navier-stokes/20260909/next-mean-evolution-final/` run:
  the six scalar transport forcings and the forced c2 evolution law.
- `DERIVATION-20260909-wave-energy-flux-and-mean-mass.md` and
  `source-intake/navier-stokes/20260909/wave-energy-flux-staged-series/`:
  exact improved constraints, P2 and restoration of the physical K20 term.

New companions:

- `scripts/annular_wave_assembly_20260909.py`: integrates the coefficient
  equations, reconstructs the physical fields, and exports two exact cases.
- `scripts/annular_wave_residuals_20260909.py`: evaluates the unexpanded
  retained equations using derivative jets, with the same tests for both
  reference and coupled response.

No older source, stellar/D4 result, galaxy work, or public repository is
changed. Both jobs ran serially, on one logical CPU at BelowNormal priority.

## 2. What has now been assembled

The explicit field exports contain

```text
chi_ref=epsilon a+epsilon^2 b+epsilon^3 c,
chi=chi_ref+u[epsilon a_X+epsilon^2 b_X+epsilon^3 c_X]+O(u^2),

mu_ref=mu0+epsilon mu1+epsilon^2 mu2,
mu=mu_ref+u[M0+epsilon M1+epsilon^2 M2]+O(u^2),

delta_ref=epsilon^2 d2+epsilon^3 d3,
delta=delta_ref+u[epsilon d1_X+epsilon^2 ell2]+O(u^2).
```

The C1,C3,C5 and E1,E3,E5 scalar quadratures are integrated explicitly with
zero extra boundary harmonics. The primitive routine handles finite Laurent
polynomials, including logarithms when an r^-1 term occurs; it does not
silently invoke an unspecified closure. Every primitive is differentiated
back to its sourced forcing and checked at the reference boundary.

The ordinary d3 and coupled ell2 radial lapse equations are integrated as
well. The ordinary order-epsilon-squared mean mass is not left frozen while
the coupled mean evolves. Its rate is derived from the ordinary flux under
the same boundary preparation, as described in section 3.

To restore the complete physical M2, rather than only its mean, the assembly
also computes the next curvature multiplier:

```text
J/u=epsilon j1+epsilon^2 j2+epsilon^3 j3+...,
j3=-(2/3)r^2[X3 U0+X2 U1+X1 U2].
```

X3 uses the now-integrated ordinary scalar coefficients. U2 includes the
ordinary second-order mass and matter terms. Expanding the exact boundary
term K then gives K2, including its previously unknown oscillatory part.
The physical response is M2=N2+kappa K2. Its mean reproduces the preceding
K20 expression exactly; no curvature contribution is removed from the
physical mass by changing bookkeeping variables.

The exported Fourier coefficients are real functions of slow v and r only.
All Fourier reconstructions pass, with no unresolved source functions.

## 3. The ordinary baseline receives its own mean-evolution law

Use kappa=4pi G and a fixed reference radius R. Define

```text
f=1-2mu0/R-Lambda R^2/3,
Veff=m_chi^2+2mu0/R^3-2Lambda/3,

Q0(r)=A^2[-1/r+mu0/r^2+(m_chi^2-Lambda/3)r]/4
      -b2 A^4/(6r^3).
```

Write the ordinary mean coefficient as

```text
<mu2(v,r)>=q(v)+kappa[Q0(v,r)-Q0(v,R)].
```

For the same zero additional boundary scalar harmonic and ordinary lapse
normalization, direct flux extraction gives

```text
q'/kappa = (A')^2/2-f A A'/(2R)-f A^2 Veff/4
           +kappa A^4/(8R^2)

           +b2[3A^3 A'/R^3-2f A^4/R^4+(3/2)A^4 Veff/R^2]
           +A^6[(14/3)b2^2-(3/2)b3]/R^6.
```

This formula is checked against the direct ordinary temporal flux before
specializing the profiles. q(0)=c2(0)=0 selects matched higher-order initial
mean offsets. Both rates are then integrated, rather than evolving only
the MTS correction while imposing an artificially static reference mean.

## 4. Two explicit, non-fitted test cases

All numbers below are dimensionless after choosing a fiducial length unit.
They are test inputs, not parent-derived constants or observational fits.

Shared inputs:

```text
kappa=0.1, R=4, mu0(0)=1,
mu0'=kappa A^2/2,
0<=v<=0.5, 4<=r<=8,
epsilon=0.4, 0.2, 0.1, 0.05, 0.025.
```

| Case | A(v) | Lambda | m_chi | b2 | b3 |
| --- | --- | --- | --- | --- | --- |
| Canonical | 0.1 | 0 | 0 | 0 | 0 |
| Nonlinear, modulated | 0.1(1+v/10) | 0.001 | 0.2 | 0.05 | 0.02 |

The reference is u=0 with the same scalar matter. In the canonical case it
is GR with a canonical scalar. In the nonlinear case it is GR with the
retained nonlinear scalar matter, not vacuum GR or LambdaCDM. The coupled
column is the exact first-order-u coefficient, not a finite-u total residual.
No empirical coupling value is inferred by comparing those columns.

The test samples three slow times, five radii, and 32 phases independently
of wavelength. A 64-phase refinement is performed at the finest wavelength.
The physical time derivative still includes epsilon^-1 partial_theta.
Independent phase sampling prevents an accidental favourable alignment of
v/epsilon from being mistaken for convergence.

The sampled reference F stays positive, around 0.49 or greater on these
cases. This is an exterior annulus, not a test through the horizon or centre.

## 5. Numerical method and actual measured orders

The evaluator uses Taylor coefficients through total fourth order in
physical v and r, together with an exact nilpotent first-order-u variable.
Its 30 derivative coefficients are checked against independent symbolic
derivatives of an analytic exponential/logarithmic test expression.
No finite-difference step in u is used. The retained equations are evaluated
without truncating their epsilon dependence before measuring the residual.

The scalar equation and the temporal-mass, radial-mass and radial-lapse
constraints are evaluated directly. The mass constraints use the exact
improved identity while retaining the physical mass fields and all K terms.
An independent angular metric equation and a full initial-boundary-value
evolution are not added to the acceptance claim here.

For a residual proportional to epsilon^p, halving epsilon should reduce it
by about 2^p. Slopes below use the finest three sampled wavelengths.

| Residual | Canonical reference | Canonical coupled | Nonlinear reference | Nonlinear coupled |
| --- | ---: | ---: | ---: | ---: |
| Scalar | 3.00 | 3.00 | 3.00 | 3.00 |
| Temporal mass, unaveraged | 2.00 | 2.00 | 2.00 | 2.00 |
| Radial mass | 3.01 | 3.00 | 3.00 | 3.00 |
| Radial lapse | 4.00 | 3.11 | 4.00 | 3.01 |
| Phase-mean temporal mass | 4.00 | 4.00 | 4.00 | 4.00 |

The different predicted orders reflect the actual assembled truncations and
fast derivatives. They are not relaxed thresholds invented after a failure.
The unaveraged temporal mass residual still starts at epsilon squared:
its next oscillatory mass coefficient has not been inserted. The mean law
does not eliminate that oscillatory remainder. The phase-mean gate requires
at least third order; the observed fourth order is a sampled result, not a
new exact theorem, particularly as the finest mean residuals approach small
floating-point cancellation levels.

Doubling the phase samples changes the recorded maximum residuals by less
than 1.2% in these runs. This does not certify a supremum over the continuum.

## 6. Deliberately remove the new scalar terms

As a negative control, remove every epsilon-cubed scalar coefficient while
holding the assembled geometry fixed. Apply this identical operation to
both branches and examine the scalar residual only.

| Case and branch | Omission slope | Improvement from restoring terms at epsilon=0.025 |
| --- | ---: | ---: |
| Canonical reference | 2.00 | 638 times |
| Canonical coupled | 2.00 | 158 times |
| Nonlinear reference | 2.00 | 266 times |
| Nonlinear coupled | 2.00 | 721 times |

These factors compare each approximation with its own omitted-term control.
They do not mean MTS fits physical data hundreds of times better than GR.
The useful result is that the derived terms demonstrably improve the
equations by one order in both branches, rather than simply changing labels.

## 7. Artifacts and verified provenance

Assembly directory:
`source-intake/navier-stokes/20260909/annular-assembly-initial/`.
It contains `canonical.json`, `nonlinear_modulated.json`, status, the executed
source and COMPLETE. Its script SHA-256 is
`4ef1ab575c875bf79d7107b57fbbe5f66c5a135a69d31758f4a90db63ae13e7e`.

Residual directory:
`source-intake/navier-stokes/20260909/annular-residuals-initial/`.
It contains the complete wavelength rows, slopes, controls, status, executed
source and COMPLETE. Its script SHA-256 is
`187ed2819448a9116260b669bebe5cd446da4153e7da7efabc293d8edf38038c`.

The exact run status and snapshots are authoritative. Both retain
`valid_for_physics_claim=false`. The assembly takes about 26 seconds and the
numerical job about 5 seconds on the limited worker in this run; these are
not heavy evolution jobs. No background computation is needed to retain the
result.

Post-run verification confirms matching live/snapshot script hashes, all
owner and case hashes, both COMPLETE timestamps, 44 residual/control rows
and 20 measured slopes. Both sources compile in memory. No scripts/__pycache__
or live worker from this continuation remains.

## 8. What this changes, and the next finite target

We now have explicit field approximations, their independently evaluated
residuals, and matched ordinary/coupled controls. This supports the internal
consistency of this finite-order exterior branch. It does not by itself
bound the distance to an exact solution or establish a viable full MTS theory.

The leading remaining unaveraged time-constraint error is identified, not
hidden by averaging: it requires the next oscillatory mass transport term.
The next finite target is to integrate that forcing and account for the
angular constraint at the corresponding order, then repeat the same tests.
After that, a residual-to-solution stability estimate or controlled evolution
is needed before calling this a controlled solution. Horizon and central
regularity require separate work within a justified derivative regime.
