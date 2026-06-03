# 218 - Sidecar Readonly Join Contract or Local Qloc

Private fork checkpoint. This is not a public local-GR, galaxy, SPARC, ETG,
BAO, CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 217 left a practical fork:

```text
either write the read-only galaxy join contract,
or turn the compact-shell sidecar into a q_loc/PPN residual estimate.
```

This checkpoint chooses:

```text
compact-shell q_loc proxy first.
```

Reason:

```text
local GR / q_loc silence is the bigger theory-critical gate.
```

The read-only galaxy join remains deferred.

## 2. Machine Artifact

Script:

```text
scripts/sidecar_readonly_join_or_local_qloc.py
```

Run:

```text
runs/20260601-000035-sidecar-readonly-join-contract-or-local-qloc
```

Command:

```text
python scripts/sidecar_readonly_join_or_local_qloc.py --timestamp 20260601-000035
```

Status:

```text
local_qloc_proxy_chosen_compact_shells_pass_magnitude_gate_PPN_not_derived
```

Claim ceiling:

```text
qloc_proxy_only_no_local_GR_or_galaxy_promotion
```

## 3. Proxy Definition

For compact-shell cases, use the fixed `G_K`/Weyl branch:

```text
L_cg = [L_H^-2 + G_K^2]^-1/2.
```

Then use a conservative local memory-gradient proxy:

```text
Delta C = B_mem r/L_cg
q_gradient ~= Delta C/2.
```

Add the cosmological tidal proxy from checkpoint 179:

```text
q_cosmo = Omega_mem0 (H0 r/c)^2.
```

So:

```text
q_total_proxy = Delta C/2 + q_cosmo.
```

The adopted q-like gate is:

```text
q_R_like_gate = 2.3e-5.
```

This is not a PPN derivation.

It is a magnitude compatibility proxy.

## 4. Compact-Shell Readout

Compact-shell cases tested:

| case | q proxy |
|---|---:|
| `solar_1AU_shell` | `9.685577480653662e-06` |
| `solar_Mercury_shell` | `1.556736803842303e-05` |
| `earth_GPS_shell` | `1.2597426708488547e-06` |

All are below:

```text
2.3e-5.
```

The Earth-surface case was kept as a stress diagnostic, not a compact-shell
promotion case:

```text
earth_surface_stress = 2.572125015052467e-06.
```

## 5. What This Means

This is good news in a narrow way:

```text
the compact-shell sidecar is not immediately killed by the q_R-like magnitude
gate.
```

It does not mean:

```text
gamma = 1,
beta = 1,
Phi = Psi,
or q_loc^nu = 0
```

has been derived.

Those remain open.

## 6. PPN Residual Vector

The current residual vector is:

| residual | status |
|---|---|
| `q_R_like_proxy` | passes magnitude proxy |
| `gamma - 1` | not parent-derived |
| `beta - 1` | not parent-derived |
| `Phi - Psi` | not parent-derived |
| `q_loc^nu` | blocking source-projection theorem target |

So:

```text
this checkpoint narrows the danger,
but it does not crown local GR.
```

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| fork decision | pass |
| compact shell sidecar available | pass |
| q_R-like magnitude proxy | pass |
| surface stress proxy | pass |
| PPN promotion | fail |
| real local observable run | not run |

## 8. Decision

Decision:

```text
local_qloc_proxy_chosen_compact_shells_pass_magnitude_gate_PPN_not_derived
```

Meaning:

```text
compact-shell morphology plus fixed G_K gives a plausible local magnitude
compatibility proxy.
```

But:

```text
the parent source projection q_loc^nu -> 0 is still missing.
```

## 9. Next Target

Next target:

```text
219-compact-shell-q_loc-source-projection-attempt.md
```

The exact next question:

```text
Can compact-vacuum-shell morphology force the local source projection to vanish
or stay below the q_R-like gate without inserting a plateau axiom?
```
