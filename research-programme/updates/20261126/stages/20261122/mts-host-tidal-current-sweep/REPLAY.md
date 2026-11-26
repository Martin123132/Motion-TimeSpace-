> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Local replay and ownership

Use Python 3.13 with -B, one numerical thread and assertions enabled, from this directory. No data downloads or network credentials; the [previous stage](../mts-host-local-tidal-basin-544/RESULTS.md), its pinned siblings, the raw complex anchor states and the original solver are read-only. The compact evolution and readout code do not generate a new galaxy or a new force coupling.

1. Run replay.py with arguments 32 64 128 256. The 32/64 cases reproduce the complete early three-knot state at both ends. The higher resolutions are actual new solutions; their endpoint_error field measures distance to the **64**, not to an additional saved 128/256 reference. Retain the compact intermediate state packets. Existing packets are reused. A stop sentinel is respected.
2. Run surfaces.py 8 16 24 32 and controls.py. The directions are in the original common terminal frame, not the time-varying disk angle. Tagged ordinary and cold reconstructions define comparison surfaces only. The guaranteed global outward crossing is checked in closed-surfaces.csv.
3. Run current.py 32:16 64:16 64:8 64:24 64:32 128:32 256:32 and balance.py. These integrate physical currents sampled on saved states, including failures. Run hamiltonian.py 64 256 and defect.py 64 256 for an independent split into finite-element kinetic, local potential projection and sampling/integration remainder.
4. Run cayley.py 64 128 256. This actually re-evolves every native step, including ones absent in the compact packets, reads the physical midpoint current and independently measures the boundary sweep. Stored states must match exactly without phase adjustment before a budget is written.
5. Run gd1_exterior.py, ring_check.py and verify.py. This reuses only the frozen 590 outputs and observed radial budget, not the earlier bounding surfaces. No taper is added to physical waves; a compact outer taper appears only in the manufactured polynomial test to satisfy the outer wall. Rerunning CSV/JSON writers checks their bytes against saved local results. Mesh, solver and prior seal pins are checked as inputs are read. All prior observational-exposure limits remain unchanged.

No pending worker, extra agent, automated relay, remote backup or public publication is required by this stage.

