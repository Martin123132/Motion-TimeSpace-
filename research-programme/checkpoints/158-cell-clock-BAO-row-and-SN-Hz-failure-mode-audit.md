# 158 - Cell-Clock BAO Row And SN/H(z) Failure-Mode Audit

Private failure-mode checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 157 found a mixed result:

```text
the fixed cell-clock map improves BAO relative to LCDM,
but it spends too much SN chi2;
H(z) is not the failure driver.
```

The next question is:

```text
is the projection route dead,
or is the universal/global SN clock coupling the bad assumption?
```

Short answer:

```text
global clock coupling is demoted;
ruler-only BAO projection remains live as a theorem target;
no bridge promotion is allowed.
```

This is an important distinction. The clock punch was too exposed on SN. The ruler/projection footwork is not yet dead.

## 2. Machine Artifact

Script:

```text
scripts/cell_clock_failure_mode_audit.py
```

Run:

```text
runs/20260531-235959-cell-clock-failure-mode-audit
```

Generated:

```text
source_register.csv
chi2_decomposition.csv
bao_row_delta_contributions.csv
bao_observable_summary.csv
sn_policy_sensitivity.csv
hz_pressure_summary.csv
ruler_only_projection_scores.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
global_clock_demoted_ruler_projection_route_remains_live
```

Claim ceiling:

```text
cell_clock_failure_mode_audit_no_bridge_promotion
```

## 3. Chi2 Decomposition

Primary observed-redshift SN convention:

| comparison | Δχ² SN | Δχ² BAO | Δχ² total | dominant pressure |
|---|---:|---:|---:|---|
| clock u3fit vs LCDM | 3.9022881824178057 | -1.775550459705185 | 2.1267377227127326 | SN |
| clock u3quarter vs LCDM | 3.01730457282315 | -1.9215936658404544 | 1.095710906982731 | SN |
| clock u3fit vs no-clock u3fit | 6.272527029391767 | 0.9557024644384935 | 7.228229493830213 | SN |
| clock u3quarter vs no-clock u3quarter | 5.503106382193664 | 0.8465455779075466 | 6.349651960101255 | SN |
| no-clock u3quarter vs LCDM | -2.485801809370514 | -2.768139243748001 | -5.253941053118524 | BAO |

Interpretation:

```text
the late-time no-clock 2/27 branch is still the better empirical branch;
the global clock map is not losing because BAO fails;
it is losing because SN dislikes the global redshift remap.
```

That narrows the failure. It is not “MTS cosmology collapsed.” It is:

```text
do not globally couple this clock map to SN without a stronger theorem.
```

## 4. SN Convention Sensitivity

Strict SN convention:

```text
D_L=(1+z_true)D_M(z_true)
```

adds extra penalty:

| branch | Δχ² SN strict-primary | Δχ² BAO strict-primary | Δχ² total strict-primary |
|---|---:|---:|---:|
| LCDM | 0.0 | 0.0 | 0.0 |
| MTS clock u3fit | 2.275647792230302 | 0.35092194655051756 | 2.626569738780745 |
| MTS clock u3quarter | 2.0620532166751673 | 0.331567900454651 | 2.3936211171298964 |

Readout:

```text
the clock route is SN-convention sensitive.
```

That is a demotion signal for universal clock coupling. A parent action would need to prove exactly why SN should see the softer observed-redshift convention. Without that, the global clock route is not allowed to carry the bridge.

## 5. BAO Row Anatomy

Against LCDM, the global clock map helps the radial sector overall:

| comparison | observable | sum Δ contribution | readout |
|---|---|---:|---|
| clock u3fit vs LCDM | DH_over_rs | -1.9404533402234005 | better |
| clock u3quarter vs LCDM | DH_over_rs | -2.002957011783607 | better |
| clock u3fit vs LCDM | DM_over_rs | 0.03870757065235156 | roughly neutral/slightly worse |
| clock u3quarter vs LCDM | DM_over_rs | -0.0021185856672257947 | neutral/slightly better |
| clock u3fit vs LCDM | DV_over_rs | 0.12619530986586522 | worse |
| clock u3quarter vs LCDM | DV_over_rs | 0.08348193161038443 | worse |

But against the no-clock MTS branch, the clock projection worsens BAO:

| comparison | observable | sum Δ contribution | readout |
|---|---|---:|---|
| clock u3fit vs no-clock u3fit | DH_over_rs | 0.4515457466128947 | worse |
| clock u3fit vs no-clock u3fit | DM_over_rs | 0.3578455715270542 | worse |
| clock u3quarter vs no-clock u3quarter | DH_over_rs | 0.3934692267750892 | worse |
| clock u3quarter vs no-clock u3quarter | DM_over_rs | 0.34631457459997894 | worse |

Worst row pressures:

| comparison | row | z | observable | Δ contribution |
|---|---:|---:|---|---:|
| clock u3fit vs LCDM | 1 | 0.51 | DM_over_rs | 1.430438174326115 |
| clock u3quarter vs LCDM | 1 | 0.51 | DM_over_rs | 1.374495555347281 |
| clock u3fit vs no-clock u3fit | 11 | 2.33 | DH_over_rs | 1.084420797846999 |
| clock u3quarter vs no-clock u3quarter | 11 | 2.33 | DH_over_rs | 1.0340424833554571 |

Interpretation:

```text
the clock map is not just “fixing BAO”;
it helps some radial pressure but overmoves specific rows,
especially low-z transverse and high-z radial rows.
```

So a real projection theorem must be row-shape disciplined, not just sign-disciplined.

## 6. H(z) Pressure

The audit confirms checkpoint 157:

```text
H(z) is not the primary failure driver.
```

The clock branches remain competitive draws against LCDM in the source-locked H(z) sets. The chronometer derivative-map pressure is not zero, but it is not the thing killing the branch.

So the live decision is between:

```text
global SN clock coupling,
or ruler/BAO projection only.
```

## 7. Ruler-Only Projection Diagnostic

The key new diagnostic:

```text
SN uses the no-clock MTS branch;
BAO uses the fixed cell-clock projection;
Omega_m is still fitted once;
no redshift polynomial or extra clock parameter is added.
```

Result:

| policy | ΔBIC vs LCDM | ΔBIC vs no-clock | ΔBIC vs global clock | readout |
|---|---:|---:|---:|---|
| ruler-only projection u3fit | -3.43119613128556 | 1.6702956398319202 | -5.557933853998293 | preferred vs LCDM, worse than no-clock, better than global |
| ruler-only projection u3quarter | -3.868328116780731 | 1.3856129363377931 | -4.964039023763462 | preferred vs LCDM, worse than no-clock, better than global |

This is the sharpest result in the checkpoint:

```text
ruler-only projection survives;
global clock coupling does not;
no-clock MTS still scores best among these MTS variants.
```

So the correct move is not to claim the clock map. The correct move is:

```text
demote global clock coupling;
keep a ruler/projection theorem target alive;
require it to explain why BAO sees the projection but SN clocks do not.
```

## 8. Gates

Machine gate result:

| gate | status | evidence |
|---|---|---|
| source paths | pass | all 157 source artifacts exist |
| SN failure driver | pass | u3fit ΔSN = 3.9022881824178057; ΔBAO = -1.775550459705185 |
| quarter branch milder | pass | primary ΔBIC vs LCDM = 1.095710906982731 |
| strict SN convention | fail_global_clock | strict u3fit ΔBIC = 4.753307461493478 |
| H(z) derivative pressure | pass_not_driver | no primary H(z) BIC disfavor vs LCDM |
| ruler-only projection | pass_live_subroute | quarter ruler-only ΔBIC vs LCDM = -3.868328116780731 |
| global clock coupling | demote_or_rederive | global SN coupling is damaging |
| promotion | fail | no bridge promotion |

## 9. Decision

Current fair status:

```text
global_clock_demoted_ruler_projection_route_remains_live
```

Meaning:

```text
the universal/global clock-map route is demoted;
the BAO/ruler projection route remains live;
the no-clock 2/27 background remains the stronger empirical late-time branch;
the ruler-only projection is better than LCDM but still worse than no-clock MTS;
no CMB/bridge/local-GR promotion is allowed.
```

This is a useful defensive round. We found the opening:

```text
do not make SN inherit the BAO projection automatically.
```

But this creates a new burden:

```text
derive a projection tensor or ruler-calibration map that affects BAO rulers
without becoming an arbitrary BAO-only patch.
```

## 10. Next Target

Next checkpoint:

```text
159-ruler-only-projection-theorem-contract.md
```

Task:

```text
write the exact parent-theory contract for a ruler/BAO projection
that does not globally remap SN clocks.
```

Pass condition:

```text
projection follows from observer/ruler calibration, geodesic ruler transport,
or domain-boundary coframe physics before looking at BAO rows.
```

Fail condition:

```text
projection exists only because BAO needed help.
```

Boxing-card version:

```text
We stop throwing the global clock punch.
The ruler feint is still live,
but now it has to prove it is footwork,
not a sneaky low blow.
```
