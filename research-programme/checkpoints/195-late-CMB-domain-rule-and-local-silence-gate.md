# 195 - Late/CMB Domain Rule and Local Silence Gate

Private theory checkpoint. This is not a public CMB, BAO, or local-GR claim.

## 1. Trigger

Checkpoint 194 gave the half-memory bridge a real geometric foothold:

```text
tilde_g_munu = exp(C) g_munu
```

implies:

```text
d tilde_tau = exp(C/2) d tau,
tilde_H ~= H exp(-C/2)
```

when `C` is saturated or slowly varying.

The remaining danger was:

```text
why does CMB see the memory map while late local calibrators do not get wrecked?
```

This checkpoint tries to turn that into an endpoint rule instead of branch
switching.

## 2. Machine Artifact

Script:

```text
scripts/late_CMB_domain_rule_local_silence_gate.py
```

Run:

```text
runs/20260601-000012-late-CMB-domain-rule-and-local-silence-gate
```

Command:

```text
python scripts/late_CMB_domain_rule_local_silence_gate.py --timestamp 20260601-000012
```

Status:

```text
late_CMB_endpoint_rule_partially_derived_local_silence_still_closure
```

Claim ceiling:

```text
endpoint_clock_map_internal_only_local_silence_not_parent_derived_no_CMB_claim
```

## 3. Endpoint Rule

Using the matter metric:

```text
tilde_g_munu = exp(C) g_munu,
```

local clocks and rulers scale as:

```text
exp(C/2).
```

For an emitted and observed photon, the conformal clock map gives the endpoint
redshift relation:

```text
1 + tilde_z = exp[(C_obs - C_emit)/2] (1 + z_g).
```

So the observable is not controlled by absolute `C_obs` alone. It is controlled
by:

```text
Delta C = C_obs - C_emit.
```

This is the key narrowing:

```text
late-local observables can be common-mode,
early-to-late observables can see the memory jump.
```

## 4. Observable Classification

| observable | endpoint class | `Delta C` | status |
|---|---|---|---|
| local clock comparison | same screened local domain | `~0` | safe only if local fixed point exists |
| SN distance ladder anchor | late local calibrator to late observer | `~0` | partial pass with environmental silence |
| late `H(z)` | late clocks inside saturated frame | small if saturated | conditional |
| CMB acoustic angle | early recombination ruler to late observer | `~B_mem` | best endpoint case |
| BAO drag ruler | early drag ruler to late galaxy survey ruler | mixed | hazard |
| growth | path-dependent perturbation history | path-dependent | not closed |

This gives us a non-cheaty rule:

```text
classify observables by their calibration endpoints.
```

But it does not close every observable.

## 5. What Improved

The CMB/late H0 split now has a possible logic:

```text
CMB compares an early ruler to a late clock across Delta C ~= B_mem,
so it can inherit the exp(-B_mem/2) H0 bridge.
```

Late local calibration can avoid the same shift when:

```text
C_emit ~= C_obs,
```

because the conformal factor is common-mode.

That means the theory no longer has to say:

```text
use one H0 here and another H0 there because it fits.
```

It can instead try to say:

```text
use the same endpoint-memory rule for every observable.
```

## 6. What Still Fails Open

BAO is the biggest exposed hazard.

BAO is not purely late-local:

```text
the drag ruler is an early-universe object measured by late surveys.
```

So endpoint algebra alone cannot prove that BAO safely follows the late branch.
It needs its own `r_d` bridge.

The local branch is also still not parent-derived. The conformal connection
shift is:

```text
Delta Gamma^rho_munu =
1/2 (delta^rho_mu partial_nu C
   + delta^rho_nu partial_mu C
   - g_munu partial^rho C).
```

Therefore local GR/PPN silence requires:

```text
partial_mu C -> 0 locally,
dot_C -> 0 locally,
```

or a parent fixed point such as:

```text
q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) -> 0.
```

This is still closure-level. A universal unscreened `C(t)` leaking into local
laboratories is rejected as a parent route.

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| endpoint `Delta C` rule derived algebraically | pass |
| late local common-mode cancellation | partial |
| CMB endpoint bridge classified | partial |
| BAO/`r_d` safety | fail open |
| local PPN silence parent-derived | fail |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
late_CMB_endpoint_rule_partially_derived_local_silence_still_closure
```

Meaning:

```text
The late/CMB split can now be organized by one endpoint-memory rule rather than
branch switching. CMB sees an early-to-late memory jump; late local calibrators
can absorb common-mode scaling. But BAO/r_d and local PPN silence remain open.
```

Current theory status:

```text
the clock-map route survives this gate;
BAO is now the next serious hazard;
local GR still requires a true local fixed point;
no public support claim is allowed.
```

Next target:

```text
196-BAO-rd-endpoint-bridge-or-demotion.md
```
