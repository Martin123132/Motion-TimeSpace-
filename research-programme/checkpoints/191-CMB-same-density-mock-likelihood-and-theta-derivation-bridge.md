# 191 - CMB Same-Density Mock Likelihood and Theta Derivation Bridge

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 190 said:

```text
same-density profiled MTS is mock-competitive,
locked-Omega_m profiled MTS is not.
```

The useful next step is therefore not more celebration. It is:

```text
try to turn the same-density H0/theta compensation into a derivation bridge.
```

This checkpoint asks:

```text
Can we explain the required H0 shift from the FLRW theta identity and the MTS
distance response, without pretending the parent theory has derived it yet?
```

## 2. Machine Artifact

Script:

```text
scripts/CMB_same_density_mock_likelihood_and_theta_derivation_bridge.py
```

Run:

```text
runs/20260601-000008-CMB-same-density-mock-likelihood-and-theta-derivation-bridge
```

Command:

```text
python scripts/CMB_same_density_mock_likelihood_and_theta_derivation_bridge.py --timestamp 20260601-000008
```

Status:

```text
CMB_same_density_mock_competitive_theta_bridge_closure_not_derived_late_H0_tension_flagged
```

Claim ceiling:

```text
same_density_theta_bridge_internal_only_no_official_likelihood_no_CMB_claim
```

## 3. Mock Result Carried Forward

Checkpoint 190’s same-density proxy is preserved:

| vector | MTS `chi2_proxy` | verdict |
|---|---:|---|
| TT | `0.002965457778117229` | competitive draw proxy |
| EE | `0.002378361771962178` | competitive draw proxy |
| TT+EE | `0.005343819550079403` | competitive draw proxy |

This stays a mock proxy, not real CMB evidence.

## 4. Theta Identity Bridge

The same-density raw CMB hazard decomposes cleanly:

| piece | value | readout |
|---|---:|---|
| observed `Delta ln theta*` | `0.004583244969814429` | raw angle shift |
| `Delta ln rdrag` proxy | `-0.0000011056790626147686` | sound horizon barely moves |
| `- Delta ln DAstar` | `0.004583605741985429` | late-distance projection dominates |
| predicted `Delta ln theta` from `rdrag/DAstar` | `0.004582500062922814` | matches the hazard |
| identity residual | `0.0000007449068916143275` | small CAMB-definition mismatch |

So the first derivation bridge is:

```text
Delta ln theta* ~= Delta ln r_s - Delta ln D_A.
```

For this branch:

```text
Delta ln r_s is tiny,
so the CMB problem is basically a D_A(z*) problem.
```

That is good because it sharpens the target. We are not chasing random CMB
ghosts; we are chasing the late-distance projection.

## 5. H0 Compensation Bridge

Using the checkpoint-188 same-density root trace:

| bridge item | value |
|---|---:|
| target `theta*` | `1.0415969851026594` |
| unprofiled MTS `theta*` | `1.0464546828731176` |
| local `d theta*/dH0` | `0.003049462325859172` |
| dimensionless `d ln theta*/d ln H0` | `0.19670102333562017` |
| linear predicted `Delta H0` | `-1.5929686126191303` |
| actual profiled `Delta H0` | `-1.5794920921325684` |
| linear predicted profiled `H0` | `65.90703138738087` |
| actual profiled `H0` | `65.92050790786743` |
| prediction error | `-0.013476520486563004` |

So a simple first-order bridge predicts the profiled solution very well:

```text
Delta H0 ~= - Delta theta* / (d theta*/dH0).
```

But this is still a numerical bridge, not a parent-theory derivation.

## 6. The New Problem

The same-density branch wants:

```text
H0 = 65.92050790786743.
```

The previous late-reference branch used:

```text
H0 = 68.42175693081872.
```

Difference:

```text
Delta H0 = -2.501249022951285 km/s/Mpc.
```

That is now the big consistency issue.

MTS can slip the CMB shape punches in the same-density profile, but the footwork
points toward a lower CMB-compatible H0 than the late-time reference we had been
using.

## 7. Derivation Contract

To promote this from a clever closure to theory, the next derivation must supply:

| contract item | needed result |
|---|---|
| distance identity owner | derive MTS memory contribution to `D_A(z*)` from parent FLRW equations |
| H0 compensation law | derive `H0_MTS/H0_LCDM` or equivalent clock-calibration relation |
| late-reference consistency | decide whether late SN/BAO/H(z) or CMB same-density branch owns H0 |
| fixed locks | derive or continue explicitly locking `B_mem,p,u3` |
| mock likelihood | replace proxy with official/controlled likelihood under equal freedoms |

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| distance identity bridge works | pass |
| linear H0 bridge predicts profile | pass |
| H0 compensation derived from parent theory | fail |
| late-reference H0 consistency | warning |
| official CMB likelihood | not run |
| support claim allowed | fail |

## 9. Decision

Decision:

```text
CMB_same_density_mock_competitive_theta_bridge_closure_not_derived_late_H0_tension_flagged
```

Meaning:

```text
The same-density CMB branch now has a clean first-order theta/H0 bridge. It is
not random fitting. But the parent theory has not derived why this compensation
must occur, and it creates a real H0 consistency tension with the late-reference
branch.
```

Next target:

```text
192-theta-H0-compensation-derivation-attempt.md
```
