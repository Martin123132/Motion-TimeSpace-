# 5271 - Soft-energy angular-boundary surface oracle

## Construction

Checkpoint 5270 derived the shared angular boundary equation

`log|z_label(x,c)| = 0`

at eight soft-energy witnesses. This checkpoint evaluates the same equation on
a `31`-node Chebyshev-Lobatto energy ladder that
also contains every checkpoint-5270 witness. At every energy and transverse
angular node, all labelled roots are rescanned over the complete angular
domain, localized, merged, and converted into topology-uniform panels. No
surface interpolation is used to decide occupation.

Adjacent energy slices are linked by nearest boundary coordinate. Unmatched
boundaries and owner-signature exchanges are retained as explicit topology
event brackets rather than silently interpolated through.

## Result

- Energy nodes: `31`.
- Energy slabs: `30`.
- Boundary functions: `5952`.
- Raw boundaries: `3582`.
- Merged boundaries: `1070`.
- Topology-uniform panels: `1318`.
- Boundary branch links: `1010`.
- Classified surface-event brackets: `50`.
- Event types: `angular_endpoint_entry_or_exit, interior_birth_death_or_merge, owner_merge_split_or_order_exchange`.
- Maximum adjacent-slice coordinate shift: `0.597116597606`.
- Maximum panel coverage residual: `2.22044604925e-16`.
- Checkpoint-5270 witnesses reproduced: `281/281`.

## Decision

`ADOPT_SOFT_ENERGY_BOUNDARY_SURFACE_ORACLE__LOCALIZE_CLASSIFIED_TOPOLOGY_EVENTS`

Validation passed: `true`.

This accepts an independently rescanned boundary oracle over soft energy and
classifies every detected surface-topology event. It does not yet solve those
event locations exactly, authorize interpolation through them, produce a full
phase-space coefficient, establish a numeric UV value, derive local GR, or
complete MTS.

## Next derivation

For every classified event slab, solve either the angular-endpoint equation or
the interior double-root system

`m_label(x,c)=0`, `partial_c m_label(x,c)=0`.

Insert those exact event energies into the ladder, reconnect boundary families,
and require stable three-dimensional cell counts before angular cubature.

## Artifacts

- Runner: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5271_soft_energy_boundary_surface_oracle.py`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\soft_energy_boundary_surface_oracle_result.json`
- Energy nodes: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\soft_energy_surface_nodes.csv`
- Merged boundaries: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\soft_energy_merged_boundaries.csv`
- Boundary links: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\soft_energy_boundary_branch_links.csv`
- Surface events: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\soft_energy_surface_topology_events.csv`
- Witness reproduction: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\5270_witness_reproduction.csv`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5271\soft_energy_boundary_surface_oracle_validation.csv`
