# Preserve the two represented scale factors

The first cancellation-only diagnostic stopped at its exact-equality prerequisite: an offset packet has slightly different represented scale factors on the two native paths. Rather than relax that prerequisite or set their difference to zero, v2 retains both scales and derives the general identity. The failed cancellation-half-01 receipt is preserved; no physical result was accepted from it.

Let u=1/H, w=omega=a m, P=a/sqrt(w), V=Z/H. For reference minus retained, with overbars meaning pairwise arithmetic means,

    Delta(wu)=wbar Delta u + ubar Delta w,
    Delta gamma=(k^2/2)[(1/w)bar Delta u + ubar Delta(1/w)],
    Delta(1/w)=(w_ret-w_ref)/(w_ref w_ret),
    Delta P=(a_ref-a_ret)/(m(P_ref+P_ret)),
    Delta(P p V)=Pbar Delta(pV)+(pV)bar Delta P.

Then Delta A_N=-i[Delta(wu)+Delta gamma]A-i Delta gamma exp(2i chi)A*-i k exp(i chi)Delta(P p V). The native implementation's products and square roots retain their own rounding; the final native agreement check measures that finite arithmetic discrepancy. This generalizes the common-scale identity instead of hiding the difference. No input, fit, tolerance or frozen prediction is altered.
