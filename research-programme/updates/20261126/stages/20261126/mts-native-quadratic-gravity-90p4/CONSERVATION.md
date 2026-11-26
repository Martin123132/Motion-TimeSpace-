# A pressure-free consistency test on the linear metric

Use the flat scalar sector of the retained native code. Let E=dgrho, J=dgq, Π=dgpi, R=grho and p=gpres in the code's conformal, gravitationally weighted units, k the **incoming** wave number, ηk=etak, H=adotoa and X=(E/2+k ηk)/H. The flat constraints give k²α=X+3J/(2k), ηk'=J/2, and k²(Phi-Psi)=Π. The factor for the full native dgpi is **one**, not 3/2. The 3/2 in the first-order hierarchy forecast converts only its massive-species S convention; do not multiply the native total Π by 3/2. The alternative 3/2-total column in the initial direct-reader output is a failed convention check, not a 26% shear failure.

For synchronous total conservation the energy equation is E'+HE+3H δp+kJ+(R+p)X=0; the momentum equation is J'+2HJ-kδp+2kΠ/3=0. Adding 3H/k times the latter gives the directly testable combination
    C = E'+3H J'/k + HE+kJ+(R+p)X+6H² J/k +2HΠ.
Thus the pressure perturbation need not be estimated to test this combination. Its vanishing alone is necessary but not sufficient for both conservation laws.

Differentiate the two algebraic gravity constraints WITHOUT assuming conservation:
    2H k² [α' + 2Hα - ηk/k + Π/k²]
      = C + 2k(ηk' - J/2) - [R+p+2H'-2H²] X.
With a as the integrating factor, integrate a² times the right side divided by 2H k² and separately include 2a²(a'/a-H)α. The sum must reproduce the endpoint change of a²α minus the accumulated shear drive. This permits a signed, independent diagnosis using native total density and current, rather than defining the conservation residual as whatever the shear readout is missing. Compare cubic and quintic interpolation with Gaussian quadrature; report accuracy on the actual small shear change, the ordinary code's own derivative and the native domain. A discrepancy in archived outputs of the retained solver is not evidence of a violation by the universe.
