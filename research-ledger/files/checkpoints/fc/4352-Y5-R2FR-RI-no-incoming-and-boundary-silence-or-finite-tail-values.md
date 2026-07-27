# 4352 Y5-R2FR RI no-incoming and boundary silence or finite tail values

Marker: `PPC4161_RI_NO_INCOMING_AND_BOUNDARY_SILENCE_OR_FINITE_TAIL_VALUES_4352`

Decision: `BRI_IRI_ZERO_ON_STATIONARY_COMPACT_ANCHORED_BRANCH_ELSE_FINITE_TAIL_VALUES_NONCLAIM`

## Result

4352 conditionally closes the two owner-tail legs left by 4351:

```text
B_RI=0 and I_RI=0
```

on the same compact anchored stationary branch as `lambda_4350>0`. If the branch is open/radiative/nonstationary, the fallback is no longer vague:

```text
|Y_a| <= |Pi_a^RI|C_Lambda|R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI_bound|
       + |Pi_a^I||I_RI_bound|.
```

## Next

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4353-Y5-R2FR-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md | Can the full clean owner-tail zero branch be propagated into the local residual vector, or must finite B_RI/I_RI/lambda_4350 values be scored? | propagate Y_owner=0 through the compact static private selector and identify remaining non-owner local-GR/source-readout gates | fill finite B_RI_bound, I_RI_bound, R_Lambda, C_Lambda, Pi_a, ell_RI and Eta_RI,total rows for arena scoring |
