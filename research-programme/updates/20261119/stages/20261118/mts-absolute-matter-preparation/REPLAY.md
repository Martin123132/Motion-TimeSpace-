# Reproduce locally in a fresh sibling with the same retained input folders

Use the retained 64-bit Python 3.13 scientific environment and the local Visual Studio C build tools. Scripts create outputs exclusively rather than overwriting them. Copy the source and protocol into a fresh sibling; do not run acquisition or build commands over sealed outputs. Run sequentially, single numerical thread. Primary and control work in this checkpoint:

1. build.cmd; same_inputs.py (native input/chemical derivative at the same incoming accuracy as the restart).
2. driver.py pilot --length 320 --step .2; driver.py off --length 320 --step .2 --chem zero. These deliberately test the earlier separate high-accuracy incoming-wave convention.
3. driver.py matched --length 368 --step .2 --same; driver.py angular --length 1450 --step .2 --same; driver.py time --length 368 --step .1 --same; driver.py screened --length 368 --step .1 --same --gas --conserved. The last is a joint sensitivity, not separate causal attribution.
4. driver.py full --length 2704 --step .1 --same; driver.py full-off --length 1450 --step .1 --same --chem zero.
5. overlap.py prepare; overlap.py to49 full 4080 .16; overlap.py check49 full 2200 .22. Both continuations restart the high-resolution z=99 packet. Compare absolute angular and time refinements at z=99 using full versus angular; check49 does not retroactively change its input packet.
6. readout.py angular; readout.py full; constraint.py angular; constraint.py full; interface.py primary full to49; interface.py overlapcheck angular check49; controls.py; initial_constraint.py; wave_replay.py; observable_targets.py. verification uses the datum in each named output, not merely a count of runs. For sensitivity-budget.json also run sensitivity.py.
7. Use verify.py --seal only on a new result folder; verify.py without arguments rechecks the existing manifest read-only. JSON/NPZ/CSV contain the component data and definitions; there is no need for a catalogue download here. Windows compiler intermediates (.obj/.lib/.exp) are unnecessary after compilation. Do not remove either retained dll needed to reproduce or verify results.

