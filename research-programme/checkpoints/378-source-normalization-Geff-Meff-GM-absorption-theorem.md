# 378 - Source Normalization Geff Meff GM Absorption Theorem

Private source-normalization/local-GR checkpoint. This is not a public `G_eff`, `Gdot/G`, fifth-force, PPN, WEP, Einstein-Hilbert, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 377 made fifth-force scoring honest:

```text
delta_G_or_fifth_force needs alpha_Y(lambda_Y),
or a theorem that the surviving effect is only measured-GM normalization.
```

This checkpoint asks:

```text
can a universal monopole residual be safely absorbed into measured GM?
```

Short answer:

```text
not parent-derived yet.
```

Checkpoint 244 already gives a useful conditional result:

```text
closed Pi_M flux -> radially conserved M_eff.
```

But safe measured-GM absorption needs more:

```text
absolute calibration,
constant universal G_eff,
universal matter response,
Ward-owned flux,
no range dependence,
no time drift,
no species dependence.
```

Current result:

```text
M_eff flux conservation imported,
GM absorption not parent-derived,
delta_G/Gdot rows remain active.
```

## 2. Machine Artifact

Script:

```text
scripts/source_normalization_Geff_Meff_GM_absorption_theorem.py
```

Run:

```text
runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem
```

Outputs:

```text
results/source_register.csv
results/source_normalization_objects.csv
results/GM_absorption_theorem_attempt.csv
results/absorption_gate_matrix.csv
results/residual_impact_map.csv
results/source_normalization_contract.csv
results/runner_update.csv
results/failure_modes.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
Meff_flux_conservation_imported_GM_absorption_not_parent_derived_deltaG_Gdot_rows_remain_active
```

Claim ceiling:

```text
source_normalization_GM_absorption_contract_only_no_deltaG_Gdot_PPN_EH_WEP_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. What 244 Already Gave Us

Checkpoint 244 defined:

```text
M_eff(r) := (1 / 4 pi G_ref) int_{S^2_r} Pi_M J.
```

If the compact exterior annulus obeys:

```text
d(Pi_M J) = 0,
```

then:

```text
M_eff(r_2) - M_eff(r_1)
  = int_{S^2 x [r_1,r_2]} d(Pi_M J)
  = 0.
```

Therefore:

```text
M_eff(r) = constant.
```

That is good.

It says radial source hair is killed if the parent theory really gives closed absolute mass flux.

But:

```text
M_eff conserved
```

is not the same as:

```text
measured GM absorption derived.
```

That distinction matters a lot.

## 4. Source Normalization Objects

The branch now distinguishes:

| Object | Needed definition | Current status |
|---|---|---|
| `kappa_parent` | coefficient multiplying local metric equation | not parent-calibrated |
| `G_eff` | Newtonian coupling inferred from local Poisson limit | open |
| `M_eff` | conserved absolute `S^2` harmonic mass flux | conditional from 244 |
| `GM_measured` | product actually determined by local dynamics | absorption tests written |
| `delta_G_residual` | deviation from measured-GM normalization | active if tests fail |
| `Gdot/G` | secular drift of `G_eff` or `M_eff` | active if time-independence fails |

This is the point:

```text
local experiments usually measure mu = GM,
not G and M separately.
```

So a constant universal monopole can be harmless.

But only if it really is:

```text
constant,
universal,
source-normalized,
Ward-owned,
range-independent,
and time-independent.
```

## 5. GM Absorption Attempt

The theorem attempt is:

```text
1. preserve ordinary absolute mass flux as M_eff;
2. prove d(Pi_M J)=0 in compact exterior;
3. define mu_obs = G_eff M_eff;
4. show delta mu / mu is only a constant universal calibration;
5. absorb that calibration into measured GM.
```

The safe case is:

```text
delta mu / mu = constant
```

with:

```text
partial_r mu = 0,
partial_t mu = 0,
Delta mu_A = 0,
alpha_Y(lambda) = 0.
```

The current branch has:

```text
conditional M_eff radial conservation.
```

It does not yet have:

```text
absolute calibration,
G_eff constancy,
universal coupling,
or parent-owned GM absorption.
```

Therefore:

```text
GM absorption is not promoted.
```

## 6. Absorption Gate Matrix

| Gate | Required | Current status |
|---|---|---|
| absolute mass class preserved | `Pi_M` extracts ordinary `S^2` mass flux | conditional pass from 244 |
| radial flux closed | `d(Pi_M J)=0` in compact exterior | conditional pass from 244, not globally parent-owned |
| absolute calibration fixed | parent action fixes units of `Pi_M J -> M_eff` | fail open |
| `G_eff` constant | no radius/time/source/species/environment dependence | not derived |
| universality | same `GM` normalization for all matter/clocks | closure axiom required |
| Ward-owned monopole | flux conserved in total Ward ledger | mapped, not proved |
| no range dependence | no Yukawa/spectral/domain-wall profile | range law missing |

This is the decision line:

```text
M_eff conservation is necessary.
```

But:

```text
it is not sufficient for safe GM absorption.
```

## 7. Residual Impact

If a gate fails, the residual row stays active:

| Failure | Observable rows | Meaning |
|---|---|---|
| `dM_eff/dr != 0` | fifth-force / `delta_G`, `beta` | radial source hair |
| `dG_eff/dt` or `dM_eff/dt` | `Gdot/G`, secular drift | source normalization drifts |
| species-dependent `GM` | `eta_WEP`, composition force | WEP leakage |
| unowned boundary flux | `alpha3`, `Gdot/G`, `beta` | fake conservation |
| constant universal monopole only | absorbed into measured `GM` | safe case if all gates pass |

Current status:

```text
safe case not parent-derived.
```

So:

```text
delta_G,
Gdot/G,
WEP,
beta,
and fifth-force rows remain guarded.
```

## 8. Source-Normalization Contract

A future parent action must satisfy:

| Contract item | Required form | Current status |
|---|---|---|
| define reference `G` | fix `G_ref` used in `M_eff = (4 pi G_ref)^-1 int Pi_M J` | not parent-derived |
| derive `kappa -> G_eff` | `kappa = 8 pi G_eff/c^4` in local metric branch | conditional EH branch only |
| prove `M_eff` conserved | `d(Pi_M J)=0`, no radial memory hair | conditional from 244 |
| prove `GM` absorption | `G_eff M_eff` differs from measured `GM` only by constant universal calibration | not parent-derived |
| retain failed rows | if gates fail, keep `delta_G/Gdot/WEP/beta/fifth-force` active | enforced |

This is a proper engineering rule:

```text
absorb only constants.
```

Do not absorb:

```text
range dependence,
time drift,
composition dependence,
radial hair,
or unowned flux.
```

## 9. Runner Update

| Runner row | After 378 | Claim status |
|---|---|---|
| `delta_G_or_fifth_force_yukawa` | `GM` absorption requires parent source-normalization theorem | active/unscored |
| `Gdot_over_G` | active if `G_eff` or `M_eff` time-independence is not derived | contingent budget-only |
| `beta_minus_1` | radial memory hair still feeds beta unless no-hair/source theorem closes it | budget-only |
| `eta_WEP` | species-dependent source normalization linked to WEP | budget-only |
| Newtonian limit | requires `kappa/G_eff/M_eff/GM` theorem | not promoted |

So:

```text
source normalization is sharper,
but not passed.
```

## 10. Failure Modes

The main traps:

| Failure | Consequence |
|---|---|
| confusing `M_eff` conservation with `GM` absorption | hides `delta_G` |
| ignoring `G_eff` drift | bypasses `Gdot/G` |
| species-dependent source normalization | WEP violation disguised as calibration |
| absorbing radial hair into mass | erases fifth force/beta residual |
| declaring flux conserved without Ward ownership | fake Bianchi closure |

This checkpoint keeps the project honest about a common physics move:

```text
we measure GM anyway.
```

Yes.

But only constant universal normalization disappears that way.

Not everything with an `M` in it.

## 11. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| `M_eff` flux theorem imported | conditional pass | checkpoint 244 closed-flux theorem imported |
| `GM` absorption tests written | pass | seven absorption gates recorded |
| absolute calibration parent-derived | fail | physical mass units remain open |
| `G_eff` constancy parent-derived | fail | no radius/time/source/species theorem |
| measured-`GM` absorption parent-derived | fail | universal constant calibration not proved |
| `delta_G/Gdot` rows retained | pass | active/contingent if gates fail |
| local-GR or PPN pass claimed | fail | source-normalization contract only |
| claim ceiling enforced | pass | no local-GR/source pass |

## 12. Decision

Decision:

```text
Meff_flux_conservation_imported_GM_absorption_not_parent_derived_deltaG_Gdot_rows_remain_active
```

Meaning:

```text
M_eff radial conservation is conditionally available from checkpoint 244.
```

But:

```text
GM absorption requires calibration, G_eff constancy, universality, Ward ownership,
and no range/time/species dependence.
```

Those are not parent-derived.

Therefore:

```text
delta_G,
Gdot/G,
WEP,
beta,
and fifth-force/source-normalization rows remain active as needed.
```

No promotion:

```text
Newtonian source normalization not passed,
PPN not passed,
EH not derived,
local GR not derived.
```

## 13. Next Target

Next:

```text
379 - Class-Only Boundary Action No-Angular Theorem
```

Aim:

```text
attempt the class-only boundary action theorem that would kill
B_0i,
trace-free angular shear,
and radial/vector boundary hair.
```

Pass condition:

```text
boundary vector/shear/radial sources are theorem-zero,
or retained as coefficients.
```

Why this next:

```text
source normalization now says a safe monopole is possible only if boundary hair is really monopole-only.
```

So the next theorem target is:

```text
prove class-only boundary action,
or stop pretending boundary terms are harmless.
```
