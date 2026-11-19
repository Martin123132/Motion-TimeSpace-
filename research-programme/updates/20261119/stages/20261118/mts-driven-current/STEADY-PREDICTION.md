# Separate a burst from a stationary external moment

The prescribed initially rotating charges have ZERO initial transverse field. That is valid initial data, not the magnetostatic equilibrium of that current. A transient reaching a detector does not prove persistent radiation or a long-range magnetic moment. On the static η=1 ordinary branch derive the unique regular, decaying equilibrium and compare different calculations before interpreting the burst. Use no incoming wave or exterior applied magnetic field. A is a linear rotation coefficient, energies are per squared rotation amplitude as before.

Let L=−∂r B∂r+U and S as in SPECTRAL-PREDICTION.md. The stationary minimizer satisfies L A*=S. Its finite positive quadratic form includes material recoil and the rotational constraint as well as magnetic energy. Completing the square gives the energy initially available ABOVE that new steady state: E_free=½∫SA*dr=½∫[B A*'²+U A*²]dr>0 if S is nonzero. This is not the integral actually observed at a particular exterior sphere, and does not assume that all that energy has left the system by t=6.5.

Normalize the regular homogeneous solution y=r²c by c(0)=1 and the decaying homogeneous exterior d by r d→1. At the surface R=5 set W=B(y' d−y d'). Outside, A*=μ∞ d(r). Self-adjointness gives Wμ∞=∫yS dr. Integrate the principal term by parts using I'=w l and both zero endpoints. A numerically safer and more informative identity is
    Wμ∞ = ∫ I [4F Q c/r² − η(cα)'] dr  (static W_lorentz=1).
A nonzero total spin would add a surface term and would also change the exterior source. In flat space without metric or self-recoil corrections, α=c=1 and the monopole feedback term is absent: μ_Newton=η∫w l dr/3=0 exactly for these preparations. This does NOT set the retarded transient to zero.

Prospective prediction: scale the spherical D and Q together by b, keeping η=1, radial shape and the prescribed l(N/N_total) fixed. The extremal radial equilibrium exists throughout this sequence. At lowest order c=1, W=3. The homogeneous interior equation gives (r⁴c₁')'=3r⁴D, while α₁'=N/r². Hence the first surviving moment is second order in compactness normalization:
    μ₂=∫ I(r)[N(r)/r²−r⁻⁴∫₀ʳ s⁴D(s)ds] dr,    μ∞(b)=b² μ₂+O(b³),
where the integrand uses original unit-amplitude monopole inputs. For the primary preparation this coefficient is strictly positive: s⁴<r²s² inside a nonempty ball and I>0. This is a sign and scaling prediction from the source, not a matched dipole. Compare the regular Green identity, a separate weak-form solution with an exterior Robin condition, and the scaled result at b=1,1/2,1/4,1/8. The leading asymptotic approximation need not meet the waveform tolerance at finite compactness. Do not tune the spin law to remove this correction.

