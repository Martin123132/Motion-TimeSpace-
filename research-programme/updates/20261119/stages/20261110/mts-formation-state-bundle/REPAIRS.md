# Attempt ledger

All repairs are confined to this new stage. No parent bank, original numerical
grid, background, physical parameter or tolerance changed.

1. Prelaunch parser failure: a missing list bracket in the symbolic matrix.
   No worker output existed. See PRELAUNCH-REPAIR.md.
2. worker-start/end.json: early extraction succeeded, late extraction stopped
   at the unchanged pressure algebra gate. Kept early packets, source hashes,
   symbolic receipt and failed worker receipt. diagnose_pressure.py finds21of1995
   ill-conditioned comparisons; maximum naive relative discrepancy1.45112e-7.
   Stable synchronous evaluation gives <=4.45e-16. complete_bundle.py reuses
   the early packets and exports only the remaining late data. completion-end.json
   is the successful result receipt. DERIVATION.md's pressure equation is
   unchanged; this is an equivalent evaluation, not a new closure.
3. validation-start/end.json: checks reached report writing, then numpy int64
   serialization failed. validation.json is deliberately partial and INVALID.
   validate_bundle_attempt01.py preserves the source. validate_bundle.py casts
   that report count to a Python integer and uses new validation-02 receipts;
   no assertion or tolerance changed. validation-02.json is authoritative.
4. VOLUME-MEASURE.md is an explicitly labelled additional derivation, not a
   retcon of the late packet's leading flat-measure coordinate. add_volume_state.py
   writes a separate packet and receipts, preserving both physical density
   and metric-correct coordinate number. No old artifact was overwritten.

The standalone pressure diagnosis ran synchronously and exited0. All numerical
workers have exact start/end identities. The final seal checks their absence.
No temporary app/server/subagent was started and no unrelated process was changed.
