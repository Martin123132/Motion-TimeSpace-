# 188 - CMB Theta Compensation Theorem or Profiled Fit Gate

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 187 made the CMB pressure point sharp:

```text
locked h/Omega_m transfer runs,
but it does not reduce the raw theta* hazard.
```

This checkpoint asks the next disciplined question:

```text
Can theta* compensation be derived from the locked MTS branch itself?
```

If not, the fallback is not to pretend. The fallback is:

```text
quantify the H0/theta profile cost,
and require LCDM/wCDM/CPL/MTS to receive the same fit freedoms and penalties
in any later likelihood run.
```

## 2. Machine Artifact

Script:

```text
scripts/CMB_theta_compensation_theorem_or_profiled_fit_gate.py
```

Run:

```text
runs/20260601-000005-CMB-theta-compensation-theorem-or-profiled-fit-gate
```

Command:

```text
python scripts/CMB_theta_compensation_theorem_or_profiled_fit_gate.py --timestamp 20260601-000005
```

Status:

```text
CMB_theta_compensation_theorem_blocked_H0_profile_quantified_no_likelihood_claim
```

Claim ceiling:

```text
theta_profile_gate_only_no_official_likelihood_no_CMB_claim
```

## 3. Theorem Attempt

The theorem route does not clear.

| attempted claim | result | reason |
|---|---|---|
| locked MTS background internally compensates `theta*` | rejected as derived theorem | checkpoints 186/187 show positive theta shift |
| late memory moves `r_s` enough to compensate | rejected for current branch | `rdrag` barely moves while `theta*` shifts at the `10^-3` level |
| locked `h/Omega_m` transfer is the compensation | rejected at smoke gate | locked transfer slightly worsened the theta shift |
| parent action supplies compensation | not derived | parent action / exact perturbations / local GR remain open gates |
| H0 profiling removes theta hazard | allowed only as fit gate | not a theorem, must be matched for baselines |

So the honest read is:

```text
theta compensation is not derived from the current locked branch.
```

## 4. Matched Profile Rule

The profile rule used here is deliberately narrow:

```text
profile H0 until CAMB theta* equals the checkpoint-183 LCDM target,
keep B_mem=2/27, p=3, u3=1/4 fixed,
run the matching LCDM profile in the same density family,
do not run an official CMB likelihood,
do not score this as MTS evidence.
```

Future likelihood rule:

| model | fair freedom rule |
|---|---|
| LCDM | same H0/theta profiling treatment |
| wCDM | same treatment, plus penalty if `w` is freed |
| CPL | same treatment, plus penalty if `w0,wa` are freed |
| MTS | same treatment, plus penalty if `B_mem,p,u3` are ever freed |

No one gets secret hand-wraps before the fight.

## 5. H0 Profile Results

Target:

```text
theta* = 1.0415969851026594
```

Same physical-density family:

| model | profiled `H0` | shift vs unprofiled | shift vs LCDM profile | status |
|---|---:|---:|---:|---|
| LCDM | `67.49999761581421` | `-0.000002384185791015625` | `0.0` | pass |
| MTS high-cs | `65.92050790786743` | `-1.5794920921325684` | `-1.5794897079467773` | pass |

Locked `Omega_m`, neutrino-subtracted family:

| model | profiled `H0` | shift vs unprofiled | shift vs LCDM profile | status |
|---|---:|---:|---:|---|
| LCDM | `68.19550275802612` | `-0.22625417279259352` | `0.0` | pass |
| MTS high-cs | `67.53464937210083` | `-0.8871075587178865` | `-0.660853385925293` | pass |

Interpretation:

```text
H0 profiling can force theta* to match, but it costs MTS a lower H0 than the
matched LCDM control. That is a compensation cost, not a theory win.
```

## 6. Profiled Shape Residuals

After theta matching, the remaining spectra residuals are:

| branch | control | RMS `Delta TT/TT` | RMS `Delta EE/EE` | max `|Delta TT/TT|` |
|---|---|---:|---:|---:|
| same-density MTS profile | same-density LCDM profile | `0.0014215437366681932` | `0.000371472406174854` | `0.013753960874984879` |
| locked-`Omega_m` MTS profile | locked-`Omega_m` LCDM profile | `0.0117857505662772` | `0.0057690052417175095` | `0.020187930290631147` |

That is the important boxing-card update:

```text
same-density H0 profiling makes the high-ell shape smoke look much less scary,
but the required H0 shift is sizeable and points low.
```

The locked-`Omega_m` profile is less clean:

```text
theta can be forced, but residual shape differences stay around percent level.
```

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| theta theorem derived | fail |
| H0 profile roots found | pass |
| MTS fixed locks preserved | pass |
| matched baseline freedom | pass |
| official CMB likelihood | not run |
| profiled spectra residuals logged | pass |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
CMB_theta_compensation_theorem_blocked_H0_profile_quantified_no_likelihood_claim
```

Meaning:

```text
The theory does not yet derive theta compensation. H0 profiling can numerically
repair theta*, but only as a matched fit freedom. It must not be counted as a
CMB win unless LCDM/wCDM/CPL/MTS are all treated under the same likelihood and
penalty rules.
```

Next target:

```text
189-CMB-profiled-shape-residual-and-likelihood-readiness.md
```
