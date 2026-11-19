# Preserved failures and source-specific repairs

## Unused early polarization index

The first cold tight-coupling run stopped at an overstrict byte comparison of the serialized regime signature. A dedicated diagnostic found all physical vectors, derivatives, observers, caches, cache masks and clocks byte-identical. Only signature column 6 (`EV%polind`, zero-based 5) differed. `SetupScalarArrayIndices` in the copied `native/fortran/equations.f90` assigns that index only in the NOT-tight-coupled branch: there are no independent photon polarization multipoles in the tight-coupled vector.

`run_checked.py` compares every other signature field exactly and excludes this unused index ONLY when both reference and new capture are actually tight coupled. It records both raw index sequences. It does not alter physical states, initialize/zero active caches, remove a regime guard or change tolerances. Native code and the sealed historical packets remain unchanged. Matching-window signatures still receive a complete exact comparison.

The original cold-tca failure receipt and diagnostic remain. The diagnostic itself exits deliberately with SystemExit(0); the inherited worker wrapper consequently labels its end receipt failed although the shell exit was 0. That receipt is preserved and classified as a deliberate diagnostic stop, not a second failed scientific calculation.

## Adaptive tolerance alone was insufficient

The original MTS matching run at rtol=1e-10 and max_step=window/64 misses the unchanged derivative gate for native zero-based coordinate 96 (the tiny slow-field velocity derivative): absolute discrepancy 1.2967757990285633e-22 against reference peak 5.320305310975871e-18, or 2.437408613286337e-5. The coarser-rtol run's result happened to be smaller; that is not evidence of monotonic convergence. The original result remains passed=false.

A separately frozen step check holds rtol=1e-10, normalized atol=1e-12, physical inputs, output grids and both acceptance gates fixed, and caps internal steps at window/128 and window/256 for BOTH cases and BOTH windows. MTS matching worst derivative discrepancies fall to 2.8654504919048633e-6 and 8.716976213768378e-7; worst moment physical-subspace errors fall from 1.2103057344090099e-8 to 2.977335792363352e-9. Both refinements pass. This supplies measured resolution evidence, not a certified global error bound or permission to relax a gate.

The baseline matching result is already at floating-point/native interpolation scales and is not claimed to improve monotonically. The early tight-coupling baseline also has a small native-integrator comparison floor. All are retained and tested symmetrically.

## Normalized initial state is not a bitwise identity operation

The first independent verifier demanded byte equality after the solver's input division by each coordinate's scale and output multiplication by that scale. That arithmetic can change a final binary digit. It does not choose new physical initial conditions. The verifier and its failed receipt are retained. `verify_normalized_seed.py` reproduces the exact division/multiplication sequence, demands byte equality to that represented seed, requires every change to be at most 2 machine epsilons times the absolute original seed, checks normal-range intermediate arithmetic and requires zero seed entries to remain exactly zero. All later numerical/algebra/physics gates remain unchanged. No numerical calculation was rerun to fix this validator.
