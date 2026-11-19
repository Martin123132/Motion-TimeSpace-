> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Physical right-edge restart and live coupling — verified

Original numerical gate2e-5 and algebra gate1e-10 retained. Original banks, masses, couplings, mode order, background tables, observation grids and source normalization unchanged. No fits or observations newly scored.

## Preparation and current state

- Complete original4253-output preparation:136 cold component/mode checks are bit-identical;672 heavy checks pass, maximum relative difference7.90795e-8. The heavy rerun is not called bit-identical. Mode15 of the original16-mode batch is k=5; no replacement one-mode preparation.
- Captured9 original samples, indices2892..2900, starting at the actual available right edge. Native restart reproduces the captured state, derivative, sources and active caches exactly in both branches. The original full hierarchy and regime are retained.
-415 cold and423 heavy same-state algebra checks pass. Maximum algebra RHS relative differences1.3038e-11 and4.1199e-14, respectively. All7 bidirectional metric/phase controls pass; this includes both the density constraint and momentum constraint at k=5.

## Short physical continuation

Live native rest/metric, scalar stress and time-dependent background; no frozen metric or supplied future rest trajectory. DOP853, rtol1e-10, normalized atol1e-12, fixed output nodes,32/64 maximum-step subdivision. Each branch passes both runs and their comparison, with421 cold and435 heavy component checks per run.

| Fine64 run versus native | Cold baseline | Heavy/MTS |
|---|---:|---:|
| Maximum active-state relative difference |1.4602e-13|3.8637e-9|
| Maximum source relative difference |6.1813e-14|7.5577e-10|
| Maximum active-derivative relative difference |3.2494e-10|1.8574e-7|
| Maximum coherent-subspace remainder, normalized by each reference moment |6.2961e-15|9.4639e-12|

Heavy native interval: tau89.70491681253633..89.71478078459928. Cold uses its own native clock89.70485251770474..89.71471667261746, with the same original scale-factor grid. This is eight early-time saved intervals, not a late-epoch forecast. Heavy32/64 differences: source8.1918e-11, state7.3687e-11, derivative1.5353e-8. All remain below the original2e-5 gate; no claim that every component shrinks monotonically against the fixed native reference.

## Connection to recovered memory

All9 endpoint/coordinate/source checks pass; maximum9.46382e-9 comes from the old rest readout, whose reconstruction used float-origin output columns. Current-source algebra agrees to1.5244e-16. The old carrier and all902 signed historical samples remain unchanged.

Current normalized (D,Q,P) is (-0.0455189919446,-0.0000848416057,0.0319144787077). The HISTORICAL weighted average remains (-0.0470334883794,0.0345313725018,-0.0002538081209). These are deliberately different readouts of oscillatory data. Copying the averaged pressure into the instantaneous native boundary would not be a coordinate transformation.

The actual-clock j-generator, including self-gravity, current rest coupling, representation defects and source-map derivatives, passes all4 independent derivative-component checks with maximum3.7969e-12. Its native rate differs from physical H by up to1.7642e-7 relative; the implementation retains that distinction rather than altering the original table.

## Meaning of this result

The prior frozen control is now supplemented by a real coupled short continuation from the original preparation. The source-complete instantaneous chart and the initial nonzero history meet at a consistent causal boundary. Next, advance the fixed-lag readout using the saved past plus these generated current sources, and quantify the interpolation/readout error before replacing the explicit history with a compact kernel. The short chart test is not itself that reduced-memory test.

## Handover and ownership

[Operational or machine-specific passage omitted from public reading copy.]

All numerical workers release their native owners and exit. The compiler's138 observed child identities exited and its temporary short-path drive was removed. Final external cleanup receipt is CLEANUP-VERIFIED.json. User-owned coordinator tab remains open. No GitHub, subagents, new timer, service changes or unattended goal resume.
