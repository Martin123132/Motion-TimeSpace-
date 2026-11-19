# Native transfer convention: distinguish two Weyl readouts

The first readout file deliberately evaluates KINEMATIC Newtonian potentials from the actual differentiated saved metric. Its column weyl=(eta_k+sigma')/(2k) is not automatically the old solver's exported Weyl variable when the old history violates the spatial-pressure equation.

Inspection of retained native equations.f90 lines2756-2771 confirms:
```
W_native=-(D+3H Q/k+Pi)/(2k^2)
Transfer_Weyl=k^2 W_native
Transfer_Newt_vel_baryon=-k(v_b+sigma)/H.
```
Phi_native=-(D+3H Q/k)/(2k^2) and Psi_native=Phi_native-Pi/k^2. The native k^2 factor and H-normalized velocity must not be silently dropped. The retained observer.f90 stores W_native directly at Python column9; old captured packets permit an independent no-rerun comparison.

The existing metric residuals give exact bridge identities:
```
W_kin-W_native=R_shear/(2k)-C00/k
Phi_kin-Phi_native=(H-r)sigma/k-C00/k
Psi_kin-Psi_native=R_shear/k+(r-H)sigma/k-C00/k.
```
Therefore a large correction of the OLD inconsistent kinematic potential is not evidence of an equally large change in the historical exported lensing transfer. Compare the actual native transfer too, and retain both results. This convention audit was added after the kinematic readout showed a large old-to-coherent potential difference; it is not a retuning or replacement of that failed old-envelope diagnostic.

The supplement freezes each native-output norm from ORIGINAL934 states, checks the saved observer, then processes the same cached32/64 old/coherent histories. It verifies the bridge identities without subtracting their physical residuals to manufacture an old-forecast match. Both primary and supplementary output files remain authoritative for their explicitly different definitions.

