# Live coupled coherent phase stress

## Retained theory and actual question

This extends `../mts-coherent-projection-20261110` and the live native owner in `../mts-early-state-handoff-20261110`. It does not replace the action, backgrounds, masses, gravitational normalization, abundance, initial perturbations, radiation hierarchy, or measured-data status. The new calculation asks whether the previously derived phase-stress coordinates work when they supply the metric sources and receive that live metric back. The earlier forced-history success alone could not answer that question.

The native reference is the same retained real-scalar quadratic subfamily. CAMB's metric/species evolution and its physical approximations are imported implementation, not newly derived MTS gravity. All code modifications are isolated under this folder. No galaxy release or population prescription is changed.

## Variables and units

Conformal time `tau` is in Mpc with c=1; k, mass, conformal H and omega are in inverse Mpc. Retain the native gravitationally rescaled scalar normalization for background b and perturbation u. Write v=b' and w=u' in the continuum equations. The numerical tables have explicit interpolation defects, accounted for below. D, P, Q are the native rescaled density, pressure and momentum source amplitudes, in inverse Mpc squared, not unscaled SI densities. No new coupling constant is introduced.

For each real scalar:

    mu2=(a*m)^2; omega=sqrt(k^2+mu2)>0
    B=(b,v/omega)^T; U=(u,w/omega)^T; M=B U^T
    D=omega^2 M22+mu2 M11
    P=omega^2 M22-mu2 M11
    Q=k*omega*M21
    U=M^T B/(B^T B)

M has four stored entries but only two physical degrees of freedom. Its columns must remain parallel to B. Neither a field zero nor a velocity zero is singular when B^T B>0. The implementation rejects a zero background norm. It does not assume a positive ensemble or introduce extra occupied modes. The retained signed secular projection is unchanged and is not used to initialize this test.

## Exact derivative of the retained numerical background

Distinguish the native Friedmann rate H from `r=d ln(a_thermal)/d tau`, the derivative of the actual thermal interpolant used by every RHS evaluation. In the continuum r=H, but silently equating their finite interpolation representations would spoil a coordinate-change test.

The thermal table represents a(tau)=tau*p(d), where d is the local fraction of log(tau)/dlntau and p is its retained cubic. Therefore:

    a' = a/tau + p_d/dlntau
    r = a'/a
    chi = omega'/omega = r*mu2/omega^2

FieldJet differentiates the SAME retained slow cubic and heavy endpoint-quintic polynomials with respect to N=ln(a). It neither refits nor replaces those tables. Existing FieldValues arithmetic remains unchanged.

Define the background representation defects:

    E_f = r*b_N-v
    E_b = r*v_N+2H*v+mu2*b
    d=(E_f,E_b/omega)^T
    A_b0=[[0,omega],[-mu2/omega,-2H-chi]]
    A_b=A_b0+d B^T/(B^T B)
    A_u=[[0,omega],[-omega,-2H-chi]]
    F=(0,-k*z*B2)^T

Then A_b B equals the derivative of the actual interpolated B, and the retained scalar equation gives U'=A_u U+F. Differentiating the product, without averaging, gives:

    M'=A_b M+M A_u^T+B F^T.

The defect term is a coordinate representation correction for the existing background, NOT an added physical force. On the physical subspace this is exactly B' U^T+B U'^T. No rank projection or fitted damping is applied during integration. Transverse drift is measured separately, per entry.

## Actual two-way coupling

The phase vector removes the two primitive scalar coordinates per field from the active native vector and inserts four constrained moment entries. It retains every other active species coordinate and, for MTS, the exact-zero branch selector. The removed primitive coordinates are not independently integrated shadow variables.

Each call reconstructs primitive scalar coordinates only for native plumbing/diagnostics. Crucially, native PerturbedStressEnergy receives D and Q DIRECTLY from M; it does not recompute them from the recovered primitives. Native scalar pressure is reported directly from M. This native scalar Einstein formulation consumes D and Q explicitly; P's influence is carried by their evolution, not by a fictional extra pressure argument.

The same call builds the total sources and live metric, including:

    z=(D_total/(2k)+eta_k)/H
    eta_k'=Q_total/2                  (flat retained branch)

Its actual z then drives F in the phase RHS. Radiation, baryons, CDM and the active neutrino hierarchy evolve with that same metric. The original radiation caches, approximation flags and thermal owner are retained. The allowed windows have fixed active layouts. No tight-coupling guard is removed; active photon quadrupole/derivative caches are explicitly compared. Approximate massive-neutrino memories are not active in these windows and the new interface rejects that untested regime.

The interface is deliberately single-worker/single-thread and tied to one live CAMBdata owner. It restores the custom-source callback and disables source override after each RHS evaluation. It rejects times outside the captured interval. It is not a portable checkpoint or general regime-switching interface.

## Conservation bookkeeping remains explicit

Direct differentiation of the retained scalar sources gives:

    D'+H(D+3P)+kQ+k*z*v^2
       = E_b*w+mu2*E_f*u+2(r-H)*mu2*b*u
    Q'+2H*Q-kP = k*E_b*u
    R'+H(R+3P_background)
       = v*E_b+mu2*b*E_f+(r-H)*mu2*b^2

These identities separate native interpolation defects from physical source coupling. They become the continuum scalar conservation equations when E_f=E_b=0 and r=H. Reproducing the retained native solution does not erase these defects or establish additional matter-sector closure. The next transfer should carry them as an explicit error budget, not hide them in a compensating stress.

## Evidence and controls

Fifteen exact symbolic identities check the product evolution, recovery, source maps, off-shell conservation ports and thermal derivative. Independent numerical differentiation-by-product uses captured primitive derivatives, not the phase RHS formula. All original 4253 standard/real64 output rows reproduce exactly with the override disabled.

Physical controls perturb CDM at fixed phase state to test metric-to-phase forcing in both models. A heavy-field control changes the physical scalar amplitude at fixed other species and checks the predicted metric and momentum-constraint changes. A deliberately NONPHYSICAL transverse-M probe keeps recovered primitives fixed while changing direct D/Q. The metric responds to those direct sources, detecting any hidden projection. The probe is a code-path test, not a new allowed physical perturbation or population.

The original bank, background grids, 300-point matching output grid, nine-point tight-coupling grid, numerical acceptance 2e-5 and algebra acceptance 1e-10 are unchanged. Internal integration refinement is separately declared in step-refinement-contract.json.
