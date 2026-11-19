# The wavelength change acts on the same coupled operator

The background trajectory and thermodynamics are independent of the comoving perturbation wavelength in this linear test. Keeping them fixed is therefore appropriate; copying the perturbation coordinates is not. In particular the metric constraints contain inverse powers of k, the streaming terms contain k*v, and the heavy canonical coefficients depend on the physical gradient. All are reevaluated by the retained operator with its new k. `ModePort` changes that input before the canonical block is constructed, not after an old block has been evaluated.

The new controlled preparation retains the same physical monochromatic seed prescription: neutrino F0=4Theta, Theta=1e-6, higher multipoles zero, specified baryon/cold perturbations, and the inherited live-D0 heavy constraints. The physical density/current targets include the newly evaluated gauge conversion. The four canonical coordinates are solved from those constraints, including the live metric derivative. They are not transferred from k=5. This is a prescribed linear initial-value control, not a derivation of primordial amplitudes, a quantum vacuum or a galactic occupation.

## Same angular elimination, new streaming phase

The retained equation is

    partial_tau F + i k v mu F = -4 k z/3 - (8 k sigma/3) P2(mu).

For s(q,tau)=k integral[tau0,tau]v(q,t)dt, its exact characteristic solution gives

    F_l = 4Theta j_l(s) + integral[-4kz j_l(Delta s)/3 - 8k sigma K_l(Delta s)/3]dt,
    K_l = b_l j_l - a_l j_(l+2) - c_l j_(l-2).

Coefficients and the finite-interval Volterra derivation are retained from the preceding sealed stage. With l=17, this supplies the missing boundary in F16'=kv(16F15-17F17)/33. Nothing in this derivation fixes k=5. Nevertheless the actual causal integral, metric history, approximation regimes and initial constraints must be regenerated for k=1; replacing the phase of a saved k=5 trajectory would not be equivalent.

The bootstrap's asymptotic boundary supplies only the initial metric iterate. An accepted result must evolve the whole coupled system using the characteristic boundary and reproduce both its low source moments and supplied F17 from its own final metric history. One iteration is sufficient only if those independent final-history tests pass at the unchanged tolerance. A second explicit iteration is permitted if required, not presumed necessary or automatically successful.

## Conserved sources and metric checks

The same positive momentum distribution supplies background and perturbations. Its coefficients d_i=A*B_i/(a^2*v_i), j_i=A*B_i/a^2 and p_i=A*B_i*v_i/a^2 obey d_i'=-H(d_i+p_i), j_i'=-2H*j_i and S_nu=4sum(d_i)/3. Consequently

    D_nu' + H(D_nu+3P_nu) + k Q_nu + k z S_nu = 0,
    Q_nu' + 2H Q_nu - k P_nu + 2k Pi_nu/3 = 0.

These arbitrary-state row identities are tested on the new mode's actual matrix, including its affine boundary coordinate. The boundary acts on l16 and cannot excuse a failure in l0/l1 conservation. Independent metric and scalar-source identities use the same live coupled state with16/32derivative stencils. This separates conservation compatibility from accuracy of the angular or time approximation.

The original2e-5numerical and1e-10algebra gates remain fixed. Peak-normalized source comparisons and absolute source amplitudes are reported separately. Passing this mode would establish another controlled prediction of the retained equations, not an observational fit or an all-wavelength/uniform-time theorem.
