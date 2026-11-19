# Preflight caught a copied derivative omission

The first heavy current-state preflight stopped before any heavy integration. The native owner was released; the original failed receipt and all four failed chain rows are preserved under heavy-live-memory-stable-remainder. Other checks passed, including the coordinate roundtrip, metric-step and linearity controls. This was not a failed native theory evolution and is not reclassified as a passing first attempt.

Inspection identifies an implementation error in the new live_memory_model.py: the second-row/second-column derivative omitted multiplication by the background field in the expansion term. The retained earlier prop_model.py contains the correct factor. No original checkpoint is changed.

The map entry is M_11=-beta*mu*b/(2*omega), with beta'/beta=mu'/mu=r and omega'/omega=r*mu^2/omega^2. Its product rule is

    M_11'=-(beta*mu/(2*omega)) [b'+r*(2-mu^2/omega^2)*b].

The failed adapter instead used b'+r*(2-mu^2/omega^2), omitting b. This explains why map inversion could pass while its derivative chain failed. The correction restores the already derived equation; it changes neither the map, physical model, effective generator, seeds, bank, grids nor tolerances.

run_checked_mapping.py uses a separately named subclass and output label, verifies this product rule symbolically before native dispatch, preserves the original frozen source and failure, and requires the old worker to be gone and its native release receipt true. It also retains the pre-dispatch stable ordering of the exact-minus-effective remainder described by stable-remainder-contract.json. The cold baseline is reused because it does not enter the heavy geometry routine and its correction is exactly zero. Successful execution of the corrected adapter must still pass all original preflight and integration gates; the diagnosis alone is not acceptance.
