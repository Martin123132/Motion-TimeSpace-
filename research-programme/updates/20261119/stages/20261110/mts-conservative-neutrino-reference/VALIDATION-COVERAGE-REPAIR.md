# Preserve all four retained case labels

The first validator failed one coverage assertion. It incorrectly required
the source report to contain only cold and heavy labels. Inspection shows
that it also contains canonical D0 and D01 labels, sharing the heavy
background masses. All twelve case/epoch labels were already preserved
by the numerical reference and correctly mapped in its per-row checks.

The completed validator requires all four cases at initial/mid/final
epochs. It reuses and verifies the exact existing comparison CSV; no
numerical calculation, source mass or tolerance is altered. The original
validator, validation.json and failed worker receipts remain in place.
The authoritative completed check is validation-complete.json.
