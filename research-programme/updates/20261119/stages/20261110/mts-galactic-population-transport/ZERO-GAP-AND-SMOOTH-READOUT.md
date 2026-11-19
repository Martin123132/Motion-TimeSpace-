# Physical zero-gap qualification and a gap-free response observable

The full Newtonian bound spectrum is not generally gapped away from escape.
For an isolated finite gravitating mass the potential has a -GM/r tail. Trial
waves supported on widely separated large-radius shells have kinetic energy
of order hbar^2/(m R^2) and potential energy of order -GMm/R. Infinitely many
disjoint shells therefore provide negative-energy trial directions tending
to zero. The familiar point-mass Coulomb spectrum is an explicit example.
A finite numerical box does not turn this physical accumulation into a
positive continuum gap.

Consequently the gapped-projector rate estimate in DERIVATION.md applies to
a deliberately separated deep-bound subset, or another genuinely isolated
spectral cluster. It must not be advertised as a uniform all-halo capture
bound. The final functional Tr(P_final U Gamma_i U_dagger) is still a defined
readout whenever the final projector is defined; its time derivative needs
the differentiability/domain hypotheses. Spatial-aperture flux requires no
spectral gap and remains the direct count-in-volume observable.

## Constructive alternative: smooth escape-energy readout

For a fixed positive resolution sigma and specified escape reference E_esc,
define

    w_sigma(E)=1/2-arctan[(E-E_esc)/sigma]/pi,
    W=w_sigma(H),  N_w=Tr(W Gamma).

This is an energy-resolution-weighted count, not a sharp bound mass, a new
physical distribution, a temperature, a fitted coupling or a claim that
halo particles obey Fermi statistics. It is a declared observable. Freeze
sigma before using it; changing sigma is a resolution study, not model fitting.

For the closed NR evolution, [W,H]=0, so

    N_w_dot=Tr(Dw_H[H_dot-E_esc_dot I] Gamma)

with constant sigma. In an instantaneous eigenbasis the Fréchet derivative is

    (Dw_H[V])_ij =
        [w(E_i)-w(E_j)]/(E_i-E_j) V_ij,  E_i != E_j,
    (Dw_H[V])_ij = w'(E_i) V_ij,          E_i = E_j.

This stays finite through degeneracies and threshold crossings. It must
retain off-diagonal matrix elements, not merely differentiate eigenvalues.

For a bounded self-adjoint V, use the spectral identity

    arctan(A/sigma)=integral_0^infinity exp(-sigma s) sin(s A) ds/s.

Duhamel differentiation of exp(+/-i s A) bounds the norm of the derivative
of sin(s A) by s||V||. It follows, independently of matrix dimension, that

    ||Dw_H[V]|| <= ||V||/(pi sigma),
    boxed: |N_w_dot| <= N ||H_dot-E_esc_dot I||/(pi sigma).

The integral argument is directly valid for bounded regulated operators.
It extends to self-adjoint A with bounded perturbation V using the unitary
Duhamel identity and the derivative integral; an unbounded perturbation
requires its own domain/relative-bound control. In a fixed local patch with
bounded Phi_dot, V=m_h Phi_dot is bounded. The expanding kinetic derivative
is not automatically bounded on the continuum Hilbert space. A finite
Galerkin result alone does not settle that continuum issue.

Unlike the separated-projector bound, this estimate has no spectral-gap
denominator. The price is explicit energy smoothing: it is not permission
to rename N_w as the exact number of permanently bound particles.

## Frozen additional controls

Use sigma=.2 and a threshold crossing H=diag(-1,t) at t=0, initial occupation
diag(0,1). The prediction before evaluation is N_w=.5 and
N_w_dot=-1/(pi sigma), saturating the bound. The sharp projector must refuse
the same crossing.

Test thirty fixed-seed noncommuting Hermitian operators against independent
central differences, and test positivity, [W,H]=0, the derivative norm bound
and energy-unit rescalings. Algebra gate1e-10 and numerical gate2e-5 remain
unchanged. These tests validate the new readout, not an all-halo formation law.
