> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What an uncertain array can learn about the retained occupied field

## Fixed signal, changing question

The sealed timing derivation (not bundled here) supplies the Earth, pulsar and integrated pressure-curvature terms. There is no change of kinetic term, gravitational coupling, mass or occupation in this stage. [Protocol](PROTOCOL.md) fixes the roster, preparation, noise scale and unblinding rule in advance. All ten matches of the [pinned Discovery EPTA directory](https://github.com/nanograv/discovery/tree/18ab4c010b2e8e09eb81fdb145b296da024659fa/data/epta_dr2) to the saved 26 real geometries are used, without timing residuals. The two earlier pilot inputs are reused instead of counted twice. Single-pulsar hyperparameters and timing designs come from the same public source and are empirical nuisance inputs.

For receiver j the signal has a complex degree-two envelope over the same MJD reference and carrier. Its six real coefficients multiply the three powers of normalized time times cosine and sine. At distance D define a 6×2 matrix Bⱼ(D) mapping (cos φ,sin φ) to those coefficients for the unknown *common* initial phase. B includes the whole line integral on its actual past ray; it is not just an arbitrary Earth-minus-pulsar phase. D is drawn independently across pulsars according to the stated distance-error scenarios. Array geometry uncertainties and the actual physical state are different: an uncertain propagation phase is not proof of decoherence in the field.

## Eliminate timing, red processes and the clock in the correct order

For each pulsar, whiten by its packaged fixed intrinsic covariance Nⱼ (backend radiometer terms plus its own red, dispersion and chromatic modes), then project out the whitened published timing design. Denote this map PⱼWⱼ. It need not be square or invertible on timing parameters. Let X=diag(PⱼWⱼXⱼ) contain the six signal columns for every pulsar. Let F=diag(PⱼWⱼFⱼ) contain scaled common Fourier columns. With directions nᵢ, x=(1−nᵢ·nⱼ)/2 and Hᵢⱼ=1/2−x/4+(3/2)x ln x for distinct pulsars, Hᵢᵢ=1. The independent-process control uses H=I. The timing-marginal signal information matrix is

    G₀ = XᵀX − XᵀF [(H⁻¹⊗I)+FᵀF]⁻¹ FᵀX.

This is block Gaussian elimination, not a white-noise projection followed by a sum of single-pulsar S/N values. An independent direct inversion of the full covariance before marginalizing a timing model checks the order on a three-source, real-cadence submatrix. For the repeated two-column Earth-clock design E in coefficient space, G=G₀−G₀E(EᵀG₀E)⁻¹EᵀG₀; hence GE=0. The dipole control adds sine and cosine columns scaled by each Cartesian sky direction. Killing a nuisance removes only indistinguishable components; it is not adding independent observations.

The published [EPTA common-process analysis](https://doi.org/10.1051/0004-6361/202346844) motivates a *fixed scenario* A=2.5×10⁻¹⁵ at 1/yr, γ=13/3, with 1.8 and 3.2 as sensitivity endpoints. This study is not the release likelihood and does not propagate its full posterior. The ordinary grid uses frequencies j/T with spacing 1/T, sine and cosine spectral powers A² year³(f·year)^(−γ)df/(12π²). The **primary** retains j=2…30 and replaces the first atom by integration on [0,1.5/T]; the higher mid-bins then touch without overlap. This is an explicit model scenario, not an assertion that the release used this grid. In the low cell subtract the constant, linear and quadratic Taylor terms, already in every timing design. The surviving sine is O(f³), cosine O(f⁴), so the pair covariance has a finite low-frequency integral for γ<7. Use Jacobi weights proportional to f^(6−γ); stable series prevent artificial cancellation near zero. Check 8, 12 and 16 low-cell nodes, and 60 high harmonics. Repeating the subtracted polynomial with huge low-frequency power before fitting would obscure the finite answer.

## Unknown distances: marginalize rather than pick a good configuration

For stacked template b=B(D)v with v uniform on the unit circle, E[b]=0. If μⱼ=E_D[Bⱼ] and μ stacks these matrices, then exactly

    S = E[bbᵀ] = { μμᵀ + blockdiag(E[BⱼBⱼᵀ]−μⱼμⱼᵀ) } / 2.

Only one-dimensional distance integrals are needed for this full-array second moment. The dominant phase error at this pole is kσ_D where the light wavelength is 20.96 pc, not the much longer nonrelativistic matter de Broglie wavelength. A narrow Gaussian error with slowly varying pulsar envelope multiplies its coherent phasor by exp(−k²σ_D²/2); half amplitude requires σ_D≈3.93 pc. We also compute the actual averaged *ground* pulsar-plus-path phasor after removing the Earth term, including the finite ±3σ interval and the changing envelope. A truncated Gaussian does not have an exponentially small transform at arbitrarily high frequency, so the untruncated formula alone would overstate how perfectly the phase is erased. Compare G-projected signal covariance to a distinct controlled model with a separate random phase per pulsar after the common Earth clock is removed. This is a test of second moments only, not a proof these models have identical distributions or that an occupied number-diagonal state has no fluctuations.

## Detectability and a bound independent of our statistic

Take the sufficient score h to have covariance G and mean Gb under an exact fixed-template injection. For amplitude multiplier a, marginalization of exp(a bᵀh−a² bᵀGb/2) leaves Q=hᵀSh as the first nonconstant data-dependent term. Thus Q is locally optimal in *power* a² for the specified symmetric ensemble; at finite amplitude it need not be the exact optimal likelihood ratio. Under the null Q is a sum of independent χ²₁ variables weighted by the positive eigenvalues of G¹ᐟ² S G¹ᐟ². A separate simulation constructs noisy individual arrival times from detector noise, intrinsic processes, shared correlated Fourier coefficients, arbitrary timing nuisance offsets and injected signals, and repeats the full analysis. No measured residual is used for any of these figures.

Let r²=bᵀGb and let z=Φ⁻¹(1−α), Φ the standard normal CDF. An oracle told the exact distance and phase of a signal has conditional detection probability Φ(r−z) at size α. Any test of the same Gaussian data, invariant to the declared timing/clock nuisances and ignorant of the signal direction, cannot beat this bound for that b. For x=r², f(x)=Φ(√x−z) has

    f″(x)=−φ(√x−z)[x−z√x+1]/(4x^(3/2)).

At α=.05, z≈1.645<2; the square bracket is strictly positive for every r≥0. Jensen therefore yields a distribution-wide bound for **any** such test,

    mean power ≤ E[Φ(r−z)] ≤ Φ(√tr(GS)−z).

Consequently 80% mean power needs tr(GS)≥[z+Φ⁻¹(.8)]² before accounting for the cost of *finding* the template. This is not a bound on all possible observations, on residual data at other baselines, or on tests that know the terrestrial clock externally. It requires the stated Gaussian null, noise covariance, MTS preparation and distance ensemble. The CSV also retains simpler looser bounds from a Lipschitz/Taylor inequality for cross-check. Factors scaling a template or its information are not automatically factors by which to increase the physical halo mass: a new occupation would require re-solving the self-gravitating state.

## Fixing false alarms when the common noise amplitude is uncertain

As a secondary robustness repair, keep the score and filter fixed at A₀. If the true amplitude changes while its spectrum shape and spatial covariance stay fixed, the actual covariance of h is G+(A²/A₀²−1)Δ with Δ positive semidefinite, obtained by applying the actual score map to the correlated Fourier factors. For A₁≤A₂ this orders the score covariance in the positive-semidefinite sense. The null quadratic score eigenvalues are ordered too (apply the same congruence with S¹ᐟ²); coupling to identical independent χ²₁ variates proves stochastic domination. A threshold calibrated at A_max thus controls upper-tail false alarms throughout the interval, not just at sampled amplitudes. It does not protect against arbitrary spectral slopes, noise families, or misestimated individual-pulsar parameters.

Compute weighted χ² tails by characteristic-function inversion. For positive eigenvalues λᵢ and threshold q, the phase is ½Σatan(2tλᵢ)−qt and modulus Π(1+4t²λᵢ²)⁻¹ᐟ⁴. Integrate the sine times this modulus over πt, adding ½. The neglected absolute tail beyond T is bounded using the leading m eigenvalues by [2/(mπ)] Π(2λᵢ)⁻¹ᐟ² T^(−m/2); choose a sufficient truncation and check against ordinary χ² quantiles and independent draws. The worst-amplitude cutoff targets .05−10⁻⁶ for numerical margin. This conservative single cutoff is **not** a claim to have measured or calibrated the noise amplitude on these ten sources.
