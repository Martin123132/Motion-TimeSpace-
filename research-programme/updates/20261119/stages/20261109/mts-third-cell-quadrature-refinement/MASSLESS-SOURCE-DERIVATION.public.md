> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Source-derived massless monopole/quadrupole decomposition

## Ownership and assumptions

This is an identity of the EXISTING flat ultra-relativistic-fluid approximation, not a newly derived MTS matter law or a validation against a full massless hierarchy. The massive G192 hierarchy is a different sector.

Both saved contexts have zero-based signature[12]=1 (high_ktau_neutrino_approx) and signature[13]=0 (massless multipoles present). The three massless slots are monopole, dipole and quadrupole.

[Operational or machine-specific passage omitted from public reading copy.]

The native source credits [Blas, Lesgourgues and Tram, CLASS II: Approximation schemes](https://arxiv.org/abs/1104.2933v3), JCAP07(2011)034, https://doi.org/10.1088/1475-7516/2011/07/034. Its public abstract confirms the ultra-relativistic-fluid approximation. The exact equations tested here come from the retained local compiled-source chain, not from reconstructing the paper's equations from its abstract.

## Derivation

Let tau be conformal time, N=ln(a), H=dN/dtau, and d,q,p the native massless monopole, dipole and quadrupole. With wave number k, the retained equations are

    d_dot = -k(q + 4z/3)
    p_dot = -3p/tau - d_dot
    d_N + p_N = -3p/(tau H).

The existing GR and Poisson-spatial metric corrections cancel in this sum. In fixed native units U0,U2, r0=d_N/U0 and r2=p_N/U2. At the SAME perturbation state, reference minus retained gives

    U0 Δr0 + U2 Δr2 = -3p Δ[1/(tau H)].

This does not assume the two background times agree. Tau H is dimensionless in the native conformal conventions.

For T=tau H, arithmetic mean denoted by mean:

    ΔT = mean(tau) ΔH + mean(H) Δtau
    Δ(1/T) = -ΔT/(T_ref T_ret).

The verifier evaluates this identity with exact rational arithmetic on the saved binary inputs and rounds the resulting scalar once. This is not an improvement or error certificate for the upstream histories.

For native observable covector a=Tmap^(-transpose)lambda, the pair contribution separates as

    a0 Δr0 + a2 Δr2
      = (a0-a2 U0/U2) Δr0 - (3a2 p/U2) Δ[1/(tau H)].

The first part is the shared monopole transfer; the second is clock damping. A separate residual records the difference from the separately rounded native rates. It is NOT silently discarded or installed as a source repair.

## Verification and localization

All1025MTS and1017baseline points, both metric branches and both backgrounds were tested. Maximum normalized individual sum-law residuals: MTS2.393e-16, baseline2.035e-16 (unchanged algebra gate1e-10). Coordinate-pair refinement reproduction is within2.321e-18 of its conditional source budget.

An independent exact-rational Lagrange-basis integration checks the original quadratic weights within5.255e-16. Independent attribution integral checks are within2.028e-17. The previous attribution retains40passing exact-rational contraction spot checks.

MTS signed fine-minus-coarse changes divided by the channel's conditional source budget:

| Branch/channel | Total | Monopole transfer | Clock damping | Rate residual |
|---|---:|---:|---:|---:|
| GR/Pi | -4.30990089e-5 | -3.53567695e-5 | -1.33967445e-10 | +9.63287716e-11 |
| GR/delta_massless | +4.60594613e-5 | +4.62066569e-5 | +9.19126914e-10 | -4.94414775e-10 |
| Poisson-spatial/Pi | -2.67808599e-5 | -2.19682295e-5 | -8.36411184e-11 | +1.20227013e-10 |
| Poisson-spatial/delta_massless | +2.72271902e-5 | +2.73136020e-5 | +5.46487121e-10 | -6.42269890e-10 |

The monopole-transfer part contributes about82% of net Pi refinement and slightly over100% of delta_massless, with compensating contributions from other coordinates. These are signed contributions, not independent error fractions.

Replacing the pair by this identity WOULD change the MTS integral by at most3.536e-10 of its conditional budget, or2.426e-18 of its saved observable scale. That cannot explain the order1e-5 flags. No replacement was made.

The baseline has different conditioning: hypothetical changes reach4.013e-4 of its tiny budget, but only7.370e-18 of its observable scale. Its unresolved flags remain explicit.

## Next finite-increment law

The same monopole equation implies, at fixed dipole q,

    Δr0 = -(k/U0) [q Δ(1/H) + (4/3) Δ(z/H)].

The next calculation must evaluate z INDEPENDENTLY from the metric/stress equations. Rearranging the same monopole rate to obtain z would be circular.

For the existing driver representation z=X/D, an exact finite-background identity is

    Δ(z/H) =
      [mean(DH) ΔX - mean(X) Δ(DH)] / [(DH)_ref (DH)_ret].

Derive X and D from the actual retained stress terms, then test a frozen subset before any full evaluation. No smoothing cutoff, new fit parameter or unbounded sequence of grid doublings is justified by the present results.

