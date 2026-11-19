# Retain the failure, refine the actual time step

The characteristic repair passes physical-source and independent reconstruction checks, but128/256time steps give maximum normalized state difference4.94018e-5, exceeding2e-5. The original validation and both failed numerical flags remain unchanged. No redefinition of the state norm or deletion of high-frequency nodes is permitted.

Run512steps for cold and MTS with the SAME iteration2 forcing history, taken directly from the saved boundary2 source_clock/source_metric. Bank the additional512step evaluation times using the same derived F17 formula, mass, background, momentum rule and10-point time quadrature. Verify overlap with the existing bank and6/10quadrature controls. Only the time step changes.

Use32-step immutable archive packets for this refinement to keep the directory manageable. The existing eight-step original archives stay untouched. Bound processes at900seconds and yield at the first32-step boundary after720seconds; resume only a deliberately completed bounded worker. Track exact identities and preserve all failure evidence.

Compare256/512on all common saved boundaries and common-scale-factor probes, with the original2e-5state/source gates. Recheck the final metric/source identities and characteristics against the512step metric. Recompute the missing F17 from that final history at every saved boundary. Do not promote the repair unless this additional numerical control passes.
