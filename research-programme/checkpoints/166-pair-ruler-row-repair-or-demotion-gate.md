# 166 - Pair Ruler Row Repair Or Demotion Gate

Private repair/demotion checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 165 found:

```text
pair-ruler MTS beats LCDM,
but no-clock MTS remains the cleaner empirical control.
```

The open question was:

```text
can a parent-constrained row-shape repair fix the low-z transverse and high-z
radial pressure without fitting a projection amplitude?
```

Short answer:

```text
one structural repair improves the pair branch;
none beat the no-clock control.
```

So the pair-ruler route is not dead, but it is demoted/frozen as a non-leading side branch.

## 2. Machine Artifact

Script:

```text
scripts/pair_ruler_row_repair_or_demotion_gate.py
```

Run:

```text
runs/20260531-235959-pair-ruler-row-repair-or-demotion-gate
```

Generated:

```text
source_register.csv
repair_variant_contract.csv
repair_variant_scorecard.csv
repair_row_delta_vs_no_clock.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
half_kernel_repair_improves_draw_but_no_clock_remains_lead
```

Claim ceiling:

```text
pair_ruler_row_repair_or_demotion_gate_no_bridge_promotion
```

## 3. Repair Rule

Allowed:

```text
discrete endpoint/envelope/symmetry variants motivated by the source-law or
effective-pair-action structure.
```

Forbidden:

```text
continuous fitted projection amplitude;
row-wise BAO repair;
choosing Pi_perp/Pi_parallel after seeing rows.
```

This was a repair gate, not a fit.

## 4. Tested Variants

| variant | formula | status |
|---|---|---|
| projection off | `T=0`, `S=0` | no-clock control |
| base 161 fixed | `T=(B/4)F(1-2e^-N)`, `S=(B/6)(1-e^-2N)` | current branch |
| pair-action half kernel | `T=(B/8)F(1-2e^-N)`, `S=(B/12)(1-e^-2N)` | best repair candidate |
| half quadrupole only | `T=(B/4)F(1-2e^-N)`, `S=(B/12)(1-e^-2N)` | diagnostic |
| one-endpoint quadrupole | `T=(B/4)F(1-2e^-N)`, `S=(B/6)(1-e^-N)` | weak diagnostic |
| determinant-gated quadrupole | `T=(B/4)F(1-2e^-N)`, `S=(B/6)F(1-e^-2N)` | structural check |
| trace pair envelope | `T=(B/4)F(1-2e^-N)(1-e^-2N)`, `S=(B/6)(1-e^-2N)` | structural check |
| three-endpoint quadrupole | `T=(B/4)F(1-2e^-N)`, `S=(B/6)(1-e^-3N)` | diagnostic |

The important one is:

```text
pair-action half kernel.
```

It is motivated by the normal-ordered symmetric pair action:

```text
S_pair ~ 1/2 integral :delta_g(x)delta_g(y): ell_A K_c^A_B ell^B.
```

If that `1/2` belongs to the kernel normalization, the source law becomes:

```text
T_D = (B_mem/8)F_D(1-2e^-N)
S_D = (B_mem/12)(1-e^-2N).
```

This is not fitted, but it still needs parent ownership before becoming the default branch.

## 5. Scorecard

| variant | delta BIC vs no-clock | delta BIC vs base 161 | delta BIC vs LCDM | readout |
|---|---:|---:|---:|---|
| projection off | 0.0 | -1.5020119090340813 | -5.2539410531194335 | no-clock control |
| pair-action half kernel | +0.5114297958095904 | -0.990582113224491 | -4.742511257309843 | best repair, still draw |
| trace envelope + half quad | +0.7653015995988426 | -0.7367103094352387 | -4.488639453520591 | draw |
| trace pair envelope | +1.1617947900617764 | -0.3402171189723049 | -4.092146263057657 | draw |
| half quadrupole only | +1.252596379577426 | -0.24941552945665535 | -4.0013446735420075 | draw |
| one-endpoint quadrupole | +1.3142258540751754 | -0.18778605495890588 | -3.939715199044258 | draw |
| base 161 fixed | +1.5020119090340813 | 0.0 | -3.751929144085352 | draw |
| three-endpoint quadrupole | +1.6758935192017361 | +0.1738816101676548 | -3.5780475339176974 | draw |

So the half-kernel repair is clearly better than the base pair branch:

```text
delta BIC improvement vs base = -0.990582113224491.
```

But it still does not beat no-clock:

```text
delta BIC vs no-clock = +0.5114297958095904.
```

## 6. Row Readout

For the best half-kernel repair, the same pressure rows remain but are reduced:

| row | z | observable | delta contribution vs no-clock | readout |
|---:|---:|---|---:|---|
| 1 | 0.51 | `DM_over_rs` | +0.38892733263447843 | still worse |
| 11 | 2.33 | `DH_over_rs` | +0.16369125612925509 | still worse |
| 7 | 1.321 | `DM_over_rs` | +0.005590452959953765 | small worse |

The repair helps many rows:

```text
0.934 DH improves,
1.484 DM/DH improves,
2.33 DM improves.
```

But it does not remove the two main pressure points.

## 7. Gates

| gate | status | readout |
|---|---|---|
| candidate repairs structural | pass limited | only discrete variants tested; no fitted projection amplitude |
| base 161 status | live but not lead | delta BIC vs no-clock `+1.5020119090340813` |
| best repair variant | pass improves base | half-kernel delta BIC vs base `-0.990582113224491` |
| beats no-clock control | fail draw only | best repair delta BIC vs no-clock `+0.5114297958095904` |
| parent derivation required | fail open | half factor must be owned by the effective pair action |
| demotion decision | freeze as non-leading side branch | no tested repair beats no-clock |
| promotion | fail | no bridge/CMB/local-GR claim |

## 8. Decision

Current fair status:

```text
half_kernel_repair_improves_draw_but_no_clock_remains_lead
```

Meaning:

```text
the pair-ruler route has a better structural side-branch;
the half-kernel version should replace the base pair-ruler sidecar if the pair
action owns the 1/2 factor;
but no-clock MTS remains the empirical lead branch.
```

This is a disciplined demotion, not a burial.

The branch now becomes:

```text
non-leading theorem/test sidecar,
useful for two-point safety checks,
not the lead cosmology branch.
```

Boxing-card readout:

```text
The half-kernel repair tightens the guard and lands cleaner.
But no-clock still takes the round on the cards.
So we stop trying to force pair-ruler into the main event and use it as a
sidecar test of the two-point machinery.
```

## 9. Next Target

Create:

```text
167-no-clock-lead-and-pair-sidecar-test-plan.md
```

Task:

```text
prioritize no-clock MTS as the empirical lead while keeping the half-kernel
pair-ruler branch as a fixed sidecar for growth/RSD, lensing, and CMB-ruler
safety tests.
```

Pass condition:

```text
the test plan cleanly separates lead empirical claims from sidecar theorem
targets and prevents BAO-only tuning.
```

Fail condition:

```text
pair-ruler keeps being treated as lead despite not beating the no-clock control.
```
