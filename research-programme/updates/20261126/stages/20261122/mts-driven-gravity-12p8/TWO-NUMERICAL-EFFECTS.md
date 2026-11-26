# Two different reasons a small signal can look wrong

## Different incoming clocks

There are two stored *incident* first-order distributions: the common-speed wave on the finer old time grid and each physical finite-momentum wave on the old twice-as-wide grid. Earlier flight calculations used a matching common-speed grid for subtraction; stitching at 6.4 without respecting that pairing is a new source of error. The raw continuation uses the actual stored arrays as delivered. It is a useful negative control and has not been removed. The corrected packet reruns only the incoming angular histories from the same regular preparation on the finer old grid, and derives the missing upper order from that preparation. It does **not** reset the already accumulated quadratic distribution. Both use the same new time grid, original native source, wave numbers and tolerance.

A falsifiable way to diagnose this is to set the *incident particle mass* to zero in an auxiliary transfer while retaining both clocks; this is a numerical null, not a cosmology. Let \(dS=S^0_{\rm coarse}-S^0_{\rm fine}\) be the resulting difference of the quadratic massless drivers. In the exactly massless problem the angular offset obeys
\[
 A'=\mathcal L A+dS,\quad A(6.4)=0.
\]
The term proportional to \((w+4)dS_w\) averages to zero because \(\int q^3 W(w+4)\,dq=0\). Thus the artificial thermal stress in units of the massive background density has independently predicted energy, flux, shear and trace proportional to \((A_0,A_1,-A_2,0)\), with coefficient \(4\,e_{\nu,\rm massless}/e_\nu\). Pass that source through the same coupled material response. Test its predicted metric increment against the *difference* of the two independently computed finite-mass runs, not against total gravity. Nothing here subtracts a best-fitting numerical constant. This diagnostic need not work bin-by-bin for extremely slow particles, and the physical massive stress trace need not have zero discretization error.

Outputs: raw and matched direct-bin checks; carrier-attribution and carrier-by-speed tables for cold and heavy MTS. The subtracted controls do not all correspond to an exactly conserved physical matter sector: the trace comparison explicitly accounts for their divergence.

## Angular information lost before the restart

The old quadratic calculation stopped at angular order \(h=18\). Preserving its first 19 moments and filling only the missing upper moments exactly preserves the stored state, but cannot undo a wave already reflected into the retained moments. The new higher-order computation measures the omitted angular current, rather than guessing a new primordial perturbation. At fixed supplied metric and common driver, the difference between the restricted true solution and the closed old hierarchy satisfies
\[
 C'=\mathcal L_h C-e_h\,k\frac{h+1}{2h+1}N_{h+1},\qquad C(t_i)=0.
\]
This follows by subtracting the finite tridiagonal equations. Use the reconstructed earlier \(N_{19}\) to predict the perturbation of the **old** state, then evolve it in the **new** common matter system, without consulting the native target to choose its size. Compare the independent primordial free mode (free minus forced) with the native output and with free streaming driven by the native potentials. The auxiliary boundary-response files change the common angular state while holding the saved thermal increment fixed. They do not silently replace the fully momentum-resolved restart.

For a consistent all-particle repair the equivalent normal distribution at each momentum obeys the projected equation with \(v(q)\mathcal L_h\) and the incoming term \(-e_h k v(h+1)F_{h+1}(q)/(2h+1)\); the thermal shape and mass lag must be corrected consistently too. Its change to early gravity and source, and the finite regular initial surface, must be controlled before treating the shadow calculation as a replacement state. A good agreement of total gravity alone would tell us little about this much smaller error.

