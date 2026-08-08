# 5062 - nonzero kernel transport replay

Marker: `MTS_5062_NONZERO_KERNEL_TRANSPORT_REPLAY`.

The saved nontrivial `S503402_N0001/A13` primary24 job was replayed once with
its full topology and once with the 5061 constructed topology. The case has
eight surface crossings and nonzero topological correction
`1448.6789107030336 + 37.72565733758558 i`.

The full and transported runs return exactly the same correction and final
kernel, `1586.4863075171124 + 39.46239615491207 i`, and both reproduce the
saved job. Their physics-projection digests are identical. Raw JSON digests are
not identical only because the constructed collision roots differ at about
machine precision, changing diagnostic `matching_residual` fields; no consumed
numeric output changes.

## Evidence

- Result: `source-intake/functional_rg/5062/nonzero_kernel_transport_replay.json`
- Full replay: `source-intake/functional_rg/5062/full_homotopy_kernel_gate.json`
- Transport replay: `source-intake/functional_rg/5062/transport_constructed_kernel_gate.json`
- Generator: `scripts/Y5_R2FR_5062_nonzero_kernel_transport_replay.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5062_VALIDATION.csv`

This authorizes topology acceleration operationally, not a new science result.
