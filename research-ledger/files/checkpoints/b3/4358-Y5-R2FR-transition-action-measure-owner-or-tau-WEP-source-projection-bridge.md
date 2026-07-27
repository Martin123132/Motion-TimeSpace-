# 4358 Y5-R2FR transition action-measure owner or tau-WEP source projection bridge

Marker: `PPC4161_TRANSITION_ACTION_MEASURE_OWNER_OR_TAU_WEP_SOURCE_PROJECTION_BRIDGE_4358`

Decision: `TAU_WEP_PRODUCT_TO_AMPLITUDE_BRIDGE_DERIVED_ACTION_MEASURE_OWNER_UNSIGNED_TAUMIN_TARGET_SELECTED_NONCLAIM`

## Result

4358 gives the exact bridge from the MICROSCOPE product anchor to an actual source-weight amplitude:

```text
abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15
```

implies:

```text
abs(Delta_w_TiPt) <= 2.8e-15/tau_min
```

only if:

```text
abs(tau_WEP) >= tau_min > 0.
```

No `tau_WEP=1` shortcut. No measured-G absorption. No WEP/local-GR score yet.

## Next

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4359-Y5-R2FR-transition-tau-min-lower-bound-or-action-measure-zero-proof.md | Can we derive a strictly positive tau_WEP lower bound from source/readout geometry, or parent-sign the action-measure owner that kills w_A? | derive tau_min>0 from the symbolic tau_WEP functional using source worldtube, readout kernel, material tensor and normalization signs | close the parent action-measure/no-w_A theorem; if neither closes, keep only the product-bound nonclaim |
