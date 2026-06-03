# 226 - Local Bound Preflight and Baseline Comparison

Private dry-run checkpoint. This is not a public local-GR, PPN, clock, WEP, or
field-theory completion claim.

## 1. Trigger

Checkpoint 225 decided that the next useful move is:

```text
local-bound empirical preflight,
not another V_def placeholder derivation.
```

The aim here is narrow:

```text
use the existing q proxy, J_rel leakage budget, and PPN closure vector to rank
which local residual would bite first.
```

No external/local official data is pulled in this checkpoint.

This is a dry run against the internal q-like gate already used in the local
route.

## 2. Machine Artifact

Script:

```text
scripts/local_bound_preflight_and_baseline_comparison.py
```

Run:

```text
runs/20260601-000043-local-bound-preflight-and-baseline-comparison
```

Command:

```text
python scripts/local_bound_preflight_and_baseline_comparison.py --timestamp 20260601-000043
```

Status:

```text
local_bound_preflight_dryrun_ranked_no_PPN_promotion
```

Claim ceiling:

```text
dryrun_local_bound_proxy_baseline_no_external_data_or_PPN_claim
```

## 3. Fair Baseline Setup

The baseline rows are explicit:

| baseline | role |
|---|---|
| `GR_reference` | local weak-field residuals set to zero by baseline construction |
| `screened_EFT_cosmo_only` | checkpoint-179 cosmological tidal/background fence |
| `MTS_base_compact_proxy` | current compact q proxy before unmodelled `J_rel` leakage |
| `MTS_at_Jrel_budget` | compact proxy plus max allowed `J_rel` leakage |

This is deliberately not:

```text
beat up MTS while GR gets treated as invisible.
```

It is:

```text
same residual vector,
same internal q-like gate,
explicit baseline reference,
explicit MTS closure residual.
```

## 4. Compact Dry-Run Readout

Current compact base proxies:

| case | q proxy / gate | q headroom | J_rel budget |
|---|---:|---:|---:|
| `solar_1AU_shell` | `0.42111206437624615` | `0.5788879356237538` | `1.3314422519346338e-05` |
| `solar_Mercury_shell` | `0.6768420886270882` | `0.32315791137291183` | `7.432631961576971e-06` |
| `earth_GPS_shell` | `0.054771420471689335` | `0.9452285795283106` | `2.1740257329151147e-05` |

Interpretation:

```text
solar_Mercury_shell is tightest on raw q-proxy headroom.
```

It is also tightest on absolute remaining source-leakage budget:

```text
7.432631961576971e-06.
```

So if the question is:

```text
where does q-like source leakage break first?
```

the dry-run answer is:

```text
solar_Mercury_shell.
```

## 5. Coefficient Budget Readout

For coefficient-mapped PPN residuals:

```text
residual_i = c_i epsilon_J.
```

The tightest proxy coefficient budget is:

```text
earth_GPS_shell:
max |c_i| = 1.057945159147665.
```

That applies to the placeholder residual coefficients:

```text
c_gamma,
c_beta,
c_slip,
c_G,
c_clock,
c_matter.
```

Interpretation:

```text
if any local response coefficient is much above order unity in the GPS-like
case, the current proxy budget can fail.
```

This does not mean GPS proves or disproves MTS.

It means the next derivation must not leave those coefficients floating.

## 6. Priority Queue

Dry-run ranking:

| rank | target | reason |
|---:|---|---|
| 1 | `earth_GPS_shell` coefficient map | smallest allowed unknown response coefficient |
| 2 | `solar_Mercury_shell` base q proxy | largest current q-proxy ratio |
| 3 | `solar_Mercury_shell` `J_rel` leakage | smallest absolute source-leakage budget |
| 4 | official local-bound manifest | required before any observational claim |

So the next exact theory target is:

```text
derive or bound the coefficient map from epsilon_J into gamma, beta, slip,
G_eff, clock, and matter residuals.
```

The next empirical target is:

```text
prepare official local-bound sources before claiming any pass/fail.
```

## 7. What This Does Not Claim

This checkpoint does not claim:

```text
MTS passes Cassini,
MTS passes GPS clocks,
MTS passes WEP,
MTS derives local GR,
MTS has a local PPN solution.
```

It only says:

```text
under the internal q-like dry-run gate,
the base compact proxies are below the gate,
the closure-budget pressure points are now ranked,
and the fair-baseline table exists.
```

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| compact base proxies below q-like gate | pass |
| fair baseline rows included | pass |
| tightest coefficient budget identified | pass |
| external local data used | fail by design |
| PPN/local GR promoted | fail |

The failed external-data row is intentional.

This was a dry run before external-source work.

## 9. Decision

Decision:

```text
local_bound_preflight_dryrun_ranked_no_PPN_promotion
```

Meaning:

```text
the local-bound pressure points are now ranked without hiding the baseline or
pretending the closure coefficients are derived.
```

Main gain:

```text
we now know where the next derivation has to land.
```

Main failure:

```text
the coefficient map and official external local-bound manifest are still not
done.
```

Current status:

```text
local compatibility remains alive as a private proxy;
local PPN remains unpromoted;
next target is coefficient map or official-bound manifest.
```

## 10. Next Target

Create:

```text
227-local-PPN-coefficient-map-or-official-bound-manifest.md
```

Purpose:

```text
either derive/bound the coefficient map from epsilon_J into gamma, beta, slip,
G_eff, clock, and matter residuals, or prepare the official local-bound data
manifest needed before using real observational gates.
```

Pass condition:

```text
at least one residual coefficient is derived or tightly bounded from the local
weak-field structure, or the official-bound manifest is ready for a later run.
```

Fail condition:

```text
we keep using the q-like proxy as if it were a real PPN likelihood.
```
