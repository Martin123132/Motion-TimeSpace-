# Live preparation and a metric residual that cannot be assumed away

Primes mean conformal-time derivatives. Use the preceding source bridge
and canonical closure conventions, with real coupled state Y, Y'=A(t)Y.
Write Phi=fY, Psi=gY, C=Psi+3Phi=cY, mu=am,
a0=lambda0-H and rate=lambda0+lambda_k.

## Forced preparation from the operator, not a supplied metric history

For any row r(t), define the total row derivative L(r)=r'+r A. Therefore

    C'=L(c)Y,
    C''=[c''+2c'A+c A'+c A^2]Y.

The leading response row and next correction are

    d0=[a0 L(c)-2mu^2 g]/rate,
    d1=-L(d0)/rate,
    L(d0)={a0' L(c)+a0 L^2(c)-2(mu^2)'g-2mu^2 L(g)}/rate
           -(rate'/rate) d0.

These follow from the existing exact affine response equation

    D'+rate D=C'a0-2mu^2Psi+C R0-Rk Z.

The D0/D01 conditional preparations initially set

    V+a0 C=d0 Y, or V+a0 C=(d0+d1)Y.

The nonzero R0/Rk terms are NOT silently deleted from subsequent unrestricted
evolution or conservation accounting. D0/D01 are explicitly truncated
preparations, not exact particular solutions. Impose these two real rows
along with the two retained physical density/current rows, holding all
91 rest coordinates fixed. Check invertibility and conditioning. An
adiabatic expansion cannot be assumed to improve an arbitrary free fast
state; test the resulting preparation and evolution instead of asserting it.

The scalar derivatives a0', rate' and (mu^2)' can be obtained directly from
the same homogeneous-background Taylor jets used by the retained W2
carrier. Native c', c'', A' are evaluated by numerical differentiation
of current-state operators at known background times, with nested-stencil
checks. No future species state or metric trajectory is sampled.

## Generalized constraint-defect identity

Let S=8piG a^2(rho+p) for the carried total background and define

    Ephi=Phi'+H Psi-Q/(2k),
    EH=H'-(H^2-S/2),
    ED=D'+H(D+3P)+kQ-3S Phi',
    EQ=Q'+2HQ-k(P+S Psi-2Pi/3),
    Ec=2k^2Phi+D+3H Q/k.

Direct differentiation gives, without imposing the momentum equation,

    Ec'+H Ec = ED+3H EQ/k+3EH Q/k+(2k^2+3S) Ephi.

The earlier identity assumed Ephi=0. Since this implementation eliminates
the Hamiltonian constraint algebraically, Ec is near zero by construction;
that alone does not prove momentum conservation. Ephi must be calculated
from L(f)Y, not from the native observer's momentum-law readout. The total
source combination needed on the right does not require an assumed rest
pressure because it cancels:

    J=ED+3H EQ/k+3EH Q/k
     =D'+HD+kQ-3S Phi'+3H Q'/k+6H^2Q/k
       -3H S Psi+2H Pi+3EH Q/k.

Compute the heavy contribution separately with its action-derived P_h.
The remaining J_rest=J-J_heavy identifies any rest hierarchy or gauge/
background contribution; it is not proof of each individual rest species'
conservation. Compare the same independent Ephi/J diagnostics for both
retained native heavy and cold controls.

For the new block S=S_native-R_native_heavy+S_carried_heavy. Keep this
correction in EH, Newtonian gauge transformations and all total sources.
Tiny W2 background defects and numerical differentiation errors remain
distinct from exact identities and from observational evidence.
