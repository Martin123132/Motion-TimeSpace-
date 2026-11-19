# Current-state source coupling of predictive carrier memory

This implements the previous block-operator derivation on the retained native perturbation system, rather than treating the future rest-source history as external forcing. The common homogeneous background remains the parent's existing native background tables. No new background solution, local coupling, state population or pressure law is introduced.

## Coordinates and metric source

Let r collect retained non-heavy perturbation coordinates, including the original slow-field moment block. The heavy physical pair p=(u,w) maps to X=M p=T y+h zeta. Here zeta=L(t)r is obtained by evaluating the CURRENT metric constraint after setting only the heavy perturbation block to zero, not removing its homogeneous background.

The native phase representation contains perturbations, not evolving homogeneous field values. Its background jets are common coefficients returned by the parent. Thus applying its linear operator to a correction vector does not evolve a second background. Zero-state, superposition and current-rest/heavy bidirectional response controls check that use on the retained branch.

The source derivative is computed as

    zeta'=(partial_t L)r + L r'.

The first term uses a local time stencil at fixed CURRENT rest state. The second uses the native CURRENT rest-state derivative with its heavy perturbation block zeroed before applying L. It is not the derivative of the total metric source with the newly generated heavy response accidentally included. H' uses the same native background stencil. These derivatives are numerical and separately refined; no saved future perturbation is read by the evolving RHS.

## Exact and effective actions

For each current Z=(r,y), reconstruct the heavy primitive pair by solving M p=T y+h zeta, repack it into the physical native moment, and call the original native RHS. That call supplies r' and the exact primitive derivative p'. Then

    X'=M' p+M p',
    y_exact'=T^-1[X'-T' y-h' zeta-h zeta'].

The effective action retains the already derived B,b coefficients and source-derivative response:

    y_effective'=B y+b zeta-T^-1 h zeta'.

Both actions have the same CURRENT r' for a given Z. Their difference therefore has zero direct rest rows. This is the matrix-free implementation of A_lift-B_lift derived previously; it does not mean the evolving rest correction is zero.

The forward system is

    Z0'=B_lift Z0,
    Delta'=B_lift Delta+(A_lift-B_lift)Z0,
    Z1=Z0+Delta, Delta(t0)=0.

Rest corrections are generated through their retained coupling to the heavy correction. In floating-point evaluation, form A_lift Z0-B_lift Z0 first and then add B_lift Delta, so exact zero rest remainders are not recovered by subtracting a large rate after adding a small one. No exact reference trajectory appears in these forward arguments.

## Actual evolution derivative, not merely the native RHS at a close state

Comparing the exact native RHS evaluated at Z1 alone would not test whether Z1 actually evolves at that rate. The saved calculation also forms v1=Z0'+Delta' and the coordinate residual v1-A_lift Z1. For the time-dependent linear inverse map x=J(t)Z, the physical candidate derivative is

    x1'=F_native(t,x1)+J(t)[v1-A_lift Z1].

The inverse current-state map is applied to that residual. This gives the actual evolution derivative recorded as actual_physical_derivative. It is separately compared with the original native derivative and checked directly on the retained non-field coordinates. The raw exact-at-candidate derivative is kept distinct in the packet.

## Domain and implementation repairs

The tested branch has positive expansion, nonzero heavy background energy and invertible M/T. Field and velocity zero crossings do not require division by either separately. The numerical mode is the original k=1 and the window is the original65 epochs2892..2956. This is not a demonstration for arbitrary backgrounds, modes, nonlinear perturbations or a newly averaged late-time branch.

The first live adapter omitted a background-field factor in M'[1,1]. The derivative is fixed by the product rule, not by fitting a result; the earlier retained conditional implementation already had the correct expression. MAPPING-DERIVATIVE-REPAIR.md gives the symbolic identity. A separate eight-step diagnostic selected a usable two-step band for the independent subtraction-based derivative checker while preserving the physical metric/integration steps and tolerances. CHAIN-PRECISION-DIAGNOSIS.md records all failures and that diagnostic-informed selection.

For reuse, import CheckedLiveMemory from checked_live_memory_model.py. Its class AST is verified identical to the accepted corrected implementation. The frozen base live_memory_model.py remains as failure provenance and MUST NOT be used alone for new heavy evolution.
