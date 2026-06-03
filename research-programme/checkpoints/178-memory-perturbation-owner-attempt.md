# 178 - Memory Perturbation Owner Attempt

Private derivation attempt. This is not a public claim.

## 1. Trigger

Checkpoint 177 wrote the parent-action contract and made the next bottleneck
explicit:

```text
derive F_fric(a,k), mu(a,k), slip/Sigma(a,k), S_mem(a,k),
or demote the growth/perturbation lane to closure-only.
```

This checkpoint asks whether the existing smooth/high-sound-speed memory route
can actually own those perturbation outputs.

## 2. Machine Artifact

Script:

```text
scripts/memory_perturbation_owner_derivation_attempt.py
```

Run:

```text
runs/20260531-235959-memory-perturbation-owner-derivation-attempt
```

Command:

```text
python scripts/memory_perturbation_owner_derivation_attempt.py --timestamp 20260531-235959
```

Status:

```text
memory_perturbation_owner_effective_high_cs_partial_P06_exact_auxiliary_open
```

Claim ceiling:

```text
effective_memory_perturbation_owner_no_parent_promotion
```

## 3. Core Result

The ordinary perfect-fluid exact-smooth route remains rejected.

But the reconstructed canonical scalar route gives a real effective
perturbation owner:

```text
S_phi = integral sqrt(-g) [-1/2 (partial phi)^2 - V(phi)].
```

For this effective owner:

```text
rho_mem = K + V
p_mem = K - V
c_s_eff^2 = 1
pi_mem = 0
F_fric = 0
```

and the memory clustering correction is subhorizon-suppressed:

```text
|delta_mem / delta_m| <= |1+w_mem| (aH/ck)^2
```

with:

```text
|mu-1| <= (Omega_mem/Omega_m) |delta_mem/delta_m|.
```

This partially relaxes blocker `P06`.

It does not clear promotion because `V(phi)` is reconstructed from the locked
background instead of being derived from the MTS parent variables `Q`, `D`, `R`,
or the boundary charge.

## 4. Reconstruction Checks

The canonical reconstruction stays healthy on the sampled late-time branch:

| check | value | readout |
|---|---:|---|
| field excursion `0 <= z <= 3` | `0.14537255076761377 Mpl` | small sub-Planckian |
| minimum `w_mem` | `-1.0` | non-phantom |
| maximum `1+w_mem` | `0.15878590317200947` | peak near `z = 0.238753` |
| maximum `K/rho_crit0` | `0.058045612887593086` | positive kinetic |
| minimum `V/rho_crit0` | `0.6656833997817613` | positive potential |
| maximum `|dphi/dN|` | `0.516695005572889` | finite roll |
| failed reconstruction checks | `0` | pass |

So as an effective EFT object, the memory stress is legal:

```text
no ghost,
no gradient instability,
no anisotropic stress,
minimal-coupling Bianchi conservation.
```

## 5. Perturbation Output Contract

The checkpoint writes the required `P06` outputs as follows:

| output | result | status |
|---|---|---|
| `F_fric(a,k)` | `0` | derived effectively from minimal coupling |
| `c_s_eff^2` | `1` | derived effectively from canonical kinetic term |
| `delta_mem/delta_m` | bounded by `|1+w_mem|(aH/ck)^2` | effective subhorizon bound |
| `mu(a,k)-1` | worst sampled bound `4.74196829708e-05` | effective late-time bound |
| slip/lensing | no anisotropic stress; lensing source tracks same Poisson bound | effective, spectra not run |
| `S_mem(a,k)` | bounded by `(3/2) Omega_m |mu-1|` | effective growth-source bound |

Worst sampled `|mu-1|` row:

```text
z = 0.24
k = 0.02 h/Mpc
|mu-1| <= 4.74196829708e-05
```

That is tiny for the late-time source-locked growth rows. It is not a
superhorizon theorem, not a CMB spectra result, and not a local PPN proof.

## 6. Exact Auxiliary Route

The exact-smooth route is still open but not derived.

The obstruction ledger is:

| route | result | reason |
|---|---|---|
| ordinary perfect fluid exact silence | rejected | activation has `w_mem != -1`, so energy/momentum perturbation sources remain |
| canonical scalar exact silence | not exact | metric perturbations source `delta_phi` on large/superhorizon scales |
| auxiliary constraint `delta I_M^GI = 0` | open | needs constraint stress and Bianchi identity |
| local GR silence | open/blocking | needs `q_loc^nu -> 0`, `G_eff/G -> 1`, `gamma=beta=1`, `Phi=Psi` |

So the exact-title route is:

```text
derive an auxiliary/geometric memory constraint with a real divergence identity.
```

Until then, exact smoothness is not owned.

## 7. Promotion Gate Effects

| gate | effect |
|---|---|
| P04 parent perturbation action | not cleared |
| P06 perturbation outputs | partially relaxed, effective only |
| P07 CMB Boltzmann interface | not cleared |
| P08 local GR / PPN silence | not cleared |
| P09 zero-knob domain selector | not cleared |
| P10 `B_mem = 2/27` amplitude owner | not cleared |

This is a real improvement, but not a crown.

The growth lane should no longer be described as a naked GR proxy. It now has a
specific effective owner. But it is still not a parent MTS derivation.

## 8. Gate Results

All run-level gates passed:

| gate | result |
|---|---|
| all cited sources exist | pass |
| canonical reconstruction healthy | pass |
| `P06` outputs written | pass |
| late subhorizon bound small | pass |
| exact auxiliary not smuggled | pass |
| theory promotion blocked | pass |
| claim ceiling preserved | pass |

## 9. Decision

Decision:

```text
memory_perturbation_owner_effective_high_cs_partial_P06_exact_auxiliary_open
```

Meaning:

```text
MTS now has an effective high-sound-speed perturbation owner for the late-time
growth lane. This makes the GR-proxy growth treatment defensible as an EFT
limit, but it does not derive the parent action, CMB spectra, local GR silence,
domain selector, or 2/27 amplitude.
```

Boxing-card readout:

```text
This round was won on footwork, not a knockout. The jab is now legal: the
growth correction has a real effective hand behind it. But the belt still asks
for the parent trainer: local GR, CMB, domain selection, and 2/27 ownership.
```

## 10. Next Target

Create:

```text
179-local-GR-PPN-silence-contract.md
```

Next task:

```text
Make the effective scalar route face the local ring: either derive local
weak-field silence for q_loc^nu, G_eff/G, gamma, beta, Phi-Psi, clock response,
and matter universality, or fence the high-c_s owner as cosmology-only EFT.
```
