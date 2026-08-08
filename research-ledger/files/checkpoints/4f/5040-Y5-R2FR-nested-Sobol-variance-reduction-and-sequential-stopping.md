# 5040 - nested Sobol variance reduction and sequential stopping

**Status: COMPLETE AFTER RESTRICTED-SCOPE REPAIR; the matrix is numerically complete, but the production-precision gate remains open.**

## Scope-repair notice

Checkpoint 5045 found that the fourth-scramble continuation had applied the
5041 theorem beyond the two independently witnessed `direct:g1` families. The
original eight third-scramble repairs remain valid. Checkpoints 5047 and 5048
recomputed all 45 fourth-scramble jobs under the restricted guard, with zero
theorem substitutions and 684 stable numerical residue evaluations. All 378
live jobs now converge under that corrected contract.

## Why simply adding scrambles is not enough

Checkpoint 5039 established non-exclusion, not agreement. The fixed 5018
`hhh` target is the signed half of the known nonlocal residual. Its inherited
componentwise uncertainty is therefore

```text
tau_j = known_master_error_j / 2.
```

The five resulting equivalence margins are approximately
`(0.264,0.0365,0.310,0.0490,0.264)`. Giving half of each margin to statistical
uncertainty makes the current one-point outer variance require normal-planning
counts

```text
(9,582,816; 32,208,461; 2,305,997; 25,011,199; 2,717,914).
```

These are planning values rather than stopping guarantees, but they decisively
reject brute one-point sampling as the primary route. The calculation now tests
variance reduction instead of spending millions of kernels to reproduce the
same noisy estimator.

## Equal-cost design

Both candidate arms cost four new outer event points:

1. add four independent one-point scrambles, giving `n=8,m=1`;
2. add the second nested Sobol point to each existing Owen scramble, giving
   `n=4,m=2`.

At 95% confidence their estimated halfwidths are

```text
H_ind = t_7 s_1 / sqrt(8),
H_nest = t_3 s_2 / sqrt(4).
```

Thus the nested arm beats the independent arm only if

```text
s_2 / s_1 < (t_7/t_3) sqrt(4/8) = 0.5253951466.
```

The pilot selects the arm with the smaller worst component value of
`H_j/tau_j`; it does not assume randomized-QMC improvement in advance. The
nested arm is calculated first because it determines whether the integrand is
smooth enough for base-2 stratification to beat merely doubling the number of
independent point estimates.

## Regulator-bias contract

For an expansion `R(e)=R_0+a e+b e^2+...`, define

```text
Q = [R(0.02)-R(0.04)] - 0.5[R(0.04)-R(0.08)].
```

Then `Q=0.0012 b+O(e^3)`, while the linear Richardson error in
`2R(0.02)-R(0.04)` is `-0.0008 b+O(e^3)`, hence its leading bias is
`-(2/3)Q`. A target component passes only if

```text
|mean residual| + 95% statistical halfwidth
                    + (2/3) upper defect bound <= tau_j.
```

The same bound is applied to the imaginary part. Contraction requires the upper
95% bound of `|step_2|-|step_1|` to be negative for every component. Reflection
is measured against the propagated odd target and is never imposed.

## Current calculation

The immutable power-1 run contains `378` jobs:

```text
exact sample-0 imports       = 189
new sample-1 jobs required   = 189
current sample-1 primary     = 180/180 converged
current sample-1 audit       =  9/9
terminal                     = 378/378
failed / unconverged         = 0 / 0
production-clean scrambles   = 4/4
```

The complete `S503401_N0001` primary vector passes its independent 32-order
central audit at all three epsilon values. The maximum primary/audit relative
difference is `1.54e-14`. No topology repair, endpoint substitution or target
fit was required for those 54 kernels. `S503402_N0001` also closes all 45
primary rows directly. After the exact cross-source repair, `S503403_N0001`
closes all 45 rows; theorem-guarded continuation then closes all 45
`S503404_N0001` rows.

## Third-scramble cross-source residue closure

`S503403_N0001` initially closed 37 of 45 primary rows. Each of the eight
remaining rows had exactly one required collision between a causally owned
`direct:g1` pole and an unowned `subtraction:decay` pole. There are no topology
failures and every adaptive chamber integral converges. The affected arguments
are `A00`, `A13`, and `A14` across the three epsilon levels.

Checkpoint 5041 resolves this obstruction analytically. The finite-plus
integrand is an additive sum of direct and subtraction components. On the local
global contour following the owned direct pole, the subtraction component is
holomorphic and has zero contour integral. The direct residue is holomorphic at
the relative collision because the only coincident second pole belongs to the
other additive component. Since the collision has nonzero relative and global
coordinates, the outer `dq/q` and inner `dz/z` measures add no pole. The nested
cross-source residue is therefore exactly zero in the causal order used by the
runner; it is not set to zero from a tolerance.

Independent 70-digit, 16-by-16 Cauchy evaluations cover both
`plus_v/plus_u` and `minus_v/minus_u`. Halving the relative radius suppresses
the finite-node remainder by `65536=2^16`, from approximately `1.24e-19` to
`1.89e-24`, exactly as expected for an analytic integrand sampled with 16
trapezoid nodes. All eight kernels were recomputed from backed-up originals and
now converge with theorem certificates. The former 372 fourth-scramble
certificates are quarantined as overbroad. Their 45 jobs were independently
recomputed under the restricted guard and contain no exact theorem zeros. The
live matrix contains no failed or unconverged job.

With all four production-clean scrambles included, the nested/sample-0
standard-deviation
ratios are

```text
(0.935, 0.657, 0.632, 0.759, 0.673).
```

No component is below the predeclared `0.525395` threshold, and nested 95%
halfwidths divided by the equal-cost eight-independent-point estimates are
`(1.780,1.251,1.203,1.445,1.281)`. Nested sampling wins no component. The
predeclared worst-component rule therefore returns
`SWITCH_TO_ADDITIONAL_INDEPENDENT_SCRAMBLES`; this verdict was not selected
before the fourth replicate.

## Completed design decision and boundary

The 378-job matrix is complete, but none of the strict sequential stopping
claims closes. Target equivalence fails 5/5 components, imaginary-zero
equivalence fails 5/5, and contraction is supported for only 3/5. The selected
independent route is less inefficient than another nested point at equal cost,
but the raw strict planning scale remains prohibitive; the next stage must not
confuse a design choice with attained precision.

- no fixed-target match or exclusion is made;
- no epsilon-zero limit is claimed;
- no production `hhh`, local-GR, Newton, Maxwell or full-MTS claim is made;
- the exact cross-source zero is a numerical-subproblem result only and does not
  by itself establish a production `hhh` or MTS physics claim.

The next calculation should first derive an unbiased independent-scramble
control variate or stratification from the known endpoint/soft structure, then
run a small independent pilot against the completed matrix. Brute-force millions
of one-point scrambles are not authorized by this checkpoint.

Marker: `MTS_5040_NESTED_SOBOL_VARIANCE_REDUCTION`.

Resolution marker: `MTS_5041_CROSS_SOURCE_ADDITIVE_ZERO_REPAIR`.

Completion marker: `MTS_5041_THEOREM_GUARDED_5040_RESUME`.
