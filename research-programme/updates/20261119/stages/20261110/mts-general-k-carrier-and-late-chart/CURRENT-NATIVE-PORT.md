# Solving the metric connection while retaining native other-species variables

This is the direct implementation consequence of the derived chart map. It avoids incorrectly holding transformed rest sources fixed. It uses the original Einstein normalization and no new coupling.

Let the replaced canonical scalar have fixed current background b,v, Sh=v^2, Dstar_h=v*p+mu^2*b*u and Qh=k*v*u. Keep the OTHER species in their native synchronous variables with current sources Dr,Qr. Keep native eta as its existing dynamical coordinate, and retain their anisotropic stress Pi. The scalar's native sources must be

    Dh_sync=Dstar_h+3*Sh*eta,
    Qh_sync=Qh-k*Sh*alpha.

The original native constraints imply

    2*k^2*H*alpha = Dsync_total+2*k^2*eta+3*H*Qsync_total/k.

Substitution solves the apparently implicit metric feedback:

    numerator=Dr+Dstar_h+3*H*(Qr+Qh)/k,
    denominator=2*k^2+3*Sh,
    Phi=-numerator/denominator,
    alpha=(eta-Phi)/H,
    Psi=Phi-Pi/k^2.

For H>0,k>0 and Sh>=0 this has a unique algebraic solution. The denominator contains the REPLACED component's enthalpy only, because Dr,Qr here are still SYNCHRONOUS source values. This is not a different gravitational theory from the total canonical denominator2*k^2+3*S_total. Indeed converting the rest sources as

    Dstar_r=Dr-3*Sr*eta,
    QN_r=Qr+k*Sr*alpha

in the total canonical constraint gives exactly the same solution. Using the total denominator while leaving Dr,Qr native would mix charts and double count the rest-source response.

For the scalar pressure, the same inverse chart gives

    Ph_sync=Pstar_h+3*Sh*eta+2*mu^2*b*v*alpha,
    Pstar_h=v*p-mu^2*b*u.

The lapse and potential then enter the existing unrestricted canonical equations:

    u'=p+(Psi+3*Phi)*v,
    p'=-2*H*p-(k^2+mu^2)*u+mu^2*(3*Phi-Psi)*b.

The other species and eta continue to evolve with the returned TOTAL native stress, including Qh_sync, and Pi is not discarded. No prescribed future rest history or derivative of a future metric is needed. If background or metric equations have representation defects, the arbitrary-defect formulas in DERIVATION.md apply; this algebraic solution alone does not set those terms to zero.

## Independent saved-data check

The metric part is a source-chart identity for any component with the stated density/current transformation. It can therefore be tested against the already saved native CDM component, for which Sh=Rc, Dstar_h=Rc*(delta_c-3eta), Qh=Rc*k*alpha and Qh_sync=0. The test removes ONLY this component's native density from Dr, then reconstructs the saved Phi,alpha,Psi and component stress. It is run on both the cold-baseline and MTS late packets, including the saved sign/zero/precision controls.

This CDM test validates the metric connection, not a claim that dust has the scalar's pressure law. The actual late heavy selector is still an averaged density/current pair and contains no unique unaveraged scalar phase. Selecting or carrying its canonical phase/ensemble and background remains the next matching calculation. The source connection is now explicit rather than unspecified.
