# 190 - CMB Matched Mock Likelihood or Derivation Pivot

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 189 found a split:

```text
same-density profiled MTS:
  very small post-theta shape residuals to lmax=1000,
  but with H0 around 65.92 and no theta theorem.

locked-Omega_m profiled MTS:
  closer to the declared matter lock,
  but still has percent-level shape residuals.
```

This checkpoint asks:

```text
Under equal rules, does a mock CMB likelihood proxy say the CMB route is worth
continuing, or should we pivot back to derivation before spending more work?
```

## 2. Machine Artifact

Script:

```text
scripts/CMB_matched_mock_likelihood_or_derivation_pivot.py
```

Run:

```text
runs/20260601-000007-CMB-matched-mock-likelihood-or-derivation-pivot
```

Command:

```text
python scripts/CMB_matched_mock_likelihood_or_derivation_pivot.py --timestamp 20260601-000007
```

Status:

```text
CMB_matched_mock_likelihood_proxy_same_density_competitive_locked_branch_pivot_to_derivation
```

Claim ceiling:

```text
mock_likelihood_proxy_only_no_official_CMB_likelihood_no_CMB_claim
```

## 3. Mock Likelihood Definition

This is a proxy only.

It uses:

```text
synthetic data = matched profiled LCDM control spectrum,
covariance proxy = independent cosmic-variance fractional sigma sqrt(2/(2ell+1)),
data vectors = TT, EE, TT+EE,
ell range = 2..1000.
```

It excludes TE from `chi2` because fractional TE residuals are unstable near
zero crossings without the real TT/TE/EE covariance.

Fairness rule:

```text
H0/theta profiling is shared by LCDM, wCDM, CPL, and MTS.
```

So in this proxy:

| model | extra parameters counted |
|---|---:|
| LCDM profiled control | `0` |
| wCDM nested control | `1` |
| CPL nested control | `2` |
| MTS fixed high-cs branch | `0` |

If `B_mem,p,u3` are ever freed, MTS must be re-penalized.

## 4. Main Scorecard

For `TT+EE`, `ell=2..1000`:

| arena | model | `chi2_proxy` | `Delta AIC` | `Delta BIC` | readout |
|---|---|---:|---:|---:|---|
| same physical densities | LCDM profiled | `0.0` | `0.0` | `0.0` | control |
| same physical densities | wCDM nested | `0.0` | `2.0` | `7.599901959208498` | penalty only |
| same physical densities | CPL nested | `0.0` | `4.0` | `15.199803918416997` | penalty only |
| same physical densities | MTS fixed profiled | `0.005343819550079403` | `0.005343819550079403` | `0.005343819550079403` | competitive proxy |
| locked `Omega_m` | LCDM profiled | `0.0` | `0.0` | `0.0` | control |
| locked `Omega_m` | MTS fixed profiled | `81.73575719923768` | `81.73575719923768` | `81.73575719923768` | fails proxy |

Readout:

```text
same-density MTS is essentially a mock-likelihood draw against LCDM in this
synthetic proxy.
```

But:

```text
locked-Omega_m MTS is not competitive in this proxy.
```

## 5. Decision Snapshot

| arena | vector | MTS `chi2_proxy` | verdict |
|---|---|---:|---|
| same physical densities | TT | `0.002965457778117229` | competitive draw proxy |
| same physical densities | EE | `0.002378361771962178` | competitive draw proxy |
| same physical densities | TT+EE | `0.005343819550079403` | competitive draw proxy |
| locked `Omega_m` | TT | `27.723999221374935` | strong pressure proxy |
| locked `Omega_m` | EE | `54.01175797786288` | fails proxy badly |
| locked `Omega_m` | TT+EE | `81.73575719923768` | fails proxy badly |

This is the cleanest CMB split so far.

## 6. Derivation Pivot

The machine ledger says:

| route | status | evidence | required derivation |
|---|---|---|---|
| same-density matched mock likelihood | worth running next | `TT+EE chi2_proxy=0.005343819550079403` | derive why MTS predicts the lower-H0 compensation |
| locked-`Omega_m` CMB branch | pivot to derivation before claim | `TT+EE chi2_proxy=81.73575719923768` | derive locked-matter theta/shape compensation or demote this branch |
| official likelihood | not ready but scoped | proxy and policy are now logged | infrastructure, not theory |
| fundamental promotion | blocked | `B_mem`, theta compensation, perturbations, local GR not derived | parent action and GR/local fixed point |

## 7. Boxing-Card Read

This is not a knockout either way.

It is more like:

```text
same-density MTS:
  slips the CMB shape punches beautifully after theta matching,
  but the footwork requires H0 around 65.92.

locked-Omega_m MTS:
  tries to stand in the declared late-time stance,
  but gets tagged hard by the CMB shape proxy.
```

So the best next move is two-track:

```text
1. Continue the same-density mock likelihood route under equal rules.
2. Try deriving the theta/H0 compensation so the same-density branch is not just
   a fitted escape hatch.
```

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| equal baseline policy logged | pass |
| same-density proxy competitive | pass |
| locked-`Omega_m` proxy competitive | fail |
| theta compensation derived | fail |
| official CMB likelihood | not run |
| support claim allowed | fail |

## 9. Decision

Decision:

```text
CMB_matched_mock_likelihood_proxy_same_density_competitive_locked_branch_pivot_to_derivation
```

Meaning:

```text
The same-density profiled branch deserves a stricter matched mock likelihood.
The locked-Omega_m branch should pivot back to derivation before any CMB claim.
No public CMB support claim is allowed.
```

Next target:

```text
191-CMB-same-density-mock-likelihood-and-theta-derivation-bridge.md
```
