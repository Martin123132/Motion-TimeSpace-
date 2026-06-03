# 185 - CAMB MTS Effective Background Module Contract

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 184 put the locked no-clock MTS branch into the CMB pipeline only as:

```text
background table + closure contract,
no spectra,
no likelihood,
no support claim.
```

The missing object was the exact bridge from that locked payload to CAMB without
adding hidden rescue knobs.

This checkpoint asks:

```text
Can installed CAMB accept the locked MTS w(a) background as a legal dark-energy
module for a tiny spectra smoke?
```

and separately:

```text
Can installed CAMB represent the exact auxiliary delta=theta=0 branch?
```

## 2. Machine Artifact

Script:

```text
scripts/CAMB_MTS_effective_background_module_contract.py
```

Run:

```text
runs/20260601-000002-CAMB-MTS-effective-background-module-contract
```

Command:

```text
python scripts/CAMB_MTS_effective_background_module_contract.py --timestamp 20260601-000002
```

Status:

```text
CAMB_MTS_effective_background_module_contract_ready_for_tiny_high_cs_wtable_spectra_smoke
```

Claim ceiling:

```text
CAMB_mapping_contract_only_no_MTS_CMB_spectra_no_CMB_claim
```

## 3. CAMB Capability Probe

Installed engine:

```text
CAMB Python 1.6.6
```

Capability readout:

| CAMB object | result | MTS use | limitation |
|---|---|---|---|
| `DarkEnergyFluid` | accepts locked MTS `w(a)` table and validates | default high-`c_s` effective-fluid smoke | not parent MTS perturbation theory |
| `DarkEnergyPPF` | accepts locked MTS `w(a)` table and validates | comparator / sensitivity branch | ad hoc PPF, not a physical owner |
| `DarkEnergyEqnOfState` | abstract inventory class, not directly instantiated | API source only | not a runnable branch |
| exact auxiliary constraint | no built-in primitive found | blocked | needs custom module or parent-derived auxiliary equations |

So the next legal move is not a full CMB claim. It is:

```text
run a tiny CAMB spectra smoke for the high-cs effective-fluid w(a) branch.
```

## 4. Locked Background Mapping

The table written for CAMB is:

```text
MTS_CAMB_w_table.csv
```

with 700 monotone scale-factor nodes from:

```text
z = 10000
```

to:

```text
z = 0.
```

The locked law is unchanged:

```text
rho_mem(a) = 1 - Omega_m0 + B_mem A[-ln(a)]
1 + w_mem = B_mem dA/dN / (3 rho_mem)
B_mem = 2/27
p = 3
u3 = 1/4
```

Interpolation checks:

| check | result |
|---|---|
| monotone `a` grid | pass |
| finite `a,w,rho,1+w` | pass |
| positive `rho_mem` | pass |
| non-phantom fluid branch | pass |
| no fitted spline nodes | pass |

Numerical range on the CAMB table:

| quantity | value |
|---|---:|
| `rho_mem` minimum | `0.6967172573233342` |
| `rho_mem` maximum | `0.7707913313974083` |
| `w_mem` minimum | `-1.0` |
| `w_mem` maximum | `-0.8414734524357945` at `z ~= 0.24207734900064581` |

## 5. Perturbation Closure Mapping

Allowed next branch:

| branch | CAMB object | status | claim limit |
|---|---|---|---|
| high-`c_s` effective fluid | `DarkEnergyFluid.set_w_a_table(a,w_mem)`, `cs2=1` | ready for tiny smoke | P06 partial/effective only |
| high-`c_s` PPF comparator | `DarkEnergyPPF.set_w_a_table(a,w_mem)` | allowed diagnostic | not physical MTS evidence by itself |
| exact auxiliary smooth memory | no built-in object | blocked | needs custom equations |
| parent field-theory branch | no built-in object | blocked | needs parent action/perturbation derivation |

This matters because the exact auxiliary route cannot be smuggled into CAMB by
calling it a fluid. CAMB Fluid evolves perturbations. The exact route needs a
real constraint handoff:

```text
delta_mem = theta_mem = delta_p_mem = sigma_mem = 0
```

or a custom perturbation module.

## 6. Fair-Comparison Branches

Two tiny-smoke branches are now explicitly separated:

| branch | purpose | rule |
|---|---|---|
| LCDM-density isolation smoke | isolate what the locked MTS `w(a)` does inside the same baseline physical-density setup | use checkpoint 183 `H0, ombh2, omch2, tau, As, ns, mnu, omk` |
| locked-transfer smoke | test the declared MTS late-time transfer reference | use `H0=100 h`, `Omega_m0`, and declare baryon/neutrino convention before deriving `omch2` |

This keeps the boxing match honest: first we test whether the footwork survives
the same ring conditions, then we test the branch in its own locked transfer
stance. No post-hoc calibration haymakers.

## 7. Forbidden Rescue Knobs

The machine ledger forbids:

| forbidden knob | reason |
|---|---|
| extra fitted `w(a)` nodes | would become generic dark-energy reconstruction |
| refitting `B_mem,p,u3` in the CMB pass | breaks the locked no-clock branch |
| fitting `c_s_eff^2` | hides perturbation-owner failure |
| adding anisotropic stress or lensing rescale | rescues lensing without parent stress owner |
| freeing `N_eff`, curvature, or neutrino mass only for MTS | moves acoustic scales by unrelated calibration freedom |
| retuning `H0/Omega_m` after seeing spectra | makes the pass post hoc |
| treating exact auxiliary as CAMB Fluid output | Fluid is not the exact constrained branch |

If a comparator theory is given the same extra freedom, it must be scored with
the same parameter-count penalties. No guilty-until-proven-innocent asymmetry.

## 8. Readiness Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| CAMB installed | pass |
| `DarkEnergyFluid` accepts locked MTS `w(a)` | pass |
| `DarkEnergyPPF` comparator accepts locked MTS `w(a)` | pass |
| background interpolation contract clean | pass |
| exact auxiliary CAMB mapping | blocked |
| MTS spectra run | not run |
| official CMB likelihood | not run |

## 9. Decision

Decision:

```text
CAMB_MTS_effective_background_module_contract_ready_for_tiny_high_cs_wtable_spectra_smoke
```

Meaning:

```text
The locked MTS high-c_s effective-fluid background can now be passed to CAMB for
a tiny spectra smoke. The exact auxiliary branch remains a custom-module or
parent-derivation debt. No MTS CMB support claim is allowed yet.
```

Next target:

```text
186-CAMB-high-cs-wtable-spectra-smoke.md
```
