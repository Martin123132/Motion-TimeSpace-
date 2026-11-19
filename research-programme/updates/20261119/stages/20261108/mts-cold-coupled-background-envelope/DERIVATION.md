# Whole cold coupled-source uncertainty and physical growth structure

This continues the retained source and relative-phase coordinates from `../mts-cold-exact-coupled-jets-20261108`. Its sealed direct/factored identity is unchanged. We now bound the complete coupled generator, not merely its separately estimated ingredients.

## 1. Scope and inherited tube

Let x=(U,V,rho,tau), with N=ln(a), U=a m_s phi_s, V=phi_s', conformal heavy density rho and physical conformal clock tau. The inherited cold interval is N in [-1.0140872889512205,-0.7640872889512206]. Parent bounds give the MTS componentwise replacement radii

    e_U=e_V=5.894762004660344e-11
    e_rho=2.176107332714176e-13
    e_tau=0.017485713632227135 Mpc.

The parent source-envelope files supply the enclosing box and exact provenance. The scalar Euclidean-radius information is retained for independent fixtures; the componentwise bound is a conservative use of that radius. Baseline heavy-averaging replacement radii are zero, not its complete numerical or observational error.

At each comparison N, both states use the SAME retained external finite thermal source, sound-speed/opacity history, wave number and phase. The box encloses all N in the cold window; c=cos(2theta) and s=sin(2theta) are conservatively enclosed by independent [-1,1] intervals. This contains the physical circle and does not approximate it by samples.

The native finite five-node perturbation quadrature, external finite Fermi quadrature, normalization defect and its first two derivatives are kept separate. UFA/full radiation options and the G192 massive hierarchy retain their original source choices.

## 2. Differentiate the cancellation-factored generator

The retained physical equation and endpoint maps give

    A = T^-1(GT-T_N) + T^-1 K S
    K = (GW-W_N+F)L - W(L_N+LG+LFL).

Here G is the free source, F the metric injection, L the complete metric readout, T the periodic heavy map, W the physical affine map, and S=(I-WL)^-1 T. The first term is evaluated using the already derived heavy normal-form cancellation plus gamma I. All other free rows remain in the full system.

An outer interval automatic derivative follows all four variables x. An inner directional derivative follows the exact physical source rates, including theta_N=mu-1.5s. Thus an outer derivative of L_N or W_N includes the derivative of the flow itself: it is not obtained by holding the physical flow coefficients fixed. `BackgroundJet` supports the negative-half power needed when differentiating a square root inside the directional derivative. It does not modify the earlier jet implementation.

All interval arithmetic uses 50 decimal digits. Outward float conversions enlarge bounds before saving. Denominators and positive square-root arguments are checked across the full box. A failure of one of those conditions stops the enclosure.

For each matrix entry, the interval calculation yields a_j,rc >= sup |partial A_rc / partial x_j|. The mean-value theorem along the segment between the two states then gives

    |Delta A_rc| <= E_rc = sum_j a_j,rc e_j.

Both states and their connecting segment must lie in the inherited convex box. No sampled maximum is used as a supremum. The saved entry bounds imply

    ||Delta A||_2 <= min(||E||_F, sqrt(||E||_1 ||E||_infinity)).

`factored_sparse.py` evaluates the SAME algebra in sparse form. The metric correction has finite row/column support inside the inherited core plus first two massive-tail levels. Remote G192 rows stay equal to the qualified free source. The enclosure nevertheless includes ALL 190 retained tail levels per massive node and their terminal clock/drift terms; it is not a reduced hierarchy run.

## 3. Separate amplitude growth from skew streaming

For the physical Euclidean norm, d||z||²/dN=2 z^T Sym(A) z. Large skew streaming rotates perturbations without producing norm growth. Bounding it as positive growth would be physically and numerically misleading.

The retained photon, polarization, full/UFA massless and slow-scalar streaming pairs are exactly weighted-skew. Massive higher-multipole streaming is also skew. The exceptional massive monopole/dipole pair has width w=sqrt(v²+4H²/k²), and its symmetric entry simplifies to

    [ -w k/(sqrt(3)H) + v² k/(sqrt(3)H w) ] / 2
      = -2H/(sqrt(3)k w).

`symmetric_source.py` cancels the exact skew pairs algebraically BEFORE applying interval arithmetic, retains this massive contribution, and includes all drift, clock, collision, pressure, heavy normal-form and metric-correction terms. Simply adding interval estimates of opposite skew entries would lose their correlation.

The same mixed derivatives and mean-value argument give an independent bound E_sym on ||Sym(Delta A)||_2. Weyl's inequality yields

    mu_2(A_new) <= mu_2(A_reference) + E_sym,

where mu_2 is the logarithmic norm. E_sym is a perturbation of a growth-rate bound, not the entire growth rate or the total transfer error. The full E_A is still relevant to state differences: skew coefficient changes can affect phases and observables even when they do not amplify the norm.

## 4. Carry the bound through the normalized phase clock

The retained phase mean is time-weighted, not a uniform phase average. Write a_phase=3/2, omega=mu-a_phase sin(2theta), mu>a_phase, and

    J(mu) = integral_0^pi dtheta/omega = pi/sqrt(mu²-a_phase²)
    p_mu(theta) = sqrt(mu²-a_phase²)/[pi(mu-a_phase sin(2theta))]
    Abar(x) = integral_0^pi p_mu(x)(theta) A(x,theta) dtheta.

The expression for J follows by shifting the full-period sinusoid to a cosine and substituting the tangent of half its angle; the resulting real-line integral is proportional to integral dt/[(mu-a_phase)+(mu+a_phase)t²]. It is not inferred from numerical quadrature.

Differentiating the normalized probability density gives

    partial_mu log p_mu
      = a_phase[a_phase-mu sin(2theta)]/[(mu²-a_phase²)(mu-a_phase sin(2theta))].

For |sin(2theta)|<=1, its magnitude is at most a_phase/(mu-a_phase)². Therefore, over the whole-tube minimum mu_min,

    ||p_mu1-p_mu0||_L1 <= a_phase |Delta mu|/(mu_min-a_phase)².

The SAME background derivatives give |Delta mu|<=e_mu. Decompose the change of mean without dropping the change of measure:

    Delta Abar = integral p_mu1 (A1-A0) + integral (p_mu1-p_mu0) A0.

If M_A bounds ||A0|| across the box and all phases, then

    ||Delta Abar|| <= E_A + M_A a_phase e_mu/(mu_min-a_phase)².

Apply the same formula to Sym(A) to bound the logarithmic-norm change of the mean. `mean_weight_bound.py` obtains M_A and M_sym from outward interval value bounds, not sampled matrices. These absolute operator bounds are used only in this linear measure-change term; they are NOT exponentiated as growth rates. The baseline has no heavy phase map and no extra normalized-weight term.

This is a continuous frozen-slow-state mean replacement bound. The original 256-node phase evaluation, its finite-grid arithmetic and the moving-slow-state averaging remainder remain separate. A small change in the period must not be mistaken for a bound on the accumulated unaveraged phase angle.

## 5. Independent checks and arithmetic scope

Sparse pointwise generators are compared against the sealed dense physical pullback for both models, all three wavelengths, three cold epochs and both gravity branches. The structured symmetric expression is compared against the symmetric part of that complete matrix, including remote G192 support.

After freezing the interval bounds, 70-digit complex parameter derivatives at two step sizes independently check the outer mixed derivatives. Background fixtures check actual coefficient changes against the frozen entry and Frobenius bounds. Their success tests the implementation; the interval/mean-value argument above supplies the all-state result. The derivative comparison permits a fixed 1e-50 arithmetic floor and the Frobenius fixture check 1e-45, separate from the physical ALGEBRA=1e-10 and GATE=2e-5 thresholds. Reported ratios are checked separately rather than silently treating these floors as increased physics bounds.

The interval theorem is conditional on the retained finite source coefficients, source model and inherited background error radii. Parent continuum quadrature accuracy, native input representation and global solver arithmetic are not upgraded by these interval checks. This calculation propagates the specific saved background replacement error through the complete coupled equations.

## 6. Toward the original prepared perturbation

These enclosures supply a uniform coefficient-error contribution and its growth-sensitive counterpart for the physical averaging/transport calculation. Apply their saved entrywise structure to the actual original prepared mode, rather than automatically treating a worst-case unit-vector operator bound as an observed transfer discrepancy. Keep both physical endpoint maps, the previously derived averaging remainder, the phase-clock measure correction and global integration error. Do not reset the perturbation at the late cold boundary or discard low-amplitude hierarchy components without an explicit bound.
