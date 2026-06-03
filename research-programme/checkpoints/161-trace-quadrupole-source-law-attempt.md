# 161 - Trace Quadrupole Source Law Attempt

Private source-law checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 160 found the clean algebraic tensor:

```text
R^A_B = delta^A_B + T_D h^A_B + S_D(n^A n_B - h^A_B/3).
```

The open question was:

```text
can T_D and S_D come from MTS source laws,
or are they just two BAO closure functions?
```

Short answer:

```text
T_D has a surprisingly strong candidate law.
S_D has a plausible but rough candidate law.
Neither is parent-derived yet.
```

This is a good round, not a title claim.

## 2. Machine Artifact

Script:

```text
scripts/trace_quadrupole_source_law_attempt.py
```

Run:

```text
runs/20260531-235959-trace-quadrupole-source-law-attempt
```

Generated:

```text
source_register.csv
source_law_scorecard.csv
source_law_predictions.csv
combined_projection_scorecard.csv
combined_projection_predictions.csv
equation_contract.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
trace_law_strong_quadrupole_law_rough_parent_derivation_missing
```

Claim ceiling:

```text
trace_quadrupole_source_law_attempt_no_bridge_promotion
```

## 3. Candidate Source Laws

Use the coherent FLRW load:

```text
N = ln(1+z).
```

Use the fixed-quarter memory activation:

```text
F_D(N) = 1 - exp[-(N/u_3)^3],
u_3 = 1/4.
```

The strongest trace candidate is:

```text
T_D = (B_mem/4) F_D(N)(1 - 2 exp[-N]).
```

Interpretation:

```text
determinant-gated endpoint balance.
```

The rough quadrupole candidate is:

```text
S_D = (B_mem/6)(1 - exp[-2N]).
```

Interpretation:

```text
two-endpoint radial/screen pair saturation.
```

Then:

```text
Pi_perp     = T_D - S_D/3
Pi_parallel = T_D + 2S_D/3.
```

## 4. Why This Is Interesting

The trace law is not just a generic crossing fit.

The ungated balance:

```text
1 - 2 exp[-N]
```

crosses at:

```text
z = 1.
```

The BAO trace target from checkpoint 160 crosses very close to that. But ungated endpoint balance fails the zero-memory identity because at `N=0` it is nonzero.

The determinant gate fixes that:

```text
F_D(0)=0,
so T_D(0)=0.
```

That matters. Without this gate, the nice row match would be a trap.

## 5. Scorecard

Trace candidates:

| candidate | RMS | max abs | signs | status |
|---|---:|---:|---:|---|
| `T=(B/4)F_D(1-2e^-N)` | 0.00020722041294733985 | 0.0005049925374637975 | 6/6 | strong theorem target |
| same shape, fitted amplitude | 0.00014248997339416178 | 0.000256330548307389 | 6/6 | diagnostic only |
| ungated `T=(B/4)(1-2e^-N)` | 0.0002110757985309706 | 0.0005049925374637975 | 6/6 | row match but zero-memory fail |
| `T ∝ N-ln2` | 0.0008207814471741445 | 0.0014669639095958795 | 6/6 | row match but zero-memory fail |

Quadrupole candidates:

| candidate | RMS | max abs | signs | status |
|---|---:|---:|---:|---|
| `S=(B/6)(1-e^-2N)` | 0.0012395564613583109 | 0.0017327323007234122 | 6/6 | rough theorem target |
| same shape, fitted amplitude | 0.0005136061280492368 | 0.0009592499062242498 | 6/6 | diagnostic only |
| determinant activation only | 0.002804070038657303 | 0.005401643299338258 | 6/6 | too saturated |

The trace coefficient is also close:

```text
fitted trace amplitude is -3.361984878955295% away from B_mem/4.
```

The quadrupole coefficient is less locked:

```text
fitted quadrupole amplitude is +12.005747637375164% away from B_mem/6.
```

So the fair readout is:

```text
trace law: strong clue;
quadrupole law: plausible rough clue;
parent derivation: still missing.
```

## 6. Combined Projection

The fixed, no-fit combined law gives:

```text
T_D = (B_mem/4)F_D(1-2e^-N)
S_D = (B_mem/6)(1-e^-2N)
```

Score:

| branch | RMS all projection residual | max abs residual | signs |
|---|---:|---:|---:|
| fixed trace + fixed quadrupole | 0.0006590935857515172 | 0.0011430642863089775 | 11/12 |
| fixed trace + fitted quadrupole | 0.00034330959988313115 | 0.0006025727400655843 | 12/12 |
| fitted trace + fitted quadrupole | 0.00033407793762829603 | 0.0008023140619541078 | 12/12 |

The fixed branch misses one sign only because `Pi_perp` near `z=1.484` is extremely close to zero:

```text
target Pi_perp = -0.0004489595015024772
predicted Pi_perp = +0.00015999763015481965.
```

That is not a collapse. It is a precision warning.

## 7. Physics Interpretation

The candidate route is now:

```text
trace strain = determinant-gated endpoint balance;
quadrupole strain = two-endpoint pair saturation;
ruler tensor = trace + screen/radial quadrupole.
```

This is much cleaner than:

```text
choose Pi_perp(z) and Pi_parallel(z) by hand.
```

But it is still not derived from an action.

The parent theory must explain why:

```text
B_mem/4
```

belongs to the trace endpoint balance, and why:

```text
B_mem/6
```

belongs to the radial/screen quadrupole saturation.

It must also derive why this operator acts on:

```text
BAO pair separation
```

and not on:

```text
SN luminosity distance,
cosmic chronometer H(z),
generic photon geodesics,
local rods/clocks.
```

## 8. Gates

| gate | status | readout |
|---|---|---|
| source paths | pass | all required sources exist |
| trace source law | strong theorem target, not derived | RMS `0.00020722041294733985` |
| trace zero-memory | pass with `F_D` | ungated law fails at `N=0` |
| quadrupole source law | rough theorem target | fixed amplitude is about 12% low versus best fit |
| combined projection | competitive theorem target, not exact | fixed branch RMS `0.0006590935857515172` |
| pre-data lock | fail open | formulas were identified after BAO decomposition |
| SN/H(z) immunity | fail open | pair-vs-one-point theorem missing |
| parent action derivation | fail open | no variation/conservation identity yet |
| promotion | fail | no bridge, CMB, or local-GR claim |

## 9. Decision

Current fair status:

```text
trace_law_strong_quadrupole_law_rough_parent_derivation_missing
```

Meaning:

```text
the route should not be demoted to arbitrary closure yet;
the trace law is too clean to ignore;
the quadrupole law is viable but needs a better owner;
the whole route still fails promotion until the parent operator proves SN/H(z)
null response and pre-data source-law status.
```

Boxing-card readout:

```text
This was a sharp counterpunch.
Not a knockout, not a belt.
But the footwork is real enough that we keep the route alive for one more
derivation gate.
```

## 10. Next Target

Create:

```text
162-pair-ruler-operator-null-response-contract.md
```

Task:

```text
derive why the operator acts on BAO pair separations while SN/H(z) remain null,
or demote the trace/quadrupole route to an empirical closure.
```

Pass condition:

```text
the action/operator distinguishes two-point ruler transport from one-point
luminosity/clock observables without violating metric/equivalence safety.
```

Fail condition:

```text
SN/H(z) are simply declared exempt.
```
