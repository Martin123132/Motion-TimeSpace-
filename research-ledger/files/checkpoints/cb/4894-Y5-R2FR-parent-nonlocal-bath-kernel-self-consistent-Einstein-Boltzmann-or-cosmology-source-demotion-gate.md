# 4894 — Nonlocal bath kernel, reciprocal spectral completion, and cosmology-source demotion gate

Marker: `MTS_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_GATE_4894`

## Decision

Checkpoint 4894 derives the exact causal kernel associated with the 4892–4893
super-Drude FDT spectrum and asks whether it can be inserted into the current
MTS cosmological equations without adding anything else.

It cannot.

The auto-memory kernel itself is healthy and can be localized with two causal
auxiliaries. Three one-sided nonlocal backgrounds can also be reshot. However,
the same positive bath spectrum that owns `gamma_bar=1` and
`sigma_bar=0.3` necessarily generates a large reciprocal compression kernel,
diagonal counterterms, and bath stress. Those terms are absent from the
current parent equations. Consequently, running another high-`k`
Einstein–Boltzmann solve with only the auto-memory replacement would not be a
variation of the proposed parent action.

The present local-in-time bath cosmology is therefore demoted to an explicit
phenomenological closure. Its previous CMB and growth calculations remain
useful conditional diagnostics, but they are no longer candidates for a
fundamental parent prediction until the full reciprocal kernel is supplied.

This demotion does **not** alter the stationary metric-only
EH/Newton/PPN/Maxwell correspondence, and it does not alter the separate galaxy
empirical programme.

## 1. Exact causal auto kernel

Start from

\[
J_{\phi\phi}(\omega)
=\frac{\bar\gamma\,\omega}
 {[1+(\omega/\bar\Lambda)^2]^2}.
\]

The causal friction kernel is the exact cosine transform

\[
\Gamma_{\bar\Lambda}(t)
=\frac{\bar\gamma\bar\Lambda}{2}
(1+\bar\Lambda t)e^{-\bar\Lambda t}\Theta(t).
\]

It satisfies

\[
\int_0^\infty dt\,\Gamma_{\bar\Lambda}(t)=\bar\gamma,
\]

\[
\operatorname{Re}\widetilde\Gamma(\omega)
=\frac{\bar\gamma}{[1+(\omega/\bar\Lambda)^2]^2},
\qquad
J_{\phi\phi}=\omega\operatorname{Re}\widetilde\Gamma.
\]

The kernel localizes without approximation as

\[
\dot r_1=\dot\phi-\bar\Lambda r_1,
\qquad
\dot r_2=\bar\Lambda(r_1-r_2),
\]

\[
F_{\rm mem}=\frac{\bar\gamma\bar\Lambda}{2}(r_1+r_2).
\]

Numerical transforms at three allowed cutoffs and four frequencies reproduce
the analytic response below the validation tolerance.

## 2. Gamma–sigma spectral sum rule

If `gamma` and `sigma` come from one positive bath, the zero-frequency
susceptibilities obey

\[
C_{\phi\phi}=\frac{\bar\gamma\bar\Lambda}{2},
\qquad
C_{\phi\theta}=\bar\sigma,
\]

\[
C_{\theta\theta}\ge
\frac{C_{\phi\theta}^2}{C_{\phi\phi}}
=\frac{2\bar\sigma^2}{\bar\gamma\bar\Lambda}.
\]

The positive rank-one saturation is

\[
J_{AB}=J_{\phi\phi}(1,q)_A(1,q)_B,
\qquad
q=\frac{2\bar\sigma}{\bar\gamma\bar\Lambda}.
\]

At the exact 4893 FDT ceiling

```text
Lambda = 0.251716646,
gamma  = 1,
sigma  = 0.3,
```

the compulsory values are

```text
C_phi_phi       = 0.1258583,
q               = 2.383633,
C_theta_theta   >= 0.715090,
C_theta_theta/(3 Omega_X) >= 4.86456.
```

The completed rank-one matrix has determinant zero and is positive
semidefinite. Setting the absent `C_theta_theta` term to zero instead gives

\[
\det C=-\bar\sigma^2=-0.09,
\]

which cannot represent the positive bath without an explicit diagonal
counterterm prescription.

An equal-coupling completion `q=1` would select

```text
Lambda = 2 sigma/gamma = 0.6,
```

already above the exact FDT ceiling. Any allowed cutoff therefore requires a
strongly asymmetric compression coupling and a large reciprocal diagonal
term.

## 3. Markov incompatibility

At frequency `omega=H0`, the fraction of nominal local friction retained by
the largest FDT-allowed cutoff is

\[
\frac{\operatorname{Re}\widetilde\Gamma(H_0)}{\bar\gamma}
=\frac1{[1+(1/0.2517166)^2]^2}
=3.55047\times10^{-3}.
\]

Thus `99.645%` of the local `gamma=1` damping used by the current cosmological
background is absent at an `H0`-scale frequency. The FDT-compatible spectrum
is non-Markovian on the very timescale where the local background closure was
used.

The conflict is not resolved by choosing a smaller cutoff; that makes the
Markov error larger.

## 4. One-sided background attempt

As a falsification diagnostic, only the auto-memory term was localized while
the old local `sigma theta` source was retained. The quartic coefficient and
initial clock scale were reshot at three allowed cutoffs.

| `Lambda` | `kappa/kappa_local` | max `|Delta E/E|` | result |
|---:|---:|---:|---|
| `0.1` | `1.018325` | `6.4984e-5` | background shoot closes |
| `0.2` | `1.017958` | `6.5013e-5` | background shoot closes |
| `0.2517166` | `1.017776` | `6.5025e-5` | background shoot closes |

This explains why background-only tests did not expose the problem: a
`~1.8%` reshoot of `kappa` hides most of the expansion change.

These rows are not parent predictions. They include auto memory but omit the
reciprocal `theta-theta` kernel, its counterterm rule, and the bath stress in
Einstein's equations.

## 5. Why the high-k run stops here

The 4893 high-`k` split was between a branch preserving the clock equation and
a branch enforcing the momentum constraint. Checkpoint 4894 identifies the
missing variational owner: the reciprocal compression kernel and bath stress.

Running the old equations with only `gamma phi_dot` replaced by
`Gamma*phi_dot` would knowingly preserve the same incomplete source map. It
could produce numbers, but those numbers would not test the full positive
bath parent. The correct high-`k` state vector and Einstein sources change once
`C_theta_theta`, reciprocal cross response, counterterms, and bath stress are
varied.

Accordingly, the high-`k` point calculation and nonlocal FDT covariance are
blocked by a proved action-level omission, not by missing computer time or an
untried parameter scan.

## Arbitration

Derived and closed:

- the causal super-Drude auto kernel;
- its exact two-auxiliary localization;
- a positive rank-one gamma–sigma spectral completion at the sum-rule level;
- three one-sided nonlocal background reshoots.

Not closed:

- the reciprocal `theta-theta` kernel in the parent action;
- a diagonal counterterm and stability prescription;
- the covariant bath stress entering Einstein's equations;
- the corresponding high-`k` constraint system;
- response and FDT noise generated by the same completed kernel.

Decision:

```text
CURRENT MTS BATH COSMOLOGY SOURCE
    -> DEMOTED TO PHENOMENOLOGICAL CLOSURE

MTS STATIONARY METRIC-ONLY LOCAL CORRESPONDENCE
    -> RETAINED UNCHANGED
```

No likelihood should be run on the demoted source as though it were the
fundamental MTS parent.

## Next target

`4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-GR-decoupling-or-bath-cosmology-retirement-gate.md`

