# Join audit: normalization round trip, not a state reset

The first final auditor demanded byte identity between the incoming unscaled candidate and the first saved integrator output. The retained mean solver normalizes each branch by its state norm before integration and denormalizes its saved outputs. Floating-point division followed by multiplication need not reproduce the original bytes. No physical equation or numerical gate failed; the new audit assertion ignored that pre-existing arithmetic representation.

Independent inspect_join.py reproduces the normalize/denormalize operation for all six model/wavenumber cases. Every saved first mean state equals that independently reconstructed state **byte for byte**; every corrected first state equals the mean first state byte for byte. Preparation packets retain the incoming candidate byte for byte. The maximum inherited-state relative norm change is 9.327080786095005e-17, against unchanged ALGEBRA=1e-10. Physical readout joining checks also pass their original gate.

audit_extension_v3.py replaces the invalid byte comparison across representations with these stronger explicit round-trip identities plus the existing representation tolerance. It does not alter or rerun any prediction, source, numerical integration, data, arithmetic, grid or tolerance. Original audit-01 receipts and code are retained; its empty audit/ directory is not promoted as a result. The accepted audit is attempted separately at audit-02/result.json. This diagnosis contributes a separately identified join-rounding term to the numerical error ledger.

