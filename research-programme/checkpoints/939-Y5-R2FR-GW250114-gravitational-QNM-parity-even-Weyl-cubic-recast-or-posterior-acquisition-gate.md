# 4923 - GW250114 gravitational-QNM Weyl-cubic recast and compact-domain gate

**Status:** The official GW250114 companion release has been acquired,
checksum-verified and converted into two source-backed, branch-conditional
posteriors for the corpus parity-even Weyl-cubic coefficient. Both
polarizations include GR at 90 percent. The new dimensionless envelope is
much tighter than the GW170608 interval, but it still misses the declared
one-percent compact-domain gate. No finite MTS coefficient or polarization
excitation law is derived.

Marker: MTS_GW250114_GRAVITATIONAL_QNM_WEYL_C3_RECAST_4923.

## 1. Official release and exact sample selection

The complete 1,671,496,586-byte GW250114 data release was downloaded from
Zenodo DOI 10.5281/zenodo.17018009. Its MD5 is
8778398081EF5713E4C762169C9FD65C, exactly matching the release record.

The primary product is the released pSEOBNRv5PHM HDF5 posterior, not a
digitized figure and not the broader generic PyRing comparator. It contains
40,776 samples. The paper's own plotting notebook reports the pSEOB
deviations after

    domega440 < 0.8,
    dtau440 < 0.8.

This leaves 17,742 samples. Removing the 23 samples with remnant spin above
the gravitational-QNM source's chi=0.7 endpoint leaves 17,719 samples, or
99.8704 percent of the paper-reporting selection.

The theory-supported posterior summaries are approximately

    deltahat_f220   = 0.016 with 90-percent range about [-0.007, 0.038],
    deltahat_tau220 = -0.004 with 90-percent range about [-0.10, 0.09],
    chi_f            = 0.678 with 90-percent range [0.662, 0.691],
    M_f              = 68.27 solar masses with range [67.04, 69.19].

The released priors on domega220 and dtau220 are independent uniform
distributions on [-0.8, 2.0]. Their joint posterior and its correlation with
remnant spin are retained.

## 2. Exact gravitational-QNM coefficient map

For the corpus parity-even invariant,

    alpha_ev = alpha_bar1 = a_plus/M^4
             = s_plus (ell_plus/M)^4.

The gravitational-QNM source gives, for each parity-even polarization,

    omega = omega_Kerr + alpha_ev deltaomega_branch(chi)/M,
    deltaomega_branch(chi) = sum(n=0..12) c_n chi^n.

Supplemental Table 1 supplies the full complex coefficient vectors for the
(2,2,0) mode. The numerical Kerr baseline is evaluated with qnm 0.4.4.
At chi=0.7 the imported polynomials reproduce the source's convergence table:

    polar plus:  deltaomega =  0.21994 - 0.29291 i,
    axial minus: deltaomega = -0.22099 + 0.25098 i.

The released pSEOB convention is

    f220   = f220_GR (1 + deltahat_f220),
    tau220 = tau220_GR (1 + deltahat_tau220).

Linearizing the complex frequency therefore gives the exact conversion

    deltahat_f220
      = alpha_ev Re(deltaomega_branch)/Re(M omega_Kerr),

    deltahat_tau220
      = -alpha_ev Im(deltaomega_branch)/Im(M omega_Kerr).

Near the median spin, the two theory lines are approximately

    polar plus:  (deltahat_f, deltahat_tau)
                 = alpha_ev ( 0.4612, -3.4839),

    axial minus: (deltahat_f, deltahat_tau)
                 = alpha_ev (-0.4332,  2.5540).

This is a coefficient-level map. It is not a generic-QNM relabelling.

## 3. Why there are two answers

The parity-even cubic operator breaks the Kerr axial/polar isospectrality.
The theory source predicts two different complex frequencies. The released
pSEOB model fits one generic complex frequency per harmonic, and the current
MTS parent does not predict which polarization is excited or their relative
weights.

Accordingly, checkpoint 4923 computes two conditional posteriors:

- polar-plus, assuming that branch supplies the fitted 220 shift;
- axial-minus, assuming that branch supplies the fitted 220 shift.

They are not averaged, multiplied or selectively chosen. The pSEOB 440
posterior is also excluded because arXiv:2307.07431 supplies cubic
coefficients for 220 and 330, not 440.

## 4. Joint-spin posterior-density recast

The primary calculation constructs a three-dimensional Gaussian KDE in
(deltahat_f220, deltahat_tau220, chi_f). For each alpha_ev it evaluates the
corresponding theory manifold and integrates over 0.63 <= chi_f <= 0.70.
The smoke prior is uniform on -0.15 <= alpha_ev <= 0.15; posterior support at
those edges is negligible.

The resulting 90-percent branch-conditional intervals are

    polar plus:
      alpha_ev = 0.00848,
      90 percent [-0.01687, 0.03195],
      MAP 0.0078,
      P(alpha_ev>0) = 0.713,
      Delta chi-square proxy over GR = 0.372;

    axial minus:
      alpha_ev = -0.01302,
      90 percent [-0.04306, 0.02104],
      MAP -0.0126,
      P(alpha_ev>0) = 0.255,
      Delta chi-square proxy over GR = 0.531.

Both intervals include alpha_ev=0, and neither improves the line likelihood
over GR by even one chi-square unit. Under the explicitly chosen
[-0.15,0.15] prior, the corresponding density-at-zero diagnostics favor GR
over the one-parameter line by factors about 6.6 and 4.7. Those factors are
prior-width dependent and are not promoted as model-selection claims.

The correct result is therefore a tighter upper envelope, not a detection.

## 5. Robustness envelope

A separate sensitivity matrix varies

- the KDE bandwidth by factors 0.75, 1 and 1.25;
- remnant spin over its 5th, 50th and 95th percentiles;
- the entire complex QNM shift by plus or minus five percent, matching the
  theory paper's conservative accuracy statement near chi=0.7.

Every resulting 90-percent interval still contains GR. The largest absolute
90-percent endpoint is about 0.054. This conservative envelope is used only
for domain and weak-field safety checks; it is not a unique posterior.

At the median remnant mass, the nominal branch envelopes correspond
illustratively to

    polar plus:  ell_plus about 42.6 km,
    axial minus: ell_plus about 45.9 km.

Using the robust alpha endpoint and the 95th-percentile remnant mass gives an
illustrative envelope of about 49 km. The conversion is deliberately labelled
illustrative because the KDE recast does not perform a full four-dimensional
mass-coupling waveform reanalysis.

## 6. Compact-domain decision

For continuity with checkpoint 4922, use the Schwarzschild-horizon control
proxy

    epsilon_h = (3/4) abs(alpha_ev).

The nominal branch endpoints give approximately

    polar plus:  epsilon_h <= 0.02396,
    axial minus: epsilon_h <= 0.03229.

The robust envelope gives epsilon_h about 0.040. These are dramatically
smaller than the old positive GW170608 endpoint epsilon_h=2.115, but they
remain roughly four times above the declared one-percent gate.

The posterior probability lying inside abs(alpha_ev)<0.013333 is about
54 percent on the polar-plus recast and 40 percent on the axial-minus recast.
That is substantial support for a controlled branch, but not the 90-percent
certificate required here.

Therefore

    weak invariant-vacuum GR    -> retained;
    compact-vacuum GR           -> not promoted;
    compact-matter GR           -> not promoted;
    full MTS-to-GR              -> not promoted.

The robust physical-length smoke envelope leaves the inherited Earth
acceleration and Galileo clock residuals below a few times 10^-25, so it does
not threaten the weak local certificate.

## 7. What is closed and what is not

Closed:

- official GW250114 release acquisition and checksum;
- exact action coefficient to gravitational-QNM coefficient identity;
- exact complex-frequency to pSEOB frequency/damping conversion;
- source-backed 220 coefficients through chi=0.7;
- two branch-conditional joint-spin posterior-density recasts;
- explicit 440 and scalar-sector exclusions;
- weak-versus-compact domain decision.

Not closed:

- finite parent prediction of zeta_plus, including sign and scale;
- parent excitation or mixing weights for the two polarizations;
- a 440 cubic-QNM coefficient;
- a waveform-level reanalysis with the modified two-frequency ringdown;
- compact-matter interiors and EOS matching;
- parity-odd matching;
- MTS-to-Maxwell and calibrated source coupling.

The next target returns to derivation rather than collecting another bound:

4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md

The task is to calculate the finite zeta_plus and its sign from the already
selected parent determinant/renormalization prescription, or prove that an
independent finite counterterm remains part of the theory definition. The
GW250114 interval is then a target for that prediction, not a substitute for
it.

No GitHub action or public claim is authorized.

## Sources

- https://doi.org/10.5281/zenodo.17018009
- https://arxiv.org/abs/2509.08099
- https://arxiv.org/abs/2307.07431
- https://github.com/duetosymmetry/qnm
- post-checkpoint-work/source-intake/parent_coupling/4923/PROVENANCE.md
- post-checkpoint-work/scripts/Y5_R2FR_4923_GW250114_QNM_recast.py
- post-checkpoint-work/4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-bound-or-compact-vacuum-GR-domain-gate.md
