# 122 - Early-Late Omega Map Theorem Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 121 sharpened the joint late+CMB problem:

```text
the failed gate is not an alpha/r_d calibration failure at fixed shape.
```

The live problem is:

```text
CMB-compatible Omega_m0 is higher than the late SN+BAO preferred Omega_m0,
and that shift creates BAO-shape penalty.
```

So this checkpoint asks:

```text
Can MTS derive a lawful early-to-late Omega_m0 map?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\early_late_Omega_map_theorem_attempt.py
```

Run:

```text
research-programme\runs\20260531-172300-early-late-Omega-map-theorem-attempt
```

Generated:

```text
source_register.csv
candidate_values.csv
map_target_rows.csv
aggregate_map_diagnostics.csv
candidate_map_audit.csv
theorem_route_audit.csv
decision.csv
status.json
```

Status:

```text
Omega_map_theorem_rejected_under_current_assumptions
```

Claim ceiling:

```text
internal_theorem_attempt_not_public_evidence
```

## 3. Locked Constants

The tempting number is:

```text
DeltaR = 2/9
B_mem = 2/27
B_mem * DeltaR = 4/243 = 0.016460905349794237
```

Since:

```text
B_mem = DeltaR/3,
```

this is also:

```text
DeltaR^2 / 3.
```

That matters because the joint late+CMB rows need an average shift:

```text
0.01647749874764233,
```

which is almost exactly:

```text
B_mem * DeltaR.
```

This is interesting. It is not enough.

## 4. Map Diagnostics

The late-only locked T7 target remains:

```text
Omega_m0_late = 0.3032827426766658.
```

Aggregate diagnostics:

| Quantity | Value | Readout |
|---|---:|---|
| joint mean shift needed | `0.01647749874764233` | mean joint compromise shift relative to late-only T7 |
| joint mean beta in `shift = beta B_mem` | `0.22244623309317146` | nearly `DeltaR = 0.222222...` |
| joint beta spread | `0.11099837779064542` | branch dependence across the four gates |
| mean residual after `B_mem DeltaR` map | `1.659339784811087e-05` | very good centering |
| worst joint residual after `B_mem DeltaR` map | `0.004301287036071966` | not exact |
| CMB-only beta to T7 | `0.3664931527623321` | much larger than `DeltaR` |
| best CMB-only residual after `B_mem DeltaR` map | `0.009830345482600256` | not repaired |
| CMB locked-vs-zero response beta | `0.20617358130050434` | compressed-prior response to `B_mem` |

Readout:

```text
B_mem * DeltaR is an excellent center for the joint compromise rows,
but it does not map the CMB-only locked solution onto the late-only solution.
```

Boxing-score version:

```text
This is a lovely counterpunch, not a knockout. It lands clean on the joint
scorecard, but it does not explain the whole exchange.
```

## 5. Row-Level Target

The four joint rows:

| Prior | Mode | `Omega_source` | shift needed | beta | residual after `B_mem DeltaR` |
|---|---|---:|---:|---:|---:|
| `wCDM` | `strict_full4` | `0.32240555317663316` | `0.01912281049996739` | `0.2581579417495598` | `+0.0026619051501731716` |
| `wCDM` | `marginal_R_lA` | `0.31582283300396563` | `0.012540090327299858` | `0.16929121941854808` | `-0.003920815022494362` |
| `LCDM` | `strict_full4` | `0.32404493506253196` | `0.020762192385866185` | `0.2802895972091935` | `+0.004301287036071966` |
| `LCDM` | `marginal_R_lA` | `0.31676764445410166` | `0.013484901777435887` | `0.18204617399538447` | `-0.0029760035723583322` |

This says:

```text
The B_mem DeltaR map is numerically coherent as a joint-fit centering rule.
```

But the beta values are branch-dependent:

```text
0.169 <= beta <= 0.280.
```

So an exact theorem:

```text
Omega_m0_late = Omega_m0_source - B_mem DeltaR
```

is not proven by these rows.

## 6. CMB-Only Transfer Check

The CMB-only locked rows need more than `B_mem DeltaR` to reach T7:

| Prior | Mode | CMB-only locked `Omega_m0` | residual after `B_mem DeltaR` map |
|---|---|---:|---:|
| `wCDM` | `strict_full4` | `0.3295740146787432` | `0.009830366652283207` |
| `wCDM` | `marginal_R_lA` | `0.32957399350906025` | `0.009830345482600256` |
| `LCDM` | `strict_full4` | `0.331286732138333` | `0.011543084111872992` |
| `LCDM` | `marginal_R_lA` | `0.3312867941619584` | `0.011543146135498394` |

Therefore:

```text
B_mem DeltaR is not a full CMB-to-late transfer theorem.
```

The CMB-only locked-vs-zero response is:

```text
beta_CMB ~= 0.20617,
```

which is close-ish to `DeltaR`, but not exact and not a field equation.

## 7. Theorem Attempt

Assume a standard single-metric parent action with minimally coupled dust:

```text
S = integral sqrt(-g) [R/(2 kappa) + L_matter + L_memory + ...].
```

Diffeomorphism invariance gives:

```text
nabla_mu (T_matter^{mu nu} + T_memory^{mu nu}) = 0.
```

If ordinary matter is separately conserved:

```text
nabla_mu T_matter^{mu nu} = 0,
```

then in FLRW:

```text
dot rho_m + 3 H rho_m = 0
```

and therefore:

```text
rho_m(a) = rho_m0 a^-3.
```

That means:

```text
Omega_m0^early = Omega_m0^late.
```

So under the clean conservative assumptions, the only derived map is:

```text
identity.
```

But the identity map fails the empirical target.

To get a nontrivial map, the parent action must provide an exchange current:

```text
nabla_mu T_matter^{mu nu} = Q^nu
nabla_mu T_memory^{mu nu} = -Q^nu.
```

In FLRW this becomes:

```text
dot rho_m + 3 H rho_m = Q^0.
```

The needed integrated effect is roughly:

```text
Delta Omega_m0 ~= 0.0165
```

for the joint compromise, and up to:

```text
Delta Omega_m0 ~= 0.0208
```

for the failing strict-LCDM joint row.

No such `Q^nu` has been derived.

And introducing one is not harmless. It must satisfy:

```text
total Bianchi conservation,
local-GR/PPN screening,
no hidden fitted amplitude,
identity limit when B_mem -> 0.
```

Therefore the nontrivial map is rejected under current assumptions.

## 8. Candidate Audit

| Candidate | Verdict | Reason |
|---|---|---|
| identity map | conservative theory default | follows from separately conserved dust, but fails the empirical target |
| `B_mem DeltaR` map | useful closure coincidence | centers joint rows but fails CMB-only transfer and is branch dependent |
| compressed-prior response map | diagnostic only | beta is a likelihood-response coefficient, not a covariant field equation |
| interacting memory-matter map | not allowed yet | would need derived `Q^nu` and local screening |
| BAO shape correction | possible future route | targets the real residual but needs acoustic/perturbation derivation |

## 9. Decision

Allowed statement:

```text
The relation B_mem DeltaR = 4/243 almost exactly centers the four joint
late+CMB compromise rows.
```

Allowed statement:

```text
Under the current conservative field-theory assumptions, a nontrivial
early-to-late Omega_m0 map is not derived.
```

Allowed statement:

```text
The joint compressed-CMB bridge remains closure-only unless MTS derives either
a matter-memory exchange current Q^nu or a memory-sector BAO/acoustic-shape
correction.
```

Forbidden statement:

```text
MTS predicts the early-to-late Omega_m0 map.
```

Forbidden statement:

```text
MTS passes joint late+CMB cosmology.
```

Current status:

```text
CMB compressed-prior bridge demoted to empirical closure, not promoted theory.
```

This is not a disaster. It is a useful narrowing:

```text
late SN+BAO locked 2/27 remains alive;
BAO-only remains alive;
compressed CMB distance is not a knockout either way;
the missing piece is now specifically a CMB/BAO-shape or Q^nu derivation.
```

## 10. Next Target

Next checkpoint:

```text
123-CMB-bridge-demotion-and-next-test-route.md
```

Task:

```text
Stop treating compressed CMB background priors as promotion evidence.
Decide the next fair empirical route:

1. full CMB perturbation/acoustic contract,
2. BAO-shape residual decomposition,
3. growth/H(z) non-CMB stress test,
4. or local-GR/PPN derivation work.
```

Recommendation:

```text
Do 123 as a routing gate, then run a BAO-shape residual decomposition before
spending tokens on a full CMB perturbation machine.
```

