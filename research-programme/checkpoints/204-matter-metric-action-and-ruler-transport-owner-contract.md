# 204 - Matter-Metric Action and Ruler-Transport Owner Contract

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 203 conditionally derived fossil-ruler transport:

```text
u^mu partial_mu X^A = 0
and
(D_t1 + D_t2) xi = 0
imply
D_t r_BAO^comoving = 0.
```

But it did not show that a parent action owns:

```text
u^mu partial_mu X^A = 0.
```

This checkpoint asks whether that label-transport piece can be derived from a
matter action, rather than inserted as a closure.

## 2. Machine Artifact

Script:

```text
scripts/matter_metric_action_and_ruler_transport_owner_contract.py
```

Run:

```text
runs/20260601-000021-matter-metric-action-and-ruler-transport-owner-contract
```

Command:

```text
python scripts/matter_metric_action_and_ruler_transport_owner_contract.py --timestamp 20260601-000021
```

Status:

```text
matter_metric_action_derives_label_transport_MTS_source_zero_conditionally_C_silence_missing
```

Claim ceiling:

```text
parent_matter_action_candidate_internal_only_C_silence_and_full_parent_missing
```

## 3. Candidate Matter Action

Use the matter metric:

```text
tilde_g_munu = exp(C) g_munu.
```

For universal late matter coupling:

```text
S_matter = integral sqrt(-tilde_g) L_m(psi_m, tilde_g_munu) d^4x.
```

For post-drag pressureless matter labels, use a dust-label action:

```text
S_dust =
integral [
  -sqrt(-tilde_g) rho(n)
  + J^mu(partial_mu phi + alpha_A partial_mu X^A)
] d^4x.
```

This is not the full MTS parent action. It is the minimal matter-sector action
needed to test whether BAO fossil-ruler transport can have an action owner.

## 4. What the Action Derives

Variation with respect to `phi` gives:

```text
partial_mu J^mu = 0.
```

Variation with respect to `alpha_A` gives:

```text
J^mu partial_mu X^A = 0.
```

Writing:

```text
J^mu = sqrt(-tilde_g) n u^mu
```

gives:

```text
u^mu partial_mu X^A = 0.
```

So the label-transport condition from checkpoint 203 is now conditionally
action-derived.

The matter-frame Noether identity also gives:

```text
tilde_nabla_mu T_tilde^{mu nu} = 0,
```

provided matter couples universally and metric-only to `tilde_g_munu`.

## 5. BAO Gain

This gives the BAO branch a real improvement:

```text
the conserved-label half of fossil-ruler transport can be owned by a matter
action.
```

It also conditionally removes one dangerous MTS-specific source:

```text
non-universal tracer/ruler coupling.
```

If all late matter tracers see the same `tilde_g_munu`, then the late distance
and the late transported fossil ruler use the same matter unit:

```text
tilde_D_X / tilde_r_BAO^late = D_X / r_BAO.
```

This strengthens the late common-mode BAO route.

## 6. What It Does Not Derive

The action does not yet prove:

```text
partial_i C ~= 0
```

over BAO survey domains, or:

```text
dot_C/H
```

is below radial BAO tolerance.

It also does not eliminate all post-drag BAO peak motion. Standard nonlinear
evolution, reconstruction, bias, baryon-CDM slip, and shell crossing remain
shared modelling terms. That is not automatically bad for MTS, but it must be
handled symmetrically against `LambdaCDM`, `wCDM`, and `CPL`.

The candidate action removes only the extra MTS-specific non-universal matter
ruler source, and only if the universal matter metric is accepted.

## 7. Source-Term Audit

| source | result |
|---|---|
| standard nonlinear BAO evolution | shared nuisance, not MTS-only proof/failure |
| baryon pressure/slip after drag | bounded/shared correction |
| spatial `C` gradients | MTS-specific open source |
| `dot_C/H` radial leakage | empirically bounded, not parent-derived |
| non-universal tracer metric | closed conditionally by universal matter action |
| photon endpoint memory applied to BAO | projection error unless domain selector is derived |

This is the clean split:

```text
the matter action can own labels;
the C-silence/source problem is still the live enemy.
```

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| candidate matter action written | pass |
| matter-frame conservation derived | conditional pass |
| label transport derived from variation | conditional pass |
| MTS-specific non-universal BAO source removed | conditional pass |
| `C` silence derived | fail |
| full BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
matter_metric_action_derives_label_transport_MTS_source_zero_conditionally_C_silence_missing
```

Meaning:

```text
The BAO fossil-ruler branch now has a candidate action owner for conserved
post-drag matter labels and universal late matter-ruler coupling.
```

But:

```text
spatial C gradients, time drift, the full two-point source S_xi, and the full
MTS parent action are still not derived.
```

Current theory status:

```text
BAO route improved again;
no promotion yet;
next target is to derive or bound the C-silence source terms.
```

Next target:

```text
205-C-silence-source-bound-for-BAO-and-local-rulers.md
```
