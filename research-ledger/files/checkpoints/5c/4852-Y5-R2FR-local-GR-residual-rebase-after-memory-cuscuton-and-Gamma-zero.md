# 4852 Y5 R2FR local-GR residual rebase and linearized source-charge closure

**Status:** The private local correspondence branch now closes the leading Newtonian source-charge mismatch rather than leaving `Pi_M/H_tau/M_H_ref` as an assumed identity. The same linearized Einstein equation that gives Poisson also makes the first-order ADM/Hamiltonian surface mass equal the Hilbert volume mass. Coupling drift, source-only weights, active `Gamma`, stationary coherent-load stress and the Newton-order source-charge residual are therefore removed from the live private Newton vector. Strict parent derivation of the EH/coframe block, Maxwell/Hodge/current ownership, post-Newtonian source charge, boundary/radiation and non-source PPN remain open.

**Decision:** `LOCAL_GR_RESIDUAL_REBASED_LINEARIZED_ADM_HILBERT_SOURCE_CHARGE_EQUALITY_DERIVED_ACTIVE_GAMMA_AND_STATIONARY_MEMORY_REMOVED_PARENT_EH_MAXWELL_PPN_OPEN_NONCLAIM`.

Marker: `LINEARIZED_ADM_HILBERT_SOURCE_CHARGE`.

## 1. Branch and scope

This derivation is inside the explicit private correspondence branch:

\[
S_{\rm loc}=\frac{c^3}{16\pi G_{\rm cal}}
\int\!\sqrt{-g}\,R\,d^4x
+S_{\rm src}[g,e,A,\psi,\theta]+S_{\rm silent}.
\]

The assumptions used here are:

1. the 4072 Cartan/EH block is adopted as private correspondence infrastructure, not claimed derived from primitive MTS;
2. matter and any ordinary EM contribution are varied from one observed-frame source action to form `T_H`;
3. `kappa_cal=8*pi*G_cal/c^4` is constant and source-blind on the 4654 private branch;
4. the source is stationary and asymptotically flat at the order used, with compact support or finite-energy falloff;
5. active `Gamma` and coherent-load memory obey the 4845/4847 local zero theorems;
6. no orbital `GM` is used as an input.

This is not a derivation of the numerical value of `G`, a global parent-action proof, a Maxwell normal-form proof, or a full PPN proof.

## 2. Source coupling and Poisson

At first weak-field order,

\[
G^{(1)}_{00}=\kappa_{\rm cal}T^H_{00},
\qquad
\kappa_{\rm cal}=\frac{8\pi G_{\rm cal}}{c^4}.
\]

For

\[
g_{00}=-(1+2\Phi/c^2),
\qquad
T^H_{00}=\rho_Hc^2+O(\epsilon^2),
\]

the EH identity `G00^(1)=2 nabla^2 Phi/c^2` gives

\[
\boxed{\nabla^2\Phi=4\pi G_{\rm cal}\rho_H.}
\]

No separate source-normalization coefficient is available: `G_cal` multiplies the same Hilbert source that defines `rho_H`.

## 3. Gauss mass is the Hilbert volume mass

For any enclosing surface `S=partial V`, define

\[
M_\Phi(S):=\frac{1}{4\pi G_{\rm cal}}
\oint_S\nabla_i\Phi\,dS^i.
\]

The divergence theorem and the Poisson equation give

\[
\boxed{
M_\Phi(S)=\int_V\rho_H\,d^3x
=\frac{1}{c^2}\int_VT^H_{00}\,d^3x
}
\]

at first perturbative order. For stationary finite-energy Maxwell fields the volume is the complete slice, not merely the material body; exterior field energy must be included once in `T_H`.

## 4. Hamiltonian/ADM surface mass

The linear ADM mass is

\[
M_{\rm ADM}^{(1)}
=\frac{c^2}{16\pi G_{\rm cal}}
\oint_S(\partial_jh_{ij}-\partial_ih_{jj})n^i\,dS.
\]

In the static isotropic weak field,

\[
h_{ij}=-\frac{2\Phi}{c^2}\delta_{ij},
\]

so

\[
\partial_jh_{ij}-\partial_ih_{jj}
=\frac{4}{c^2}\partial_i\Phi.
\]

Therefore

\[
\boxed{
M_{\rm ADM}^{(1)}
=\frac{1}{4\pi G_{\rm cal}}\oint_S\nabla_i\Phi\,dS^i
=M_\Phi(S)
=\int_V\rho_H\,d^3x.
}
\]

This proves the Newton-order `Pi_M/H_tau` glue that 4171 and 4839 previously took as a branch condition.

The ADM/Hamiltonian result is standard Hamiltonian GR structure; the relevant primary sources are [Arnowitt, Deser and Misner](https://arxiv.org/abs/gr-qc/0405109) and the covariant Noether-charge treatment of [Iyer and Wald](https://arxiv.org/abs/gr-qc/9403028).

## 5. Unit correction to the old `M_H_ref` notation

For an asymptotic time translation, the Hamiltonian charge is energy:

\[
H_\tau-H_{\rm ref}=E_{\rm ADM}^{(1)}=M_{\rm ADM}^{(1)}c^2.
\]

Thus, with explicit SI units,

\[
\boxed{
M_{H,{\rm ref}}^{(1)}
:=\frac{H_\tau-H_{\rm ref}}{c^2}
=M_{\rm ADM}^{(1)}
=\int_V\frac{T^H_{00}}{c^2}\,d^3x.
}
\]

The older line `M_H_ref=H_tau-H_ref` is valid only in `c=1` units or if `H_tau` was pre-divided by `c^2`. This checkpoint supersedes that ambiguous notation.

## 6. What is actually zero

The first-order source-charge residual is now a theorem:

\[
\epsilon_{\rm src}^{N}
:=\frac{M_{\rm ADM}^{(1)}-\int\rho_Hd^3x}
{M_{\rm ADM}^{(1)}}=0.
\]

Together with previous private theorems:

\[
\delta_\kappa=0,
\qquad E_{\rm source\ prefactor}=0,
\]

\[
\Gamma_{\rm active}=\Pi_{\rm active}
=\Sigma_{\rm active}=q_\Gamma=0,
\]

\[
T^{\rm mem}_{\mu\nu}=0,
\qquad \mathcal E^{\rm mem}_{\tau,\mu}=0
\]

on the stationary local branch. At cosmological subhorizon scales the coherent-load Poisson correction is additionally `O(H^2 a^2/k^2)`.

## 7. Nonlinear source charge is not bare `T00`

The preceding equality is first-order Newtonian, not an exact nonlinear identity. For a stationary GR solution the exact mass is controlled by the ADM/Komar/Tolman charge. With conventional Killing normalization its matter form is

\[
M_{\rm K/T}
=\frac{2}{c^2}\int_\Sigma
\left(T_{\mu\nu}-\frac12Tg_{\mu\nu}\right)
n^\mu\xi^\nu\,dV,
\]

subject to the field equations, asymptotic conditions and boundary terms. Pressure, Maxwell stress, gravitational binding and any surviving nonminimal field contribution matter at post-Newtonian order. Therefore `E_source_charge_PN` remains live; replacing it by `integral T00/c^2` would be a new closure assumption.

## 8. Rebased residual vector

The 4650 vector

```text
(E_EH_action_owner, E_kappa_drift, E_source_owner, E_source_label,
 E_metric_coframe_fork, E_EM_metric_source, E_tail_selector,
 E_boundary_flux, E_domain_projector, E_PPN_transfer)
```

now reduces on the private Newton branch as follows:

```text
theorem-zero/private-closed:
  E_kappa_drift
  E_source_label
  E_source_owner at first Newton order
  active-Gamma part of E_tail_selector
  stationary-H-load part of E_tail_selector

surviving:
  E_parent_to_EH
  E_EM_normal_form
  E_source_charge_PN
  E_PPN_non_source
  E_boundary_domain_radiation
  E_Gamma0_background
```

The ADM surface charge is not a boundary leak and must not be set to zero. Only outgoing radiative or transition flux is a residual.

## 9. Machine smoke

The runner evaluates a uniform spherical source at three exterior radii. It computes the Poisson flux, ADM mass and Hamiltonian energy independently and verifies

```text
surface flux/(4*pi*G) = source volume mass
(H_tau-H_ref)/c^2 = ADM mass
```

to floating-point precision. This is a theorem smoke, not empirical evidence.

## 10. Verdict

This checkpoint makes a real reduction:

- the leading Newton source coupling is no longer a symbolic missing row inside the private correspondence branch;
- the `c^2` unit ambiguity is repaired;
- the nonlinear source-charge burden is separated from the first-order Newton theorem;
- the first surviving same-source target is now Maxwell/Hodge/current ownership and stationary Poynting routing.

Strict MTS-to-GR derivation remains unproved until the local EH/coframe action itself is obtained from the parent motion-time-space grammar.

## Next target

`4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md`

